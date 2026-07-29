---
name: audit-prose
description: Add descriptive prose to bare sections in whitepapers (FR + EN) using 9 parallel agents
argument-hint: "[wp-number|all]"
---

# Audit Prose — Enrichissement des Sections Bare

Ajoute de la prose descriptive (2-4 phrases) devant chaque section "bare" des whitepapers.
Une section "bare" = heading suivi directement d'une table, code block, ou liste sans paragraphe d'intro.

## Usage

```
/audit-prose        # Tous les WPs (00-08), FR + EN
/audit-prose 07     # WP07 seulement (FR + EN)
/audit-prose 03 07  # WP03 et WP07 seulement
```

## Définition "Bare Section"

Section (`##` ou `###`) suivie DIRECTEMENT par :
- Une table Markdown (`|`)
- Un code block (` ``` `)
- Une liste à puces (`-`) ou numérotée

Sans paragraphe d'introduction (minimum 2 phrases).

## Règles Strictes (non négociables)

1. **NE JAMAIS** terminer un paragraphe par `:` avant une liste à puces → bug Typst qui fusionne les bullets en inline
2. **NE PAS** inventer de chiffres, métriques, ou citations
3. **NE PAS** ajouter de callouts (`:::`), Mermaid, ou scénarios persona
4. **NE PAS** dépasser +15% de lignes par fichier
5. Versions maintenues à **3.27.6**
6. Prose EN = anglais naturel, **pas** de traduction mot-à-mot du FR
7. Chaque ajout = **minimum 2 phrases, maximum 4 phrases**

## Exemple de Transformation

```
AVANT :
### Exit Codes
| Code | Signification |
|------|---------------|
| 0    | Autorisé      |

APRÈS :
### Exit Codes
Les hooks communiquent avec Claude Code via des codes de sortie standardisés.
C'est le mécanisme qui permet de bloquer ou autoriser une action en temps réel,
sans intervention humaine.

| Code | Signification |
|------|---------------|
| 0    | Autorisé      |
```

## Workflow : 9 Agents Parallèles

### Sources de contexte

- `machine-readable/reference.yaml` : mapping sujets → lignes du guide principal
- `guide/ultimate-guide.md` : guide de référence (aux lignes indiquées dans reference.yaml)
- Connaissance Claude Code (v3.27.6, MCP, hooks, agent teams, etc.)

### Mapping WPs

| # | FR | EN | ~Bare sections |
|---|----|----|----------------|
| 00 | `whitepapers/fr/00-introduction-serie.qmd` | `whitepapers/en/00-series-introduction.qmd` | ~10 |
| 01 | `whitepapers/fr/01-prompts-efficaces.qmd` | `whitepapers/en/01-effective-prompts.qmd` | ~14 |
| 02 | `whitepapers/fr/02-personnalisation.qmd` | `whitepapers/en/02-customization.qmd` | ~18 |
| 03 | `whitepapers/fr/03-securite.qmd` | `whitepapers/en/03-security.qmd` | ~20 |
| 04 | `whitepapers/fr/04-architecture.qmd` | `whitepapers/en/04-architecture.qmd` | ~14 |
| 05 | `whitepapers/fr/05-equipe.qmd` | `whitepapers/en/05-team.qmd` | ~20 |
| 06 | `whitepapers/fr/06-privacy.qmd` | `whitepapers/en/06-privacy.qmd` | ~12 |
| 07 | `whitepapers/fr/07-guide-reference.qmd` | `whitepapers/en/07-reference-guide.qmd` | ~36 |
| 08 | `whitepapers/fr/08-agent-teams.qmd` | `whitepapers/en/08-agent-teams.qmd` | ~16 |

### Exécution

**Si argument = numéro WP spécifique** : lancer 1 agent pour cette paire FR/EN uniquement.

**Si pas d'argument (ou "all")** : créer une équipe `audit-prose-{date}` et lancer 9 agents en parallèle.

Pour chaque WP ciblé, lancer un agent avec ce prompt :

```
Tu es un éditeur technique senior. Ta mission : ajouter de la PROSE DESCRIPTIVE
aux sections "bare" du whitepaper [XX - Titre].

## Définition "bare section"
Section (## ou ###) suivie DIRECTEMENT par une table, un code block, ou une
liste à puces, SANS paragraphe d'introduction (2+ phrases).

## Ce que tu fais
Pour CHAQUE bare section identifiée :
1. Ajouter 2-4 phrases AVANT le contenu structuré
2. Chaque phrase apporte une INFO NOUVELLE : le pourquoi, le quand utiliser,
   les implications, le choix de design, ou le contexte pratique
3. PAS de reformulation de ce qui suit — COMPLETER avec du contexte manquant

## Sources de contexte
- `machine-readable/reference.yaml` : mapping complet sujets → guide principal
- Ta connaissance de Claude Code (v3.27.6, MCP, hooks, agent teams, etc.)

## Règles strictes
- NE PAS inventer de chiffres, métriques, ou citations
- NE PAS ajouter de callouts (:::), Mermaid, ou scénarios persona
- NE JAMAIS terminer un paragraphe par ":" avant une liste à puces (bug Typst)
- NE PAS dépasser +15% de lignes
- Garder les versions à 3.27.6
- Prose EN = anglais naturel, pas traduction mot-à-mot
- Chaque ajout = minimum 2 phrases, maximum 4 phrases

## Processus
1. LIRE reference.yaml (sections pertinentes au WP)
2. LIRE le WP FR complet
3. IDENTIFIER toutes les bare sections
4. ÉDITER le fichier FR (Edit tool, section par section)
5. LIRE le WP EN complet
6. ÉDITER le fichier EN
7. VÉRIFIER : aucun paragraphe ne finit par ":" avant une liste
8. Rapporter : sections traitées, delta lignes FR/EN
```

### Attente et Reporting

Attendre les retours de tous les agents. Pour chaque WP completed, afficher :

```
WP[XX] ✅ — [N] sections, +[X]% FR/EN
```

### Shutdown

Quand tous les agents ont terminé, envoyer shutdown_request à chacun, puis TeamDelete.

## Vérification Post-Enrichissement

```bash
# 1. Delta lignes (max +15%)
for f in whitepapers/fr/*.qmd; do
  echo "$(wc -l < "$f") $(basename $f)"
done

# 2. Vérifier bug Typst : paragraphe finissant par ":" suivi de liste
grep -n ':$' whitepapers/fr/*.qmd whitepapers/en/*.qmd | head -20

# 3. Versions intactes
grep "^version:" whitepapers/fr/*.qmd whitepapers/en/*.qmd

# 4. Rebuild PDFs
for f in whitepapers/fr/*.qmd whitepapers/en/*.qmd; do
  quarto render "$f"
done
```

## Budget Lignes par WP

| WP | Budget max FR | Budget max EN |
|----|--------------|--------------|
| 00 | +54 lignes | +54 lignes |
| 01 | +142 lignes | +142 lignes |
| 02 | +189 lignes | +189 lignes |
| 03 | +145 lignes | +145 lignes |
| 04 | +120 lignes | +120 lignes |
| 05 | +143 lignes | +143 lignes |
| 06 | +79 lignes | +79 lignes |
| 07 | +281 lignes | +281 lignes |
| 08 | +241 lignes | +241 lignes |
