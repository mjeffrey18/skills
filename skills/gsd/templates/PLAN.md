---
updated: { date }
version: 1
---

# Plan

## Approach

{Components, repository evidence, interfaces and chosen approach.}

## Program design

{Required for L3 and L2 interface changes. Start from the caller's view:
usage before shape, then changed types, function signatures and call paths.
Remove when not applicable.}

## Fit and operation

{L2 and L3. Remove for L1 and untiered items.}

- Project patterns: {the existing patterns this follows, or why it departs from them}.
- Next change: {the likely next change and how this design takes it}.
- Failure modes: {how it can fail in use}.
- Signals: {the logs and metrics that show each failure}.
- Rollback signal: {what tells you to roll back, and how}.

## Diagrams

{L2: a context diagram and one flow diagram from entry to exit. L3: also a
layer diagram and one flow per main path, including failure and rollback
paths. Label entry, execution and exit points. Plain ASCII, lines at most 120
characters. Remove for untiered items that need none.}

### Context

```text
{actors} --> [ {system boundary: where the change sits} ] --> {other systems}
```

### Flow: {path name}

```text
entry: {command, route, hook or event}
   |
   v
execution: {component} -> {component}
   |
   v
exit: {output or side effect}; on failure: {error or rollback path}
```

## Sequence

{Order vertical slices that each run end to end. For each slice, name affected
paths and the check that must pass before the next slice starts. L3 may mark
one slice "smoke review".}

## Acceptance

{L2 only; L3 and untiered items keep criteria in SPEC.md. Remove otherwise.}

- AC-01: {Observable result.}

## Verification

{The verification plan: observable checks, expected evidence and completion
boundary. For each criterion, the automated test that exercises it, the
verification layers it needs - tests and specs, code checks, run with mock
data, benchmark (performance-sensitive), UI walkthrough (UI changes) - and, for
L2 and L3, the end-to-end method (screenshot, computer use, browser
automation, simulation or live check), or the test that stands in and why no
method applies. CP2 approves it.}

- AC-01: test {test name}; layers: {tests and specs, run with mock data}; end
  to end: {method and environment}.

## Topology

{L2 and L3. Who does the work; CP2 approves it and the user may change it.
Parallel implementers only when slices touch separate files, do not depend
on each other, have interfaces fixed here or in SPEC.md and can each be
tested alone - each in its own worktree.}

- Orchestrator: {this session - harness, provider and model}; the only
  writer of GSD records and every commit.
- Implementers: {one subagent on the same provider and model, by default;
  for parallel slices, each subagent with its provider, model, slices and
  worktree}.
- Reviewers: {plan review and counter-review reviewer and model, from
  Kickoff}.

## Risks and remaining decisions

{Trade-offs, compatibility, rollback and unresolved technical decisions.}

## Authority

{Link to the relevant decision entry or state that approval is pending.}
