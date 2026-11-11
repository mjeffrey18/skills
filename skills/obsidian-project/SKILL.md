---
name: obsidian-project
description: Create, resume and maintain an Obsidian vault project through close-out or reopening. Use when asked to start a vault project, continue one, incorporate new notes or evidence, reconcile its documents or assess completion. Formerly obsidian-create-project. Inbox idea capture belongs to obsidian-create-idea; codebase delivery items belong to gsd.
---

# Obsidian project

Keep a vault project's purpose, decisions, knowledge and next actions coherent across sessions.
Work within the requested project and action. Maintenance happens during requested work;
recurring reviews, vault-wide reorganisation and external actions need their own authorisation.

## Orient

1. Resolve the vault and project from the request and working context. Read the vault,
   projects directory and project's applicable `AGENTS.md` instructions. Ask only when
   the target remains ambiguous. Keep writes inside the chosen vault.
2. For existing work, read `IDEA.md`, `DECISIONS.md` and the relevant plan, tasks, facts
   and sources. Read `FINAL.md` if present. Establish what is settled, what remains open
   and the requested next action. Do not restart discovery or expand the scope of
   historical approvals.
3. Before writing, read [project-structure.md](references/project-structure.md).
   Use [file-templates.md](references/file-templates.md) only for files being created.
   Adopt existing projects in place: preserve their names, content, human comments and
   useful conventions. Do not regenerate them from templates or bulk-migrate other projects.

## Create

Read [scoping-questions.md](references/scoping-questions.md). Use the conversation and
related vault material to establish the outcome, scope, completion criteria and first actions.
Ask one focused question at a time where a material gap remains. A sufficient brief does
not need another interview.

Choose a short kebab-case slug under `<vault>/projects/<slug>/`. Search for an existing
matching project before creating one. Resume a clear match when that is the request;
clarify a genuine naming collision rather than merging distinct projects.

Create `IDEA.md`, `TODO.md`, `AGENTS.md` and the `CLAUDE.md` pointer. Add supporting
files only when there is substantive content for them. Record decisions and sourced findings
already established during scoping. Confirm unresolved scope choices before presenting them
as agreed; an explicit instruction to create from an agreed brief is sufficient authority.

## Resume and maintain

Perform the requested work, then reconcile the affected records using
[maintenance.md](references/maintenance.md). In particular:

- Preserve raw captures and source links when extracting decisions, findings and actions.
- Distinguish proposals, assumptions, verified findings and human commitments.
- Keep the agreed sequence in `PLAN.md` and the immediate queue in `TODO.md`.
- Keep lifecycle status and the current position in `IDEA.md`; instructions stay stable.
- Carry forward unresolved questions and superseded conclusions with their history.

A request to incorporate meeting notes authorises recording their contents and supported
outcomes. It does not authorise carrying out every action mentioned in the meeting.
Routine record updates need no repeated approval. Ask when evidence conflicts with an agreed
scope, priority or commitment and the choice materially affects the project.

Use compatible research, writing or review skills when the task benefits from them. Keep
project records here. If delivery requires codebase work, link the relevant GSD item and
summarise its contribution; leave its implementation tasks and technical evidence in the
repository. Do not start a GSD item or implement code merely because a project mentions it.

## Close, pause or reopen

Read the lifecycle section of [maintenance.md](references/maintenance.md). Compare actual
outcomes and evidence with the goals and completion criteria before marking complete.
Record a concise `FINAL.md` with artefacts, accepted limitations and any remaining work.
Preserve previous conclusions when reopening; cancellation is distinct from completion.

## Check and hand over

Re-read changed documents. Check that status, plan, tasks and decisions agree, internal
links resolve and no empty scaffold or invented commitments remain. Check any affected
vault project-index row against `IDEA.md`. Report the substantive changes, evidence,
next action and actual blockers. Document checks alone do not prove the project succeeded.

Follow the target vault's conventions. Defaults are British English, spaced hyphens,
no Oxford comma and vault-relative `[[wikilinks]]` for internal links. Use qualified
links such as `[[projects/<slug>/IDEA]]` where common filenames could be ambiguous.
