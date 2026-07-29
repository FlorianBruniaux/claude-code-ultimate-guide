---
model: haiku
description: Show status of all active worktrees
---

# Worktree Status

Show all active git worktrees with branch, path, and modified files count.

## Usage

```bash
/worktree-status                    # List all worktrees
/worktree-status feature/pr-9       # Check specific branch
```

## Implementation

Execute this script with optional branch name from `$ARGUMENTS`:

```bash
#!/bin/bash
set -euo pipefail

BRANCH_FILTER="${ARGUMENTS:-}"

# Resolve repo root
GIT_COMMON_DIR="$(git rev-parse --git-common-dir 2>/dev/null)"
if [ -z "$GIT_COMMON_DIR" ]; then
  echo "❌ Not in a git repository"
  exit 1
fi
REPO_ROOT="$(cd "$GIT_COMMON_DIR/.." && pwd)"

echo "📂 Git Worktrees"
echo "================"
echo ""

# List all worktrees with details
WORKTREE_LIST=$(git worktree list --porcelain)

if [ -z "$WORKTREE_LIST" ]; then
  echo "No worktrees found."
  exit 0
fi

WORKTREE_COUNT=0

while IFS= read -r block; do
  # Parse each worktree block
  PATH_LINE=$(echo "$block" | grep "^worktree " | head -1)
  BRANCH_LINE=$(echo "$block" | grep "^branch " | head -1)
  HEAD_LINE=$(echo "$block" | grep "^HEAD " | head -1)

  [ -z "$PATH_LINE" ] && continue

  WT_PATH="${PATH_LINE#worktree }"
  WT_BRANCH="${BRANCH_LINE#branch refs/heads/}"
  WT_HEAD="${HEAD_LINE#HEAD }"

  # Apply filter if provided
  if [ -n "$BRANCH_FILTER" ] && ! echo "$WT_BRANCH" | grep -q "$BRANCH_FILTER"; then
    continue
  fi

  WORKTREE_COUNT=$((WORKTREE_COUNT + 1))

  # Determine if main repo
  IS_MAIN=""
  if [ "$WT_PATH" = "$REPO_ROOT" ]; then
    IS_MAIN=" (main repo)"
  fi

  echo "🌿 ${WT_BRANCH:-detached}${IS_MAIN}"
  echo "   Path:   $WT_PATH"
  echo "   Commit: ${WT_HEAD:0:8}"

  # Count modified files (only for existing paths)
  if [ -d "$WT_PATH" ]; then
    MODIFIED=$(git -C "$WT_PATH" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    if [ "$MODIFIED" -gt 0 ]; then
      echo "   Changes: $MODIFIED file(s) modified"
    else
      echo "   Changes: clean"
    fi

    # Show commits ahead/behind main
    if [ -n "$WT_BRANCH" ] && [ "$WT_BRANCH" != "main" ]; then
      AHEAD=$(git -C "$WT_PATH" rev-list "main..HEAD" --count 2>/dev/null || echo "?")
      echo "   Ahead of main: $AHEAD commit(s)"
    fi
  else
    echo "   ⚠️  Directory missing (stale reference)"
  fi
  echo ""

done < <(git worktree list --porcelain | awk 'BEGIN{RS="";FS="\n"} {print $0"\n---"}' | while IFS= read -r line; do
  if [ "$line" = "---" ]; then
    echo "$block"
    block=""
  else
    block="${block}${line}\n"
  fi
done)

# Simpler approach: iterate worktrees line by line
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

git worktree list | while IFS= read -r line; do
  WT_PATH=$(echo "$line" | awk '{print $1}')
  WT_HEAD=$(echo "$line" | awk '{print $2}')
  WT_BRANCH=$(echo "$line" | grep -oE '\[.*\]' | tr -d '[]' || echo "detached")

  IS_MAIN=""
  if [ "$WT_PATH" = "$REPO_ROOT" ]; then
    IS_MAIN=" ← current repo"
  fi

  echo "🌿 ${WT_BRANCH}${IS_MAIN}"
  echo "   Path:   $WT_PATH"
  echo "   Head:   ${WT_HEAD:0:8}"

  if [ -d "$WT_PATH" ]; then
    MODIFIED=$(git -C "$WT_PATH" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    if [ "$MODIFIED" -gt 0 ]; then
      echo "   Status: $MODIFIED file(s) changed"
    else
      echo "   Status: clean"
    fi

    if [ -n "$WT_BRANCH" ] && [ "$WT_BRANCH" != "main" ] && [ "$WT_BRANCH" != "(bare)" ]; then
      AHEAD=$(git -C "$WT_PATH" rev-list "main..HEAD" --count 2>/dev/null || echo "?")
      echo "   Ahead:  $AHEAD commit(s) vs main"
    fi
  else
    echo "   ⚠️  Stale reference (directory missing)"
  fi
  echo ""
done

echo "Run /clean-worktrees to remove merged worktrees."
```

## Output Example

```
🌿 main ← current repo
   Path:   /Users/.../claude-code-ultimate-guide
   Head:   f5d78e1c
   Status: clean

🌿 feature/pr-9-skill-improvements
   Path:   /Users/.../.worktrees/feature-pr-9-skill-improvements
   Head:   f5d78e1c
   Status: 6 file(s) changed
   Ahead:  0 commit(s) vs main

Run /clean-worktrees to remove merged worktrees.
```
