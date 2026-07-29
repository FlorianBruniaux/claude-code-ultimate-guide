---
model: haiku
description: Remove a specific worktree cleanly (directory + git reference + branch)
---

# Remove Worktree

Remove a specific worktree: directory, git reference, and local branch.

## Usage

```bash
/remove-worktree feature/pr-9-skill-improvements
/remove-worktree fix/typo-in-guide
```

## Implementation

Execute this script with branch name from `$ARGUMENTS`:

```bash
#!/bin/bash
set -euo pipefail

BRANCH_NAME="${ARGUMENTS:-}"

if [ -z "$BRANCH_NAME" ]; then
  echo "❌ Usage: /remove-worktree <branch-name>"
  echo ""
  echo "Available worktrees:"
  git worktree list
  exit 1
fi

# Resolve repo root
GIT_COMMON_DIR="$(git rev-parse --git-common-dir 2>/dev/null)"
REPO_ROOT="$(cd "$GIT_COMMON_DIR/.." && pwd)"

# Convert branch name to worktree path
WORKTREE_NAME="${BRANCH_NAME//\//-}"
WORKTREE_DIR="$REPO_ROOT/.worktrees/$WORKTREE_NAME"

echo "🔍 Looking for worktree: $BRANCH_NAME"
echo ""

# Find worktree in git list
if ! git worktree list | grep -q "$BRANCH_NAME"; then
  echo "❌ Worktree not found for branch: $BRANCH_NAME"
  echo ""
  echo "Available worktrees:"
  git worktree list
  exit 1
fi

# Get actual path from git worktree list
WORKTREE_FULL_PATH=$(git worktree list | grep "\[$BRANCH_NAME\]" | awk '{print $1}')
if [ -z "$WORKTREE_FULL_PATH" ]; then
  # Fallback: try matching the calculated path
  WORKTREE_FULL_PATH="$WORKTREE_DIR"
fi

# Safety: never remove main repo
if [ "$WORKTREE_FULL_PATH" = "$REPO_ROOT" ]; then
  echo "❌ Cannot remove the main repository worktree"
  exit 1
fi

# Safety: never remove protected branches
if [ "$BRANCH_NAME" = "main" ] || [ "$BRANCH_NAME" = "develop" ]; then
  echo "❌ Cannot remove protected branch: $BRANCH_NAME"
  exit 1
fi

echo "📂 Path:   $WORKTREE_FULL_PATH"
echo "🌿 Branch: $BRANCH_NAME"
echo ""

# Check if merged into main
IS_MERGED=false
if git branch --merged main 2>/dev/null | grep -q "^[* ] ${BRANCH_NAME}$"; then
  IS_MERGED=true
  echo "✅ Branch is merged into main (safe to delete)"
else
  echo "⚠️  Branch is NOT merged into main"
fi
echo ""

# Confirm if not merged
if [ "$IS_MERGED" = false ]; then
  echo "⚠️  This will DELETE unmerged work. Are you sure? [y/N]"
  read -r confirm
  if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Aborted."
    exit 0
  fi
fi

# Remove worktree
echo "🗑️  Removing worktree..."
if git worktree remove "$WORKTREE_FULL_PATH" 2>/dev/null; then
  echo "✅ Worktree removed"
else
  echo "⚠️  Git remove failed, forcing..."
  rm -rf "$WORKTREE_FULL_PATH" 2>/dev/null || true
  git worktree prune 2>/dev/null || true
  echo "✅ Removed (forced)"
fi

# Delete local branch
echo ""
echo "🌿 Deleting local branch..."
if [ "$IS_MERGED" = true ]; then
  git branch -d "$BRANCH_NAME" 2>/dev/null && echo "✅ Branch deleted" || echo "⚠️  Branch already gone"
else
  git branch -D "$BRANCH_NAME" 2>/dev/null && echo "✅ Branch force-deleted" || echo "⚠️  Branch already gone"
fi

echo ""
echo "✅ Done!"
echo ""
echo "📊 Remaining worktrees:"
git worktree list
```

## Safety

- Never removes `main` or `develop`
- Asks confirmation for unmerged branches
- Falls back to force-remove if git fails
- Reports remaining worktrees after cleanup
