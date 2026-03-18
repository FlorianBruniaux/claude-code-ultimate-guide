---
name: git-worktree
description: "Create isolated git worktrees for feature development without switching branches"
---

# Git Worktree Setup

Create isolated git worktrees for feature development without switching branches.

**Core principle:** Smart directory selection + symlink optimization + background verification = fast, reliable isolation.

**Requires:** Git 2.5.0+ (July 2015)

**Companion commands:** [`/git-worktree-status`](./git-worktree-status.md) | [`/git-worktree-remove`](./git-worktree-remove.md) | [`/git-worktree-clean`](./git-worktree-clean.md)

## Process

1. **Validate Branch Name**: Check naming convention and conflicts
2. **Check Existing Directories**: `.worktrees/` or `worktrees/`
3. **Verify .gitignore**: Ensure worktree dir is ignored
4. **Create Worktree**: `git worktree add`
5. **Symlink Dependencies**: Reuse `node_modules/` from main worktree
6. **Detect Database Provider**: Check for DB branching capability
7. **Install Dependencies**: Auto-detect package manager (if not symlinking)
8. **Run Background Verification**: Type check + tests in background
9. **Report Location**: Confirm ready with status

## Flags

| Flag | Effect |
|------|--------|
| `--fast` | Skip dependency install and baseline tests |
| `--isolated` | Fresh `node_modules` install (no symlink) |
| `--skip-install` | Skip dependency install, keep baseline tests |

## Branch Name Validation

```bash
# Auto-prefix based on naming convention
# "auth" → "feat/auth" (default prefix)
# "fix/login-bug" → kept as-is
# "refactor/db-layer" → kept as-is

# Accepted prefixes: feat/, fix/, refactor/, chore/, docs/, test/, perf/
# If no prefix → default to feat/

# Reject invalid characters
echo "$BRANCH_NAME" | grep -qE '^[a-zA-Z0-9/_-]+$' || exit 1

# Check branch doesn't already exist
git show-ref --verify --quiet "refs/heads/$BRANCH_NAME" && echo "Branch already exists" && exit 1
```

## Directory Selection

### Priority Order

```bash
# 1. Check existing directories
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative

# 2. Check CLAUDE.md for preference
grep -i "worktree.*director" CLAUDE.md 2>/dev/null

# 3. Ask user if neither exists
```

**If both exist:** `.worktrees/` wins.

## Safety Verification

**For project-local directories:**

```bash
# Check if directory in .gitignore
grep -q "^\.worktrees/$" .gitignore || grep -q "^worktrees/$" .gitignore
```

**If NOT in .gitignore:**
1. Add line to .gitignore
2. Commit the change
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents.

## Creation Steps

```bash
# 1. Detect project name
project=$(basename "$(git rev-parse --show-toplevel)")

# 2. Create worktree with new branch
git worktree add .worktrees/$BRANCH_NAME -b $BRANCH_NAME

# 3. Navigate
cd .worktrees/$BRANCH_NAME
```

## Dependency Optimization (Node.js)

**Default behavior:** Symlink `node_modules` from main worktree to avoid duplicate installs (~30s saved).

```bash
# Symlink node_modules (default, unless --isolated)
if [ -d "../../node_modules" ] && [ ! "$ISOLATED" = true ]; then
  ln -s "$(cd ../.. && pwd)/node_modules" node_modules
  echo "Symlinked node_modules from main worktree"
fi

# With --isolated: fresh install
if [ "$ISOLATED" = true ]; then
  pnpm install   # or npm/yarn based on lockfile detection
fi
```

**When to use `--isolated`:**
- Schema changes requiring different package versions
- Testing dependency upgrades
- Debugging `node_modules` issues

## Auto-Detect Setup (Multi-Stack)

```bash
# Node.js (if not symlinked)
if [ -f package.json ] && [ ! -L node_modules ]; then
  pnpm install   # Detect from lockfile: pnpm-lock.yaml / yarn.lock / package-lock.json
fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## Background Verification

**Instead of blocking on full test suite, run verification in background:**

```bash
# Create log directory
mkdir -p .worktree-logs

# Background type check (Node.js)
if [ -f tsconfig.json ]; then
  npx tsc --noEmit > .worktree-logs/typecheck.log 2>&1 &
  echo "Type check running in background (check with /git-worktree-status)"
fi

# Background test run
if [ -f package.json ]; then
  npx vitest run --reporter=json > .worktree-logs/tests.log 2>&1 &
  echo "Tests running in background (check with /git-worktree-status)"
fi
```

**With `--fast`:** Skip all verification.

## Final Report

```
Worktree ready at <full-path>
Branch: feat/auth (created from main)
Dependencies: symlinked from main worktree
Background checks: type check + tests running
Check status: /git-worktree-status

Ready to implement <feature-name>
```

## Database Branch Suggestion

**After worktree creation, detect database provider and suggest isolation.**

### Quick Command Reference

| Provider | Suggested Command |
|----------|-------------------|
| **Neon** | `neonctl branches create --name <branch> --parent main` |
| **PlanetScale** | `pscale branch create <db> <branch>` |
| **Local Postgres** | `psql -c "CREATE SCHEMA <schema>;"` |
| **Other** | Manual setup or shared DB |

**Example output:**

```
Worktree created at .worktrees/feat/auth

DB Isolation: neonctl branches create --name feat-auth --parent main
   Then update .env with new DATABASE_URL
   Full guide: ../workflows/database-branch-setup.md
```

### .worktreeinclude Setup

**Critical for environment variables:**

```bash
# .worktreeinclude (at project root)
.env
.env.local
.env.development
**/.claude/settings.local.json
```

**Why:** Without this, `.env` files won't be copied to worktrees.

### When to Create Database Branch

| Scenario | Create Branch? |
|----------|---------------|
| Schema migrations | Yes |
| Data model refactoring | Yes |
| Bug fix (no schema change) | No |
| Performance experiments | Yes |

**See:** [Database Branch Setup Guide](../workflows/database-branch-setup.md) for complete workflows.

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify .gitignore) |
| `worktrees/` exists | Use it (verify .gitignore) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md, then ask user |
| Not in .gitignore | Add + commit immediately |
| No branch prefix | Auto-prefix with `feat/` |
| Node.js project | Symlink `node_modules` by default |
| `--fast` flag | Skip install + tests |
| `--isolated` flag | Fresh `node_modules` install |
| Neon detected | Suggest `neonctl branches create` |
| PlanetScale detected | Suggest `pscale branch create` |
| No .worktreeinclude | Create with `.env` pattern |

## Common Mistakes

**Skipping .gitignore verification**
- Worktree contents get tracked, pollute git status

**Assuming directory location**
- Follow priority: existing > CLAUDE.md > ask

**Installing full node_modules in every worktree**
- Wastes disk and time. Use symlink by default, `--isolated` only when needed

**Not copying .env to worktree**
- Symptom: Claude fails with "DATABASE_URL not found"
- Fix: Add `.env` to `.worktreeinclude`

**Using shared database for schema changes**
- Symptom: Migration conflicts, broken dev environment
- Fix: Create database branch before modifying schema

## Usage

```
/git-worktree auth
/git-worktree fix/session-bug
/git-worktree feature/new-api --fast
/git-worktree refactor/db-layer --isolated
```

Branch name: $ARGUMENTS