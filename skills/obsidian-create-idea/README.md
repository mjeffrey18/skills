# obsidian-create-idea

Version 1

Capture a new idea as one note in an Obsidian vault's inbox. The note follows a fixed shape: outcome, scope, completion boundary and open questions. The skill checks for duplicates first, writes the note and logs a task in the vault's inbox file.

## When to use

- You say "new idea", "park this for later" or similar, and want the idea saved without starting a planning session.

## Setup

- Set `OBSIDIAN_VAULT_PATH` to your vault, or edit `references/vaults.md` to list your vaults and paths.
- The vault needs an `inbox/` folder and an `action/6_INBOX.md` file. The skill creates `inbox/ideas/` if it is missing. The inbox line uses the [Obsidian Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) format.

## Related skills

- [obsidian-project](../obsidian-project/README.md) turns an idea into a vault project. [gsd](../gsd/README.md) turns it into a code work item.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work. The vault lookup is based on the `obsidian` skill bundled with [Hermes Agent](https://github.com/NousResearch/hermes-agent).
