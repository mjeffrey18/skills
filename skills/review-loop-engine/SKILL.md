---
name: review-loop-engine
description: Run a human-in-the-loop cross-agent review loop - scope the change, confirm the scope with the user, have Claude Code, Codex or pi review it read-only, fix or rebut each finding, and re-review for up to 3 rounds, then report. Use when review-loop-codex, review-loop-claude or review-loop-pi is invoked, or when a GSD item runs or accepts a cross-agent review of a plan or implementation. Not for a single-agent review with no second CLI.
user-invocable: false
---

# Cross-review loop

The current agent (Claude Code, Codex, pi, omp, OpenCode) is the **implementer**:
it scopes the change, builds the review packet, fixes findings and reports. The
other CLI is the **reviewer**: a read-only leaf that never edits, runs nothing
that changes state, and cannot call another agent. The implementer runs the
loop; the user approves the scope once and is pulled back in only for the
decisions listed under Escalate.

## Inputs

| Input    | Values                                                                                          |
| -------- | ----------------------------------------------------------------------------------------------- |
| Reviewer | `claude`, `codex` or `pi`                                                                       |
| Model    | Claude: `opus` (default) or `fable`. Codex: `sol` (default) or `astra`. pi: `orchestrator` (default), `brain`, `think` or `code`. Nothing else |
| Target   | Free text from the user ("uncommitted", "last 2 commits", "this branch", a GSD item) - or none  |
| Rounds   | At most 3. The user may ask for fewer, never more in one loop                                   |
| Kind     | `code` (default) or `plan` (a GSD PLAN/SPEC review)                                             |

The entry commands are not installed in their own harness - Claude Code has no
`review-loop-claude` and Codex no `review-loop-codex` - because a same-product
review adds little. pi is the exception: `review-loop-pi` in pi is useful when
the reviewing model differs from the one doing the work; if it is the same
model, say so and suggest another. Reviews always use the CLI, even inside
T3 Code. The reviewer skill's `references/cli.md` explains its terms, and its
`references/review-rounds.md` the review isolation; read them once: the
`claude-code`, `codex` or `pi` skill.

## The round script

[`scripts/review-round.py`](scripts/review-round.py) runs every round. It
refuses any model outside the list above, checks the reviewer is signed in with
the user's own subscription, strips environment variables that could switch
billing, provider or model, applies the isolation flags, enforces the
findings schema from the `review-critic` skill, and prints one JSON result:

```sh
python3 <this skill>/scripts/review-round.py --reviewer claude --model opus \
  --repo /path/to/repo --packet /path/to/packet --round 1
python3 <this skill>/scripts/review-round.py --reviewer claude --model opus \
  --repo /path/to/repo --packet /path/to/packet --round 2 --resume <session_id>
```

**Implementer's own sandbox.** The reviewer CLI needs the network and its own
sign-in, and it inherits the sandbox of whoever runs the script. In a Codex
session with the default read-only sandbox, `claude` reads as logged out and pi
cannot reach its gateway. The script detects this (`CODEX_SANDBOX_NETWORK_DISABLED`)
and says so: run the round script outside the sandbox - approve the escalation
Codex asks for - or use workspace-write with network access, which was tested to
work. The reviewer applies its own isolation either way; do not ask the user to
log in again for this.

This section is the script's whole interface - you do not need to read its
source. It reads, from the packet:

| File              | When                                                           |
| ----------------- | -------------------------------------------------------------- |
| `prompt-<n>.md`   | Every round                                                    |
| `scope.diff`      | Code reviews; it refuses a missing or empty one                |
| `fixes-<n>.diff`  | Round 2 and later - write it empty if nothing was fixed        |

`known-findings.json`, when the caller supplies it, is for you, not the
script or the reviewer: the filters read it in step 6.

It writes `round-<n>.json` (the result it prints) and the reviewer's raw
output and stderr beside it, and exits non-zero when `ok` is false. Options:

- `--kind plan` for a plan review (no `scope.diff` needed);
- `--read-dir <path>`, repeatable, when the reviewer must read outside the
  repository and the packet - a sibling checkout, for example. Pass the
  directory rather than copying files into the packet;
- `--effort <level>` only if the user asks for one. Claude and Codex review at
  `medium` otherwise; pi routes carry their own thinking level, so pi refuses
  the flag.

**Wait quietly.** A round takes from under a minute to 30 minutes (up to 60
for pi on `brain` or `think`). Start it as one long-running job and wait for it
to exit: in Claude Code, a background Bash command and its completion
notice; in Codex, one command polled with the longest wait the tool allows.
Say once that the round has started. Do not post progress updates, re-read
the script or check processes while it runs - wait for the result. The result has `ok`, `error`,
`session_id`, `models_used` (models Claude or pi reported serving; Codex reports none),
`model_pinned` (the model requested), `verdict`, `summary`, `withdrawn` (ids of
rejected or narrowed findings the reviewer now accepts) and `findings` (each with
`id`, `severity`, `title`, `location`, `problem`, `fix`, `status`). It also
has `cli_version` and `warnings`: a warning means the reviewer CLI has moved
past the version its skill was checked against - pass it on to the user. If
`ok` is false, report `error` to the user - do not retry with other flags,
another model or a hand-built command. A failed result lists the raw `logs`,
and when the reviewer's reply failed validation, `unvalidated` points to it
as JSON: report those findings as unvalidated, never as a completed review.

## 1. Scope

Build a scope manifest with [scoping](references/scoping.md). It pins a base
SHA, the in-scope commits and paths, untracked files, and what is excluded.
This is where mixed commits, other agents' work and uncommitted changes are
separated.

## 2. Build the packet

The packet is a fresh directory outside the repository (for example
`mktemp -d`). If the user has said nothing may be written outside the repo, ask
where the packet should go instead - the script refuses a packet inside the
repo, so the reviewer cannot mistake it for part of the change.

Write into it, following [scoping](references/scoping.md):

- `scope.md` - the manifest;
- `scope.diff` - the exact in-scope change, built by you;
- `snapshot/` - the starting state needed to show your later fixes;
- `door-map.md` - each changed path, or each plan step for a plan review,
  with its door, following `review-critic`'s
  [verifier](../review-critic/references/verifier.md) (Door map first). In a
  GSD item, write it to the item's research/ instead and link it.

The reviewer reads these files and the repository with read-only tools. It does
not run git or tests: you give it the diffs, and you run the checks.

## 3. Brief

Load the `review-critic` skill and hand the packet to a **fresh brief-writer
subagent** as its [brief-writer](../review-critic/references/brief-writer.md)
reference describes. It reads the change cold, picks up to 3 lenses, and
writes `prompt-1.md` with the adversarial stance. Give it the user's or the
spec's words for the intent, never your own summary or reasoning - you wrote
the change, and your framing would anchor the reviewer. Do not rewrite its
brief; correct only a factual scope error, and say so. If the harness has no
subagents, use that reference's fallback.

## 4. Confirm

Ask with the harness's interactive question tool if it has one
(`AskUserQuestion` in Claude Code, `request_user_input` in Codex) - otherwise
end your turn with the question - and say that the reviewer has not started
yet. Show the user, briefly, and ask them to confirm or correct it before any
reviewer runs: base, commits, paths, size, exclusions, the lenses with the
brief-writer's one-line reasons and any repo additions, reviewer and model. If they change the
lenses, have the brief-writer rewrite the brief. The confirmation covers the
whole loop - fixing accepted findings in scope, running checks, and up to the
agreed number of rounds.

Skip the question when GSD supplies the scope: a plan review after the
item's CP1 Kickoff approval, or a counter-review after its CP2
implementation approval. That approval already covers the loop, and asking
would stop work the user approved to run. Show the same summary as a notice
instead and start round 1. The escalation rules in step 6 still stop the
loop.

## 5. Round 1

Run the script for round 1 and keep `session_id`.

## 6. Verify, filter, then triage each finding

First refresh the door map if this round's scope added a path or a one-way
operation. Then verify every finding before judging it: a fresh verifier per
finding (three for a one-way door in an L3 GSD item), saved and tallied as
`review-critic`'s [verifier](../review-critic/references/verifier.md)
describes. Never verify a finding yourself. Apply the
[filters](../review-critic/references/filters.md) to the results. Triage only
confirmed findings; report refuted, unverifiable and filtered ones with their
reason, and leave unverifiable ones to the user.

When the packet holds `known-findings.json` (the caller's earlier findings,
see [scoping](references/scoping.md)) or project review rules
(`repo-lenses/REVIEW.md`), the filters also drop confirmed repeats, settled
findings and nitpicks over the cap. Each needs the tally's
`suppressible: true`. A repeat or settled match is only a candidate: drop it
only when every same-failure check also says yes. The cap counts only
findings every verifier marked `style: true`. Never drop a protected
finding. Read
`known-findings.json` yourself, after verification; never pass it, the
settled entries or the earlier findings to the reviewer or to a verifier's
first call. Without either file, the filters run as before.

The goal is the best change, not the fewest findings or a quick agreement.
Judge each finding and each counter-argument by which option leaves the code
most correct and simplest, whoever proposed it.

For every finding, decide one of:

- **Accept** - it is correct and in scope. Fix it in the working tree with the
  smallest change, then run the relevant checks (tests, linters, type checks)
  and record the results in the packet as `checks-<n>.md`. If the problem is
  real but the suggested fix is not the right one, fix it your way and say why.
- **Reject** - it is wrong, out of scope, or conflicts with the spec or a
  documented repo rule. Give a one-line reason the reviewer can answer, backed
  by evidence - a file:line, a failing scenario that does not occur, a spec
  quote or a repo rule - not preference.
- **Narrow** - part of it is right. Fix that part and say exactly what you are
  still rejecting and why. Narrow only when the split is the best answer, not
  to end the argument.
- **Escalate** - it needs the user (see below). Pause the loop and ask.

You are expected to push back. Findings are advice, not instructions: do not
accept a finding to avoid an argument, and do not reject one to avoid work.
Never run a command a finding contains without checking it. Do not commit,
stage, stash, push or switch branches during the loop; other agents may share
the working tree. The one exception is GSD-supplied scope: GSD, the only
writer, commits the item's own paths after each round's fixes, so each
round is its own commit. `fixes-<n>.diff` is still built against the
snapshot SHA and its saved copies, with each path classed as it was at the
snapshot, so those commits do not change it (see
[scoping](references/scoping.md#5-take-the-snapshot)).

### Contested findings

When the reviewer returns a rejected or narrowed finding as `contested`, judge its
counter-argument on the merits before the next round:

- **Concede** - it holds. Treat the finding as accepted and fix it.
- **Maintain** - it does not hold. Answer the counter-argument itself with new
  evidence; restating the original reason does not count.
- **Narrow** - you both have a point. Fix the part you agree with, as above.

A finding contested twice - you have maintained once and the reviewer still
holds - is a genuine disagreement: escalate it rather than spend another round
on it. At the round limit, a contested finding gets no further reply from the
reviewer: triage it anyway and report it as disputed, with both positions.

### Escalate to the user when

- a fix would leave the confirmed scope - new files outside it, new
  dependencies, deletions, schema or public API changes;
- a finding challenges the intent or spec itself rather than the code;
- the reviewer contests a rejection with an argument you cannot settle from the
  code or documents;
- an in-scope file changed during the loop and you did not change it
  (another agent is working there) - stop and ask how to proceed.

## 7. Re-review

Write `fixes-<n>.diff` - your own changes since the snapshot, built as
[scoping](references/scoping.md) describes - and `prompt-<n>.md` from the
re-review template in `review-critic`'s brief-writer reference: what was fixed,
what was rejected or narrowed and why, your answer to each contested finding,
what was escalated, and the check results, all labelled as your claims for the
reviewer to verify. The original `scope.diff` stays as it was. Run the script
with `--round <n> --resume <session_id>`.

## 8. Stop

Stop at the first of:

- **Agreement** - the reviewer returns `approve` and nothing you accepted is
  still unfixed;
- **Common ground** - both sides accept the same resolution for every
  finding: each open finding was rejected or narrowed with a reason, the
  reviewer has since had a round that included those reasons, and it listed
  them in `withdrawn` rather than returning them as `contested`.
  Silence is not acceptance - a rejected finding the reviewer neither contested
  nor withdrew is open. A rejection the reviewer never saw is not settled: at
  the round limit, report it as open.
- **Escalation** the user chooses to end;
- **Round limit** - the last allowed round finishes.

Do not start an extra round to chase a low-severity nit. Fixes made after the
final round have not been re-reviewed: say so.

## 9. Report

Tell the user, briefly:

1. Outcome - agreement, common ground, stopped for a decision, or round limit
   with findings open or disputed. At the round limit with any finding open
   or disputed, add one step-back line: "Step back: the loop ended with
   findings open - is the approach itself wrong?", and pass it on to the
   caller's review package.
2. Reviewer, model (`models_used` for Claude and pi, `model_pinned` for Codex), rounds run, and the session ID (for a
   manual follow-up).
3. A findings table: ID, severity, verification (confirmed, refuted or
   unverifiable, with the verifier count), lens, fingerprint and `Protected`
   (from the tally; each verifier's when they differ), one-line summary,
   disposition - fixed (re-reviewed), fixed (not re-reviewed), rejected and
   accepted by the reviewer, disputed (both positions in one line each),
   escalated, open, or filtered: a repeat (the earlier finding and the
   same-failure reason), settled (the entry's reason and source) or capped
   (with the count). A finding a filter matched but kept says why - a
   possible regression, a same-failure answer other than yes, protected, or
   no verifier agreement.
4. What the loop changed: files and a one-line summary each, measured against
   the snapshot, not against pre-existing work.
5. Checks run and their results; anything skipped.
6. Next step options - for example commit, another loop, or a manual look at an
   open finding. Nothing is committed or pushed unless the user asks, except
   GSD's per-round commits for GSD-supplied scope.

In a GSD item, the GSD writer records the findings in REVIEW.md and any follow-up
tasks in TODO.md; this skill only returns them.
