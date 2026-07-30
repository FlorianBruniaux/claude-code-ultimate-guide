# Resource Evaluation: MCP Apps (Anthropic Announcement)

**Date**: 2026-01-27
**Evaluator**: Claude Sonnet 4.5
**Sources**:
- https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/
- https://claude.com/blog/interactive-tools-in-claude

---

## 📄 Summary

**MCP Apps (SEP-1865)** is the first official extension to the Model Context Protocol, enabling MCP servers to deliver interactive user interfaces alongside traditional tool responses.

**Key Points**:
- Co-authored by OpenAI, Anthropic, and MCP-UI creators
- Stable release: January 26, 2026
- SDK: `@modelcontextprotocol/ext-apps`
- Platform support: Claude Desktop, VS Code, ChatGPT, Goose
- 9 interactive tools at launch (Asana, Slack, Figma, Amplitude, Box, Canva, Clay, Hex, monday.com)

---

## 🎯 Scoring

### Pertinence Contenu: 4/5
- ✅ First official MCP extension (major protocol evolution)
- ✅ Co-authored by OpenAI + Anthropic (authoritative)
- ✅ SDK stable with production adoption (9 tools at launch)
- ⚠️ Announced 1 day ago (limited community best practices)
- ⚠️ CLI relevance indirect (Desktop/IDE focused)

### Fiabilité Sources: 5/5
- ✅ Official Anthropic blog post
- ✅ Official Claude blog post
- ✅ Spec published on GitHub (SEP-1865)
- ✅ No dubious claims, verified via Perplexity searches
- ✅ Co-authoring confirmed (OpenAI + Anthropic + MCP-UI)

### Applicabilité Immédiate: 3/5
- ✅ SDK stable and available (npm package)
- ✅ Production examples exist (9 interactive tools)
- ⚠️ CLI users: indirect benefit only (hybrid workflows)
- ⚠️ MCP server developers: new design option
- ❌ Not applicable for Claude Code CLI terminal usage

### Complétude Analyse: 4/5
- ✅ Technical architecture documented (primitives, SDK, security)
- ✅ Platform support verified (Claude, VS Code, ChatGPT, Goose)
- ✅ Use cases and examples provided
- ✅ Timeline clear (proposed Nov 2025, stable Jan 2026)
- ⚠️ Long-term adoption patterns unknown (too recent)

**Score Final**: (4+5+3+4)/4 = **4.0 → 4/5** (High Value - Integrate within 1 week)

---

## ⚖️ Comparative Analysis

| Aspect | MCP Apps | Claude Code Ultimate Guide |
|--------|----------|---------------------------|
| **MCP Protocol basics** | Assumes knowledge | ✅ Documented (architecture.md:506+) |
| **MCP Apps** | ✅ Full specification | ❌ Absent (before this integration) |
| **Interactive UI** | ✅ Core focus | ❌ Not covered (CLI text-based) |
| **Security model** | ✅ Multi-layered (sandbox, templates, audit) | ✅ MCP security documented (CVEs, best practices) |
| **SDK details** | ✅ Complete API reference | ❌ Not covered |
| **Platform support** | ✅ 4 clients shipping | ✅ CLI focused (different audience) |
| **Developer workflow** | ✅ Example servers (5 repos) | ❌ No MCP Apps workflow |
| **CLI relevance** | ⚠️ Indirect | ✅ Primary focus |

---

## 📍 Integration Decision

### Action: **Integrate**

**Justification**:
1. **First official MCP extension** → Significant protocol evolution
2. **Co-authored by ecosystem leaders** → Authoritative source
3. **Guide documents MCP extensively** → Incomplete without Apps coverage
4. **Indirect CLI relevance** → Ecosystem understanding, hybrid workflows, MCP server dev

### Where Documented

| File | Section | Lines |
|------|---------|-------|
| `guide/core/architecture.md` | 6. MCP Integration → MCP Extensions: Apps (SEP-1865) | 656-806 (~150 lines) |
| `guide/ultimate-guide.md` | 8.1 What is MCP → MCP Evolution: Apps Extension | 6509-6599 (~90 lines) |
| `guide/ultimate-guide.md` | 8.5 Plugin System → Table update | 7522-7525 (1 line + note) |
| `machine-readable/reference.yaml` | deep_dive section | 8 new entries |

**Total documentation**: ~240 lines across 3 files

---

## 🔥 Technical Review Challenge

**Conducted by**: technical-writer agent

**Key findings**:
- ✅ Score justified (4/5 appropriate for ecosystem impact)
- ✅ Documentation structure coherent (architecture + user context)
- ✅ CLI relevance correctly assessed (indirect but significant)
- ⚠️ Initial evaluation underestimated ecosystem importance
- ⚠️ Focus on "direct CLI usage" was too narrow

**Score adjustment**: 2/5 (initial) → 4/5 (revised after challenge)

---

## ✅ Fact-Check Results

| Claim | Verified | Source |
|-------|----------|--------|
| SEP-1865 co-authored OpenAI+Anthropic+MCP-UI | ✅ | Perplexity (CopilotKit blog) |
| SDK stable 26/01/2026 | ✅ | GitHub (modelcontextprotocol/ext-apps) |
| VS Code support | ✅ | VS Code official blog |
| Claude Desktop support | ✅ | claude.ai/directory (Pro/Max/Team/Enterprise) |
| 9 apps at launch | ✅ | Perplexity (TechCrunch, The Decoder) |
| ChatGPT rolling out | ✅ | Perplexity (week of Jan 26, 2026) |
| CLI support | ❌ N/A | Text-only terminal (no iframe rendering) |
| Cambridge Intelligence production | ✅ | Perplexity (cambridge-intelligence.com) |
| MCP Protocol 100M downloads/month | ✅ | Perplexity |

**Confidence**: High (all major claims verified)

---

## 🎯 Final Decision

- **Score**: 4/5 (High Value)
- **Action**: Integrated ✅
- **Date integrated**: 2026-01-27
- **Files modified**:
  - `guide/core/architecture.md` (new section)
  - `guide/ultimate-guide.md` (new section + table update)
  - `machine-readable/reference.yaml` (8 new entries)
- **Confidence**: High

---

## 📚 Resources

- **MCP Apps blog**: https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/
- **Claude blog**: https://claude.com/blog/interactive-tools-in-claude
- **Spec (SEP-1865)**: https://github.com/modelcontextprotocol/ext-apps
- **SDK**: https://www.npmjs.com/package/@modelcontextprotocol/ext-apps
- **VS Code announcement**: https://code.visualstudio.com/blogs/2026/01/26/mcp-apps-support

---

## 🔄 Revision History

| Date | Action | Notes |
|------|--------|-------|
| 2026-01-27 | Initial evaluation | Score 3/5 (pertinent) |
| 2026-01-27 | Technical challenge | Downgraded to 2/5 by technical-writer |
| 2026-01-27 | Perplexity research | Upgraded to 4/5 after ecosystem analysis |
| 2026-01-27 | Integration complete | Documentation added to 3 files |
