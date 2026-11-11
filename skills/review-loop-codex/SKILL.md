---
name: review-loop-codex
description: User-invoked entry point - have Codex review the current change in a human-in-the-loop fix-and-re-review loop of up to 3 rounds. Invoke as `review-loop-codex [sol|astra] [target]`, e.g. `review-loop-codex astra last 2 commits`.
disable-model-invocation: true
---

# Codex review loop

Start a `review-loop-engine` with **Codex as the reviewer**.

## Arguments

Read the text after the command name:

- **Model** - the first word, if it is one of these; otherwise Sol:

  | Word    | Model          |
  | ------- | -------------- |
  | `sol`   | `gpt-6.1-sol`  |
  | `astra` | `gpt-6-astra`  |

  Any other model name (`luna`, `terra`, `gpt-5.5`, ...) is refused: say that
  reviews run on Sol or Astra only, and stop.
- **Target** - the rest of the text, such as `uncommitted`, `last 2 commits`,
  `this branch`, or a GSD item. If there is none, scope from the current
  session's work.
- **Rounds** - `rounds=1` or `rounds=2` lowers the limit; the maximum is 3.

## Run

1. Load the `review-loop-engine` skill and the `codex` skill. If either is missing,
   say which and stop.
2. This command is not installed in Codex. If you are Codex anyway, say that a
   Codex-on-Codex review adds little and suggest Claude Code or pi.
3. Follow `review-loop-engine` with reviewer `codex`, the model and target above. It
   scopes the change, asks you to confirm the scope, runs the rounds and
   reports.
