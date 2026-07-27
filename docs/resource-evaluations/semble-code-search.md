# Evaluation: Semble (MinishLab/semble)

**Resource**: Semble, semantic code search MCP server
**Source**: [github.com/MinishLab/semble](https://github.com/MinishLab/semble)
**Author**: MinishLab (Oslo-based research team behind Model2Vec)
**License**: MIT
**Version evaluated**: v0.3.3 (2026-06-05)
**Evaluated**: 2026-06-10
**Evaluator**: Claude Opus 4.8

---

## Executive Summary

| Criterion | Value |
|-----------|-------|
| **Initial Score** | 3/5 |
| **Score after challenge** | 3/5 (maintained) |
| **Final Decision** | Integrate: one entry in `mcp-servers-ecosystem.md` Code Search section, positioned as the no-Ollama alternative to grepai |

---

## What It Is

Semble is a Python-based semantic search tool with a native Claude Code MCP server. It searches across code, documentation, and configuration files in a repository. On first run it builds a local index using Model2Vec embeddings plus BM25 ranking, fused with RRF (Reciprocal Rank Fusion). Subsequent searches hit the cached index.

Key facts, verified against the repo:

| Attribute | Details |
|-----------|---------|
| **Stars** | ~5,000 (now 5,718 as of 2026-07-28, MIT, active development) |
| **Install** | `pip install semble` then `semble mcp` |
| **MCP integration** | Native server, no wrapper layer |
| **Requires Ollama** | No. Model2Vec runs CPU-only, no external service |
| **Index** | Built on first run, cached automatically. NOT index-free (correcting a common misconception in community posts). |
| **Scope** | Code + documentation + configuration files |
| **Claimed savings** | ~98% fewer tokens vs grep + read |

---

## Scoring Breakdown

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Relevance to CC users | 4/5 | Native MCP server, direct Claude Code integration, addresses token-heavy codebase search |
| Novelty vs. guide | 3/5 | grepai already documented in mcp-servers-ecosystem.md:826. Semble is a different implementation with distinct dependencies. |
| Technical quality | 4/5 | MIT, 5k stars, active releases (v0.3.3 June 2026), built on peer-reviewed Model2Vec |
| Actionability | 4/5 | `pip install semble && semble mcp` is the full setup. No Ollama, no API key, no external service. |
| Engineering patterns | 2/5 | No new patterns. Same semantic-search-via-MCP pattern as grepai. |

**Initial score: 3/5**

---

## Critical Fact: Semble Requires an Index

Community posts (including the one that prompted this evaluation) describe Semble as "without index, therefore compatible with worktrees." This is false. The Semble README states explicitly: "It requires building an index on first run, then caches it automatically."

This matters for two reasons. First, the "worktree-compatible" claim collapses: each new worktree requires its own index build. Second, the differentiation with grepai is not "index-free vs. index-based" but rather "no external service vs. Ollama required." The latter is a real distinction, even if the former is not.

No guide content should describe Semble as index-free.

---

## Comparison with Documented Alternatives

| Aspect | grepai | Semble |
|--------|--------|--------|
| Semantic search | Yes (Ollama + nomic-embed-text) | Yes (Model2Vec, CPU-only) |
| MCP integration | Via MCP tools (grepai CLI wraps to MCP) | Native MCP server |
| Requires external service | Yes (Ollama running locally) | No |
| Code search | Yes | Yes |
| Documentation search | No (code-only) | Yes |
| Configuration search | No | Yes |
| Stars | N/A (CLI tool, not counted the same) | ~5,000 |
| Index required | Yes | Yes (cached after first run) |

**The real differentiator**: users who do not run Ollama locally get semantic search without any external dependency. The broader scope (code + docs + config) is an additional advantage over grepai.

---

## Precedent Check: qmd Rejection (score 2/5)

The guide previously rejected qmd (Simone Ruggiero) with the rationale "redundant with grepai, claims non vérifiables." Does the same logic apply to Semble?

Key differences:
- **Traction**: qmd had negligible community adoption. Semble has ~5k stars.
- **Claims verifiability**: qmd claims were unverifiable. Semble is open source with a testable index pipeline.
- **Dependency model**: qmd was a CLI tool overlapping grepai directly. Semble solves the Ollama-dependency problem that affects ~40% of CC users (those without a local GPU or preference against running Ollama).
- **Scope**: qmd searched code only, same as grepai. Semble adds docs and config.

The qmd precedent argues for caution, not rejection. Semble clears the specific objections that sank qmd.

---

## Challenge Assessment

**Challenge agent position**: Score should drop to 2/5 because "two index-based semantic search tools in the same section creates redundancy and reader confusion."

**Counter-argument**: The guide already documents multiple tools with overlapping capabilities in many sections (multiple MCP servers, multiple compression tools). The policy is to document tools that serve meaningfully different audiences or dependency stacks. A user who cannot or will not run Ollama has no path to semantic search in the guide today. Semble is that path. The entry should be brief and positioned explicitly as "if you do not use Ollama," not as a replacement for grepai.

**Score maintained: 3/5.** The entry should be positioned as a complement, not a competitor.

---

## Integration Plan

### `guide/ecosystem/mcp-servers-ecosystem.md` (Code Search & Analysis section, near line 826)

Add one entry following the existing server template, after the grepai entry. Key constraints:
- Use the `#### Name` heading level
- Include Repository/License/Status/Privacy attributes
- Do not claim index-free
- Position explicitly as the Ollama-free alternative

**No other guide files need modification.** The one addition to mcp-servers-ecosystem.md is the full integration scope for a score-3 tool.

---

## Files Modified

- `docs/resource-evaluations/semble-code-search.md` (this file)
- `docs/resource-evaluations/README.md` (index row)
- `guide/ecosystem/mcp-servers-ecosystem.md` (one entry in Code Search section)
- `CHANGELOG.md` ([Unreleased] entry)
