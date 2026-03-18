# Evaluation: SKILL.md / SKILLMIND — Boris Cherny Workflow Practices

**Date:** 2026-02-19
**Evaluator:** Claude (Sonnet 4.6)
**Status:** Mention uniquement (voir conclusion)

**Sources:**
- LinkedIn: [Stanislav Beliaev — "This SKILL.md file will make you 10x engineer"](https://www.linkedin.com/posts/stasbel_this-%F0%9D%97%A6%F0%9D%97%9E%F0%9D%97%9C%F0%9D%97%9F%F0%9D%97%9F%F0%9D%97%BA%F0%9D%97%B1-file-will-make-you-10x-activity-7430215933832425472-MDvA)
- X/Twitter: [bcherny/status/2017742741636321619](https://x.com/bcherny/status/2017742741636321619) (non fetchable — JS requis)

---

## 📄 Résumé du contenu

- **Format**: Fichier SKILL.md (ou CLAUDE.md-style) contenant des workflow practices attribuées à Boris Cherny (créateur Claude Code @ Anthropic)
- **Workflow Orchestration (6 practices)**: Plan Node Default, Subagent Strategy, Self-Improvement Loop, Verification Before Done, Demand Elegance (Balanced), Autonomous Bug Fixing
- **Task Management (6 items)**: Plan First (`tasks/todo.md`), Verify Plan, Track Progress, Explain Changes, Document Results, Capture Lessons (`tasks/lessons.md`)
- **Core Principles (3)**: Simplicity First, No Laziness, Minimal Impact
- **Concept clé unique**: Self-Improvement Loop — après TOUTE correction utilisateur → mettre à jour `tasks/lessons.md` avec des règles, review au début de session suivante → "compounding improvement"
- **Engagement LinkedIn**: 43 likes, 8 commentaires (relativement faible pour 64K followers — signal de niche)

---

## 🎯 Score de pertinence (1-5)

| Score | Signification |
|-------|---------------|
| 5 | Essentiel - Gap majeur dans le guide |
| 4 | Très pertinent - Amélioration significative |
| 3 | Pertinent - Complément utile |
| 2 | Marginal - Info secondaire |
| 1 | Hors scope - Non pertinent |

**Score: 2/5** (après challenge)

**Justification:**

La majorité du contenu est déjà couverte dans le guide:
- Plan mode pour tâches non-triviales → documenté (section plan mode)
- Subagent strategy → documenté (section subagents)
- Compounding via CLAUDE.md → documenté (ligne ~3989)
- "Would a staff engineer approve this?" → documenté (ligne 14274)
- Ralph Loop avec PROGRESS.md → couvre le même besoin que tasks/lessons.md (ligne 1575-1595)
- Simplicity / No Laziness / Minimal Impact → PRINCIPLES.md et CLAUDE.md best practices

**Delta réel = tasks/lessons.md comme convention alternative** — un fichier runtime créé pendant le travail (vs CLAUDE.md qui est une config upfront). C'est une différence d'implémentation, pas un concept nouveau.

---

## ⚖️ Comparatif

| Aspect | Cette ressource | Notre guide |
|--------|----------------|-------------|
| Plan mode (tâches non-triviales) | ✅ Couvert | ✅ Présent |
| Subagent strategy | ✅ Couvert | ✅ Présent |
| Persistent memory via fichier | ✅ `tasks/lessons.md` | ✅ Ralph Loop (PROGRESS.md) + Serena MCP |
| "Staff engineer approval" check | ✅ Couvert | ✅ Présent (ligne 14274) |
| Self-improvement / compounding | ✅ Pattern spécifique | ✅ CLAUDE.md compounding (ligne ~3989) |
| Autonomous bug fixing (principe) | ✅ Explicite | ⚠️ Implicite, non nommé |
| Demand Elegance (principe nommé) | ✅ Nommé | ⚠️ Implicite (YAGNI, KISS) |
| tasks/lessons.md convention | ✅ Runtime file | ❌ Non documenté comme tel |

---

## 📍 Recommandations

**Score 2/5 → Mention uniquement, pas d'intégration majeure.**

**Raisons du score modéré:**
1. **Attribution incertaine**: Le post LinkedIn est une source secondaire. Le tweet @bcherny est une source primaire potentielle mais non fetchable. Intégrer sans vérification = risque de duplication avec attribution inférieure aux sources primaires déjà dans le guide.
2. **Contenu majoritairement redondant**: 5 des 6 workflow practices existent déjà dans le guide sous d'autres formulations.
3. **Delta réel = nommage**: `tasks/lessons.md` vs `PROGRESS.md` + CLAUDE.md = même concept, convention différente.

**Si source primaire confirmée (bcherny tweet direct):** Score → 3/5

Action recommandée:
- **Option 1 (minimale)**: Ajouter `tasks/lessons.md` comme exemple alternatif dans la section Ralph Loop (ligne ~1590), une ligne de mention
- **Option 2 (si confirmé Cherny)**: Créer un court callout "Boris Cherny's lessons.md pattern" dans la section Memory Files comme implémentation légère sans MCP

**Où si intégration:**
- `guide/ultimate-guide.md` ligne ~1590 (Fresh Context Pattern / Ralph Loop)
- `examples/claude-md/` — ajouter un template avec `tasks/lessons.md` convention

---

## 🔥 Challenge (agent technique)

**Score challengé: 2/5 (depuis 3/5)**

Points du challenge:
- **Attribution non vérifiée**: "Basé sur Boris Cherny" via un post LinkedIn secondaire → ne pas traiter comme source primaire. Le guide a déjà des sources primaires vérifiées (InfoQ Jan 2026, paddo.dev, Twitter officiel de Cherny).
- **tasks/lessons.md = CLAUDE.md dans un dossier tasks/**: Différence de convention, pas de substance. La valeur ajoutée est quasi-nulle si le pattern est "write rules to a markdown file".
- **5/6 practices déjà dans le guide**: La redondance est élevée.
- **Seul point potentiellement nouveau**: "Autonomous Bug Fixing" comme principe autonome nommé explicitement — le guide ne l'articule pas comme tel ("just fix it, zero context switching").
- **"Demand Elegance"**: Intéressant comme formulation, mais KISS/YAGNI couvrent l'intention.

**Risques de non-intégration**: Quasi nuls — le guide couvre l'essentiel via des sources meilleures.

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| Stanislav Beliaev: 64,853 followers | ✅ | LinkedIn fetch direct |
| Date publication: Feb 19, 2026 | ✅ | LinkedIn fetch direct |
| "Based on Boris Cherny best practices" | ⚠️ | Secondaire — tweet @bcherny non fetchable |
| Boris Cherny = créateur Claude Code @ Anthropic | ✅ | Documenté dans le guide (ligne 15153) |
| 43 likes, 8 commentaires | ✅ | LinkedIn fetch direct |

**Stats non vérifiées**: Attribution directe à Boris Cherny — le tweet @bcherny référencé n'a pas pu être fetchable (JS requis sur X). La source primaire existe potentiellement mais n'est pas vérifiable sans accès X authentifié.

**Aucune hallucination de chiffres détectée.**

---

## 🎯 Décision finale

- **Score final: 2/5**
- **Action: Mention uniquement** — Ajouter une ligne dans la section Ralph Loop/Fresh Context Pattern mentionnant la convention `tasks/lessons.md` comme alternative lightweight
- **Condition pour réévaluation**: Confirmation que le tweet @bcherny/status/2017742741636321619 contient du contenu inédit non déjà capturé via ses sources primaires existantes
- **Confiance: Moyenne** — Contenu vérifié mais attribution primaire non confirmable

**Pas d'intégration majeure recommandée en l'état.**
