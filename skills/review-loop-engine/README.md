# review-loop-engine

Version 1

Run a cross-agent review loop with you in the loop. Your current agent scopes the change and confirms the scope with you. Claude Code, Codex or pi then reviews it read-only. Your agent fixes or rebuts each finding, and the loop repeats for up to three rounds before a final report.

## When to use

- A change deserves a second opinion from a different model family.
- The `review-loop-*` entry skills or a [gsd](../gsd/README.md) item ask for a cross-agent review.

## Setup

- Python 3 for `scripts/review-round.py`, which isolates the reviewer and validates its verdict.
- At least one reviewer CLI: Claude Code, Codex or pi. Each is checked so that it can only read, cannot call other agents and is billed through its own sign-in.
- For pi reviews, set `PI_REVIEW_BASE_URLS` (see [review-loop-pi](../review-loop-pi/README.md)) and edit the pi model ids in `scripts/review-round.py` to match your routes.
- The model allow-list for Claude Code and Codex is at the top of `scripts/review-round.py`. Update it when the model names change.

## Related skills

- [review-critic](../review-critic/README.md) (required), plus [claude-code](../claude-code/README.md), [codex](../codex/README.md) and [pi](../pi/README.md) for the reviewer you use.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work.
