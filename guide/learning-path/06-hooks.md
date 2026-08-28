# Module 06: Hooks & Events

**Time**: 1 hour | **Complexity**: ⭐⭐ Intermediate

**Previous:** [Module 05: Skills & Automation](05-skills.md)

## Goal

Automate responses to system events. Create scripts that run before or after Claude Code operations.

---

## What You'll Learn

- How hooks work and when they trigger
- Creating pre-commit validation
- Building post-action notifications
- Writing safe automation scripts
- Common hook patterns

---

## What Are Hooks?

A **hook** is a script that runs automatically in response to an event.

### Example: Pre-Commit Hook

Before you commit changes:

```
You run: git commit -m "Fix bug"
       ↓
Hook runs: Check version number consistency
       ↓
If version wrong:
  ❌ Commit blocked
  Error message shows what's wrong
       ↓
You fix: Update VERSION file
       ↓
Commit succeeds
```

Hooks prevent common mistakes from reaching git.

### Hook Events

Hooks can trigger on:

| Event | Timing | Use Case |
|-------|--------|----------|
| PreToolUse | Before Claude runs a tool | Validate request |
| PostToolUse | After Claude runs a tool | Log results, check output |
| PreCommit | Before git commit | Validate changes |
| PostPush | After git push | Notify team |

---

## Creating Your First Hook

Hooks are bash (or PowerShell) scripts in `.claude/hooks/`.

### Basic Hook Structure

```bash
#!/bin/bash

# Hook: validate-version
# Event: PreCommit
# Description: Check that VERSION file is updated with other changes

# Get the files being committed
FILES=$(git diff --cached --name-only)

# Check if guide files were changed
if echo "$FILES" | grep -q "guide/"; then
  # If guide/ changed, VERSION must also be changed
  if ! echo "$FILES" | grep -q "VERSION"; then
    echo "❌ Error: guide/ was modified but VERSION wasn't updated"
    echo "Run: echo '3.x.x' > VERSION"
    exit 1  # Block commit
  fi
fi

exit 0  # Allow commit
```

### File Location

```
my-project/
└── .claude/
    └── hooks/
        ├── validate-version.sh
        └── notify-team.sh
```

### Hook Exit Codes

```bash
exit 0   # Success - allow operation to proceed
exit 1   # Failure - block operation and show error
exit 2   # Warning - allow but show warning message
```

---

## Hook Patterns

### Pattern 1: Pre-Commit Validation

Block commits that fail validation:

```bash
#!/bin/bash
# Hook: security-check.sh
# Block commits if security issues found

# Check for hardcoded API keys
if grep -r "sk_live_" .; then
  echo "❌ ERROR: Found hardcoded Stripe key"
  exit 1
fi

# Check for console.log in production code (not tests)
if grep -r "console.log" src/ --exclude-dir=tests; then
  echo "❌ ERROR: Found console.log in source code"
  exit 1
fi

# Check for TODO comments (warning, not block)
if grep -r "TODO:" src/; then
  echo "⚠️  Warning: TODO comments found (not blocking)"
fi

exit 0
```

### Pattern 2: Post-Commit Notification

After a commit succeeds:

```bash
#!/bin/bash
# Hook: notify-team.sh
# Notify team after certain commits

COMMIT_MSG=$(git log -1 --pretty=%B)

# If security-related commit
if echo "$COMMIT_MSG" | grep -i "security"; then
  echo "🔐 Security commit: $COMMIT_MSG"
  # Send to Slack (optional)
  # curl -X POST $SLACK_WEBHOOK -d "Security update: $COMMIT_MSG"
fi

exit 0
```

### Pattern 3: Dependency Check

Warn if dependencies need updating:

```bash
#!/bin/bash
# Hook: check-deps.sh
# Check if package.json changed without updating lock file

FILES=$(git diff --cached --name-only)

if echo "$FILES" | grep -q "package.json"; then
  if ! echo "$FILES" | grep -q "package-lock.json"; then
    echo "⚠️  Warning: package.json changed but lock file wasn't updated"
    echo "Run: npm install"
  fi
fi

exit 0
```

---

## Registering Hooks

Hooks are registered in `.claude/settings.json`:

```json
{
  "hooks": {
    "pre_commit": ["validate-version.sh", "security-check.sh"],
    "post_commit": ["notify-team.sh"],
    "post_push": ["deploy-staging.sh"]
  }
}
```

Or in `settings.yaml`:

```yaml
hooks:
  pre_commit:
    - path: hooks/validate-version.sh
      description: "Check VERSION file updated"
      blocking: true
    - path: hooks/security-check.sh
      blocking: true
  post_commit:
    - path: hooks/notify-team.sh
      blocking: false
```

---

## Best Practices for Safe Hooks

### DO

✅ Make hooks **idempotent** (safe to run multiple times)
✅ Log what the hook is doing
✅ Exit with clear error messages
✅ Use `set -e` at top to fail on first error
✅ Make hooks executable: `chmod +x hook.sh`

### DON'T

❌ Make hooks take >5 seconds (blocks workflow)
❌ Have hooks make network calls (unreliable)
❌ Have hooks modify files (they validate only)
❌ Make hooks too strict (frustrate developers)
❌ Forget to test hooks locally first

---

## Safe Hook Template

```bash
#!/bin/bash
set -euo pipefail

# Hook template for safe, clear automation

HOOK_NAME="my-hook"
HOOK_VERSION="1.0.0"

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log_error() {
  echo -e "${RED}❌ $1${NC}"
}

log_warn() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

log_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

# Main validation logic
main() {
  echo "Running: $HOOK_NAME ($HOOK_VERSION)"
  
  # Your checks here
  if some_check_fails; then
    log_error "Check failed because X"
    return 1
  fi
  
  log_success "All checks passed"
  return 0
}

# Run and exit
main
exit $?
```

---

## Exercise: Create a Validation Hook

### Scenario

You want to prevent accidental commits with:
- Trailing whitespace
- Missing test files for new code
- Unresolved merge conflicts

### Step 1: Create the Hook

```bash
cat > .claude/hooks/pre-commit-validation.sh << 'EOF'
#!/bin/bash
set -euo pipefail

echo "🔍 Running pre-commit validation..."

# Check 1: No trailing whitespace
if git diff --cached | grep -E '^[+].*\s+$' > /dev/null; then
  echo "❌ Trailing whitespace found:"
  git diff --cached | grep -E '^[+].*\s+$'
  exit 1
fi

# Check 2: No merge conflict markers
if git diff --cached | grep -E '^[+].*<<<<<<|^[+].*======|^[+].*>>>>>>' > /dev/null; then
  echo "❌ Merge conflict markers found"
  exit 1
fi

# Check 3: New files should have tests
STAGED_FILES=$(git diff --cached --name-only)
for file in $STAGED_FILES; do
  if [[ $file == src/*.ts && $file != *test* ]]; then
    TEST_FILE="${file%.ts}.test.ts"
    if ! git ls-files | grep -q "$TEST_FILE"; then
      echo "⚠️  Warning: New file $file has no test file"
    fi
  fi
done

echo "✅ Pre-commit validation passed"
exit 0
EOF

chmod +x .claude/hooks/pre-commit-validation.sh
```

### Step 2: Register in settings.json

```json
{
  "hooks": {
    "pre_commit": ["hooks/pre-commit-validation.sh"]
  }
}
```

### Step 3: Test It

Make a file with trailing whitespace:

```bash
echo "test line   " > test.txt  # Note the trailing spaces
git add test.txt
```

Try to commit:

```bash
git commit -m "Test hook"
```

The hook blocks:

```
❌ Trailing whitespace found:
+test line
```

### Step 4: Fix and Retry

```bash
echo "test line" > test.txt  # Remove trailing spaces
git add test.txt
git commit -m "Test hook (fixed)"
```

Now it succeeds:

```
✅ Pre-commit validation passed
```

---

## Debugging Hooks

If a hook fails mysteriously:

1. **Run manually**:
```bash
bash .claude/hooks/my-hook.sh
```

2. **Add debug output**:
```bash
set -x  # Print every command
```

3. **Check exit code**:
```bash
bash .claude/hooks/my-hook.sh; echo "Exit: $?"
```

4. **Test hook conditions**:
```bash
# Test if a file was changed
git diff --cached --name-only | grep "VERSION"
echo $?  # 0 = found, 1 = not found
```

---

## Validation: You're Ready If...

✓ You've created at least one hook script

✓ You understand hook event types (pre-commit, post-commit, etc.)

✓ You can register hooks in settings.json or settings.yaml

✓ You've tested a hook locally

✓ You know what exit codes mean (0 = success, 1 = failure)

---

## What's Next?

**Module 07: Advanced Patterns** covers:
- Multi-agent orchestration
- Building complex workflows
- Error handling and recovery
- Production-grade automation
- Team coordination patterns

This teaches you how to combine all previous concepts into sophisticated multi-agent systems.

---

**Completed Module 06?** → Ready for [Module 07: Advanced Patterns](07-advanced.md)
