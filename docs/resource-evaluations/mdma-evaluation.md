# Resource Evaluation: MDMA (MobileReality)

**URL (trigger)**: https://github.com/MobileReality/mdma
**Primary Sources**: [MDMA source repository](https://github.com/MobileReality/mdma), including its README, documentation, evaluations, and implementation
**Type**: Open-source library / DSL for agent-generated interactive UI
**Evaluated**: 2026-07-07
**Score**: 3/5 (MODERATE, integrate when time available)

---

## Executive Summary

MDMA is an open-source project that defines a Markdown-with-embedded-YAML dialect for interactive UI (forms, buttons, tables, approval gates), designed to be produced reliably by small or fine-tuned LLMs and validated deterministically before rendering. Three independent audit agents examined the source tree and reached a consistent picture: the core engineering (parser, validator, fixer pipeline, eval methodology) is genuinely solid, but several marketing claims don't survive contact with the code, and there's a real functional bug in the shipped form component.

**Why 3/5**: The validator/fixer architecture and the honest eval framing are worth documenting as a reference pattern for anyone building a similar small-model-output-reliability pipeline. But the gap between claimed and actual behavior (a form component whose "required" fields aren't enforced, "runs anywhere" that doesn't apply to rendering, non-cryptographic hashes marketed alongside "audit-log"/"pii" keywords) means this isn't a "go build on this in production" recommendation without independently fixing the validation gap first.

---

## Content Analysis

### Key Facts (Verified)

1. **Deterministic validator/fixer pipeline**: single pass, no additional LLM call, regex-based extraction tolerant of malformed markdown, 22 rule files under `packages/validator/src/rules` (19 documented in the README, 22 counted in the source at audit time), ordered fixers for field-type inference, YAML key typo correction, and binding repair.
2. **Standard parsing**: built on remark/unified as a proper plugin, with explicit handling of streaming state (distinguishes a block still generating from one that's genuinely malformed).
3. **Eval methodology**: uses promptfoo with custom assertions, documented with a "not 100%, observations not conclusions" framing in `evals/own-model/README.md`. Measured result: 41% success with a bare prompt versus 90.5% with the DSL and validator combined, on their own fine-tuned model served via Modal/Hugging Face.
4. **"Runs anywhere" for core packages**: `spec`, `parser`, `validator`, and `runtime` packages contain zero Node-specific imports (`fs`, `path`, `crypto`), confirmed by grep across all four package source trees.
5. **CI hygiene**: GitHub Actions pinned by commit SHA in `.github/workflows/ci.yml` and `release.yml` (e.g. `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6`), changesets-based per-package versioning, a `turbo run test` test suite spanning all packages.
6. **Package structure**: 10 packages (`spec`, `parser`, `validator`, `runtime`, `attachables-core`, `renderer-react`, `cli`, `mcp`, `agui`, `prompt-pack`), each independently versioned and published under the `@mobile-reality` npm org.

### Fact-Check: Claims vs. Code

| Claim | Status | Evidence |
|-------|--------|----------|
| "Guarantees valid UI" | ❌ Overstated | 90.5% measured, not 100% (`evals/own-model/README.md`) |
| Own eval results file shows 100% | ⚠️ Internal contradiction | `evals/own-model/results.json`: 95/95 pass (100%) dated 2026-06-30, unreconciled with the README's 90.5% figure for the same eval track |
| "Runs anywhere" | ⚠️ Partially true | True for `spec`/`parser`/`validator`/`runtime` (zero Node imports, verified). False for rendering: exactly one renderer exists, `@mobile-reality/mdma-renderer-react`, 100% React |
| Chart component renders charts | ❌ Misleading | `ChartRenderer.tsx` parses CSV and renders an HTML `<table>`; code comment admits "Renders chart data as a simple HTML table" (`packages/renderer-react/src/components/ChartRenderer.tsx`) |
| Webhook component executes webhooks | ❌ Misleading | `WebhookRenderer.tsx` dispatches a UI event (`INTEGRATION_CALLED`) the host app must wire up; no HTTP call happens inside MDMA (`packages/renderer-react/src/components/WebhookRenderer.tsx`, line 29). To the project's credit, this gap is listed in their own roadmap as not-yet-built |
| "On-device / mobile models" | ⚠️ Misleading framing | Refers to the size of the generator LLM (hosted on Modal, distributed via Hugging Face), unrelated to rendering. The renderer CSS has zero `@media` queries, confirmed across all `.css` files in `packages/renderer-react` |
| "Accessible by design" (demo page) | ❌ Unsupported | Native labels/buttons and one `role="alert"` exist (`CalloutRenderer.tsx`), but no `aria-invalid`/`aria-live` anywhere, and the PII-masking table cell is a clickable `<span>` with no `role="button"`/`tabIndex` (`packages/renderer-react/src/components/TableRenderer.tsx`, lines 4-15) |
| Form validation (required/pattern/min/max) is enforced | ❌ False, functional bug | See dedicated section below |
| Audit-log integrity is tamper-evident | ❌ Not cryptographically | FNV-1a hash, code comment says "non-cryptographic" (`packages/runtime/src/core/event-log-integrity.ts`, line 10) |
| PII redaction hash is secure | ❌ Not cryptographically | djb2-style rolling hash, comment says "non-cryptographic, for logging only" (`packages/runtime/src/redaction/hash.ts`) |

---

## The Form Validation Bug (Independently Found by Two Audit Agents)

This is the most consequential finding, because it contradicts the project's own documentation rather than a marketing tagline.

- `FormRenderer.tsx` wraps every field in a plain `<div className="mdma-form">`, not a `<form>` element (`packages/renderer-react/src/components/FormRenderer.tsx`, line 152).
- The submit control is `<button type="button">` with an `onClick` that dispatches an `ACTION_TRIGGERED` action directly, bypassing any form submit event (same file, lines 119-125 and 247-258).
- Native HTML5 constraint validation (the `required` attribute passed down to each input) only fires on an actual form submission event. Since there is no `<form>` and no `type="submit"` button, it never fires.
- The field-level `validation` object (`pattern`, `min`, `max`, `message`) is defined in the schema at `packages/spec/src/schemas/components/form.ts` (line 18) and is read nowhere in the renderer or the attachables-core form handler (`packages/attachables-core/src/form/form-handler.ts`).
- `docs/reference/component-catalog.md` documents this exact `validation` object with a worked example (a `pattern` matching a company email domain, lines 71-72), and the same construct appears in the repo's own `examples/approval-workflow/document.md`.

**Net effect**: a field marked `required: true` with a `pattern` constraint can be submitted empty or non-conforming, with no error shown to the user, despite the documentation presenting this as working behavior with concrete examples pulled from the repo itself. This is different in kind from the webhook gap, which is honestly listed as future work in the project's own roadmap. The validation gap is not disclosed anywhere.

---

## Gap Analysis (vs. Our Guide)

| Aspect | Our Guide (before this integration) | Gap? |
|--------|---------------------------------------|------|
| Generative UI as a category (agent-produced interactive output) | Not covered | **Yes** |
| MCP Apps (SEP-1865) | Covered (`architecture.md`, `ultimate-guide.md`) | No |
| A2UI, Vercel AI SDK generative UI patterns | Not covered | **Yes** |
| MDMA specifically | Not covered | **Yes** |
| Small-model-reliability validator/fixer pattern (reusable idea for prompt engineering) | Not covered explicitly | **Minor gap** |

---

## Integration Recommendation

### Where

**Section 7.1** in `guide/ecosystem/ai-ecosystem.md`, immediately after Section 7 (UI Prototypers) and before Section 8 (Workflow Orchestration).

### What Was Included

1. Why the generative-UI category exists (agent needs interactive output inside a single chat turn, not a separate artifact)
2. Comparison table: A2UI vs. MCP Apps vs. Vercel AI SDK generative UI vs. MDMA
3. MDMA case study: what holds up, what's overstated, the form validation bug, the hash security note
4. An honest note that the category is young (2025-2026), no standard has won, and distribution (who has a vendor behind them) matters as much as technical merit

### What Was NOT Included

- No tutorial or "how to adopt MDMA" walkthrough. This guide documents Claude Code, not a recommendation to build on a specific third-party DSL.
- No deep dive into the MDMA-AG-UI integration plan (`mdma-agui-integration-plan.md`), too speculative and pre-implementation to cite as fact.
- No comparison against MCP-UI (a separate, related but distinct project referenced by MCP Apps co-authors), out of scope for this evaluation.

### Priority

**Moderate**. Not urgent (no reader is blocked without this), but a real content gap: the guide covers MCP Apps in depth but had nothing comparing it against A2UI, the Vercel AI SDK pattern, or MDMA, and nothing on this specific reliability pattern for small-model UI generation.

---

## Challenge (Technical-Writer)

- **Score justified**: 3/5 is correct, not 4/5, because the actionable takeaway for a Claude Code user is limited (MDMA is a third-party library for a specific rendering stack, React-only, not something most readers will adopt directly). Not 2/5, because the validator/fixer architecture and the honest small-model eval methodology are a genuinely useful reference pattern, and the wider generative-UI comparison itself (A2UI vs. MCP Apps vs. Vercel AI SDK vs. MDMA) was a real gap worth covering regardless of MDMA's own flaws.
- **Risk of over-crediting**: the initial pass from the audit agents leaned toward praising the validator engineering without weighing the form-validation bug heavily enough. That bug is corrected to first billing in the Case Study text precisely because it contradicts documented behavior, which is a more serious category of problem than an aspirational marketing line.
- **Score adjusted**: 3/5 (unchanged after challenge).

---

## Decision

| Criterion | Value |
|-----------|-------|
| **Final score** | 3/5 |
| **Action** | Integrated as Section 7.1 in `guide/ecosystem/ai-ecosystem.md` |
| **Confidence** | High (all claims independently verified against the local source tree, not just the README) |
| **Priority** | Moderate |
| **Files modified** | `guide/ecosystem/ai-ecosystem.md` (new Section 7.1 + TOC entry), `docs/resource-evaluations/mdma-evaluation.md` (this file), `machine-readable/reference.yaml` (new `deep_dive` entries) |

---

## Resources

- **Repository**: https://github.com/MobileReality/mdma
- **Eval README**: [Evaluation methodology](https://github.com/MobileReality/mdma/blob/main/evals/own-model/README.md)
- **Component catalog (documents the unenforced validation)**: [Component reference](https://github.com/MobileReality/mdma/blob/main/docs/reference/component-catalog.md)
