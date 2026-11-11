# Resume checklist

Work through this before acting on a handoff. How far you go depends on the
staleness level from `handoff.py status`: FRESH needs a quick check, VERY_STALE
needs re-exploration.

## Verify the ground

- Read the whole handoff, and its predecessor if the newest one leaves a gap.
- Confirm the repository and branch match, or understand why they differ.
- Run `git status` and `git log --oneline <handoff commit>..HEAD` to see what
  changed since the handoff was written.
- For a GSD item, read IDEA.md and DECISIONS.md: they override the handoff where
  the two disagree.

## Check the context still holds

- Are the listed blockers resolved? Are the assumptions still true?
- Do the critical files still exist and look as described?
- Are the services, processes or environment variables it names available?

## Stop and ask when

- Referenced files are missing or the architecture has visibly changed.
- The branch has diverged substantially or the recorded commit is not in history.
- A blocker marked unresolved is still blocking and needs the user.
- The handoff and the GSD documents disagree about scope.

## Then

- Start with Immediate next steps item 1.
- Apply the gotchas and failed approaches it records rather than rediscovering them.
- When you hand off again, create a new handoff so the chain continues.
