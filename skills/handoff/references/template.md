# Handoff template

`handoff.py new` writes this structure with the metadata and Environment state
filled in. Replace every `TODO:` line. Headings are fixed so any harness can parse
and compare handoffs - add a section at the end if you need one, but do not rename
or remove these. A section with nothing to say gets "None", never an empty body or
a deleted heading; `validate` rejects both. Current state and Immediate next steps
cannot be "None".

```markdown
---
title: Short task title
created: 2026-09-28T18:30:00+04:00
status: draft            # draft -> complete -> superseded
harness: claude          # claude, codex, pi, manual ...
trigger: manual          # manual, or compact-auto / compact-manual / compact-threshold
session: <harness session id, if known>
gsd_item: 2026-09-15-gsd # empty when there is no GSD item
branch: main
commit: c94f7e6
continues_from: 2026-09-27-101500-previous.md
---

# Handoff: Short task title

## Current state
One paragraph: what is being worked on, how far it got, exactly where it stopped.

## Work item
GSD item link, or "No GSD item".

## Work completed
- Bullets for what this session finished, referencing commits or files.

## Decisions made
- Decision - rationale - options rejected. For a GSD item, link DECISIONS.md.

## Immediate next steps
1. The first thing the next agent does.
2. ...

## Blockers and open questions
- Blocker or question - what would unblock it. "None" when there are none.

## Important context
Assumptions, gotchas, failed approaches and user preferences that are not obvious
from the code or documents. This is the section the next agent most needs.

## Critical files
- `path/to/file.ts:142` - why it matters for the next step.

## Suggested skills
- Skills the next agent should run, or "None".

## Environment state
Filled in automatically: repository, branch, HEAD, recent commits, uncommitted files.

## Chain
Continues from [previous handoff](previous.md), or "Start of chain".
```

## Filling it in well

- Be specific: file paths with line numbers, command names, exact error text.
- Record why, not just what - rationale is what a fresh agent cannot reconstruct.
- Write for an agent that has the repository but none of the conversation.
- Prefer links to GSD documents, specs, issues and commits over restating them.
- Name environment variables and services; never include secret values.
