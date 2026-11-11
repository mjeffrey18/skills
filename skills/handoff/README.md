# handoff

Version 1

Write, complete or resume a handoff document, so a fresh agent in any harness can carry on the work. Each handoff links to the one before it. The bundled script scaffolds, validates and checks handoffs for staleness.

## When to use

- You want to pause, change harness or start a new session without losing state.
- Optional: run it from compaction hooks, so a draft checkpoint is saved before the context is compacted.

## Setup

- Python 3 for `scripts/handoff.py`, which only uses the standard library.
- Optional: add the compaction hooks below, so a draft checkpoint is saved before the context is compacted, and the agent is asked to complete it afterwards. pi, omp and OpenCode need a small extension or plugin that calls the same subcommands. Those adapters are not included, and the Hooks section of `SKILL.md` lists the events they must handle.

## Hooks

Two hooks are enough. `pre-compact` writes or refreshes the draft checkpoint. `session-start` points a new session at the latest handoff. After a compaction, it also asks the agent to complete the draft. Each hook does nothing outside a git repository, and an error never blocks the harness.

The paths below assume the skill is installed in the default skills directory. Change them if you installed it elsewhere.

### Claude Code

Add this to `~/.claude/settings.json`, or to a project's `.claude/settings.json`. Merge it with any `hooks` you already have:

```json
{
  "hooks": {
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/handoff/scripts/handoff.py hook pre-compact --harness claude",
            "timeout": 30
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/handoff/scripts/handoff.py hook session-start --harness claude",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Codex

Turn hooks on in `~/.codex/config.toml`:

```toml
[features]
hooks = true
```

Then add this to `~/.codex/hooks.json`, merging it with any hooks you already have:

```json
{
  "hooks": {
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/skills/handoff/scripts/handoff.py hook pre-compact --harness codex",
            "timeout": 30
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/skills/handoff/scripts/handoff.py hook session-start --harness codex",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Codex may ask you to review and trust new hooks the first time it loads them.

To test either setup, run `/compact` in a git repository. A draft handoff should appear in `.agents/handoffs/`, or in the active GSD item's `handoffs/` folder.

## Related skills

- [gsd](../gsd/README.md). Handoffs for a GSD item are stored inside that item.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Adapted and largely rewritten from `handoff` in [mattpocock/skills](https://github.com/mattpocock/skills) by Matt Pocock (MIT) and `session-handoff` in [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) (MIT). The licences are in [LICENSE-mattpocock](LICENSE-mattpocock) and [LICENSE-softaworks](LICENSE-softaworks).
