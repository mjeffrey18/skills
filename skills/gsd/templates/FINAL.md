---
updated: {date}
version: 1
---

# Final

## Delivered

{Scope completed and the exact revision covered.}

## Verification and review

{Current acceptance evidence and review resolution/accepted limitations, with links.}

## Human acceptance

{L2 and L3: who accepted the review package, when, and the commit it covered;
name any one-way door accepted below proof level 4.
L1: whether the package was offered and taken. Untiered: only when sign-off was
explicitly required; remove otherwise.}

## Documentation updated

{Link actual feature docs (default docs/features/), authoritative ADRs and
runbooks updated. Link applicable .agents/rules/, .agents/DESIGN.md and
.agents/styles/ guidance through concise conditional AGENTS.md links.
Respect existing project locations. Say not applicable where appropriate.}

## Review memory

{Tiered items: what the retro changed - each check, rubric line or project
review rules entry with its source finding IDs, and each change to
`settled`, `risk_paths` or `always_high` marked as a one-way door - and the
proposals it deferred, with the reason. Say "none" when it changed nothing.
Untiered: remove.}

## Release readiness

{Completion boundary met, deployment status, remaining rollout requirements and
rollback information where relevant. This report does not authorise deployment.}

## Delivery

{Items with an item branch only; remove otherwise. This is the snapshot at
CP3 close-out. The PR or local delivery ledger tracks the later delivery result.}

- PR: {link}
- CI attempts: {none yet, or attempts known at close-out}
- CP4 outcome: pending at close-out
- Delivery ledger: {PR link, or local ledger path}
- Close-out method: {Archive | Compact | Fold (default)}
- GSD scope: accepted and complete; merge and deployment remain separate

## Fold map

{Fold only; remove for Archive and Compact. The map accepted at CP3: one row
per lasting fact. Create a page only where no existing page fits.}

| Fact | Destination (file, section) | Action | Why this page |
| --- | --- | --- | --- |
| {Lasting fact} | {docs/features/x.md, Usage} | {edit, append or new page} | {Reason} |

## Limitations and follow-up

{Accepted limitations and separately tracked future work. Link deferred
features/specs in the optional .agents/TODO.md project backlog to their source
item or spec. Item TODO.md stays the task authority; backlog entries do not
silently waive unfinished acceptance criteria.}

## Conclusion

{Supported close-out statement. Create this report only once completion conditions
are met; no placeholder success claim. On reopening, preserve this conclusion as
superseded history under a heading such as `## Superseded v1 close-out`.}
