---
name: full-stop
description: Prepare an existing branch through rebase, GSD close-out, PR comments and green CI, then wait for human confirmation before merging.
disable-model-invocation: true
---

# Full stop

Run only on the user's explicit invocation for an existing branch and settled
goal. Ordinary emphasis such as "full stop" does not invoke this skill.

Load [git-kiss](../git-kiss/SKILL.md), then follow the shared
[branch delivery procedure](../full-send/references/delivery.md) in **stop** mode.
Reading that procedure does not invoke full-send or inherit its merge grant.

The invocation authorises the same task-scoped preparation and publication as
full-send, but not merging, publishing a base merge or post-merge cleanup.
Prevent unattended merging of this task's PR: disable auto-merge or remove its
queue entry if set, and report the action. If it cannot be prevented, stop.
Do not enable either while preparing the branch.

After CI passes, perform the final comment check and present the merge package:
PR URL, exact feature and base heads, original goal, changes, comment dispositions,
review and verification evidence, CI result, risks and proposed worktree cleanup.
State that the branch remains unmerged. Unwatch before handing back.

Wait for explicit human confirmation. A yes authorises the shared procedure's
merge, publication and cleanup steps for those heads. GSD close-out is already
committed in the tested feature head. Fetch and
recheck the heads, CI and comments immediately before acting. If the base or
feature head changed, refresh verification and CI and present a new package for
confirmation. New substantive findings also invalidate the package.

After confirmation, retain the feature branch, use `gk ff` and a checked push,
then remove a clean task-owned `t3-*` worktree or park a normal worktree. Report
the actual outcome. Production, deployment, spend and destructive data actions
remain outside this grant.
