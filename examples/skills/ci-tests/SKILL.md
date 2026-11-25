---
name: ci-tests
description: Run the test suite for the current repo, auto-detecting Python (pytest/uv), Node (vitest/pnpm), or Rust (cargo test)
argument-hint: "[file or folder target]"
allowed-tools: [Bash]
model: haiku
effort: low
disable-model-invocation: true
---

# /ci-tests: Run tests

Detects the stack and runs tests with the right command.

## Stack detection

```bash
if [ -f "uv.lock" ]; then
  STACK="python"
elif [ -f "pnpm-lock.yaml" ]; then
  STACK="node"          # pnpm + vitest
elif [ -f "package.json" ]; then
  STACK="node-npm"      # npm test (jest or the repo's own runner)
elif [ -f "Cargo.toml" ]; then
  STACK="rust"
else
  STACK="unknown"
fi
```

## Commands by stack

### Python (uv + pytest)

```bash
# All tests
uv run pytest --tb=short -q $ARGUMENTS

# With coverage
uv run pytest --cov=src --cov-report=term-missing -q

# Specific file or folder
uv run pytest $ARGUMENTS -v
```

### Node (pnpm + vitest)

```bash
# All tests
pnpm vitest run $ARGUMENTS

# With coverage
pnpm vitest run --coverage

# Watch mode (dev)
pnpm vitest
```

### Node (npm + jest)

```bash
npm test -- --passWithNoTests $ARGUMENTS
```

### Rust (cargo)

```bash
cargo test --quiet $ARGUMENTS 2>&1
```

## Expected output

```
Tests: my-api (Python/pytest)
───────────────────────────────

uv run pytest --tb=short -q

[pytest output]

✅ 42 passed in 3.1s  →  Ready to push
```

On failure:
```
❌ 2 failed

FAILED tests/test_billing.py::TestInvoice::test_promo_expired
AssertionError: expected discount=0, got discount=10

→ Fix before pushing.
```

## Usage

```
/ci-tests
/ci-tests tests/test_orders.py
/ci-tests src/components/Button.test.tsx
```

Target: $ARGUMENTS