---
updated: {date}
version: 1
---

# Facts

## Current findings

{Curated observations with sources; distinguish assumptions from verified facts.}

## Verification

{One record per verification layer that runs: tests, code checks, mock-data run, benchmark or UI walkthrough.}

### E-01 - {Check}

- Layer: tests.
- Criteria: AC-01.
- Result: not_run.
- Date: {date}.
- Tested revision: {Commit `abc1234`, paths `src/`, `tests/`; or "uncommitted - freshness unknown".}
- Baseline: {L2/L3: base commit `9f0e1d2` - the criterion's assertion failed (quote it); or "baseline unavailable:
  {reason}; fallback: {check, such as a mutation check that went red}"; or "regression - passes on base and final".
  Remove for L1.}
- Environment: {Where the check ran.}
- Procedure: {Command or steps.}
- Evidence: {Short result summary; link research/ output only when it is needed later.}
- Freshness: {Current, stale or unknown; `gsd progress` computes it.}

### E-02 - {End-to-end check}

- Layer: {mock-data run or UI walkthrough; when the plan did not name it, add "added by the diff" and the paths, e.g.
  "UI walkthrough, added by the diff (`page/index.html`)"}.
- Criteria: AC-01.
- Result: not_run.
- Date: {date}.
- Tested revision: {Commit `abc1234`, paths `src/`.}
- Method: {Screenshot, computer use, browser automation, simulation or live check.}
- Data: {Mock-data run: the fixtures or seeds used, or the data created and removed; never real or production data. Remove otherwise.}
- Environment: {Harness, tool, machine, browser or fixture.}
- Procedure: {The steps a user or caller takes.}
- Evidence: {What was seen; link the final screenshots in the feature docs, e.g.
  [after](../../../docs/features/greetings/after.png), and raw runs under research/.}
- Fallback: {If not_run or blocked: the reason and the fallback used or requested. Remove otherwise.}
- Freshness: {Current, stale or unknown.}

### E-03 - {Performance check, only when a gain is claimed or a hot path changes}

- Layer: benchmark.
- Criteria: AC-01.
- Result: not_run.
- Date: {date}.
- Tested revision: {Commit `abc1234` against base `9f0e1d2`, paths `src/`.}
- Environment: {One machine, load and versions.}
- Procedure: {Command and batch seed data; at least 5 runs per variant, alternating A and B; PLAN's threshold, if any.}
- Evidence: {The table, then the raw runs or a link to them under research/.}

| Metric | Baseline | Result | Method | Environment | Runs per variant |
| --- | --- | --- | --- | --- | --- |
| {p50 latency} | {median (min-max)} | {median (min-max)} | {tool} | {machine} | {5} |

## Useful failed approaches

{Only failures worth retaining to avoid repeated work. Remove empty sections.}
