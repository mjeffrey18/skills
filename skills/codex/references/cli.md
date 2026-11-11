# Codex CLI path

Use this path outside T3 Code, and for the exceptions listed in
[SKILL.md](../SKILL.md). It runs the CLI as a child process from a shell.

Use the installed `codex` command as a bounded worker. This skill needs shell
access and an authenticated Codex installation; it does not require tools from
any particular calling harness.

## Choose and run the task

1. Establish the working directory, requested outcome, permitted changes, and
   acceptance checks. Pass the relevant context explicitly: a child CLI process
   does not automatically receive the calling harness's conversation.
2. Check `codex --version` and the relevant subcommand's `--help` before relying
   on version-sensitive syntax. Use `codex login status` if authentication is
   uncertain. Report missing installation or authentication without reading or
   printing credential files. Run the child with `env -u CODEX_API_KEY` so it
   uses the user's ChatGPT sign-in: a set `CODEX_API_KEY` is used instead and
   bills the API.
3. Prefer `codex exec` for bounded, non-interactive work. Use `codex exec review`
   for a quick built-in review of a Git target, and interactive `codex` when a
   person needs an ongoing terminal conversation. See
   [commands](commands.md) for examples, output handling, resume,
   and fork. When Codex is the reviewer in a scoped or multi-round review
   (`review-loop-engine`), follow [review rounds](review-rounds.md).
4. Run on Sol or Astra only: pass `-m gpt-6.1-sol` (the default) or
   `-m gpt-6-astra` on every call - never inherit the configured model or use
   a lower-tier one. Read [models and modes](models-and-modes.md)
   when choosing between them, or setting effort, service tier, profile, or
   permissions.
5. Supply the prompt through a quoted argument or stdin. Include the task,
   relevant paths, scope, constraints, and required evidence. Quote shell
   variables and use a quoted heredoc delimiter for literal multiline prompts.
6. Capture the process exit status and output. Inspect the result, changed files,
   and appropriate checks before reporting completion. A successful process or
   confident final message alone does not prove that the task succeeded.

## Keep the controls distinct

- **Model** selects the worker; **reasoning effort** selects a supported effort
  level for that model. Neither grants permission to act.
- **Execution mode** selects interactive, exec, or review behaviour.
  **Sandbox settings** constrain command access. **Approval policy** controls
  when approval is requested. Set these according to the authorised task.
- Pass `--sandbox` on every call. Your own config may set a
  permissive default, so an omitted sandbox can give the worker more access
  than the task needs.
- Interactive `/plan` is not an `exec` flag. For non-interactive planning, request
  analysis without edits and select a read-only sandbox.
- Pass the caller's scope and restrictions to Codex. Delegation does not extend
  authority to deploy, publish, delete, or use connected services. A filesystem
  sandbox does not itself make every MCP or connected-service action read-only.
- If a run is blocked, report the blocker. Do not silently change the requested
  model, bypass permissions, ignore rules, or repeat a potentially mutating task.
  If Sol or Astra is unavailable, stop and report it - do not fall back.
- Write-capable runs keep the user config, so the user's command-guard
  hook and the user's rules apply to every command. Do not add
  `--ignore-user-config` to them; that is for reviews, which cannot write.

## Keep the worker a leaf

Codex loads far more than a delegated task needs. A workspace-write run with
default flags exposed every ChatGPT connector (including ones that can
merge, write or deploy), plus sub-agents, browser, computer use, image
generation and goals. Every run therefore adds:

```sh
--disable apps --disable plugins --disable multi_agent -c 'agents.enabled=false' \
--disable browser_use --disable browser_use_external --disable in_app_browser \
--disable computer_use --disable image_generation --disable goals \
-c 'web_search="disabled"' -c 'skills.include_instructions=false'
```

- `multi_agent` and `agents.enabled=false` together remove sub-agent tools;
  `multi_agent` alone leaves `spawn_agent` in place.
- `skills.include_instructions=false` drops the skills catalogue, so the
  worker is not offered this or a review skill. There is no switch that
  removes every skill.
- The user's own MCP servers still load. Disable each one the task does not
  need with `-c 'mcp_servers.<name>.enabled=false'` - list them with
  `codex mcp list --json`. `node_repl` runs code in its own process, outside
  the command sandbox and the guard hook, so disable it for any run that must
  not write.
- The prompt still says not to invoke Claude Code, Codex, pi or any other
  agent: with network access a shell command could call one. For reviews,
  [review rounds](review-rounds.md) removes the user config and
  every MCP server as well.

## Compatibility

Examples, review rounds, resume and the Sol and Astra models were exercised
with live runs on **2026-09-28**. Review rounds were rechecked at medium
effort on **2026-10-22**. On the same day a workspace-write run with the leaf
flags above showed no connector, sub-agent, browser, image or goal tools; the
guard hook blocked a recursive force delete and an ordinary write succeeded.
Rechecked on **2026-10-27**: three review rounds resumed on Astra, and every
disabled feature name still exists. A read-only run with the review flags
listed no sub-agent, web, browser or connector tools. Code mode's `exec`
could not import `fs`, and a shell write to `/tmp` was refused.
Local help establishes accepted flags; current official docs
explain behaviour. If they differ, investigate the installed version rather
than combining incompatible examples. Model catalogues describe capabilities,
not guaranteed account access.

Sources: [developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli),
[non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode), and
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).
