# Idea note template

Path: `<vault>/inbox/ideas/YYYY-MM-DD-<slug>.md`

The sections mirror the GSD IDEA document so a note can be moved into `.agents/gsd/<date>-<slug>/IDEA.md` later with the body intact and only the GSD front matter added. The front matter here follows the vault's conventions (see `obsidian-project/references/project-structure.md`), not GSD's - an inbox idea has no delivery state, owner or branches yet.

```markdown
---
title: <Human-readable idea title>
status: idea
created: YYYY-MM-DD
tags:
  - "#idea"
related:
  - "[[<existing note, project or person>]]"
---

# <Title>

## Outcome

<The problem and the intended outcome. One short paragraph. Why this would be worth doing.>

## Scope

<What the idea includes, what it deliberately excludes, and any constraints already known.>

## Completion boundary

<What "done" would look like if this were taken on. One or two sentences. If unknown, write "Not yet defined" rather than inventing one.>

## Open questions

<Only unresolved material choices, one per line. Remove this section if there are none.>
```

Rules:

- `created` is today's date from the conversation, never guessed.
- `related` holds only wikilinks you verified exist in the vault. Remove the key if there are none.
- Keep the whole note under roughly 300 words. If it wants to be longer, that is a sign the idea is ready for a GSD item or a project, so say so in the report.
- Do not add `type`, `updated`, `version`, `delivery` or `next_action`. Those arrive when the note becomes a GSD IDEA.md.

Task appended to `<vault>/action/6_INBOX.md` (Obsidian Tasks plugin format - the `➕` created date is today's date, and the wikilink alias keeps the title readable):

```markdown
- [ ] Triage idea [[YYYY-MM-DD-<slug>|<Title>]] - <one-line outcome> #idea ➕ YYYY-MM-DD
```
