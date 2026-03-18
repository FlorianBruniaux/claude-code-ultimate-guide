# Resource Evaluation: Boris Paillard — "Son site custom en 2h avec Claude Code"

**Date**: 2026-03-05
**Source**: [LinkedIn Pulse](https://www.linkedin.com/pulse/son-site-custom-en-2h-avec-claude-code-m%C3%A9thodes-et-prompts-paillard-7q8je/)
**Type**: Tutorial / Workflow walkthrough
**Author**: Boris Paillard — ex-Le Wagon instructor, co-founder mixt.care
**Score**: 3/5

---

## Summary

Workflow for building a custom website in ~2h using Claude Code, centered on a "design-first" approach. Core thesis: Claude Code executes your design taste — it doesn't replace it. You must define a design system before prompting, or every generated page drifts.

Four-step method with concrete prompts published in the article:
1. **brand-book.html** — color palette with semantic roles, fonts, CSS variables
2. **ui-kit.html** — base components documented with Tailwind CSS
3. **Full site development** — scroll animations, sticky images, statement footers
4. **Conditional forms** (bonus) — JSON-driven multi-step forms with Google Apps Script

Concrete project: mixt.care (personalized dermatology). Stack: Tailwind CSS + vanilla JS (Intersection Observer).

---

## Score Justification

**3/5 — Relevant, integrate as field example.**

The four-step methodology is structurally sound and the 4 prompts are specific and usable. The core insight (HTML reference files as persistent Claude Code context) is not documented in the guide and is genuinely reusable.

However: no WCAG/accessibility coverage, no differentiation from Cursor/Copilot, no GitHub repo to verify results, and no discussion of maintainability past the MVP. The guide's technical sections need more rigorous sources.

---

## Gap Identified → Action Taken

**Gap**: The guide had no documentation of the "Design Reference File" pattern — keeping `brand-book.html` and `ui-kit.html` at the project root as permanent context files for Claude Code. This pattern ensures design coherence across all generated pages without re-prompting.

**Action**: Added `examples/claude-md/design-reference-file.md` — a standalone template for the pattern, with:
- Recommended project structure
- CLAUDE.md snippet to activate automatic design system reference
- Prompt for brand-book.html with WCAG audit embedded
- Prompt for ui-kit.html documentation
- Color audit prompt (WCAG 2.1 compliance, color blindness simulation, fix suggestions)

No changes to `ultimate-guide.md` — the pattern is documented as an example, not promoted to a guide section. Score does not justify central placement.

---

## What the Article Does NOT Cover

- WCAG accessibility / contrast ratios for the generated palette
- Maintainability after the 2h MVP (technical debt, component evolution)
- Why Claude Code specifically vs. Cursor or Copilot
- No GitHub repo or live code to verify the claimed output

---

## Fact-Check

| Claim | Status |
|-------|--------|
| Author: Boris Paillard | Confirmed — LinkedIn byline |
| Date: March 5, 2026 | Confirmed — `datePublished: 2026-03-05T08:14:35Z` |
| Project: mixt.care (dermatology) | Confirmed — mentioned explicitly |
| 2h timeframe | Confirmed — title + body |
| Font sizes: 6rem desktop / 3rem mobile | Confirmed — in footer prompt |
| Animations: 0.6s + 100ms stagger | Confirmed — in Intersection Observer prompt |
| 4 prompts published in article | Confirmed — verified on second fetch |
| "Co-founder Le Wagon" | Correction — article says "launched a workshop 10 years ago", not co-founder |

---

## Decision

**Integrate as field example.** The "Design Reference File" pattern (brand-book.html + ui-kit.html as permanent project context) is the one novel, reusable insight. Extract as a standalone example template. Do not cite as a primary technical source.
