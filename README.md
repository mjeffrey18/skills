# Agent Skills

Release v1

Skills for coding agents such as Claude Code, Codex, pi and OpenCode. Each skill is a folder in the open [Agent Skills](https://agentskills.io) format: a `SKILL.md` file with instructions, plus any references, templates and scripts it needs.

The skills come from a private working setup and are shared here as they are. This repository receives exported releases only, so changes are not made here.

Some skills still refer to the setup they were written for: particular harnesses, model names and routes, tools, folder layouts and conventions. Treat them as a starting point. For results that fit your work, fork the repository and adapt the skills to your own tools, models and conventions.

## Skills

| Skill                                                         | Version | What it does                                                                                                                         |
| ------------------------------------------------------------- | :-----: | ------------------------------------------------------------------------------------------------------------------------------------ |
| [claude-code](skills/claude-code/README.md)                   |    1    | Delegate analysis, implementation or review to Claude Code from another agent harness, such as Codex or pi.                          |
| [codex](skills/codex/README.md)                               |    1    | Delegate analysis, implementation or review to the Codex CLI from another agent harness.                                             |
| [full-send](skills/full-send/README.md)                       |    1    | Finish an existing branch from start to end.                                                                                         |
| [full-stop](skills/full-stop/README.md)                       |    1    | Prepare an existing branch for merging and then stop.                                                                                |
| [git-kiss](skills/git-kiss/README.md)                         |    1    | A reference for [git-kiss](https://github.com/mjeffrey18/git-kiss) (`gk`), a small CLI for rebase-based git workflows.               |
| [goal-builder](skills/goal-builder/README.md)                 |    1    | Turn a long-horizon objective into a `GOAL.md` completion contract.                                                                  |
| [gsd](skills/gsd/README.md)                                   |    1    | GSD manages a piece of work as a set of Markdown documents in your repository, under `.agents/gsd/<date>-<slug>/`.                   |
| [handoff](skills/handoff/README.md)                           |    1    | Write, complete or resume a handoff document, so a fresh agent in any harness can carry on the work.                                 |
| [modernise](skills/modernise/README.md)                       |    1    | Bring a stale branch up to date.                                                                                                     |
| [obsidian-create-idea](skills/obsidian-create-idea/README.md) |    1    | Capture a new idea as one note in an Obsidian vault's inbox.                                                                         |
| [obsidian-project](skills/obsidian-project/README.md)         |    1    | Create, resume and maintain a project in an Obsidian vault, from the first scoping to close-out or reopening.                        |
| [pi](skills/pi/README.md)                                     |    1    | Delegate analysis, implementation or review to the [pi](https://github.com/earendil-works/pi) coding agent on your own model routes. |
| [rebase](skills/rebase/README.md)                             |    1    | Run or finish a git rebase in place and resolve its conflicts.                                                                       |
| [review-critic](skills/review-critic/README.md)               |    1    | Build an adversarial review brief.                                                                                                   |
| [review-local](skills/review-local/README.md)                 |    1    | A quick review in your current harness.                                                                                              |
| [review-loop-claude](skills/review-loop-claude/README.md)     |    1    | Have Claude Code review your current change in a fix-and-re-review loop of up to three rounds, with you in the loop.                 |
| [review-loop-codex](skills/review-loop-codex/README.md)       |    1    | Have Codex review your current change in a fix-and-re-review loop of up to three rounds, with you in the loop.                       |
| [review-loop-engine](skills/review-loop-engine/README.md)     |    1    | Run a cross-agent review loop with you in the loop.                                                                                  |
| [review-loop-pi](skills/review-loop-pi/README.md)             |    1    | Have pi review your current change on your own models in a fix-and-re-review loop of up to three rounds, with you in the loop.       |
| [triage](skills/triage/README.md)                             |    1    | Walk through a list of items one decision at a time.                                                                                 |

Each skill's README explains what it does, what you need to set up and which other skills it depends on.

## Install

Copy the skill folders you want into your agent's skills directory:

| Agent       | Personal skills directory    |
| ----------- | ---------------------------- |
| Claude Code | `~/.claude/skills/`          |
| Codex       | `~/.codex/skills/`           |
| pi          | `~/.pi/agent/skills/`        |
| OpenCode    | `~/.config/opencode/skills/` |

For example:

```sh
git clone https://github.com/mjeffrey18/skills.git
cp -R skills/skills/handoff ~/.claude/skills/
```

You can also use the [`skills` CLI](https://github.com/vercel-labs/skills): `npx skills add mjeffrey18/skills`.

Some skills work together. For example, the `review-loop-*` skills need `review-loop-engine` and `review-critic`. Check the Setup and Related skills sections in each README before you install one on its own.

## Versions

Each release has a number (`v1`, `v2` and so on) and a matching git tag. Each skill has its own version, shown at the top of its README. A skill's version goes up only when its content changes. `manifest.json` records the release and every skill's version.

## Also recommended

These skills are used here unchanged from their authors, so they are not copied into this repository. Install them from the original source:

- [`grilling` and `grill-me`](https://github.com/mattpocock/skills) by Matt Pocock - interview rounds that stress-test a plan. `gsd` and `goal-builder` use this format.
- [`code-simplification`](https://github.com/addyosmani/agent-skills) by Addy Osmani - simplifies code without changing its behaviour. `gsd` uses it for its simplification pass.

## Credits

Some skills are adapted from, or inspired by, other people's work. Each skill's README names its sources in a Credits section. Where a skill includes third-party material, that skill's folder also holds the original licence.

Thanks in particular to [Matt Pocock](https://github.com/mattpocock/skills), [Theo Browne](https://github.com/t3dotgg/tstack), [softaworks](https://github.com/softaworks/agent-toolkit) and [Addy Osmani](https://github.com/addyosmani/agent-skills).

## Licence

MIT - see [LICENSE](LICENSE). Third-party material keeps its own licence, stored in the folder of the skill that uses it.
