---
name: git-worktree-remove
description: "Safely remove a git worktree with branch cleanup and safety checks"
---

# Git Worktree Remove

Safely remove a single git worktree with branch cleanup, merge verification, and database branch teardown.

**Core principle:** Safety checks first, then clean removal of worktree + branch + DB resources.

**Part of:** [Worktree Lifecycle Suite](./git-worktree.md) | [`/git-worktree`](./git-worktree.md) | [`/git-worktree-status`](./git-worktree-status.md) | [`/git-worktree-clean`](./git-worktree-clean.md)

## Process

1. **Validate Target**: Identify worktree to remove
2. **Safety Check**: Protect main/develop branches
3. **Check Merge Status**: Warn if branch has unmerged changes
4. **Check Uncommitted Changes**: Warn if worktree has dirty state
5. **Remove Worktree**: `git worktree remove`
6. **Delete Local Branch**: `git branch -d` (or `-D` with confirmation)
7. **Delete Remote Branch**: `git push origin --delete` (with confirmation)
8. **Database Cleanup Reminder**: Suggest DB branch deletion if applicable
9. **Prune References**: `git worktree prune`

## Safety Checks

### Protected Branches

```bash
# Never remove worktrees for these branches (configurable)
PROTECTED_BRANCHES="main master develop staging production"

if echo "$PROTECTED_BRANCHES" | grep -qw "$BRANCH"; then
  echo "BLOCKED: Cannot remove worktree for protected branch '$BRANCH'"
  echo "Protected branches: $PROTECTED_BRANCHES"
  exit 1
fi
```

### Uncommitted Changes

```bash
cd "$WORKTREE_PATH"
if [ -n "$(git status --porcelain)" ]; then
  echo "WARNING: Worktree has uncommitted changes:"
  git status --short
  echo ""
  echo "Options:"
  echo "  1. Commit changes first"
  echo "  2. Force remove (--force)"
  echo "  3. Cancel"
  # Wait for user decision
fi
```

### Merge Status

```bash
# Check if branch is merged into main
MAIN_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')

if git merge-base --is-ancestor "$BRANCH" "$MAIN_BRANCH" 2>/dev/null; then
  echo "Branch '$BRANCH' is merged into $MAIN_BRANCH. Safe to delete."
  MERGED=true
else
  echo "WARNING: Branch '$BRANCH' is NOT merged into $MAIN_BRANCH."
  echo "You may lose work if you delete this branch."
  MERGED=false
fi
```

## Removal Steps

```bash
# 1. Remove the worktree
git worktree remove "$WORKTREE_PATH"
# If dirty state and user confirmed force:
# git worktree remove --force "$WORKTREE_PATH"

# 2. Delete local branch
if [ "$MERGED" = true ]; then
  git branch -d "$BRANCH"
else
  echo "Delete unmerged branch '$BRANCH'? (requires confirmation)"
  # On confirmation:
  git branch -D "$BRANCH"
fi

# 3. Delete remote branch (with confirmation)
if git ls-remote --heads origin "$BRANCH" | grep -q "$BRANCH"; then
  echo "Delete remote branch 'origin/$BRANCH'?"
  # On confirmation:
  git push origin --delete "$BRANCH"
fi

# 4. Prune stale references
git worktree prune
```

## Database Branch Cleanup

**After worktree removal, remind about associated database branches:**

```bash
# Detect database provider (same logic as /git-worktree)
if [ -f ".env" ] && grep -q "neon" ".env"; then
  echo ""
  echo "DB Cleanup: neonctl branches delete $BRANCH_SLUG"
elif [ -f ".pscale.yml" ]; then
  echo ""
  DB_NAME=$(grep 'database:' .pscale.yml | awk '{print $2}')
  echo "DB Cleanup: pscale branch delete $DB_NAME $BRANCH_SLUG"
elif [ -f ".env" ] && grep -q "postgresql" ".env"; then
  echo ""
  echo "DB Cleanup: psql \$DATABASE_URL -c \"DROP SCHEMA ${BRANCH_SLUG} CASCADE;\""
fi
```

## Report Format

**Successful removal (merged branch):**

```
Removed worktree: .worktrees/feat/auth
  Worktree directory: deleted
  Local branch feat/auth: deleted (was merged)
  Remote branch origin/feat/auth: deleted
  References: pruned

DB reminder: neonctl branches delete feat-auth
```

**Removal with warnings (unmerged branch):**

```
Removed worktree: .worktrees/feat/experimental
  Worktree directory: deleted
  Local branch feat/experimental: deleted (was NOT merged - forced)
  Remote branch: no remote branch found
  References: pruned

WARNING: Branch was not merged. Changes may be lost.
Last commit: a1b2c3d "WIP: experimental auth flow"
```

## Flags

| Flag | Effect |
|------|--------|
| `--force` | Skip uncommitted changes warning |
| `--keep-branch` | Remove worktree but keep the branch |
| `--keep-remote` | Don't delete remote branch |

## Quick Reference

| Situation | Action |
|-----------|--------|
| Branch is merged | Safe delete (branch -d) |
| Branch is unmerged | Warn + require confirmation (branch -D) |
| Uncommitted changes | Warn + offer force/cancel |
| Protected branch (main/develop) | Block removal |
| Remote branch exists | Ask to delete remote |
| DB branch detected | Remind with exact command |
| Stale references | Auto-prune |

## Common Mistakes

**Removing worktree for main/develop**
- Always blocked by safety check. Reconfigure protected branches if needed.

**Deleting unmerged branch without checking**
- Always verify merge status. Unmerged branches require explicit `--force` or `-D`.

**Forgetting database branch cleanup**
- Leaves orphaned DB branches consuming resources. Command reminds automatically.

**Using `rm -rf` instead of `git worktree remove`**
- Leaves stale worktree references in `.git/worktrees/`. Always use git commands.

## Usage

```
/git-worktree-remove feat/auth
/git-worktree-remove fix/login-bug --force
/git-worktree-remove refactor/db --keep-branch
```

Branch or worktree path: $ARGUMENTS