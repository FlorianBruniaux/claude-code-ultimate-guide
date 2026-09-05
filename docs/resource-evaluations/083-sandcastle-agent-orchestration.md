# Resource Evaluation: Sandcastle: Programmatic Agent Orchestration Library

**Date**: 2026-05-03
**Evaluator**: Claude (Sonnet 4.6)
**Source**: README (pasted content) — `@ai-hero/sandcastle`
**GitHub**: https://github.com/mattpocock/sandcastle
**Author**: Matt Pocock (Total TypeScript, TypeScript educator)
**Type**: TypeScript library / npm package

---

## Summary

TypeScript library for orchestrating AI coding agents in isolated sandboxes. Provides a programmatic JS/TS API for running agents (Claude Code, Codex, pi, opencode) inside Docker, Podman, or Vercel Firecracker containers, with built-in branch strategy management and a prompt templating system.

**Key capabilities**:
- `run()`, `createSandbox()`, `createWorktree()`, `interactive()` API with automatic resource cleanup (`await using`)
- Three branch strategies: `head` (direct write), `merge-to-head` (safe temp branch), `branch` (explicit named branch)
- Prompt system: `{{KEY}}` substitution + `` !`command` `` dynamic context injection
- Session capture and resume for Claude Code (JSONL auto-capture to host)
- 5 workflow templates: blank, simple-loop, sequential-reviewer, parallel-planner, parallel-planner-with-review
- Custom sandbox provider API (`createBindMountSandboxProvider`, `createIsolatedSandboxProvider`)

---

## Evaluation Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Relevance** | 4/5 | Real gap — no tool in guide covers programmatic sandboxed orchestration |
| **Originality** | 5/5 | Unique architecture (container-per-run + TS API + branch management) |
| **Authority** | 4/5 | Matt Pocock is credible; but @ai-hero namespace vs mattpocock/sandcastle repo is a signal of ongoing structure decisions |
| **Accuracy** | 5/5 | Primary source (README) — no secondary claims to verify |
| **Maturity** | 2/5 | v0.5.x, known bugs in Sequential Reviewer template, active breaking changes |

**Overall Score**: **3/5 (Watch)**

---

## Gap Analysis

### Not Covered in Guide

| Sandcastle Capability | Guide Coverage | Notes |
|----------------------|----------------|-------|
| Container-per-run isolation | ❌ | sandbox-isolation.md covers manual Docker setup, not orchestration API |
| Programmatic TS orchestration API | ❌ | Entirely absent |
| Branch strategy management | ❌ | Worktrees documented natively, not via library |
| Dynamic prompt templating (`!`cmd``) | ❌ | Not covered |
| Session capture/resume | Partial | `claude --resume` documented, not via library |
| parallel-planner workflow template | Partial | Ruflo covers parallel swarms, different model |

### Already Covered

| Sandcastle Feature | Guide Coverage | Location |
|-------------------|----------------|----------|
| Multi-agent parallel runs | ✅ | multiclaude, Ruflo — ai-ecosystem.md |
| Docker sandbox isolation | ✅ | sandbox-isolation.md |
| Agent orchestration frameworks | ✅ | Ruflo, Athena Flow — third-party-tools.md |

---

## Technical Writer Challenge

Challenge agent (Sonnet) recommended **downgrade to 3/5** based on:

1. **TypeScript-only barrier**: requires `npx tsx` setup; excludes Python/shell-first users; no other tool in the section imposes this
2. **Sandbox hard dependency**: Docker Desktop or Podman must be running; Vercel provider is separately billable; real blocker for corporate/CI environments
3. **API key model mismatch**: uses `ANTHROPIC_API_KEY` directly, not Claude Code's subscription session; costs run outside Max plan billing
4. **Architectural misclassification**: not an "orchestration framework" in the Ruflo sense; drives `claude` binary as subprocess inside a container (closer to CI agent runner)
5. **Active breaking changes**: v0.5.x with known bug: Sequential Reviewer template doesn't create branch correctly

**Recommendation**: Watch entry only. Full documentation would mislead readers evaluating production tooling.

**Accepted**: Score set to 3/5.

---

## Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| Author: Matt Pocock | ✅ | Perplexity confirms (TypeScript educator, Total TypeScript) |
| npm package: `@ai-hero/sandcastle` | ✅ | README explicit |
| Docker, Podman, Vercel providers | ✅ | README, dedicated sections |
| claudeCode(), codex(), pi(), opencode() | ✅ | README, RunOptions table |
| 5 workflow templates | ✅ | README, init CLI section |
| GitHub star count | ⚠️ | Perplexity cites ~1K (April 2026 article) — not in README, not cited |
| Version number | ⚠️ | Not in README — challenger cited v0.5.7 from training data, unconfirmed |

**Confidence**: High for capabilities, Medium for maturity signals (version/stars not in source).

---

## Integration Decision

**Action**: Watch — add to Known Gaps table in `third-party-tools.md`

**Rationale**:
- Tool exists and fills a real niche (TypeScript API + container-per-run + branch management)
- Not guide-ready: v0.5.x, active bugs, TypeScript-only, API key model different from CC auth
- Known Gaps entry signals the gap exists and points readers to the right tool when they search for it

**Revisit trigger**: v1.0.0 release, OR Sequential Reviewer bug fixed + GitHub issue #191 resolved (subscription auth support)

**Full entry location when ready**: `guide/ecosystem/third-party-tools.md` — new subsection "Programmatic Agent Runners" between the existing Multi-Agent Orchestration table and External Orchestration Frameworks

---

## References

**Source**: `@ai-hero/sandcastle` README
**Author**: Matt Pocock
**Related Guide Sections**:
- External Orchestration Frameworks: `third-party-tools.md:973`
- Sandbox isolation: `guide/security/sandbox-isolation.md`
- Multi-agent orchestration: `ai-ecosystem.md`
