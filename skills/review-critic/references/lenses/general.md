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
- **Contracts** - changed signatures, return shapes, defaults or exceptions
  that existing callers depend on; config or environment assumptions.
- **Leftovers** - debug output, commented-out code, TODOs that hide
  unfinished behaviour, dead branches that are now unreachable.

High: wrong result or crash on a plausible input; a caller broken. Medium: an
unhandled edge with a realistic trigger. Skip naming and formatting unless a
name actively misleads.
