# claude-code

Version 1

Delegate analysis, implementation or review to Claude Code from another agent harness, such as Codex or pi. The skill picks the runtime, writes a bounded task, pins the model to Opus or Fable and checks the result before it is reported.

## When to use

- You work in another harness and want a Claude Code worker or reviewer.
- You need the right `claude -p` flags for models, effort, permissions, structured output or resumed sessions.

## Setup

- Install the Claude Code CLI and sign in with a Claude subscription. The skill refuses API-key billing and other providers on purpose.
- Write-capable workers load your user settings, so your own deny rules and any command-guard hook apply, for example a `PreToolUse` hook that blocks recursive deletes. No such hook is included here. Without one, only Claude Code's own permission rules protect you.
- Optional: [T3 Code](https://github.com/pingdotgg/t3code). When its orchestration tools are present, the skill can run Claude Code as a T3 child task. `scripts/t3-preflight.py` checks that path first. Without T3 Code the skill uses the CLI path.

## Related skills

- [review-loop-engine](../review-loop-engine/README.md) uses this skill when Claude Code is the reviewer.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work, written from the official Claude Code documentation and live CLI runs.
