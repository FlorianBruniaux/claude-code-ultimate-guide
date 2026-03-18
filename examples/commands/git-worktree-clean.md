---
name: git-worktree-clean
description: "Clean up stale git worktrees with merged branch detection and disk usage report"
---

# Git Worktree Clean

Batch cleanup of stale git worktrees. Safely removes merged branches, reports disk usage, and handles unmerged branches interactively.

**Core principle:** Auto-clean merged worktrees, interactive review for unmerged, always report what was reclaimed.

**Part of:** [Worktree Lifecycle Suite](./git-worktree.md) | [`/git-worktree`](./git-worktree.md) | [`/git-worktree-status`](./git-worktree-status.md) | [`/git-worktree-remove`](./git-worktree-remove.md)

## Process

1. **List All Worktrees**: `git worktree list`
2. **Classify Each**: merged vs unmerged vs protected
3. **Calculate Disk Usage**: Per-worktree size
4. **Auto Mode**: Remove all merged worktrees (safe)
5. **Interactive Mode**: Review unmerged worktrees one by one
6. **Database Cleanup Reminder**: List DB branches to clean
7. **Report**: Summary of actions taken and space reclaimed

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Preview what would be cleaned, no changes |
| `--all` | Include unmerged worktrees (interactive confirmation each) |
| `--force` | Remove all worktrees without confirmation (dangerous) |

## Worktree Discovery

```bash
# Get main branch name
MAIN_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
MAIN_BRANCH=${MAIN_BRANCH:-main}

# Protected branches (never auto-clean)
PROTECTED="main master develop staging production"

# List all worktrees (skip main working tree)
git worktree list --porcelain | while read line; do
  # Parse worktree path and branch
  # Skip the main worktree (first entry)
done
```

## Classification

```bash
for WORKTREE in $WORKTREES; do
  BRANCH=$(git -C "$WORKTREE" rev-parse --abbrev-ref HEAD)

  # Skip protected
  if echo "$PROTECTED" | grep -qw "$BRANCH"; then
    echo "PROTECTED: $BRANCH (skipped)"
    continue
  fi

  # Check merge status
  if git merge-base --is-ancestor "$BRANCH" "$MAIN_BRANCH" 2>/dev/null; then
    echo "MERGED: $BRANCH → safe to remove"
    MERGED_LIST="$MERGED_LIST $WORKTREE"
  else
    echo "UNMERGED: $BRANCH → requires review"
    UNMERGED_LIST="$UNMERGED_LIST $WORKTREE"
  fi
done
```

## Disk Usage Calculation

```bash
for WORKTREE in $ALL_WORKTREES; do
  # Calculate size excluding symlinked node_modules
  SIZE=$(du -sh --exclude='node_modules' "$WORKTREE" 2>/dev/null | cut -f1)
  # Or on macOS:
  SIZE=$(du -sh -I 'node_modules' "$WORKTREE" 2>/dev/null | cut -f1)
  echo "  $WORKTREE: $SIZE"
done
```

## Dry Run Mode

```bash
# --dry-run: show what would happen without making changes

echo "=== Dry Run ==="
echo ""
echo "Would remove (merged):"
for WT in $MERGED_LIST; do
  echo "  $WT ($BRANCH) - $SIZE"
done
echo ""
echo "Would ask about (unmerged):"
for WT in $UNMERGED_LIST; do
  echo "  $WT ($BRANCH) - $SIZE - last commit: $(git log -1 --format='%s' $BRANCH)"
done
echo ""
echo "Total space to reclaim: $TOTAL_SIZE"
echo ""
echo "Run without --dry-run to execute."
```

## Auto Mode (Default)

**Only removes merged worktrees. Safe by default.**

```bash
echo "Cleaning merged worktrees..."

for WORKTREE in $MERGED_LIST; do
  BRANCH=$(git -C "$WORKTREE" rev-parse --abbrev-ref HEAD)

  # Remove worktree
  git worktree remove "$WORKTREE"

  # Delete local branch
  git branch -d "$BRANCH" 2>/dev/null

  # Delete remote branch
  git push origin --delete "$BRANCH" 2>/dev/null

  echo "  Removed: $WORKTREE ($BRANCH)"
done

# Report unmerged (not touched)
if [ -n "$UNMERGED_LIST" ]; then
  echo ""
  echo "Unmerged worktrees (kept):"
  for WT in $UNMERGED_LIST; do
    echo "  $WT - use /git-worktree-remove or --all to review"
  done
fi
```

## Interactive Mode (--all)

**Reviews unmerged worktrees one by one:**

```bash
for WORKTREE in $UNMERGED_LIST; do
  BRANCH=$(git -C "$WORKTREE" rev-parse --abbrev-ref HEAD)
  LAST_COMMIT=$(git log -1 --format='%h %s (%cr)' "$BRANCH")
  AHEAD=$(git rev-list --count "$MAIN_BRANCH".."$BRANCH")

  echo ""
  echo "Unmerged: $WORKTREE"
  echo "  Branch: $BRANCH ($AHEAD commits ahead of $MAIN_BRANCH)"
  echo "  Last commit: $LAST_COMMIT"
  echo "  Size: $SIZE"
  echo ""
  echo "  [r]emove  [k]eep  [s]kip remaining"

  # Wait for user decision per worktree
done
```

## Report Format

**After cleanup:**

```
=== Worktree Cleanup Report ===

Removed (merged):
  .worktrees/feat/auth (feat/auth) - 2.3 MB
  .worktrees/fix/login-bug (fix/login-bug) - 1.1 MB
  .worktrees/chore/deps-update (chore/deps-update) - 0.8 MB

Kept (unmerged):
  .worktrees/feat/experimental (feat/experimental) - 4.2 MB
    Last commit: a1b2c3d "WIP: new auth flow" (3 days ago)

Kept (protected):
  .worktrees/develop (develop)

Space reclaimed: 4.2 MB
Worktrees remaining: 2
References pruned: yes

DB branches to clean:
  neonctl branches delete feat-auth
  neonctl branches delete fix-login-bug
  neonctl branches delete chore-deps-update
```

**Dry run report:**

```
=== Dry Run - No Changes Made ===

Would remove (3 merged):
  .worktrees/feat/auth - 2.3 MB
  .worktrees/fix/login-bug - 1.1 MB
  .worktrees/chore/deps-update - 0.8 MB

Would keep (1 unmerged):
  .worktrees/feat/experimental - 4.2 MB

Would keep (1 protected):
  .worktrees/develop

Potential space savings: 4.2 MB
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Default (no flags) | Remove merged worktrees only |
| `--dry-run` | Preview without changes |
| `--all` | Merged (auto) + unmerged (interactive) |
| `--force` | Remove everything except protected |
| Protected branch | Always kept |
| Merged branch | Auto-removed |
| Unmerged branch | Kept (default) or interactive (--all) |
| DB branches detected | Reminder with exact commands |

## Common Mistakes

**Running `--force` without `--dry-run` first**
- Always preview with `--dry-run` before force-cleaning

**Forgetting DB branch cleanup**
- Worktree cleanup doesn't auto-delete DB branches. Follow the reminder commands.

**Not running cleanup regularly**
- Stale worktrees accumulate disk space. Run `/git-worktree-clean --dry-run` weekly.

## Usage

```
/git-worktree-clean
/git-worktree-clean --dry-run
/git-worktree-clean --all
```

Flags: $ARGUMENTS