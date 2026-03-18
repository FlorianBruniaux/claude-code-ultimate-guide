# Claude Code Ultimate Guide - Project Context

## Purpose

This repository is the **comprehensive documentation for Claude Code** (Anthropic's CLI tool). It teaches users how to use Claude Code effectively through guides, examples, and templates.

**Meta-note**: This repo documents Claude Code, so its own configuration should be exemplary.

## Repository Structure

```
guide/                    # Core documentation
├── ultimate-guide.md     # Main guide (~20K lines, the reference)
├── cheatsheet.md         # 1-page printable summary
├── cowork.md             # Cowork redirect page
├── core/                 # Architecture, methodologies, releases, known-issues, visual-reference
├── security/             # security-hardening, sandbox-isolation, sandbox-native, production-safety, data-privacy
├── ecosystem/            # ai-ecosystem, mcp-servers-ecosystem, third-party-tools, remarkable-ai
├── roles/                # ai-roles, adoption-approaches, learning-with-ai, agent-evaluation
├── ops/                  # devops-sre, observability, ai-traceability
├── diagrams/             # Mermaid visual diagrams
└── workflows/            # Step-by-step workflow guides

examples/                 # Production-ready templates
├── agents/               # Custom agent templates
├── commands/             # Slash command templates
├── hooks/                # Event hook examples (bash/powershell)
├── skills/               # Skill module templates
└── scripts/              # Utility scripts (audit, health check)

machine-readable/         # For LLM consumption
├── reference.yaml        # Condensed index (~2K tokens)
└── llms.txt              # AI indexation file

whitepapers/              # Focused whitepapers (FR + EN)
├── fr/                   # 10 source files in French (.qmd)
└── en/                   # 10 translated files in English (.qmd)
# Published at: https://www.florian.bruniaux.com/guides

tools/                    # Interactive utilities
├── audit-prompt.md       # Setup audit prompt
└── onboarding-prompt.md  # Personalized learning prompt

docs/                     # Public documentation (tracked)
└── resource-evaluations/ # External resource evaluations (68 files)

claudedocs/               # Claude working documents (gitignored)
├── resource-evaluations/ # Research working docs (prompts, private audits)
└── *.md                  # Analysis reports, plans, working docs
```

## Key Files

| File | Purpose |
|------|---------|
| `VERSION` | Single source of truth for version (currently 3.34.1) |
| `guide/ultimate-guide.md` | The main reference (search here first) |
| `guide/cheatsheet.md` | Quick reference for daily use |
| `machine-readable/reference.yaml` | LLM-optimized index with line numbers |
| `CHANGELOG.md` | All changes with detailed descriptions |

## Commands

### Version Management
```bash
# Check version consistency across all docs
./scripts/sync-version.sh --check

# Fix version mismatches (updates from VERSION file)
./scripts/sync-version.sh

# Bump version
echo "3.7.0" > VERSION && ./scripts/sync-version.sh
```

### Whitepaper Generation (PDF + EPUB)

```bash
# --- PDF (default format: whitepaper-typst → Typst → PDF) ---

# Single file
cd whitepapers/fr && quarto render 00-introduction-serie.qmd

# All FR whitepapers
cd whitepapers/fr && quarto render *.qmd

# All EN whitepapers
cd whitepapers/en && quarto render *.qmd

# Preview with hot-reload
cd whitepapers/fr && quarto preview 00-introduction-serie.qmd

# Batch with error summary (loop)
cd whitepapers/fr && for f in *.qmd; do echo "→ $f" && quarto render "$f" 2>&1 | grep -E "(Output created|ERROR)"; done

# --- EPUB (format: epub → Pandoc → EPUB3) ---

# Single file
cd whitepapers/fr && quarto render 00-introduction-serie.qmd --to epub

# All EPUBs (FR + EN) → epub-output/{fr,en}/
cd whitepapers && ./render-epub.sh all
cd whitepapers && ./render-epub.sh fr   # French only
cd whitepapers && ./render-epub.sh en   # English only
```

**PDF stack** : Quarto → Typst 0.13 → PDF. Template : `whitepapers/_extensions/whitepaper/`. Palette Bold Guy (warm beige + orange brûlé).

**EPUB stack** : Quarto → Pandoc → EPUB3. CSS : `whitepapers/epub-styles.css`. Cover : `_extensions/whitepaper/assets/claude-code-ai-logo.jpg`.

**Skill disponible** : `/pdf-generator` pour aide contextuelle (template YAML, stack, dépannage).

### Recap Cards (Fiches Mémo Thématiques)

Fiches A4 1-page imprimables, format intermédiaire entre cheatsheet et whitepapers.

```bash
# Single card
cd whitepapers/recap-cards/fr && quarto render 01-commandes-essentielles.qmd --to recap-card-typst

# All FR cards (via script)
cd whitepapers/recap-cards && ./render-recap-cards.sh fr

# All cards (FR + EN)
cd whitepapers/recap-cards && ./render-recap-cards.sh all
```

**Stack** : Extension `recap-card` (`whitepapers/_extensions/recap-card/`). Format `recap-card-typst`. Même palette Bold Guy.

**Source des fiches** : `whitepapers/recap-cards/fr/*.qmd` (FR), `whitepapers/recap-cards/en/*.qmd` (EN à venir).

**25 fiches planifiées** — 5 prototypes Phase 1-2 livrés : 01, 03, 04, 06, 25.

### Before Committing
```bash
# Verify versions are synchronized
./scripts/sync-version.sh --check
```

### Slash Commands (Maintenance)

Custom slash commands available in this project:

| Command | Description |
|---------|-------------|
| `/release <bump-type>` | Release guide version (CHANGELOG + VERSION + sync + commit + push) |
| `/update-infos-release [bump-type]` | Update Claude Code releases tracking + optional guide version bump |
| `/version` | Display current guide and Claude Code versions with stats |
| `/changelog [count]` | View recent CHANGELOG entries (default: 5) |
| `/sync` | Check guide/landing synchronization status |
| `/audit-agents-skills [path]` | Audit quality of agents, skills, and commands in .claude/ config |
| `/security-check` | Quick config check against known threats database (~30s) |
| `/security-audit` | Full 6-phase security audit with score /100 (2-5min) |
| `/update-threat-db` | Research & update threat intelligence database |

**Examples:**
```
/release patch                 # Bump patch + release (3.20.4 → 3.20.5)
/release minor                 # Bump minor + release (3.20.4 → 3.21.0)
/update-infos-release          # Update CC releases only
/update-infos-release patch    # Update CC + bump guide (3.9.11 → 3.9.12)
/update-infos-release minor    # Update CC + bump guide (3.9.11 → 3.10.0)
/version                       # Show versions and content stats
/changelog 10                  # Last 10 CHANGELOG entries
/sync                          # Check guide/landing sync status
/audit-agents-skills           # Audit current project
/audit-agents-skills --fix     # Audit + fix suggestions
/audit-agents-skills ~/other   # Audit another project
/security-check                # Quick scan config vs known threats
/security-audit                # Full audit with posture score /100
/update-threat-db              # Research + update threat-db.yaml
```

These commands are defined in `.claude/commands/` and automate:
- Claude Code releases tracking (YAML + Markdown + Landing badge)
- Guide version management (VERSION file + sync across all docs)
- CHANGELOG updates
- Landing site synchronization verification
- Git commit and push to both repositories

### Command Naming Conventions

Implicit prefixes used in `.claude/commands/`:

| Prefix | Pattern | Examples |
|--------|---------|---------|
| `audit-*` | Quality checks with scored output | `audit-agents-skills`, `audit-deps` |
| `update-*` | Sync or refresh data from external source | `update-infos-release`, `update-threat-db` |
| `security-*` | Security scans, ascending depth | `security-check` (quick), `security-audit` (full) |
| *(no prefix)* | Core guide workflow commands | `release`, `sync`, `version`, `changelog` |

When adding a new command, pick the prefix that matches the action type. Avoid creating new prefix categories unless the existing four don't fit.

## Behavioral Rules

These rules come from observed friction patterns in actual sessions on this repo.

### Always update CHANGELOG.md
After any file modification or feature implementation, update `CHANGELOG.md` under `[Unreleased]`. Never skip this step unless explicitly told to. This is the most common missed step.

### Be exhaustive on first pass
When asked to analyze, audit, or review anything — read every relevant file. Do not do a superficial scan. If unsure of scope, ask rather than delivering shallow results. This applies to resource evaluations, doc audits, and codebase reviews.

### Use absolute paths
When referencing files in documentation, reports, or resource evaluations, always use full absolute paths. Never relative paths.

### Closing checklist
After completing all requested tasks, always confirm unprompted:
1. Files changed (list them)
2. CHANGELOG.md updated
3. Committed and pushed (if applicable) — include the commit hash

### Bias toward action
Do not spend extended time in exploration or planning loops. Produce files and concrete output early, then iterate. If stuck for more than 2 attempts on any step, explain the blocker instead of looping.

## Conventions

### Documentation Style
- **Accuracy over marketing**: No invented percentages or unverified claims
- **Practical examples**: Every concept has a concrete example
- **Source attribution**: Credit community contributions with links
- **Version alignment**: All version numbers must match `VERSION` file

### File Organization
- New guides → `guide/`
- New templates → `examples/{agents,commands,hooks,skills}/`
- Navigation updates → Update both `README.md` and `guide/README.md`

### Versioning
- `VERSION` file is the single source of truth
- Run `./scripts/sync-version.sh` after changing version
- Files that contain version: README.md, cheatsheet.md, ultimate-guide.md, reference.yaml

## Current Focus

Check `IDEAS.md` for planned improvements and `CHANGELOG.md [Unreleased]` for work in progress.

## Model Configuration

**Recommended mode**: `/model opusplan`

**Rationale**: This documentation repository benefits from hybrid intelligence:
- **Planning phase** (Opus + thinking): Architecture decisions, research synthesis, multi-file analysis
- **Execution phase** (Sonnet): Doc updates, version syncing, template edits, formatting

**OpusPlan workflow**:
1. `/model opusplan` → Set hybrid mode
2. `/plan` or `Shift+Tab × 2` → Plan with Opus (thinking enabled)
3. `Shift+Tab` → Execute with Sonnet (faster, cheaper)

**Typical task breakdown**:
| Task Type | Model | Justification |
|-----------|-------|---------------|
| Doc edits, typo fixes | Sonnet | Straightforward, no deep reasoning |
| Version sync, formatting | Sonnet | Mechanical pattern matching |
| Guide restructuring | Opus (plan) → Sonnet (execute) | Needs architecture thinking first |
| Research synthesis | Opus (plan) → Sonnet (write) | Complex analysis, then clear writing |
| Multi-file consistency checks | Opus (plan) → Sonnet (fix) | Dependency analysis, then edits |

**Cost optimization**: OpusPlan pays Opus only for planning (typically 10-20% of tokens), Sonnet handles 80-90% of execution work.

## Landing Site Synchronization

**Important**: Ce guide a un site landing associé qui doit être mis à jour après certains changements.

**Landing repo**: `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/`

### Éléments à synchroniser

| Élément | Source (guide) | Destination (landing) |
|---------|----------------|----------------------|
| Version | `VERSION` | index.html footer + FAQ |
| Templates count | Count `examples/` files | Badges, title, meta tags |
| Guide lines | `wc -l guide/ultimate-guide.md` | Badges |
| Golden Rules | README.md | index.html section |
| FAQ | README.md | index.html FAQ |

### Triggers de sync

Après ces modifications, **rappeler** de mettre à jour le landing:

1. **Version bump** → Modifier `VERSION` ici, puis landing
2. **Ajout/suppression templates** → Recalculer count, mettre à jour landing
3. **Modification Golden Rules ou FAQ** → Répercuter sur landing
4. **Changement significatif du guide** (>100 lignes)

### Rebuild du guide reader (à chaque release)

Le landing expose le contenu du guide sur `cc.bruniaux.com/guide/`. Le contenu est généré depuis ce repo au moment du build — **jamais commité dans le landing**.

```bash
# Depuis le repo landing, avant chaque push sur main :
cd ../claude-code-ultimate-guide-landing
node scripts/prepare-guide-content.mjs && pnpm build
```

**Quand le faire** : à chaque release (`/release patch|minor|major`) pour que le site reflète la dernière version du guide.

### Commande de vérification

```bash
./scripts/check-landing-sync.sh
```

**Ce que fait le script (4 vérifications):**

| Check | Source | Comparaison |
|-------|--------|-------------|
| Version | `VERSION` | index.html (footer + FAQ) |
| Templates | `find examples/` | index.html + examples.html |
| Quiz questions | `questions.json` | index.html + quiz.html |
| Guide lines | `wc -l ultimate-guide.md` | index.html (tolérance ±500) |

**Output attendu (si synchronisé):**
```
=== Landing Site Sync Check ===

1. Version
   Guide:   3.8.1
   Landing: 3.8.1
   OK

2. Templates Count
   Guide:         53 files
   index.html:    53
   examples.html: 53
   OK

3. Quiz Questions
   questions.json: 159
   index.html:     159
   quiz.html:      159
   OK

4. Guide Lines
   Actual:  9881
   Landing: 9800+ (approximate)
   OK (within tolerance)

=== Summary ===
All synced!
```

**En cas de mismatch:**
- Le script indique quel fichier est désynchronisé
- Exit code = nombre d'issues trouvées
- Consulter `landing/CLAUDE.md` pour les numéros de ligne exacts à modifier

## Écosystème Complet (4 Repositories)

Ce guide fait partie d'un écosystème de 4 repositories interconnectés, séparant les audiences (devs vs knowledge workers) et les use cases (documentation vs vitrine).

### Architecture

```
        REPOS SOURCES (Documentation)
        ┌──────────────────┬──────────────────┐
        │                  │                  │
    ┌───▼───┐          ┌───▼───┐
    │ Guide │          │Cowork │
    │ Code  │◄────────►│ Guide │
    │ vX.Y  │ liens    │ v1.0  │
    └───┬───┘          └───┬───┘
        │                  │
        │ source           │ source
        │                  │
        LANDING SITES (Vitrine)
        ┌──────────────────┬──────────────────┐
        │                  │                  │
    ┌───▼───┐          ┌───▼───┐
    │ Code  │◄────────►│Cowork │
    │Landing│cross-links│Landing│
    │ vX.Y  │          │ v1.0  │
    └───────┘          └───────┘
```

### 1. Claude Code Ultimate Guide (ce repo)

**Pour qui**: Développeurs utilisant Claude Code CLI

| Aspect | Détails |
|--------|---------|
| **GitHub** | https://github.com/FlorianBruniaux/claude-code-ultimate-guide |
| **Local** | `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/` |
| **Contenu** | Guide ~19K lignes, 116 templates, workflows, architecture |
| **Audience** | Développeurs, DevOps, tech leads |

### 2. Claude Cowork Guide (repo dédié)

**Pour qui**: Knowledge workers utilisant Claude Desktop (non-devs)

| Aspect | Détails |
|--------|---------|
| **GitHub** | https://github.com/FlorianBruniaux/claude-cowork-guide |
| **Local** | `/Users/florianbruniaux/Sites/perso/claude-cowork-guide/` |
| **Contenu** | 6 guides, 67 prompts, 5 workflows, cheatsheet, FAQ |
| **Audience** | Non-devs, assistants, managers, knowledge workers |

**Migration**: Le dossier `cowork/` a été migré du repo principal vers ce repo dédié (v1.0.0, commit 7a686a8).

### 3. Code Landing Site

**Pour qui**: Visiteurs découvrant le guide Code

| Aspect | Détails |
|--------|---------|
| **Local** | `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/` |
| **Contenu** | Page marketing, badges, FAQ, quiz (274 questions) |
| **Sync avec** | Guide principal (version, templates, guide lines) |

### 4. Cowork Landing Site

**Pour qui**: Visiteurs découvrant le guide Cowork

| Aspect | Détails |
|--------|---------|
| **Local** | `/Users/florianbruniaux/Sites/perso/claude-cowork-guide-landing/` |
| **Contenu** | Page marketing Cowork, prompts showcase |
| **Sync avec** | Cowork guide (version, prompts count) |

### Synchronisation Inter-Repos

**Déclencheurs de mise à jour multi-repos**:

| Changement | Repos à mettre à jour |
|------------|----------------------|
| Version bump (Guide Code) | 1. Guide Code, 2. Code Landing |
| Templates ajoutés/supprimés | 1. Guide Code, 2. Code Landing |
| Version bump (Cowork) | 1. Cowork Guide, 2. Cowork Landing |
| Prompts ajoutés/supprimés | 1. Cowork Guide, 2. Cowork Landing |
| Cross-links modifiés | Tous les 4 repos |

**Scripts de vérification**:

```bash
# Vérifier sync Code Landing
./scripts/check-landing-sync.sh

# Vérifier sync Cowork
cd ../claude-cowork-guide && ./scripts/check-version-sync.sh
```

### Relations & Liens

**Guide Code → Cowork Guide**:
- `guide/cowork.md`: Summary avec liens vers repo dédié
- `guide/README.md`: Table avec 6 liens vers guides Cowork
- `machine-readable/reference.yaml`: 23 entrées pointant vers GitHub

**Landing Code ↔ Landing Cowork**:
- Cross-links bidirectionnels (hero, ecosystem, sections)
- Navigation fluide entre les 2 audiences

**Principe**: Séparation claire des audiences, navigation facilitée, synchronisation maintenue.

### Historique de l'Écosystème

| Date | Événement | Commits |
|------|-----------|---------|
| 2026-01-19 | Création repo Cowork dédié v1.0.0 | 7a686a8 |
| 2026-01-19 | MAJ README Guide Code → liens GitHub | 9a743cd |
| 2026-01-20 | Suppression cowork/ du guide principal | 9a29ba4 |
| 2026-01-20 | Sync Code Landing (v3.9.7, 66 templates) | 5b5ce62 |
| 2026-01-20 | Fix Cowork Landing (paths, README, UI) | cab83f5, af497b7, 539912b |

**Résultat**: 7 commits, 4 repos synchronisés, -8,297 lignes (cleanup massif), écosystème opérationnel.

## Research Resources

**Perplexity Pro disponible**: Pour toute recherche nécessitant des sources fiables ou des informations récentes sur Claude Code, Anthropic, ou les pratiques de développement assisté par IA:
- Demande-moi de faire une recherche Perplexity (plus efficace que WebSearch basique)
- Je te fournirai les résultats avec les sources
- Utile pour: nouvelles features Claude Code, best practices communauté, comparaisons d'outils, documentation officielle mise à jour

## Claude Code Releases Tracking

Ce repo maintient un historique condensé des releases officielles de Claude Code.

### Fichiers

| Fichier | Rôle |
|---------|------|
| `machine-readable/claude-code-releases.yaml` | Source de vérité (YAML) |
| `guide/core/claude-code-releases.md` | Version lisible (Markdown) |
| `scripts/update-cc-releases.sh` | Script de vérification des nouvelles versions |

### Vérifier les nouvelles versions

```bash
./scripts/update-cc-releases.sh
```

Le script:
1. Fetch le CHANGELOG officiel depuis GitHub
2. Compare avec notre version trackée
3. Affiche les nouvelles releases à condenser

### Workflow de mise à jour

1. **Vérifier**: `./scripts/update-cc-releases.sh`
2. **MAJ YAML**: Ajouter nouvelle entrée dans `claude-code-releases.yaml`
   - Mettre à jour `latest` et `updated`
   - Ajouter l'entrée dans `releases` (condensée: 2-4 highlights max)
   - Ajouter aux `breaking_summary` si applicable
   - Ajouter aux `milestones` si feature majeure
3. **MAJ Markdown**: Mettre à jour `claude-code-releases.md` en cohérence
4. **Landing sync**: `./scripts/check-landing-sync.sh`
5. **Commit**: `docs: update Claude Code releases (vX.Y.Z)`

### Format des entrées YAML

```yaml
- version: "2.1.13"
  date: "2026-01-20"
  highlights:
    - "Feature principale"
    - "Autre feature notable"
  breaking:
    - "Description du breaking change (si applicable)"
```

## Resource Evaluation Workflow

External resources (articles, videos, discussions) are evaluated before integration into the guide.

### Process

1. **Research**: Initial Perplexity search → Save prompt + results in `claudedocs/resource-evaluations/` (private)
1b. **Cross-reference**: Si ressource liée à Claude Code, vérifier les claims contre `https://code.claude.com/docs/llms-full.txt` (source officielle ~98KB)
2. **Evaluation**: Systematic scoring (1-5) → Create evaluation file in `docs/resource-evaluations/` (tracked)
3. **Challenge**: Technical review by agent to ensure objectivity
4. **Decision**: Integrate (score 3+), mention (score 2), or reject (score 1)

### File Organization

| Location | Content | Tracking |
|----------|---------|----------|
| `docs/resource-evaluations/` | Final evaluations (68 files) | ✅ Git tracked (public) |
| `claudedocs/resource-evaluations/` | Working docs, prompts, private audits | ❌ Gitignored (private) |

### Scoring Grid

| Score | Action |
|-------|--------|
| 5 | Critical - Integrate immediately (<24h) |
| 4 | High Value - Integrate within 1 week |
| 3 | Moderate - Integrate when time available |
| 2 | Marginal - Minimal mention or skip |
| 1 | Low - Reject |

See full methodology: [`docs/resource-evaluations/README.md`](docs/resource-evaluations/README.md)

## Quick Lookups

For answering questions about Claude Code:
0. **Doc officielle Anthropic (LLM-optimized)**: `https://code.claude.com/docs/llms.txt` (index ~65 pages) ou `https://code.claude.com/docs/llms-full.txt` (doc complète ~98KB) pour les faits officiels
1. Search `machine-readable/reference.yaml` first (has line numbers to full guide)
2. Use those line numbers to read relevant sections from `guide/ultimate-guide.md`
3. Check `examples/` for ready-to-use templates
4. Check `guide/core/claude-code-releases.md` for recent features/changes
5. Si info manquante ou incertaine → demander une recherche Perplexity (communauté, comparaisons, retours)
