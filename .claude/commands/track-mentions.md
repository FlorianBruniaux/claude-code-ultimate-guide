---
name: track-mentions
description: Search for new online mentions of the Claude Code Ultimate Guide and update the tracker
argument-hint: "[--add-all | --dry-run]"
---

# Track Mentions Workflow

Find new online mentions of the Claude Code Ultimate Guide (GitHub + cc.bruniaux.com) and update `docs/media-mentions/mentions.yaml`.

## Usage

```
/track-mentions            # Search + report new mentions, confirm before adding
/track-mentions --dry-run  # Search + report only, no YAML changes
/track-mentions --add-all  # Search + add all found mentions automatically
```

## Step 1: Load existing tracker

Read `docs/media-mentions/mentions.yaml` to get:
- Current `meta.total_mentions` count
- All existing `url` fields → build a deduplication set

## Step 2: Run Perplexity deep research

Use `mcp__perplexity__perplexity_deep_research` with `reasoning_effort: "high"` and this query
(do NOT mention specific dates or "past 30 days" — triggers a refusal on date-awareness):

```
Find all articles, blog posts, newsletters, Reddit threads, Twitter/X posts, LinkedIn posts,
YouTube videos, podcasts, GitHub issues/repos, and directories that mention "Claude Code
Ultimate Guide" by Florian Bruniaux (GitHub: FlorianBruniaux/claude-code-ultimate-guide,
website: cc.bruniaux.com). Search broadly for third-party content only — exclude the GitHub
repo itself and cc.bruniaux.com own pages.

For each result provide: URL, publication date if available, author/platform name, language,
and one sentence on how they reference the guide.

Also search explicitly for:
- "cc.bruniaux.com" cited as a resource on third-party sites
- "claude-code-ultimate-guide florian bruniaux" in blog posts and tutorials
- "FlorianBruniaux" in dev tutorials referencing the guide
- The guide mentioned in non-English content (French, Spanish, German, Korean, Portuguese, etc.)
```

**If Perplexity returns no results** (model refuses citing knowledge cutoff), fall back to
WebSearch with these parallel queries:
```
"claude code ultimate guide" -site:github.com -site:cc.bruniaux.com 2026
site:reddit.com "cc.bruniaux.com" OR "claude code ultimate guide"
site:dev.to OR site:hashnode.com OR site:medium.com "claude code ultimate guide" "florian" OR "bruniaux"
"claude code ultimate guide" twitter OR x.com
```
Then use `WebFetch` on each candidate URL to verify the guide is explicitly mentioned by name or URL.

## Step 3: Deduplicate

For each result from Perplexity:
1. Normalize the URL (strip trailing slash, lowercase domain)
2. Check against existing URLs in the YAML
3. Skip if already tracked

## Step 4: Report new mentions

Display a table for review:

```
New mentions found: N

| # | Platform | Author | Title | URL | Date |
|---|----------|--------|-------|-----|------|
| 1 | article  | ...    | ...   | ... | ...  |
```

If `--dry-run`: stop here, no changes.

## Step 5: Add to YAML (unless --dry-run)

For each new mention (all if `--add-all`, else ask confirmation per item):

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

## Step 8: Commit

```bash
git add docs/media-mentions/
git commit -m "docs: track-mentions — add N new mentions (YYYY-MM-DD)"
```

## Notes

- Skip own properties (cc.bruniaux.com pages, GitHub repo itself, FlorianBruniaux profile)
- Skip mentions where the guide is cited only by implication or context, not by name or URL
- For ambiguous cases (guide not named but URL present), add with a note
- If Perplexity finds 0 new mentions, report "No new mentions found since last run."