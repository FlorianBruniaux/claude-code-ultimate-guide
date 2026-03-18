# Resource Evaluation: UI UX Pro Max Skill

**Date**: 2026-02-23
**Evaluator**: Claude Code (Sonnet 4.6) + technical-writer agent challenge
**Score**: 4/5

---

## Resource

| Field | Value |
|-------|-------|
| **URL** | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| **Site** | https://ui-ux-pro-max-skill.nextlevelbuilder.io/ |
| **Author** | Organisation "nextlevelbuilder" (anonyme) |
| **License** | MIT |
| **Version** | v2.2.1 (26 jan 2026) |
| **Created** | 30 nov 2025 |
| **Stars** | 33,658 (vérifiés gh CLI) |
| **Forks** | 3,327 (vérifiés gh CLI) |

---

## Summary

Skill multi-plateforme (15 assistants AI) fournissant un moteur de design intelligence pour Claude Code et ses équivalents. Engine Python offline (BM25 sur JSON de règles locales). Feature flagship v2.0 : Design System Generator → génère MASTER.md + pages/ overrides.

**Contenu** : 67 styles UI, 96 palettes couleurs, 57 typographies, 25 charts, 99 UX guidelines, 100 règles industrie.

---

## Fact-Check Results

| Claim | Status | Source |
|-------|--------|--------|
| 33,658 stars | ✅ Vérifié | `gh api repos/nextlevelbuilder/ui-ux-pro-max-skill` |
| 3,327 forks | ✅ Vérifié | gh CLI |
| Créé 30 nov 2025 | ✅ Vérifié | `created_at` gh CLI |
| Mis à jour 23 fev 2026 | ✅ Vérifié | `updated_at` gh CLI |
| Site HTTP 200 | ✅ Vérifié | `curl -s -o /dev/null -w "%{http_code}"` |
| v2.2.1 latest | ✅ Vérifié | Perplexity + releases page |
| 67 styles | ⚠️ README claim | Non compté individuellement |
| 96 palettes | ⚠️ README claim | Non compté individuellement |
| Python 80.6%, TS 18% | ✅ Vérifié | GitHub languages bar |
| BM25 engine | ✅ Vérifié | README technique |
| Auteur identifié | ⚠️ Org anonyme | "nextlevelbuilder", aucun individu nommé |

---

## Gap Analysis

| Aspect | Cette ressource | Guide (avant intégration) |
|--------|----------------|--------------------------|
| Skill design UI/UX spécialisé | ✅ Leader du marché | ❌ Absent |
| Design System Generator | ✅ Feature flagship | ❌ Absent |
| Multi-plateforme AI (15 outils) | ✅ Couvert | ⚠️ Partiel |
| Community skills section | ✅ Exemple majeur | ✅ Autres entrées présentes |

---

## Challenge (technical-writer agent)

L'agent a challengé le score et le plan avec ces arguments :

1. **Placement** : Section 5 "Skills" peut induire en erreur — ce n'est pas un skill Claude Code natif mais un outil externe avec CLI Python. Reconnu dans la documentation (sous-section dédiée "Community Skill Repositories", pas dans la mécanique de création de skills).

2. **Score ajusté initial** : 2.75/5 proposé par l'agent (avant vérification des stars). Post-vérification, 4/5 maintenu car traction organique confirmée.

3. **Sécurité** : Note `npm install -g` insuffisante → enrichie dans la doc finale avec alternative git clone et instructions d'audit.

4. **Protocole de test recommandé** (non exécuté avant intégration) :
   - Star history curve (star-history.com) → vérifier organicité
   - `npm view uipro-cli scripts` → chercher preinstall/postinstall suspect
   - Clone + lecture `search.py` head → vérifier absence de requêtes réseau runtime
   - Test Design System Generator en environnement isolé

---

## Decision

| Field | Value |
|-------|-------|
| **Score** | 4/5 |
| **Action** | Intégré dans `guide/ultimate-guide.md §5.5` |
| **Placement** | Section 5.5 Community Skill Repositories — "Design Intelligence: UI UX Pro Max" |
| **Confidence** | Haute (traction vérifiée) / Moyenne (claims fonctionnels non audités) |
| **Tests pending** | Star history curve, npm audit, search.py source review |

---

## References

- Perplexity searches : jimmysong.io mention, mcpmarket.com listing, YouTube tutorial (fev 2026), hylarucoder benchmark repo
- gh CLI verification : stars, forks, dates
- README v2.0 : Design System Generator workflow documenté
- Technical-writer agent challenge : session 2026-02-23
