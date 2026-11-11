# Brief-writer

Round 1's brief is written by a fresh subagent, not by the agent that made the
change. This file is what the caller hands it, what it does, and the templates
it fills. Later rounds use the re-review template at the end.

## Handing off

Spawn one subagent with the harness's own mechanism (Claude Code's Agent tool,
Codex `spawn_agent`, pi subagents, the omp or OpenCode task agent). Give it
read access to the repo and packet and write access to the packet only.
Writing a brief takes a minute or two: wait for it once with a long timeout,
not in short polls.

**Give it only:**

- the path to this skill and to the packet;
- `scope.md` (the manifest) and `scope.diff`, or for a plan review the plan and
  authority documents;
- the intent **in the user's words or quoted from the spec** - never the
  author's own summary;
- the paths of the spec and standards files;
- the kind (`code` or `plan`) and any lenses the user named.

The repo's own review rules, if any, are already in `<packet>/repo-lenses/`
(see [repo lenses](repo-lenses.md)), with the project review rules as
`REVIEW.md`; nothing extra needs handing over.

**Withhold:** the author's reasoning, design justifications, what it thinks is
risky or safe, what it already checked, and any earlier review of this change.
Never hand it the settled entries of the project review rules or the item's
earlier findings (`known-findings.json`): they would anchor the reviewer on
what was rejected before. They apply after verification, as filters.
If the only intent available is the author's, write "Intent: not stated - infer
it from the change and say what you inferred".

## The subagent's task

Pass this as its instructions, with the paths filled in:

```markdown
You write the brief for an adversarial code or plan review. You do not review
it yourself and you do not edit the repository.

1. Read <packet>/scope.md and <packet>/scope.diff (or the plan documents), cold.
2. Read <review-critic>/SKILL.md and pick up to 3 lenses from its table, by
   risk. A plan review always includes `plan`. Use `general` only if nothing
   else fits. If <packet>/repo-lenses/index.md exists, follow
   <review-critic>/references/repo-lenses.md: its repo lenses compete for
   the 3 places, and its extensions join their built-in lens.
3. If <packet>/repo-lenses/REVIEW.md exists and is the project review rules
   (not a lens or stage agent - see repo-lenses.md), read its front matter
   and keep: every `review_focus` entry; each `known_landmines` entry whose
   glob (first field; `**` crosses folders, `*` stays inside one) matches a
   changed path in scope.md. Ignore `settled`, `nitpick_cap`,
   `risk_paths`, `always_high` and `rollback`: the caller applies the
   nitpick cap after verification, so the reviewer reports every finding.
4. Note up to 5 places that deserve attack - as questions, not conclusions
   ("what happens to X when Y is nil?"). Do not say what is fine.
5. Write <packet>/prompt-1.md from the round 1 template in
   <review-critic>/references/brief-writer.md: inline the adversarial stance
   and each chosen lens file verbatim, with any repo additions after it as
   repo-lenses.md shows, fill in the project review rules from step 3 (or
   leave that section out when there are none), the scope, intent, spec,
   standards and your questions. Never copy a settled entry into it.
6. Reply with only: the lenses chosen, one line each on why, the repo
   additions and repo lenses used, whether project review rules were inlined
   (or the legacy-name collision found), any problem with the repo index,
   and the path you wrote.
```

The caller shows the lenses and reasons to the user at scope confirmation, and
changes only factual scope errors in the brief - telling the user if it does.

**No subagents available:** the caller fills the template itself, using only
the neutral fields - scope, the user's or spec's intent, spec, standards,
lenses chosen from the signals table and the packet's repo index, as
[repo lenses](repo-lenses.md) describes, and the project review rules from
the packet copy as step 3 says. It leaves the attack questions out rather
than write them from its own knowledge of the change.

## Round 1 template - code

```markdown
You are reviewing a change made by another coding agent. Review only: do not
edit files, and do not invoke Claude Code, Codex, pi or any other agent.

<adversarial stance, verbatim>

## Scope

<scope manifest from scope.md>

The in-scope change is in <packet>/scope.diff. Untracked files appear there as
new-file diffs - being untracked is expected, not a finding. Excluded items are
context: report a problem there only if an in-scope change causes it.

## Intent

<the user's words or a spec quote - or "not stated - infer it from the change
and say what you inferred">

## Spec

<path to the spec, issue or GSD SPEC.md, or pasted requirements - or "none">

## Standards

Read these and check the change against them: <standards files>. A documented
repo rule overrides general preference.

## Lenses

<each chosen lens file, verbatim, followed by its repo additions; then any
chosen repo lens - see repo-lenses.md for the headings>

## Project review rules

From .agents/rules/review/REVIEW.md at the review's base commit. A
documented repo rule overrides general preference.

Review focus:

- <each review_focus entry, verbatim>

Known landmines on the changed paths:

- <glob> - <what bites> (<source>)

<Omit a part that is empty; omit the section when the repository has no
project review rules.>

## Where to attack first

<up to 5 questions from the brief-writer - or omit this section>

## How to work

Read <packet>/scope.diff first, then the surrounding code - callers, tests,
config - wherever the diff alone is not enough. Use read-only file tools. Do
not run git, tests or builds; the author runs checks and reports results.

## Output

- One finding per problem, most severe first, ids F1, F2, ...
- `lens`: the lens that found it. `location`: file:line. `problem`: what is
  wrong and the concrete failure. `evidence`: what you read and checked.
  `fix`: the smallest change that resolves it. `status`: "new".
- `verdict`: "approve" only if there are no high or medium findings, otherwise
  "changes_requested". `summary`: what you attacked and the overall result, in
  two or three sentences. `withdrawn`: an empty list in this round.
```

## Round 1 template - plan

As the code template, with these sections replaced:

```markdown
## Scope

- Plan: <PLAN.md> (and <SPEC.md / TODO.md> if present)
- Authority: <IDEA.md> (scope and completion boundary), <DECISIONS.md>
- Code the plan touches: <paths>

## How to work

Read the authority documents first, then the plan, then the code it touches.
There is no diff for a plan review. Use read-only file tools; do not run git,
tests or builds.
```

`location` is file:section or file:line.

## Re-review template - round 2 and later

The caller writes this; the author's notes are labelled as claims.

```markdown
Round <n> of at most <max>. The original change is still in
<packet>/scope.diff (or the plan documents). The author's changes since the
start of the loop are in <packet>/fixes-<n>.diff.

## The author's claims

Fixed:

- <F-id> - <what changed, file:line>

Rejected:

- <F-id> - <one-line reason and evidence>

Narrowed (partly fixed, the rest rejected):

- <F-id> - <what was fixed; what is still rejected and why>

Answers to last round's contested findings:

- <F-id> - conceded and fixed at <file:line> / maintained: <new evidence>

Escalated to the user (do not report again):

- <F-id> - <decision>

Checks the author reports running:

- <command> - <result>

<re-review addendum from adversarial.md, verbatim>

Return only findings that are new or still unresolved, keeping existing ids.
List the id of every rejected or narrowed finding you now accept in
`withdrawn`; a rejected finding that is in neither list is treated as open.
Status: "still_open" if the fix did not resolve it; "contested" for a rejected or narrowed
finding you still hold, with your counter-argument in `problem`; "new" for
anything else. Do not edit files or invoke other agents.
```
