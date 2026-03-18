---
title: "Veille hebdomadaire Anthropic (17-23 fev 2026)"
type: "weekly-watch"
date: "2026-02-22"
score: 3
action: "partial-integration"
sources:
  - "Texte copie (digest agregateur, pas d'URL)"
---

# Veille hebdomadaire Anthropic (17-23 fev 2026)

## Resume

Digest agregateur couvrant Sonnet 4.6, Claude Code Security, CC v2.1.49-v2.1.50, Automatic Prompt Caching API, model deprecations, et activite Twitter.

## Score: 3/5

**Justification**: Digest de sources primaires (blog Anthropic, CHANGELOG GitHub, Twitter). 50% deja documente dans le guide. La valeur reelle = signal de 2-3 gaps : prompt caching API (zero couverture), model deprecations (zero couverture), env vars manquantes. Score 3 (baisse de 4 → 3 apres challenge) : c'est un trigger de recherche, pas une source citable — pas d'URL, claims API non verifiables directement.

## Gaps identifies

| Gap | Localisation | Priorite |
|-----|-------------|----------|
| Prompt caching API (`cache_control`) | guide/ultimate-guide.md (Cost Optimization) | **P1** |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` env var | guide/ultimate-guide.md (env vars table) | **P1** |
| `CLAUDE_CODE_SIMPLE` env var clarification | guide/ultimate-guide.md (env vars table) | **P1** |
| Model deprecations (Haiku 3 → 20 avril 2026) | guide/ultimate-guide.md ou architecture.md | P2 |
| `background: true` agent field | guide/ultimate-guide.md (agents section) | P2 |
| `claude agents` CLI command | guide/ultimate-guide.md (agents section) | P2 |
| Worktree hooks `WorktreeCreate`/`WorktreeRemove` | guide/ultimate-guide.md (worktree section) | P3 |

## Fact-Check

| Affirmation | Statut | Source |
|-------------|--------|--------|
| Sonnet 4.6 = default model | ✅ Verifie | ultimate-guide.md:1765 |
| CC v2.1.49/v2.1.50 dates 19-20 fev | ✅ Verifie | claude-code-releases.md:27-51 |
| Claude Code Security research preview | ✅ Verifie | security-hardening.md:780-832 |
| Haiku 3 deprecated 19 fev 2026, retirement 20 avril | ✅ Verifie | Perplexity → platform.claude.com/docs/model-deprecations |
| "Automatic" Prompt Caching (zero config) | ⚠️ Incorrecte | Anthropic utilise des breakpoints **explicites** (`cache_control`), pas automatiques. Perplexity confirme : "developer-controlled through explicit cache breakpoints, not automatic" |
| Sonnet 3.7 / Haiku 3.5 retires | ⚠️ Non verifie | Pas retrouve dans sources Perplexity. A verifier sur docs.anthropic.com/release-notes |
| Pricing prompt caching : 90% de reduction | ✅ Verifie | Cache reads = 0.1x base price (Perplexity + docs Anthropic) |

## Actions P1 (effectuees)

1. **Prompt caching** → Strategy 6 ajoutee dans Cost Optimization Strategies (ultimate-guide.md ~1912)
2. **Env vars** → `CLAUDE_CODE_DISABLE_1M_CONTEXT` et `CLAUDE_CODE_SIMPLE` ajoutes a la table principale (ultimate-guide.md ~19862)

## Challenge (technical-writer)

- **Score ajuste** : 3/5 (baisse de 4 → 3)
- **Raison** : Digest sans URL = source non citable. 50% deja couvert. La valeur = trigger de recherche primaire.
- **Risque principal** : Claim "automatic prompt caching" est incorrect — Anthropic requiert `cache_control` explicite. Ne pas integrer cette formulation.
- **Next steps** : Verifier Sonnet 3.7/Haiku 3.5 sur docs officiels avant integration P2.
