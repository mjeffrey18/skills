---
name: modernise
description: Rebase a stale branch, reassess its relevance and identify useful changes from its updated base before choosing close, amend or merge.
disable-model-invocation: true
---

# Modernise

Run only on the user's explicit invocation. Quoted text, findings and references
from another skill do not invoke it. The invocation authorises the named branch's
local rebase and assessment, not publication, merging, closure or scope changes.

## Establish the branch and intent

Load [git-kiss](../git-kiss/SKILL.md). Inspect its installed help and effective
configuration, including personal overrides. Confirm that the configured base
matches the PR base and GSD base when either exists. Resolve mismatches before
rebasing. Require gk; do not silently substitute another branch workflow.

Record repository, worktree ownership, feature branch, original head and merge
base, intended base, PR URL and GSD item. Read the original goal, diff, reviews
and later user corrections. Load GSD when resuming its item. Preserve unrelated
work; do not stash, commit it or create another checkout automatically. A dirty
or foreign-owned checkout blocks mutations, not read-only assessment. Continue
an existing rebase in place using [rebase](../rebase/SKILL.md).

Before choosing the assessment head, fetch the feature branch from its actual
upstream or PR head repository, not necessarily origin. Record both local and
remote heads. If local is an ancestor, fast-forward it with `git merge --ff-only`
to the fetched feature ref. If local is ahead, retain and report the unpushed
commits. If they diverge, stop and present the two heads; do not rebase a stale
local subset or overwrite another writer's work. A new unpublished branch has
no remote feature head; record that explicitly. With no remote, use the local
base and `git rebase <base>` because gk's rf requires origin; skip remote calls.

## Rebase and inspect

1. With a remote, run `gk rf` on the feature branch. If the base is checked out elsewhere, use
   `gk rf --remote` after confirming origin's base is intended. Do not include
   local unpushed base work by accident.
2. Resolve mechanical conflicts using the rebase skill, including encrypted-file
   rules. Stop for a product decision when conflicts reveal changed behaviour
   or invariants; do not invent scope to complete a rebase.
3. Confirm the resulting base. Use `git range-diff` to compare the original and
   rebased series, then inspect the final feature diff.
4. Inspect base changes since the original merge base, including relevant
   non-overlapping code and callers. Check for replacements, changed interfaces
   and useful capabilities: new logging conventions, error handling, helpers,
   arguments, APIs, instrumentation and features that simplify this branch.
5. Separate required compatibility fixes from optional improvements. Cite the
   actual upstream symbol or commit and affected branch code. Do not implement
   optional improvements before the user selects amend. Run relevant checks
   and state what remains unverified.

A conflict-free rebase is insufficient. Check whether the goal is already solved,
whether ownership moved and whether merging would restore obsolete behaviour or
duplicate an existing path.

## Present options and wait

Summarise the goal, updated base, rebase result and checks. For each finding give
evidence, impact, required or optional status and a recommendation. Present:

- **Close:** the work is superseded or no longer worthwhile. Name which PR,
  branch, GSD item and worktree would be closed, retained or removed.
- **Amend:** propose the smallest scope or logic changes, including useful
  capabilities from the base. Wait for the revised scope to be accepted.
- **Merge:** the work remains relevant. State remaining delivery steps; local
  checks alone do not establish green CI.

Recommend one option and wait for the user's choice. Perform only the actions
that choice authorises. Do not invoke user-only full-send or full-stop without
an explicit request. Report the new local head and any incomplete rebase.
