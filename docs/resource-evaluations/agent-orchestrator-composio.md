# Évaluation de Ressource: Agent Orchestrator (AO)

**URL**: https://github.com/AgentWrapper/agent-orchestrator
**Type**: GitHub repository
**Date d'évaluation**: 2026-07-08
**Évaluateur**: Claude Code Ultimate Guide Team
**Version guide**: 3.40.0

---

## 📄 Résumé du contenu

- **Repo renommé** : identifié initialement sous `ComposioHQ/agent-orchestrator` dans une recherche croisée sur le pattern "PRD → tâches → build isolé → gate → merge → audit trail" présenté au meetup GenAI France (Maleus, juillet 2026). L'API GitHub redirige désormais vers `AgentWrapper/agent-orchestrator` (org renommée), même repo (`repositories/1156994049`), 8 129 stars (désormais 8 608 au 28/07/2026), license Apache-2.0
- **Ce que c'est réellement** : pas un générateur PRD→code, mais un "meta-harness agent IDE" qui supervise plusieurs CLI d'agents de code en parallèle (Claude Code, Codex, Cursor, Aider, Goose, Devin et 18 autres, 23 harnesses au total), chacun dans son propre git worktree, avec app desktop + CLI
- **Boucle de feedback automatique** : un observateur SCM (GitHub) route les échecs de CI, les commentaires de review et les conflits de merge vers la bonne session d'agent ("nudges"), documenté dans `docs/STATUS.md`
- **Télémétrie par défaut** : le renderer Electron envoie des événements PostHog anonymisés, avec enregistrement de session (chemins et URLs locaux redacted), désactivable via `VITE_AO_POSTHOG_KEY` vide
- **Jeune projet à forte croissance** : créé le 2026-02-13, 8 129 stars en moins de 5 mois, mais 416 issues ouvertes signalant un produit encore rugueux

---

## 🎯 Score de pertinence: 3/5

| Score | Signification |
|-------|---------------|
| ~~5~~ | ~~Critique, gap majeur dans le guide~~ |
| ~~4~~ | ~~Très pertinent - Amélioration significative~~ |
| **3** | **Pertinent - Complément utile** |
| ~~2~~ | ~~Marginal - Info secondaire / Redondant~~ |
| ~~1~~ | ~~Hors scope - Non pertinent~~ |

**Justification**: `guide/ecosystem/third-party-tools.md` documente déjà Conductor en détail (worktrees isolés, diff viewer, intégration GitHub/Linear, boucle CI→fix automatique) mais le présente comme macOS-only, propriétaire, limité à Claude Code + Codex. AO est le pendant open source direct de ce même pattern : cross-plateforme, Apache-2.0, 23 CLI d'agents supportés au lieu de 2. C'est un gap réel et net, mais pas critique : le pattern lui-même (worktree + CI feedback loop) est déjà documenté via Conductor, AO n'apporte pas un concept nouveau, seulement une variante OSS/cross-plateforme.

**Correction importante par rapport à la recherche initiale**: la recherche croisée transmise attribuait à ce projet une logique explicite "retry CI deux fois puis escalade humaine" présentée comme l'implémentation la plus aboutie du principe d'andon cord. Vérification directe du README, de `docs/architecture.md` et `docs/STATUS.md` : cette logique de comptage de tentatives n'apparaît nulle part dans la documentation actuelle. Le comportement réel documenté est plus simple : le daemon détecte les échecs CI/review/conflits et "nudge" l'agent concerné, sans seuil de tentatives ni escalade documentée. Ce point ne doit pas être repris tel quel dans le guide.

---

## ⚖️ Comparatif détaillé

| Aspect | Agent Orchestrator (AO) | Conductor (déjà couvert) |
|--------|--------------------------|----------------------------|
| Licence | Apache-2.0 (open source) | Propriétaire |
| Plateforme | Windows, macOS, Linux + CLI headless | macOS uniquement |
| Agents CLI supportés | 23 (Claude Code, Codex, Cursor, Aider, Goose, Devin...) | 2 (Claude Code, Codex) |
| Isolation d'exécution | Git worktree par session | Git worktree par workspace |
| Boucle CI/review/conflits | Automatique, routée vers la session (non quantifiée) | Automatique vers Claude uniquement (v0.12.0+) |
| Intégrations tierces | GitHub (SCM observer) | GitHub, Linear, Slack, VS Code |
| Télémétrie | PostHog activé par défaut (opt-out via var d'env) | Non documenté publiquement |
| Maturité | 5 mois, 416 issues ouvertes | Mature (versionné jusqu'à v0.37.0) |
| Stars | 8 129 (désormais 8 608 au 28/07/2026) | N/A (propriétaire, pas de repo public) |

---

## 📍 Recommandations

**Où intégrer**: `guide/ecosystem/third-party-tools.md`, nouvelle entrée juste après la section Conductor (ligne ~1379), présentée explicitement comme son équivalent open source cross-plateforme plutôt que comme un outil indépendant. Éviter de la rattacher à la catégorie "Full-cycle AI software factories" ajoutée dans `spec-first.md` : ce n'est pas un générateur PRD→code, ce serait une erreur de catégorisation.

**Format suggéré**: tableau attributs + section "How it works" courte + note de vigilance sur la télémétrie par défaut (cohérent avec le ton du guide sur `data-privacy.md`), sans reprendre l'affirmation non vérifiée sur la logique de retry/escalade.

---

## 🔥 Challenge

**Objection testée**: "Un outil de 5 mois avec 416 issues ouvertes, n'est-ce pas trop tôt et trop instable pour l'intégrer ?"

**Réponse**: La croissance (8 129 stars en 5 mois, soit un rythme largement supérieur à spec-kitty par exemple) et le fait qu'il comble un gap net et vérifiable (seul équivalent OSS cross-plateforme identifié à Conductor) justifient une mention. Le nombre d'issues ouvertes reflète un projet actif avec une communauté qui remonte des bugs, pas nécessairement un signal d'instabilité disqualifiant. Le score reste à 3/5 et non 4/5 précisément à cause de cette jeunesse et de l'absence de différenciation technique vérifiée au-delà du multi-CLI.

**Risque de non-intégration**: un lecteur qui a lu la section Conductor et cherche un équivalent Linux/Windows ou compatible avec un agent autre que Claude Code/Codex ne trouvera pas d'alternative documentée dans le guide.

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source/Commentaire |
|-------------|----------|---------------------|
| 8 129 stars, 1 155 forks, 416 issues ouvertes | ✅ | Vérifié via `gh api repositories/1156994049` le 2026-07-08 (redirection depuis `ComposioHQ/agent-orchestrator`) |
| Licence Apache-2.0 | ✅ | Confirmé par l'API GitHub (`license.spdx_id: Apache-2.0`) et le README |
| 23 agent CLI supportés | ✅ | Liste énumérée dans le README (claude-code, codex, aider, opencode, grok, droid, amp, agy, crush, cursor, qwen, copilot, goose, auggie, continue, devin, cline, kimi, kiro, kilocode, vibe, pi, autohand) |
| Isolation par git worktree | ✅ | Confirmé section "How it works" du README, point 3 |
| Télémétrie PostHog activée par défaut | ✅ | Confirmé section "Telemetry" du README, avec mécanisme d'opt-out documenté |
| "CI retry runs twice, then escalates" (affirmation de la recherche croisée) | ❌ Non confirmé | Recherché dans README, `docs/architecture.md`, `docs/STATUS.md` : aucune mention d'un compteur de tentatives ou d'un seuil d'escalade. Le comportement réel documenté est un "nudge" automatique sans logique de comptage explicite |
| Repo créé le 2026-02-13 | ✅ | Champ `created_at` de l'API GitHub |

---

## 🎯 Décision finale

| Critère | Valeur |
|---------|--------|
| **Score final** | 3/5 |
| **Action** | ✅ Mention dans `third-party-tools.md`, juste après Conductor, comme équivalent OSS cross-plateforme |
| **Confiance** | Haute sur les faits vérifiés (stars, licence, agents supportés, télémétrie) ; la comparaison qualitative avec Conductor reste une lecture éditoriale |
| **Point de vigilance** | Ne pas reprendre l'affirmation "retry twice then escalate" de la recherche source, non confirmée dans la documentation primaire du projet |

---

*Rapport généré manuellement pour Claude Code Ultimate Guide v3.40.0*
