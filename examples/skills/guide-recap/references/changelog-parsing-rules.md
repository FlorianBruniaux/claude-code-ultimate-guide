# CHANGELOG Parsing Rules

How to extract and categorize entries from `CHANGELOG.md` for social content generation.

## CHANGELOG Format

The project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

```
## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Added
- **Title**: Description
  - Sub-detail 1
  - Sub-detail 2

### Changed
- **Title**: Description

### Fixed
- **Title**: Description

---
(horizontal rule separates grouped entries within same version)
```

## Extraction Methods

### By Version (`/guide-recap v3.20.5`)

1. Read CHANGELOG.md
2. Find line matching `## [3.20.5]`
3. Extract everything until next `## [` line
4. Parse all `### Added/Changed/Fixed` sections

### Latest (`/guide-recap latest`)

1. Read CHANGELOG.md
2. Skip `## [Unreleased]`
3. Extract first `## [X.Y.Z]` block (= latest released version)

### By Week (`/guide-recap week` or `/guide-recap week 2026-01-27`)

1. Determine date range:
   - `week` with no date: Monday of current week -> today
   - `week YYYY-MM-DD`: That Monday -> following Sunday
2. Read CHANGELOG.md
3. Collect all `## [X.Y.Z] - YYYY-MM-DD` entries where date falls in range
4. Aggregate all entries across versions

## Entry Structure

Each top-level bullet under `### Added/Changed/Fixed` is one **entry**. Parse:

| Field | Source | Example |
|-------|--------|---------|
| `title` | Bold text after `- **` | `Visual Reference` |
| `description` | Text after `:` or `--` on same line | `4 new high-value ASCII diagrams (16 -> 20 total)` |
| `sub_items` | Indented bullets below | List of detail lines |
| `section` | Parent `###` header | `Added`, `Changed`, `Fixed` |
| `files` | Filenames/paths in description | `guide/ultimate-guide.md`, `machine-readable/reference.yaml` |
| `source` | URLs or named references | `Pat Cullen's Final Review Gist` |
| `metrics` | Numbers in description | `227 -> 257`, `+522 lines`, `4 new` |
| `score` | Evaluation score if present | `Score: 4/5` |

## Category Classification

Each entry gets exactly one category with a weight:

| Category | Weight | Pattern |
|----------|--------|---------|
| `NEW_CONTENT` | 3 | New guide sections, new files, new diagrams, new quiz questions |
| `GROWTH_METRIC` | 2 | Line count increases, template counts, quiz count changes |
| `RESEARCH` | 1 | Resource evaluations, external source integrations |
| `FIX` | 1 | Bug fixes, corrections, accuracy improvements |
| `MAINTENANCE` | 0 | README updates, badge updates, count syncs, landing syncs |

### Classification Rules

1. If entry creates a new `.md` file or new section -> `NEW_CONTENT`
2. If entry contains `-> ` with numbers (growth) -> `GROWTH_METRIC`
3. If entry references external source with evaluation score -> `RESEARCH`
4. If entry is under `### Fixed` -> `FIX`
5. If entry only updates counts, badges, or sync -> `MAINTENANCE`
6. If entry has sub-items with substantial content -> upgrade one level
7. When ambiguous, prefer higher-weight category

### Examples

```
"4 new ASCII diagrams (16 -> 20)"           -> NEW_CONTENT (new diagrams)
"30 New Quiz Questions (227 -> 257)"        -> NEW_CONTENT (new questions)
"Quiz badge updated (227 -> 257)"           -> MAINTENANCE (badge sync)
"Guide line count: 15,771 -> 16,293"        -> GROWTH_METRIC (growth)
"Score: 4/5 - Docker Sandboxes"             -> RESEARCH (evaluation)
"Fixed 14 -> 15 categories in landing"      -> FIX (correction)
"README.md: Added Visual Reference to table" -> MAINTENANCE (nav update)
```

## Scoring Algorithm

For each entry, compute:

```
score = (category_weight * 3)
      + (has_number * 2)
      + (named_source * 1)
      + (new_file * 1)
      + (min(impact_files, 3))
      + (breaking * 2)
```

| Factor | Value | Detection |
|--------|-------|-----------|
| `category_weight` | 0-3 | From category table above |
| `has_number` | 0 or 1 | Entry contains numeric change (`N -> M`, `+N lines`, `N new`) |
| `named_source` | 0 or 1 | Entry credits a person or external source |
| `new_file` | 0 or 1 | Entry mentions creating a new file (`NEW`, new `.md`) |
| `impact_files` | 0-3 | Count of distinct files mentioned (capped at 3) |
| `breaking` | 0 or 1 | Entry is under `### Breaking` or mentions breaking change |

### Score Interpretation

| Score | Action |
|-------|--------|
| 10+ | Lead highlight (hook line) |
| 6-9 | Secondary highlight (bullet point) |
| 3-5 | Include if space allows |
| 0-2 | Skip (maintenance noise) |

Select top 3-4 entries by score. If all scores < 3, flag as "no social content recommended."

## Week Aggregation Rules

When generating for a week with multiple versions:

1. Score all entries across all versions in the date range
2. De-duplicate: if same topic appears in multiple versions, keep highest-scored one
3. Prefix week output with version count: `X releases this week`
4. Use date range in header, not individual version numbers
