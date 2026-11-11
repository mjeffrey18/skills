# Maintaining project records

## Incorporate new material

Read the relevant existing records before editing. Preserve human text and raw captures;
extract concise updates rather than replacing sources with a summary. Link an existing
source where possible. Save a supplied raw note in NOTES or a dated research file when
it has no durable home. CONTEXT indexes sources without duplicating their contents.

Route substantive changes to their canonical records. Do not rewrite every file after
every interaction. Leave an unresolved conflict visible with its source and the decision
needed. Re-read immediately before writing if other work may have changed the files;
stop conflicting writes when ownership is unclear.

## Decisions and ADRs

DECISIONS has an Open section and a newest-first Log. Record the date, decision,
decision-maker and source when known. Identify an agent recommendation as proposed until
accepted; do not infer approval from discussion or positive feedback. Existing explicit
scoped authorisation persists. Record what it covered without claiming review of an
unseen document version.

When a decision changes, add a new entry that names the superseded decision and explains
why. Keep the earlier entry readable. Move resolved open questions into the log.

Use an ADR when a durable choice has meaningful alternatives and consequences that a
one-line log cannot explain. This can cover architecture, a vendor, a process or another
significant project trade-off. Keep routine choices in DECISIONS. Follow the vault's ADR
conventions, use stable IDs and link each ADR from the decision log. A proposed ADR is
not an accepted decision. Superseding it retains the old rationale and links the replacement.
If a repository already owns the architectural decision, link it rather than copy it.

## Facts and evidence

FACTS contains findings supported by identifiable sources, with observation or verification
dates when freshness matters. Distinguish observed results from reported claims and
inferences. A user statement can establish intent or a constraint; it does not automatically
verify an external claim. Keep untested assumptions visible in NOTES, research or an open
question rather than promoting them to settled facts.

For an outcome check, record the criterion, method, date, observed result and evidence link.
Use passed, failed, not checked or blocked as appropriate. A document review, interview,
measurement or delivered artefact can be evidence; Git commits and software tests are not
required for a vault project. Identify the artefact version or date when it matters.

If new evidence contradicts a fact, mark the earlier conclusion superseded with the reason,
date and replacement link. Keep enough history to explain decisions made from it. Archive
bulky superseded material only when useful and within scope, leaving a pointer. An old
observation remains historical evidence, not automatic proof of today's state.

## Plan, tasks and status

PLAN is the project-wide route to completion. TODO is the immediate Now / Next / Later
queue. Check a task only when its action is actually complete; record blockers beside it.
Use owners and dates only when supported, distinguishing suggestions from commitments.

Reconcile new work with the agreed scope. Record an authorised scope or sequence change
in DECISIONS and update the affected IDEA, SPEC, PLAN and TODO sections. Present unresolved
material changes as proposals. Refresh affected audience plans or explicitly mark them
stale; they must not create competing commitments.

Update IDEA's Current position with the meaningful progress, current blockers and next
practical action, naming who must act when known. Update its lifecycle status only when
supported. Reflect status changes in an existing vault project-index row.

## Lifecycle

- **Pause:** record the reason and condition for resuming. Preserve remaining tasks.
- **Block:** identify the missing dependency or decision and who can resolve it when known.
  Ordinary unfinished work is not a blocker.
- **Complete:** compare each goal and completion criterion with current evidence. If evidence
  is missing, report the gap. Present any unfulfilled criteria or limitations for explicit
  acceptance before treating them as a reduced completion boundary. Record FINAL and set
  IDEA complete once the agreed boundary is met. An existing explicit acceptance needs no
  repeated approval. Link finished artefacts and distinguish follow-up work from completed work.
- **Cancel:** record the cancellation reason, completed outcomes and abandoned work in FINAL.
  Use the vault's cancellation status convention; do not label the project successful.
- **Reopen:** read the prior FINAL, record why the project reopened and reassess affected
  scope, decisions, tasks and evidence. Mark the previous conclusion historical or superseded
  with a date. Preserve it; append a new dated outcome on later close-out.

Closing records does not authorise publishing, sending deliverables or changing external
systems. Do not archive, rename or relocate the whole project merely because it is complete.

## Examples of the intended behaviour

- “Continue the supplier project”: read its current position and settled decisions, then
  act on the authorised next step without repeating the original scoping interview.
- “Incorporate this meeting”: preserve the source, record explicit decisions and actions,
  and leave a tentative delivery date labelled tentative.
- “The estimate was wrong”: retain the old estimate as superseded, link the new evidence
  and surface its effect on the plan; do not silently accept a larger budget.
- “Close this out”: check goals against delivered artefacts and evidence. A ticked TODO
  with an unmet goal needs resolution before completion.
- “Reopen the project”: preserve the old close-out, record the new scope and next action,
  and update the existing folder rather than making a duplicate project.
