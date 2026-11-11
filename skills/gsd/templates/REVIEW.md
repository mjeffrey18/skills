---
updated: { date }
version: 1
---

# Review

## Scope

{Reviewed document/implementation revisions, paths, requirements and environment.
Name the review: pre-implementation or counter-review, the reviewer and model,
and the rounds run. Its run or waiver is recorded in DECISIONS.md.
Link the door map: [door map](research/{date}-door-map.md).
When a changed path matches `always_high` (workflow.md, Security gate), add
the line `Security gate: applies - <paths> (<rule source: base, HEAD or both>)`
on its own; once recorded it is never removed.}

## Findings

### R-01 - {Finding} ({reviewer id, such as F1})

- Severity: {critical, high, medium or low}.
- Evidence: {Location and observation; acceptance ID if relevant}.
- Door: {one-way or two-way, from the door map}.
- Verified: {confirmed, refuted or unverifiable}.
- Verifier: {model; "2-of-3" when voted}.
- Method: {one line; link research/verification/{review}/round-{n}/ and the reviewed revision}.
- Lens: {the lens that raised it, such as general or security}.
- Fingerprint: `{path}#{symbol or *}:{rule class}` {from the tally; each verifier's, comma-separated, when they differ, and why it cannot be suppressed}.
- Protected: {no, unsure, security, migration, idempotency or concurrency; each verifier's, comma-separated, when they differ}.
- Disposition: open.
- Corrective task: {TODO task link}.
- Resolution: {Fix and verification, or accepting authority and rationale; for a security finding in a gated item, "Fix verified by a fresh verifier on {revision} ({verifier file})." or the user's acceptance as DECISIONS.md records it}.
- Prevention: {Useful regression check, if warranted}.

{If there are no findings, remove the example and state the actual review outcome.}

## Review package

{L2/L3 at close-out: Changed (final commit), Door and blast radius, Safe because (proof level 1-5), How tested,
How to undo, Evidence by type, Review, Residual risk, Offered. Link each one-way door's files.}

## Waived

{Only when a counter-review did not happen: "Counter-review waived on
{date}: {reason, such as Codex unavailable or Sam declined}." Remove otherwise.}
