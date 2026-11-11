# Project structure

Resolve paths relative to the chosen vault. Vault and project instructions take precedence.
Only `IDEA.md` carries project frontmatter by default. Other files start with an H1.
Preserve existing metadata in adopted projects.

## Start small

Create these files for a new project:

- `IDEA.md` - purpose, goals, scope, completion criteria and current position.
- `TODO.md` - immediate Now / Next / Later queue.
- `AGENTS.md` - stable working instructions and document routing.
- `CLAUDE.md` - the single line `@AGENTS.md`.

Create the following when useful content exists. A substantial initial brief can justify
all of them immediately; a small project may keep its requirements and approach in IDEA.

| Record         | Responsibility                                                                      |
| -------------- | ----------------------------------------------------------------------------------- |
| `SPEC.md`      | Detailed requirements and constraints; IDEA retains the purpose and scope boundary. |
| `PLAN.md`      | Canonical agreed sequence, dependencies and risks. TODO supplies the action queue.  |
| `DECISIONS.md` | Open questions and dated decisions; significant reasoning links to an ADR.          |
| `FACTS.md`     | Sourced findings, evidence and explicitly superseded conclusions.                   |
| `CONTEXT.md`   | Source index: meetings, threads, documents and related projects.                    |
| `NOTES.md`     | Raw capture, explicitly unsettled until assessed.                                   |
| `README.md`    | Optional human entry point linking the authoritative records.                       |
| `FINAL.md`     | Completion or cancellation outcome and its evidence.                                |
| `research/`    | Dated research notes with source links and unresolved questions.                    |
| `ADRs/`        | Significant architectural or other durable project trade-offs.                      |
| `plan/`        | Audience-specific views derived from PLAN, without independent commitments.         |
| `final/`       | Finished artefacts such as briefs, decks and reports.                               |
| `_archive/`    | Superseded material retained for history, not active guidance.                      |

Create folders with their first useful content. Add an index only when it improves navigation.
Keep existing folder and filename conventions; for new research use `YYYY-MM-DD-topic.md`,
and for new ADRs use `ADR-NNN-slug.md` with the next unused number.

## One home for each kind of state

`IDEA.md` owns lifecycle status and a short Current position section: progress, blockers
and next action. `TODO.md` owns task progress. `SPEC.md` owns requirements, not status.
`AGENTS.md` owns stable instructions, not a second progress summary. Project-index rows
and audience-specific plans are derived views; update affected views or label them stale.

When adopting an older scaffold, reconcile its SPEC Status and AGENTS status summaries
into IDEA as part of authorised maintenance. Preserve useful history, replacing duplicate
current summaries with links. If they conflict, surface the conflict rather than guessing.
Do not move status when the vault's own rules explicitly prescribe another home.

## Frontmatter

```yaml
---
title: <Human-readable title>
project: <slug>
status: idea
created: <YYYY-MM-DD>
tags:
  - "#project/<slug>"
related: []
purpose: <one-line purpose>
---
```

Use the actual current date for creation. Keep the existing vocabulary:
`idea`, `wip`, `active`, `paused`, `blocked`, `complete`; add `cancelled` where the vault
allows it. If its schema excludes cancellation, record the outcome in prose and use its
approved inactive status. Do not silently alter vault schemas.

For new projects, `idea` means scoped but not started, `wip` means being shaped and
`active` means carrying out the agreed work. Respect an existing vault's definitions.
`paused` is deliberately on hold; `blocked` needs a named dependency or decision.
`complete` requires supported outcomes. Do not infer completion from an empty task queue.

Populate `related` only with real existing notes. Add `pillar` only when the vault defines pillars,
using the current list in the vault's guidance (for example `projects/AGENTS.md`).
Do not copy a historical pillar list from this skill.

## Design and project index

If `<vault>/context/DESIGN.md` exists, link it from the project's AGENTS when relevant.
Otherwise create a local `DESIGN.md` only when the project has actual design guidance.
Do not generate a placeholder or a link to a nonexistent file.

If `projects/AGENTS.md` has a project table, add or update only this project's row,
matching its columns and deriving status from IDEA. Preserve unrelated entries.
