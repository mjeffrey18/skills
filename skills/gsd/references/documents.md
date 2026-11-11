# Documents and records

## Item location and metadata

Active items live in .agents/gsd/YYYY-MM-DD-name/. Closed items move to
docs/gsd/YYYY/MM/, as the full folder or a one-file summary (workflow.md,
Close-out method). Remove branch type prefixes
such as feature/ and normalise remaining separators to hyphens. On a base branch
such as main/develop, use a content-based name. Append -v2, -v3 for folder
collisions; those suffixes are unrelated to document versions. Preserve the slug
through branch renames and archive moves.

[IDEA template](../templates/IDEA.md) is the item entry point throughout delivery.
Required front matter: slug (full folder identity), title, purpose, type
(feature or goal), stage, delivery, created, updated, version, next_action and
responsible (human or agent, identifying who can take the next action). Set human
when the next action is a required user decision; do not leave agent as a default
while it is waiting for that decision. Optional fields: complexity, priority,
branches, parents, dependencies and blockers.

branches lists the item branch first, then its base as `"base: <base>"`,
for example `branches: ["feature/greet-languages", "base: main"]`; a tiered
item records both at Kickoff (workflow.md, Item branch), and its pushes
check their destination against the first entry.

complexity is the item's confirmed tier, exactly `L1`, `L2` or `L3`
([complexity.md](complexity.md)). It is the only thing that makes an item
tiered; the IDEA.md Complexity section gives the reasons. Without it the item
is untiered and keeps the rules that predate tiers. Any other value is an
`idea-complexity` warning, and the item is treated as untiered. Use stable item slugs for relationships; qualify
another repository in prose when necessary. Do not infer relationships.

- stage: ideation, planning, execution, review, complete.
- delivery: proposed, ready, in_progress, implemented, verified, cancelled.
- Keep blockers separate from stage/delivery. Missing evidence is not verified.
- complete requires verified delivery; verified requires current acceptance
  evidence and review resolution. Cancellation retains its last active stage.
- completed: YYYY-MM-DD when complete; cancelled: YYYY-MM-DD when cancelled.
  On reopening, remove the active terminal date and retain it in the decision
  history and superseded close-out.
- A goal needs its own acceptance evidence; child completion alone is insufficient.

All maintained Markdown, including ADRs, uses updated (ISO date) and positive
integer version. A substantive scope, requirement, approach or task-scope change
bumps the version. Routine task completion, comment processing and editorial
changes update the date. Research dumps have no mandatory format or front matter.

## Responsibilities and templates

- [IDEA.md](../templates/IDEA.md): purpose, scope, tier and authoritative item
  metadata. For L1, also the goal, criteria, tests, tasks and topology.
- [PLAN.md](../templates/PLAN.md): approach, fit and operation (L2 and L3),
  diagrams, sequence, verification plan, topology, risks and unresolved
  technical choices. For L2, also the acceptance criteria.
- [SPEC.md](../templates/SPEC.md): detailed behaviour, stable acceptance IDs
  such as AC-01 and the completion boundary.
- [TODO.md](../templates/TODO.md): checkboxes with task IDs such as T-01,
  acceptance links, dependencies and blockers.
- [DECISIONS.md](../templates/DECISIONS.md): chronological dated bullets for
  decisions, scoped approvals and review offers.
- [FACTS.md](../templates/FACTS.md): curated facts and evidence from any
  stage, including end-to-end evidence; useful failed approaches.
- [REVIEW.md](../templates/REVIEW.md): stable finding IDs such as R-01,
  severity, evidence and disposition; review waivers.
- [FINAL.md](../templates/FINAL.md): delivered scope, acceptance, review,
  documentation updates, review memory, human acceptance and readiness
  conclusion.
- [PR.md](../templates/PR.md): the pull request body - the review package,
  one-way-door links and screenshots - when the work ships as a PR.
- [PROJECT-REVIEW.md](../templates/PROJECT-REVIEW.md): the repository's
  project review rules, not an item record; installed once as
  `.agents/rules/review/REVIEW.md` (Permanent documentation and deferred
  work).
- `research/<date>-door-map.md`: each changed path or plan step with its door
  (workflow.md, Doors).
- handoffs/: chained session handoffs written by the handoff skill and
  compaction hooks. They say where a session stopped; they are not lifecycle
  state.

Templates are drafting aids. Replace brace placeholders and remove unused
instructions/sections before writing an item document. Do not replace an existing
document with a blank template. Preserve content and add only needed structure.

## Document sets

Each tier has a minimum set. Other records appear when the work needs them.

- L1: IDEA.md only, with Goal, Success, Tests, TODO and Topology sections.
  Success holds the acceptance criteria (AC-NN), Tests names the automated
  test for each, TODO holds the tasks (T-NN) as checkboxes, and Topology
  names who implements and reviews. Keep each section short and
  goal-driven.
- L2: IDEA.md, PLAN.md and TODO.md. PLAN.md has a Diagrams section, an
  Acceptance section with the criteria, a Verification section and a
  Topology section. Add SPEC.md when detailed behaviour needs its own
  document; it does not replace PLAN.md approval.
- L3: IDEA.md, PLAN.md, SPEC.md and TODO.md. SPEC.md holds the criteria.
- Untiered: the documents the item already has, under the rules that predate
  tiers.

DECISIONS.md, FACTS.md, REVIEW.md, FINAL.md, research/ and ADRs appear at any
tier when there is something to record. The completion boundary lives in
IDEA.md for L1 and L2, and in SPEC.md for L3.

### Promotion

When the tier rises, change `complexity` and the Complexity section, then move
content into the new tier's documents:

- L1 to L2: Goal and approach go to PLAN.md, Success to PLAN.md Acceptance,
  Tests to PLAN.md Verification, Topology to PLAN.md Topology, and the TODO
  section to TODO.md.
- L2 to L3: PLAN.md Acceptance goes to SPEC.md.

Keep every AC and task ID, text and checkbox state. Leave a one-line pointer
where the content was, for example "Moved to PLAN.md, Acceptance (L2,
2026-10-18)". Do not keep two live copies of a criterion. Record the
promotion in DECISIONS.md. A lowered tier keeps its documents; nothing is
deleted.

### Diagrams

Diagrams live in PLAN.md under a Diagrams section, as plain ASCII in fenced
`text` blocks, so every harness and reviewer can read and diff them. IDEA.md
stays text only at every tier.

- L1: no diagram. An L1 item that needs one is probably not L1.
- L2: a context diagram (the system boundary, the actors and where the change
  sits) and one flow diagram from entry to exit.
- L3: the L2 diagrams, a layer diagram, and one flow per main path, including
  failure and rollback paths.

Each diagram labels its entry points, execution path and exit points. Lines
are at most 120 characters. For example:

```text
entry: `gsd validate ITEM`
   |
   v
execution: parse IDEA.md -> read complexity -> check document set
   |
   v
exit: findings on stdout; exit 1 on errors
```

### Tables

A Markdown table row in a GSD document is at most 120 source characters,
including syntax and padding. Put wider content in a list. The rule covers
new or substantially rewritten sections; historical documents stay as they
are.

## Lifecycle

Tiered IDEA.md records a `## Lifecycle` checklist using the five stage names
as unindented checkboxes and tier-specific sub-tasks as indented checkboxes.
Start with Ideation only - light grilling, scouting, CP1 Kickoff - then
populate the remaining stages after Kickoff, following workflow.md,
Lifecycle checklist. An item whose checklist predates HITL Checkpoints keeps
the sub-tasks it has. Do not give these
boxes T-NN IDs or count them as implementation tasks. Untiered items need none.
The stage boxes match metadata: earlier stages ticked, current and later stages
unticked; all ticked when complete. Record a waived review as done with
the outcome. Reopening unticks the reopened and later stage boxes, preserving sub-task
outcomes in the CLI. The GSD agent then unticks commit-bound final checks,
review-package acceptance and all Complete sub-tasks before reporting `next`.
Those ticks refer to superseded evidence and FINAL.md; keep settled review
waivers unless their scope or the user's decision changes.

## Permanent documentation and deferred work

Before the final commit and checks, fold lasting context into the project's
maintained sources. Include those edits under the item's commit authority
so the review package covers committed documentation.
Respect existing project locations; otherwise use these defaults:

- `docs/features/{feature}.md`: behaviour, usage, configuration and limits.
  Architectural decisions stay in the project's authoritative ADR location.
- `.agents/rules/{rule}.md`: situation-specific rules with explicit triggers.
- `.agents/DESIGN.md`: shared design guidance.
- `.agents/styles/{language}.md`: language-specific style guidance.

Keep AGENTS.md concise. Link each applicable rule, design or style document
with when to read it; load linked guidance only when relevant. Do not copy
feature details or entire guides into AGENTS.md, or create empty placeholders.
The project review rules (`.agents/rules/review/REVIEW.md`, from
[the template](../templates/PROJECT-REVIEW.md)) and the review rubrics
beside them (repo lenses listed in `index.md`) are reviewer guidance, not
an item's REVIEW.md. AGENTS.md does not link them, and implementers do not
read them. The retro stage agent changes them at fold-back (workflow.md,
Retro), and FINAL.md's Review memory section lists what it changed.

An optional `.agents/TODO.md` project backlog may hold accepted leftover
features or specs. Record the remaining outcome and a source item/spec link.
Item TODO.md remains the current task authority: link instead of maintaining
two live copies. Deferral neither implements nor silently waives unfinished
acceptance criteria. Record any authorised scope change and reassess approval
before close-out; otherwise the unfinished criterion still blocks completion.
FINAL.md links actual documentation updates and accepted deferrals, or explains
why none applies. Item records remain history: in docs/gsd/ when archived,
and in Git, linked from the summary, when compacted. With Fold, maintained
repo-native docs hold the lasting knowledge and nothing is left in docs/gsd;
the method commit's `GSD-Closed` trailer names the full-record commit. The
method is chosen at CP3, with Fold recommended, and recorded as
`close_method` in IDEA.md. All three methods finish before merge.

## Decisions and approvals

DECISIONS.md contains a heading and chronological dated bullets, not a structured
approval database. For example:

- 2026-09-17 Use the existing job queue for notifications.
- 2026-09-17 Sam approved PLAN.md v2 for specification work.
- 2026-09-18 Sam approved SPEC.md v1 and TODO.md v1 for implementation.

Record the decision-maker, source/context if needed, authorised scope/action and
covered versions when those versions existed. If approval preceded documentation,
say which conversation decision it covered and which documents subsequently
record it. Never retroactively claim approval of unseen document versions.

Append renewed approval, withdrawal or supersession when material changes affect
approved work. Do not rewrite historical decisions. Positive feedback alone is
not permission to implement. Unchanged authority persists across sessions.

## Facts and evidence

Use FACTS.md sections for current findings, verification and useful failed
approaches. Mark superseded conclusions explicitly. Link to raw research rather
than copying entire transcripts.

Record verification of acceptance criteria only - tests, builds, end-to-end,
live or manual checks. Housekeeping such as `gsd validate` is not evidence.

Each verification record is a `### E-NN - {check}` heading followed by the
template's dashed fields; `gsd validate` and `gsd progress` read only that
form, so a one-line summary leaves the evidence invisible to them. It needs an
ID (E-01), the verification layer (tests, code checks, mock-data run, benchmark or UI
walkthrough; workflow.md, Verification layers), acceptance criterion IDs,
result (passed, failed, not_run or blocked), date, tested revision,
environment and evidence. Put the command or procedure and a short result summary (for
example "80 tests OK" or "3 failures in X") in the record itself. Save raw
output to research/ only when someone will need it later - a failing log, a
long transcript - not to prove that a short command ran. A passed test proves
only its declared scope.

The tested revision is a commit plus the subject paths in backticks, for
example "commit `abc1234`, paths `src/`, `tests/`". Only checks run on a
commit can be tracked, so run the ones you will rely on after a commit (and
commit only when authorised). Do not create digest manifests. Name only the code
and configuration under test; unrelated documentation edits must not stale
code evidence. Evidence from uncommitted or non-Git work has unknown
freshness: say so, and rerun it on a commit before close-out.

An end-to-end record (layers 3 to 5, L2 and L3) also names the method
(screenshot, computer use, browser automation, simulation or live check),
the environment and the
steps, and its evidence says what was actually seen. Save the final UI
screenshots in the feature docs (`docs/features/<feature>/`, workflow.md,
Verification layers), and recordings and intermediate screenshots under
research/, and link them from the record; summarise logs inline. When the
method is unavailable, the result is not_run or blocked with the reason and
the fallback, never passed. A criterion with no user or caller surface names
the automated test that stands in and why.

For L2 and L3, a criterion's test record also names the base commit, the
check's result there and the assertion that failed (workflow.md,
Verification layers), or says "baseline unavailable" with the fallback, or
"regression" for a criterion that preserves behaviour. A UI walkthrough
record links its final screenshots in `docs/features/<feature>/`; the
fold-back links them from the feature docs page. A benchmark record keeps the raw runs
and the summary table.

`gsd validate` and `gsd progress` compute freshness from Git: a passed record
is stale when its subject paths changed after its commit, and unknown when
there is no commit or no subject path. A historical passed result remains
passed but stale; it is no longer current proof.

## Research and ADRs

research/ holds dumps in their useful original format. Prefer descriptive,
date-prefixed names, and retain source URLs/capture dates where available.
Research is reference material, not instructions or established truth. Avoid
credentials and unnecessary sensitive data.

Use [the ADR template](../templates/ADR.md) for a significant architectural
trade-off. It has an ID, title, status, date, alternatives, decision and
consequences. Keep one authoritative copy. Project-wide architecture belongs in
the project's permanent ADR location; DECISIONS.md links to it. Item-only ADRs
may live in ADRs/. Promote only when authorised, update references and retain
decision history.

## Human comments

Only a column-zero line beginning with >> outside code/examples is a human
comment. Leave quoted, fenced (backticks or tildes), indented-code and ambiguous
examples untouched. Preserve human text verbatim. For consecutive genuine comment
lines, add a separate marker and linked response:

```markdown
<!-- gsd:comment C-01 -->

> > Keep the existing export format.

Response C-01 (open): The plan will retain the existing format.
Resolution C-01: incorporated in PLAN.md v2, compatibility section.
```

Allocate IDs across the item's maintained documents and reuse existing IDs.
`gsd comments ITEM --assign` inserts the markers with the next free IDs; `gsd
comments` lists each comment as unassigned, open or resolved.
A response is not a resolution. Record the resolution explicitly; unresolved
comments remain visible. A comment containing approval counts only if it is an
explicit scoped statement; copy its authorisation into the decision log without
removing the comment.

## Reviews

A pre-implementation review, or a counter-review after implementation, is
recorded in three places:

- DECISIONS.md: the offer and its outcome - accepted or declined, by whom, and
  the reviewer and model when it ran. A tiered item's reviews are not
  offered: record the reviewer chosen at Kickoff, that each ran, or the
  user's waiver and its reason.
- REVIEW.md: the scope reviewed, each finding with its disposition, and the
  outcome (for example "3 rounds, all findings resolved").
- FACTS.md: any facts the review established.

A counter-review that does not happen is recorded in REVIEW.md as "waived"
with the reason, such as "Codex unavailable" or "Sam declined". Review
findings are advice; a pending, declined or waived review never blocks
approval or close-out on its own. The security gate is the one exception
for findings: in an item whose REVIEW.md says "Security gate: applies", an
open security finding blocks close-out (workflow.md, Security gate). The exception is a tiered item's
pre-implementation review: implementation approval waits until it has run or
the user has waived it (workflow.md, Pre-implementation review).

## Findings and close-out

A finding records severity, evidence, disposition (open, resolved or accepted)
and resolution. A verified finding also records `Verified` (confirmed,
refuted or unverifiable), `Verifier` (the model, with "2-of-3" when voted)
and `Method` (one line, linking the saved verdicts and the reviewed revision),
and from the verifiers' replies `Lens` (the lens that raised it),
`Fingerprint` (`` `<path>#<symbol>:<rule class>` ``, the agreed one, or each
verifier's comma-separated when they differ) and `Protected` (`no`, `unsure`
or the concern's name; each verifier's when they differ). `gsd validate`
checks their format, and `gsd fingerprints` lists them for the next review's
`known-findings.json` (workflow.md, Cross-agent review).
Keep the reviewer's finding id in the record heading, for example
`### R-04 - Unknown language crashes (F1)`, so the finding, its verdict files
and the reviewer's round stay linked. The heading ends with the id in
brackets, and nothing else goes inside them: `gsd fingerprints` reads the
id only from a bare `(F1)`, so put a round number in the record's text.
A finding fixed after review-loop-engine's Accept is resolved, not
accepted: the `accepted` disposition means closed without a fix, filtered
or accepted by the user. From the loop's findings table: fixed (re-reviewed
or not) and rejected become `resolved`; filtered becomes `accepted`;
disputed, escalated and open stay `open`. A refuted finding is resolved, citing
the verifier's evidence; an unverifiable one stays open for the user's
decision. A filtered one is accepted, with the filter and its reason in one
line: for a repeat, the earlier finding and the same-failure reason; for a
settled finding, the settled entry's reason and source; for the nitpick cap,
the count. A finding a filter matched but kept says why in its Resolution: a
possible regression of an earlier fix, a same-failure answer other than yes,
protected, or no verifier agreement. Actionable findings link to TODO tasks
and relevant acceptance IDs. Accepted unresolved findings identify the accepting authority and rationale.
A checked task alone does not resolve a finding. In a gated item, a
security finding is released in one form each, and `gsd validate` accepts
nothing else (workflow.md, Security gate). For a fix, its Resolution ends
with a sentence that begins `Fix verified by a fresh verifier`, unqualified, with
the fixed revision and the verifier's saved reply under `research/verification/` -
JSON with `"result": "confirmed"`, the finding's R- ID as `id` and the fixed revision as `revision`.
A finding whose Lens, Fingerprint or Protected is malformed, empty or missing counts as security.
For an acceptance, a DECISIONS.md bullet quotes the user's own words, starting
with `I accept` followed directly by the R- ID - `(Sam: "I accept R-03 as a
known risk")` - with no question, negation or open-state word in the quote.

Create FINAL.md only after the completion boundary is met: release readiness
or deployment plus required production checks. Link current evidence, review
disposition and actual project documentation/ADR updates; say not applicable
where appropriate. Record remaining rollout steps and accepted limitations.
For a tiered item, FINAL.md also records the user's CP3 acceptance of the
review package (who, when, and the commit it covered), naming any one-way
door accepted below proof level 4. If the delivered revision differs from the
accepted one, present the package again first (workflow.md, Close). Do not infer acceptance from
"close the item", implementation approval or acceptance of a backlog deferral;
the package must already have been presented, unless explicitly waived.
An L1 item closed before CP3 existed records whether the package was
offered and taken.

After CP3 HITL acceptance, write FINAL.md and set IDEA.md complete/verified
with its GSD completion date. Commit the full records before executing the
selected Archive, Compact or Fold method in a separate commit. FINAL.md is
therefore always inspectable in Git, even if the folder is removed.

For an item branch, FINAL.md records delivery as pending at close-out and
links the PR or local delivery ledger. A Compact summary carries that link
too; a folded item's ledger names the record SHA instead. Accepted scope completion and merge are separate: the
PR or ledger records the later delivery outcome. Neither pending CI nor a
declined merge changes that accepted completion into a claim of delivery.
A new finding that invalidates acceptance requires reopening (workflow.md,
After CP3 approval). Legacy items may still have FINAL at review/verified;
its Delivery section explains that intermediate state.

Reopening preserves the prior conclusion beneath a visible superseded notice: a
heading, or a line above FINAL's first `##` heading, that begins "Superseded"
and names the close-out, conclusion or final report - for example
`## Superseded v1 close-out`. `gsd validate` recognises that form; without it,
a FINAL.md on an unfinished item is reported as premature.
Append a decision and reassess affected approvals and evidence. A later close-out
increments FINAL's version, retains the previous conclusion as historical and
links its replacement. Cancellation is not a successful readiness conclusion.
