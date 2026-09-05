---
title: "reMarkable 2 + AI: Hacks, Tools, and Workflows"
description: "Complete mapping of AI integrations for reMarkable 2: MCP server, OCR, Obsidian/Notion pipelines, and automations"
tags: [mcp, integration, hardware, workflow, remarkable]
---

# reMarkable 2 + AI: Complete Mapping of Hacks, Tools, and Workflows

> **Last verified**: February 2026

The reMarkable 2 is a full-root-access Linux e-ink tablet. Its zero-distraction philosophy makes it a thinking tool, but its native integrations are minimal. This page covers everything that exists to augment it with AI, from the simplest to the most technical.

See also: [AI Ecosystem](ai-ecosystem.md) for the broader mapping of the AI ecosystem (beyond hardware).

## Table of Contents

1. [remarkable-mcp: direct MCP access via SSH](#1-remarkable-mcp-direct-mcp-access-via-ssh)
2. [Ghostwriter: Vision-LLM Interface](#2-ghostwriter-vision-llm-interface)
3. [Sync reMarkable → Obsidian](#3-sync-remarkable--obsidian)
4. [OCR + Custom AI Pipeline](#4-ocr--custom-ai-pipeline)
5. [SSH Access and Community Tools](#5-ssh-access-and-community-tools)
6. [Underused Native Features](#6-underused-native-features)
7. [Official API and Developer Portal](#7-official-api-and-developer-portal)
8. [Zapier Automation](#8-zapier-automation)
9. [Read-it-later: Web to reMarkable](#9-read-it-later-web-to-remarkable)
10. [Meeting Notes → AI Summary](#10-meeting-notes--ai-summary)
11. [Zotero to reMarkable (research)](#11-zotero-to-remarkable-research)
12. [Screen sharing as an AI-assisted whiteboard](#12-screen-sharing-as-an-ai-assisted-whiteboard)
13. [Custom apps and fun hacks](#13-custom-apps-and-fun-hacks)
14. [AI-augmented workflows to build](#14-ai-augmented-workflows-to-build)
15. [Where to start](#15-where-to-start)

---

## 1. remarkable-mcp: direct MCP access via SSH

**ROI: maximal | Effort: medium | Connection: SSH over USB (no cloud)**

Sam Morrow created an **MCP server** that connects the reMarkable directly to Claude Code, VS Code Copilot, and any MCP-compatible AI assistant.

| Attribute | Details |
|---------|---------|
| **Repo** | https://github.com/SamMorrowDrums/remarkable-mcp |
| **Blog** | https://sam-morrow.com/blog/building-an-mcp-server-for-remarkable |
| **Connection** | SSH over USB (no cloud, no subscription) |
| **Language** | Python (FastMCP) |

### What it does

- **Native extraction of typed text** (Type Folio / virtual keyboard), instant, no OCR
- **Handwriting OCR** via Google Cloud Vision (1000 free requests/month)
- **Smart search** across your entire library
- **Text extraction** from PDF and EPUB, plus annotations
- **Full traversal** of documents

### Why it's #1

You can ask Claude "what did I note about X during the January 15 meeting?" It will search through your handwritten notes. The reMarkable becomes a **queryable second brain**.

### Technical stack

```
FastMCP + rmscene (native .rm parsing) + PyMuPDF (PDF)
+ Google Cloud Vision (OCR) + Paramiko (SSH)
```

### Quick installation

```bash
# 1. Enable SSH on the reMarkable
# Settings → Help → Copyrights and licenses → IP + root password

# 2. Clone the repo
git clone https://github.com/SamMorrowDrums/remarkable-mcp
cd remarkable-mcp && pip install -e .

# 3. Add to Claude Code
# In ~/.claude.json or via "claude mcp add"
```

### Configuration in Claude Code

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

## 2. Ghostwriter: Vision-LLM Interface

**ROI: experimental | Effort: low (a Rust binary to copy)**

| Attribute | Details |
|---------|---------|
| **Repo** | https://github.com/awwaiid/ghostwriter |
| **Model** | GPT-4o Vision |
| **HN discussion** | https://news.ycombinator.com/item?id=42979986 |

### Concept

You write a prompt by hand on the reMarkable. A vision-LLM (GPT-4o) reads your handwriting and drawings and responds **directly on the tablet**.

### Installation

```bash
# 1. Download the compiled Rust binary
scp ghostwriter root@10.11.99.1:/home/root/

# 2. SSH in and launch
ssh root@10.11.99.1
chmod +x ghostwriter && ./ghostwriter
```

### Supported interactions

- Handwriting recognition
- Sketch analysis (wireframes, diagrams)
- Small iconographic language
- Gestures

### Concrete use case

You draw an architecture diagram, you write "optimize this." The LLM analyzes it visually and responds. A fascinating prototype for pen-based human-AI interaction.

**Honest limitation**: The reMarkable's native drawing app is minimal (no free text placement in the response).

---

## 3. Sync reMarkable → Obsidian

**ROI: high if you use Obsidian | Effort: low to medium**

### Option A: Scrybble (the most complete)

| Attribute | Details |
|---------|---------|
| **Site** | scrybble.ink |
| **Obsidian plugin** | Community plugin (vault settings) |
| **Hosting** | Self-hosted or Scrybble server |
| **Discussion** | https://forum.obsidian.md/t/scrybble-sync-plugin/103194 |

**What it does:**

- Sync notebooks, PDFs, ePubs to Obsidian vault
- Extract PDF/ePub highlights as Markdown
- Extract typed text as Markdown
- Full rendering of notebooks as PDF in the vault
- Organization by page with tags

**Use case**: Academic research, meeting note-taking with Obsidian search behind it.

### Option B: Custom Cloud Sync plugin

- **Demo**: https://www.youtube.com/watch?v=EsRdi8J9Cnc
- "remarkable insert" command, pulls files from the reMarkable cloud
- PDF in the `rm/` folder, embedded in Obsidian notes
- Automatic re-fetch when you make changes on the tablet

---

## 4. OCR + Custom AI Pipeline

**ROI: high for a custom workflow | Effort: medium-high**

### rmirror + Claude API (recommended pattern)

Source: https://news.ycombinator.com/item?id=47110872 (February 2026)

**Concept**: A macOS background agent that:
1. Syncs notebooks from the reMarkable
2. OCRs via Claude API (better than Tesseract for handwriting with context)
3. Pushes the transcribed notes to Notion as searchable pages

**Why Claude beats Tesseract for OCR**: Claude understands context, corrects malformed words, and structures lists and tables automatically.

### DIY pipeline

```
reMarkable → SSH/USB
  → extract .rm files
  → rmscene parse (native text if Type Folio)
  → Claude Vision API (page screenshots for handwriting)
  → structured text + auto tags
  → Notion/Obsidian/GitHub via API
```

### Parsing tools

| Tool | Usage | Link |
|-------|-------|------|
| **rmscene** | Native parsing of .rm files | https://github.com/ricklupton/rmscene |
| **rmc** | Converts .rm to SVG/PNG | https://github.com/ricklupton/rmc |
| **rmapi** | Cloud API interface in Go | https://github.com/juruen/rmapi |

---

## 5. SSH Access and Community Tools

**Essential foundation for everything else**

### Enable SSH

```bash
# Via the tablet interface:
# Settings → Help → Copyrights and licenses
# → Displays: IP + root password

# USB (direct connection)
ssh root@10.11.99.1

# WiFi (after activation)
rm-ssh-over-wlan on
# or via "Simply Customize It"
```

### Essential tools

| Tool | Usage | Link |
|-------|-------|------|
| **RMHacks/xovi** | Mod framework for rM1/2/Paper Pro | https://www.nilorea.net/2025/08/11/latest-rmhacks-with-xovi-for-remarkable-1-2-paper-pro/ |
| **Simply Customize It** | GUI to toggle features (WLAN SSH, etc.) | Third-party app |
| **ReMy** | GUI to browse/preview/export docs via SSH (no cloud) | https://github.com/bordaigorl/remy |
| **rmirro** | Bidirectional PDF sync, tablet ↔ local folder | https://github.com/hersle/rmirro |
| **reStream** | Stream the reMarkable's screen to Mac/PC | https://github.com/rien/reStream |
| **KOReader** | Alternative reader (more formats, customizable) | Via SSH |
| **reGitable** | Automatic backup via git | awesome-reMarkable |

### Custom templates

```bash
# Create an SVG template, copy via SSH
scp mon-template.svg root@10.11.99.1:/usr/share/remarkable/templates/

# Edit templates.json to register it
ssh root@10.11.99.1 'vi /usr/share/remarkable/templates/templates.json'
```

**Generation tools**: ReCalendar.me, Remarkable Grid Generator, Remarkably Planner Builder

---

## 6. Underused Native Features

**Effort: zero | Included in Connect (~6 EUR/month)**

| Feature | Usage |
|---------|-------|
| **Handwriting conversion** | Select, convert, copy/paste into any app |
| **Cloud sync** | Google Drive, Dropbox, OneDrive |
| **Send to Slack** | Share meeting notes directly into a channel |
| **Handwriting search** (beta AI) | Search through your past handwritten notes |
| **Screen sharing** | Share the screen on a PC (presentations, meetings) |
| **Send to email** | Send as PDF or PNG |

**Tip**: Handwriting-to-text conversion works well for isolated words but less well for dense cursive sentences. Prefer print handwriting for conversion.

---

## 7. Official API and Developer Portal

| Resource | Link |
|-----------|------|
| **Developer Portal** | https://developer.remarkable.com |
| **Cloud API docs** | https://github.com/splitbrain/ReMarkableAPI |
| **Community guide** | https://remarkable.guide/ |
| **rmfakecloud** | Self-hosted Cloud (no Connect subscription) |

**OS**: Linux (Codex), full SSH root access, GPL-compliant. The cross-compiler toolchain allows deploying custom native apps.

**rmfakecloud**: Open-source alternative to the reMarkable cloud, for self-hosting sync and skipping the Connect subscription.

---

## 8. Zapier Automation

**ROI: medium | Effort: low | No code required**

**Mechanism**: reMarkable, then email (my@remarkable.com), then Zapier intercepts, then automatic action

### Possible destinations

Google Drive, Asana, ClickUp, Trello, Slack, WordPress, Evernote, Notion

### Free plan

- 100 tasks/month
- 2-step Zaps
- Check every 15 min

### Concrete workflows

```
Meeting notes → PDF auto-uploaded to Google Drive
Sketches → File sent to a Slack channel
Action items → Tasks created in Asana/ClickUp
```

**Source**: https://myremarkable.substack.com/p/integrating-remarkable

---

## 9. Read-it-later: Web to reMarkable

**ROI: high for reading | Effort: near zero**

| Tool | Description |
|-------|-------------|
| **Chrome extension "Read on reMarkable"** | Save any web page as EPUB/PDF on the tablet (ads removed) |
| **Goosepaper** | Daily RSS feed + news + Wikipedia, formatted for e-ink |
| **remarkable_news** | Daily news/comics/images as a screensaver |
| **Instapaper workaround** | Download articles as EPUB, import via desktop app |

**PDF option**: Right-click the extension, "Read on reMarkable as PDF" (adjustable margins for annotating).

---

## 10. Meeting Notes → AI Summary

**ROI: high | Effort: very low**

### Manual workflow (without MCP)

```
1. Handwritten notes during the meeting
2. Screenshot via the reMarkable mobile app (or cloud sync)
3. Upload the image to Claude/ChatGPT
4. Prompt: "Summarize these notes, extract action items with deadlines and owners"
```

### MCP workflow (with remarkable-mcp installed)

```
Claude, summarize my notes from today's meeting
→ Claude fetches the files via SSH
→ OCR if needed
→ Structured summary, directly
```

**MCP advantage**: Skips the screenshot and upload steps. Works even without a Connect subscription.

### Recommended template

Paper Pro Move Meeting Notebook: 60 meetings, 5 interlinked pages per meeting (overview + notes + action items + follow-up).

---

## 11. Zotero to reMarkable (research)

**ROI: high if you read papers | Effort: medium**

| Tool | Usage |
|-------|-------|
| **Zotero2reMarkable Bridge** | Sync PDFs from Zotero with highlight support |
| **KOReader + Toltec + Zotero plugin** | Better 2-column PDF reading, bidirectional sync |
| **sync_zotero_remarkable** | Lighter alternative |

**Honest limitation**: reMarkable is a closed system. Zotero integration requires workarounds. Not as smooth as an Android e-reader with native Zotero. Functional but with friction.

---

## 12. Screen sharing as an AI-assisted whiteboard

**ROI: presentation/facilitation | Effort: zero (native Connect feature)**

- **Screen Share**: Your live handwriting appears on the external screen/virtual meeting
- **Laser pointer**: Pen near the top of the screen activates a laser pointer
- **Combo workflow**: Screen Share + a colleague feeding your notes into ChatGPT in real time = augmented whiteboard

**Price**: Included in Connect (~$30/year US, ~6 EUR/month EU).

---

## 13. Custom apps and fun hacks

| App/Hack | Description |
|----------|-------------|
| **Ephemeris** | Daily agenda generated from your calendars (Python) |
| **Remarcal** | Sync Google/Outlook/Apple calendars to reMarkable |
| **reMarkable keywriter** | Distraction-free keyboard notes app |
| **remarkable-wikipedia** | Offline Wikipedia reader |
| **whiteboard-hypercard** | Live collaboration, shared drawing |
| **NetSurf** | Minimal web browser (via SSH) |
| **pdf2remarkable** | Upload PDFs to the cloud from the command line |
| **send-to-remarkable** | Upload docs by email (send-to-Kindle style) |
| **libreMarkable** | Framework for developing native apps |
| **oxide/remux/draft** | Launchers for multitasking |
| **latex-yearly-planner** | Annual planner generated in LaTeX |

**Full catalog**: https://github.com/reHackable/awesome-reMarkable

---

## 14. AI-augmented workflows to build

Workflows not yet packaged but achievable with the building blocks available.

### A. AI-analyzed logbook

```
Every evening → write 1 page of reflection on the reMarkable
→ remarkable-mcp + Claude → weekly analysis of patterns, emotions, decisions
→ Output: insights in Obsidian with a connection graph
```

### B. Assisted inbox processing

```
Papers/articles read and annotated on reMarkable
→ OCR via Claude Vision → structured summaries
→ Automatic tags + filing in Obsidian/Notion
```

### C. Sketch-to-code

```
Draw a UI wireframe on reMarkable
→ Screenshot → Claude Vision → HTML/React code
```

### D. Automatic flashcards

```
Course/reading notes on reMarkable
→ remarkable-mcp → Claude extracts the key concepts
→ Automatically generates Anki flashcards
```

### E. Automated daily standup

```
TODOs written every morning (custom template)
→ OCR → Slack/email automatically formatted
→ End of day: check off items, diff sent
```

### F. Brainstorm capture → Mind map

```
Freely scribbled ideas
→ Claude Vision analyzes the spatial layout + text
→ Generates a structured mind map (Mermaid/Markmap)
```

---

## 15. Where to start

### Phase 1: This weekend (2h)

1. Enable SSH via Settings → Help → Copyrights and licenses
2. Install **remarkable-mcp** and connect it to Claude Code
3. Test: ask Claude to search through your notes

### Phase 2: The following week

4. If you use Obsidian, install Scrybble
5. Try **Ghostwriter** (10 min to install, fun guaranteed)

### Phase 3: When you want to go further

6. Build a custom OCR pipeline with Claude Vision API
7. Explore rmfakecloud to skip the Connect subscription

---

## Sources

**GitHub projects**

- https://github.com/SamMorrowDrums/remarkable-mcp (MCP server, Nov 2025)
- https://github.com/awwaiid/ghostwriter (Vision-LLM interface)
- https://github.com/reHackable/awesome-reMarkable (community catalog)
- https://github.com/hersle/rmirro (sync without cloud)
- https://github.com/bordaigorl/remy (GUI SSH)
- https://github.com/rien/reStream (screen streaming)
- https://github.com/splitbrain/ReMarkableAPI (Cloud API docs)
- https://github.com/ricklupton/rmscene (native .rm parsing)

**Articles and discussions**

- https://sam-morrow.com/blog/building-an-mcp-server-for-remarkable
- https://news.ycombinator.com/item?id=47110872 (rmirror + Claude OCR, Feb 2026)
- https://news.ycombinator.com/item?id=42979986 (Ghostwriter HN)
- https://news.ycombinator.com/item?id=46099997 (Hacking reMarkable 2, HN 2025)
- https://sgt.hootr.club/blog/hacking-on-the-remarkable-2/ (SSH hacking guide)
- https://myremarkable.substack.com/p/integrating-remarkable (Zapier integration)

**Obsidian**

- https://forum.obsidian.md/t/scrybble-sync-plugin/103194
- https://www.youtube.com/watch?v=EsRdi8J9Cnc (Cloud sync demo)

**Official**

- https://developer.remarkable.com (Developer Portal, SDK, API)
- https://remarkable.guide/ (Community guide)
