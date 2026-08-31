# Media Mentions Tracker

Tracks all external sources that mention the Claude Code Ultimate Guide (GitHub or cc.bruniaux.com).

This file remains guide-specific. The public cross-project catalog, including Cowork, StarMapper,
CCBoard, CC-Copilot Bridge, ctxharness, Dep Scope, flow-lean, GSC MCP, and Claude Code Plugins, lives in
`~/Sites/perso/florian-portfolio/src/data/mentions.json` and is published at
`https://www.florian.bruniaux.com/mentions/`. RTK is outside that catalog by design.

## Source of truth

- `mentions.yaml`: one entry per confirmed mention.
- `review-queue.yaml`: inaccessible candidates and rejected false positives kept for future deduplication.

## Schema

```yaml
- id: "001"                  # Sequential, zero-padded
  platform: article          # article | reddit | linkedin-own | linkedin-other | twitter | directory | instagram | podcast | forum | video | translation
  url: "https://..."
  title: "..."
  author: "..."              # Handle, name, or publication name. Use "unknown" if not found.
  date: "YYYY-MM-DD"         # Publication date, or null if unknown
  angle: "..."               # One sentence: how they framed the guide
  reach: unknown             # low (<1K) | medium (1K-10K) | high (10K-100K) | viral (100K+) | unknown | null (own property)
  status: active             # active | dead | paywall
  notes: "..."               # Optional. Anything worth remembering (quote, context, SEO value).
  first_seen: "YYYY-MM-DD"   # Date we logged it
```

## Adding a new mention

1. Add an entry to `mentions.yaml` with the next sequential id.
2. Update `meta.total_mentions` and `meta.last_updated`.
3. Commit: `docs: add media mention: [platform] [author/publication]`

## Slash command

`/track-mention <url>` is not yet implemented. Add manually for now.

## Stats (as of 2026-08-31)

| Platform | Count |
|---|---|
| Articles / blogs | 12 |
| Videos (YouTube) | 2 |
| Podcasts | 1 |
| Reddit | 4 |
| LinkedIn (own) | 2 |
| LinkedIn (third-party) | 7 |
| Twitter / X | 3 |
| Instagram | 1 |
| Directories / registries | 14 |
| Forums (HN) | 1 |
| Translations / adaptations | 2 |
| **Total** | **49** |

The 49 tracked references include 2 posts from Florian Bruniaux. The guide catalog therefore contains
47 third-party references: 32 editorial or community mentions, 2 translations, and 13 directory
entries. Automated indexes are discovery signals, not independent endorsements. The portfolio catalog
is synchronized separately and may temporarily lag this source during concurrent work.

### Languages spotted

| Language | Mentions |
|---|---|
| English | 39 |
| French | 3 |
| Spanish | 2 |
| Korean | 1 |
| Chinese | 2 |
| Ukrainian | 1 |
| Unknown | 1 |

## Slash command

Run `/track-mentions` to search for new mentions via Perplexity and update this file automatically.

For unattended runs, use `/track-mentions --scheduled`. This mode produces a candidate report only:
it must not modify either catalog or create a commit. The exact Perplexity prompt and review procedure
live in `perplexity-scheduled-search.md`.

Validate the catalog and review queue after every accepted update:

```bash
python3 scripts/check-media-mentions.py
```
