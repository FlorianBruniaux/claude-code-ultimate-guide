# Resource Evaluation: Spec-to-Code Factory

**Resource**: https://github.com/SylvainChabaud/spec-to-code-factory
**LinkedIn**: https://www.linkedin.com/posts/sylvain-chabaud-831415aa_ia-claudecode-ai-activity-7430257228928163840-jOxD
**Author**: Sylvain Chabaud (Ingénieur & formateur — WEB, Système embarqué)
**Published**: 2026-01 (repo ~4 weeks old at evaluation time)
**Evaluation Date**: 2026-02-19
**Evaluator**: Claude Code Ultimate Guide Team
**Score**: **3/5** (Pertinent — Mention ciblée)

---

## Summary

Pipeline multi-agents open-source entièrement construit sur Claude Code, qui transforme un `requirements.md` en projet livrable via 4 phases séquentielles et 6 gates de validation outillées.

**Points clés :**
- Méthodologie **BREAK → MODEL → ACT → DEBRIEF** avec 6 gates (Gate 0-5)
- Deux invariants absolus vérifiés automatiquement : "No Spec, No Code" et "No Task, No Commit"
- Chaîne de traçabilité complète : `COMMIT → TASK → US → EPIC → BRIEF`
- Budget token transparent par phase : ~900K total (BREAK 70K, MODEL 100K, PLAN 120K, BUILD 500K+, DEBRIEF 80K)
- Repo clonable : implémentation référence concrète (pas juste une documentation)

**Limites notables :**
- Jeune (22 commits, 8 stars) — pas encore validé en production à large échelle
- JavaScript uniquement (Clean Architecture React)
- Overhead massif (~900K tokens/projet) — adapté aux projets greenfield importants

---

## Scoring Breakdown

### 1. Relevance to Claude Code (5/5)

✅ **Entièrement construit sur Claude Code** : Skills orchestrant les phases, hooks validant les invariants, agents spécialisés par rôle
✅ **Patterns directs** : Utilise skills + hooks + agents exactement comme le guide les documente
✅ **Implémentation référence** : Repo clonable illustrant les concepts du guide en situation réelle

### 2. Technical Accuracy (4/5)

✅ **Phases vérifiées** : BREAK→MODEL→ACT→DEBRIEF confirmées dans le README
✅ **Gates vérifiées** : Gate 0-5 via scripts Node.js (requirements, structure, secrets/PII, planning, code quality, release)
✅ **Invariants réels** : Enforcement via tools/validate-commit-msg.js — pas juste des suggestions
⚠️ **Maturité limitée** : 4 semaines, architecture encore en évolution

### 3. Novelty/Uniqueness (3/5)

✅ **Enforcement outillé** : Scripts Node.js qui *bloquent* si gates non passées — pattern non documenté dans le guide
✅ **Budget token par phase** : Estimation concrète ~900K avec breakdown — unique dans l'écosystème
✅ **Traceability chain** : TASK→US→EPIC→BRIEF pas explicitement couverte dans le guide
⚠️ **Redondance ~80%** : spec-first.md (830 lignes), methodologies.md (Spec Kit/OpenSpec), agent-teams.md couvrent déjà l'essentiel

### 4. Practicality (3/5)

✅ **Clé en main** : Repo clonable, structure prête
⚠️ **Coût élevé** : ~900K tokens × $0.003 = ~$2.70/projet + maintenance hooks
⚠️ **JavaScript uniquement** : Clean Architecture React — pas polyglot
⚠️ **Complexité setup** : Git hooks + scripts Node.js à configurer

### 5. Source Credibility (3/5)

✅ **Présenté en public** : Talk à l'IA CAFE CLUB (Paris), validé par communauté
⚠️ **Adoption limitée** : 8 stars, 2 forks, 2 contributeurs (auteur + Claude)
⚠️ **Pas encore versionné** : 0 releases officielles

---

## Comparative Analysis

| Aspect | Spec-to-Code Factory | Notre Guide |
|--------|---------------------|-------------|
| **Spec-first workflow** | ✅ BREAK phase | ✅ spec-first.md (830 lignes) |
| **SDD greenfield** | ✅ Implémentation complète | ✅ Spec Kit (methodologies.md:366) |
| **Multi-agent orchestration** | ✅ 6 agents spécialisés | ✅ agent-teams.md |
| **Enforcement via hooks** | ✅ Scripts Node.js bloquants | ⚠️ Patterns seulement |
| **Traceability chain** | ✅ TASK→US→EPIC→BRIEF | ❌ Manquant |
| **Token budget par phase** | ✅ Breakdown transparent | ❌ Manquant |
| **Implémentation référence** | ✅ Repo clonable | ❌ Templates seulement |
| **Brownfield support** | ✅ V2+ mode | ✅ OpenSpec (methodologies.md:375) |

---

## Challenge (technical-writer agent)

**Verdict du challenge** : Score initial 4/5 → ramené à 3/5 justifié

**Principaux arguments du challenge :**
- Redondance à ~80% avec guide existant sous-estimée initialement
- "900K tokens" est un overhead non négligeable, pas un argument de vente
- Repo trop jeune (4 semaines) pour recommandation forte
- Enforcement via Git hooks side-car = gouvernance externe, pas native Claude Code

**Risques de non-intégration** : Faibles. La ressource est utile pour les devs cherchant une implémentation clé-en-main, mais le guide couvre les concepts fondamentaux.

---

## Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| BREAK → MODEL → ACT → DEBRIEF (4 phases) | ✅ | GitHub README (WebFetch) |
| 6 gates de validation (Gate 0-5) | ✅ | GitHub README |
| "No Spec, No Code" + "No Task, No Commit" | ✅ | GitHub README + LinkedIn post |
| ~900K tokens total estimé | ✅ | LinkedIn post (screenshot + tableau) |
| 8 stars / 22 commits | ✅ | GitHub (vérifié 2026-02-19) |
| JavaScript 100% | ✅ | GitHub (WebFetch) |
| Enforcement via Node.js scripts | ✅ | tools/validate-commit-msg.js mentionné dans README |

**Corrections apportées** : Aucune. "6 gates" (LinkedIn) correspond aux Gates 0-5 du README — cohérent numériquement.

---

## Decision

- **Score final** : **3/5** (Pertinent — Mention ciblée)
- **Action** : Mention dans `guide/methodologies.md` (tableau SDD Tools) + `guide/workflows/spec-first.md` (See Also)
- **Confiance** : Haute

**Intégration réalisée** :
1. `guide/methodologies.md` ligne ~365 : Ligne ajoutée dans le tableau SDD Tools
2. `guide/workflows/spec-first.md` section "See Also" : Lien + description ajoutés

**Révision recommandée** : Mai 2026 — vérifier adoption (stars, forks, issues), éventuellement upgrader à 4/5 si projet mature.

---

## Sources

**Primary**:
- [GitHub — spec-to-code-factory](https://github.com/SylvainChabaud/spec-to-code-factory)
- [LinkedIn post](https://www.linkedin.com/posts/sylvain-chabaud-831415aa_ia-claudecode-ai-activity-7430257228928163840-jOxD)

**Internal verification**:
- `guide/workflows/spec-first.md` (830 lignes — spec-first existant)
- `guide/methodologies.md` (SDD Tools section, ligne ~356)
- `guide/workflows/agent-teams.md`

**Challenge Agent** : technical-writer via Task tool (Explore subagent)

---

**Evaluation Methodology**: [docs/resource-evaluations/README.md](./README.md)
**Guide Version**: 3.27.8
**Integration Status**: ✅ Mention ciblée (2026-02-19)
