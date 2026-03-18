---
title: "RTK Token Optimization Template"
description: "CLAUDE.md configuration for minimizing token consumption with RTK CLI proxy"
tags: [claude-md, template, performance]
---

# RTK Token Optimization

**Context**: Using RTK (Rust Token Killer) to minimize token consumption from command outputs.

## Commands to Optimize

Always use RTK wrapper for these high-verbosity commands:

### Git Operations (92.3% avg reduction)
- `rtk git log` instead of `git log`
- `rtk git status` instead of `git status`
- `rtk git diff` instead of `git diff`

### File Operations (69.4% avg reduction)
- `rtk find "*.md" .` instead of `find . -name "*.md"`
- `rtk read <file>` instead of `cat <file>` (for large files >10K lines)
- `rtk ls .` instead of `ls -la`
- `rtk grep "pattern"` instead of `grep -r "pattern"`

### JS/TS Stack (70-90% reduction)
- `rtk vitest run` instead of `pnpm test`
- `rtk pnpm list` instead of `pnpm list`
- `rtk pnpm outdated` instead of `pnpm outdated`
- `rtk prisma migrate status` instead of `pnpm prisma migrate status`

### Rust Toolchain (80-90% reduction)
- `rtk cargo test` instead of `cargo test`
- `rtk cargo build` instead of `cargo build`
- `rtk cargo clippy` instead of `cargo clippy`

### Python (90% reduction)
- `rtk python pytest` instead of `pytest`

### Go (90% reduction)
- `rtk go test` instead of `go test`

### GitHub CLI (79-87% reduction)
- `rtk gh pr view <num>` instead of `gh pr view <num>`
- `rtk gh pr checks <num>` instead of `gh pr checks <num>`

## Token Savings Target

**Baseline**: ~150K tokens per 30-min session
**With RTK**: ~45K tokens (70% reduction)

## Installation

```bash
# Homebrew (macOS/Linux)
brew install rtk-ai/tap/rtk

# Cargo (all platforms)
cargo install rtk

# Hook-first install
rtk init
```

## Verification

Check RTK availability:
```bash
rtk --version  # Should show: rtk 0.16.0+
```

## When NOT to use RTK

- Quick exploration (1-2 commands): overhead not worth it
- Already using tools like Grep/Read (Claude native tools are optimized)
- Small outputs (<100 chars): minimal gain

## Automation

Use RTK automatically via hook (see `.claude/hooks/bash/rtk-wrapper.sh`) or `rtk init` for hook-first setup.
