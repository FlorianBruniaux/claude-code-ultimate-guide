---
title: "drona23/claude-token-efficient — CLAUDE.md output verbosity template"
type: "github-repo"
date: "2026-03-31"
score: 3
action: "monitor-then-integrate-framing"
sources:
  - "https://github.com/drona23/claude-token-efficient"
  - "GitHub API (metadata, README, CLAUDE.md, profiles, BENCHMARK.md)"
---

# drona23/claude-token-efficient

## Summary

Universal `CLAUDE.md` template (~15 rules) targeting Claude **output behavior** — not input context. Core
rules: no sycophantic openers/closers, no em dashes or Unicode, no unsolicited suggestions, no scope creep,
no speculation when uncertain. Three domain profiles included: `CLAUDE.coding.md`, `CLAUDE.agents.md`,
`CLAUDE.analysis.md`.

Key conceptual framing: input tokens and output tokens are separate cost axes. Most practitioners optimize
input (context loading, compaction, RTK). Output behavior shaping via CLAUDE.md rules is underexplored.

Claimed ~63% output token reduction. Benchmark: 5 prompts, no repeated runs, no variance controls. Author
explicitly acknowledges this in BENCHMARK.md: "directional indicator only, not a statistically controlled
study." The headline figure should not be cited.

- **Stars**: 865 (in ~24h, likely HN or newsletter spike, now 5,884 as of 2026-07-28 with sustained growth)
- **Forks**: 33
- **Created**: 2026-03-30 (one day old at time of evaluation)
- **Author**: Drona Gangarapu

## Score: 3/5

**Justification**: The conceptual gap is real. The guide has 305 CLAUDE.md references — all focused on
project context, conventions, and memory. Zero coverage of output behavior shaping as a cost or workflow
lever. This resource names the gap clearly. However, the actual CLAUDE.md content is thin (~15 minimal
rules), the benchmark is weak, and the repo is one day old. Score held at 3 by the framing value, not the
template.

## Gap Analysis

### Already Covered in Guide

| Topic | Location |
|-------|----------|
| CLAUDE.md structure and hierarchy | §3.1, lines 75-128 |
| Input token optimization (RTK, compaction) | §7.5, lines 17351-17525 |
| Profile-based module assembly | lines 5784-6101 |
| CLAUDE.md caching behavior | line 2337 |

### Not Covered (Real Gap)

| Gap | Impact |
|-----|--------|
| Output behavior shaping via CLAUDE.md rules | Anti-sycophancy, hollow closers, scope creep — none documented |
| Input vs output token cost as separate optimization axes | Guide treats token efficiency as one axis |
| Anti-sycophancy rules for agentic loops | Claude adding unsolicited suggestions between task steps is a real agentic workflow pain |

## Fact-Check

| Claim | Status | Notes |
|-------|--------|-------|
| 865 stars, 33 forks | Verified | GitHub API 2026-03-31 |
| Created 2026-03-30 | Verified | GitHub API `created_at` |
| ~63% output token reduction | Weak | 5 prompts, no repeats — author admits: "directional indicator only" |
| CLAUDE.md read automatically by Claude Code | Verified | Official docs + guide §3.1 |
| "Most Claude costs = input tokens" | Plausible | Consistent with Anthropic pricing (input cheaper/token but dominates volume) |
| 3 profiles (coding, agents, analysis) | Verified | GitHub API repo contents |
| GitHub issues cited (#3382, #14759, #9340...) | Not verified individually | Plausible given Claude Code issue volume |

No hallucinations detected. README is honest about benchmark limitations.

## Integration Recommendation

**Do not integrate now. Monitor 2-3 weeks.**

The repo is 1 day old. 865 stars in 24h is hype velocity from a high-traffic forum post, not a validated
signal. Wait for community stress-testing before citing.

**When ready, integrate the conceptual framing only:**

- **Where**: `guide/ultimate-guide.md` §3.1 CLAUDE.md section — add a "Output Behavior Optimization"
  subsection
- **What to include**:
  - The input/output cost split framing (novel angle for the guide)
  - Anti-sycophancy rules list (5-6 concrete examples)
  - Agentic loop angle: Claude adding unsolicited steps between agent tasks
  - Honest caveat: output savings only offset CLAUDE.md input cost at high output volume
- **What to exclude**: the 63% stat, the CLAUDE.md template verbatim (too thin), the profiles (guide
  already covers this more thoroughly)

**Priority**: Low-Medium. The gap is real but not urgent.

## Challenge Notes (technical-writer review)

- 3/5 confirmed. +1 rejected: benchmark too weak to justify higher score.
- Key risk of non-integration: guide becomes the Claude Code reference while missing an optimization axis
  practitioners are independently discovering — slow credibility erosion.
- The agentic loop angle (Claude inserting unsolicited suggestions between pipeline steps) is more valuable
  than the pure cost framing and should lead the integration when it happens.
- Do not cite the repo as source for any stat. Frame as community-discovered patterns.