---
name: gsd
description: Coordinate GSD work items - starting, resuming, planning, approved implementation, review and close-out - using persistent Markdown documents and compatible specialist skills.
disable-model-invocation: true
---

# GSD

When the user explicitly invokes `full-send` or `full-stop` for an existing
item, apply [explicit branch delivery](references/workflow.md#explicit-branch-delivery)
instead of the default CP3/CP4 acceptance and branch-deletion steps below.
All other scope, planning, review, security and verification requirements remain.

Use this skill when explicitly asked to manage a GSD item. Records are edited with
ordinary file tools. The bundled `scripts/gsd` CLI (Python 3, standard library)
inventories and validates items, and provides safe metadata updates, prune,
reopen and comment IDs when those actions are authorised; see
[pilot.md](references/pilot.md). There is no custom tool.

## Orient

1. Inspect applicable repository instructions and Git status. Resolve the named
   item, or list items with `<this skill>/scripts/gsd status` (add `--all` for
   completed and cancelled work, `attention` or `next` for what needs acting on). Use the current request and
   branches to disambiguate; ask only if several candidates remain.
2. Read IDEA.md and DECISIONS.md, then the planning documents, remaining TODOs,
   facts and review findings relevant to the requested step. Read an existing
   FINAL.md when resuming or reopening. Do not restart settled discovery.
3. Establish the document-owning checkout. V1 uses one writer in one explicitly
   selected checkout. If ownership or concurrent changes are ambiguous, stop
   writes and explain the conflict; read-only investigation can continue.
4. Identify the requested action and its existing authorisation. Read
   [workflow.md](references/workflow.md) for the corresponding stage. Before
   creating or changing records, read [documents.md](references/documents.md).
   Load only the relevant template linked there.

For a new item, IDEA.md is the first record, written after light grilling. Items are tiered L1, L2 or L3 by
complexity: after light grilling and scouting, score the item with
[complexity.md](references/complexity.md) and propose the tier at CP1
Kickoff; record it once the user confirms. The tier sets the minimum
documents, reviews, approvals and verification; items without a tier keep
the earlier rules. Other documents appear when useful, not as an empty bundle. A legacy INTENT.md is a migration candidate: preserve its
content and approval history, and rename/update references only when authorised.

## Compose

GSD owns item state, approval records, document paths and handover. Specialist
skills supply methods. When an activity would benefit from one, read
[specialists.md](references/specialists.md), check the actual available skill
and load its instructions. Supply the settled scope, bounded task, destination,
authorisation and expected output. Announce the selected skill briefly.

Reuse a compatible skill, not merely one with a matching name. Never start an
issue-tracker setup or publication workflow just to produce a local GSD document.
Missing optional skills do not block ordinary work: use the documented fallback.
If a user explicitly requires a missing specialist, explain that limitation.

Loading a skill does not imply spawning an agent. A tiered item delegates
through its stage agents, which this skill permits; other delegation needs
the user's, the repository's or the active skill's permission. Keep one
document writer; scouts, implementers and reviewers return their results to
that writer.

## Act and hand over

Perform the authorised step, then update the relevant documents and inspect the
result. Run `<this skill>/scripts/gsd validate <item>` after changing records and
fix, or report, each error and warning it lists; it reports and never edits.
It is a lint, not evidence: never record a validate run in FACTS.md or save
its output. Preserve unrelated edits and original human comments. Re-read before
writing; this reduces mistakes but is not concurrency protection.

A tiered item has three HITL Checkpoints, on every tier (workflow.md,
HITL Checkpoints): CP1 Kickoff after light grilling and scouting, CP2
Pre-implementation after the full planning set and its cross-agent review,
and CP3 Review after the counter-review, verification and final checks; an
item with an item branch adds CP4 Merge once CI is green or skipped. Each
checkpoint asks all its questions at once, with a recommended answer for
each, so "go" accepts every default. Between checkpoints, ask only when no
approved work can continue: the user's attention is the scarce resource, and
a question that can wait belongs in the next checkpoint. An L3 smoke review
is the one extra stop, only when PLAN marks one. Untiered items keep plan
then specification/task approval; their reviews are offered, never gates.
Record explicit scoped authorisation already given in the conversation,
including an instruction to document and implement; do not demand it again
merely because the documents were written later. Do not claim the user
reviewed unseen versions. If the user limits the task to planning, that
remains the boundary.

Each stage's subagents are defined in `references/<stage>/` and resolved
with `gsd agents <stage>`, so a repository can replace, extend or add them
(specialists.md, Stage agents). The topology approved at CP2 decides who
implements; by default one implementer subagent on the same provider and
model, with this session as orchestrator and the only writer of GSD records.

Use current acceptance evidence and review disposition to decide completion.
Checked tasks alone are insufficient. Evidence follows the verification
layers the plan names - for L2 and L3, tests that fail on the base commit, a
run with mock data, a benchmark for performance claims and screenshots for
UI changes (workflow.md, Verification layers) - and review findings are verified before anyone acts on them. At CP3 the user
accepts a short review package, with the door and the safety fact, and chooses
Archive, Compact or Fold (default), before FINAL.md is written; the acceptance
covers that commit only. A close-out
request or acceptance of deferred work does not accept an unseen package;
present it and wait unless the user explicitly waives package review.
FINAL.md records the agreed completion boundary and documentation updates;
it does not authorise deployment.

End every GSD reply and summary with one plain "Next:" line naming one
action - the first unticked lifecycle sub-task, checkpoint decision or, after
GSD closure, remaining delivery action. Keep active IDEA.md `next_action`
consistent with it; after closure, keep the delivery ledger current instead. Report
changed scope, evidence and blockers before that line. Keep lifecycle
metadata in IDEA.md. Do not silently switch branches, deploy, prune or run a
bulk migration. A tiered item gets its own branch from the base after CP1
approval - with gk when the CLI responds, the git-kiss skill is available
and a remote exists, otherwise plain git, and from the local base without
a remote - recorded in IDEA.md `branches` (workflow.md, Item branch). It
commits only its own paths on that branch at fixed points (workflow.md,
Commits): the item records after CP1, the planning set and each
plan-review round before CP2, then, under CP2's authority, the CP2
decisions and the close-out commits through to the review package without
stopping. After the final checks it pushes the item branch and opens a
draft PR carrying the review package (workflow.md, Draft PR). Every push
names the remote and one refspec whose destination is the item branch from
IDEA.md, checked before the push whatever is checked out, with git even on
the gk path (never `gk pf` or `gk pr`); never push any
other branch, and the base only as the CP4 merge. When the permission hook
denies a push, force push or remote
delete, stop, print the exact command for the user to run, try no other
way round it, and check the remote ref after they confirm (workflow.md,
Pushes). An untiered item never pushes. CP3
on a draft PR also asks about staging QA (only when a staging procedure
exists) and approves the post-approval rebase and force push; feedback is
fixed, committed, pushed and the PR body updated before CP3 is asked again.
After all CP3 HITL questions are accepted, write FINAL.md, mark the accepted
GSD scope complete/verified and commit the full records on the item branch.
Then carry out Archive, Compact or Fold in a separate commit, before CI and
merge (workflow.md, Close-out method). FINAL.md must remain inspectable in the
full-record commit. Record the choice as `close_method` in IDEA.md. Fold
discovers the repo's documentation from every tracked Markdown file, folds
the item's lasting knowledge into the existing docs through a fold map
accepted at CP3, and leaves nothing in docs/gsd; Compact retains a standalone
GSD summary; Archive retains the full folder. Each method commit ends with
the `GSD-Closed` trailer its command prints. Offer these methods
at CP3 with Fold recommended, never "now or after merge". An earlier choice
must be presented at CP3, not used to bypass it. Do not close an unaccepted item.

GSD closure means the accepted scope is finished, not that the branch merged
or deployed. FINAL.md and any Compact summary say delivery was pending at close-out
and link the PR or local delivery ledger for the eventual outcome. Preserve the
branch/base refs, recovery SHA, tested heads and CI attempts there so delivery
can resume after the active GSD folder is removed. A new finding that invalidates
the acceptance requires reopening and renewed acceptance; a declined merge or
blocked CI alone leaves the accepted scope closed and branch delivery pending.

With an item branch, then rebase on the base, rerun the relevant final checks,
and push the final head including both close-out commits. Use a plain push when
the fetched remote head is an ancestor, a lease bound to it when it is the
agent's own last pushed head and the rebase rewrote it, otherwise stop. Mark
the PR ready. CI must cover this head: fix, commit and push at most 3 times
before asking; never count missing checks as green, and name skipped CI when
none exists. Before CP4 fetch the base; if it moved, rebase, check, push and
run CI again. CP4 shows what changed since CP3 and reminds when the PR has no
approving review. Missing FINAL.md in the recovery commit or an uncommitted
close-out method blocks merge. After acceptance, merge locally without a
remote, else with `gk ff` (never `gk ff!`) or the exact plain-git `--no-ff`
sequence; check the merge parents, push the base by explicit refspec and verify
publication before deleting the item branch. No GSD close-out commits follow
the merge (workflow.md, CP4 Merge).

Without an item branch, finish at the close-out method commit. When pruning,
compacting or reopening, run the `gsd` command with `--dry` first and inspect
the moves. An untiered item commits only when the user asks.

For local testing and harness constraints, see
[pilot.md](references/pilot.md).
