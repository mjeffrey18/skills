### Lens: data-pipeline

For analytics SQL, transformation models, ETL and ELT jobs, replication and
change-data capture, reports and dashboards. The question is whether the
numbers are right, every run. Attack:

- **Incremental boundaries** - a watermark taken from rows already written
  after a partial run; late or out-of-window rows skipped for good; schema,
  key or logic changes that need a full rebuild but do not get one.
- **Deterministic results** - window functions and "latest row" picks
  ordered by a non-unique key; ties broken at random; results that depend on
  row order or the engine's NULL handling.
- **Grain and double counting** - joins that fan out rows, records counted in
  two periods, totals summed across a grain that already includes them.
- **Periods and units** - future or partial periods treated as complete,
  calendar against rolling windows, time zone of the period boundary, tax or
  fees included on one side of a comparison and not the other, amounts in
  different currencies combined.
- **Reconciliation that cancels out** - parity checks on counts or sums where
  missing and extra rows offset each other; compare key by key.
- **Leaks into artefacts** - keys, secrets and personal data copied into
  build caches, compiled output, temp tables, exports or logs; redaction that
  nested or escaped values get past.
- **Freshness and failure** - a step that ignores the exit code of the one
  before it, or a stale source that still yields a confident number.

High: a wrong number that a person will act on, or a leak of personal data or
keys. Medium: a result that drifts under a realistic condition (late rows, a
tie, a period edge).
