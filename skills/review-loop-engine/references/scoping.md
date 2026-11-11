# Scoping a review

The reviewer sees only what the packet contains. A good scope is exact about
the base, the commits and the paths, and says out loud what is excluded.
Resolve it before the first round; it stays fixed for the whole loop.

## 1. Look before deciding

```sh
git status --porcelain=v1 -uall      # staged, unstaged and untracked files
git log --oneline --decorate -n 20   # recent commits, branch tips
git rev-parse --abbrev-ref HEAD      # current branch
git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null   # default branch, if known
```

Never assume every dirty file or recent commit is part of this work. Other
agents and sessions often share a working tree, a branch, or even one commit.

## 2. Decide what is in scope

Use, in this order:

1. What the user said ("my last 2 commits", "the uncommitted changes", "this
   branch").
2. What this session did: the commits it made and the files it edited.
3. The work item's own record - a GSD TODO.md, FACTS.md or PLAN.md naming
   files and commits.
4. Commit metadata: author, `Co-Authored-By` trailers, agent names in
   messages, branch names.

If these disagree, or the evidence is thin, put the doubt in the manifest and
let the user decide at confirmation.

## 3. Pick the base

Always resolve the base to a SHA, not a branch name, so it cannot move during
the loop.

| Case                               | Base SHA                                           |
| ---------------------------------- | -------------------------------------------------- |
| Uncommitted only                   | `git rev-parse HEAD`                               |
| Last commit (plus any uncommitted) | `git rev-parse HEAD~1`                             |
| Last N commits                     | `git rev-parse HEAD~N`                             |
| Whole branch                       | `git merge-base <default-branch> HEAD`             |
| First commit in the repo           | the empty tree, `git hash-object -t tree /dev/null` |
| Commits that are not at the tip    | none - use each commit's own diff (below)          |

If the tree is dirty and the user asked only for committed work, say so and
let them choose whether the uncommitted changes are in scope.

## 4. Build `scope.diff`

You build the diff; the reviewer only reads it. Write every part to
`<packet>/scope.diff`.

Add `--no-color --no-ext-diff --no-textconv --src-prefix=a/ --dst-prefix=b/`
to every `git diff` and `git show` below. User git config can otherwise change
the output - for example `diff.mnemonicPrefix` turns `a/`/`b/` into `c/`/`w/`
or `1/`/`2/`, which a reviewer may flag as a malformed diff - or run an
external diff program. The examples leave the flags out for readability.

**Tracked changes.** Working tree against the base, limited to in-scope paths:

```sh
git diff <base> -- <path> <path> > "$packet/scope.diff"          # commits + uncommitted
git diff <base> HEAD -- <path> <path> > "$packet/scope.diff"     # commits only
```

**Other commits interleaved with yours.**

- File sets do not overlap: the path limit above already excludes them. Name
  the other commits as excluded in the manifest.
- Files overlap: append each of your commits' own diff instead -
  `git show --format='commit %H%n%s' <sha> -- <paths> >> "$packet/scope.diff"` -
  and optionally write the combined `git diff <base> -- <paths>` to
  `context.diff`, labelled context only.

**Uncommitted changes that are not all yours.** Limit by path to your files. If
a single file holds both your hunks and someone else's, the diff cannot
separate them: ask the user at confirmation and record in `scope.md` which
parts are yours (function or line range). Do not stage, stash or `git add -N`
to separate them - that changes the shared index under the other agent.

**Untracked files.** `git diff` does not show them. Append each in-scope one as
a new-file diff (the command exits 1 when there is a difference; that is
normal):

```sh
git diff --no-index /dev/null <file> >> "$packet/scope.diff"
```

**Path lists in zsh.** zsh does not split an unquoted variable into words, so
`git diff <base> -- $paths` passes one path that matches nothing and writes an
empty diff. Write the paths out, or use an array (`paths=(a b); git diff <base>
-- "${paths[@]}"`). The round script refuses an empty `scope.diff` for code
reviews.

**Generated, vendored and lock files.** Exclude them unless they are the point
of the change, with a pathspec such as `':(exclude)package-lock.json'`, and list
what was excluded.

## 5. Take the snapshot

The re-review needs your fixes separately from the original change, and the
report needs the loop's own edits separately from work that already existed.

```sh
snap=$(git stash create); snap=${snap:-$(git rev-parse HEAD)}   # tracked state; touches nothing
mkdir -p "$packet/snapshot"
# copy each in-scope untracked file, keeping its path, into "$packet/snapshot/"
```

`git stash create` records the tracked working tree as a commit without
changing the tree, the index or the stash list. Record `$snap` in `scope.md`,
with the list of untracked files you copied. That list fixes each path's class
for the whole loop: a file untracked at the snapshot stays "untracked" even if
GSD commits it between rounds.

Later, `fixes-<n>.diff` is your changes since the snapshot, for the files you
touched:

```sh
git diff "$snap" -- <tracked files you edited> > "$packet/fixes-2.diff"     # never a file on the untracked list
git diff --no-index "$packet/snapshot/<file>" <file> >> "$packet/fixes-2.diff"   # untracked at the snapshot, committed or not
git diff --no-index /dev/null <new file> >> "$packet/fixes-2.diff"             # files you created
```

Each `fixes-<n>.diff` is cumulative since the snapshot, so the reviewer always
sees the whole of the loop's changes.

## 6. Copy the repo review rules

A repository can extend the review lenses in `.agents/rules/review/` (see
`review-critic`'s [repo lenses](../../review-critic/references/repo-lenses.md)).
Copy them from the base commit, not the working tree, so the change under
review cannot rewrite the rules that judge it:

```sh
git ls-tree -rz <base> -- .agents/rules/review |
while IFS= read -r -d '' line; do
  mode=${line%% *}; sha=${line#* blob }; sha=${sha%%$'\t'*}; file=${line#*$'\t'}
  case "$mode" in
    100644|100755)
      dest="$packet/repo-lenses/${file#.agents/rules/review/}"
      mkdir -p "$(dirname "$dest")"
      git cat-file blob "$sha" > "$dest" ;;
    *) printf '%s %s\n' "$mode" "$file" >> "$packet/repo-lenses-skipped.txt" ;;
  esac
done
```

`-z` keeps unusual file names verbatim instead of quoting them. This writes
each regular file's content as committed at the base. It skips
symlinks (mode `120000`) and submodules, listing them in
`repo-lenses-skipped.txt`: a symlink would read its target as it is now,
outside the base commit. If the base has none, nothing is written. Name any
skipped entry in the manifest. If the in-scope change touches
`.agents/rules/review/`, say so in the manifest.

### Known findings

A caller that keeps earlier findings - GSD writes the item's with
`gsd fingerprints <item> --format json` - may put them in the packet as
`known-findings.json`. Each entry has the finding's id, fingerprints,
`Protected`, lens, disposition, outcome (fixed, rejected or open), problem
text and rejection reason. Only the filters read it, after verification
(`review-critic`'s [filters](../../review-critic/references/filters.md)):
never paste it into a prompt, and do not show it to the brief-writer.
Without it, the repeat filter does not run.

## 7. Check the size

Count the tracked diff (`git diff --shortstat` with the same arguments) and the
untracked files separately. Stop only if both are empty - a change made
entirely of new files is still a change. If the whole is very large (roughly
1,500 changed lines or 40 files), propose splitting it into separate loops by
area and let the user choose at confirmation.

## 8. Plan reviews

For a GSD plan review there is no diff and no size check. Scope is the
documents: PLAN.md (and SPEC.md/TODO.md if present) reviewed against IDEA.md
and DECISIONS.md, plus the repository paths the plan touches, so the reviewer
can check it against the real code. `scope.md` lists them; `scope.diff` is not
needed. For re-review, put the plan's changes since the snapshot in
`fixes-<n>.diff` as above.

## The manifest

Show this to the user, write it to `scope.md`, and paste it into the round 1
prompt:

```markdown
- Repo: <absolute path>
- Base: <sha> - <how it was chosen, e.g. merge-base with main>
- In-scope commits: <sha subject>, ... (or: none - uncommitted only)
- Excluded commits (context only): <sha subject - why>, ...
- Uncommitted changes: included | excluded
- In-scope paths: <paths, or "all changed paths">
- Untracked files (included in scope.diff): <paths>
- Excluded paths: <paths - why>
- Shared files and which parts are ours: <file - function or lines>
- Snapshot: <sha>
- Repo review rules: <packet>/repo-lenses from <base> | none (and whether this change edits them)
- Known findings: <packet>/known-findings.json (N findings, from <caller>) | none - leave this line out of the prompt
- Size: <N tracked files, +A / -D; M untracked files>
- Open scope questions: <anything the user must settle>
```
