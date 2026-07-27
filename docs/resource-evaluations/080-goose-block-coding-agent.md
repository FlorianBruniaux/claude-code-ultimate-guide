# Resource Evaluation #080 — Goose (Block): Open-Source AI Coding Agent

**Source:** [block.github.io/goose](https://block.github.io/goose) / [github.com/block/goose](https://github.com/block/goose)
**Type:** Open source tool (Apache 2.0) — on-machine AI coding agent
**Author:** Block (formerly Square) — maintained by Block's engineering team
**Evaluated:** 2026-03-17
**Maturity at evaluation:** Launched officially January 2025, 33,166 stars (now 51,819 as of 2026-07-28), 3,058 forks

---

## Summary

- **On-machine AI coding agent**: local-first CLI + desktop app, not cloud. Automates complex engineering tasks end-to-end
- **Model-agnostic**: works with Claude (recommended for tool calling), GPT-4o, Gemini, Groq, local models (Ollama) — 20+ providers
- **Recipes**: versionable, shareable, parameterized multi-step workflows. Distinct from "rules files" — recipes define what agents do, not how they behave
- **Subagent orchestration**: spawn specialized agents autonomously or via sub-recipes, with dynamic model switching per task/cost
- **1,700+ MCP servers** supported (first open source agent to support MCP, January 2025)
- **Goose Grant Program**: Block funds developers building Goose extensions (launched July 2025)
- **Custom Distributions**: teams can build branded Goose distros with preconfigured providers, extensions, and branding
- **Backed by Block** (Square, Cash App) — institutional engineering resources, not a solo project

---

## Status in the Guide

**Already documented**: `guide/ecosystem/ai-ecosystem.md` §11.1 "Goose: Open-Source Alternative (Block)"

**The entry exists and is structurally sound.** The issue is outdated data and two missing feature callouts.

---

## Relevance Score

| Score | Meaning |
|-------|---------|
| 5 | Essential — Major gap in the guide |
| **4** | **Very relevant — Significant improvement needed** |
| 3 | Pertinent — Useful complement |
| 2 | Marginal — Secondary information |
| 1 | Out of scope — Not relevant |

**Final score: 4/5 (Update existing entry)**

**Justification:** Goose is already documented. Score reflects the importance of keeping the entry current — at 33k stars (2x what the guide says), Goose is clearly not a niche alternative. The missing Recipes and subagent orchestration paragraphs are also directly relevant to a guide that extensively documents Claude Code's equivalent patterns (skills, slash commands, multi-agent).

---

## What Needs Updating in §11.1

### 1. Stats (outdated)

| Field | Current guide (Jan 2026) | Actual (Mar 2026) |
|-------|--------------------------|-------------------|
| GitHub Stars | 15,400+ | 33,166 (now 51,819 as of 2026-07-28) |
| MCP servers | 3,000+ (table) vs 1,700+ (inconsistency) | 1,700+ (per Goose docs) |
| Releases | 100+ | ~175+ (estimated, fast release cadence) |

**Fix**: Update the metrics table and resolve the 3,000 vs 1,700 MCP inconsistency.

### 2. Recipes — missing

Recipes are Goose's equivalent of Claude Code slash commands + skills combined. They are:
- Versionable, shareable as standalone workflows
- Importable via deeplinks
- Parameterized (reusable across contexts)
- Can be shared across teams

This is directly relevant to a guide section that extensively documents commands and skills. One paragraph with a cross-reference to §3 (commands) and §4 (skills) is warranted.

### 3. Subagent orchestration — missing

Goose's July 2025 roadmap introduced subagent orchestration: spawn specialized sub-agents (Planner, Architect, Frontend Dev, Backend Dev) with dynamic model switching per agent. Example from Berkeley Agentic AI Summit: 7 agents collaboratively built a full-stack app in under an hour.

This overlaps with Claude Code's own multi-agent patterns (§9). A one-paragraph callout with a comparison to Claude Code's Agent tool would help readers understand the architectural difference (Claude Code: single agent + Tool spawning vs Goose: recipe-defined multi-agent subflows).

### 4. agentskills.io — verify live status

The "Skill Portability" paragraph references agentskills.io. **Verified live** (2026-03-17). No change needed.

---

## Challenge (technical-writer agent)

**Score confirmed: 4/5 (update pass)**

Key points:
- 15.4k → 33k stars: 2x undercount signals the section hasn't been maintained. Trust erosion, not just a metric miss.
- MCP discrepancy (3,000 vs 1,700): one of these is wrong. Fix before any update goes live.
- Recipes and subagents absent: closest Goose analogy to Claude Code's skills + multi-agent. Should be documented.
- Risk of not updating: low urgency for readers, moderate for guide credibility as a current reference.
- Scope: 30-minute update pass, not a restructure.

---

## Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| 33,166 GitHub stars | Verified (now 51,819 as of 2026-07-28) | GitHub API (2026-03-17) |
| 3,058 forks | Verified | GitHub API |
| Apache 2.0 license | Verified | GitHub API + README |
| Rust (primary language) | Verified | GitHub API (`language: "Rust"`) |
| Created August 2024, launched Jan 2025 | Verified | GitHub API + "1 Year of goose" discussion (Jan 2026) |
| First open source agent to support MCP | Claimed | "1 Year of goose" GitHub discussion |
| 1,700+ MCP servers | Per Perplexity (sourced from Goose docs) | Cross-check recommended |
| Claude 3.5 Sonnet recommended for tool calling | Claimed | Perplexity search citing Goose docs |
| Goose Grant Program (July 2025) | Verified | block.xyz/inside/introducing-the-goose-grant-program |
| agentskills.io live | Verified | HTTP fetch (2026-03-17) |
| Dynamic model switching per subagent | Claimed | GitHub roadmap discussion #3319 |

**MCP server count discrepancy**: Guide says 3,000+ (comparison table), Perplexity reports 1,700+ from Goose docs. Need to check Goose documentation directly before updating. Use the more conservative figure if unsure.

---

## Final Decision

- **Final score**: 4/5
- **Action**: Update existing `guide/ecosystem/ai-ecosystem.md` §11.1 — stats refresh + Recipes paragraph + subagent orchestration paragraph
- **Confidence**: High on stats, medium on MCP server count (needs direct doc check)
- **Priority**: Medium — not urgent, but a 2x star count delta is worth fixing promptly
