# Resource Evaluation: Karl MAZIER — LinkedIn post on CLAUDE.md structure + reizam/claude-md-templates

**Source**: LinkedIn post (Karl MAZIER) + https://github.com/reizam/claude-md-templates
**Author**: Karl MAZIER (co-founder, Open Source & SaaS, YC)
**Date**: ~2026-03-02 (LinkedIn post date estimated ~2 weeks before 2026-03-16)
**Type**: LinkedIn post + GitHub repo (community toolkit)
**Evaluated**: 2026-03-16

---

## 📄 Summary

- Two-level CLAUDE.md structure: `~/.claude/CLAUDE.md` (global, ~30 lines) + `./CLAUDE.md` per repo (~40 lines). Global = coding philosophy/conventions. Project = what the agent can't discover from code alone.
- References ETH Zurich paper arXiv 2602.11988: AI-generated context files yield -3% agent success rate and +20% inference cost. Human-written minimal files yield ~+4%.
- Core rule: write only what the agent cannot discover independently from the codebase.
- GitHub repo (https://github.com/reizam/claude-md-templates): 2 fork-ready templates + 3 slash commands installable via `npx skills add reizam/claude-md-templates` (generate global, generate project, audit existing CLAUDE.md).
- The `Philosophy` section highlighted as the most critical part of global CLAUDE.md.

---

## 🎯 Score

| Score | Meaning |
|-------|---------|
| 5 | Essential — major gap in the guide |
| 4 | High value — significant improvement |
| 3 | Relevant — useful complement |
| **2** | **Marginal — secondary info** |
| 1 | Out of scope |

**Score: 2/5**

**Justification**: The ETH Zurich paper (arXiv 2602.11988) was already evaluated on 2026-02-19 and scored 4/5 with a full integration plan. This LinkedIn post is a community summary of that same paper without original analysis. The GitHub repo templates (8 stars, created 2026-02-27) are redundant with existing `examples/memory/CLAUDE.md.personal-template` (68 lines) and `CLAUDE.md.project-template` (72 lines) in the guide. One element is genuinely new: the `/claude-md-audit` slash command concept — a skill to analyze existing CLAUDE.md for bloat — which the guide doesn't have as an installable command.

---

## ⚖️ Comparison

| Aspect | This resource | Our guide |
|--------|--------------|-----------|
| ETH Zurich paper data (-3%/+20%) | ✅ Cited | ✅ Already evaluated (2026-02-19) |
| Two-level hierarchy (global vs project) | ✅ Described | ✅ Well covered (context-engineering.md) |
| Size targets (~30 / ~40 lines) | ✅ Specific numbers | ⚠️ Guide says <200 lines global (more conservative) |
| "Write only what agent can't discover" rule | ✅ Clear decision test | ⚠️ Implied but not stated as a test |
| Practical templates | ✅ Fork-ready | ✅ Already in examples/memory/ |
| CLAUDE.md audit command | ✅ `/claude-md-audit` skill | ❌ Not implemented |
| Philosophy section emphasis | ✅ Named as most critical | ⚠️ Covered implicitly |

---

## 📍 Recommendations

**Not worth a standalone integration** given the paper is already evaluated.

One targeted addition is worth considering:

**Where**: `guide/core/context-engineering.md`, existing section on CLAUDE.md size/quality.

**What**: Add the decision test as a one-liner: "Write only what the agent cannot discover from the code itself." This is a sharper formulation than the current guidance ("essentiels au projet") and passes as a practical heuristic.

**Priority**: Low. The paper integration (already planned from 2026-02-19 evaluation) is the priority. This is a wording improvement at best.

The `/claude-md-audit` command concept from the GitHub repo is worth tracking for the examples/commands/ directory if the repo gains adoption (currently 8 stars — too early).

---

## 🔥 Challenge

**Score: 2/5 confirmed** by technical-writer agent with one nuance:

The evaluation correctly separates the paper (already covered) from the packaging (LinkedIn post + 8-star repo). The agent challenged whether the score should stay at 2/5 or drop to 1/5 given prior coverage. It stays at 2/5 because:
- The "write only what the agent can't discover" formulation is genuinely more actionable than current guide wording
- The audit command concept is novel even if the repo is too young to reference

**Risks of not integrating**: Near zero. The paper is already queued for integration. This post adds no independent value beyond the paper.

**Points missed**: The post misreads the paper slightly — suggesting global CLAUDE.md should be "~30 lines." The paper's recommendation is more nuanced: write only the essential commands and project-specific tooling, not a target line count. The guide's adherence degradation data (lines 132-141 in context-engineering.md) is actually more actionable than the "~30 lines" heuristic.

---

## ✅ Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| ETH Zurich paper exists (arXiv 2602.11988) | ✅ | Prior evaluation 2026-02-19 |
| AI-generated files: -3% perf | ✅ | arXiv abstract + Perplexity |
| Human-written files: slight gain | ✅ | +4% confirmed in paper |
| +20% inference cost claim | ✅ | "over 20%" in arXiv abstract |
| reizam/claude-md-templates on GitHub | ✅ | 8 stars, 2 forks, created 2026-02-27 |
| `npx skills add` mechanism | ✅ | GitHub repo confirms this |
| "~30 lines global / ~40 lines project" | ⚠️ | Author's interpretation, not paper recommendation |

**Corrections**: The "~30 lines / ~40 lines" targets are the author's own heuristic, not a finding from the ETH Zurich paper. The paper recommends minimal context focused on build/test commands and specific tooling, without a line count target.

---

## 🎯 Final Decision

- **Score**: 2/5
- **Action**: No integration — the underlying paper is already queued (2026-02-19 evaluation). Note the "write only what the agent can't discover" formulation for possible wording improvement in context-engineering.md.
- **Confidence**: High

**Cross-reference**: `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/docs/resource-evaluations/agents-md-empirical-study-2602-11988.md` — the paper this post summarizes, already evaluated at 4/5 with full integration plan.

---

*Evaluated: 2026-03-16 | Method: text analysis + grepai_search + technical-writer challenge + agent research*
