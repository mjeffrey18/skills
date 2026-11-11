#!/usr/bin/env python3
"""Run one read-only review round with Claude Code, Codex or pi.

The implementer writes the round prompt to <packet>/prompt-<n>.md; this script
runs the reviewer with the hardened flags, validates the result and prints one
normalised JSON object. It never edits the repository.

    python3 review-round.py --reviewer claude --model opus \
        --repo /path/to/repo --packet /path/to/packet --round 1
    python3 review-round.py --reviewer codex --model astra \
        --repo /path/to/repo --packet /path/to/packet --round 2 --resume <id>
    python3 review-round.py --reviewer pi --model orchestrator \
        --repo /path/to/repo --packet /path/to/packet --round 1
    python3 review-round.py ... --read-dir /path/to/sibling/checkout
    python3 review-round.py --validate findings.json   # check a reply, run nothing
    python3 review-round.py --validate-verdict F1-1.json  # check one verifier reply
    python3 review-round.py --validate-same-failure F1-1.json  # check one same-failure reply
    python3 review-round.py --tally --expect 3 F1-1.json F1-2.json F1-3.json
"""

import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path
from typing import NoReturn

# The findings contract belongs to the review-critic skill, deployed alongside.
SCHEMA = Path(__file__).resolve().parents[2] / "review-critic" / "references" / "findings.schema.json"

# Only these models may review. Anything else is refused before a run starts.
MODELS = {
    "claude": {"opus": "opus", "fable": "fable"},
    "codex": {"sol": "gpt-6.1-sol", "astra": "gpt-6-astra"},
    # pi runs the user's local models through a model gateway: model:thinking.
    "pi": {
        "brain": "gateway/brain:max",
        "orchestrator": "gateway/orchestrator:high",
        "think": "gateway/think:xhigh",
        "code": "gateway/code:medium",
    },
}
PI_TOOLS = ["read", "grep", "find", "ls"]
PI_AGENT_DIR = Path.home() / ".pi" / "agent"
# The user's own gateway, as comma-separated base URLs in PI_REVIEW_BASE_URLS;
# a review must not be routed anywhere else. Unset refuses every pi review.
PI_ALLOWED_BASE_URLS = {u for u in os.environ.get("PI_REVIEW_BASE_URLS", "").split(",") if u}
PI_TIMEOUT = 3600  # local models at high thinking levels are slow
# GLM, denied bash, has written a tool call as plain text and ended the turn
# without a review. Say plainly which tools exist and what the reply must be.
PI_SYSTEM_NOTE = (
    "You are a read-only reviewer. Your only tools are read, grep, find and ls. "
    "There is no bash, edit, write or sub-agent tool: never write a tool call as "
    "text. When you have finished reading, reply with only the JSON object the "
    "prompt asks for."
)
# Claude and Codex review at this effort unless the user asks for another;
# pi routes carry their own fixed thinking level.
DEFAULT_EFFORT = "medium"
CLAUDE_MODEL_PREFIXES = ("claude-opus-", "claude-fable-")
# Claude Code runs background tasks on a small model; pin them to Opus too.
CLAUDE_HELPER_MODEL = "claude-opus-5-5"

# Variables that could switch billing, provider or model away from the
# user's subscription sign-in and the chosen model.
CLAUDE_UNSET = [
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_MODEL",
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_FABLE_MODEL",
    "CLAUDE_CODE_SUBAGENT_MODEL",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
]
CODEX_UNSET = ["CODEX_API_KEY", "OPENAI_API_KEY", "OPENAI_BASE_URL"]
# The only event items a read-only review may produce. Anything else - an MCP
# or connector call, web search, file change or sub-agent - fails the round.
CODEX_ALLOWED_ITEMS = {"agent_message", "reasoning", "command_execution", "todo_list"}

# Codex tools a reviewer must not have: sub-agents, connectors, plugins,
# browsers, computer use, image generation and goals.
CODEX_DISABLE = [
    "apps",
    "plugins",
    "multi_agent",
    "browser_use",
    "browser_use_external",
    "in_app_browser",
    "computer_use",
    "image_generation",
    "goals",
]


# Set once the round is known, so every failure can point at the raw logs.
STATE = {"packet": None, "round": None, "warnings": []}


def round_logs():
    if STATE["packet"] is None:
        return []
    return sorted(
        str(f)
        for f in STATE["packet"].glob(f"round-{STATE['round']}*")
        if f.suffix in (".jsonl", ".err") or f.name.endswith(".raw.json")
    )


def fail(msg, **extra) -> NoReturn:
    out = {"ok": False, "error": msg, **extra}
    if STATE["warnings"]:
        out["warnings"] = STATE["warnings"]
    if round_logs():
        out["logs"] = round_logs()
    print(json.dumps(out, indent=2))
    sys.exit(1)


def fail_reply(problem, reply, **base) -> NoReturn:
    """A reply that fails validation still holds the reviewer's work; keep it
    readable rather than leaving it buried in the raw log."""
    extra = {}
    if isinstance(reply, (dict, list)) and STATE["packet"] is not None:
        f = STATE["packet"] / f"round-{STATE['round']}.unvalidated.json"
        f.write_text(json.dumps(reply, indent=2))
        extra["unvalidated"] = str(f)
    fail(problem, **extra, **base)


def cli_version(reviewer, repo):
    """Record the installed reviewer CLI version."""
    try:
        p = subprocess.run([reviewer, "--version"], cwd=repo, capture_output=True, timeout=60, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired) as e:
        fail(f"cannot run `{reviewer} --version`: {e}")
    m = re.search(r"\d+\.\d+\.\d+", (p.stdout + p.stderr).decode(errors="replace"))
    version = m.group(0) if m else None
    return version


def clean_env(unset, extra=None):
    env = {k: v for k, v in os.environ.items() if k not in unset}
    env.update(extra or {})
    return env


def run(cmd, env, cwd, stdin_path=None, timeout=1800):
    handle = open(stdin_path, "rb") if stdin_path else None
    try:
        return subprocess.run(
            cmd, env=env, cwd=cwd, stdin=handle or subprocess.DEVNULL, capture_output=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        fail(f"reviewer timed out after {timeout}s: {cmd[0]}")
    finally:
        if handle:
            handle.close()


def validate_findings(data):
    """Full check against the findings schema, for reviewers that cannot
    enforce it themselves (pi)."""
    problem = check_shape(data)
    if problem:
        return problem
    top = {"verdict", "summary", "withdrawn", "findings"}
    if set(data) != top:
        return f"unexpected top-level keys {sorted(set(data) - top)}"
    if not isinstance(data["summary"], str) or not isinstance(data["findings"], list):
        return "summary must be a string and findings a list"
    if not isinstance(data["withdrawn"], list) or not all(isinstance(w, str) for w in data["withdrawn"]):
        return "withdrawn must be a list of finding ids"
    keys = {"id", "severity", "lens", "title", "location", "problem", "evidence", "fix", "status"}
    for i, f in enumerate(data["findings"]):
        if not isinstance(f, dict) or set(f) != keys:
            return f"finding {i} must have exactly the keys {sorted(keys)}"
        if not all(isinstance(f[k], str) for k in keys):
            return f"finding {i} has a non-string field"
        if f["severity"] not in ("high", "medium", "low"):
            return f"finding {i} has severity {f['severity']!r}"
        if f["status"] not in ("new", "still_open", "contested"):
            return f"finding {i} has status {f['status']!r}"
    return None


def sandbox_guard(reviewer):
    """The reviewer CLI needs the network and its own sign-in. Inside the
    implementer's sandbox (Codex marks commands with CODEX_SANDBOX) neither may
    be reachable, and the failure looks like a logged-out account. Say so."""
    if os.environ.get("CODEX_SANDBOX_NETWORK_DISABLED") == "1":
        fail(
            f"this round was started inside Codex's sandbox with the network off, "
            f"so the {reviewer} reviewer cannot sign in or reach its model. Run the "
            "round script outside the sandbox (approve the escalation when Codex "
            "asks), or give the session workspace-write with network access. The "
            "reviewer applies its own isolation either way."
        )


def sandbox_hint():
    return (
        " If this runs inside Codex's sandbox (CODEX_SANDBOX is set), the "
        "sign-in may simply be unreadable from there - run the round script "
        "outside the sandbox before asking the user to log in."
        if os.environ.get("CODEX_SANDBOX")
        else ""
    )


def check_shape(data):
    """Light validation; Claude and Codex enforce the schema themselves."""
    if not isinstance(data, dict):
        return "result is not a JSON object"
    for key in ("verdict", "summary", "withdrawn", "findings"):
        if key not in data:
            return f"result is missing {key!r}"
    if data["verdict"] not in ("approve", "changes_requested"):
        return f"unknown verdict {data['verdict']!r}"
    # The schema cannot say a withdrawn finding must not also be open.
    if isinstance(data["withdrawn"], list) and isinstance(data["findings"], list):
        both = set(w for w in data["withdrawn"] if isinstance(w, str)) & {
            f.get("id") for f in data["findings"] if isinstance(f, dict)
        }
        if both:
            return f"{sorted(both)} both withdrawn and returned as findings"
    return None


def claude_round(a, prompt, schema_text):
    sandbox_guard("Claude")
    env = clean_env(
        CLAUDE_UNSET,
        {
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": CLAUDE_HELPER_MODEL,
            "ANTHROPIC_SMALL_FAST_MODEL": CLAUDE_HELPER_MODEL,
        },
    )

    status = run(["claude", "--setting-sources", "", "auth", "status", "--json"], env, a.repo)
    try:
        auth = json.loads(status.stdout.decode() or "null")
    except json.JSONDecodeError:
        auth = None
    if not (
        status.returncode == 0
        and isinstance(auth, dict)
        and auth.get("loggedIn")
        and auth.get("authMethod") == "claude.ai"
        and auth.get("apiProvider") == "firstParty"
    ):
        fail(
            "Claude is not signed in with a claude.ai subscription "
            "(claude auth status must show loggedIn, authMethod claude.ai, "
            "apiProvider firstParty). Ask the user to run `claude` and log in." + sandbox_hint(),
            auth_status=status.stdout.decode()[:500],
        )

    cmd = [
        "claude",
        "-p",
        "--model",
        MODELS["claude"][a.model],
        "--setting-sources",
        "",  # no inherited allow rules, hooks, helpers
        "--permission-mode",
        "dontAsk",
        "--strict-mcp-config",  # no MCP servers
        "--tools",
        "Read,Grep,Glob",  # no Bash, Edit, Write or Agent
        "--add-dir",
        str(a.packet),
    ]
    for d in a.read_dir:
        cmd += ["--add-dir", str(d)]
    cmd += ["--json-schema", schema_text, "--output-format", "json"]
    cmd += ["--effort", a.effort or DEFAULT_EFFORT]
    if a.resume:
        cmd += ["--resume", a.resume]

    p = run(cmd, env, a.repo, prompt)
    raw = a.packet / f"round-{a.round}.raw.json"
    raw.write_bytes(p.stdout)
    (a.packet / f"round-{a.round}.err").write_bytes(p.stderr)
    try:
        d = json.loads(p.stdout.decode())
    except json.JSONDecodeError:
        fail(f"claude exited {p.returncode} without JSON output", stderr=p.stderr.decode()[-1000:])

    models = sorted(d.get("modelUsage") or {})
    base = {
        "reviewer": "claude",
        "model": a.model,
        "models_used": models,
        "model_pinned": MODELS["claude"][a.model],
        "session_id": d.get("session_id"),
        "denials": d.get("permission_denials") or [],
    }
    if p.returncode != 0 or d.get("is_error") or d.get("subtype") != "success":
        fail(f"claude run failed: subtype={d.get('subtype')} exit={p.returncode}", **base)
    lower = [m for m in models if not m.startswith(CLAUDE_MODEL_PREFIXES)]
    if lower or not models:
        fail(f"review used a model outside Opus/Fable: {lower or 'none reported'}", **base)
    out = d.get("structured_output")
    problem = check_shape(out)
    if problem or out is None:
        fail_reply(problem or "reply is not JSON", out, **base)
    return {**base, **out}


def codex_user_mcp_names():
    """Names in the user's config.toml (not a credential file)."""
    import tomllib

    home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    f = home / "config.toml"
    if not f.is_file():
        return set()
    try:
        return set(tomllib.loads(f.read_text()).get("mcp_servers", {}))
    except tomllib.TOMLDecodeError as e:
        fail(f"cannot parse {f}: {e}")


def codex_doctor_check(repo, known_mcp):
    """Fail closed unless the signed-in, cloud-policy-aware view is first-party.

    `codex doctor` loads the invocation config including cloud-managed policy,
    so it sees what an organisation account could push. Require the OpenAI
    provider, no managed proxy, chatgpt.com endpoints, and no MCP servers the
    script cannot name (and therefore cannot disable).
    """
    env = clean_env(CODEX_UNSET)
    p = run(
        ["codex", "doctor", "--json", "-c", 'model_provider="openai"', "-c", 'forced_login_method="chatgpt"'],
        env,
        repo,
        timeout=180,
    )
    try:
        checks = json.loads(p.stdout.decode())["checks"]
        provider = checks["config.load"]["details"]["model provider"]
        proxy = checks["network.env"]["details"]["managed proxy"]
        reach = checks["network.provider_reachability"]["details"]
        inference = reach["ChatGPT inference URL"]
        websocket = checks["network.websocket_reachability"]["details"]["endpoint"]
        configured = int(checks["mcp.config"]["details"]["configured servers"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        fail(f"cannot verify Codex provider and MCP isolation from `codex doctor`: {e!r}")
    problems = []
    if provider != "openai":
        problems.append(f"model provider is {provider!r}")
    if proxy != "not configured":
        problems.append(f"a managed proxy is configured ({proxy})")
    if not inference.startswith("https://chatgpt.com/"):
        problems.append(f"inference endpoint is {inference.split()[0]}")
    if not websocket.startswith("wss://chatgpt.com/"):
        problems.append(f"websocket endpoint is {websocket}")
    if configured > len(known_mcp):
        problems.append(
            f"{configured} MCP servers configured but only {len(known_mcp)} "
            "can be named and disabled (cloud-managed policy?)"
        )
    if problems:
        fail("Codex reviewer isolation cannot be established: " + "; ".join(problems))


def codex_disabled_mcp(repo):
    """Disable MCP servers from config layers --ignore-user-config keeps.

    `codex mcp list` with an empty CODEX_HOME reports the servers that the
    system, managed and project layers would add. The two known files are
    also parsed directly. Any failure stops the round rather than risk a
    reviewer with MCP tools.
    """
    import tempfile
    import tomllib

    names = set()
    with tempfile.TemporaryDirectory() as home:
        env = clean_env(CODEX_UNSET, {"CODEX_HOME": home})
        p = run(["codex", "mcp", "list", "--json"], env, repo, timeout=120)
        try:
            listed = json.loads(p.stdout.decode())
        except json.JSONDecodeError:
            listed = None
        if p.returncode != 0 or not isinstance(listed, list):
            fail("cannot list Codex MCP servers to disable them", stderr=p.stderr.decode()[-500:])
        names.update(s["name"] for s in listed if isinstance(s, dict) and s.get("name"))
    for f in (Path("/etc/codex/config.toml"), repo / ".codex" / "config.toml"):
        if f.is_file():
            try:
                names.update(tomllib.loads(f.read_text()).get("mcp_servers", {}))
            except tomllib.TOMLDecodeError as e:
                fail(f"cannot parse {f} to disable its MCP servers: {e}")
    codex_doctor_check(repo, names | codex_user_mcp_names())
    overrides = []
    for name in sorted(names):
        overrides += ["-c", f"mcp_servers.{name}.enabled=false"]
    return overrides


def codex_round(a, prompt, schema_text):
    env = clean_env(CODEX_UNSET)
    status = run(["codex", "login", "status"], env, a.repo)
    text = (status.stdout + status.stderr).decode()
    if status.returncode != 0 or "ChatGPT" not in text:
        fail(
            "Codex is not signed in with ChatGPT (`codex login status`). " "Ask the user to run `codex login`.",
            login_status=text[:500],
        )

    slug = MODELS["codex"][a.model]
    last = a.packet / f"round-{a.round}.raw.json"
    cmd = ["codex", "exec", "-C", str(a.repo), "--ignore-user-config"]
    for feature in CODEX_DISABLE:
        cmd += ["--disable", feature]
    cmd += [
        "-c",
        'web_search="disabled"',
        "-c",
        "agents.enabled=false",
        # First-party provider and ChatGPT sign-in, whatever other
        # config layers select.
        "-c",
        'model_provider="openai"',
        "-c",
        'forced_login_method="chatgpt"',
    ]
    cmd += codex_disabled_mcp(a.repo)
    cmd += ["-m", slug, "-c", f'review_model="{slug}"']
    cmd += ["-c", f'model_reasoning_effort="{a.effort or DEFAULT_EFFORT}"']
    cmd += [
        "--sandbox",
        "read-only",
        "-c",
        'approval_policy="never"',
        "--output-schema",
        str(SCHEMA),
        "--json",
        "-o",
        str(last),
    ]
    if a.resume:
        cmd += ["resume", a.resume]
    cmd += ["-"]

    if last.exists():
        last.unlink()
    p = run(cmd, env, a.repo, prompt)
    (a.packet / f"round-{a.round}.jsonl").write_bytes(p.stdout)
    (a.packet / f"round-{a.round}.err").write_bytes(p.stderr)

    thread, errors, stray = a.resume, [], set()
    for line in p.stdout.decode().splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "thread.started":
            thread = e.get("thread_id")
        if e.get("type") in ("turn.failed", "error"):
            errors.append(e)
        item = e.get("item") or {}
        if item.get("type") and item["type"] not in CODEX_ALLOWED_ITEMS:
            stray.add(item["type"])
    # Codex does not report the serving model; this is the pinned request.
    base = {
        "reviewer": "codex",
        "model": a.model,
        "models_used": [],
        "model_pinned": slug,
        "session_id": thread,
        "denials": [],
    }
    if stray:
        fail(f"codex reviewer used tools outside a read-only review: {sorted(stray)}", **base)
    if p.returncode != 0 or errors or not last.exists():
        fail(f"codex run failed: exit={p.returncode}", errors=errors[:3], stderr=p.stderr.decode()[-1000:], **base)
    try:
        out = json.loads(last.read_text())
    except json.JSONDecodeError:
        fail("codex final message is not JSON", **base)
    problem = check_shape(out)
    if problem or out is None:
        fail_reply(problem or "reply is not JSON", out, **base)
    return {**base, **out}


def extract_json(text):
    """The last fenced JSON block, else the outermost braces."""
    candidates = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)[::-1]
    if "{" in text:
        candidates.append(text[text.find("{") : text.rfind("}") + 1])
    for c in candidates:
        try:
            return json.loads(c)
        except json.JSONDecodeError:
            continue
    return None


def pi_call(a, sessions, sid, message, tag):
    model, thinking = MODELS["pi"][a.model].rsplit(":", 1)
    cmd = [
        "pi",
        "-p",
        "--mode",
        "json",
        "--model",
        model,
        "--thinking",
        thinking,
        "--tools",
        ",".join(PI_TOOLS),  # applies to extension tools too
        "--no-extensions",
        "--no-skills",
        "--no-prompt-templates",
        "--no-themes",
        "--no-approve",  # ignore project-local pi files
        "--no-mcp",  # --tools keeps MCP tools since pi 1.0.4
        "--no-context-files",  # the prompt names the standards
        "--append-system-prompt",
        PI_SYSTEM_NOTE,
        "--session-dir",
        str(sessions),
        "--session-id",
        sid,
        "--",
        message,
    ]  # an argument, not @file: pi treats
    # file contents as untrusted data
    env = clean_env(["PI_CODING_AGENT_DIR"])  # use the default config, checked below
    p = run(cmd, env, a.repo, timeout=PI_TIMEOUT)  # stdin closed
    (a.packet / f"round-{a.round}{tag}.jsonl").write_bytes(p.stdout)
    (a.packet / f"round-{a.round}{tag}.err").write_bytes(p.stderr)
    events = []
    for line in p.stdout.decode(errors="replace").splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    ends = [e for e in events if e.get("type") == "agent_end"]
    if p.returncode != 0 or not ends:
        fail(f"pi run failed: exit={p.returncode}", stderr=p.stderr.decode()[-1000:], reviewer="pi", session_id=sid)
    msgs = [m for m in ends[-1].get("messages", []) if m.get("role") == "assistant"]
    if not msgs:
        fail("pi returned no assistant message", reviewer="pi", session_id=sid)
    return model, msgs


def pi_check_routing(route):
    """The chosen route must resolve to the user's gateway. pi takes a
    model's own baseUrl before the provider's, so check both; route labels
    alone do not prove where traffic goes."""
    provider, model_id = route.split("/", 1)
    f = PI_AGENT_DIR / "models.json"
    try:
        conf = json.loads(f.read_text())["providers"][provider]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as e:
        fail(f"cannot read the {provider} provider from {f}: {e!r}")
    models = [m for m in conf.get("models", []) if isinstance(m, dict) and m.get("id") == model_id]
    if len(models) != 1:
        fail(f"{f} must define exactly one {provider} model with id {model_id!r}")
    base = models[0].get("baseUrl") or conf.get("baseUrl")
    allowed = {u.rstrip("/") for u in PI_ALLOWED_BASE_URLS}
    if not isinstance(base, str) or base.rstrip("/") not in allowed:
        fail(f"pi route {route} resolves to {base}, not the user's gateway " f"({sorted(PI_ALLOWED_BASE_URLS)})")


def pi_round(a, prompt, schema_text):
    sandbox_guard("pi")
    pi_check_routing(MODELS["pi"][a.model].rsplit(":", 1)[0])
    sessions = a.packet / "pi-sessions"
    sessions.mkdir(exist_ok=True)
    if a.resume:
        sid = a.resume
        if not any(sid in f.name for f in sessions.glob("*.jsonl")):
            fail(f"no pi session {sid} in {sessions} to resume")
    else:
        sid = str(uuid.uuid4())

    # pi cannot enforce a schema, so the prompt carries it and the script
    # validates the reply, allowing one repair turn.
    message = (
        prompt.read_text() + "\n\n## Reply format\n\nReply with only a JSON "
        "object matching this JSON Schema - no other text, no code fence:\n\n" + schema_text
    )
    model, msgs = pi_call(a, sessions, sid, message, "")

    def check(msgs):
        """Return (models used, parsed reply, problem, repairable)."""
        used = sorted({f"{m.get('provider')}/{m.get('model')}" for m in msgs})
        if used != [model]:
            return used, None, f"review used {used}, expected only {model}", False
        tools = {
            c.get("name")
            for m in msgs
            for c in m.get("content", [])
            if isinstance(c, dict) and c.get("type") == "toolCall"
        }
        if tools - set(PI_TOOLS):
            return used, None, f"pi used tools outside the allowlist: {sorted(map(str, tools - set(PI_TOOLS)))}", False
        if msgs[-1].get("stopReason") != "stop":
            return used, None, f"pi stopped with {msgs[-1].get('stopReason')!r}", False
        text = "".join(
            c.get("text", "") for c in msgs[-1].get("content", []) if isinstance(c, dict) and c.get("type") == "text"
        )
        out = extract_json(text)
        # Every round-1 finding is new; GLM has dropped the field after a
        # long review, which would otherwise fail the whole round.
        if a.round == 1 and isinstance(out, dict) and isinstance(out.get("findings"), list):
            for f in out["findings"]:
                if isinstance(f, dict):
                    f.setdefault("status", "new")
        problem = validate_findings(out) if out is not None else "reply is not JSON"
        return used, out, problem, True

    used, out, problem, repairable = check(msgs)
    if problem and repairable:
        _, msgs = pi_call(
            a,
            sessions,
            sid,
            "Your last reply did not match the required format "
            f"({problem}). Do not call any tool. Reply again with only the "
            "JSON object for your review - no other text, no code fence. "
            "Top-level keys: verdict (approve or changes_requested), summary, "
            "withdrawn (list of finding ids), findings. Every finding has "
            "exactly these string keys: id, severity (high, medium or low), "
            "lens, title, location, problem, evidence, fix, status (new, "
            "still_open or contested).",
            "-repair",
        )
        used, out, problem, _ = check(msgs)
    base = {
        "reviewer": "pi",
        "model": a.model,
        "models_used": used,
        "model_pinned": MODELS["pi"][a.model],
        "session_id": sid,
        "denials": [],
    }
    if problem or out is None:
        fail_reply(problem or "reply is not JSON", out, **base)
    return {**base, **out}


def validate_file(path):
    """--validate: check a findings reply (JSON, or text containing it) from
    any reviewer against the schema rules, without running anything."""
    try:
        text = Path(path).read_text()
    except OSError as e:
        fail(f"cannot read {path}: {e}")
    out = extract_json(text)
    problem = validate_findings(out) if out is not None else "reply is not JSON"
    if problem or out is None:
        fail(problem or "reply is not JSON")
    print(json.dumps({"ok": True, "error": None, **out}, indent=2))


VERDICTS = ("confirmed", "refuted", "unverifiable")
# review-critic's fixed rule classes and the verifier's `protected` judgement (review-critic, verifier.md).
RULE_CLASSES = (
    "auth",
    "injection",
    "secrets",
    "data-exposure",
    "input-validation",
    "error-handling",
    "race",
    "idempotency",
    "migration",
    "resource-leak",
    "edge-case",
    "spec-gap",
    "test-gap",
    "convention",
    "docs",
    "other",
)
PROTECTED = ("no", "unsure", "security", "migration", "idempotency", "concurrency")
SAME_FAILURE = ("yes", "no", "unsure")


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate_verdict(data):
    """One verifier reply: {id, result, evidence}, plus the `call` the implementer adds when saving it, and the
    optional finding metadata - `fingerprint`, `protected` and `style`. A reply without the metadata stays valid,
    so reviews outside GSD are unchanged; it simply never makes a finding suppressible (see tally)."""
    if not isinstance(data, dict):
        return "verdict must be a JSON object"
    extra = set(data) - {"id", "result", "evidence", "call", "fingerprint", "protected", "style"}
    if extra:
        return f"unexpected verdict keys {sorted(extra)}"
    for key in ("id", "result", "evidence"):
        if not nonempty(data.get(key)):
            return f"verdict {key} must be a non-empty string"
    if data["result"] not in VERDICTS:
        return f"verdict result {data['result']!r} is not one of {list(VERDICTS)}"
    if "call" in data and not nonempty(data["call"]):
        return "verdict call must be a non-empty string"
    if "fingerprint" in data:
        fp = data["fingerprint"]
        if not isinstance(fp, dict) or set(fp) != {"path", "symbol", "rule_class"}:
            return "verdict fingerprint must be an object with exactly path, symbol and rule_class"
        if not all(nonempty(fp[key]) for key in fp):
            return "verdict fingerprint path, symbol and rule_class must be non-empty strings"
        if fp["rule_class"] not in RULE_CLASSES:
            return f"verdict fingerprint rule_class {fp['rule_class']!r} is not one of {list(RULE_CLASSES)}"
    if "protected" in data and data["protected"] not in PROTECTED:
        return f"verdict protected {data['protected']!r} is not one of {list(PROTECTED)}"
    if "style" in data and not isinstance(data["style"], bool):
        return "verdict style must be true or false"
    return None


def validate_same_failure(data):
    """One same-failure reply: {id, earlier, same_failure, reason}, plus the `call` added when saving it."""
    if not isinstance(data, dict):
        return "same-failure reply must be a JSON object"
    extra = set(data) - {"id", "earlier", "same_failure", "reason", "call"}
    if extra:
        return f"unexpected same-failure keys {sorted(extra)}"
    for key in ("id", "earlier", "same_failure", "reason"):
        if not nonempty(data.get(key)):
            return f"same-failure {key} must be a non-empty string"
    if data["same_failure"] not in SAME_FAILURE:
        return f"same_failure {data['same_failure']!r} is not one of {list(SAME_FAILURE)}"
    if "call" in data and not nonempty(data["call"]):
        return "same-failure call must be a non-empty string"
    return None


def validate_reply_file(path, check):
    """--validate-verdict and --validate-same-failure: check one saved reply, without running anything."""
    try:
        out = extract_json(Path(path).read_text())
    except OSError as e:
        fail(f"cannot read {path}: {e}")
    problem = check(out) if out is not None else "reply is not JSON"
    if problem or out is None:
        fail(problem or "reply is not JSON")
    print(json.dumps({"ok": True, "error": None, **out}, indent=2))


def fingerprint_text(fp):
    return f"{fp['path']}#{fp['symbol']}:{fp['rule_class']}" if fp else None


def metadata(data):
    return {
        "fingerprint": fingerprint_text(data.get("fingerprint")),
        "protected": data.get("protected"),
        "style": data.get("style"),
    }


def suppression(result, verifiers, ignored, expect):
    """(metadata_agreed, suppressible, reasons). A filter may drop a finding only when every confirming verifier
    gives the same fingerprint and style, and every one of the `expect` distinct verifiers - whatever its vote -
    says `protected: no`. A missing, invalid, conflicting or duplicate reply cannot say no, so it blocks
    suppression too."""
    reasons = []
    confirming = [v for v in verifiers if v["result"] == "confirmed"]
    if not confirming:
        reasons.append("no confirming verifier")
    for key in ("fingerprint", "style"):
        values = {v[key] for v in confirming}
        if None in values:
            reasons.append(f"a confirming verifier gave no {key}")
        elif len(values) > 1:
            reasons.append(f"confirming verifiers differ on {key}")
    agreed = not reasons
    if result != "confirmed":
        reasons.append(f"the result is {result}")
    not_no = sorted({str(v["protected"]) for v in verifiers if v["protected"] != "no"})
    if not_no:
        reasons.append("protected is not no from every reply: " + ", ".join(not_no))
    if ignored:
        reasons.append("a reply was missing, invalid or conflicting, so it cannot say protected: no")
    if len(verifiers) < expect:
        reasons.append(
            f"only {len(verifiers)} of {expect} expected verifiers replied, so the others cannot say " "protected: no"
        )
    return agreed, not reasons, reasons


def tally(paths, expect):
    """Combine the saved replies for one finding. Each distinct `call` gives at most one vote, so a copied
    reply cannot make a majority; a missing, invalid or call-less reply gives none. One expected verifier:
    its vote is the result. Three: a result needs votes from two distinct calls. Anything else is unverifiable.
    It also reports each counted verifier's fingerprint, `protected` and `style`, whatever its vote, and whether
    the finding may be suppressed by a filter; the vote result does not depend on them."""
    ids, by_call, ignored = set(), {}, []
    for path in paths:
        try:
            data = extract_json(Path(path).read_text())
        except OSError:
            data = None
        problem = validate_verdict(data) if data is not None else "missing or not JSON"
        if not problem and data is not None and "call" not in data:
            problem = "no call id, so it cannot count as a distinct verifier"
        if problem or data is None:
            ignored.append({"file": str(path), "reason": problem})
            continue
        ids.add(data["id"])
        by_call.setdefault(data["call"], []).append(data)
    votes, verifiers = {}, []
    for call, replies in by_call.items():
        results = {r["result"] for r in replies}
        if len(results) > 1:
            ignored.append({"call": call, "reason": "one call gave conflicting results"})
            continue
        votes[call] = results.pop()
        metas = [metadata(r) for r in replies]
        if any(m != metas[0] for m in metas):
            ignored.append({"call": call, "reason": "one call gave conflicting metadata"})
            metas = [{"fingerprint": None, "protected": None, "style": None}]
        verifiers.append({"call": call, "result": votes[call], **metas[0]})
    if len(ids) > 1:
        ignored = ignored + [{"reason": "replies name different findings"}]
        _, _, reasons = suppression("unverifiable", verifiers, ignored, expect)
        return {
            "id": sorted(ids),
            "result": "unverifiable",
            "votes": votes,
            "expected": expect,
            "ignored": ignored,
            "verifiers": verifiers,
            "metadata_agreed": False,
            "suppressible": False,
            "suppression_blocked": reasons,
        }
    need = 1 if expect == 1 else 2
    counts = {v: list(votes.values()).count(v) for v in VERDICTS}
    winners = [v for v in VERDICTS if counts[v] >= need]
    result = winners[0] if len(winners) == 1 else "unverifiable"
    agreed, suppressible, reasons = suppression(result, verifiers, ignored, expect)
    out = {
        "id": ids.pop() if ids else None,
        "result": result,
        "votes": votes,
        "expected": expect,
        "ignored": ignored,
        "verifiers": verifiers,
        "metadata_agreed": agreed,
        "suppressible": suppressible,
        "suppression_blocked": reasons,
    }
    if agreed:
        confirming = next(v for v in verifiers if v["result"] == "confirmed")
        out.update(fingerprint=confirming["fingerprint"], style=confirming["style"])
    return out


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--validate":
        return validate_file(sys.argv[2])
    if len(sys.argv) == 3 and sys.argv[1] == "--validate-verdict":
        return validate_reply_file(sys.argv[2], validate_verdict)
    if len(sys.argv) == 3 and sys.argv[1] == "--validate-same-failure":
        return validate_reply_file(sys.argv[2], validate_same_failure)
    if len(sys.argv) >= 5 and sys.argv[1:3] == ["--tally", "--expect"]:
        if sys.argv[3] not in ("1", "3"):
            fail("--expect must be 1 or 3")
        print(json.dumps({"ok": True, "error": None, **tally(sys.argv[4:], int(sys.argv[3]))}, indent=2))
        return
    ap = argparse.ArgumentParser(description=(__doc__ or "Run one review round.").splitlines()[0])
    ap.add_argument("--reviewer", required=True, choices=sorted(MODELS))
    ap.add_argument("--model", required=True)
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--packet", required=True, type=Path)
    ap.add_argument("--round", required=True, type=int)
    ap.add_argument("--resume")
    ap.add_argument("--kind", choices=["code", "plan"], default="code")
    ap.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument(
        "--read-dir",
        action="append",
        default=[],
        type=Path,
        help="extra directory the reviewer may read, such as a sibling " "checkout; repeatable",
    )
    a = ap.parse_args()

    if a.model not in MODELS[a.reviewer]:
        fail(f"{a.model!r} is not allowed for {a.reviewer} reviews; " f"use one of {sorted(MODELS[a.reviewer])}")
    if not 1 <= a.round <= 3:
        fail("round must be 1, 2 or 3")
    if a.reviewer == "pi" and a.effort:
        fail("pi routes have fixed thinking levels; choose another route instead of --effort")
    if a.round > 1 and not a.resume:
        fail("rounds after the first must --resume the reviewer's session")
    a.repo, a.packet = a.repo.resolve(), a.packet.resolve()
    a.read_dir = [d.resolve() for d in a.read_dir]
    for d in a.read_dir:
        if not d.is_dir():
            fail(f"--read-dir {d} is not a directory")
    if a.packet == a.repo or a.repo in a.packet.parents:
        fail("the packet directory must be outside the repository")
    prompt = a.packet / f"prompt-{a.round}.md"
    if not prompt.is_file():
        fail(f"missing {prompt}")
    scope = a.packet / "scope.diff"
    if a.kind == "code" and (not scope.is_file() or scope.stat().st_size == 0):
        fail(f"{scope} is missing or empty - check the paths used to build it")
    fixes = a.packet / f"fixes-{a.round}.diff"
    if a.round > 1 and not fixes.is_file():
        fail(f"missing {fixes} (write it even if empty, when nothing was fixed)")

    if not SCHEMA.is_file():
        fail(f"missing {SCHEMA} - install the review-critic skill next to this one")
    schema_text = SCHEMA.read_text()
    STATE["packet"], STATE["round"] = a.packet, a.round
    version = cli_version(a.reviewer, a.repo)
    rounds = {"claude": claude_round, "codex": codex_round, "pi": pi_round}
    result = rounds[a.reviewer](a, prompt, schema_text)
    result = {
        "ok": True,
        "error": None,
        "round": a.round,
        **result,
        "cli_version": version,
        "warnings": STATE["warnings"],
    }
    (a.packet / f"round-{a.round}.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
