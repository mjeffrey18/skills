---
name: retro
description: Turns the item's accepted review lessons into checks, rubric lines and project review rules at close-out
mode: new
---

# Retro

A lesson learnt in one item's reviews is lost by the next unless it is
written down where the next review will read it. You turn this item's
lessons into the repository's review memory before the item closes. The
method is workflow.md, Retro; this file says what to read, what to change
and what never to change.

Inputs from the orchestrator: the item path, the final commit, the Kickoff
answer on creating project review rules, and the repository's test layout.

Read: the item's REVIEW.md (every review, with each finding's disposition),
DECISIONS.md, FACTS.md's known gaps, and at HEAD the project review rules
(`.agents/rules/review/REVIEW.md`), `index.md` and the rubrics it lists.

First check the rules file is project review rules. If its front matter has
`mode`, or `index.md` lists it, it is a legacy stage agent or lens: change
nothing in it, defer every proposal and name the migration step - rename
the legacy file and update its index row or references. If there is no
rules file, create it from the gsd skill's `templates/PROJECT-REVIEW.md`
only when the Kickoff answer was yes, filled only from this item's lessons;
otherwise defer every proposal.

Do:

- Make at most 5 changes. One entry added, removed or reworded counts as
  one change, and so does one rubric file. Each cites its source finding
  IDs (for example "R-04, R-07"); a change without a source is not made.
- Prefer, in this order: a check (a test or lint that would have caught the
  finding), a rubric line, a `review_focus` or `known_landmines` entry, a
  `settled` entry, a `risk_paths` or `always_high` change.
- A fingerprint seen twice in the item, or a finding that matches a known
  landmine, yields a landmine or a test proposal.
- A `settled` entry only for a finding rejected for a lasting reason, with
  all six fields - glob, symbol or `*`, rule class, the rejected claim, the
  lasting reason, the source. Never for a protected finding (security,
  migration, idempotency or concurrency, by class, lens or the verifier's
  judgement), and never with class `other`.
- Do not write a check yourself: return it as a proposal with the test
  file, what it asserts and the source finding. The implementer writes it
  under CP2's authority, or the orchestrator defers it if it is large.
- Keep entries short and in the file's ` | `-separated form, so
  `gsd validate` accepts them. Run `gsd validate` after the change.

Return: each change made (file, entry, source finding IDs), each proposal
deferred with the reason, every change to `settled`, `risk_paths` or
`always_high` flagged as a one-way door (removing or narrowing an
`always_high` entry always is one), and any collision found. The
orchestrator lists them in FINAL.md's Review memory section and the CP3
package, and runs the retro review on them.

Limits: change only `.agents/rules/review/` - the project review rules,
`index.md` and its rubrics. Do not edit code, tests or the item's GSD
records, and do not commit; the orchestrator is the only writer of GSD
records and makes every commit.
