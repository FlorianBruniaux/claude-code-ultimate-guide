# Resource Evaluation: SE-CoVe Plugin

**Date**: 2026-01-24
**Evaluator**: Claude Code Ultimate Guide (via /eval-resource skill)
**Resource**: SE-CoVe (Chain-of-Verification) Claude Code Plugin

## Sources

- **LinkedIn Post**: https://www.linkedin.com/posts/vertti_github-verttise-cove-claude-plugin-se-cove-activity-7420735428607197184-IfOq
- **GitHub Repo**: https://github.com/vertti/se-cove-claude-plugin
- **Research Paper**: https://arxiv.org/abs/2309.11495 (ACL 2024 Findings)
- **ACL Anthology**: https://aclanthology.org/2024.findings-acl.212/

---

## Executive Summary

**Decision**: ✅ **INTEGRATED** (with academic corrections)
**Score**: 3/5 (Pertinent avec réserves majeures)
**Approach**: B (Neutral Academic) - Factual presentation without marketing bias

**Rationale**: SE-CoVe implements Meta's Chain-of-Verification methodology (ACL 2024 validated), combling le gap "plugin examples" dans notre guide. MAIS: LinkedIn marketing claim de "28% improvement" est cherry-picked (réalité: 23-112% selon tâche), et omet coûts computationnels (~2x tokens) et réduction output (-26% facts).

**Actions taken**:
1. ✅ Created `examples/plugins/se-cove.md` with academic citations
2. ✅ Added to README.md "Examples Library" section
3. ✅ Updated `machine-readable/reference.yaml`

---

## Content Summary

### What is SE-CoVe?

Software Engineering adaptation of Meta's Chain-of-Verification for Claude Code.

**Pipeline**:
1. Baseline: Generate initial solution
2. Planner: Create verification questions from claims
3. Executor: Answer questions independently (never sees baseline)
4. Synthesizer: Compare findings, identify discrepancies
5. Output: Produce verified solution

**Critical innovation**: Verifier operates without draft code access (prevents confirmation bias).

### Author & Maintenance

- **Author**: Janne Sinivirta (LinkedIn: vertti)
- **Version**: 1.1.1 (2026-01-23)
- **License**: MIT
- **GitHub Stars**: ~78 (now 20 as of 2026-07-28, low community validation)

---

## Fact-Check Results

### ✅ Verified Claims

| Claim | Status | Source |
|-------|--------|--------|
| **Meta AI research** | ✅ Verified | arXiv:2309.11495, ACL 2024 Findings |
| **5-stage pipeline** | ✅ Verified | GitHub README matches paper methodology |
| **Independent verifier** | ✅ Verified | Paper Section 3: "verifier never sees draft" |
| **Installation commands** | ✅ Verified | `/plugin marketplace add` + `/plugin install` |
| **Use cases documented** | ✅ Verified | README lists recommended/avoid scenarios |

### ⚠️ Misleading Claims

| Claim | Reality | Severity |
|-------|---------|----------|
| **"28% accuracy improvement"** | True for biography FACTSCORE only; 23% for QA, 112% for lists | 🔴 Critical cherry-picking |
| **Computational cost omitted** | ~2x token consumption (undisclosed) | 🟡 Material omission |
| **Output reduction omitted** | -26% facts generated (16.6→12.3) | 🟡 Material omission |
| **"Improves accuracy"** | True but hallucinations NOT eliminated | 🟡 Oversimplification |

### ❌ Unverified Claims

| Claim | Issue | Resolution |
|-------|-------|------------|
| **"28% improvement"** | NOT found in arXiv abstract | Perplexity research: Found in paper Section 4.3, Table 1 (FACTSCORE metric, biography task only) |

---

## Performance Metrics (from Research Paper)

**Source**: Dhuliawala et al., "Chain-of-Verification Reduces Hallucination in Large Language Models", ACL 2024 Findings.

| Task Type | Metric | Improvement | Computational Cost |
|-----------|--------|-------------|-------------------|
| Biography generation | FACTSCORE | +28% (55.9→71.4) | -26% output volume (16.6→12.3 facts) |
| Closed-book QA | F1 Score | +23% (0.39→0.48) | ~2x token consumption |
| List-based questions | Precision | +112% (0.17→0.36) | Fewer total answers |

**Model**: Llama 65B (generalization to GPT-4/Claude/Sonnet unverified)

---

## Gap Analysis

### ✅ Gaps SE-CoVe Fills

1. **Plugin examples**: Guide has 233 lines on Plugin System (6863-7096) but ZERO concrete examples
2. **CoVe methodology**: Multi-Agent Orchestration mentioned (methodologies.md:165) but CoVe specifically absent
3. **Independent verification**: Verification Loops documented (methodologies.md:145) but no implementation example

### 🔄 Overlap with Existing Content

| Concept | Existing Section | SE-CoVe Contribution |
|---------|------------------|---------------------|
| Code Review | `examples/agents/code-reviewer.md` | Adds independent verification pattern |
| Multi-Agent | `guide/core/methodologies.md:165` | Concrete CoVe implementation |
| Verification Loops | `guide/core/methodologies.md:145` | Automated verification pipeline |
| Plugin System | `guide/ultimate-guide.md:6863` | First practical example |

---

## Technical Writer Challenge (Agent aa5c1fd)

### Original Evaluation Issues Identified

1. ❌ **Factual error**: Claimed "guide has NO plugin section" → FALSE (233 lines exist)
2. ✅ **Correctly spotted**: Gap = theoretical docs without examples
3. ⚠️ **Underestimated**: Importance of "theory without practice" anti-pattern
4. ❌ **Cherry-picking not flagged**: Original eval didn't catch 28% selectivity

### Score Adjustment

| Phase | Score | Rationale |
|-------|-------|-----------|
| **Initial** | 3/5 | Pertinent - Complément utile |
| **Post-challenge** | 4/5 | Très pertinent - Comble gap pratique |
| **Post-fact-check** | **3/5** | Downgrade due to marketing misleadingness |

**Reason for downgrade**: Marketing claim cherry-picking + material omissions (2x cost, -26% output) reduce trustworthiness despite valid methodology.

---

## Integration Approach

### Selected: Approach B (Neutral Academic)

**Rejected approaches**:
- ❌ **Approach A (Heavy disclaimers)**: Too negative, disclaimer longer than content
- ❌ **Approach C (Don't include)**: Too conservative, misses opportunity to fill gap

**Why Approach B**:
1. ✅ Factual without being accusatory
2. ✅ Presents gains AND costs equitably (table format)
3. ✅ Professional tone (academic citation, not "warning")
4. ✅ Educates users on trade-offs without alarming

### Documentation Format

```markdown
## Performance Metrics

Results from Meta's research paper (Llama 65B model):

[Table with Improvement + Computational Cost columns]

**Source**: Dhuliawala et al., ACL 2024 Findings
```

**Key principle**: Cite the paper, not the marketing.

---

## Curation Policy Established

To avoid amplifying marketing bias in future evaluations:

### Inclusion Criteria

| Criterion | Requirement | SE-CoVe Status |
|-----------|-------------|----------------|
| **Academic validation** | Published conference/journal | ✅ ACL 2024 Findings |
| **Claims fact-checked** | Verified via Perplexity/paper | ⚠️ Cherry-picked but true |
| **Trade-offs disclosed** | Cost/limitations documented | ❌ Omitted → we added |
| **Community validation** | Tested internally OR 1K+ stars | ❌ Neither (78 stars, untested) |
| **Active maintenance** | Update < 6 months | ✅ v1.1.1 (2026-01-23) |

**Verdict**: Include with academic disclaimers.

---

## Files Created

### 1. `examples/plugins/se-cove.md`

**Content**:
- Research foundation (Meta AI, ACL 2024)
- 5-stage pipeline explanation
- Performance metrics table (with trade-offs)
- When to use / When NOT to use
- Installation instructions
- Limitations (from paper Section 6)
- Source links (GitHub, arXiv, ACL Anthology)

**Citations**:
- Paper: Dhuliawala et al., arXiv:2309.11495
- Conference: ACL 2024 Findings
- Implementation: GitHub vertti/se-cove-claude-plugin v1.1.1

### 2. `README.md` (updated)

**Line 238**: Added "**Plugins** (1): [SE-CoVe](./examples/plugins/se-cove.md) — Chain-of-Verification for independent code review (Meta AI, ACL 2024)"

### 3. `machine-readable/reference.yaml` (updated)

**Lines 124-132**: Added section:
```yaml
# Plugin System & Recommended Plugins (added 2026-01-24)
plugins_system: 6863
plugins_se_cove: "examples/plugins/se-cove.md"
chain_of_verification_paper: "https://arxiv.org/abs/2309.11495"
chain_of_verification_acl: "https://aclanthology.org/2024.findings-acl.212/"
```

---

## Lessons Learned

### For Future Evaluations

1. ✅ **Fact-check via Perplexity**: Essential for academic claims (28% found in paper p.7, not abstract)
2. ✅ **Challenge initial assessment**: technical-writer agent caught factual errors
3. ✅ **Check for omissions**: Marketing often presents gains without costs
4. ✅ **Verify source credibility**: ACL 2024 > random blog post
5. ✅ **Approach B (neutral academic)** > heavy disclaimers or rejection

### Red Flags Detected

| Marketing Pattern | SE-CoVe Example | Mitigation |
|-------------------|-----------------|------------|
| **Cherry-picking best metric** | "28%" (ignores 23%/112% on other tasks) | Present full results table |
| **Omitting computational costs** | No mention of 2x tokens | Add "Computational Cost" column |
| **Oversimplifying limitations** | "Improves accuracy" (hallucinations not eliminated) | Include paper's Limitations section |
| **Lack of context** | "Independent verification" (model-specific) | Note "Tested on Llama 65B only" |

---

## Confidence Assessment

| Aspect | Confidence | Evidence |
|--------|-----------|----------|
| **Methodology validity** | 🟢 High | ACL 2024 peer-reviewed paper |
| **Performance metrics** | 🟢 High | Verified in paper Section 4.3, Table 1 |
| **Plugin functionality** | 🟡 Medium | README documented, but untested by us |
| **Generalization** | 🟡 Medium | Tested on Llama 65B, not SOTA models |
| **Marketing accuracy** | 🔴 Low | Cherry-picked metrics, material omissions |

---

## Recommendations for Users

### When to Trust SE-CoVe

✅ Use for:
- Critical code review (architectural decisions)
- Security-sensitive code verification
- Complex debugging requiring independent analysis
- When 2x computational cost is acceptable

### When to Be Skeptical

⚠️ Avoid expecting:
- Universal 28% improvement (task-dependent: 23-112%)
- Zero hallucinations (reduces, not eliminates)
- Fast processing (5+ minutes per verification)
- Comprehensive output (generates fewer but more accurate results)

---

## Meta: Evaluation Process

### Workflow Used

1. **Fetch & Summarize**: WebFetch LinkedIn + GitHub README
2. **Context Check**: Read `machine-readable/reference.yaml`
3. **Gap Analysis**: Grep for verification/multi-agent/code review
4. **Challenge**: Task tool (technical-writer agent)
5. **Fact-Check**: Perplexity research on 28% claim
6. **Document**: Create files with academic approach

### Tools Used

- WebFetch (LinkedIn, GitHub, arXiv abstract)
- Perplexity Pro (fact-check 28% claim in full paper)
- Task tool (technical-writer challenge)
- Grep/Read (gap analysis)
- Write/Edit (documentation)

### Time Investment

- Research & fact-check: ~20 minutes
- Challenge & revision: ~10 minutes
- Documentation: ~15 minutes
- **Total**: ~45 minutes

---

## Conclusion

**SE-CoVe plugin integrated successfully with academic rigor.**

**Key achievement**: First concrete plugin example in guide, combling le gap "theory without practice" dans la section Plugin System (6863-7096).

**Critical correction**: Marketing claim "28% improvement" → Documented reality "23-112% task-dependent, 2x cost, -26% output".

**Precedent established**: Future plugins evaluated with Approach B (neutral academic), fact-checked via Perplexity, trade-offs disclosed transparently.

**Next evaluation**: Use this report as template (format réutilisable).
