# Évaluation de Ressource: GET SHIT DONE (GSD)

**URL**: https://github.com/glittercowboy/get-shit-done
**Type**: GitHub repository
**Date d'évaluation**: 2026-01-25
**Évaluateur**: Claude Code Ultimate Guide Team
**Version guide**: 3.12.0

---

## 📄 Résumé du contenu

- **Système de meta-prompting** pour Claude Code résolvant le "context rot" (dégradation qualité avec contexte accumulé)
- **Workflow en 6 phases**: Initialize → Discuss → Plan → Execute → Verify → Complete
- **Multi-agent orchestration**: Agents parallèles spécialisés (researchers, planners, executors, debuggers)
- **Documents structurés**: PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, PLAN.md
- **Fresh executor contexts**: Chaque plan s'exécute dans un contexte isolé de 200k tokens
- **Quick mode**: Fast-track pour tâches ad-hoc sans planification complète

---

## 🎯 Score de pertinence: 2/5

| Score | Signification |
|-------|---------------|
| ~~5~~ | ~~Essentiel - Gap majeur dans le guide~~ |
| ~~4~~ | ~~Très pertinent - Amélioration significative~~ |
| ~~3~~ | ~~Pertinent - Complément utile~~ |
| **2** | **Marginal - Info secondaire / Redondant** |
| ~~1~~ | ~~Hors scope - Non pertinent~~ |

**Justification**: Les concepts clés de GSD sont déjà couverts sous d'autres noms dans le guide:

| Concept GSD | Équivalent dans le guide | Emplacement |
|-------------|-------------------------|-------------|
| "Context rot" | Fresh Context Pattern | `guide/ultimate-guide.md:1547-1593` |
| "Fresh executor contexts" | Ralph Loop | `guide/ultimate-guide.md:1561` |
| Multi-agent orchestration | Gas Town, multiclaude | `guide/ecosystem/ai-ecosystem.md:816-890` |
| Workflow multi-phases | BMAD methodology | `guide/core/methodologies.md:44-55` |
| Documents structurés | CLAUDE.md + TodoWrite | Sections 3.4, 4.5 |

---

## ⚖️ Comparatif détaillé

| Aspect | GSD | Notre guide |
|--------|-----|-------------|
| Context rot / dégradation | ✅ Concept central | ✅ Couvert (Chroma research, 16K threshold) |
| Fresh context per task | ✅ "Fresh executor contexts" | ✅ Fresh Context Pattern + Ralph Loop |
| Multi-agent parallel | ✅ Researchers, planners, executors | ✅ Gas Town, multiclaude, Task subagents |
| Workflow phases | ✅ 6 phases spécifiques | ✅ BMAD (5 agents), TDD/SDD/BDD workflows |
| XML-structured plans | ✅ Nouveau format | ⚠️ Pas documenté (mais TodoWrite + Markdown) |
| State persistence | ✅ STATE.md pattern | ✅ Serena memory, CLAUDE.md |
| Quick mode for ad-hoc | ✅ Fast-track option | ❌ Non documenté explicitement |

**Delta réel**: XML formatting et "Quick mode" uniquement.

---

## 📍 Recommandations

### Option retenue: **Ne pas intégrer** (ou mention minimale)

**Raisons**:
1. **Overlap >90%** avec concepts existants
2. **Pas d'adoption mesurable significative** (7.5k stars, now 64,798 as of 2026-07-28, mais repo récent créé 2025-12-14, pas d'historique prouvé)
3. **Coût de maintenance** (liens morts, versions obsolètes)
4. **Le guide a déjà BMAD** pour multi-agent governance
5. **Claims non vérifiées** ("Trusted by Amazon, Google..." sans preuve)

**Si vraiment nécessaire** (mention minimale):
- **Où**: `guide/core/methodologies.md` Tier 1 (à côté de BMAD)
- **Format**: 1-2 lignes dans le tableau existant
- **Contenu suggéré**:
  ```markdown
  | **GSD** | Meta-prompting phases (6-stage workflow) | Solo devs, Claude Code | ⭐⭐ Similar to BMAD |
  ```

---

## 🔥 Challenge (technical-writer)

### Score ajusté
**2/5** (inchangé après challenge)

### Points manqués identifiés
- Maturité du projet non évaluée initialement (repo créé 2025-12-14)
- Delta précis BMAD vs GSD non explicité
- Coût d'intégration/maintenance ignoré

### Risques de non-intégration
**Négligeables**:
- Aucun utilisateur ne cherchera "GSD" dans le guide
- Concepts couverts sous d'autres noms
- Ajout possible ultérieur si popularité croît

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source/Commentaire |
|-------------|----------|-------------------|
| Auteur: TÂCHES (glittercowboy) | ⚠️ Partiel | Username = glittercowboy, "TÂCHES" = signature README non vérifiable |
| MIT License | ✅ | Badge visible + fichier LICENSE |
| "Trusted by Amazon, Google, Shopify, Webflow" | ⚠️ Non vérifiable | **Aucune preuve, témoignages ou liens fournis** |
| 6-stage workflow | ✅ | Confirmé: Initialize → Discuss → Plan → Execute → Verify → Complete |
| 7.5k stars | ✅ | Snapshot au 2026-01-25, now 64,798 as of 2026-07-28 |
| Repo créé | ✅ | 2025-12-14 (commit initial) |

**⚠️ Warning**: La claim "Trusted by engineers at Amazon, Google, Shopify, and Webflow" n'est pas vérifiable. Aucune attribution, lien, ou témoignage. Considérer comme marketing non validé.

---

## 🎯 Décision finale

| Critère | Valeur |
|---------|--------|
| **Score final** | 2/5 |
| **Action** | **Ne pas intégrer** (concepts déjà couverts) |
| **Confiance** | Haute |
| **Révision suggérée** | Dans 3-6 mois si adoption significative |

### Synthèse

GSD est un framework bien structuré mais **conceptuellement redondant** avec le contenu existant du guide:
- Le "context rot" = Fresh Context Pattern
- Les "fresh executor contexts" = Ralph Loop
- Le multi-agent = Gas Town/multiclaude/BMAD

L'absence de données empiriques uniques, combinée à l'overlap >90%, ne justifie pas d'alourdir le guide avec une entrée supplémentaire.

**Alternative recommandée**: Si des utilisateurs demandent spécifiquement GSD, référencer vers les sections existantes du guide couvrant les mêmes concepts.

---

## 📚 Références croisées internes

Les utilisateurs cherchant les concepts GSD trouveront déjà:

| Concept recherché | Section du guide |
|-------------------|------------------|
| Context management | `guide/ultimate-guide.md:1547-1593` (Fresh Context Pattern) |
| Multi-agent workflows | `guide/ecosystem/ai-ecosystem.md:816-890` (Gas Town, multiclaude) |
| Structured planning | `guide/core/methodologies.md:44-55` (BMAD) |
| State persistence | `guide/ultimate-guide.md` Section 3.4 (CLAUDE.md) |
| Task tracking | `guide/ultimate-guide.md` Section 4.5 (TodoWrite) |

---

*Rapport généré par /eval-resource — Claude Code Ultimate Guide v3.12.0*
