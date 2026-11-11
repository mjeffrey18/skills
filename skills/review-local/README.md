# review-local

Version 1

A quick review in your current harness. A fresh reviewer sub-agent makes one adversarial pass. Each finding is then checked on its own, and the confirmed ones are fixed. There is no second CLI and no re-review loop. You invoke it as `review-local [target] [lenses=a,b] [fix=off]`.

## When to use

- You want a fast, independent review of uncommitted work or recent commits without setting up another CLI.

## Setup

- A harness with sub-agents (for example Claude Code, Codex or pi).

## Related skills

- [review-critic](../review-critic/README.md) (required) writes the brief.
- For a review by a second agent, use [review-loop-engine](../review-loop-engine/README.md).

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work.
