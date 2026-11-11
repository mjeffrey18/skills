# Claude Code CLI path

Use this path outside T3 Code, and for the exceptions listed in
[SKILL.md](../SKILL.md). It runs the CLI as a child process from a shell.

Use the installed `claude` binary as a bounded worker. This skill needs shell
access and the user's signed-in Claude Code; it does not require tools from
any particular calling harness.

## Choose and run the task

1. Establish the working directory, requested outcome, permitted changes and
   acceptance checks. Pass the relevant context explicitly: a child CLI process
   does not receive the calling harness's conversation.
2. Check `claude --version` and `claude --help` before relying on
   version-sensitive syntax, and check sign-in (below).
3. Prefer `claude -p` for bounded, non-interactive work. See
   [commands](commands.md) for examples, output handling, resume
   and fork. When Claude Code is the reviewer in a scoped or multi-round
   review (`review-loop-engine`), follow
   [review rounds](review-rounds.md).
4. Supply the prompt on stdin or as a quoted argument. Include the task,
   relevant paths, scope, constraints and required evidence.
5. Capture the exit status and the JSON result. Inspect the result, changed
   files and appropriate checks before reporting completion. A successful
   result alone does not prove the task succeeded.

## Stay within the subscription terms

The user's subscription covers ordinary, individual use of the official
Claude Code binary, including headless `-p` runs they start themselves. Keep
every run inside that:

- Run the unmodified `claude` binary and let it authenticate itself. Do not
  read, print, copy, or pass on OAuth tokens, Keychain entries, or
  `~/.claude*` credential files.
- Strip anything that would bill or route elsewhere: `ANTHROPIC_API_KEY`,
  `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL` and the
  `CLAUDE_CODE_USE_BEDROCK/VERTEX/FOUNDRY` switches.
- Before running, `claude auth status --json` - under the same environment
  and `--setting-sources` value as the run - must exit 0 and show
  `loggedIn: true`, `authMethod: claude.ai` and `apiProvider: firstParty`.
  Anything else -
  including empty output - means stop and ask the user to log in with
  `claude`; do not attempt the login yourself. First rule out your own
  sandbox: inside Codex's read-only sandbox (`CODEX_SANDBOX` set, network
  off), `claude` cannot read its sign-in and reports `loggedIn: false` even
  when the user is signed in - run the command outside the sandbox instead.
- Do not use `--bare`: it refuses OAuth and only accepts an API key.
- Run only when the user asks in the current session. Do not schedule runs, wire
  them into hooks, run them for other people, or leave a loop unattended.

Sources: [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance),
[authentication](https://code.claude.com/docs/en/authentication) and
[headless mode](https://code.claude.com/docs/en/headless).

## Model

Delegated work runs on Opus or Fable only - never Sonnet, Haiku, or the
user's configured default. Pass `--model opus` (default) or `--model fable`,
and:

- strip `ANTHROPIC_MODEL` and the `ANTHROPIC_DEFAULT_*_MODEL` /
  `CLAUDE_CODE_SUBAGENT_MODEL` overrides so the alias cannot be remapped;
- set `ANTHROPIC_DEFAULT_HAIKU_MODEL` and `ANTHROPIC_SMALL_FAST_MODEL` to
  `claude-opus-5-5` - Claude Code otherwise runs background tasks on Haiku;
- after the run, every `modelUsage` key must start `claude-opus-` or
  `claude-fable-`.

`--effort` sets the effort level. Inherit it unless the user sets one; reviews
run at `medium`. If the chosen model is unavailable, stop and report it - do
not fall back.

## Keep the controls distinct

- **Model** selects the worker; **effort** selects how hard it thinks.
  Neither grants permission to act.
- **Tools** decide what Claude can do. `--tools "Read,Grep,Glob"` is
  read-only: use it for analysis, planning and review. Add `Edit,Write,Bash`
  only for authorised implementation.
- **Settings** decide which guards apply. Read-only runs load none
  (`--setting-sources ""`). Write-capable runs load the user's settings
  (`--setting-sources user`) so the deny rules and the user's
  command-guard hook apply to every command. Those settings define no
  `apiKeyHelper` (checked 2026-10-22); if one appears, stop and ask.
- **Permission mode** decides what runs without approval. Nobody can answer a
  prompt in `-p`, so anything that would ask is denied. Use `dontAsk` for
  read-only runs and `acceptEdits` plus `--allowedTools` for the commands an
  implementation needs. `bypassPermissions` and
  `--dangerously-skip-permissions` are not a workaround for a blocked task.
- Pass the caller's scope and restrictions to Claude. Delegation does not
  extend authority to deploy, publish, delete or use connected services.
- If a run is blocked, report the blocker. Do not widen tools or permissions,
  drop the guard, change the model or repeat a potentially mutating task.

## Keep the worker a leaf

Every run sets `--strict-mcp-config` (no MCP servers) and leaves out the
Agent tool. Runs that are not limited to read tools also set
`--disable-slash-commands`, so Claude cannot load this or a review skill and
recurse. With `Bash`, Claude could
still run `claude`, `codex` or `pi` itself, so the prompt says not to invoke
Claude Code, Codex, pi or any other agent.

## Compatibility

Live review runs on **2026-09-28**: Read/Grep/Glob only, no Bash or Write tool
present; auth still `claude.ai` with settings ignored; `--json-schema` result
in `structured_output`; pinning the helper model removed Haiku from
`modelUsage`; `--resume` keeps finding IDs. Rechecked on **2026-10-22**:
review rounds at `--effort medium` with a second `--add-dir`, and a
write-capable run with `--setting-sources user` (see
[commands](commands.md)).
