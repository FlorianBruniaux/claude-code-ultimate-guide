# CI commands

Slash commands for CI/CD workflows. Auto-detect stack (Python/Node/Rust) and support both GitLab CI and GitHub Actions.

## Commands

| Command | Description |
|---------|-------------|
| `/ci:all` | Full pipeline: tests + type check + push + pipeline URL. The only command you need before a PR. |
| `/ci:tests` | Run the test suite. Auto-detects pytest, vitest, cargo test. |
| `/ci:pipeline` | Push current branch and return the pipeline tracking URL. |
| `/ci:status` | Show current pipeline status for the active branch. |

## Usage pattern

```
# Before every PR:
/ci:all

# Run only tests:
/ci:tests
/ci:tests tests/test_billing.py   # specific file

# Check pipeline after push:
/ci:status
/ci:status 42   # specific MR/PR number

# Push without re-running tests (e.g. doc-only change):
/ci:all --skip-tests
```

## Stack support

| Stack | Test command | Type check |
|-------|-------------|------------|
| Python + uv | `uv run pytest --tb=short -q` | mypy (optional) |
| Node + pnpm | `pnpm vitest run` | `pnpm tsc --noEmit` |
| Node + npm | `npm test` | `npx tsc --noEmit` |
| Rust | `cargo test --quiet` | `cargo clippy` |

## CI platform support

Both commands support **GitLab CI** (via `glab` CLI) and **GitHub Actions** (via `gh` CLI).
If neither CLI is installed, the commands fall back to showing the pipeline URL.