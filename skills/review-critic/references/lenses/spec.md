### Lens: spec

For any change with a spec, issue, plan or acceptance criteria to check it
against. This is a separate axis from standards: a change can follow every
repo rule and still build the wrong thing, or do exactly what was asked in a
way that breaks the rules. Report spec findings on their own - do not trade
them off against standards findings. Attack:

- **Missing** - requirements the spec asks for that the change does not
  deliver, or delivers only in part. Quote the spec line.
- **Wrong** - requirements that look implemented but behave differently from
  what the spec says, including edge cases and error behaviour it names.
- **Unasked** - behaviour, options or abstractions the spec did not ask for;
  scope creep is a finding even when it works.
- **Acceptance** - each acceptance criterion: can it be observed, and does the
  change actually satisfy it, or only look as if it does?
- **Silent spec changes** - the change quietly redefines a requirement (a
  renamed field, a narrowed input, a new default) without saying so.

Every finding quotes the spec line it rests on. High: a required behaviour is
missing or wrong. Medium: partial delivery, or unasked behaviour with real
cost. If there is no spec, say so in `summary` and use another lens instead.
