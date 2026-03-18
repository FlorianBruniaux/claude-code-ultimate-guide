# Resource Evaluation: "AGENTS.md Outperforms Skills in Our Agent Evals"

**Date**: 2026-01-30
**Evaluator**: Claude (Opus 4.5)
**URL**: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
**Author**: Jude Gao (Vercel)
**Publication Date**: January 27, 2026

---

## Summary

Vercel blog post comparing four documentation strategies for coding agents on 19 Next.js 16 tasks (APIs not in model training data). Finds that a static AGENTS.md docs index achieves 100% pass rate vs skills at 79% (with explicit instructions) or 53% (without, equal to baseline). Core finding: skills were only auto-invoked 56% of the time. A compressed 8KB index (reduced from ~40KB) maintained full performance.

**Key metrics**:

| Configuration | Pass Rate |
|---------------|-----------|
| Baseline (no docs) | 53% |
| Skills (default) | 53% (+0pp) |
| Skills (with instructions) | 79% (+26pp) |
| AGENTS.md docs index | 100% (+47pp) |

**Detailed breakdown** (Build / Lint / Test):
- AGENTS.md: 100% / 100% / 100%
- Skills + instructions: 95% / 100% / 84%
- Baseline: 84% / 95% / 63%

---

## Evaluation Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Relevance** | 3/5 | Validates existing CLAUDE.md architecture; indirect (Claude Code ≠ AGENTS.md) |
| **Originality** | 4/5 | First quantified benchmark of eager vs lazy context loading in coding agents |
| **Authority** | 3/5 | Vercel employee, transparent methodology, but conflict of interest (see below) |
| **Accuracy** | 5/5 | All 13 claims fact-checked and verified against source |
| **Actionability** | 3/5 | 3 surgical insertions in existing guide sections |

**Overall Score**: **3/5 (Pertinent)**

---

## Gap Analysis

### Already Covered in Guide

| Article Concept | Guide Coverage | Location |
|-----------------|----------------|----------|
| Always-loaded context files | CLAUDE.md architecture | ultimate-guide.md:4074-4080 |
| CLAUDE.md sizing (4-8KB) | Size guideline | ultimate-guide.md:3527 |
| Skills as lazy-loaded modules | Memory Loading Comparison | ultimate-guide.md:4074-4080 |
| skills.sh marketplace | Full documentation | ultimate-guide.md:5606-5694 |

### What's New

- **56% invocation rate**: First quantified data on skill auto-discovery failure rate
- **8KB compression benchmark**: 5x compression (40KB → 8KB) with zero performance loss
- **Eager vs lazy evidence**: First empirical data supporting always-loaded context over on-demand skills for critical instructions

---

## Fact-Check Results

| Claim | Verified | Source |
|-------|----------|--------|
| Author: Jude Gao | ✅ | Article byline |
| Date: January 27, 2026 | ✅ | Article metadata |
| AGENTS.md 100% pass rate | ✅ | Article table |
| Skills + instructions: 79% | ✅ | Article table |
| Baseline: 53% | ✅ | Article table |
| Compressed index: 8KB | ✅ | Article text |
| Original size: ~40KB | ✅ | Article ("around 40KB") |
| Skills invoked 56% of time | ✅ | Article text |
| Next.js 16 APIs | ✅ | Article (multiple references) |
| 12 APIs listed | ✅ | All enumerated in article |
| Command: npx @next/codemod@canary agents-md | ✅ | Article code block |
| Build/Lint/Test breakdown (all configs) | ✅ | Article detailed table |
| Skills without instructions = baseline | ✅ | Both at 53% |

**Confidence**: High (13/13 claims verified directly in source article + Perplexity cross-check)

---

## Technical Writer Challenge

Agent challenged the evaluation from a documentation perspective:

**Key arguments**:
1. **Score correct at 3, not 4**: The article confirms existing guidance rather than introducing new guidance. A user reading our guide is already doing the right thing.
2. **56% is the real finding**: The headline buries the lead. Skills fail because agents don't discover them, not because skill content is bad. Claude Code already solved this with always-loaded CLAUDE.md.
3. **Sample too small**: 19 tasks, ~4 task difference between 100% and 79%. Not statistically robust for broad conclusions.
4. **Self-serving narrative**: Vercel operates skills.sh AND authored the AGENTS.md codemod. They're deprecating one positioning and upselling another under the cover of transparency.
5. **Integration scope correct**: 3-5 lines, no dedicated section needed.

**Score adjustment**: None (3/5 confirmed)

---

## System Architect Challenge

Agent challenged the evaluation from an architectural perspective:

**Key arguments**:
1. **Correct score, wrong reasoning**: "Validates our choices" is a non-argument. What saves the 3/5 is the compression benchmark — the only actionable data point.
2. **Missing architectural pattern**: The article demonstrates the **eager loading vs lazy invocation** trade-off. The guide documents this factually (line 4074-4080 table) but never names the pattern or provides empirical evidence for it.
3. **Plan under-specified**: Original "3-5 lines, 2 sections" is a placeholder. Correct plan: **3 lines, 3 specific locations** (lines 3527, 4082, 5641).
4. **Missing compression technique**: The guide says "keep it concise" but never shows *how* to compress. The 5x compression (40KB → 8KB) with zero loss is actionable guidance the guide lacks.
5. **Decision criteria gap**: The guide's loading table (line 4074) lacks a **criticality criterion** — if instructions are critical, use CLAUDE.md (eager, 100% loaded); if supplementary, skills suffice (lazy, 56% invocation acceptable).

**Score adjustment**: None (3/5 confirmed), but integration plan upgraded to 3 precise locations.

---

## Conflict of Interest Note

Vercel operates skills.sh (the skills marketplace) and authored the `npx @next/codemod@canary agents-md` tool evaluated in this article. The article concludes that their own skills.sh platform underperforms compared to AGENTS.md. While this appears intellectually honest (arguing against their own product), Vercel is positioning a different Vercel tool as the replacement. The methodology is transparent and reproducible, so this is noted as context rather than a disqualifier.

---

## Integration Plan

Three surgical insertions in existing sections:

### 1. CLAUDE.md Sizing (line ~3527)
Add compression benchmark after the size guideline paragraph.

### 2. Memory Loading Key Insight (line ~4082)
Add warning about skill invocation reliability after the existing key insight.

### 3. Skills Trade-offs (line ~5652)
Add bullet about invocation reliability.

---

## Decision

| Aspect | Verdict |
|--------|---------|
| **Score** | 3/5 (unanimous across 2 challenger agents) |
| **Action** | Integrate (3 lines, 3 sections) |
| **Confidence** | High (13/13 fact-checked + double challenge) |
| **Priority** | Low (confirms existing architecture) |
| **Transferable insights** | 56% invocation rate, 8KB compression benchmark, eager vs lazy evidence |
