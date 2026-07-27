# Évaluation de Ressource: OpenHands (All Hands AI)

**URL**: https://github.com/OpenHands/OpenHands
**Type**: GitHub repository
**Date d'évaluation**: 2026-07-08
**Évaluateur**: Claude Code Ultimate Guide Team
**Version guide**: 3.40.0

---

## 📄 Résumé du contenu

- **Anciennement OpenDevin**, plateforme open source d'agents de code cloud maintenue par All Hands AI
- **Délégation de sous-agents**: un agent planificateur principal construit un graphe de dépendances (Tier 0 exécuté en parallèle, Tier 1 démarre dès résolution de sa dépendance spécifique, pas d'attente de la fin complète de Tier 0)
- **Merge géré par un "integrator"**: fusionne les fichiers, résout les chemins d'import, connecte les appels API au frontend, fait tourner la suite de tests complète
- **Sandbox isolé**: exécution dans un environnement sécurisé, auditabilité intégrée
- **OpenHands Cloud/Enterprise**: "Agent Control Plane" pour gouvernance à l'échelle (guardrails, budgets, marketplace de plugins interne), fonctionnalités réservées à l'offre payante, pas dans le cœur open source

---

## 🎯 Score de pertinence: 4/5

| Score | Signification |
|-------|---------------|
| ~~5~~ | ~~Critique, gap majeur dans le guide~~ |
| **4** | **Très pertinent - Amélioration significative** |
| ~~3~~ | ~~Pertinent - Complément utile~~ |
| ~~2~~ | ~~Marginal - Info secondaire / Redondant~~ |
| ~~1~~ | ~~Hors scope - Non pertinent~~ |

**Justification**: `guide/ecosystem/agentic-tools.md` Section 2 (Autonomous Coding Agents) documente déjà Devin et SWE-agent en détail (tableaux comparatifs, pricing, cas d'usage) mais ne mentionne pas OpenHands nulle part dans le guide, malgré ses 79 947 stars (now 82,324 as of 2026-07-28), soit près de 3x SWE-agent et une popularité comparable à Devin. C'est l'omission la plus visible du guide sur ce segment.

---

## ⚖️ Comparatif détaillé

| Aspect | OpenHands | Devin (déjà couvert) | SWE-agent (déjà couvert) |
|--------|-----------|----------------------|---------------------------|
| Licence | Permissive (NOASSERTION API, à vérifier) | Propriétaire | MIT |
| Modèle | Multi-modèle (Claude, GPT, Gemini, open) | Propriétaire | Multi-modèle |
| Exécution parallèle native | ✅ Graphe de dépendances Tier 0/1 | ❌ Non documenté | ❌ Séquentiel |
| Gouvernance/audit trail complet | ⚠️ Réservé à Cloud/Enterprise (payant) | N/A (boîte noire) | ❌ |
| Prix | Gratuit (self-host) + Cloud payant | $20-$500+/mo | Gratuit (self-host requis) |
| Stars | 79 947 (now 82,324 as of 2026-07-28) | N/A (closed source) | 19 300+ |

---

## 📍 Recommandations

**Où intégrer**: `guide/ecosystem/agentic-tools.md`, nouvelle entrée "2.4 OpenHands (All Hands AI)" dans la Section 2 (Autonomous Coding Agents), juste après SWE-agent (2.2) et avant Claude Code en mode headless (2.3), ou en fin de section pour éviter de renuméroter l'existant.

**Format suggéré**: même structure que Devin/SWE-agent (tableau attributs + "What is X" + "When to choose X"), avec accent sur le pattern de graphe de dépendances Tier 0/Tier 1, qui est son point différenciant réel face à Devin.

---

## 🔥 Challenge

**Objection testée**: "OpenHands n'est-il pas juste un SWE-agent avec plus de stars ?"

**Réponse**: Non, la différence structurelle est l'exécution parallèle par graphe de dépendances (SWE-agent est séquentiel, conçu pour un seul GitHub issue à la fois) et l'existence d'une couche d'intégration/merge automatisée. C'est le candidat OSS le plus proche du pattern "build isolé parallèle + merge" du talk WeScale/Maleus, avec Devin comme seul concurrent direct côté propriétaire.

**Risque de non-intégration**: un lecteur cherchant un équivalent OSS auto-hébergeable à Devin ne le trouvera pas dans le guide alors qu'il existe et qu'il est plus mature que la plupart des alternatives déjà citées.

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source/Commentaire |
|-------------|----------|---------------------|
| 79 947 stars, 10 194 forks | ✅ | Vérifié via `gh api repos/OpenHands/OpenHands` le 2026-07-08 (now 82,324 stars as of 2026-07-28) |
| Push le plus récent | ✅ | 2026-07-08, très activement maintenu |
| Licence | ⚠️ | `NOASSERTION`, à vérifier manuellement (le repo affiche historiquement MIT côté doc, mais l'API ne le confirme pas automatiquement) |
| Graphe de dépendances Tier 0/1 | ⚠️ Partiellement vérifié | Confirmé par la documentation officielle OpenHands SDK (docs.openhands.dev/sdk/guides/agent-delegation) citée dans la recherche, non testé en pratique |
| "Agent Control Plane" réservé au payant | ⚠️ Non vérifié en détail | Repris de la description produit officielle, roadmap possible plutôt que fonctionnalité shippée à 100% |

---

## 🎯 Décision finale

| Critère | Valeur |
|---------|--------|
| **Score final** | 4/5 |
| **Action** | ✅ Intégrer dans `agentic-tools.md` Section 2 |
| **Confiance** | Haute (star count et activité vérifiés directement via API GitHub) |
| **Point de vigilance** | Vérifier la licence exacte et ne pas surestimer les capacités de gouvernance de la version gratuite (le Control Plane est vraisemblablement payant) |

---

*Rapport généré manuellement pour Claude Code Ultimate Guide v3.40.0*
