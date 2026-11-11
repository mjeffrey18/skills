# gsd

Version 1

GSD manages a piece of work as a set of Markdown documents in your repository, under `.agents/gsd/<date>-<slug>/`. It covers the full life of an item: the idea, decisions, facts, plan, spec, TODOs, reviews and the final summary. Three human checkpoints control the work: Kickoff, Pre-implementation and Review. A complexity tier from L1 to L3 decides how much planning, review and verification an item needs.

## Visual guides

Two interactive pages show how GSD runs. Download them and open them in a browser, because GitHub shows HTML files as source.

- [GSD lifecycle](../../docs/gsd-lifecycle.html) - every stage by tier, with what each checkpoint asks and which records each stage writes.
- [GSD stage agents](../../docs/gsd-stage-agents.html) - the subagent each stage runs, and how a repository replaces, extends or adds to them.

## When to use

- You want a change to survive across sessions and harnesses, with its decisions and evidence written down.
- You want a fixed process that runs from idea to merged branch, with human approval at set points.

## Setup

- Python 3 for the bundled `scripts/gsd` CLI, which only uses the standard library. It lists, validates and updates items. You can add it to your `PATH`.
- `git`. Branch delivery uses the GitHub CLI (`gh`).
- Optional: repository review rules in `.agents/rules/review/` and your own rule overrides in `~/.agents/rules/`.

## Related skills

GSD calls other skills at set points. Install the ones you want:

- [review-loop-engine](../review-loop-engine/README.md) and [review-critic](../review-critic/README.md) for cross-agent reviews.
- [full-send](../full-send/README.md) and [full-stop](../full-stop/README.md) for branch delivery.
- [handoff](../handoff/README.md) to pass the work to a new session.
- `grilling` and `grill-me` from [mattpocock/skills](https://github.com/mattpocock/skills) for discovery interviews.
- `code-simplification` from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) for the simplification pass.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work. GSD calls the grilling and code-simplification skills credited above, but it does not include them.
