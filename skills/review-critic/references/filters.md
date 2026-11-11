# Finding filters

Filters run after verification and before triage. They keep the review on
real problems: a review is worth acting on only for failures that can happen.

1. **Refuted findings** are not acted on. Report each with the verifier's
   evidence.
2. **Unverifiable findings** are shown to the user with the reason. They are
   not fixed as if confirmed; the user decides.
3. **Hypothetical with no call site** - drop an implementation concern whose
   failure needs a caller, input or state that does not exist in the
   repository. For a plan or configuration review, a concrete requirement,
   consumer or proposed execution path counts as the call site, so a missing
   plan step or an unverifiable criterion is kept.
4. **Preference** - drop "I would have done it differently" when the current
   choice is correct and meets the spec and the repository's documented
   rules.
5. **Nits only** - a review whose remaining confirmed findings are all low
   passes; fix them if cheap, never hold the work for them.

Rules 6 to 8 use the review's memory: the item's earlier findings and the
project review rules. Each runs only when its input is in the packet -
`known-findings.json` for rule 6, the base-commit copy of
`.agents/rules/review/REVIEW.md` (`repo-lenses/REVIEW.md`) for rules 7 and 8.
Without them a review runs as before. They run after verification, in this
order, and never reach the reviewer: the brief carries no earlier findings
and no settled entries, so the reviewer is not anchored by them.

A fingerprint match is only a **candidate**. Two different defects can share
a path, a symbol and a rule class, so a match never drops a finding by
itself. Rules 6 to 8 may drop a finding only when the tally says
`suppressible: true` - every confirming verifier gave the same fingerprint
(and, for rule 8, `style: true`) and every expected verifier replied and,
whatever its vote, says `protected: no`. Any disagreement, missing field or
missing reply (fewer distinct replies than `--expect`) keeps the finding, and
the record says why (the tally's `suppression_blocked`).

6. **Repeat** - the fingerprint matches an earlier finding in
   `known-findings.json`. An earlier fix: keep the finding, marked as a
   possible regression of it. An earlier rejection (refuted, rejected or
   accepted without a fix): run the
   [same-failure check](verifier.md#same-failure-mode) against the earlier
   finding's text and rejection reason, and drop the finding as a repeat
   only when every call says yes. An earlier open finding: keep it, and
   link the two.
7. **Settled** - the fingerprint matches a `settled` entry in the
   base-commit rules (its glob matches the path, its symbol is the same or
   `*`, and its rule class is the same): run the same-failure check against
   the entry's rejected claim and lasting reason, and drop the finding only
   when every call says yes, citing the entry's reason and source.
8. **Nitpick cap** - only style or preference findings count: rule class
   `convention` or `docs`, with `style: true` from every verifier. Keep the
   first `nitpick_cap` of them, in the order the reviewer listed them, and
   drop and count the rest. A confirmed behavioural defect - any other
   class, or a verifier saying `style: false` - is never capped, whatever
   its severity. No `nitpick_cap` means no cap.

Never filtered, whatever rules 3, 4, 6, 7 or 8 say: **security, migration,
idempotency and concurrency** findings. A finding is protected when any
verifier's `protected` is not `no` (including `unsure`), when its rule class
is a protected class (`race`, `idempotency`, `migration`, `auth`,
`injection`, `secrets`, `data-exposure`), or when it comes from the
`security` lens. Protected findings go to triage when confirmed, and to the
user when unverifiable.

Report what each filter removed and why, in one line each - nothing is
dropped silently. For rules 6 and 7, the line names the earlier finding or
the settled entry and the same-failure reason; for rule 8, how many were
capped. A finding a rule matched but kept says why in its record too: a
possible regression, a same-failure answer other than yes, protected, or
no verifier agreement.
