---
name: rebase
description: Run or finish a git rebase in place and resolve its conflicts, including encrypted files (any .enc file, git-crypt, sops, vault). Use when the user wants a branch rebased (onto main or its upstream), asks to fix rebase conflicts, or is stuck mid-rebase ("continue the rebase", "rebase in progress").
---

# Rebase

Resolve the rebase **in place**: the working tree the user is in is the rebase, so there is no worktree, scratch branch or clone. Any command that discards a commit, the rebase, or one side of an encrypted file runs only on the user's say-so.

## 1. Find the rebase state

```bash
git status
cat "$(git rev-parse --git-path rebase-merge)/onto"   # the new base - note the hash, the file disappears when the rebase ends
```

`<onto>` below is that hash; `REBASE_HEAD` is the commit being replayed. If no rebase is running, ask the user one question with your recommended defaults first: which branch to rebase (default: the current one), onto what (default: its upstream or the main branch), and whether to autostash uncommitted changes. Then run `git rebase [--autostash] <onto> [<branch>]`.

Done: a rebase is in progress and you know the branch, the base and the commit in flight.

## 2. List and classify the conflicts

```bash
git diff --name-only --diff-filter=U
```

A path is **plain** only when no filter, diff or merge attribute applies to it and both sides are readable text with no encryption marker; everything else, and any path whose name marks it as a secret (`.enc` and friends), is **encrypted**. The check and the marker table are in [`references/encrypted-files.md`](references/encrypted-files.md). When in doubt, treat it as encrypted - a wrong automatic merge of a secret costs more than one extra question.

Done: every conflicted path is in exactly one of the two lists.

## 3. Resolve plain files yourself

For each plain file:

```bash
git diff -- <path>                                   # the conflict hunks, both sides
git show REBASE_HEAD -- <path>                       # what the user's commit changed
git log --oneline REBASE_HEAD~1..<onto> -- <path>    # what upstream changed that the commit never saw
```

Keep both intents where they do not collide. Where they do, prefer the reading that matches the commit message of REBASE_HEAD and say so in the report. If one side deleted the file (`git ls-files -u -- <path>` lacks stage 2 or 3), keep it unless upstream removed it and the user's commit did not depend on it; flag the decision either way.

```bash
! grep -nE '^(<{7}|={7}|>{7})' <path> && git add <path>
```

Done: every plain file is staged with no markers left.

## 4. Hand encrypted files to the user

Read only stage headers and commit metadata for these files; a decrypted worktree copy is still a secret. Build one question that shows, per file, both sides in plain language - in a rebase `--ours` is the new base and `--theirs` is the user's own commit, so say "upstream" and "your commit", never ours/theirs:

- **Upstream version** - `git log -1 --format='%h %s (%an, %ad)' <onto> -- <path>`
- **Your commit's version** - `git log -1 --format='%h %s (%an, %ad)' REBASE_HEAD -- <path>`
- **Resolve by hand** - stop and let the user decrypt, merge and re-encrypt themselves, then continue when they say so

Apply the answer, then confirm the staged blob is exactly the chosen side (read the stage hash first - staging collapses the stages):

```bash
WANT=$(git rev-parse :2:<path>)   # upstream version; :3: for your commit's version
git checkout --ours -- <path>     # --theirs for your commit's version
git add <path> && test "$(git rev-parse :0:<path>)" = "$WANT"
git rm -- <path>                  # instead, when the chosen side deleted it (that stage is missing in git ls-files -u)
```

Done: every encrypted file is staged exactly as the user chose.

## 5. Continue and loop

```bash
GIT_EDITOR=true git rebase --continue
```

New conflicts: back to step 2. If it fails without new conflicts, read git's message and decide with the user before any command that drops a commit:

- **"No changes - did you forget to use 'git add'?"** with `git diff --cached --quiet` succeeding means upstream already has this commit; ask before `git rebase --skip`. Otherwise something is still unstaged - fix that.
- **Autostash pop conflicts** at the end: the rebase itself is complete and the stash is still in `git stash list`; report the files.

Done: `git status` shows no rebase in progress.

## 6. Verify and report

```bash
git range-diff <onto> ORIG_HEAD HEAD   # ORIG_HEAD is the pre-rebase tip; only your resolutions should differ
```

Run the project's checks if it has them. Report each conflicted file and how it was resolved, every encrypted-file decision the user made, and the undo command `git reset --hard ORIG_HEAD`.

Done: range-diff shows only the resolutions you made, checks pass or the failures are listed, report delivered.
