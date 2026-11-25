---
name: update-whitepapers
description: Update whitepapers (FR + EN) based on recent CHANGELOG entries using a parallel agent team
argument-hint: "[--since <version>] [--wp <00-08|cheatsheet>]"
---

# Whitepaper Update Workflow

Analyze recent CHANGELOG entries and update affected whitepapers (FR + EN) using a parallel agent team.

## Usage

```
/update-whitepapers                        # Update WPs based on latest CHANGELOG entry
/update-whitepapers --since 3.27.0         # Update WPs for all changes since v3.27.0
/update-whitepapers --wp 03                # Force update WP03 only (FR + EN)
/update-whitepapers --wp 07,08             # Force update WP07 + WP08
```

## Step 1: Parse Arguments

Parse `$ARGUMENTS`:
- `--since <version>` → analyze all CHANGELOG entries from that version to latest
- `--wp <list>` → skip analysis, force-update specified WPs (comma-separated: `03`, `07,08`, `cheatsheet`)
- No args → use only the most recent CHANGELOG entry (latest `## [X.Y.Z]` block)

## Step 2: Read CHANGELOG

Read `CHANGELOG.md`. Extract the relevant entries:
- If `--since <version>`: extract all `## [X.Y.Z]` blocks with version > specified version
- If no `--since`: extract only the first (most recent) `## [X.Y.Z]` block

Display the extracted entries to the user for confirmation.

## Step 3: Map Changes to Whitepapers

Unless `--wp` was specified, analyze the changelog text and map changes to affected whitepapers using this matrix:

| Keywords / Topics | Affected WPs |
|-------------------|-------------|
| hooks, security, permissions, threat, injection, scanner, allowlist, blocklist | WP03, WP07 |
| context, thinking, architecture, pricing, tokens, model, API, memory | WP04, WP07 |
| CLAUDE.md, settings.json, customization, project, persona, agent-type, MCP | WP02, WP07 |
| prompts, slash commands, commands, output format, `#`, `!` | WP01, WP07 |
| team, multi-agent, orchestration, subagent, background, worktree | WP05, WP08 |
| privacy, ZDR, retention, data, enterprise, telemetry | WP06, WP07 |
| release, version, new feature, introduction | WP00, WP07 |
| cheatsheet | cheatsheet |
| agent teams, Agent Teams | WP08, WP05 |

Always include WP07 (reference guide) if any significant feature change is detected — it's the catch-all reference.

Build the list of affected WPs. Remove duplicates. Display the list:
```
Affected whitepapers: WP00, WP03, WP07, WP08
Changes to integrate: [summary of relevant changes]
```

Ask: "Launch team to update these WPs? (y/n)"

If user confirms, proceed. If `--wp` was specified, skip confirmation.

## Step 4: Launch Agent Team

### Setup

Teammates join the session's implicit team: spawn each one with the Agent tool and a `name` (TeamCreate was removed in Claude Code v2.1.178).

Create one task per affected WP.

### Launch Agents in Parallel

For each affected WP, launch one agent (`run_in_background: true`) with this prompt template:

---
**Agent prompt template:**

```
You are wp-updater for [WP_ID].

You have changelog changes to integrate into two files:
- FR: whitepapers/fr/[FR_FILENAME]
- EN: whitepapers/en/[EN_FILENAME]

## Changes to integrate

[CHANGELOG_EXCERPT]

## Instructions

1. Read the FR file completely
2. Identify sections that need updating based on the changelog
3. Apply targeted edits using the Edit tool (do NOT rewrite entire sections unless necessary)
4. Read the EN file completely
5. Apply the same changes in English
6. Be surgical: only change what's factually outdated or newly relevant
7. Do not change the structure, tone, or style
8. Keep version numbers in frontmatter at [CURRENT_VERSION]

When done, send message to team-lead: "wp-updater [WP_ID] done: [list of sections updated]"
```
---

### WP → File mapping

| WP ID | FR filename | EN filename |
|-------|-------------|-------------|
| WP00 | fr/00-introduction-serie.qmd | en/00-series-introduction.qmd |
| WP01 | fr/01-prompts-efficaces.qmd | en/01-effective-prompts.qmd |
| WP02 | fr/02-personnalisation.qmd | en/02-customization.qmd |
| WP03 | fr/03-securite.qmd | en/03-security.qmd |
| WP04 | fr/04-architecture.qmd | en/04-architecture.qmd |
| WP05 | fr/05-equipe.qmd | en/05-team.qmd |
| WP06 | fr/06-privacy.qmd | en/06-privacy.qmd |
| WP07 | fr/07-guide-reference.qmd | en/07-reference-guide.qmd |
| WP08 | fr/08-agent-teams.qmd | en/08-agent-teams.qmd |
| cheatsheet | fr/cheatsheet.qmd | en/cheatsheet.qmd |

All paths are relative to the `whitepapers/` directory inside the current working directory.
The agent must resolve absolute paths at runtime using the project root (current working directory).

## Step 5: Wait and Collect Results

Wait for all agents to report completion. Track:
- ✅ Completed agents
- ❌ Failed agents (if any)

When all agents are done, display summary table:

```
WP00 ✅ — Updated: intro section (9 WPs → 10 WPs)
WP03 ✅ — Updated: hooks count (14 → 17), new scanner hook added
WP07 ✅ — Updated: flags table, reference section
WP08 ✅ — No changes needed
```

## Step 6: Update Frontmatter Version

If changelog contains a version bump:
- Read `VERSION` file → get current version
- Update `version:` field in frontmatter of ALL updated files (FR + EN)

## Step 7: Cleanup

Shutdown all agents via `SendMessage(type: shutdown_request)`.
No team to delete: the implicit team ends with the session (TeamDelete was removed in Claude Code v2.1.178).

## Step 8: Post-update verification

Run quick sanity checks:
```bash
# No leftover stale versions
grep -r "3\.26\." whitepapers/fr/*.qmd whitepapers/en/*.qmd

# Frontmatter versions consistent
grep "^version:" whitepapers/fr/*.qmd whitepapers/en/*.qmd | sort -u
```

Display results. Flag any inconsistencies.

## Important Notes

- **Surgical edits only** — agents use Edit tool, not full rewrites
- **Both FR and EN always updated together** — never one without the other
- **WP07 is the reference hub** — almost always included
- **Source of truth**: CHANGELOG.md + `guide/ultimate-guide.md` (if deeper context needed)
- **No hallucination**: agents must cite specific changelog lines they're acting on
