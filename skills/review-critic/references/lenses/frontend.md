### Lens: frontend

For UI code, client state and templates. Attack:

- **Async races** - responses arriving out of order or after unmount; missing
  abort or ignore-stale logic; double submits.
- **State** - derived state stored and drifting from its source; effects with
  missing or wrong dependencies and stale closures; optimistic updates with no
  rollback on failure.
- **States the design forgot** - loading, empty, error, partial data, offline,
  slow network, very long text, many items.
- **Lists and keys** - index keys on reorderable lists, unstable keys causing
  lost input or focus.
- **Accessibility** - inputs without labels, click handlers on non-buttons,
  keyboard traps or unreachable controls, focus not managed on dialogs and
  route changes, colour as the only signal, misused ARIA.
- **XSS** - `dangerouslySetInnerHTML`, `v-html` or template raw output fed by
  user or API content.
- **Rendering cost** - re-rendering large trees on every keystroke, heavy work
  in render, whole-library imports inflating the bundle.
- **Server and client** - hydration mismatches (dates, random ids, locale),
  validation done only on the client.
- **Copy** - hard-coded strings in a localised app; dates and numbers not
  formatted for the locale.

High: data loss, an XSS path, or an unusable flow for keyboard or screen-reader
users. Medium: a race or missing state with a realistic trigger.
