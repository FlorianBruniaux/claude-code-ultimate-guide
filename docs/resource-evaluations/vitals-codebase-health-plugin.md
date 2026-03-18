# Resource Evaluation: Vitals — Codebase Health Plugin

**Date**: 2026-03-06
**Evaluator**: Claude (Sonnet 4.6) via /eval-resource
**Source**: LinkedIn post (text) + GitHub repo
**GitHub**: https://github.com/chopratejas/vitals
**Author**: Tejas Chopra
**Score**: 3/5 (Pertinent)
**Decision**: Integrated into guide/ultimate-guide.md §8.5

---

## Summary

Vitals is a Claude Code plugin (v0.1 alpha, MIT, Python stdlib + git) that identifies code hotspots using a composite metric: `git churn × structural complexity × coupling centrality`. Claude then reads the flagged files and provides semantic diagnosis rather than raw metrics.

**Key points**:
1. Computes churn × complexity × coupling centrality — no linter does this combination
2. Claude reads top-flagged files: diagnosis says "this class handles routing, caching, rate limiting, AND metrics in 7,137 lines" not just "high complexity"
3. Background tracking of AI-generated edits via PostToolUse hooks
4. Zero dependencies, zero API keys — Python stdlib + git only
5. v0.1 alpha: core detection works, trend tracking planned for v0.2+

---

## Evaluation Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Relevance** | 3/5 | Addresses real AI code quality problem, original approach |
| **Originality** | 4/5 | churn×complexity×centrality not covered elsewhere in guide |
| **Authority** | 2/5 | New author, v0.1 alpha, limited community validation |
| **Accuracy** | 4/5 | Methodology sound; post had one misquoted stat (see fact-check) |
| **Actionability** | 4/5 | Install + use in 2 commands |

**Overall Score**: **3/5 (Pertinent)**

---

## Gap Analysis

### Already Covered in Guide

| Concept | Guide Coverage | Location |
|---------|----------------|----------|
| AI code quality degradation | GitClear stats, comprehension debt | quiz/questions, learning-with-ai.md |
| Plugin system | Full section 8.5 | ultimate-guide.md:12015 |
| SE-CoVe plugin example | Full documentation | examples/plugins/se-cove.md |

### What's New

- **Hotspot identification methodology**: `churn × complexity × coupling centrality` as a composite metric — not in guide
- **Concrete tool** that maps the "AI code debt" problem to actionable file-level output
- **Bus factor / knowledge risk** metric — unique angle not documented
- **PostToolUse hook for AI provenance tracking** — interesting hook usage pattern

---

## Fact-Check Results

| Claim | Verified | Note |
|-------|----------|------|
| "41% of code is now AI-generated" | ❌ INCORRECT | GitClear actual stat: AI code has **41% higher churn**, not 41% of code volume. Post misquotes the stat. |
| "Refactoring collapsed from 25% to under 10%" | ✅ | GitClear 211M lines, 2021–2025, confirmed via Perplexity |
| "GitClear's research on 211M lines" | ✅ | Confirmed |
| "METR's RCT showed 20% faster perception, 19% slower reality" | ✅ | METR RCT (Jul 2025, 16 devs, 246 tasks): estimated +20-24%, actual -19% |
| "Zero dependencies, Python stdlib + git" | ✅ | README confirms |
| v0.1 alpha status | ✅ | README confirms |

**Key correction**: The post's "41% of code is now AI-generated" is a misquote. The guide documents this correctly as "AI-generated code has 41% higher churn."

---

## Integration Actions

1. ✅ Added "Featured Community Plugins" subsection to `guide/ultimate-guide.md` §8.5 (~line 12385)
   - Vitals section with install commands, use cases
   - SE-CoVe section (updated from existing coverage)
   - Vitals vs. SE-CoVe comparison table
2. ✅ Updated `machine-readable/reference.yaml` with Vitals entry (install, command, purpose, status)

---

## Metadata

```yaml
evaluated_by: Claude (Sonnet 4.6)
skill_used: /eval-resource
perplexity_used: Yes (fact-check GitClear + METR stats)
changes_made:
  - guide/ultimate-guide.md (§8.5 Featured Community Plugins)
  - machine-readable/reference.yaml (plugins_vitals, plugins_se_cove_detail)
  - docs/resource-evaluations/vitals-codebase-health-plugin.md (this file)
integration_decision: Integrated (score 3/5)
```
