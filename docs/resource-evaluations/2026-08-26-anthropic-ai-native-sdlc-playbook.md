# Évaluation de Ressource: The AI-Native SDLC Playbook (Anthropic)

**URL**: https://claude.com/blog/the-ai-native-sdlc-playbook
**Type**: Article de blog officiel Anthropic
**Date d'évaluation**: 2026-08-26
**Évaluateur**: Claude Code Ultimate Guide Team
**Version guide**: voir `VERSION`

---

## 📄 Résumé du contenu

**Thèse**: le code n'est plus le goulot d'étranglement du développement logiciel (les agents IA en écrivent vite), donc c'est le cycle de vie entier qu'il faut refondre en boucle continue avec le jugement humain placé au-dessus, pas dans la boucle d'exécution.

**Boucle fermée à 6 étapes**, Claude au centre: `Plan → Design → Build → Test → Deploy → Maintain`. L'étape `Maintain` reboucle sur `Plan`: une anomalie détectée en production (seuil de monitoring dépassé) génère automatiquement un nouvel `intent.md`, sans qu'un humain ait à l'écrire, seulement à le valider.

**Chaîne de trois documents versionnés**, chacun avec son propre gate humain:
- `intent.md`: le problème en langage naturel, écrit et validé par le PM (auteur, contraintes, questions ouvertes)
- `spec.md`: la spec technique produite par Claude, contrainte par les Skills (politiques org sécurité/conformité), validée contre les contraintes métier
- `plan.md`: le plan d'implémentation détaillé (fichiers, ordonnancement, risques, preuves), approuvé avant génération de code

**Gates humains** à chaque étape: validation `intent.md`, validation `spec.md`, review de PR, autorisation de prod via hooks, triage des incidents autonomes.

**Contrôles techniques cités**: Skills (politiques versionnées), Hooks (barrières déterministes), CLAUDE.md (conventions du repo), continuous evals (suite de régression).

**Exemples concrets**: monitoring qui déclenche Claude automatiquement, Claude Tag dans Slack pour les incidents 24/7, revue de code IA qui détecte des vulnérabilités, déploiement autonome en dev mais autorisé en prod.

**KPIs proposés** (pas de chiffres absolus): temps jusqu'au premier commit `intent.md`, taux de PR passant du premier coup, réduction du taux d'anomalies échappées en prod.

---

## 🎯 Score de pertinence: 3/5

| Score | Signification |
|-------|---------------|
| ~~5~~ | ~~Critique, gap majeur dans le guide~~ |
| ~~4~~ | ~~Très pertinent - Amélioration significative~~ |
| **3** | **Pertinent - Complément utile** |
| ~~2~~ | ~~Marginal - Info secondaire / Redondant~~ |
| ~~1~~ | ~~Hors scope - Non pertinent~~ |

**Justification**: la majorité du contenu de l'article recouvre ce que le guide documente déjà ailleurs, en détail. `guide/workflows/spec-first.md` (avant modification, 1029 lignes) couvre déjà le pattern spec-avant-code, Spec Kit, OpenSpec, BMAD-METHOD et TDD. `docs/resource-evaluations/bmad-method-spec-driven-agents.md` a déjà intégré le principe d'agents-rôles (Analyst→PM→Architect) avant code. Les hooks comme barrières déterministes, la review de code par IA et CLAUDE.md comme mémoire du repo sont documentés ailleurs dans le guide. `docs/resource-evaluations/anthropic-2026-agentic-coding-trends.md` (rapport Anthropic de février, score 4/5) a déjà établi le précédent méthodologique pour ce type de source: autorité officielle élevée, mais overlap massif avec l'existant, donc diffusion ciblée plutôt que section dédiée.

Deux éléments du playbook n'ont pas d'équivalent direct dans le guide:
1. La décomposition en trois documents distincts `intent.md → spec.md → plan.md`, chacun avec son propre gate humain en amont du code. Le guide n'a que `spec.md`.
2. La boucle fermée `Maintain → Plan`: une anomalie de production qui génère automatiquement un nouvel `intent.md`, avant validation humaine.

C'est un score 3/5 et pas 4/5: le gap est réel mais localisé à deux ajouts dans un fichier existant, pas une section entière manquante comme l'était BMAD-METHOD.

---

## ⚖️ Comparatif

| Aspect | Playbook Anthropic | Guide actuel | Action |
|--------|--------------------|---------------|--------|
| Spec avant code | ✅ `spec.md` dans la chaîne | ✅ `guide/workflows/spec-first.md` en entier | Aucune, déjà couvert |
| Document d'intention en amont de la spec | ✅ `intent.md`, gate PM | ❌ Absent | ➕ Ajouter comme document optionnel avant `spec.md` |
| Plan d'implémentation distinct de la spec | ✅ `plan.md`, gate technique séparé | ⚠️ Implicite via `/speckit.plan` (Spec Kit), jamais nommé comme document autonome | ➕ Nommer `plan.md` comme document distinct |
| Agents-rôles multi-personas avant code | ✅ Mentionné en filigrane | ✅ BMAD-METHOD déjà intégré (score 4/5) | Aucune |
| Hooks comme barrières déterministes | ✅ Cité | ✅ Documenté ailleurs dans le guide | Aucune |
| Review de PR par IA | ✅ Cité | ✅ Documenté ailleurs dans le guide | Aucune |
| CLAUDE.md comme mémoire du repo | ✅ Cité | ✅ Déjà central au guide | Aucune |
| Boucle fermée `Maintain → Plan` | ✅ Anomalie prod → nouvel `intent.md` automatique | ❌ Le diagramme `06-development-workflows.md` s'arrête à `Merge ✓` | ➕ Fermer la boucle dans le diagramme Mermaid |
| Continuous evals comme garde-fou de régression | ✅ Cité | ✅ Couvert par la section evals existante | Aucune |
| KPIs (temps au premier `intent.md`, taux PR ok du premier coup) | ✅ Proposés, sans chiffres absolus | ❌ Non repris | Non retenu: aucun chiffre vérifiable, risque de citer un KPI vague sans valeur |

---

## 📍 Recommandations

**Où intégrer**: `guide/workflows/spec-first.md`, section "The Pattern" (mention de la chaîne à 3 documents) et nouvelle sous-section "With intent.md (Upstream Problem Statement)" dans "Integration with Tools", à côté de Spec Kit/OpenSpec/BMAD-METHOD. Le diagramme `guide/diagrams/06-development-workflows.md` (Spec-First Development Pipeline) est mis à jour pour faire apparaître `intent.md` avant `spec.md` et fermer la boucle avec une étape `Maintain` qui reboucle sur l'écriture d'un nouvel `intent.md`.

**Format retenu**: exemple concret de contenu `intent.md` (auteur, problème, contraintes, questions ouvertes, gate), pas de section monolithique dédiée à l'article. `plan.md` est mentionné comme document distinct, rattaché à `/speckit.plan` quand Spec Kit est utilisé, ou en fichier autonome sinon.

**Rejeté**: section dédiée `guide/workflows/ai-native-sdlc.md` ou équivalent. L'overlap avec `spec-first.md`, BMAD-METHOD et les sections hooks/CLAUDE.md existantes rendrait une section séparée redondante à 80%, le même verdict que celui déjà posé sur le rapport Anthropic de février 2026.

---

## 🔥 Challenge

**Objection testée**: "`intent.md` n'est-il pas juste une reformulation d'un ticket Jira ou d'une issue GitHub bien écrite ?"

**Réponse**: en partie, oui, le contenu (problème, contraintes, questions ouvertes) n'est pas nouveau. Ce qui est spécifique au pattern documenté par Anthropic est la place de `intent.md` dans une chaîne versionnée avec deux gates humains distincts en aval (spec, puis plan), et surtout la génération automatique de ce document par le système de monitoring quand `Maintain` détecte une anomalie, sans intervention humaine pour l'écriture initiale. C'est ce deuxième point, la boucle fermée, qui n'a pas d'équivalent dans le guide et justifie l'ajout au diagramme.

**Risque de non-intégration**: un lecteur qui vient de lire l'article Anthropic et cherche à savoir "comment ça se traduit concrètement avec Claude Code" ne trouve pas le fil entre `intent.md` et le `spec.md` déjà documenté dans le guide.

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Commentaire |
|-------------|----------|-------------|
| Boucle `Plan → Design → Build → Test → Deploy → Maintain` | ✅ | Structure confirmée dans l'article source |
| Chaîne `intent.md → spec.md → plan.md` avec gates distincts | ✅ | Confirmé dans l'article source |
| `Maintain` reboucle automatiquement sur `Plan` (nouvel `intent.md` sur anomalie) | ✅ | Confirmé dans l'article source |
| Skills utilisés comme politiques org versionnées contraignant `spec.md` | ✅ | Confirmé dans l'article source |
| KPIs cités (temps au premier commit `intent.md`, taux PR ok du premier coup, réduction anomalies prod) | ✅ | Confirmé dans l'article source, aucun chiffre absolu fourni, pas de vérification externe possible |

**Corrections apportées**: aucune, le résumé du contenu correspond à l'article source.

---

## 🎯 Décision finale

| Critère | Valeur |
|---------|--------|
| **Score final** | 3/5 |
| **Action** | ✅ Intégration ciblée sur deux gaps (`intent.md` en amont de `spec.md`, boucle fermée `Maintain → Plan` dans le diagramme), pas de section dédiée |
| **Fichiers modifiés** | `guide/workflows/spec-first.md`, `guide/diagrams/06-development-workflows.md`, `machine-readable/reference.yaml` |
| **Confiance** | Haute (source officielle Anthropic, gap vérifié par comparaison ligne à ligne avec le contenu existant de `spec-first.md`) |
| **Point de vigilance** | Ne pas laisser `intent.md` dupliquer le contenu déjà couvert sur `spec.md`, TDD ou BMAD-METHOD dans le même fichier |

---

*Rapport rédigé pour Claude Code Ultimate Guide*
