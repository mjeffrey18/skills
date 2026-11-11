# Commands and results

Read this for command construction and result handling. Examples use a POSIX
shell. Replace sample paths, task text and session IDs before running them.

Every example starts with the same environment prefix, shown here as `$CLAUDE_ENV`
for brevity. Write it out in full in a real command:

```sh
env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL \
    -u ANTHROPIC_MODEL -u ANTHROPIC_DEFAULT_OPUS_MODEL \
    -u ANTHROPIC_DEFAULT_SONNET_MODEL -u ANTHROPIC_DEFAULT_FABLE_MODEL \
    -u CLAUDE_CODE_SUBAGENT_MODEL -u CLAUDE_CODE_USE_BEDROCK \
    -u CLAUDE_CODE_USE_VERTEX -u CLAUDE_CODE_USE_FOUNDRY \
    ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-opus-5-5 \
    ANTHROPIC_SMALL_FAST_MODEL=claude-opus-5-5 \
  claude ...
```

Before each run, check sign-in with the same prefix and the same
`--setting-sources` value the run will use:

```sh
$CLAUDE_ENV claude --setting-sources user auth status --json
```

## Analysis and planning

```sh
cd /path/to/repo
$CLAUDE_ENV claude -p --model opus \
  --setting-sources "" --strict-mcp-config --disable-slash-commands \
  --tools "Read,Grep,Glob" --permission-mode dontAsk \
  --output-format json < /path/to/task.md > /path/to/fresh-result.json
```

Claude works in the current directory; add `--add-dir` for each other
directory it must read. Read-only tools make the run read-only whatever the
prompt says. `--permission-mode plan` is the interactive Plan mode; for
unattended planning, use read-only tools and a no-edit prompt.

## Authorised implementation

```sh
cd /path/to/repo
$CLAUDE_ENV claude -p --model opus \
  --setting-sources user --strict-mcp-config --disable-slash-commands \
  --tools "Read,Grep,Glob,Edit,Write,Bash" --permission-mode acceptEdits \
  --allowedTools "Bash(npm test:*)" "Bash(git diff:*)" \
  --output-format json < /path/to/task.md > /path/to/fresh-result.json
```

| Control                     | Purpose                                                                                 |
| --------------------------- | --------------------------------------------------------------------------------------- |
| `--setting-sources user`    | Loads the user's deny rules and the user's command-guard hook                  |
| `--permission-mode acceptEdits` | File edits go ahead; a command that would need approval is denied and listed in `permission_denials` |
| `--allowedTools`            | Pre-approves the commands the task needs; the guard hook still runs on each one         |
| `--strict-mcp-config`       | No MCP servers                                                                          |
| `--disable-slash-commands`  | No skills, so the worker cannot load this one or a review skill and recurse             |

Checked on 2026-10-22: with this setup and `Bash(rm:*)` allowed, the guard
hook still blocked a recursive force delete, the Write tool created a file,
and `auth status` reported `claude.ai` and `firstParty`. A file-writing
command that was not pre-approved was denied; a read-only one (`date`) ran.

The task text says what may change, which checks to run, and "do not commit,
push or deploy, and do not invoke Claude Code, Codex, pi or any other agent".
Add `--worktree` for a separate checkout; check the result rather than assume
uncommitted files were copied into it.

## Reading the result

With `--output-format json` the result is one object:

| Field                | Use                                                                 |
| -------------------- | ------------------------------------------------------------------- |
| `subtype`            | `success` or an error subtype                                       |
| `is_error`           | `true` means the run failed even if the exit status was 0           |
| `result`             | The final reply                                                     |
| `structured_output`  | Present with `--json-schema`; validate it before passing it on      |
| `session_id`         | Pass to `--resume` to continue                                      |
| `modelUsage`         | Every key must start `claude-opus-` or `claude-fable-`              |
| `permission_denials` | Tool calls refused - a sign the task needed access it was not given |

A successful result is not proof that the task succeeded: inspect the diff
and run the checks.

## Continue or branch a session

Pass `--resume "<session_id>"` to continue, adding `--fork-session` to branch
into a new session instead. Repeat the environment and every flag - none are
inherited - and reassert the current task's scope rather than relying on an
older session's. `--continue` picks the most recent session in the directory;
prefer the exact ID when several runs may be in flight.
`--no-session-persistence` saves nothing, so resume is impossible.

## Timeouts

A large task can take many minutes. Wait on the same process; a timeout in
the caller does not prove the child stopped. Check for a leftover `claude`
process and partial changes before retrying.
