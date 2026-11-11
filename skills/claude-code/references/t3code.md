# Claude Code T3 Code path

Use this path when the caller runs inside T3 Code and the conditions in
[SKILL.md](../SKILL.md) hold. T3 Code starts Claude Code as a native child
thread through its own Claude provider. The user sees the child in T3 Code,
can open its thread, and can stop it there.

## Run the task

1. Call `orchestrator_capabilities` once per thread, before the first
   `delegate_task`. Confirm that the `claudeAgent` provider instance lists
   the model you need.
2. Call `delegate_task` with:

   | Field                       | Value                                                                      |
   | --------------------------- | -------------------------------------------------------------------------- |
   | `target.providerInstanceId` | `claudeAgent`                                                              |
   | `target.model`              | `claude-opus-5-5` (default) or `claude-fable-5-1`                          |
   | `target.options`            | `{"effort": "medium"}` unless the user sets one                            |
   | `interactionMode`           | `plan` for analysis, planning and review; omit for implementation          |
   | `role`                      | `implementation`, `research`, `review`, `design`, `test` or `general`      |
   | `isolation`                 | `worktree` for risky or parallel changes; `shared` (the default) otherwise |
   | `mode`                      | `wait` only when this turn needs the result; `async` otherwise             |
   | `title`                     | A short name the user will recognise in the thread list                    |
   | `task`                      | The complete brief - see [SKILL.md](../SKILL.md) for what it must contain  |

3. With `async`, end the turn or carry on with other work. T3 Code wakes you
   when the child finishes. Do not poll with `task_status`, `sleep` or a
   watcher. With `wait`, a question or approval request from the child ends
   the wait; answer it or report it.
4. Read the result from `summary`, and check that the returned `model` is the
   one you asked for. Then inspect the changed files and run the checks. For
   `isolation: worktree`, the changes are in the child's worktree, not your
   checkout - inspect them there and say where they are.
5. Stop a child you no longer need with `task_cancel`.

Set `effort` explicitly. Options inherited from a non-Claude parent do not
apply.

Leave `runtimeMode` unset unless the user asks for a supervised child. The
child then inherits the parent's runtime mode. Narrower modes pause for
human approval; they do not make the child read-only. Use `plan` interaction
mode for read-only work: on 2026-10-27 an Opus child in `plan` mode refused
to write a file outside its plan file.

## Subscription

T3 Code runs Claude Code through its `claudeAgent` provider instance. This
path cannot strip `ANTHROPIC_*` variables or pin the helper model per run as
the CLI path does, so it requires both from the provider's configuration.
Before the first `delegate_task` in a thread, run:

```sh
python3 <this skill>/scripts/t3-preflight.py
```

It exits 0 only when all of these hold:

- the `claudeAgent` instance's environment in T3 Code's settings pins
  `ANTHROPIC_DEFAULT_HAIKU_MODEL` and `ANTHROPIC_SMALL_FAST_MODEL` to an Opus
  or Fable model, so background helpers do not run on Haiku, and sets
  nothing else. Any other variable could point the child at a configuration
  the check cannot see;
- neither `~/.claude/settings.json` nor your own environment sets an API key,
  auth token, base URL, `CLAUDE_CONFIG_DIR`, Bedrock/Vertex/Foundry switch or
  `CLAUDE_CODE_SUBAGENT_MODEL`, and the settings define no `apiKeyHelper`;
- `claude auth status --json`, run with the instance's environment, shows
  `loggedIn: true`, `authMethod: claude.ai` and `apiProvider: firstParty`.

If it fails, use the CLI path and pass its `problems` on to the user. The
user fixes the pins in T3 Code's settings for the Claude provider; do not
edit T3 Code's settings, set environment variables, read credential files or
pass tokens yourself. The script prints variable names only, never values,
apart from the two helper-model pins.

The check reads configuration, not the running child: a change to T3 Code's
settings applies to provider sessions started after it. Helper calls are
still not visible in the result (see below).

## What this path does not enforce

- **Not a leaf.** The child keeps the Agent and Workflow tools, T3 Code's
  delegation tools, the user's MCP servers and skills. T3 Code tells child
  threads not to start subagents, and the task repeats it, but nothing blocks
  it.
- **No exact tool list.** Outside `plan` mode the child has every tool the
  provider grants. Guards come from the user's Claude Code settings, which
  the T3 provider loads; this was not re-checked under T3 Code.
- **No `modelUsage`.** The returned `model` names the main model only, so
  background helper calls are not visible.

When a task needs any of these guarantees, use the CLI path.

## Evidence

Checked on 2026-10-27 inside T3 Code, from a Claude Code parent:
`orchestrator_capabilities` listed `claudeAgent` with `claude-opus-5-5` and
`claude-fable-5-1`. A `claude-opus-5-5` child at `low` effort in `plan` mode
completed, refused the file write, and reported `Agent`, `Workflow`,
`delegate_task`, `t3_thread_launch` and `create_threads` among its tools.
