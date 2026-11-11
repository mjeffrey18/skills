---
updated: {date}
version: 1
# Project review rules: reviewer guidance, installed as .agents/rules/review/REVIEW.md.
# Each entry with fields is one list item, its fields separated by " | ".
# risk_paths: "<glob> | <tier 0, 1 or 2>"; a path no entry matches counts as 1.
risk_paths:
  - "{glob} | {tier}"
# always_high: globs; each is a one-way door and turns on the security gate.
always_high: []
# review_focus: what matters in this code, one line each, with its source.
review_focus: []
# known_landmines: "<glob> | <what bites> | <source>".
known_landmines: []
# settled: "<glob> | <symbol or *> | <rule class> | <rejected claim> | <lasting reason> | <source>".
settled: []
# nitpick_cap: style or preference findings reported per review; remove the line for no cap.
nitpick_cap: 3
rollback: "{how to undo a change in this repository, or a link to the runbook}"
---

# Project review rules

Reviewers read this file; implementers do not. The review loop copies it
from the review's base commit, so a change cannot weaken the rules that
judge it. `gsd risk` reads only `risk_paths` and `always_high`. The brief
inlines `review_focus`, the landmines whose glob matches a changed path and
the cap. The settled list is applied after verification and never reaches
the reviewer.

Globs: `**` crosses folders, `*` stays inside one. A path matching several
`risk_paths` entries takes the highest tier. Rule classes for `settled`
come from review-critic's fixed list; a settled entry is never in a
protected class (`race`, `idempotency`, `migration`, `auth`, `injection`,
`secrets`, `data-exposure`) and never `other`.

## Conventions

{Short rules a reviewer should hold this code to, each with its source.}

## Do not nitpick

{Style or preference points that are settled here, so reviewers spend no
time on them.}

## Rollback

{Link to the rollback runbook, or the steps in short.}
