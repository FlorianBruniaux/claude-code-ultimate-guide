# Resource Evaluation: fp.dev — Agent-Native Issue Tracking

**Evaluated**: 2026-02-22
**Evaluator**: Claude Sonnet 4.6 + technical-writer agent challenge
**Target Guide**: Claude Code Ultimate Guide
**Source**: https://fp.dev/ + LinkedIn post (community)

---

## Executive Summary

**Resource**: fp.dev — "Agent-native issue tracking for ambitious Claude Code users"
**URL**: https://fp.dev/

**Initial Score**: 3/5
**Challenged Score**: 2/5
**Final Score**: **2/5 (Marginal — Watchlist)**

**Decision**: **Ne pas intégrer activement. Ajouter dans Known Gaps + Watch List.**

---

## 📄 Résumé du contenu

- **fp.dev** est un outil de tracking d'issues local-first conçu spécifiquement pour Claude Code
- Issues stockées en `.md` dans `/.claude/` — git-committables (différentiateur réel vs Tasks API)
- Workflow via skills custom (`/fp-plan`, `/fp-implement`, `/fp-review`) + CLI (`fp tree`, `fp issue list`, `fp issue show`, `fp review`)
- Résout le "context rot" : permet de `/clear` la session sans perdre l'état projet
- App desktop Mac (Apple Silicon uniquement) + UI code review avec diff viewer intégré
- Zéro dépendance externe, zéro MCP server
- Installation : `curl -fsSL https://setup.fp.dev/install.sh | sh -s && fp setup claude && fp init`

---

## 🎯 Score de pertinence (1-5)

| Score | Signification |
|-------|---------------|
| 5 | Essentiel - Gap majeur dans le guide |
| 4 | Très pertinent - Amélioration significative |
| 3 | Pertinent - Complément utile |
| 2 | Marginal - Info secondaire |
| 1 | Hors scope - Non pertinent |

**Score final : 2/5**

**Justification** : Problème adressé réel mais déjà couvert partiellement par le guide (fresh-context-loop.sh, Tasks API native). Un seul différentiateur solide (issues .md git-committables). Adoption insuffisante, restriction Apple Silicon disqualifiante pour recommandation large.

---

## ⚖️ Comparatif

| Aspect | fp.dev | Guide actuel |
|--------|--------|-------------|
| Context rot / session clear | ✅ Issues .md persistées | ✅ `fresh-context-loop.sh` (Ralph Wiggum pattern) |
| Task management structuré | ✅ CLI + skills dédiés | ✅ Tasks API native |
| Issues git-committables | ✅ (.md files dans repo) | ❌ Manquant |
| Code review avec diff viewer | ✅ UI locale dédiée | ❌ Non couvert |
| Multi-plateforme | ❌ Desktop = Apple Silicon only | ✅ N/A |
| MCP intégration | ❌ Pas de MCP | ✅ Couvert dans le guide |
| Équipes / sync | ❌ Local only | ✅ Tasks API multi-agent |

---

## 🔥 Challenge (technical-writer)

Arguments pour descendre à 2/5 :

1. **Redondance** : `/clear` + Tasks API couvre déjà le problème principal
2. **Restriction plateforme** : Apple Silicon only pour le desktop = dealbreaker Linux/Windows
3. **Signaux d'adoption manquants** : Pas de GitHub stars, pas de release cadence documentée → risque d'abandon
4. **Mauvaise catégorisation** : Ne va pas aux côtés de Gas Town/multiclaude (multi-agent orchestration) — fp.dev est du task tracking
5. **Un vrai différentiateur** : Issues `.md` git-committables → mais insuffisant seul pour 3/5

**Score ajusté** : 2/5
**Risques de non-intégration** : Faibles. Le guide couvre déjà le problème. La valeur est dans documenter le GAP (markdown-based issue tracking) pas nécessairement fp.dev.

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| Issues stockées en `.md` dans `/.claude/` | ✅ | fp.dev (WebFetch) + Perplexity |
| CLI : `fp tree`, `fp issue list`, `fp issue show`, `fp review` | ✅ | WebFetch direct |
| Installation : `fp setup claude` + `fp init` | ✅ | fp.dev + Perplexity |
| Local-first, no external services | ✅ | fp.dev |
| Mac desktop app = Apple Silicon requis | ✅ | fp.dev |
| Skills `/fp-plan`, `/fp-implement`, `/fp-review` | ✅ | Description + WebFetch |

Zéro hallucination. Toutes les claims vérifiées.

---

## 📍 Recommandations

**Score < 3 → Watchlist, pas d'intégration directe.**

Actions effectuées :
1. ✅ Ajout dans `docs/resource-evaluations/watch-list.md`
2. ✅ Ajout du gap "Agent-native issue tracking (markdown-based, git-committable)" dans `guide/third-party-tools.md` Known Gaps

**Trigger de re-évaluation** : GitHub stars visibles + release cadence documentée + au moins un write-up praticien en production.

---

**Évaluation complétée** : 2026-02-22
**Prochaine révision** : Sur trigger (adoption signals)
