# Évaluation de Ressource: Spec-Kitty

**URL**: https://github.com/Priivacy-ai/spec-kitty
**Type**: GitHub repository
**Date d'évaluation**: 2026-07-08
**Évaluateur**: Claude Code Ultimate Guide Team
**Version guide**: 3.40.0

---

## 📄 Résumé du contenu

- **Spec-Driven Development avec isolation d'exécution**: chaque work package s'exécute dans son propre git worktree, éliminant le chaos de branches lors de build parallèles
- **Boucle explicite de gouvernance**: `next → review → accept → merge`, avec commandes dédiées
- **Dashboard kanban local**: état de mission versionné dans le repo (specs, plans, work packages, critères d'acceptation, état de review, décisions de merge)
- **Positionnement explicite anti-boîte-noire**: la doc affirme "not a lights-out black box by default", soit humain définit intention/architecture/critères d'acceptation, agents implémentent dans des worktrees traçables, reviewers accept/reject/merge avec audit trail
- **Compatible** Claude Code, Codex, Cursor, Gemini, Copilot, OpenCode, Kiro et autres

---

## 🎯 Score de pertinence: 3/5

| Score | Signification |
|-------|---------------|
| ~~5~~ | ~~Critique, gap majeur dans le guide~~ |
| ~~4~~ | ~~Très pertinent - Amélioration significative~~ |
| **3** | **Pertinent - Complément utile** |
| ~~2~~ | ~~Marginal - Info secondaire / Redondant~~ |
| ~~1~~ | ~~Hors scope - Non pertinent~~ |

**Justification**: c'est l'implémentation open source la plus proche du pattern "isolation par worktree + gates de review + audit trail" décrit dans le talk WeScale/Maleus (juillet 2026), mais l'adoption reste modeste (1 397 stars, now 1,449 as of 2026-07-28, 120 forks) comparée à Spec Kit (118 688 stars) ou BMAD-METHOD (50 215 stars) déjà couverts ou en cours d'intégration. Utile en complément, pas urgent.

---

## ⚖️ Comparatif détaillé

| Aspect | Spec-Kitty | GitHub Spec Kit (déjà couvert) | BMAD-METHOD (évaluation séparée) |
|--------|------------|----------------------------------|-------------------------------------|
| Isolation d'exécution parallèle | ✅ Git worktree natif | ❌ Non | ❌ Non |
| Dashboard kanban | ✅ Local, versionné | ❌ | ❌ |
| Gate humain avant code | ✅ (via specs/plans) | ✅ (`/speckit.plan`) | ✅ (PRD + Architecture) |
| Audit trail merge | ✅ Explicite | ⚠️ Implicite (fichiers `.specify/`) | ❌ |
| Adoption (stars) | 1 397 | 118 688 | 50 215 |
| Maturité | Récente, communauté petite | Standard de facto | Établi |

---

## 📍 Recommandations

**Où intégrer**: `guide/workflows/spec-first.md`, section "Integration with Tools", en mention courte après le bloc BMAD-METHOD, présentée comme "si vous voulez en plus l'isolation d'exécution parallèle par worktree avec dashboard kanban, spec-kitty implémente ce pattern spécifique". Pas de section dédiée complète vu l'adoption encore limitée.

**Format suggéré**: 3-4 lignes + commande d'installation, pas de tableau comparatif complet (réservé aux outils avec adoption prouvée).

---

## 🔥 Challenge

**Objection testée**: "1 397 stars sur un outil créé récemment, n'est-ce pas trop tôt pour l'intégrer ?"

**Réponse**: Le seuil ne devrait pas être uniquement le nombre d'étoiles mais l'unicité du pattern. Spec-Kitty est le seul projet identifié dans cette recherche qui combine isolation d'exécution + kanban + audit trail en un seul outil léger MIT. Les alternatives plus populaires (Spec Kit, BMAD) ne couvrent pas cette combinaison spécifique. Une mention courte (pas une section complète) est le bon dosage : signale l'existence du pattern sans sur-pondérer un outil à l'adoption encore incertaine.

**Risque de non-intégration**: faible. Le concept d'isolation par worktree est déjà documenté ailleurs dans le guide (`guide/security/sandbox-isolation.md`, git worktrees natifs de Claude Code), spec-kitty n'est qu'une implémentation packagée parmi d'autres possibles.

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source/Commentaire |
|-------------|----------|---------------------|
| 1 397 stars, 120 forks | ✅ | Vérifié via `gh api repos/Priivacy-ai/spec-kitty` le 2026-07-08 |
| License MIT | ✅ | Confirmé par l'API GitHub (`license.spdx_id: MIT`) |
| Push le plus récent | ✅ | 2026-07-08, actif |
| Boucle next→review→accept→merge | ⚠️ Non testé en pratique | Repris de la documentation du projet (spec-driven.md), non vérifié par usage réel |

---

## 🎯 Décision finale

| Critère | Valeur |
|---------|--------|
| **Score final** | 3/5 |
| **Action** | ✅ Mention courte dans `spec-first.md` (pas de section dédiée) |
| **Confiance** | Moyenne (pattern confirmé unique, adoption réelle non prouvée à grande échelle) |
| **Révision suggérée** | Dans 3-6 mois si adoption croît significativement (repasser à 4/5 si >5K stars) |

---

*Rapport généré manuellement pour Claude Code Ultimate Guide v3.40.0*
