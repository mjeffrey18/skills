#!/usr/bin/env python3
"""Chained, agent-neutral handoff documents for coding agents.

Handoffs live beside the work they describe:

- the active GSD item, as .agents/gsd/<item>/handoffs/, when one can be
  identified from IDEA.md front matter and the current branch;
- otherwise .agents/handoffs/ at the repository root.

Each handoff links to its predecessor (continues_from), so a resuming agent can
walk the chain back. Harness hooks call the `hook` subcommand: pre-compact
writes a draft checkpoint from git and GSD state, post-compact asks the agent
to complete it from its fresh summary, and session-start points at the latest
handoff.

Usage:
    handoff.py locate
    handoff.py new [slug] [--title T] [--continues-from FILE] [--harness H]
    handoff.py list
    handoff.py validate FILE
    handoff.py status FILE
    handoff.py hook {pre-compact,post-compact,session-start} --harness H
        [--cwd DIR] [--session ID] [--trigger T] [--source S]

Standard library only, so it runs unchanged on macOS and Linux.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

TODO_MARK = "TODO:"
SECTIONS = [
    "Current state",
    "Work item",
    "Work completed",
    "Decisions made",
    "Immediate next steps",
    "Blockers and open questions",
    "Important context",
    "Critical files",
    "Suggested skills",
    "Environment state",
    "Chain",
]
# Every section must be present and filled; "None" is an explicit answer for all but these.
NEVER_NONE = ["Current state", "Immediate next steps"]
RESUME_NUDGE_MAX_DAYS = 7
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-./+]{12,}"),
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


# --- git -------------------------------------------------------------------


def git(cwd, *args):
    try:
        result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def repo_root(cwd):
    root = git(cwd, "rev-parse", "--show-toplevel")
    return Path(root) if root else None


def git_state(root):
    status = git(root, "status", "--porcelain") or ""
    return {
        "branch": git(root, "branch", "--show-current") or "(detached)",
        "commit": git(root, "rev-parse", "--short", "HEAD") or "(no commits)",
        "commits": (git(root, "log", "--oneline", "-5", "--no-decorate") or "").splitlines(),
        "dirty": [line for line in status.splitlines() if line.strip()],
    }


# --- front matter ----------------------------------------------------------


def split_front_matter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    return parse_front_matter(text[4:end]), text[end + 4 :].lstrip("\n")


def parse_front_matter(block):
    """A small YAML subset: scalars, inline [] lists and block '- ' lists."""
    data, key = {}, None
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key:
            if not isinstance(data.get(key), list):
                data[key] = []
            data[key].append(item.group(1).strip().strip("'\""))
            continue
        pair = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not pair:
            continue
        key, value = pair.group(1), pair.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [v.strip().strip("'\"") for v in inner.split(",")] if inner else []
        else:
            data[key] = value.strip("'\"")
    return data


def render_front_matter(meta):
    lines = ["---"]
    for key, value in meta.items():
        text = "" if value is None else str(value)
        if text and (text[0] in "[{&*!|>%@`'\"#" or ": " in text or text.endswith(":")):
            text = json.dumps(text)
        lines.append(f"{key}: {text}".rstrip())
    lines.append("---")
    return "\n".join(lines)


def read_handoff(path):
    meta, body = split_front_matter(path.read_text(encoding="utf-8"))
    return meta, body


def write_handoff(path, meta, body):
    path.write_text(render_front_matter(meta) + "\n\n" + body.rstrip() + "\n", encoding="utf-8")


# --- location --------------------------------------------------------------


def active_gsd_items(root):
    items = []
    for idea in sorted((root / ".agents" / "gsd").glob("*/IDEA.md")):
        meta, _ = split_front_matter(idea.read_text(encoding="utf-8"))
        if meta.get("stage") == "complete" or meta.get("delivery") == "cancelled":
            continue
        branches = meta.get("branches") or []
        items.append(
            {
                "dir": idea.parent,
                "slug": meta.get("slug") or idea.parent.name,
                "branches": branches if isinstance(branches, list) else [branches],
            }
        )
    return items


def default_branch(root):
    head = git(root, "symbolic-ref", "--short", "refs/remotes/origin/HEAD") or ""
    return head.split("/", 1)[-1] if head else ""


def handoff_dirs(root):
    """Every place a handoff can live: each GSD item's handoffs/ and .agents/handoffs/."""
    dirs = sorted((root / ".agents" / "gsd").glob("*/handoffs"))
    return dirs + [root / ".agents" / "handoffs"]


def session_dir(root, session):
    """The directory already holding a handoff from this session, so its chain stays together."""
    if not session:
        return None
    for directory in handoff_dirs(root):
        for path in reversed(list_handoffs(directory)):
            if read_handoff(path)[0].get("session") == session:
                return directory
    return None


def locate(root, gsd_item=None, session=""):
    """Return (handoff dir, GSD item slug or None, note).

    An explicit item wins, then the directory this session already uses, then the one active
    item listing the current branch - unless that branch is the default one, which many
    unrelated workstreams share, so it never identifies an item by itself.
    """
    gsd_root = root / ".agents" / "gsd"
    if gsd_item:
        if not (gsd_root / gsd_item / "IDEA.md").exists():
            raise SystemExit(f"GSD item not found: {gsd_item}")
        return gsd_root / gsd_item / "handoffs", gsd_item, ""
    directory = session_dir(root, session)
    if directory:
        slug = directory.parent.name if directory.parent.parent == gsd_root else None
        return directory, slug, ""
    items = active_gsd_items(root)
    branch = git(root, "branch", "--show-current") or ""
    shared = branch in ("main", "master", default_branch(root))
    on_branch = [] if shared else [i for i in items if branch and branch in i["branches"]]
    if len(on_branch) == 1:
        item = on_branch[0]
        return item["dir"] / "handoffs", item["slug"], ""
    note = ""
    if len(on_branch) > 1:
        note = (
            "Several active GSD items match (" + ", ".join(i["slug"] for i in on_branch) + "); using .agents/handoffs/."
        )
    elif shared and items:
        note = (
            f"On the shared branch {branch}, a GSD item is not assumed; pass --gsd-item <slug> to file "
            "under one (active: " + ", ".join(i["slug"] for i in items) + ")."
        )
    return root / ".agents" / "handoffs", None, note


def list_handoffs(directory):
    if not directory.is_dir():
        return []
    return sorted(p for p in directory.glob("*.md") if re.match(r"\d{4}-\d{2}-\d{2}-\d{6}", p.name))


def latest_handoff(directory):
    handoffs = list_handoffs(directory)
    return handoffs[-1] if handoffs else None


# --- scaffold --------------------------------------------------------------


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "handoff"


def scaffold_body(title, root, state, gsd_slug, previous):
    item_line = (
        f"GSD item `{gsd_slug}` - IDEA.md, DECISIONS.md, TODO.md and FACTS.md in the parent folder are "
        "authoritative. Link to them here rather than restating them."
        if gsd_slug
        else "No GSD item. This handoff is the only record, so be complete."
    )
    commits = "\n".join(f"- {c}" for c in state["commits"]) or "- (none)"
    dirty = "\n".join(f"- `{d}`" for d in state["dirty"][:40]) or "- (clean)"
    if len(state["dirty"]) > 40:
        dirty += f"\n- ... and {len(state['dirty']) - 40} more"
    chain = f"Continues from [{previous.name}]({previous.name})." if previous else "Start of chain."
    return f"""# Handoff: {title}

## Current state

{TODO_MARK} One paragraph - what is being worked on, how far it got and exactly where it stopped.

## Work item

{item_line}

## Work completed

{TODO_MARK} What this session finished, as bullets. Reference commits or files; do not paste diffs. Write "None" if nothing was finished.

## Decisions made

{TODO_MARK} Decisions with their rationale and the options rejected. For a GSD item, record them in DECISIONS.md and link here. Write "None" if there were none.

## Immediate next steps

{TODO_MARK} Numbered, concrete actions. Step 1 is what the next agent does first.

## Blockers and open questions

{TODO_MARK} Anything waiting on the user or an external party, with what would unblock it. Write "None" if there are none.

## Important context

{TODO_MARK} What the next agent must know that is not obvious from the code or the documents: assumptions, gotchas, failed approaches, user preferences expressed in the session. Write "None" if there is nothing.

## Critical files

{TODO_MARK} `path/to/file:line` - why it matters. Keep to the files the next step touches. Write "None" if there are none.

## Suggested skills

{TODO_MARK} Skills the next agent should run (for example gsd, tdd, review-loop), or "None".

## Environment state

Captured automatically when this handoff was created.

- Repository: `{root.name}`
- Branch: `{state['branch']}`
- HEAD: `{state['commit']}`

Recent commits:

{commits}

Uncommitted changes:

{dirty}

## Chain

{chain}
"""


def create_handoff(
    root, slug=None, title=None, continues_from=None, harness="manual", trigger="manual", session="", gsd_item=None
):
    directory, gsd_slug, note = locate(root, gsd_item, session)
    directory.mkdir(parents=True, exist_ok=True)
    previous = None
    if continues_from:
        candidate = Path(continues_from)
        previous = candidate if candidate.is_absolute() else directory / candidate.name
        if not previous.exists():
            raise SystemExit(f"continues-from not found: {previous}")
    else:
        previous = latest_handoff(directory)

    state = git_state(root)
    title = title or (slug.replace("-", " ") if slug else f"{state['branch']} checkpoint")
    now = datetime.now().astimezone()
    path = directory / f"{now:%Y-%m-%d-%H%M%S}-{slugify(slug or title)}.md"
    meta = {
        "title": title,
        "created": now.isoformat(timespec="seconds"),
        "status": "draft",
        "harness": harness,
        "trigger": trigger,
        "session": session,
        "gsd_item": gsd_slug or "",
        "branch": state["branch"],
        "commit": state["commit"],
        "continues_from": previous.name if previous else "",
    }
    write_handoff(path, meta, scaffold_body(title, root, state, gsd_slug, previous))
    if previous and previous.exists():
        prev_meta, prev_body = read_handoff(previous)
        if prev_meta.get("status") == "complete":
            prev_meta["status"] = "superseded"
            prev_meta["superseded_by"] = path.name
            write_handoff(previous, prev_meta, prev_body)
    return path, note


def refresh_draft(path, root):
    """Update the metadata of an existing draft instead of stacking another one."""
    meta, body = read_handoff(path)
    state = git_state(root)
    meta["branch"], meta["commit"] = state["branch"], state["commit"]
    meta["refreshed"] = datetime.now().astimezone().isoformat(timespec="seconds")
    write_handoff(path, meta, body)


# --- validate and status ---------------------------------------------------


def sections(body):
    parts = re.split(r"^## +(.+)$", body, flags=re.MULTILINE)
    return {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


def referenced_paths(body):
    """Backticked repo paths, ignoring placeholders and the captured git state."""
    body = re.split(r"^## +Environment state\s*$", body, maxsplit=1, flags=re.MULTILINE)[0]
    text = "\n".join(line for line in body.splitlines() if TODO_MARK not in line)
    found = set()
    for token in re.findall(r"`([^`\s]+)`", text):
        candidate = re.sub(r":\d+(-\d+)?$", "", token)
        if "/" in candidate and not candidate.startswith(("http", "~", "$")) and "*" not in candidate:
            found.add(candidate)
    return sorted(found)


def validate(path, root):
    meta, body = read_handoff(path)
    problems, warnings = [], []
    todo_count = body.count(TODO_MARK)
    if todo_count:
        problems.append(f"{todo_count} unfilled {TODO_MARK} placeholder(s)")
    found = sections(body)
    for name in SECTIONS:
        if name not in found:
            problems.append(f"section missing: {name} - keep every heading")
            continue
        content = found[name]
        if not content or TODO_MARK in content:
            problems.append(f'section empty: {name} - fill it or write "None"')
        elif name in NEVER_NONE and re.match(r"[-*]?\s*none\b", content, re.IGNORECASE):
            problems.append(f'section cannot be "None": {name}')
    for pattern in SECRET_PATTERNS:
        if pattern.search(body):
            problems.append(f"possible secret matches /{pattern.pattern[:30]}.../")
    base = root or path.parent
    for ref in referenced_paths(body):
        if not (base / ref).exists() and not (path.parent / ref).exists():
            warnings.append(f"referenced path not found: {ref}")
    if not re.search(r"^\s*1\.", found.get("Immediate next steps", ""), re.MULTILINE):
        warnings.append("Immediate next steps is not a numbered list")
    score = max(0, 100 - 20 * len(problems) - 5 * len(warnings))
    return meta, problems, warnings, score


def staleness(path, root):
    meta, body = read_handoff(path)
    findings, level = [], 0
    try:
        created = datetime.fromisoformat(meta.get("created", ""))
        age_days = (datetime.now().astimezone() - created).total_seconds() / 86400
    except ValueError:
        created, age_days = None, None
    if age_days is not None:
        findings.append(f"age {age_days:.1f} days")
        level = max(level, 0 if age_days < 1 else 1 if age_days < 3 else 2 if age_days < 14 else 3)
    commit = meta.get("commit", "")
    if root and commit and not commit.startswith("("):
        count = git(root, "rev-list", "--count", f"{commit}..HEAD")
        if count is None:
            findings.append(f"recorded commit {commit} not in history (rebased or other branch)")
            level = max(level, 2)
        else:
            findings.append(f"{count} commit(s) since handoff")
            level = max(level, 0 if int(count) == 0 else 1 if int(count) < 5 else 2 if int(count) < 20 else 3)
    branch = git(root, "branch", "--show-current") if root else None
    if branch and meta.get("branch") and branch != meta["branch"]:
        findings.append(f"branch differs: handoff {meta['branch']}, current {branch}")
        level = max(level, 1)
    missing = [r for r in referenced_paths(body) if root and not (root / r).exists()]
    if missing:
        findings.append("missing referenced paths: " + ", ".join(missing[:5]))
        level = max(level, 2)
    labels = ["FRESH", "SLIGHTLY_STALE", "STALE", "VERY_STALE"]
    return labels[level], findings, meta


def chain(path):
    seen, current = [], path
    while current and current.exists() and current not in seen:
        seen.append(current)
        meta, _ = read_handoff(current)
        prev = meta.get("continues_from")
        current = current.parent / prev if prev else None
    return seen


# --- hooks -----------------------------------------------------------------


def hook_input(args):
    data = {}
    if not sys.stdin.isatty():
        raw = sys.stdin.read()
        if raw.strip():
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                data = {}
    return {
        "cwd": args.cwd or data.get("cwd") or ".",
        "session": args.session or data.get("session_id") or "",
        "trigger": args.trigger or data.get("trigger") or "auto",
        "source": args.source or data.get("source") or "",
    }


def script_path():
    return str(Path(__file__).resolve())


def emit_context(harness, text):
    if harness in ("claude", "codex"):
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text}}))
    else:
        print(text)


def hook(args):
    info = hook_input(args)
    root = repo_root(info["cwd"])
    if not root:
        return 0
    directory, _, _ = locate(root, session=info["session"])
    latest = latest_handoff(directory)
    if args.event == "session-start" and info["source"] != "compact":
        # A new session has no chain yet: point at the newest handoff wherever it lives.
        newest = [h for d in handoff_dirs(root) for h in list_handoffs(d)[-1:]]
        latest = max(newest, key=lambda p: p.name) if newest else None

    if args.event == "pre-compact":
        if latest:
            meta, _ = read_handoff(latest)
            if meta.get("status") == "draft" and meta.get("session") == info["session"] and info["session"]:
                refresh_draft(latest, root)
                return 0
        create_handoff(root, harness=args.harness, trigger=f"compact-{info['trigger']}", session=info["session"])
        return 0

    source = info["source"]
    if args.event == "post-compact" or source == "compact":
        if not latest:
            return 0
        meta, _ = read_handoff(latest)
        if meta.get("status") != "draft":
            return 0
        rel = latest.relative_to(root)
        prev = meta.get("continues_from")
        emit_context(
            args.harness,
            (
                f"Context was just compacted. A draft handoff checkpoint was written to {rel}"
                + (f" (continues from {prev})" if prev else "")
                + ". Before continuing the task, complete it: replace every 'TODO:' section with concrete content from "
                "your compaction summary and current knowledge - write 'None' where a section has nothing to say, "
                "never delete a section - keep it brief, link GSD documents instead of restating "
                "them, never include secrets, set 'status: complete' in its front matter, then run "
                f"`python3 {script_path()} validate {rel}` and fix any problems it reports. Then resume the task."
            ),
        )
        return 0

    if args.event == "session-start" and latest:
        meta, _ = read_handoff(latest)
        if meta.get("status") == "superseded":
            return 0
        level, findings, _ = staleness(latest, root)
        try:
            age = (datetime.now().astimezone() - datetime.fromisoformat(meta.get("created", ""))).days
        except ValueError:
            age = 0
        if age > RESUME_NUDGE_MAX_DAYS:
            return 0
        rel = latest.relative_to(root)
        emit_context(
            args.harness,
            (
                f"Latest handoff in this repository: {rel} ({meta.get('status', 'unknown')}, {level}; "
                + "; ".join(findings)
                + "). If the user is continuing that work, read it before acting and follow "
                "the handoff skill's resume steps; otherwise ignore it."
            ),
        )
    return 0


# --- CLI -------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p_locate = sub.add_parser("locate")
    p_new = sub.add_parser("new")
    p_new.add_argument("slug", nargs="?")
    p_new.add_argument("--title")
    p_new.add_argument("--continues-from")
    p_new.add_argument("--harness", default="manual")
    p_list = sub.add_parser("list")
    for p in (p_locate, p_new, p_list):
        p.add_argument("--gsd-item", help="file under this GSD item instead of detecting one")
    sub.add_parser("validate").add_argument("file")
    sub.add_parser("status").add_argument("file")
    p_hook = sub.add_parser("hook")
    p_hook.add_argument("event", choices=["pre-compact", "post-compact", "session-start"])
    p_hook.add_argument("--harness", default="unknown")
    for flag in ("--cwd", "--session", "--trigger", "--source"):
        p_hook.add_argument(flag)
    args = parser.parse_args()

    if args.command == "hook":
        try:
            return hook(args)
        except Exception as error:  # a hook must never break the harness
            print(f"handoff hook skipped: {error}", file=sys.stderr)
            return 0

    root = repo_root(".")
    if args.command in ("locate", "new", "list") and not root:
        raise SystemExit("not inside a git repository")

    if args.command == "locate":
        directory, gsd_slug, note = locate(root, args.gsd_item)
        print(directory)
        if gsd_slug:
            print(f"gsd item: {gsd_slug}")
        if note:
            print(note)
        latest = latest_handoff(directory)
        if latest:
            print(f"latest: {latest.name}")
    elif args.command == "new":
        path, note = create_handoff(
            root, args.slug, args.title, args.continues_from, args.harness, gsd_item=args.gsd_item
        )
        if note:
            print(note, file=sys.stderr)
        print(path)
    elif args.command == "list":
        directory, _, _ = locate(root, args.gsd_item)
        handoffs = list_handoffs(directory)
        if not handoffs:
            print(f"no handoffs in {directory}")
        for path in reversed(handoffs):
            meta, _ = read_handoff(path)
            prev = meta.get("continues_from") or "-"
            print(f"{path.name}  [{meta.get('status', '?')}]  {meta.get('title', '')}  <- {prev}")
    elif args.command == "validate":
        path = Path(args.file)
        meta, problems, warnings, score = validate(path, root)
        print(f"score {score}/100, status {meta.get('status', '?')}")
        for p in problems:
            print(f"problem: {p}")
        for w in warnings:
            print(f"warning: {w}")
        if meta.get("status") != "complete":
            print("problem: status is not 'complete'")
            problems.append("status")
        return 1 if problems or score < 70 else 0
    elif args.command == "status":
        path = Path(args.file)
        level, findings, meta = staleness(path, root)
        print(f"{level}: " + "; ".join(findings))
        links = chain(path)
        if len(links) > 1:
            print("chain (newest first): " + " <- ".join(p.name for p in links))
    return 0


if __name__ == "__main__":
    sys.exit(main())
