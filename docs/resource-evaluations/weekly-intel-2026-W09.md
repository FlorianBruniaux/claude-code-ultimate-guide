# Évaluation Ressource: Veille hebdomadaire Anthropic/Claude Code — Semaine W09 2026

**Source**: Texte copié (rapport de veille interne)
**Type**: Rapport de veille structuré — 6 sujets, sources multi-canaux
**Période couverte**: 24 février – 1er mars 2026
**Canaux**: GitHub anthropics/claude-code, blog Anthropic, docs/release notes, X @AnthropicAI
**Date d'évaluation**: 2026-03-02
**Évaluateur**: Claude Sonnet 4.6
**Reviewer**: technical-writer agent

---

## 📄 Résumé du contenu

- **Claude Code v2.1.63** (27 fév): nouvelles slash commands bundlées `/simplify` + `/batch`, HTTP hooks (POST JSON → URL), partage config/auto-memory entre worktrees du même repo, nouvel env var `ENABLE_CLAUDEAI_MCP_SERVERS=false`, série de fixes memory leaks critiques
- **Model deprecations urgentes**: `claude-3-haiku-20240307` deprecated le 19 fév, retirement API le **20 avril 2026** (7 semaines), replacement recommandé: `claude-haiku-4-5-20251001`
- **Acquisition Vercept** (24 fév): startup vision/GUI automation, équipe rejoint Anthropic pour renforcer computer use — contextuel, pas de changement API immédiat
- **Opus 3 deprecation update**: Opus 3 reste accessible via canal dédié + Substack "Claude's Corner" — anecdotique pour le guide
- **Anthropic vs Department of War**: lignes rouges (pas de surveillance masse, pas d'armes autonomes) — hors scope technique
- **Cowork: plugins + tâches planifiées** (24-25 fév): marketplace plugins, contrôles admin, scheduled tasks — audience non-dev, hors scope

---

## 🎯 Score de pertinence: 4/5

**Score initial préliminaire**: 4/5
**Score challenge agent**: 3/5 (report complet), 5/5 (v2.1.63 isolé)
**Score final retenu**: **4/5** — le rapport contient 2 éléments haute valeur + 1 urgence deadline

**Justification**: Le rapport agrège des infos de valeurs très différentes. Si on exclut les 50% hors scope (Cowork, DoW, Opus 3 Substack), les items techniques restants justifient une intégration active:
- HTTP hooks = **gap réel** dans le guide (section hooks ne couvre que shell scripts)
- v2.1.63 release tracking = mise à jour mécanique du YAML + MD
- Haiku 3 retirement le 20/04/2026 = **urgence actionnable dans 7 semaines**

---

## ⚖️ Comparatif

| Aspect | Ce rapport | Guide actuel |
|--------|-----------|--------------|
| HTTP hooks (nouveau type) | ✅ Documenté + exemple config | ❌ Absent — seulement hooks shell |
| v2.1.63 dans release tracking | ✅ Détails CHANGELOG | ❌ Dernier tracké = 2.1.59 |
| Worktree config sharing | ✅ Confirmé | ⚠️ Worktrees couverts mais pas ce détail |
| Haiku 3 retirement deadline | ✅ Date précise (20/04/2026) | ❌ Absent ou non à jour |
| Bundled `/simplify` + `/batch` | ✅ Confirmé | ⚠️ `/simplify` existe comme skill custom — confusion possible |
| Cowork features | ✅ Couvert | ✅ Hors scope volontairement |
| DoW/Vercept/Opus 3 Substack | ✅ Couvert | ✅ Hors scope technique |

---

## 📍 Recommandations

### Items à intégrer (score ≥ 4/5 individuel)

**1. Claude Code v2.1.63 → Release tracking**
- Fichiers: `machine-readable/claude-code-releases.yaml` + `guide/claude-code-releases.md`
- Action: Ajouter versions 2.1.60 → 2.1.63 (le script `./scripts/update-cc-releases.sh` a déjà les données)
- Priorité: **Haute** (release récente, notre tracking a 4 versions de retard)

**2. HTTP hooks → Section Hooks du guide**
- Fichier: `guide/ultimate-guide.md` (section 7.x Hooks)
- Action: Ajouter sous-section "HTTP Hooks" avec config et cas d'usage (intégrations CI/CD, webhooks)
- Priorité: **Haute** (nouveau type de hook, absent du guide, pertinent pour intégrations enterprise)
- Config minimal documentée:
  ```json
  { "type": "http", "url": "https://...", "allowedEnvVars": ["MY_TOKEN"] }
  ```

**3. Haiku 3 API retirement → Section modèles**
- Fichier: `guide/ultimate-guide.md` (section modèles) + potentiellement dans la section entreprise/API
- Action: Note avec deadline `claude-3-haiku-20240307` → retirement 20/04/2026, migration vers `claude-haiku-4-5-20251001`
- Priorité: **Urgente** (deadline < 7 semaines au moment de l'évaluation)

### Items à rejeter (hors scope)

- Cowork plugins/scheduled tasks: audience non-dev, hors périmètre
- Acquisition Vercept: contextuel, pas d'impact technique sur CC
- DoW statements: politique/gouvernance, hors scope guide technique
- Opus 3 + Claude's Corner: anecdotique pour guide développeurs

---

## 🔥 Challenge (technical-writer)

**Points clés du challenge agent**:

- Score révisé à la baisse pour le rapport entier (3/5), mais 5/5 pour les items extraits
- **Avertissement principal**: la fiabilité de v2.1.63 était à vérifier — script `update-cc-releases.sh` a confirmé que la version est réelle avec le CHANGELOG officiel ✅
- HTTP hooks = item le plus intéressant, gap réel confirmé par grepai search
- **Haiku 3 deadline sous-priorisée** dans l'évaluation initiale — urgence réelle à 7 semaines
- Recommande exclusion explicite des 50% hors scope avec justification

**Score ajusté**: 4/5 maintenu (le challenge agent score 3/5 pour le rapport brut, mais 4/5 après extraction des items pertinents)

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| v2.1.63 publiée le 27 fév 2026 | ✅ | CHANGELOG officiel via `./scripts/update-cc-releases.sh` |
| `/simplify` et `/batch` bundlées dans 2.1.63 | ✅ | CHANGELOG officiel: "Added /simplify and /batch bundled slash commands" |
| HTTP hooks dans v2.1.63 | ✅ | CHANGELOG officiel: "Added HTTP hooks, which can POST JSON to a URL and receive JSON" |
| Worktree config sharing dans v2.1.63 | ✅ | CHANGELOG officiel: "Project configs & auto memory now shared across git worktrees" |
| `ENABLE_CLAUDEAI_MCP_SERVERS` env var | ✅ | CHANGELOG officiel |
| Memory leak fixes (liste longue) | ✅ | CHANGELOG officiel (12+ fixes distincts) |
| "Task tool replaced by Agent tool" | ❌ | NON présent dans le CHANGELOG v2.1.63 — info probablement fausse ou mal attribuée par la source Reddit |
| Haiku 3 retirement le 20 avril 2026 | ⚠️ | Sourced depuis docs officielles platform.claude.com — non re-vérifié directement ici |
| Python SDK v0.72.0 dernière version | ⚠️ | Suspect (date octobre 2025) — SDK a probablement évolué depuis |
| Acquisition Vercept (24 fév 2026) | ⚠️ | Multi-sources presse (Forbes, MLQ, TechCrunch) — vraisemblable mais pas vérifié blog officiel |

**Corrections apportées**:
- "Task tool replaced by Agent tool" retiré du plan d'intégration (non confirmé CHANGELOG officiel)
- Python SDK info ignorée (non pertinente pour le guide + données potentiellement obsolètes)

---

## 🎯 Décision finale

- **Score final**: 4/5
- **Action**: Intégrer (3 items ciblés: v2.1.63 tracking, HTTP hooks section, Haiku 3 deadline)
- **Confiance**: Haute pour items CC (CHANGELOG officiel vérifié) / Moyenne pour model deprecations

### Prochaines actions prioritaires

1. `./scripts/update-cc-releases.sh` → intégrer v2.1.60 à 2.1.63 dans le YAML + MD
2. Section HTTP hooks dans `guide/ultimate-guide.md` §7 (Hooks)
3. Note urgente Haiku 3 retirement (20/04/2026) dans section modèles

---

*Évaluation réalisée le 2026-03-02 | Claude Sonnet 4.6 | Challenge: technical-writer agent*
