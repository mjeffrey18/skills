---
name: review-loop-pi
description: User-invoked entry point - have pi review the current change on the user's local models in a human-in-the-loop fix-and-re-review loop of up to 3 rounds. Invoke as `review-loop-pi [orchestrator|brain|think|code] [target]`, e.g. `review-loop-pi brain last 2 commits`.
disable-model-invocation: true
---

# pi review loop

Start a `review-loop-engine` with **pi as the reviewer**.

## Arguments

Read the text after the command name:

- **Model** - the first word, if it is one of these; otherwise `orchestrator`:

  | Word           | Model and thinking                  | Use                          |
  | -------------- | ----------------------------------- | ---------------------------- |
  | `orchestrator` | GLM-5.3-Flash, high                 | Difficult work, slower       |
  | `brain`        | GLM-5.3-Flash, max                  | Hard work, slowest           |
  | `think`        | Qwen3.8-27B, xhigh                  | Difficult work, slower       |
  | `code`         | Qwen3.8-27B, medium                 | Moderate work, fastest       |

  Any other model name is refused: say that pi reviews run on these four only,
  and stop.
- **Target** - the rest of the text, such as `uncommitted`, `last 2 commits`,
  `this branch`, or a GSD item. If there is none, scope from the current
  session's work.
- **Rounds** - `rounds=1` or `rounds=2` lowers the limit; the maximum is 3.

## Run

1. Load the `review-loop-engine` skill and the `pi` skill. If either is
   missing, say which and stop.
2. If you are pi yourself, a pi review is still useful when the reviewer is a
   different model from the one you are running on - a GLM route reviewing
   Qwen's work, or the reverse. If it would be the same model, say that the
   review loses its independence and suggest another of the four.
3. Follow `review-loop-engine` with reviewer `pi`, the model and target above.
   It scopes the change, asks you to confirm the scope, runs the rounds and
   reports. Warn that `brain` and `think` rounds can take a long time, and
   that pi is slow on a change past the scoping size limit: offer smaller
   loops, or Claude or Codex for the large one (timings are in the `pi`
   skill's `references/cli.md`).
