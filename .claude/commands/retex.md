---
model: sonnet
description: Retex - Capture lesson learned dans memory après fix, rollback, erreur
---

# Retex - Capture Lesson Learned

**Arguments**: $ARGUMENTS

Capture et persiste une leçon apprise (fausse piste, bug introduit, rollback, décision à revoir) dans memory pour les sessions futures.

---

## Step 1 : Gather Git Context

Run in parallel :

- `rtk git status`
- `rtk git log --oneline -5`
- `git branch --show-current`

---

## Step 2 : Gather Input

**Mode 1 — Direct** (si `$ARGUMENTS` non vide) :

- Utiliser `$ARGUMENTS` comme description de l'incident
- Inférer la catégorie et le root cause depuis le texte

**Mode 2 — Interactive** (si pas d'arguments) :

- Utiliser `AskUserQuestion` avec deux questions :
  1. "Que s'est-il passé ?" — options : Fausse piste, Bug de script/hook, Rollback, Décision doc à revoir, Piège outil/stack, Autre
  2. "Décris en 1-3 phrases : ce qui s'est passé et ce que tu aurais dû faire"

---

## Step 3 : Structure the Retex

Synthétiser depuis le contexte git + input user dans ce format :

| Champ                          | Description                                                                                                                                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Title**                      | 3-5 mots, forme substantif (ex: "Quarto render wrong format")                                                                                                                                           |
| **What happened**              | 1-3 phrases factuelles, pas de jugement                                                                                                                                                                 |
| **Root cause**                 | Cause technique racine — PAS le symptôme                                                                                                                                                                |
| **What should have been done** | L'approche correcte, actionnable                                                                                                                                                                        |
| **Prevention rule**            | Règle impérative courte, commençant par un verbe (ex: "Toujours utiliser --to whitepaper-typst pour les PDFs")                                                                                          |
| **Tags**                       | 1-4 tags parmi : `documentation`, `markdown`, `yaml`, `versioning`, `release`, `landing-sync`, `whitepaper`, `template`, `hook`, `script`, `quarto`, `typst`, `writing`, `structure`, `configuration` |
| **Severity**                   | `critical` (sync cassée/release bloquée), `high` (feature cassée), `medium` (perte de temps >1h)                                                                                                       |
| **Scope**                      | `project` (spécifique ce guide) ou `general` (tout projet doc/Quarto)                                                                                                                                   |

---

## Step 4 : Compute Memory Name

Format : `retex-{YYYY-MM-DD}-{slug}`

- Slug = 2-4 mots kebab-case du root cause
- Si doublon même jour : suffixer `-2`, `-3`...
- Exemple : `retex-2026-03-03-quarto-wrong-format`

---

## Step 5 : Write Retex Memory

Via Write tool, créer le fichier `.claude/memories/retex-{slug}.md` avec ce contenu exact :

```
# Retex: {Title}

**Date**: {YYYY-MM-DD} | **Severity**: {severity} | **Scope**: {scope}
**Tags**: {tag1, tag2, tag3}

## What Happened

{description factuelle}

## Root Cause

{analyse technique du root cause}

## What Should Have Been Done

{approche correcte et actionnable}

## Prevention Rule

> {règle impérative}

## Context

- Branch: `{current-branch}`
- Files: {fichiers clés impliqués si connus}
- Commit: {hash court si applicable}
```

---

## Step 6 : Update Retex Index

1. Lire `.claude/memories/retex-index.md` (ou créer si inexistant)
2. Ajouter la nouvelle entrée dans le tableau :

```markdown
# Retex Index

| Date   | Slug   | Title   | Severity   | Tags   | Scope   |
| ------ | ------ | ------- | ---------- | ------ | ------- |
| {date} | {slug} | {title} | {severity} | {tags} | {scope} |

Total: {N} | Last updated: {date}
```

3. Cap à 50 entrées (supprimer les plus anciennes si dépassement)
4. Écrire l'index mis à jour

---

## Step 7 : Confirm

Afficher un résumé compact :

```
✓ Retex capturé :
  Fichier    : .claude/memories/retex-{slug}.md
  Title      : {title}
  Severity   : {severity}
  Prevention : "{prevention rule}"
  Tags       : [{tags}]
```

---

## Edge Cases

- **Premier retex** : créer `retex-index.md` from scratch (header + première entrée)
- **Pas de contexte git** : omettre la section "Context" sans erreur
- **$ARGUMENTS très courts** (<10 chars) : basculer en mode interactif
