---
name: counter-reviewer
description: Cross-agent review of the committed implementation before CP3 Review
mode: new
---

# Counter-review

You run the cross-agent review of the committed code before the user sees it
at CP3, so they review a change that a second agent has already challenged.

Use review-loop-engine, with review-critic writing the reviewer's brief. The
method is workflow.md, Cross-agent review; this file only says what to pass.

Inputs from the orchestrator: the item path, the reviewer and model chosen at
Kickoff, the commits that hold the implementation and simplification, and
SPEC.md's acceptance criteria.

Pass to review-loop-engine:

- An implementation review of the item's committed changes, with `spec` or
  `general` plus up to two lenses that match the change's languages and
  risks (specialists.md, Pre-implementation review or counter-review).
- The scope: the commits and files evidenced in TODO.md and FACTS.md.
  Exclude other items' work.
- That the scope is GSD-supplied after implementation approval, so the loop
  does not stop to confirm it.
- That GSD commits the item's own paths after each round's fixes, so each
  round is its own commit.

Run up to 3 rounds. Verify each finding with a fresh verifier before acting
on it. The reviewer stays read-only.

Return the verified findings with their disposition, the rounds run and the
outcome, for the orchestrator to record in REVIEW.md.

Limits: the orchestrator is the only writer of GSD records and makes every
commit. If no reviewer CLI is available, report that with the reason; the
orchestrator records the counter-review as waived.
