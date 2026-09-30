# Sentry MCP server reference

Reference file for the Sentry MCP server. Read this before making any Sentry MCP calls. It contains the query syntax, known gotchas, and working examples that reduce call failures.

> This is a template reference file. Replace the Sentry-specific content with the equivalent for your MCP server.

---

## Available tools

### `mcp__sentry-mcp__list_issues`

**Purpose**: Fetch a list of issues from one or more projects.

**Key parameters**:
- `organization_slug` (required): Your Sentry org slug, not the org name. Get it from the Sentry URL: `sentry.io/organizations/<slug>/`.
- `project_slug` (optional): Scope to one project. Omit to fetch across all projects.
- `query` (optional): Sentry search query. Supports `is:unresolved`, `level:error`, `has:user`. Default: `is:unresolved`.
- `limit` (optional): Max issues returned. Default: 25. Max: 100.

**Gotchas**:
- Organization and project slugs are lowercase, hyphen-separated. Do not use the display name.
- Without `query`, you get all statuses including `resolved`. Always add `is:unresolved` unless you specifically want resolved issues.
- The `limit` cap is 100 per call. For large orgs, use `cursor` for pagination (see below).

### `mcp__sentry-mcp__get_issue`

**Purpose**: Fetch full details for one issue, including the latest event and stack trace.

**Key parameters**:
- `issue_id` (required): The numeric Sentry issue ID. Get it from `list_issues`.
- `organization_slug` (required): Same as above.

**Gotchas**:
- Returns the most recent event only. If you need a specific event, use `get_event` with the event ID instead.
- Stack frames are ordered outermost to innermost by default. The bottom frame is typically the crash point.

### `mcp__sentry-mcp__get_event`

**Purpose**: Fetch full details for a specific event within an issue.

**Key parameters**:
- `event_id` (required): Full 32-character event ID (UUID format, no dashes).
- `organization_slug` (required): Same as above.
- `issue_id` (required): The parent issue ID.

**Gotchas**:
- Event IDs are case-insensitive but the API is case-sensitive. Use lowercase.
- Events older than 90 days may not be available in the default retention plan.

### `mcp__sentry-mcp__search_events`

**Purpose**: Search raw events across issues. Slower than `list_issues` but supports full-text queries.

**Key parameters**:
- `query` (required): Full-text search. Supports field filters: `message:`, `level:`, `user.id:`, `url:`, `transaction:`.
- `project_slug` (optional): Scope to one project. Required if org has many projects (performance).
- `start` / `end` (optional): ISO 8601 timestamps. Default: last 24 hours.
- `limit` (optional): Default: 10. Max: 100.

**Gotchas**:
- Full-text search is case-insensitive but field filters are exact-match. `level:ERROR` fails; use `level:error`.
- Time ranges must use ISO 8601: `2026-04-10T00:00:00Z`. Relative formats like `now-24h` are not supported here (use `list_issues` for relative ranges).
- Without `project_slug`, large orgs time out on `search_events`. Always scope by project when searching events.

---

## Query syntax

### Sentry Search Query (for `query` parameter in `list_issues` and `search_events`)

```
is:unresolved                          # Unresolved issues only
is:unresolved level:error              # Unresolved errors (not warnings)
is:unresolved has:user                 # Issues affecting identified users
is:unresolved times_seen:>100          # High-frequency issues
project:api-service is:unresolved      # Scope to one project
assigned:me is:unresolved              # Issues assigned to current user
!has:assignee is:unresolved            # Unassigned issues
```

### Pagination

For orgs with many issues, use cursor-based pagination:
1. First call: `list_issues(..., limit=100)` - response includes `cursor` field
2. Next page: `list_issues(..., limit=100, cursor="<cursor from previous response>")`
3. Stop when response has no `cursor` field or issue count < limit

---

## Known patterns and exclusions

When analyzing issues, these patterns are typically noise and should be excluded from reports unless explicitly requested:

| Pattern | Reason to Exclude |
|---------|-------------------|
| `404` errors on `/static/` or `/assets/` | Expected behavior: browser requests stale asset URLs after deploy |
| `ChunkLoadError` in frontend bundles | Usually caused by the same deploy timing, not a code bug |
| `ResizeObserver loop limit exceeded` | Browser-level warning, not actionable |
| Health check endpoint errors | Monitoring infrastructure, not user-facing |

If you exclude an issue, state it explicitly in the report's "Out of Scope" section.

---

## Working examples

### Fetch top unresolved errors in production

```
list_issues(
  organization_slug="your-org",
  query="is:unresolved level:error",
  limit=50
)
```

### Fetch issues from a specific project in the last week

```
list_issues(
  organization_slug="your-org",
  project_slug="api-service",
  query="is:unresolved",
  limit=100
)
```

### Get full stack trace for a specific issue

```
get_issue(
  organization_slug="your-org",
  issue_id="1234567"
)
```

---

## Adapting this file

When forking this template for a different MCP (Datadog, PagerDuty, Linear, etc.):

1. Replace "Sentry" with your MCP server name throughout
2. Replace the tool names (`mcp__sentry-mcp__*`) with your MCP's actual tool names
3. Document the 2-3 most common parameter mistakes for each tool
4. Add query syntax specific to your MCP (SQL dialect, filter syntax, etc.)
5. Add a "Known Patterns and Exclusions" section for noise in your data source
6. Include 3-5 working examples that cover the 80% use case

The goal: after reading this file, Claude should make zero syntax errors and zero retry calls caused by wrong parameter format.
