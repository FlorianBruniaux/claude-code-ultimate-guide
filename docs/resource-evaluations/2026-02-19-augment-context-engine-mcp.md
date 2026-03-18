# Evaluation: Augment Code - Context Engine MCP

**Date**: 2026-02-19
**Evaluator**: Claude Sonnet 4.6
**Source Type**: Product page (commercial tool)
**URL**: https://www.augmentcode.com/product/context-engine-mcp
**Verdict**: RELEVANT (Score: 3/5)

---

## Content Summary

Augment Code launched its Context Engine as a standalone MCP server on February 6, 2026. It provides semantic code search for any MCP-compatible coding agent (Claude Code, Cursor, Zed, Kilo Code, Roo Code, GitHub Copilot).

**Key points**:

1. **What it does**: Cloud-hosted semantic search MCP that indexes codebases (across repos, docs, wikis) and provides context to AI agents via MCP protocol. Indexes up to 400,000-500,000 files using semantic dependency graphs.

2. **Benchmark claims**: Tested on 300 Elasticsearch pull requests (900 attempts with 3 prompts each). Results:
   - Claude Code + Opus 4.5: +80% quality improvement
   - Cursor + Opus 4.5: +71% improvement (completeness +60%, correctness +5x)
   - Cursor + Composer-1: +30% improvement

3. **Efficiency**: Requires fewer tool calls and conversation turns; reduces token usage vs baseline without context engine.

4. **Architecture**: Cloud-hosted (not local), real-time indexing, multi-source connectors (GitHub, GitLab, Bitbucket).

5. **Pricing**: Credit-based ($20/month Indie = 40,000 credits, $50/month Developer = 600 messages). 1,000 free requests during launch period (through Feb 2026, now expired).

---

## Fact-Check Results

| Claim | Source | Verdict |
|-------|--------|---------|
| **"+80% quality improvement" (Claude Code + Opus 4.5)** | Augment blog, confirmed by Perplexity search | ✅ CONFIRMED — but note: published by Augment themselves, no independent replication |
| **"300 Elasticsearch PRs, 900 attempts"** | Augment blog | ✅ PLAUSIBLE — methodology is at least described, unlike many competitor claims |
| **"2x faster task completion"** | Product page only | ⚠️ UNVERIFIED — not backed by the benchmark data cited; appears in marketing copy only |
| **"Works with Claude Code, Cursor, Zed..."** | Product page, confirmed | ✅ CONFIRMED — standard MCP compatibility |
| **"400,000-500,000 file indexing"** | Augment comparison page | ✅ CONFIRMED via Perplexity |
| **Model cited: "Claude Opus 4.6"** | Product page | ⚠️ DISCREPANCY — Perplexity sources + Augment blog consistently say "Claude Opus 4.5". The product page appears to have been updated after the original benchmark. The underlying benchmark used Opus 4.5. |

### Factual Corrections

**Model version discrepancy**: The product page references "Claude Opus 4.6" but the original benchmark blog post (Feb 6, 2026) and all secondary sources reference "Claude Opus 4.5". The product page was likely updated to reflect the current model after the benchmark was run. This is a minor but notable inconsistency — the 80% figure comes from Opus 4.5 testing.

**"2x faster" claim**: This specific number appears in marketing copy on the product page but is not directly backed by the Elasticsearch benchmark data. The benchmark measures quality dimensions (correctness, completeness, best practices, code reuse, documentation) — not task completion speed. Treat as unverified.

---

## Gap Analysis: What the Guide Already Covers

The guide has strong coverage of the semantic code search MCP space:

| Aspect | Guide Coverage | Augment Context Engine |
|--------|---------------|----------------------|
| **Semantic search MCP** | grepai (fully documented, Section: Code Search & Analysis) | Same use case, cloud-hosted |
| **Local vs cloud tradeoff** | grepai = local/private documented explicitly | Augment = cloud-hosted, no local option |
| **Call graph analysis** | grepai: callers/callees/graph tools | Not mentioned in Augment product |
| **Setup & config** | Full install guide for grepai | Install via MCP config |
| **Token efficiency** | grepai: ~4K tokens vs 15K brute force | Augment: "fewer tool calls" (unquantified) |
| **Benchmark data** | None for grepai | 300 PRs, 3 dimensions, specific % gains |
| **Multi-repo support** | Not in grepai | Yes — GitHub, GitLab, Bitbucket connectors |
| **Pricing/cost** | grepai = free, local | Augment = $20+/month subscription |
| **Privacy** | grepai = fully local ("no data leaves your machine") | Augment = cloud-hosted, data sent to Augment |

**Gap identified**: The guide's Code Search & Analysis section documents only grepai (1 server). The section introduction does not discuss the cloud vs local tradeoff for semantic search MCPs, nor does it acknowledge commercial/cloud alternatives like Augment. Users who want a managed, multi-repo solution with proven benchmark results have no guidance.

**Secondary gap**: Augment's benchmark is the most concrete published data comparing semantic context provision to AI coding agents. The guide cites no equivalent quality-improvement benchmarks for grepai.

---

## Scoring

### Score: **3/5** (Relevant - useful complement)

| Criterion | Score | Justification |
|-----------|-------|---------------|
| **Source Credibility** | 3/5 | Commercial product page. Benchmark methodology is described (300 PRs) but self-published. No independent replication. |
| **Factual Accuracy** | 3/5 | Core benchmark claim confirmed via Perplexity. Minor model version discrepancy. "2x faster" claim unverified. |
| **Timeliness** | 5/5 | GA launched Feb 6, 2026 — evaluated Feb 19, 2026. Current. |
| **Practical Value** | 3/5 | Fills a real gap: cloud/managed semantic search MCP for users who don't want local Ollama setup |
| **Novelty** | 3/5 | Same category as grepai (already in guide), but different deployment model + benchmark data is genuinely new |
| **Completeness** | 3/5 | Benchmark methodology described, but quality metrics aren't reproduced publicly; pricing requires separate page |

**Weighted Average**: (3+3+5+3+3+3)/6 = **3.3/5** → rounded to **3/5**

---

## Comparative Analysis: Augment vs Grepai vs Guide's Current Coverage

| Dimension | Grepai (in guide) | Augment Context Engine | Winner for guide |
|-----------|-------------------|----------------------|-----------------|
| **Privacy** | Local only, zero cloud | Cloud-hosted | Grepai for privacy-conscious users |
| **Setup friction** | High (Ollama + nomic-embed-text + grepai init) | Low (MCP config + account signup) | Augment for ease |
| **Multi-repo** | Single project at a time | Cross-repo, cross-wiki | Augment for large orgs |
| **Cost** | Free | $20+/month | Grepai |
| **Call graph** | Full (callers/callees/graph) | Not documented | Grepai |
| **Benchmark evidence** | None published | 80% quality improvement (self-published) | Augment |
| **Independence** | Open source (MIT) | Proprietary, vendor lock-in | Grepai |

**Key finding**: These are genuinely different tools serving different users. Grepai = privacy-first, free, local, with call graphs. Augment = managed, paid, cloud, multi-repo, with benchmark data. The guide currently presents grepai as the only option in this category — that's an incomplete picture.

---

## Integration Recommendation

Score 3/5 — integrate as a documented alternative.

**Recommended action**: Add Augment Context Engine MCP as a secondary entry in the `mcp-servers-ecosystem.md` Code Search & Analysis section, positioned explicitly as "the cloud/managed alternative to grepai."

**What to include**:
1. Brief description of the tool and its differentiation (cloud, multi-repo, managed)
2. Reference to the Elasticsearch benchmark (with caveat: self-published, Opus 4.5)
3. Privacy warning: data sent to Augment cloud
4. Pricing note: credit-based subscription required
5. Link: https://www.augmentcode.com/product/context-engine-mcp

**What to explicitly NOT do**:
- Do not present the 80% or "2x faster" marketing numbers as facts without caveat
- Do not displace grepai as the primary recommendation (grepai remains better for privacy, cost, and call graph analysis)
- Do not expand this to a full section — it's an alternative mention, not a primary recommendation

**Suggested placement** in `mcp-servers-ecosystem.md` after the existing grepai section:

```markdown
#### Augment Context Engine MCP

**Commercial alternative** for users who prefer a managed cloud service over local Ollama setup.
Indexes across multiple repos, wikis, and documentation sources via GitHub/GitLab/Bitbucket connectors.

**Trade-offs vs grepai**:
- Pro: No local setup, multi-repo support, managed indexing
- Con: Cloud-hosted (data leaves your machine), paid subscription ($20+/month), no call graph analysis

**Benchmark**: Augment reports 80% quality improvement on a 300-PR Elasticsearch test dataset
(self-published benchmark, Claude Opus 4.5, Feb 2026).

**Setup**: https://app.augmentcode.com/mcp/configuration
**Docs**: https://www.augmentcode.com/product/context-engine-mcp
```

---

## Final Decision

- **Score**: **3/5** (Relevant - integrate as secondary alternative)
- **Action**: APPROVED for minimal integration in `mcp-servers-ecosystem.md`
- **Confidence**: High
- **Priority**: Low — not urgent, but useful to prevent the impression that grepai is the only option

### Why NOT a higher score?

- Not a new concept: same category as grepai, already well-covered
- Self-published benchmarks without independent replication
- Cloud-only = non-starter for any privacy-sensitive environment
- The guide's primary audience (developers using Claude Code CLI) likely prefers local/free tools over managed subscriptions

---

**Evaluation completed**: 2026-02-19
**Result**: Score 3/5. Useful complement to document as a cloud alternative to grepai. Integrate with clear privacy/cost caveats, no displacement of primary grepai recommendation.
