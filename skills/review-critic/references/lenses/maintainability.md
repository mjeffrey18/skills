### Lens: maintainability

For code whose shape will cost the next change. A baseline of well-known code
smells, applied with two rules: a documented repo standard always wins - where
the repo endorses something below, do not report it - and every smell is a
judgement call, never a hard violation, so none is above medium. Skip anything
tooling already enforces. Attack:

- **Names that mislead** - a function, variable or type whose name does not say
  what it does or holds. If no honest name comes easily, the design is murky.
- **Duplication** - the same logic shape in more than one hunk or file of the
  change.
- **Misplaced behaviour** - a function that works mostly on another object's
  data (it belongs there), or a class that only forwards calls onward.
- **Types waiting to exist** - the same few fields or parameters travelling
  together, or a primitive or string standing in for a domain concept.
- **Scattered change** - one logical change forcing edits across many files,
  or one file edited for several unrelated reasons.
- **Repeated branching** - the same switch or if-cascade on the same type in
  several places.
- **Speculative generality** - parameters, hooks or abstraction for needs the
  spec does not have.
- **Reaching through** - long chains navigating other objects' internals that
  the caller should not depend on.
- **Rejected inheritance** - a subclass that ignores or overrides most of what
  it inherits.
- **Inconsistent with project patterns** - the change does a job another way
  than the repository already does it elsewhere (error handling, config,
  logging, data access, test style). Name the established example. Not a
  finding when the plan records why it departs.

Name the smell, quote the hunk, and say what the next change will cost. Medium:
a smell likely to cause a bug or a costly next change. Low: the rest.
