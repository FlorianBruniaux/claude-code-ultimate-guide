---
model: haiku
description: Automatically remove all merged worktrees (safe, no confirmation needed)
---

# Clean Worktrees (Automatic)

Remove all worktrees for branches already merged into `main`. No interactive prompts.

**Difference with `/remove-worktree`**:
- `/remove-worktree <branch>`: Targeted removal, asks confirmation for unmerged branches
- `/clean-worktrees`: Batch removal of merged branches only, fully automatic

## Usage

```bash
/clean-worktrees              # Remove all merged worktrees
/clean-worktrees --dry-run    # Preview without deleting
```

## Implementation

Execute this script:

```bash
#!/bin/bash
set -euo pipefail

DRY_RUN=false
if [[ "${ARGUMENTS:-}" == *"--dry-run"* ]]; then
  DRY_RUN=true
fi

echo "🧹 Cleaning Merged Worktrees"
echo "============================="
echo ""

# Resolve repo root
GIT_COMMON_DIR="$(git rev-parse --git-common-dir 2>/dev/null)"
REPO_ROOT="$(cd "$GIT_COMMON_DIR/.." && pwd)"

# Step 1: Prune stale git references
echo "1️⃣  Pruning stale references..."
PRUNED=$(git worktree prune -v 2>&1 || true)
if [ -n "$PRUNED" ]; then
  echo "$PRUNED"
  echo "✅ Stale references pruned"
else
  echo "✅ No stale references"
fi
echo ""

# Step 2: Find merged worktrees
echo "2️⃣  Finding merged worktrees..."
MERGED_ITEMS=()

while IFS= read -r line; do
  WT_PATH=$(echo "$line" | awk '{print $1}')
  WT_BRANCH=$(echo "$line" | grep -oE '\[.*\]' | tr -d '[]' || true)

  [ -z "$WT_BRANCH" ] && continue
  [ "$WT_BRANCH" = "main" ] && continue
  [ "$WT_BRANCH" = "develop" ] && continue
  [ "$WT_PATH" = "$REPO_ROOT" ] && continue

  if git branch --merged main 2>/dev/null | grep -q "^[* ] ${WT_BRANCH}$"; then
    MERGED_ITEMS+=("$WT_BRANCH|$WT_PATH")
    echo "  ✓ $WT_BRANCH (merged into main)"
  fi
done < <(git worktree list)

if [ ${#MERGED_ITEMS[@]} -eq 0 ]; then
  echo "✅ No merged worktrees to clean"
  echo ""
  echo "📊 Active worktrees:"
  git worktree list
  exit 0
fi

echo ""
echo "📋 Found ${#MERGED_ITEMS[@]} merged worktree(s)"
echo ""

if [ "$DRY_RUN" = true ]; then
  echo "🔍 DRY RUN — nothing will be deleted"
  echo ""
  echo "Would remove:"
  for item in "${MERGED_ITEMS[@]}"; do
    branch=$(echo "$item" | cut -d'|' -f1)
    path=$(echo "$item" | cut -d'|' -f2)
    echo "  - $branch"
    echo "    $path"
  done
  echo ""
  echo "Run without --dry-run to delete."
  exit 0
fi

# Step 3: Remove merged worktrees
echo "3️⃣  Removing..."
REMOVED=0

for item in "${MERGED_ITEMS[@]}"; do
  branch=$(echo "$item" | cut -d'|' -f1)
  path=$(echo "$item" | cut -d'|' -f2)

  echo ""
  echo "🗑️  $branch"

  if git worktree remove "$path" 2>/dev/null; then
    echo "   ✅ Worktree removed"
  else
    rm -rf "$path" 2>/dev/null || true
    git worktree prune 2>/dev/null || true
    echo "   ✅ Removed (forced)"
  fi

  if git branch -d "$branch" 2>/dev/null; then
    echo "   ✅ Branch deleted"
  else
    echo "   ⚠️  Branch already gone"
  fi

  REMOVED=$((REMOVED + 1))
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Done — removed $REMOVED worktree(s)"
echo ""
echo "📊 Remaining:"
git worktree list
```

## Safety

- Only removes branches merged into `main`
- Never touches `main` or `develop`
- Never removes the current working directory (main repo)
- `--dry-run` to preview before acting

## When to use

- After merging a PR: `/clean-worktrees`
- Before creating a new worktree (declutter): `/clean-worktrees`
- Weekly maintenance: `/clean-worktrees`
