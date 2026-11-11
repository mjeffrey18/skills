# Specialist composition

There are no mandatory external skill dependencies. GSD's references and templates
provide a complete document workflow; specialist methods are optional enhancements.
A skill name is not a callable tool or portable slash-command API. Load it through
the current harness's supported skill mechanism or read its available SKILL.md.

Before using a candidate, inspect its instructions for prerequisites, output
location, side effects, model/agent requirements and permission compatibility.
If the user explicitly named it, follow the user's instruction within available
capabilities. Otherwise select it only when it improves the requested activity.

Each activity lists its candidate, then compatibility and the fallback.

- Light grilling (tiered start): grilling, limited to one short round on the
  outcome and how success is judged; the success question is always in it
  unless the request answers it. Find facts locally first. Fall back to a
  few direct questions through the harness's interactive Q&A.
- Full grilling (L3; offered for L1 and L2) or other unsettled intent:
  grilling. Use it for real material questions; skip settled scope. Fall back
  to concise interactive Q&A.
- Scouting: the idea-stage agents (Stage agents below) - scout-codebase,
  scout-prs and scout-worktrees in parallel, plus reproduce for a bug item.
  They are read-only and return findings; GSD records them. Fall back to
  inspecting the repository directly where the harness or user does not
  permit subagents. No separate scouting skill is required.
- Complexity tier: [complexity.md](complexity.md), bundled with GSD. No
  external skill.
- Investigate a question: an available research or documentation skill.
  Confirm it permits local research and does not publish or require
  unrelated setup. Fall back to repository inspection and authoritative
  sources.
- Plan implementation: an applicable planning skill, including plan-mode
  where mandated. Honour the harness's planning and delegation rules; some
  modes cannot persist files. Fall back to local planning only when no
  mandatory route applies.
- Define terms or an ADR: domain-modeling. Use it only when changing domain
  terminology or recording an architectural decision. Honour established
  project document locations; do not create a glossary merely to run GSD.
  Fall back to the ADR template for an in-scope decision.
- Implement or diagnose: task-specific implementation and debugging skills.
  Give them the approved scope and acceptance criteria; GSD remains the sole
  document-state writer.
- End-to-end verification (workflow.md, Verification layers, 3 to 5): what
  the harness provides - an in-app browser, Chrome or an app-preview tool for
  the UI walkthrough, a run skill that launches the app, computer use, or a
  scratch project or dry run for the mock-data run.
  Check the tool exists before planning on it. Fall back to another method,
  or ask the user to check by hand; record not_run or blocked with the
  reason, never passed.
- Simplification (tiered, after the checkpoint commit): code-simplification
  on the changed code only, preserving behaviour. Pin the behaviour first with
  a characterisation check where no check covers it, and revert a
  simplification that does not make the code easier to read. A no-op is fine.
  Fall back to a direct read of the diff for dead code, duplication and
  needless abstraction.
- Pre-implementation review or counter-review: review-loop-engine through the
  other CLI's entry (review-loop-codex, review-loop-claude) or pi
  (review-loop-pi). review-critic writes the brief: the `plan` lens for plans,
  `spec` or `general` plus up to two lenses matching the change's languages
  and risks (for example `ruby`, `frontend`, `security`, `agent-config`) for
  implementations. A default step for a tiered item (pre-implementation
  review and counter-review); an offer for an untiered one -
  see workflow.md, Cross-agent review. It needs
  the other CLI installed and signed in. Fall back to the local review; a
  counter-review that does not happen is recorded as waived.
- Local implementation review: review-local (user-invoked only) or a
  verification skill. review-local cannot be model-invoked. Offer the user
  `review-local <item> lenses=spec`: one adversarial pass over uncommitted and
  untracked work against the acceptance criteria; it verifies each finding
  and fixes the confirmed ones (`fix=off` for a review only), returning them
  for GSD to record. If declined or unavailable, review the actual changes
  against the criteria and evidence, verifying findings the same way.

Known local compatibility checks:

- grill-me is a wrapper around grilling; its optional closing question records
  decisions and ADRs through GSD's documents when an item is in play.
  GSD usually calls the underlying capability, without nesting unnecessary wrappers.
- The current to-spec publishes to an issue tracker and requires tracker setup.
  Do not invoke it to write local SPEC.md. Use the GSD template.
- code-review is retired (`skills/1_retired/`); offer review-local instead. It
  needs no tracker setup and reviews uncommitted and untracked files, but only
  the user can invoke it.
- A planning skill may mandate a particular subagent. That requirement applies
  to its invocation; GSD does not mandate that role globally.

Before delegating, supply: item/owner path, settled decisions, allowed scope,
existing approval, bounded question, required output and write ownership.
Specialists return findings to GSD; they do not independently change approvals,
mark the item verified or dispatch implementation outside the user's authority.

If a specialist unexpectedly asks to publish, install, deploy or create unrelated
configuration, keep that action outside this task. Explain the incompatibility
and use the local fallback. Do not silently rewrite a third-party skill's rules
and claim to have followed it.

## Stage agents

Each stage's subagents are defined in `references/<stage>/<name>.md` (stages
idea, plan, build, review and complete). Each file is a short brief; the
method stays in the skill it names. Resolve them with `gsd agents <stage>`,
and hand a subagent the composed brief from
`gsd agents <stage> <name> --body`. `gsd agents --all` lists every stage and
where each part came from, for Kickoff's override list.

Overrides come from `~/.agents/rules/<stage>/`, then the repo's
`.agents/rules/<stage>/`; the repo wins, so a project can pin its own
behaviour. A file with the same name replaces the agent, `NAME_N.md`
(`name: NAME`, `mode: append`, `extends: NAME`) appends to it in number
order, and a new name adds an agent. An append file keeps the base agent's
name in its front matter, because `gsd agents` rejects any other name. Files
without `mode` in their front matter are not definitions, so
review-critic's repo lenses and the project review rules
(`.agents/rules/review/REVIEW.md`) can share the folder. A `REVIEW.md` that
already has `mode` stays a stage agent, and one that `index.md` lists stays
a lens; `gsd agents`, `gsd validate` and `gsd risk` report the collision and
read no project review rules from it until it is renamed.

The skill sets the order of its own agents in a stage; any other agent in
that stage runs in parallel. At most 4 subagents are active at once in a
stage, and the rest queue, so a stage with many overrides does not flood the
machine or the provider. Launch subagents through T3 Code when it is present,
so each child has a thread the user can watch and stop. Outside T3 Code, a
subagent on the session's own provider and model uses the harness's own
subagent tool (Claude Code's Agent tool, Codex's spawn_agent); another
provider goes through the claude-code, codex or pi skill.

Topology: by default one implementer subagent on the same provider and model
as the session. Run implementers in parallel only when the slices touch
separate files, do not depend on each other, have interfaces fixed in PLAN or
SPEC and can each be tested alone - and then each in its own worktree, so
they cannot overwrite each other. CP2 approves the topology; the user may
change it there.
