---
name: "source-command-audit-whitepapers"
description: "Audit version freshness, FR/EN parity, and metadata quality of all whitepapers and recap cards"
---

# source-command-audit-whitepapers

Use this skill when the user asks to run the migrated source command `audit-whitepapers`.

## Command Template

# Audit Whitepapers & Recap Cards

Comprehensive freshness and quality audit for all whitepapers (FR + EN) and recap cards (FR + EN). Scores each document against the current guide version, checks FR/EN parity, and validates metadata consistency.

## Arguments

- `--fix` - Generate update suggestions and frontmatter patches (does not modify files)
- `--verbose` - Show all criteria including passing ones, not just failures
- `--cards-only` - Audit only recap cards (skip main whitepapers)
- `--wp-only` - Audit only main whitepapers (skip recap cards)

## Usage

```bash
/audit-whitepapers                  # Full audit, failures only
/audit-whitepapers --fix            # Audit + prioritized update suggestions
/audit-whitepapers --verbose        # Full details for all criteria
/audit-whitepapers --cards-only     # Recap cards only
/audit-whitepapers --wp-only        # Whitepapers only
```

---

## Phase 1: Discovery

**Objective**: Locate and inventory all auditable documents.

### Steps

1. **Read current guide version**: Read the `VERSION` file at the project root. This is the target version all documents should be synced against.

2. **Scan directories** for `.qmd` files:
   ```
   whitepapers/fr/         (main whitepapers FR)
   whitepapers/en/         (main whitepapers EN)
   whitepapers/recap-cards/fr/    (recap cards FR)
   whitepapers/recap-cards/en/    (recap cards EN)
   ```

3. **Classify each file**:
   - **Main whitepaper**: files matching `[0-9][0-9]-*.qmd` in `whitepapers/fr/` or `whitepapers/en/`
   - **Cheatsheet**: files matching `*cheatsheet*.qmd` (tracked separately, not scored)
   - **Custom whitepaper**: files matching `*-whitepaper.qmd` or `*-cheatsheet.qmd` from external partners (strangebee, purchasely, devwithai) -- excluded from scoring, listed separately
   - **Recap card**: all `.qmd` files in `recap-cards/fr/` or `recap-cards/en/`
   - **Bundle/include**: `fiches-recap-serie.qmd`, files in `fiches/` subdirectory -- excluded (they are composed documents)

4. **Parse YAML frontmatter** for each included file (read between first `---` and second `---`). Extract:
   - `title`, `subtitle`, `author`, `date`
   - `version` (guide version tracked in main WPs and recap cards)
   - `wp-version` (whitepaper own semver, main WPs only)
   - `guide-version` (explicit guide version field used in recap cards)
   - `card-number`, `category`, `difficulty` (recap cards only)
   - `series` (main WPs only)

5. **Display discovery summary**:
   ```
   Guide version: {VERSION}
   Found: {N} main whitepapers ({FR}/{EN} FR/EN), {N} recap cards ({FR}/{EN} FR/EN)
   Excluded: {N} custom files (strangebee, purchasely, devwithai), {N} bundle files
   ```

---

## Phase 2: Version Gap Analysis (40 points per file)

**Objective**: Score how current each document is relative to the guide.

### Semver comparison logic

Parse version strings as `MAJOR.MINOR.PATCH`. The staleness metric is `minor_gap = current_minor - file_minor` (using the same MAJOR). If MAJOR differs, treat as critical.

For **main whitepapers**, the guide version field is `version`.
For **recap cards**, the guide version field is `guide-version` (fall back to `version` if absent).

### Scoring table

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Guide version current (0-1 minor behind) | 15 | `minor_gap` <= 1 |
| Guide version recent (2-3 minor behind) | 10 | `minor_gap` 2-3 (partial credit, replaces the 15) |
| Guide version old (4-10 minor behind) | 5 | `minor_gap` 4-10 (partial credit) |
| wp-version field present and valid semver | 5 | Field exists AND matches `\d+\.\d+\.\d+` (WP only) |
| wp-version consistent with FR/EN pair | 10 | Same `wp-version` value in the counterpart file (WP only) |
| guide-version consistent with FR/EN pair | 10 | Same `guide-version` (or `version`) in the counterpart (cards) |

**Freshness labels**:
- 0-1 minor behind: Fresh
- 2-3 minor behind: Stale
- 4-10 minor behind: Very Stale
- 11+ minor behind: Critical

Note: The 15, 10, 5 pts for guide version are mutually exclusive (award only the highest applicable tier).

---

## Phase 3: Content Staleness Check (20 points per file)

**Objective**: Detect whether the guide sections a whitepaper covers have changed since it was last updated.

### Whitepaper-to-guide mapping (embedded)

| WP# | FR filename prefix | EN filename prefix | Guide sections |
|-----|--------------------|--------------------|----------------|
| 00 | `00-introduction` | `00-series-introduction` | `guide/ultimate-guide.md` Ch.1-2 |
| 01 | `01-prompts` | `01-effective-prompts` | Ch.2 prompting sections |
| 02 | `02-personnalisation` | `02-customization` | Ch.3 Memory, Ch.4 Agents, Ch.5 Skills |
| 03 | `03-securite` | `03-security` | Ch.7 Hooks, security sections |
| 04 | `04-architecture` | `04-architecture` | Ch.2 internals, architecture sections |
| 05 | `05-equipe` | `05-team` | Ch.3 team config, Ch.9 CI/CD |
| 06 | `06-privacy` | `06-privacy` | Ch.2 data/privacy sections |
| 07 | `07-guide-reference` | `07-reference-guide` | Ch.10 Reference |
| 08 | `08-agent-teams` | `08-agent-teams` | Ch.9 agent teams |
| 09 | `09-apprendre` | `09-learning` | `guide/roles/learning-with-ai.md` |
| 10 | `10-budget` | `10-ai-budget` | Business/ROI content |

### Steps

1. For each main whitepaper, extract the `date` field. If the date is not in `YYYY-MM-DD` format, parse it (e.g., "2026-02-12" or "March 2026").
2. Run `git log --since="{date}" --oneline -- guide/ultimate-guide.md guide/roles/ guide/core/` to count commits that touched guide content since the whitepaper's date.
3. Score:

| Criterion | Points | Detection |
|-----------|--------|-----------|
| No guide commits since wp date | 10 | `git log` returns 0 commits |
| Few commits since wp date (1-5) | 7 | 1-5 commits (partial) |
| Moderate commits (6-15) | 4 | 6-15 commits (partial) |
| Many commits (>15) | 0 | More than 15 commits |
| Mapping defined for this WP | 5 | WP number is in the mapping table above |
| Git history accessible | 5 | `git log` command executes without error |

**Recap cards**: Skip detailed git analysis. Award a flat staleness score based on `minor_gap`:
- 0-1 behind: 20 pts
- 2-3 behind: 15 pts
- 4-10 behind: 8 pts
- 11+ behind: 0 pts

---

## Phase 4: FR/EN Parity Check (20 points per file)

**Objective**: Every document should have a complete, version-consistent counterpart in the other language.

### Pairing strategy

**Main whitepapers**: Match on the two-digit numeric prefix (e.g., `00`, `03`, `10`). FR and EN filenames differ but the prefix is consistent.

**Recap cards**: Match on identical filename (both language directories use the same filenames).

### Scoring table

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Counterpart file exists in other language | 10 | File with matching prefix (WP) or identical name (cards) found |
| wp-version matches between pairs | 5 | Same `wp-version` value (WP only) |
| guide version matches between pairs | 5 | Same `version`/`guide-version` value |

Score both the FR and EN files of a pair identically on parity (if the pair is complete, both get 20; if one is missing, the existing file scores 0 on parity).

---

## Phase 5: Metadata Quality (20 points per file)

**Objective**: Validate frontmatter completeness, field formats, and consistency across files of the same type.

### Main whitepapers (20 points max)

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Required fields present | 6 | Has all of: `title`, `subtitle`, `author`, `date`, `version`, `wp-version`, `series` |
| `version` follows semver pattern | 3 | Matches `\d+\.\d+\.\d+` |
| `wp-version` follows semver pattern | 3 | Matches `\d+\.\d+\.\d+` |
| `date` is parseable and not in the future | 3 | Valid date, not after today |
| `series` value is consistent | 2 | Equals "Claude Code Ultimate Guide" |
| No missing `wp-version` (not left empty or absent) | 3 | Field has a non-empty value |

### Recap cards (20 points max)

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Required fields present | 5 | Has all of: `title`, `subtitle`, `card-number`, `category`, `difficulty`, `guide-version`, `author`, `version`, `date` |
| `card-number` matches filename prefix | 4 | e.g., `C01` in `card-number` matches `c01-` in filename |
| `category` valid for language | 4 | FR: one of "Technique", "Methodologie", "Conception"; EN: one of "Technical", "Methodology", "Design" (flag "Conceptual" as inconsistent in EN) |
| `difficulty` is valid value | 3 | One of: "beginner", "intermediate", "advanced" |
| `guide-version` and `version` fields match each other | 4 | Both fields exist and have the same value within the same file |

**Known issue to detect automatically**: EN C-series cards use two different category values ("Conceptual" on c01-c05, "Design" on c06+). Flag this inconsistency explicitly in the Metadata Issues section of the report.

---

## Phase 6: Scoring and Grading

### Score formula (per file)

```
Total = Version Gap (40) + Content Staleness (20) + FR/EN Parity (20) + Metadata Quality (20)
Score = (Total / 100) * 100  [as a percentage]
```

### Grade scale

| Grade | Score | Status |
|-------|-------|--------|
| A | 90-100 | Fresh, fully synced |
| B | 80-89 | Good (production threshold) |
| C | 70-79 | Needs update soon |
| D | 60-69 | Stale, should prioritize |
| F | <60 | Critical: likely outdated content |

### Overall health score

```
Weighted Health = (Sum of WP scores * 2 + Sum of card scores * 1) / (WP count * 2 + card count * 1)
```

Whitepapers are weighted 2x because they are 20-80 pages each vs. 2-page recap cards. A stale whitepaper carries more risk.

---

## Phase 7: Report

Output the following Markdown report. Use `<details>` blocks for individual file breakdowns to keep the top level scannable.

```markdown
# Whitepaper & Recap Card Audit

**Date**: {today}
**Guide Version**: {VERSION}
**Overall Health**: {score}% ({grade})
**Files Audited**: {total} ({wp_count} whitepapers, {card_count} recap cards)

---

## Version Status Dashboard

| Status | Whitepapers | Recap Cards | Total |
|--------|-------------|-------------|-------|
| Fresh (0-1 minor behind)   | N | N | N |
| Stale (2-3 minor behind)   | N | N | N |
| Very Stale (4-10 behind)   | N | N | N |
| Critical (11+ behind)      | N | N | N |

**Versions currently in use**:
- Main WP 00-09: {version} ({gap} minor versions behind)
- Main WP 10: {version} ({gap} minor versions behind)
- Recap cards: {guide-version} ({gap} minor versions behind)

---

## Whitepaper Scores

| WP# | Title | version | Gap | wp-version | Parity | Score | Grade |
|-----|-------|---------|-----|------------|--------|-------|-------|
| 00  | ...   | ...     | -N  | ...        | OK/gap | N%    | X     |
...

<details>
<summary>Individual criteria breakdown (WP 00)</summary>

| Phase | Criterion | Result | Points |
|-------|-----------|--------|--------|
| Version Gap | Guide version current | Critical (-11) | 0/15 |
| Version Gap | wp-version valid semver | OK | 5/5 |
| ... | ... | ... | ... |
| **Total** | | | **N/100** |
</details>

---

## Recap Card Scores

| Series | Cards | Avg guide-version | Avg Gap | Avg Score | Grade |
|--------|-------|-------------------|---------|-----------|-------|
| T (Technical)    | 22 | ... | -N | N% | X |
| M (Methodology)  | 22 | ... | -N | N% | X |
| C (Conceptual)   | 13 | ... | -N | N% | X |

<details>
<summary>Individual card scores</summary>

| Card | Category | guide-version | Gap | Parity | Metadata | Score | Grade |
|------|----------|---------------|-----|--------|----------|-------|-------|
...
</details>

---

## FR/EN Parity Report

### Whitepapers
| WP# | FR | EN | wp-version Match | version Match |
|-----|----|----|------------------|---------------|
...

### Recap Cards
- **FR count**: {N} | **EN count**: {N}
- **Missing FR**: [list or "None"]
- **Missing EN**: [list or "None"]
- **Version mismatches**: [list or "None"]

---

## Metadata Issues

### Known: EN Recap Card Category Inconsistency
EN C-series cards use two different values for the "Conceptual/Design" category:
- "Conceptual": c01, c02, c03, c04, c05
- "Design": c06, c07, c08, ...
Recommendation: standardize to "Design" to match guide terminology.
Affected files: whitepapers/recap-cards/en/c01-*.qmd through c05-*.qmd (change "Conceptual" to "Design")

### Other issues
[List any missing fields, bad formats, date issues...]

---

## Prioritized Action Items

### Critical (Grade F, 11+ versions behind)
[List specific whitepapers with filename paths]

### High (Grade D-F, 2+ versions behind)
[List specific files]

### Medium (Metadata quality, category fixes)
[List specific issues]

### Low (Polish, date alignment)
[List specific issues]

---

## Next Steps

1. Run `/update-whitepapers --since {oldest_version}` to update all stale WPs
2. Fix EN category inconsistency (5 files: c01 through c05, change "Conceptual" to "Design")
3. Re-run `/audit-whitepapers` after updates to track progress
4. Target: 80%+ health (Grade B) across all files
```

---

## Fix Mode (`--fix`)

When `--fix` is passed, append a **Fix Suggestions** section after the report. This section provides concrete patches but does NOT modify any files.

### Frontmatter version patches

For each file with a stale guide version, output:
```yaml
# File: whitepapers/fr/00-introduction-serie.qmd
# Change:
version: "3.27.6"  ->  version: "{current_VERSION}"
date: 2026-02-12   ->  date: {today}
```

### Category fix patches (EN recap cards)

```
Files to update (category: "Conceptual" -> "Design"):
- whitepapers/recap-cards/en/c01-trust-calibration.qmd
- whitepapers/recap-cards/en/c02-*.qmd
- whitepapers/recap-cards/en/c03-*.qmd
- whitepapers/recap-cards/en/c04-*.qmd
- whitepapers/recap-cards/en/c05-*.qmd
```

### Update command checklist

Based on the stale WPs detected, output the `/update-whitepapers` commands to run in order:
```
Suggested update sequence:
1. /update-whitepapers --since {oldest_stale_version} --wp 00,01,02,03,04,05,06,07,08,09
2. /update-whitepapers --since {oldest_stale_version} --wp 10
3. Review and bump wp-version for each updated WP (patch = content corrections, minor = new sections)
4. Bump guide-version in all recap cards to {current_VERSION}
5. Re-run /audit-whitepapers to verify
```

---

## Verbose Mode (`--verbose`)

When `--verbose` is passed, expand all `<details>` blocks by default and show the complete per-file criteria table (all criteria, not just failures) for every audited file.

---

## Exclusions Reference

The following files are excluded from scoring (listed in discovery summary only):

| Pattern | Reason |
|---------|--------|
| `strangebee-*.qmd`, `purchasely-*.qmd`, `devwithai-*.qmd` | Client/partner custom files, separate lifecycle |
| `fiches-recap-serie.qmd`, `fiches/*.qmd` | Bundle/include files, no independent versioning |
| `*_quarto.yml`, `references.bib` | Build config, not content |
| `cheatsheet.qmd` | Listed separately in discovery, not scored in main audit |
