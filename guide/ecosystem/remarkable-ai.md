---
title: "reMarkable 2 + AI : Hacks, Outils et Workflows"
description: "Cartographie complète des intégrations AI pour reMarkable 2 — MCP server, OCR, pipelines Obsidian/Notion, et automatisations"
tags: [mcp, integration, hardware, workflow, remarkable]
---

# reMarkable 2 + AI : Cartographie complète des hacks, outils et workflows

> **Last verified**: February 2026

La reMarkable 2 est une tablette e-ink Linux full-root-access. Sa philosophie de distraction zéro en fait un outil de pensée, mais ses intégrations natives sont minimalistes. Cette page couvre tout ce qui existe pour l'augmenter avec l'AI — du plus simple au plus technique.

## Table of Contents

1. [remarkable-mcp : Le game-changer](#1-remarkable-mcp--le-game-changer)
2. [Ghostwriter : Interface Vision-LLM](#2-ghostwriter--interface-vision-llm)
3. [Sync reMarkable → Obsidian](#3-sync-remarkable--obsidian)
4. [OCR + AI Pipeline custom](#4-ocr--ai-pipeline-custom)
5. [Accès SSH et outils communautaires](#5-accès-ssh-et-outils-communautaires)
6. [Features natives sous-exploitées](#6-features-natives-sous-exploitées)
7. [API et Developer Portal officiel](#7-api-et-developer-portal-officiel)
8. [Automatisation Zapier](#8-automatisation-zapier)
9. [Read-it-later : Web → reMarkable](#9-read-it-later--web--remarkable)
10. [Meeting Notes → AI Summary](#10-meeting-notes--ai-summary)
11. [Zotero → reMarkable (recherche)](#11-zotero--remarkable-recherche)
12. [Screen sharing comme whiteboard AI-assisté](#12-screen-sharing-comme-whiteboard-ai-assisté)
13. [Apps custom et hacks fun](#13-apps-custom-et-hacks-fun)
14. [Workflows AI-augmentés à construire](#14-workflows-ai-augmentés-à-construire)
15. [Par où commencer](#15-par-où-commencer)

---

## 1. remarkable-mcp : Le game-changer

**ROI : maximal | Effort : moyen | Connexion : SSH over USB (sans cloud)**

Sam Morrow a créé un **serveur MCP** qui connecte directement la reMarkable à Claude Code, VS Code Copilot, et tout assistant AI compatible MCP.

| Attribut | Détails |
|---------|---------|
| **Repo** | https://github.com/SamMorrowDrums/remarkable-mcp |
| **Blog** | https://sam-morrow.com/blog/building-an-mcp-server-for-remarkable |
| **Connexion** | SSH over USB — pas de cloud, pas d'abonnement |
| **Langage** | Python (FastMCP) |

### Ce que ça fait

- **Extraction native du texte tapé** (Type Folio / clavier virtuel) — instant, sans OCR
- **OCR handwriting** via Google Cloud Vision (1000 requêtes gratuites/mois)
- **Recherche intelligente** dans toute ta bibliothèque
- **Extraction de texte** depuis PDF et EPUB + annotations
- **Traverse complète** des documents

### Pourquoi c'est le #1

Tu peux demander à Claude "qu'est-ce que j'ai noté sur X pendant la réunion du 15 janvier ?" — il va chercher dans tes notes manuscrites. La reMarkable devient un **second brain queryable**.

### Stack technique

```
FastMCP + rmscene (parsing .rm natif) + PyMuPDF (PDF)
+ Google Cloud Vision (OCR) + Paramiko (SSH)
```

### Installation rapide

```bash
# 1. Activer SSH sur la reMarkable
# Settings → Help → Copyrights and licenses → IP + mot de passe root

# 2. Cloner le repo
git clone https://github.com/SamMorrowDrums/remarkable-mcp
cd remarkable-mcp && pip install -e .

# 3. Ajouter à Claude Code
# Dans ~/.claude.json ou via "claude mcp add"
```

### Configuration dans Claude Code

```json
{
  "mcpServers": {
    "remarkable": {
      "command": "python",
      "args": ["-m", "remarkable_mcp"],
      "env": {
        "REMARKABLE_HOST": "10.11.99.1",
        "REMARKABLE_PASSWORD": "<root-password>"
      }
    }
  }
}
```

---

## 2. Ghostwriter : Interface Vision-LLM

**ROI : expérimental | Effort : faible (un binary Rust à copier)**

| Attribut | Détails |
|---------|---------|
| **Repo** | https://github.com/awwaiid/ghostwriter |
| **Modèle** | GPT-4o Vision |
| **HN discussion** | https://news.ycombinator.com/item?id=42979986 |

### Concept

Tu écris un prompt à la main sur la reMarkable. Un vision-LLM (GPT-4o) lit ton écriture + tes dessins et répond **directement sur la tablette**.

### Installation

```bash
# 1. Télécharger le binary Rust compilé
scp ghostwriter root@10.11.99.1:/home/root/

# 2. SSH + lancer
ssh root@10.11.99.1
chmod +x ghostwriter && ./ghostwriter
```

### Interactions supportées

- Handwriting recognition
- Analyse de croquis (wireframes, schémas)
- Petit langage iconographique
- Gestes

### Use case concret

Tu dessines un schéma d'architecture, tu écris "optimise ça" — le LLM analyse visuellement et répond. Prototype fascinant pour l'interaction humain-AI par le stylo.

**Limite honnête** : L'app native de dessin de la reMarkable est minimaliste (pas de placement libre de texte dans la réponse).

---

## 3. Sync reMarkable → Obsidian

**ROI : élevé si tu utilises Obsidian | Effort : faible à moyen**

### Option A : Scrybble (le plus complet)

| Attribut | Détails |
|---------|---------|
| **Site** | scrybble.ink |
| **Plugin Obsidian** | Plugin communautaire (vault settings) |
| **Hébergement** | Self-hosted ou serveur Scrybble |
| **Discussion** | https://forum.obsidian.md/t/scrybble-sync-plugin/103194 |

**Ce que ça fait :**

- Sync notebooks, PDFs, ePubs → vault Obsidian
- Extraction highlights PDF/ePub en Markdown
- Extraction du texte tapé en Markdown
- Rendu complet des notebooks en PDF dans le vault
- Organisation par page avec tags

**Use case** : Recherche académique, prise de notes en réunion avec recherche Obsidian derrière.

### Option B : Plugin custom Cloud Sync

- **Démo** : https://www.youtube.com/watch?v=EsRdi8J9Cnc
- Commande "remarkable insert" → pull fichiers depuis le cloud reMarkable
- PDF dans dossier `rm/` → embed dans notes Obsidian
- Re-fetch automatique quand tu modifies sur la tablette

---

## 4. OCR + AI Pipeline custom

**ROI : élevé pour un workflow sur-mesure | Effort : moyen-élevé**

### rmirror + Claude API (Pattern recommandé)

Source : https://news.ycombinator.com/item?id=47110872 (février 2026)

**Concept** : Agent macOS background qui :
1. Sync les notebooks depuis la reMarkable
2. OCR via Claude API (meilleur que Tesseract pour le manuscrit avec contexte)
3. Push les notes transcrites vers Notion comme pages searchables

**Pourquoi Claude > Tesseract pour l'OCR** : Claude comprend le contexte, corrige les mots mal formés, structure les listes et tableaux automatiquement.

### Pipeline DIY

```
reMarkable → SSH/USB
  → extract .rm files
  → rmscene parse (texte natif si Type Folio)
  → Claude Vision API (screenshot des pages pour handwriting)
  → texte structuré + tags auto
  → Notion/Obsidian/GitHub via API
```

### Outils de parsing

| Outil | Usage | Lien |
|-------|-------|------|
| **rmscene** | Parsing natif des fichiers .rm | https://github.com/ricklupton/rmscene |
| **rmc** | Convertit .rm → SVG/PNG | https://github.com/ricklupton/rmc |
| **rmapi** | Interface Cloud API en Go | https://github.com/juruen/rmapi |

---

## 5. Accès SSH et outils communautaires

**Base indispensable pour tout le reste**

### Activer SSH

```bash
# Via l'interface tablette :
# Settings → Help → Copyrights and licenses
# → Affiche : IP + mot de passe root

# USB (connexion directe)
ssh root@10.11.99.1

# WiFi (après activation)
rm-ssh-over-wlan on
# ou via "Simply Customize It"
```

### Outils essentiels

| Outil | Usage | Lien |
|-------|-------|------|
| **RMHacks/xovi** | Framework de mods pour rM1/2/Paper Pro | https://www.nilorea.net/2025/08/11/latest-rmhacks-with-xovi-for-remarkable-1-2-paper-pro/ |
| **Simply Customize It** | GUI pour toggler features (WLAN SSH, etc.) | App tierce |
| **ReMy** | GUI pour browse/preview/exporter docs via SSH (sans cloud) | https://github.com/bordaigorl/remy |
| **rmirro** | Sync PDFs bidirectionnel tablette ↔ dossier local | https://github.com/hersle/rmirro |
| **reStream** | Stream l'écran de la reMarkable sur Mac/PC | https://github.com/rien/reStream |
| **KOReader** | Reader alternatif (plus de formats, customisable) | Via SSH |
| **reGitable** | Backup auto via git | awesome-reMarkable |

### Templates custom

```bash
# Créer un SVG template → copier via SSH
scp mon-template.svg root@10.11.99.1:/usr/share/remarkable/templates/

# Editer templates.json pour l'enregistrer
ssh root@10.11.99.1 'vi /usr/share/remarkable/templates/templates.json'
```

**Outils de génération** : ReCalendar.me, Remarkable Grid Generator, Remarkably Planner Builder

---

## 6. Features natives sous-exploitées

**Effort : zéro | Inclus dans Connect (~6€/mois)**

| Feature | Usage |
|---------|-------|
| **Handwriting conversion** | Sélectionner → Convertir → Copier/Coller dans n'importe quelle app |
| **Cloud sync** | Google Drive, Dropbox, OneDrive |
| **Send to Slack** | Partager des notes de réunion direct dans un channel |
| **Handwriting search** (beta AI) | Recherche dans tes notes manuscrites passées |
| **Screen sharing** | Partager l'écran sur PC (présentations, meetings) |
| **Send to email** | Envoyer comme PDF ou PNG |

**Astuce** : La conversion handwriting → texte fonctionne bien pour les mots isolés mais moins bien pour les phrases cursives denses. Privilégier l'impression pour la conversion.

---

## 7. API et Developer Portal officiel

| Ressource | Lien |
|-----------|------|
| **Developer Portal** | https://developer.remarkable.com |
| **Cloud API docs** | https://github.com/splitbrain/ReMarkableAPI |
| **Community guide** | https://remarkable.guide/ |
| **rmfakecloud** | Self-hosted Cloud (sans abonnement Connect) |

**OS** : Linux (Codex), full SSH root access, GPL-compliant. Le cross-compiler toolchain permet de déployer des apps custom natives.

**rmfakecloud** : Alternative open-source au cloud reMarkable pour self-héberger la sync et se passer de l'abonnement Connect.

---

## 8. Automatisation Zapier

**ROI : moyen | Effort : faible | Aucun code nécessaire**

**Mécanisme** : reMarkable → email (my@remarkable.com) → Zapier intercepte → action automatique

### Destinations possibles

Google Drive, Asana, ClickUp, Trello, Slack, WordPress, Evernote, Notion

### Plan gratuit

- 100 tasks/mois
- Zaps 2 étapes
- Check toutes les 15 min

### Workflows concrets

```
Notes de réunion → PDF auto-uploadé dans Google Drive
Croquis → Fichier envoyé dans un channel Slack
Action items → Tâches créées dans Asana/ClickUp
```

**Source** : https://myremarkable.substack.com/p/integrating-remarkable

---

## 9. Read-it-later : Web → reMarkable

**ROI : élevé pour la lecture | Effort : quasi nul**

| Outil | Description |
|-------|-------------|
| **Extension Chrome "Read on reMarkable"** | Save n'importe quelle page web → EPUB/PDF sur la tablette (ads supprimées) |
| **Goosepaper** | Flux RSS + news + Wikipedia quotidien → formaté e-ink |
| **remarkable_news** | News/comics/images du jour comme écran de veille |
| **Instapaper workaround** | Download articles en EPUB → import via app desktop |

**Option PDF** : Clic droit sur l'extension → "Read on reMarkable as PDF" (marges ajustables pour annoter).

---

## 10. Meeting Notes → AI Summary

**ROI : élevé | Effort : très faible**

### Workflow manuel (sans MCP)

```
1. Notes manuscrites pendant la réunion
2. Screenshot via l'app mobile reMarkable (ou sync cloud)
3. Upload l'image dans Claude/ChatGPT
4. Prompt : "Résume ces notes, extrais les action items avec deadlines et responsables"
```

### Workflow MCP (avec remarkable-mcp installé)

```
Claude, résume mes notes de la réunion d'aujourd'hui
→ Claude fetch les fichiers via SSH
→ OCR si nécessaire
→ Résumé structuré directement
```

**Avantage MCP** : Skip les étapes de screenshot et d'upload. Fonctionne même sans abonnement Connect.

### Template recommandé

Paper Pro Move Meeting Notebook : 60 meetings, 5 pages interlinked par meeting (overview + notes + action items + follow-up).

---

## 11. Zotero → reMarkable (recherche)

**ROI : élevé si tu lis des papers | Effort : moyen**

| Outil | Usage |
|-------|-------|
| **Zotero2reMarkable Bridge** | Sync PDFs depuis Zotero avec support des highlights |
| **KOReader + Toltec + plugin Zotero** | Meilleure lecture PDFs 2 colonnes, sync bidirectionnelle |
| **sync_zotero_remarkable** | Alternative plus légère |

**Limitation honnête** : reMarkable est un système fermé. L'intégration Zotero demande des workarounds. Pas aussi fluide qu'un Android e-reader avec Zotero natif. Fonctionnel mais avec friction.

---

## 12. Screen sharing comme whiteboard AI-assisté

**ROI : présentation/facilitation | Effort : nul (feature native Connect)**

- **Screen Share** : Ton écriture live apparaît sur l'écran externe/meeting virtuel
- **Laser pointer** : Stylo proche du haut de l'écran → active un pointeur laser
- **Workflow combo** : Screen Share + un collègue qui envoie tes notes dans ChatGPT en temps réel = whiteboard augmenté

**Prix** : Inclus dans Connect (~30$/an US, ~6€/mois EU).

---

## 13. Apps custom et hacks fun

| App/Hack | Description |
|----------|-------------|
| **Ephemeris** | Agenda quotidien généré depuis tes calendriers (Python) |
| **Remarcal** | Sync Google/Outlook/Apple calendriers → reMarkable |
| **reMarkable keywriter** | App de notes clavier distraction-free |
| **remarkable-wikipedia** | Lecteur Wikipedia offline |
| **whiteboard-hypercard** | Collaboration live, dessin partagé |
| **NetSurf** | Navigateur web minimaliste (via SSH) |
| **pdf2remarkable** | Upload PDFs au cloud depuis la ligne de commande |
| **send-to-remarkable** | Upload docs par email (style send-to-Kindle) |
| **libreMarkable** | Framework pour développer des apps natives |
| **oxide/remux/draft** | Launchers pour multitasking |
| **latex-yearly-planner** | Planner annuel généré en LaTeX |

**Catalogue complet** : https://github.com/reHackable/awesome-reMarkable

---

## 14. Workflows AI-augmentés à construire

Workflows pas encore packagés mais réalisables avec les briques disponibles.

### A. Journal de bord AI-analysé

```
Chaque soir → écrire 1 page de réflexion sur la reMarkable
→ remarkable-mcp + Claude → analyse hebdo des patterns, émotions, décisions
→ Output : insights dans Obsidian avec graph de connexions
```

### B. Inbox processing assisté

```
Papiers/articles lus et annotés sur reMarkable
→ OCR via Claude Vision → résumés structurés
→ Tags automatiques + classement dans Obsidian/Notion
```

### C. Sketch-to-code

```
Dessiner un wireframe UI sur reMarkable
→ Screenshot → Claude Vision → code HTML/React
```

### D. Flashcards automatiques

```
Notes de cours/lectures sur reMarkable
→ remarkable-mcp → Claude extrait les concepts clés
→ Génère des flashcards Anki automatiquement
```

### E. Daily standup automatisé

```
TODOs écrits chaque matin (template custom)
→ OCR → Slack/email formaté automatiquement
→ Fin de journée : cocher les items, diff envoyé
```

### F. Brainstorm capture → Mind map

```
Idées griffonnées librement
→ Claude Vision analyse le layout spatial + le texte
→ Génère une mind map structurée (Mermaid/Markmap)
```

---

## 15. Par où commencer

### Phase 1 — Ce week-end (2h)

1. Activer le SSH via Settings → Help → Copyrights and licenses
2. Installer **remarkable-mcp** et le connecter à Claude Code
3. Test : demander à Claude de chercher dans tes notes

### Phase 2 — Semaine suivante

4. Si tu utilises Obsidian → installer Scrybble
5. Tester **Ghostwriter** (10 min d'install, fun garanti)

### Phase 3 — Quand tu veux aller plus loin

6. Monter un pipeline OCR custom avec Claude Vision API
7. Explorer rmfakecloud pour se passer de l'abonnement Connect

---

## Sources

**Projets GitHub**

- https://github.com/SamMorrowDrums/remarkable-mcp (MCP server, nov 2025)
- https://github.com/awwaiid/ghostwriter (Vision-LLM interface)
- https://github.com/reHackable/awesome-reMarkable (catalogue communautaire)
- https://github.com/hersle/rmirro (sync sans cloud)
- https://github.com/bordaigorl/remy (GUI SSH)
- https://github.com/rien/reStream (screen streaming)
- https://github.com/splitbrain/ReMarkableAPI (Cloud API docs)
- https://github.com/ricklupton/rmscene (parsing .rm natif)

**Articles et discussions**

- https://sam-morrow.com/blog/building-an-mcp-server-for-remarkable
- https://news.ycombinator.com/item?id=47110872 (rmirror + Claude OCR, fév 2026)
- https://news.ycombinator.com/item?id=42979986 (Ghostwriter HN)
- https://news.ycombinator.com/item?id=46099997 (Hacking reMarkable 2, HN 2025)
- https://sgt.hootr.club/blog/hacking-on-the-remarkable-2/ (guide SSH hacking)
- https://myremarkable.substack.com/p/integrating-remarkable (Zapier integration)

**Obsidian**

- https://forum.obsidian.md/t/scrybble-sync-plugin/103194
- https://www.youtube.com/watch?v=EsRdi8J9Cnc (Cloud sync démo)

**Officiel**

- https://developer.remarkable.com (Developer Portal, SDK, API)
- https://remarkable.guide/ (Community guide)
