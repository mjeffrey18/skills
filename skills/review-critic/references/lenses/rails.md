### Lens: rails

For Rails apps: models, controllers, jobs, migrations, views. Attack:

- **Queries** - N+1 in views, serializers and loops (`includes`/`preload`
  missing); `where` with string interpolation (SQL injection); `find_each` vs
  `each` on large sets; default scopes changing results.
- **Callbacks** - side effects in `before_*`/`after_save` (emails, jobs, API
  calls) that fire on every save, inside a transaction that may roll back; use
  `after_commit` for external effects.
- **Validation gaps** - `update_all`, `update_column`, `insert_all` and
  `delete_all` skipping validations and callbacks; uniqueness validated
  without a unique index (race).
- **Parameters** - `permit!`, permitting nested or admin-only attributes, mass
  assignment of foreign keys or roles.
- **Authorisation** - records found by id without scoping to the current
  user or account (`current_user.orders.find` vs `Order.find`).
- **Transactions** - multi-record writes without one; network calls inside a
  transaction; `rescue` inside a transaction block hiding a rollback.
- **Jobs** - not idempotent under retry, arguments that are records deleted
  before the job runs, enqueued before the transaction commits.
- **Migrations** - see the `database` lens; in particular locking a large
  table, and deploy order with code that expects the new column.
- **Views** - `html_safe`/`raw` on user content, missing CSRF on custom forms,
  caching keys that omit the user or locale.
- **Time and enums** - `Time.now` vs `Time.current`; reordering or removing
  integer enum values.

High: data leak across accounts, injection, or corrupted writes. Medium: N+1 on
a listed page, a non-idempotent job, a callback side effect on rollback.
