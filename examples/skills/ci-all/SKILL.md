---
name: ci-all
description: "Run the local test suite and type check, push the current branch, and return the pipeline URL. Use before opening a PR."
argument-hint: "[--skip-tests | --e2e]"
allowed-tools: [Bash]
model: haiku
effort: medium
disable-model-invocation: true
---

# /ci-all: Full CI before PR

Runs everything in order: local tests → type check → push → pipeline URL.

One `/ci-all` replaces: manual tests + git push + copying the pipeline URL. It pushes, so it runs only when you invoke it.

## Stack detection

```bash
if [ -f "uv.lock" ]; then STACK="python"
elif [ -f "pnpm-lock.yaml" ]; then STACK="node"
elif [ -f "package-lock.json" ]; then STACK="node-npm"
elif [ -f "Cargo.toml" ]; then STACK="rust"
fi
```

Refuse to run on `main`, `master` or `production`: tell the user to switch to a feature branch.

## Step 1: Local tests (blocking)

Run each command on its own and stop at the first failure: a failing step means do not push.

**Python (uv/pytest):**
```bash
uv run pytest --tb=short -q
# Failure → STOP + print failing tests
```

**Node (pnpm/vitest):**
```bash
pnpm vitest run
pnpm tsc --noEmit
# Failure → STOP
```

**Rust:**
```bash
cargo test --quiet 2>&1
```

If `--skip-tests` is passed → skip to step 2. If `--e2e` is passed, also run the project's E2E command when the repo defines one (for example a `test:e2e` script), and say so when none exists.

## Step 2: Push + pipeline

```bash
BRANCH=$(git branch --show-current)

# Verify commits exist to push
AHEAD=$(git rev-list --count origin/$BRANCH..HEAD 2>/dev/null || echo "1")
if [ "$AHEAD" = "0" ]; then
  echo "Branch already up to date on origin."
else
  git push origin "$BRANCH"
fi
```

## Step 3: Pipeline URL

### GitLab CI

```bash
REMOTE=$(git remote get-url origin)
WEB_URL=$(echo "$REMOTE" | sed 's/git@gitlab\.com:/https:\/\/gitlab.com\//' | sed 's/\.git$//')
echo "Pipeline: $WEB_URL/-/pipelines?ref=$BRANCH"

# Optional: live status via glab CLI
if command -v glab &>/dev/null; then
  sleep 3
  glab ci status --branch "$BRANCH" 2>/dev/null || true
fi
```

### GitHub Actions

```bash
REMOTE=$(git remote get-url origin)
WEB_URL=$(echo "$REMOTE" | sed 's/git@github\.com:/https:\/\/github.com\//' | sed 's/\.git$//')
echo "Actions: $WEB_URL/actions?query=branch%3A$BRANCH"

# Optional: live status via gh CLI
if command -v gh &>/dev/null; then
  sleep 5
  gh run list --branch "$BRANCH" --limit 3 2>/dev/null || true
fi
```

## Expected output

```
CI: my-app (Node/Vitest)
──────────────────────────

① Local tests
  ✅ 47 passed in 8.2s

② Type check
  ✅ No errors

③ Push
  ✅ origin/feat/my-feature

④ Pipeline
  🔗 https://gitlab.com/org/my-app/-/pipelines?ref=feat/my-feature

Next step: open a PR or MR on the forge.
```

If tests fail:
```
CI: my-api (Python/pytest)
────────────────────────────

① Local tests
  ❌ 2 failed

  FAILED tests/test_orders.py::TestOrderService::test_refund_validation
  AssertionError: expected 400, got 500

→ Fix tests before pushing. Pipeline not triggered.
```

## Usage

```
/ci-all
/ci-all --skip-tests    # push without re-running tests
/ci-all --e2e           # include E2E tests (if configured)
```

Target: $ARGUMENTS