# Resource Evaluation: MCP Servers Veille (March 2026)

**Date**: 2026-03-02
**Type**: Copied text (veille / research report)
**Language**: French
**Source**: Internal research by Perplexity, covers servers: `github/github-mcp-server`, `exa-labs/exa-mcp-server`, `rawr-ai/mcp-graphiti`

---

## Summary

A research report evaluating 3 open-source MCP servers for Claude Code development workflows, applying criteria: ≥50 stars, recent release (<3 months), clear README, tests/CI, specific use case.

Key findings from the veille:

- **GitHub MCP Server** (`github/github-mcp-server`): 27.1k stars, release v0.31.0 Feb 19 2026, official GitHub, Go, remote MCP at `api.githubcopilot.com/mcp/`, OAuth 2.1 + PAT, covers Issues/PRs/Projects/Enterprise
- **Exa MCP Server** (`exa-labs/exa-mcp-server`): claimed 3.1k stars (unverified — see fact-check), no formal GitHub releases, TypeScript, key feature `get_code_context_exa` for dev-focused code search
- **Graphiti MCP Server** (`rawr-ai/mcp-graphiti`): 74 stars, multi-project knowledge graph on Neo4j + Docker, Python/pipx, CLI (`graphiti compose`, `graphiti up`), early-stage project

---

## Score de pertinence

| Server | Initial Score | Challenge | Final Score |
|--------|--------------|-----------|-------------|
| GitHub MCP | 5/5 | -1 (missing privacy warning, missing Git MCP comparison) | **4/5** |
| Exa MCP | 4-5/5 | -2 (unverified stars, no formal releases, WebSearch native covers use case) | **2/5** |
| Graphiti MCP | 3.5/5 | -1.5 (74 stars, Kairn already in guide, stack too heavy) | **2/5** |

---

## Comparatif

| Aspect | GitHub MCP | Our Guide (pre-integration) |
|--------|-----------|---------------------------|
| GitHub Issues/PRs/Projects | Full coverage | Missing |
| Local Git operations | Partial (GitHub only) | Missing (→ Git MCP fills this) |
| Remote HTTP MCP transport | Yes | Not documented |
| Privacy warning (remote mode) | Needs documentation | Missing |
| Exa code search | Claimed 3.1k stars | WebSearch (built-in) covers basic need |
| Knowledge graphs | Heavy stack | Kairn (already documented) |

---

## Challenge (technical-writer agent)

**GitHub MCP — points manqués**:
- Missing: privacy warning for remote `api.githubcopilot.com` mode (sends data to GitHub servers)
- Missing: explicit comparison with Git MCP Server (two complementary layers: local vs cloud)
- Missing: recommendation to check existing `git-mcp-server-evaluation.md` (5/5 CRITICAL, never integrated)
- Score adjusted: 4/5 (not 5/5)

**Exa MCP — points manqués**:
- Star count unverifiable: veille claims 3.1k, Perplexity search found ~220 stars
- No formal GitHub releases — versioning via npm only, recency criterion relaxed without clear evidence
- Native WebSearch in Claude Code covers basic web/code search use case without extra SaaS dependency
- Score adjusted: 2/5 (reject)

**Graphiti MCP — points manqués**:
- 74 stars barely clears the threshold; project maturity uncertain
- Kairn (already in guide §8.2) covers the persistent memory / knowledge graph use case for Claude Code workflows
- Neo4j + Docker + LLM API dependency is heavy for most users
- Score adjusted: 2/5 (reject)

**Risques de non-intégration (GitHub MCP)**:
- Guide users miss the most useful GitHub automation MCP for Claude Code
- No differentiation between Git (local) and GitHub (cloud) — common confusion point
- Git MCP evaluation was 5/5 CRITICAL but never integrated — oversight corrected simultaneously

---

## Fact-Check

| Claim | Verified | Notes |
|-------|----------|-------|
| GitHub MCP: 27.1k stars | ✅ (approximate) | Perplexity: "20k+" — compatible |
| GitHub MCP: release v0.31.0 Feb 19 2026 | ✅ | 54 total releases confirmed |
| GitHub MCP: Go implementation | ✅ | Confirmed |
| GitHub MCP: OAuth 2.1 + PKCE | ✅ | Confirmed in GitHub changelog |
| Exa: 3.1k stars | ❌ | Perplexity found ~220 stars — major discrepancy, not published |
| Exa: no formal GitHub releases | ✅ | Confirmed — npm + hosted endpoint only |
| Graphiti: 74 stars | ✅ | Approximately verified |
| Graphiti: Neo4j + Docker dependency | ✅ | Confirmed in README |
| Firecrawl: last release Sep 26 2025 | ✅ | v3.2.1 confirmed |
| Chrome MCP: last release Jul 9 2025 | ✅ | v0.0.6 confirmed |

---

## Decision

| Server | Decision | Reason |
|--------|----------|--------|
| **GitHub MCP** | ✅ Integrated | Score 4/5, real gap in guide, official GitHub project, active maintenance |
| **Git MCP** | ✅ Integrated | Pre-existing evaluation 5/5 CRITICAL (`git-mcp-server-evaluation.md`), never integrated — added simultaneously |
| **Exa MCP** | ❌ Rejected | Score 2/5, unverified star count, WebSearch native covers the need, SaaS dependency |
| **Graphiti MCP** | ❌ Rejected | Score 2/5, 74 stars, Kairn already in guide, heavy stack |

**Integration location**: `guide/ultimate-guide.md` §8.2 MCP Server Catalog, before `</details>` closing tag (~line 10625 pre-edit)

**Confidence**: High (facts verified for accepted servers, Exa stars discrepancy flagged)

---

## Related Files

- `docs/resource-evaluations/git-mcp-server-evaluation.md` — Pre-existing 5/5 evaluation for Git MCP (Feb 2026)