### Lens: security

For auth, permissions, input handling, secrets, crypto and outbound calls.
Start by naming the trust boundaries the change crosses. Attack:

- **Authorisation** - every new or changed entry point checks who may act on
  _this_ record, not just that someone is signed in (IDOR); admin-only paths
  stay admin-only; checks cannot be skipped by a different route or verb.
- **Bypass branches** - blanket role or legacy fallbacks in policies and
  scopes, a read permission used to gate a write, an alternate format or
  export branch left unchecked, a GET that writes, and a "trusted" flag the
  client can set.
- **Normalise like the consumer** - a guard must see input the way the tool
  that uses it will: expanded paths, symlinks, wrappers (`env`, `sh -c`,
  command substitution), line continuations and other encodings. Input the
  guard cannot parse or decode fails closed.
- **Privilege crossing** - a more privileged process that reads or writes
  paths, hooks or config a less-trusted user or agent controls.
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
- **Data exposure** - PII in logs or analytics, over-broad API responses;
  customer data or real identifiers in committed docs, plans, fixtures or
  published artefacts.
- **Dependencies** - new packages: maintained, pinned, needed?

High: any exploitable path or leaked secret. Medium: a missing check with a
plausible attacker. Name the attacker and the step they take.
