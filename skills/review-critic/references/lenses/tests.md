### Lens: tests

For changed or missing tests. The question is not "are there tests" but "would
these tests catch the bug". Attack:

- **Would it fail?** - if the change were reverted or subtly broken, which test
  goes red? A test that passes either way proves nothing.
- **Assertions** - tests that only check "no exception", truthiness, or call
  counts instead of the actual result.
- **Mocks** - mocks that re-implement the logic under test, stub away the
  behaviour that changed, or assert on implementation details.
- **Coverage of the change** - error paths, edge inputs and each branch the
  change added; a regression test for the bug being fixed.
- **Flakiness** - real clocks, sleeps, ordering between tests, shared state,
  network, randomness without a seed.
- **Honesty** - test names that claim more than the test checks; skipped or
  pending tests that hide failures.
- **Tautologies** - a test that asserts what it just set up, compares a value
  with itself, or re-computes the expected value with the code under test.
- **Source reading** - a test that greps or parses the source text instead of
  running the behaviour; it passes while the behaviour is broken.

High: the headline behaviour is untested, or a test passes with the bug
present. Medium: an important branch or error path untested.
