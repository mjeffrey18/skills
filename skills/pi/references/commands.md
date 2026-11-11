# Commands and results

Read this for command construction and result handling. Examples use a POSIX
shell. Replace sample paths, task text and session IDs before running them.

## Analysis and planning

```sh
cd /path/to/repo
pi -p --model gateway/orchestrator --thinking high \
  --tools read,grep,find,ls \
  --no-extensions --no-skills --no-prompt-templates --no-themes \
  --no-mcp --no-approve \
  -- "$(cat /path/to/task.md)" < /dev/null
```

pi has no working-directory flag; it works in the current directory, and its
read tools also accept absolute paths elsewhere. Pass the prompt as an
argument after `--`. Passed as `@file`, pi treats it as untrusted file
contents and may not follow it. Close stdin with `< /dev/null`: in print mode
pi waits on an open stdin and never starts.

Project AGENTS.md and CLAUDE.md files load by default, which is usually what
an implementation needs. Add `--no-context-files` when the prompt should be
the only instruction, as in a review.

## Authorised implementation and output capture

Write-capable runs add `bash`, `edit` and `write`, and load pi-defender
explicitly, because `--no-extensions` otherwise drops it with the other
packages:

```sh
pi_run_dir=$(mktemp -d)
cd /path/to/repo
if pi -p --mode json --model gateway/agent --thinking medium \
  --tools read,grep,find,ls,bash,edit,write \
  --no-extensions -e ~/.pi/agent/npm/node_modules/pi-defender/src/index.ts \
  --no-skills --no-prompt-templates --no-themes --no-mcp --no-approve \
  --session-dir "$pi_run_dir/sessions" --session-id "$(uuidgen)" \
  -- "$(cat /path/to/task.md)" < /dev/null \
  > "$pi_run_dir/events.jsonl" 2> "$pi_run_dir/stderr.log"
then
  pi_status=0
else
  pi_status=$?
fi
printf 'pi exit status: %s\nOutputs: %s\n' "$pi_status" "$pi_run_dir"
```

The task text says what may change, which checks to run, and "do not commit,
push or deploy, and do not invoke Claude Code, Codex, pi or any other agent".

Checked on 2026-10-22: with this command on `code`, pi-defender blocked a
recursive force delete and pi reported the block; an ordinary write in the
same run succeeded.

Without `--mode json`, pi prints only the final reply. With it, stdout is one
JSON event per line, ending with `agent_end`. Read the exit status, stderr and
the final assistant message together; inspect the diff and test results
before reporting completion. Each assistant message names the model that
answered - check it is the route you asked for.

## Continue or branch a session

| Flag                             | Effect                                                         |
| -------------------------------- | -------------------------------------------------------------- |
| `--session-dir D --session-id U` | Creates session `U` in `D`, or resumes it exactly if it exists |
| `--continue`                     | Continues the most recent session for this directory           |
| `--fork <path\|id>`              | Starts a new session from an existing one                      |
| `--no-session`                   | Saves nothing; later resume is impossible                      |

Prefer an explicit session ID over `--continue` when several runs may be in
flight. Repeat every flag on resume - model, tools and the `--no-*` controls
are not inherited from the earlier run. The first run with a new ID writes
`Warning: No project session found ... creating a new session` to stderr;
that is expected.

## Interactive use

```sh
pi --model gateway/orchestrator
pi --resume
```

Use these with a person at a terminal, not as an unattended worker.
