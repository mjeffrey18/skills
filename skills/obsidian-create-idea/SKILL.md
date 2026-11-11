---
name: obsidian-create-idea
description: Capture a new idea as a single note in an Obsidian vault's inbox (`inbox/ideas/YYYY-MM-DD-<slug>.md`) using the GSD IDEA shape - outcome, scope, completion boundary, open questions - and log it in the vault's `action/6_INBOX.md`. Use whenever the user says "new idea", "capture this idea", "add an idea", "note this down as an idea", "park this for later", invokes /obsidian-create-idea, or describes something they might build or do later without asking to plan or start it. Checks the vault for an existing or similar idea first. Not for managing a project (obsidian-project) or starting a GSD work item (gsd).
---

<what-this-is>

This skill captures an idea fast, in a fixed shape, in the right vault, without losing it and without turning capture into a planning session. It is the front door of a pipeline: an idea note sits in `inbox/ideas/` until the user either drops it or moves it into `.agents/gsd/` in the owning repository and fleshes it out there with the `gsd` skill.

It does one thing: **write one idea note and log it**. Do not scope the idea into a project (that is `obsidian-project`), do not create a GSD item, and do not start researching the idea unless asked.

The flow is always four steps:

1. **Locate** the vault.
2. **Check** the vault for the same or a similar idea.
3. **Clarify** only what the note cannot be written without.
4. **Write** the note and the inbox line, then report.

</what-this-is>

<the-workflow>

### Step 1 - Locate the vault

Resolve the vault in this order and stop at the first that works:

1. `OBSIDIAN_VAULT_PATH` is set. Verify the directory exists and contains an `AGENTS.md` or an `inbox/` folder. Use it without asking. Set it per agent or per shell to fix a default vault.
2. The user named a vault or a path. Resolve the name through [references/vaults.md](./references/vaults.md).
3. Neither. Ask one question listing the vaults in [references/vaults.md](./references/vaults.md) with their paths and recommend the one that fits the idea's domain (for example work ideas → `work`, everything else → `personal`).

Never pick whichever vault the Obsidian app happens to have open, and never write across vault boundaries. Read the vault's root `AGENTS.md` if there is one - its conventions override anything here.

### Step 2 - Check for duplicates

Before writing, search the vault for the same idea under a different name. Cheap and fast - do not turn it into research:

- List `inbox/ideas/` and scan titles and slugs.
- Grep `inbox/`, `projects/` and `action/4_IDEAS.md` for two or three distinctive words from the idea (product names, nouns that would appear in any phrasing of it). Match filenames as well as content, restrict to `.md` files and ignore `logs/` and similar artefact folders, since project trees hold test output that produces false hits. With the Obsidian CLI available, `obsidian vault=$OBSIDIAN_VAULT_NAME search query='<words>' format=json` does the same in one call.
- If a project folder already exists for it, the idea is not new.

If you find a match or a near match, show the user the path and its first lines and ask one question: append to the existing note, create a new one anyway and link them under `related`, or stop. Do not silently create a second note.

### Step 3 - Clarify

The note needs an outcome and a rough scope. If the user's message already gives both, write without asking. If one is missing, ask one question with a recommended answer. Two questions is the ceiling. A one-line idea from a chat message is a valid input; the point is to capture it, so when in doubt write what you have and leave the gap under Open questions.

Do not grill. Do not ask about approach, timeline, risks or priority. Those belong to the GSD item or project that may follow.

### Step 4 - Write

Create `<vault>/inbox/ideas/YYYY-MM-DD-<slug>.md` from [references/idea-template.md](./references/idea-template.md). Use today's date, a short kebab-case slug of three to five words, and the vault's frontmatter conventions. Create `inbox/ideas/` if it does not exist. If the exact path already exists, stop and ask rather than overwrite.

Populate `related` with `[[wikilinks]]` to the notes, projects or people the Step 2 search surfaced, since that is the one piece of context that is cheap now and expensive later.

Then append one Markdown task to `<vault>/action/6_INBOX.md`. The vaults use the Obsidian Tasks plugin, so the line is a checkbox with a created-date marker (`➕`) so it appears in the `tasks` queries and sorts by age:

```
- [ ] Triage idea [[YYYY-MM-DD-<slug>|<Title>]] - <one-line outcome> #idea ➕ YYYY-MM-DD
```

Keep whatever heading and existing lines the file has. If the vault's `6_INBOX.md` carries extra conventions (for example an ownership tag), add them to the same line rather than dropping the task format.

Report back in two or three lines: the note path, the inbox line, and any match you decided not to merge with.

</the-workflow>

<conventions>

Obey the target vault's `AGENTS.md` first. Default style rules, when the vault sets none: British English, `-` spaced hyphen never an em dash, no Oxford comma, prose by default with lists only where the content is a list, `[[wikilinks]]` for internal links, and none of the AI-giveaway phrasing (no "delve", "leverage" as a verb, "it's worth noting", "landscape" or "realm" as filler). Use the resolved absolute path with file tools, never a literal `$OBSIDIAN_VAULT_PATH`.

</conventions>

<references>

- [references/idea-template.md](./references/idea-template.md) - the note template and what each section holds.
- [references/vaults.md](./references/vaults.md) - the known vaults, their paths per machine and which domain each serves.

</references>
