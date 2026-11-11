---
slug: "{dated-slug}"
title: "{title}"
purpose: "{purpose}"
type: feature
stage: ideation
delivery: proposed
complexity: "{L1, L2 or L3, once the user confirms it}"
created: "{date}"
updated: {date}
version: 1
next_action: "{next authorised step}"
responsible: agent
branches: []
parents: []
dependencies: []
blockers: []
# branches: the item branch, then "base: <base>", recorded at Kickoff.
# Optional: priority; close_method (archive, compact or fold), set at CP3.
# Add completed or cancelled: YYYY-MM-DD only when
# that outcome applies. Empty lists may be removed. Remove complexity
# until the tier is confirmed, and for an untiered item.
---

# Idea

## Outcome

{Problem and intended outcome.}

## Scope

{Included work, exclusions and constraints.}

## Complexity

{Tier and reasons, one per dimension, for example: "L2. Risk L1: internal,
reversible. Change L2: ten files in one skill. Confidence Medium: scenario
checks only. Base L2; no demotion." See references/complexity.md.}

## Completion boundary

{Release readiness, or deployment plus defined production checks.}

## Goal

{L1 only: the concrete change and the approach in a few lines. Remove for L2
and L3; their approach lives in PLAN.md.}

## Success

{L1 only. Remove for L2 and L3.}

- AC-01: {Observable result.}

## Tests

{L1 only. Remove for L2 and L3. This is L1's verification plan: name the
verification layers each criterion needs - tests and specs, code checks,
run with mock data, benchmark, UI walkthrough.}

- AC-01: {The automated test that exercises it}; layers: {tests and specs}.

## TODO

{L1 only. Remove for L2 and L3.}

- [ ] T-01: {Action} (AC-01).

## Topology

{L1 only. Remove for L2 and L3; their topology lives in PLAN.md. CP2
approves it.}

- Orchestrator: {this session - harness, provider and model}; the only
  writer of GSD records and every commit.
- Implementers: {one subagent on the same provider and model, by default}.
- Reviewers: {plan review and counter-review reviewer and model, from
  Kickoff}.

## Lifecycle

{Start with Ideation only. After CP1 Kickoff, add the other four stages
and tier-specific sub-tasks from references/workflow.md, Lifecycle checklist.
Remove for an explicitly untiered item. Keep these separate from T-NN tasks.}

- [ ] Ideation
  - [ ] Light grilling
  - [ ] Scouting
  - [ ] CP1 Kickoff

## Open questions

{Only unresolved material choices; remove this section if none.}
