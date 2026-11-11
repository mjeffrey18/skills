# full-send

Version 1

Finish an existing branch from start to end. The skill rebases it, closes out any GSD item, answers PR comments, waits for green CI, merges locally, publishes and cleans up the worktree. You invoke it by name, and it never runs on its own.

## When to use

- The branch is done and you want it delivered without stopping for confirmation before the merge.
- Use [full-stop](../full-stop/README.md) instead when you want to confirm the merge yourself.

## Setup

- `git` and the GitHub CLI (`gh`), signed in.
- Works best with [git-kiss](../git-kiss/README.md) for branch commands.

## Related skills

- [full-stop](../full-stop/README.md), [modernise](../modernise/README.md), [gsd](../gsd/README.md), [rebase](../rebase/README.md).

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Adapted from `full-send` in [t3dotgg/tstack](https://github.com/t3dotgg/tstack) by Theo Browne (MIT). This version adds GSD close-out and stricter review and verification gates, and it removes the upstream's model-specific review and blanket permissions. The MIT licence is in [LICENSE](LICENSE).
