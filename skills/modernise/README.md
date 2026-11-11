# modernise

Version 1

Bring a stale branch up to date. The skill rebases the branch, checks whether its change is still relevant and finds useful changes on the updated base. Then it recommends whether to close, amend or merge the branch. You invoke it by name.

## When to use

- A branch has sat for a while and you are not sure whether it still makes sense.

## Setup

- `git`. The GitHub CLI (`gh`) helps when the branch has a PR.

## Related skills

- [rebase](../rebase/README.md) resolves the conflicts, [git-kiss](../git-kiss/README.md) provides the branch commands, and [full-send](../full-send/README.md) delivers the branch afterwards.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Adapted from `modernize` in [t3dotgg/tstack](https://github.com/t3dotgg/tstack) by Theo Browne (MIT). This version keeps rebasing separate from publishing and delivery. The MIT licence is in [LICENSE](LICENSE).
