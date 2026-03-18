# Tech-to-Product Transformation Rules

This document defines how to transform technical commit messages into user-friendly product language.

## Transformation Categories

### 1. COMMUNICATE (Transform to product language)

| Technical Pattern | Product Message |
|-------------------|-----------------|
| `N+1 queries`, `DataLoader`, `batching` | "Faster list loading" |
| `embeddings`, `vector search`, `pgvector` | "Improved intelligent search" |
| `permissions`, `scope`, `access control` | "Fixed an access bug" |
| `retry logic`, `resilience`, `connection errors` | "Better connection stability" |
| `SSE`, `real-time`, `WebSocket` | "Real-time updates" |
| `cache`, `memoization` | "Improved performance" |
| `responsive`, `mobile` | "Better mobile experience" |
| `accessibility`, `a11y`, `WCAG` | "Improved accessibility" |
| `monitoring`, `alerting`, `error tracking` | "Better error tracking" |
| `validation`, `sanitization` | "Enhanced security" |

### 2. DO NOT COMMUNICATE (Internal/Technical only)

These patterns should NOT appear in Slack announcements:

| Technical Pattern | Reason |
|-------------------|--------|
| `refactor`, `refactoring` | Internal code quality |
| `webpack`, `turbopack`, `bundler` | Build tooling |
| `eslint`, `prettier`, `linting` | Code style |
| `kebab-case`, `naming convention` | Internal standards |
| `TypeScript`, `type safety` | Developer experience |
| `test`, `spec`, `coverage` | Testing infrastructure |
| `chore`, `maintenance` | Routine maintenance |
| `docs`, `documentation` | Internal docs |
| `deps`, `dependencies`, `bump` | Dependency updates |
| `CI`, `CD`, `workflow` | DevOps infrastructure |

### 3. SECURITY (Always communicate, simplified)

| Technical | Product |
|-----------|---------|
| `CVE-XXXX-XXXXX` | "Fixed a security vulnerability" |
| `XSS`, `injection` | "Enhanced data protection" |
| `authentication`, `auth bypass` | "Improved login security" |
| `CORS`, `CSRF` | "Protection against web attacks" |

## Context-Aware Transformations

### API-related
- "Fix endpoint rate limiting" -> "Improved API stability"
- "Add request validation" -> "Better input handling"
- "Optimize query performance" -> "Faster data loading"

### Dashboard-related
- "Fix dashboard widget rendering" -> "Fixed display issues on dashboard"
- "Add export functionality" -> "New data export feature"
- "Improve chart performance" -> "Faster dashboard loading"

### Notification-related
- "Fix email delivery queue" -> "Improved notification reliability"
- "Add webhook retry logic" -> "More reliable integrations"
- "Optimize notification batching" -> "Faster notification delivery"

### Search-related
- "Fix search indexing race condition" -> "Improved search reliability"
- "Add fuzzy matching" -> "Better search results"
- "Optimize search query execution" -> "Faster search"

## Role-Based Impact

Always specify who is affected:

| Impact | Roles |
|--------|-------|
| Dashboard changes | End-users, Admins |
| API changes | End-users, Power users |
| Admin panel | Admins only |
| Billing/Payment | Admins, Stakeholders |
| Reports/Analytics | Admins, Power users |
| Notifications | All users |
| Search | All users |

## Severity Indicators

Use these prefixes when appropriate:

- **Critical** : Production-blocking issues
- **Important** : User-facing bugs
- **Minor** : Quality of life improvements
- *Do not mention* : Internal fixes
