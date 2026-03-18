# Evaluation: Skill Doctor (GitHub Action)

**Date**: 2026-02-01
**Source**: [github.com/tcarac/skill-doctor](https://github.com/tcarac/skill-doctor) | [LinkedIn post](https://www.linkedin.com/posts/tomascaraccia_github-tcaracskill-doctor-a-github-activity-7422266051263995904-Ue60)
**Author**: Tomas Caraccia
**Type**: Open-source tool (GitHub Action)
**License**: Apache 2.0

---

## Résumé du contenu

- GitHub Action qui valide les Agent Skills contre la spécification officielle agentskills.io
- Vérifie: YAML frontmatter, naming conventions (lowercase, 1-64 chars), description (non-vide, max 1024), structure de fichiers, champs inattendus
- Intégration PR: commentaires détaillés + annotations inline + suggestions auto-fix
- Modes: skill unique, multiple skills, ou fichiers modifiés uniquement (optimisé CI)
- Stack: Python 3.11+, uv, pytest, Docker, Apache 2.0

## Score de pertinence: 2/5

**Justification**:

1. **Adoption quasi-nulle**: 3 stars, 0 forks, 17 commits, repo créé le 28 janvier 2026 (4 jours). Post LinkedIn: 8 likes, 0 commentaires. Aucune validation communautaire.
2. **Guide déjà exhaustif sur la structure SKILL.md**: Le guide documente extensivement le frontmatter, la structure de fichiers, les bonnes pratiques (lignes 4420-5950+ du ultimate-guide.md), incluant des quiz de validation (19 questions).
3. **agentskills.io n'est pas documenté dans le guide**: La spécification formelle n'apparaît nulle part, mais c'est un choix délibéré - le guide documente la spec Claude Code native, pas une spec tierce.
4. **Concept valide, outil immature**: L'idée de CI/CD pour skills est pertinente, mais l'outil est trop jeune pour être recommandé.
5. **Engagement LinkedIn minimal**: 8 likes sur un réseau de plusieurs millions d'utilisateurs techniques = signal de niche.

## Comparatif

| Aspect | Skill Doctor | Notre guide |
|--------|-------------|-------------|
| Structure SKILL.md | Validation automatisée | Documentation détaillée (spec + exemples) |
| Frontmatter YAML | Check programmatique | Documentation + quiz interactif |
| Bonnes pratiques naming | Enforcement via CI | Guidelines documentées |
| Spécification agentskills.io | Référence centrale | Non mentionnée (spec Claude Code native) |
| CI/CD pour skills | GitHub Action clé-en-main | Non couvert |
| Auto-fix suggestions | Oui (PR comments) | Non applicable |
| Maturité | 3 stars, 4 jours | 3.20.5, 11K+ lignes |

## Recommandations

**Action: Ne pas intégrer.**

L'outil est trop immature pour justifier une mention. Réévaluer si:
- Le repo atteint 100+ stars (signal d'adoption réelle)
- agentskills.io devient un standard reconnu au-delà des articles de blog
- D'autres outils de validation émergent (signal d'un besoin marché)

**Alternative possible** (si croissance future): Mention dans la section Skills Marketplace (ultimate-guide.md:5873) comme outil QA complémentaire.

## Challenge (auto-critique)

### Arguments pour score +1 (3/5):
- **Gap réel**: Le guide ne couvre PAS le CI/CD pour skills. Aucune section ne traite de "comment valider automatiquement ses skills en CI". C'est un pattern DevOps pertinent.
- **Spec agentskills.io absente**: La recherche Perplexity confirme que cette spec est adoptée par Spring AI, AWS Strands, et d'autres. Ne pas la mentionner est un trou.
- **Premier outil du genre**: Skill Doctor est (à date) le seul linter de skills public. Premier-mover dans une niche = potentiellement important plus tard.

### Arguments pour score -1 (1/5):
- **4 jours d'existence**: Impossible de juger la qualité ou la pérennité. Le repo pourrait être abandonné dans 2 semaines.
- **Spec non-Anthropic**: agentskills.io n'est pas maintenu par Anthropic. Claude Code a sa propre spec de skills. Documenter une spec tierce crée de la confusion.
- **Self-promotion pure**: Le post LinkedIn est de l'auteur lui-même. Zéro validation externe.

### Verdict du challenge:
Le score 2/5 tient. Le gap CI/CD pour skills est réel mais ne justifie pas d'intégrer un outil de 4 jours avec 3 stars. Le gap agentskills.io mérite une note dans la watchlist mais pas une documentation à ce stade.

### Points manqués:
- La spec agentskills.io gagne en traction (Spring AI, AWS Strands) - à surveiller indépendamment de cet outil
- Le threat model de SafeDep (safedep.io/agent-skills-threat-model) identifie des vulnérabilités dans la spec - angle sécurité potentiellement intéressant pour le guide

### Risques de non-intégration:
**Faibles.** Si l'outil explose en popularité, on l'intègre plus tard. Le guide ne perd rien à attendre. Le pattern "attendre l'adoption" a été validé pour d'autres évaluations (Remotion: score 2/5, même logique).

## Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| 3 stars GitHub | ✅ | GitHub repo (vérifié 2x) |
| 0 forks | ✅ | GitHub repo |
| 17 commits | ✅ | GitHub repo |
| Apache 2.0 license | ✅ | GitHub repo |
| Repo créé 28 jan 2026 | ✅ | GitHub repo |
| Python 3.11+ | ✅ | GitHub repo |
| 8 likes LinkedIn | ✅ | LinkedIn post |
| 0 comments LinkedIn | ✅ | LinkedIn post |
| agentskills.io = spec formelle | ✅ | Perplexity (Spring AI, AWS Strands, rushis.com) |
| Spec adoptée multi-plateforme | ✅ | Perplexity (Spring AI, AWS Strands, Medium articles) |
| Threat model exists (SafeDep) | ✅ | Perplexity (safedep.io, jan 2026) |

**Corrections apportées**: Aucune. Toutes les claims vérifiées.

## Décision finale

- **Score final**: 2/5
- **Action**: Ne pas intégrer
- **Confiance**: Haute
- **Watchlist**: Oui - réévaluer si adoption > 100 stars ou si agentskills.io devient standard Anthropic
- **Note**: La spec agentskills.io elle-même (indépendamment de cet outil) mérite une évaluation séparée si elle continue à gagner en traction