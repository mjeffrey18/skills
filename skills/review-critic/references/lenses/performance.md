### Lens: performance

For hot paths, data access, caching and batch work. A performance finding must
name the growth dimension (rows, users, items, payload) and what happens as it
grows - no speculative micro-optimisation. Attack:

- **Queries** - a query per item in a loop (N+1), missing index for a new
  filter or sort, `SELECT *` on wide tables, counts on large tables.
- **Unbounded work** - no pagination or limit, loading every row into memory,
  recursion or loops whose size comes from input.
- **Complexity** - nested loops over growing collections, repeated linear
  searches that should be a hash lookup, sorting inside loops.
- **Blocking** - synchronous network or disk I/O in a request path, locks held
  across I/O, work that belongs in a background job.
- **Caching** - no cache where the same expensive result is rebuilt, or a
  cache with a wrong key, no invalidation, or unbounded growth.
- **Payloads** - large responses, over-fetching, images or bundles shipped
  uncompressed or unused.
- **Retries and timeouts** - missing timeouts; retries without backoff that
  multiply load during an outage.
- **Regex** - patterns open to catastrophic backtracking on input.

High: an outage or timeout path at realistic scale. Medium: a clear
degradation as data grows. Low: measurable but minor.
