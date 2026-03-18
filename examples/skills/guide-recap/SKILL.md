---
name: guide-recap
description: Transform CHANGELOG entries into social content (LinkedIn, Twitter/X, Newsletter, Slack) in FR + EN. Use after releases or weekly to generate ready-to-post content from guide updates.
argument-hint: "<latest|vX.Y.Z|week [YYYY-MM-DD]> [--interactive] [--format=linkedin|twitter|newsletter|slack] [--lang=fr|en] [--save]"
tags: [changelog, social-media, content, linkedin, twitter]
---

# Guide Recap

Generate social media content from CHANGELOG.md entries. Produces 8 outputs by default (4 formats x 2 languages).

## When to Use

- After running `/release` to create social announcements
- Weekly to summarize multiple releases
- Before posting on LinkedIn, Twitter/X, newsletter, or Slack

## Usage

```
/guide-recap latest              # Latest released version
/guide-recap v3.20.5             # Specific version
/guide-recap week                # Current week (Monday to today)
/guide-recap week 2026-01-27     # Specific week (Monday to Sunday)
```

### Flags

| Flag | Effect | Default |
|------|--------|---------|
| `--interactive` | Guide mode: choose angle, audience, highlight | Off (auto-draft) |
| `--format=X` | Single format: `linkedin`, `twitter`, `newsletter`, `slack` | All 4 formats |
| `--lang=X` | Single language: `fr`, `en` | Both FR + EN |
| `--save` | Save output to `[project-docs]/social-posts/` | Display only |
| `--force` | Generate even if only maintenance entries | Skip low-score |

## Workflow (7 Steps)

### Step 1: Parse Input

Parse `$ARGUMENTS` to determine mode:

| Input | Mode | Target |
|-------|------|--------|
| `latest` | Single version | First `## [X.Y.Z]` after `[Unreleased]` |
| `vX.Y.Z` or `X.Y.Z` | Single version | Exact version match |
| `week` | Week range | Monday of current week -> today |
| `week YYYY-MM-DD` | Week range | That Monday -> following Sunday |

If no argument or invalid argument, display usage and exit.

### Step 2: Extract CHANGELOG Entries

Read `CHANGELOG.md` from the project root.

**Single version:**
1. Find line matching `## [{version}]`
2. Extract all content until next `## [` line
3. Parse `### Added`, `### Changed`, `### Fixed` sections

**Week range:**
1. Collect all `## [X.Y.Z] - YYYY-MM-DD` entries where date falls in range
2. Parse all sections from all matching versions

**Error: version not found** -> List last 5 versions, suggest `latest`.
**Error: week has no entries** -> Show date of last release, suggest that version.

### Step 3: Categorize Entries

For each top-level entry (first-level bullet under `###`), assign a category:

| Category | Weight | Detection |
|----------|--------|-----------|
| `NEW_CONTENT` | 3 | New files, new sections, new diagrams, new quiz questions |
| `GROWTH_METRIC` | 2 | Line count growth, item count changes |
| `RESEARCH` | 1 | Resource evaluations, external source integrations |
| `FIX` | 1 | Under `### Fixed`, corrections |
| `MAINTENANCE` | 0 | README updates, badge syncs, landing syncs, count updates |

See `references/changelog-parsing-rules.md` for detailed classification rules.

### Step 4: Transform to User Value

Apply mappings from `references/content-transformation.md`:

- Technical language -> user benefit
- Extract concrete numbers
- Credit named sources
- Cluster related entries

Validate against `references/tone-guidelines.md` DO/DON'T checklist.

### Step 4b: Interactive Mode (--interactive only)

If `--interactive` flag is set, insert between steps 4 and 5:

1. Display candidate highlights with scores:
   ```
   Highlights (by score):
   [14] 4 new ASCII diagrams (16 -> 20)     [NEW_CONTENT]
   [ 9] 30 new quiz questions (227 -> 257)   [NEW_CONTENT]
   [ 6] Docker sandbox isolation guide        [NEW_CONTENT]
   [ 1] README updated                        [MAINTENANCE]
   ```

2. Ask angle:
   - Auto (highest scored = hook)
   - User picks specific entry as hook
   - Custom angle (user provides theme)

3. Ask target audience:
   - `devs` (technical depth)
   - `tech-leads` (impact focus)
   - `general` (accessible language)
   - `all` (default, balanced)

4. Ask primary highlight:
   - Auto (top score)
   - User selects from list

5. Confirm selection and proceed to step 5.

### Step 5: Score and Select

Compute score for each entry:

```
score = (category_weight * 3)
      + (has_number * 2)
      + (named_source * 1)
      + (new_file * 1)
      + (min(impact_files, 3))
      + (breaking * 2)
```

Select top 3-4 entries by score. Highest score = hook line.

**If all scores < 3**: Output "No social content recommended for this version. Use `--force` to generate anyway." and exit (unless `--force`).

### Step 6: Generate Content

For each requested format (default: all 4) and language (default: both):

1. Read the corresponding template from `assets/`
2. Fill template fields using scored and transformed entries
3. Apply tone-guidelines.md quality checklist

**Links:**

| Format | Link Target |
|--------|-------------|
| LinkedIn | Landing site URL |
| Twitter | GitHub repo URL |
| Newsletter | Both (landing + GitHub) |
| Slack | GitHub repo URL |

**URLs:**
- Landing: `https://{DOMAIN}/`
- GitHub: `https://github.com/{OWNER}/{REPO}`

### Step 7: Output

Display each generated post in a fenced code block, labeled by format and language:

```
## LinkedIn (FR)

```text
[content]
`` `

## LinkedIn (EN)

```text
[content]
`` `

## Twitter/X (FR)

```text
[content]
`` `

...
```

If `--save` flag: write all outputs to `[project-docs]/social-posts/YYYY-MM-DD-vX.Y.Z.md` (for version) or `[project-docs]/social-posts/YYYY-MM-DD-week.md` (for week). Create `[project-docs]/social-posts/` directory if it doesn't exist.

## Error Handling

| Error | Response |
|-------|----------|
| No argument | Display usage block |
| Invalid argument | Display usage block with examples |
| Version not found | List 5 most recent versions, suggest `latest` |
| Week has no entries | Show date of last release, suggest version |
| All entries MAINTENANCE (score 0) | "No social content recommended. Use `--force` to override." |
| CHANGELOG.md not found | "CHANGELOG.md not found in project root." |

## Reference Files

- `references/tone-guidelines.md` - DO/DON'T rules, emoji budget, language register
- `references/changelog-parsing-rules.md` - CHANGELOG format, extraction, scoring algorithm
- `references/content-transformation.md` - Technical -> user value mappings (30+)
- `assets/linkedin-template.md` - ~1300 chars, hook + bullets + CTA + hashtags
- `assets/twitter-template.md` - 280 chars single or 2-3 tweet thread
- `assets/newsletter-template.md` - ~500 words, structured sections
- `assets/slack-template.md` - Compact, emoji-rich, Slack formatting
- `examples/version-output.md` - Full example output for v3.20.5
- `examples/week-output.md` - Full example output for week 2026-01-27

## Tips

- Run `/guide-recap latest` right after `/release` to prepare social posts
- Use `--interactive` the first few times to understand the scoring
- Use `--format=linkedin --lang=fr` when you only need one specific output
- `--save` outputs are gitignored via `[project-docs]/` convention
- Review and personalize before posting (these are drafts, not final copy)
