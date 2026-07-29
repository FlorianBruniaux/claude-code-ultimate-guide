# Ecosystem: 4 Interconnected Repositories

This guide is part of a 4-repo ecosystem separating audiences (devs vs knowledge workers) and use cases (documentation vs showcase).

## Architecture

```
        SOURCE REPOS (Documentation)
        ┌──────────────────┬──────────────────┐
        │                  │                  │
    ┌───▼───┐          ┌───▼───┐
    │ Guide │          │Cowork │
    │ Code  │◄────────►│ Guide │
    │ vX.Y  │ links    │ v1.0  │
    └───┬───┘          └───┬───┘
        │                  │
        │ source           │ source
        │                  │
        LANDING SITES (Showcase)      DISTRIBUTION
        ┌──────────────────┬──────────────────┐       ┌──────────────┐
        │                  │                  │       │              │
    ┌───▼───┐          ┌───▼───┐          ┌───▼───────▼──┐
    │ Code  │◄────────►│Cowork │          │   Plugins    │
    │Landing│cross-links│Landing│          │  Marketplace │
    │ vX.Y  │          │ v1.0  │          │  (8 plugins) │
    └───────┘          └───────┘          └──────────────┘
```

## 1. Claude Code Ultimate Guide (this repo)

**For**: Developers using Claude Code CLI

| Aspect | Details |
|--------|---------|
| **GitHub** | https://github.com/FlorianBruniaux/claude-code-ultimate-guide |
| **Local** | `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/` |
| **Content** | Guide ~25K lines, 268 templates, workflows, architecture |
| **Audience** | Developers, DevOps, tech leads |

## 2. Claude Cowork Guide (dedicated repo)

**For**: Knowledge workers using Claude Desktop (non-devs)

| Aspect | Details |
|--------|---------|
| **GitHub** | https://github.com/FlorianBruniaux/claude-cowork-guide |
| **Local** | `/Users/florianbruniaux/Sites/perso/claude-cowork-guide/` |
| **Content** | 6 guides, 67 prompts, 5 workflows, cheatsheet, FAQ |
| **Audience** | Non-devs, assistants, managers, knowledge workers |

**Migration**: The `cowork/` folder was migrated from the main repo to this dedicated repo (v1.0.0, commit 7a686a8).

## 3. Code Landing Site

**For**: Visitors discovering the Code guide

| Aspect | Details |
|--------|---------|
| **Local** | `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/` |
| **Content** | Marketing page, badges, FAQ, quiz (473 questions) |
| **Syncs with** | Main guide (version, templates, guide lines) |

## 3b. Claude Code Plugins (Marketplace)

**For**: Developers who want to install guide templates without manual file copying

| Aspect | Details |
|--------|---------|
| **GitHub** | https://github.com/FlorianBruniaux/claude-code-plugins |
| **Local** | `/Users/florianbruniaux/Sites/perso/claude-code-plugins/` |
| **Content** | 8 plugins, 181 templates migrated from `examples/` |
| **Audience** | All Claude Code users |

**Relationship**: Templates are authored and maintained in `examples/` of this repo. The plugins repo is a published copy — **source of truth stays here**.

**Install**:
```bash
claude plugin marketplace add FlorianBruniaux/claude-code-plugins
claude plugin install security-suite   # or any of the 8 plugins
```

**Plugins**: security-suite, devops-pipeline, release-automation, code-quality, pr-workflow, session-tools, ai-methodology, session-summary

## 4. Cowork Landing Site

**For**: Visitors discovering the Cowork guide

| Aspect | Details |
|--------|---------|
| **Local** | `/Users/florianbruniaux/Sites/perso/claude-cowork-guide-landing/` |
| **Content** | Cowork marketing page, prompts showcase |
| **Syncs with** | Cowork guide (version, prompts count) |

## Cross-Repo Sync Triggers

| Change | Repos to update |
|--------|----------------|
| Version bump (Code Guide) | 1. Code Guide, 2. Code Landing |
| Templates added/removed | 1. Code Guide, 2. Code Landing, 3. Plugins repo |
| Plugin added/updated | 1. Plugins repo, 2. Code Guide README, 3. Code Landing ecosystem-data |
| Version bump (Cowork) | 1. Cowork Guide, 2. Cowork Landing |
| Prompts added/removed | 1. Cowork Guide, 2. Cowork Landing |
| Cross-links modified | All repos |

**Verification scripts**:

```bash
# Check Code Landing sync
./scripts/check-landing-sync.sh

# Check Cowork sync
cd ../claude-cowork-guide && ./scripts/check-version-sync.sh
```

## Relations & Links

**Code Guide → Cowork Guide**:
- `guide/cowork.md`: Summary with links to dedicated repo
- `guide/README.md`: Table with 6 links to Cowork guides
- `machine-readable/reference.yaml`: 23 entries pointing to GitHub

**Code Landing ↔ Cowork Landing**:
- Bidirectional cross-links (hero, ecosystem, sections)
- Smooth navigation between the 2 audiences

**Principle**: Clear audience separation, easy navigation, maintained synchronization.

## Ecosystem History

| Date | Event | Commits |
|------|-------|---------|
| 2026-01-19 | Cowork dedicated repo created v1.0.0 | 7a686a8 |
| 2026-01-19 | Code Guide README → GitHub links | 9a743cd |
| 2026-01-20 | Remove cowork/ from main guide | 9a29ba4 |
| 2026-01-20 | Sync Code Landing (v3.9.7, 66 templates) | 5b5ce62 |
| 2026-01-20 | Fix Cowork Landing (paths, README, UI) | cab83f5, af497b7, 539912b |

**Result**: 7 commits, 4 repos synchronized, -8,297 lines (massive cleanup), ecosystem operational.
