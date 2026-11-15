# rebase

Version 2

Run or finish a git rebase in place and resolve its conflicts. The skill resolves plain-text conflicts itself. For encrypted files (any `.enc` file, git-crypt, sops, vault and similar), it uses the tool that owns the file, and it never discards one side silently. After the rebase, it checks that the branch still fits its new base. It updates upstream code that still uses what the branch replaced, and it asks you when upstream has changed the same logic.

## When to use

- You want a branch rebased onto main or its upstream.
- A rebase stopped on conflicts, or you are stuck in the middle of one.

## Setup

- `git`. To resolve encrypted files, you need the matching tool and its keys.

## Related skills

- [modernise](../modernise/README.md) reassesses the whole branch when the base has moved a long way. The skill recommends it; you invoke it by name.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work.
