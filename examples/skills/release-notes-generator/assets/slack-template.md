# Slack Announcement Template

Use this template for generating product-focused Slack messages.

```
Version X.Y.Z - Deployed to production

PR : [Release PR URL, e.g.: https://github.com/{owner}/{repo}/pull/XXX]

In brief : [Sentence describing the main objective of this release]

---

New Features

[Feature Name 1]
> [1-2 sentence description of user impact]
> Who is affected: [End-users / Admins / All]

[Feature Name 2]
> [1-2 sentence description]
> Who is affected: [Roles]

---

Important Fixes

- [Bug fix described in user-friendly language]
- [Bug fix described in user-friendly language]

---

Improvements

- [UX/UI or workflow improvement in user language]
- [...]

---

By the numbers

- X new features
- Y bugs fixed
- Z improvements

---

Questions? Contact @[team-lead] or the dev team
```

## Guidelines

### DO
- Use accessible language (no technical jargon)
- Focus on user impact
- Be concise (max 10 lines per section)
- Use emojis sparingly

### AVOID
- "Implementation of the DataLoader pattern to solve N+1 queries"
- "Complete refactoring of the permissions system with scope ANY/ASSIGNED"
- "Migration from webpack to Turbopack"

### Tech -> Product Transformation

| Technical | Product |
|-----------|---------|
| N+1 query optimization with DataLoader | Faster loading of user and feature lists |
| AI embeddings implementation with pgvector | New intelligent search for similar items |
| Fix scope permissions in getPermissionScope() | Fixed a bug preventing some users from accessing their data |
| Migration to kebab-case for files | *Do not communicate (purely technical)* |
| Fix DB connection with retry logic | Better database connection stability |
| Add error monitoring for orphan records | Automatic detection of orphan records |

### Optional Sections

If the release contains important items, add:

Heads up
- [Important information users should know]
- [Behavior changes they might notice]

Coming soon
- [Teaser for the next big feature]
- [Feature in development coming soon]
