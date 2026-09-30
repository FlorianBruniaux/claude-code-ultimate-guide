# Resource evaluation: "You're probably using Claude Code wrong" - Alex Ischenko

## Metadata

| Field | Value |
|-------|-------|
| **Author** | Alex Ischenko |
| **Role** | AI-Driven CTO, Top 100 Leaders @ CTO Craft |
| **Published** | 2026-03-19 |
| **Type** | LinkedIn Pulse article |
| **URL** | https://www.linkedin.com/pulse/youre-probably-using-claude-code-wrong-i-too-until-shift-ischenko-bwdkf/ |
| **Evaluated** | 2026-03-19 |
| **Score** | 2/5 (Marginal) |
| **Decision** | Do not integrate |

## Summary

LinkedIn article arguing that Claude Code quality is an engineering system question, not a model question. Proposes 7 workflow patterns for improving output quality, each with a full copy-paste prompt template:

1. **Reality checks before implementation** - verify codebase assumptions before coding
2. **Separate author/reviewer** - two-role pattern within same session
3. **Project-aware reviews** - review with project context, not just diff
4. **Requirements as mandatory artifact** - REQUIREMENTS.md before code
5. **TDD workflow** - anchor behavior with tests first
6. **Small task sizes** - reduce scope for better AI output
7. **Human abstraction elevation** - move engineers to architecture/trade-off level

Claims "20-30% quality improvement" from these workflow changes.

## Scoring rationale

### Overlap with guide (75-85%)

| Pattern | Guide Coverage | Location |
|---|---|---|
| Reality checks | Partial | `exploration-workflow.md`, Plan Mode (L3717) |
| Author/reviewer | Moderate | SE-CoVe (L13095), Scope-Focused Agents (L4410) |
| Project-aware reviews | Partial | `code-review.md` (CLAUDE.md + REVIEW.md) |
| Requirements artifact | Partial | `spec-first.md` (full workflow) |
| TDD | Strong | `tdd-with-claude.md`, L19183-19320, skill template L7336 |
| Small tasks | Scattered | `spec-first.md` L62-93, L1529, L1733 |
| Human elevation | Thin | L17458, L15725, L3216 |

### What's unique

The 7 copy-paste prompt templates are the only non-redundant element. These are practical formatting convenience but not structural insight. The guide's existing workflow files and skill templates serve the same purpose.

### Credibility assessment

- No GitHub repo, no production artifact, no tooling behind the article
- "20-30% quality improvement" has no methodology, no baseline, no control group
- Compare to higher-scored resources: Cullen (shipped working slash command, 5/5), Chabaud (clonable repo, 3/5), Rusitschka (repo with working code, 4/5)

### Accumulation risk

The guide already integrates Chabaud, Rusitschka, Cullen, and paddo.dev team tips covering adjacent workflow territory. Adding Ischenko without new substance dilutes the signal-to-noise ratio.

## Identified Gaps (for future work, not from this resource)

Two gaps surfaced during analysis that the guide could address independently:

1. **Multi-model review pattern** (near zero coverage): deliberately using different models to review each other's work. Ischenko mentions it briefly but provides no template.
2. **Consolidated task sizing section**: currently scattered across multiple files with no single reference point.

## Fact-check

| Claim | Status | Notes |
|---|---|---|
| Author credentials | Unverifiable | CTO Craft exists, "Top 100" not independently verifiable |
| "20-30% quality improvement" | Unfalsifiable | No methodology described |
| Tool landscape (Claude Code, Cursor, etc.) | Verified | All exist as active tools |
| LLM behavioral patterns (overconfidence, compound errors) | Verified | Well-documented in literature |

## Decision

**Do not integrate.** Solid engineering advice but the guide already covers these patterns through better-sourced, more detailed, and more production-grounded resources. The prompt templates could theoretically be extracted as addenda to existing workflow files, but this is low priority.
