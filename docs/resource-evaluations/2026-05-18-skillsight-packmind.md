# Resource Evaluation: Skillsight (Packmind)

**Source:** [GitHub: PackmindHub/skillsight](https://github.com/PackmindHub/skillsight)
**Type:** Open-source self-hosted dashboard — Claude Code skills usage analytics
**Evaluated:** 2026-05-18
**Method:** 4-agent parallel audit (Security/Opus, Architecture/Sonnet, Docs/Sonnet, Ops/Sonnet)
**Version:** 0.2.1
**Related eval:** [#076: Packmind ContextOps Platform](076-packmind-contextops-platform.md)

---

## Content Summary

Skillsight is a self-hosted dashboard that ingests Claude Code OTEL telemetry and visualizes which skills are actually invoked across a team or organization. Two ingestion paths: push via OTLP HTTP/JSON (Claude Code → Skillsight directly), or pull via Loki (Grafana Cloud relay). Skills usage is visible per user, per session, per plugin, with cohort segmentation.

**What it actually ships (verified against code):**
- Dashboard with skill usage charts, team-level breakdowns, plugin tracking
- Marketplace sync: pulls skills catalogs from Git sources (GitHub PAT or token-based)
- Auth: JWT HS256 (jose) + argon2 password hashing, session cookies + separate ingestion tokens
- Real-time SSE events page (`/live-events`)
- Audit log of all administrative actions
- Cohort segmentation (in Roadmap but already implemented)
- Onboarding page that auto-generates Claude Code settings.json snippet

**Stack:** Bun monorepo, Hono backend, Drizzle ORM + PostgreSQL, React 18 + Vite 7 + Tailwind 4 + Recharts. Hexagonal architecture. 28K LOC, 33 test files, Biome lint, CI on GitHub Actions (lint+test+build+docker), Dockerfile multi-stage, Apache 2.0.

**Author:** Cédric Teyton, Packmind (see also [#076](076-packmind-contextops-platform.md)).

---

## Score

| Score | Meaning |
|-------|---------|
| 5 | Essential — Major gap in the guide |
| 4 | Very relevant — Significant improvement |
| **3** | **Relevant — Useful complement** |
| 2 | Marginal — Secondary info |
| 1 | Out of scope |

**Score: 3/5**

Skillsight addresses a real gap: no tool in the current guide covers team-level skills usage observability. The code is real (not vaporware), architecture is sound, auth is implemented seriously. However, three security issues are significant enough that recommending self-hosted deployment without explicit caveats would be irresponsible. Score reflects current state; upgrade to 4/5 when the three critical security issues are resolved.

---

## Comparison

| Aspect | Skillsight | Guide coverage |
|--------|-----------|---------------|
| Skills usage analytics per user/team | ✅ Core feature | ❌ No tool covers this |
| OTLP telemetry ingestion | ✅ HTTP/JSON endpoint | ⚠️ Mentions telemetry, no tools |
| Loki/Grafana Cloud integration | ✅ Pull scheduler | ❌ Not covered |
| Marketplace/plugin catalog sync | ✅ Git-based sync | ❌ Not covered |
| Auth (argon2 + JWT) | ✅ Implemented | N/A |
| Default-safe deployment | ❌ Weak defaults shipped | ✅ Guide warns on secrets |
| Automatic DB migrations on upgrade | ❌ Missing | N/A |
| Team-level observability tools | ❌ Missing (this is the gap) | ❌ Not in guide either |

---

## Integration Recommendation

**Target:** `guide/ecosystem/third-party-tools.md` — new subsection "Skills Observability"

**When to integrate:** Now, with explicit caveats. Promote to full recommendation (4/5) when three critical issues are fixed (see Conditions below).

**Framing in guide:**
- Position as the only open-source tool for tracking which Claude Code skills your team actually uses vs which ones you think they use.
- Mandatory caveats:
  1. Never deploy without overriding `JWT_SECRET` and `ADMIN_PASSWORD_INITIAL` — defaults are public and no boot-time warning is issued.
  2. Run Drizzle migrations manually on upgrades until automatic entrypoint is added.
  3. Set `PUBLIC_BASE_URL` in `.env` even if not load-balanced — affects both CORS policy and onboarding snippet correctness.
- Note the related Packmind ContextOps platform (eval #076) for the complementary standards distribution angle.

**Conditions for promotion to 4/5:**
1. Boot failure or explicit warning if `JWT_SECRET` matches the shipped default
2. Separate `ENCRYPTION_KEY` for at-rest credential encryption (decoupled from JWT rotation)
3. Automatic Drizzle migration execution at container startup

---

## Security Findings (Audit Summary)

Four findings are worth flagging to any operator before self-hosting:

**Deployment default risk.** `JWT_SECRET=change-me-in-production-please-at-least-32-chars` and `ADMIN_PASSWORD_INITIAL=admin` are literal defaults in `docker-compose.yml`. No boot-time warning. Zod validation accepts the JWT default because it meets the minimum character count. `docker compose up` without a `.env` produces a full-access instance in seconds. The README warns but nothing enforces it at runtime.

**Shared encryption key.** The `JWT_SECRET` is also the encryption key for at-rest storage of Loki and GitHub credentials (`encrypt.ts`: `getKey() = SHA-256(JWT_SECRET)`). Rotating the JWT secret (supported via `JWT_SECRET_PREVIOUS`) silently makes all stored credentials undecipherable. A leaked JWT secret also exposes external credentials. No AAD per row means stored blobs are interchangeable across integrations.

**Permissive CORS.** `PUBLIC_BASE_URL` defaults to echoing the request origin with `credentials: true` (`app.ts:55-65`). This variable is not in `.env.example`. An admin connected to a Skillsight instance who visits an attacker-controlled page can be cross-origin-requested against the admin API.

**No rate limiting.** Neither `/api/auth/login` nor the OTLP ingestion endpoint `/api/v0/telemetry/v1/logs` have rate limiting. Body size on the ingestion endpoint is uncapped.

---

## Architecture Highlights

The hexagonal architecture is real, not cargo-cult: ports are interfaces, use cases depend on abstractions, test coverage uses in-memory fakes with meaningful behavioral assertions. The PostgreSQL schema has proper constraints (FK, NOT NULL, functional indexes including partial JSONB indexes).

Three structural issues worth noting:

- Ingest pipeline has no DB transaction wrapping its 6 sequential upsert steps — partial failure creates inconsistent state silently.
- Loki and marketplace schedulers swallow errors with `.catch(() => {})` — a failing integration leaves no trace in logs or UI.
- Marketplace source config is captured at schedule creation time (stale after any UI edit until restart).

---

## Docs & DX Findings

Two issues directly block first-time setup:

1. **Image name mismatch**: README uses `ghcr.io/packmindhub/skills-obs:latest` in 7 places. The actual `docker-compose.yml` image is `ghcr.io/packmindhub/skillsight:latest`. Users following the Quick Start will encounter this immediately.

2. **OTLP endpoint variable inconsistency**: README documents `OTEL_EXPORTER_OTLP_ENDPOINT` (generic). The onboarding UI generates `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` (logs-specific, higher priority). Two sources, different configuration outcomes.

Onboarding experience is otherwise well-designed: the UI page auto-generates a complete `settings.json` snippet with a pre-created ingestion token. Time-to-operational for a prepared developer: 30–75 minutes depending on whether the above issues are hit.

---

## Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| Apache 2.0 license | ✅ | GitHub LICENSE |
| Self-hosted, single Docker container | ✅ | Dockerfile, docker-compose.yml |
| OTLP HTTP/JSON ingestion | ✅ | backend/src/http/telemetry.ts |
| Loki pull integration | ✅ | backend/src/infrastructure/gateways/loki-gateway.ts |
| JWT auth (jose) + argon2 passwords | ✅ | backend/src/infrastructure/crypto/jwt.ts, login.ts |
| Hexagonal architecture | ✅ | domain/, application/, infrastructure/, http/ |
| 33 test files | ✅ | Verified via tree |
| CI on GitHub Actions | ✅ | .github/workflows/ci.yml |
| Cohort segmentation | ✅ | frontend/src/pages/Cohorts/, backend/src/application/cohorts/ |
| Marketplace Git sync | ✅ | git-marketplace-http-gateway.ts |
| Real-time events page | ✅ | frontend/src/pages/LiveEvents/ |

---

## Final Decision

- **Score**: 3/5
- **Action**: Integrate with explicit caveats
- **Confidence**: High (code verified directly, not based on README claims)
- **Promote to 4/5 when**: Boot-time default detection, separate encryption key, automatic migrations
- **Constraints when citing in guide**:
  - Always include the three deployment caveats listed above
  - Do not claim "production-ready" until critical security issues are resolved
  - Note the project is v0.2.1 — still young, active development (101 commits, same-day release)
  - Cross-reference [#076 Packmind ContextOps](076-packmind-contextops-platform.md) for the broader Packmind ecosystem context
