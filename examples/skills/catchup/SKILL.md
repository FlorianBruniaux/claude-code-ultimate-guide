---
name: catchup
description: Restore context after /clear by summarizing recent work and project state
argument-hint: "[branch] [--since <date>]"
effort: low
when_to_use: "Use after /clear or at session start to restore context."
disable-model-invocation: true
---

# Context catchup

Restore context after `/clear` - summarize recent work and project state.

## Purpose

After clearing context with `/clear`, use this command to quickly rebuild understanding of:
- What was recently modified
- Current project state
- Outstanding TODOs and issues
- Where to resume work

## Instructions

### Step 1: Git history analysis

```bash
# Recent commits (last 10)
git log --oneline -10

# Files modified in last 5 commits
git diff --stat HEAD~5 2>/dev/null || git diff --stat $(git rev-list --max-parents=0 HEAD)

# Current branch and status
git branch --show-current
git status --short
```

### Step 2: Recent changes summary

```bash
# What changed today
git log --oneline --since="midnight" --author="$(git config user.name)" 2>/dev/null

# Uncommitted work
git diff --name-only
git diff --cached --name-only
```

### Step 3: TODO/FIXME scan

```bash
# Find outstanding work markers in recently modified files
git diff --name-only HEAD~5 2>/dev/null | head -20 | xargs grep -n "TODO\|FIXME\|XXX\|HACK" 2>/dev/null | head -30
```

### Step 4: Project state check

```bash
# Check for common state indicators
[ -f "package.json" ] && echo "📦 Node project: $(jq -r '.name // "unnamed"' package.json)"
[ -f "Cargo.toml" ] && echo "🦀 Rust project: $(grep '^name' Cargo.toml | head -1)"
[ -f "pyproject.toml" ] && echo "🐍 Python project"
[ -f "go.mod" ] && echo "🐹 Go project: $(head -1 go.mod | cut -d' ' -f2)"

# Active branch purpose (from branch name)
BRANCH=$(git branch --show-current)
echo "🌿 Branch: $BRANCH"
```

## Output format

Provide a structured summary:

---

### 📍 Context restored

**Project**: [name from package.json/Cargo.toml/etc]
**Branch**: [current branch]
**Last Activity**: [time of last commit]

### 🔄 Recent work (last 5 commits)

1. [commit message 1] - [files affected]
2. [commit message 2] - [files affected]
...

### 📝 Uncommitted changes

- [list of modified files with brief description of changes]

### ⚠️ Outstanding TODOs

- [file:line] TODO: [description]
- [file:line] FIXME: [description]

### 🎯 Suggested next steps

Based on recent activity:
1. [Most likely next action based on patterns]
2. [Alternative focus area]

---

## Usage examples

**After a long break:**
```
/catchup
```
→ Full context restoration

**Quick status check:**
```
/catchup --brief
```
→ Just commits and uncommitted changes

**Focus on specific area:**
```
/catchup auth
```
→ Filter to auth-related changes

## Pro tips

1. **Document before `/clear`**: Write a brief note in a commit message or CLAUDE.md before clearing context
2. **Use with Memory Bank**: Combine with `.claude/memory/` files for persistent state
3. **Branch naming**: Use descriptive branch names (e.g., `feat/user-auth`) to aid context restoration

$ARGUMENTS
