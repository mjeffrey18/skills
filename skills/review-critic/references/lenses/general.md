### Lens: general

The fallback for any code change. Attack:

- **Behaviour against intent** - does the code do what the intent or spec says,
  for every case it names? Anything it does that nobody asked for?
- **Edge inputs** - empty, nil/null/undefined, zero, negative, very large,
  duplicate, unicode and whitespace, off-by-one at every boundary.
- **Error paths** - errors swallowed, logged and ignored, or turned into a wrong
  default; retries that repeat side effects; cleanup skipped on failure.
- **State and ordering** - shared or global state, caching that goes stale,
  order-dependent logic, re-entrancy, concurrent callers.
- **Bind to what was checked** - an action that runs on what was approved,
  validated or locked must use that exact version (a commit SHA, a record
  version, a resolved path), not a moving name (HEAD, a branch, "latest") read
  again later; checks made before the lock is taken.
- **Interrupted runs** - kill the operation at each step: does the next run
  finish the job, or refuse, duplicate or corrupt it? Partial results
  reported as success.
- **One bad record** - a malformed, unreadable or unexpected entry must not
  abort the whole scan or batch, nor be silently skipped.
- **Contracts** - changed signatures, return shapes, defaults or exceptions
  that existing callers depend on; config or environment assumptions.
- **Inherited side effects** - when a call moves onto a shared helper, list
  what the helper also does (events, flags, notifications, error reports,
  failure rules) and check each one is wanted on the new path.
- **Data the tool cannot restore** - deletes, moves or overwrites that touch
  ignored, untracked or generated files, or work not yet saved.
- **Docs against code** - comments, docs, runbooks and records the change
  touches claim no more than the code enforces, and still name things that
  exist.
- **Leftovers** - debug output, commented-out code, TODOs that hide
  unfinished behaviour, dead branches that are now unreachable.

High: wrong result or crash on a plausible input; a caller broken. Medium: an
unhandled edge with a realistic trigger. Skip naming and formatting unless a
name actively misleads.
