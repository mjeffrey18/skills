# review-council

Version 1

A review panel. Two or three reviewers on different CLIs (Claude Code, Codex, pi) review the same change in parallel for one round. Each finding is checked by a fresh verifier, and the results are merged into one report. Nothing is fixed unless you ask. You invoke it as `review-council [heavy|moderate|light|<models>] [target] [fix=on] [cli=on]`.

## When to use

- A change is large or risky enough that one reviewer may miss things: permissions, migrations, a whole branch before merge.
- You want several independent reads and one merged list to decide from, not a fix-and-re-review loop.

## Modes

| Mode       | Claude Code | Codex   | pi             |
| ---------- | ----------- | ------- | -------------- |
| `heavy`    | `fable`     | `astra` | `brain`        |
| `moderate` | `opus`      | `sol`   | `orchestrator` |
| `light`    | `opus`      | `sol`   | -              |

Or type two or three model words yourself, such as `review-council astra opus this branch`. With no mode, the skill asks you to pick one when it confirms the scope.

## Setup

- The Claude Code, Codex and pi CLIs, each signed in, for the members you use.
- A harness with sub-agents and background commands (for example Claude Code or Codex). Inside T3 Code each member is a child thread on its own provider and model; elsewhere each member is a CLI review round.
- [review-loop-engine](../review-loop-engine/README.md) and [review-critic](../review-critic/README.md) (both required), and the CLI skills [claude-code](../claude-code/README.md), [codex](../codex/README.md) and [pi](../pi/README.md).

## Related skills

- [review-loop-codex](../review-loop-codex/README.md), [review-loop-claude](../review-loop-claude/README.md) and [review-loop-pi](../review-loop-pi/README.md) for one reviewer with re-review rounds.
- [review-local](../review-local/README.md) for a quick pass with no second CLI.
- [triage](../triage/README.md) to settle the decisions a council leaves you.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Adapted from `council` in [t3dotgg/tstack](https://github.com/t3dotgg/tstack) by Theo Browne (MIT). The MIT licence is in [LICENSE](LICENSE).
