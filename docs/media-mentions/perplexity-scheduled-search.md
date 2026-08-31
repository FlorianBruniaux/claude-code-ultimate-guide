# Scheduled public-mentions search

Use this prompt for a weekly Perplexity Scheduled Search. The search is discovery-only: the local
`source-command-track-mentions` skill validates, deduplicates, and applies accepted candidates later.

## Scheduled prompt

```text
Search the public web for third-party references to Florian Bruniaux's active public projects,
especially Claude Code Ultimate Guide, Claude Cowork Guide, StarMapper, CCBoard,
CC-Copilot Bridge, ctxharness, Dep Scope, flow-lean, Google Search Console MCP,
Claude Code Plugins, CC-Sessions, cc-skill-usage, YouTube Video Insights,
AgentSec Triage, and GitHub Roast TPC.

Search articles, newsletters, podcasts, YouTube, Reddit, Hacker News, LinkedIn, X,
GitHub repositories and discussions, package or MCP registries, automated directories,
translations, adaptations, and mirrors. Search broadly on every run because pages may be
indexed late. Exclude Florian Bruniaux's own sites, repositories, and social posts from
third-party totals.

Confirm a result only when the page, public metadata, or indexed snippet contains an explicit
project name, canonical repository slug, or official domain. A generic title such as
"ultimate Claude Code guide" is not evidence.

Return exactly three sections:
1. new_confirmed
2. already_tracked
3. rejected_or_unverified

For every result return: canonical URL, title, author, platform, publication date when available,
language, project, identifier found, evidence location, classification, confidence, metadata
problems, and one sentence describing the reference.

Classifications: editorial, social, forum, translation, mirror, adoption, registry,
automated_directory.

Do not treat directory counters, token counts, trust scores, saves, or repository stars as
audience measurements. Flag stale install commands, package names, content counts, authorship,
or capabilities. Do not modify a repository or publish a result.
```

## Review contract

1. Export or paste the scheduled result into a guide task.
2. Run `/track-mentions --dry-run` against `mentions.yaml` and `review-queue.yaml`.
3. Verify every `new_confirmed` URL independently.
4. Add inaccessible candidates to the review queue.
5. Reject title collisions and owned properties.
6. Apply only the entries explicitly approved by the user.
7. Run `python3 scripts/check-media-mentions.py`.
8. Commit only when `/track-mentions --commit` was requested.

The scheduled search never owns the source of truth. `mentions.yaml` and the portfolio catalog do.
