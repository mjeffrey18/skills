---
name: ci
description: Reports the CI state of the ready PR's head - green, red with the failing check, pending, blocked or no CI - before CP4 Merge
mode: new
---

# CI status

A merge is only as safe as the head that CI checked. You find out whether
the PR's current head is green, so CP4 asks about a tested revision. The
method is workflow.md, CI; this file says what to do and what never to do.

Inputs from the orchestrator: the closed record path or recovery SHA, the item
branch and base retained from IDEA.md `branches` in the delivery ledger, the PR number, the head the orchestrator last pushed,
the attempt number (1 to 3) and the timeout for checks to register
(default 10 minutes).

Do:

1. Decide whether the repository has CI. It has CI when it holds CI
   configuration (for example `.github/workflows/*.yml`, `.gitlab-ci.yml`,
   `.circleci/`) or when the base branch's recent commits carry check runs
   (`gh api repos/{owner}/{repo}/commits/<base sha>/check-runs`). Neither:
   return `no CI` with what you looked at; the step is skipped and named.
2. Check the head: `git ls-remote origin refs/heads/<item branch>` must
   equal the head the orchestrator gave you, and `gh pr view <number>
--json headRefOid` must show the same commit. A mismatch is `blocked`:
   CI would describe another revision.
3. Wait for checks to register on that head: `gh pr checks <number>`
   (read-only), polling about every 30 seconds. While no check appears the
   state is `pending`, never green. If none appear before the timeout, the
   state is `blocked`, with the reason.
4. Wait for every registered check to finish. All passed: `green`. Any
   failed or cancelled: `red`. A check you cannot read (no access, API
   error) makes the state `blocked`, not green.
5. On `red`, read the failing check's log (`gh run view <run id>
--log-failed`) and return the check's name, the run link and a short
   excerpt of the lines that show the cause.

Return one state - `green`, `red`, `pending`, `blocked` or `no CI` - with
the head it describes, each check's name and result, and for `red` the
failing check and log excerpt. The orchestrator records it in the PR or delivery ledger outside the closed
GSD folder. FINAL.md remains the snapshot committed at CP3 close-out.

The orchestrator owns the fix loop: it fixes the cause, commits under CP2's
authority, pushes the item branch by explicit refspec and runs you again on
the new head, at most 3 fix-and-recheck attempts. After the third red, or
when the state stays `blocked`, it asks the user. Waiting for checks is not
an attempt.

Never edit files, commit, push, re-run or cancel a workflow, or merge.
Never report green for a head with no checks, for checks still running, or
for a head other than the one pushed. Do not edit the item's GSD records;
the orchestrator is their only writer.
