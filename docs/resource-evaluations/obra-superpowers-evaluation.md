# Evaluation: obra/superpowers — Agentic Skills Framework for Claude Code

**Resource Type**: GitHub Repository (Claude Code Plugin)
**Author**: Jesse Vincent, Prime Radiant
**URL**: https://github.com/obra/superpowers
**Evaluation Date**: 2026-03-18
**Evaluator**: Claude Sonnet 4.6

---

## 1. Content Summary

Superpowers is a complete software development methodology packaged as a Claude Code plugin — a suite of composable skills that enforces structured workflows from idea to merged branch. Skills trigger automatically based on context (no manual invocation needed).

**Key content**:
- **Brainstorm-first gate**: Before any code, the agent elicits a spec through Socratic questioning and presents it in reviewable sections
- **Implementation planning**: Breaks work into 2-5 minute tasks with exact file paths, complete code blocks, and verification steps
- **Subagent-driven development**: Dispatches a fresh subagent per task with a two-stage review (spec compliance, then code quality); designed for hours of autonomous work
- **Mandatory TDD**: RED → GREEN → REFACTOR enforced; code written before a test gets deleted and redone
- **Full branch lifecycle**: `using-git-worktrees` + `finishing-a-development-branch` cover the complete arc from workspace creation to merge/PR decision

**Philosophy**: Test-driven development as non-negotiable, systematic over ad-hoc, complexity reduction as primary goal, evidence over claims.

---

## 2. Score: 5/5 (Essential)

| Score | Signification | Action |
|-------|---------------|--------|
| **5** | **Essential — fills major gap** | **< 24h** |
| 4 | High value — significant improvement | < 1 week |
| 3 | Moderate — useful complement | When time available |
| 2 | Marginal — secondary info | Minimal or skip |
| 1 | Low — reject | — |

### Justification

**Points forts**:
- ✅ **95,299 GitHub stars** (verified via GitHub API, March 18, 2026), now 262,101 as of 2026-07-28, among the most-starred Claude Code resources in existence
- ✅ **7,546 forks** — genuine adoption signal, not bot-inflated
- ✅ **Available on the official Claude Code plugin marketplace** — `/plugin install superpowers@claude-plugins-official`
- ✅ **obra already in our guide** (line 8104, TDD skill at 721 skills.sh installs) — not mentioning the full suite is a credibility gap
- ✅ **MIT license** — freely integrable, referentiable
- ✅ **Multi-platform** (Claude Code, Cursor, Codex, OpenCode, Gemini CLI) — broad ecosystem relevance
- ✅ **Structured workflow the guide lacks**: brainstorm → spec → plan → subagent TDD → review → close — no single page in the guide covers this end-to-end pipeline
- ✅ **Created Oct 2025**, reached 95k stars in 5.5 months — clear community signal

**Pourquoi 5/5 et pas 4/5**:
At 95k stars on a Claude Code tool (verified), this is the dominant community methodology for structured agentic development. The guide documents TDD, spec-first, plan-driven, and worktrees separately — but has no unified workflow suite entry at this adoption level. Not covering it is a meaningful gap.

---

## 3. Comparative Analysis

| Aspect | Superpowers | Current guide |
|--------|-------------|---------------|
| **End-to-end methodology as a plugin suite** | ✅ Single `/plugin install` | ❌ Scattered across 5+ workflow pages |
| **Automatic skill triggering** | ✅ Context-based activation | ❌ No equivalent (manual skill use) |
| **Subagent-driven development** | ✅ Native skill with two-stage review | ⚠️ Task tool documented mechanically |
| **Branch lifecycle workflow** | ✅ `finishing-a-development-branch` | ⚠️ Worktrees documented, not end-to-end lifecycle |
| **TDD enforcement** | ✅ Code deleted if written before test | ✅ `tdd-with-claude.md` covers cycle |
| **Brainstorm-first spec gate** | ✅ `brainstorming` skill mandatory | ⚠️ `spec-first.md` exists but not enforced |
| **Plugin marketplace listing** | ✅ Official | ❌ Not cross-referenced |
| **Community adoption signal** | ✅ 95k stars / 7.5k forks | N/A |

---

## 4. Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| 95k+ GitHub stars | ✅ 95,299 (now 262,101 as of 2026-07-28) | GitHub API, March 18, 2026 |
| 7,546 forks | ✅ Exact | GitHub API |
| MIT license | ✅ | GitHub API (`license.spdx_id: MIT`) |
| Available on official Claude Code marketplace | ✅ | README: `/plugin install superpowers@claude-plugins-official` |
| Created by Jesse Vincent, Prime Radiant | ✅ | GitHub repo, README attribution |
| Works with Claude Code, Cursor, Codex, OpenCode | ✅ | README installation sections |
| obra = test-driven-development skill on skills.sh | ✅ | Guide line 8104 (existing reference) |
| "Couple hours autonomous" claim | ⚠️ Not measurable | Self-reported in README, no benchmark |
| Gemini CLI support | ✅ | README: `gemini extensions install` |

**No hallucinations detected**. The "couple hours autonomous" claim is marketing language — no benchmark, can't verify. All other material claims check out.

---

## 5. Challenge (technical-writer agent)

**Key challenges raised and resolved**:

**Challenge 1: "Verify the 95k star count before assigning 5/5"**
→ Verified via GitHub API. 95,299 stars, 7,546 forks, created Oct 2025. This is the gate for the score — gate passed. Score stands at 5/5.

**Challenge 2: "The guide already covers each component separately (TDD, spec-first, worktrees). Is Superpowers truly additive?"**
→ Yes: the value is the *package* and *automatic triggering*. Users installing a single plugin get a structured methodology without manually composing five workflow pages. The guide has no single entry for "install this to enforce good workflow habits automatically." That's the gap.

**Challenge 3: "Is third-party-tools.md + Plugin Ecosystem the right integration point?"**
→ Partially agreed with challenge. Better approach: (a) upgrade the obra row at line 8104 in ultimate-guide.md to reference the full Superpowers suite with link, (b) add a dedicated Notable Workflow Suites entry in the Plugin Ecosystem section of third-party-tools.md alongside gstack, (c) reference from tdd-with-claude.md and spec-first.md as "community methodology that bundles this workflow."

**Challenge 4: "What about the subagent workflow — is it really different from native Task tool?"**
→ Superpowers' `subagent-driven-development` enforces a two-stage review (spec compliance then code quality) that the native Task tool doesn't provide out of the box. Worth noting as a genuine workflow differentiation.

**Score adjustment**: Challenge confirmed 5/5 after star count verification.

---

## 6. Integration Plan

### Decision: **INTEGRATE** ✅ — Score 5/5, Priority: High

### Where to integrate

**1. ultimate-guide.md line ~8104 — Upgrade obra row**

Current row:
```
| **Testing** | test-driven-development | 721 | obra |
```

Upgrade to note the full suite exists, with link to Superpowers.

**2. guide/ecosystem/third-party-tools.md — Plugin Ecosystem section**

Add Superpowers to the Notable Skill Packs section alongside gstack. Entry format:

```markdown
- **[Superpowers](https://github.com/obra/superpowers)** — Full software development methodology suite (95k+ stars). 7 skills covering the complete arc: spec elicitation, implementation planning, subagent-driven development with two-stage review, mandatory TDD (RED → GREEN → REFACTOR), code review, git worktrees, and branch lifecycle completion. Context-aware: skills trigger automatically based on task type. Install: `/plugin install superpowers@claude-plugins-official`. Created by Jesse Vincent (Prime Radiant). MIT. Supported platforms: Claude Code, Cursor, Codex, OpenCode, Gemini CLI.
```

**3. guide/workflows/tdd-with-claude.md — Cross-reference**

Add a note: "Superpowers bundles TDD enforcement as an automatic skill that deletes code written before a test — a stricter version of this workflow available as a plugin."

**4. guide/workflows/spec-first.md — Cross-reference**

Add: "Superpowers' `brainstorming` skill enforces spec-first as a mandatory gate before any code is written, available as a Claude Code plugin."

### Priority

**High** — The obra credibility issue (guide mentions them at 721 installs, not the 95k-star suite) makes this time-sensitive. Fix the obra row first (5 min), then Plugin Ecosystem entry (15 min).

---

## 7. Final Metadata

**Initial Score**: 4/5
**Score after challenge + fact-check**: **5/5**
**Decision**: Integrate ✅
**Confidence**: High (all material facts verified)

**Integration Timeline**:
1. ✅ Evaluation complete (2026-03-18)
2. ⏳ Upgrade obra row in ultimate-guide.md ~line 8104
3. ⏳ Add entry in Plugin Ecosystem section of third-party-tools.md
4. ⏳ Cross-reference from tdd-with-claude.md and spec-first.md

**Archive**: `docs/resource-evaluations/obra-superpowers-evaluation.md`

---

*Evaluation complete: 2026-03-18*
*Attribution: Jesse Vincent, [github.com/obra/superpowers](https://github.com/obra/superpowers)*