### Lens: operability

For a build that will run unattended - services, jobs, retries, deploys,
runtime configuration. The question is whether someone on call can see it
fail and undo it. Check the build against the plan's Fit and operation
section when there is one. Attack:

- **Silent failure** - errors caught and dropped, a job that exits 0 after
  failing, a retry loop that gives up without a trace.
- **Signals** - each failure mode in the plan has a log line or metric that
  would show it, with enough context (ids, counts) to act on; nothing logs
  secrets or personal data.
- **Timeouts and retries** - outbound calls without a timeout; retries
  without a limit, backoff or idempotency; a retry that repeats a side effect.
- **Rollback** - the rollback signal named in the plan is observable, and the
  change can be undone (a feature flag, a revert, a reversible migration).
- **Configuration** - new settings have safe defaults, fail fast when
  missing, and are documented where the service's other settings are.
- **Resource use** - unbounded queues, caches, file growth or connections.

High: a failure that would go unnoticed in production, or a change that
cannot be rolled back. Medium: a missing signal, timeout or limit with a
plausible trigger.
