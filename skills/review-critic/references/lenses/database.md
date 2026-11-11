### Lens: database

For migrations, schema changes, raw SQL and data backfills. Assume a large,
busy production table unless the change says otherwise. Attack:

- **Locking** - adding an index without `CONCURRENTLY` (or the engine's
  equivalent), changing a column type, adding `NOT NULL` or a default that
  rewrites the table, long transactions around DDL.
- **Backfills** - one giant `UPDATE` instead of batches; backfill in the same
  migration as the schema change; no way to resume after failure.
- **Deploy order** - code that needs the new column deployed before the
  migration, or old code breaking once a column is removed or renamed; missing
  expand-then-contract steps.
- **Reversibility** - a `down` that cannot restore data, or no rollback plan
  for a destructive change.
- **Integrity** - uniqueness or foreign keys enforced only in application code;
  cascade deletes wider than intended; nullable columns that should not be.
- **Indexes** - new query patterns without a supporting index; redundant
  indexes; index column order not matching the filter.
- **Types and values** - enum or status values reordered or removed, time zone
  handling of timestamps, precision of money columns.
- **Reads after writes** - replicas lagging behind a write the next request
  reads.

High: a production lock or outage, data loss, or an irreversible step without a
plan. Medium: a missing index or constraint with a realistic cost.
