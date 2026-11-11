# Verifier

A review finding is a claim. Before anyone acts on it, a fresh verifier checks
it against the version that was reviewed. The reviewer's findings schema does
not change: verification runs afterwards, on the implementer's side, in
`review-loop-engine` (section 6) and `review-local`.

## Door map first

Each round builds or refreshes the door map from its own pinned scope before
verification: `door-map.md` in the packet, or `research/<date>-door-map.md`
in a GSD item. It lists each changed path - or, for a plan review, each plan
step - with its door and a one-line reason. One-way doors by default:

- schema or data migrations, and deletions;
- auth, permissions and secrets;
- deploy and infrastructure scripts;
- payments and sent messages;
- public API removals.

Everything else is two-way. An unclear case is proposed to the user; an
unresolved one counts as one-way. A later round whose fixes add a one-way
operation refreshes the map before its findings are verified.

## How many verifiers

- One fresh verifier per finding, at every tier.
- Three for a finding on a one-way door in an L3 GSD item, combined with
  `review-round.py --tally --expect 3`: a result needs two distinct verifiers
  agreeing, otherwise it is `unverifiable`.

## Who verifies

Spawn a fresh subagent with the harness's own mechanism (Claude Code's Agent
tool, Codex `spawn_agent`, pi subagents, the omp or OpenCode task agent), with
read-only tools. Each verifier is a new agent: never reuse one across findings
or votes, and never verify a finding yourself - you would grade your own work.

When the harness has no subagents, run a separate read-only CLI call instead:
`claude -p` with read-only tools, `codex exec --sandbox read-only`, or `pi -p`
on a reviewer route, on an allowed model (review-local, Reviewer model). If no
fresh call is possible, the finding is `unverifiable`: show it to the user,
and do not act on it as confirmed.

## The verifier's task

Give it only: the one finding (as the reviewer wrote it), the packet path
(`scope.md`, `scope.diff` or `snapshot/`, the door map, the review kind) and
the authority documents (spec, IDEA.md, PLAN.md). Withhold your view of the
finding. Pass this as its instructions:

```markdown
You verify one review finding. You do not fix anything, edit files, run
commands that change state, or start other agents.

1. Read the finding below, then the reviewed version: <packet>/scope.diff and
   <packet>/snapshot/ (or the pinned commit named in <packet>/scope.md), not
   the working tree, which may have moved on. For a plan review, read the
   plan documents in the packet snapshot and the authority documents.
2. Decide whether the failure the finding describes really happens in that
   version: trace the code path, the caller or the plan step it names.
   - confirmed: you reproduced the failure by reading or by a read-only check;
   - refuted: the code or plan prevents it - say exactly where;
   - unverifiable: the reviewed version is unavailable, or the evidence is
     not enough either way.
3. Name the finding's fingerprint, whatever your result: the path; the
   symbol - the enclosing function or method, the heading for a document,
   or `*`; and the rule class, from this list: auth, injection, secrets,
   data-exposure, input-validation, error-handling, race, idempotency,
   migration, resource-leak, edge-case, spec-gap, test-gap, convention,
   docs, other. Pick the class for what the failure is, not for the label
   the reviewer used.
4. Judge by meaning, not by the reviewer's label or lens, whether the
   finding raises a security, migration, idempotency or concurrency
   concern: "no", "unsure", or the concern's name ("security", "migration",
   "idempotency", "concurrency"). A race filed as an edge case is still
   "concurrency"; a missing permission check filed as "other" is still
   "security". When in doubt, say "unsure".
5. Say whether it is only a style or preference point with no effect on
   behaviour: style true or false.
6. Reply with only this JSON object:
   {"id": "<finding id>", "result": "confirmed|refuted|unverifiable",
    "evidence": "<file:line or section, and what you checked>",
    "fingerprint": {"path": "<path>", "symbol": "<symbol or *>",
                    "rule_class": "<class>"},
    "protected": "no|unsure|security|migration|idempotency|concurrency",
    "style": true|false}

<the finding, verbatim>
```

The fingerprint, `protected` and `style` let the [filters](filters.md) match
a finding with earlier ones without showing them to the reviewer. A reply
without them is still a valid vote, but the finding can then never be
dropped as a repeat, as settled or by the nitpick cap.

## Same-failure mode

A fingerprint match with an earlier finding, or with a settled entry in the
project review rules, is only a candidate: two different defects can share
a path, a symbol and a class. Before a filter drops a candidate, ask a
fresh verifier - one per verifier the finding had, never one that saw the
finding before - whether both describe the same failure. Give it the new
finding, the earlier finding's text (or the settled entry's rejected claim),
the rejection reason (or the entry's lasting reason) and the packet, and
pass this as its instructions:

```markdown
You compare one new review finding with an earlier one that was rejected.
You do not fix anything, edit files, run commands that change state, or
start other agents.

1. Read the new finding, the earlier finding and the reason it was
   rejected, then the reviewed version: <packet>/scope.diff and
   <packet>/snapshot/ (or the pinned commit named in <packet>/scope.md).
2. Decide whether both describe the same failure at the same site - the
   same input or state, the same wrong result - and whether the rejection
   reason still holds for the current code.
   - yes: the same failure, and the reason still holds;
   - no: a different failure, or the reason no longer holds - say which;
   - unsure: you cannot tell from the code and the texts.
   The same function and class is not enough: an earlier finding about
   empty input to parse() is a different failure from a later one about
   overflow in parse().
3. Reply with only this JSON object:
   {"id": "<new finding id>", "earlier": "<earlier finding id or settled
    entry source>", "same_failure": "yes|no|unsure",
    "reason": "<what you compared, and why>"}

New finding:
<the new finding, verbatim>

Earlier finding (or settled entry's rejected claim):
<its text>

Rejection reason (or the entry's lasting reason):
<the reason>
```

Only a yes from every same-failure call lets a filter drop the finding;
anything else keeps it.

## Saving and counting

Save each reply as `verification/<review>/round-<n>/<finding id>-<k>.json`
(in a GSD item under research/, otherwise in the packet; a review-only pass,
such as review-local `fix=off`, keeps them in the packet). `<review>` is the
run's start time, kind and reviewer, for example
`2026-11-03T1412-counter-codex`; append `-2` if that folder exists. Never
overwrite an earlier reply. Add `"call"`: the verifier's own session, agent or
process id, so distinct calls can be told apart. Check each file with
`review-round.py --validate-verdict FILE`; a reply that fails, or a verifier
that errors or times out, is `unverifiable` and shown to the user, never
dropped silently. Combine with `review-round.py --tally --expect N FILE...`
(N is 1, or 3 for an L3 one-way door): one vote per distinct call, so a copied
reply never makes a majority. The tally also lists every verifier's
fingerprint, `protected` and `style`, whatever its vote, with
`metadata_agreed` (every confirming verifier gave the same fingerprint and
style) and `suppressible` (agreed, all N distinct verifiers replied, and
every reply - confirming, refuting or unverifiable - says `protected: no`),
and `suppression_blocked` with the reasons when it is not. Two agreeing
replies out of 3 can confirm a finding but never make it suppressible. Its vote result does not depend on them.

Save each same-failure reply as
`verification/<review>/round-<n>/same-failure/<finding id>-<k>.json`, with its
`"call"`, and check it with `review-round.py --validate-same-failure FILE`. A
reply that fails, or a call that errors or times out, counts as unsure.

The round folder holds only the verifiers' replies; do not save tally output
or notes there. Record the result beside the finding - in a GSD item,
REVIEW.md's `Verified`,
`Verifier` and `Method` fields, linking the saved files and the reviewed
revision, and `Lens`, `Fingerprint` and `Protected` from the replies - then
apply the [filters](filters.md).
