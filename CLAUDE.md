# Claude Code Ultimate Guide - Project Context

## Purpose

This repository is the **comprehensive documentation for Claude Code** (Anthropic's CLI tool). It teaches users how to use Claude Code effectively through guides, examples, and templates.

**Meta-note**: This repo documents Claude Code, so its own configuration should be exemplary.

## Repository Structure

```
guide/                    # Core documentation
├── ultimate-guide.md     # Main guide (~26K lines, the reference)
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
├── reference.yaml        # Condensed index (~43K tokens)
└── llms.txt              # AI indexation file

whitepapers/              # Focused whitepapers (FR + EN)
├── fr/                   # 10 source files in French (.qmd)
└── en/                   # 10 translated files in English (.qmd)
# Published at: https://cc.bruniaux.com/whitepapers/

tools/                    # Interactive utilities
├── audit-prompt.md       # Setup audit prompt
└── onboarding-prompt.md  # Personalized learning prompt

docs/                     # Public documentation (tracked)
└── resource-evaluations/ # External resource evaluations (167 files)

claudedocs/               # Claude working documents (gitignored)
├── resource-evaluations/ # Research working docs (prompts, private audits)
└── *.md                  # Analysis reports, plans, working docs
```

## Key Files

| File | Purpose |
|------|---------|
| `VERSION` | Single source of truth for version (currently 3.41.1) |
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

### Whitepaper, Recap Cards & Guide Export

Full build commands (PDF/EPUB/recap-card), stack details, ebook versioning, and Typst template sync rules:

@docs/workflows/whitepaper-build.md

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

Sync workflow, trigger conditions, guide reader rebuild, RSS feed, sitemap, and announcement banner:

@docs/workflows/landing-sync.md

## Ecosystem (4 Repositories)

Architecture, repo details, cross-repo sync triggers, relations between repos, and history:

@docs/ecosystem.md

## Research Resources

**Perplexity Pro disponible**: Pour toute recherche nécessitant des sources fiables ou des informations récentes sur Claude Code, Anthropic, ou les pratiques de développement assisté par IA:
- Demande-moi de faire une recherche Perplexity (plus efficace que WebSearch basique)
- Je te fournirai les résultats avec les sources
- Utile pour: nouvelles features Claude Code, best practices communauté, comparaisons d'outils, documentation officielle mise à jour

## Claude Code Releases Tracking

Files, update workflow, and YAML entry format:

@docs/workflows/releases-tracking.md

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
| `docs/resource-evaluations/` | Final evaluations (167 files) | ✅ Git tracked (public) |
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
