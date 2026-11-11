---
slug: {item folder name}
title: {title}
type: {feature or goal}
complexity: {L1, L2 or L3; remove if untiered}
delivery: {verified or cancelled}
completed: {YYYY-MM-DD; use cancelled: for a cancelled item}
record: {full SHA of the close-out commit that holds the whole item folder}
updated: {date}
version: 1
---

# {title}

## Outcome

{One paragraph: what was delivered (or why it was cancelled) and the
completion boundary that was met.}

## Decisions

{The few decisions a future reader needs, each with its reason. Leave out
routine approvals and superseded options.}

## Acceptance and review

{Who accepted what and the commit it covered, the review disposition, and any
one-way door accepted below proof level 4. "Not applicable" where it is.}

## Documentation

{Links to the permanent docs, ADRs, rules and backlog entries the item's
lasting context was folded into.}

## Limitations and follow-up

{Accepted limitations and tracked follow-up work, or "none".}

## Delivery

{For an item branch: pending at close-out. Link the PR or local delivery ledger
for current CI and merge status. GSD completion does not claim merge or deployment.
Remove this section for an item without a branch.}

## Full record

The complete item folder is in Git at `{record}`:
`git show {record}:{path to the item folder}/FINAL.md`. To reopen the item,
revert the commit that added this summary (workflow.md, Close-out method).
