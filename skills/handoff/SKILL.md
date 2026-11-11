---
name: handoff
description: Write, complete or resume a chained handoff document so a fresh agent in any harness can continue the work. Use when the user asks to hand off, save state or pause, when a hook reports a draft handoff checkpoint after compaction, or when resuming from a handoff ("load handoff", "continue where we left off"). Not for GSD lifecycle records - those stay in the GSD item.
argument-hint: "[resume | what the next session will focus on]"
---

# Handoff

A handoff lets another session - Claude Code, Codex, pi or anything else - pick up
the work without the conversation. The file is the shared contract, so every
harness writes the same structure to the same place, and each handoff links to the
one before it.

`scripts/handoff.py` (standard library Python) does the mechanical work: locating,
scaffolding, chaining, validation and staleness checks. Run it with `python3` from
the repository you are handing off. The examples below use `$HANDOFF` for the
script's path next to this file.

## Where handoffs live

`python3 $HANDOFF locate` prints the directory:

1. **A named GSD item** - `--gsd-item <slug>` on `new`, `locate` or `list` files
   under `.agents/gsd/<slug>/handoffs/`.
2. **The session's existing chain** - hooks put a checkpoint wherever an earlier
   handoff from the same session already is.
3. **The branch's GSD item** - the one active item (not complete or cancelled)
   whose `branches` lists the current branch. The default branch (`main`,
   `master` or `origin/HEAD`) never counts: unrelated work shares it, so an item
   listing `main` is not assumed.
4. **Otherwise** `.agents/handoffs/` at the repository root.

On the default branch, pass `--gsd-item` when the work belongs to an item. If a
compaction checkpoint lands in `.agents/handoffs/` but belongs to an item, `git mv`
it into the item's `handoffs/`; later checkpoints from that session follow it.

Handoffs are committed with the work. Files are named
`YYYY-MM-DD-HHMMSS-<slug>.md`, with front matter recording status (`draft`,
`complete`, `superseded`), harness, branch, commit and `continues_from`.

## Create a handoff

1. Scaffold: `python3 $HANDOFF new <slug> --title "<title>" --harness <name>`. It
   chains to the latest handoff automatically; pass `--continues-from <file>` to
   pick a different predecessor. Environment state (branch, HEAD, recent commits,
   uncommitted files) is filled in for you.
2. Complete every `TODO:` section using the structure in
   [references/template.md](references/template.md). Current state, Immediate next
   steps and Important context matter most: the next agent acts on those first.
   If the user passed a focus for the next session, tailor the document to it.
   Never delete a section: where one has nothing to say, write "None", so the
   next agent can tell "nothing to report" from "forgot to fill it in". Only
   Current state and Immediate next steps cannot be "None".
3. Set `status: complete` and run `python3 $HANDOFF validate <file>`. Fix every
   problem it reports - unfilled placeholders, missing or empty sections, possible
   secrets, a score below 70. Completing a handoff marks its completed
   predecessor `superseded`.
4. Tell the user the path, the validation score and the first next step.

**Do not duplicate what other records already hold.** When there is a GSD item,
decisions go in its DECISIONS.md, evidence in FACTS.md and tasks in TODO.md; the
handoff links to them and captures only what they do not - where the session
stopped, what it was about to do and what it learned along the way. The same goes
for specs, ADRs, issues, commits and diffs: reference them by path or URL.

Redact API keys, passwords, tokens and personal data. Name environment variables,
never their values.

## Complete a draft after compaction

Harness hooks write a `draft` checkpoint just before the context is compacted,
then tell you where it is once compaction finishes. Fill it in from your
compaction summary and anything you still know, following steps 2 and 3 above,
then carry on with the task. Keep it short - a few precise lines per section beat
a long recap. If nothing meaningful happened since the previous handoff, say so in
Current state and point to that handoff.

## Resume from a handoff

1. `python3 $HANDOFF list` shows the chain, newest first, with status and
   predecessor. Pick the newest non-superseded handoff unless the user names one.
2. `python3 $HANDOFF status <file>` reports staleness (FRESH, SLIGHTLY_STALE,
   STALE, VERY_STALE) from age, commits since the handoff, branch and missing
   files, and prints the chain.
3. Read the whole handoff before acting. When it continues from an earlier one,
   read that too if the newest handoff leaves a gap. For a GSD item, resume
   through the GSD skill as well: its documents stay authoritative over the
   handoff.
4. Work through [references/resume-checklist.md](references/resume-checklist.md).
   The more stale the handoff, the more you verify before trusting it.
5. Start with Immediate next steps item 1. When you hand off again, create a new
   handoff so the chain continues rather than rewriting the old one.

## Hooks

The hooks call `python3 $HANDOFF hook <event> --harness <name>`:

| Event | Claude Code / Codex | pi / omp | OpenCode |
| --- | --- | --- | --- |
| `pre-compact` - write or refresh the draft checkpoint | `PreCompact` | `session_before_compact` | `compaction` session hook |
| `post-compact` - ask the agent to complete the draft | `SessionStart` with source `compact` | `session_compact` | `session.compaction.ended` event |
| `session-start` - point at a recent handoff | `SessionStart` | `session_start` | first `context` session hook |

Claude Code and Codex register the hooks in their settings; pi and omp need an
extension, and OpenCode a plugin, that call the same subcommands. Those
adapters are not included here. OpenCode has no
context channel for hook output, so such a plugin keeps the session-start pointer
as system context and steers the post-compact prompt in as a synthetic message.

A hook outside a git repository does nothing, and any error is written to stderr
without blocking the harness. A second compaction in the same session refreshes
the existing draft rather than stacking a new one.
