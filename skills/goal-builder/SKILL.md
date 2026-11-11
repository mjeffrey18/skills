---
name: goal-builder
description: Interview the user in grilling rounds, bounded by a ten-dimension readiness rubric, and write a GOAL.md that a long-running agent and an independent judge would both read as the same completion contract.
disable-model-invocation: true
---

# Goal builder

A goal for a long-horizon agent is a **completion contract**, not a task description: it names one observable end state, and gives the worker and a judge the same evidence to decide whether that state has been reached. This skill turns an under-specified intention into that contract through a short, rubric-bounded interview, and writes it to disk as a Markdown document.

Two references carry the detail - read them before round 1:

- [`references/rubric.md`](references/rubric.md) - the ten dimensions, how to score each 0-2, the probing questions for each, and the default that applies when the user has no preference.
- [`references/goal-template.md`](references/goal-template.md) - the document you write.

This skill prepares the contract; it does not start the goal or implement it. When maintaining the skill, use [`references/evaluation.md`](references/evaluation.md) to check its behaviour.

## 1. Classify

Decide whether the request is goal-shaped: a clear endpoint, more than one action or turn to reach it, and evidence that can be observed when it is reached. A one-shot question or edit, recurring monitoring, or a many-worker dependency graph each want a different mode; if so, name the better fit in one sentence and stop here.

Done: the request is classified as a goal, or redirected.

## 2. Extract and score

Pre-fill the ten dimensions from what the user has already said and from the conversation so far. Score each 0-2 against the rubric. Where a fact is missing, leave the dimension scored low rather than inventing a value to make the draft look complete - an invented test command or scope line is worse than a visible gap, because the judge will trust it.

Done: every dimension has a score and a one-line note of what is known.

## 3. Find the facts

Look up facts the available environment can supply: canonical checks, the working root, authoritative files, existing progress documents and relevant current state. Keep discovery within the authorised scope; ask early if the target or permission boundary is unclear. Dispatch a sub-agent for a long independent exploration when delegation is available.

Inspect command definitions, dependencies and target environments before executing checks. Run only checks that meet the rubric's gate eligibility rules within existing authorisation. Record commands that cannot yet be validated in the criteria table, with the missing prerequisite; treat that gap as blocking if a critical criterion has no other adequate verifier. Do not execute an unknown command just to confirm that it exists.

Done: relevant discoverable facts are checked, and unavailable facts are explicit gaps. Collect any delegated findings before the final audit.

## 4. Grill

Interview in rounds, in the grilling format (from the `grilling` skill, restated here so this skill stands alone):

```
❓ **Q1** - **<question title>**: <question body, with concrete options where they exist>

➡️ <your recommended answer>
```

Apply fitting defaults and check readiness before asking a round. If the contract already meets the rubric's readiness conditions, write it without an interview. Otherwise ask up to three material questions whose prerequisites are settled, each numbered with a recommended answer, then wait. Resolve unclear outcomes or scope first; defer a question only when its answer actually depends on another unresolved decision. Do not reopen supplied answers or interview merely to raise a non-critical score to 2.

Use the supplied file path, or default to `.agents/goals/<YYYY-MM-DD>-<slug>.md` under the working root and report it. Ask about the path only when the choice is material, such as an existing file that could be overwritten. Dimensions with defaults are only asked about when the task makes the default unsuitable; otherwise include the fitting defaults in the document.

Every recommended answer should be one the user could accept verbatim, so a reply of "all recommended" is always a valid way to finish a round.

Done: the readiness conditions are met, a split is needed, or the user has asked to stop. Do not require 20/20.

## 5. Write and audit

Write the document to the selected path using the template. Re-score all ten dimensions and apply the rubric's readiness conditions, including the independent blocker check. Record only genuinely non-blocking assumptions as assumptions; a passing total never resolves a missing decision, permission or verifier. If the user stops the interview, write the current draft with its actual status and unresolved blockers. Keep the status line, audit and open questions consistent.

If the work contains independent outcomes, or cannot plausibly fit a single bounded run, propose a sequence of goals with an explicit hand-off artefact between them instead of forcing one document to carry two projects.

Done: the file exists at the selected path, the audit line is reported to the user, and nothing in the document was invented to fill a gap.

## Pitfalls

- An activity is not an outcome. "Work on the upgrade" becomes "the application runs on Rails 8 and the canonical test suite passes".
- Adjectives are not criteria. Replace "robust", "clean", "production-ready" with a behaviour, a threshold, an example or a rubric.
- A plan is not proof. Every critical criterion pairs with a rerunnable check or an explicit evidence rubric.
- Do not ask a question whose answer would not change the document.
- Do not weaken a criterion, test or gate to make the goal easier to pass; record the tension and let the user decide.
