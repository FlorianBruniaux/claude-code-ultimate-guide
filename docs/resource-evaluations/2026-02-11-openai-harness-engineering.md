# Resource evaluation: OpenAI harness engineering (ryan Lopopolo, Feb 2026)

**Source**: https://openai.com/index/harness-engineering/
**Type**: Engineering blog post, OpenAI
**Author**: Ryan Lopopolo (OpenAI)
**Date of evaluation**: 2026-05-09

---

## Summary

First-person account of building a 1M-line internal product using Codex agents exclusively, with zero manual code, over 5 months with a 3-person engineering team. The reported throughput was 3.5 PRs per engineer per day.

The post is not a tutorial. It is a practitioner's retrospective on what environmental engineering decisions made that throughput possible. The central argument: model capability is only one variable. The harness (instruction files, knowledge base structure, observability, linters, architecture enforcement) determines whether capable models produce reliable output at scale.

**10 patterns documented**:

1. AGENTS.md as ~100-line TOC pointing to a docs/ hierarchy, not an encyclopedia
2. "What the agent can't see doesn't exist": everything implicit must be encoded as repo content
3. Exec plans as first-class artifacts in docs/exec-plans/ with active/completed/tech-debt-tracker structure
4. Ephemeral per-worktree observability stack (Vector, VictoriaLogs/Metrics/Traces, LogQL/PromQL/TraceQL)
5. Taste invariants: opinionated mechanical rules encoded as custom linters with agent-readable error messages
6. Doc-gardening agent: recurring background agent that opens PRs when docs drift from code behavior
7. Anti-entropy via background cleanup agents that track quality scores per domain (QUALITY_SCORE.md)
8. Layered domain architecture enforced by linters: Types, Config, Repo, Service, Runtime, UI
9. High-throughput merge philosophy: fixes cheap, waiting expensive (only valid at genuine agent throughput levels)
10. Agent autonomy progression: full end-to-end loop from bug reproduction to PR to merge

---

## Relevance score: 5/5 (Critical)

### Justification

**Strengths**:
- First published account of a complete production system built exclusively by agents at this scale (1M lines, 5 months, 3 engineers)
- Introduces patterns not present elsewhere in the guide: ephemeral observability stacks, taste invariants as linter-encoded rules, doc-gardening agents, layered domain architecture as a prerequisite rather than a deferred decision
- Directly extends §9.25 Harness Engineering with production-validated evidence
- Figures cited (3.5 PRs/engineer/day, 1M lines, 5 months, zero manual code) come from a named author at OpenAI with first-person attribution
- No overlap with HumanLayer patterns already in §9.25; these are complementary, not duplicative

**Limitations**:
- Single company's internal toolchain (Codex-specific worktree setup, internal observability infrastructure); some patterns require significant investment to replicate
- No independent verification of throughput claims
- Observability stack (Vector + VictoriaLogs + ephemeral per-worktree setup) assumes infrastructure access not universally available

**Why 5/5 and not 4/5**:

The Anthropic Agentic Trends report (4/5) provided industry validation of known patterns. This post introduces new patterns. The AGENTS.md-as-TOC principle, taste invariants with agent-readable linter messages, and the anti-entropy model via background cleanup agents are not documented elsewhere in the guide and directly address failure modes practitioners encounter at scale. Score stays at 5/5 because the marginal information density is high and the integration path is clear.

---

## Comparison with existing guide content

| Pattern from article | Existing guide coverage | Action |
|----------------------|------------------------|--------|
| AGENTS.md as TOC | §9.25 mentions AGENTS.md as an Instructions subsystem artifact, no guidance on size or structure | Add §9.25.1 |
| What agent can't see doesn't exist | §3.1 CLAUDE.md covers instruction files, no knowledge boundary principle | Add §9.25.2 |
| docs/ knowledge base structure | No equivalent structure documented | Add §9.25.3 |
| Exec plans as first-class artifacts | §9.25 feature_list.json covers scope tracking, not plan/decision records | Add in §9.25.3 |
| Ephemeral observability stack | §9.5 Tight Feedback Loops covers test/lint/typecheck, not runtime observability | Add §9.25.4 |
| Taste invariants + custom linters | §9.25 Verification Gap covers lint as verification, not as agent-readable instruction injection | Add §9.25.5 |
| Doc-gardening agent | §9.24 Instinct-Based Continuous Learning touches on session notes, not doc-behavior drift detection | Add §9.25.3 |
| Anti-entropy / quality scores | No equivalent | Add §9.25.5 |
| Layered domain architecture | §8.x Architecture sections discuss patterns, not enforcement as prerequisite at agent scale | Add §9.25.5 |
| High-throughput merge philosophy | No equivalent | Add §9.25.5 |

**Overlap with existing §9.25**: approximately 0%. The HumanLayer patterns (Verification Gap, WIP=1, Session Lifecycle, feature_list.json, init.sh, progress.md) are orthogonal. Both sets address the harness, but at different layers.

---

## Integration decision

**Action**: Integrate as §9.25.1 through §9.25.5 (new subsections appended to existing §9.25)

**Rationale**: The patterns complement, not duplicate, the HumanLayer content already in §9.25. Adding subsections preserves the existing content while extending coverage to the knowledge base, observability, and enforcement layers of the harness.

**Files to modify**:
1. `guide/ultimate-guide.md`: add §9.25.1 through §9.25.5 after the existing Templates section
2. `machine-readable/reference.yaml`: add 9 new entries in the deep_dive section
3. `CHANGELOG.md`: log under [Unreleased]

**Priority**: Immediate. These patterns address failure modes that practitioners hit at scale and that are not covered elsewhere in the guide.

---

## Fact-check

| Claim | Verifiable | Notes |
|-------|-----------|-------|
| 1M-line codebase | First-person, named author | Cannot independently verify; cited as stated |
| 5 months | First-person, named author | Cannot independently verify; cited as stated |
| 3-person team | First-person, named author | Cannot independently verify; cited as stated |
| 3.5 PRs/engineer/day | First-person, named author | Cannot independently verify; cited as stated |
| Zero manual code | First-person, named author | Cannot independently verify; cited as stated |
| Layered architecture (Types/Config/Repo/Service/Runtime/UI) | Described in post | Architectural claim, not a metric |
| Observability stack components (Vector, VictoriaLogs, VictoriaMetrics, Jaeger-compatible traces) | Described in post | Technology names verifiable independently |

All figures cited in the guide carry the attribution "Ryan Lopopolo, OpenAI Engineering blog, Feb 2026" and are presented as claimed, not as independently verified.

---

## Final decision

- **Score**: 5/5 (Critical)
- **Action**: Integrate as §9.25.1 through §9.25.5
- **Timeline**: Immediate
- **Confidence**: High (patterns are novel, directly applicable, and fill documented gaps in the guide)

---

**File**: `docs/resource-evaluations/2026-02-11-openai-harness-engineering.md`
**Version**: 1.0
**Date**: 2026-05-09
**Evaluator**: Claude Sonnet 4.6 (Technical Writer)
