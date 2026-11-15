# Codex T3 Code path

Use this path when the caller runs inside T3 Code and the conditions in
[SKILL.md](../SKILL.md) hold. T3 Code starts Codex as a native child thread
through its own Codex provider. The user sees the child in T3 Code, can open
its thread, and can stop it there.

## Run the task

T3 Code supplies the `delegate_task` schema and its own rules: call
`orchestrator_capabilities` once per thread, do not poll a running child, and
stop one you no longer need with `task_cancel`. Follow them. This file adds
only what is specific to Codex.

| Field                       | Value                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| `target.providerInstanceId` | `codex` (the official provider), not a model gateway or other Codex instance, unless the user names it |
| `target.model`              | Sol by default, or Astra - use the ID that `orchestrator_capabilities` lists               |
| `target.options`            | `{"reasoningEffort": "medium"}` unless the user sets one - see below                       |
| `isolation`                 | `worktree` for risky or parallel changes; `shared` (the default) otherwise                 |
| `mode`                      | `wait` only when this turn needs the result; `async` otherwise                             |
| `task`                      | The complete brief - see [SKILL.md](../SKILL.md) for what it must contain                  |

With `wait`, a question or approval request from the child ends the wait;
answer it or report it.

Read the result from `summary`. Then inspect the changed files and run the
checks. For `isolation: worktree`, the changes are in the child's worktree,
not your checkout - inspect them there and say where they are.

Always set `reasoningEffort`. The T3 catalogue default for `gpt-6.1-sol` is
`low`, and options inherited from a non-Codex parent do not apply.

Leave `runtimeMode` unset unless the user asks for a supervised child. The
child then inherits the parent's runtime mode. Narrower modes pause for
human approval; they do not make the child read-only.

## What this path does not enforce

The CLI path builds its guarantees from flags. T3 Code launches Codex with
the user's normal configuration, so none of these apply:

- **No sandbox choice.** The child runs with the parent's runtime mode. On
  2026-10-27 a Sol child in `plan` interaction mode under a full-access parent
  created a file. Read-only work therefore uses the CLI path.
- **Not a leaf.** The child keeps `spawn_agent` and its other collaboration
  tools, the user's MCP servers and ChatGPT connectors. T3 Code tells child
  threads not to start subagents, and the task repeats it, but nothing blocks
  it.
- **Guards.** The user's command-guard hook and the user's rules load
  with the user config, as on a CLI write-capable run. This was not
  re-checked under T3 Code.

When a task needs any of these guarantees, use the CLI path.

## Evidence

Checked on 2026-10-27 inside T3 Code, from a Claude Code parent:
`orchestrator_capabilities` listed `codex` with `gpt-6.1-sol` and
`gpt-6-astra`, and `canRunChildTask` and `canRunCrossProviderChildTask`
true. A `gpt-6.1-sol` child at `low` effort completed and returned its
`summary`; it reported `spawn_agent` among its tools and wrote a file in
`plan` interaction mode.
