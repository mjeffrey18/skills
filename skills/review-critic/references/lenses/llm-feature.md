### Lens: llm-feature

For product features built on a language model: system prompts, tool
definitions and gating, agent actions on behalf of users, and the code that
parses model output. (Instructions for the coding agents themselves belong to
`agent-config`.) Attack:

- **Consent before writes** - an action that books, pays, sends or deletes
  needs the user's confirmation of the latest, complete terms (every field
  and quantity the write uses). Attack stale or partial confirmations, a
  confirmation from an earlier turn, and an unrelated reply taken as a yes.
- **Model output as input** - values the model produces (ids, quantities,
  dates, amounts) are validated like user input before a tool acts on them:
  fractions, negatives, ids from another account, dates in the past.
- **Authority** - tools act only on records the end user may reach; the
  model's choice of id is never the access check.
- **Prompt and tool agreement** - routing rules, tool descriptions, limits
  and gating agree with each other and with the code. A rule moved into an
  optional or loaded section must stay reachable wherever its tool is
  attached.
- **Untrusted content** - messages, documents and tool results that the
  model reads can carry instructions; they must not unlock tools or change
  who the model acts for.
- **Turn state and ordering** - late webhooks, retries and parallel turns
  must not revive a stale state, answer the wrong turn, or act twice.
- **Empty and failed turns** - blank model replies, tool errors and timeouts
  reach the user as a clear message, and are not retried into a duplicate
  side effect.
- **Signals** - each turn outcome (answered, refused, tool failed, handed to
  a person) emits an event with the context needed to find it later.

High: an action taken without valid consent or authority, or a model value
written unchecked. Medium: a prompt-tool mismatch or a stale-state path with
a realistic trigger.
