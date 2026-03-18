# Resource Evaluation: Anthropic System Prompts Release Notes (Opus 4.6 Update)

**Evaluated**: 2026-02-13
**Evaluator**: Claude Opus 4.6 + technical-writer agent challenge
**Target Guide**: Claude Code Ultimate Guide v3.9.9

---

## Executive Summary

**Resource**: Anthropic System Prompts Release Notes (Opus 4.6 entry, 5 Feb 2026)
**URL**: https://platform.claude.com/docs/en/release-notes/system-prompts
**Type**: Documentation officielle Anthropic

**Initial Score**: 2/5 (Marginal)
**Challenged Score**: 2/5 (Marginal)
**Final Score**: **2/5 (Marginal - Already Covered)**

**Decision**: **Ne pas intégrer. Watch only. Deuxieme evaluation de la meme URL (premiere: Jan 2026, score 2/5).**

---

## Resource Description

### Content Summary

**Type**: Official Anthropic system prompt documentation

**Key Points**:
1. **System prompts pour 4 modeles**: Opus 4.6 (5 Feb 2026), Opus 4.5, Sonnet 4.5, Haiku 4.5
2. **Guidelines de comportement**: Formatage anti-listes, ton conversationnel, pas d'emojis par defaut, CommonMark requis
3. **Regles de securite**: Armes/WMDs, code malveillant, protection des mineurs, personnalites publiques
4. **Produits beta listes**: Claude in Chrome, Claude in Excel, Cowork
5. **Systeme de reminders internes**: `image_reminder`, `cyber_warning`, `system_warning`, `ethics_reminder`, `ip_reminder`, `long_conversation_reminder`
6. **Knowledge cutoff dates**: End of May 2025 (Opus 4.5/Sonnet 4.5)

### Prior Art

**Evaluation precedente**: [`system-prompts-official-vs-community.md`](./system-prompts-official-vs-community.md) (2026-01-26, score final 2/5)

Cette evaluation avait:
- Decouvert que Anthropic publie deja les prompts officiellement
- Genere l'integration dans `guide/architecture.md:354-380` ("System Prompt Contents")
- Ajoute les entrees dans `machine-readable/reference.yaml:217-220`
- Conclu au watch-only pour cette URL

---

## Evaluation Score: 2/5 (Marginal)

### Justification

La ressource est **deja referencee et documentee** dans le guide:

| Aspect | Statut dans le guide |
|--------|---------------------|
| URL officielle | `architecture.md:358` — lien direct |
| Reference YAML | `reference.yaml:217-220` — 4 entrees |
| Opus 4.6 | 62 mentions dans 7 fichiers (pricing, adaptive thinking, API, agent teams) |
| Evaluation existante | `system-prompts-official-vs-community.md` score 2/5 |

Le contenu specifique (formatting rules, safety rules, evenhandedness) concerne **Claude.ai/Mobile**, pas Claude Code CLI. La note a `architecture.md:380` le dit deja.

---

## Comparative Analysis

| Aspect | Cette ressource (Feb 2026 update) | Notre guide |
|--------|-----------------------------------|-------------|
| Opus 4.6 model info | System prompt date 5 Feb 2026 | 62 mentions, pricing, adaptive thinking |
| Knowledge cutoff dates | "End of May 2025" explicite | Pas documente explicitement |
| Formatting rules (anti-lists, CommonMark) | Detaille | Absent (mais concerne Claude.ai, pas CLI) |
| Safety/moderation rules | Detaille | Couvert dans `security-hardening.md` (cote pratique) |
| Reminder system | 6 types listes | Absent (mais plomberie interne Claude.ai) |
| Beta products (Chrome, Excel, Cowork) | Liste | Cowork documente, Chrome/Excel en ecosystem |
| Evenhandedness guidelines | Detaille | Absent (mais hors scope CLI) |

---

## Challenge Results (technical-writer agent)

Le technical-writer a **confirme le score 2/5** avec ces observations:

### Score correct

La distinction CLI vs Claude.ai est le filtre qui justifie le 2/5. Le guide documente Claude Code, pas Claude.ai.

### Trois micro-gaps identifies (non prioritaires)

1. **Knowledge cutoff dates** pas explicites dans le guide
2. **Reminder system** non documente
3. **Frequence de MAJ** de la page non trackee dans le workflow

### Score ajuste: 2/5 (pas de changement)

### Risques de non-integration

Quasi nuls. Le seul vrai risque serait de rater une publication future du system prompt **specifique au CLI** sur cette page.

---

## Fact-Check

| Affirmation | Verifiee | Source |
|-------------|----------|--------|
| Opus 4.6 date 5 Feb 2026 | Oui | Page officielle (section header) |
| Model string `claude-opus-4-6` | Oui | Page officielle |
| Knowledge cutoff "end of May 2025" | Oui | Page officielle |
| 6 reminder types listes | Oui | Page officielle |
| CommonMark formatting requis | Oui | Page officielle (multiple sections) |
| Beta products: Chrome, Excel, Cowork | Oui | Page officielle |
| Guide reference deja cette URL | Oui | `architecture.md:358`, `reference.yaml:217` |
| Evaluation precedente existe | Oui | `system-prompts-official-vs-community.md` (score 2/5) |

**Corrections apportees**: Aucune. Toutes les affirmations verifiees.

---

## Recommendations

### Actions opportunistes

Lors du prochain passage sur `architecture.md`:

1. **Ajouter knowledge cutoff dates** par modele (end of May 2025 pour Opus 4.5/Sonnet 4.5) — info architecture utile, explique pourquoi Claude "ne sait pas" certaines choses recentes
2. **Ajouter mention du reminder system** (6 types) — explique des comportements "mysteres" (refus sur images, warnings non demandes en longues conversations)

### Ce qu'on ne fait PAS

- Pas de section dediee dans le guide
- Pas de nouveau contenu sur les formatting rules Claude.ai
- Pas d'integration des safety/evenhandedness rules (hors scope CLI)

---

## Decision finale

- **Score final**: 2/5 (Marginal)
- **Action**: Ne pas integrer. Watch only. Deja couvert.
- **Confiance**: Haute (source officielle, fact-check complet, evaluation precedente coherente)
- **Note**: Deuxieme evaluation de la meme URL. La premiere (Jan 2026) avait conclu a 2/5 et a genere l'integration dans `architecture.md:354-380`. Rien de nouveau ne justifie une mise a jour.

---

## References

- **Page officielle**: https://platform.claude.com/docs/en/release-notes/system-prompts
- **Evaluation precedente**: [`system-prompts-official-vs-community.md`](./system-prompts-official-vs-community.md)
- **Guide sections**: `architecture.md:354-380`, `reference.yaml:217-220`

---

**End of Evaluation**
