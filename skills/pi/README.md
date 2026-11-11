# pi

Version 1

Delegate analysis, implementation or review to the [pi](https://github.com/earendil-works/pi) coding agent on your own model routes. The skill covers route and thinking choice, tool and permission controls, JSON output and resumed sessions.

## When to use

- You want a pi worker or reviewer on models you run or route yourself.

## Setup

- Install pi and define your models in `~/.pi/agent/models.json`.
- Install [pi-defender](https://github.com/Serhioromano/pi-defender) (`pi install npm:pi-defender`) for write-capable workers. The examples load it from `~/.pi/agent/npm/node_modules/pi-defender/src/index.ts`. Change that path if pi installs packages elsewhere on your machine. pi-defender checks `bash` commands only. If you use other shell tools, add your own guard for them.
- The examples use a provider named `gateway` with five routes: `orchestrator`, `brain`, `think`, `agent` and `code`. Rename them, or create matching entries in your `models.json`. The routes table in `references/cli.md` shows one example setup. Replace it with your own models.

## Related skills

- [review-loop-engine](../review-loop-engine/README.md) uses this skill when pi is the reviewer.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work, written from the pi CLI documentation and live runs.
