# Resource Evaluation #081: Rippletide Code: Runtime Rule Enforcement for Claude Code

**Source:** LinkedIn post (Patrick Joubert, CEO Rippletide) + [rippletide.com/dev](https://www.rippletide.com/dev)
**Type:** Commercial tool — hook-native rule enforcement layer for Claude Code
**Evaluated:** 2026-03-17
**Note:** Distinct from eval 072 (2026-02-28) which covered Rippletide's MCP/eval/decision runtime SaaS. This is a different product: a CLI enforcement tool (`npx rippletide-code`), hook-native, no MCP overhead.

---

## 📄 Content Summary

1. **Problem addressed**: CLAUDE.md rules degrade at scale — after ~40 rules, Claude Code follows them inconsistently; context compaction causes rule loss between sessions. Per Rippletide: "50% of Claude Code CLAUDE.md issues are about rules being ignored" (18+ public GitHub reports cited).

2. **Core mechanism**: Reads codebase and existing CLAUDE.md → builds a "Context Graph" stored outside the LLM context window → uses Claude Code hooks to intercept tool calls pre-execution → blocks violations before they run.

3. **Architecture**: Hook-native (not MCP), avoiding token injection overhead. Pre-execution blocking (not post-execution logging). Example output: `[BLOCKED] Rule: "DO NOT modify .env files"`.

4. **Installation**: `npx rippletide-code` — free beta, no API key, no sign-up required. Graph builds in "less than 5 seconds" (company claim).

5. **Background**: Founded February 2024, SF + Paris, team of 8. Won OpenAI Codex Hackathon. Co-founders: Patrick Joubert (CEO) + Yann Bilien (Chief Scientist). Enterprise tier available (custom pricing, "2-week validation sprint").

---

## 🎯 Relevance Score

| Score | Meaning |
|-------|---------|
| 5 | Essential — Major gap in the guide |
| 4 | Very relevant — Significant improvement |
| **3** | **Pertinent — Useful complement** |
| 2 | Marginal — Secondary info |
| 1 | Out of scope |

**Score: 3/5**

**Justification**: Addresses a real, documented community pain point (CLAUDE.md rule degradation at scale, compaction-driven rule loss) that the guide acknowledges but does not cover with solutions. The hook-based enforcement pattern is genuinely novel in the Claude Code ecosystem — no other documented tool does pre-execution blocking. However, multiple claims are unverified (Context Graph compaction-resistance, "less than 5 seconds" graph build, "50% of issues"), the product is in free beta with no adoption signals, and the company has a prior pattern of publishing unverifiable performance claims (eval 072: "<1% hallucinations" without methodology).

Score does not exceed 3 because: the guide's credibility requires holding commercial tools to evidence standards, and this tool fails that bar without independent corroboration.

---

## ⚖️ Comparative

| Aspect | This resource | Our guide |
|--------|--------------|-----------|
| CLAUDE.md rule degradation at scale | ✅ Documented as core problem | ⚠️ Mentioned briefly (context compaction section), no dedicated coverage |
| Hook-based pre-execution blocking | ✅ Core feature | ✅ Hooks documented, but no enforcement pattern described |
| Rule enforcement tools | ✅ Full solution | ❌ No tool covers this (Known Gaps table has no "rule enforcement" entry) |
| Context compaction rule loss | ✅ Problem + solution claimed | ⚠️ Problem mentioned, no mitigation strategy |
| Security surface of enforcement layer | ❌ Not addressed | ✅ Security section covers hook security |
| Verifiable performance claims | ❌ Marketing without methodology | ✅ Stats with sources only |

---

## 📍 Recommendations

**Score 3 — integrate as limited entry with explicit caveats.**

### What to integrate (and how)

**Priority 1 — Document the pattern, not just the tool.**

The guide should cover "runtime rule enforcement via hooks" as a concept in the CLAUDE.md limitations section of ultimate-guide.md. This section currently documents compaction behavior and path-scoped CLAUDE.md files as mitigations, but has no entry for pre-execution enforcement. This gap exists regardless of Rippletide. The pattern: use `PreToolUse` hooks to validate tool calls against a rule set and exit non-zero to block. Rippletide is then one commercial implementation of this pattern.

Do NOT create a section in the guide that only exists to justify one beta product.

**Priority 2 — Add "Rule enforcement" gap to third-party-tools.md Known Gaps table.**

The Known Gaps table has no entry for runtime rule enforcement. This should be added first. Then Rippletide can be cited under a new "Rule Enforcement" section as the only known implementation, with clear watch caveats (beta, unverified claims, no adoption signals).

**Where to integrate:**
- `guide/ultimate-guide.md` CLAUDE.md limitations section: add 3-4 lines on the enforcement pattern + Rippletide reference
- `guide/ecosystem/third-party-tools.md`: add "Rule Enforcement" section (after Hook Utilities or after Engineering Standards Distribution) + update Known Gaps table

**What NOT to integrate:**
- Do not cite "50% of issues are about rule ignoring" as a fact — it is Rippletide's own framing
- Do not cite "Context Graph persists across compaction" as confirmed — it is unverified
- Do not use "less than 5 seconds" build time as a guide stat
- Do not create a section solely for this tool without the Known Gaps entry first

---

## 🔥 Challenge (technical-writer)

**Score after challenge: 3/5 (held)**

Key points raised by challenge:

1. **Unverified claims embedded as facts**: The evaluation initially treated "Context Graph compaction-resistance" as a verified feature. It is Rippletide's own claim. The guide must not repeat it without qualification — same error that kept eval 072 at 2/5.

2. **Security surface not addressed**: A pre-execution hook in the critical path of every tool call has a real attack surface. Fail-open vs fail-closed behavior when the Context Graph service is unavailable is unspecified. Whether `npx rippletide-code` runs a persistent background process with access to tool inputs (which may contain secrets) is undocumented.

3. **"Free beta" is a risk flag**: No pricing page, no post-beta plan, no stated data handling policy for convention scanning. The guide documents Straude with data transmission caveats — Rippletide deserves identical scrutiny.

4. **"Auto-detects implicit conventions" is unexamined**: How? Does it send code to an external service? Local only? This is a security and privacy question before it is a feature.

5. **Integration sequence matters**: Do not add a "Rule Enforcement" section to third-party-tools.md without first adding "Rule enforcement" to the Known Gaps table. Category before tool, not tool creating category.

6. **The stronger integration point is the PATTERN**: The guide should document hook-based pre-execution enforcement as a concept. Rippletide is one implementation. A minimal DIY example (PreToolUse hook that checks a rule list and exits non-zero) would serve readers better than a commercial product endorsement.

**Risks of NOT integrating**: Low-medium. The rule degradation problem is real and under-documented in the guide. Not covering it leaves a gap that practitioners regularly encounter. But the pattern can be documented without Rippletide — the risk is solved by covering the concept, not the product.

---

## ✅ Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| `npx rippletide-code` installation command | ✅ | rippletide.com/dev — confirmed |
| Free beta, no API key required | ✅ | rippletide.com/dev — confirmed |
| Hook-native architecture (not MCP) | ✅ | rippletide.com/dev — confirmed |
| Co-founders: Patrick Joubert + Yann Bilien | ✅ | rippletide.com/dev — confirmed |
| Founded February 2024, SF + Paris, team of 8 | ✅ | rippletide.com/dev — confirmed |
| Won OpenAI Codex Hackathon | ✅ | rippletide.com/dev — confirmed |
| "50% of CLAUDE.md issues are about rules being ignored" | ⚠️ | Rippletide's own framing, no external source |
| "18+ public GitHub reports of non-compliance" | ⚠️ | Not linked, not verifiable from evaluation |
| Context Graph persists across compaction | ⚠️ | Rippletide claim only — no external confirmation |
| Graph builds in "less than 5 seconds" | ⚠️ | Rippletide claim — no benchmark published |
| Pre-execution blocking (not post-execution logging) | ✅ | Confirmed by hook architecture description |
| Coming soon: Cursor, Windsurf, Cline | ✅ | rippletide.com/dev — confirmed |
| Perplexity search returns no external coverage | ✅ | No independent coverage found as of 2026-03-17 |

**Corrections applied**: Claims marked ⚠️ removed from factual statements. "Context Graph compaction-resistance" and the "50%" stat are presented as Rippletide claims, not guide facts.

---

## 🎯 Final Decision

- **Score**: 3/5
- **Action**: Integrate with caveats — pattern documentation in ultimate-guide.md + limited entry in third-party-tools.md + Known Gaps table update
- **Confidence**: Medium (product verified to exist and work as described; performance and persistence claims unverified)
- **Prerequisite**: Add "Rule enforcement" to Known Gaps table *before* adding tool entry
- **Watch trigger for upgrade to 4/5**: GitHub repo becomes public + >100 stars OR independent practitioner write-up from production use + Context Graph compaction claim independently verified