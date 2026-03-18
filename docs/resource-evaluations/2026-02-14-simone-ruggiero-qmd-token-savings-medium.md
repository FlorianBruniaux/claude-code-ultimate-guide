# Evaluation: Simone Ruggiero - qmd Token Savings (Medium)

**Date**: 2026-02-14
**Evaluator**: Claude Opus 4.6
**Source Type**: Medium article (tool promotion)
**Verdict**: ⚠️ **MARGINAL** (Score: 2/5)

---

## Summary

Simone Ruggiero (Feb 1, 2026) promotes **qmd** (github.com/tobi/qmd), a local document indexer exposed as an MCP server for Claude Code. Main claim: "95% token savings" by replacing Glob/Grep/Read with indexed semantic searches. The tool indexes codebases locally and serves results via MCP, allowing Claude Code to query an index instead of reading raw files.

**Key claim**: Replace native Claude Code file operations with indexed lookups to reduce token consumption by ~95%.

**Source**: [Medium Article](https://medium.com/@simone.ruggiero92) (exact URL from Feb 2026)

---

## Content Summary

**Main Points**:
- **qmd** is a local document indexer by Tobi Lutke (Shopify CEO)
- Exposes a Model Context Protocol (MCP) server for Claude Code
- Claims 95% token savings on file exploration operations
- Token math scenario: 500-line file = ~10K tokens via Read → qmd returns ~500 tokens (summary/chunks)
- Positions qmd as replacement for Glob + Grep + Read workflow
- Setup: `qmd index .` then configure as MCP server in Claude Code settings

---

## Fact-Check Results

| Claim | Verified | Verdict |
|-------|----------|---------|
| **"95% token savings"** | ⚠️ UNVERIFIABLE | No benchmark methodology, no reproducible test. Percentage depends entirely on query type, codebase size, and what "savings" means (input tokens? output? both?) |
| **"qmd by Tobi Lutke"** | ✅ TRUE | github.com/tobi/qmd exists, authored by Tobi Lutke (Shopify) |
| **"MCP server for Claude Code"** | ✅ TRUE | qmd does expose an MCP interface |
| **"500 lines = 10K tokens"** | ⚠️ MISLEADING | Assumes every file read sends full content. Claude Code already has intelligent context management and doesn't blindly read entire files |
| **"Replaces Glob/Grep/Read"** | ⚠️ OVERSIMPLIFIED | Semantic search complements but doesn't replace exact pattern matching (Grep) or file discovery (Glob) |

### Factual Corrections

**Major issue**: The 95% claim assumes a worst-case baseline (reading entire files raw) and compares against best-case indexed retrieval. Real-world savings depend on:
1. Whether Claude Code would have read the full file anyway (often it reads specific line ranges)
2. Whether the semantic index returns the right chunks (precision matters)
3. Whether the query requires exact matching (where Grep is superior)

**Context missing**: Article doesn't mention that Claude Code already optimizes token usage via:
- Line-range reads (offset + limit parameters)
- Targeted Grep searches (returns only matching lines)
- reference.yaml pattern (machine-readable index, ~2K tokens)

---

## Scoring & Decision

### Score: **2/5** (Marginal)

**Scoring Grid**:

| Criterion | Score | Justification |
|-----------|-------|---------------|
| **Source Credibility** | 2/5 | Medium article, author has no established Claude Code expertise. Tool itself is from credible author (Tobi Lutke) but article is promotional |
| **Factual Accuracy** | 2/5 | Core claim (95%) unverifiable, misleading baseline comparison, missing context about existing optimizations |
| **Timeliness** | 3/5 | Recent (Feb 2026), MCP ecosystem is active topic |
| **Practical Value** | 2/5 | Concept valid (semantic indexing) but already covered by existing tools (grepai MCP) |
| **Novelty** | 2/5 | Semantic code search MCP already exists (grepai), reference.yaml pattern already documented |
| **Completeness** | 1/5 | No benchmarks, no comparison with alternatives, no discussion of trade-offs or limitations |

**Weighted Average**: (2+2+3+2+2+1)/6 = **2.0/5**

---

## Comparative Analysis

| Aspect | qmd | grepai (MCP) | reference.yaml |
|--------|-----|-------------|----------------|
| **Type** | Local indexer + MCP | Semantic search MCP | Static YAML index |
| **Setup** | `qmd index .` + MCP config | MCP server config | Manual maintenance |
| **Search type** | Semantic (embeddings) | Semantic (embeddings) | Key-value lookup |
| **Token cost** | ~500 tokens/query (claimed) | ~500 tokens/query | ~2K tokens (full load) |
| **Exact matching** | No (semantic only) | No (semantic only) | No (manual keys) |
| **Freshness** | Re-index required | Auto-indexed | Manual updates |
| **Already in guide?** | No | No (but used in this project) | Yes (documented pattern) |
| **Unique value** | None over grepai | Callgraph tracing, callers/callees | Human-curated, zero dependencies |

**Key finding**: qmd and grepai solve the same problem (semantic code search via MCP). For users already using grepai, qmd adds zero value. For users without either tool, the guide already documents the reference.yaml pattern as a lightweight alternative.

---

## Why NOT Integrate

1. **Already covered**: Semantic code search MCP = grepai (same capability, already available)
2. **Unverifiable claims**: 95% savings claim has no benchmark, no methodology, no reproducible test
3. **Misleading baseline**: Compares against worst-case (full file reads) while ignoring Claude Code's existing optimizations
4. **No unique contribution**: Doesn't add new concepts beyond "use an indexer" which is already a known pattern
5. **Promotional tone**: Article reads as tool promotion, not technical analysis

---

## Final Decision

- **Score**: **2/5** (Marginal - Do not integrate)
- **Action**: **NOT APPROVED** - No integration, no watch-list addition
- **Confidence**: **High** (concept valid but redundant with existing tools and patterns)

### What Would Change This Score?

- **Independent benchmarks** comparing qmd vs grepai vs native Claude Code operations → could justify a mention
- **Unique feature** not available in grepai (e.g., cross-repo indexing, natural language queries with context) → could merit evaluation
- **Adoption signal** from Claude Code community (multiple practitioners reporting real savings) → could revisit

---

**Evaluation completed**: 2026-02-14
**Result**: Score 2/5 rejected. Concept valid (semantic indexing reduces tokens) but already covered by grepai MCP and reference.yaml pattern. Core claim (95% savings) is unverifiable and uses misleading baseline. No integration into guide.
