# Review rounds

Read this when Claude Code is the read-only reviewer for another agent, usually
inside the `review-loop-engine` skill.
`review-loop-engine/scripts/review-round.py --reviewer claude` runs exactly
this; use it when it is installed. The command is here so the flags are
visible and for a standalone review outside the loop.

## Keep the reviewer a leaf

The reviewer gets **only Read, Grep and Glob**. The caller writes the diffs into
a packet directory outside the repo and passes it with `--add-dir`; Claude
reads them and the repository. This is the isolation, not a prompt request:

- no Bash, so no git, tests, network or other CLIs - the inherited allow rules
  in the user's settings have nothing to apply to;
- no Edit, Write or Agent, so no file changes and no sub-agents;
- `--setting-sources ""` loads no user or project settings, hooks or plugins;
- `--strict-mcp-config` loads no MCP servers.

Reviews run at `--effort medium` unless the user asks for another level. Keep
the same model for every round of one loop. Do not widen these controls to get
past a blocker. Report the blocker instead.

## Round 1

The caller has already written the packet (`scope.diff`, `prompt-1.md`) to a
directory outside the repo. Run from the repo root.

```sh
packet=/path/to/packet
schema=/path/to/review-critic/references/findings.schema.json
model=opus                       # or fable

env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL \
    -u ANTHROPIC_MODEL -u ANTHROPIC_DEFAULT_OPUS_MODEL \
    -u ANTHROPIC_DEFAULT_SONNET_MODEL -u ANTHROPIC_DEFAULT_FABLE_MODEL \
    -u CLAUDE_CODE_SUBAGENT_MODEL -u CLAUDE_CODE_USE_BEDROCK \
    -u CLAUDE_CODE_USE_VERTEX -u CLAUDE_CODE_USE_FOUNDRY \
    ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-opus-5-5 \
    ANTHROPIC_SMALL_FAST_MODEL=claude-opus-5-5 \
  claude -p --model "$model" \
    --setting-sources "" \
    --permission-mode dontAsk \
    --strict-mcp-config \
    --tools "Read,Grep,Glob" \
    --add-dir "$packet" \
    --effort medium \
    --json-schema "$(cat "$schema")" \
    --output-format json \
  < "$packet/prompt-1.md" > "$packet/round-1.raw.json" 2> "$packet/round-1.err"
```

First run `claude --setting-sources "" auth status --json` with the same `env`
prefix, so it sees exactly what the review will. Stop unless it exits 0 and
shows `loggedIn: true`, `authMethod: claude.ai`, `apiProvider: firstParty`.

## Reading the result

Treat the round as failed if the exit status is non-zero, `is_error` is true,
`subtype` is not `success`, `modelUsage` names another model, or
`structured_output` is missing. Report the failure rather than retrying with
wider permissions or another model. The JSON is a single object:

| Field                | Use                                                            |
| -------------------- | -------------------------------------------------------------- |
| `subtype`            | `success` or an error subtype; anything else is a failure      |
| `is_error`           | `true` means the run failed even if the exit status was 0      |
| `structured_output`  | The findings, shaped by the schema                             |
| `session_id`         | Pass to `--resume` for the next round                          |
| `modelUsage`         | Every key must start `claude-opus-` or `claude-fable-`         |
| `permission_denials` | Tool calls refused; with only read tools there should be none  |
| `total_cost_usd`     | Notional on a subscription; not a bill                         |

## Round 2 and later

Resume the same session so Claude keeps its earlier reading. Repeat the whole
environment and every flag - none are inherited - and add
`--resume "<session_id>"`, reading `prompt-<n>.md`.

## Timeouts

A full review can take several minutes. Allow up to 30 minutes and wait on the
same process; a timeout in the caller does not prove the child stopped. Check
for a leftover `claude` process before retrying.
