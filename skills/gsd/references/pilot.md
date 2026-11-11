# Testing and availability

V1 is a portable Markdown skill using existing file tools. Its supported test
entry point before installation is explicit loading by path:

Read /absolute/path/to/skills/gsd/SKILL.md and use it to resume the GSD item at
/absolute/path/to/project/.agents/gsd/YYYY-MM-DD-name. Report its next authorised
step without implementing anything.

Run from the target project or supply its absolute path. Bare $gsd or /gsd works
only after that harness has discovered the skill; source-library presence alone
does not install it. Start a fresh session after installation if discovery is
cached. Do not claim autocomplete or native discovery from a path-based test.

Use a scratch project for the first start/close/reopen trial. Select a mode that
permits the requested Markdown edits. Repository inspection previously found
Markdown-capable OpenCode Plan and pi/omp Plan roles, and read-only Codex planning
instructions. These are candidate routes, not certified current runtime support.
Follow the active mode instructions and verify actual file access.

Test skill loading, scoped edits, an approval boundary and a fresh-session resume
in each target harness. Record version, mode, skill revision and observed files.
Do not change mode, model, role controllers or permissions silently to pass.

Explicit-only invocation is enforced only where a harness reads it: Codex reads
agents/openai.yaml (allow_implicit_invocation: false). Other harnesses may load
the skill from its description alone; the policy there is a convention, not a
control, until verified in that harness.

Optional specialist skills are loaded only if available and compatible. Without
them, GSD's own local document workflow still works. Do not install a dependency
or call a service merely because a reference names it.

`scripts/gsd` provides, in text, Markdown or JSON:

- Read-only: `status`, `attention`, `next` (with approvals read from
  DECISIONS.md), `progress` (with evidence freshness), `legacy`, `comments`,
  `validate` (with the project review rules file and the security gate),
  `agents` and
  `risk PATH... [--base REV]` (each path's tier, `always_high` match and
  Risk floor from the project review rules, never their guidance text).
- Writes: `new`, `set ITEM KEY=VALUE`, `plan ITEM --write DOC|--set`,
  `comments ITEM --assign`, `owner show|set|unset`, `prune [--dry]` and
  `reopen ITEM [--dry]`. They act only in the owning checkout, under an
  advisory lock, with `--expect SHA256` checks and atomic replacement. Exit 3
  means a conflict (lock, digest, ownership or a move that would break links),
  and nothing was changed.

Invoke it by its path inside the installed skill; a bare `gsd` on PATH is a
convenience for people and may be shadowed by a shell alias. It never stages,
commits or switches branches. Locks and the owner mapping
(`~/.config/gsd/owners.json`) are per machine. Single-writer use across
machines and review are conventions, not enforcement.

## Lifecycle CLI checks

`gsd new "Title"` writes the Ideation checklist before a tier is confirmed.
After confirmation, populate its later stages from workflow.md. `gsd validate`
warns on a missing or inconsistent checklist for tiered items; untiered items
keep their earlier behaviour. `gsd next --format json` includes `lifecycle_next`
(the first unfinished sub-task, or null), beside the recorded `next_action`.
Text and Markdown views show the next step too. `gsd reopen ITEM --dry` previews
the normal reopen; the write unticks the reopened and later stage boxes, preserving settled
sub-task outcomes, earlier work and fenced examples. The dry-run output names
the stage boxes that would be unticked. After reopening delivered work, the
GSD agent also clears the superseded final-check, package-acceptance and Complete
sub-tasks, preserves settled waivers, and verifies the new `next` action.

Replies end with a plain `Next: ...` line. Path-based smoke checks exercise
this convention without claiming installed skill discovery.
