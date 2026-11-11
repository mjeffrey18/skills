# Workflow

Choose the requested stage; do not mechanically restart at the beginning.
Read documents.md for record formats and templates, and complexity.md for
tiers.

## Explicit branch delivery

For an existing item, a user's explicit `full-send` or `full-stop` invocation
selects the [shared branch delivery procedure](../../full-send/references/delivery.md).
This section takes precedence over the default CP3/CP4 acceptance, branch
deletion and final delivery sequence in this document and the GSD entrypoint.
It does not invoke either skill automatically.

Both modes authorise task-scoped close-out commits and pushes and delegate CP3
package acceptance, conditional on required reviews, current verification and
security gates. Full-send also delegates CP4 merge acceptance under those
conditions. Full-stop requires human acceptance of the exact head/base package
before merging; changed heads or substantive new findings require fresh
confirmation. Record the user's actual instruction as conditional delegation,
not as review of an unseen package. CP1/CP2 approvals and scope remain intact.
An untiered item gains commit/push authority only for the explicit delivery task.

Close the GSD item before CI and merge: write and commit FINAL with delivery
pending, then commit Archive, Compact or Fold (default). An explicit delivery
invocation delegates CP3 acceptance; reuse an explicit close-out method, otherwise
use Fold and record that default. This does not claim the branch has merged.
Do not wait for a GitHub review, but address existing PR findings and fetch comments again after green CI. Required internal
reviews and repository protection still apply. Use three 15-minute pending-CI
windows with intervention on failure or the third timeout; a host without a
supported timed wake is a reported prerequisite before publication, not an
unbounded wait. Comment-driven repairs share the three-cycle CI repair budget.

Merge with `gk ff`, inspect the merge parents, then explicitly push and verify
the base. Linked tasks transfer the tested feature to the clean idle canonical
checkout after detaching their task checkout; do not park a foreign checkout.
Without a remote, use the local Git rebase/merge path and skip remote calls.
Keep both feature refs: do not use `gk ff!` or default deletion steps.
Finish GSD close-out before merge and verify publication before removing a
task-owned `t3-*` worktree with `gk wt rm`, or parking a normal worktree on
`park/<worktree-name>` without moving its directory. Preserve local-only data.
Permission denials, deployment/spend boundaries and unresolved security
findings retain their existing treatment. The shared procedure owns the full
comment, CI, readiness, cleanup and partial-failure rules.

## Tiers

An item is tiered when IDEA.md has the front-matter field `complexity` set
to `L1`, `L2` or `L3`. The tier sets the document set, grilling depth,
diagrams, reviews, approvals and verification; complexity.md lists them per
tier. An item without the field is untiered and follows the untiered path
below: the rules that predate tiers, unchanged. Do not add a tier to an
existing item unless the user asks.

### Stages and files

| Stage | Step | Files created or updated |
| --- | --- | --- |
| ideation | Light grilling, scouting, CP1 Kickoff | IDEA.md, DECISIONS.md; FACTS.md, research/ when useful |
| planning | The tier's full planning set, topology and verification plan | IDEA.md, PLAN.md, SPEC.md, TODO.md by tier |
| planning | Plan review; CP2 Pre-implementation | DECISIONS.md, REVIEW.md, FACTS.md |
| execution | Implementation and checks | Code, TODO.md, FACTS.md |
| execution | Checkpoint and simplification | Code, TODO.md, FACTS.md, DECISIONS.md |
| review | Counter-review, verification and documentation fold-back | REVIEW.md, FACTS.md, project docs, TODO.md |
| review | Final checks, draft PR and CP3 Review | FACTS.md, DECISIONS.md, REVIEW.md |
| complete | After CP3: FINAL.md committed, then Archive, Compact or Fold committed | FINAL.md, IDEA.md, project docs |
| complete | With an item branch: rebase, push, PR ready, CI, CP4 Merge | PR and delivery ledger |

Update IDEA.md lifecycle metadata and checklist at each step. Decisions, facts,
comments and handoffs may be recorded at any step when needed. L1 has no
PLAN.md; L2 has an optional SPEC.md; L3 requires both.

### Lifecycle checklist

A tiered IDEA.md has a `## Lifecycle` checklist. Use the five stage names as
unindented checkboxes, with indented sub-task checkboxes and no T-NN IDs.
A new item starts with only the Ideation skeleton - light grilling, scouting,
CP1 Kickoff - and `next` shows those steps even before a tier is recorded.
After Kickoff, fill the remaining stages with the tier's sub-tasks below.
Untiered items do not need this checklist and retain the earlier rules.

An item whose checklist predates HITL Checkpoints keeps it: the checklist is
the item's contract, so follow the sub-tasks it has rather than rewriting
them. For example, its "Tier confirmed" and "IDEA approved for planning"
sub-tasks stand where CP1 Kickoff stands in a new item.

Ideation sub-tasks: light grilling (or already settled), scouting, CP1
Kickoff. The rest depends on the tier:

- L1 Planning: IDEA goal, criteria, tests, tasks and topology; planning set
  committed; pre-implementation review, each round committed; CP2
  approval of IDEA.md.
- L2 Planning: PLAN with diagrams, acceptance, topology and verification
  plan; TODO; SPEC when the work needs it; planning set committed;
  pre-implementation review, each round committed; CP2 approval of PLAN
  and TODO.
- L3 Planning: PLAN with diagrams, topology and verification plan; SPEC and
  TODO; planning set committed; pre-implementation review, each round
  committed; CP2 approval of PLAN, SPEC and TODO.
- Every tier Execution: implement through the approved topology (for L3,
  with the smoke review when PLAN names one); run criterion checks;
  checkpoint committed; simplification committed.
- Every tier Review: counter-review, each round's fixes committed;
  security review when the gate applies (Security gate);
  verification layers recorded; documentation fold-back and retro committed,
  with the retro review when the retro changed anything; accepted
  deferrals recorded; final checks on final commit; CP3 review package
  accepted. An item with an item branch adds draft PR opened (before CP3)
  and the close-out method accepted at CP3.
- Every tier Complete: completion boundary met; FINAL written with delivery
  pending where applicable; metadata closed; full records committed; then
  Archive, Compact or Fold committed (Close-out method). These steps finish
  before an item branch enters CI or CP4. Completion means the accepted GSD
  scope is finished; it does not mean merged or deployed. Track delivery
  separately in the PR and delivery ledger. Do not leave merge sub-tasks
  unticked in a closed IDEA: put the remaining delivery steps in that ledger.

Keep the label "Pre-implementation review" at the start of that sub-task:
while it is the next step, `gsd next` reports the agent, not the user, as
the one to act. Tick each sub-task as it finishes. Replace generic
placeholder steps with the tier's actual actions; keep unfinished approval
sub-tasks open.
Tick a review with its outcome, for example
`- [x] Pre-implementation review - Codex Sol, 2 rounds` or
`- [x] Counter-review - waived (user declined)`. Tick a stage only after all
its sub-tasks are ticked and the item moves on; every earlier stage is ticked,
the current and later ones remain unticked, and complete has all five ticked.
Promotion re-scopes open sub-tasks and preserves settled ones. `gsd validate`
reports `lifecycle-missing` or `lifecycle-stage`; `gsd next` shows the first
unticked sub-task. `gsd reopen` unticks stage boxes from the reopened stage onward, preserving
settled sub-task outcomes. Reassess which checks need repeating after reopening.
The CLI does not count lifecycle checkboxes as implementation tasks.

### HITL Checkpoints

A tiered item stops for the user at three HITL Checkpoints, on every tier;
an item with an item branch adds a fourth, CP4 Merge, before anything
reaches the base. Grouping the questions means the user decides everything a stage needs in
one sitting, and the work between checkpoints runs without waiting on them.

```text
ideation   light grilling -> scouts -> tier + IDEA draft -> [CP1 Kickoff] -> item branch -> commit item records
planning   planning set + topology + verification plan -> commit -> plan review, commit per round
           -> [CP2 Pre-implementation] -> commit CP2 decisions
execution  implementer per topology -> checks -> checkpoint commit -> simplify -> commit
review     counter-review, commit per round -> verification -> fold-back commit -> final checks
           -> push the item branch, draft PR -> [CP3 Review] -> feedback: fix, commit, push, PR body, CP3 again
complete   CP3 accepted -> FINAL.md + closed IDEA -> full-record commit -> Archive | Compact | Fold commit
delivery   rebase -> checks -> push (lease if rewritten) -> PR ready -> CI (fix loop, at most 3)
           -> base moved? rebase, checks, push, CI -> [CP4 Merge] -> merge -> push the base
           (without an item branch: finish at the close-out method commit)
```

How to ask: put all the checkpoint's questions at once through the
harness's interactive Q&A tool (`AskUserQuestion` in Claude Code,
`request_user_input` in Codex), up to 4 questions per call with the
recommended answer first. Without such a tool, end the turn with a numbered
list, each question with its default. "go" accepts every default. Before
the questions, say where the item stands, what each answer decides and what
happens next without another stop.

Between checkpoints, ask only when no approved work can continue - a
blocked check, an escalation from a review loop, a premise that failed
twice. A question that can wait goes to the next checkpoint. Every summary,
at a checkpoint or not, ends with one "Next:" line naming one action in
plain words.

**CP1 Kickoff**, at the end of ideation (Start or clarify):

- the tier, with one reason for each of Risk, Change and Confidence, each
  named (complexity.md), never below the Risk floor scouting reported from
  the project review rules. When there is a floor, state it as the Risk
  floor with the rule that set it (`always_high`, or the `risk_paths` tier)
  and the path it matched, for example "Risk floor L3: `always_high`
  matches `auth/tokens.py`";
- IDEA.md - approve it for planning, change it, or grill deeper; L3 runs its
  full grilling inside Kickoff, before the approval;
- the reviewer and model for the plan review and the counter-review
  (Cross-agent review);
- overlap with work in progress that the scouts found, if any;
- the stage-agent overrides in use, from `gsd agents --all` (any agent with
  a `user` or `repo` source);
- for L2 and L3 in a repository without project review rules
  (`.agents/rules/review/REVIEW.md`), whether the retro may create them at
  close-out (Retro) - recommend yes. Not asked for L1, nor when the file
  exists. A legacy `REVIEW.md` (a stage agent or an indexed lens, as `gsd
validate` reports) is not project review rules: name the collision and
  its migration step instead of asking.

A change or a deeper grilling round loops back to the IDEA draft and asks
Kickoff again. On approval, record the tier, the IDEA approval ("approved
IDEA.md vN for planning") and the other answers in IDEA.md and
DECISIONS.md, create the item branch (Item branch), then commit the item
records on it (Commits). No planning document is written before Kickoff
approval.

**CP2 Pre-implementation**, after the tier's full planning set and the plan
review (Plan): approve the reviewed set - IDEA.md for L1, PLAN.md and
TODO.md for L2, PLAN.md, SPEC.md and TODO.md for L3 - with the topology and
the verification plan. Present with it the one-way doors, the findings still
disputed after the review and the two-way-door choices the agent settled, so
the user can change any of them. Approval authorises the item-scoped commits
through to CP3 and the counter-review (Commits). Record it as "approved
PLAN.md vN ..." (Approval). A change revises the documents, reruns the review
on the changed ones and asks CP2 again.

**CP3 Review**, after the counter-review, verification, final checks and
the draft PR (Draft PR): the review package (Close), on every tier, plus
the close-out method: Archive, Compact or **Fold (recommended)** (Close-out
method). Explain what each option keeps and, for Fold, show the fold map:
each fact to keep, its destination page and section, and why. Record the
answer as `close_method` in IDEA.md. Reconfirm an earlier choice here; do not silently override it. A bare
"go" accepts the presented default, Fold unless the user already chose another
method. Do not ask "now or after merge". When
the item has a draft PR, CP3 asks once the PR exists and adds:

- the work in the draft PR - approve it, or give feedback (link the PR);
- staging QA, only when `~/.agents/rules/deploy/staging.md` or the
  repository's deploy docs describe a staging deploy - otherwise not asked
  and not named. The question names every branch that procedure pushes;
  a yes covers only those pushes. Afterwards check out the item branch
  again and rerun the final checks before going on;
- approval to rebase the item branch on the base and push it after
  approval, with a lease if the rebase rewrites pushed commits (After CP3
  approval). Recommend yes.

Feedback is fixed and committed under CP2's authority; the final checks
rerun on the new commit; the orchestrator rewrites the PR body for that
commit and runs the pull-request agent again, which pushes by explicit
refspec (Pushes) and updates the body with `gh pr edit <number>
--body-file <body>`; then the package is presented at CP3 again, until the
user approves. A PR body that still names the old final commit is stale. Without a draft PR, feedback is fixed,
committed and presented again the same way, without the push.
Approval concludes the CP3 HITL checkpoint. Record the accepted revision,
method and other CP3 decisions in DECISIONS.md. It leads directly to FINAL.md
and the full-record commit, then the chosen close-out method in a separate
commit, without another stop (After CP3 approval). Only then may branch
delivery continue. If CP3 is not accepted, do not write a successful FINAL
or close the item.

**CP4 Merge**, with an item branch, after CI is green or skipped (CI) and
the base-moved check (CP4 Merge): show what changed since CP3 - CI fix
commits, rebases, with the new head - and ask:

- accept that head and merge it into the base - recommend yes when CI is
  green; say when the PR has no approving review: merging is the user's
  call within their PR permissions, and GitHub enforces any required
  review;
- nothing else: the GSD item is already closed using the CP3 method.

A yes covers the merge, the base push and then deleting the item branch
(CP4 Merge). A no or blocked CI leaves branch delivery pending; it does not
undo the accepted GSD close-out (After CP3 approval).

The L3 smoke review stays an extra stop, only when PLAN marks one (Smoke
review). Untiered items keep the earlier rules (Pre-implementation review,
Approval).

### Commits

A tiered item commits only its own paths - its records and, from execution
on, its changed code and documentation - on its item branch (Item branch),
never other writers' changes. It pushes only the item branch, under the
guards in Pushes. Each commit marks a point the user can inspect or revert
to:

1. after CP1 Kickoff: the item records;
2. the planning set, before the plan review;
3. one commit per plan-review round, with that round's fixes;
4. the CP2 decisions and any changes the user asked for;
5. the checkpoint, the simplification and one commit per counter-review
   round (Checkpoint, simplify and counter-review);
6. the documentation fold-back;
7. after CP3 acceptance, the full-record close-out including FINAL.md, then
   Archive, Compact or Fold in its own commit on the item branch;
8. any CI fixes and delivery-ledger updates on the item branch. The tested
   merge includes the closed GSD item; no close-out commits follow it.

A review round always changes REVIEW.md, so it always has a commit, even
when it found nothing to fix.

Kickoff approval covers the item branch and commits 1 to 3; CP2 approval
covers the rest and the pushes of the item branch (Commit authority).

### Item branch

After CP1 approval the agent puts the item on its own branch before the
first commit, so its commits never land on the base or on another feature.

The base is `develop_branch` from `.gitkiss.jsonc` when it is set, else its
`main_branch`; without that file, the repository's default branch as Git
records it (`origin/HEAD`, or without a remote the local `main` or
`master`). If none of these settles it, the base is a Kickoff question.
Never take the base from GitHub's default branch alone: a repository can
set another base in `.gitkiss.jsonc`. The branch is `feature/<name>`, where
`<name>` is the item folder without its date.

First check `git status`: if it shows uncommitted changes outside the item
folder, stop and ask, because the switch would carry another writer's work
onto the item branch; never stash or discard it. Then choose the first path
that applies:

1. **gk** - the `gk` CLI responds (`gk version`), the git-kiss skill is
   available and the repository has a remote. Set the item folder aside, so
   nothing else moves: `git stash push -u -- <item folder>`, then
   `gk nf <name>` and `git stash pop`. gk may add initials to the name;
   record the branch it created (`git branch --show-current`). gk reads
   its base from layered configuration, personal overrides included, and
   no gk command prints the base it used, so check the outcome: after
   `git fetch origin <base>`, `git rev-parse HEAD` must equal `git
rev-parse origin/<base>`. If it does not, stop and say so: gk branched
   from another base, or the local base has commits of its own. With the
   user's go, recreate the branch with `git switch -C <branch>
origin/<base>` (gk's branch has no commits yet) and record in FACTS.md
   that the item uses plain git, so every later step takes the plain-git
   path.
2. **Plain git with a remote** - `git fetch origin <base>`, then
   `git switch -c feature/<name> origin/<base>`. The uncommitted item
   records come along. If the switch would conflict, stop and ask.
3. **No remote** - `git switch -c feature/<name> <base>` from the local base,
   with no fetch or pull. Name every later step that needs the remote (push,
   draft PR) as skipped in the review package; do not ask about them.

Either way the branch starts from the base, not from whatever is checked
out: a Kickoff started on another feature branch still branches from the
base. Record the result in IDEA.md `branches` - the item branch first, then
the base as `"base: <base>"`, for example
`branches: ["feature/greet-languages", "base: main"]` - and commit it with
the item records. If the item already has a recorded branch (a resumed
item), check it out instead of creating another.

### Pushes

A tiered item pushes only its own item branch, after CP2 approval, and only
to deliver it as a draft PR (Draft PR) and keep that PR current. Before
every push:

- Name the remote and one refspec whose destination is the item branch
  recorded in IDEA.md `branches`:
  `git push origin refs/heads/<item branch>:refs/heads/<item branch>`.
  Check the destination against IDEA.md before running the command,
  whatever is checked out. Write the branch names out in the command, not
  through shell variables: the permission hook checks the command as
  written, and zsh reads `$B:r...` as a modifier and mangles the refspec.
  Never push without a refspec, `HEAD`, a wildcard or several refspecs.
- Push with that git command on the gk path too: the permission hook and
  reviewers can only check a push whose refspec is written out. gk is used
  only for `gk nf`, `gk rf` and `gk ff`; never `gk pf`, `gk pr`, `gk ff!`,
  `gk ds`, `gk ds!`, `gk dp` or `gk dp!`.
- Refuse any push whose destination is the base or any other branch. The
  one exception is the CP4 merge
  (CP4 Merge): `git push origin refs/heads/<base>:refs/heads/<base>`, only
  after CP4's yes, only when the merge commit's first parent is the base
  fetched just before the merge and its second parent the tested head.
  Never force push the base.
- Keep the head of every successful push of the item branch; the last one
  is the agent's last pushed head, recorded in FACTS.md with the pushed
  heads.
- After a rebase (After CP3 approval, CP4 Merge), fetch the remote head
  first, so its commits are local: `git fetch origin refs/heads/<item
branch>`, then `git rev-parse FETCH_HEAD`. Then run `git merge-base
--is-ancestor <remote sha> refs/heads/<item branch>`:
  - exit 0 - the rebase rewrote nothing that was pushed: push by explicit
    refspec, without force. A force push asks the permission hook, which
    often denies it, so never force a fast-forward.
  - exit 1, and the remote head is the agent's last pushed head - the
    rebase rewrote the agent's own pushed commits: force push the item
    branch with a lease bound to that ref and that head:
    `git push --force-with-lease=refs/heads/<item branch>:<remote sha>
origin refs/heads/<item branch>:refs/heads/<item branch>`. Never
    `--force`, `-f`, a bare `--force-with-lease` or a `+` refspec.
  - exit 1, and the remote head is not the agent's last pushed head -
    another writer pushed to the item branch: stop and ask. Never force.
  - any other exit - the check failed, not "not an ancestor": stop and say
    so.

Some harnesses deny a push, a force push or a remote branch delete through
the permission hook (in Codex the hook turns an ask into a deny). When that
happens, stop: print the exact command for the user to run and ask them to
say when it is done. Do not try another way round the denial - no
`--no-verify`, other flags, another remote or the GitHub API. After they
confirm, check the remote ref (`git ls-remote origin refs/heads/<item
branch>`, or the base after a CP4 push) against the local head before
continuing - for a delete, that the ref is gone - and stop again if it does
not match.

### Stage changes

At a stage boundary, consider in order: continue in the same session; clear
context if it is large; hand off only when the harness, directory or person
changes; use a subagent for unattended work when permitted; compaction last.
Continue by default because a summary loses reasoning. This is a guide, not a
gate or permission to discard required context or delegate without authority.

## Start or clarify

Inspect the repository and current work first. Establish purpose, scope,
constraints and completion boundary from available context. Keep accepted
decisions settled. Create IDEA.md with ideation/proposed initially unless
evidence supports a later stage. Add facts and decisions as they arise. Do
not create eight empty files. Do not silently enrol or rename legacy
documentation.

For a new item, unless the user asks for an untiered item:

1. Light grilling: one short round that settles the outcome and how success
   will be judged. Ask only what the repository cannot answer, but always
   ask how success will be judged unless the request states it. Skip the
   round when the request already settles both.
2. Scout: run the idea-stage agents in parallel - resolve them with
   `gsd agents idea` and hand each its brief from
   `gsd agents idea <name> --body` (specialists.md, Stage agents).
   scout-codebase finds what already exists, where the change belongs and
   what it touches; scout-prs and scout-worktrees find overlapping work in
   progress; reproduce runs only for a bug item. Record their findings in
   FACTS.md or the IDEA.md scope, and keep overlap for Kickoff. For L2 and
   L3, save scout-codebase's dated research snapshot under research/ - the
   files, line references and how the code works today - and link it from
   FACTS.md. Regenerate it when stale from current code rather than
   maintaining it by hand.
3. Tier and IDEA draft: score Risk, Change and Confidence with complexity.md,
   propose a tier with one reason per dimension, and draft IDEA.md. Risk is
   never below the Risk floor scout-codebase reported from `gsd risk`
   (complexity.md, Risk).
4. CP1 Kickoff (HITL Checkpoints): ask the Kickoff questions together. For
   L3, run full grilling inside Kickoff, then ask for the IDEA approval. The
   user confirms or changes the tier. Record the confirmed tier in IDEA.md
   (`complexity` and the Complexity section) and the IDEA approval in
   DECISIONS.md, for example "Sam approved IDEA.md v1 for planning", then
   fill the Lifecycle checklist and commit the item records.

Without tiers, use grilling only for unresolved material choices or an
explicit request to stress-test the idea.

For a bug item, the reproduce agent runs a failing reproduction command for
the user's exact symptom; record the command and observed failure in
FACTS.md. It lists 3-5 ranked hypotheses that a test could disprove before
testing any. If the symptom cannot be reproduced, record the limitation and
settle the reproduction route at Kickoff rather than inventing a failure.

## Resume

Resuming an existing item in a fresh session or a different harness starts
from the persisted documents, not from memory of the earlier conversation.
Read IDEA.md for stage, delivery, tier and scope, DECISIONS.md for the
approvals that already exist, then only the documents the requested step
needs. Report the current position and the next authorised action. If the
item has a handoffs/ folder, read its newest non-superseded handoff for where
the last session stopped; the item documents stay authoritative. Do not
repeat the interview, re-request approvals already recorded, or restart
settled discovery. If the documents and the request disagree about scope,
surface that before writing.

## Plan

Write the tier's minimum documents (documents.md, Document sets). Set stage
to planning. For a tiered item, planning runs from Kickoff approval to CP2
without a stop: write the whole set, then review it.

- L1: complete IDEA.md with Goal, Success, Tests, TODO and Topology
  sections. There is no PLAN.md.
- L2: write PLAN.md, with Diagrams, Acceptance, Verification and Topology
  sections, and TODO.md. Add SPEC.md or other records only when the work
  needs them.
- L3: write PLAN.md, SPEC.md and TODO.md as one set (see Specify).
- Untiered: write PLAN.md, then SPEC.md and TODO.md after plan approval (see
  Specify).

With the set, a tiered item settles three things the user approves at CP2:

- Two-way-door choices: decide them and list each in PLAN.md (IDEA.md for
  L1) with its reason, rather than asking. A revert undoes them, so the
  user's time is better spent on the list at CP2. One-way doors (Doors) stay
  open for CP2.
- Topology: the orchestrator, the implementer subagents with provider and
  model, and the reviewers (specialists.md, Stage agents). The default is
  one implementer subagent on the same provider and model as the session.
- Verification plan: the layers each criterion needs (Verification
  planning).

Then commit the planning set (Commits) and run the pre-implementation
review.

Investigate the implementation paths first. Select a compatible planning
skill when available. Preserve any required planning-agent route imposed by
the harness. Give it the settled scope and exact output destination. In a
read-only mode, return the plan in the conversation and state that
persistence requires a mode permitting edits; a custom tool is not a bypass.

### Program design and slices

For L3, and L2 interface changes, PLAN.md has a Program design section. Start
from the caller's view: show usage before shape, then the new or changed
types, function signatures and call paths. L1 skips it. Order the Sequence as
vertical slices that each run end to end; end each slice with a named check
before starting the next. Do not split into disconnected technical layers. An
L3 Sequence may mark one slice for a smoke review (Smoke review).

### Fit and operation

For L2 and L3, PLAN.md has a Fit and operation section, with the template's
five labelled lines: the project patterns
the change follows (or why it departs from them), the likely next change and
how the design takes it, the failure modes, the logs and metrics that show
them, and the rollback signal. The `plan` lens checks it; the `operability`
lens checks the build against it.

### Diagrams

For L2 and L3, draw ASCII diagrams in PLAN.md before any code is written.
They show the layers or components involved, the entry points (commands,
routes, hooks, events), the execution path and the exit points (outputs,
side effects, error and rollback paths). Label entry, execution and exit
explicitly. documents.md lists the diagrams each tier needs. Update a diagram
when the design changes; reviewers check it against the implementation.

### Verification planning

For every tier, name the automated test (unit, integration or scenario) that
exercises each acceptance criterion: in the IDEA.md Tests section for L1, in
PLAN.md for L2, in SPEC.md for L3. For L2 and L3, also name an end-to-end
method for each criterion (Verification layers, layers 3 to 5), or say
which test stands in and why no end-to-end method applies.

The verification plan - PLAN.md's Verification section, or IDEA.md's Tests
for L1 - names the layers each criterion needs: tests and specs; code checks; a run
with mock data; a benchmark when the change is performance-sensitive; a UI
walkthrough with screenshots when it touches UI (Verification layers). For
a tiered item, verification also runs the layers the diff implies when the
plan omits them.

### Pre-implementation review

For a tiered item, the pre-implementation review is a default step, not an
offer. Once the tier's planning set is complete and committed, run the
plan-reviewer stage agent (`gsd agents plan plan-reviewer --body`) with the
reviewer and model chosen at Kickoff (Cross-agent review below); do not ask
whether the user wants one. A summary that names the review as the next
step names the reviewer and model too, for example "Next: run the plan
review with Codex (Sol)". The scope is GSD-supplied from Kickoff, so
review-loop-engine starts without its scope question. The review covers
IDEA.md, PLAN.md, SPEC.md, TODO.md, FACTS.md and DECISIONS.md as they
exist, and checks them against each other as well as on their own. Fold the
confirmed findings into the documents and commit each round's fixes on its
own, so each round's change to the plan is visible. Findings still disputed
go to CP2. A document changed after the review is named at CP2.

Skip it only on the user's explicit waiver, recorded with its reason in
DECISIONS.md and REVIEW.md. When no second CLI is available, say so and put
pi, review-local or a waiver to the user as one question - the one thing
that blocks planning; never skip it silently. Do not ask for CP2 while the
review is pending. An approval that comes with an explicit decline of the
review counts as the waiver; an approval that says nothing about it does
not - ask once whether the user means to waive the review.

For an untiered item, offer the review before SPEC and TODO approval, and
recommend a plan review before plan approval with a suggested plan PR for
peer review. Each is advice and never blocks approval.

Record the review or waiver in DECISIONS.md (reviewer, model and rounds, or
the waiver and its reason), the findings and their disposition in REVIEW.md,
and any facts in FACTS.md.

### Approval

Present the documents for approval unless scoped approval already exists.
Unapproved choices remain explicit. Every tier first approves IDEA.md for
planning at CP1 Kickoff; the approvals below are CP2 for a tiered item,
authorise implementation and follow the pre-implementation review or its
waiver. Record the first with the words "for planning" and the others
without them: `gsd next` counts an approval "for planning" only at
ideation.

- L1: approve the completed IDEA.md.
- L2: approve PLAN.md and TODO.md. An optional SPEC.md is reviewed with them
  but does not replace that approval.
- L3: approve PLAN.md, SPEC.md and TODO.md together.
- Untiered: approve PLAN.md, then SPEC.md and TODO.md.

For a tiered item, CP2 says that approval also covers the topology and the
verification plan, authorises the close-out commits and runs the
counter-review (Commit authority), so the user can change the topology or
opt out of either there. Record what the user chose, then commit the CP2
decisions.

## Specify

For L3, write SPEC.md and TODO.md with PLAN.md, before the
pre-implementation review. For untiered items, write them after plan
approval. Define observable acceptance criteria with stable IDs, legal edge cases and
the completion boundary. Name the test seams; for a tiered item the user
confirms them at CP2, for an untiered one confirm them with the user. Link
tasks to criteria. Record approval of implementation scope before execution.

The user can explicitly authorise a smaller workflow or instruct you to
document and implement an already agreed approach. Record that scoped
exception and proceed; do not introduce another gate for paperwork produced
under that instruction. This exception does not apply to vague praise or
planning-only asks.

## Promote

When the tier rises, move content into the new tier's documents with the
same AC and task IDs, as documents.md describes. Record the change and
reason in DECISIONS.md. A rise reopens approval of any document the new tier
requires that has not been approved, and the pre-implementation review runs
again over the new set. When new approval is needed, return to
planning/ready and untick Planning and later stage boxes. Add the new required
sub-tasks, preserve settled outcomes and pause execution until the new scope
is approved. A tier never drops silently; lowering
it needs the user's agreement.

## Execute

Confirm current scope and authority, then carry out approved work using
relevant implementation skills and tools. Set execution/in_progress. Update
task progress and facts with evidence. Material scope changes require
assessing the affected approval; continue unaffected approved work where
possible.

For a tiered item, implement through the topology approved at CP2: launch
the implementer subagent or subagents with the brief from
`gsd agents build implementer --body`, the slices each one owns and the
checks to run (specialists.md, Stage agents). The session orchestrates: it
checks the returned work, fixes in-scope failures and stays the only writer
of GSD records and the only one who commits. New questions wait for CP3
unless no approved work can continue.

Challenge a failing premise: when two fixes built on the same premise (an
assumption about the cause or the behaviour) fail the same check, stop.
Write the premise in FACTS.md and test it directly - a probe, a log line, a
minimal reproduction - before a third fix. Record the result: a disproved
premise goes under useful failed approaches with what replaced it.

When implementation is done, run each criterion's automated test. The
verification agent runs the planned layers on the committed code at the
Verify step (Checkpoint, simplify and counter-review). Use implemented
delivery until
current acceptance and review establish verification. Keep failures, skipped
checks and limitations visible.

### Smoke review

The smoke review is a hard checkpoint: the one planned stop for the user
during execution. An L3 PLAN.md may name one smoke-review point, usually
after the first vertical slice, so the user can catch a wrong direction
before later slices repeat it. When the slice passes its checks, commit it
(Commit authority) and stop. Present a short early review: what the slice
does, its checks and evidence, any departure from the plan, and the open
questions. Wait for the user's go-ahead, and record it or their changes in
DECISIONS.md; a change to the approved plan reopens that approval (Stage
changes). The user may ask for a cross-agent pass first. The smoke review
does not replace the counter-review. L1 and L2 items do not have one.

### Verification layers

The verification plan names the layers each criterion needs (Verification
planning). The verification stage agent
(`gsd agents review verification --body`) runs them in this order and stops
at the first failure, because a later layer proves little when an earlier
one fails. Layers 3 to 5 check the change end to end, as a user or caller
meets it.

The verifier first classifies the changed paths, and each class implies
layers: source code - tests, code checks and a mock-data run; tests only -
tests and code checks; migrations - all three, with a migration check;
configuration, routes or translations - code checks and a mock-data run;
UI files - a UI walkthrough; dependency manifests - code checks with an
install check; a hot path - a benchmark. The plan still names the layers.
For a tiered item, a layer the diff implies but the plan omits runs by
default: a diff touching views, components, styles or templates gets a UI
walkthrough, and one touching source code gets a mock-data run. It is
never skipped or added silently: its FACTS.md record says "added by the
diff" and names the paths that imply it, and the orchestrator adds it to
the plan's verification. A repository replaces or extends the verification
agent with `.agents/rules/review/verification.md` or `verification_N.md`
(Stage agents in specialists.md).

1. **Tests and specs.** Every criterion and edge case has an automated test,
   and the tests pass on the final commit. Gaps go back to the implementer.
   For L2 and L3, each criterion's test also fails on the old code. Run it
   on the base commit (the commit before the item's first change) and on the
   final commit, with the same check command. Apply the new or changed test
   to a temporary worktree at the base commit (`git worktree add`), run it
   there, then remove the worktree. The record passes only when the
   criterion's own assertion fails on base and passes on final. A test that
   passes on base proves nothing: rewrite it. A setup, import or build error
   on base is "baseline unavailable", recorded with a fallback check or the
   user's waiver - never as a pass. When the base lacks the interface under
   test (a new command, option or file), record "baseline unavailable" and
   name the fallback, such as a check of the old behaviour the change
   replaces. A criterion that preserves existing behaviour is marked
   "regression": its test passes on both commits, and the record says so.
   When the base run is unavailable or too costly, a mutation check stands
   in: snapshot the diff, break the new behaviour in the smallest way that
   matters, see the test fail, then restore and confirm the tree matches
   the snapshot byte for byte. A test that stays green proves nothing.
   Each behaviour the diff adds or alters - branch, guard, error path,
   default, side effect - maps to an assertion; the rest are gaps.
2. **Code checks.** The project's own lint, type, static-analysis,
   security, dependency-boundary, translation and generated-file checks, as
   AGENTS.md or its docs name them, and an install check when a dependency
   manifest changed. A load failure stops verification; other failures are
   recorded and the layer continues. A changed generated file that is not
   committed is a finding, and an autocorrecting linter's edits are listed
   for the author.
3. **Run with mock data.** Run the change and check its results - a scratch
   project, a dry run, a fixture environment or a replayed request. Data
   comes from the repository's fixtures or seeds, or the agent creates it
   and removes it afterwards; never real or production data. Call the entry
   point the way callers do and cover the edges: empty and missing input, a
   second user or tenant, dates across midnight, non-Latin or right-to-left
   text where text is shown, and large input. Stub anything that sends
   messages, charges or calls an external service.
4. **Benchmark**, when the change is performance-sensitive: it claims a speed
   or resource gain, or touches a known hot path. Before and after, or A/B,
   with batch seed data: at least 5 runs of each variant, alternating on one
   machine. A table with the FACTS.md template's columns - Metric, Baseline,
   Result, Method, Environment, Runs per variant (median and range) - leads the review package and the PR
   body; FACTS.md keeps the raw runs. PLAN sets the threshold; without one,
   the numbers go to CP3 for the user to judge. A gap inside the run-to-run
   range is "no difference". No performance claim without a measurement.
   Record the dataset size and the counts that matter (queries, I/O calls,
   allocations); a count that grows with the dataset is a finding whatever
   the wall time.
5. **UI walkthrough**, when the change touches views, components, styles or
   templates, or the item scope names it as UI. Walk the flow in the
   harness's in-app browser, or Chrome, and take screenshots - before and
   after when the change alters an existing screen. Reach each changed
   screen by navigation, as a user would, and simulate the changed flow
   through its options and states: each option or variant, the empty,
   error and loading states, and a second user where the screen differs by
   user. Check it renders with no console errors or stuck loading state.
   The final screenshots - the before and the after of each changed screen
   and state - go straight to the project's feature docs,
   `docs/features/<feature>/` unless the project keeps them elsewhere
   (compressed PNG or WebP), linked from FACTS.md.

When the branch already has CI runs, the verifier reads the latest run
(read only) and compares its failures with the local results.

When the completion boundary includes production, a live check after
deployment follows the layers. Use what the harness provides, such as a
browser or app-preview tool, a run skill or computer use; GSD requires no
specific tool.

Record each layer that runs in FACTS.md, naming the layer, with the method,
environment, steps and observed result (documents.md, Facts and evidence).
Save recordings, raw runs and intermediate screenshots under the item's
research/ and link them; summarise logs inline. The final UI screenshots are
already in the feature docs. At the fold-back (Checkpoint, simplify and
counter-review, step 5) the docs stage agent links them from the feature
docs, compresses any that are still large, and folds in the benchmark
table; the PR description links them.

When a layer's method is unavailable (no browser, no display, no access),
record not_run or blocked with the reason, never passed. Name a fallback -
another method, or a manual check by the user, such as their own
screenshot - and use it or ask for it.

For L2 and L3 the planned layers are evidence, not reviews: a missing layer
stops close-out until it is met or the user waives it in DECISIONS.md. L1
runs the layers IDEA.md's Tests section names, with at least one automated
test per criterion on the final commit; the old-code rule does not apply.

## Doors

A door says how hard a change is to undo. These count as one-way doors by
default:

- schema or data migrations, and deletions;
- auth, permissions and secrets;
- deploy and infrastructure scripts;
- payments and sent messages;
- public API removals.

The project review rules add to this list. A path that matches
`always_high` - in the rules at the item's base commit or at HEAD - is a
one-way door: run `gsd risk --base <item base> --changed` and take
the paths it reports with an `always_high` match, naming the rule source in
the door map. As with any one-way door, an L3 item verifies their findings
with three verifiers.
Removing or narrowing an `always_high` entry inside an item is a one-way
door too: it weakens every later gate in the repository. It does not turn
off this item's gate: `gsd risk --base` still reads the removed entry at the
base, so a formerly protected path the item changes stays gated (Security
gate). The item base is the commit before the item's first change
(Verification layers).

Everything else is a two-way door: a revert or redeploy undoes it. When a case
is unclear, propose a class and let the user decide; an unresolved case counts
as one-way.

The door map lists each changed path - or, for a plan review, each plan step -
with its door and a one-line reason, as a table with one row per path or step:
`| Path | Door | Reason |`, where the path cell may be a relative link and
the door is `one-way` or `two-way`. In a tiered item it is
`research/<date>-door-map.md`, linked from REVIEW.md. Build it at the
checkpoint commit, even when every review is waived, and refresh it against
the final commit before presenting the package. A review round builds or
refreshes its own map first (review-loop-engine); without an item it lives in
the review packet. Findings map to it, and the verifier count follows it.

## Checkpoint, simplify and counter-review

These steps apply to tiered items after implementation and checks. They run
without stopping, so the user's next stop is CP3 Review. Each commit
holds only the item's own paths - the changed code, its documentation and the
item's records, never other writers' changes - on the item branch (Item
branch); the only push is the draft PR's (Pushes). Implementation approval
at CP2 is the authority for these commits and that push (Commit authority).
Each step gets its own commit, so the history shows the implementation, the
simplification and the review fixes apart.

1. Checkpoint: commit the implementation and carry on - a soft checkpoint,
   not a stop. Build the door map (Doors) for the checkpoint.
2. Simplify: run code-simplification on the changed code through the
   simplifier stage agent (`gsd agents build simplifier --body`;
   specialists.md).
   First pin the current behaviour: where no check covers the code being
   simplified, add a characterisation check (it records what the code does
   now, and passes before the simplification). A pass that changes nothing
   is fine. If it changes code, rerun the affected checks. Revert a
   simplification that does not make the code easier to read - longer,
   cleverer or merely different code is not simpler - and record the
   decision in DECISIONS.md. Commit the simplification if it changed code.
3. Counter-review: run the counter-reviewer stage agent
   (`gsd agents review counter-reviewer --body`) over the committed
   implementation (Cross-agent review); do not ask whether the user wants
   one. Fix the confirmed in-scope findings and commit each round's fixes
   on its own. If it does not happen - no second CLI or pi is available, or
   the user waived it - record "waived" with the reason in REVIEW.md and
   continue. It is never a gate. Then check the security gate and, when it
   applies, run the security review before step 4 (Security gate).
4. Verify: run the verification stage agent
   (`gsd agents review verification --body`) with the layers the
   verification plan names, and record each layer in FACTS.md (Verification
   layers).
5. Fold lasting documentation and accepted deferrals into the item's paths
   (documents.md, Permanent documentation and deferred work) before final
   checks, and commit them. The docs stage agent
   (`gsd agents complete docs --body`) does the fold-back here, so the
   review package covers it. This includes feature docs, the lasting
   evidence and screenshots, and conditional agent guidance. The retro
   stage agent (`gsd agents complete retro --body`) runs beside it and its
   changes go into the same fold-back commit; when it changed anything, the
   retro review follows that commit (Retro).
6. Final checks: rerun the checks relied on for acceptance against the last
   commit and record them. Evidence from the working tree has unknown
   freshness and cannot close a tiered item.
7. Draft PR: run the pull-request stage agent
   (`gsd agents review pull-request --body`) to push the item branch and
   open a draft PR with the review package as its body (Draft PR).

Other agents a repository adds to a stage (`gsd agents <stage>`) run in
parallel with the skill's own, at most 4 at a time.

### Retro

The retro turns the item's accepted review lessons into the repository's
review memory: a check, a rubric line or an entry in the project review
rules (`.agents/rules/review/REVIEW.md`). It runs at step 5, beside the docs
agent, on tiered items. Hand the retro stage agent the item path, the
Kickoff answer on creating project review rules, and the repository's test
layout; it reads the rest itself.

- It makes at most 5 changes, each citing its source finding IDs, and
  returns any proposal it did not make as deferred. A check it proposes is
  written by the implementer under CP2's authority, or deferred if large.
- Without project review rules, it creates them from
  [the template](../templates/PROJECT-REVIEW.md) only when the user said
  yes at Kickoff; otherwise every proposal is deferred. A legacy `REVIEW.md`
  (a stage agent, or a lens `index.md` lists) is never written to: the
  proposals are deferred and the migration step named.
- FINAL.md's Review memory section lists the changes made and the
  proposals deferred.

Retro review: the counter-review never saw the retro's changes, so when the
retro changed anything they get their own review before the final checks.
After the fold-back commit:

1. Run one review round on that commit through review-loop-engine, with the
   Kickoff counter-reviewer and model, its own session and brief, and the
   lenses review-critic chooses (at least `agent-config` for rules and
   rubrics, `tests` for new checks). The scope is the retro's changes in
   that commit, GSD-supplied as for the counter-review.
2. Verify each finding with a fresh verifier, as for any review. Fix the
   confirmed ones and commit the fixes; a fix needs a fresh verifier too.
   A finding still open goes into the CP3 package.
3. Re-check the door map and gate on every path the item changed since its
   base: `gsd risk --base <item base> --changed`, which reads the rules the
   retro left at HEAD. A new
   `always_high` entry can cover code the item changed before the retro, so
   a path can become a one-way door and the security gate can turn on;
   when it does, record "Security gate: applies" with the paths and the
   rule source in REVIEW.md and run the security review before CP3
   (Security gate).
4. Rerun the checks the retro's changes affect, now on the retro commit
   rather than at the final checks: new tests, `gsd validate`, the
   scenarios or checks whose rules changed, and the project's checks for
   every path whose door or gate changed in step 3.

Record the round, its verified findings, the gate re-check and the reruns
in REVIEW.md under their own heading, and carry them into the CP3 package's
Review part. When no second CLI is available, record the round as waived
with the reason, as for the counter-review.

### Security gate

A change to an `always_high` path gets a separate security review, and
close-out waits while a security finding in the item is open. Every other
review stays advice.

Trigger: after the counter-review, run `gsd risk --base <item base>
--changed`. It checks every path changed from the base to HEAD, both sides
of a rename, so moving a file out of an `always_high` glob still matches
it. The gate applies when any path reports an `always_high` match. `gsd risk --base` unions the rules at the
item base with the rules at HEAD: an entry the item adds counts, and so does
one it removes or narrows, so an item cannot drop an entry and then change
the formerly protected path unreviewed. When it applies, record one line in
REVIEW.md's Scope - `Security gate: applies - <paths> (<rule source: base,
HEAD or both>)` - and commit it with the item's records. When it does not
apply, record nothing.

The gate is sticky. Once the line is recorded, it stays on for the item:
`gsd validate` reads REVIEW.md's committed history, so removing or
rewording the line, or deleting REVIEW.md, is an error and the item stays
gated. Later checks - after a CP3 fix, or the retro re-check (Retro) - can add
paths in a new line but never remove one, and `gsd validate` treats an item
with that line as gated whatever else REVIEW.md says.

Security review: run the security-reviewer stage agent (`gsd agents review
security-reviewer --body`). It is a separate loop through
review-loop-engine, after the counter-review: its own session and brief,
lens `security` only (with the repository's security lens extension, if
any), the Kickoff reviewer and model, up to 3 rounds, one commit per round.
Record its findings in REVIEW.md as for the counter-review (Cross-agent
review), under their own heading, with the outcome - "no findings" too.
When no reviewer CLI is available, record the security review as not run,
with the reason; the gate stays on.

Open security finding: in a gated item, a finding that is security in kind
and is confirmed or unverifiable and not released, whichever review and
lens raised it. Security in kind means `Lens: security`, a security rule
class in its fingerprint (`auth`, `injection`, `secrets`, `data-exposure`),
or `Protected: security` from any verifier; a finding whose Lens,
Fingerprint or Protected field is malformed, empty or missing (when the
record has any of the three) counts too, so it fails closed. The kind is
sticky like the gate: a finding that was security in kind in any committed
version of REVIEW.md stays so, and stays open if its record is stripped,
relabelled or deleted, until it is released. So a general-lens finding about authentication blocks
even when the security review found nothing.

Block: while an open security finding remains, do not write FINAL.md, do
not set the item complete or delivery verified, and start no delivery step:
no ready PR, no CI round, no CP4. The CP3 package names each one in its
Review part, with what would release it. CP3 acceptance of the package
does not release one unless it names the finding.

Release, only in one of two ways:

- A fix, committed, that a fresh verifier confirms against the fixed
  revision. Mark the finding resolved and end its Resolution with one
  sentence that begins `Fix verified by a fresh verifier`, with the
  revision and the verifier's file - for example `Fix verified by a fresh
verifier on abc1234 ([vote](research/verification/.../F1-1.json)).`
  `gsd validate` accepts only this form, and only when the sentence names
  the fixed revision and cites the verifier's saved reply under
  `research/verification/`, a file that exists in the item and is a JSON
  reply with `"result": "confirmed"`, the finding's R- ID as `id` (a
  reviewer ID such as F1 recurs across reviews, so it does not count), and
  the fixed revision as `revision` (7 or more hex characters). Brief the
  fix verifier to reply with that R- ID and revision.
  It does not
  release the finding when that sentence is a question or also says not, yet, pending, awaiting, once, until,
  unless, failed, refuted, unverifiable, unconfirmed, partly, still,
  remains, cannot, exploit, reproduces or bypass, or any "n't" word. Until
  a verifier confirms the fix, do not write the sentence; the finding stays
  open.
- The user's acceptance, recorded in DECISIONS.md with the user's own words
  quoted. The quote starts with `I accept`, `accept`, `accepts` or
  `accepted`, followed directly by the finding's R- ID, optionally with `finding` or `security finding`
  between - for example `- 2026-11-01 CP3 (Sam: "I accept R-03 as a known
risk"): Sam accepted R-03.` or a quote the bullet ends with ` - Sam`.
  `gsd validate` accepts only this form. It does not release the finding
  when the quote is a question, or also says not, no, cannot, never, refuse, reject, open,
  unresolved, unless, until or if, or any "n't" word, when the bullet says
  the agent accepted or settled it, or when the quote accepts only the
  package. If the user's words do not fit, ask the user to confirm the
  acceptance in that form. Mark the finding accepted.

The agent never resolves, accepts or filters a security finding on its own
judgement - only a verifier's verdict refutes one - and never writes an
acceptance the user did not give. `gsd validate` reports `security-gate-open` as an error when
FINAL.md exists, the stage is complete or delivery is verified while one is
open, and `security-release` as a warning for a security finding resolved
or accepted without its release form.

Advisory: findings that are not security in kind, in any item, and every
finding in an item that touches no `always_high` path by either set of
rules. They follow Review and Close as before.

### Draft PR

After the final checks, the orchestrator writes the PR body from
[the PR template](../templates/PR.md) - the review package, with any
screenshots - and the pull-request agent delivers the item branch for
review: it pushes the branch by explicit refspec (Pushes) and opens a draft
PR against the recorded base:
`gh pr create --draft --base <base> --head <item branch> --title "<title>"
--body-file <body>`, on the gk path too (`gk pr` targets gk's own base, not
the recorded one). If a PR for the branch already exists, it updates the
body with `gh pr edit --body-file` instead.

Without a remote or without `gh`, the agent pushes nothing, the
orchestrator saves the body as `research/<date>-pr.md`, and the package
names the push and the draft PR as skipped; no question is asked. Record the PR link, or the skip, in
FACTS.md, and present CP3 with it.

### Commit authority

Kickoff approval authorises the item branch and the item-records,
planning-set and plan-review commits (Commits).
Implementation approval authorises the close-out commits above, the CP3
feedback commits and their pushes, the close-out commit, the L3 smoke-review
commit (Smoke review), and the pushes of the item branch and the draft PR
(Pushes, Draft PR) for that item; CP3 approval adds the rebase, the force
push with lease of the item branch and `gh pr ready` (After CP3 approval); record it with the approval in DECISIONS.md.
CP2's authority also covers the CI fix commits and their item-branch pushes,
and a rebase and leased force push when the base moved before CP4 (CI, CP4
Merge). CP3 also approves the chosen close-out method and its commit.
CP4's yes adds the merge, the base push and then deleting the item branch
(CP4 Merge). The user
can opt out at CP2, or later. Then
propose each commit and wait for confirmation; if the user declines, leave the
work uncommitted and say so - the item cannot close until the final checks
run on a commit.

Untiered items keep the earlier rule: do not commit unless asked, and offer a
cross-agent implementation review for a substantial change.

## Review

Read the acceptance criteria, implementation changes and verification
evidence. Confirm the review covers uncommitted and untracked work when
relevant. Select a compatible review skill or directly review against
requirements if its prerequisites do not fit.

Verify each finding before acting on it, with a fresh verifier against the
reviewed version, then apply the filters (`review-critic`'s verifier and
filters references); this holds for GSD's own review, review-local and a
cross-agent loop. Record findings in REVIEW.md with their verification
(documents.md, Findings and close-out) and actionable fixes in TODO.md. GSD
fixes the confirmed in-scope findings itself and reruns the affected checks;
a refuted, filtered or unverifiable finding is reported, not fixed. Verify
fixes and record useful regression prevention. Resolve or explicitly accept
findings. Update stage to review. Do not invent a required separate reviewer
or model.

## Cross-agent review

At the plan and implementation review points, a second coding-agent CLI can
review the work through the `review-loop-engine` skill, with review-critic
writing the brief and choosing the lenses. For a tiered item, the
plan-reviewer and counter-reviewer stage agents run it by default unless
waived; for an untiered item it is an offer, never a gate:

1. Choose the reviewer. Pair by the session's model family, not the harness
   product: on a non-OpenAI model (including Claude, GLM or a local model
   inside any harness), the default is Codex with Sol; on an OpenAI model,
   Claude Code with Opus. A pi review on local models remains another
   option. For a tiered item, the reviewer and model are a Kickoff question
   with this default; if the model family is unknown, make that question
   open. For an untiered item, offer the review when the plan or change is
   substantial - several files, risky operations, or a design the user will
   not read line by line - naming the default reviewer and model.
2. Run an offered review only if the user accepts; a tiered review runs
   unless the user waives it. If the chosen reviewer is unavailable after
   implementation approval, use pi when it is available; otherwise record the
   counter-review as "waived" in REVIEW.md and continue. For tiered items,
   record the run or waiver and the outcome in DECISIONS.md. For untiered
   items, record declining only if the user asks.
3. Scope it from the item's own records: IDEA.md, PLAN.md and SPEC.md for a
   plan review (`kind: plan`); the commits and files evidenced in TODO.md
   and FACTS.md for an implementation review. Exclude other items' work.
   For a tiered item, tell review-loop-engine that the scope is
   GSD-supplied: Kickoff approval stands in for its scope confirmation for
   the plan review, and CP2 approval for the counter-review, so it shows the
   scope as a notice and starts without a stop. Its escalation rules still
   apply. When the item's REVIEW.md already holds findings, write them into
   the packet first: `gsd fingerprints <item> --format json >
<packet>/known-findings.json`. Only the filters read it, after
   verification; the brief never names the earlier findings or the settled
   entries.
4. GSD stays the only writer. The loop returns its findings, verified; record
   them in REVIEW.md with their verification, `Lens`, `Fingerprint`,
   `Protected` and disposition (documents.md, Findings and close-out), each
   repeat, settled or capped finding in one line with its reason, link the
   door map, and add follow-up tasks to TODO.md. The cross-agent reviewer stays
   read-only: GSD applies the fixes. For GSD-supplied scope, GSD commits the
   item's own paths after each round's fixes, so each round is its own
   commit; review-loop-engine still builds `fixes-<n>.diff` against its
   snapshot. Plan findings are folded into the plan before CP2.

## Close

Check each applicable acceptance criterion, evidence freshness, review
findings, comments affecting acceptance, required project documentation and
ADRs, and the agreed completion boundary. Open failures, required
unavailable checks, or an open security finding in a gated item (Security
gate) prevent close-out. Report the exact remaining work instead
of creating a draft FINAL that looks like successful completion.

Documentation fold-back precedes the final commit and checks (Checkpoint,
simplify and counter-review). If more delivery documentation changes during
close-out, return to that commit/check step before presenting the package.
The accepted commit must include the delivered documentation. Keep
AGENTS.md concise, with conditional routing links. FINAL.md lists actual
updates and accepted deferrals; a backlog move never waives an unfinished
criterion. Review-memory changes come from the retro at fold-back (Retro),
and FINAL.md's Review memory section lists them.

For every tier, present a short review package as CP3 Review (HITL
Checkpoints) and wait for the user's acceptance before writing FINAL.md.
Feedback is fixed, committed under CP2's authority and the package presented
again at CP3, until the user approves. The L1 package stays short. A request to close the item, confirmation
that checks passed, or acceptance of a deferral does not accept an unseen
review package. Implementation approval is separate too. Only acceptance of
a package already presented, or an explicit waiver of package review, permits
skipping this wait. Record the user's actual acceptance; never invent it from
an instruction to prepare close-out documents.

Refresh the door map against the final commit first. When the work ships as a
pull request, write the PR body too (see below) before presenting. Show the package itself
in the reply - a link to REVIEW.md is not enough - and record it in
REVIEW.md. It contains, in order, each part under its label:

1. **Changed** - scope delivered and the final commit.
2. **Door and blast radius** - one-way or two-way, and the blast radius:
   who and what it reaches if it goes wrong.
3. **Safe because** - the one fact the change is safe because of, with its
   proof level: 1 stated; 2 reasoned from the code; 3 covered by a unit test;
   4 reproduced by an integration or end-to-end test; 5 reproduced in the
   running app.
4. **How tested** - the acceptance evidence, with base and final commits and
   end-to-end evidence such as screenshots.
5. **How to undo** - the revert, redeploy or data step.
6. **Evidence by type** - the performance table (first, when there is one),
   UI screenshots, or "none".
7. **Review** - the disposition with verification results, or the waiver.
   When a counter-review ended at the round limit with findings open, add
   one step-back line: is the approach itself wrong? In a gated item, give
   the gate line and the security review's outcome, and name each open
   security finding and what would release it (Security gate).
8. **Residual risk** - accepted limitations, and any one-way door below proof
   level 4, flagged.
9. **Offered** - the offers made, such as a line-by-line read.

List every one-way door's files as relative links, so the reviewer can open
each one. The retro's changes to `settled`, `risk_paths` or `always_high`
alter later reviews and the gate, so list each as a one-way door, naming
its path or glob and its source finding IDs; removing or narrowing an `always_high` entry always is
one (Doors). The Review part carries the retro review's findings and gate
re-check (Retro). Offer the user a line-by-line read of each one-way door; it is an
offer, never a gate - GitHub enforces any required human review. A one-way
door below proof level 4 never blocks: it is flagged, and the user's
acceptance names it.

When the work ships as a pull request, its description carries the same
package, following [the PR template](../templates/PR.md): the pull-request
agent opens the draft PR with it (Draft PR), and later changes update it
with `gh pr edit --body-file`; without a remote or `gh` it is saved as
`research/<date>-pr.md`.

Acceptance covers the reviewed scope and evidence at the shown commit.
The chosen close-out method authorises its mechanical record, relocation,
index and link changes. Those commits, recovery-pointer repairs and a rebase
that preserves the accepted behaviour do not require another CP3. CP4 accepts
the final delivery head and shows what changed. A product fix, scope change or
new evidence that invalidates the accepted package requires reopening and
presenting that revised package at CP3 again before close-out. A new push alone
does not invalidate acceptance. A counter-review is not human acceptance.

For untiered items, ask for human final sign-off only if explicitly required
for that item.

In a gated item, an open security finding blocks this step and every
delivery step after it, whatever the user accepted at CP3, until a fix
confirmed by a fresh verifier or the user's acceptance in DECISIONS.md
naming the finding releases it (Security gate).

Once conditions are met, write FINAL.md with supporting links, record the
acceptance where it applies, and update IDEA to complete/verified with its
completion date. For a tiered item, CP3 approval carries straight on to
FINAL.md, the full-record commit and the selected close-out method, without
another stop. An item branch delivers only after these steps (After CP3
approval). Completing a pilot milestone must not close a parent item
with remaining capabilities.

### After CP3 approval

CP3 acceptance closes the accepted GSD scope before branch delivery. An open
security finding still blocks close-out (Security gate). After all CP3 HITL
questions are settled, continue without another stop:

1. Finish the accepted method's permanent-doc edits and useful asset moves.
   If they materially exceed the CP3 package, present that changed content
   for acceptance first (Close-out method). Then write FINAL.md with the
   accepted scope, evidence, CP3 acceptance and chosen method. For an item
   branch, its Delivery section says `pending at close-out`
   and links the PR or local delivery ledger. Set IDEA.md complete/verified,
   set its completion date, `next_action` to no remaining GSD work, and finish
   its GSD lifecycle checklist. Move any legacy merge sub-tasks to the delivery
   ledger instead of checking them off as if already done. Do not
   describe a pending merge as delivered. Commit the full records, including
   FINAL.md, on the item branch. Preserve this commit as the recovery record.
2. Carry out Archive, Compact or Fold (Close-out method), then commit it
   separately on the same branch. FINAL.md remains inspectable in the prior
   commit even when the folder is removed. Validate the resulting records,
   check repaired links and run the relevant final checks on this final head.
   Retain the branch/base refs and record SHA in the PR or delivery ledger so
   delivery can resume without the active GSD folder. Without an item branch,
   close-out ends here.
3. Rebase on the base: `gk rf` on the gk path, otherwise `git fetch origin
   <base>` and `git rebase origin/<base>`; without a remote, `git rebase
   <base>`. After `gk rf`, check the outcome, because gk may act on
   another base: `git fetch origin <base>`, then `git merge-base
   --is-ancestor origin/<base> refs/heads/<item branch>` must exit 0. If
   it does not, stop and say so before any push; the user decides how to
   restore the branch, and the delivery ledger records that it uses plain git
   from then on. A conflict stops the flow: use
   the rebase skill and ask only if it cannot settle the conflict. If the
   rebase changes accepted behaviour or invalidates evidence, reopen and
   repeat affected review and CP3 acceptance. Otherwise rerun the final checks;
   CP4 shows the rebase and asks for acceptance of the delivery head.
   After any history rewrite, refresh the summary's `record`, the
   `GSD-Closed` trailer's `record=` and the ledger links to the rewritten
   full-record commit. Verify that commit is an ancestor of
   the new head and still holds the entire closed item including FINAL.md.
   Commit these pointer repairs before final checks and CI; an old unpushed
   SHA may disappear and cannot be the recovery record.
4. Push the item branch, after checking the destination against the retained
   IDEA.md branch metadata or the delivery ledger,
   with the push the remote head calls for (Pushes): fetch it, then a
   plain push when it is an ancestor of the local head, a leased force
   push when it is the agent's last pushed head and the rebase rewrote it,
   and a stop when another writer pushed. The orchestrator runs this and
   step 5, not the pull-request agent. Never force push the base or
   another branch. If the permission hook denies it, hand the command to
   the user (Pushes) and check the remote ref afterwards.
5. Mark the PR ready: `gh pr ready <number>`, then check
   `gh pr view --json isDraft,headRefOid` shows it ready at the pushed head.

Without a remote, steps 4 and 5 are skipped and CI is `no CI`. Name these
in the FINAL.md snapshot before the full-record commit when known; otherwise
record them in the delivery ledger, without changing the preserved snapshot.

The PR description must link the close-out record commit and the resulting
archive, summary or maintained docs. Record tested heads, CI attempts and delivery
status in the PR or a task-scoped delivery ledger, outside the removed item
folder. FINAL.md is a truthful snapshot at close-out; the PR or ledger is the
source for the later merge outcome. No post-merge GSD close-out commit is needed.
Any commit after the PR is ready creates a new head that CI must pass before CP4.

Declined or blocked delivery leaves the accepted GSD scope closed. Report the
branch, PR, blocker and next delivery action without claiming a merge. A later
CP4 acceptance resumes delivery. If a finding invalidates the accepted scope or
verification, reopen the GSD item (Reopen), repair it and repeat affected review
and CP3 acceptance before closing it again and returning to delivery.

### CI

After `gh pr ready`, run the CI stage agent (`gsd agents complete ci
--body`) on the pushed head. It reports one state: `green`, `red` with the
failing check and a log excerpt, `pending`, `blocked`, or `no CI`. It reads
and never edits or pushes.

- **No CI** - no CI configuration in the repository and no check runs on
  the base's recent commits. Skip the step, name it in FINAL.md's Delivery
  snapshot when known, or the delivery ledger and CP4, and go on without a question. A repository without a
  remote has no CI either.
- **Pending** - checks not yet registered or still running. Wait: a head
  with no checks is never green. A timeout with no checks is `blocked`.
- **Red** - assess whether the failure invalidates the accepted scope or
  evidence. If it does, reopen and repeat affected verification, review and
  CP3 acceptance before closing again. Otherwise fix the CI cause and commit
  it on the item branch (CP2's authority),
  rerun the local checks, push by explicit refspec (Pushes) and run the CI
  agent again on the new head. That is one fix-and-recheck attempt; at most 3. After the third red, stop and ask the user, with the failing check and
  the excerpt. CP4 shows every change since CP3; it does not replace renewed
  CP3 acceptance when the earlier package was invalidated.
- **Blocked** - checks inaccessible, the head mismatched, or no checks
  before the timeout. Ask the user; never treat it as green.
- **Green** - every registered check passed on the pushed head. Keep the
  item branch at that head: the head, the checks and the attempts go into
  the PR or delivery ledger, separate from the closed GSD record. Then the base-moved check (CP4 Merge).

A delivery left blocked in CI records `blocked` and the failing check in
the PR or delivery ledger. The accepted GSD scope stays closed unless new
evidence invalidates its completion boundary (After CP3 approval).

### CP4 Merge

Before asking CP4, fetch the base (`git fetch origin <base>`) and compare it
with the base the head was rebased on. If the base moved since CI passed,
the tested head is not what would merge: rebase the item branch (`gk rf`,
checked as after CP3, or `git rebase origin/<base>`), rerun the local
checks, push it as the remote head calls for (Pushes; a rebase that
rewrote the agent's own pushed head needs the leased force) and run CI on
the new head before asking CP4. `gk ff` refusing a feature that is behind
its base takes the same path. Without a remote, compare with the local
base and rebase on it.

Ask CP4 (HITL Checkpoints) with: the PR link, the CI result on the head (or
"no CI", named), what changed since CP3 (`git log --oneline <CP3
commit>..<head>` - CI fixes, rebases), and a reminder when `gh pr view
--json reviewDecision,reviews` shows no approving review. Acceptance at CP3
covered the CP3 commit only, so a yes here also accepts the new head.

On yes, check the CP4 conditions first, because the permission hook cannot
see inside gk:

- CP4's yes is recorded in the conversation or delivery ledger.
- The accepted GSD scope is closed, FINAL.md exists in the full-record
  commit, and the selected Archive, Compact or Fold result is committed
  in the tested head. Missing close-out blocks merge on every delivery path.
- The item branch head equals the head shown and accepted at CP4: the head
  CI passed, or with no CI the head whose local checks passed after the
  close-out.
- With a remote: `origin/<base>` is the commit just fetched (keep its
  SHA), and the local `refs/heads/<base>` equals that SHA immediately
  before the merge - before `gk ff`, and on plain git after the pull.
  Unpushed or divergent local base commits stop the merge.
- Without a remote: the local base is unchanged since it was read before
  CP4.

If any fails, stop and say which. Then merge by the first path that
applies:

1. **No remote** - a local merge: `git switch <base>`, `git merge --no-ff
<branch>`; no pull, no push. This comes first: gk needs a remote, as at
   Kickoff.
2. **gk** - the gk CLI responds, the git-kiss skill is available and
   FACTS.md does not record that the item uses plain git: with the item
   branch checked out and the tree clean, `gk ff`. It pulls the base,
   refuses a feature behind it and merges with `--no-ff`; it neither
   pushes nor deletes. Never `gk ff!`: branch deletion waits until
   publication has been verified.
3. **Plain git with a remote** - exactly:
   `git switch <base>`, `git pull --rebase origin <base>`, `git switch
<branch>`, `git rebase <base>`, `git switch <base>`, `git merge --no-ff
<branch>`. If the pull brings new base commits, or the rebase changes
   the branch, stop before the merge: the head is no longer the tested
   one, so push it (Pushes), rerun CI and ask CP4 again.

Never squash, fast-forward or rebase-merge, and never merge with red or
pending CI. Before pushing anything, on every path, check the merge: the
current branch is the base (`git branch --show-current`), and the new merge
commit's first parent is the fetched base SHA (without a remote, the local
base read before CP4) and its second parent the tested head (`git rev-parse
HEAD^1 HEAD^2`). If not, stop and say so: nothing is pushed. With a remote,
push the base by explicit refspec, `git push origin
refs/heads/<base>:refs/heads/<base>`, and check that `git ls-remote origin
refs/heads/<base>` is the merge commit.

Report the verified merge outcome in the delivery ledger or final reply,
including merge SHA and publication status. Do not defer FINAL.md, GSD closure,
Archive, Compact or Fold until here, or make automatic GSD records commits on
the base after merge.

Only after verified publication, delete the item branch: `git push origin
--delete <branch>`, verify its remote ref is gone, then `git branch -d <branch>`.
Without a remote, only delete the local branch after verifying the local merge.
If a hook denies a push or delete, stop and hand the exact command to the user
(Pushes). A no at CP4 leaves delivery declined; the accepted GSD scope stays
closed unless its acceptance evidence is invalidated.

### Close-out method

Offer these three methods at CP3, with **Fold as the default**. For Fold,
present the fold map in that package (below). Earlier method choices are
inputs to CP3, not permission to skip it. Untiered items and cancellations
get the same choice at their authorised close-out. For explicit
full-send/full-stop delegation, reuse an explicit choice or record the Fold
default without introducing another checkpoint. Record the accepted method in
IDEA.md front matter as `close_method: archive`, `compact` or `fold`
(`gsd set ITEM close_method=fold`).

After HITL acceptance, commit FINAL.md and the complete/verified IDEA.md before
relocating or removing the GSD folder. For a cancellation, preserve the stopped
stage, `delivery: cancelled` and its cancellation date instead of claiming
completion. This full-record commit must preserve the entire item as it is
after the accepted permanent-doc preparation; its SHA is the record. Then
perform the chosen method and commit its result separately, before CI and
merge. Run the method's command with `--dry` first, inspect the moves and link
repairs, then run the real command. Each command prints a `GSD-Closed` trailer;
put it as the last line of the method commit's message exactly as printed,
for example `GSD-Closed: <slug> method=fold delivery=verified record=<sha>`.
A trailer in any other form is ignored. A trailer only points at the record:
dependency checks read the closed state from the record commit's own
IDEA.md, so an Archive trailer, which has no record, only reserves the slug. The trailer
lets dependency checks, slug reservation and recovery find an item that left
no file behind. The commands never commit.

| | Archive | Compact | Fold (default) |
| --- | --- | --- | --- |
| Keeps | The whole item folder | One GSD summary | Nothing GSD-specific |
| `docs/gsd/` afterwards | `YYYY/MM/<slug>/` | `YYYY/MM/<slug>.md` | Nothing |
| Main docs | Work's own updates | Work's own updates | Those, plus the fold map's facts |
| Command | `gsd prune ITEM` | `gsd compact ITEM` | `gsd fold ITEM --record <sha>` |
| Recovery | The folder | `record:` in the summary | The `GSD-Closed` trailer |

Every method includes the documentation updates the work itself needed
(documents.md, Permanent documentation). Only Fold also moves the GSD
record's decisions, reasons and limitations into the main docs.

1. **Archive** - keep the full folder. Run `gsd prune ITEM --dry`, then
   `gsd prune ITEM`. The folder moves to `docs/gsd/YYYY/MM/<slug>/`.
2. **Compact** - keep one GSD summary. Write `docs/gsd/YYYY/MM/<slug>.md`
   from the summary template, with `record` set to the full-record commit.
   Run `gsd compact ITEM --dry`, then `gsd compact ITEM`. The folder is
   removed and its links point to the summary.
3. **Fold (default)** - make the repository's maintained docs the only
   record and leave nothing in `docs/gsd/`. Before CP3:
   1. Inventory: list every tracked Markdown file with
      `git ls-files '*.md'`, leaving out `.agents/gsd/`, `docs/gsd/` and
      vendored trees. Do not stop at `docs/`: READMEs, `CONTEXT.md`,
      `AGENTS.md`, ADRs and runbooks can sit anywhere.
   2. Topology: work out how the repository organises its documentation -
      where feature docs, architecture and ADR pages, runbooks and
      directory READMEs live, how navigation works (index pages, nav
      files, "see also" lists) and the naming and tone they use. Read the
      candidate pages in full, not only their headings.
   3. Extract: from FINAL, DECISIONS, SPEC, FACTS and REVIEW, keep only
      lasting knowledge - behaviour, decisions with their reasons,
      constraints, operational guidance, known limitations and evidence
      worth keeping, such as screenshots. Follow-ups go to the project
      backlog (documents.md). Do not copy lifecycle logs, review rounds or
      superseded plans.
   4. Fold map: one row per kept fact - the destination file and section,
      the action (edit, append or new page) and why that page fits. Create
      a page only where no existing page fits, and say so in its row.
      Present the map in the CP3 package. FINAL.md is written only after
      acceptance, so record the accepted map there then.

   After acceptance, record the map in FINAL.md, apply it, update navigation, move assets and
   point every link into the item folder at its new home, then commit with
   the full records. Run `gsd fold ITEM --record <sha> --dry`, then
   `gsd fold ITEM --record <sha>`. Finally check that every row of the map
   landed and that `gsd validate` is clean.

All methods preserve FINAL.md in the full-record commit. Prepare substantive
permanent-doc edits before the CP3 package where possible. If the chosen
method introduces material new content beyond the accepted package, present
that changed content for acceptance before the full-record commit; mechanical
relocation and link repairs are already covered by the method choice. Commit
those accepted permanent-doc edits and asset moves with the full records so
the source item folder and incoming-link files are clean when the command
plans its moves. After that commit, do not move individual files out of the
item before the command runs: it must still match the recorded tree. For
Compact, leave the new summary untracked until the removal commit; it is the
destination, not an incoming-link file. If a source folder or incoming-link
file is dirty, stop and commit only the authorised edits before retrying the
dry run. Do not stash unrelated work.

YYYY/MM is the GSD completion date, or the cancellation date. Closure records
accepted scope completion, not merge or deployment. FINAL and, for Compact,
the summary link the PR or local delivery ledger for the eventual outcome; a
folded item's ledger names the record SHA. Never offer to close now or after
merge. An unaccepted CP3 keeps the item open; an accepted CP3 carries through
both close-out commits before delivery.

`gsd compact` refuses unless the summary names the item, does not link into
the folder, and `record` is the full SHA of a commit that holds the folder
exactly as it is now. It also refuses untracked or ignored files in the
folder, because Git could not give them back, and uncommitted changes in
the files whose links it rewrites. A summary is not an item, so
`gsd status --all` no longer lists it, but it still satisfies other items'
`dependencies` and `parents`.

If `gsd validate` reports `compact-leftover`, a compaction stopped part-way:
the item folder sits parked as `.gsd-compact-<slug>` and some links may
already name the summary. Git holds every file it touched, because
compaction refuses untracked folder content and unclean link files. Show the user `git status`, then, with their agreement, delete
the parked folder, run `git restore -- <item folder>` plus every link file
`git status` lists as modified, and run `gsd compact ITEM` again.

Keep the compaction in a commit of its own. To reopen a compacted item, with
the user's agreement, revert that commit. Find it as the commit that added
the summary, `git log --diff-filter=A --format=%H -- <summary path>`, and
check with `git show --name-status <commit>` that it also deleted the item
folder. Then run `git revert <commit>`. The revert restores the committed
folder and the links that compaction pointed at the summary, and removes the summary.
If the summary changed after compaction, the revert stops on it: delete it
and continue the revert. Links added after compaction still name the
summary: find them with `grep -rln '<slug>.md' --include='*.md' .`, point
them at the restored IDEA.md and commit that. Then run `gsd reopen`.

`gsd fold` refuses unless `--record` is the full SHA of a commit that holds
the folder exactly as it is now. It also refuses untracked or ignored files
in the folder, any tracked Markdown file outside the folder that still links
into it, and an existing `docs/gsd/YYYY/MM/<slug>` folder or `<slug>.md`
file. A folded item satisfies other items' `dependencies` and `parents`, and
keeps its slug reserved, through its `GSD-Closed` trailer.

Keep the fold in a commit of its own. To reopen a folded item, with the
user's agreement, find that commit with
`git log --fixed-strings --grep='GSD-Closed: <slug> ' --format=%H`, check with
`git show --name-status <commit>` that it deleted the item folder, and run
`git revert <commit>`. The doc edits from the fold map stay, because they
were committed with the full records; reassess them as part of the reopened
work. Then run `gsd reopen`.

## Reopen or cancel

An explicit reopen request can resume an active item: preserve and visibly
supersede FINAL, record prior state/date, remove active terminal dates and
choose the state supported by remaining work. Reopened verified work needing
checks normally returns to review/implemented; new implementation belongs in
execution/in_progress. Reassess affected approvals. Clarify only a material
ambiguity, particularly for cancelled work.

After reopening delivered work, the GSD agent must reset commit-bound
sub-tasks before reporting the next action: untick final checks on the final
commit, review-package acceptance, and the Complete sub-tasks for the boundary,
FINAL and closed metadata. Their earlier ticks belong to superseded evidence
and close-out. Keep settled decisions such as a declined or waived review
unless their scope or the user's decision changes. The CLI only resets stage
boxes; the agent performs this semantic reset in IDEA.md, then confirms that
`gsd next` names an unfinished verification or acceptance action. Old acceptance
never authorises closing the reopened delivery.

On cancellation, record the user's decision, keep the stage where work
stopped, set delivery to cancelled and record the cancellation date. Do not
claim release readiness.

`gsd reopen ITEM` performs the reopen steps above: it restores the active
folder, removes the terminal date, sets review/implemented (or the given
state), supersedes FINAL.md and appends the DECISIONS entry. The approvals
themselves still need reassessing with the user.

`gsd prune` moves complete and cancelled items to `docs/gsd/YYYY/MM/` and
rebases links, and only when the user asks. Without ITEM it also moves items
left in the old `.agents/gsd/YYYY/MM/` and `.agents/gsd/archive/` locations,
which `gsd validate` reports as `location-legacy`. It skips items with errors,
uncommitted changes, another owner or an existing destination, and rolls back
if a link would break. Run it with `--dry` first. Inventory across projects
uses `--root`, for example `gsd attention --root ~/Projects`.
