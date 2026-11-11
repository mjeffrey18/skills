# Readiness rubric

**Read this when** scoring a goal (step 2 and step 5 of `goal-builder`) or building a round of questions (step 4). Each dimension scores 0, 1 or 2. The goal is **Ready** only when all of these conditions hold:

- The total is at least 16/20.
- Outcome, Acceptance criteria, Verification, Boundaries and Budget each score 2.
- No unresolved material blocker remains: a gap that changes correctness, acceptance, scope, required authorisation, feasibility or the ability to verify and stop.
- The work fits one bounded outcome; otherwise use `Split recommended`.

Check blockers independently of the score. Defaults and a high total cannot compensate for a missing critical decision. A future action that is explicitly excluded or covered by an agreed approval checkpoint is not itself a drafting blocker; uncertainty about whether the goal requires that action is.

Where a dimension has a **default**, write it into the document without asking unless the task makes it unsuitable. Where it has none, use supplied answers or inspected facts first, and ask only for remaining material gaps.

Applying a default that fits the task scores that dimension 2. For Incremental execution, Persistent state, Recovery and Final report the default is the whole dimension, so a fitting default settles it outright. For Verification, Boundaries and Context the default covers only part of the dimension (gate eligibility, the "never" tier, the starting file list); the rest still has to be settled before the dimension reaches 2.

A Ready goal can retain lower non-critical scores. Record their limitations and any genuinely non-blocking assumptions without inventing missing facts. Blocking gaps stay under Open questions regardless of the total and prevent `Ready`. Stop interviewing when all readiness conditions hold; 20/20 is not required.

## 1. Outcome

| 0                                               | 1                                      | 2                                                        |
| ----------------------------------------------- | -------------------------------------- | -------------------------------------------------------- |
| An activity ("improve", "work on", "look into") | An end state is implied but not stated | One observable end state a judge can answer yes or no to |

Formula: `[artefact or system] is in [final state] for [named users or use case]`.

Ask when below 2:

- What must be true when the work is over? Offer the strongest end-state reading of what they said.
- If two or more independent deliverables are present: which one is the goal, and do the others become criteria, a later goal, or out of scope?

No default - use a supplied observable outcome; otherwise settle it in the first round.

## 2. Acceptance criteria

| 0    | 1                                 | 2                                                                             |
| ---- | --------------------------------- | ----------------------------------------------------------------------------- |
| None | Partial, or subjective adjectives | Atomic, independently observable, and collectively sufficient for the outcome |

Cover what applies: required behaviour, required artefacts and their paths, regressions that must not occur, quality thresholds, documentation or operational readiness, and the evidence the agent must report at the end. Five to ten criteria is the healthy range; substantially more means the goal wants splitting.

Ask when below 2:

- Which of these candidate criteria are required, and which are missing? (List your candidates.)
- For each subjective term the user has used: what would you observe to know it holds?

No default.

## 3. Verification

| 0                | 1                            | 2                                                                                                     |
| ---------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------- |
| Self-report only | Incomplete or unclear checks | Rerunnable checks or explicit evidence rubrics for every critical criterion, with evidence to capture |

Separate the **action** (`run the canonical test command`) from the **evidence** (exit code, summary line, changed paths, screenshot, cited section). Judgement checks stay in the criteria table with an explicit rubric; manual verification can be sufficient. Require fresh evidence against the final state before claiming completion. Do not fix one implementation path when several would satisfy the outcome.

### Gate eligibility

Before executing or selecting a gate, inspect its definition, dependencies and target environment. A gate must be relevant to the criteria, deterministic, rerunnable, available in the stated environment, safe within existing authorisation, non-destructive and bounded by a practical timeout. Incidental local test artefacts are acceptable; shared-data resets, production mutations, automatic source fixes and unapproved paid services are not suitable completion gates.

Record the working directory, prerequisites, timeout, pass condition and observed baseline result for each validated gate. A safely observed test failure can be the baseline for a repair goal; availability does not mean the goal already passes. If validation is unavailable or unsafe, retain the proposed verifier and its prerequisite in the criteria table, without claiming it is a confirmed gate. Missing essential verification remains a blocker unless an adequate alternative exists.

Ask when below 2:

- For criteria that have no obvious check: what evidence would convince you? Offer the closest rerunnable proxy.
- Should a confirmed command be a hard gate (blocks completion) or a reported check?

Default: select eligible canonical checks that prove the goal's criteria. Do not promote every discovered command automatically.

## 4. Boundaries

| 0         | 1             | 2                                                        |
| --------- | ------------- | -------------------------------------------------------- |
| Unbounded | Partial scope | In-scope and out-of-scope named, plus protected surfaces |

Positive boundary: repositories, directories, branches, services, environments, accounts, data, tools, permitted side effects. Protected surfaces: interfaces, behaviours and modules that must not regress. Approval policy in three tiers: may do freely / ask first / never.

Carry forward the user's existing authorisation. The example approval tiers below are prompts for unresolved permissions, not reasons to ask again about an action already authorised within the same scope.

Ask when below 2:

- Where may the agent act? Offer a concrete path or system list from what you inspected.
- What must not change? Offer the interfaces you found adjacent to the work.
- Which actions need approval first? Offer the standard tier list (public API change, new production dependency, migration, push, deploy, delete data, credentials).

Default for the "never" tier: disable security checks, weaken tests, expose secrets, rewrite unrelated history.

## 5. Context

| 0               | 1               | 2                                                                         |
| --------------- | --------------- | ------------------------------------------------------------------------- |
| No starting map | Some references | Authoritative, high-signal references and which one wins if they conflict |

The smallest set of files, URLs, issues, schemas, logs and commands that fully specifies expected behaviour, plus known current state, settled decisions, and what is unknown. Paths and identifiers over pasted content.

Ask when below 2:

- Which of these sources is authoritative when they disagree? (List the candidates you found.)
- Which decisions are already settled that the agent should not reopen?

Default: the files you inspected in step 3, listed with a one-line reason each.

## 6. Incremental execution

| 0                    | 1                       | 2                                                                      |
| -------------------- | ----------------------- | ---------------------------------------------------------------------- |
| No progression model | A generic "make a plan" | Milestones each with their own check, with re-planning on new evidence |

Default (software work): inspect the authoritative context and produce a concise plan mapped to the criteria before mutating state; work in the smallest coherent milestone that can be verified; after each, run its checks, tick the milestone and any criteria it proved in the progress artefact and leave the workspace resumable; re-plan when evidence invalidates the approach.

Ask only when the default is wrong - research, operational or non-repository work - and then ask what a milestone is in that domain.

## 7. Persistent state

| 0               | 1              | 2                                                                                         |
| --------------- | -------------- | ----------------------------------------------------------------------------------------- |
| Transcript only | Informal notes | A named state artefact with a schema, read before acting and updated before ending a turn |

Default: a progress section in the goal document itself (or a sibling `PROGRESS.md` when the run will be long) with a checkbox per acceptance criterion (ticked only once its evidence is recorded), the agent's milestone checklist, and a record of evidence, decisions, failed attempts, blockers, next action and last known-good checkpoint. Software work additionally checkpoints with clean commits at verified milestones where repository policy allows.

Ask only when the default is wrong - no repository, or an existing tracker the user prefers.

## 8. Budget and stopping

| 0         | 1             | 2                                                                              |
| --------- | ------------- | ------------------------------------------------------------------------------ |
| Unlimited | Vague caution | Explicit limits and stop rules that distinguish a blocker from unfinished work |

Limits that may apply: turns, elapsed time, retries, spend, destructive operations. Strong stop conditions: missing credential, unavailable required system, product judgement not resolved by the cited sources, irreversible unapproved action, contradictory authoritative requirements, N materially different attempts failed. "Ask whenever uncertain" is not a stop rule - it defeats autonomy; set a materiality threshold instead.

Ask when below 2:

- What is the run budget? Offer a figure appropriate to the harness (Hermes defaults to 20 turns per chunk).
- Which of the standard stop conditions apply, and are there domain-specific ones?

Default for the on-stop report: blocker, evidence, approaches tried, current safe state, and the smallest decision or access needed.

## 9. Recovery

| 0             | 1                   | 2                                      |
| ------------- | ------------------- | -------------------------------------- |
| "Keep trying" | Some retry language | Diagnose, re-plan, roll back, escalate |

Default: never repeat an identical failed action without new evidence or a changed hypothesis; classify a failure as transient, environmental, specification or implementation before acting; reproduce before broad changes; preserve logs and the minimal failing case; roll back changes that move away from known-good; escalate at the stop condition.

Ask only when irreversible operations are in scope - then ask what the rollback point is.

## 10. Final report

| 0           | 1           | 2                                                |
| ----------- | ----------- | ------------------------------------------------ |
| Unspecified | "Summarise" | Evidence, changes, risks and residual work named |

Default: changed paths, verification output per criterion, dependency or configuration changes, remaining warnings, known risks, rollback notes, and anything the user still has to do.

Ask only when the consumer of the report is not the user - a ticket, a PR, a handover - and then ask what that consumer needs.

## Audit line

```
Readiness: <n>/20 - Ready | Needs answers | Split recommended

Material risks:

- <risk, or "None identified">

Open questions:

- <dimension: question, or "None" when Ready>
```

`Split recommended` when the outcome contains independent deliverables or the criteria list will not fit a bounded run. `Needs answers` whenever any readiness condition fails for another reason, even if the total is at least 16/20.
