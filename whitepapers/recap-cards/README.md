# Recap Cards: Claude Code Ultimate Guide

Fiches mémo thématiques A4 une page, conçues pour être imprimées et gardées à portée. Chaque fiche couvre un concept précis du guide, avec commandes, tableaux et exemples concrets.

58 fiches par langue, organisées en 3 séries visuelles. Les sources QMD et les PDF A4 sont disponibles en FR et EN, y compris C14 Agent Harness Map.

**Langues & formats :**

| Format | FR | EN |
|--------|----|----|
| PDF (`recap-card-typst`) | 58 | 58 |
| EPUB / HTML | Non applicable | Non applicable |

## Build

```bash
# Une fiche
cd fr && quarto render t01-commandes-essentielles.qmd --to recap-card-typst

# Toute la série FR
cd .. && ./render-recap-cards.sh fr

# FR + EN
./render-recap-cards.sh all
```

Vérification des pages (doit retourner 1 partout) :

```bash
cd fr && for pdf in *.pdf; do echo "$pdf: $(pdfinfo "$pdf" | grep Pages | awk '{print $2}')"; done
```

## Stack technique

Extension Quarto dédiée `recap-card-typst` dans `../_extensions/recap-card/`. Palette Bold Guy (beige chaud + orange brûlé). Même stack que les whitepapers long-form.

---

## Série Technique — 22 fiches

Référence rapide. Commandes, configuration, outils, permissions.

| Fiche | Fichier | Titre | Difficulté |
|-------|---------|-------|------------|
| T01 | `01-commandes-essentielles.qmd` | Commandes Essentielles & Raccourcis | Beginner |
| T02 | `t02-mode-non-interactif.qmd` | Mode Non-Interactif & Headless | Intermediate |
| T03 | `03-permission-modes.qmd` | Permission Modes | Beginner |
| T04 | `t04-permissions-glob-patterns.qmd` | Permissions : Glob Patterns & Whitelist | Intermediate |
| T05 | `06-hierarchie-configuration.qmd` | Hiérarchie de Configuration | Beginner |
| T06 | `t06-settings-json.qmd` | Settings.json — Structure Complète | Intermediate |
| T07 | `t07-claudemd-best-practices.qmd` | CLAUDE.md Best Practices | Intermediate |
| T08 | `t08-auto-memories.qmd` | Auto-Memories — Quand et Comment | Intermediate |
| T09 | `t09-workspace-hygiene.qmd` | Workspace Hygiene & .claudeignore | Beginner |
| T10 | `t10-config-multi-machine.qmd` | Config Multi-Machine & Backup | Intermediate |
| T11 | `t11-search-tools-decision.qmd` | Search Tools Decision Tree | Intermediate |
| T12 | `t12-mcp-servers-overview.qmd` | MCP Servers Overview | Intermediate |
| T13 | `t13-context7-sequential.qmd` | Context7 & Sequential MCP | Intermediate |
| T14 | `t14-grepai-semantic-search.qmd` | Grepai — Recherche Sémantique | Intermediate |
| T15 | `t15-mcp-secrets-management.qmd` | MCP Secrets Management | Advanced |
| T16 | `t16-sandbox-natif-architecture.qmd` | Sandbox Natif — Architecture | Advanced |
| T17 | `t17-sandbox-natif-vs-docker.qmd` | Sandbox : Natif vs Docker | Advanced |
| T18 | `t18-modeles-thinking-modes.qmd` | Modèles & Thinking Modes | Beginner |
| T19 | `t19-context-window-200k-1m.qmd` | Context Window : 200K vs 1M | Intermediate |
| T20 | `t20-token-optimization.qmd` | Token Optimization | Intermediate |
| T21 | `t21-fast-mode-api.qmd` | Fast Mode & API Breaking Changes | Intermediate |
| T22 | `t22-third-party-tools.qmd` | Third-Party Tools | Intermediate |

---

## Série Méthodologie — 22 fiches

Comment travailler. Workflows, agents, CI/CD, debug.

| Fiche | Fichier | Titre | Difficulté |
|-------|---------|-------|------------|
| M01 | `m01-workflow-quotidien.qmd` | Workflow Quotidien | Beginner |
| M02 | `04-context-management.qmd` | Context Management | Beginner |
| M03 | `m03-sessions-continuité.qmd` | Sessions & Continuité | Intermediate |
| M04 | `m04-compact-vs-clear.qmd` | Compact vs Clear | Beginner |
| M05 | `m05-plan-mode.qmd` | Plan Mode | Intermediate |
| M06 | `m06-task-management-system.qmd` | Task Management System | Intermediate |
| M07 | `m07-todowrite-vs-tasks-api.qmd` | TodoWrite vs Tasks API | Intermediate |
| M08 | `m08-agents-custom.qmd` | Agents Custom | Intermediate |
| M09 | `m09-slash-commands.qmd` | Slash Commands | Intermediate |
| M10 | `m10-skills.qmd` | Skills | Intermediate |
| M11 | `m11-hooks-evenements-systeme.qmd` | Hooks : Événements & Système | Intermediate |
| M12 | `m12-hooks-patterns-concrets.qmd` | Hooks : Patterns Concrets | Intermediate |
| M13 | `m13-worktrees.qmd` | Worktrees | Advanced |
| M14 | `m14-plan-validate-execute.qmd` | Plan-Validate-Execute Pipeline | Advanced |
| M15 | `m15-tdd-bdd-sdd.qmd` | TDD / BDD / SDD Workflows | Intermediate |
| M16 | `m16-multi-agent-topologie.qmd` | Multi-Agent : Topologie & Orchestration | Advanced |
| M17 | `m17-multi-agent-communication-trust.qmd` | Multi-Agent : Communication & Trust | Advanced |
| M18 | `m18-event-driven-agents.qmd` | Event-Driven Agents | Advanced |
| M19 | `m19-github-actions.qmd` | GitHub Actions + Claude Code | Advanced |
| M20 | `m20-cicd-production.qmd` | CI/CD & Production Security | Advanced |
| M21 | `m21-debug-methodique.qmd` | Debug Méthodique | Intermediate |
| M22 | `m22-observabilite-jsonl.qmd` | Observabilité JSONL & jq | Advanced |

---

## Série Conception: 14 fiches

Comment penser et décider. Mental models, stratégie, sécurité par design.

| Fiche | Fichier | Titre | Difficulté |
|-------|---------|-------|------------|
| C01 | `c01-trust-calibration.qmd` | Trust Calibration & Mental Model | Beginner |
| C02 | `c02-prompting-basics.qmd` | Prompting Basics pour Claude Code | Beginner |
| C03 | `c03-xml-prompting-anchors.qmd` | XML Prompting & Semantic Anchors | Advanced |
| C04 | `c04-commands-skills-plugins-agents.qmd` | Commands vs Skills vs Plugins vs Agents | Intermediate |
| C05 | `c05-memory-stack.qmd` | Memory Stack (4 niveaux) | Intermediate |
| C06 | `c06-configuration-decision-guide.qmd` | Configuration Decision Guide | Intermediate |
| C07 | `c07-conventions-equipe-scale.qmd` | Conventions Équipe à Grande Échelle | Advanced |
| C08 | `c08-surface-attaque-menaces.qmd` | Surface d'Attaque & Menaces | Intermediate |
| C09 | `c09-prompt-injection-defenses.qmd` | Prompt Injection : Défenses | Intermediate |
| C10 | `c10-ai-traceability.qmd` | AI Traceability | Intermediate |
| C11 | `c11-subscription-vs-api-patterns.qmd` | Subscription vs API : Patterns de Coût | Intermediate |
| C12 | `c12-agent-sdk-integrations-ide.qmd` | Agent SDK & Intégrations IDE | Advanced |
| C13 | `25-erreurs-courantes.qmd` | Erreurs Courantes | Beginner |
| C14 | `c14-agent-harness-map.qmd` | Agent Harness Map | Advanced |

---

## Ajouter une fiche

1. Créer le fichier `.qmd` dans `fr/` avec le frontmatter suivant :

```yaml
---
title: "Titre"
subtitle: "Sous-titre"
card-number: "T23"
category: "Technique"
difficulty: "intermediate"
guide-version: "3.37.0"
author: "Florian BRUNIAUX"
version: "3.37.0"
date: "Mars 2026"
layout: "two-col"
lang: fr
format:
  recap-card-typst: default
---
```

2. Compiler : `cd fr && quarto render ma-fiche.qmd --to recap-card-typst`
3. Vérifier : `pdfinfo ma-fiche.pdf | grep Pages` doit retourner `1`
4. Mettre à jour ce README

## Contraintes de format

- 1 page A4 stricte (2 colonnes, marges 1.2cm)
- Code blocks : 6-7 lignes max
- Tables : 6-7 lignes de données max
- Prose : 2-4 phrases par paragraphe
- Pas de callouts Quarto, pas de divs spéciaux

## Fichiers de l'extension

```
../_extensions/recap-card/
  _extension.yml
  typst-template.typ    -> ../whitepaper/recap-card-template.typ (source)
  typst-show.typ        -> ../whitepaper/recap-card-show.typ (source)
```

Les sources canoniques sont dans `../_extensions/whitepaper/`. Mettre à jour les deux si modification.
