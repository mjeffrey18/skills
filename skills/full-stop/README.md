# full-stop

Version 1

Prepare an existing branch for merging and then stop. The skill rebases the branch, closes out any GSD item, answers PR comments and waits for green CI. Then it waits for you to confirm the merge. You invoke it by name.

## When to use

- The branch is ready for its final steps, but you want to approve the merge yourself.

## Setup

- `git` and the GitHub CLI (`gh`), signed in.
- Uses the delivery procedure from [full-send](../full-send/README.md), so install both.

## Related skills

- [full-send](../full-send/README.md), [gsd](../gsd/README.md), [git-kiss](../git-kiss/README.md).

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Adapted from `full-stop` in [t3dotgg/tstack](https://github.com/t3dotgg/tstack) by Theo Browne (MIT). The MIT licence is in [LICENSE](LICENSE).
