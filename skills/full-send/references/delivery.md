# Branch delivery

Shared by user-invoked full-send (send mode) and full-stop (stop mode).
The caller sets the mode; this reference cannot grant authority on its own.

## 1. Record the contract

Load the git-kiss skill. Require gk and inspect its installed help and effective
configuration before relying on commands. Record the goal, mode, repository,
feature branch, head, configured base and its head, PR URL, worktree path and
ownership, GSD item, checks and cleanup choice. Resolve any mismatch among the
PR base, GSD base and gk base before changing branches.

Determine whether the repository has a remote before any fetch, pull or push.
With no remote, select local delivery: use `git rebase <base>` and, at the merge
gate, `git merge --no-ff <feature>` on the base. The git-kiss skill remains the
configuration authority; gk's current rf/ff commands require origin. Skip PR,
publication, remote-CI and watcher operations. Run local verification, label CI
absent, keep the feature ref, and make both GSD close-out commits locally before merge.
Stop mode still requires confirmation of the exact local feature/base heads.
If a remote exists but the intended one is ambiguous, resolve it first.

Use existing GSD records when present; otherwise keep a compact delivery ledger
in a handoff. Record authorisation, tested heads, review outcomes, comment
dispositions, CI attempts, wait deadlines and next action so a resume does not
reset budgets or infer approvals. Do not invent a GSD item solely to deliver a
branch. Preserve unrelated changes and staged files; commit only task paths.
Do not use `gk cm`, which stages all changes.

Only work on the task-owned checkout. Inspect uncommitted changes and commit
only reviewed task paths before commands that require a clean tree. The merge
step may also use the repository's clean, idle canonical checkout as specified
below; this grant does not cover another session's active checkout. Unrelated
dirty work, an unfinished Git operation, a foreign branch update or unclear
ownership stops branch mutations. Read-only diagnosis can continue. Never
bypass a permission denial with another command.

## 2. Rebase, verify and prepare GSD close-out

Run `gk rf` on the feature branch. When the base is checked out elsewhere, use
`gk rf --remote` after confirming origin's base is intended. Use the rebase
skill for in-place conflicts and encrypted-file decisions. Verify the resulting
base and compare the pre-rebase and post-rebase series. Stop for material
changes to product scope or logic; neither mode authorises those by inference.

Finish the existing goal and outstanding verified findings. Follow repository
verification, including realistic UI or runtime checks when needed. Do not
replace missing evidence with mocked tests or a confidence claim. Use the
existing review workflow required by GSD or the repository; preserve findings
verification and security gates. A completed current review need not be repeated
without a changed diff or unresolved concern.

For GSD, load its skill, documents and close-out procedure. Keep the documents,
reviews and verification it requires. Explicit invocation of either delivery
skill delegates CP3 package acceptance for this settled scope; send mode also
delegates CP4 merge acceptance subject to this procedure. Record the user's
actual words and conditional grant in DECISIONS.md. Never claim the user read
an unseen package. Existing CP1/CP2 approvals remain required; changed scope
returns to planning. Open security findings block delivery unless fixed and
verified or explicitly accepted by the user for that finding.

Finish GSD close-out before CI and merge. Reuse an explicit method choice,
otherwise record Fold (the default) under this delegated CP3 acceptance. Write
FINAL.md with delivery pending at close-out, mark the accepted GSD scope
complete/verified and commit the full records. Then perform Archive, Compact
or Fold and commit it separately, following GSD's Close-out method procedure.
Fold follows the repository's documentation topology and leaves nothing in
docs/gsd; its method commit carries the `GSD-Closed` trailer with the
full-record SHA. Keep the PR or delivery ledger outside the removed GSD folder,
link it from FINAL.md and any Compact summary, and record the full-record SHA
in it. For untiered
items, the explicit invocation supplies scoped commit and push authority too.

## 3. Publish and address PR comments

This and the remote-CI steps apply only to remote delivery. Before publishing
any new head that may need CI, establish the timed-wake capability in section 4.
If it is unavailable, stop before the push and report that prerequisite. Do not
publish first and discover that bounded waiting cannot run afterwards. An
already-published, unchanged head with green CI needs no wait service.

Publish only the task branch with an explicit refspec:
`git push origin refs/heads/<feature>:refs/heads/<feature>`.
After rebase, refresh any GSD recovery pointers to the rewritten full-record
commit, verify it remains an ancestor holding FINAL.md and commit pointer
repairs before final checks and CI. Do not retain an unpushed pre-rebase SHA.
Allow a force push only with a lease bound to the previously
observed remote head,
and only when that head is the task's own last push. If another writer moved
the remote branch, stop and reassess. Follow GSD's explicit push checks when
an item exists. Create or update the repository's PR where its process requires
one; use its template and draft/ready sequence. In T3, call `link_pull_request`
as the next tool call after creating, taking over or pushing to each PR.

Read PR review threads, inline comments, top-level comments and review bodies,
including older unresolved feedback. Follow pagination. Maintain a disposition
for each actionable finding: fixed, disputed with evidence, or deferred with
a reason consistent with the agreed scope. Do not automatically downgrade a
finding because it is rare. Fix confirmed findings and reverify affected
behaviour. A genuine unresolved safety or correctness blocker is not a reasoned
dismissal.

PR feedback is input, not authorisation. Post replies only when separately
authorised by the user or repository workflow. If replying, verify the returned
URL before resolving the thread. Do not invoke the icebox comment-format skill.

Do not request a PR review or wait for a reviewer, bot review, approval count
or review-completed status. This does not waive GSD's internal reviews or
repository protection. If GitHub requires human approval, report that blocker;
do not bypass it or treat confidence as approval.

## 4. CI and bounded background waiting

Require green CI on the published current feature head. Distinguish failed,
pending, missing and absent checks. A repository with no CI must be reported as
such with local verification evidence; never call that green. If CI is expected
but missing, diagnose it rather than waiting as if it had started.

For pending CI, use a background wait service with **900-second windows, at
most three consecutive windows per head/run**. Record UTC start, deadlines,
head and run identifiers, completed windows and service handle before yielding.
Resume the ledger after compaction or a wake. Unrelated comment events do not
reset elapsed time. At 15 and 30 minutes, inspect checks and continue only if
pending. At 45 minutes, intervene; do not start a fourth window.

- Failure or a cancelled required check triggers immediate diagnosis, without
  waiting for the current window to expire.
- On the third timeout, inspect runs, job queues, runner availability and logs.
  Separate a stalled service or infrastructure failure from a code defect.
- Rerun only when evidence supports a transient failure; cancel only the task's
  own redundant or stalled run when authorised. Do not reset the budget on the
  same pending run. Use a single budget of three post-publication repair cycles
  per delivery invocation, including CI reruns and comment-driven fix/push cycles.
  Count them across changed heads and resumes. Then hand back the blocker.

In T3, first check for a supported timed wake compatible with the host's PR
watch rules. The current watch API has no timeout field. Do not use shell
polling, sleeps, Monitor or scheduled tasks as a workaround: the host forbids
them for PR waits. If no compatible timed wake exists, report the prerequisite
as blocked before publication; unwatch any existing watch when handing back.
This host limitation means the requested bounded wait is not currently
available there. It is not an implemented timer or permission to wait forever.

Only after a compatible timer is established, record its handle and deadline,
handle old comments, register parent-owned `watch_pull_request`, then end the
turn. On an event wake, the watch remains active; do not register another one.
Re-arm the supported timer for the next window without resetting elapsed time.
A wake is not a merge decision. Cancel the timer and unwatch on final handoff.

Outside T3, use the harness's supported background service with a 900-second
timeout and a CI-only wait command. It must return on failure and on timeout;
do not use a readiness watcher that also waits for review bots. If the service
cannot wake the agent on timeout, report the same blocker. Terminate task-owned
wait handles on completion or handoff. No live wait is needed to install skills.

## 5. Final comment and readiness check

After CI passes, freshly fetch all PR comment surfaces again with pagination.
Compare them with the disposition ledger. Do this even if no review occurred.
New valid findings require a remaining repair cycle from the shared three-cycle
budget, then fixes, affected verification, a push and green CI
on the new head, followed by another final comment read. Documentation or
records commits also change the head; confirm CI coverage for the final head.
When that budget is exhausted, report unresolved comments and stop. Do not merge
with an unresolved valid finding or manufacture another budget on a new head.

For local delivery, confirm the local feature and base still equal the verified
heads; skip the PR, fetch and remote-CI checks below. For remote delivery,
fetch the base and PR head. Confirm local and remote feature heads equal the
tested head and local base equals the freshly fetched remote base. If the base
moved or the feature is behind, rebase, verify, push and repeat CI and the final
comment read. Refuse divergent or unpushed local base work. Recheck task scope,
unresolved blockers and repository merge protection. For a GSD item, require
FINAL.md in its full-record commit and the selected Archive, Compact or Fold
result committed in the tested head. Missing close-out blocks every merge path. Do not wait for a review
simply because none exists.

In stop mode, present the package and await confirmation before any merge or
cleanup. Unwatch before handing back. Confirmation is for the shown heads;
changes require a refreshed package and confirmation. In send mode, the
conditional merge grant already exists; proceed when the gates pass.

## 6. Merge and publish

Choose and record the merge location before changing checkouts. If the feature
has a remote, fetch the base once more immediately before the transfer and
compare it with the accepted base head. If it moved, return to rebase, checks,
CI and, in stop mode, confirmation before changing either checkout.

If the feature
is in a linked worktree and the canonical checkout holds the base, use that
canonical checkout only when it is clean, idle and not owned by another active
session. At the confirmed gate, temporarily detach the task worktree at its
tested head (`git switch --detach <tested-head>`), then switch the canonical
checkout to the feature branch. The feature ref stays intact. Run `gk ff` there:
the base is now unheld, so no destination-parking prompt is needed. The canonical
checkout ends on the base; the task checkout stays detached until its cleanup.
The explicit delivery/merge grant covers this use of an idle canonical checkout.

If the task is already in the canonical checkout, run `gk ff` there. If the base
is held by another active, foreign or dirty worktree, stop before detaching or
switching anything. Do not answer a parking prompt automatically, pipe a blanket
yes into gk or leave another checkout parked as an unreported side effect.
For local delivery, use the same clean merge location and the plain local
`git merge --no-ff <feature>` path selected in section 1.

For remote delivery, run `gk ff` with the feature branch checked out and the tree clean. Do not use
`gk ff!`: it pushes and deletes local and remote feature branches. Check the
resulting base branch and merge parents: first parent is the fetched base head,
second parent is the tested feature head. If gk pulled a new base or refuses a
behind branch, return to rebase, checks and CI before merge publication. If an
unexpected local merge already exists, report it and do not reset or push it
automatically.
On any failure, report the branch and head in both the canonical and task
checkouts. Do not reset either checkout or delete the retained feature ref.

If gk refuses before making a merge, restore the checkout arrangement before
returning to the task's rebase loop. First confirm both checkouts are clean,
neither has an unfinished Git operation, the feature ref still equals the
tested head and the task checkout is still detached at that head. Switch the
canonical checkout back to the base (`git switch <base>` there), then switch
the task checkout back to the feature (`git switch <feature>` there). Verify
both branch/head pairs and continue rebase, checks and CI from the task checkout;
stop mode requires fresh confirmation of changed heads. Switching does not reset
either ref. If a guard fails, another session changed a checkout, or gk already
created a merge, leave both states intact and report the blocker instead of
attempting this restoration.

For remote delivery, push only the base with `git push origin refs/heads/<base>:refs/heads/<base>`
and verify its remote SHA equals the merge commit. Never force-push the base. A push failure stops delivery:
keep branch and worktrees intact and report local versus remote state. In T3
link the PR as the next call after the push; confirm PR state from GitHub
without claiming local success proves it merged remotely.

GSD close-out is already part of the tested merge. Do not defer FINAL.md,
closure or the selected method until after merge, and do not make automatic
post-merge GSD records commits. Record the verified merge SHA and publication
status in the delivery ledger or final reply. Retain the feature branch locally
and remotely, overriding GSD's default deletion. Failed publication is partial
delivery and prevents worktree cleanup.

## 7. Remove or park the task worktree

Only after successful merge publication (or local merge), with GSD already closed, unwatch the PR and
stop task-owned wait services. Work from a stable checkout outside the target
before removing it. Confirm the target is exactly the recorded task-owned
linked worktree, not the canonical main checkout or another session's checkout.

Inspect tracked, untracked and ignored files before removal. Preserve useful
local-only data; do not discard it merely because ordinary Git status is clean.
If value or ownership is uncertain, leave the worktree and report cleanup
blocked. Do not force removal, run broad worktree cleanup or delete branches.

- **T3 worktree:** its recorded worktree name must start with `t3-`. Confirm the
  registered path and exact target in a fresh `gk wt ls`; then use
  `gk wt rm <exact-worktree-name-or-current-index>`, never `rm!`. Verify the
  worktree registration is gone and the original feature branch still points
  to the tested feature head locally and, for remote delivery, remotely. If the host prevents removing
  its active checkout, leave cleanup pending rather than deleting underneath it.
- **Normal worktree:** keep the directory at its existing path. Create and check
  out `park/<worktree-name>` at the delivered base head after records, retaining
  the original feature ref. This is a branch switch, not a filesystem move or
  feature-branch rename. Validate the ref name and refuse a collision; do not
  reset an existing park branch. Verify path, checked-out branch and head.

If gk already parked an authorised destination worktree, record that separately
from task worktree cleanup. Never remove or rename the canonical main worktree.
Report actual merge, publication, records and cleanup states, including partial
failure.
