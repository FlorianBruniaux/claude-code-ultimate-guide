# Resource Evaluation: Addy Osmani - "How to write a good spec for AI agents"

**Resource**: https://addyosmani.com/blog/good-spec/
**Author**: Addy Osmani (former Head of Chrome Developer Experience at Google, 14 years on Chrome team)
**Published**: 2026-01-13
**Evaluation Date**: 2026-02-01
**Evaluator**: Claude Code Ultimate Guide Team
**Score**: **4/5** (High Value - Integrate within 1 week)

---

## Summary

Comprehensive guide on writing effective specifications for AI coding agents (Claude Code, Gemini CLI, Cursor, GitHub Copilot). Published by Addy Osmani (author of "Learning JavaScript Design Patterns" - O'Reilly, former Chrome team lead) 19 days ago.

**Key contributions:**
- Six core spec areas (commands, testing, project structure, code style, git workflow, boundaries)
- Three-tier boundary system (Always/Ask first/Never) for operational decision-making
- Modular prompts strategy to avoid context overload
- Built-in verification and self-checks
- Anti-patterns: monolithic CLAUDE.md, vague instructions

**Why 4/5:** Fills specific gaps in our `guide/workflows/spec-first.md` (modular design, operational boundaries, command specs) with patterns directly applicable to Claude Code workflows. From credible practitioner, published recently, addresses daily user pain points.

---

## Scoring Breakdown

### 1. Relevance to Claude Code (5/5)

✅ **Directly applicable**: All six spec areas map to Claude Code's `.claude/` structure
✅ **CLAUDE.md focus**: Explicitly uses CLAUDE.md as persistent reference pattern
✅ **Permission modes**: Three-tier boundaries align with Claude Code's ask/auto-accept/plan modes
✅ **MCP integration**: Mentions Context7, skills system, agent coordination

**Evidence**: Article uses Claude Code examples, references Anthropic documentation, shows command specs (`npm test`, `pytest -v`).

### 2. Technical Accuracy (5/5)

✅ **Fact-checked**: All claims verified (2,500+ GitHub configs analysis, six core areas, three-tier boundaries)
✅ **Author credentials verified**: Addy Osmani (14 years Chrome, O'Reilly author) via Perplexity search
✅ **No hallucinations**: Statistics sourced from GitHub blog, tools correctly named

**Minor correction**: Osmani left Chrome team Dec 1, 2025 (still at Google, different role).

### 3. Novelty/Uniqueness (4/5)

✅ **Modular prompts**: Not explicitly covered in our spec-first.md (new pattern)
✅ **Operational boundaries**: Always/Ask/Never framework missing from our binary MUST/MUST NOT
✅ **Command specs**: Template for executable commands not in our guide
⚠️ **Some overlap**: Feature/API spec templates already exist (spec-first.md:55-156)

**Gap analysis**: 3 out of 6 core patterns are net-new to our guide.

### 4. Practicality (5/5)

✅ **Immediately actionable**: Each pattern has concrete examples (React/TypeScript stack, testing commands)
✅ **Daily workflow impact**: Addresses context pollution (>200 line CLAUDE.md problem)
✅ **Solves real pain**: Modular design prevents performance degradation
✅ **No dependencies**: Patterns work with existing Claude Code setup

**User impact**: High - reduces context overhead, improves spec clarity, provides operational framework.

### 5. Source Credibility (5/5)

✅ **Professional credentials**: Google Chrome team (14 years), O'Reilly author
✅ **Recent publication**: Jan 13, 2026 (19 days ago) = current best practices
✅ **Cited sources**: GitHub blog (2,500+ configs), Anthropic docs, research papers
✅ **Production validation**: Patterns from real-world AI agent usage at scale

**Authority level**: Expert practitioner (not just theorist).

---

## Comparative Analysis

| Aspect | Osmani Article | Our Guide (spec-first.md) |
|--------|----------------|---------------------------|
| **Spec Structure** | 6 areas (commands, testing, structure, style, git, boundaries) | ✅ Feature/Architecture/API templates (lines 55-156) |
| **CLAUDE.md Pattern** | ✅ Persistent reference | ✅ Core pattern (line 31: "CLAUDE.md IS your spec file") |
| **Boundaries/Constraints** | ✅ 3-tier (Always/Ask/Never) | ⚠️ **GAP**: Binary MUST/MUST NOT, lacks operational framework |
| **Modular Prompts** | ✅ Break tasks into focused pieces | ❌ **GAP**: Not explicitly covered |
| **Self-Checks** | ✅ Built-in verification commands | ⚠️ Acceptance criteria only (lines 75-78) |
| **Command Specs** | ✅ Executable command templates | ❌ **GAP**: Focus on feature specs only |
| **Anti-Patterns** | ✅ Warns against bloated CLAUDE.md | ⚠️ Mentions "keep concise (<200 lines)" but no modularization strategy |

**Verdict**: 3 major gaps + 2 partial gaps = High integration value.

---

## Integration Plan

### Primary Integration: guide/workflows/spec-first.md

**Add 4 new sections** (after line 318, before "See Also"):

1. **"Modular Spec Design"** (~50 lines, lines 320-369)
   - Pattern: Split large specs into multiple CLAUDE.md files (per-feature/domain)
   - When to split: >200 lines, multi-domain projects, team collaboration
   - Example: `CLAUDE-auth.md`, `CLAUDE-api.md`, `CLAUDE-testing.md`
   - Reference Osmani's "focused pieces" principle

2. **"Operational Boundaries"** (~60 lines, lines 370-429)
   - Extend MUST/MUST NOT with **Always/Ask First/Never** framework
   - Map to Claude Code permission modes:
     - **Always** → Auto-accept mode (tests, formatting)
     - **Ask First** → Default mode (schema changes, dependencies)
     - **Never** → Plan mode/blocked (production push, secrets)
   - Decision table with examples

3. **"Command Spec Template"** (~40 lines, lines 430-469)
   - Template for testing, CI, deployment commands
   - Format: `command → expected output → error handling`
   - Example: `pnpm test` → coverage report → fail on <80%

4. **"Anti-Pattern: Monolithic CLAUDE.md"** (~30 lines, lines 470-499)
   - Explain cognitive load problem (>200 lines = context pollution)
   - Show split strategies (feature-based, role-based, workflow-based)
   - Link to Osmani article for deeper rationale

**File growth**: 327 lines → ~507 lines

### Secondary Updates

**machine-readable/reference.yaml** (8 new entries after line 476):
```yaml
spec_first_workflow: "guide/workflows/spec-first.md"
spec_modular_design: "guide/workflows/spec-first.md:320"
spec_operational_boundaries: "guide/workflows/spec-first.md:370"
spec_command_template: "guide/workflows/spec-first.md:430"
spec_anti_monolithic: "guide/workflows/spec-first.md:470"
spec_osmani_source: "https://addyosmani.com/blog/good-spec/"
spec_osmani_evaluation: "docs/resource-evaluations/addy-osmani-good-spec.md"
spec_osmani_score: "4/5"
```

**README.md** (line 427): Update count `35 → 36 assessments`

---

## Risks of NOT Integrating

1. **Users write bloated, monolithic CLAUDE.md** → Context pollution → Performance degradation → Frustration
2. **No operational framework for boundaries** → Users struggle to map MUST/MUST NOT to daily decisions (when to trust vs validate)
3. **Missed best practice from credible source** → Guide loses authority when practitioners cite Osmani but don't find it referenced here
4. **No command spec pattern** → Users only write feature specs, miss tooling/workflow configuration opportunities

**Impact**: Medium-High. These are daily workflow issues, not edge cases.

---

## Challenge Phase (technical-writer agent feedback)

**Initial score**: 3/5 → **Corrected to 4/5** ✅

**Undervaluation identified:**
- Modular prompts = fundamental gap (not "nice to have")
- Three-tier boundaries = operational framework missing from binary MUST/MUST NOT
- Command spec templates = daily workflow pattern not covered
- Professional credibility (Osmani's credentials) underweighted

**Arguments for 4/5 validated:**
- Fills specific, actionable gaps users encounter daily
- From credible practitioner (14 years Chrome, O'Reilly author)
- Published recently (19 days ago) = current best practices
- Directly applicable to Claude Code workflows

---

## Fact-Check Summary

| Claim | Verified | Source |
|-------|----------|--------|
| Addy Osmani = Chrome team | ⚠️ **Partially** | Was on Chrome 14 years, left Dec 1, 2025 (Perplexity search) |
| Author "Learning JavaScript Design Patterns" | ✅ **Yes** | O'Reilly book verified (1st ed 2012, 2nd ed recent) |
| Published Jan 13, 2026 | ✅ **Yes** | WebFetch confirmed |
| 2,500+ agent configs analyzed | ✅ **Yes** | Cited from GitHub blog in article |
| Six core areas | ✅ **Yes** | Commands, testing, structure, style, git, boundaries (article text) |
| Three-tier boundaries | ✅ **Yes** | Always/Ask first/Never system (article text) |

**Corrections applied**: Osmani is **former** Chrome team (current: different role at Google).

**Confidence**: High (all major claims verified, minor correction on current role).

---

## Decision

**Final Score**: **4/5** (High Value - Integrate within 1 week)

**Action**: **INTEGRATE**
- Add 4 sections to spec-first.md (~180 lines)
- Update reference.yaml with 8 new entries
- Increment README.md evaluation count
- Cite Osmani as practitioner validation

**Priority**: **High** (within 1 week)

**Rationale**: Fills specific, actionable gaps (modular design, operational boundaries, command specs) that users encounter daily. From credible practitioner, published recently (19 days ago), directly applicable to Claude Code workflows. Not theoretical—these patterns improve real-world spec quality and prevent context pollution.

---

**Integration Status**: ✅ **COMPLETED** (2026-02-01)
**Files Modified**: spec-first.md (+180 lines), reference.yaml (+8 entries), README.md (+1 count)
