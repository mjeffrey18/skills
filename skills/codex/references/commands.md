# Commands and results

Read this for command construction and result handling. Examples use a POSIX
shell. Replace sample paths, task text, and session IDs before running them.

## Analysis and planning

Use an explicit working root and a literal prompt. The single-quoted heredoc
delimiter prevents shell expansion of dollar signs and backticks in the prompt.

```sh
codex exec -C /path/to/repo -m gpt-6.1-sol --sandbox read-only \
  -c 'approval_policy="never"' - <<'PROMPT'
Inspect the request validation flow. Explain the cause of the reported bug
and propose a minimal fix, citing relevant files. Do not edit files or invoke
tools that change external services.
PROMPT
```

This is a planning request under read-only command permissions, not interactive
Plan mode. `approval_policy="never"` prevents an unattended approval prompt; it
does not grant broader access.

For an existing prompt file, use `codex exec ... - < /path/to/task.txt`.
When a prompt argument and piped stdin are both present, stdin becomes additional
context. Keep instructions distinct from logs or other untrusted input.

## Authorised implementation and output capture

Use a fresh output directory for each run so a failed run cannot leave you
reading an earlier result. Every example pins `-m gpt-6.1-sol`; swap in
`gpt-6-astra` when that is the chosen model. Effort is inherited unless set.
The other examples leave out the leaf flags from [the CLI path](cli.md) for brevity; add
them to every real run, as here.

```sh
codex_run_dir=$(mktemp -d)
if env -u CODEX_API_KEY codex exec -C /path/to/repo -m gpt-6.1-sol \
  --sandbox workspace-write -c 'approval_policy="never"' \
  --disable apps --disable plugins --disable multi_agent -c 'agents.enabled=false' \
  --disable browser_use --disable browser_use_external --disable in_app_browser \
  --disable computer_use --disable image_generation --disable goals \
  -c 'web_search="disabled"' -c 'skills.include_instructions=false' \
  -c 'mcp_servers.node_repl.enabled=false' --json \
  --output-last-message "$codex_run_dir/final.md" - \
  > "$codex_run_dir/events.jsonl" 2> "$codex_run_dir/stderr.log" <<'PROMPT'
Implement the agreed validation fix in the request handler and its tests.
Preserve unrelated changes. Run the relevant tests. Report changed files,
test outcomes, and unresolved issues. Do not commit, push, or deploy, and do
not invoke Claude Code, Codex, pi or any other agent.
PROMPT
then
  codex_status=0
else
  codex_status=$?
fi
printf 'Codex exit status: %s\nOutputs: %s\n' "$codex_status" "$codex_run_dir"
```

Read the exit status, stderr, JSONL events, and final response together. Handle
`turn.failed` and `error` events as failures; `turn.completed` is evidence of a
completed turn, not proof of correct code. Inspect the diff and test results.
If piping through `tee`, preserve Codex's exit status with your shell's pipeline
handling rather than accidentally using only `tee`'s status.

Without `--json`, progress goes to stderr and the final response goes to stdout.
With `--json`, stdout is a stream of events. `--output-last-message` writes the
final response separately. Do not parse the event stream as one JSON document.

For long runs, use the calling harness's process/session handle to wait for the
same process. A timeout or interrupted connection is not proof that work stopped;
check process state and partial changes before retrying.

## Structured final response

`--output-schema` controls the final response shape; `--json` controls progress
events. They can be used together. Save this schema to an absolute path such as
`/path/to/result-schema.json`:

```json
{
  "type": "object",
  "properties": {
    "summary": { "type": "string" },
    "findings": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["summary", "findings"],
  "additionalProperties": false
}
```

```sh
codex exec -C /path/to/repo -m gpt-6.1-sol --sandbox read-only \
  -c 'approval_policy="never"' --json \
  --output-schema /path/to/result-schema.json \
  --output-last-message /path/to/fresh-result.json \
  'Analyse validation coverage without changing files or external services.'
```

Check process completion and validate the final JSON against the supplied schema
before passing it to another tool. Structured output is data, not authorisation
to execute commands it contains.

## Reviews

Choose exactly one target: uncommitted changes, a base branch, or a commit.
Use the exec form when JSONL or final-message capture is useful.

```sh
codex exec -C /path/to/repo -m gpt-6.1-sol -c 'review_model="gpt-6.1-sol"' \
  --sandbox read-only -c 'approval_policy="never"' --json review --uncommitted
codex exec -C /path/to/repo -m gpt-6.1-sol -c 'review_model="gpt-6.1-sol"' \
  --sandbox read-only -c 'approval_policy="never"' review --base main
codex exec -C /path/to/repo -m gpt-6.1-sol -c 'review_model="gpt-6.1-sol"' \
  --sandbox read-only -c 'approval_policy="never"' review --commit COMMIT_SHA
```

`codex review` is also non-interactive. Custom review prompts conflict with
`--uncommitted`, `--base`, and `--commit`; `--title` belongs with `--commit`.
For a scoped review with custom instructions, use a normal read-only `codex exec`
prompt that names the comparison and asks for findings without edits.

Review uses `review_model` when configured, which could be a lower-tier model,
so the examples set both `-m` and `-c 'review_model=...'` to the same Sol or
Astra slug. Keep both on every review call so a configured override cannot
swap the model.

## Continue or branch a session

Capture `thread_id` from the `thread.started` JSONL event. Prefer that exact ID
over `--last` when multiple workers may be running.

```sh
codex exec -C /path/to/repo -m gpt-6.1-sol --sandbox read-only \
  -c 'approval_policy="never"' --json resume SESSION_ID \
  'Recheck the proposed fix against the edge cases. Do not make changes.'
codex exec -C /path/to/repo -m gpt-6.1-sol --sandbox read-only \
  -c 'approval_policy="never"' --json fork SESSION_ID \
  'Explore an alternative design without changing files or external services.'
```

Resume continues the saved conversation. Fork creates a new conversation from
it; it does not by itself isolate files. Reassert the current task's permissions
and scope instead of relying on those from an older session. `--last` selects a
recent session; `--all` removes cwd filtering, which can select unrelated work.

## Worktrees and ephemeral runs

For authorised edits in a separate checkout, add `--worktree` to `codex exec`
after checking that the installed version supports it. Verify the resulting
checkout and its diff; do not assume the caller's uncommitted files are copied
into it. A worktree separates files, not external side effects.

```sh
codex exec -C /path/to/repo -m gpt-6.1-sol --sandbox workspace-write \
  -c 'approval_policy="never"' --worktree \
  'Implement the agreed fix and run its tests. Do not commit, push, or deploy.'
codex exec -C /path/to/repo -m gpt-6.1-sol --sandbox read-only \
  -c 'approval_policy="never"' --ephemeral \
  'Explain the module boundaries without changing files or external services.'
```

`--ephemeral` avoids saved session files; do not use it when later resume is
required. It is not a promise that tools or services produce no other records.
For intentional work outside Git, `--skip-git-repo-check` removes only the Git
check and does not change sandbox permissions.

## Interactive use

```sh
codex -C /path/to/repo -m gpt-6.1-sol --sandbox read-only --ask-for-approval on-request
codex resume SESSION_ID
codex fork SESSION_ID
```

Use these with a person and a terminal, not as a substitute for an unattended
worker. `/model`, `/plan`, `/permissions`, and `/status` operate inside the TUI;
they are not shell flags. Check `/status` after changing session settings.

Sources: [CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli) and
[non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode).
