# Resource Evaluation: AI's Impact on Software Engineering in 2026

**URL**: https://eventuallymaking.io/p/ai-s-impact-on-the-state-of-the-art-in-software-engineering-in-2026
**Author**: Hugo (Software Engineer, 20+ years, Founder Malt/Writizzy)
**Published**: February 6, 2026
**Type**: Opinion article based on 7 French company interviews
**Evaluated**: February 6, 2026
**Evaluator**: Claude Code Guide Team

---

## Summary

Opinion piece on AI's impact on software engineering practices in 2026, based on interviews with 7 French tech companies (Doctolib, Malt, Alan, Google Cloud, Brevo, ManoMano, Ilek, Clever Cloud).

**Key arguments**:
1. **Context Engineering** (Thoughtworks framework) — shift toward complete specifications with constraints before coding
2. **Spec/Plan/Act workflow standardization** — industry consensus on 3-phase approach
3. **Corporate AI governance** — organizational marketplaces to pool AI skills, agents, rules
4. **QA via CI/CD** — traditional practices (linting, testing, review) essential for AI-generated code validation
5. **HR disruption** — junior training, recruitment, career trajectories require restructuring

**Stats cited**:
- Monthly costs: ~$20/dev (adoption), ~$200/dev (strong adoption), $200-1000+/dev (advanced multi-agent)
- 90%+ of engineers at Alan use AI-powered coding assistants daily
- Interviews: 7 companies (no detailed verbatims provided)

---

## Evaluation Scores

| Criterion | Score (1-5) | Notes |
|-----------|-------------|-------|
| **Relevance** | 2 | Marginal — concepts largely covered in guide, one legitimate gap (Context Engineering) |
| **Accuracy** | 3 | Moderate — terminology error ("Context Driven" vs "Context Engineering"), stats lack methodology |
| **Actionability** | 1 | Low — no templates, code, or concrete workflows |
| **Novelty** | 2 | Marginal — Spec/Plan/Act and QA/CI/CD already in guide, Context Engineering framework new |
| **Production-Ready** | 1 | Low — opinion piece, no implementation details |

**Overall Score**: **2/5** (Marginal - Info secondaire)

---

## Gap Analysis

### What's NEW (not in guide)

| Aspect | Hugo's Resource | Our Guide | Gap? |
|--------|----------------|-----------|------|
| **Context Engineering** (Thoughtworks) | ✓ Mentioned (but miscited as "Context Driven") | ✗ Absent | ✅ **Legitimate gap** |
| **Corporate AI marketplaces** | ✓ Concept described | ✗ Not covered | ⚠️ **Minor gap** (RH focus, not technical) |

### What's ALREADY COVERED

| Aspect | Hugo's Resource | Our Guide |
|--------|----------------|-----------|
| Spec/Plan/Act workflow | ✓ Described | ✅ `guide/workflows/spec-first.md`, `/plan` mode |
| QA via CI/CD | ✓ Mentioned | ✅ `guide/production-safety.md`, hooks |
| HR/Junior disruption | ✓ Opinion | ✅ `guide/learning-with-ai.md` (comprehensive) |
| Cost estimates | ✓ Ranges ($20-1000) | ✅ `guide/ai-ecosystem.md` (precise: $20-50) |

---

## Fact-Check Results

| Claim | Verified | Source | Correction |
|-------|----------|--------|------------|
| **"Context Driven Engineering"** | ⚠️ **Terminology error** | Perplexity search | ✅ Correct term: "Context Engineering" (Thoughtworks Tech Radar Vol 33, Nov 2025) |
| **"90%+ engineers at Alan"** | ✅ Yes | Emma Goldblum quote (article) | ✅ Verbatim exact |
| **"$20-200-1000/dev costs"** | ✅ Table present | Article | ⚠️ No methodology, 50x spread too large |
| **"Hugo 20+ years XP"** | ✅ Yes | Schema markup | ✅ Malt CTO 2012-2024, Writizzy founder 2025 |
| **"Published Feb 6, 2026"** | ✅ Yes | Metadata | ✅ Correct |
| **"Interviews 7 companies"** | ✅ List present | Article | ⚠️ No verbatims, no raw data |

**Critical error detected**: Hugo miscites Thoughtworks framework as "Context Driven Engineering" when the actual term is "Context Engineering" (verified via Perplexity and Thoughtworks Technology Radar Vol 33).

---

## Technical-Writer Challenge

**Agent ID**: `ae2f481` (technical-writer subagent)

**Challenge summary**:
- Initial score 4/5 **reduced to 2/5** after critical analysis
- Overestimated novelty — Spec/Plan/Act already in `spec-first.md`, QA/CI/CD in `production-safety.md`
- Underestimated marketing angle — no peer review, stats lack methodology, Writizzy link in footer
- Compared unfavorably to validated score-4 resources (Pat Cullen: 3 templates, Paddo: 10 actionable tips)

**Legitimate points**:
- "Context Engineering" (Thoughtworks) is a real gap in the guide
- Corporate governance angle minimally covered
- Stats too vague for practical use ($20-1000 spread, no methodology)

**Recommendation upheld**: Minimal integration (footnotes only), not full section.

---

## Integration Decision

**Action taken**: **Minimal integration** (2 footnotes)

### 1. Context Engineering (Thoughtworks) — Priority HIGH

**File**: `guide/methodologies.md` (after line 66, "Foundational Discipline" section)

**Added**:
```markdown
> **Context Engineering**: Thoughtworks designates this broader approach "Context Engineering"
> in their Technology Radar (Nov 2025) — the systematic design of information provided to LLMs
> during inference. Three core techniques: context setup, context management for long-horizon
> tasks, and dynamic information retrieval. Related patterns in Claude Code: AGENTS.md,
> MCP Context7, Plan Mode.
```

**Rationale**: Legitimate framework gap, verified via Perplexity and Thoughtworks documentation.

### 2. Corporate AI Marketplaces — Priority LOW

**File**: `guide/adoption-approaches.md` (after line 277, "Larger Team" section)

**Added**:
```markdown
> **Emerging approach**: Some organizations explore "corporate AI marketplaces" to pool AI
> skills, agents, and rules at the organizational level rather than individual teams
> (Hugo/Writizzy 2026). Few documented production implementations yet, but the concept
> addresses governance at scale.
```

**Rationale**: Interesting RH concept, minimal technical implementation details available.

---

## Why NOT More Integration?

### Rejected: Full "Team Governance" section

**Reason**: Redundant with existing content:
- `guide/adoption-approaches.md` lines 236-278 already cover team coordination
- `guide/production-safety.md` covers hooks and permission rules
- `guide/security-hardening.md` covers team conventions

### Rejected: Stats integration

**Reason**: Unusable methodology:
- "$20-1000/dev" range is 50x spread
- No methodology documentation
- Our guide has more precise estimates (`ai-ecosystem.md`: $20-50 Claude Code typical)

### Rejected: Citing "Context Driven Engineering"

**Reason**: Term doesn't exist — Thoughtworks framework is "Context Engineering"

---

## Comparison to Other Evaluations

| Resource | Score | Templates/Code | Stats Quality | Integration |
|----------|-------|----------------|---------------|-------------|
| **Pat Cullen** (review-pr) | 4/5 | 3 templates | N/A | Full guide section |
| **Paddo Team Tips** | 4/5 | 0 (10 actionable tips) | N/A | Integrated throughout |
| **RTK** | 4/5 | 1 tool + examples | Measured 72.6% reduction | Full guide section |
| **Hugo AI Impact** | **2/5** | 0 | Vague ($20-1000 spread) | **2 footnotes only** |

---

## Lessons Learned

### Evaluation Process Improvements

1. **Terminology verification**: Always cross-check framework names with authoritative sources (Perplexity, official docs)
2. **Gap analysis rigor**: Grep existing guide before claiming "missing content"
3. **Stats scrutiny**: Require methodology documentation, not just numbers
4. **Technical-writer challenge**: Proved valuable — caught overestimation of novelty

### What Worked

1. **Fact-check protocol**: Caught terminology error early
2. **Agent challenge**: technical-writer agent provided brutal but accurate reality check
3. **Minimal integration**: 10-minute footnotes vs 2-hour full section = better ROI

---

## Sources

- **Primary**: Hugo, ["AI's Impact on State of the Art in Software Engineering in 2026"](https://eventuallymaking.io/p/ai-s-impact-on-the-state-of-the-art-in-software-engineering-in-2026), Feb 6, 2026
- **Verification**: Perplexity search for "Context Engineering Thoughtworks 2024 2025"
- **Authoritative**: [Thoughtworks Technology Radar Vol 33](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2025/11/tr_technology_radar_vol_33_en.pdf), Nov 2025
- **Supporting**: [Thoughtworks macro trends blog](https://www.thoughtworks.com/insights/blog/technology-strategy/macro-trends-tech-industry-november-2025)

---

## Metadata

- **Evaluation date**: 2026-02-06
- **Time spent**: ~45 minutes (research, fact-check, agent challenge, integration)
- **Agent tools used**: WebFetch, Grep, Read, Perplexity, Task (technical-writer)
- **Integration time**: 10 minutes (2 footnotes)
- **Files modified**: 2 (`guide/methodologies.md`, `guide/adoption-approaches.md`)
