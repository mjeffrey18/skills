# pi CLI path

Use this path outside T3 Code, and for the exceptions listed in
[SKILL.md](../SKILL.md). It runs the CLI as a child process from a shell.

Use the installed `pi` binary as a bounded worker on the user's local models.
This skill needs shell access and network access to the user's model
gateway; it does not require tools from any particular calling harness.

## Choose and run the task

1. Establish the working directory, requested outcome, permitted changes and
   acceptance checks. Pass the relevant context explicitly: a child CLI process
   does not receive the calling harness's conversation.
2. Check `pi --version` and `pi --help` before relying on version-sensitive
   syntax.
3. Pick the route (below) and the tool set (see Keep the controls distinct).
   See [commands](commands.md) for examples, output handling and
   resume. When pi is the reviewer in a scoped or multi-round review
   (`review-loop-engine`), follow [review rounds](review-rounds.md).
4. Supply the prompt as an argument after `--`, with stdin closed. Include the
   task, relevant paths, scope, constraints and required evidence.
5. Capture the exit status and output. Inspect the result, changed files and
   appropriate checks before reporting completion. A confident final message
   does not prove the task succeeded.

## Routes

pi runs on the user's named model gateway routes, `gateway/<word>` in
`~/.pi/agent/models.json`. Pass `--model gateway/<word>` and `--thinking` on
every call rather than inheriting the configured default.

| Word           | Route                      | Thinking | Use                                                  |
| -------------- | -------------------------- | -------- | ---------------------------------------------------- |
| `orchestrator` | GLM-5.3-Flash              | high     | Difficult work, slower - default for analysis        |
| `brain`        | GLM-5.3-Flash              | max      | Hard work, slowest                                   |
| `think`        | Qwen3.8-27B (reasoning)    | xhigh    | Difficult work, slower                               |
| `agent`        | Qwen3.8-27B (coding/agent) | medium   | Moderate work, fastest, 6 concurrency (200k context) |
| `code`         | Qwen3.8-27B (coding)       | medium   | Moderate work, fastest, 4 concurrency (256k context) |

There is no subscription question: these models are the user's explicit
choice for pi and sit outside the Opus/Fable and Sol/Astra rule for Claude
and Codex. Other providers in `models.json` are for the user's own sessions;
use one only when the user names it. If a route is unavailable, stop and
report it - do not fall back to another. Reviews use only `orchestrator`,
`brain`, `think` or `code` (see [review rounds](review-rounds.md)).

## Keep the controls distinct

- **Route** selects the model; **thinking** selects its effort. Neither grants
  permission to act.
- **Tools** decide what pi can do. `--tools read,grep,find,ls` is read-only:
  use it for analysis, planning and review. Add `bash,edit,write` only for
  authorised implementation.
- **pi has no OS sandbox.** `bash` runs as the user, with the user's network,
  credentials and file access. The only guard is pi-defender, a pattern
  blocker for dangerous commands and protected paths - not a sandbox. Every
  write-capable run loads it explicitly with `-e` (see
  [commands](commands.md)). Use a separate worktree when the change
  is risky.
- Pass the caller's scope and restrictions to pi. Delegation does not extend
  authority to deploy, publish, delete or use connected services.
- If a run is blocked, report the blocker. Do not widen tools, drop
  pi-defender, change the route or repeat a potentially mutating task.

## Keep the worker a leaf

Every run sets `--no-extensions --no-skills --no-prompt-templates --no-themes
--no-mcp --no-approve`:

- `--no-extensions` removes the sub-agent, web-access and other extension
  tools; explicit `-e` paths still load, which is how pi-defender comes back;
- `--no-skills` and `--no-prompt-templates` stop pi loading this or any other
  agent skill and recursing;
- `--no-mcp` removes MCP servers, which `--tools` would otherwise keep;
- `--no-approve` ignores project-local pi files, which could add tools.

With `bash`, pi could still run `claude`, `codex` or `pi` itself, so the
prompt says not to invoke Claude Code, Codex, pi or any other agent.

## Sandboxed callers

pi needs the network to reach the gateway. Inside Codex's sandbox with the
network off (`CODEX_SANDBOX_NETWORK_DISABLED=1`), run pi outside the sandbox -
approve the escalation Codex asks for - or use workspace-write with network
access.

## Timing

Local models are much slower than hosted ones. A small review on `code` took
about 40 seconds; a large one on `orchestrator` took 18 minutes. Allow up to
60 minutes on `brain` or `think`, and wait on the same process: a timeout in
the caller does not prove the child stopped.

## Compatibility

Checked on **2026-10-22**: the flags above are accepted together in print
mode, `--no-mcp` and `--tools` behave as the CLI docs and changelog describe,
JSON mode still ends with `agent_end`, and pi-defender loads with `-e` under
`--no-extensions`.
