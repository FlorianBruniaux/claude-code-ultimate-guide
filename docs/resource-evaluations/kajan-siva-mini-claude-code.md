# Evaluation: "Construire un mini Claude Code pas à pas" - Kajan Siva

**Resource Type**: Blog article
**Author**: Kajan Siva
**URL**: https://www.kajansiva.com/blog/construire-mini-claude-code-pas-a-pas
**Companion repo**: [KajanSiva/du-prompt-a-l-agent](https://github.com/KajanSiva/du-prompt-a-l-agent)
**Evaluation Date**: 2026-08-05
**Evaluator**: Claude Sonnet 5

---

## 1. Content Summary

Long-form article (~9 min read) walking through the construction of a minimal Claude Code-like agent in four steps: basic API call, context window (message history), tool calling, and the agentic loop that ties them together. JavaScript/Node.js, Anthropic API (Claude Sonnet 5). Code is provided for each step, including a `searchCode` tool schema and a simplified agent loop. Covers `stop_reason`, `tool_use_id` linking, and flags prompt injection risk when tool output re-enters the context unfiltered.

**Key claims**: agent = LLM + context + tools + loop + stop condition; tool calling is a request, not a direct execution, the app decides whether to run it; the loop repeats until `stop_reason` is not `tool_use`.

---

## 2. Initial Scoring: 2/5 (Marginal)

| Score | Signification | Action |
|-------|----------------|--------|
| 5 | Critical | Intégrer sous 24h |
| 4 | High Value | Intégrer sous 1 semaine |
| 3 | Moderate | Intégrer si temps disponible |
| **2** | **Marginal** | **Ne pas intégrer (ou mention minimale)** |
| 1 | Low | Rejeter |

### Justification

**Points forts**: contenu technique réel (pas un post promotionnel), code exécutable, repo GitHub compagnon, couvre le prompt injection ce que beaucoup de tutoriels équivalents en anglais effleurent à peine.

**Points faibles**:
- **Aucun gap comblé** : `guide/core/architecture.md` §1 "The Master Loop" (ligne 109) documente déjà le même mécanisme (boucle, `tool_use`, `stop_reason`), sourcé Tier 1 officiel Anthropic. L'article ne fait que redémontrer pédagogiquement ce que le guide explique déjà avec une source plus solide.
- **Contraire à la règle de langue du repo** : contenu 100% français, alors que ce repo est intégralement en anglais (mémorisé, règle ferme). Une source française ne peut pas être citée comme référence dans le guide sans traduction, ce qui n'a pas de sens pour un tutoriel dont l'intérêt est justement d'être lu tel quel.
- **Pattern pédagogique non-original** : la formule "agent = LLM + contexte + outils + boucle + condition d'arrêt" et sa démonstration en 4 étapes croissantes est un genre établi depuis mi-2025, popularisé par Thorsten Ball (équipe Amp), "How to Build an Agent" (https://ampcode.com/blog/how-to-build-an-agent), largement cité comme la référence du genre. Recherche web (2026-08-05) a remonté au moins 6 tutoriels équivalents publiés entre mai et juillet 2026 suivant la même structure.
- **Auteur déjà évalué à 2/5** : un post LinkedIn antérieur du même auteur (`/insights` command, éval du 2026-02-06, voir [kajan-siva-insights-command.md](./kajan-siva-insights-command.md)) avait été jugé sans contenu technique exploitable. Celui-ci est nettement plus solide, mais confirme un pattern : contenu accessible, jamais la source la plus dense sur son sujet.

**Comparaison avec nos critères**:
- Breakthrough/nouvelle capacité ? ❌
- Profondeur technique inédite ? ❌ (déjà couvert, source moins forte que l'officielle)
- Exemples actionnables ? ✅ (repo GitHub fonctionnel)
- Comble un gap du guide ? ❌
- Validation communautaire ? ⚠️ (pas mesurée, pas de signal fort trouvé)

---

## 3. Comparative Analysis

| Aspect | Article Kajan Siva | Guide (`architecture.md` §1) |
|--------|---------------------|-------------------------------|
| Boucle agentique | Expliquée + code from-scratch | Expliquée, sourcée officiel Anthropic |
| `stop_reason` | Couvert | Couvert |
| `tool_use_id` | Couvert | Couvert |
| Prompt injection | Mentionné (risque général) | Couvert en détail dans `guide/security/security-hardening.md` |
| Langue | Français | Anglais (règle du repo) |
| Format | Tutoriel pédagogique, code pas-à-pas | Référence technique |

---

## 4. Integration Decision

### Decision: **DO NOT INTEGRATE** ❌

**Rationale**:
1. Zéro gap comblé, le mécanisme est déjà documenté avec une source plus solide.
2. Contenu français, incompatible avec la règle de langue du repo (anglais uniquement).
3. Le genre "construis ton propre agent pour comprendre" mérite une entrée dans `guide/roles/learning-with-ai.md` § External Resources, mais avec la source canonique anglophone du genre plutôt que celle-ci.

### Alternative Action

Ajout de **Thorsten Ball, "How to Build an Agent"** (https://ampcode.com/blog/how-to-build-an-agent) dans `guide/roles/learning-with-ai.md` § External Resources, à la place de cet article : même genre pédagogique (comprendre l'agent loop en le construisant), en anglais, référence la plus citée du genre.

---

## 5. Final Metadata

**Initial Score**: 2/5
**Final Score**: 2/5
**Decision**: Do Not Integrate ❌ (genre remplacé par une source équivalente anglophone, Thorsten Ball, dans `learning-with-ai.md`)
**Confidence**: High

**Archive Location**: `docs/resource-evaluations/kajan-siva-mini-claude-code.md`
