# pi T3 Code path

Use this path when the caller runs inside T3 Code and the conditions in
[SKILL.md](../SKILL.md) hold. T3 Code starts pi as a native child thread
through its own pi provider. The user sees the child in T3 Code, can open its
thread, and can stop it there.

## Run the task

1. Call `orchestrator_capabilities` once per thread, before the first
   `delegate_task`. Confirm that the `pi` provider instance lists the route
   you need.
2. Call `delegate_task` with:

   | Field                       | Value                                                                     |
   | --------------------------- | ------------------------------------------------------------------------- |
   | `target.providerInstanceId` | `pi`                                                                      |
   | `target.model`              | `gateway/<word>` - see [routes](cli.md#routes)                            |
   | `target.options`            | `{"thinking": "<level>"}` - the level the routes table gives that route   |
   | `role`                      | `implementation`, `research`, `design`, `test` or `general`               |
   | `isolation`                 | `worktree` for every write-capable child - see Partial guard below        |
   | `mode`                      | `async` - local models are slow                                           |
   | `title`                     | A short name the user will recognise in the thread list                   |
   | `task`                      | The complete brief - see [SKILL.md](../SKILL.md) for what it must contain |

3. End the turn or carry on with other work. T3 Code wakes you when the
   child finishes. Do not poll with `task_status`, `sleep` or a watcher. A
   run on `brain` or `think` can take up to an hour.
4. Read the result from `summary`, and check that the returned `model` is the
   route you asked for. Then inspect the changed files in the child's
   worktree and run the checks. Say where the changes are.
5. Stop a child you no longer need with `task_cancel`.

The T3 catalogue offers one thinking level per route, matching the routes
table. Set it explicitly: options inherited from a non-pi parent do not
apply. Ignore `default` and the other catalogue routes unless the user names
one.

Leave `runtimeMode` unset unless the user asks for a supervised child. The
child then inherits the parent's runtime mode. T3 Code's pi extension lets
`read`, `grep`, `find` and `ls` through in every mode. Under `full-access` it
lets everything through. Under `auto-accept-edits` it also lets `edit` and
`write` through and asks the user in T3 Code before anything else, such as
`bash`. Under `auto` or `approval-required` it asks before every other tool.
These modes add a human approval step; they do not make the child read-only.

## What T3 Code launches

T3 Code runs `pi --mode rpc --session <path>`, then the provider's launch
arguments, then `--extension <T3's MCP extension>`. Unless your pi provider
adds launch arguments, the child loads your normal pi set-up:

- the `packages` in `~/.pi/agent/settings.json`, such as `pi-defender`;
- the extensions in `~/.pi/agent/extensions/`;
- your skills (this one included), prompt templates and MCP servers;
- project `AGENTS.md` and `CLAUDE.md` files;
- T3 Code's own extension, which adds `delegate_task` and the other T3 tools
  and appends T3's orchestration instructions to the system prompt.

T3 Code adds `--no-extensions` and `--no-tools` only for its own short
text-generation calls, not for agent threads.

## What this path does not enforce

- **No read-only mode.** The pi driver has no `plan` interaction-mode support,
  and the runtime modes only add approval. Read-only work uses the CLI path.
- **Not a leaf.** The child has `delegate_task` and whatever sub-agent,
  web and MCP tools your set-up loads. T3 Code tells child threads not to
  start subagents, and the task repeats it, but nothing blocks it.
- **Partial guard.** pi-defender blocks dangerous `bash` commands and
  protected paths. It matches command text and does not cover other shell
  or file tools; add your own extension if you use them.
  Recursive deletes through common scripting APIs are now caught, but
  a delete hidden in a script file still passes. Run every write-capable pi
  child in its own worktree, and inspect what it changed there before using
  it.

When a task needs any of these guarantees, use the CLI path.

## Evidence

Checked on 2026-10-27 against T3 Code's pi driver and pi-defender's source,
with live write-capable children in their own worktrees: writes succeeded,
and pi-defender blocked a recursive force delete through `bash`. Deletes
through tools pi-defender does not cover ran unblocked.
