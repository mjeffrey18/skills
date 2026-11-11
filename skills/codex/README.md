# codex

Version 1

Delegate analysis, implementation or review to the Codex CLI from another agent harness. The skill covers model and reasoning choice, sandbox and approval modes, structured output and resumed sessions.

## When to use

- You work in Claude Code, pi or another harness and want a Codex worker or reviewer.
- You need the right `codex exec` flags and want the result checked rather than trusted.

## Setup

- Install the Codex CLI and sign in with ChatGPT.
- Write-capable workers keep your user config, so your own rules and any command-guard hook apply. No such hook is included here. Without one, only the Codex sandbox and approval policy protect you.
- Optional: [T3 Code](https://github.com/pingdotgg/t3code). When its orchestration tools are present, the skill can run Codex as a T3 child task. Without T3 Code the skill uses the CLI path.

## Related skills

- [review-loop-engine](../review-loop-engine/README.md) uses this skill when Codex is the reviewer.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work, written from the official Codex documentation and CLI help.
