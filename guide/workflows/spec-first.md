---
title: "Spec-First Development with Claude"
description: "Define specifications in CLAUDE.md before implementation for structured development"
tags: [workflow, architecture, config]
---

# Spec-First Development with Claude

> **Confidence**: Tier 2 — Validated by multiple production teams and aligns with official SDD guidance.

Define what you want in CLAUDE.md BEFORE asking Claude to build. One well-structured iteration equals 8 unstructured ones.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [The Pattern](#the-pattern)
3. [Task Granularity: Sizing Work for Agents](#task-granularity-sizing-work-for-agents)
4. [CLAUDE.md Spec Templates](#claudemd-spec-templates)
5. [Step-by-Step Workflow](#step-by-step-workflow)
6. [Integration with Tools](#integration-with-tools)
7. [When to Use](#when-to-use)
8. [Anti-Patterns](#anti-patterns)
9. [See Also](#see-also)

---

## TL;DR

```
1. Write spec in CLAUDE.md
2. Claude reads spec automatically
3. Implementation follows spec exactly
4. Verify against spec
```

CLAUDE.md IS your spec file. Treat it as a contract.

---

## The Pattern

Spec-First Development inverts the typical AI coding flow:

```
Traditional:        Spec-First:
───────────         ──────────
Prompt → Code       Spec → Prompt → Code → Verify
  │                   │               │       │
  └─ Hope it's       └── Contract    └── Follows spec
     what you want        defined          └── Check against spec
```

The spec becomes the source of truth that:
- Constrains what Claude builds
- Documents decisions for the team
- Enables verification of completeness

---

## Task Granularity: Sizing Work for Agents

Before writing the spec, verify the task is the right size. Agents work best with **vertical slices** — thin, end-to-end units that cut through all layers but implement exactly one complete user behavior (e.g. "password reset via email", not "authentication system").

**Rule of thumb**: One agent session = one vertical slice. If the task description requires "and" between two user behaviors, split it.

### PRD Quality Checklist

Run this before handing any task to an agent. Six dimensions to verify:

| Dimension | Question to ask | Red flag |
|-----------|----------------|----------|
| **Problem Clarity** | Is the problem statement unambiguous? | "Improve performance" |
| **Testable Criteria** | Can completion be verified automatically? | "Works well" |
| **Scope Boundaries** | What is explicitly OUT of scope? | Nothing listed as excluded |
| **Observable Done** | What does "done" look like to a user? | Internal-only description |
| **Requirements Clarity** | No implementation details in the spec? | "Use Redis for caching" |
| **Terminology** | Same terms used throughout? | "user" and "account" mixed |

A task that fails 2+ dimensions needs rework before an agent touches it. The spec review catches ambiguity that will otherwise surface as incorrect implementation mid-session.

```
❌ Too big, ambiguous:
"Add user authentication to the app"

✅ One vertical slice:
"Users can log in with email + password.
- POST /auth/login returns JWT on success, 401 on failure
- Invalid credentials show 'Email or password incorrect' (not which is wrong)
- Session expires after 24h
- Out of scope: OAuth, password reset, remember me"
```

---

## CLAUDE.md Spec Templates

### Feature Spec (Most Common)

```markdown
## Feature: [Name]

### Description
[2-3 sentences explaining the feature purpose]

### Capabilities
- MUST: [Required functionality]
- MUST: [Another requirement]
- SHOULD: [Nice to have]
- MUST NOT: [Explicit exclusions]

### Tech Stack
- Required: [lib1, lib2, lib3]
- Forbidden: [lib4, lib5]

### Acceptance Criteria
- [ ] Criterion 1: [Specific, testable condition]
- [ ] Criterion 2: [Another condition]
- [ ] Criterion 3: [Edge case handling]

### API Contract (if applicable)
- Endpoint: POST /api/[resource]
- Request: { field1: string, field2: number }
- Response: { id: string, created: timestamp }
- Errors: 400 (validation), 404 (not found), 500 (server)
```

### Architecture Spec

```markdown
## Architecture: [Component Name]

### Purpose
[Why this component exists]

### Boundaries
- Owns: [What this component is responsible for]
- Delegates to: [What other components handle]
- Does NOT: [Explicit non-responsibilities]

### Dependencies
- Upstream: [Components that call this]
- Downstream: [Components this calls]

### Data Flow
```
Input → Validation → Processing → Output
         │              │
         └─ Errors ─────┘
```

### Constraints
- Performance: [Response time, throughput]
- Security: [Auth requirements, data handling]
- Scalability: [Expected load, limits]
```

### API Spec

```markdown
## API: [Endpoint Name]

### Endpoint
`POST /api/v1/[resource]`

### Authentication
Bearer token required. Scopes: `read:resource`, `write:resource`

### Request
```json
{
  "field1": "string (required, max 255 chars)",
  "field2": "number (optional, default: 0)",
  "nested": {
    "subfield": "boolean"
  }
}
```

### Response
```json
{
  "id": "uuid",
  "created_at": "ISO 8601 timestamp",
  "data": { ... }
}
```

### Error Codes
| Code | Meaning | Response Body |
|------|---------|---------------|
| 400 | Validation failed | `{ "errors": [...] }` |
| 401 | Not authenticated | `{ "message": "..." }` |
| 403 | Not authorized | `{ "message": "..." }` |
| 404 | Resource not found | `{ "message": "..." }` |
```

---

## Step-by-Step Workflow

### Step 1: Write the Spec

Before any implementation request, add spec to CLAUDE.md:

```markdown
## Feature: User Authentication

### Capabilities
- MUST: Email/password login
- MUST: JWT token generation
- MUST: Password hashing with bcrypt
- SHOULD: Remember me functionality
- MUST NOT: Store plain text passwords

### Tech Stack
- Required: bcrypt, jsonwebtoken
- Forbidden: passport.js (too heavy for this use case)

### Acceptance Criteria
- [ ] User can login with valid credentials
- [ ] Invalid credentials return 401
- [ ] Token expires after 24h (or 7d with remember me)
- [ ] Passwords hashed with cost factor 12
```

### Step 2: Reference Spec in Prompt

```
Implement the User Authentication feature as specified in CLAUDE.md.
Follow the acceptance criteria exactly.
```

Claude automatically reads CLAUDE.md and follows the spec.

### Step 3: Verify Against Spec

After implementation, verify:

```
Review the implementation against the User Authentication spec.
Check off each acceptance criterion that's satisfied.
List any gaps.
```

### Step 4: Update Spec if Needed

If requirements change during implementation:

```
Update the User Authentication spec to include:
- MUST: Rate limiting (5 attempts per minute)
Then implement the rate limiting.
```

---

## Integration with Tools

### With Spec Kit (Greenfield)

```bash
# Install Spec Kit
npx @anthropic/spec-kit init

# Use slash commands
/speckit.constitution  # Define project guardrails
/speckit.specify       # Write feature specs
/speckit.plan          # Create implementation plan
/speckit.implement     # Build from spec
```

### With OpenSpec (Brownfield)

```bash
# Install OpenSpec
npm install -g @fission-ai/openspec@latest
openspec init

# Use slash commands
/openspec:proposal "Add dark mode"  # Create change proposal
/openspec:apply add-dark-mode       # Implement changes
/openspec:archive add-dark-mode     # Merge to specs
```

### With Plan Mode

```
[Press Shift+Tab to enter Plan Mode]

I need to implement the Payment Processing feature.
Review the spec in CLAUDE.md and create an implementation plan.
```

---

## When to Use

### Use Spec-First

| Scenario | Why |
|----------|-----|
| New features | Define before building |
| API design | Contract must be explicit |
| Architecture decisions | Document constraints |
| Team collaboration | Shared understanding |
| Complex requirements | Reduce ambiguity |

### Skip Spec-First

| Scenario | Why |
|----------|-----|
| Quick fixes | Overhead not worth it |
| Exploration | Don't know what you want yet |
| Prototyping | Requirements will change |
| Single-line changes | Obvious intent |

---

## Anti-Patterns

### Vague Specs

```markdown
# Wrong
## Feature: User Management
- Handle users

# Right
## Feature: User Management
### Capabilities
- MUST: Create user with email, password, name
- MUST: Update user profile (name, avatar)
- MUST: Soft delete (mark as inactive, don't remove data)
- MUST NOT: Allow duplicate emails
```

### Spec After Code

```
# Wrong workflow
1. Ask Claude to implement feature
2. Write spec documenting what was built

# Right workflow
1. Write spec defining what should be built
2. Ask Claude to implement from spec
```

### Ignoring Forbidden

```markdown
# Don't forget exclusions
### Tech Stack
- Required: React, TypeScript
- Forbidden: jQuery, vanilla JS, class components
             ↑ These constraints prevent drift
```

---

## Modular Spec Design

**Pattern**: Break large specifications into multiple focused files instead of cramming everything into a single CLAUDE.md.

### The Problem: Monolithic CLAUDE.md

When specs exceed ~200 lines, several issues emerge:

- **Context pollution**: Claude struggles to extract relevant information from bloated context
- **Cognitive overload**: Developers can't quickly scan for what they need
- **Maintenance burden**: Updating one area requires navigating unrelated sections
- **Performance degradation**: Large CLAUDE.md files slow down context loading and processing

### When to Split

| Threshold | Action |
|-----------|--------|
| **<100 lines** | Single CLAUDE.md is fine |
| **100-200 lines** | Consider splitting if distinct domains exist |
| **>200 lines** | **Split immediately** — you're past the cognitive load threshold |
| **Multi-team projects** | Split by domain/ownership regardless of size |

### Split Strategies

**1. Feature-Based Split**

```
CLAUDE.md              # Core project context
CLAUDE-auth.md         # Authentication spec
CLAUDE-api.md          # API endpoints spec
CLAUDE-billing.md      # Payment processing spec
```

**2. Role-Based Split**

```
CLAUDE.md              # Shared conventions
CLAUDE-frontend.md     # UI/UX specifications
CLAUDE-backend.md      # API/database specs
CLAUDE-infra.md        # DevOps/deployment specs
```

**3. Workflow-Based Split**

```
CLAUDE.md              # Daily development rules
CLAUDE-testing.md      # Test specifications
CLAUDE-release.md      # Release process spec
CLAUDE-security.md     # Security requirements
```

### Implementation Pattern

**Main CLAUDE.md** (stays concise):
```markdown
# Project: [NAME]

## Tech Stack
[Core technologies]

## Commands
[Daily commands]

## Rules
[Universal rules]

## Detailed Specs
- Authentication: See @CLAUDE-auth.md
- API Design: See @CLAUDE-api.md
- Testing: See @CLAUDE-testing.md
```

**CLAUDE-auth.md** (focused spec):
```markdown
# Authentication Specification

## Capabilities
- MUST: JWT-based authentication
- MUST: Refresh token rotation
- MUST NOT: Store tokens in localStorage

## API Contract
[Detailed auth endpoints...]

## Security Requirements
[Specific auth security rules...]
```

**Benefits**:
- Claude can reference specific files with `@CLAUDE-auth.md`
- Faster context loading (only relevant specs)
- Easier maintenance (edit one domain without affecting others)
- Better team collaboration (ownership per spec file)

**Source**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Jan 2026)

---

## Operational Boundaries

**Pattern**: Define explicit boundaries for what AI agents should do automatically, ask about, or never touch.

### The Three-Tier System

Traditional specs use binary constraints (MUST/MUST NOT), but operational work requires three levels:

| Tier | Meaning | Claude Code Mapping |
|------|---------|---------------------|
| **Always** | Execute automatically without asking | Auto-accept mode |
| **Ask First** | Get user confirmation before proceeding | Default mode |
| **Never** | Block or require Plan Mode | Plan mode / Hook blocking |

### Operational Boundaries Template

```markdown
## Boundaries

### Always (Auto-accept)
- Run tests after code changes
- Format code with Prettier
- Update imports when moving files
- Fix linting errors
- Add type annotations for untyped code

### Ask First (Confirm)
- Modify database schemas
- Add new dependencies
- Change API contracts
- Refactor >50 lines of code
- Update configuration files

### Never (Block)
- Push to production branch
- Commit secrets or API keys
- Delete data without backup
- Modify CI/CD workflows without review
- Bypass security checks
```

### Mapping to Claude Code Permissions

**Always → Permission Allowlist**:
```json
// In .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm test*)",
      "Bash(npx prettier*)",
      "Bash(npx tsc*)"
    ]
  }
}
```

**Ask First → Default Mode**:
- Standard behavior, prompts for every action
- Use for actions with moderate risk/impact

**Never → Plan Mode + Hooks**:
```bash
# Hook configured via settings.json (PreToolUse event)
#!/bin/bash
if [[ "$TOOL_NAME" == "Bash" ]] && [[ "$INPUT" =~ "git push origin main" ]]; then
  echo "BLOCKED: Direct push to main blocked. Use feature branches."
  exit 2  # Send feedback to Claude (non-zero exit blocks the action)
fi
```

### Decision Framework

Ask yourself for each action:
1. **Can it cause data loss?** → Ask First or Never
2. **Is it reversible with git?** → Maybe Always
3. **Does it affect other developers?** → Ask First
4. **Is it a security risk?** → Never
5. **Is it part of the standard workflow?** → Always

### Example: API Development

```markdown
### Always
- Run unit tests (npm test)
- Validate request schemas
- Generate API documentation
- Check response formats

### Ask First
- Add new API endpoints
- Change existing endpoint signatures
- Modify authentication requirements
- Update rate limiting rules

### Never
- Expose internal endpoints publicly
- Log sensitive user data
- Disable authentication checks
- Remove rate limiting
```

### Maintenance

Review boundaries quarterly:
- **Promote**: Actions that never caused issues (Ask First → Always)
- **Demote**: Actions that caused problems (Always → Ask First)
- **Block**: Repeated mistakes (Ask First → Never)

**Source**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Jan 2026)

---

## Command Spec Template

**Pattern**: Document executable commands with expected outputs and error handling.

### Why Command Specs Matter

Most specs focus on **features** ("build authentication"), but **commands** ("how to test authentication") are equally critical for AI agents.

### Template Structure

```markdown
## Commands

### [Command Category]

**Purpose**: [What this command accomplishes]

#### Command: `[actual command]`
**When**: [Trigger condition]
**Expected Output**: [What success looks like]
**Error Handling**: [What to do on failure]
**Flags**: [Important options]

---
```

### Example: Testing Commands

```markdown
## Commands

### Testing

#### Command: `pnpm test`
**When**: Before every commit, after code changes
**Expected Output**:
- All tests pass (exit code 0)
- Coverage ≥80% (lines, branches, functions)
- No console warnings
**Error Handling**:
- If tests fail → Fix tests, don't skip
- If coverage drops → Add tests for uncovered code
- If warnings appear → Investigate before committing
**Flags**:
- `--coverage`: Generate coverage report
- `--watch`: Run in watch mode for development
- `--silent`: Suppress console output

#### Command: `pnpm test:e2e`
**When**: Before merging to main, in CI pipeline
**Expected Output**:
- All E2E scenarios pass
- Screenshots captured for failures
- Test duration <5 minutes
**Error Handling**:
- If flaky → Investigate race conditions, don't retry blindly
- If timeout → Check network mocks, async handling
- If screenshots differ → Review UI changes deliberately
**Flags**:
- `--headed`: Run with visible browser (debugging)
- `--project chromium`: Test specific browser
```

### Example: Build & Deployment

```markdown
## Commands

### Build

#### Command: `pnpm build`
**When**: Before deployment, in CI pipeline
**Expected Output**:
- Build succeeds (exit code 0)
- Output in `dist/` directory
- No TypeScript errors
- Bundle size <500KB (main chunk)
**Error Handling**:
- If TypeScript errors → Fix types, don't use `@ts-ignore`
- If bundle too large → Analyze with `pnpm analyze`, code-split
- If missing assets → Check public/ directory, update paths
**Flags**:
- `--mode production`: Production optimizations
- `--analyze`: Generate bundle size report

### Deployment

#### Command: `pnpm deploy:staging`
**When**: After PR approval, before production
**Expected Output**:
- Deployment succeeds
- Health check returns 200 OK
- Staging URL: https://staging.example.com
**Error Handling**:
- If health check fails → Rollback automatically
- If database migration fails → Don't proceed, investigate
- If environment vars missing → Check .env.staging, update secrets
**Never**: Run `pnpm deploy:production` manually — use CI/CD only
```

### Example: Database Commands

```markdown
## Commands

### Database

#### Command: `pnpm db:migrate`
**When**: After pulling schema changes, before development
**Expected Output**:
- Migrations applied successfully
- Database schema matches models
- Seed data loaded (development only)
**Error Handling**:
- If migration fails → Check database connection, review SQL
- If conflicts detected → Resolve migrations, don't force
**Never**: Run migrations in production manually — CI/CD only

#### Command: `pnpm db:reset`
**When**: Development only, never in staging/production
**Expected Output**:
- Database dropped and recreated
- All migrations applied
- Seed data loaded
**Error Handling**:
- If production check fails → Abort immediately, verify environment
**Safety**: Requires `NODE_ENV=development` check
```

### Integration with CLAUDE.md

Reference command specs in your main CLAUDE.md:

```markdown
## Commands
- Build: `pnpm build` (see spec for error handling)
- Test: `pnpm test` (must pass before commit)
- Deploy: See CLAUDE-deployment.md for full procedures
```

**Source**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Jan 2026)

---

## Anti-Pattern: Monolithic CLAUDE.md

### The Problem

**Symptom**: Your CLAUDE.md has grown to 300+ lines, mixing feature specs, API contracts, testing requirements, deployment procedures, and team conventions.

**Impact**:
- **Context inefficiency**: Claude loads entire 300 lines for every request, even for simple tasks
- **Slow response time**: Large context = slower processing
- **Reduced accuracy**: Important details get lost in noise
- **Maintenance overhead**: Updating one section requires navigating unrelated content
- **Team friction**: Multiple developers editing same file = merge conflicts

### Real-World Example

**Before** (monolithic):
```markdown
# CLAUDE.md (387 lines)

## Tech Stack
[20 lines]

## Authentication
[45 lines of auth spec]

## API Endpoints
[67 lines of API contracts]

## Database Schema
[52 lines of schema rules]

## Testing
[38 lines of test requirements]

## Deployment
[41 lines of deployment procedures]

## Security Rules
[55 lines of security requirements]

## Team Conventions
[33 lines of coding standards]

## Git Workflow
[28 lines of branching rules]

## Troubleshooting
[8 lines of common issues]
```

**Problem**: Claude loads all 387 lines even when user asks: "Add a new API endpoint for user profile"

**After** (modular):
```
CLAUDE.md (82 lines)          # Core context: tech stack, commands, rules
CLAUDE-auth.md (45 lines)     # Authentication spec only
CLAUDE-api.md (67 lines)      # API contracts only
CLAUDE-database.md (52 lines) # Database schema only
CLAUDE-testing.md (38 lines)  # Test requirements only
CLAUDE-deploy.md (41 lines)   # Deployment procedures only
CLAUDE-security.md (55 lines) # Security requirements only
```

**Benefit**: Claude loads CLAUDE.md (82 lines) + CLAUDE-api.md (67 lines) = 149 lines (61% reduction)

### Split Strategy

**Step 1: Identify Domains**

Look for natural boundaries in your spec:
- Do these sections serve different purposes?
- Would different team members own different sections?
- Are some sections referenced more frequently than others?

**Step 2: Extract to Focused Files**

Move domain-specific content to dedicated files:

```bash
# Keep in CLAUDE.md (always loaded)
- Tech stack (unchanging baseline)
- Daily commands (frequent reference)
- Universal rules (apply to all work)

# Extract to domain files (load on demand)
- Feature specs → CLAUDE-[feature].md
- API contracts → CLAUDE-api.md
- Testing → CLAUDE-testing.md
- Deployment → CLAUDE-deploy.md
```

**Step 3: Create Index in Main CLAUDE.md**

```markdown
# Project: [NAME]

## Tech Stack
[Core technologies]

## Commands
[Daily commands]

## Rules
[Universal rules]

## Detailed Specifications
Reference these files for domain-specific requirements:
- @CLAUDE-auth.md — Authentication & authorization
- @CLAUDE-api.md — API endpoint contracts
- @CLAUDE-database.md — Schema and migrations
- @CLAUDE-testing.md — Test requirements
- @CLAUDE-deploy.md — Deployment procedures
- @CLAUDE-security.md — Security requirements
```

**Step 4: Reference When Needed**

Claude can reference specific files:
```
User: "Add a new API endpoint for user settings"
Claude: Reads CLAUDE.md + @CLAUDE-api.md (relevant context only)
```

### Maintenance Rules

1. **Keep CLAUDE.md <100 lines** (core context only)
2. **Domain files <150 lines each** (if bigger, split further)
3. **Review quarterly**: Merge rarely-used files, split frequently-updated sections
4. **Use @file references**: Explicitly load what you need

### Migration Checklist

- [ ] Identify domains in current CLAUDE.md (>200 lines?)
- [ ] Create domain-specific files (CLAUDE-[domain].md)
- [ ] Move content to focused files
- [ ] Update main CLAUDE.md with index/references
- [ ] Test: Ask Claude to perform domain-specific task
- [ ] Verify: Check context usage with `/status`
- [ ] Document: Update team on new structure

**Source**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Jan 2026)

---

## See Also

- [../core/methodologies.md](../core/methodologies.md) — SDD and other methodologies
- [Spec Kit Documentation](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [OpenSpec Documentation](https://github.com/Fission-AI/OpenSpec)
- [tdd-with-claude.md](./tdd-with-claude.md) — Combine with TDD
- [Spec-to-Code Factory](https://github.com/SylvainChabaud/spec-to-code-factory) — Implémentation référence complète avec enforcement outillé (6 gates via Node.js, invariants "No Spec No Code" + "No Task No Commit", ~900K tokens/projet)
