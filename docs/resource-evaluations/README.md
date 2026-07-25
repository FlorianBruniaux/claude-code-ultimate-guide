# Resource Evaluations

Ce dossier contient les évaluations de ressources externes (articles, vidéos, discussions) pour déterminer leur pertinence pour le Claude Code Ultimate Guide.

## Méthodologie

Chaque ressource est évaluée selon un système de scoring standardisé et challengée par un agent technique pour garantir l'objectivité.

### Grille de score (sur 5)

| Score | Signification | Action |
|-------|---------------|--------|
| 5 | **Critical** - Breakthrough, must integrate immediately | Intégrer sous 24h |
| 4 | **High Value** - New capability or major improvement | Intégrer sous 1 semaine |
| 3 | **Moderate** - Useful addition but not urgent | Intégrer si temps disponible |
| 2 | **Marginal** - Secondary info or niche use case | Ne pas intégrer (ou mention minimale) |
| 1 | **Low** - Redundant, incorrect, or off-topic | Rejeter |

### Process

1. **Analyse initiale**: Extraction des faits, vérification des sources
2. **Scoring**: Attribution d'un score avec justification
3. **Challenge**: Agent technical-writer remet en question le score
4. **Décision finale**: Intégration ou rejet avec traçabilité

### Nomenclature des fichiers

Format: `[topic-slug].md` (date supprimée pour stabilité des liens)

Exemple: `remotion-claude-code-video.md`

## Working Documents

Les documents de travail bruts (prompts Perplexity, audits clients) restent dans `claudedocs/resource-evaluations/` (gitignored).

## Index des Évaluations

| Ressource | Score Initial | Score Final | Décision | Fichier |
|-----------|---------------|-------------|----------|---------|
| **Anthropic Releases** (Jan 16-23, 2026) | - | - | ✅ Suivi régulier | [anthropic-releases-jan16-23-2026.md](./anthropic-releases-jan16-23-2026.md) |
| **Caliber** (rely-ai-org/caliber) | 3/5 | 3/5 | ✅ Intégré: Configuration Quality | [caliber-config-quality-tool.md](./caliber-config-quality-tool.md) |
| **AST-grep** (Flavien Métivier) | 3/5 | **4/5** | ✅ Intégrer workflow | [astgrep-flavien-metivier.md](./astgrep-flavien-metivier.md) |
| **MCP Apps** (SEP-1865) | 3/5 | **4/5** | ✅ Intégré (architecture + guide) | [mcp-apps-announcement.md](./mcp-apps-announcement.md) |
| **Boris Cherny** (Cowork Video) | 4/5 | **4/5** | ✅ Intégré (mental models) | [boris-cowork-video-eval.md](./boris-cowork-video-eval.md) |
| **Clawdbot** (Twitter Analysis) | 2/5 | **2/5** | ⚠️ Watch only | [clawdbot-twitter-analysis.md](./clawdbot-twitter-analysis.md) |
| **GSD** (Getting Shit Done) | 4/5 | **4/5** | ✅ Intégré (workflow) | [gsd-evaluation.md](./gsd-evaluation.md) |
| **Nick Jensen Plugins** | 3/5 | **3/5** | ✅ Mention | [nick-jensen-plugins.md](./nick-jensen-plugins.md) |
| **Prompt Repetition Paper** | 3/5 | **4/5** | ✅ Intégrer best practices | [prompt-repetition-paper.md](./prompt-repetition-paper.md) |
| **Remotion + Claude Code** (Video Production) | 2/5 | **3/5** | ✅ Mention minimale | [remotion-claude-code-video.md](./remotion-claude-code-video.md) |
| **SE-Cove Plugin** | 2/5 | **2/5** | ⚠️ Watch only | [se-cove-plugin.md](./se-cove-plugin.md) |
| **Self-Improve Skill** | 3/5 | **3/5** | ✅ Template ajouté | [self-improve-skill.md](./self-improve-skill.md) |
| **Steinberger** (Inference Speed) | 3/5 | **3/5** | ✅ Intégré (minimal) | [steinberger-inference-speed.md](./steinberger-inference-speed.md) |
| **UML & OOP Diagrams** | 3/5 | **3/5** | ✅ Mention | [uml-oop-diagrams.md](./uml-oop-diagrams.md) |
| **Vibe Coding Level 2** (Rusitschka) | 4/5 | **4/5** | ✅ Intégré (workflows) | [vibe-coding-rusitschka.md](./vibe-coding-rusitschka.md) |
| **Peter Wooldridge** (Productivity Stack) | 2/5 | **3/5** | ✅ Practitioner Insights | [wooldridge-productivity-stack.md](./wooldridge-productivity-stack.md) |
| **System Prompts** (Official vs Community) | 4/5 | **2/5** | ⚠️ Watch only (official sources exist) | [system-prompts-official-vs-community.md](./system-prompts-official-vs-community.md) |
| **Worktrunk** | 4/5 | **4/5** | ✅ Intégré (workflow) | [worktrunk-evaluation.md](./worktrunk-evaluation.md) |
| **Pat Cullen** (Multi-Agent PR Review) | 5/5 | **5/5** | ✅ Intégré (review-pr, code-reviewer, guide) | [017-pat-cullen-final-review.md](./017-pat-cullen-final-review.md) |
| **Docker Sandboxes** (Isolation Landscape) | 4/5 | **4/5** | ✅ Intégré (guide + notice) | [docker-sandboxes-isolation.md](./docker-sandboxes-isolation.md) |
| **dclaude** (Dockerized Claude Code) | 2/5 | **2/5** | ⚠️ Footnote (sandbox-isolation.md) | [dclaude-docker-wrapper.md](./dclaude-docker-wrapper.md) |
| **10 Tips from Inside the Claude Code Team** (paddo.dev) | 4/5 | **4/5** | ✅ Intégré (4 sections) | [paddo-team-tips-eval.md](./paddo-team-tips-eval.md) |
| **Sankalp's Claude Code 2.0 Experience** | 2/5 | **2/5** | ⚠️ Watch only (85% overlap, probable errors) | [sankalp-claude-code-experience.md](./sankalp-claude-code-experience.md) |
| **Kajan Siva** (/insights command) | 2/5 | **2/5** | ❌ Do not integrate (no technical content) | [kajan-siva-insights-command.md](./kajan-siva-insights-command.md) |
| **Zolkos** (/insights deep dive) | 4/5 | **4/5** | ✅ Integrate (architecture + facets) | [zolkos-insights-deep-dive.md](./zolkos-insights-deep-dive.md) |
| **Grenier** (Agent/Skill Quality) | 3/5 | **3/5** | ✅ Intégrer partiellement | [grenier-agent-skill-quality.md](./grenier-agent-skill-quality.md) |
| **Awesome Claude Skills** (BehiSecc) | 3/5 | **3/5** | ✅ Mention spécialisée | [awesome-claude-skills-github.md](./awesome-claude-skills-github.md) |
| **Wasp Fullstack Essentials** (Vinny @ Wasp) | 3/5 | **3/5** | ✅ Intégrer concepts framework-agnostiques | [wasp-fullstack-essentials-eval.md](./wasp-fullstack-essentials-eval.md) |
| **Master Claude Code Infographic** (Rakesh Gohel / Aakash Gupta) | 2/5 | **2/5** | ❌ Ne pas intégrer (surface-level, erreur Cursor) | [rakesh-gohel-aakash-gupta-master-claude-code.md](./rakesh-gohel-aakash-gupta-master-claude-code.md) |
| **Snyk ToxicSkills** (Supply Chain Audit) | 4/5 | **4/5** | ✅ Intégré (security-hardening.md §1.1, §1.2, §1.5) | [snyk-toxicskills-evaluation.md](./snyk-toxicskills-evaluation.md) |
| **System Prompts Opus 4.6** (Official Update) | 2/5 | **2/5** | ⚠️ Watch only (2nd eval, same URL, already covered) | [system-prompts-opus-4-6-update.md](./system-prompts-opus-4-6-update.md) |
| **Straude** (Social usage tracker) | 3/5 | **3/5** | ✅ Intégré (third-party-tools.md, analyse sécurité) | [straude-evaluation.md](./straude-evaluation.md) |
| **qmd Token Savings** (Simone Ruggiero, Medium) | 2/5 | **2/5** | ❌ Ne pas intégrer (redundant avec grepai, claims non vérifiables) | [2026-02-14-simone-ruggiero-qmd-token-savings-medium.md](./2026-02-14-simone-ruggiero-qmd-token-savings-medium.md) |
| **Rippletide** (AI Reliability Platform) | 2/5 | **2/5** | ⚠️ Watch only (MCP server tiers, claims non vérifiables, pas de traction) | [072-rippletide-ai-reliability-platform.md](./072-rippletide-ai-reliability-platform.md) |
| **Community Signals & Benchmark** (March 2026 synthesis) | 4/5 | **3/5** | ✅ No integration (all gaps already covered; 2 factual errors detected) | [community-signals-benchmark-march-2026.md](./community-signals-benchmark-march-2026.md) |
| **context-evaluator** (PackmindHub/context-evaluator) | 4/5 | **4/5** | ✅ Integrated: third-party-tools.md + 2 patterns in skill-design-patterns.md | [context-evaluator-evaluation.md](./context-evaluator-evaluation.md) |
| **liza-mas CLI Tools** (scip-search, mdtoc, functional-clusters, stacklit-cli) | 1-2/5 | **1-2/5** | ❌ Reject (3 tools) / ⚠️ Watch only (stacklit-cli, one-line note) | [liza-mas-token-saving-cli-tools.md](./liza-mas-token-saving-cli-tools.md) |
| **Semble** (MinishLab/semble) | 3/5 | **3/5** | ✅ Integrated: mcp-servers-ecosystem.md Code Search section | [semble-code-search.md](./semble-code-search.md) |
| **MDMA** (MobileReality/mdma) | 3/5 | **3/5** | ✅ Integrated: ai-ecosystem.md Section 7.1 (generative UI) | [mdma-evaluation.md](./mdma-evaluation.md) |
| **BMAD-METHOD** (bmad-code-org) | 4/5 | **4/5** | ✅ Integrated: spec-first.md (multi-role planning) | [bmad-method-spec-driven-agents.md](./bmad-method-spec-driven-agents.md) |
| **OpenHands** (All Hands AI) | 4/5 | **4/5** | ✅ Integrated: agentic-tools.md §2.4 | [openhands-autonomous-agent.md](./openhands-autonomous-agent.md) |
| **Spec-Kitty** (Priivacy-ai) | 3/5 | **3/5** | ✅ Mention: spec-first.md (worktree isolation) | [spec-kitty-worktree-isolation.md](./spec-kitty-worktree-isolation.md) |
| **Agent Orchestrator** (AgentWrapper, ex-ComposioHQ) | 3/5 | **3/5** | ✅ Mention: third-party-tools.md (OSS equivalent to Conductor) | [agent-orchestrator-composio.md](./agent-orchestrator-composio.md) |
| **Liza** (framework MAS, liza-mas/liza) | 3/5 | **3/5** | ✅ Mention: spec-first.md (OSS governance reference architecture) | [liza-mas-framework.md](./liza-mas-framework.md) |
| **IA-QA CLI** (@ia-qa/cli, Jean-Christophe Jamet) | 3/5 | **2/5** | ⚠️ Watch only (thin client, tous les inputs partent sur un serveur tiers ; heuristiques mesurées à -35% sur du code) | [ia-qa-cli-llm-testing.md](./ia-qa-cli-llm-testing.md) |
| **Fusion** (Runfusion/Fusion, MIT) | 4/5 | **4/5** | ✅ Case study only, not a recommended tool (double-checkout anti-cheat pattern + agentic velocity without architecture ; bus factor 1, 94% of commits by one person) | [fusion-multi-agent-orchestrator.md](./fusion-multi-agent-orchestrator.md) |

## Watch List

Ressources surveillées mais pas encore intégrées : [watch-list.md](./watch-list.md)

---

**Dernier update**: 2026-07-15 (162 fichiers d'évaluation sur disque, 45 indexés ci-dessus ; l'écart est un reliquat connu qui attend une passe d'audit dédiée)
