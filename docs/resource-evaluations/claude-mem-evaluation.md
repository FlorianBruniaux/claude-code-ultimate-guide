# Resource Evaluation: claude-mem

**Resource**: thedotmack/claude-mem - Persistent Memory for Claude Code
**URL**: https://github.com/thedotmack/claude-mem
**Type**: Plugin / MCP Server
**Evaluated**: 2026-02-10
**Evaluator**: Florian BRUNIAUX + Claude (Anthropic)

---

## Quick Summary

**Score**: **4/5** (High Value - Integrate within 1 week)

Claude-mem is a Claude Code plugin providing **automatic session memory** through AI-compressed capture of tool usage, observations, and decisions. It fills a gap in the guide: while Serena (symbol memory) and grepai (semantic search) are documented, **automatic session capture** is not.

**Key Stats** (verified 2026-02-10):
- 26.5k GitHub stars, 1.8k forks
- 181 releases, 46 contributors
- Latest: v9.1.1 (Feb 7, 2026)
- License: AGPL-3.0 + PolyForm Noncommercial

---

## Content Summary

**What claude-mem does**:

1. **Automatic Capture**: Hooks into Claude Code lifecycle (SessionStart, PostToolUse, Stop, SessionEnd) to record all tool operations
2. **AI Compression**: Uses Claude to generate semantic summaries of observations (~10x token reduction)
3. **Hybrid Search**: Full-text + vector search (Chroma) + natural language queries
4. **Progressive Disclosure**: 3-layer retrieval (search → timeline → get_observations) saves 95% tokens
5. **Web Dashboard**: Real-time UI at `http://localhost:37777` for exploring session history
6. **Automatic Injection**: Relevant context auto-injected at session start

**Architecture**:
```
Lifecycle Hooks → Observation capture → AI compression (Claude)
                                             ↓
                                    SQLite storage
                                             ↓
                              Chroma vector indexation
                                             ↓
                              Session start injection
```

**Performance claims** (from articles, not independently verified):
- Progressive disclosure: 10x token reduction
- Endless Mode (beta): 95% context reduction → 20x more tool calls before limits
- Cost: ~$0.15 per 100 observations processed

---

## Relevance Score: 4/5

### Why 4/5 (High Value)?

**✅ Strengths**:

1. **Gap Identified**: Guide documents Serena (symbol memory, manual) and grepai (semantic search) but **not automatic session capture**
2. **Massive Adoption**: 26.5k stars, 181 releases, 46 active contributors
3. **Production-Ready**: AGPL-3.0 licensed, stable API, active maintenance
4. **Complementary**: Doesn't replace existing tools, enhances them
5. **Token Efficiency**: Progressive disclosure pattern valuable for context management

**⚠️ Why Not 5/5?**:

1. **Pattern Partially Covered**: Serena `write_memory()` exists for manual memory, so gap is "automatic" not "memory"
2. **AGPL-3.0 Restrictions**: Commercial use limitations, source disclosure requirements
3. **Hidden Costs**: $0.15/100 observations not documented in official README
4. **CLI Only**: No web interface, no cloud sync, no multi-machine support
5. **Niche Use Case**: Benefits users with >10 sessions/week, less valuable for occasional users

### Comparison to Existing Coverage

| Aspect | This Resource (claude-mem) | Our Guide (v3.23.4) |
|--------|----------------------------|---------------------|
| **Automatic session capture** | ✅ Core feature | ❌ **Missing** |
| **Tool usage tracking** | ✅ Hooks-based | ➕ Documented (hooks architecture) but no specific tool |
| **Progressive disclosure** | ✅ 3-layer workflow | ❌ Pattern not documented |
| **Session-to-session memory** | ✅ Automatic injection | ➕ Partial (Serena manual, not auto) |
| **Web dashboard** | ✅ Real-time UI | ❌ Missing |
| **Token efficiency patterns** | ✅ 95% reduction | ➕ Documented (context management) but not this magnitude |
| **AGPL licensing implications** | ⚠️ Restrictions | ❌ **Missing** (licensing considerations) |
| **Cost**: API compression | ⚠️ $0.15/100 obs | ❌ **Missing** (hidden costs) |
| **Platform limitations** | ⚠️ CLI only | ❌ **Missing** |

**Summary**: Guide covers building blocks (hooks, MCP, Serena) but **lacks integrated solution** that claude-mem provides. Gap is moderate (not critical) because patterns exist, but automatic capture adds significant value.

---

## Integration Recommendations

### Where to Document

**Recommended**: **Section 8.2.5** (after grepai) in `guide/ultimate-guide.md` ~line 8463

**Structure**:

```markdown
## 8.2.5 claude-mem (Automatic Session Capture)

### Architecture & Features
- Lifecycle hooks integration
- AI compression workflow
- Progressive disclosure pattern
- Web dashboard overview

### Installation & Setup
- Plugin marketplace installation
- Configuration options
- Privacy controls (<private> tags)

### Usage Patterns
- Automatic injection workflow
- Natural language queries
- Web UI navigation

### Cost & Privacy Considerations
- API compression costs ($0.15/100 obs)
- AGPL-3.0 licensing implications
- Data locality (SQLite + Chroma)
- Privacy tags for sensitive content

### Decision Matrix: vs Serena vs grepai
| Need | Tool | Rationale |
|------|------|-----------|
| Auto capture tool usage | claude-mem | Zero manual effort |
| Symbol-aware navigation | Serena | Precise editing |
| Semantic discovery | grepai | Intent-based search |
| Manual decision storage | Serena | Explicit control |

### Hybrid Workflows
- claude-mem + Serena (auto capture + manual decisions)
- claude-mem + grepai (session history + semantic search)
- Complete stack: rg → grepai → Serena → claude-mem
```

**Size**: 300-400 lines (not 800 as initially proposed)

### Files to Create/Modify

1. **guide/ultimate-guide.md**
   - Add Section 8.2.5 (~300 lines)
   - Update Section 2.2 (Session vs Persistent Memory) with claude-mem reference

2. **machine-readable/reference.yaml**
   ```yaml
   claude_mem: "guide/ultimate-guide.md:8463"
   claude_mem_architecture: "guide/ultimate-guide.md:8470"
   claude_mem_progressive_disclosure: "guide/ultimate-guide.md:8520"
   claude_mem_dashboard: "guide/ultimate-guide.md:8550"
   claude_mem_vs_serena: "guide/ultimate-guide.md:8600"
   claude_mem_installation: "/plugin marketplace add thedotmack/claude-mem"
   claude_mem_repo: "https://github.com/thedotmack/claude-mem"
   claude_mem_stars: "26.5k"
   claude_mem_license: "AGPL-3.0"
   claude_mem_score: "4/5"
   ```

3. **examples/plugins/claude-mem.md** (installation template)

4. **CHANGELOG.md**
   ```markdown
   ## [3.24.0] - 2026-02-XX

   ### Added
   - **Section 8.2.5**: claude-mem plugin documentation
   - Memory Stack Patterns (claude-mem + Serena + grepai integration)
   - Decision matrix for memory tools
   ```

### Priority

**High Value** - Integrate within **1 week**

**Rationale**:
- Fills genuine gap (automatic capture not documented)
- Massive community adoption (26.5k stars)
- Complementary to existing tools
- BUT not "Critical" (5/5) because patterns partially exist

---

## Technical Analysis: claude-mem vs Serena vs grepai

### Architecture Comparison

| Aspect | claude-mem | Serena | grepai |
|--------|-----------|---------|--------|
| **Purpose** | Session capture | Symbol memory | Semantic search |
| **Trigger** | Auto (hooks) | Manual API | Manual CLI |
| **Storage** | SQLite + Chroma | `.serena/memories/` | Ollama vectors |
| **Technology** | AI compression | Key-value store | Embeddings |
| **Indexation** | Session events | Project symbols | Code files |
| **Query** | Natural language | Key lookup | Semantic search |
| **Dashboard** | ✅ Web UI | ❌ No | ❌ No |
| **Cost** | $0.15/100 obs | Free (local) | Free (local) |
| **Privacy** | ✅ Local | ✅ Local | ✅ Local |

### Use Case Matrix

| Need | Tool | Example |
|------|------|---------|
| "What did we do yesterday?" | claude-mem | Auto-inject previous context |
| "Find function login" | Serena | `find_symbol --name "login"` |
| "Who calls this function?" | grepai | `grepai trace callers "login"` |
| "Record arch decision" | Serena | `write_memory("auth", "JWT")` |
| "Find code that does X" | grepai | `grepai search "payment validation"` |
| "Summary of all sessions" | claude-mem | Web dashboard + search |
| "Exact pattern 'authenticate'" | rg (native) | `rg "authenticate" --type ts` |

### Memory Stack Pattern (Proposed)

```
┌─────────────────────────────────────────────────────────┐
│           Memory Stack (4 layers)                       │
├─────────────────────────────────────────────────────────┤
│ Layer 4: Session Capture   → claude-mem (automatic)    │
│ Layer 3: Symbol Memory     → Serena (manual decisions) │
│ Layer 2: Semantic Search   → grepai (discovery)        │
│ Layer 1: Exact Search      → rg (native, fast)         │
└─────────────────────────────────────────────────────────┘
```

**Integrated Workflow Example**:

```bash
# Scenario: Refactoring auth module after 3 days

# 1. AUTO CONTEXT (claude-mem)
# At session start, Claude injects:
# "3 previous sessions explored auth module.
#  Decision: Migrate to JWT.
#  Files modified: auth.service.ts, session.middleware.ts"

# 2. ARCH DECISIONS (Serena)
serena list_memories
# → "auth_decision: Use JWT for stateless API (2026-02-07)"

serena read_memory("auth_decision")

# 3. SEMANTIC DISCOVERY (grepai)
grepai search "JWT token validation"
# → Finds validateJWT() in auth.service.ts

# 4. DEPENDENCIES (grepai trace)
grepai trace callers "validateJWT"
# → Called by: ApiGateway, AdminPanel, UserController

# 5. EXACT SEARCH (rg)
rg "validateJWT" --type ts -A 5
```

**Result**: Complete context without re-reading all files, safe refactoring.

---

## Fact-Check Results

| Claim | Source | Verified | Notes |
|-------|--------|----------|-------|
| **26.5k stars** | GitHub (WebFetch 2026-02-10) | ✅ | Perplexity had 15.6k (outdated) |
| **1.8k forks** | GitHub | ✅ | Confirmed |
| **181 releases** | GitHub | ✅ | Perplexity had 174 (outdated) |
| **46 contributors** | GitHub | ✅ | Perplexity had 22 (outdated) |
| **AGPL-3.0 license** | GitHub README | ✅ | + PolyForm Noncommercial for ragtime/ |
| **Latest: v9.1.1 (Feb 7, 2026)** | GitHub releases | ✅ | Active |
| **Target: Claude Code** | GitHub README | ✅ | Primary (+ Desktop secondary support) |
| **Guide doesn't document Serena** | ultimate-guide.md grep | ❌ **FALSE** | 10 occurrences found |
| **Guide doesn't document grepai** | ultimate-guide.md grep | ❌ **FALSE** | 22 occurrences found |
| **Progressive disclosure 10x** | Perplexity + articles | ⚠️ | Claim verified but metric approximate |
| **$0.15/100 observations** | External articles | ⚠️ | Not found in official README |
| **95% Endless Mode** | Articles | ⚠️ | Beta claim, not independently verified |

**Corrections Applied**:

1. **Gap analysis corrected**: Guide DOES document Serena (lines 686, 762, 765, 770, 775, 779, 968, 1521, 1532) and grepai (22 mentions). Gap is **not "no memory docs"** but **"no automatic capture solution"**.

2. **Stats verified**: 26.5k stars (Perplexity outdated), 181 releases, 46 contributors.

3. **Product target**: Claude Code (primary), not confused with Desktop.

4. **Perplexity reliability**: Detected outdated data → always verify GitHub directly for critical stats.

---

## Limitations & Considerations

### claude-mem Limitations

1. **AGPL-3.0 License**
   - Modifications require source disclosure
   - Network deployment requires AGPL
   - Commercial use restrictions

2. **Hidden Costs**
   - $0.15 per 100 observations (API compression)
   - Not documented in official README
   - Can accumulate on large projects

3. **CLI Only**
   - No web interface support
   - No cloud sync between machines
   - No VS Code integration

4. **Manual Privacy Tags**
   - `<private>` tags required for sensitive content
   - Forgetting tags → sensitive data in DB
   - No automatic secret detection

### Overlaps with Existing Tools

Guide already documents:
- Session search (`guide/observability.md:29`)
- Session migration (`guide/observability.md:175`)
- Context management (`/compact`, `/clear`)

**Question**: Does claude-mem provide enough **incremental value** to justify 300-400 lines?

**Answer**: Yes, because:
- ✅ **Automatic** capture (vs manual Serena)
- ✅ AI compression (vs raw sessions)
- ✅ Web dashboard (vs CLI only)
- ✅ Progressive disclosure (token efficiency)

---

## Technical Writer Challenge Results

**Agent ID**: ac8e0c6

**Challenge Summary**:

The technical-writer agent challenged the initial 5/5 score, identifying:

1. **False premise**: "Guide doesn't document Serena/grepai" → **FALSE** (both documented)
2. **Stats contradictions**: 15.6k vs 26.5k stars → Required verification
3. **Product confusion**: Clarified Claude Code vs Claude Desktop targeting
4. **Sizing issues**: 800 lines over-dimensioned → Reduced to 300-400 lines
5. **Urgency questioned**: <24h unrealistic → Changed to 1 week

**Result**: Score adjusted from 5/5 → 4/5 based on:
- Gap is real but **moderate** (Serena/grepai exist, automatic capture missing)
- AGPL-3.0 + hidden costs + CLI-only = limitations
- Complementary tool, not critical infrastructure

---

## External Resources

**Articles**:
- [Corti.com: Claude-Mem Deep Dive](https://corti.com/claude-mem-persistent-memory-for-ai-coding-assistants/) (2026-02-03)
- [yuv.ai: Persistent Memory Guide](https://yuv.ai/blog/claude-mem) (2026-02-05)
- [byteiota: Progressive Disclosure Analysis](https://byteiota.com/claude-mem-persistent-memory-for-claude-code/) (2026-02-04)

**Videos**:
- [YouTube: 5-Minute Setup Guide](https://www.youtube.com/watch?v=ryqpGVWRQxA) (2026-02-06)
- [YouTube: Unlimited Memory Demo](https://www.youtube.com/watch?v=qhuS__jC4n8) (2026-02-05)

**GitHub**:
- [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)
- [Release Notes v9.1.1](https://github.com/thedotmack/claude-mem/releases/tag/v9.1.1)

**Benchmarks**:
- No independent benchmarks found as of 2026-02-10
- Claims from articles: "95% context reduction, 20x tool calls" (not verified)
- Progressive disclosure: "10x token reduction" (plausible based on architecture)

---

## Decision

**Score**: **4/5** (High Value - Integrate within 1 week)

**Action**:
1. Integrate Section 8.2.5 in `guide/ultimate-guide.md` (300-400 lines)
2. Update `machine-readable/reference.yaml` with claude-mem entries
3. Create plugin template in `examples/plugins/claude-mem.md`
4. Add to CHANGELOG.md v3.24.0

**Confidence**: High (stats verified, architecture understood, integration plan clear)

---

**Evaluated**: 2026-02-10
**Next Review**: Before v3.24.0 integration
**Status**: Approved for integration
