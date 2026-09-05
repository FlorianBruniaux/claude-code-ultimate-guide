# Whitepapers CHANGELOG

Suivi des versions des ebooks, indépendamment de la version du guide.

**Convention de version** : `MAJOR.MINOR.PATCH`
- `MAJOR` : refonte structurelle (nouveau périmètre, nouvelle audience, changement de titre)
- `MINOR` : enrichissement significatif (nouvelles sections, nouveaux angles, feedback terrain intégré)
- `PATCH` : corrections, clarifications mineures, données mises à jour

**Relation avec le guide** : chaque entrée de changelog indique la version du guide à laquelle correspond la mise à jour de l'ebook (champ `version` dans le frontmatter).

---

## [2026-08-30] DORA 2026 et corpus Pavan Belagatti

### Fixed

- **WP11 FR/EN**: version 1.3.0 à 1.3.1. Le modèle historique à quatre métriques et MTTR est remplacé par les cinq métriques DORA actuelles: Change Lead Time, Deployment Frequency, Failed Deployment Recovery Time, Change Fail Rate et Deployment Rework Rate. Les anciennes tables Elite, High, Medium et Low sont retirées comme cibles courantes, les chiffres internes d'Anthropic sont bornés à leur environnement, et le protocole relie désormais déploiements, incidents et rework.
- **WP12 FR/EN**: version 1.4.0 à 1.4.1. La recommandation Engineering Manager cite les cinq métriques DORA actuelles; la version anglaise est alignée pour conserver une version bilingue commune.

## [2026-08-30] Loop, graph, harness, orchestrator: publications dérivées

### Added

- **WP12 FR/EN**: version 1.3.0 à 1.4.0. Une synthèse explicite distingue boucle, graphe, harness et orchestrateur, remplace la hiérarchie de couches par la plus petite structure de contrôle qui résout le besoin en sécurité, précise le sens opérationnel de `unknown`, et renvoie vers la nouvelle page `Loop & Graph Engineering` (`https://cc.bruniaux.com/guide/loop-graph-engineering/`).
- **Fiche WP12 FR**: la synthèse remplace le point générique sur le harness par la taxonomie loop/graph/harness/orchestrator et la consigne de qualifier les mécanismes observés avant le pilote.
- **C14 FR/EN Agent Harness Map**: la carte une page précise que boucle et graphe sont des vues, pas des couches supplémentaires, ajoute l'étape de flux versionné, rappelle les quatre statuts appliqués aux mécanismes observés, et renvoie vers la nouvelle page `Loop & Graph Engineering`.
- **Cheatsheets FR/EN**: la carte rapide des quatre couches ajoute la frontière boucle/graphe, réserve `confirmed`/`claimed`/`unknown` aux mécanismes observés, et renvoie vers la nouvelle page `Loop & Graph Engineering`.

## [2026-08-28] Agent Harness Map, publications dérivées

### Added

- **WP12 FR/EN**: version 1.1.1 à 1.3.0. La sélection distingue runtime, contrat de dépôt, orchestrateur et boucle externe d'optimisation. Le whitepaper remplace l'affirmation universelle sur la primauté du harness par le couple modèle-harness, ajoute les résultats contrôlés de *The Scaffold Effect*, et documente Meta-Harness, Agentic Harness Engineering et HarnessOpt-Bench avec leurs limites expérimentales.
- **WP04 FR/EN**: version 1.4.1 à 1.5.0. Les responsabilités des quatre couches sont ajoutées.
- **WP08 FR/EN**: version 1.5.1 à 1.6.0. La frontière entre runtime et orchestrateur est ajoutée.
- **WP11 FR/EN**: version 1.2.1 à 1.3.0. Le protocole d'essai et ses métriques sont ajoutés.
- **WP07 FR/EN**: version 1.4.3 à 1.4.4. Les références canoniques portables sont ajoutées sans transformer le catalogue étendu en classement de runtimes.
- **C14 FR/EN Agent Harness Map**: fiche parallèle sur les quatre couches, les cinq surfaces de preuve, le couple modèle-harness et la position externe des optimiseurs.
- **Cheatsheets FR/EN et guide cheatsheet**: table compacte des quatre couches, couple modèle-harness, optimiseur externe et liens canoniques vers Agent Harness Map, Agent Harness Engineering, Agent Tools et le glossaire.

### Changed

- **C12 FR/EN**: claims larges sur les intégrations IDE, le SDK et MCP remplacés par des surfaces à vérifier; les volumes d'installation non sourcés sont retirés.
- **M16 FR/EN**: seuils de taille, de contexte, de budget et de nombre d'agents non justifiés remplacés par des critères observables de décomposition, coût, récupération et revue indépendante.
- **T22 FR/EN**: les outils tiers sont décrits comme des couches adjacentes, pas comme des runtimes.
- **Catalogues de publication**: série corrigée à 13 whitepapers et 58 fiches par langue. Les PDF C14 FR/EN ont été rendus en A4 sur une page et portent le total à 58 PDF par langue dans le lot de publication. Les frontmatters C12, C14 et T22 utilisent désormais la date ISO `2026-08-28`, ce qui empêche Typst de rabattre les pieds de page localisés sur une date incorrecte.

## [2026-08-24] Audit de style anti-IA, 13 whitepapers + 57 fiches récap, PDF régénérés et déployés

Passage systématique des 13 whitepapers et des 57 fiches récap (FR+EN, 70 documents bilingues) contre la checklist `~/.claude/ANTI_AI.md` (em dash, ouvertures stéréotypées, deux-points rhétoriques d'annonce, chutes sentencieuses, emoji décoratifs, personas inventées, buzzwords creux), via 70 agents en parallèle (1 par document bilingue), suivi d'une passe de vérification. 59 documents sur 70 étaient déjà conformes. 11 ont reçu des corrections réelles, la plus importante étant WP07 (51 corrections, essentiellement des tirets `---` faisant office d'em dash). Deux points laissés en l'état par choix éditorial délibéré, à trancher séparément : les personas récurrentes (Antoine, Léa, Karim, Sophie, Marc, Thomas, Julien) utilisées dans les encadrés de mise en situation à travers toute la série, et le marqueur de navigation `📖 Pour aller plus loin / Further reading` répété à l'identique sur les 13 whitepapers. Les 10 whitepapers et la fiche récap M03 modifiés ont vu leurs PDF (et EPUB pour les whitepapers) régénérés et redéployés sur `florian-portfolio/public/guides/`, avec mise à jour de `guides.mjs`, `whitepapers-data.ts` et `recap-cards-data.ts` (landing), plus régénération du ZIP série méthodologie (FR+EN).

### Fixed
- **WP07 Guide de Référence** : 51 corrections (24 FR + 27 EN), essentiellement des tirets `---` en em dash et des emoji décoratifs hors tableau.
- **WP11 Team Metrics** : 20 corrections (10 FR + 10 EN), deux-points rhétoriques d'annonce réécrits en phrases directes.
- **WP00, WP01, WP02, WP04, WP05, WP06, WP08, WP09** : corrections ponctuelles (emoji décoratifs, personas isolées, buzzwords, chutes sentencieuses), 4 à 10 par whitepaper.
- **Fiche récap M03 Sessions Continuité** : chute sentencieuse type maxime réécrite en phrase factuelle (FR+EN).

---

## [2026-08-24] Audit de contenu complet, 13 whitepapers + 57 fiches récap, PDF régénérés et déployés

Premier audit de contenu (pas seulement de fraîcheur des métadonnées) mené sur l'ensemble de la série depuis sa création : chaque whitepaper et chaque fiche récap comparés phrase par phrase au guide actuel et au `CHANGELOG.md` racine, via deux passages d'agents en parallèle (13 pour les whitepapers, 12 lots de 5 fiches pour les fiches récap). 116 problèmes trouvés sur les whitepapers (35 critiques), dont plusieurs répétés à l'identique sur les fiches récap qui en dérivent : Claude Opus 4.8 présenté comme modèle par défaut (remplacé par Opus 5 depuis v2.1.219), profondeur de nesting des sub-agents à 5 niveaux (actuellement 3), outil `MultiEdit` inventé, `TodoWrite` présenté sans la mention de désactivation par défaut depuis v2.1.233, `--safe-mode` mal décrit, champ `agent:` inventé dans les frontmatters SKILL.md, chemins de fichiers cassés (`guide/security-hardening.md`, `guide/data-privacy.md`, etc.), et pour 03-securite, l'omission du gap de sécurité le plus grave documenté dans le guide (`permissions.deny` sur Read n'atteint jamais un sous-processus Bash). Détail complet : `claudedocs/whitepaper-content-audit-2026-08-24.md` et `claudedocs/recap-card-content-audit-2026-08-24.md` (non versionnés, working docs). Toutes les corrections appliquées, `wp-version` bumpé en patch sur les 13 whitepapers, `guide-version`/`version` synchronisés à 3.41.3 sur les 57 fiches récap. Les 26 PDF whitepapers et les 114 PDF de fiches récap (+ 6 ZIP par série T/M/C × FR/EN) ont été régénérés et déployés sur `florian-portfolio/public/guides/`, avec mise à jour de `guides.mjs` (liens email) et `whitepapers-data.ts`/`recap-cards-data.ts` (landing).

### Fixed
- **13 whitepapers FR+EN** : voir `CHANGELOG.md` racine, entrées "recap cards" et "whitepapers" du 2026-08-24 pour le détail par WP.
- **57 fiches récap FR+EN** : voir `CHANGELOG.md` racine, entrées "Recap cards" du 2026-08-24 pour le détail par lot.

---

## [2026-08-20] Cheatsheet v1.1.2: /ultraplan removed, /simplify description corrected

`/ultraplan` was removed from Claude Code in v2.1.222 (2026-08-04). The FR and EN cheatsheets still listed it as a research-preview command five months of releases later, discovered while syncing the release tracker to v2.1.237. `/simplify`'s description was also stale: it described general over-engineering detection with auto-fix, the behavior before v2.1.154 reworked it into a cleanup-only review (reuse, simplification, efficiency) that no longer hunts bugs.

### Fixed
- **`/ultraplan` row removed** (cheatsheet FR and EN, Essential Commands table): the command no longer exists.
- **`/simplify` description corrected** (cheatsheet FR and EN): now states the post-v2.1.154 cleanup-only behavior instead of the pre-rename general-purpose description.

---

## [2026-08-05] WP11 v1.2.0: 2026 tooling market gap closed, board-reporting section added

Fresh research against the current delivery-intelligence market surfaced content missing from WP11 since its last substantive pass: half the active 2026 tooling market, probabilistic Monte Carlo forecasting, and LLM-generated board narratives, none previously documented anywhere in the whitepaper series. A fourth gap, guidance for reporting delivery capacity to a board that doubts a team after past slips, had no existing coverage at all. Both FR and EN updated in full (not a stub translation), `wp-version` bumped 1.1.0 to 1.2.0 on both.

### Added
- **WP11 EN and FR** (Leading a Team in the Age of AI / Piloter une Équipe à l'Ère de l'IA, v1.1.0 to v1.2.0): "Broader Delivery Intelligence Platforms" subsection added under Tooling, covering DX, Multitudes, Swarmia, Cortex.io, Jellyfish, Oobeya, and Hatica, the last flagged explicitly as thinner on documented specifics than the rest. Jellyfish and Cortex.io were already cited elsewhere in the guide as data sources for PR-size and change-failure-rate figures; this is their first documentation as delivery-intelligence tools in their own right. "AI-Generated Board Narratives" subsection added, covering LinearB's AI iteration summary and Jellyfish's "AI Executive Report," both framed as explanation and prioritization of already-computed metrics, not new statistical analysis. New top-level "Probabilistic Delivery Forecasting" section added covering ActionableAgile and Nave's Monte Carlo simulation, including Nave's load-bearing quote on the single requirement for reliable forecasts (a predictable delivery system) and an explicit statement that Monte Carlo forecasting replicates an unstable system's unpredictability as a wider distribution rather than fixing it. New top-level "Reporting Delivery Capacity to a Skeptical Board" section added as general engineering-management guidance (no case study, no named individuals): reframes board doubt as a trust and visibility problem rather than a data problem, states plainly that no published study measures whether delivery-intelligence tooling repairs executive trust, and covers named delivery scenarios over velocity charts, capped strategic objectives over multi-quarter feature roadmaps, tracking commitment hit-rate as the trust-rebuilding metric, and pre-aligning board members individually before the plenary meeting. The Uplevel Copilot study (no significant change to coding speed, PR cycle time, or throughput after adoption, alongside a 41% increase in bug rate and a "Sustained Always On" burnout-risk proxy that fell more for developers without Copilot) added alongside the existing Digital Applied heavy-user review-time contradiction, both making the same point from independent data.

---

## [2026-07-29] Slash-command corrections across whitepapers and recap cards

Fallout from re-deriving the built-in command list against the official reference at `code.claude.com/docs/en/commands`. Two errors ran through every publication surface: `/execute`, which is not a Claude Code command and appears nowhere in the official reference or in the upstream CHANGELOG, and `/less-permission-prompts`, which shipped under that name in v2.1.111 and has since been renamed `/fewer-permission-prompts`. Four command descriptions were also describing something the command does not do. 11 whitepapers and 6 recap cards touched, `wp-version` bumped on each whitepaper, PDFs and EPUBs still need a rebuild.

### Fixed
- **`/execute` removed everywhere it was presented as a command** (02-personnalisation FR, 02-customization EN, 07-guide-reference FR, 07-reference-guide EN, cheatsheet FR and EN, devwithai-cheatsheet FR, m05-plan-mode FR and EN): replaced with "approve the plan Claude presents, or `Shift+Tab` to leave without approving". In the two 07 reference whitepapers the row was reused for `/code-review`, which is the command that actually belongs in a shipping-workflow table.
- **`/less-permission-prompts` to `/fewer-permission-prompts`** (01-prompts-efficaces FR, 01-effective-prompts EN, 03-securite FR, 03-security EN, 07-guide-reference FR, 07-reference-guide EN, 03-permission-modes FR and EN): the old name is kept inline as the v2.1.111 shipping name so the release notes stay findable.
- **Four command descriptions corrected against the official reference** (01-prompts-efficaces FR, 01-effective-prompts EN, 07-guide-reference FR, 07-reference-guide EN): `/proactive` was described as a "proactive mode where Claude anticipates and suggests actions" when it is an alias of `/loop`; `/undo` as "undoes Claude's last action" when it is an alias of `/rewind` and returns to a checkpoint; `/tui` as "toggle terminal UI mode" when it picks the renderer and relaunches into it; `/focus` as "reduces distractions and centers Claude on the task" when it is a fullscreen-only view toggle.
- **`/effort` enum fixed in four places** (07-guide-reference FR, 07-reference-guide EN, 01-commandes-essentielles FR): the tables listed `xlow/low/default/high/xhigh/max`. Neither `xlow` nor `default` exists. The real ladder is `low`, `medium`, `high`, `xhigh`, `max`, `ultracode`, with the last two session-only. 01-effective-prompts EN went further and built a paragraph around a fabricated "4-level scale distinct from the API scale"; that claim is now replaced with the actual ladder.
- **01-commandes-essentielles FR and EN**: `/sessions` does not exist and was removed from the session-commands block, replaced by `/branch`; `#file` / `#fichier` was listed as "add file to context" when the `#` quick-memory shortcut has been removed upstream, corrected to `@file`; the EN card still told readers to run `/vim`, removed in v2.1.92, and the FR card still gave `{"vim": true}` as the settings key when the real one is `editorMode: "vim"`; the EN keyboard table listed `Ctrl+J` / `Cmd+J` as "open Claude Code" and `Shift+Tab` as "toggle auto-accept mode", replaced with the actual mode cycle and `Ctrl+O`.
- **m05-plan-mode FR and EN**: guide `version` synced from 3.41.0 to 3.41.1, which the rest of the card set already carried.

## [2026-07-03] v3.41.1: Content freshness pass, 14 EN recap cards

Same audit as the FR recap-cards pass of July 2 (dead `settings.json` keys checked against `guide/core/settings-reference.md`, `.claude/commands/` references vs the CC 2.1.3 skills merge, invented CLI flags checked against `claude --help`), applied to all 57 EN cards. Every problem fixed in FR was also present in EN. The pass additionally surfaced 6 findings the FR audit missed, all still present in the FR counterparts: the fictitious `--no-stream` CLI flag (01, t02), the fictitious `--task-manage` flag presented as a native CC feature "since v2.1.19" (m07, it is a SuperClaude framework flag), the non-existent `{"vim": true}` settings key (01, real key is `editorMode: "vim"`), `spinnerVerbs.mode: "add"` (t06, valid values are `replace`/`append`), the non-existent `sandbox.network.policy` key (t16), and a settings-style `allowedTools:` snippet (c08). 14 EN cards fixed, `guide-version`/`version` synced to 3.41.1, all 14 PDFs rebuilt.

### Fixed
- **01-commandes-essentielles EN**: fictitious `claude --context CLAUDE.md` replaced with the auto-load note + in-session `@file` pattern; `--no-stream` tip replaced with the real `--verbose` flag / `Ctrl+O` toggle; `{"vim": true}` corrected to `/vim` or `{"editorMode": "vim"}`.
- **03-permission-modes EN**: modes table rewritten with canonical names (`default`/`acceptEdits`/`plan`/`auto`/`bypassPermissions`), the wrong "Auto-accept all via Shift+Tab x2" row replaced by Plan mode, `/less-permission-prompts` row and `--permission-mode` / `permissions.defaultMode` activation notes added.
- **04-context-management EN**: `--context` flag removed from the context-sources list and the examples, replaced with `.claude/rules/*.md` auto-loading.
- **c03-xml-prompting-anchors EN**: `.claude/commands/` reference updated to `.claude/skills/`.
- **c06-configuration-decision-guide EN**: top-level `"allowedTools"` key replaced with `permissions.allow`.
- **c08-surface-attaque-menaces EN**: `allowedTools:` snippet replaced with `permissions.allow:`.
- **m07-todowrite-vs-tasks-api EN**: fictitious `--task-manage` flag section replaced with the real default-on behavior (Tasks API default since v2.1.142, `CLAUDE_CODE_ENABLE_TASKS=0` to revert); wrong "enabled by default since v2.1.19" comment corrected.
- **m11-hooks-evenements-systeme EN**: `SessionEnd` and `PreCompact` rows added to the main events table.
- **t02-mode-non-interactif EN**: entire `--no-stream` section rewritten, print mode already writes the complete response in one block, real-time streaming is opt-in via `--output-format stream-json`.
- **t04-permissions-glob-patterns EN**: 3 `autoApproveTools` blocks replaced with `permissions.allow`.
- **t06-settings-json EN**: model example bumped to `claude-sonnet-5`; `permissions.defaultMode`, `permissions.additionalDirectories`, `statusLine`, `outputStyle` added to the JSON example and keys table; `mode: "add"` corrected to `mode: "append"`; `commands/` updated to `skills/` in the commit list.
- **t09-workspace-hygiene EN**: `.claude/` tree and commit list updated for the commands/skills merge.
- **t10-config-multi-machine EN**: `commands/` removed from the shareable table, symlink setup, git add, and cron backup examples (4 spots).
- **t16-sandbox-natif-architecture EN**: non-existent `sandbox.network.policy` key removed; allowlist/blocklist explained via the real `allowedDomains`/`deniedDomains` keys.

---

## [2026-07-03] v3.41.1: WP03 FR stale malicious-author/skill counters

### Fixed
- **WP03 FR** (Sécurité, v1.4.0 → v1.4.1): the July 2 EN pass had flagged stale malicious-author/skill counts as affecting both languages, but only the EN file got the fix. FR still claimed 5 confirmed authors and 314+/341+ malicious skills. Corrected against `threat-db.yaml` v2.23.0: 6 confirmed authors (sakaen736jih added), hightower6eu alone at 677 VirusTotal-confirmed skills, ClawHavoc campaign grown from 341 to 1,184+ confirmed entries by March 1, 2026. PDF and EPUB rebuilt.

---

## [2026-07-02] v3.41.1: Content freshness pass, 13 whitepapers EN

Same deep-dive audit and fix method applied to FR (13 dedicated sub-agents, one per whitepaper) extended to the EN series after FR/EN drift was flagged. Same class of gaps confirmed present in EN: WP04 and WP07 had the identical "sub-agents cannot spawn sub-agents (depth=1)" factual error, WP08 was missing the same 450-line Advanced Orchestration Patterns section, WP11 was missing the same Agentic Metrics section, WP12 was missing the same 4 evaluation subsections. Every fix was independently verified line-by-line post-edit (not just a version-field bump) after an earlier FR fix pass on WP00 was found to have missed its series-list correction despite a clean version bump. All 13 EN whitepapers corrected, PDF+EPUB rebuilt. `whitepapers/en/05-team.qmd` confirmed untracked by git (blanket `whitepapers/` gitignore rule, unlike sibling files), flagged but not fixed in this pass.

### Fixed
- **WP04 EN** (Architecture, v1.3.0 → v1.4.0): same factual error as FR, 4 occurrences of "depth=1" sub-agent claim corrected to 5 levels (v2.1.172). Sonnet 5 and Fable 5 added to model/knowledge-cutoff tables. Footer version mismatch and series count fixed.
- **WP07 EN** (Reference Guide, v1.3.0 → v1.4.0): same "depth=1" error corrected. Sonnet 5 added, Dynamic Workflows section added, 4 previously-unreferenced guide pages linked (agent-harness, memory-systems, hooks-events-reference, tools-reference). Series count and footer version fixed.
- **WP02 EN** (Customization, v1.4.0 → v1.5.0): same commands→skills internal contradiction as FR fixed in the Recommended Structure tree and Memory Loading Comparison table.
- **WP09 EN** (Learning with AI, v1.2.0 → v1.3.0): Agent Adoption Curve table replaced with the guide's real 7-level scale (was inventing labels matching no guide table, same pre-existing bug as FR). Deleuze/Lepine practitioner paragraphs added.
- **WP01 EN** (Effective Prompts, v1.2.0 → v1.3.0): additionally found and fixed 3-4 dead internal section links caused by guide renumbering, not present in the FR audit brief.

### Added
- **WP00 EN** (Series Introduction, v1.4.0 → v1.5.0): series footer corrected to list all 13 whitepapers (was 12, WP12 missing, WP04/06/10 wrongly marked "coming soon"). Stats and feature table (Opus 4.8, Fable 5, Sonnet 5, nested sub-agents) updated.
- **WP03 EN** (Security, v1.3.0 → v1.4.0): threat-db reference updated v2.17.0 → v2.23.0, T030-T033 and 4 CVEs added, WASM MCP sandboxing (§7b) added, `sandbox.credentials` added. Additionally found stale malicious-author/skill counts affecting both FR and EN (6 authors not 5, ClawHavoc total 1,184 not 341+) and a new guide §1.6 missing from both languages.
- **WP05 EN** (Team, v1.5.0 → v1.6.0): api-gateway.md, observability.md §10, and enterprise-governance.md §2.3 cross-references added, mirroring FR.
- **WP06 EN** (Privacy, v1.2.0 → v1.3.0): 7-point audit checklist items and WASM MCP sandboxing added, mirroring FR.
- **WP08 EN** (Agent Teams, v1.4.0 → v1.5.0): same 7 advanced orchestration patterns ported as FR, plus the same 4 IFTTD testimonials.
- **WP10 EN** (AI Budget, v1.2.0 → v1.2.1): api-gateway.md cross-reference and pricing date stamp refreshed, mirroring FR.
- **WP11 EN** (Team Metrics, v1.0.1 → v1.1.0): same "Agentic Metrics: What DORA Doesn't Measure" section ported as FR (METR, DeputyDev, c-CRAB, Code Review Bench, Strata/Zenity studies), self-hosted observability stack, PR Audit Trail summary.
- **WP12 EN** (Agent Engineering, v1.0.0 → v1.1.0): same 4 missing "Evaluating Probabilistic Systems" subsections added as FR, plus a dynamic-workflows.md reference.

---

## [2026-07-02] v3.41.1: Content freshness pass, 13 whitepapers FR

Deep-dive content audit (13 dedicated sub-agents, one per whitepaper, cross-referenced against CHANGELOG `[Unreleased]` and `machine-readable/`) found content drift the earlier version-only check missed, including two factually wrong claims. All 13 FR whitepapers (00-12) corrected, `version` field synced to 3.41.1, PDF and EPUB rebuilt for all.

**Follow-up fix (same day):** the first content-correction pass bumped `version` and `wp-version` but left the `date` frontmatter field unchanged on 12 of 13 files (still April/May 2026), which drives the cover-page date via `date-format: "MMMM YYYY"`. 7 files also had a stale in-body "Version X.Y.Z | Month Year" footer stamp not synced by the fix agents (00, 01, 02, 03, 06, 09, 12; WP09's was the worst offender at "Version 3.27.6"). Bumped `date` to 2026-07-02 on all 13, corrected the 7 stale footer stamps, and rebuilt all 13 PDF+EPUB a second time to reflect the corrected cover date.

### Fixed
- **WP04 FR** (Architecture, v1.3.0 → v1.4.0): corrected a factually wrong claim, "sub-agents cannot spawn sub-agents (depth=1)" was outdated since v2.1.172 (up to 5 levels now). Updated the model table from Sonnet 4.6 to Sonnet 5 as default (native 1M context). Added Fable 5. Fixed footer version/date inconsistency.
- **WP07 FR** (Guide Référence, v1.3.0 → v1.4.0): same "depth=1" factual error corrected. Added Sonnet 5 to the model table, Dynamic Workflows, references to 7 previously unlinked guide pages (agent-harness, memory-systems, hooks-events-reference, tools-reference, team-knowledge-base, practitioner-insights, agentic-tools). Series listing corrected from 12 to 13 whitepapers.
- **WP02 FR** (Personnalisation, v1.4.0 → v1.5.0): fixed an internal contradiction, the doc correctly stated the commands→skills migration but its own "Structure Recommandée" and Git rules table still showed a separate `commands/` folder.
- **WP09 FR** (Apprendre avec l'IA, v1.2.0 → v1.2.1): replaced the "Courbe d'Adoption Agentique" table, its 7 labels matched no table in the current guide (pre-existing drift, unrelated to recent guide changes).

### Added
- **WP00 FR** (Introduction, v1.4.0 → v1.5.0): series footer now lists all 13 whitepapers (was 12, WP12 missing; WP04/06/10 wrongly marked "à venir"). Corrected stats (26,496 lines, 181 templates) and feature table (Opus 4.8, Fable 5, `--safe-mode`, nested sub-agents).
- **WP01 FR** (Prompts efficaces, v1.2.0 → v1.3.0): Thinking Modes section updated to Opus 4.8/Fable 5 and the 5-tier effort parameter (was binary Opus 4.5/4.6). Added a 5th context-engineering layer covering §9.26 Review-Driven Context Optimization (`crit`).
- **WP03 FR** (Sécurité, v1.3.0 → v1.4.0): threat-db reference updated from v2.17.0 to v2.23.0. Added T030 TrustFall, T031 Shadow Escape, T032 Miasma Worm, T033 Agentjacking, and 4 CVEs (2026-50548/50549, 32871, 32625, 0621). Added experimental WASM MCP sandboxing (§7b) and `sandbox.credentials`.
- **WP05 FR** (Équipe, v1.5.0 → v1.6.0): new "API Gateway & budgets centralisés" section (LiteLLM, virtual keys, model allowlists) and team-level log aggregation (Loki/Tempo/Grafana). Governance callout replaced with the 3 concrete config-propagation mechanisms now documented.
- **WP06 FR** (Privacy, v1.2.0 → v1.3.0): audit checklist enriched with runnable shell commands. Added WASM MCP sandboxing and the June `/bug` command refactor clarification (no scrubbing before submission).
- **WP08 FR** (Agent Teams, v1.4.0 → v1.5.0): new "Patterns d'Orchestration Avancés" section adapting the guide's 7 advanced patterns (Hub-and-Spoke, Programmatic Prerequisites, Dynamic Subagent Selection, Research Space Partitioning, Crash Recovery Manifest, Iterative Refinement Loop, Narrow Task Decomposition). Added 4 new IFTTD practitioner testimonials.
- **WP10 FR** (Budget IA, v1.2.0 → v1.2.1): referenced api-gateway.md in the cost-control and governance callouts.
- **WP11 FR** (Team Metrics, v1.0.1 → v1.1.0): new "Métriques Agentiques : Ce Que DORA Ne Mesure Pas" section (METR, DeputyDev, c-CRAB, Code Review Bench, Strata/Zenity studies), the self-hosted observability stack, and a PR Audit Trail reference.
- **WP12 FR** (Agent Engineering, v1.0.0 → v1.1.0): added the 4 missing subsections of "Evaluating Probabilistic Systems" and a reference to Claude Code's native `agent()/parallel()/pipeline()` orchestration primitives (dynamic-workflows.md).

---

## [2026-06-10] v3.40.0: WP11 FR frontmatter sync

### Fixed
- **WP11 FR** (Piloter une Équipe): version bumped from 3.38.3 to 3.40.0 to match EN counterpart. Date aligned to 2026-05-12. wp-version bumped to 1.0.1 (patch: metadata correction). Bodies confirmed identical via full content comparison — no translation work needed.

---

## [2026-05-21] v3.41.0 — Whitepaper 12 Agent Engineering (initial release)

### Added
- **WP12 FR/EN** (Agent Engineering): initial release v1.0.0. 7 sections, ~700 lines FR+EN. Public : tech leads et ingénieurs seniors. Angle : J-curve L2-L3, architecture harness (9 composants, 3 propriétés arXiv 2605.18747), CI/CD agentic productisé (c-CRAB 32.1%, GitHub Agentic Workflows, AWS Bedrock AgentCore, GitLab Duo), spec-driven development (Spec Kit vs Tessl, spec drift), évaluation (CovQValue, TOGLL, creator-neq-verifier), gouvernance HITL (93% Anthropic). Distingue rigoureusement données RCT (METR arXiv 2507.09089, n=16) des estimations practitioner. Attribution L0-L5 : Dan Shapiro/Glowforge/factorydark.com.
- **Fiche mémo WP12 FR** (`whitepapers/fr/fiches/fiche-12-agent-engineering.qmd`): 5 points + 4 actions. Format Typst `#fiche-recap`. EN non créée (dossier fiches/en inexistant).

---

## [2026-05-19] v3.41.0 — Skills-Commands Merger Update (CC 2.1.3)

### Changed
- **WP02 FR/EN** (Personnalisation/Customization): 3-way Agent/Skill/Command table unified to 2-way Agent/Skill model. Chapter "Commands" renamed to "Skills User-Invocables". All `.claude/commands/` paths updated to `.claude/skills/` with `disable-model-invocation: true`. wp-version bumped to 1.4.0.
- **WP04 FR/EN** (Architecture): Decision tree updated (`.claude/commands/` → `.claude/skills/` + `disable-model-invocation: true`). Extension comparison row updated with user/model invocation distinction.
- **WP07 FR/EN** (Guide Référence): Chapter 5 title stripped of ", Commands". Comparison table updated to user-invocable/model-invocable/agent structure. Anatomy section renamed. Directory tree updated.
- **Recap cards c04 FR/EN**: Full rewrite — title "Skills, Plugins & Agents", 4-row table with Skill (user)/Skill (auto)/Plugin/Agent.
- **Recap cards m09 FR/EN**: Reframed as "User-Invocable Skills". CC 2.1.3 callout added. `.claude/commands/` → `.claude/skills/`.
- **Recap cards m10 FR/EN**: "Invocation Modes" table added. Version bumped.
- **Recap cards 01-commandes-essentielles FR/EN**: Minor path update. Version bumped to 3.41.0.

---

## Fiches Mémo (Recap Cards)

Fiches A4 1-page imprimables. Versionnement global par série (pas par fiche individuelle).

**Sources** : `whitepapers/recap-cards/fr/*.qmd`
**Extension** : `recap-card-typst` (palette Bold Guy, 2 colonnes, marges 1.2cm)

### Série FR complète

#### v1.1.0 — 2026-04-01 (guide v3.38.1)

Mise à jour de contenu sur 5 fiches prioritaires (FR + EN) :

- **m16** — Nouvelle section "Guardrails (v3.38.0)" : `MAX_ITERATIONS=8`, Dedicated Reviewer (Opus 4.6 read-only, 1:4 ratio), token budget par agent avec pause à 85%
- **m17** — Nouvelle section "Récupération itérative (v3.38.0)" : pattern WHY/WHAT, budget de 3 cycles max avant escalade à l'orchestrateur
- **c04** — `effort: low|medium|high` dans le frontmatter Skills (v3.37.3+), `${CLAUDE_PLUGIN_DATA}` dans la section Plugins
- **t15** — Note `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` (v2.1.78+) : scrub automatique des variables sensibles avant transmission aux sous-processus MCP
- **t16** — `sandbox.failIfUnavailable: true` (v2.1.78+) dans le bloc JSON de configuration

#### v1.0.0 — 2026-03-17 (guide v3.37.0)

Série FR complète — 57 fiches en 3 séries :

- **Technique (T01-T22)** — 22 fiches : commandes, configuration, outils, MCP, sandbox, tokens
- **Méthodologie (M01-M22)** — 22 fiches : workflows, agents, hooks, CI/CD, debug, observabilité
- **Conception (C01-C13)** — 13 fiches : mental models, prompting, sécurité, mémoire, traceability

Toutes les fiches respectent la contrainte 1 page A4 stricte (vérifiée via `pdfinfo`).

---

## Ebooks de la série principale

### Mise à jour campagne — 2026-04-01 (guide v3.38.1)

Tous les ebooks 00-09 mis à jour de v3.27.6 → v3.38.1. Résumé des wp-version après campagne :

| WP | Titre | wp-version |
|----|-------|-----------|
| 00 | Intro série | 1.3.0 |
| 01 | Prompts efficaces | 1.1.0 |
| 02 | Personnalisation | 1.1.0 |
| 03 | Sécurité | 1.2.0 |
| 04 | Architecture | 1.1.0 |
| 05 | Équipe | 1.3.0 |
| 06 | Privacy | 1.1.0 |
| 07 | Guide référence | 1.2.0 |
| 08 | Agent teams | 1.3.0 |
| 09 | Apprendre avec l'IA | 1.2.0 |
| 10 | Budget IA | 1.2.0 (inchangé) |

Détail des changements par ebook : voir `CHANGELOG.md` principal (section [Unreleased]).

---

### 10 — Budget IA / AI Budget

**FR** : `whitepapers/fr/10-budget-ia.qmd`
**EN** : `whitepapers/en/10-ai-budget.qmd`

#### v1.2.0 — 2026-03-17 (guide v3.36.0)

Retours Marc Sélince (DAF/finance background) — 6 corrections FR+EN :

- **Section DAF/CFO** : placeholder callout remplacé par une vraie section `## Pour le DAF/CFO` avec argument ROI mesurable (bugs prod, onboarding) et framing OpEx/CapEx explicite (pas d'amortissement, déductible immédiatement)
- **Freins COMEX** : nouvelle section `## Freins COMEX au-delà du coût` dans le Q&A (après Budget & Procurement) — 3 objections non financières avec réponses factuelles : dépendance fournisseurs US, risque IP/espionnage industriel, hausse de prix future (lock-in pricing)
- **§3.1 Rétention** : reframé "Attraction et rétention des top performers" — le marché est tendu pour les seniors/experts, pas tous les profils ; distinction dev mid vs senior avec 3 offres dans les 48h
- **§3.2 CTO** : nouveau sous-point "Le ROI des heures d'ingénieur" — LLMs sur le code mécanique (tests, boilerplate, CRUD) libèrent du temps d'ingé pour l'architecture et l'investigation
- **§4.1 Budget** : option 4 ajoutée (remplacer un outil payant par un équivalent open source pour financer le pilote à coût net zéro) ; "200-500$/mois" retiré du budget discrétionnaire (trop variable selon les orgs)

#### v1.1.0 — 2026-03-17 (guide v3.36.0)

Corrections v2 — retours relecteurs (Mat, Marc, Anthony) :
- Fix ratio Cursor Pro/Claude Max : plage ~1,5-3% (Claude Max) et ~0,15-0,3% (Cursor Pro) au lieu de valeurs ponctuelles — FR+EN
- Fusion de la courbe d'apprentissage dupliquée en une seule section structurée (Phases 1/2/3)
- Source BCG 2025 précisée avec titre indicatif
- Note temporelle ajoutée sur les tarifs ("constatés en mars 2026")
- "Des équipes de 5-10 personnes... en 2020" → reformulé sans date précise ni chiffre non sourcé
- Executive summary ajouté (5 indicateurs clés + recommandation pilote)
- Message clé "augmentation > outil" remonté en tête de document
- Section "Au-delà des équipes tech" développée avec 3 use cases concrets (analyste, account manager, support L2)
- Références section 9 (prompt repo) et section 6 (augmentation) ajoutées en entrée
- Callout placeholder CFO/DAF ajouté (amortissement, OpEx vs CapEx)
- Callout placeholder change management ajouté

#### v1.0.0 — 2026-03-04 (guide v3.30.0)

Publication initiale avec système de versioning ebook.

**Contenu enrichi dans cette version (par rapport à la version non-versionnée) :**

Round 1 — Feedback terrain (Samuel Retiere, responsable adoption IA 50+ devs) :
- Piège framing headcount : encadré warning callout sur la comparaison workforce
- Rétention chiffrée : coût de remplacement d'un dev senior (6-12 mois salaire, calcul explicite)
- Watch point gains anecdotiques + fatigue mentale post-pic IA
- "Le ratio qui tue" : Claude Max = ~1,6% du coût mensuel d'un dev chargé
- Seuils enterprise à anticiper dans le Q&A budget
- Q&A "on arrive en cours d'année" : 3 approches concrètes (réallocation, budget discrétionnaire, argument de taille)
- PR merge rate/dev/jour comme métrique directionnelle (avec caveats : seuil 50 devs, PR size variance)
- Point hebdo du pilote reframé sur frictions techniques, pas ressenti qualitatif
- Section "Du pilote au déploiement" avec tableau rollout par cohortes (5→15→30)
- Attribution retour terrain dans les sources

Round 2 — Refonte framing stratégique :
- Audience map CEO/CTO/CIO selon taille d'organisation (encadré intro)
- Section CEO restructurée : TTM + données AI-native (BCG 47% vs 13%) + fenêtre stratégique
- Arguments financiers absorbés dans CEO, section CFO supprimée
- Nouvelle section "Au-delà des équipes tech" (agents métier, co-développement tech/business)
- Nouvelle section "L'IA comme augmentation, pas comme outil" (intuition de contextualisation, dev mini-CTO)
- Courbe d'apprentissage en 3 phases dans CTO (terrain/observationnel, plateau de 10%)
- Encadré TCO : lock-in vendor, API unbounded, hypothèse ×2 en scénario prudent

---

### 00 — Introduction de la série / Series Introduction

**FR** : `whitepapers/fr/00-introduction-serie.qmd`
**EN** : `whitepapers/en/00-series-introduction.qmd`

#### v1.2.0 — 2026-03-17 (guide v3.36.0)

Mise à jour contenu guide v3.36.0 :
- Fenêtre contexte 1M tokens : corrigée "beta" → GA (v2.1.75, mars 2026) — FR+EN
- Tableau de 7 nouvelles features majeures ajouté : Tasks API (v2.1.16), Auto-memories (v2.1.32), Agent Teams (v2.1.32), LSP Tool (v2.0.74), Remote Control (v2.1.51), MCP Elicitation (v2.1.76), contexte 1M GA — FR+EN

#### v1.1.0 — 2026-03-17 (guide v3.36.0)

Corrections v2 — retours relecteurs (Marc, Anthony) :
- npm : "déprécié" → "non recommandé" — FR+EN
- EN : installeur natif (`curl | sh`) ajouté comme méthode recommandée principale
- Fenêtre de contexte clarifiée : 200K par défaut (session standard), 1M par teammate dans les agent teams — FR+EN
- Tableau "Personnalisable" reformulé en phrase complète — FR
- `/init` ajouté dans la liste des 8 commandes essentielles — EN

#### v1.0.0 — 2026-03-04 (guide v3.27.6)

Baseline versioning établi.

---

### 01 — Prompts Efficaces / Effective Prompts

**FR** : `whitepapers/fr/01-prompts-efficaces.qmd`
**EN** : `whitepapers/en/01-effective-prompts.qmd`

#### v1.0.0 — 2026-03-04 (guide v3.27.6)

Baseline versioning établi.

---

### 02 — Personnalisation / Customization

**FR** : `whitepapers/fr/02-personnalisation.qmd`
**EN** : `whitepapers/en/02-customization.qmd`

#### v1.1.0 — 2026-03-17 (guide v3.36.0)

Corrections v2 — retours relecteurs (Edouard, Mat, Nicolas) :
- Restauration des accents sur ~10 passages — FR
- Anglicismes : "on-demand" → "à la demande", "per-project" → "par projet", "Memories" → "mémoires", "Feature opt-in" → "fonctionnalité opt-in" — FR

#### v1.0.0 — 2026-03-04 (guide v3.27.6)

Baseline versioning établi.

---

### 03 — Sécurité / Security

**FR** : `whitepapers/fr/03-securite.qmd`
**EN** : `whitepapers/en/03-security.qmd`

#### v1.1.0 — 2026-03-17 (guide v3.36.0)

Mise à jour contenu guide v3.36.0 :
- Callout warning ajouté : security fix v2.1.77 — hooks `PreToolUse` retournant `"allow"` contournaient les règles enterprise `deny` ; retourner `"continue"` à la place — FR+EN
- Paramètre sandbox `allowRead` ajouté (v2.1.77) : chemins en lecture seule sans accès écriture — FR+EN

#### v1.0.0 — 2026-03-04 (guide v3.27.6)

Baseline versioning établi.

---

### 04 — Architecture

**FR** : `whitepapers/fr/04-architecture.qmd`
**EN** : `whitepapers/en/04-architecture.qmd`

#### v1.0.0 — 2026-03-04 (guide v3.27.6)

Baseline versioning établi.

---

### 05 — Équipe / Team

**FR** : `whitepapers/fr/05-equipe.qmd`
**EN** : `whitepapers/en/05-team.qmd`

#### v1.2.0 — 2026-03-17 (guide v3.36.0)

Mise à jour contenu guide v3.36.0 :
- Section "Code Review natif" ajoutée (Research Preview, Teams/Enterprise) : architecture multi-agents, 3 modes de déclenchement, `REVIEW.md`, tarification $15-25/PR — FR+EN

#### v1.1.0 — 2026-03-17 (guide v3.36.0)

Corrections v2 — retours relecteurs (Nicolas, Marc) :
- "Multiple Claude instances... codebase partagee" → phrase complète avec sujet et verbe — FR+EN
- "Turnkey Quickstart" expliqué (démarrage rapide clé en main) — FR+EN
- "user-level et project-level" → traduction ajoutée entre parenthèses — FR
- Correction résidu FR ("OUI →") dans le fichier EN

#### v1.0.0 — 2026-03-04 (guide v3.27.6)

Baseline versioning établi.

---

### 06 — Privacy

**FR** : `whitepapers/fr/06-privacy.qmd`
**EN** : `whitepapers/en/06-privacy.qmd`

#### v1.0.0 — 2026-03-04 (guide v3.27.6)

Baseline versioning établi.

---

### 07 — Guide de Référence / Reference Guide

**FR** : `whitepapers/fr/07-guide-reference.qmd`
**EN** : `whitepapers/en/07-reference-guide.qmd`

#### v1.1.0 — 2026-03-17 (guide v3.36.0)

Mise à jour contenu guide v3.27.6 → v3.36.0 :
- 12 nouvelles commandes slash ajoutées : `/loop`, `/simplify`, `/batch`, `/stats`, `/rename`, `/copy`, `/effort`, `/branch` (remplace `/fork`), `/btw`, `/voice`, `/remote-control`/`/rc`, `/mobile`, `/fast` — FR+EN
- 7 nouveaux événements hook : `Elicitation`, `ElicitationResult`, `PostCompact`, `WorktreeCreate`, `WorktreeRemove`, `TeammateIdle`, `TaskCompleted` — FR+EN
- Flags CLI étendus : `-n`/`--name`, `--worktree`/`-w`, `--tools`, `--max-budget-usd`, `--add-dir`, `worktree.sparsePaths` — FR+EN
- Fenêtre contexte 1M tokens : corrigée "beta" → GA (v2.1.75, mars 2026) — FR+EN
- Section Remote Control ajoutée (v2.1.51, Pro/Max, Research Preview) — FR+EN

#### v1.0.0 — 2026-03-04 (guide v3.27.6)

Baseline versioning établi.

---

### 08 — Agent Teams

**FR** : `whitepapers/fr/08-agent-teams.qmd`
**EN** : `whitepapers/en/08-agent-teams.qmd`

#### v1.2.0 — 2026-03-17 (guide v3.36.0)

Mise à jour contenu guide v3.36.0 :
- Pattern "dérive d'identité après compaction" ajouté dans la section Context Isolation : hook `UserPromptSubmit` qui ré-injecte `.claude/agent-identity.txt` via `additionalContext` — FR+EN

#### v1.1.0 — 2026-03-17 (guide v3.36.0)

Corrections v2 — retours relecteurs (Emmanuel) :
- Restauration massive des accents sur 977 lignes FR (~200+ corrections)
- "C'est la seule définition de cette valeur dans ce document" → supprimé (FR+EN)
- "chez dans une fintech" → "chez une fintech" — FR+EN
- Clarification que les agent teams diffèrent des sub-agents par la communication bilatérale P2P et les outils de coordination (pas l'isolation de contexte, commune aux deux) — FR+EN
- Ajout note "Un agent Claude Code solo est un agent autonome complet, pas un chatbot" — FR+EN
- "~30K lignes de code" → "~30K lignes de code (environ 1M tokens)" — FR+EN
- "Fusion continue" → reformulé: changes committed, pulled et pushed automatiquement — FR+EN
- Note ajoutée: tmux est un outil externe, pas une fonctionnalité native Claude Code — FR+EN

#### v1.0.0 — 2026-03-04 (guide v3.27.6)

Baseline versioning établi.

---

### 09 — Apprendre avec l'IA / Learning with AI

**FR** : `whitepapers/fr/09-apprendre-avec-ia.qmd`
**EN** : `whitepapers/en/09-learning-with-ai.qmd`

#### v1.1.0 — 2026-03-17 (guide v3.36.0)

Mise à jour contenu guide v3.36.0 :
- Section "Inversion du bottleneck de review" ajoutée : les juniors génèrent du code plus vite que les seniors ne peuvent l'auditer — FR+EN
- Section "Exposition réglementaire" ajoutée (tech leads/managers) : EU AI Act (GPAI août 2025, high-risk août 2026) + FDA AI/ML Guidance (jan/juin 2025) — FR+EN

#### v1.0.0 — 2026-03-04 (guide v3.27.6)

Baseline versioning établi.

---

### 11 — Métriques d'Équipe / Team Metrics

**FR** : `whitepapers/fr/11-team-metrics.qmd`
**EN** : `whitepapers/en/11-team-metrics.qmd`

#### v1.0.0 — 2026-04-04 (guide v3.38.3)

Publication initiale.

---

### 12 — Ingénierie d'Agents / Agent Engineering

**FR** : `whitepapers/fr/12-agent-engineering.qmd`
**EN** : `whitepapers/en/12-agent-engineering.qmd`

#### v1.0.0 — 2026-05-21 (guide v3.41.0)

Publication initiale. 7 sections (J-curve L2-L3, harness, CI/CD agentic, SDD, évaluation/observabilité, gouvernance HITL, évolution des rôles). Attribution Shapiro Scale : Dan Shapiro/Glowforge/factorydark.com. Fiche récap FR incluse.

---

### Cheatsheet

**FR** : `whitepapers/fr/cheatsheet.qmd`
**EN** : `whitepapers/en/cheatsheet.qmd`

#### v1.0.0 — 2026-03-04 (guide v3.29.2)

Baseline versioning établi.

---

## Ebooks custom / client

> Ces ebooks suivent leur propre cycle de version, indépendant de la série principale.

### StrangeBee

**Whitepaper** : `whitepapers/fr/strangebee-whitepaper.qmd`
**Cheatsheet** : `whitepapers/fr/strangebee-cheatsheet.qmd`

#### v1.0.0 — 2026-03-04 (guide v3.29.2)

Baseline versioning établi.

---

### Purchasely

**Whitepaper** : `whitepapers/fr/purchasely-whitepaper.qmd`
**Cheatsheet** : `whitepapers/fr/purchasely-cheatsheet.qmd`

#### v1.0.0 — 2026-03-04 (guide v3.29.2)

Baseline versioning établi.

---

### DevWithAI Cheatsheet

**FR** : `whitepapers/fr/devwithai-cheatsheet.qmd`

#### v1.0 — 2026-03-04

Baseline versioning établi.

---

## Comment mettre à jour ce changelog

Quand tu modifies un ebook :

1. Bumper le `wp-version` dans le frontmatter du fichier `.qmd` concerné
2. Ajouter une entrée dans ce fichier sous l'ebook concerné
3. Format de l'entrée :

```markdown
#### vX.Y.Z — YYYY-MM-DD (guide vX.Y.Z)

Description des changements (bullets si plusieurs).
```

4. Rebuilder le PDF : `cd whitepapers/fr && quarto render XX-nom.qmd --to whitepaper-typst`
