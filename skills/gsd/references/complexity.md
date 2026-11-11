# Complexity tiers

Complexity decides how much care a GSD item gets: which documents it needs,
how deep discovery and grilling go, which reviews are recommended and what
evidence closes it. It is not "how hard the code is to write". It is "how
much care this change deserves".

## Dimensions

Score each dimension on its own. Use what scouting found, not a guess.

### Risk - the impact if it goes wrong

- L1: internal or single-user impact; fully reversible by a revert or
  redeploy; no secrets, compliance or sensitive paths.
- L2: visible to customers or other teams; reversible with effort (a data
  fix, a flag flip, a coordinated redeploy); may touch personal data; no
  critical path.
- L3: affects every user or cannot be undone (sent messages, charged cards,
  deleted or migrated production data); or touches authentication,
  permissions, secrets, payments, production schemas or another critical
  path the repository names.

Risk floor: when the repository has project review rules
(`.agents/rules/review/REVIEW.md`), `gsd risk PATH...` on the paths the
change will touch sets the lowest Risk score - L3 for an `always_high`
match or tier 2, L2 for tier 1, none for tier 0.

### Change - the size and surface

- L1: under about 50 changed lines and 5 files; one component; no schema,
  public interface or dependency change beyond a patch bump.
- L2: under about 500 lines and 30 files; one or two components; internal
  interface changes; minor dependency bumps.
- L3: more than about 500 lines, or three or more components, a schema
  migration, a public interface change, a new dependency or a major version
  bump.

The line and file counts are guides. A change that reaches across several
projects, harnesses or machines scores at least L2.

### Confidence - the safety net that already exists

- High: automated tests cover the affected behaviour, failures would be
  visible, and the change follows an established pattern in the repository.
- Medium: partial tests, basic visibility of failures.
- Low: few or no tests, a new pattern, or behaviour that only shows at run
  time.

## Scoring rule

1. Score Risk (L1, L2 or L3).
2. Score Change (L1, L2 or L3).
3. Score Confidence (High, Medium or Low).
4. Base tier is the higher of Risk and Change.
5. Demotion: if Confidence is High and the base tier is L2 or L3, lower the
   tier by one. Medium and Low never demote.
6. Floor: the tier is never lower than Risk.

Risk floors the tier, Change can push it up, and Confidence can pull it down
by one, never below Risk. When the scores are uncertain, propose L2; an item
earns L1, it is not the default.

Examples:

- Fix a typo in a skill's reference: Risk L1, Change L1, Confidence High.
  Tier L1.
- Refactor an internal CLI across 12 files with full tests: Risk L1, Change
  L2, Confidence High. Base L2, demoted to L1.
- Revise a skill used across several harnesses, with scenario checks only:
  Risk L1, Change L2, Confidence Medium. Tier L2.
- One-line change to a deployed permission rule: Risk L3, Change L1,
  Confidence High. Tier L3 (Risk floors; no demotion below it).
- Large refactor across three services with sparse tests: Risk L2, Change
  L3, Confidence Low. Tier L3.

## Proposing and recording the tier

The agent scores the item after the light grilling round and scouting, and
before any planning document. It proposes the tier with one reason per
dimension at CP1 Kickoff (workflow.md, HITL Checkpoints), and the user
confirms or changes it there. The agent never settles the
tier alone. Anyone may raise a tier; lowering a confirmed tier needs the
user's agreement.

IDEA.md records the confirmed tier in two places:

- the front-matter field `complexity`, exactly `L1`, `L2` or `L3`;
- a Complexity section with the three scores, the base tier and any
  demotion, for example: "L2. Risk L1: internal, reversible. Change L2: ten
  files in one skill, used by several harnesses. Confidence Medium:
  scenario checks only. Base L2; no demotion."

Re-score when discovery, the design or the test coverage changes materially.
When the tier rises, promote the documents as documents.md describes and keep
every AC and task ID. Items without the `complexity` field are untiered and
follow the rules that predate tiers.

## What each tier means in GSD

Every tier has the same three HITL Checkpoints - CP1 Kickoff, CP2
Pre-implementation and CP3 Review - and the same commits (workflow.md, HITL
Checkpoints and Commits). The tier changes what is written, reviewed and
verified between them.

### L1

- Documents: IDEA.md only, with Goal, Success (AC-NN), Tests, TODO (T-NN)
  and Topology sections. No diagram; an L1 item that needs one is probably
  not L1.
- Discovery: light grilling, then scouting. Kickoff offers deeper grilling.
- Pre-implementation review: of the completed IDEA.md and any other records,
  a default step; skipped only on an explicit waiver.
- Approval: IDEA.md for planning at Kickoff, then the completed IDEA.md with
  its topology at CP2.
- Verification: an automated test for each acceptance criterion.
- Close-out: checkpoint commit, simplification, counter-review and fixes,
  each committed, then final checks. The user accepts a short review package
  at CP3 before FINAL.md.

### L2

- Documents: IDEA.md, PLAN.md and TODO.md. PLAN.md holds the Diagrams,
  Acceptance, Verification and Topology sections. SPEC.md and other records
  are added when the work needs them.
- Diagrams: a context diagram and one flow diagram from entry to exit.
- Discovery: light grilling, then scouting. Kickoff offers deeper grilling.
- Pre-implementation review: of the whole planning set, a default step;
  skipped only on an explicit waiver.
- Approval: IDEA.md for planning at Kickoff, then PLAN.md and TODO.md with
  the topology and verification plan at CP2.
- Verification: an automated test and an end-to-end method for each
  criterion, in the layers the verification plan names.
- Close-out: checkpoint commit, simplification, counter-review and fixes,
  each committed, then verification and final checks. The user accepts a
  review package at CP3 before FINAL.md.

### L3

- Documents: IDEA.md, PLAN.md, SPEC.md and TODO.md, plus the other records
  as they arise.
- Diagrams: the L2 diagrams, a layer diagram, and one flow per main path,
  including failure and rollback paths.
- Discovery: light grilling, scouting, then full grilling inside Kickoff.
- Pre-implementation review: of the whole planning set - PLAN.md, SPEC.md
  and TODO.md written together - a default step; skipped only on an
  explicit waiver.
- Approval: IDEA.md for planning at Kickoff, then PLAN.md, SPEC.md and
  TODO.md together with the topology and verification plan at CP2.
- Verification: an automated test and an end-to-end method for each
  criterion, in the layers the verification plan names.
- Smoke review: optional, at one slice the PLAN marks; a hard checkpoint
  where the agent commits the slice and waits for the user's early review.
- Close-out: checkpoint commit, simplification, counter-review and fixes,
  each committed, then verification and final checks. The user accepts a
  review package at CP3 before FINAL.md.
