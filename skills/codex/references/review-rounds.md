# Review rounds

Read this when Codex is the read-only reviewer for another agent, usually inside
the `review-loop-engine` skill. `review-loop-engine/scripts/review-round.py --reviewer codex`
runs exactly this; use it when it is installed.

## Why a custom prompt, not `codex exec review`

`codex exec review --base/--commit/--uncommitted` cannot take custom
instructions, so it cannot carry a scope manifest, excluded commits or the
shared findings schema. Loop reviews use a read-only `codex exec` with the
prompt on stdin and the caller's packet of diffs.

## Round 1

```sh
packet=/path/to/packet       # outside the repo; holds scope.diff and prompt-1.md
schema=/path/to/review-critic/references/findings.schema.json
model=gpt-6.1-sol            # or gpt-6-astra - nothing lower

env -u CODEX_API_KEY -u OPENAI_API_KEY -u OPENAI_BASE_URL \
  codex exec -C /path/to/repo --ignore-user-config \
    --disable apps --disable plugins --disable multi_agent \
    --disable browser_use --disable browser_use_external \
    --disable in_app_browser --disable computer_use \
    --disable image_generation --disable goals \
    -c 'web_search="disabled"' -c 'agents.enabled=false' \
    -c 'model_provider="openai"' -c 'forced_login_method="chatgpt"' \
    -m "$model" -c "review_model=\"$model\"" \
    -c 'model_reasoning_effort="medium"' \
    --sandbox read-only -c 'approval_policy="never"' \
    --output-schema "$schema" --json -o "$packet/round-1.raw.json" - \
  < "$packet/prompt-1.md" \
  > "$packet/round-1.jsonl" 2> "$packet/round-1.err"
```

Run `codex login status` with the same `env` prefix first; stop unless it
exits 0 and reports ChatGPT sign-in.

| Control                                  | Purpose                                                                                   |
| ---------------------------------------- | ----------------------------------------------------------------------------------------- |
| `env -u CODEX_API_KEY ...`               | Uses the ChatGPT sign-in; a set `CODEX_API_KEY` would be used instead and bill the API     |
| `--ignore-user-config`                   | Skips `config.toml`: no configured MCP servers, profiles or model overrides. Auth still comes from `CODEX_HOME` |
| `--disable apps`, `plugins`              | No ChatGPT connectors or plugin tools, which load even without user config               |
| `multi_agent` + `agents.enabled=false`   | No sub-agent tools - `multi_agent` alone left `spawn_agent` in place                      |
| browser, computer-use, image, goals, `web_search="disabled"` | No web, browser, desktop or image tools                              |
| `model_provider`, `forced_login_method`  | First-party OpenAI provider and ChatGPT sign-in, even if another config layer selects a proxy or API key |
| `-m` and `review_model`                  | Pins Sol or Astra; the second stops a configured review model swapping it                 |
| `--sandbox read-only`                    | OS-enforced: no file writes and no network from shell commands                            |
| `approval_policy="never"`                | Blocked actions fail instead of waiting for an approval nobody will give                  |
| `--output-schema`                        | The final message must match the findings schema                                          |
| `-` with stdin                           | The prompt comes from the file; with an argument prompt, exec also waits on stdin         |

`--ignore-user-config` does not skip system, managed or project config layers,
and there is no switch that denies all MCP servers. List what those layers add
with `CODEX_HOME=$(mktemp -d) codex mcp list --json` (run in the repo; an empty
home hides only the user config) and add `-c mcp_servers.<name>.enabled=false`
for each name, plus any in `/etc/codex/config.toml` or the repo's
`.codex/config.toml`. The round script does this and stops if the list cannot
be read.

That list is built without the account signed in, so it cannot see
configuration an organisation account pushes from the cloud. The script
therefore also runs `codex doctor --json` (signed in, "including cloud-managed
policy") with the provider pins, and stops unless the provider is `openai`,
no managed proxy is configured, the inference and websocket endpoints are on
`chatgpt.com`, and the MCP server count is no more than the servers it can name
and disable. Stopping is deliberate: an account whose policy adds unknown
servers or endpoints cannot be used as an isolated reviewer.

After the run the script fails the round if the event stream contains any item
other than a message, reasoning step, shell command or to-do list - an MCP or
connector call, web search, file change or sub-agent. That catches a server the
checks above missed, after the fact.

One gap remains: MCP servers are matched by name across config layers, and
doctor reports only counts. If an organisation's cloud policy defined a server
with the same name as one in the user's own config, neither check could tell,
and the review run - which skips the user's config - would load it enabled.
The user's personal ChatGPT plan has no cloud policy; on an organisation-managed
account, treat Codex reviews as not isolated from MCP.

Codex does not report which model served a run, so the model is pinned, not
observed; the script reports it as `model_pinned`.

Checked on 2026-09-28: with these flags the worker reported no agent, MCP,
connector, plugin, web or image tools; the read-only sandbox refused a `touch`
in a resumed session; the schema-shaped result arrived in the `-o` file.

## Reading the result

- Failure: a non-zero exit status, a `turn.failed` or `error` event, or a
  missing or non-JSON `-o` file. Report it; do not retry with wider access or
  another model.
- Findings: the JSON in the `-o` file.
- Session: `thread_id` from the `thread.started` event - keep it for resume.

## Round 2 and later

Resume the same thread with every flag repeated - none are inherited - and the
same model: put `resume "<thread_id>" -` in place of the trailing `-`, reading
`prompt-<n>.md`.

## Keep the reviewer a leaf

The prompt says "do not edit files, and do not invoke Claude Code, Codex or any
other agent", and the flags above remove the means: no sub-agent tools, no
network for a `claude` call, no writes. Never run a review with
`workspace-write`, `danger-full-access` or the bypass flags, and do not widen
access to get past a blocker - report it.
