# Resource Evaluation: Allan Hill - "The Real Secret to Agentic Development is Small PRDs and Vertical Slices"

**Source**: https://www.linkedin.com/pulse/real-secret-agentic-development-small-prds-vertical-slices-allan-hill-puihc/
**LinkedIn post**: https://www.linkedin.com/posts/allanhillgeek_ai-is-the-easy-part-decomposition-is-the-activity-7430210715606556672-HHa6/
**Author**: Allan Hill (@allanhillgeek), Fractional CTO
**Type**: LinkedIn Pulse article (opinion + architecture walkthrough)
**Published**: ~Early 2026 (exact date not shown)
**Evaluation Date**: 2026-02-19
**Evaluator**: Claude Sonnet 4.6
**Challenger**: general-purpose agent (ac79d16)
**Score**: **3/5** (Pertinent — intégration ciblée, pas fichier dédié)

---

## 📄 Summary

Allan Hill describes a production agentic development pipeline built around the thesis that decomposition discipline matters more than AI sophistication:

- **Core thesis**: "AI is the easy part. Decomposition is the hard part." — The bottleneck in agentic development is breaking work into AI-digestible units before handing to agents, not prompt optimization
- **Key unit of work**: Vertical Slice — thin, end-to-end feature through all stack layers for one complete user behavior (e.g. "password reset via email"); ideal for agents because clear boundaries → reviewable PR
- **3-phase pipeline**: Phase 0 (PM agents produce Small PRDs with 6-dimension quality review) → Phase 1 (Orchestrator decomposes PRD into ordered independent slices, human Slack approval required) → Phase 2 (per-slice: Gherkin scenarios → ATDD → implementation → PR)
- **Infrastructure**: Multipass VMs (1 per ticket), Node.js dispatcher polling GitHub API every 60s, deterministic CI (ESLint/Playwright/SonarQube) + AI CI (5 parallel review agents via GitHub Actions)
- **Open challenges acknowledged**: resume state fragility, Boy Scout Rule vs PR scope balance, review agent false positive tuning

---

## 🎯 Score: 3/5 — Pertinent, intégration ciblée

### Justification

**Arguments for 3 (not 4):**
- Pipeline too tightly coupled to specific stack (Multipass/GCP/Jira/Slack) → ~80% must be rewritten for generic use; low reuse
- No production metrics: no cycle time data, defect rates, throughput — it's architectural storytelling, not validated case study
- Core concepts (vertical slices, decomposition-first) originate in Agile literature (Dan North BDD 2003, David Hussman) — this is Agile applied to AI agents, not novel theory
- Open challenges are unresolved (resume state fragility, false positive tuning) — documenting unstable practices as reference is risky
- Claude Code is not explicitly mentioned; author uses "agents" generically — mapping to the guide is indirect

**Arguments against 5 (confirmed gaps are real but not critical):**
- Gap "task decomposition" is legitimate but partially addressable by existing `spec-first.md`
- The 6-dimension PRD review checklist is extractable and generic — the single most actionable content in the article
- ATDD is genuinely absent from the guide (only TDD covered)

---

## ⚖️ Gap Analysis vs. Claude Code Ultimate Guide

| Aspect | This resource | Guide (grep-verified) |
|--------|--------------|----------------------|
| Vertical slice as AI work unit | ✅ Core framework | ❌ Zero mentions |
| Small PRD with 6 quality dimensions | ✅ Actionable checklist | ❌ Absent |
| ATDD (Acceptance Test-Driven Dev) | ✅ Phase 2 core pattern | ❌ Only TDD covered |
| Task decomposition discipline | ✅ Main thesis | ❌ Not addressed |
| Human approval gates in pipeline | ✅ Slack approval at Phase 1 | ⚠️ Mentioned conceptually |
| AI review agents in CI/CD | ✅ 5 parallel agents pattern | ❌ Not documented |
| Orchestrator → slice decomposition | ✅ Explicit | ⚠️ Orchestration exists, not pipeline |
| VM per ticket isolation | ✅ Multipass pattern | ❌ Absent |
| Spec before code | ↔️ Related different scope | ✅ `spec-first.md` (CLAUDE.md spec) |
| Multi-agent orchestration | ↔️ Implicit | ✅ `workflows/agent-teams.md` |

---

## 📍 Recommendations

**Priority: Medium — integrate 2 specific patterns, not the full pipeline**

### Integration 1: `guide/workflows/spec-first.md` — Add "Task Granularity" section

Extract the 6-dimension PRD quality checklist as a generic pre-coding checklist:

```markdown
## PRD Quality Checklist (before handing to agents)

Before assigning work to an agent, verify the task definition covers:

1. **Problem Clarity** — Is the problem statement unambiguous?
2. **Testable Acceptance Criteria** — Can completion be verified automatically?
3. **Scope Boundaries** — What is explicitly OUT of scope?
4. **Observable Done Definition** — What does "done" look like to an end user?
5. **Requirements Clarity** — No ambiguous terms, no implementation details
6. **Terminology Consistency** — Same terms used throughout (not "user" and "account" interchangeably)
```

**Location**: After the "The Pattern" section in `spec-first.md` (~line 60)
**Effort**: Low (20-30 lines)

### Integration 2: `guide/methodologies.md` — Add ATDD section

ATDD is genuinely absent. Add a section explaining how ATDD extends TDD for agent workflows:
- Gherkin scenarios as the contract between PM intent and implementation
- Write Gherkin first → agent writes failing tests → implementation

**Location**: After TDD section in `guide/methodologies.md`
**Effort**: Medium (50-80 lines)

### What NOT to do

❌ Do NOT create `guide/workflows/agentic-pipeline.md` — pipeline is too stack-specific, author's challenges are unresolved, and it would document an unstable pattern as authoritative. Wait for a second independent source before creating a dedicated workflow guide.

---

## 🔥 Challenge Verdict

**Challenger (ac79d16) conclusions:**
- **Score 3/5 confirmed** — "storytelling architecturel, pas case study validé"
- **Most actionable content**: 6-dimension PRD checklist — treat as standalone checklist, not full pipeline
- **Best integration path**: Existing files (`spec-first.md` + `methodologies.md`), not new file
- **Key oversight in initial eval**: Article doesn't mention Claude Code specifically — the mapping is indirect

**Points raised not in initial analysis:**
- Human Slack approval gate is under-analyzed as human-in-the-loop pattern
- Stack dependency (Jira + GitHub + Slack + GCP) makes direct reuse impractical
- "Vertical slices" concept is Agile (2003) not AI-native — risk of documenting old concept as new insight

---

## ✅ Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| Author = Allan Hill, Fractional CTO | ✅ | LinkedIn profile (browser extraction) |
| Article accessible without auth | ✅ | WebFetch succeeded on Pulse URL |
| 3-phase pipeline structure | ✅ | Direct article extraction |
| 6 PRD review dimensions (Problem Clarity, Testable Criteria, Scope Boundaries, Observable Done, Requirements Clarity, Terminology Consistency) | ✅ | Direct article extraction |
| ATDD approach (Gherkin → failing tests → implementation) | ✅ | Direct article extraction |
| 5 parallel AI review agents in CI | ✅ | Direct article extraction |
| Multipass VMs + Node.js dispatcher | ✅ | Direct article extraction |
| Open challenges: resume state fragility | ✅ | Author explicitly lists it |
| "Vertical slices" from Agile literature (Dan North 2003) | ✅ | Perplexity context — established pattern |
| Claude Code mentioned specifically | ❌ | Article uses generic "agents" — Claude Code NOT mentioned |
| Production metrics (cycle time, defect rates) | ❌ | Not present in article |

**No hallucinations.** Score downgraded from initial "inspiration-level 3/5" to confirmed "targeted-integration 3/5" based on full content.

---

## 🎯 Final Decision

- **Score**: **3/5** — Pertinent, intégration ciblée
- **Action**: Intégrer 2 éléments spécifiques dans fichiers existants (PRD checklist + ATDD)
- **Do NOT create**: New `agentic-pipeline.md` file
- **Confidence**: High (full article read, challenge performed, fact-checked)
- **Trigger for re-evaluation**: Second independent source documenting vertical slice pattern for Claude Code specifically → would justify 4/5 + dedicated workflow file

**Related evaluations:**
- `addy-osmani-good-spec.md` (4/5) — overlapping territory (spec quality, PRD structure)
- `spec-first.md` in guide — primary integration target
- `guide/methodologies.md` — secondary integration target (ATDD)