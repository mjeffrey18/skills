### Lens: ruby

For Ruby code outside Rails specifics (pair with `rails` in a Rails app).
Attack:

- **nil** - `&.` and `try` hiding a value that should never be nil; methods
  returning nil on a path the caller treats as a value; `||=` memoising `false`
  or `nil` and recomputing every time.
- **Exceptions** - `rescue => e` or `rescue StandardError` swallowing errors,
  `rescue Exception`, retries without a limit, `ensure` blocks that raise.
- **Mutation** - mutating arguments, frozen string literals mutated, shared
  mutable defaults (`Hash.new([])`, constants holding arrays or hashes).
- **Numbers and money** - floats for money, integer division truncating,
  `BigDecimal` mixed with floats, rounding mode.
- **Time** - `Time.now` or `Date.today` ignoring the app's time zone; parsing
  without a zone.
- **Metaprogramming** - `method_missing` without `respond_to_missing?`,
  `send` with input-controlled names, monkey patches on core classes.
- **Concurrency** - class-level instance variables or memoisation shared
  across threads, non-thread-safe globals.
- **Keyword and splat arguments** - changed keyword defaults, `**opts`
  swallowing typos.

High: data corruption or a swallowed failure. Medium: a nil or type path with a
realistic trigger. Skip what RuboCop enforces.
