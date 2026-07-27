# Evaluation: Caliber (rely-ai-org/caliber)

**Date:** 2026-03-23
**Evaluator:** Claude (Sonnet 4.6)
**Status:** ✅ Integrated — Configuration Quality section

## 📄 Résumé du contenu

- **Caliber** is a CLI tool that scores, generates, and continuously syncs AI agent configs (CLAUDE.md, MCP servers) with a codebase. Zero-install: `npx @rely-ai/caliber score`
- Scoring is 100% local and deterministic: 6 categories (Existence 25 + Quality 25 + Grounding 20 + Accuracy 15 + Freshness 10 + Bonus 7), 61 checks, no LLM calls, no network requests
- Drift detection is git-based: SHA256(file tree + dirty files) + git HEAD pointer cache, supports `caliber refresh` for automated doc updates after code changes
- Learner module captures tool events via hooks → JSONL → incremental LLM analysis → `CALIBER_LEARNINGS.md` with 70% similarity deduplication
- **GitHub: 65 stars (now 1,223 as of 2026-07-28), 12 forks, created 2026-03-10 (13 days old), MIT, TypeScript/Node.js ≥20**

## 🎯 Score de pertinence (1-5)

| Score | Signification |
|-------|---------------|
| 5 | Essentiel - Gap majeur dans le guide |
| 4 | Très pertinent - Amélioration significative |
| 3 | Pertinent - Complément utile |
| 2 | Marginal - Info secondaire |
| 1 | Hors scope - Non pertinent |

**Score: 3/5**

**Justification:** The guide already covers three config tools (claude-code-config, AIBlueprint, Packmind), but none solve the same problem as Caliber. The existing tools create or distribute config; Caliber scores existing config quality and detects when it drifts from the actual codebase. The drift detection feature (git-based, automatic) is genuinely absent from the guide's current ecosystem coverage. Score stays at 3 rather than 4 because the tool is 13 days old at time of evaluation — not enough community validation to claim "high value."

## ⚖️ Comparatif

| Aspect | Caliber | Guide actuel |
|--------|---------|-------------|
| Config quality scoring (0-100) | ✅ 61 checks, local, deterministic | ❌ Not covered |
| Config drift detection (git-based) | ✅ SHA256 tree + git HEAD cache | ❌ Not covered |
| CLAUDE.md generation from codebase | ✅ Codebase fingerprinting + LLM | ✅ AIBlueprint (scaffold only, no drift) |
| MCP server auto-suggestion | ✅ Based on detected deps | ❌ Not covered |
| Continuous sync (`caliber watch`) | ✅ Loop: score → propose → review | ❌ Not covered |
| Org-scale distribution | ❌ Single-project only | ✅ Packmind |
| Machine-to-machine config sync | ❌ Does not solve this | ❌ Still a guide gap |
| GitHub Action / CI integration | ✅ PR scoring with delta + fail-below | ❌ Not covered |
| Backup + undo | ✅ `.caliber/backups/` + manifest | ❌ Not covered |
| Multi-tool (Cursor, Codex, Copilot) | ✅ 4 tools in one | ✅ Mentioned separately |

## 🔬 Analyse technique (post-audit complet du code source)

Full source code audit conducted on `/Users/florianbruniaux/Sites/ai-setup` (local clone). Key findings:

### Scoring system

**6 categories, 61 checks, ~102 points normalized to 100:**

| Category | Max | Method |
|----------|-----|--------|
| Existence | 25 | `existsSync()` checks on CLAUDE.md, skills, MCP, rules |
| Quality | 25 | Content parsing: code blocks, token budget, concreteness ratio, duplicate detection |
| Grounding | 20 | % of project dirs/files mentioned in config (2-level scan) |
| Accuracy | 15 | Path validation + git commits since last config update |
| Freshness | 10 | Git-based staleness + secret detection (13 regex patterns) |
| Bonus | 7 | Hooks, AGENTS.md, learned content, external sources |

Scoring is hybrid: file presence (40%), content analysis (50%), git heuristics (10%). All logic in `src/scoring/checks/*.ts`. Extractable as a standalone library.

### Drift detection

Three independent signals:
1. **Tree signature:** `SHA256(sorted file tree + git dirty files)` — any add/remove/rename triggers invalidation
2. **Git HEAD pointer:** cache valid only if on same commit
3. **Git diff:** `git diff <lastSha>..HEAD` (code only, excluding CLAUDE.md/skills from drift consideration)

Cache stored at `.caliber/cache/fingerprint.json`. Stale if version mismatch, HEAD change, or signature mismatch.

### Learner module

Events captured via hooks into `.caliber/learning/session.jsonl` → incremental LLM analysis every 50 events → `CALIBER_LEARNINGS.md` (bullet format: `**[pattern|gotcha|fix|correction]** text`). Deduplication at 70% normalized text similarity. ROI tracking compares failure rates with vs without learnings across sessions.

### GitHub Action

`github-action/action.yml` + `index.js` (266 lines total). Inputs: `agent`, `fail-below`, `comment`, `auto-refresh`. Posts PR comment with score, grade, delta vs base branch. Fails CI if score < `fail-below`. Deterministic — no LLM calls in the Action itself.

### Security note

Caliber has write access to CLAUDE.md in continuous sync mode (`caliber watch`, `caliber refresh`). Same risk class as Packmind: a compromised config generation or a malicious source can propagate instructions to AI sessions. Treat `caliber init` output with the same review discipline as a Packmind playbook update.

## 🔥 Challenge (technical-writer)

Score 3/5 confirmed. Key points raised:

- **Scoring rubric opacity**: The 100-point scale is deterministic but undocumented from a user-facing standpoint (no SCORING.md). A score of 74 tells you less than it should without knowing the rubric.
- **Multi-tool depth concern**: Supporting 4 tools (Claude Code + Cursor + Codex + Copilot) risks producing generically adequate configs rather than deeply Claude Code-specific ones.
- **Write access risk underplayed in README**: The security surface of `caliber watch` (continuous writes to CLAUDE.md) deserves explicit mention.
- **Placement in guide**: Should NOT sit alongside AIBlueprint (scaffolding) — different operational category. Belongs in its own "Configuration Quality" subsection, bridging "one-project drift" (Caliber) and "org-scale distribution" (Packmind).
- **Risk of not integrating**: Low to moderate. The drift detection gap is real but not critical for most users starting from scratch.

## ✅ Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| Scoring 100% local, no LLM calls | ✅ | `src/scoring/` — no HTTP calls, pure filesystem + git |
| 61 checks across 6 categories | ✅ | `src/scoring/checks/` — counted directly |
| Zero-install `npx @rely-ai/caliber score` | ✅ | README + `package.json` bin entry |
| MIT license | ✅ | LICENSE file + `gh repo view` |
| 65 stars, 12 forks, created 2026-03-10 | ✅ | `gh repo view rely-ai-org/caliber --json` |
| Backup to `.caliber/backups/` | ✅ | `src/writers/backup.ts` |
| Before/After 35→94 score example | ⚠️ | Marketing example, not independently verifiable |
| Node.js ≥20 required | ✅ | `package.json` engines field |

No hallucinated stats. The 35→94 progression is a marketing illustration, not a measured average.

## 📍 Décision et intégration

**Score final: 3/5**
**Action: Integrated**
**Confiance: Haute sur les faits techniques, réservée sur la pérennité (outil de 13 jours)**

**Placement:** New `### Caliber` entry under `## Configuration Management` in `guide/ecosystem/third-party-tools.md`, in its own "Configuration Quality" subsection above "Engineering Standards Distribution". Explicit early-stage language, security note, and cross-ref to AIBlueprint (scaffolding) and Packmind (org-scale).

**Gaps table update:** Do NOT update the "Cross-platform config sync" row — Caliber solves config-to-codebase drift, not machine-to-machine sync. These are distinct problems.

**Re-evaluation trigger:** 200 stars or v1.0 release — whichever comes first.
