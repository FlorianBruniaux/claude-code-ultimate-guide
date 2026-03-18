---
# Resource Evaluation: "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"

**Source**: https://arxiv.org/abs/2602.11988
**Authors**: Thibaud Gloaguen, Niels Mündler, Mark Müller, Veselin Raychev, Martin Vechev (ETH Zürich)
**Date**: February 13, 2026
**Type**: Peer-reviewed academic paper (arXiv cs.SE)
**Evaluated**: 2026-02-19

---

## 📄 Résumé du contenu

- **Question de recherche** : Les fichiers de contexte de type AGENTS.md améliorent-ils réellement les performances des coding agents ?
- **Résultat principal** : Les fichiers developer-written améliorent légèrement le taux de succès (+4%), mais LLM-generated les dégradent (-3%) — dans tous les cas, le coût d'inférence augmente de 20-23%
- **AGENTbench** : Nouveau benchmark introduit, 138 instances, 12 repositories avec des context files écrits par des développeurs (bug fixes + feature additions)
- **Mécanisme identifié** : Les agents suivent fidèlement toutes les instructions du context file, même celles non pertinentes à la tâche → surcharge cognitive, exploration plus large, chaînes de raisonnement plus longues
- **Recommandation centrale** : Inclure UNIQUEMENT les commandes build/test + tooling spécifique ; exclure style guides, descriptions d'architecture, et documentation générale

---

## 🎯 Score de pertinence

| Score | Signification |
|-------|---------------|
| 5 | Essentiel - Gap majeur dans le guide |
| **4** | **Très pertinent - Amélioration significative** |
| 3 | Pertinent - Complément utile |
| 2 | Marginal - Info secondaire |
| 1 | Hors scope - Non pertinent |

**Score: 4/5**

**Justification**: Le guide recommande déjà un CLAUDE.md concis (<200 lignes), mais sans validation empirique. Ce paper fournit exactement cette validation + une nuance critique absente : même un context file "optimal" ajoute 20-23% de coût sans ROI proportionnel. La tension entre "générer son CLAUDE.md avec Claude" et "-3% pour LLM-generated" est directement actionnable.

---

## ⚖️ Comparatif

| Aspect | Ce paper | Notre guide |
|--------|----------|-------------|
| CLAUDE.md concis recommandé | ✅ Validé empiriquement | ✅ Déjà présent (opinion) |
| Impact sur taux de succès agent | ✅ +4% (dev) / -3% (LLM) | ❌ Absent |
| Cost penalty des context files | ✅ +20-23% dans tous les cas | ❌ Absent |
| LLM-generated context file = risque | ✅ Prouvé empiriquement | ❌ Non mentionné |
| Recommandation: build/test commands only | ✅ Recommandation précise | ⚠️ Vague ("essentiel") |
| Distinction minimal vs comprehensive | ✅ Empiriquement justifiée | ⚠️ Présente mais non chiffrée |

---

## 📍 Recommandations d'intégration

**Trois points d'intégration, par priorité:**

### 1. Section "CLAUDE.md Best Practices" (guide/ultimate-guide.md, ligne ~13395)
**Priorité: Haute**

Ajouter un encadré "Research note" après la liste des best practices existantes :

```markdown
> **Research Note (Feb 2026)**: ETH Zürich a publié la première évaluation empirique des fichiers de contexte agent (AGENTS.md/CLAUDE.md). Résultats clés sur 138 benchmarks, 12 repos :
> - Developer-written : **+4% success rate** vs baseline (pas de context file)
> - LLM-generated : **-3% success rate** (agents suivent toutes les instructions, même hors-sujet)
> - Dans tous les cas : **+20-23% inference cost**
>
> **Implication** : Incluez UNIQUEMENT les commandes build/test et le tooling spécifique. Style guides et descriptions d'architecture → docs séparés.
> Source: [Gloaguen et al., 2026](https://arxiv.org/abs/2602.11988)
```

### 2. Section token cost / token efficiency (ligne ~13382)
**Priorité: Moyenne**

Ajouter dans la table Token Cost Estimation : "CLAUDE.md avec infos non-essentielles → +20-23% inference cost (Gloaguen et al., 2026)"

### 3. Toute section conseillant de générer CLAUDE.md avec Claude
**Priorité: Haute**

Ajouter une mise en garde :

```markdown
> ⚠️ **Attention**: Les context files générés par LLM réduisent les performances des agents (-3% vs baseline). Révisez et épurez tout CLAUDE.md généré automatiquement avant de le committer.
```

---

## 🔥 Challenge (agent de révision)

**Score ajusté**: 4/5 (confirmé)

**Points manqués dans l'évaluation initiale** :
- Le ROI net de +4% (developer-written) ne compense pas toujours le +20-23% cost — le guide ne documente pas ce trade-off nulle part
- Les agents testés n'incluent pas Claude Haiku (utilisé pour les sub-agents) ni Opus — limitation à mentionner lors de l'intégration
- La section SWE-bench Lite n'est pas mentionnée (comparison baseline avec AGENTbench)

**Tension identifiée** : Si le guide mentionne d'autres études valorisant les context files, ne pas mentionner celle-ci crée un biais de sélection. Priorité d'intégration confirmée.

**Risques de non-intégration** :
- Les conseils "lean CLAUDE.md" restent des opinions sans backing empirique
- Crédibilité du guide fragilisée face aux concurrents citant ce paper
- Les utilisateurs générant leur CLAUDE.md avec Claude (pratique répandue) ne sont pas alertés du risque -3%

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| Auteurs : ETH Zürich | ✅ | arXiv abstract |
| Date de publication : 13 février 2026 | ✅ | arXiv metadata |
| +4% dev-written / -3% LLM-generated | ✅ | Perplexity search + arXiv HTML |
| +20-23% inference cost | ✅ | arXiv abstract ("over 20%") + HTML full text |
| AGENTbench : 138 instances, 12 repos | ✅ | Perplexity + arXiv HTML |
| Agents testés : Claude Code, Codex, Qwen Code | ⚠️ | Partiellement — noms de modèles exacts non vérifiables via Perplexity |
| Recommandation : build/test commands only | ✅ | arXiv HTML + blog d'analyse (jangwook.net) |

**Corrections** : Les noms de modèles spécifiques (ex. "GPT-5.2", "Qwen3-30b-coder") ont été évités — potentielle hallucination du fetcher PDF. Le paper confirme "4 coding agents" sans préciser les versions exactes dans les sources vérifiées.

---

## 🎯 Décision finale

- **Score final**: 4/5
- **Action**: Intégrer (3 points d'intégration prioritarisés)
- **Confiance**: Haute (données clés vérifiées via Perplexity + arXiv HTML)

**Next step**: Ajouter le "Research Note" callout dans `guide/ultimate-guide.md` ligne ~13395 et la mise en garde sur LLM-generated context files.

---

---

## 📣 Réception communautaire

La communauté a simplifié les résultats en "delete your CLAUDE.md" (cf. [Charly Wargnier, LinkedIn](https://www.linkedin.com/posts/charlywargnier_everyone-is-screaming-delete-your-claudemd-activity-7431988275193622528-pfBW)).

**Nuance importante à intégrer dans le guide** : la commande `/init` génère un context file LLM-generated → c'est ce type de fichier qui dégrade les performances (-3%). Les fichiers écrits manuellement restent bénéfiques (+4%).

D'autres posts (ex: [Daniel Vikulov, LinkedIn](https://www.linkedin.com/)) paraphrasent fidèlement l'étude sans valeur ajoutée — ne pas les citer comme sources indépendantes.

---

*Évaluation effectuée le 2026-02-19 | Méthode: WebFetch + Perplexity + grepai_search + agent challenge*