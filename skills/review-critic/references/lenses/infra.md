### Lens: infra

For infrastructure as code, cloud and database grants, container images,
service units, provisioning and deploy scripts, and shell. Assume it will run
more than once, against a machine that has drifted. Attack:

- **Least privilege** - roles, grants and policies give exactly the stated
  scope: no wildcard resources or secrets, no "all tables" or default
  privileges on future objects, no flags that bypass row or object security.
- **Network trust** - access allowed by source address, where a load
  balancer, NAT, proxy or loopback connection lets anyone through; services
  bound wider than needed.
- **Provider scope** - global services, service-linked roles and replication
  paths that a regional or account guardrail does not cover; retention that
  versioning or backups silently extend.
- **Converge on re-run** - running the script twice reaches the intended
  state. "Create if not exists" does not repair drift; replacing an object can
  detach what depended on it; a re-run must not lock the operator out.
- **Runtime parity** - the image, user and uid, writable paths, environment
  variables, installed packages and names used across repositories match
  what the deploy target actually loads.
- **Privilege crossing** - a root or other-user process that reads or writes
  paths, hooks or config a less-trusted user or agent can change.
- **Shell semantics** - unquoted or raw interpolation, `pipefail` with a
  reader that exits early, prefix matching on names and devices, numbers with
  leading zeros, relative paths, and a "check" mode that writes.
- **Teardown** - resources created per run (preview environments, keys,
  buckets) are removed on every exit path, keyed by an id that is stable.

High: access wider than stated, a secret reachable by the wrong principal, or
a re-run that breaks a working system. Medium: drift a re-run leaves behind,
or a runtime mismatch that stops the first deploy.
