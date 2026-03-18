# Resource Evaluation: "Echoes of AI: Investigating the Downstream Effects of AI Assistants on Software Maintainability"

**Date:** 2026-02-19
**Evaluator:** Claude Code (eval-resource skill)
**Status:** Integrated (section Productivity Research)

---

## Resource Details

| Field | Value |
|-------|-------|
| **Title** | Echoes of AI: Investigating the Downstream Effects of AI Assistants on Software Maintainability |
| **Authors** | Markus Borg, Dave Hewett, Nadim Hagatulah, Noric Couderc, Emma Söderberg, Donald Graham, Uttam Kini, Dave Farley |
| **Dave Farley credentials** | Co-author of "Continuous Delivery" (with Jez Humble), Jolt Award winner |
| **Publication Date** | July 2025 |
| **URL** | https://arxiv.org/abs/2507.00788 |
| **Type** | Academic preprint (arXiv, not yet peer-reviewed in conference proceedings as of 2026-02-19) |
| **LinkedIn context** | Post by Olivier LOVERDE (Co-founder & CPTO @Innovorder) summarizing the study |
| **LinkedIn URL** | https://www.linkedin.com/posts/loverdeolivier_investigating-the-downstream-effects-of-ai-ugcPost-7426914640300802048 |

---

## Summary

Two-phase controlled experiment investigating whether AI-assisted code creation impacts maintainability for downstream developers:

- **Phase 1**: 151 participants add features to a Java web app (with or without AI: GitHub Copilot / Cursor)
- **Phase 2**: A *different* group of developers evolves those solutions **without AI** (blind review — reviewers don't know if code was AI-assisted)

**Key findings:**
1. AI users completed tasks **30.7% faster** (median) than non-AI users
2. Habitual AI users showed an estimated **55.9% speedup**
3. **No significant differences** in downstream evolution time or code quality — the "AI code is unmaintainable" myth is not supported empirically
4. Researchers recommend future investigation into excessive code generation and cognitive debt risks
5. Dave Farley's explicit takeaway: developers must guide AI (not autopilot), think about the business problem, and decompose complexity

---

## Evaluation Score: **4/5** (Très pertinent — amélioration significative)

### Scoring Breakdown

| Criterion | Score | Justification |
|-----------|-------|---------------|
| **Content novelty** | 4/5 | Directly addresses the #1 FUD against AI-assisted coding ("unmaintainable code") with empirical data |
| **Research rigor** | 4/5 | 151 participants, 95% professional developers, 2-phase blind design — solid for this domain. Caveat: arXiv preprint, not yet peer-reviewed in proceedings |
| **Guide specificity** | 4/5 | Complements METR 2025 (already in guide) — provides the counter-evidence the guide currently lacks |
| **Credibility** | 5/5 | Dave Farley authorship = exceptional signal for the software engineering community |
| **Actionability** | 3/5 | Results are confirmatory, not prescriptive — validates approach but doesn't change workflow |

**Overall: 4/5**

---

## Gap Analysis

### What the guide already covers

| Topic | Coverage | Location |
|-------|----------|----------|
| AI productivity gains | ✅ General stats (Copilot, McKinsey) | `learning-with-ai.md:921-924` |
| METR RCT (19% slower) | ✅ Present | `learning-with-ai.md:925` |
| Vibe coding risks | ✅ Full section | Multiple locations |
| Skill atrophy concern | ✅ Present | `learning-with-ai.md:925` |
| AI code maintainability myth | ❌ **ABSENT** | **Gap identified** |
| Productivity curve (habitual users) | ⚠️ Partially | `learning-with-ai.md:~100` |

### What this study adds

| Contribution | Value |
|--------------|-------|
| Empirical refutation of "AI code is unmaintainable" | **High** — directly debunks the most common objection |
| 55.9% speedup for habitual users | **High** — validates learning curve section |
| Blind review methodology | **Medium** — demonstrates scientific rigor of the finding |
| Balance to METR 2025 results | **High** — METR = complex codebases, AI slower; this study = mixed tasks, AI faster → complete picture |

---

## Recommendations

**Where to integrate**: `guide/learning-with-ai.md` — section "Productivity Research" (~line 925)

**What to add** (1-2 lines):
```markdown
- **Borg et al. "Echoes of AI" RCT (2025)** — [arXiv:2507.00788](https://arxiv.org/abs/2507.00788) — Controlled experiment (151 participants, 95% professional developers, 2-phase blind design): AI users 30.7% faster (median), habitual users ~55.9% faster. **Key finding**: no significant maintainability impact for downstream developers. Directly refutes the "AI code is unmaintainable" myth. Caveat: arXiv preprint (July 2025), not yet peer-reviewed in conference proceedings.
```

**Priority**: Medium-High — completes the empirical picture alongside METR 2025.

---

## Challenge Summary (technical-writer agent)

**Initial score:** 4/5
**Challenged score:** 3.5 → 4/5 confirmed with corrections

**Key points from challenge:**

1. **Score justified** — but "peer-reviewed" was overstated. Corrected to "arXiv preprint."
2. **Blind review design** (phase 2 reviewers don't know if code is AI-assisted) = most important methodological detail, absent from initial eval. Added.
3. **55.9% habitual users** more actionable than 30.7% median — validates learning curve section.
4. **Limitations not flagged by the post**: tâches bornées en labo ≠ 12-month production codebase drift; potential selection bias (volunteer participants likely pro-AI); knowledge debt not measured.
5. **Risk of non-integration**: Guide would retain pro-METR bias (AI slower on complex tasks) without empirical counter-balance on maintainability.

---

## Fact-Check

### LinkedIn Post Claims

| Claim (Olivier LOVERDE's post) | Verified | Source | Notes |
|--------------------------------|----------|--------|-------|
| Dave Farley = co-auteur de Continuous Delivery | ✅ | Perplexity, continuous-delivery.co.uk | Co-author with **Jez Humble** (not alone — minor omission in post) |
| 151 développeurs | ✅ | arXiv abstract | Exact |
| 95% professionnels | ✅ | arXiv abstract | Not mentioned in post but verified |
| Un groupe crée, un autre reprend (sans IA) | ✅ | arXiv methodology | 2-phase blind design confirmed |
| Code IA = aucun problème de maintenance | ✅ | arXiv abstract | "No systematic maintainability advantages or disadvantages" |
| 30% de temps gagné | ✅ | arXiv: 30.7% median | Rounded, correct |
| 50% pour ceux qui maîtrisent | ⚠️ | arXiv: 55.9% | Slight underestimate — actual is 55.9% |
| Devs n'ont pas débranché leur cerveau (qualifier) | ✅ | Study design | Phase 1 participants guided AI, did not use autopilot |

### arXiv Paper Claims

| Claim | Verified | Source |
|-------|----------|--------|
| 30.7% median reduction in completion time | ✅ | WebFetch arXiv abstract |
| 55.9% speedup for habitual users | ✅ | WebFetch arXiv abstract |
| No significant differences in Phase 2 | ✅ | WebFetch arXiv findings |
| 151 participants | ✅ | WebFetch arXiv abstract |
| 95% professional developers | ✅ | WebFetch arXiv abstract |

**Corrections applied:**
- "50%" → actual figure is **55.9%** (LinkedIn slight understatement)
- "peer-reviewed" → **arXiv preprint** (July 2025, not yet peer-reviewed in proceedings)

**Confidence**: High — primary source directly fetched and cross-validated.

---

## Decision finale

- **Score final**: 4/5
- **Action**: Intégrer (1-2 lignes dans section Productivity Research)
- **Confiance**: Haute (primary source verified, methodology solid, gap confirmed)
- **Nuance à conserver**: Limitations du design labo (tâches bornées, biais de sélection, knowledge debt non mesuré)

---

## Integration Log

**Date integrated**: 2026-02-19
**Post-audit corrections applied**: 2026-02-19 (technical-writer audit + Perplexity v2 check)

| File | Change | Line |
|------|--------|------|
| `guide/learning-with-ai.md` | Citation réécriture — retrait claims éditoriaux, "July 2025" → "v2 Dec 2025", restructuration factuelle | ~926 |
| `guide/ultimate-guide.md` | Ajout blockquote nuance downstream maintainability dans section 1.7 Trust Calibration | ~1092 |
| `guide/learning-with-ai.md` | Ajout note "On maintainability fear" dans "Why Teams Get Results" | ~151 |
| `machine-readable/reference.yaml` | Ajout 4 entrées: productivity_rct_metr, productivity_rct_echoes, productivity_maintainability_empirical, trust_calibration_maintainability_nuance | ~94 |

**Corrections post-audit:**
- "peer-reviewed" → "arXiv preprint (v2 Dec 2025), not yet published in peer-reviewed proceedings" — Perplexity confirmé
- Retrait formulation éditoriale "directly refutes the myth" → description factuelle neutre
- Ajout "First RCT to explicitly target maintainability of AI-assisted code" (Perplexity: arXiv v2 HTML confirmed wording)
- Séparation bibliographie / analyse : la comparaison METR déplacée dans le corps du guide, pas dans la biblio
