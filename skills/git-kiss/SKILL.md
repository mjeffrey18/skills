---
name: git-kiss
description: >
  Reference for git-kiss (`gk`) — a rebase-based git workflow CLI. Use this skill
  whenever the user is working in a project that has a `.gitkiss.jsonc` config, asks
  about `gk` commands, wants to start/finish/squash/rebase a feature branch, deploy to
  staging or production with `gk ds`/`gk dp`, manage worktrees with `gk wt`, configure
  git-kiss, or migrate a legacy `.gitkiss` file. Trigger on any mention of `gk`, `git-kiss`,
  `gk nf`, `gk ff`, `gk wt`, `gk dp`, `gk rf`, `.gitkiss`, or "feature branch workflow".
  Also trigger when the user asks how to start a branch, merge a feature, or set up
  worktrees in a project that uses git-kiss.
---

# git-kiss (`gk`) Reference

git-kiss wraps common git operations into short commands for clean, rebase-based workflows.
Almost everything uses **rebase** to keep history linear. The one exception is `gk ff`,
which uses `--no-ff` merge so feature integration points are visible in history.

## Commands at a glance

| Command                      | What it does                                          |
| ---------------------------- | ----------------------------------------------------- |
| `gk nf {name}`               | New feature branch from base branch                   |
| `gk rf [--remote]`           | Rebase onto local base, or fetch and use origin/base |
| `gk cm "{msg}"`              | Stage all (`git add -A`) and commit                   |
| `gk rc` / `gk rc!`           | Safely undo the last commit, keeping changes unstaged |
| `gk pf`                      | Publish feature branch to remote                      |
| `gk pr "{title}" [gh flags]` | Create pull request via `gh` CLI                      |
| `gk pr ls`                  | List pull requests for local branches and worktrees |
| `gk sf` / `gk sf!`           | Squash all feature commits into one                   |
| `gk ff` / `gk ff!`           | Finish feature — merge into base (`--no-ff`)          |
| `gk ds` / `gk ds!`           | Deploy feature to staging (force push)                |
| `gk dp` / `gk dp!`           | Deploy develop → main, tag a semver release           |
| `gk wt {cmd}`                | Manage git worktrees (see Worktrees section)          |
| `gk init`                    | Interactively create config in a chosen scope         |
| `gk migrate`                 | Convert legacy shell `.gitkiss` to JSONC              |
| `gk shell-init`              | Print shell integration for `gk wt co`                |
| `gk version`                 | Print the installed version                           |
| `gk help`                    | Show all commands                                     |

### `!` suffix = skip confirmation, auto-push

Any command with `!` runs without prompts. Use in scripts or when you're confident:

```bash
gk ff!    # merge + push + delete branch, no prompt
gk sf!    # squash, no prompt
gk ds!    # force-push to staging, no prompt
gk dp!    # tag + push to production, no prompt
gk wt rm! 1   # remove worktree, discard dirty files, delete its merged branch
gk wt clean!  # remove merged worktrees, no prompt
```

### Rebase from the local base or origin

`gk rf` checks out the local base, pulls with rebase, returns to the feature
branch and rebases onto the updated local base. If checkout or pull fails,
it reports the failed stage and offers to fetch and rebase onto `origin/<base>`
instead. The prompt defaults to no; EOF also declines. A pull conflict stops
with recovery instructions. Resolve or abort any unfinished Git operation
before trying another rebase.

`gk rf --remote` fetches the configured base explicitly from origin and rebases
onto its refreshed remote-tracking reference. It stays on the current branch
and leaves the local base untouched. Fetch failure stops the command.
Remote rebasing excludes local, unpushed base commits; `gk ff` still updates
the local base and refuses to merge a feature that is behind it.

### Parking a destination worktree

`gk ff`, `gk ds` and `gk dp` can release a destination branch held by another
worktree. They show the owning path and offer to switch that worktree onto a
new `park/<worktree-name>` branch at its current commit. Their `!` forms park
automatically. `repo--task` becomes `park/task`; the canonical main worktree
uses its directory basename.

Dirty worktrees, unfinished Git operations, invalid park names and existing
park branches stop parking. The command then checks out and pulls the local
destination before merging or deploying. The other worktree remains parked,
including if a later step fails. No automatic parking occurs during `gk rf`
or new-branch creation.

---

## Two flows

### Simple flow

`develop_branch` is empty (`""`). Feature branches come off `main`; `gk ff` merges back into `main`.

```
main  ←─(--no-ff merge)─  feature/*
```

### Full flow

`develop_branch` is set (e.g. `"develop"`). Features branch off `develop`; staging is tested
via `gk ds`; `gk dp` rebases develop onto main and tags a release.

```
main  ←─(rebase + semver tag)─  develop  ←─(--no-ff merge)─  feature/*
                                     ↑
                                 staging  (rebased from feature for QA)
```

**Base branch rule:** `gk` targets `develop` when it's configured, `main` otherwise.
Most commands operate against this base — not necessarily `main` directly.

---

## Configuration

Configuration is resolved from built-in defaults and four cascading JSONC files. Each later
layer overrides keys set by earlier layers:

| File                   | Scope                         | Commit?           |
| ---------------------- | ----------------------------- | ----------------- |
| `~/.gk/.gitkiss.jsonc` | Global defaults for all repos | n/a (personal)    |
| `~/.gk/projects.jsonc` | Per-project personal defaults | n/a (managed)     |
| `.gitkiss.jsonc`       | Per-repo team config          | Yes — commit this |
| `.gitkiss.local.jsonc` | Per-repo personal overrides   | No — gitignored   |

Project-store entries use the canonical main-worktree path, so linked worktrees share
personal defaults. `gk init` can create global, project-store, shared, or local configuration.
Do not manually edit the machine-managed project store while git-kiss is running. A legacy
`~/.git-kiss.jsonc` is migrated to `~/.gk/.gitkiss.jsonc` on a normal command when there is no
destination collision.

### All keys

```jsonc
// .gitkiss.jsonc — commit this to share with the team
{
  // production branch (default: "main")
  "main_branch": "main",
  // integration branch; "" for simple flow
  "develop_branch": "develop",
  // staging branch; "" if unused
  "staging_branch": "staging",
  // prefix added to new feature branch names
  "feature_prefix": "feature/",
  // auto-increment semver tags on gk dp
  "use_tags": true,
}
```

```jsonc
// .gitkiss.local.jsonc — gitignored, personal only
{
  // prepended to branch names: feature/mj-{name}
  "initials": "mj",
  // files copied into each new worktree
  "worktree_copy": [".env*", "config/local"],
}
```

**Comment rules:** `//` comments must be on their own line. Inline and `/* */` comments
are not supported. A malformed layer is skipped with a warning — the other layers still apply.

**Cascade for `worktree_copy`:** an explicit `[]` in a later layer clears the earlier
value. Absent key = inherit from earlier layer unchanged.

**Worktree config fallback:** when `cd`-ed into a worktree that has no config of its own,
git-kiss automatically reads shared and local configuration from the canonical main worktree.

---

## Worktrees (`gk wt`)

Each worktree is a sibling directory named `{repo}--{name}`:

```
~/projects/my-repo/              ← main worktree
~/projects/my-repo--mj-login/   ← gk wt nf login
~/projects/my-repo--hotfix-db/  ← gk wt nb hotfix-db
```

All other `gk` commands (`cm`, `rf`, `pf`, `pr`, etc.) work inside worktrees — just
`cd` into one and use `gk` as normal.

### Worktree commands

| Command                   | What it does                                                       |
| ------------------------- | ------------------------------------------------------------------ |
| `gk wt nf {name}`         | New worktree + feature branch (`feature/{initials}-{name}`)        |
| `gk wt nb {name}`         | New worktree + plain branch (no prefix/initials)                   |
| `gk wt ls`                | List all worktrees with branch, path, ahead/behind, dirty state    |
| `gk wt co [index]`        | Select, or directly choose a displayed index (needs shell-init)    |
| `gk wt copy [index\|name]` | Preview and copy configured files from another worktree into the current one |
| `gk wt rm <index\|name>`  | Remove worktree, keep branch; prompts if dirty |
| `gk wt rm! <index\|name>` | Remove worktree without the dirty-tree prompt; delete its merged branch |
| `gk wt clean` / `clean!`  | Remove merged worktrees; `clean!` also removes dirty ones          |

### Removing a worktree

`gk wt rm <index|name>` keeps the branch, even when merged. It asks before
removing a dirty worktree. `gk wt rm! <index|name>` skips that prompt and can
discard uncommitted files. After verified removal, it deletes the branch only
if merged into the configured local base and Git's safe branch-deletion check
passes. Unmerged branches remain. Neither form removes the canonical main
worktree. `gk wt clean` retains its existing merged-worktree cleanup behaviour.

### Reading `gk wt ls` output

```
  #    Branch                   Path                               Status
● 0    main                     ~/projects/my-repo
  1    feature/mj-login         ~/projects/my-repo--mj-login       3↑ 1↓
  2    feature/mj-signup        ~/projects/my-repo--mj-signup      2↑ *
```

- `●` = current worktree
- `*` = dirty working tree
- `↑` / `↓` = commits ahead / behind base branch on origin

### File seeding into new worktrees

When a worktree is created, git-kiss copies files from the canonical main worktree. An
existing `.worktreeinclude` is authoritative; otherwise it falls back to `worktree_copy`:

1. `.worktreeinclude` in the canonical main worktree - `.gitignore`-style (one glob per line,
   `#` comments, blank lines ignored)
2. `worktree_copy` array in effective config (globs supported, e.g. `".env*"`) when no
   include file exists

An empty or comment-only include file intentionally copies nothing. Patterns are project-root
relative; absolute paths and `.` / `..` components are rejected. Relative symlinks
are preserved only when their targets remain inside the project and are also
copied. Absolute, broken, escaping and partially copied symlinks are refused.
Use this for gitignored files each worktree needs (`.env`, local credentials, etc.).

### Refreshing files in an existing worktree

`gk wt copy [index|name]` uses the selected worktree as the source and the
current worktree as the destination. An omitted selector shows a worktree
table and asks for one. It displays the rules, previews matched files and asks
before copying. Matching files are overwritten; directories are merged and
destination-only files remain. Progress lists copied files.

Rules come from the current destination's `.worktreeinclude` when present,
otherwise its effective `worktree_copy` configuration. An empty include file
copies nothing. This differs from worktree creation, which uses the canonical
main worktree's include file. Unsafe paths, Git metadata, destination symlinks,
file/directory conflicts and copying into the source worktree are refused.

### Shell integration for `gk wt co`

A subprocess can't change the parent shell's directory, so without shell integration
`gk wt co` prints the path but doesn't navigate there. Add to `~/.bashrc` or `~/.zshrc`:

```bash
eval "$(gk shell-init)"
```

Or a manual alias if you prefer not to wrap `gk`:

```bash
alias wtco='cd $(gk wt co)'
```

---

## Common workflows

### Simple flow — start to finish

```bash
gk nf my-feature        # branch: feature/mj-my-feature from main
# ... edit, test ...
gk cm "add my feature"
gk pf                   # push to remote
gk rf                   # rebase if main has moved
gk ff!                  # merge into main, push, delete branch
```

### Full flow — feature through to production

```bash
gk nf my-feature        # branch: feature/mj-my-feature from develop
gk cm "wip"
gk pf
gk ds!                  # rebase feature onto staging for QA
gk rf                   # rebase onto latest develop before merging
gk ff!                  # merge into develop
gk dp!                  # rebase develop → main, tag v1.x.x, push
```

### Parallel work with worktrees

```bash
gk wt nf task1          # creates repo--task1/ with feature/mj-task1
gk wt nf task2          # creates repo--task2/ with feature/mj-task2
gk wt ls                # see status of all worktrees
cd ~/projects/repo--task1 && gk cm "done" && gk ff!
gk wt clean!            # remove merged worktrees
```

### First-time setup in a new repo

```bash
gk init                 # interactive: choose scope and flow, enter initials
# Optionally edit .gitkiss.local.jsonc to add worktree_copy
git add .gitkiss.jsonc && git commit -m "chore: add git-kiss config"
```

### Migrating a legacy config

```bash
gk migrate              # converts ~/.git-kiss and/or .gitkiss to JSONC
# Backup is saved as .bak; review output, delete .bak when satisfied
git add .gitkiss.jsonc && git commit -m "chore: migrate git-kiss config to JSONC"
```

---

## Requirements

- `git` — required
- `jq` — required for config parsing (`brew install jq` / `apt install jq`)
- `gh` — only needed for `gk pr` ([cli.github.com](https://cli.github.com))

## Debugging

```bash
GK_DEBUG=1 gk {command}   # verbose config loading, version check, and command trace
```

## Updating

```bash
curl -fsSL https://raw.githubusercontent.com/mjeffrey18/git-kiss/main/install.sh | bash
```

Version is checked automatically once per day after each command and prints a notice
if a newer release is available.

Set `GK_NO_VERSION_CHECK=1` to disable this non-blocking check, for example in CI or an
air-gapped environment.
