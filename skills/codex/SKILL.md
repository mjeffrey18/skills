---
name: codex
description: Delegate analysis, implementation, or review to Codex from another agent harness. Use when a task calls for a Codex worker, Codex CLI commands, model and reasoning selection, execution and permission modes, structured output, or session continuation. Does not cover OpenAI API integration or building a new CLI.
user-invocable: false
---

# Codex

Use Codex as a bounded worker. There are two ways to run it. Pick one before
you build the task.

## Choose the runtime

Use the **T3 Code path** - [t3code.md](references/t3code.md) - when both
hold:

- the T3 Code `delegate_task` and `orchestrator_capabilities` tools are in
  your tool list (they may be deferred - search for `delegate_task` once);
- `orchestrator_capabilities` lists the `codex` provider with
  `canRunChildTask: true`.

Otherwise use the **CLI path** - [cli.md](references/cli.md).

Use the CLI path even inside T3 Code when:

- Codex is the reviewer in a `review-loop-engine` round. `review-round.py`
  enforces the reviewer's isolation and validates its verdict; a T3 child has
  neither (see [review rounds](references/review-rounds.md));
- the work must be read-only. T3 Code cannot make a Codex child read-only: on
  2026-10-27 a child in `plan` interaction mode wrote a file;
- the task needs a CLI-only feature: `--output-schema`, `codex exec review`,
  or resuming or forking a CLI session;
- the user asks for the CLI.

## Rules for both paths

- Run on Sol or Astra only: `gpt-6.1-sol` (the default) or `gpt-6-astra`.
  Never inherit the configured model or use a lower tier. If neither is
  available, stop and report it - do not fall back.
- The child does not see your conversation. Pass the working directory,
  outcome, permitted changes, acceptance checks and relevant paths in the
  task.
- Pass on the caller's scope and restrictions. Delegation does not extend
  authority to deploy, publish, delete, or use connected services.
- Every task says: do not commit, push or deploy unless authorised, and do not
  invoke Claude Code, Codex, pi or any other agent, or start subagents.
- If a run is blocked, report the blocker. Do not widen permissions, change
  the model, or repeat a potentially mutating task.
- A confident final message does not prove success. Inspect the result,
  changed files and checks before you report completion.
