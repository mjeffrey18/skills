# Goal document template

**Read this when** writing the document in step 5 of `goal-builder`. Keep the headings and order - a reader (or a later agent) should find the same thing in the same place in every goal. Drop a section only when the rubric says its default does not apply; otherwise fill it with the default. Angle-bracket placeholders are replaced, never left in.

The core sections (Outcome through Stop conditions) map one-to-one onto the fields of a Hermes `/goal` completion contract - outcome, verify, constraints, boundaries, stop when - so a user on that harness can lift them straight out.

```markdown
# Goal: <one-line outcome>

Status: Ready | Needs answers | Split recommended · Readiness <n>/20 · <YYYY-MM-DD>

## Outcome

<One sentence. [artefact or system] is in [final state] for [users or use case].>

## Acceptance criteria

| #   | Criterion             | Verify with                             | Evidence to report                                         |
| --- | --------------------- | --------------------------------------- | ---------------------------------------------------------- |
| 1   | <observable property> | <command, inspection or artefact check> | <exit code, summary line, path, screenshot, cited section> |
| 2   | ...                   | ...                                     | ...                                                        |

## Quality gates

Deterministic checks that block completion. Each meets the rubric's gate eligibility rules and was safely run in the stated environment. Re-run against the final state for completion evidence.

| Command     | Working directory and prerequisites | Timeout | Pass condition and what it proves | Observed baseline result     |
| ----------- | ----------------------------------- | ------- | --------------------------------- | ---------------------------- |
| `<command>` | <directory; prerequisites>          | <limit> | <exit code and expected result>   | <result; evidence reference> |

<If none qualify, say "None confirmed" and explain why. Put proposed verifiers in the criteria table; classify missing prerequisites as non-blocking assumptions or blocking open questions. Never list a guessed command as a gate.>

## Constraints

Protected - must not change or regress:

- <interface, behaviour, compatibility promise>

Ask first:

- <actions requiring new approval under this goal's actual scope; preserve existing authorisation>

Never:

- Disable security checks, weaken tests or gates, expose secrets, rewrite unrelated history.

## Boundaries

In scope:

- <paths, systems, environments, tools>

Out of scope:

- <explicit exclusions>

Authoritative context (read first; earlier entries win on conflict):

- `<path or URL>` - <why it is authoritative>

Settled decisions - do not reopen:

- <decision>

## Execution policy

<Default: Inspect the authoritative context and produce a concise plan mapped to the criteria before mutating state. Work in the smallest coherent milestone that can be verified. After each milestone run its checks, tick it and any criteria it proved in Progress below, and leave the workspace resumable. Re-plan when evidence invalidates the approach rather than keeping a stale plan for consistency.>

## State and checkpoints

<Default: Progress is recorded in the section below, read before acting and updated before ending a turn or compacting context. Checkpoint with a clean commit at each verified milestone where repository policy allows.>

## Budget and stop conditions

Budget: <turns / time / retries / spend as applicable>

Stop and report when:

- <missing credential, unavailable system, unresolved product decision, irreversible unapproved action, contradictory authority, N different attempts failed>

On stop, report: blocker, evidence, approaches tried, current safe state, and the smallest decision or access needed.

## Recovery

<Default: Never repeat an identical failed action without new evidence or a changed hypothesis. Classify a failure (transient, environmental, specification, implementation) before acting. Reproduce before broad changes. Preserve logs and the minimal failing case. Roll back anything that moves away from the last known-good state. Escalate at a stop condition.>

## Final report

<Default: changed paths; verification output per criterion; dependency and configuration changes; remaining warnings; known risks; rollback notes; anything the user still has to do.>

## Assumptions and open questions

Assumptions (non-blocking, stated so they can be corrected):

- <assumption>

Open questions (blocking regardless of the score; any unresolved item prevents Ready):

- <dimension>: <question>

## Progress

Criteria - one box per row of the acceptance criteria table. Tick a box only once that criterion's evidence is recorded under Evidence; untick it if a later change invalidates that evidence. Before claiming completion, re-run every check against the final state, even for boxes already ticked.

- [ ] 1. <criterion>
- [ ] 2. ...

Milestones - the agent's own plan, written as `- [ ] <milestone> - <check>` before it mutates state and revised when it re-plans. The builder leaves this empty:

- None yet.

Log:

- Evidence:
- Decisions and rationale:
- Failed attempts and why:
- Blockers:
- Next action:
- Last known-good checkpoint:

## Readiness audit

Readiness: <n>/20 - Ready | Needs answers | Split recommended

<Apply all readiness conditions in the rubric. List each dimension's score and a short reason, including any remaining limitation.>

Material risks:

- <risk, or "None identified">

Open questions:

- <dimension: question, or "None" when Ready>
```
