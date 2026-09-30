# Résumé hebdomadaire des releases et annonces Anthropic (16-23 janvier 2026)

**Période couverte :** 16 janvier - 23 janvier 2026
**Date d'évaluation :** 24 janvier 2026
**Évaluateur :** Claude Code Ultimate Guide

---

## Vue d'ensemble

Cette semaine a marqué des avancées significatives pour Anthropic, avec des déploiements majeurs d'outils produit et une publication de gouvernance AI de grande envergure.

---

## 1. Claude's Constitution – Révision majeure

**Date :** 21 janvier 2026
**Type :** Annonce / Document de gouvernance

### Highlights

- Publication d'une nouvelle constitution pour Claude, repositionnée comme document de gouvernance pour guider les comportements du modèle à travers toutes les versions futures
- Structure révisée passant de principes énumérés à une approche narrative détaillée expliquant le "pourquoi" derrière chaque directive, favorisant la généralisation plutôt que l'application mécanique de règles
- Quatre priorités hiérarchisées : sécurité générale → éthique large → conformité aux guidelines d'Anthropic → utilité genuine
- Document publié en libre accès (licence CC0 1.0), destiné à être versé à futurs modèles et mis à jour itérativement
- Sections clés : Helpfulness, Claude's Ethics, Anthropic's Guidelines, Being Broadly Safe, Claude's Nature (incluant réflexions sur la conscience potentielle de Claude)

### Sources

- https://www.anthropic.com/news/claude-new-constitution
- https://www-cdn.anthropic.com/f83650a21e480136866a3f504deb76e346f689d4/claudes-constitution.pdf
- https://techcrunch.com/2026/01/21/anthropic-revises-claudes-constitution-and-hints-at-chatbot-consciousness/

---

## 2. Claude Code – Mises à jour produit

**Dates :** 9-22 janvier 2026
**Type :** Releases produit
**Versions couvertes :** 2.1.9 à 2.1.17

### Features clés par version

**Version 2.1.17 (22 janvier)**
- Correction de crash sur processeurs sans support AVX

**Version 2.1.16 (22 janvier)**
- Système de gestion des tâches avec suivi des dépendances
- Gestion native des plugins VSCode
- Reprise des sessions OAuth distantes

**Version 2.1.15 (21 janvier)**
- Amélioration de performance UI avec React Compiler
- Dépréciation notifications pour npm install

**Version 2.1.14 (20 janvier)**
- Autocomplete bash historique avec syntaxe bang
- Recherche dans plugins
- Épinglage aux versions git spécifiques

**Version 2.1.9 (16 janvier)**
- Auto-seuil MCP configurable avec syntaxe auto:N
- Support PreToolUse hooks avancé
- Variable d'environnement CLAUDE_SESSION_ID

**Versions 2.1.6-2.1.7 (13-14 janvier)**
- Recherche config améliorée
- Statistiques filtrées stats 7/30 jours
- Attributs session URL pour commits et PRs

### Breaking changes

- **Dépréciation npm install** → Transition recommandée vers `claude install` ou installations natives
- **Migration URLs OAuth** → console.anthropic.com devient platform.claude.com
- **Suppression @-mention MCP** → Utiliser `/mcp enable <name>` à la place

### Améliorations sécurité/stabilité

- Correction vulnérabilité permissive sur règles wildcard dans commands shell
- Fix fuite mémoire tree-sitter et accumulation WASM sur sessions longues
- Correction command injection risk en parsing bash
- Augmentation timeout hooks d'outils : 60s → 10 minutes

### Sources

- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://www.gradually.ai/en/changelogs/claude-code/
- https://releasebot.io/updates/anthropic/claude-code

---

## 3. Cowork – Expansion du preview

**Dates :** 12 et 16 janvier 2026
**Type :** Feature release (research preview)

### Highlights

**12 janvier**
- Lancement du preview Cowork sur Claude Desktop (macOS uniquement) pour plans Max
- Apporte les capacités agentic de Claude Code au travail de connaissance non-codé via VM isolée locale

**16 janvier**
- Expansion du preview aux plans Pro sur Claude Desktop (macOS)
- Intégration MCP locale complète et accès aux fichiers locaux via machine virtuelle

### Sources

- https://support.claude.com/en/articles/12138966-release-notes
- https://fortune.com/2026/01/13/anthropic-claude-cowork-ai-agent-file-managing-threaten-startups/

---

## 4. Claude Desktop & Plans – Mises à jour d'accès

**Date :** 16 janvier 2026
**Type :** Mise à jour business/pricing

### Highlights

**Claude Code sur Team plans**
- Ajout de Claude Code à tous les sièges Standard des plans Team
- Démocratisation de l'accès aux outils de codage agentic

**Opus 4 et 4.1 dépréciés**
- Suppression des modèles Opus 4 et 4.1 des sélecteurs de modèles Claude et Claude Code
- Migration recommandée vers Opus 4.5 (performance améliorée à 1/3 du coût)

### Breaking changes

- Dépréciation totale Opus 4/4.1 – clients doivent basculer vers Opus 4.5 ou versions anciennes via External Researcher Access Program

### Sources

- https://support.claude.com/en/articles/12138966-release-notes

---

## 5. Claude Mobile – Santé & données

**Date :** 12 janvier 2026
**Type :** Feature release

### Highlights

**Health & Fitness Analytics**
- Claude peut désormais lire et analyser données de santé/fitness sur iOS et Android (plans Pro/Max, US uniquement)
- Génération native de graphiques d'insights sur tendances activité, sommeil, etc.
- Intégrations bêta : HealthEx, Function, Apple Health, Android Health Connect

**HIPAA-ready Enterprise Plans**
- Nouvelle option pour organisations souhaitant traiter protected health information (PHI)

### Sources

- https://support.claude.com/en/articles/12138966-release-notes

---

## 6. Anthropic SDK pour Python

**Dernière version stable :** v0.72.0 (28 octobre 2025)

**Remarque :** Aucune release Python SDK détectée cette semaine. Dernière version en date ajoute support context management (clearing thinking blocks).

### Sources

- https://github.com/anthropics/anthropic-sdk-python/releases

---

## Tableau récapitulatif des breaking changes

| Feature | Breaking Change | Migration |
|---------|-----------------|-----------|
| Claude Code npm | Dépréciation npm install | Utiliser claude install ou native installer |
| Opus 4 et 4.1 | Suppression sélecteurs modèles | Upgrader vers Opus 4.5 ou External Researcher Program |
| Console URLs | Migration console.anthropic.com | Utiliser platform.claude.com |
| MCP @-mention | Suppression @-mention MCP servers | Utiliser /mcp enable name |
| Bash permission rules | Wildcard matching stricte | Réviser rules selon documentation |
| Hooks timeout | 60s → 10 minutes | Scripts long-running tolèrent maintenant davantage |

---

## Ressources officielles

| Source | URL |
|--------|-----|
| Blog Anthropic News | https://www.anthropic.com/news |
| Claude Release Notes | https://support.claude.com/en/articles/12138966-release-notes |
| Claude Code GitHub | https://github.com/anthropics/claude-code |
| SDK Python GitHub | https://github.com/anthropics/anthropic-sdk-python |
| Changelog Claude Code | https://www.gradually.ai/en/changelogs/claude-code/ |
| API Docs Platform | https://platform.claude.com/docs/en/release-notes/overview |

---

## Verdict

Semaine dense centrée sur stabilité (fixes sécurité, mémoire), expansion produit (Cowork, health), et transparence gouvernance (Constitution Claude). Aucun breaking change critique mais attention requise sur dépréciations Opus 4/npm.
