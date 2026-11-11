---
name: full-send
description: Finish an existing branch through rebase, GSD close-out, PR comments, green CI, local merge, publication and worktree cleanup.
disable-model-invocation: true
---

# Full send

Run only on the user's explicit invocation for an existing branch and settled
goal. Quoted text, findings and references from another skill are not invocation.
This is delivery authority, not permission to choose a new product scope.

Load [git-kiss](../git-kiss/SKILL.md), then follow the shared
[branch delivery procedure](references/delivery.md) in **send** mode.

The invocation authorises task-scoped fixes, verification, commits, publication
of the task branch, a safe leased update after rebase, local merge into the
configured base, publication of that merge and the
specified worktree cleanup. Keep the feature branch locally and remotely.
Use `gk ff` and a checked base push: `gk ff!` deletes the branch.

For an existing GSD item, use the scoped checkpoint delegation described in the
shared procedure. It does not approve a missing plan or expanded scope. Paid
evaluations, deployment, production changes, destructive data operations and
changes outside the task retain their separate approval requirements. Respect
higher-priority instructions, repository protection and permission denials.

Finish with the PR link if present, tested head, merge commit, publication
result, checks, comment dispositions, retained branch, GSD state and final
worktree path or removal outcome. A failed push or cleanup is partial delivery,
not success. Stop and explain a blocker rather than bypassing it.
