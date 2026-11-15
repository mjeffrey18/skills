---
name: review-council
description: User-invoked review panel - two or three reviewers on different CLIs (Claude Code, Codex, pi) review the same change in parallel for one round, each finding is verified, and the results are merged into one report. Nothing is fixed unless you pass `fix=on`. Invoke as `review-council [heavy|moderate|light|<models>] [target] [fix=on] [cli=on]`, e.g. `review-council heavy this branch` or `review-council astra opus last 2 commits`. For one reviewer with fix-and-re-review rounds, use review-loop-codex, review-loop-claude or review-loop-pi.
disable-model-invocation: true
---

# Review council

Several reviewers read the same change at once, each on a different CLI. You
are the **host**: you scope the change once, start the members, have their
findings verified and merge them into one report. Inside T3 Code each member
is a child thread on its own provider and model, so the reviewer is the
thread the user sees. Elsewhere each member is a read-only CLI round run by
`review-loop-engine`'s round script, exactly as in a review loop.

A council is one round and review only. Its value is breadth - three models
miss different things - and verification, not agreement: a finding counts
because a verifier confirmed it, not because two members raised it.

## Arguments

Read the text after the command name:

- **Mode** - the first word, if it is one of these:

  | Mode       | Claude Code | Codex   | pi             |
  | ---------- | ----------- | ------- | -------------- |
  | `heavy`    | `fable`     | `astra` | `brain`        |
  | `moderate` | `opus`      | `sol`   | `orchestrator` |
  | `light`    | `opus`      | `sol`   | -              |

- **Custom members** - instead of a mode, two or three model words from
  `review-loop-engine`'s model list, such as `astra opus` or
  `fable sol think`. Each word names its own CLI: `opus` and `fable` are
  Claude Code; `sol` and `astra` are Codex; `orchestrator`, `brain`, `think`
  and `code` are pi. Two members on one CLI are allowed. Refuse any other
  model name: say which words are allowed, and stop.
- **Target** - the rest of the text, such as `uncommitted`, `last 2 commits`,
  `this branch` or a GSD item. If there is none, scope from the current
  session's work.
- **Fixing** - `fix=on` lets you fix the confirmed findings after the report.
  Without it, no file in the repository changes.
- **Runtime** - `cli=on` runs every member as a CLI round, even inside
  T3 Code.

The model words resolve to the newest model through the engine and the CLI
skills, so this skill names no model ID.

## Run

1. **Load.** Load the `review-loop-engine` and `review-critic` skills; if
   either is missing, say which and stop. For a member that will run as a
   CLI round, also load its CLI skill (`claude-code`, `codex` or `pi`) and
   read its `references/review-rounds.md` once. Your own harness does not
   install its own CLI skill; the engine's round-script section is enough
   for that member. For a Claude Code member that will run as a T3 Code
   child, load `claude-code` for its subscription check.
2. **Scope and packet.** Follow the engine's sections 1 and 2 once: the
   manifest, `scope.diff`, `scope.md`, `snapshot/` and `door-map.md` in a
   fresh packet outside the repository.
3. **Brief.** Follow the engine's section 3 once. Every member gets the same
   `prompt-1.md`, so they answer the same question and their findings can be
   compared.
4. **Confirm.** Ask one question with the harness's interactive question
   tool, and say that no reviewer has started. Show the base, commits, paths,
   size, exclusions, the lenses with their reasons, and the members.
   - If the user typed a mode or members, show them.
   - If not, offer `heavy`, `moderate` and `light` as the choices, each with
     its members, and let the user type custom members as free text.
     Recommend `heavy` when the door map has a one-way door, `light` for a
     small two-way change, and `moderate` otherwise.

   The confirmation covers the whole council. In a GSD item whose checkpoint
   already approved the review, show the same summary as a notice and ask
   only for the mode, if it was not given.

5. **Start every member at once.** Give each member its own folder with a
   copy of the packet. Record the [repository state](#repository-state). Then start
   every [member](#members) in one turn, so they run side by side. Say once
   that the members have started and how long the slowest may take (pi on
   `brain` or `think` can take 60 minutes).
6. **Leave the scope alone while they read.** Members read the working tree.
   Until the last one finishes, do not edit, stage, commit or switch
   branches. If the user gives you other work meanwhile, do it only when it
   stays outside the scoped paths.
7. **Verify and filter.** As each member finishes, verify each of its
   findings and apply the filters, exactly as the engine's section 6
   describes up to triage. Never verify a finding yourself, and never skip a
   finding because another member raised something similar: the second
   verifier is the independent check. Run at most 4 verifiers at once and
   queue the rest, so a member with many findings does not flood the machine
   or the provider.
8. **Merge.** Wait for every member, then build one list. Two findings are
   the same issue only when they describe the same failure at the same site;
   a matching fingerprint is a candidate, not proof. Give each distinct issue
   one row, the highest severity any member gave it, and the members that
   raised it. Keep refuted, unverifiable and filtered findings in their own
   list with the reason. If a verifier noticed a different problem while
   checking a finding, list it apart as unreviewed.
9. **Report**, as below. Then stop, unless `fix=on`.
10. **Fix (`fix=on` only).** Triage and fix the confirmed findings as the
    engine's section 6 describes - accept, reject, narrow or escalate - and
    run the affected checks. These fixes have not been re-reviewed: say so.

## Members

Choose the runtime for each member separately.

Run a member as a **T3 Code child** when all hold:

- the T3 Code `delegate_task` and `orchestrator_capabilities` tools are in
  your tool list (they may be deferred - search for `delegate_task` once);
- `orchestrator_capabilities` lists the member's provider with
  `canRunChildTask: true` (and `canRunCrossProviderChildTask` when it is not
  your own provider);
- that provider lists the member's model.

Otherwise run it as a **CLI round**. A missing provider or model moves that
one member to the CLI; it never changes the member's model.

### T3 Code child

The child is the reviewer. Call `orchestrator_capabilities` once, then start
each member with `delegate_task`, `mode: "async"`, shared isolation, a title
that names the member, such as `Council: Codex Astra`, and:

| Member's CLI | `target.providerInstanceId` | `target.model`                             | Also set                                                  |
| ------------ | --------------------------- | ------------------------------------------ | --------------------------------------------------------- |
| Claude Code  | `claudeAgent`               | the ID listed for Opus or Fable            | `options: {"effort": "medium"}`                           |
| Codex        | `codex`                     | the ID listed for Sol or Astra             | `options: {"reasoningEffort": "medium"}`                  |
| pi           | `pi`                        | the ID listed for the route word           | `options: {"thinking": ...}` - the level listed for that route |

Always set the options: a child does not inherit them from a parent on
another provider, and the catalogue default can be lower. Use the official
provider instances above, not another variant of the same provider, unless
the user names one.

Leave `interactionMode` unset. Plan mode asks the child to end its turn with
a plan or a question, which a reviewer that must reply with JSON cannot do.

**Claude subscription check.** Before starting a Claude Code member as a
child, run the check in the `claude-code` skill's
`references/t3code.md` (Subscription). If it fails, run that member as a CLI
round and pass its `problems` on to the user. If you are Claude Code
yourself, that skill is not installed and the check cannot run, so run your
Claude Code members as CLI rounds: the round script clears API-key routes
and pins the helper models before the reviewer starts. Your own session's
settings do not prove what a new child starts with.

Write the task to `task.md` in the member's folder: this wrapper, then the
whole of `prompt-1.md`, unchanged. Give `delegate_task` a one-line task that
names the file, such as "Read <folder>/task.md and follow it exactly", so a
long brief is not pasted into the thread.

```markdown
You are one reviewer in a review council. This is a read-only review: do
not edit, create or delete any file in the repository, do not run commands
that change state, do not stage, commit, push or switch branches, do not
start other agents, do not enter plan mode, and do not ask the user
anything.

Repository: <path>
Packet: <this member's folder> - read scope.md, scope.diff and snapshot/
there. Do not run git or tests; the diff is the change under review. Use
only tools that read and search files in the repository and the packet. Do
not run scripts, and do not connect to any other machine or service.

Follow the brief below. Reply with only the JSON object it describes, and
nothing else. The reply must validate against
<review-critic>/references/findings.schema.json: read it first, and give
every finding every required field, including `title` and `status`
("new").

<contents of prompt-1.md>
```

T3 Code wakes you as each child finishes; do not poll, and stop a child you
no longer need with `task_cancel`. When one finishes:

1. Check the returned `model` when T3 Code reports one. If it is not the
   one you asked for, report the member as failed. If none is reported, say
   in the report that the model was requested, not confirmed.
2. Save its reply as `round-1.json` in the member's folder and run
   `python3 <review-loop-engine>/scripts/review-round.py --validate <file>`.
   If it fails, mark the member unvalidated in the report, never as a
   completed review. Still verify the findings you can read, so they are
   not lost.
3. Compare the [repository state](#repository-state) with what you
   recorded. A change you did not make means a member wrote to the
   repository: name the change and the members that were running, leave it
   in place, and tell the user.
4. Note in the report any command the member ran beyond reading files, or
   any other machine it reached, as a warning against that member.

### Repository state

Three values, taken in the repository before the members start and again
after each one finishes:

- `git rev-parse HEAD`;
- `git status --porcelain --ignored`, which also lists new ignored files;
- `git diff HEAD | shasum`, which changes when a file that was already
  modified is edited again.

This catches a write to the checkout. It does not catch a change to a file
that was already untracked or ignored, a write outside the repository, or
an effect on another system.

### CLI round

Run the engine's round script for round 1 in the member's folder as a
long-running job, started with the others, and wait quietly as the engine
describes. If the harness cannot run jobs side by side, run them one after
another.

### What a T3 Code child gives up

A review loop always uses the CLI, because it needs the reviewer's session
for later rounds and the round script's guarantees. A council runs one round,
so inside T3 Code it trades those for a thread the user can watch and stop:

- the child is read-only by instruction, not by a sandbox, and it shares
  your checkout - hence the repository state check, with the gaps it names;
- it loads the user's normal configuration, tools and connectors, so it is
  not the isolated leaf a CLI round is;
- its reply is validated after the fact, not forced into the schema.

If the user asks for the CLI, or passes `cli=on`, run every member as a CLI
round.

## When a member fails

If a child fails, a round returns `ok: false`, or a reply does not validate,
report the error and carry on with the other members. Do not retry with
other flags, and do not put another model in its place. With fewer than two
members finished, report what you have and say that it is one review, not a
council.

## Report

1. **Outcome** - how many members finished, and the count of distinct
   confirmed issues by severity.
2. **Members** - a table: member, the model that served it, its T3 thread
   link or CLI session ID, verdict, findings raised, confirmed and refuted,
   and any warning.
3. **Confirmed issues** - a table: number, severity, the problem in one line
   with its location, raised by, `Protected`, and the suggested fix. Keep the
   `spec` findings apart from the standards view, as `review-critic`'s
   Reporting section describes.
4. **Not confirmed** - refuted, unverifiable and filtered findings, each with
   its member and the reason in one line.
5. **Your decisions** - any confirmed issue that challenges the intent or
   spec, or whose fix would leave the confirmed scope.
6. **Next step** - one recommendation. Usually `triage` to settle the
   decisions, then fix; for a second round on the fixes, a `review-loop-*`
   command with the member that found the most.

If the change has an open pull request, offer to record the result in its
description under a `## Council review` heading: the members table and the
confirmed issues with their outcome. Edit the description, do not post a
comment, and only after the user agrees. In a GSD item, GSD stays the document
writer: return the members, findings and verification for it to record in
REVIEW.md.

## Limits

- One round. A council never loops until every member approves, and it gives
  no scores: a later round belongs to a review loop.
- The member on your own harness's provider shares a vendor with the author.
  It is a fresh session, so it still counts as one voice, but it is the
  least independent of the three.
- More members do not make a finding more correct. Report agreement as
  information, and let verification decide.
