# Resource Evaluation: claude-security-audit (VicKayro)

**Date**: 2026-03-16
**Evaluator**: Claude Sonnet 4.6
**Resource URL**: https://github.com/VicKayro/claude-security-audit
**Resource Type**: Open-source Claude Code command (GitHub)
**Author**: VicKayro
**Published**: 2026-02-26
**Stars**: 60 | **Forks**: 6 | **License**: MIT (README-declared, no SPDX file)

---

## Executive Summary

A single-file `/security-audit` slash command for Claude Code that runs a 16-section OWASP-mapped web app audit with scoring /10. The repo is 18 days old. The guide already has full OWASP coverage via `security-audit.md`, `security-check.md`, `security-auditor.md` agent, and the 41KB `security-hardening.md`. Two patterns in this resource are genuinely better than what we have: an environment context step (dev/staging/prod) before auditing, and an anti-false-positive factual check before reporting secrets (runs real git history before raising a finding). One area is a genuine gap: paywall/billing logic audit. Everything else overlaps.

---

## Content Summary

- **16 audit sections** with OWASP Top 10 (2021) + CWE IDs: HTTP headers, auth, CSRF, open redirect, injection (SQL/XSS/command), IDOR/access control, secrets and crypto, paywall/billing, vulnerable deps (npm audit + pip-audit), CORS, files/config, WebSocket, SSRF, logging/monitoring, data integrity, software integrity
- **Context-aware pre-step**: asks dev/staging/prod before starting — avoids false positives on debug flags, CORS `*`, and HTTP-only configs that are normal in local dev
- **Factual verification requirement**: before reporting any secret, runs `git log --all -p -- '*.env'` and checks `.gitignore` — no finding without concrete proof
- **Scoring /10** with a structured severity table (CRITIQUE → HAUTE → MOYENNE → BASSE), file:line, and recommended fix with code
- **Disclaimer**: report includes an explicit reminder that it needs human review before any action
- **258 lines**, French-language prompts, MIT

---

## Gap Analysis vs. Guide

| Section | VicKayro's Command | Our Coverage |
|---------|-------------------|--------------|
| OWASP Top 10 structure | ✅ Full mapping + CWE | ✅ `security-auditor.md` agent, `security-hardening.md` |
| HTTP headers | ✅ 7 headers with CWE | ⚠️ Mentioned in hardening guide, not in audit command |
| Auth / JWT | ✅ 10 checks | ✅ `security-audit.md` Phase 2+3 |
| Secrets / git history | ✅ Factual check pattern | ✅ `security-audit.md` Phase 2 (pattern similar but less strict) |
| Dep scan (npm/pip) | ✅ | ✅ `security-audit.md` Phase 4 |
| CSRF / open redirect | ✅ | ⚠️ Not explicit in our commands |
| IDOR / access control | ✅ | ⚠️ Not explicit in our commands |
| CORS | ✅ | ⚠️ Not explicit in our commands |
| **Paywall / billing** | ✅ Full section | ❌ **Not covered anywhere in the guide** |
| WebSocket | ✅ | ❌ Not covered |
| SSRF | ✅ | ⚠️ Mentioned in hardening guide, not in audit command |
| Dev/staging/prod context step | ✅ Explicit pre-step | ❌ Not in our command |
| Anti-FP factual verification | ✅ Explicit requirement | ⚠️ Partial — our command checks `.gitignore` but doesn't mandate git log proof |
| Claude Code-specific (hooks, prompt injection, MCP) | ❌ Not covered | ✅ Our unique angle |
| Score /100 posture model | ❌ Score /10 only | ✅ `security-audit.md` Phase 6 |

**Real gaps**: paywall/billing audit, the strict anti-false-positive pattern, the environment context pre-step.

---

## Score

**Score: 2/5** (Marginal)

The overlap with existing guide content is substantial. Most of the 16 sections are already covered through the combination of `security-audit.md`, `security-auditor.md`, and `security-hardening.md`. The command is 18 days old with 60 stars — insufficient track record for security tooling, where false confidence is worse than no tool. The LinkedIn post framing ("vibe coding security") is accurate marketing but doesn't change the technical substance.

The two extractable patterns (environment context step + factual git-history check before secrets findings) and the paywall/billing gap are worth acting on, but they can be addressed by enhancing our existing command without citing this repo.

---

## Challenge (technical-writer agent)

> "The score is wrong. It should be 2/5, not 3/5. The evaluator confused 'interesting' with 'valuable.'"
>
> "The repo is 18 days old with 60 stars. That is not a signal of validation, it is a signal of recency bias. Security tooling needs a longer track record."
>
> "The integration recommendation is backwards. 'Mention in security-hardening.md as community resource' means we are directing readers to a 60-star, 18-day-old single-file command. If the patterns are worth having, extract them. If not, don't mention the repo."
>
> "The paywall/billing section is the one genuinely novel angle. None of our existing commands audit billing logic or access control around paywalled features. The evaluation mentions it in the feature list and then says nothing about it."

Challenge accepted. Score adjusted to 2/5. Integration plan revised accordingly.

---

## Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| MIT license | ⚠️ Partial | README says MIT, no SPDX file or LICENSE in repo |
| 16 audit sections | ✅ | Read from command file directly (gh api) |
| OWASP Top 10 (2021) mapping | ✅ | Command file contains OWASP reference table with A01-A10 |
| npm audit + pip-audit | ✅ | Section 9 of the command file |
| Score /10 | ✅ | Command file output format |
| 60 stars, created 2026-02-26 | ✅ | GitHub API |
| VicKayro author profile | ⚠️ | GitHub API returns 404 for user profile — minimal public presence |

No invented stats. The LinkedIn post claims "16 sections" and "OWASP Top 10 (2021) mappé" — both accurate.

---

## Decision

**Score: 2/5 — Ne pas intégrer comme ressource externe**

**Action: Extract two patterns silently into existing commands**

1. Add an environment context pre-step to `examples/commands/security-audit.md` (ask dev/staging/prod before Phase 1)
2. Strengthen the anti-false-positive requirement in Phase 2 (mandate `git log --all -p` before reporting secrets)
3. Add a Paywall/Billing audit section to `examples/agents/security-auditor.md`
4. Revisit the repo in 3 months if it reaches 200+ stars with active issues/PRs

**No guide mention.** The resource does not meet the threshold for a community reference link given its age, minimal author profile, and the absence of a formal LICENSE file. The guide already has security coverage that is broader in several dimensions (Claude Code-specific threats, hook security, prompt injection). Extracting the useful patterns internally is cleaner than sending readers to an immature repo.

**Confidence**: High — full command file reviewed, all claims verified against source.
