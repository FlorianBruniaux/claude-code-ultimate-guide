# Evaluation: Context-Evaluator (context-evaluator.ai)

**Date**: 2026-02-25
**Type**: URL + texte (LinkedIn post de Cédric Teyton, CTO Packmind)
**Source**: https://context-evaluator.ai/

---

## Resume du contenu

- **Outil open-source** (Apache-2.0) par Packmind (même équipe que coding-agents-matrix déjà dans le guide)
- **Scanner de fichiers CLAUDE.md, AGENTS.md, copilot-instructions.md** avec 17 évaluateurs spécialisés (13 détecteurs d'erreurs + 4 générateurs de suggestions)
- **Multi-agent**: Claude Code, Cursor, GitHub Copilot, OpenCode, OpenAI Codex
- **Dual interface**: CLI local + web UI (context-evaluator.ai)
- **Stack**: Bun, React, Tailwind CSS, TypeScript
- **GitHub**: PackmindHub/context-evaluator | 8 stars | 2 contributeurs | v0.3.0 (23 fev 2026)

---

## Score de pertinence: 3/5

**Justification**: Premier outil qui formalise des critères de qualité pour les fichiers CLAUDE.md avec des checks reproductibles. Valeur pédagogique des 17 critères même indépendamment de l'outil. Mais v0.3.0 avec 8 stars = side project expérimental, risque d'abandon réel.

---

## Comparatif

| Aspect | Context-Evaluator | Notre guide |
|--------|------------------|-------------|
| Audit CLAUDE.md | 17 évaluateurs automatisés (déterministe) | audit-prompt.md (LLM-dependent, subjectif) |
| Scope | Multi-agent (5 outils) | Claude Code spécifique |
| Maintenance context files | Détection erreurs + suggestions | Documentation des bonnes pratiques (section 3.1) |
| Maturité | v0.3.0, 8 stars, expérimental | 20K lignes, 175 templates, établi |
| Remediation | Auto-fix via AI intégré | Templates + checklists manuelles |
| Context drift detection | Oui (mismatch code/docs) | Mentionné en concept (iterative-refinement.md:253) |

---

## Recommandations

**Action**: Intégrer comme mention légère (pas de section dédiée)

1. **`guide/ai-ecosystem.md` ligne ~2064** (section Packmind Related Resources): Ajouter context-evaluator à côté de coding-agents-matrix. 3-5 lignes max.
2. **`machine-readable/reference.yaml`**: Ajouter entrée `context_evaluator` pointant vers ai-ecosystem.md
3. **Ne PAS créer de section dédiée** à 8 stars et v0.3.0
4. **Optionnel**: Lien depuis section maintenance CLAUDE.md vers ai-ecosystem pour les curieux

**Priorité**: Basse (intégrer quand opportun)

---

## Challenge (technical-writer)

- **Score ajusté**: 3/5 confirmé, justification retravaillée
- **Points manqués**: Les 17 critères concrets (le vrai trésor), le modèle de scoring, le dogfooding potentiel sur notre propre CLAUDE.md
- **Risques de non-intégration**: Quasi nuls. 8 stars = personne ne reprochera l'absence. Le risque inverse (contenu mort si outil abandonné) est plus réel.
- **Vraie valeur ajoutée**: Les critères formels d'évaluation, pas l'outil lui-même
- **Suggestion pertinente**: Faire tourner l'outil sur notre propre CLAUDE.md pour data factuelle

---

## Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| Open-source Apache-2.0 | OK | GitHub repo confirmé |
| Par Packmind (Cédric Teyton) | OK | GitHub + ai-ecosystem.md:2012 déjà référencé |
| 17 évaluateurs (13+4) | OK | Page web + README GitHub |
| Supporte Claude Code, Cursor, Copilot, OpenCode, Codex | OK | Page web |
| v0.3.0, release 23 fev 2026 | OK | GitHub releases |
| 8 stars, 2 contributeurs | OK | GitHub repo (au 25 fev 2026) |
| Gratuit ($0) | OK | Page web |
| "An AI coding agent is only as smart as the last time your context was reviewed" | Claim marketing, non vérifiable | N/A |

**Perplexity**: Aucun résultat spécifique trouvé sur context-evaluator.ai. Outil trop récent/niche pour avoir de la couverture presse.

**Corrections**: Aucune hallucination détectée. Le texte LinkedIn est fidèle aux faits du repo.

---

## Decision finale

- **Score final**: 3/5
- **Action**: Intégrer comme mention dans ai-ecosystem.md section Packmind + entrée reference.yaml
- **Confiance**: Haute (facts vérifiés, repo existe, même auteur que ressource déjà intégrée)
