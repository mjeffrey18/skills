# Models, reasoning, and modes

Read this when changing the worker's configuration. The model is always pinned
to Sol or Astra (below). For everything else, preserve an explicit user choice
and otherwise inherit the existing configuration.

## Discover capabilities

```sh
codex --version
codex debug models --help
codex debug models
```

`codex debug models` returns the model catalogue as JSON.
Inspect `slug`, `default_reasoning_level`, `supported_reasoning_levels`, and
`service_tiers`. Use `codex debug models --bundled` for an offline snapshot
shipped with the binary. The bundled catalogue may be stale and neither form
guarantees that the account can access every listed model.

If an older binary lacks model discovery, use its interactive `/model` picker
and current official documentation. Do not invent a model ID or silently replace
an unavailable model requested by the user.

## Allowed models: Sol and Astra only

Delegated work, and reviews in particular, runs on one of these two models.
Pass `-m` on every call; do not inherit the configured model, and do not use a
lower-tier model (Luna, Terra, older generations) even for small tasks.

| Model | `-m`           | Use                                                        |
| ----- | -------------- | ---------------------------------------------------------- |
| Sol   | `gpt-6.1-sol`  | Default for analysis, implementation and review            |
| Astra | `gpt-6-astra`  | When the user asks for it, or for a large or risky change  |

The Sol model ID is confirmed in the [official model documentation](https://developers.openai.com/api/docs/models/gpt-6.1-sol).
Account access has not been tested for this update. Check the live catalogue
before running. If the chosen slug is unavailable, stop and report it rather
than substituting another model.

## Set model and reasoning separately

```sh
codex exec -C /path/to/repo -m gpt-6.1-sol \
  -c 'model_reasoning_effort="high"' --sandbox read-only \
  -c 'approval_policy="never"' \
  'Analyse the concurrency bug without changing files or external services.'
```

`-m` selects the model. `-c model_reasoning_effort=...` selects effort; there is
no separate `--reasoning` flag. Sol 6.1 supports `low`, `medium`, `high`, `xhigh` and `max` in the
[official model documentation](https://developers.openai.com/api/docs/models/gpt-6.1-sol).
Check `supported_reasoning_levels` in the CLI catalogue for the chosen model
rather than assuming the same range for Sol and Astra. Review rounds run at `medium`
unless the user asks for another level. Otherwise, inherit the
configured effort unless the user sets one; raise it for ambiguous design,
difficult debugging, or a complex review. Some effort levels can change
delegation behaviour; read their capability descriptions.

## Service tiers and profiles

Service tier is separate from model and effort. Only request a tier advertised
for the selected model and supported by the active provider. A per-run override
uses `-c 'service_tier="priority"'` when that tier is supported. The interactive
`/fast` command is capability-dependent and can persist the user's selection;
prefer per-run overrides for delegated tasks.

Use `-p PROFILE_NAME` only when the user asks for an existing profile or the task
requires it. On the checked binary, this layers
`$CODEX_HOME/PROFILE_NAME.config.toml` over the base user configuration. Older
versions have different profile formats, so consult installed help. Profiles
can affect more than the model: inspect relevant settings before selecting one.
Command-line `-c` overrides apply to that invocation; they do not edit the
configuration file. Managed policy can constrain effective settings.

Profiles can switch the model or provider (for example a model gateway or local
profile). Do not use one for delegated work unless it resolves to Sol or Astra,
and still pass `-m` explicitly. Local and open-source providers (`--oss`) are
out of scope for this skill.

## Execution mode and permissions

| Control                        | Meaning                                                             |
| ------------------------------ | ------------------------------------------------------------------- |
| Interactive `codex`            | Terminal conversation with interactive controls.                    |
| `codex exec`                   | Non-interactive task with capturable output.                        |
| `codex exec review`            | Non-interactive review of a selected Git target.                    |
| `--sandbox read-only`          | Read-only command sandbox for inspection and analysis.              |
| `--sandbox workspace-write`    | Permit command writes within the allowed workspace roots.           |
| `--sandbox danger-full-access` | Broad command access; not a routine workaround for blocked work.    |
| Approval `on-request`          | The agent can request approval when needed.                         |
| Approval `never`               | No approval prompts; blocked execution fails instead of escalating. |

For unattended exec examples, set `-c 'approval_policy="never"'` and the required
sandbox explicitly. For interactive use, the checked root command exposes
`--ask-for-approval`. Do not assume every root flag is accepted after every
subcommand.

`--approve-for-me` routes approvals through automatic review with a
workspace-write sandbox. It is not the same as `never` or unrestricted access.
`--dangerously-bypass-approvals-and-sandbox` disables both approval prompts and
sandboxing; use only when explicitly authorised in a suitably isolated
environment. Do not enable it to bypass a caller's restrictions.

Use `--add-dir` for specifically authorised additional writable directories
rather than broadening access to the whole host. Network access is a separate
setting; workspace-write does not by itself establish network availability.
Connected tools can have their own side effects outside the command sandbox.
Preserve user/project rules and hook trust; skipping them is not normal setup.

Use explicit `--sandbox workspace-write` in new commands. `--full-auto` is a
deprecated compatibility option, not the recommended automation mode.

## Plan mode

In the interactive TUI, `/plan` enters Plan mode and can take inline task text.
It is not a shell command or an `exec --plan` option. Non-interactive planning
uses a clear no-edit prompt and read-only command permissions, as shown in
[commands](commands.md). Do not claim these are identical mechanisms.

Sources: [CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli),
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference),
and the installed CLI's help and model catalogue (checked 2026-09-28).
