# Resource Evaluation #071 — Steven Ge: Claude Code for Technical Writing

**Source:** [LinkedIn Post](https://www.linkedin.com/posts/steven-ge-ab016947_i-started-using-claude-code-for-technical-activity-7432831185392816129-ARa8?utm_source=share&utm_medium=member_desktop&rcm=ACoAABGhhKgBLYdSS8KjqEyTSCUE4m21LrNR0_I)
**Author:** Steven Ge (14.6K followers, academic/technical writer and educator)
**Date:** 2026-02-26 (edited 2026-02-27)
**Engagement:** 177 likes, 15 comments
**Evaluated:** 2026-02-28
**Type:** LinkedIn post — 12-step workflow walkthrough

---

## 📄 Résumé du contenu

- Workflow de 12 étapes pour rédiger des manuscrits, rapports et matériaux pédagogiques avec Claude Code en traitant l'écriture comme un projet de code
- Stack complet: Claude Code + CLAUDE.md + GitHub + VS Code + Obsidian + Grammarly + Word
- Principe central: drafts en Markdown, version control Git, rendu Word en fin de processus — "Treat writing like a coding project"
- Philosophie de responsabilité humaine: "You become the architect. Your work is thinking, structuring, and revising. Claude is the assistant." Les sections critiques sont rédigées manuellement avant refinement par Claude
- Résultats déclarés: rapport technique, manuscrit et série de tutoriels complétés avec disclosure IA explicite dans toutes les publications
- **Fait notable**: utilise CLAUDE.md pour définir goals, scope et writing specifications du projet — usage d'une feature Claude Code spécifique

---

## 🎯 Score de pertinence

| Score | Signification |
|-------|---------------|
| 5 | Essentiel — Gap majeur dans le guide |
| 4 | Très pertinent — Amélioration significative |
| **3** | **Pertinent — Complément utile** |
| 2 | Marginal — Info secondaire |
| 1 | Hors scope — Non pertinent |

**Score final: 3/5**

**Justification:** Le workflow de Steven Ge a été initialement évalué à 2/5 (mauvais ciblage audience), mais le challenge a révélé deux éléments sous-estimés: (1) l'usage de CLAUDE.md est une feature Claude Code spécifique, ce qui ancre le workflow dans le CLI et pas seulement Claude.ai, et (2) les développeurs qui produisent de la documentation technique (ADR, API docs, whitepapers, READMEs, runbooks) constituent une sous-audience réelle non couverte par le guide actuel. Le workflow Git + Markdown + CLI est aligné avec la philosophie du guide. Aucune métrique d'efficacité quantifiée — le workflow reste "expérimental" selon l'auteur lui-même.

---

## ⚖️ Comparatif

| Aspect | Cette ressource | Notre guide |
|--------|----------------|-------------|
| CLAUDE.md pour projets writing | ✅ Workflow détaillé (goals, scope, specs) | ✅ Documenté en général, pas pour writing |
| Git + Markdown pour documentation | ✅ 12 étapes détaillées | ❌ Non couvert (coding projects uniquement) |
| Workflow "docs-as-code" pour devs | ✅ Applicable aux tech writers/leads | ❌ Absent du guide |
| Features avancées (MCP, hooks, agents) | ❌ Non utilisées | ✅ Extensivement couvert |
| Non-développeurs / knowledge workers | ✅ Cible principale | ➡️ Redirigé vers Cowork Guide |
| Métriques d'efficacité | ❌ Aucun chiffre vérifiable | ✅ Stats documentées avec sources |

---

## 📍 Recommandations

**Action: Intégration conditionnelle (score 3 = quand temps disponible)**

1. **Où documenter**: `guide/ultimate-guide.md` — section "Real-World Use Cases" ou "Workflows for Technical Writers"
2. **Comment intégrer**: Mention du workflow comme exemple de "docs-as-code" avec Claude Code, en insistant sur l'usage de CLAUDE.md pour les projets d'écriture. Ne pas reproduire les 12 étapes en détail (trop verbeux) — synthèse en 4-5 principes clés avec attribution et lien
3. **Angle d'intégration**: "Beyond Code: Using Claude Code for Technical Documentation" — pour les devs qui écrivent (docs produit, ADR, guides d'architecture)
4. **Priorité**: Basse — gap réel mais audience secondaire pour ce guide. À intégrer dans une prochaine passe sur les use cases non-traditionnels

**Ce qu'il ne faut PAS faire:**
- Ne pas créer une section dédiée à l'écriture académique (hors scope du guide)
- Ne pas présenter ce workflow comme applicable aux non-développeurs (c'est le rôle du Cowork Guide)

---

## 🔥 Challenge (technical-writer)

**Score initial proposé:** 2/5
**Score après challenge:** 3/5 ⬆️

**Points manqués dans l'évaluation initiale:**

1. **CLAUDE.md usage** — Élément clé ignoré initialement. L'auteur utilise CLAUDE.md pour définir project goals, scope, et writing specs. C'est une feature Claude Code CLI spécifique, pas remplaçable par Claude.ai
2. **Sous-audience "devs qui écrivent"** — Les développeurs produisent régulièrement de la documentation technique (ADR, API docs, whitepapers, runbooks). Ce workflow leur est directement applicable
3. **Git + Markdown alignment** — Le workflow s'aligne avec la philosophie du guide (Git workflows, version control, CLI-first)
4. **Erreur de scoring comparative** — La distinction "academic writer ≠ cible du guide" est vraie pour 90% du contenu, mais le workflow Git + CLAUDE.md dépasse cette catégorisation

**Risques de non-intégration:**
- Le guide rate la sous-audience "tech documentation writers" (DevOps, Engineering leads, Architects)
- Précédent: rejeter tout workflow writing-related sans analyser l'applicabilité réelle aux devs
- Gap: "docs-as-code avec Claude Code" n'est documenté nulle part dans le guide

**Critique brutale:**
> "Tu substitues 'audience' à 'applicabilité'. Steven cible des academic writers, mais son workflow Git + Markdown + CLAUDE.md est directement utilisable par des devs qui font de la documentation. La distinction est fine mais réelle."

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| Auteur: Steven Ge, academic/technical writer | ✅ | Profil LinkedIn |
| 14.6K followers | ✅ | Page LinkedIn |
| Date: 2026-02-26, édité 2026-02-27 | ✅ | Métadonnées post |
| 177 likes, 15 comments | ✅ | WebFetch direct |
| Stack: Claude Code + GitHub + VS Code + Obsidian + Grammarly + Word | ✅ | Contenu du post |
| Usage de CLAUDE.md pour writing specs | ✅ | WebFetch confirmé |
| 3 outputs complétés (rapport, manuscrit, tutoriels) | ✅ | Post, sans dates/délais précis |
| Aucun chiffre d'efficacité (%, x fois) | ✅ | Post dit "experimental", pas de benchmarks |
| MCP/hooks/agents/custom commands utilisés | ❌ Non mentionnés | WebFetch confirme absence |

**Corrections apportées:**
- Score initial 2/5 → 3/5 après discovery du CLAUDE.md usage et re-analyse audience
- Aucune hallucination de chiffres détectée — le post ne prétend pas à des gains d'efficacité quantifiés

---

## 🎯 Décision finale

- **Score final**: 3/5
- **Action**: Intégrer (priorité basse) — synthèse en 4-5 principes dans une section "docs-as-code" ou "beyond code workflows"
- **Confiance**: Haute (fact-check complet, sources vérifiées, pas de chiffres non vérifiables)
- **Audience cible dans le guide**: Développeurs qui produisent de la documentation technique, pas les academic writers en général