---
name: review-critic
description: Build an adversarial review brief - pick up to 3 lenses (plan, spec, general, maintainability, security, performance, tests, operability, ruby, rails, frontend, database, agent-config) from the change, attach the adversarial stance and the findings contract, and have a fresh brief-writer subagent write the reviewer's prompt so the author's framing never reaches the reviewer. Use when review-loop-engine or review-local prepares a review, or for any code or plan review that needs a lens-specific, adversarial brief. Not a review runner - it prepares what a reviewer is told.
user-invocable: false
---

# Review critic

A review is only as good as its brief. This skill owns what a reviewer is told:
the adversarial stance, the lenses that fit the change, and the findings
contract. `review-loop-engine` owns how the review is run.

## Why a separate brief-writer

The agent that made the change is the worst author of its review brief: its
framing ("a small validation tweak", "the tests cover it") anchors the reviewer
towards agreement. So round 1's brief is written by a **fresh subagent** that
sees the change cold and never receives the author's reasoning. Follow
[brief-writer](references/brief-writer.md): what to hand the subagent, what to
withhold, and the fallback when the harness has no subagents.

## Parts of a brief

1. **Adversarial stance** - [adversarial](references/adversarial.md), always
   included verbatim.
2. **Lenses** - up to 3 from the table below, chosen from signals in the change,
   inlined verbatim. `general` is the fallback when nothing else fits; a plan
   review always uses `plan`. A repository can extend a lens or add its own in
   `.agents/rules/review/` - see [repo lenses](references/repo-lenses.md).
3. **Project review rules** - when the repository has them
   (`.agents/rules/review/REVIEW.md`, read from the base-commit copy), the
   review focus and the landmines on the changed paths, inlined; never the
   settled entries, the nitpick cap or earlier findings - the cap applies
   after verification. See
   [repo lenses](references/repo-lenses.md) for the file and its legacy-name
   check.
4. **Scope** - the confirmed manifest and packet paths.
5. **Findings contract** - [findings schema](references/findings.schema.json):
   every finding carries `evidence` and the `lens` that found it.

| Lens            | Signals in the change                                                                                                  | File                                                    |
| --------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| plan            | A PLAN.md, SPEC.md or design document under review                                                                     | [plan](references/lenses/plan.md)                       |
| spec            | A spec, issue, plan or acceptance criteria exists to check the change against                                          | [spec](references/lenses/spec.md)                       |
| general         | Any code; the fallback                                                                                                 | [general](references/lenses/general.md)                 |
| maintainability | Code whose shape will cost the next change: naming, duplication, misplaced behaviour, speculative abstraction          | [maintainability](references/lenses/maintainability.md) |
| security        | Auth, sessions, permissions, input parsing, uploads, secrets, crypto, outbound requests, shell or SQL built from input | [security](references/lenses/security.md)               |
| performance     | Loops over data, queries, caching, hot paths, batch jobs, payload sizes                                                | [performance](references/lenses/performance.md)         |
| tests           | Test files changed or missing for changed behaviour                                                                    | [tests](references/lenses/tests.md)                     |
| operability     | Services, jobs, retries, timeouts, logging, metrics, deploy or runtime configuration                                   | [operability](references/lenses/operability.md)         |
| ruby            | `*.rb`, `Gemfile`, `*.gemspec`, `*.rake`                                                                               | [ruby](references/lenses/ruby.md)                       |
| rails           | `app/`, `config/routes.rb`, `db/migrate/`, ActiveRecord, ActiveJob, controllers                                        | [rails](references/lenses/rails.md)                     |
| frontend        | `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, CSS, templates, client state                                                    | [frontend](references/lenses/frontend.md)               |
| database        | Migrations, schema files, raw SQL, indexes, backfills                                                                  | [database](references/lenses/database.md)               |
| agent-config    | Skills, AGENTS.md/CLAUDE.md, hooks, agent settings, deploy manifests                                                   | [agent-config](references/lenses/agent-config.md)       |

When a spec exists, prefer `spec` as one of the three - it is the axis most
often skipped.

Choose by risk, not by file count: a one-line change to an auth check earns
`security` over `general`. Language lenses (`ruby`, `rails`, `frontend`) pair
well with one risk lens. Never more than 3 - a longer brief dilutes attention,
especially on local models.

## Using it

- **Inside `review-loop-engine`**: the loop hands you the scope manifest and
  packet; you return `prompt-1.md` and the chosen lenses with a one-line reason
  each, plus any repo additions used, which the loop shows the user at scope
  confirmation. Later rounds use the re-review template in
  [brief-writer](references/brief-writer.md).
- **Inside `review-local`**: the same brief goes to a fresh reviewer subagent in
  the current harness, for one pass.
- **Standalone**: build the brief the same way and give it to any reviewer - a
  subagent, another CLI, or a person.

## Rule classes

A finding's rule class names the kind of failure, from this fixed list:
`auth`, `injection`, `secrets`, `data-exposure`, `input-validation`,
`error-handling`, `race`, `idempotency`, `migration`, `resource-leak`,
`edge-case`, `spec-gap`, `test-gap`, `convention`, `docs`, `other`.

The protected classes are `race` (concurrency), `idempotency`, `migration`
and the four security classes (`auth`, `injection`, `secrets`,
`data-exposure`). A settled entry in the project review rules never names a
protected class or `other`; `gsd validate` refuses one.

## Verifying findings

A finding is a claim until checked. Before triage, each finding goes to a
fresh verifier - one per finding, three for a one-way door in an L3 GSD item -
against the reviewed version, after the round's door map is built. The
verifier also returns the finding's fingerprint (`<path>#<symbol>:<rule
class>`), whether it is protected by meaning, and whether it is only style.
Then the [filters](references/filters.md) drop hypothetical and preference
findings, and - when the packet carries the item's earlier findings or
project review rules - confirmed repeats, settled findings and nitpicks over
the cap. A fingerprint match is only a candidate, dropped only when a
same-failure check confirms it. Security, migration, idempotency and
concurrency findings are never dropped.
[verifier](references/verifier.md) holds the door map rules, the verifier's
brief, the same-failure mode, the fallback when the harness has no
subagents, and how replies are saved and tallied. `review-loop-engine` and `review-local` both follow it.

## Reporting

Group findings by lens when reporting. Keep the `spec` findings apart from the
standards view (`general`, `maintainability` and the language lenses) and do not
rerank one against the other: a change can pass one and fail the other, and
merging them lets one hide the other.
