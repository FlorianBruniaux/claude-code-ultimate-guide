# Resource Evaluation: Tree-Sitter & AST-Based Progressive Code Exploration

**Resource**: Ecosystem of tools (Alex Newman's "smart explore" concept + implementations)
**Type**: Pattern + MCP Servers + CLI Tool
**Evaluated**: 2026-03-20
**Evaluator**: Florian BRUNIAUX + Claude Sonnet 4.6
**Context**: Signal from Alex Newman (Claude-MEM, 38k+ stars, now 88,747 as of 2026-07-28), showing "14k tokens to 200 using tree-sitter progressive search"

---

## Quick Summary

**Score: 4/5** (High Value — Integrate within 1 week)

The "smart explore" pattern uses tree-sitter AST parsing to compress code exploration from 10-15k tokens per file to ~200-500 tokens by showing function signatures and structure first, then drilling into specific functions only when needed. RTK handles command outputs (60-90% savings); this pattern handles code reading (90-97% savings). Together they cover both major token sinks in a Claude Code session.

No single "official" implementation exists — Alex Newman's skill is private. But the ecosystem has multiple working implementations ranging from a pure CLI approach to production-ready MCP servers.

---

## The Pattern: Progressive Code Exploration

Three layers, executed in order:

```
Layer 1 — Structure (~200 tokens)
  tree-sitter parse file.rs → function signatures, types, fields
  Claude sees: "what exists?" without reading any body

Layer 2 — Search (~300 tokens)
  "Show me the body of filter_output()"
  tool returns lines 47-120 only, not the whole file

Layer 3 — Context (~500 tokens)
  "Who calls filter_output()?"
  cross-reference table, not file dumps
```

**vs naive approach** (read file, read another file, read another file):
- Naive: 10 files × ~1,400 tokens = 14,000 tokens
- Progressive: 10 structures (2,000) + 2 functions (1,000) = 3,000 tokens
- **Reduction: ~78% average, up to 97% for large repos**

Same pattern that Aider (40k+ stars) uses for its repo map, validated at scale.

---

## Tools Evaluated (March 2026)

### 1. jCodeMunch-MCP

**GitHub**: https://github.com/jgravelle/jcodemunch-mcp
**Stars**: ~1,200 (now 2,290 as of 2026-07-28) | **License**: Non-commercial free / paid commercial ($79 indie)
**Last commit**: March 19, 2026 | **Status**: Active, production-polished

**What it does**: Indexes codebase once with tree-sitter, exposes symbols via MCP. Claude calls `get_symbol("filter_output")` instead of reading the whole file.

**Install**:
```bash
claude mcp add jcodemunch uvx jcodemunch-mcp
# or
pip install jcodemunch-mcp
```

**Token claims vs reality**:
| Claim source | Figure | Assessment |
|---|---|---|
| Marketing headline | 95%+ | Cherry-picked (single symbol lookup on large repo) |
| Demo benchmark | 214k → 480 tokens | Best case (fastapi/fastapi, full repo vs one symbol) |
| Controlled A/B test (50 iterations) | 10.5% cache savings, 15-25% tool layer | Realistic for typical workflows |

**Commercial friction**: Free for personal/OSS, $79 for commercial use. Teams require $349+. Worth flagging for readers.

**Verdict**: Most polished install experience, honest architecture, but headline savings are marketing. Real savings meaningful for symbol-heavy workflows.

---

### 2. mcp-server-tree-sitter (wrale)

**GitHub**: https://github.com/wrale/mcp-server-tree-sitter
**Stars**: ~270 (now 311 as of 2026-07-28) | **License**: Not specified | **Last commit**: February 25, 2026

**What it does**: Pure MCP server wrapping tree-sitter. Exposes AST queries, symbol extraction, dependency analysis, parse tree caching. Most complete feature set of the pure MCP options.

**Languages**: Python, JS, TS, Go, Rust, C, C++, Swift, Java, Kotlin, Julia, APL

**Install**:
```bash
pip install mcp-server-tree-sitter
```

**Key feature**: Run tree-sitter queries directly (not just symbol lookup). Lets you extract any AST pattern across a codebase.

**Benchmarks**: None published. No commercial friction. MIT spirit (license file missing — confirm before commercial use).

**Verdict**: Best for users who want raw AST access, not just symbol lookup. Steeper learning curve (need to know tree-sitter query syntax), but most flexible.

---

### 3. code-review-graph

**GitHub**: https://github.com/tirth8205/code-review-graph
**Stars**: ~2,000 (now 26,910 as of 2026-07-28) | **License**: MIT | **Last commit**: March 17, 2026

**What it does**: Persistent SQLite-backed code graph, updated incrementally on file edits and git commits. Exposes a code review tool that focuses on changed files and their dependencies only.

**Install**:
```bash
pip install code-review-graph
code-review-graph install
# or via Claude Code marketplace
claude plugin marketplace add tirth8205/code-review-graph
```

**Token claims** (tested on httpx, FastAPI, Next.js):
| Repo | Token reduction |
|---|---|
| httpx | 26.2x |
| FastAPI | 8.1x |
| Next.js | 6.0x |
| Average | 6.8x |
| Peak (Next.js monorepo) | 49x |

**Methodology note**: "Review quality: 8.8/10 vs 7.2/10" — no published rubric. Treat quality claims with caution, token reduction figures more credible (file-count measurement).

**Unique angle**: Targets **code review specifically**, not general exploration. The graph knows which files changed and their blast radius. Strongest ROI for PR review workflows.

**Verdict**: Best for teams doing PR reviews. MIT license, marketplace listed, most real-world stars of the MCP options. 2,000 stars in ~2 weeks suggests strong product-market fit.

---

### 4. CodeRLM

**GitHub**: https://github.com/JaredStewart/coderlm
**Stars**: 192 (now 294 as of 2026-07-28) | **License**: MIT | **Last commit**: February 7, 2026

**What it does**: Rust server + tree-sitter index + Python CLI skill wrapper. Claude queries symbols on demand instead of file-reading. Ships as a Claude Code skill via `SessionStart`/`UserPromptSubmit` hooks.

**Languages**: Rust, Python, TypeScript, JavaScript, Go (full tree-sitter); others via regex fallback.

**Critical limitation** (author's own words): "Claude demonstrates substantial resistance to using CodeRLM in exploration tasks." Requires explicit CLAUDE.md instructions. Doesn't trigger autonomously.

**Verdict**: Interesting architecture, honest maintainer, MIT. Under-maintained since February. The Claude autonomy problem needs a workaround (explicit CLAUDE.md instructions). Worth watching but not ready-to-use without friction.

---

### 5. Aider Repo Map (reference implementation)

**Project**: Aider (https://aider.chat), 40k+ stars (now 47,733 as of 2026-07-28)
**Approach**: tree-sitter + NetworkX graph + PageRank ranking + binary search for token budget

**How it works**:
1. Parse every file with tree-sitter → extract symbols + where they're referenced
2. Build dependency graph (files = nodes, cross-references = edges)
3. PageRank: files referenced by many others score higher (public API > private helper)
4. Budget fitting: binary search to fit within `--map-tokens` limit (default: 1,000 tokens)

**Why it matters**: This is the most technically documented implementation of the pattern. Invented in 2023, validated at 40k+ star scale. No MCP server, but shows what the ideal implementation looks like.

**Default token budget**: `--map-tokens 1000` gives the entire repo structure in 1k tokens.

---

## Comparison Table

| Tool | Stars | Install | Token Claims | License | Use Case |
|---|---|---|---|---|---|
| jCodeMunch | ~1,200 (now 2,290 as of 2026-07-28) | `claude mcp add jcodemunch uvx jcodemunch-mcp` | 10-25% realistic (95% cherry-pick) | Free non-commercial | Symbol lookup |
| mcp-server-tree-sitter | ~270 (now 311 as of 2026-07-28) | `pip install mcp-server-tree-sitter` | None published | Check license | Raw AST queries |
| code-review-graph | ~2,000 (now 26,910 as of 2026-07-28) | `pip install code-review-graph` | 6.8x avg (PR review) | MIT | PR code reviews |
| CodeRLM | 192 (now 294 as of 2026-07-28) | Cargo build needed | None published | MIT | On-demand exploration |
| Aider repo map | 40k+ (now 47,733 as of 2026-07-28) | Built into Aider | 1k token budget (default) | Apache 2.0 | Full repo context |

---

## Relevance Assessment: 4/5

### Why 4/5?

**Strengths supporting integration**:

1. **Signal from credible source**: Alex Newman (Claude-MEM, 38k+ stars) explicitly calls this out as a pattern producing "14k → 200 tokens". Not marketing, peer signal.
2. **Multiple production implementations**: code-review-graph has 2k stars and MIT license, jCodeMunch ships with `uvx` one-liner, Aider validates the pattern at 40k+ scale.
3. **Genuine gap in current guide**: Guide documents RTK (command output savings) but not code reading savings. The two problems are complementary, covering both is complete.
4. **Pattern is teachable**: Progressive disclosure (structure → search → drill) works even without any external tool, using just Claude's Read tool with discipline.
5. **Aider credibility**: The pattern isn't experimental — Aider's repo map has been in production since 2023.

**Why not 5/5**:

1. **Alex's "smart explore" skill is not public**: Can't cite it directly or link to it. The guide should document the pattern + available implementations, not "Alex Newman's skill".
2. **Benchmarks vary widely**: 6.8x to 49x to 95% — the honest number for typical workflows is harder to pin down than RTK's measured 60-90%.
3. **grepai already does this partially**: The guide already recommends grepai for semantic code search. Tree-sitter adds structural awareness (not just semantic), but overlap is real.
4. **MCP servers are early-stage**: mcp-server-tree-sitter has no benchmarks, CodeRLM has a known autonomy problem, jCodeMunch charges for commercial use.

### Comparison with Existing Coverage

| Aspect | This pattern | Guide (v3.37.2) |
|---|---|---|
| Command output compression | ❌ Not this | ✅ RTK (5/5 score) |
| Semantic code search | ❌ Not this | ✅ grepai (documented) |
| Structural code exploration | ✅ Core value | ❌ Missing |
| Progressive disclosure pattern | ✅ Core value | ❌ Missing |
| Tree-sitter usage | ✅ Core tech | ⚠️ ast-grep skill (different goal) |
| PR code review workflow | ✅ code-review-graph | ❌ Missing |
| Repo-wide structure overview | ✅ Core value | ❌ Missing |

---

## Integration Recommendations

### What to Create

**1. Skill file**: `examples/skills/smart-explore.md`

Teach the pattern + provide copy-paste implementations. Three approaches:
- Pure CLI (tree-sitter CLI + bash/python script, no MCP)
- MCP server (jCodeMunch or mcp-server-tree-sitter)
- Quick wins (just using Claude's Read tool progressively, no setup)

**2. Guide section**: Add to `guide/ultimate-guide.md` near RTK token efficiency section

Content: Pattern explanation, decision matrix (when to use each tool), comparison with grepai.

**3. CHANGELOG entry** (this eval, not guide section yet)

### Where in the Guide

The natural location is near the RTK and grepai sections. The guide uses RTK for command savings and grepai for semantic search — tree-sitter adds the structural layer between the two.

Draft section title: **"9.X.X Progressive Code Exploration (AST-Based)"** or added to the MCP ecosystem section under "Code Search & Analysis".

---

## Technical Notes (for Guide Writers)

### What tree-sitter IS and ISN'T

**Is**: A parser library that turns source code into an AST (abstract syntax tree). Same engine VSCode/Neovim/Zed use for syntax highlighting and code folding.

**Is not**: A semantic analyzer. It understands syntax, not meaning. `tree-sitter` can tell you "this is a function named X with these parameters", but not "this function is called by Y across the codebase" (that's what grepai/Aider graph does).

### The DOM analogy (for documentation)

"Tree-sitter does for code what a browser does for HTML — turns flat text into a navigable structure. Instead of a DOM tree, you get an AST: every function, class, struct, and field as a typed node with exact position in the file."

### Honest token math

| Operation | Tokens | Method |
|---|---|---|
| Read 500-line file | ~3,500 | Claude's Read tool |
| Get file structure only | ~200 | tree-sitter signatures |
| Read one function (50 lines) | ~350 | tree-sitter offset lookup |
| Explore 10-file module (naive) | ~35,000 | Read × 10 |
| Explore 10-file module (progressive) | ~3,500 | Structure × 10 + drill × 2 |

Real-world reduction for typical feature work: **70-90%**. The 97% figures require giant codebases + lucky access patterns.

---

## Fact-Check

| Claim | Source | Status | Notes |
|---|---|---|---|
| Alex Newman, Claude-MEM creator | GitHub (thedotmack/claude-mem, 38k+ stars, now 88,747 as of 2026-07-28) | ✅ Verified | Stars confirmed at time of eval |
| "14k → 200 tokens" claim | Alex Newman's LinkedIn DM | ⚠️ Unverified | Plausible based on architecture, not independently tested |
| jCodeMunch 95% token savings | jcodemunch-mcp marketing | ⚠️ Inflated | Controlled test shows 10-25%; 95% is cherry-picked single-symbol best case |
| jCodeMunch A/B test -10.5% cache tokens | benchmarks/ab-test-naming-audit-2026-03-18.md | ✅ Credible | 50 iterations, methodology documented |
| code-review-graph 6.8x average | Medium article + HN | ⚠️ Partially verified | File-count methodology more credible than quality scores (8.8/10) |
| Aider 1k token default budget (47,733 stars as of 2026-07-28) | aider.chat official docs | ✅ Verified | --map-tokens documented |
| mcp-server-tree-sitter ~270 stars (now 311 as of 2026-07-28) | GitHub (wrale/mcp-server-tree-sitter) | ✅ Verified | March 2026 |
| CodeRLM "Claude resistance" | Author README | ✅ Author admission | Requires explicit CLAUDE.md workaround |
| tree-sitter used by VSCode/Neovim/Zed | Public documentation | ✅ Verified | Widely documented |

---

## Decision

**Score: 4/5** (High Value — Integrate within 1 week)

**Actions**:
1. Create `examples/skills/smart-explore.md` skill (progressive code exploration pattern)
2. Add guide section near RTK/grepai explaining the complementary three-layer token strategy
3. Document code-review-graph separately as the strongest standalone MCP for PR review workflows (MIT, 2k stars, marketplace listed)

**Not recommended immediately**:
- jCodeMunch in the guide: commercial friction ($79) and inflated claims make it hard to recommend cleanly
- mcp-server-tree-sitter: good tool but no benchmarks and license unclear
- CodeRLM: Claude autonomy problem makes it friction-heavy for readers

**Primary recommendation for guide readers**: Start with the pattern (no setup), then add jCodeMunch/code-review-graph based on use case.

---

**Evaluated**: 2026-03-20
**Next Review**: Before v3.40 (monitor code-review-graph growth, jCodeMunch open-source trajectory)
**Status**: Approved for integration

**Related**:
- `examples/skills/smart-explore.md` (to be created)
- `docs/resource-evaluations/rtk-evaluation.md` (complementary tool)
- Guide: `guide/ultimate-guide.md` (RTK section, grepai section)
- External: https://aider.chat/docs/repomap.html (reference implementation)