---
name: pi
description: Delegate analysis, implementation, or review to the pi coding agent on the user's own model gateway routes (orchestrator, brain, think, agent, code). Use when a task calls for a pi worker, pi CLI commands, route and thinking selection, tool and permission controls, JSON output, or session continuation. Does not cover configuring pi, its extensions, MCP servers or its interactive TUI.
user-invocable: false
---

# pi

Use pi as a bounded worker on the user's local models. There are two ways to
run it. Pick one before you build the task.

## Choose the runtime

Use the **T3 Code path** - [t3code.md](references/t3code.md) - when both
hold:

- the T3 Code `delegate_task` and `orchestrator_capabilities` tools are in
  your tool list (they may be deferred - search for `delegate_task` once);
- `orchestrator_capabilities` lists the `pi` provider with
  `canRunChildTask: true`.

Otherwise use the **CLI path** - [cli.md](references/cli.md).

Use the CLI path even inside T3 Code when:

- pi is the reviewer in a `review-loop-engine` round. `review-round.py`
  enforces the reviewer's isolation and validates its verdict; a T3 child has
  neither (see [review rounds](references/review-rounds.md));
- the work must be read-only. T3 Code has no read-only mode for pi children;
  only `--tools read,grep,find,ls` on the CLI path enforces it;
- the task needs a CLI-only feature: an exact tool list, JSON event output,
  or resuming a CLI session;
- the user asks for the CLI.

## Rules for both paths

- Run on a named route - `orchestrator`, `brain`, `think`, `agent` or `code`
  (the table is in [cli.md](references/cli.md#routes)). Use another provider
  only when the user names it. If a route is unavailable, stop and report it
  - do not fall back.
- pi has no OS sandbox. Its shell runs as the user, with the user's network,
  credentials and files.
- The child does not see your conversation. Pass the working directory,
  outcome, permitted changes, acceptance checks and relevant paths in the
  task.
- Pass on the caller's scope and restrictions. Delegation does not extend
  authority to deploy, publish, delete, or use connected services.
- Every task says: do not commit, push or deploy unless authorised, and do not
  invoke Claude Code, Codex, pi or any other agent, or start subagents.
- If a run is blocked, report the blocker. Do not widen tools, drop
  pi-defender, change the route, or repeat a potentially mutating task.
- A confident final message does not prove success. Inspect the result,
  changed files and checks before you report completion.
