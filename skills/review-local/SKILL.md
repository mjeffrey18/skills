---
name: review-local
description: User-invoked quick review - one adversarial pass by a fresh reviewer subagent in the current harness, then independent verification of each finding and fixes for the confirmed ones, with no second CLI and no re-review loop. Invoke as `review-local [target] [lenses=a,b] [fix=off]`, e.g. `review-local uncommitted` or `review-local last 2 commits lenses=rails,spec fix=off`. For a cross-agent review with re-review, use review-loop-codex, review-loop-claude or review-loop-pi.
disable-model-invocation: true
---

# Local review

One adversarial review pass, run inside the current harness. It uses the same
scoping and brief as the review loops, but the reviewer is a fresh subagent
here rather than another CLI and it runs once. Each finding is then verified
by another fresh agent, and the confirmed ones are fixed unless `fix=off`.

## Arguments

- **Target** - the text after the command, such as `uncommitted`, `last 2
  commits`, `this branch`, or a GSD item. If there is none, scope from the
  current session's work.
- **Lenses** - optional `lenses=a,b`, built-in or from the repo's
  `.agents/rules/review/index.md`; otherwise the brief-writer picks up to 3.
- **Fixing** - fixes confirmed findings by default; `fix=off` makes it a
  review only, with no file in the repository changed - not the code, and not
  a GSD item's records: the door map, verdicts and report stay in the packet.

## Run

1. **Scope and packet.** Follow the `review-loop-engine` skill's
   [scoping](../review-loop-engine/references/scoping.md) to build the manifest,
   `scope.diff` and `scope.md` in a fresh packet directory outside the repo.
   Mixed commits, other agents' work and uncommitted or untracked changes are
   handled the same way as in the loop. Write the packet's `door-map.md`
   (`review-critic`'s [verifier](../review-critic/references/verifier.md),
   Door map first); in a GSD item, the item's research/ door map - except with
   `fix=off`, when it stays in the packet.
2. **Brief.** Load the `review-critic` skill and have a fresh brief-writer
   subagent write `prompt-1.md`, as its brief-writer reference describes. Never
   pass your own reasoning about the change.
3. **Confirm.** Show the user the base, commits, paths, size, exclusions, the
   lenses with their reasons and any repo additions, and the reviewer model. Wait for confirmation or
   corrections.
4. **Review.** Spawn one more fresh subagent - not the brief-writer - with the
   contents of `prompt-1.md` as its whole task, and tell it to reply with only
   the JSON object that `review-critic`'s findings schema describes. Keep it
   read-only: where the harness lets you choose the subagent's tools, give it
   only file reading and search; otherwise put "do not edit files, run commands
   that change anything, or start other agents" at the top of its task.
5. **Validate.** Save the reply to the packet and run
   `python3 <review-loop-engine>/scripts/review-round.py --validate <file>`. On a
   format problem, ask the same subagent once to reply with only the corrected
   JSON; if it still fails, report the raw reply instead.
6. **Verify and filter.** Verify each finding with a fresh agent - never the
   reviewer, never yourself - and save, validate and tally the replies, as
   `review-critic`'s [verifier](../review-critic/references/verifier.md)
   describes. Then apply its [filters](../review-critic/references/filters.md).
   If the reviewer's reply is already saved (a resumed run), start here from
   that reply and any verdicts already saved. With `fix=off`, save the verdicts
   in the packet even for a GSD item.
7. **Fix.** Unless `fix=off`, fix each confirmed, unfiltered, in-scope finding
   with the smallest change, then rerun the affected checks. Leave refuted,
   filtered and unverifiable findings alone, and any fix that would leave the
   confirmed scope to the user. With `fix=off`, change no file.
8. **Report.** Findings grouped by lens, with the `spec` findings kept apart from
   the standards view (see `review-critic`'s Reporting section); each with
   severity, location, evidence, verification result and what was done -
   fixed (with the check result), not fixed and why, or the suggested fix
   when `fix=off`. Then offer a cross-agent review loop for a second opinion.

In a GSD item, GSD stays the document writer: return the findings, their
verification and the fixes for it to record in REVIEW.md.

## Reviewer model

The same floor as the loops applies. The reviewer subagent runs on:

| Harness | Allowed |
| --- | --- |
| Claude Code | Opus or Fable - pass the model when spawning |
| Codex | GPT-6.1 Sol or GPT-6 Astra |
| pi | `gateway/orchestrator`, `brain`, `think` or `code` |
| omp, OpenCode | the same four gateway routes as pi |

If the harness cannot set the subagent's model, the subagent inherits the
session's model: continue only if that model is allowed, otherwise stop and say
so.

## Limits

An in-harness subagent shares the session's permissions and connected tools;
its read-only status rests on the tools you give it and its instructions, not
on a separate sandbox. It also shares a vendor with the author: this is a fast
self-check, not the independent second opinion a `review-loop-*` command gives.
