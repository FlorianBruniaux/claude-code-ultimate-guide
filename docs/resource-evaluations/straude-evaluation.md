# Évaluation de Ressource: Straude (straude.com)

**Source**: [straude.com](https://straude.com) / [npm: straude](https://www.npmjs.com/package/straude)
**Type**: Outil communautaire (CLI npm)
**Producteur**: oscar.hong2015@gmail.com (indépendant)
**Date d'analyse**: 2026-03-04
**Méthode**: Inspection directe du code source (`npm pack straude@0.1.9`, lecture des fichiers compilés)
**Guide cible**: Claude Code Ultimate Guide

---

## 📄 Résumé du contenu

Straude est un dashboard social pour tracker et partager sa consommation Claude Code. L'outil pousse les stats d'usage locales (tokens, coûts, modèles) vers une plateforme partagée avec leaderboard, streaks, et rang global.

**Flux technique**:
1. Authentification OAuth via navigateur → token stocké dans `~/.straude/config.json`
2. Collecte via `ccusage daily --json` (outil officiel Claude Code) et `@ccusage/codex`
3. POST des données agrégées sur `https://straude.com/api/usage/submit`

**Données envoyées au serveur** (par jour):
- Coût en USD
- Tokens : input, output, cache creation, cache read, total
- Modèles utilisés (ex: `claude-sonnet-4-6`, `claude-opus-4-6`)
- Breakdown coût par modèle
- Hash SHA256 des données brutes ccusage
- `device_id` : UUID aléatoire généré à la première utilisation
- `device_name` : hostname de la machine (ex: `prenom-macbook.local`)

**Ce qui n'est PAS envoyé**: fichiers, code source, conversations, clés API.

---

## 🎯 Score de pertinence: 3/5 (Intégration partielle)

| Score | Signification |
|-------|---------------|
| 5 | Essentiel - Gap majeur dans le guide |
| 4 | Très pertinent - Amélioration significative |
| **3** | **Pertinent - Complément utile** |
| 2 | Marginal - Info secondaire |
| 1 | Hors scope - Non pertinent |

### Justification

Notre guide documente déjà `ccusage` (l'outil de référence) et `ccburn`. Straude couvre un angle différent — le tracking social — qui n'était pas documenté. La pertinence est réelle mais limitée : c'est un outil de niche (leaderboard), encore très jeune (13 jours à la date d'analyse), sans historique de confiance ni politique de confidentialité publiée.

Le score 3/5 se justifie par:
- Angle unique (social tracking) non couvert ailleurs dans le guide
- Analyse de sécurité disponible et factuelle
- Usage réel possible sans risque majeur identifié
- Maturité insuffisante pour un score plus élevé

---

## 🔍 Analyse de sécurité détaillée

### Inspection du code source

Le package a été inspecté directement depuis le registre npm (`npm pack straude@0.1.9`) et les fichiers compilés lus intégralement. Pas d'obfuscation détectée.

**Architecture** (20 fichiers, 35KB non compressés):

```
dist/
├── index.js              # CLI entry point
├── config.js             # DEFAULT_API_URL = "https://straude.com"
├── commands/
│   ├── login.js          # OAuth browser-based (poll + token save)
│   ├── push.js           # Collecte ccusage + POST /api/usage/submit
│   └── status.js         # GET /api/users/me/status
└── lib/
    ├── auth.js           # Lecture/écriture ~/.straude/config.json
    ├── api.js            # fetch() avec Bearer token
    ├── ccusage.js        # exec("ccusage daily --json")
    └── codex.js          # exec("npx @ccusage/codex daily --json")
```

### Points positifs

- Token stocké avec permissions `0600` (lecture propriétaire uniquement)
- Pas d'accès au filesystem au-delà de `~/.straude/config.json`
- Pas de daemon ou persistence système (pas de crontab, launchd, systemd)
- Payload limité aux métriques agrégées, cohérent avec la description
- Option `--dry-run` pour inspecter sans envoyer

### Points de vigilance

| Risque | Niveau | Détail |
|--------|--------|--------|
| Projet très récent | Moyen | Créé 2026-02-18, 10 versions en 13 jours, pas d'audit externe |
| Hostname envoyé | Faible | `device_name = os.hostname()` → souvent identifiable |
| Pas de politique confidentialité | Moyen | Aucune mention légale sur straude.com à date |
| Données sur serveur tiers | Faible | Coûts et tokens publiés partiellement (rang global) |
| Dépendance transitoire | Faible | Installe `@ccusage/codex@18` via npx sans confirmation explicite |

### Verdict sécurité

**Pas de malware ni de comportement malveillant détecté.** Le code est lisible, cohérent, et fait ce qu'il dit. Les risques sont ceux d'un projet indie jeune sans track record : absence de garanties sur la pérennité du service, la gestion des données, et la confidentialité des métriques.

---

## ⚖️ Comparatif avec l'existant

| Aspect | ccusage | ccburn | Straude |
|--------|---------|--------|---------|
| Tracking local | ✅ Complet | ✅ Visuel | ✅ Via ccusage |
| Partage/leaderboard | ❌ | ❌ | ✅ Unique |
| Streak / gamification | ❌ | ❌ | ✅ |
| Données envoyées serveur | ❌ | ❌ | ✅ (métriques agrégées) |
| Audit de sécurité | N/A | N/A | Fait (2026-03-04) |
| Maturité | ✅ Stable | ✅ Stable | ⚠️ Jeune |
| Open source | ✅ | ✅ | ⚠️ Code compilé only |

---

## 📍 Recommandations

### Action: Intégrer dans third-party-tools.md

**Raisons**:
1. Angle unique (social tracking) non couvert ailleurs
2. Analyse de sécurité factuelle disponible — bonne occasion de documenter la bonne pratique d'inspecter un outil avant de le lancer
3. Le guide a déjà ccusage et ccburn ; Straude complète logiquement la section

### Ce qui a été intégré

- Entrée complète dans `guide/third-party-tools.md` (section Token & Cost Tracking)
- Description fonctionnelle, tableau des données transmises, notes de sécurité
- Recommandation `--dry-run` mise en avant

### Éléments à surveiller (follow-up recommandé)

- Publication d'une politique de confidentialité sur straude.com
- Maturité du projet (stars GitHub, adoption communautaire)
- Éventuels rapports d'incidents ou audits externes

---

## 🔥 Challenge

**Points de résistance potentiels**:

1. "Un outil de 13 jours mérite-t-il une entrée dans le guide ?"

   Réponse : Oui, à condition de contextualiser clairement la maturité et les risques — ce qui est fait. Le guide documente déjà des outils récents (RTK). L'analyse de sécurité ajoute de la valeur indépendamment de l'outil lui-même.

2. "L'envoi de données usage vers un tiers est-il acceptable ?"

   Réponse : C'est un choix utilisateur, pas une décision du guide. Notre rôle est d'informer clairement ce qui est transmis (fait), pas de décider à la place de l'utilisateur.

3. "Le code source n'est pas open source, juste compilé lisible."

   Point valide. Noté comme limitation dans la fiche. Le TypeScript compilé sans minification reste lisible et auditable, ce qui est suffisant pour une analyse de surface.

**Verdict challenge**: Score 3/5 maintenu. Intégration justifiée avec les guardrails documentés.

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| Créé le 2026-02-18 | ✅ | `npm view straude time.created` |
| Version 0.1.9, 10 releases | ✅ | npm registry JSON |
| Maintenu par oscar.hong2015@gmail.com | ✅ | npm registry JSON |
| Token stocké en 0600 | ✅ | `dist/lib/auth.js` ligne `writeFileSync(..., { mode: 0o600 })` |
| Hostname envoyé | ✅ | `dist/commands/push.js` : `device_name: hostname()` |
| Données envoyées = métriques agrégées uniquement | ✅ | Corps du POST dans `push.js`, aucun accès fs autre que `~/.straude` |
| Pas de policy confidentialité | ✅ | straude.com inspecté 2026-03-04 |
| DEFAULT_API_URL = https://straude.com | ✅ | `dist/config.js` |

---

## 🎯 Décision finale

| Critère | Valeur |
|---------|--------|
| **Score final** | 3/5 |
| **Action** | ✅ Intégré (third-party-tools.md) |
| **Confiance** | Haute (code source inspecté directement) |

**Résumé**: Outil unique pour le tracking social de consommation Claude Code. Analyse de sécurité rassurante sur les risques malveillants, réserves légitimes sur la maturité et l'absence de politique de confidentialité. Intégration avec guardrails clairs.

---

## 📚 Références

- Fiche dans le guide: `guide/third-party-tools.md` (section Token & Cost Tracking, après ccburn)
- Package npm: https://www.npmjs.com/package/straude
- Site: https://straude.com
- Code inspecté: `npm pack straude@0.1.9` → 20 fichiers, 35KB