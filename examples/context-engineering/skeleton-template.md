# CLAUDE.md — [Project Name]

<!--
HOW TO USE THIS SKELETON

Fill in each section based on your project. Delete placeholder comments when done.
Goal: give Claude enough context to make correct decisions without asking, while staying under 500 lines.

Key principles:
- Specific beats vague: "Use zod for external input validation" beats "validate inputs"
- Anti-patterns are as valuable as rules: tell Claude what NOT to do
- Update after each significant session (see rules/update-loop-retro.md)
- Run `canary-check.sh` weekly to catch drift
-->

## Project Overview

<!--
Write 2-3 sentences answering:
- What does this project do?
- Who uses it? (internal tool, public API, consumer app, etc.)
- What's the primary language and deployment target?

Example:
"A REST API that processes financial transactions for retail merchants, consumed by a Next.js
dashboard and a React Native mobile app. Built with Node.js + TypeScript, deployed to AWS ECS.
PCI-DSS compliance applies to all payment-adjacent code."
-->

[PROJECT DESCRIPTION]

## Architecture

<!--
Describe the shape of the system. Not a tutorial — just the decisions Claude needs to
make correct assumptions. Diagrams are optional; prose is fine.

Cover:
- Monolith or services? If services, how many and how do they communicate?
- How is state managed (database, cache, event sourcing)?
- Key data flow (request lifecycle, async patterns)
- Folder structure if non-obvious
-->

### Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | TypeScript | 5.x |
| Runtime | Node.js | 20.x |
| Framework | [e.g., Express, Fastify, NestJS] | x.x |
| Database | [e.g., PostgreSQL] | x.x |
| ORM / Query Builder | [e.g., Prisma, Drizzle, Knex] | x.x |
| Cache | [e.g., Redis, none] | - |
| Message Queue | [e.g., BullMQ, SQS, none] | - |
| Frontend | [e.g., Next.js, none] | x.x |
| Testing | [e.g., Vitest, Jest] | x.x |
| CI/CD | [e.g., GitHub Actions] | - |

### Folder Structure

```
src/
  [describe key directories and what belongs in each]
  [example: api/ — route handlers only, no business logic]
  [example: services/ — business logic, called by handlers]
  [example: db/ — Prisma schema, migrations, query functions]
```

### Key Architectural Decisions

<!--
Record the "why" behind non-obvious choices. This prevents Claude from suggesting
alternatives that were already considered and rejected.

Example:
- Repository pattern is NOT used — we use Prisma directly in services (decision: team
  familiarity, added abstraction not worth it at current scale)
- Zod schemas are colocated with route handlers, not in a shared schemas/ directory
-->

- [DECISION 1]
- [DECISION 2]

## Code Standards

<!--
Be specific. "Write clean code" is useless. "Use named exports only — no default exports" is actionable.
Organize by language/domain if you have multiple.
-->

### TypeScript

- Strict mode is enabled (`"strict": true` in tsconfig). Never use `any` — use `unknown` and narrow.
- All public function signatures must have explicit return types.
- Use `type` for unions and intersections, `interface` for object shapes that may be extended.
- [ADD YOUR RULES]

### Naming

- Files: `kebab-case.ts` (e.g., `user-service.ts`, `create-order.test.ts`)
- Classes: `PascalCase`
- Functions and variables: `camelCase`
- Constants: `SCREAMING_SNAKE_CASE`
- [ADD ANY EXCEPTIONS]

### Error Handling

<!--
Undefined behavior here causes the most inconsistency. Be explicit.

Example:
- All async functions must be wrapped in try/catch at the handler boundary
- Errors propagate up as typed error objects, never raw strings
- Use the AppError class in src/errors.ts — never throw plain Error objects in service layer
-->

- [ERROR HANDLING RULES]

### Comments

<!--
Example:
- Inline comments only on non-obvious logic (never explain what the code does, only why)
- All exported functions must have a JSDoc block with @param and @returns
- TODO comments are not allowed in production code — open an issue instead
-->

- [COMMENT RULES]

## Development Workflow

### Git Conventions

- Branch naming: `[type]/[short-description]` — e.g., `feat/add-refund-flow`, `fix/order-status-race`
- Commit format: [Conventional Commits](https://www.conventionalcommits.org/)
  - `feat:` new feature
  - `fix:` bug fix
  - `chore:` maintenance, dependency updates
  - `docs:` documentation only
  - `test:` tests only
  - `refactor:` no behavior change
- Commits should be atomic — one logical change per commit
- [ADD ANY EXCEPTIONS OR ADDITIONAL TYPES]

### PR Requirements

<!--
Example:
- All PRs require at least one reviewer
- CI must be green before merge
- PR description must include "Why" not just "What"
- Link to issue or ticket in PR body
-->

- [PR RULES]

### Local Setup

```bash
# Install dependencies
[INSTALL COMMAND]

# Set up environment
cp .env.example .env
# Edit .env with your local values

# Run database migrations
[MIGRATION COMMAND]

# Start development server
[DEV COMMAND]
```

## Testing

<!--
Vague testing rules produce no tests. Specific rules produce correct tests.
Tell Claude: what framework, what to test, how to structure tests, what coverage means here.
-->

### Framework and Location

- Framework: [e.g., Vitest]
- Test files: colocated with source (`foo.ts` → `foo.test.ts`) OR in `__tests__/` [choose one]
- Run tests: `[TEST COMMAND]`
- Run with coverage: `[COVERAGE COMMAND]`

### What Requires Tests

- All service layer functions (unit tests with mocked dependencies)
- All API routes (integration tests using supertest or equivalent)
- All utility functions that contain branching logic
- **Not required**: pure pass-through functions, simple getters/setters, Prisma model definitions

### Test Structure

```typescript
// Follow this pattern:
describe('[unit under test]', () => {
  describe('[method or scenario]', () => {
    it('[expected behavior in plain English]', async () => {
      // Arrange
      // Act
      // Assert
    })
  })
})
```

### Mocking

- Mock at the boundary: mock external services, never internal modules
- [ADD YOUR MOCKING CONVENTIONS — e.g., "Use vi.mock() at file level, not inside tests"]

## Deployment

### Environments

| Environment | Branch | URL | Notes |
|------------|--------|-----|-------|
| Local | any | localhost:[PORT] | |
| Staging | `main` | [STAGING URL] | Auto-deploys |
| Production | [TAG/BRANCH] | [PROD URL] | Manual trigger |

### Deploy

```bash
# Staging (auto on merge to main — no manual step needed)

# Production
[DEPLOY COMMAND OR PROCESS]
```

### Post-Deploy Checks

<!--
Tell Claude what to verify after deploying so it can suggest this when relevant.

Example:
- Check /health endpoint returns 200
- Verify Sentry has no new errors in first 5 minutes
- Confirm database migrations ran (check migration table)
-->

- [POST-DEPLOY CHECKS]

## What Claude Should NOT Do

<!--
This section is high-value. Anti-patterns prevent regressions and stop Claude from
suggesting alternatives that were already rejected.

Be specific about the pattern AND why it's banned.
-->

### Technologies Not in Use

- Do NOT suggest GraphQL — REST is the architectural decision for this project
- Do NOT use [LIBRARY NAME] — replaced by [ALTERNATIVE] in [VERSION/DATE]
- [ADD YOUR BANNED TECHNOLOGIES]

### Patterns to Avoid

<!--
Example:
- Never use class components in React — functional components only
- Never mutate request/response objects directly — use immutable patterns
- Never use console.log in production code — use the logger at src/lib/logger.ts
- Never hardcode environment-specific values — use process.env with validation in src/config.ts
-->

- [ANTI-PATTERN 1]
- [ANTI-PATTERN 2]
- [ANTI-PATTERN 3]

### Known Problem Areas

<!--
Patterns that caused production bugs or significant rework. Claude should be extra careful here.

Example:
- The order state machine in src/orders/state.ts is complex — always read it fully before modifying
- Payment webhooks are idempotent — every handler must check for duplicate event IDs
-->

- [KNOWN PROBLEM AREA 1]
- [KNOWN PROBLEM AREA 2]
