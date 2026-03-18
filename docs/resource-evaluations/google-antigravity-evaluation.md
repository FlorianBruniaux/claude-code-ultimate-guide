# Resource Evaluation: Google Antigravity (Agent-First IDE)

**URL (trigger)**: https://www.linkedin.com/posts/prajwal-tomar-9472081a5_claude-code-antigravity-is-the-most-slept-on-activity-7428808594835558400-pui4
**Primary Sources**: Google Codelabs, Google Cloud Blog, Bind AI, XDA Developers, npm (antigravity-claude-proxy)
**Type**: IDE / Development Platform
**Evaluated**: February 16, 2026
**Score**: 3/5 (PERTINENT — complément utile)

---

## Executive Summary

Google Antigravity is an **agent-first IDE** (VS Code fork) launched late 2025 that shifts development from traditional code editing to autonomous agent-driven workflows. It represents a fundamentally different philosophy from Claude Code: maximum agent autonomy vs explicit developer control.

**Why 3/5**: Not a direct integration with Claude Code, but a significant ecosystem player that our guide should acknowledge. The philosophical contrast (terminal-first vs agent-first) is educational for readers choosing their workflow. The antigravity-claude-proxy bridge creates a concrete connection.

---

## Content Analysis

### Key Facts (Verified)

1. **Architecture**: Agent-first IDE (VS Code fork) with three surfaces — Editor, Agent Manager, Browser integration
2. **Multi-model**: Uses Gemini 3 Pro, Claude 4.5, Liquid AI simultaneously for different tasks
3. **Skills ecosystem**: Community repos with 58 to 856+ skills (GitHub repos verified: rmyndharis/antigravity-skills, sickn33/antigravity-awesome-skills)
4. **Pricing**: $20/month (bundled) or $80-90/month
5. **Claude bridge**: `antigravity-claude-proxy` npm package — proxy server exposing Anthropic-compatible API backed by Antigravity's Cloud Code

### Philosophy Comparison

| Dimension | Claude Code | Google Antigravity |
|-----------|-------------|-------------------|
| **Paradigm** | Terminal-first, CLI-native | Agent-first, IDE-native |
| **Developer control** | Explicit approval per edit | Higher autonomy, agents act independently |
| **Context model** | Codebase-level via CLAUDE.md | Multi-surface (editor + browser + terminal) |
| **CI/CD** | Native (headless, pipelines) | Not mature |
| **Risk profile** | Predictable, conservative | Higher autonomy = higher risk of overstep |
| **Multi-agent** | Agent Teams (v2.1+) | Built-in multi-agent orchestration |
| **Skills** | `.claude/skills/` (YAML frontmatter) | Directory-based, different format |
| **Pricing** | Max plan subscription | $20-90/month |

---

## Fact-Check

| Claim | Status | Source |
|-------|--------|--------|
| Antigravity = VS Code fork, agent-first | ✅ Verified | Google Codelabs, Google Cloud Blog |
| Multi-model (Gemini + Claude + Liquid AI) | ✅ Verified | Multiple reviews, Vertu, Emergent.sh |
| $20/month pricing | ✅ Verified | Vertu review, multiple sources |
| Skills ecosystem (community repos) | ✅ Verified | GitHub repos (rmyndharis, sickn33, Sounder25) |
| antigravity-claude-proxy exists | ✅ Verified | npm package, GitHub repo (badrisnarayanan) |
| "50,000+ stars" (from LinkedIn post) | ⚠️ Unverifiable | Likely refers to Antigravity repo, not skills |
| 32 min benchmark (vs 5-10 min Copilot) | ⚠️ Single source | addshore.com blog, not peer-reviewed |
| Google official comparison page | ✅ Verified | cloud.google.com/blog (Antigravity vs Gemini CLI) |

---

## Gap Analysis

| Aspect | Our Guide | Gap? |
|--------|-----------|------|
| IDE-based tools (Cursor, Windsurf, Cline) | ✅ Section 6 | No |
| Agent-first IDEs (Antigravity) | ❌ Not mentioned | **Yes** |
| Claude Code vs Antigravity comparison | ❌ Not covered | **Yes** |
| antigravity-claude-proxy bridge | ❌ Not documented | **Minor gap** |
| Skills format comparison (SKILL.md vs AG skills) | ❌ Not covered | **Minor gap** |
| Multi-model orchestration concept | ✅ Partially (Section 8) | No |

---

## Integration Recommendation

### Where

**Section 6.1**: New subsection after Section 6 (IDE-Based Tools), before Section 7.

Title: `## 6.1 Google Antigravity (Agent-First IDE)`

### What to Include

1. **What it is** (3 lines): Agent-first IDE, VS Code fork, multi-agent orchestration
2. **Philosophy comparison**: Terminal-first vs agent-first (table)
3. **Bridge tool**: antigravity-claude-proxy npm package
4. **Trade-offs**: Autonomy vs predictability, CI/CD maturity, cognitive overhead
5. **When to consider**: Vibe coding, rapid prototyping, non-CLI workflows

### What NOT to Include

- No tutorial (out of scope — we document Claude Code, not competitors)
- No skills migration guide (different ecosystems)
- No pricing deep-dive (changes too fast)

### Priority

**Medium** — Not urgent, but a real gap in ecosystem coverage.

---

## Challenge (Technical-Writer)

- **Score justified**: 3/5 correct. Not 4/5 because Antigravity is a separate tool, not a Claude Code integration. Not 2/5 because the philosophical contrast is genuinely educational.
- **Risk of non-integration**: Readers comparing tools won't find Antigravity in our guide. The AI Coding Agents Matrix (Section 11) partially covers this, but lacks the nuanced comparison we can provide.
- **Score adjusted**: 3/5 (unchanged)

---

## Decision

| Criterion | Value |
|-----------|-------|
| **Final score** | 3/5 |
| **Action** | Integrate as Section 6.1 in ai-ecosystem.md |
| **Confidence** | High (multiple primary sources verified) |
| **Priority** | Medium |