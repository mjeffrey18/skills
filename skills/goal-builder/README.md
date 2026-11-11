# goal-builder

Version 1

Turn a long-horizon objective into a `GOAL.md` completion contract. The skill interviews you in short rounds against a ten-point readiness rubric. It then writes one document that both a long-running agent and an independent judge read the same way.

## When to use

- You are about to hand an agent a long task, such as a `/goal` run, and want a clear end state, checks and stop conditions first.

## Setup

- None. The template maps onto the `/goal` completion contract used by harnesses such as [Hermes Agent](https://github.com/NousResearch/hermes-agent). It works with any harness.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work, based on a review of long-horizon goal prompting. The interview rounds follow the grilling format from [mattpocock/skills](https://github.com/mattpocock/skills) by Matt Pocock.
