---
name: git-worktree-status
description: "Report the type check, test and build results that /git-worktree started in the background for the current worktree, read from .worktree-logs/. Use when asked whether a worktree's checks passed or are still running."
effort: low
---

# Git worktree status

Check background verification tasks (type check, tests, build) launched by `/git-worktree`.

**Core principle:** Non-blocking feedback on worktree health without interrupting development flow.

**Part of:** Worktree Lifecycle Suite: [`/git-worktree`](../git-worktree/SKILL.md) | [`/git-worktree-remove`](../git-worktree-remove/SKILL.md) | [`/git-worktree-clean`](../git-worktree-clean/SKILL.md)

## Process

1. **Detect Current Worktree**: Verify we're inside a git worktree
2. **Check Log Files**: Read `.worktree-logs/` for background task results
3. **Parse Results**: Extract pass/fail counts, errors
4. **Report Status**: Color-coded summary with actionable next steps

## Worktree detection

```bash
# In a linked worktree, --git-dir is <repo>/.git/worktrees/<name> and
# --git-common-dir is <repo>/.git. In the main working tree they are equal.
[ "$(git rev-parse --git-dir 2>/dev/null)" != "$(git rev-parse --git-common-dir 2>/dev/null)" ] || {
  echo "Not inside a linked worktree. Use from a worktree directory."
  exit 1
}

# Get worktree info
WORKTREE_PATH=$(git rev-parse --show-toplevel)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
MAIN_REPO=$(dirname "$(git rev-parse --git-common-dir)")
```

## Background task checks

### Type check status

```bash
LOG=".worktree-logs/typecheck.log"

if [ -f "$LOG" ]; then
  if grep -q "error TS" "$LOG"; then
    ERROR_COUNT=$(grep -c "error TS" "$LOG")
    echo "Type check: FAIL ($ERROR_COUNT errors)"
    # Show first 5 errors
    grep "error TS" "$LOG" | head -5
  else
    echo "Type check: PASS"
  fi
elif pgrep -f "tsc --noEmit" > /dev/null; then
  echo "Type check: RUNNING..."
else
  echo "Type check: NOT RUN"
fi
```

### Test status

```bash
LOG=".worktree-logs/tests.log"

if [ -f "$LOG" ]; then
  if grep -q '"numFailedTests":0' "$LOG"; then
    TOTAL=$(grep -o '"numTotalTests":[0-9]*' "$LOG" | cut -d: -f2)
    echo "Tests: PASS ($TOTAL tests)"
  else
    FAILED=$(grep -o '"numFailedTests":[0-9]*' "$LOG" | cut -d: -f2)
    echo "Tests: FAIL ($FAILED failures)"
    # Show failed test names
    grep '"fullName"' "$LOG" | head -5
  fi
elif pgrep -f "vitest run" > /dev/null; then
  echo "Tests: RUNNING..."
else
  echo "Tests: NOT RUN"
fi
```

### Build status

```bash
LOG=".worktree-logs/build.log"

# /git-worktree does not start a build, so this log exists only if you ran one yourself.
# A log has no exit status: judge it by its content, and say so in the report.
if [ -f "$LOG" ]; then
  if grep -qi "error" "$LOG"; then
    echo "Build: FAIL (error found in log)"
    tail -10 "$LOG"
  else
    echo "Build: no error found in log"
  fi
elif pgrep -f "cargo build\|next build\|go build" > /dev/null; then
  echo "Build: RUNNING..."
else
  echo "Build: NOT RUN"
fi
```

## Report format

```
Worktree Status: .worktrees/feat/auth
Branch: feat/auth (from main, 3 commits ahead)

Checks:
  Type check:  PASS
  Tests:       PASS (142 tests)
  Build:       NOT RUN

Dependencies: symlinked from main
Disk usage: 2.3 MB (excl. node_modules)

Log files: .worktree-logs/
```

**If failures detected:**

```
Worktree Status: .worktrees/feat/auth
Branch: feat/auth (from main, 3 commits ahead)

Checks:
  Type check:  FAIL (3 errors)
    src/auth.ts:42 - error TS2345: Argument of type 'string' is not assignable
    src/auth.ts:67 - error TS2304: Cannot find name 'AuthConfig'
    src/middleware.ts:12 - error TS7006: Parameter 'req' implicitly has an 'any' type
  Tests:       FAIL (2 failures)
    auth.test.ts > should validate token
    auth.test.ts > should reject expired token
  Build:       NOT RUN

Action: Fix type errors before proceeding. Run `npx tsc --noEmit` for full output.
```

## Log management

Run these only when the user asks to re-run the checks; a status read never deletes or restarts anything.

```bash
# Clean old logs (useful for re-running checks)
rm -f .worktree-logs/*.log

# Re-run all checks
npx tsc --noEmit > .worktree-logs/typecheck.log 2>&1 &
npx vitest run --reporter=json > .worktree-logs/tests.log 2>&1 &
```

## Quick reference

| Situation | Output |
|-----------|--------|
| All checks pass | Green status, ready to work |
| Checks still running | "RUNNING..." with PID |
| Type errors found | Error count + first 5 errors |
| Test failures | Failure count + failed test names |
| No logs found | "NOT RUN" (use `--fast` or logs deleted) |
| Not in worktree | Error message with instructions |

## Usage

```
/git-worktree-status
```

No arguments needed. Run from inside any worktree directory.