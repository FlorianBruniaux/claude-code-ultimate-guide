---
model: haiku
description: Create a git worktree for isolated feature/fix work
---

# Git Worktree Setup

Create an isolated git worktree for a feature or fix branch.

**Note**: This is a documentation-only repo (no node_modules, no type check). Setup is instant.

## Usage

```bash
/worktree feature/pr-9-skill-improvements   # Create worktree from main
/worktree fix/typo-in-guide                 # Fix branch
/worktree feat/new-section --fast           # Skip gitignore check
```

**Naming convention**: Always use `prefix/description` format.
- Branch: `feature/pr-9-skill-improvements`
- Directory: `.worktrees/feature-pr-9-skill-improvements`

## Implementation

Execute this script with branch name from `$ARGUMENTS`:

```bash
#!/bin/bash
set -euo pipefail

# Parse flags
RAW_ARGS="${ARGUMENTS:-}"
BRANCH_NAME="$RAW_ARGS"
SKIP_CHECK=false

if [[ "$RAW_ARGS" == *"--fast"* ]]; then
  SKIP_CHECK=true
  BRANCH_NAME="${BRANCH_NAME// --fast/}"
fi

# Validate branch name
if [ -z "$BRANCH_NAME" ]; then
  echo "❌ Usage: /worktree <branch-name>"
  echo ""
  echo "Examples:"
  echo "  /worktree feature/pr-9-skill-improvements"
  echo "  /worktree fix/typo-in-guide"
  exit 1
fi

if [[ "$BRANCH_NAME" =~ [[:space:]\$\`] ]]; then
  echo "❌ Invalid branch name (spaces or special characters not allowed)"
  exit 1
fi

if [[ "$BRANCH_NAME" =~ [~^:?*\\\[\]] ]]; then
  echo "❌ Invalid branch name (git forbidden characters: ~ ^ : ? * [ ])"
  exit 1
fi

# Resolve repo root (works from any worktree)
GIT_COMMON_DIR="$(git rev-parse --git-common-dir 2>/dev/null)"
if [ -z "$GIT_COMMON_DIR" ]; then
  echo "❌ Not in a git repository"
  exit 1
fi
REPO_ROOT="$(cd "$GIT_COMMON_DIR/.." && pwd)"

# Paths
WORKTREE_NAME="${BRANCH_NAME//\//-}"
WORKTREE_DIR="$REPO_ROOT/.worktrees/$WORKTREE_NAME"

# Check .gitignore
if [ "$SKIP_CHECK" = false ]; then
  if ! grep -qE "^\.worktrees/?$" "$REPO_ROOT/.gitignore" 2>/dev/null; then
    echo "⚠️  .worktrees/ not in .gitignore — adding it now..."
    echo ".worktrees/" >> "$REPO_ROOT/.gitignore"
    echo "✅ Added .worktrees/ to .gitignore"
    echo ""
  fi
fi

# Check if worktree already exists
if [ -d "$WORKTREE_DIR" ]; then
  echo "❌ Worktree already exists: $WORKTREE_DIR"
  echo ""
  echo "Options:"
  echo "  /worktree-status $BRANCH_NAME  # Check its status"
  echo "  /remove-worktree $BRANCH_NAME  # Remove it first"
  exit 1
fi

# Create worktree
echo "Creating worktree for branch: $BRANCH_NAME"
mkdir -p "$REPO_ROOT/.worktrees"

if ! git worktree add "$WORKTREE_DIR" -b "$BRANCH_NAME" 2>/tmp/worktree-error.log; then
  ERR=$(cat /tmp/worktree-error.log)
  if echo "$ERR" | grep -q "already exists"; then
    echo "⚠️  Branch already exists, reusing it..."
    if ! git worktree add "$WORKTREE_DIR" "$BRANCH_NAME" 2>/tmp/worktree-error.log; then
      echo "❌ Failed to create worktree"
      cat /tmp/worktree-error.log
      exit 1
    fi
  else
    echo "❌ Failed to create worktree"
    cat /tmp/worktree-error.log
    exit 1
  fi
fi

echo ""
echo "✅ Worktree ready: $WORKTREE_DIR"
echo "✅ Branch: $BRANCH_NAME"
echo ""
echo "🚀 Next steps:"
echo ""
echo "If Claude Code is running:"
echo "   1. /exit"
echo "   2. cd $WORKTREE_DIR"
echo "   3. claude"
echo ""
echo "If Claude Code is NOT running:"
echo "   cd $WORKTREE_DIR && claude"
echo ""
echo "When done: /remove-worktree $BRANCH_NAME"
```

## Branch Naming

| Pattern | Branch | Directory |
|---------|--------|-----------|
| `feature/pr-9-skills` | `feature/pr-9-skills` | `.worktrees/feature-pr-9-skills` |
| `fix/typo-in-guide` | `fix/typo-in-guide` | `.worktrees/fix-typo-in-guide` |
| `docs/add-section` | `docs/add-section` | `.worktrees/docs-add-section` |

## Cleanup

```bash
/remove-worktree feature/pr-9-skills    # Remove specific worktree
/clean-worktrees                         # Remove all merged worktrees
```
