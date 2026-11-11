---
name: claude-code
description: Delegate analysis, implementation, or review to Claude Code on the user's own Claude subscription, pinned to Opus or Fable. Use when a task calls for a Claude Code worker, Claude Code CLI commands, model and effort selection, tool and permission modes, structured output, or session continuation. Does not cover the Anthropic API, the Agent SDK, or building products on Claude.
user-invocable: false
---

# Claude Code

Use Claude Code as a bounded worker. There are two ways to run it. Pick one
before you build the task.

## Choose the runtime

Use the **T3 Code path** - [t3code.md](references/t3code.md) - when all
three hold:

- the T3 Code `delegate_task` and `orchestrator_capabilities` tools are in
  your tool list (they may be deferred - search for `delegate_task` once);
- `orchestrator_capabilities` lists the `claudeAgent` provider with
  `canRunChildTask: true`;
- `python3 <this skill>/scripts/t3-preflight.py` exits 0 - see
  [t3code.md](references/t3code.md#subscription).

Otherwise use the **CLI path** - [cli.md](references/cli.md).

Use the CLI path even inside T3 Code when:

- Claude Code is the reviewer in a `review-loop-engine` round.
  `review-round.py` enforces the reviewer's isolation and validates its
  verdict; a T3 child has neither (see
  [review rounds](references/review-rounds.md));
- the task needs a CLI-only feature: `--json-schema` structured output, an
  exact tool list, `modelUsage` evidence, or resuming or forking a CLI
  session;
- the user asks for the CLI.

## Rules for both paths

- Run on Opus or Fable only - never Sonnet, Haiku, or the user's configured
  default. If the chosen model is unavailable, stop and report it - do not
  fall back.
- Stay within the user's subscription: run only when the user asks in the
  current session, never on a schedule or for other people, and never read,
  copy or pass on credentials.
- The child does not see your conversation. Pass the working directory,
  outcome, permitted changes, acceptance checks and relevant paths in the
  task.
- Pass on the caller's scope and restrictions. Delegation does not extend
  authority to deploy, publish, delete, or use connected services.
- Every task says: do not commit, push or deploy unless authorised, and do not
  invoke Claude Code, Codex, pi or any other agent, or start subagents.
- If a run is blocked, report the blocker. Do not widen tools or permissions,
  drop a guard, change the model, or repeat a potentially mutating task.
- A confident final message does not prove success. Inspect the result,
  changed files and checks before you report completion.
