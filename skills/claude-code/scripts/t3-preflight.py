#!/usr/bin/env python3
"""Check that a T3 Code Claude child would run on the subscription with Opus or Fable helpers.

The provider instance may set only the two helper-model pins. Anything else
could point the child at a configuration this check cannot see, so the
caller's own `claude auth status` would no longer describe the child.

Prints one JSON object and exits non-zero when the T3 path must not be used.
It prints variable names only, never values, except the two helper-model pins.
"""

import json
import os
import pathlib
import subprocess
import sys

HELPER_PINS = ("ANTHROPIC_DEFAULT_HAIKU_MODEL", "ANTHROPIC_SMALL_FAST_MODEL")
ALLOWED_MODEL_PREFIXES = ("claude-opus-", "claude-fable-")
FORBIDDEN = {
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CONFIG_DIR",
    "CLAUDE_CODE_SUBAGENT_MODEL",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
}


def instance_environment(t3_home, instance):
    settings = json.loads((t3_home / "userdata" / "settings.json").read_text())
    entry = settings.get("providerInstances", {}).get(instance, {})
    return {e["name"]: e.get("value") for e in entry.get("environment") or [] if "name" in e}


def user_settings():
    path = pathlib.Path.home() / ".claude" / "settings.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text())


def auth_status(env):
    try:
        p = subprocess.run(
            ["claude", "auth", "status", "--json"],
            capture_output=True,
            text=True,
            timeout=60,
            stdin=subprocess.DEVNULL,
            env={**os.environ, **env},
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"cannot run `claude auth status`: {e}"
    if p.returncode != 0:
        return None, f"`claude auth status` exited {p.returncode}"
    try:
        return json.loads(p.stdout), None
    except json.JSONDecodeError:
        return None, "`claude auth status` returned no JSON"


def main():
    instance = sys.argv[1] if len(sys.argv) > 1 else "claudeAgent"
    t3_home = pathlib.Path(os.environ.get("T3CODE_HOME") or pathlib.Path.home() / ".t3")
    problems = []

    try:
        env = instance_environment(t3_home, instance)
    except (OSError, json.JSONDecodeError) as e:
        env = {}
        problems.append(f"cannot read T3 Code settings: {e}")

    for name in HELPER_PINS:
        value = env.get(name) or ""
        if not value.startswith(ALLOWED_MODEL_PREFIXES):
            problems.append(f"T3 provider instance '{instance}' does not pin {name} to an Opus or Fable model")

    for name in sorted(set(env) - set(HELPER_PINS)):
        problems.append(f"T3 provider instance '{instance}' sets {name}; only the helper-model pins are allowed")

    try:
        settings = user_settings()
    except (OSError, json.JSONDecodeError) as e:
        settings = {}
        problems.append(f"cannot read ~/.claude/settings.json: {e}")
    if "apiKeyHelper" in settings:
        problems.append("~/.claude/settings.json defines apiKeyHelper")

    for source, names in (
        ("~/.claude/settings.json env", settings.get("env") or {}),
        ("this process's environment", os.environ),
    ):
        for name in sorted(FORBIDDEN & set(names)):
            problems.append(f"{source} sets {name}")

    status, error = auth_status(env)
    if error or status is None:
        problems.append(error or "cannot read Claude auth status")
    elif not (
        status.get("loggedIn") is True
        and status.get("authMethod") == "claude.ai"
        and status.get("apiProvider") == "firstParty"
    ):
        problems.append("Claude is not signed in with a claude.ai subscription (first party)")

    print(
        json.dumps(
            {
                "ok": not problems,
                "instance": instance,
                "helper_models": {name: env.get(name) for name in HELPER_PINS},
                "problems": problems,
            },
            indent=2,
        )
    )
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
