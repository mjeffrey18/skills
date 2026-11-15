### Lens: plan

For a plan, spec or design document under review. Attack:

- **Scope fit** - does it deliver what the document that sets the scope (an
  issue, brief or idea note) asks, no more and no less? Does it respect every recorded
  decision, or quietly reopen one?
- **Reality** - check each assumption against the actual code: the files,
  functions, flags and data it relies on exist and behave as the plan says.
- **Order and dependencies** - steps that depend on later steps, missing
  migrations or data moves, parallel work that collides on the same files.
- **Irreversible and outward steps** - deploys, deletions, migrations,
  publishing, messages to people: is each gated by an approval and does it
  have a rollback?
- **Verifiability** - can every acceptance criterion be observed and checked?
  What would a false "done" look like?
- **Unknowns** - risks named as solved, spikes skipped, "should just work".
- **Simpler route** - a materially smaller plan reaching the same outcome.
- **Fit and operation** - for a change that will run in production, does the
  plan say how it fits the project's existing patterns and how it will be
  run, and is that true? Check the claimed patterns against the code, and
  that each failure mode has a log or metric that would show it and a
  rollback signal. A section the workflow requires but the plan lacks, or a
  failure mode nobody would see, is medium.

High: a step that cannot work as written, or an ungated irreversible step.
Medium: a missing step or unverifiable criterion. Location is file:section.
