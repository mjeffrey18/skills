# Codex T3 Code path

Use this path when the caller runs inside T3 Code and the conditions in
[SKILL.md](../SKILL.md) hold. T3 Code starts Codex as a native child thread
through its own Codex provider. The user sees the child in T3 Code, can open
its thread, and can stop it there.

## Run the task

1. Call `orchestrator_capabilities` once per thread, before the first
   `delegate_task`. Confirm that the `codex` provider instance lists the model
   you need. Use `codex` (the official provider), not a model gateway or other Codex
   instance, unless the user names it.
2. Call `delegate_task` with:

   | Field                | Value                                                                                     |
   | -------------------- | ----------------------------------------------------------------------------------------- |
   | `target.providerInstanceId` | `codex`                                                                            |
   | `target.model`       | `gpt-6.1-sol` (default) or `gpt-6-astra`                                                  |
   | `target.options`     | `{"reasoningEffort": "medium"}` unless the user sets one - see below                       |
   | `role`               | `implementation`, `research`, `design`, `test` or `general`                               |
   | `isolation`          | `worktree` for risky or parallel changes; `shared` (the default) otherwise                |
   | `mode`               | `wait` only when this turn needs the result; `async` otherwise                            |
   | `title`              | A short name the user will recognise in the thread list                                   |
   | `task`               | The complete brief - see [SKILL.md](../SKILL.md) for what it must contain                 |

3. With `async`, end the turn or carry on with other work. T3 Code wakes you
   when the child finishes. Do not poll with `task_status`, `sleep` or a
   watcher. With `wait`, a question or approval request from the child ends
   the wait; answer it or report it.
4. Read the result from `summary`. Then inspect the changed files and run the
   checks. For `isolation: worktree`, the changes are in the child's worktree,
   not your checkout - inspect them there and say where they are.
5. Stop a child you no longer need with `task_cancel`.

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
