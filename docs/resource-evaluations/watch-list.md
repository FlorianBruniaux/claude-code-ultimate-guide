# Watch List

Resources monitored but not yet integrated into the guide. Event-driven re-evaluation (not time-based).

## Lifecycle

```
New resource → /eval-resource
  Score >= 3 but not ready → Active Watch
  Score < 3               → Dropped (or not listed)

Trigger reached → re-evaluation → Integrate (Graduated) / Drop (Dropped)
```

## Active Watch

| Resource | Type | Added | Why Watching | Re-eval Trigger |
|----------|------|-------|--------------|-----------------|
| [save-webpage-to-obsidian](https://github.com/benoitvx/claude-skill-save-webpage-to-obsidian) | Skill | 2026-02-25 | Skill Claude Code qui archive des articles web dans un vault Obsidian (dual extraction: Chrome MCP + WebFetch). Pattern dual-strategy intéressant mais config hardcodée, sécurité non adressée, pas de métriques adoption. Score 2/5. | >200 stars GitHub |
| [fp.dev](https://fp.dev/) | Tool | 2026-02-22 | Agent-native issue tracking pour Claude Code. Un vrai différentiateur (issues .md git-committables) mais adoption insuffisante, Apple Silicon only, redondant avec Tasks API. Score 2/5. | GitHub stars visibles + release cadence + write-up praticien en prod |
| [ICM](https://github.com/rtk-ai/icm) | MCP | 2026-02-12 | Pre-v1 (1 star, now 508 as of 2026-07-28, 11 commits) | First release + >20 stars |
| [System Prompts](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) | Tool | 2026-01-26 | Redundant with official sources. Re-evaluated 2026-02-13 (Opus 4.6 update): still 2/5. | Anthropic confirms CLI prompts not published |
| [o16g — Outcome Engineering](https://o16g.com/) | Manifesto | 2026-02-13 | Emerging framework by Cory Ondrejka (CTO Onebrief, co-creator Second Life, ex-VP Google/Meta). 16 principles for shifting from "code writing" to "outcome engineering". Honeycomb endorsement. No Claude Code-specific content yet. Memetic potential (naming follows i18n/k8s pattern). | Term adopted in >3 independent AI engineering resources OR author publishes tool-specific implementation |
| [Fabro](https://github.com/fabro-sh/fabro) | Tool | 2026-03-17 | Graph-based workflow orchestrator for AI coding agents (Rust binary, zero deps, MIT). DOT graph pipelines + multi-model routing (CSS stylesheets) + Git checkpointing per stage (unique, no equivalent found) + Daytona cloud sandboxes. Direct Claude Code integration via `curl \| claude`. Score 3/5. Eval: [079](079-fabro-workflow-orchestration.md) | >200 GitHub stars OR practitioner write-up from production use |
| [Rippletide Code](https://www.rippletide.com/dev) | Tool | 2026-03-17 | Hook-native runtime rule enforcement for Claude Code. Builds a Context Graph outside LLM context window, uses PreToolUse hooks to block violations pre-execution. Addresses CLAUDE.md degradation at scale (40+ rules) and compaction-driven rule loss. Free beta (`npx rippletide-code`, no signup). Distinct from eval 072 (MCP/SaaS). Score 3/5. Eval: [081](081-rippletide-code-rule-enforcement.md) | Public GitHub repo >100 stars OR independent practitioner write-up from production |

| [stacklit-cli](https://github.com/liza-mas/stacklit-cli) | Tool | 2026-06-10 | Go reimplementation of the documented stacklit concept (glincker/stacklit). Claims ~250 tokens codebase context, auto-configures Claude Code/Cursor/Aider. Same concept, different runtime (no npm/Node). Score 2/5. Eval: [liza-mas-token-saving-cli-tools.md](./liza-mas-token-saving-cli-tools.md) | >50 GitHub stars AND practitioner write-up from production use |

## Graduated

Resources that moved from watch to integrated in the guide.

| Resource | Graduated | Evaluation |
|----------|-----------|------------|

## Dropped

Resources removed from watch after re-evaluation.

| Resource | Dropped | Reason |
|----------|---------|--------|
