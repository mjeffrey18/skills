# Review rounds

Read this when pi is the read-only reviewer for another agent, usually inside
the `review-loop-engine` skill. `review-loop-engine/scripts/review-round.py
--reviewer pi` applies everything below - use it rather than building the
command by hand.

## Routes

Reviews run on four routes only; the script refuses anything else, including
`agent`.

| Word           | Route                   | Thinking | Use                      |
| -------------- | ----------------------- | -------- | ------------------------ |
| `orchestrator` | GLM-5.3-Flash           | high     | Default - difficult work |
| `brain`        | GLM-5.3-Flash           | max      | Hard work, slowest       |
| `think`        | Qwen3.8-27B (reasoning) | xhigh    | Difficult work, slower   |
| `code`         | Qwen3.8-27B (coding)    | medium   | Moderate work, fastest   |

Keep the same route for every round of one loop. If a route is unavailable,
stop and report it - do not fall back to another.

Route labels do not prove where traffic goes - another config could map
`gateway/code` to a hosted endpoint. Before each run the script ignores
`PI_CODING_AGENT_DIR`, reads the default `models.json`, and stops unless the
route resolves to the user's gateway (`PI_ALLOWED_BASE_URLS` in the script):
the model entry's own `baseUrl` if it has one, which pi prefers, else the
`gateway` provider's. After the run it checks that every assistant message
reports the requested route. That confirms the request, not the model behind
the gateway.

## Keep the reviewer a leaf

```sh
pi -p --mode json --model gateway/orchestrator --thinking high \
  --tools read,grep,find,ls \
  --no-extensions --no-skills --no-prompt-templates --no-themes \
  --no-approve --no-mcp --no-context-files \
  --append-system-prompt "<read-only reviewer note>" \
  --session-dir "$packet/pi-sessions" --session-id <uuid> \
  -- "<prompt text>" < /dev/null
```

| Control                                | Purpose                                                                                      |
| -------------------------------------- | -------------------------------------------------------------------------------------------- |
| `--tools read,grep,find,ls`            | Allowlist for built-in, extension and custom tools: no bash, edit, write or sub-agents       |
| `--no-extensions`                      | No extension tools or hooks (sub-agents, web access, codemode); also drops built-in MCP      |
| `--no-mcp`                             | No MCP servers or tools. `--tools` keeps MCP tools, so this is set explicitly |
| `--no-skills`, `--no-prompt-templates` | The reviewer cannot load this or any other skill and recurse                                 |
| `--no-approve`                         | Ignores project-local pi files, which could add tools                                        |
| `--no-context-files`                   | No global or project AGENTS.md; the prompt names the standards files to read                 |
| `--append-system-prompt`               | Names the four tools and the JSON-only reply (see Output)                                    |
| `--session-dir`, `--session-id`        | Sessions live in the packet; the same ID resumes exactly                                     |
| prompt as an argument                  | Passed as `@file`, pi treats the prompt as untrusted file contents and may not follow it     |
| `< /dev/null`                          | pi waits on an open stdin in print mode and never starts                                     |

pi's read tools take absolute paths, so the reviewer can read a sibling
checkout without extra flags. Do not widen these controls to get past a
blocker. Report the blocker instead.

After each run the script checks that every tool call was one of the four
read tools, that the route matches, and that the last message stopped
normally. The first round writes `Warning: No project session found ... creating
a new session` to `round-1.err`; that is expected.

## Output

pi cannot enforce a JSON schema. The script appends the findings schema to the
prompt, takes the JSON from the final message and validates it field by field.
Two failure modes have been seen with GLM on long reviews:

- The model asked for a tool it does not have by writing
  `<tool_call>bash...` as text, which ends the turn with no review. The
  appended system note says there is no such tool.
- After a long review, findings came back without `status`. In round 1 every
  finding is new, so the script fills in `status: new` there; later rounds
  must state it.

On any other formatting problem the script sends one repair turn in the same
session, restating the required keys and values. A wrong route, a disallowed
tool or an abnormal stop fails the round without a repair.

## Size

A 150-file, 360 KB diff on `orchestrator` took 18 minutes, then 8 more for a
repair turn. For a change past the size limit in `review-loop-engine`'s
scoping, say that pi will be slow and offer smaller loops - or Claude or Codex
for the large one.
