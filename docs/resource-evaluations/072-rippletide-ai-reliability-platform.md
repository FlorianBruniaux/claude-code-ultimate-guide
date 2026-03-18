# Resource Evaluation #072 — Rippletide: AI Reliability Platform

**Source:** [Rippletide Documentation](https://rippletide.com) / [llms-full.txt](https://rippletide.com/llms-full.txt)
**Type:** Documentation officielle — plateforme SaaS (eval, mémoire persistante, raisonnement déterministe)
**Evaluated:** 2026-02-28

---

## 📄 Résumé du contenu

Rippletide est une plateforme de fiabilité IA articulée autour de trois piliers:

1. **Eval** — Détection d'hallucinations, CLI installable via `npx rippletide`, intégration CI/CD, knowledge sources (fichiers locaux, Pinecone, PostgreSQL)
2. **Context Graph** — Mémoire persistante cross-session exposée via MCP server (7 outils, 4 ressources), compatible Claude Code, Claude Desktop, Cursor et VS Code
3. **Decision Runtime** — Raisonnement déterministe via hypergraph (Q&A structurés, tags, actions, state predicates), claim interne: "<1% d'hallucinations"

**Points d'intégration avec Claude Code:**
- Config `.mcp.json` documentée pour brancher le MCP server Rippletide
- Self-hosted possible (Node.js >= 18, déploiement Railway one-click)
- LangChain integration (drop-in LLM)
- Amazon Bedrock connector disponible

---

## 🎯 Score de pertinence

| Score | Signification |
|-------|---------------|
| 5 | Essentiel — Gap majeur dans le guide |
| 4 | Très pertinent — Amélioration significative |
| 3 | Pertinent — Complément utile |
| **2** | **Marginal — Info secondaire** |
| 1 | Hors scope — Non pertinent |

**Score final: 2/5**

**Justification:** Rippletide couvre un use case réel (mémoire persistante cross-session via MCP) mais reste un produit SaaS tiers sans adoption communautaire visible. Le guide documente déjà les MCP servers en détail et liste les patterns d'intégration. Rippletide serait au mieux une mention dans une liste de serveurs MCP tiers disponibles, pas un sujet à part entière. Claims de performance non vérifiables ("<1% hallucinations", "85% → 96% resolution rate") sans méthodologie publiée. Pricing non documenté. Pas de GitHub stars ni metrics Discord mentionnés.

---

## ⚖️ Comparatif

| Aspect | Cette ressource | Notre guide |
|--------|----------------|-------------|
| MCP server pour mémoire persistante | ✅ Documenté (7 outils, 4 resources) | ✅ Pattern MCP couvert, serveurs tiers listés |
| Config `.mcp.json` Claude Code | ✅ Exemple documenté | ✅ Documenté extensivement |
| Eval hallucinations + CI/CD | ✅ CLI npm + pipeline | ❌ Absent (testing LLM outputs non couvert) |
| Self-hosted AI reliability | ✅ Railway one-click | ❌ Non couvert |
| Claims performance vérifiables | ❌ Marketing sans méthodologie | ✅ Stats documentées avec sources |
| Adoption / communauté | ❌ Aucune métrique | ✅ Ressources avec engagement mesurable |

---

## 📍 Recommandations

**Action: Ne pas intégrer (score 2 = mention minimale ou watch only)**

1. **Pourquoi pas d'intégration directe**: Le guide couvre déjà les MCP servers et les patterns d'intégration. Ajouter Rippletide n'apporterait pas de valeur nette par rapport au contenu existant — ce serait une liste de serveurs tiers, pas un concept enseignable
2. **Exception possible**: Si Rippletide gagne en adoption et publie des benchmarks vérifiables, l'angle "eval CLI pour CI/CD" (pilier 1) devient pertinent pour la section testing/qualité du guide
3. **Point positif à retenir**: Le `llms.txt` de Rippletide est un bon exemple de documentation structurée pour LLM consumption, pertinent pour la section machine-readable du guide

**Ce qu'il ne faut PAS faire:**
- Ne pas citer les claims de performance sans source vérifiable
- Ne pas créer une section dédiée aux plateformes de fiabilité IA tierces (trop large, hors scope)

---

## 🔥 Challenge (technical-writer)

**Score initial proposé:** 2/5
**Score après challenge:** 2/5 (maintenu)

**Arguments pour augmenter le score:**

1. **MCP server natif** — Rippletide expose un vrai MCP server avec 7 outils documentés, compatible Claude Code. C'est concret, pas juste marketing
2. **Eval CLI unique** — `npx rippletide` pour détecter les hallucinations en CI/CD est un use case absent du guide. Gap réel
3. **llms.txt exemplaire** — Documentation structurée pour LLM consumption, valeur pour la section machine-readable

**Pourquoi le score reste 2/5:**

- L'angle MCP est couvert: le guide documente les patterns MCP, pas les serveurs individuels. Lister Rippletide dans une liste de serveurs tiers n'apporte pas de contenu enseignable
- L'angle eval CI/CD est potentiellement intéressant mais la source est le marketing d'un produit commercial sans validation externe. Citer un claim "<1% hallucinations" sans méthodologie publiée serait une erreur factuelle par association
- Le llms.txt peut être noté comme exemple de bonne pratique, mais c'est une mention marginale dans une section existante, pas un nouveau contenu

**Critique constructive:**
> "L'angle eval CLI est le seul gap réel. Mais baser une section du guide sur les claims marketing d'un SaaS sans traction visible serait une erreur. Si Rippletide publie des benchmarks ou atteint une adoption mesurable, réévaluer."

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| MCP server avec 7 outils et 4 resources | ✅ | llms-full.txt (liste explicite) |
| Config `.mcp.json` documentée | ✅ | llms-full.txt (exemple de config) |
| CLI via `npx rippletide` | ✅ | llms-full.txt (setup instructions) |
| Compatible Claude Code, Desktop, Cursor, VS Code | ✅ | llms-full.txt (liste clients) |
| Self-hosted Node.js >= 18 + Railway | ✅ | llms-full.txt (self-hosting section) |
| LangChain drop-in + Amazon Bedrock | ✅ | llms-full.txt (integrations) |
| "<1% hallucinations" | ⚠️ | Claim interne, aucune méthodologie publiée |
| "85% → 96% resolution rate" | ⚠️ | Claim interne, contexte non précisé |
| Pricing documenté | ❌ | Absent du llms-full.txt |
| GitHub stars / Discord metrics | ❌ | Non mentionnés |

---

## 🎯 Décision finale

- **Score final**: 2/5
- **Action**: Watch only — mention minimale possible si Rippletide gagne en traction ou publie des benchmarks
- **Confiance**: Haute (fact-check complet, claims non vérifiables clairement identifiés)
- **Seule intégration justifiable**: Note dans la section machine-readable/llms.txt du guide citant Rippletide comme exemple de documentation bien structurée pour LLM consumption
