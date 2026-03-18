# Resource Evaluation: Boris Cherny - Lenny's Newsletter Podcast

**Date**: 2026-02-25
**Evaluator**: Claude (Sonnet 4.6)
**Status**: À intégrer — 3 points prioritaires identifiés

---

## Resource Details

**Source**: Lenny's Newsletter Podcast
**URL**: https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens
**Title**: "What happens after coding is solved" (inferred from slug)
**Guest**: Boris Cherny, Head of Claude Code at Anthropic
**Host**: Lenny Rachitsky
**Date**: February 19, 2026
**Format**: Long-form audio interview (transcript behind paywall)
**Secondary source used**: NotebookLM transcript summary (Q: "Give me all the tips to learn and use Claude Code in the most efficient way")

**Note**: Article derrière paywall. Évaluation basée sur résumé NotebookLM + vérification Perplexity des claims majeurs.

---

## 📄 Résumé du contenu

**Tips directs Claude Code :**
- Utiliser le modèle le plus capable (Opus) — un modèle fort finit plus vite = moins de tokens au total
- Plan Mode pour **~80% des tâches** (ratio empirique de l'inventeur)
- "Multi-clauding" : lancer plusieurs instances en parallèle simultanément
- Demander à Claude de configurer lui-même ses settings
- Essayer différentes interfaces (desktop, mobile, Slack, GitHub)

**Philosophie produit / workflows :**
- Ne pas forcer de workflows rigides — donner un goal + tools, laisser le modèle naviguer
- Chaîner les outils progressivement (1 outil → chaining)
- **"Build for the model 6 months out"** : concevoir pour le modèle futur, pas l'actuel

**Conseils management / équipe :**
- Être généraliste : combiner dev + PM + design (rôles fusionnent à 50%+)
- **Donner des tokens illimités aux ingénieurs** d'abord, optimiser ensuite
- **Sous-doter les projets** légèrement : force l'utilisation intensive de l'IA, accélère le shipping

**Stats citées :**
- Claude Code représente ~**4% des commits GitHub publics**
- Daily active users ont doublé le mois précédent (janvier-février 2026)
- Boris a brièvement rejoint Cursor avant de revenir chez Anthropic (2 semaines)

---

## 🎯 Score de pertinence (1-5)

| Score | Signification |
|-------|---------------|
| 5 | Essentiel - Gap majeur dans le guide |
| 4 | Très pertinent - Amélioration significative |
| 3 | Pertinent - Complément utile |
| 2 | Marginal - Info secondaire |
| 1 | Hors scope - Non pertinent |

**Score initial : 3/5 → Score ajusté après challenge : 4/5**

**Justification :**

Source authority maximale : Boris Cherny, inventeur du produit, s'adressant à un public PM/product (Lenny's Newsletter). Ce contexte génère des formulations stratégiques et des ratios empiriques absents des sources techniques précédentes (paddo.dev blog, tweets, interviews video). Pattern établi avec les évaluations Boris précédentes : "le guide avait les features, la source primaire apportait la philosophie."

Trois contenus réellement nouveaux vs. évaluations précédentes intégrées (Boris Cowork Video, paddo.dev, SKILLMIND, worktree tips Reddit) :
1. La figure "80% Plan Mode" — ratio empirique de l'inventeur, absent du guide
2. "Build for model 6 months out" — principe stratégique long-terme, absent du guide
3. Management advice (unlimited tokens + under-resource) — zéro overlap avec contenu existant

---

## ⚖️ Comparatif

| Aspect | Cette ressource | Notre guide |
|--------|----------------|-------------|
| Plan Mode — feature documentée | ✅ Couvert | ✅ Présent + 76% token reduction |
| Plan Mode — **ratio 80% des tâches** | ➕ Plus précis (empirique) | ❌ Manquant |
| Multi-clauding / parallel instances | ✅ Couvert | ✅ Présent (Boris case study, paddo.dev) |
| "Build for model 6 months out" | ➕ Nouveau principe | ❌ Manquant |
| Unlimited tokens (management) | ➕ Nouveau (management advice) | ❌ Manquant |
| Under-resource projects | ➕ Nouveau (management advice) | ❌ Manquant |
| Généraliste dev+PM+design | ✅ Couvert (angle career) | ⚠️ Implicite, non articulé |
| CLAUDE.md compounding memory | ✅ Couvert | ✅ Intégré (Boris Cowork Video eval) |
| Ask Claude to configure itself | ⚠️ Overlap possible | ✅ CLAUDE.md auto-amélioration ? À vérifier |
| Interfaces multiples | ✅ Couvert | ✅ mobile-access.md + guide |
| Chainer les outils | ✅ Couvert | ✅ Workflows documentés |

---

## 📍 Recommandations

### Intégrations prioritaires (sans discussion)

**1. Ratio "80% Plan Mode" → `guide/ultimate-guide.md` section Plan Mode**

Format : une phrase avec attribution, pas une section entière.
```
"Boris Cherny (Head of Claude Code) recommends starting ~80% of tasks in Plan Mode —
letting the model plan before any code is written."
```
Source : Lenny's Newsletter, February 19, 2026.

**2. "Build for model 6 months out" → section stratégie long-terme ou CLAUDE.md best practices**

Principe stratégique nommé et mémorable. Seul l'inventeur du produit peut le légitimer avec cette autorité. Ajouter comme principe numéroté dans la section philosophie/strategy du guide.

**3. Management advice (unlimited tokens + under-resource) → section team/enterprise**

Nouvelle sous-section avec les 3 principes de Boris pour son équipe :
- Underfund projects on purpose
- Give engineers as many tokens as possible (optimize only after success)
- Encourage people to go faster

Cible : tech leads et managers qui lisent le guide.

### Intégrations optionnelles (vérifier overlap avant)

- "Demander à Claude de configurer ses settings" → vérifier si couvert dans CLAUDE.md auto-amélioration
- Angle généraliste dev+PM+design → mention dans intro ou section impact Claude Code

### Ne pas intégrer

- Tips interfaces multiples : déjà couverts
- "Ne pas forcer workflows rigides" : déjà présent sous goal-oriented prompting
- Chaîner outils progressivement : trop vague, couvert sous workflows

---

## 🔥 Challenge (technical-writer agent)

**Agent utilisé** : `technical-writer` (subagent)

**Verdict de l'agent :**

> "Score 3/5 est FAUX. Ca devrait être 4/5."

Arguments clés du challenge :

1. **Source authority mal évaluée** : Lenny's Newsletter force Boris à articuler pour un public PM/product — formulations différentes de ses sources techniques précédentes. Pattern établi : les évaluations Boris sous-estiment systématiquement le gap "feature documentée vs. philosophie d'usage."

2. **"80% Plan Mode" n'est pas dans le guide** : paddo.dev couvrait "re-plan when stuck" mais PAS la fréquence. Un ratio empirique de l'inventeur est différent de documenter une feature.

3. **"Build for 6 months out" absent de toutes les évaluations précédentes** : décision d'architecture de workflow, impact long-terme sur comment les utilisateurs investissent dans leur CLAUDE.md.

4. **Management advice = zéro overlap** : le guide documente comment UTILISER Claude Code, pas comment le DÉPLOYER en équipe avec budget tokens.

**Points manqués dans l'évaluation initiale** :
- Contexte audience PM/product génère du contenu différent des sources dev
- "Ask Claude to configure settings" sous-évalué (meta-loop différente du compounding memory)
- Angle généraliste a une demi-vie longue dans le guide

**Risques de non-intégration** :
- Ratio Plan Mode : utilisateurs continuent à utiliser sporadiquement au lieu de systématiquement
- "6 months out" : guide implique implicitement d'optimiser pour l'instant présent
- Management advice : le guide cède ce terrain à d'autres ressources
- Crédibilité : ignorer une interview longue-format de Boris Cherny sur Lenny's Newsletter est un signal d'angle mort pour un guide "référence exhaustive"

**Sur le paywall :**
> "Ce qui pose problème : citation directe impossible sans accès vérifié. Ce qui ne pose pas problème : l'intégration n'exige pas que les lecteurs vérifient la source. Boris Cherny + Lenny's Newsletter + date = attribution suffisamment précise."

- **Score ajusté par l'agent** : 4/5
- **Points manqués** : contexte PM/product, meta-loop configure-settings, thèse généraliste
- **Risques non-intégration** : réels sur 3 points prioritaires

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| Boris Cherny = Head of Claude Code at Anthropic | ✅ | Perplexity (Business Insider, Times of India, Waydev) |
| Date publication : 19 février 2026 | ✅ | URL + WebFetch + Perplexity |
| "Underfund projects on purpose" | ✅ | Business Insider (23 fev 2026), Perplexity |
| "Give engineers unlimited tokens first" | ✅ | Business Insider (23 fev 2026), Perplexity |
| 3 core principles (underfund, unlimited, go faster) | ✅ | Business Insider (23 fev 2026) |
| Boris a brièvement rejoint Cursor | ✅ | Business Insider (18 fev 2026) |
| "Generalist" thesis (50%+ overlap dev/PM/design) | ✅ | Perplexity (Waydev, 24 fev 2026) |
| "Coding is solved" thesis | ✅ | Business Insider (18 fev 2026), Fortune (24 fev 2026) |
| "4% of GitHub commits" | ⚠️ | WebFetch (paywalled body) — dans le lede visible, non vérifiable via Perplexity |
| "80% Plan Mode" ratio | ⚠️ | NotebookLM transcript only — non corroboré par Perplexity |
| Daily active users doubled | ⚠️ | WebFetch (paywalled) — non vérifiable via Perplexity |
| "Multi-clauding" terminology | ⚠️ | NotebookLM transcript only — terme non vérifié indépendamment |

**Corrections apportées** : Aucune. Les claims vérifiables sont corrects.

**Claims à risque** : Les points marqués ⚠️ viennent du résumé NotebookLM (source secondaire). Intégrer avec attribution conditionnelle ("selon la transcription de l'interview") jusqu'à accès direct au transcript.

**Recommandation fact-check** : Si accès Lenny's Newsletter disponible, vérifier le ratio "80% Plan Mode" et le stat "4% GitHub commits" avant intégration définitive.

---

## 🎯 Décision finale

- **Score final : 4/5** (ajusté depuis 3/5 initial suite au challenge)
- **Action** : Intégrer — 3 points prioritaires dans la semaine
- **Confiance** : Haute sur management advice (Perplexity confirmé), Moyenne sur ratios spécifiques (NotebookLM only)

### Plan d'intégration

| Point | Où | Format | Priorité |
|-------|----|--------|----------|
| "80% Plan Mode" empirique | `guide/ultimate-guide.md` section Plan Mode | 1 phrase + attribution | Haute |
| "Build for model 6 months out" | Section stratégie long-terme ou CLAUDE.md best practices | Principe nommé + citation | Haute |
| Unlimited tokens + under-resource | Section team/enterprise | Sous-section "Boris Cherny's 3 principles for teams" | Haute |
| Généraliste thesis | Intro ou section impact Claude Code | Citation courte | Basse |

---

## Sources

- **Primary (paywalled)**: [Lenny's Newsletter - Boris Cherny interview](https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens) (19 fev 2026)
- **Secondary used for evaluation**: NotebookLM transcript summary (Q: efficient tips)
- **Verification (Perplexity)**:
  - [Waydev — 8 insights from Boris Cherny](https://waydev.co/8-game-changing-insights-from-anthropic-claudecode-boris-cherny/) (24 fev 2026)
  - [Business Insider — 3 principles Boris Cherny](https://www.businessinsider.com/claude-creator-three-principles-boris-cherny-2026-2) (23 fev 2026)
  - [Business Insider — coding is solved](https://www.businessinsider.com/anthropic-claude-code-founder-ai-impacts-software-engineer-role-2026-2) (18 fev 2026)
  - [Fortune — software engineers](https://fortune.com/2026/02/24/will-claude-destroy-software-engineer-coding-jobs-creator-says-printing-press/) (24 fev 2026)
- **Related evaluations Boris Cherny** (déjà intégrées) :
  - `boris-cowork-video-eval.md` — YouTube interview Jan 2026 (Greg Isenberg)
  - `paddo-team-tips-eval.md` — paddo.dev blog synthesis (4/5, intégré)
  - `2026-02-19-stasbel-skillmind-boris-cherny-workflow.md` — LinkedIn SKILL.md (2/5, mention)
  - `2026-02-22-boris-cherny-worktree-tips-reddit.md` — Reddit worktree tips

---

## Changelog

- **2026-02-25**: Évaluation initiale. Score 3/5 → ajusté 4/5 après challenge technical-writer. Fact-check Perplexity effectué. 3 points prioritaires identifiés pour intégration.