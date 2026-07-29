---
name: audit-repo-docs
description: Audit repository documentation against 85+ best practices from claude-code-ultimate-guide
---

# Documentation Audit Skill

Analyze a repository's documentation quality and generate improvement recommendations based on 85+ patterns from the Claude Code Ultimate Guide.

## Usage

```
/audit-repo-docs              # Audit only, generate markdown report
/audit-repo-docs --generate   # Audit + propose creating missing files
```

## Workflow

### Phase 1: Discovery (Read-Only)

Scan the repository structure to detect existing documentation files.

**Files to check:**

```bash
# Root files
ls -la README.md VERSION CHANGELOG.md CLAUDE.md CONTRIBUTING.md LICENSE .gitignore 2>/dev/null

# Documentation structure
ls -la docs/ guide/ documentation/ 2>/dev/null

# Machine-readable
ls -la machine-readable/ llms.txt robots.txt 2>/dev/null

# Automation
ls -la scripts/*.sh 2>/dev/null

# Examples
find examples/ -type f 2>/dev/null | head -20
```

**Pattern detection:**

```bash
# Check README Quick Start
grep -n "Quick Start\|Getting Started\|Installation" README.md 2>/dev/null | head -3

# Check for badges
grep -c "\!\[.*\](.*badge.*)" README.md 2>/dev/null || echo "0"

# Check CHANGELOG format
head -20 CHANGELOG.md 2>/dev/null

# Check VERSION format
cat VERSION 2>/dev/null

# Check for TOC
grep -n "Table of Contents\|## Contents" README.md 2>/dev/null

# Check for metadata in docs
grep -rn "^---$\|author:\|date:\|version:" docs/ guide/ 2>/dev/null | head -10
```

### Phase 2: Evaluation (30 Criteria)

Score each criterion as: ✅ (present), ⚠️ (partial), ❌ (missing)

#### Category 1: Root Files (8 criteria, weight ×3)

| # | Criterion | Detection | Points |
|---|-----------|-----------|--------|
| 1.1 | README.md with Quick Start < 40 lines | `head -50 README.md | grep -n "Quick Start"` | 3 |
| 1.2 | VERSION (single semver line) | `cat VERSION` matches `^\d+\.\d+\.\d+$` | 3 |
| 1.3 | CHANGELOG.md (Keep a Changelog format) | Has `## [Unreleased]` or `## [x.y.z]` sections | 3 |
| 1.4 | CLAUDE.md (project instructions) | File exists with > 10 lines | 3 |
| 1.5 | CONTRIBUTING.md | File exists | 3 |
| 1.6 | LICENSE | File exists | 3 |
| 1.7 | .gitignore (categorized sections) | Has comment sections `# Category` | 3 |
| 1.8 | Functional badges in README | At least 2 badge images | 3 |

#### Category 2: Documentation Structure (7 criteria, weight ×2)

| # | Criterion | Detection | Points |
|---|-----------|-----------|--------|
| 2.1 | Dedicated docs folder | `docs/` or `guide/` exists | 2 |
| 2.2 | Metadata in docs (author, date, version) | YAML frontmatter in .md files | 2 |
| 2.3 | Table of Contents with anchors | `## Table of Contents` or `## Contents` with links | 2 |
| 2.4 | TL;DR or Quick Start section | Section exists in main doc | 2 |
| 2.5 | Time estimates | `Time:` or `minutes` or `hours` mentioned | 2 |
| 2.6 | Cheatsheet available | File named `cheatsheet.md` or similar | 2 |
| 2.7 | Examples in dedicated folder | `examples/` with > 3 files | 2 |

#### Category 3: Machine-Readable (5 criteria, weight ×1)

| # | Criterion | Detection | Points |
|---|-----------|-----------|--------|
| 3.1 | llms.txt or equivalent | File exists for AI indexation | 1 |
| 3.2 | Index YAML/JSON < 3K tokens | `machine-readable/` with index file | 1 |
| 3.3 | Line numbers for navigation | References like `file.md:123` in docs | 1 |
| 3.4 | Version synchronized | VERSION matches refs in README, docs | 1 |
| 3.5 | Keywords/tags | Tags or keywords in frontmatter | 1 |

#### Category 4: Automation (5 criteria, weight ×1)

| # | Criterion | Detection | Points |
|---|-----------|-----------|--------|
| 4.1 | Version sync script | `scripts/*version*` or `scripts/*sync*` | 1 |
| 4.2 | Check/verify script | `scripts/*check*` or `scripts/*verify*` | 1 |
| 4.3 | --check mode (dry-run) | Script supports `--check` flag | 1 |
| 4.4 | CI/CD integration | `.github/workflows/` with docs-related workflow | 1 |
| 4.5 | Slash commands documented | `.claude/commands/` with README or in CLAUDE.md | 1 |

#### Category 5: Quality (5 criteria, weight ×2)

| # | Criterion | Detection | Points |
|---|-----------|-----------|--------|
| 5.1 | Tables for structured data | At least 3 markdown tables in docs | 2 |
| 5.2 | Code blocks with language hints | ` ```language ` syntax used | 2 |
| 5.3 | Collapsibles for optional content | `<details>` tags used | 2 |
| 5.4 | Cross-references functional | Internal links `[text](./path)` present | 2 |
| 5.5 | Footer with version/date | Last line mentions version or date | 2 |

### Phase 3: Scoring

**Formula:**

```
Score = Σ(criteria_ok × weight) / Σ(max_weights) × 100

Max points:
- Root Files:     8 × 3 = 24
- Structure:      7 × 2 = 14
- Machine-Read:   5 × 1 = 5
- Automation:     5 × 1 = 5
- Quality:        5 × 2 = 10
─────────────────────────────
Total:            58 points
```

**Grade scale:**

| Score | Grade | Status |
|-------|-------|--------|
| 90-100 | A | 🟢 Excellent |
| 75-89 | B | 🟢 Good |
| 60-74 | C | 🟡 Needs work |
| 40-59 | D | 🟡 Significant gaps |
| 0-39 | F | 🔴 Critical issues |

### Phase 4: Generate Report

Output this exact format:

```markdown
# 📋 Documentation Audit Report

**Repository**: {repo_name}
**Date**: {current_date}
**Score**: {score}/100 ({grade})

## Summary

| Category | Score | Status |
|----------|-------|--------|
| Root Files | {x}/8 | {emoji} {percent}% |
| Structure | {x}/7 | {emoji} {percent}% |
| Machine-Readable | {x}/5 | {emoji} {percent}% |
| Automation | {x}/5 | {emoji} {percent}% |
| Quality | {x}/5 | {emoji} {percent}% |

## 🔴 Critical Issues (Priority 1)

{List missing items from Root Files category - weight ×3}

## 🟡 Recommended Improvements (Priority 2)

{List missing items from Structure and Quality categories - weight ×2}

## 🟢 Quick Wins (Priority 3)

{List easy-to-add items from any category that take < 5 min}

## 📝 Suggested Templates

{For each critical/recommended missing item, provide a collapsible template}

<details>
<summary>{filename} template</summary>

\`\`\`{format}
{template content}
\`\`\`

</details>
```

### Phase 5: Optional Generation (--generate flag)

If `$ARGUMENTS` contains `--generate`:

1. List all missing files that would be created
2. Ask user for approval: "Create these {n} files? (y/n/select)"
3. On approval, create files using provided templates
4. Report what was created

**Template sources:**

| File | Template Location |
|------|-------------------|
| VERSION | Single line: `1.0.0` |
| CHANGELOG.md | `examples/templates/` or Keep a Changelog format |
| CONTRIBUTING.md | Standard contributor guide |
| llms.txt | `machine-readable/llms.txt` as reference |
| Cheatsheet | `guide/cheatsheet.md` as reference |

## Example Output

```markdown
# 📋 Documentation Audit Report

**Repository**: my-awesome-project
**Date**: 2026-01-23
**Score**: 52/100 (D)

## Summary

| Category | Score | Status |
|----------|-------|--------|
| Root Files | 4/8 | 🟡 50% |
| Structure | 3/7 | 🟡 43% |
| Machine-Readable | 0/5 | 🔴 0% |
| Automation | 1/5 | 🔴 20% |
| Quality | 3/5 | 🟡 60% |

## 🔴 Critical Issues (Priority 1)

- Missing `VERSION` file (single source of truth for versioning)
- Missing `CHANGELOG.md` (track changes for users)
- Missing `CLAUDE.md` (AI context for Claude Code)
- No functional badges in README

## 🟡 Recommended Improvements (Priority 2)

- Add Table of Contents to README
- Create `examples/` folder with usage examples
- Add time estimates to documentation sections
- Create a cheatsheet for quick reference

## 🟢 Quick Wins (Priority 3)

- Add 2-3 badges to README (build status, version, license)
- Add `<details>` collapsibles for long code examples
- Add language hints to all code blocks

## 📝 Suggested Templates

<details>
<summary>VERSION template</summary>

```
1.0.0
```

</details>

<details>
<summary>CHANGELOG.md template</summary>

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup

## [1.0.0] - YYYY-MM-DD

### Added
- First release
```

</details>

<details>
<summary>CLAUDE.md template</summary>

```markdown
# {Project Name} - Claude Code Context

## Project Overview

{Brief description of what the project does}

## Tech Stack

- {Language/Framework}
- {Key dependencies}

## Directory Structure

\`\`\`
src/           # Source code
tests/         # Test files
docs/          # Documentation
\`\`\`

## Commands

\`\`\`bash
# Install dependencies
{install_command}

# Run tests
{test_command}

# Build
{build_command}
\`\`\`

## Conventions

- {Coding convention 1}
- {Coding convention 2}

## Current Focus

{What you're currently working on - update this regularly}
```

</details>

<details>
<summary>llms.txt template</summary>

```
# {Project Name}

> {One-line description}

## Overview

{2-3 sentences explaining what this project does}

## Key Files

- README.md - Project overview
- src/ - Source code
- docs/ - Documentation

## Quick Start

1. {Step 1}
2. {Step 2}
3. {Step 3}

## Keywords

{keyword1}, {keyword2}, {keyword3}
```

</details>
```

## Validation

After implementation, test:

1. **On this repo (claude-code-ultimate-guide)**: Expected score ~95%
2. **On minimal repo**: Create temp repo with just README, verify gap detection
3. **Templates validity**: Ensure generated templates are syntactically correct