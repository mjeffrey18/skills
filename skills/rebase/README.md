# rebase

Version 1

Run or finish a git rebase in place and resolve its conflicts. The skill resolves plain-text conflicts itself. For encrypted files (any `.enc` file, git-crypt, sops, vault and similar), it uses the tool that owns the file, and it never discards one side silently.

## When to use

- You want a branch rebased onto main or its upstream.
- A rebase stopped on conflicts, or you are stuck in the middle of one.

## Setup

- `git`. To resolve encrypted files, you need the matching tool and its keys.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work.
