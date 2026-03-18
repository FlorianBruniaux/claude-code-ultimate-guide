# Resource Evaluation: Mathieu Eveillard — "Génération LLM : sale temps pour les juniors"

**Date**: 2026-03-04
**Source**: LinkedIn post + https://www.mathieueveillard.com/blog/generation-llm
**Type**: Opinion editorial (blog/LinkedIn)
**Author**: Mathieu Eveillard — Software quality expert, France
**Score**: 2/5

---

## Summary

Opinion piece arguing junior developers are not building foundational skills because they over-delegate to LLMs. Core thesis: you can't outsource the cognitive effort of learning. Responsibility for structured mentoring falls on experienced developers and organizations. "It works" is not sufficient — developers must understand architecture, modularization, and testing to use AI responsibly.

Key claims:
- Juniors use LLMs without the prerequisite knowledge to evaluate output quality
- LLMs are neutral tools; the problem is the absence of method and architectural knowledge
- Experienced developers and organizations must structure "compagnonnage" (apprenticeship) to transmit fundamentals
- Architecture decisions (hexagonal, modularization) have no visible user impact but change everything about maintainability

---

## Score Justification

**2/5 — Does not integrate directly. Reveals a gap worth filling.**

The article provides a narrative, opinion-based version of a diagnostic that the guide already covers with more rigor and data (Shen & Tamkin 2026, METR RCT, DORA). It validates our existing work but adds no research or actionable frameworks.

What it *does* reveal: the guide had no section for tech leads or engineering managers responsible for structuring team-level learning. The article points at that gap without filling it.

---

## Gap Identified → Action Taken

**Gap**: `guide/learning-with-ai.md` was entirely written for individual developers. No content for the person responsible for onboarding policy, mentoring structure, or team-level AI governance.

**Action**: Added new section "For Tech Leads & Engineering Managers" (§12) to `guide/learning-with-ai.md`, covering:
- Structured onboarding (4-week model, not "here's your license")
- Metrics for real growth vs. velocity
- Three scalable mentoring models (pair rotations, architecture hot seat, collective CLAUDE.md ownership)
- Team-level CLAUDE.md policy template
- Warning signs at team level with specific responses
- Quick checklist

Research validated with Perplexity:
- Create Future (2025): structured AI training raises junior savings from 14-42% to 35-65%
- Stanford Digital Economy Study (2025): 22-25 age group employment down ~20% by July 2025
- LeadDev (2025): tech CEO perspectives on structured junior development in AI teams

---

## What the Article Does NOT Cover

- Scalability of compagnonnage past teams of 5-10
- Empirical support for the labor market claims ("sale temps")
- Any actionable framework (it's diagnostic, not prescriptive)
- Team-level tooling or policy structures

---

## Fact-Check

| Claim | Status |
|-------|--------|
| LLMs at 20-40€/month | Plausible (Claude/GPT pricing 2026) |
| "Loi de l'Instrument" reference | Correct (Maslow's Law of the Instrument) |
| Article URL functional | SSL error during evaluation — content obtained via LinkedIn post |
| Stats on junior skill degradation | Opinion-based, no study cited |

---

## Decision

**Do not cite this article as a primary source.** It could be mentioned as a practitioner voice in a section on organizational responsibility, but its anecdotal nature makes it weak compared to existing sources (Shen & Tamkin, METR, Borg et al.) already in the guide.

The real output of this evaluation was identifying and filling the team lead gap — not integrating the article itself.
