### Lens: security

For auth, permissions, input handling, secrets, crypto and outbound calls.
Start by naming the trust boundaries the change crosses. Attack:

- **Authorisation** - every new or changed entry point checks who may act on
  _this_ record, not just that someone is signed in (IDOR); admin-only paths
  stay admin-only; checks cannot be skipped by a different route or verb.
- **Injection** - SQL, shell, template, path, header, LDAP or regex built from
  input; unsafe deserialisation; HTML output without escaping (XSS).
- **Outbound requests** - URLs or hosts from input (SSRF), redirects followed,
  internal addresses reachable.
- **Secrets** - keys, tokens or passwords in code, config, logs, error messages
  or test fixtures; secrets passed on command lines or to child processes.
- **Sessions and tokens** - expiry, rotation, revocation, CSRF on
  state-changing requests, CORS wider than needed.
- **Crypto** - home-made schemes, weak algorithms, predictable randomness,
  timing-unsafe comparison of secrets.
- **Uploads and files** - type and size limits, stored outside web root, path
  traversal in names.
- **Data exposure** - PII in logs or analytics, over-broad API responses.
- **Dependencies** - new packages: maintained, pinned, needed?

High: any exploitable path or leaked secret. Medium: a missing check with a
plausible attacker. Name the attacker and the step they take.
