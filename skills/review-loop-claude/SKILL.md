---
name: review-loop-claude
description: User-invoked entry point - have Claude Code review the current change in a human-in-the-loop fix-and-re-review loop of up to 3 rounds. Invoke as `review-loop-claude [opus|fable] [target]`, e.g. `review-loop-claude opus uncommitted`.
disable-model-invocation: true
---

# Claude review loop

Start a `review-loop-engine` with **Claude Code as the reviewer**.

## Arguments

Read the text after the command name:

- **Model** - the first word, if it is one of these; otherwise Opus:

  | Word    | `--model` |
  | ------- | --------- |
  | `opus`  | `opus`    |
  | `fable` | `fable`   |

  Any other model name (`sonnet`, `haiku`, ...) is refused: say that reviews
  run on Opus or Fable only, and stop.
- **Target** - the rest of the text, such as `uncommitted`, `last 2 commits`,
  `this branch`, or a GSD item. If there is none, scope from the current
  session's work.
- **Rounds** - `rounds=1` or `rounds=2` lowers the limit; the maximum is 3.

## Run

1. Load the `review-loop-engine` skill and the `claude-code` skill. If either is
   missing, say which and stop.
2. This command is not installed in Claude Code. If you are Claude Code anyway,
   say that a Claude-on-Claude review adds little and suggest Codex or pi.
3. Follow `review-loop-engine` with reviewer `claude`, the model and target above. It
   scopes the change, asks you to confirm the scope, runs the rounds and
   reports.
