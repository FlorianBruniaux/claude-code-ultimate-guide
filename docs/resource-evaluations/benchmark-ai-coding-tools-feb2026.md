# Resource Evaluation: Benchmark Comparatif AI Coding Tools (Feb 2026)

**Date**: 2026-03-02
**Evaluator**: Claude Sonnet 4.6
**Source**: Texte copié (pas d'URL — auteur inconnu)
**Type**: Benchmark comparatif (Claude Code vs Cursor vs Windsurf vs Zed vs Copilot Workspace)
**Périmètre temporel revendiqué**: Fin février 2026

---

## Executive Summary

**Score**: 3/5 (Pertinent — Complément utile)
**Decision**: Intégration sélective (2 apports nets identifiés)
**Confidence**: Moyenne (claims non vérifiables sans URL source)

Benchmark structuré comparant 5 outils d'agentic coding avec des tableaux détaillés, un focus Claude Code et 6 recommandations documentaires. Apport réel sur deux angles manquants dans le guide : quotas précis par plan (Pro/Max) et couverture Windsurf/Zed aujourd'hui absente. Le reste chevauche des sections existantes ou est non vérifiable.

---

## Résumé du contenu

- **5 outils comparés** : Claude Code (CLI-first + sub-agents + hooks), Cursor (IDE fork VS Code, Tab, Composer), Windsurf (Cascade multi-agents, Wave 13), Zed (Rust natif, Ollama local), Copilot Workspace (GitHub-centré, issue → PR)
- **Breaking news** : Sonnet 4.6 lancé "15 fév 2026" avec 1M context (beta), modèle par défaut Pro/Free ; extension VS Code GA ; nouveaux docs Hooks (26 fév)
- **Quotas Claude Code** : Pro ≈ 10-40 prompts/5h, Max 5x = 50-200/5h, Max 20x = 200-800/5h, cap ~50 fenêtres/mois
- **Différenciation Claude Code** : points forts = CLI + Git + sub-agents + checkpoints + CLAUDE.md/init ; points faibles = pas d'autocomplétion inline, quotas Pro serrés sur sessions intensives
- **6 recommandations documentaires** : (1) cadrage modèles/contexte, (2) page quotas devs, (3) stack agentique, (4) comparaison IDE, (5) CLAUDE.md pédagogie, (6) VS Code flows

---

## Score de pertinence (1-5)

| Score | Signification |
|-------|---------------|
| 5 | Essentiel - Gap majeur dans le guide |
| 4 | Très pertinent - Amélioration significative |
| **3** | **Pertinent - Complément utile** |
| 2 | Marginal - Info secondaire |
| 1 | Hors scope - Non pertinent |

**Score: 3/5**

**Justification** : Deux apports nets confirmés après vérification du guide, mais le reste est soit déjà couvert, soit invérifiable sans URL source. La source inconnue (texte copié, auteur non identifié) empêche un score plus élevé — standard appliqué de façon cohérente avec les évaluations précédentes.

---

## Comparatif

| Aspect | Cette ressource | Notre guide |
|--------|----------------|-------------|
| Cursor comparison | Benchmark détaillé (UX, pricing, limites) | ✅ Couvert (ligne 885, 947 — migration guide) |
| Windsurf | Couvert (Wave 13, Cascade, pricing) | ⚠️ Mentions passantes (~6 lignes) |
| Zed AI | Couvert (Rust natif, Ollama, token pricing) | ❌ Absent (pas de section dédiée) |
| Copilot Workspace | Couvert (issue → PR workflow) | ⚠️ Mentionné en liste, pas comparé |
| Quotas Pro/Max précis | Chiffres précis par plan et par fenêtre | ⚠️ Existe mais éparpillé (ultime-guide + known-issues) |
| Sonnet 4.6 comme défaut | Documenté avec benchmarks préférences | ✅ Déjà dans guide (releases tracking) |
| Stack agentique hooks | Recommandation de regroupement | ✅ Couvert mais fragmenté |
| CLAUDE.md /init | Recommandation tutoriel pas-à-pas | ✅ Couvert (plusieurs sections) |
| VS Code flows prédéfinis | Recommandation workflows | ✅ Couvert (extension doc) |

---

## Recommandations d'intégration

### Apport #1 — Quotas précis par plan (PRIORITÉ HAUTE)

- **Gap réel** : Les chiffres existent dans le guide mais sont éparpillés entre `ultimate-guide.md` et `guide/known-issues.md`. Pas de tableau synthétique "Pro / Max 5x / Max 20x" avec les intervalles réels par fenêtre 5h.
- **Où** : `guide/ultimate-guide.md` section pricing/limits (~ligne 1951-2013) + potentiellement `guide/architecture.md`
- **Comment** : Tableau unique "Plan → prompts Claude Code/5h → Sonnet heures/semaine → cap mensuel" avec note sur sub-agents et 1M context comme multiplicateurs de consommation
- **Caveat** : Les chiffres du benchmark (10-40 / 50-200 / 200-800) sont des fourchettes communautaires, pas des SLAs officiels Anthropic. Sourcer depuis GitHub issues anthropics/claude-code ou docs officielles avant d'intégrer.

### Apport #2 — Section Windsurf + Zed dans le comparatif outils (PRIORITÉ MOYENNE)

- **Gap réel** : Le tableau comparatif ligne 885 couvre Copilot/Cursor/Claude Code. Windsurf et Zed sont absents du comparatif principal malgré leur adoption croissante.
- **Où** : Section Migration/Comparison (~ligne 881), étendre le tableau existant
- **Comment** : Ajouter 2 colonnes (Windsurf + Zed) + une ligne "Copilot Workspace" avec positionnement court (50-100 mots par outil). Utiliser le benchmark comme base, vérifier contre docs officielles.
- **Attention** : Windsurf Wave 13 + SWE-1.5 et Zed token pricing (+10%) sont des claims spécifiques à vérifier contre windsurf.com/changelog et zed.dev/blog avant intégration.

### À ne pas intégrer

- Recommandations 3, 5, 6 (stack agentique, CLAUDE.md, VS Code flows) : déjà couverts dans le guide, intégration = duplication sans valeur ajoutée.
- Rec 4 (page dédiée "comparaison IDE") : pertinente sur le principe mais le guide n'est pas une page marketing Anthropic — garder le focus pédagogique.

---

## Challenge (technical-writer)

**Score ajusté : 3/5** (downgrade depuis 4/5 initial)

**Points du challenge :**
- La source inconnue (texte sans URL, auteur non identifié) est un disqualificateur partiel — les évaluations précédentes de sources anonymes sans vérifiabilité finissent systématiquement en dessous de 4
- Le lancement Sonnet 4.6 "15 fév 2026" est un claim daté précis qui mérite vérification contre `llms-full.txt` avant de s'appuyer dessus
- Les 6 recommandations ne sont pas équivalentes : 2 adressent des gaps réels, 4 sont du polish sur ce qui existe — une évaluation rigoureuse les sépare
- L'absence de Windsurf/Zed dans le guide est une lacune réelle mais non critique pour l'audience cible (devs CLI qui ne cherchent pas de comparatif marketing)

**Risques de non-intégration :**
- Faibles à court terme : le comparatif existant (3 outils) couvre les besoins d'une majorité de lecteurs
- Moyen terme : si Windsurf/Zed continuent de monter, l'absence dans le guide crée un angle mort de crédibilité

---

## Fact-Check

| Affirmation | Vérifiée | Source | Notes |
|-------------|----------|--------|-------|
| Sonnet 4.6 lancé "15 fév 2026" | ⚠️ PARTIELLE | llms-full.txt à croiser | Date précise non vérifiée dans cette évaluation |
| Sonnet 4.6 = modèle par défaut Pro/Free | ✅ PROBABLE | Cohérent avec releases tracking guide | Vérifier contre anthropic.com/news |
| Quotas Pro 10-40 prompts/5h | ⚠️ COMMUNAUTAIRE | GitHub issues #6611 cité dans texte | Fourchette observée, pas SLA officiel |
| Max 5x = 50-200 prompts/5h | ⚠️ COMMUNAUTAIRE | Même source | Idem |
| Windsurf Wave 13 : multi-agents parallèles | ⚠️ NON VÉRIFIÉE | windsurf.com/changelog (non fetchable ici) | Crédible mais non confirmé |
| Zed Pro = $10/mo + $5 tokens | ⚠️ NON VÉRIFIÉE | zed.dev/blog/pricing... (non fetchable) | Crédible mais non confirmé |
| Cursor Bugbot Autofix ~35% merges directs | ⚠️ NON VÉRIFIÉE | cursor.com/changelog (non fetchable) | Chiffre spécifique, vérifier |
| Extension VS Code Claude Code en GA | ✅ CONFIRMÉE | code.claude.com/docs (dans guide) | Documenté dans releases tracking |
| Docs Hooks Claude Code (26 fév) | ✅ PROBABLE | code.claude.com/docs/en/hooks | Cohérent avec état actuel |

**Corrections apportées** : Aucune donnée intégrée sans vérification. Claims marqués ⚠️ doivent être vérifiés avant intégration dans le guide.

**Stats nécessitant recherche externe avant intégration** :
- Quotas Pro/Max précis → chercher dans GitHub issues anthropics/claude-code ou docs officielles
- Windsurf Wave 13 features → vérifier windsurf.com/changelog
- Zed token pricing → vérifier zed.dev/blog

---

## Décision finale

- **Score final** : 3/5 (Pertinent)
- **Action** : Intégration sélective — 2 apports sur 6
- **Confidence** : Moyenne (source anonyme, claims communautaires non tous vérifiables)

### Prochaines étapes

1. **Vérifier Sonnet 4.6 date** : `https://code.claude.com/docs/llms-full.txt` ou Perplexity
2. **Vérifier quotas précis** : GitHub issues anthropics/claude-code (chercher #6611)
3. **Si vérifiés** : Intégrer tableau quotas + étendre comparatif outils (Windsurf + Zed)
4. **Priorité** : Moyenne (amélioration utile, non bloquante)

---

*Fichier* : `docs/resource-evaluations/benchmark-ai-coding-tools-feb2026.md`
*Prochaine révision* : 2026-06-02 (pricing et modèles évoluent vite dans ce secteur)