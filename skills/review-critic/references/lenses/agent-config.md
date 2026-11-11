### Lens: agent-config

For skills, AGENTS.md/CLAUDE.md, hooks, agent settings, permission rules and
deploy manifests. The "code" here is instructions and configuration that other
agents obey. Attack:

- **Flags and commands** - every CLI flag, command and config key is valid for
  the installed version (check `--help`) and does what the text claims.
- **Permissions** - allow rules, sandboxes and tool lists that grant more than
  stated (inherited settings, prefix rules that admit dangerous arguments,
  tools reachable through extensions or plugins).
- **Recursion and loops** - an agent that can invoke itself or another agent
  that calls back; loops without a hard bound.
- **Secrets** - keys or tokens in committed config, prompts or logs.
- **Billing and model policy** - paths that switch provider, account, API key
  or model away from what the text promises.
- **Contradictions** - two instructions, in one file or across skills, that an
  agent cannot both follow; references to files, sections or names that do
  not exist.
- **Deployment** - manifests that deploy the wrong source, to the wrong place,
  or leave stale copies that still load; name collisions with other skills.
- **Triggering** - descriptions that fire on the wrong requests or collide
  with a neighbouring skill.
- **Untrusted input** - content read from files, tools or the web that the
  instructions would treat as commands.
- **Portability** - harness-specific mechanics presented as universal.

High: a permission, billing or recursion hole, or a leaked secret. Medium: an
instruction that fails or misleads as written.
