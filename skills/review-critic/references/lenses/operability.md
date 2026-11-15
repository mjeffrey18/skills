### Lens: operability

For a build that will run unattended - services, jobs, retries, deploys,
runtime configuration. The question is whether someone on call can see it
fail and undo it. Check the build against what the plan says about running it in
production, when it says anything. Attack:

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
- **Partial success** - a batch or multi-status response with per-item
  errors counted as complete; a sweep whose retry cannot find the items it
  left half done.
- **First run** - what the new job, flag or rule does the first time it runs
  against existing data: how many records it touches, and whether that is
  intended.
- **Resource use** - unbounded queues, caches, file growth or connections.

High: a failure that would go unnoticed in production, or a change that
cannot be rolled back. Medium: a missing signal, timeout or limit with a
plausible trigger.
