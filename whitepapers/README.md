# Série de Whitepapers Claude Code

Cette série de 13 whitepapers couvre Claude Code, de l'installation à la production en équipe, jusqu'à l'ingénierie des agents autonomes.

## La Série Complète

| # | Titre | Hook | Public | Pages |
|---|-------|------|--------|-------|
| **0** | De Zéro à Productif | "5 minutes pour commencer" | Tous | 20 |
| **1** | Prompts qui Marchent | "Une formule, 3× moins d'itérations" | Dev Junior/Senior | 40 |
| **2** | Personnaliser Claude | "CLAUDE.md, Agents, Skills : votre assistant sur-mesure" | Senior/Power | 47 |
| **3** | Sécurité en Production | "14 hooks, threat DB v2.0, 0 incident" | DevSecOps/TechLead | 48 |
| **4** | L'Architecture Démystifiée | "Pas de RAG, pas de magie noire" | Architectes | 40 |
| **5** | Déployer en Équipe | "De solo à 50 devs" | TechLead/PM | 43 |
| **6** | Privacy & Compliance | "Vos données chez Anthropic" | Compliance/Legal | 29 |
| **7** | **Le Guide de Référence** | "Synthèse complète + workflows avancés" | Tous | **87** |
| **8** | **Agent Teams** | "Coordination multi-agents pour tâches complexes" | Power/TechLead | **42** |
| **9** | **Apprendre avec l'IA** | "Protocole UVAL — apprendre sans accumuler la dette de compréhension" | Dev (tous niveaux) | **49** |
| **10** | **Convaincre son Employeur** | "Le dossier CEO/CTO/CFO pour investir dans l'IA" | CEO/CTO/CFO/Manager | **27** |
| **11** | **Piloter une Équipe à l'Ère de l'IA** | "Métriques de livraison, qualité et revue" | TechLead/Manager | **40 FR / 42 EN*** |
| **12** | **Ingénierie Logicielle à l'Ère des Agents Autonomes** | "Harnesses, CI/CD agentic et mesure" | TechLead/Staff/Principal | **39 FR / 30 EN*** |

**Total : 13 whitepapers.** Les volumes PDF et le temps de lecture dépendent de la version rendue.

\* Comptes mesurés sur les PDF existants le 28 août 2026, avant le nouveau rendu des sources modifiées.

**Langues & formats disponibles :**

| Format | FR | EN |
|--------|----|----|
| PDF (Typst) | ✅ `whitepapers/fr/*.pdf` | ✅ `whitepapers/en/*.pdf` |
| EPUB3 | ✅ `epub-output/fr/*.epub` | ✅ `epub-output/en/*.epub` |
| HTML (preview) | ✅ via `quarto preview` | ✅ via `quarto preview` |

> **Notes** :
> - Le WP07 est un **guide de référence consolidé** qui synthétise les WP 00-06 et ajoute les features v2.x (Tasks API, Background Agents, Agent Teams, etc.)
> - Le WP08 (v3.26.0) couvre en profondeur Agent Teams avec patterns, use cases, et checklist déploiement.
> - Le WP09 (v3.36.0) introduit le protocole UVAL (Understand → Verify → Apply → Learn) et la dette de compréhension.
> - Le WP10 (v3.36.0) est le dossier d'argumentation ROI pour convaincre CEO, CTO et CFO d'investir dans l'IA.
> - Le WP11 couvre les métriques de livraison, de qualité et de revue dans un workflow assisté par agent.
> - Le WP12 distingue runtime, contrat de dépôt et orchestration, avec les critères de sélection et le protocole d'essai d'un harness.

## Parcours par Profil

| Profil | Parcours Recommandé | Temps |
|--------|---------------------|-------|
| 🟢 **Junior Dev** | #0 → #1 → #9 | ~55 min |
| 🟡 **Senior Dev** | #0 → #1 → #2 → #3 | ~1h15 |
| 🔴 **Power User** | #0 → #4 → #3 → #8 | ~1h55 |
| 👔 **Tech Lead** | #0 → #5 → #3 → #8 | ~1h55 |
| 📊 **PM/Manager** | #0 → #5 → #6 → #10 | ~1h10 |
| 💼 **CEO/CFO** | #10 → #0 | ~35 min |
| 🔒 **Compliance** | #0 → #6 → #3 | ~50 min |

## Fichiers

| Fichier | Description |
|---------|-------------|
| `00-introduction-serie.qmd` | Whitepaper #0 - Introduction |
| `01-prompts-efficaces.qmd` | Whitepaper #1 - Prompts |
| `02-personnalisation.qmd` | Whitepaper #2 - Personnalisation |
| `03-securite.qmd` | Whitepaper #3 - Sécurité |
| `04-architecture.qmd` | Whitepaper #4 - Architecture |
| `05-equipe.qmd` | Whitepaper #5 - Équipe |
| `06-privacy.qmd` | Whitepaper #6 - Privacy |
| `07-guide-reference.qmd` | **Whitepaper #7 - Guide de Référence (consolidé)** |
| `08-agent-teams.qmd` | **Whitepaper #8 - Agent Teams (v3.26.0)** |
| `09-apprendre-avec-ia.qmd` | **Whitepaper #9 - Apprendre avec l'IA (v3.36.0)** |
| `10-budget-ia.qmd` | **Whitepaper #10 - Convaincre son Employeur (v3.36.0)** |
| `11-team-metrics.qmd` | **Whitepaper #11 - Piloter une Équipe à l'Ère de l'IA** |
| `12-agent-engineering.qmd` | **Whitepaper #12 - Ingénierie Logicielle à l'Ère des Agents Autonomes** |

---

# Fiches Mémo (Recap Cards)

58 fiches A4 par langue, format intermédiaire entre le cheatsheet et les whitepapers. Chaque fiche couvre un concept précis avec tables de référence et exemples de commandes. Les sources QMD et les 58 PDF sont disponibles en FR et EN, y compris C14 Agent Harness Map.

**Langues & formats disponibles :**

| Format | FR | EN |
|--------|----|----|
| PDF (recap-card-typst) | 58 | 58 |
| EPUB / HTML | Non applicable (format 1 page) | Non applicable |

**Sources** : `recap-cards/fr/*.qmd` · **PDFs** : même dossier · **En ligne** : `cc.bruniaux.com/cheatsheets/`

## Technique (T01-T22)

| Card | Titre | Difficulté | Description |
|------|-------|------------|-------------|
| T01 | Commandes Essentielles | beginner | Raccourcis clavier & commandes slash indispensables |
| T02 | Mode Non-Interactif & Headless | intermediate | Utiliser Claude Code sans interaction humaine : scripts, CI, pipes |
| T03 | Permission Modes | beginner | Contrôle des accès outils — du plus sûr au plus permissif |
| T04 | Permissions & Glob Patterns | intermediate | Contrôler précisément les outils accessibles avec des patterns glob |
| T05 | Hiérarchie de Configuration | beginner | Où configurer quoi — de global à local |
| T06 | Settings JSON | intermediate | Toutes les clés de configuration et leur portée |
| T07 | CLAUDE.md Best Practices | intermediate | Écrire des instructions efficaces que Claude lit à chaque session |
| T08 | Auto-Memories | intermediate | Le système de mémorisation automatique vs CLAUDE.md manuel |
| T09 | Workspace Hygiene | intermediate | Garder le contexte propre en excluant ce que Claude ne doit pas lire |
| T10 | Config Multi-Machine | intermediate | Synchroniser sa configuration Claude Code entre plusieurs postes |
| T11 | Search Tools Decision | intermediate | Choisir entre Glob, Grep, Read, Task et Bash selon le contexte |
| T12 | MCP Servers Overview | intermediate | Le protocole d'extension et les serveurs essentiels |
| T13 | Context7 & Sequential | advanced | Documentation officielle et raisonnement multi-étapes à portée de prompt |
| T14 | Grepai Semantic Search | advanced | Trouver du code par intention, pas par regex |
| T15 | MCP Secrets Management | advanced | Gérer les credentials des MCP servers sans les exposer |
| T16 | Sandbox Natif Architecture | advanced | Comment Claude Code isole ses opérations au niveau OS |
| T17 | Sandbox Natif vs Docker | advanced | Choisir le bon niveau d'isolation selon le contexte |
| T18 | Modèles & Thinking Modes | intermediate | Choisir le bon modèle et le bon niveau de réflexion |
| T19 | Context Window 200K-1M | intermediate | Quand passer à la fenêtre de contexte étendue et à quel coût |
| T20 | Token Optimization | advanced | Réduire la consommation de tokens sans perdre en qualité |
| T21 | Fast Mode & API | advanced | Le mode rapide et les changements API majeurs à connaître |
| T22 | Third-Party Tools | intermediate | Les outils complémentaires indispensables de l'écosystème |

## Méthodologie (M01-M22)

| Card | Titre | Difficulté | Description |
|------|-------|------------|-------------|
| M01 | Workflow Quotidien | beginner | La routine optimale pour une session de développement productive |
| M02 | Context Management | beginner | Gérer la fenêtre de contexte pour des sessions efficaces |
| M03 | Sessions & Continuité | beginner | Reprendre une session là où on l'a laissée |
| M04 | Compact vs Clear | beginner | Quand résumer et quand réinitialiser le contexte |
| M05 | Plan Mode | intermediate | Faire planifier Claude avant d'agir |
| M06 | Task Management System | intermediate | Organiser le travail de Claude avec la Tasks API |
| M07 | TodoWrite vs Tasks API | intermediate | L'ancien et le nouveau système de gestion des tâches |
| M08 | Agents Custom | intermediate | Créer des sous-agents spécialisés pour déléguer des tâches |
| M09 | Slash Commands | beginner | Créer des commandes personnalisées réutilisables |
| M10 | Skills | intermediate | Modules de compétences réutilisables avec ressources embarquées |
| M11 | Hooks Événements Système | intermediate | Réagir automatiquement aux actions de Claude Code |
| M12 | Hooks Patterns Concrets | advanced | Exemples pratiques de hooks pour automatiser le workflow |
| M13 | Worktrees | advanced | Travailler en parallèle sur plusieurs branches sans changer de répertoire |
| M14 | Plan-Validate-Execute | intermediate | Le workflow 3 phases pour des tâches complexes sous contrôle |
| M15 | TDD / BDD / SDD | intermediate | Méthodologies de développement structurées avec Claude Code |
| M16 | Multi-Agent Topologie | advanced | Architecturer des équipes d'agents pour les tâches complexes |
| M17 | Multi-Agent Communication & Trust | advanced | Passer du contexte entre agents et gérer les niveaux de confiance |
| M18 | Event-Driven Agents | advanced | Déclencher des agents automatiquement depuis GitHub, Linear, Jira |
| M19 | GitHub Actions | intermediate | Intégrer Claude Code dans les pipelines CI/CD GitHub |
| M20 | CI/CD Production | advanced | Utiliser Claude Code en production avec les bonnes garanties de sécurité |
| M21 | Debug Méthodique | intermediate | Approche structurée pour diagnostiquer et résoudre les erreurs |
| M22 | Observabilité JSONL | advanced | Auditer et analyser l'activité de Claude Code via les logs |

## Conception (C01-C14)

| Card | Titre | Difficulté | Description |
|------|-------|------------|-------------|
| C01 | Trust Calibration & Mental Model | beginner | Comment penser la relation avec Claude pour en tirer le meilleur |
| C02 | Prompting Basics | beginner | Les principes qui font la différence entre un bon et un mauvais prompt |
| C03 | XML Prompting & Semantic Anchors | advanced | Structurer les prompts complexes pour des résultats reproductibles |
| C04 | Commands, Skills, Plugins & Agents | intermediate | Choisir le bon mécanisme d'extension selon le besoin |
| C05 | Memory Stack (4 niveaux) | intermediate | Où vit l'information que Claude utilise et comment la gérer |
| C06 | Configuration Decision Guide | intermediate | Quel mécanisme de configuration utiliser selon la situation |
| C07 | Conventions Équipe Scale | intermediate | Synchroniser les pratiques Claude Code dans une équipe de 5+ développeurs |
| C08 | Surface d'Attaque & Menaces | advanced | Comprendre les vecteurs d'attaque spécifiques à Claude Code |
| C09 | Prompt Injection Defenses | advanced | Protéger Claude Code quand il traite du contenu externe non fiable |
| C10 | AI Traceability | advanced | Tracer la contribution de l'IA dans le code et les commits |
| C11 | Subscription vs API Patterns | intermediate | Comprendre quand chaque modèle de facturation est avantageux |
| C12 | Agent SDK & Integrations IDE | advanced | Intégrer Claude Code dans Xcode, VS Code et d'autres environnements |
| C13 | Erreurs Courantes | beginner | Les pièges fréquents et comment les éviter |
| C14 | Agent Harness Map | advanced | Choisir runtime, contrat de dépôt ou orchestrateur |

**Total : 58 sources QMD et 58 PDF par langue.** Les PDF font une page. Guide version 3.42.0.

---

# Guide de Génération des Whitepapers

Ce guide explique comment générer les whitepapers PDF du projet Claude Code Ultimate Guide.

## Stack Technique

| Outil | Version | Rôle |
|-------|---------|------|
| **Quarto** | ≥1.4.0 | Moteur de rendu documents |
| **Typst** | 0.13.0 | Typographie moderne (intégré à Quarto) |
| **Pandoc** | 3.x | Conversion Markdown (intégré à Quarto) |
| **EPUB3** | natif Quarto | Format ebook (Apple Books, Kindle, etc.) |

## Design Template v3.0

**Inspiré de** : Stripe, Vercel, Linear design systems (2025-2026)

| Élément | Choix | Justification |
|---------|-------|---------------|
| **Palette** | Slate + Indigo | Tendance 2025, WCAG AA compliant |
| **Font corps** | Inter | Standard moderne, excellente lisibilité |
| **Font code** | JetBrains Mono | Optimisé pour la lecture de code |
| **Cover** | Blanc minimaliste | Tendance épurée, logo centré en bas |
| **Line-height** | 1.6 (0.75em) | Optimal pour la lecture longue |
| **H1** | 24pt, tracking -0.02em | Hiérarchie claire |
| **H2** | 18pt, accent color | Distinction visuelle |
| **Code blocks** | Bordure gauche accent | Repérage facile |

## Prérequis

### macOS

```bash
# Installation Quarto via Homebrew
brew install quarto

# Vérification
quarto --version  # >= 1.4.0
```

### Linux (Debian/Ubuntu)

```bash
# Télécharger le .deb depuis https://quarto.org/docs/get-started/
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.555/quarto-1.4.555-linux-amd64.deb
sudo dpkg -i quarto-1.4.555-linux-amd64.deb

quarto --version
```

### Windows

```powershell
# Via winget
winget install Posit.Quarto

# Ou télécharger l'installeur depuis https://quarto.org/docs/get-started/
```

## Structure du Projet

```
whitepapers/
├── _extensions/
│   └── whitepaper/
│       ├── _extension.yml      # Métadonnées extension
│       ├── typst-template.typ  # Template principal
│       └── typst-show.typ      # Bridge Quarto → Typst
├── 00-introduction-serie.qmd   # Source whitepaper #0
├── 00-introduction-serie.pdf   # PDF généré
└── README.md                   # Ce fichier
```

## Génération d'un PDF

### Commande de base

```bash
cd whitepapers
quarto render 00-introduction-serie.qmd
```

### Génération de tous les whitepapers

```bash
cd whitepapers
quarto render *.qmd
```

### Mode preview (hot-reload)

```bash
quarto preview 00-introduction-serie.qmd
```

## Génération d'un EPUB

Les whitepapers supportent nativement le format EPUB3 via Quarto. Zéro dépendance supplémentaire : `format: epub` est déjà configuré dans le frontmatter de chaque `.qmd`.

### Générer un EPUB individuel

```bash
cd whitepapers/fr
quarto render 00-introduction-serie.qmd --to epub
# → produit 00-introduction-serie.epub dans le répertoire courant
```

### Générer tous les EPUBs (script batch)

```bash
cd whitepapers
./render-epub.sh all      # FR + EN
./render-epub.sh fr       # Français seulement
./render-epub.sh en       # English only
```

Les EPUBs sont générés dans `whitepapers/epub-output/{fr,en}/`.

### Style EPUB

Le fichier `whitepapers/epub-styles.css` applique la palette Bold Guy à tous les EPUBs :
- Palette : `#1a1207` (primary), `#d4520a` (accent orange brûlé), `#f5f0eb` (fond beige)
- Callouts Quarto (`callout-note`, `callout-tip`, `callout-warning`, `callout-important`) stylés nativement
- Code blocks avec bordure gauche accent
- Tables zebra
- Cover image : `_extensions/whitepaper/assets/claude-code-ai-logo.jpg`

### Compatibilité

| Reader | Testé |
|--------|-------|
| Apple Books (macOS/iOS) | ✓ |
| Calibre | ✓ |
| Kindle (via conversion) | ~ |

### Note

`whitepapers/epub-output/` est gitignored — les EPUBs générés ne sont pas versionnés.

---

## Créer un Nouveau Whitepaper

### 1. Créer le fichier source

```bash
touch whitepapers/01-methodologies.qmd
```

### 2. Ajouter le YAML frontmatter

```yaml
---
title: "Titre du Whitepaper"
subtitle: "Sous-titre explicatif"
author: "Votre Nom"
date: 2026-01-15
date-format: "MMMM YYYY"
version: "1.0"
series: "Claude Code Ultimate Guide"
format:
  whitepaper-typst:
    toc: true
    toc-depth: 2
    section-numbering: "1.1"
  html:
    toc: true
    theme: cosmo
lang: fr
---

# Premier Chapitre

Contenu ici...
```

### 3. Générer le PDF

```bash
quarto render 01-methodologies.qmd
```

## Paramètres YAML Disponibles

| Paramètre | Type | Description |
|-----------|------|-------------|
| `title` | string | Titre principal (page de couverture) |
| `subtitle` | string | Sous-titre (optionnel) |
| `author` | string | Auteur(s) |
| `date` | date | Date au format ISO (YYYY-MM-DD) |
| `date-format` | string | Format d'affichage (`MMMM YYYY` → "janvier 2026") |
| `version` | string | Badge version sur la couverture |
| `series` | string | Label série en haut de la couverture |
| `wp-number` | string | Numéro WP dans cercle géométrique (ex: "07") |
| `lang` | string | Langue (`fr`, `en`) |
| `toc` | boolean | Afficher table des matières |
| `toc-depth` | number | Profondeur TOC (1-3) |
| `section-numbering` | string | Format numérotation (`1.1`, `1.a`, etc.) |

## Syntaxe Markdown Supportée

### Sauts de page

```markdown
{{< pagebreak >}}
```

### Tableaux

```markdown
| Colonne 1 | Colonne 2 |
|-----------|-----------|
| Valeur    | Valeur    |
```

Les tableaux ont automatiquement un style zebra (lignes alternées).

### Blocs de code

````markdown
```bash
npm install -g @anthropic-ai/claude-code
```
````

Les blocs de code ont une bordure bleue à gauche.

### Séparateurs

```markdown
---
```

Les séparateurs sont stylisés en barre bleue centrée.

## Personnalisation du Template

### Couleurs (Palette Slate + Indigo)

Modifier dans `_extensions/whitepaper/typst-template.typ` :

```typst
#let primary = rgb("#0f172a")      // Slate 900 - titres, texte fort
#let secondary = rgb("#334155")    // Slate 700 - sous-titres
#let accent = rgb("#6366f1")       // Indigo 500 - accents, liens
#let muted = rgb("#64748b")        // Slate 500 - métadonnées
#let light-bg = rgb("#f8fafc")     // Slate 50 - fond code, tableaux
#let border-light = rgb("#e2e8f0") // Slate 200 - bordures
```

### Callout Boxes

4 types de callouts disponibles :

```typst
#info[Contenu informatif]
#warning(title: "Attention")[Avertissement important]
#success[Bonne pratique]
#danger(title: "Ne jamais faire")[Erreur critique à éviter]
```

| Type | Couleur fond | Couleur bordure | Icône |
|------|--------------|-----------------|-------|
| `info` | #E0F2FE | #0284C7 | 💡 |
| `warning` | #FEF3C7 | #D97706 | ⚠️ |
| `success` | #DCFCE7 | #16A34A | ✅ |
| `danger` | #FEE2E2 | #DC2626 | 🚨 |

### Polices

```typst
// Corps de texte
font: ("Inter", "SF Pro Display", "Helvetica Neue", "Arial"),
fontsize: 11pt,

// Code blocks
font: ("JetBrains Mono", "Fira Code", "SF Mono", "Consolas", "monospace"),
```

### Marges

```typst
margin: (x: 2.5cm, y: 2.5cm),
```

## Dépannage

### Erreur "Extension not found"

```bash
# Vérifier que vous êtes dans le bon dossier
cd whitepapers
ls _extensions/whitepaper/
```

### Polices manquantes (warnings)

Les warnings "unknown font family" sont normaux - Typst utilise les fallbacks :

```
warning: unknown font family: inter
warning: unknown font family: jetbrains mono
```

Pour installer les polices (optionnel) :

```bash
# macOS - Inter
brew install --cask font-inter

# macOS - JetBrains Mono
brew install --cask font-jetbrains-mono
```

### Caractères spéciaux cassés

Vérifier l'encodage UTF-8 du fichier source :

```bash
file -i 00-introduction-serie.qmd
# Doit afficher: charset=utf-8
```

---

## Problèmes Courants et Solutions

### 🔴 Code blocks imbriqués cassés

**Symptôme** : Les diagrammes ASCII sortent du code block, le contenu s'affiche comme du texte normal.

**Cause** : Un code block ````markdown` contient un code block imbriqué (ex: ` ```bash`). Quarto interprète le ` ``` ` interne comme fermant le bloc externe.

**Solution** : Utiliser 4 backticks pour le bloc externe :

````markdown
## Exemple correct

````markdown
# Contenu markdown

```bash
echo "Ce code bash est DANS le markdown"
```

Fin du contenu.
````
````

**Détection automatique** :

```bash
# Trouver les code blocks imbriqués problématiques
awk '
/^```markdown$/ { in_md=1; start=NR }
in_md && /```[a-z]/ { print FILENAME":"NR": nested code at line "start }
/^```$/ && in_md { in_md=0 }
' *.qmd
```

### 🔴 Diagrammes ASCII mal rendus

**Symptôme** : Les caractères `├`, `└`, `│`, `─` s'affichent mal ou sont coupés.

**Causes possibles** :

1. **Code block cassé** (voir ci-dessus)
2. **Largeur excessive** - Le diagramme dépasse la largeur de page

**Solution largeur** : Réduire la largeur du diagramme ou utiliser des caractères ASCII simples :

```
# Au lieu de (Unicode)
├── fichier.txt
└── autre/

# Utiliser (ASCII simple)
+-- fichier.txt
`-- autre/
```

### 🟡 Tableaux rendus comme code

**Symptôme** : Un tableau Markdown s'affiche avec fond gris comme un code block.

**Cause** : Décalage des code blocks - un ` ``` ` superflu quelque part avant.

**Diagnostic** :

```bash
# Lister tous les délimiteurs de code
grep -n '^```' fichier.qmd

# Vérifier qu'ils sont par paires (nombre pair)
grep -c '^```' fichier.qmd
```

### 🟡 Page de couverture - logo non trouvé

**Erreur** : `cannot read file outside of project root`

**Solution** : Le logo doit être dans le répertoire du projet Typst :

```bash
# Copier le logo dans l'extension
cp ../assets/logo.jpg _extensions/whitepaper/assets/

# Dans le template, utiliser le chemin relatif au .qmd
image("_extensions/whitepaper/assets/logo.jpg", width: 3.5cm)
```

### 🟢 Régénérer tous les PDFs

```bash
cd whitepapers
for f in *.qmd; do
  echo "Rendering $f..."
  quarto render "$f" 2>&1 | grep -E "(Output created|error)"
done
```

### 🟢 Vérifier la cohérence des code blocks

```bash
# Script de validation complet
for f in *.qmd; do
  opens=$(grep -c '^```' "$f")
  if [ $((opens % 2)) -ne 0 ]; then
    echo "⚠️  $f: nombre impair de \`\`\` ($opens)"
  fi
done
```

## Workflow Recommandé

```
1. Rédiger en Markdown (.qmd)
2. Preview avec `quarto preview`
3. Ajuster le contenu
4. Générer le PDF final avec `quarto render`
5. Vérifier le PDF
6. Commit les sources (.qmd) et le PDF
```

## Claude Code Skill

Un skill `pdf-generator` est disponible pour assister la génération de PDFs :

```bash
# Dans une session Claude Code
/pdf-generator
```

Le skill fournit :
- Stack technique (Quarto/Typst/Pandoc)
- Template YAML frontmatter complet
- Design system v3.0 (palette, fonts)
- Commandes de génération
- Guide de dépannage détaillé

**Emplacement** : `~/.claude/skills/pdf-generator/`

## Ressources

- [Documentation Quarto](https://quarto.org/docs/guide/)
- [Documentation Typst](https://typst.app/docs/)
- [Quarto + Typst Guide](https://quarto.org/docs/output-formats/typst.html)
