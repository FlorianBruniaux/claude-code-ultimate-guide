---
name: "source-command-track-mentions"
description: "Search for new online mentions of the Claude Code Ultimate Guide or Florian Bruniaux's public project portfolio and update the relevant tracker"
---

# source-command-track-mentions

Use this skill when the user asks to run the migrated source command `track-mentions`.

## Command Template

# Track Mentions Workflow

Find new online mentions of either the Claude Code Ultimate Guide or the wider public project portfolio.
The guide catalog lives in `docs/media-mentions/mentions.yaml`. The cross-project catalog lives in
`~/Sites/perso/florian-portfolio/src/data/mentions.json`.

## Usage

```
/track-mentions            # Search + report new mentions, confirm before adding
/track-mentions --dry-run  # Search + report only, no YAML changes
/track-mentions --scheduled # Unattended report-only run, equivalent to --dry-run
/track-mentions --add-all  # Add all confirmed results after explicit approval in this session
/track-mentions --all-projects # Search the active GitHub portfolio and update the portfolio catalog
/track-mentions --commit   # Commit only the validated tracker files after an approved update
```

`--scheduled` always wins over write flags. A scheduled run must not edit files, create a commit,
push, open a pull request, or publish a tracker update.

## Step 1: Load existing tracker

For the default guide mode, read `docs/media-mentions/mentions.yaml` to get:
- Current `meta.total_mentions` count
- All existing `url` fields → build a deduplication set
- `docs/media-mentions/review-queue.yaml` → keep inaccessible candidates pending and rejected URLs excluded

For `--all-projects`:

1. Read the public `FlorianBruniaux` GitHub profile and list active repositories owned by that account.
2. Exclude forks, landing-only repositories, support repositories such as `homebrew-tap`, and RTK.
3. Read `~/Sites/perso/florian-portfolio/src/data/mentions.json` to get tracked projects, source URLs,
   and existing multi-project assignments.
4. Treat one canonical URL as one source even when it names several projects.

## Step 2: Run Perplexity deep research

Use `mcp__perplexity__perplexity_research` with `reasoning_effort: "high"`. Append the normalized URLs
from the confirmed catalog and review queue as `<KNOWN_URLS>`. Search broadly on every run instead of
assuming that a weekly time window captures pages indexed late.

```
Find all articles, blog posts, newsletters, Reddit threads, Twitter/X posts, LinkedIn posts,
YouTube videos, podcasts, GitHub issues/repos, and directories that mention "Claude Code
Ultimate Guide" by Florian Bruniaux (GitHub: FlorianBruniaux/claude-code-ultimate-guide,
website: cc.bruniaux.com). Search broadly for third-party content only - exclude the GitHub
repo itself and cc.bruniaux.com own pages.

Return exactly three groups:
- `new_confirmed`: evidence is accessible and contains an explicit project identifier
- `already_tracked`: canonical URL matches `<KNOWN_URLS>`
- `rejected_or_unverified`: title collision, inaccessible evidence, owned property, or uncertain attribution

For each result provide: canonical URL, publication date if available, author/platform name, language,
project identifier found, evidence location, one sentence on how the source references the guide,
classification, confidence, and metadata problems.

Also search explicitly for:
- "cc.bruniaux.com" cited as a resource on third-party sites
- "claude-code-ultimate-guide florian bruniaux" in blog posts and tutorials
- "FlorianBruniaux" in dev tutorials referencing the guide
- The guide mentioned in non-English content (French, Spanish, German, Korean, Portuguese, etc.)

Known canonical URLs for deduplication:
<KNOWN_URLS>
```

**If Perplexity returns no results** (model refuses citing knowledge cutoff), fall back to
WebSearch with these parallel queries:
```
"Claude Code Ultimate Guide" -site:github.com -site:cc.bruniaux.com
site:reddit.com "cc.bruniaux.com" OR "Claude Code Ultimate Guide"
site:dev.to OR site:hashnode.com OR site:medium.com "Claude Code Ultimate Guide" "florian" OR "bruniaux"
"Claude Code Ultimate Guide" twitter OR x.com
```
Then use `WebFetch` on each candidate URL to verify the guide is explicitly mentioned by name or URL.

Treat a result as confirmed only when the page itself, its public metadata, or an indexed snippet
contains at least one project identifier: the guide name, the canonical repository slug, or
`cc.bruniaux.com`. A matching generic title such as "ultimate Claude Code guide" is not enough.

Classify every confirmed result before reporting it:
- `editorial`: article, newsletter, podcast, or video with independent commentary
- `social`: third-party LinkedIn, X, Instagram, or Facebook post
- `forum`: Reddit, Hacker News, forum, or community discussion
- `translation`: translated or adapted repository that credits the original
- `mirror`: copied or republished guide content
- `adoption`: a third-party repository visibly embeds, configures, or uses the project
- `registry`: a package or protocol registry entry proving distribution coverage
- `automated_directory`: generated index, catalog, MCP directory, or repository documentation service

Do not count the project's own pages, the author's own social posts, GitHub topic pages generated
from the repository's own metadata, or referral query parameters as earned third-party mentions.
Keep automated directories separate from organic mentions. Flag incorrect install commands, package
names, star counts, line counts, authorship, or capabilities instead of silently copying them.

## Step 3: Deduplicate

For each result from Perplexity:
1. Normalize the URL (strip trailing slash, lowercase domain)
2. Check against existing URLs in the YAML
3. Check against pending and rejected URLs in `review-queue.yaml`
4. Resolve obvious redirects and compare the canonical destination
5. Skip if already tracked
6. Keep inaccessible candidates pending; never promote them from a repeated snippet alone

## Step 4: Report new mentions

Display a table for review:

```
New mentions found: N

| # | Kind | Platform | Author | Title | Evidence | Metadata issues | URL | Date |
|---|------|----------|--------|-------|----------|-----------------|-----|------|
| 1 | ...  | ...      | ...    | ...   | Confirmed | None          | ... | ...  |
```

After the table, report separate counts:
- organic mentions: `editorial`, `social`, and `forum`
- adaptations: `translation` and `mirror`
- visible adoption: `adoption`
- distribution coverage: `registry`
- automated indexes: `automated_directory`

List probable or inaccessible candidates separately. Never add them as confirmed entries without
user approval and an explicit uncertainty note.

If `--dry-run` or `--scheduled`: stop here, no changes.

## Step 5: Add to the relevant catalog (unless --dry-run)

In default mode, add entries to `docs/media-mentions/mentions.yaml` using the rules below.

In `--all-projects` mode, add one entry to the portfolio JSON with a `projects` array containing every
explicitly cited project id and an explicit `group`. Never duplicate a source to make per-project totals
larger. Add a newly discovered active project to the top-level `projects` array even when its verified
mention count is zero.

Writing requires explicit user approval in the current interactive session. `--add-all` does not count
as approval when replayed by an automation. For each approved new mention:

1. Assign next sequential id (zero-padded to 3 digits)
2. Infer `platform` from the source type:
   - Blog/newsletter → `article`
   - reddit.com → `reddit`
   - linkedin.com/posts/* (own profile florian-bruniaux) → `linkedin-own`
   - linkedin.com/posts/* (other) → `linkedin-other`
   - twitter.com / x.com → `twitter`
   - youtube.com → `video`
   - github.com/issues or github.com/discussions → `forum`
   - news.ycombinator.com → `forum`
   - Curated list / registry / directory → `directory`
   - podcasts.apple.com / spotify.com → `podcast`
   - instagram.com → `instagram`
3. Set `reach: unknown` (unless view count is visible in snippet)
4. Set `status: active`
5. Set `first_seen: <today's date>`
6. Write entry to YAML under the appropriate section comment

## Step 6: Update meta

- Increment `meta.total_mentions` by the number of added entries
- Set `meta.last_updated` to today's date

## Step 7: Update README stats table

Recount entries by platform and update the stats table in `docs/media-mentions/README.md`.

## Step 8: Validate

Run:

```bash
python3 scripts/check-media-mentions.py
```

Do not commit if IDs, canonical URLs, totals, platforms, or review-queue boundaries fail validation.

## Step 9: Commit only when requested

Without `--commit`, report the changed files and stop. With `--commit`, stage only the validated tracker
files. Never use a broad `git add` in a dirty worktree.

```bash
git add docs/media-mentions/mentions.yaml docs/media-mentions/README.md docs/media-mentions/review-queue.yaml
git commit -m "docs: track-mentions - add N new mentions (YYYY-MM-DD)"
```

## Notes

- Skip own properties (cc.bruniaux.com pages, GitHub repo itself, FlorianBruniaux profile)
- Skip mentions where the guide is cited only by implication or context, not by name or URL
- Put ambiguous or inaccessible cases in `review-queue.yaml`; do not add them to `mentions.yaml`
- Keep rejected false positives in the review queue so later scheduled runs do not rediscover them
- If Perplexity finds 0 new mentions, report "No new mentions found since last run."
