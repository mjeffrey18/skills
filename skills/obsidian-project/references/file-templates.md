# File templates

Use only the templates needed for this project. Fill placeholders with known content;
omit unused sections or state a material unresolved question honestly. Do not generate
empty optional files. Replace `<slug>` in links and link only to files that exist.
Follow the vault's existing formatting where it differs.

## IDEA.md

```md
---
title: <Title>
project: <slug>
status: idea
created: <YYYY-MM-DD>
tags:
  - "#project/<slug>"
related: []
purpose: <one-line purpose>
---

# <Title>

## Mission

<the outcome and why it matters>

## Goals

1. <goal>

## Scope

<what is included and excluded>

## Completion criteria

- <observable outcome and how it will be checked>

## Current position

<meaningful progress, blockers and next action; who must act when known>
```

Add `pillar` when the vault defines pillars, from its current guidance. If a small project needs no separate
SPEC or PLAN, add its requirements and approach here. When extracting detail into those
files later, replace duplicated content with links while retaining the purpose and scope.

## TODO.md

```md
# TODO: <Title>

[[projects/<slug>/IDEA]]

#TODO

## Now

- [ ] <next concrete action>

## Next

- [ ] <following action>

## Later

- [ ] <deferred action within scope>
```

Retain completed tasks as useful history. Add supported owners, dates and blockers inline.
Empty queue headings are acceptable; invented tasks are not.

## AGENTS.md

```md
# <Title> - working context

<one-line stable description>

Read the applicable vault and projects-directory instructions first.
Start with [[projects/<slug>/IDEA]] for purpose and current position, then
[[projects/<slug>/TODO]] for immediate actions. Read existing decisions and relevant
supporting documents before continuing. Preserve settled decisions and human notes.

## Where to record what

- Purpose, scope, completion criteria and current position: IDEA.md.
- Immediate actions and task progress: TODO.md.
- Detailed requirements: SPEC.md when needed.
- Agreed sequence, dependencies and risks: PLAN.md when needed.
- Open questions and dated decisions: DECISIONS.md; significant rationale in ADRs/.
- Sourced findings and outcome evidence: FACTS.md; retain superseded conclusions.
- Raw capture: NOTES.md; structured investigations in research/.
- Source links: CONTEXT.md.
- Audience-specific plans: plan/, derived from PLAN.md.
- Finished artefacts: final/; completion or cancellation outcome: FINAL.md.

Create supporting records only when they have useful content. Keep current status in
IDEA.md and update any existing vault project-index row when it changes.
Preserve previous conclusions when reopening. Link codebase delivery records in their
repository rather than maintaining duplicate implementation tasks here.

## Conventions

Follow the vault's conventions. Use qualified wikilinks for repeated filenames.
```

Add a Design section only if a shared or local design document exists. Document routing
uses filenames in prose so absent optional files do not create broken wikilinks.

## CLAUDE.md

```md
@AGENTS.md
```

## SPEC.md

```md
# Specification: <Title>

[[projects/<slug>/IDEA]]

## Requirements

1. <requirement>

## Constraints

- <constraint and its source>

## Open considerations

- <unresolved trade-off>
```

## PLAN.md

```md
# Plan: <Title>

[[projects/<slug>/IDEA]]

## Phase 1 - <name>

1. <event or outcome>
2. <event or outcome>

## Dependencies and risks

- <dependency or risk and its implication>
```

Capture the high-level route through completion. Add phases as needed. Task checkboxes
belong in TODO. Label proposed changes clearly until agreed.

## DECISIONS.md

```md
# Decisions: <Title>

## Open

- <question requiring a decision>

## Log

- <YYYY-MM-DD> - <decision; who decided and source when known; ADR link if applicable>
```

Newest first. Retain earlier decisions when a later one supersedes them.

## FACTS.md

```md
# Facts: <Title>

## Current findings

- <finding> - <source and observation date when relevant>

## Outcome evidence

- <criterion> - <date; method; result; observed outcome; evidence link>

## Superseded findings

- <earlier conclusion> - superseded <date>: <reason and replacement link>
```

Include only sections with content. Keep assumptions separate from established findings.

## CONTEXT.md

```md
# Context: <Title>

- <source link or wikilink> - <what it contributes; source date when relevant>
```

## NOTES.md

```md
# Notes: <Title>

Raw capture. Proposals and assumptions here are not settled decisions or facts.

## <YYYY-MM-DD> - <source or topic>

<raw capture>
```

Retain the original capture when extracting structured updates elsewhere.

## ADRs/ADR-NNN-slug.md

```md
# ADR-NNN: <decision title>

- Status: proposed
- Date: <YYYY-MM-DD>
- Decision-maker: <name, if known>

## Context

<problem and constraints>

## Options

<alternatives and trade-offs>

## Decision

<proposed or accepted choice, explicitly labelled>

## Why

<reasoning>

## Consequences

<benefits, costs and follow-up>

## References

- <source or related record>
```

Use proposed, accepted or superseded as appropriate. When superseding, add the replacement
link and date without erasing the old reasoning. Add open questions if needed.

## FINAL.md

```md
# Outcome: <Title>

## <YYYY-MM-DD> - <Completed or Cancelled>

<agreed completion boundary, or cancellation reason>

### Outcomes and evidence

- <goal or criterion> - <result and evidence link>

### Artefacts

- <link to finished artefact>

### Remaining work and accepted limitations

<follow-up, abandoned work or limitations; who accepted a reduced boundary and when>
```

On reopening, mark the old conclusion historical or superseded with the date and reason.
Retain it when adding a later dated outcome. Omit sections that do not apply.

## Optional entry points and guidance

A README links the existing IDEA, TODO and supporting records for a human audience.
A local DESIGN records actual design guidance only when no suitable shared guidance exists.
Folder indexes describe their contents only when useful. None duplicates project status.
