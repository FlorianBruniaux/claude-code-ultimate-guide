# Resource Evaluation: Méthode Aristote — ai-instructions patterns

**Source**: Internal project — `/Users/florianbruniaux/Sites/MethodeAristote/app/doc/guides/ai-instructions/`
**Author**: Florian Bruniaux (same author as this guide)
**Date analyzed**: 2026-02-22
**Score**: 4/5

---

## Summary

Production patterns from the Méthode Aristote EdTech platform (5 developers, Claude Code + Cursor + Codex). The ai-instructions directory contains 24 files documenting team workflows, memory systems, tool-specific configurations, and governance policies. Several patterns were novel or better-documented than what existed in the guide.

---

## Scoring Grid

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Novelty** | 3/5 | Profile assembly + claude-mem already in guide; disclosure policy new |
| **Author credibility** | 5/5 | Same author, production data from real team |
| **Actionability** | 5/5 | Concrete configs, measured results, copy-pastable templates |
| **Accuracy** | 5/5 | Verified against actual codebase |
| **Depth** | 4/5 | Cost measurements, architectural decisions, failure modes |

**Overall: 4/5**

---

## Already Documented (no action needed)

| Pattern | Guide location |
|---------|---------------|
| Profile-based module assembly | Section 3.5 (comprehensive) |
| claude-mem basics | ~line 9140 |
| Search cascade (grepai → Serena → Context7 → Perplexity) | ~line 9308 |

---

## Gaps Identified and Fixed

### 1. AI Code Disclosure Policy
**Gap**: No team governance pattern for AI-generated code visibility.
**Fix**: Added section "AI Code Disclosure Policy" at end of Section 3.5.
**Content**: >10 lines threshold, PR template, graduated enforcement by level, anti-pattern warning.

### 2. claude-mem with Gemini (cost optimization)
**Gap**: Guide said "AI summarization via Claude" — missed the Gemini 2.5 Flash alternative ($14/month vs $102 Haiku, -86%).
**Fix**: Added "Cost optimization — use Gemini instead of Claude" block in claude-mem section.
**Data source**: `claude-mem-analysis-corrected.md` (553 sessions, ~400/month, measured costs).

### 3. claude-mem hooks coexistence
**Gap**: Installation instructions didn't warn about hooks array overwrite risk.
**Fix**: Added "Critical installation gotcha — hooks coexistence" with before/after JSON examples.
**Source**: `claude-mem-install-prompt.md` (6 existing hooks, explicit preservation checklist).

### 4. claude-mem fail-open (v9.1.0+)
**Gap**: No mention of reliability behavior when worker is down.
**Fix**: Added "Reliability: fail-open architecture" block with restart instructions.

---

## What Was Not Integrated

- Aristote-specific architecture (3-tier Router/Service/Repository) — too project-specific
- SSE real-time pattern — too domain-specific
- SonarQube MCP details — already exists in examples
- Multi-env .env.* pattern — marginal value, tips-level only
- Specific team profiles (florian.yaml, nico.yaml) — not generalizable

---

## Attribution

Internal source — Méthode Aristote project (`/app/doc/guides/ai-instructions/`). Same author as guide. Analysis performed 2026-02-22.
