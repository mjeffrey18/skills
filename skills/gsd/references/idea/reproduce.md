---
name: reproduce
description: For a bug item, a failing reproduction of the reported symptom and 3-5 ranked hypotheses
mode: new
---

# Reproduce the bug

Run only for a bug item. You turn the user's report into a command that fails
the same way, so planning starts from an observed failure rather than a
guess. The method is workflow.md, Start or clarify (the bug item paragraph).

Inputs from the orchestrator: the symptom in the user's words, any logs or
steps they gave, the repository root and the outcome from light grilling.

Do:

- Find or write the smallest command that shows the user's exact symptom - a
  test, a script or a CLI call. Run it and capture the failing output.
- Use the repo's fixtures or seeds, or data you create and remove yourself;
  never real or production data.
- List 3-5 hypotheses for the cause, ranked by likelihood, each with the
  check that would disprove it. Do not start testing or fixing them.
- If the symptom will not reproduce, say what you tried and what is missing
  (data, environment, access). Do not invent a failure.

Return the reproduction command, its observed output (trimmed to the
relevant lines), the environment it ran in and the ranked hypotheses. If you
wrote a scratch file to reproduce, return its content and path so the
orchestrator can keep or discard it.

Limits: do not fix the bug or change tracked files. Remove any temporary
data you created. The orchestrator records the result in FACTS.md; it is the
only writer of GSD records and makes every commit.
