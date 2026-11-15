### Lens: evals

For eval suites, graders, scorers, judges and the gates built on their
results. A grader is a test oracle for open-ended output: it is wrong when it
fails a correct answer or passes a wrong one. Attack:

- **False pass and false fail** - for each check, write one correct answer it
  rejects and one wrong answer it accepts. Run them against the grader; do not
  argue from reading the pattern.
- **Earlier examples still hold** - a grader fix must keep every earlier
  correct and wrong example grading the same way. Name one that now flips.
- **Facts tied to their subject** - a figure or claim must bind to its own
  entity, period, unit and metric. Attack swapped subjects, a second entity
  between subject and value, and labels that only sit near the value.
- **Negation and scope** - a refusal, hedge or "not" must not hide a claim in
  a later clause ("..., though", "except"), and a negated phrase must not
  match as a positive one.
- **Periods, units and bases** - wrong year, partial ranges read as whole
  periods, percentages read as counts, per-item read as per-group, averages
  read as totals, amounts in different currencies combined.
- **Verdict integrity** - missing or failed runs dropping out of the
  denominator, dev and held-out cases sharing facts, controls that cannot
  fail by construction, gates that pass when an arm or a sample is missing.
- **What the judge never sees** - a second-pass judge or adjudicator that only
  reviews failures can never catch a false pass.
- **Cost and determinism** - paid runs without a cap or a dry run; scores
  compared across runs with different models, seeds, prompts or case sets.

Report one class of wording gap once, with its root cause - not every
phrasing that hits it. High: a false pass on the behaviour the suite exists to
protect, or a gate that passes without its evidence. Medium: a false fail on
a correct answer, or a check that drifted from earlier examples.
