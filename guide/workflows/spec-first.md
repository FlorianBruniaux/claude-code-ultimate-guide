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

### Feature List: Machine-Readable Scope Control

A feature list is a JSON file that tracks scope and completion state per feature across agent sessions. Unlike a PRD, which describes intent, a feature list is the agent's operational contract: it gets read at session start, updated at session end, and persists across handoffs.

Each feature entry has three required fields. The `description` tells the agent what to build. The `verify` field is a shell command that exits 0 on success, and this matters because it forces the definition of done to be executable, not just descriptive. The `status` field tracks progress through a one-way state machine: `not_started` → `active` → `blocked` → `passing`. An entry can only move forward, never backward. When a feature reaches `passing`, an `evidence` field records what proved it (a test name, command output, or a specific log line).

The WIP=1 rule applies here: only one feature can be in `active` state at any time. Multiple active features lead to partial work and incomplete verification across all of them.

Store `feature_list.json` in the project root alongside `AGENTS.md`. At session start, the agent reads it to know what was done and what to pick next. At session end, the agent writes the updated state and evidence before committing.

The feature list works alongside `claudedocs/handoffs/`. Together, these two artifacts give the next session both the operational state (which features are done and verified) and the narrative context (what happened, what was tried, what is left open). Neither replaces the other.

A minimal example showing two features at different stages:

```json
{
  "features": [
    {
      "id": "feat-001",
      "name": "Document Import",
      "description": "Allow users to import PDF and TXT files from local filesystem",
      "verify": "npm test -- --grep 'document import'",
      "status": "passing",
      "evidence": "npm test: 12 passed, 0 failed (2026-05-01 14:22)"
    },
    {
      "id": "feat-002",
      "name": "Document Chunking",
      "description": "Split imported documents into ~500-character chunks with metadata",
      "verify": "npm test -- --grep 'chunking'",
      "status": "not_started",
      "evidence": "",
      "dependencies": ["feat-001"]
    }
  ]
}
```

The `evidence` field on `feat-001` shows exactly what ran and when. The `feat-002` entry is `not_started` with an empty `evidence` field, waiting for `feat-001` to be confirmed passing before it becomes `active`. This pattern is described in the Anthropic engineering blog post on [harness design for long-running applications](https://www.anthropic.com/engineering/harness-design-long-running-apps). A ready-to-use template is available at `examples/workflows/feature-list.json`.

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

### With BMAD-METHOD (Multi-Role Planning)

BMAD-METHOD ([bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD), 50,000+ stars) takes spec-first further: instead of one agent writing one plan, it runs 19+ role-specific agents (Analyst, PM, Architect, Dev, QA) through a planning chain, each producing a versioned artifact (Project Brief, PRD, Architecture Doc, UX spec) before a human signs off and any code gets written.

```bash
npx bmad-method install

# Planning tracks scale to task size
# Quick Flow Track: bug fixes, small features
# BMad Method Track: full PRD + Architecture + UX
# Enterprise Method Track: extended compliance requirements
```

Use it when the task benefits from separating "what to build" (PM), "how to build it" (Architect), and "how it should feel" (UX) into distinct, reviewable documents, rather than one combined plan. It does not provide isolated parallel execution on its own, pair it with git worktrees or spec-kitty (below) if you also need that.

For the strategic case (when BMAD's governance overhead pays off versus when it doesn't) see [methodologies.md § Tier 1: Strategic Orchestration](../core/methodologies.md#tier-1-strategic-orchestration).

### With Spec-Kitty (Isolated Parallel Execution)

Spec-kitty ([Priivacy-ai/spec-kitty](https://github.com/Priivacy-ai/spec-kitty), MIT) adds the piece Spec Kit and BMAD-METHOD leave out: each work package runs in its own git worktree, with a local kanban dashboard tracking the `next → review → accept → merge` loop and an audit trail of every merge decision. Smaller community than Spec Kit or BMAD-METHOD (under 1,500 stars as of July 2026), but it is the most direct open source implementation of "isolated agents, human-gated merge" available today.

```bash
pipx install spec-kitty-cli
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

## SDD vs TDD vs BDD

As of 2026, spec-driven development has productized enough to compare it meaningfully against the older methodologies. The distinction is not which is better in the abstract — it is which artifact governs.

| Methodology | Governing artifact | When it runs | Human role | Regen possible? |
|-------------|-------------------|--------------|------------|-----------------|
| TDD | Test suite | After code exists | Write tests first, then code | No — tests document what was built |
| BDD | Gherkin (.feature files) | After code exists | Write scenarios, then automate | Partial — scenarios can drive codegen |
| SDD | Spec file (natural language structured) | Before code exists | Write spec, approve contract | Yes — code is a derivable output of the spec |

The practical implication of the SDD column: if the spec is the governing artifact, then code is in principle regenerable from the spec. Tessl takes this to the logical extreme with files marked `// GENERATED FROM SPEC - DO NOT EDIT`. Martin Fowler notes this is "spec-first" (code starts from spec) but not yet "spec-anchored" (spec and code stay synchronized automatically over time). No tool has solved spec drift reliably at production scale.

Multi-file task failure rate without spec structure: pass@1 drops to 19.4% for multi-file infrastructure tasks versus 87% for isolated functions (Augment Code internal data, no published peer-reviewed study). The directional claim is credible — agents without persistent task context fail more often on tasks that span files and components. The specific numbers are vendor-sourced.

### Factory.ai Missions architecture

The most documented multi-agent SDD implementation in production. Architecture:

1. **Orchestrator** translates requirements into behavioral validation contracts before any implementation begins.
2. **Workers** implement features in parallel, each receiving a bounded task description from the contract.
3. **Validator agents** (adversarial, independent) verify each implementation against the contract. They have no context from the workers — only the contract and the output.

On a documented Slack clone project: validators caught 81 problems before any code merged, generating 34% of the total implementation work as "fix features." Median mission duration: 2 hours. The longest documented mission: 16 days. Factory.ai externalizes state in shared artifacts (validation contracts, feature lists, skill definitions) to survive context resets across multi-day missions.

CLI reference (when using Factory.ai):

```bash
droid exec --mission path/to/mission.yaml    # Start a mission
droid status                                  # Check active missions
droid validate --mission-id <id>             # Run validators manually
```

### Full-cycle AI software factories

A distinct product category emerged through 2026: commercial platforms that run the entire spec-to-deploy cycle behind a single interface, rather than a tool you drop into an existing workflow. The pitch is close to Factory.ai's Missions architecture above (spec → parallel isolated build → validation → deploy) but packaged as a managed service, often targeting non-developers as the primary user.

| Product | What it does | Funding / stage | Source |
|---------|--------------|------------------|--------|
| [Maleus](https://maleus.ai) | User describes a need in natural language, a team of specialized agents turns it into specs for human approval, then delivers a working app the customer owns on their own repository and infrastructure | Early stage, Paris-based, founder Adrien Maret | [maleus.ai](https://maleus.ai) |
| [Factory.ai](https://factory.ai) | Covered above (Missions architecture) | $150M Series C, $1.5B valuation, led by Khosla Ventures with Sequoia (April 2026) | [TechCrunch](https://techcrunch.com/2026/04/16/factory-hits-1-5b-valuation-to-build-ai-coding-for-enterprises/) |
| [Blitzy](https://blitzy.com) | Reverse-engineers an existing codebase into a dependency graph, then coordinates thousands of agents in parallel for multi-day runs (1M to 100M+ line codebases) | $200M raised, $1.4B valuation, led by Northzone (May 2026) | [SiliconANGLE](https://siliconangle.com/2026/05/05/blitzy-raises-200m-1-4b-valuation-deploy-thousands-coding-agents-parallel/) |
| [Devin](https://devin.ai) (Cognition) | Covered in [agentic-tools.md §2.1](../ecosystem/agentic-tools.md#21-devin-cognition) | $25B valuation (April 2026 fundraise) | See agentic-tools.md |

None of these cover the full governance stack end to end. The gap between "generates a working app fast" and "generates an app you can trust in production without a human re-reading every line" comes down to four questions worth asking before adopting any of them:

1. **Deterministic gate, or LLM self-grading?** Does a separate, non-LLM process (lint, type check, test suite, contract validation) block the merge, or does the agent that wrote the code also decide if it's correct? Factory.ai's independent validator agents (above) and the Spec-to-Code Factory reference implementation (see "See Also" below) are the two documented examples of a hard gate distinct from the generating agent. The strongest empirical case for this comes from security research, not vendor decks: *Refute-or-Promote* ([arXiv:2604.19049](https://arxiv.org/abs/2604.19049), Abhinav Agarwal, 2026) ran a 31-day adversarial multi-agent defect-discovery campaign where agents were assigned to refute candidates rather than confirm them, with a mandatory empirical validation gate (proof-of-concept execution) before any finding reached a human. It killed roughly 79% of 171 candidates and still produced four real CVEs. The result that matters here: ten dedicated LLM reviewers unanimously endorsed a Bleichenbacher padding oracle that did not exist, caught only by the empirical gate. Consensus among LLM reviewers is not a substitute for a deterministic check, it can be confidently, unanimously wrong.
2. **Is there a stop-the-line mechanism?** After N failed remediation attempts, does the pipeline halt and escalate to a human, or does it keep retrying and burning tokens? Few platforms document this explicitly; treat its absence as a real production risk, not an edge case.
3. **Is every decision traceable?** Can you reconstruct, after the fact, which agent (and which model version) made a given change, and whether a human approved it? This matters most in regulated environments and matches the audit-trail pattern spec-kitty implements at the OSS scale (above).
4. **Does the spec stay authoritative after the first generation?** See "Spec drift" immediately below: most platforms solve generation, few solve keeping the spec and the code in sync as the app evolves past its first version.

The commercial products above are closed and managed, so you take their governance on trust. One open source project answers the first three questions in the open: [Liza](https://github.com/liza-mas/liza) (Apache-2.0, 320 stars, single-author as of July 2026) wraps coding-agent CLIs in deterministic Go supervisors that enforce state transitions, role boundaries, merge authority, and TDD gates mechanically rather than by prompt, pairs a doer agent with an adversarial reviewer on every task, records all state on an auditable YAML "blackboard", and ships a circuit breaker that triggers a checkpoint on detected loops or repeated failures, the stop-the-line mechanism of question 2 made explicit. Adoption is tiny and it is not production-proven beyond its author's own use, so treat it as a reference architecture for what mechanical (not prompt-level) governance looks like, not as a dependency to adopt. Its behavioral-contract idea (55+ documented LLM failure modes, each mapped to a countermeasure) is the same "non-overridable rules injected into every agent" pattern that governance-first commercial platforms describe. Full evaluation: [`docs/resource-evaluations/liza-mas-framework.md`](../../docs/resource-evaluations/liza-mas-framework.md).

#### The consultancy-backed factory: a second cohort

The table above is all venture-funded startups, which made the category look narrower than it is. A distinct cohort emerged through the first half of 2026: established consultancies packaging their own agentic platform as a product rather than selling day rates on top of someone else's tools. The pitch inverts the startup one. Where Blitzy leads with thousands of parallel agents and Devin leads with autonomy, this cohort leads with governance and sells velocity second.

| Platform | Parent | What it claims to do | First-hand check |
|----------|--------|---------------------|------------------|
| [AI/works](https://www.thoughtworks.com/ai/works/) | Thoughtworks | AI-assisted reverse engineering of legacy systems into enriched specifications, then agentic workflows generating code, tests and deployment pipelines, regenerating affected components when requirements change. Markets a "3-3-3" model: 3 days to concept, 3 weeks to prototype, 3 months to MVP in production | Launched January 2026 ([press release](https://www.prnewswire.com/news-releases/aiworks-heralds-a-new-era-of-agile-and-next-generation-software-development-302664456.html)), product page read |
| [Agent/works](https://www.thoughtworks.com/en-us/about-us/news/2026/thoughtworks-launches-agent-works) | Thoughtworks | A control plane and governed runtime for enterprise agents on any cloud: central registry, capability-based and time-limited permissions, and "provable compliance before execution" (analyzing every possible path through an agent workflow to verify at least one fully compliant path exists) | Launched June 16, 2026, announced at the Databricks Data + AI Summit. AI/works runs on it |
| [Solario](https://solario.io/en/) | Joint initiative with WeScale (Paris) | Eight domain agents (Architecture, Design, Coding, Security, Testing, Modernization, Operations, Governance), positioned "Context Before Code. Governance Before Scale". Sold either as full modernization programs or as a framework licensed to client teams | Site read July 2026. **No mechanism documented**: no underlying LLM disclosed, no deployment model, no pricing, no named customer |
| IAKA / Autonyx | Sopra Steria | Sovereign multi-agent platform for critical environments (defense, energy), claiming traceability, explainability and verifiability at each step, with European data residency and on-prem deployment | Reported, not independently verified for this guide |
| AI Refinery Distiller | Accenture (with NVIDIA) | Agentic framework covering agent memory, multi-agent collaboration, workflow management, governance and observability | Reported, not independently verified for this guide |

The "provable compliance before execution" claim from Agent/works is the one worth watching. If it does what the wording says, it is closer to model checking than to prompt-level governance, and it would be the only mechanical answer to question 3 in this cohort. Treat it as a claim until someone publishes how the path analysis actually works.

Everything else here fails the same test as the startups, and Solario fails it hardest. A platform whose entire positioning is "Governance Before Scale" publishes not one sentence on how its guardrails are enforced, whether a deterministic gate blocks a merge or an LLM grades its own output, or which model sits underneath. That is not a small omission for this category; it is the whole product. Apply question 5 below before signing: ask for the runtime entry point that enforces the gate, not the slide that names it.

None of the five has a production deployment with measured outcomes verified by a third party, which is the same evidentiary position as every startup in the table above.

#### The decorative-CI trap (question 1, in practice)

The most common way question 1 fails is not "no gate at all". It is a gate that runs but does not block. A team wires up a full CI pipeline (typecheck, tests, lint, secret scan), sees the red X appear on failing PRs, and assumes the merge is protected. It is not, unless those jobs are configured as *required status checks* on the protected branch. Without that, GitHub shows the failure and still lets you merge straight over it. The pipeline is decorative: it reports, it does not gate.

This was found live on a real T3 (tRPC/Prisma) codebase during a harness audit: `gh api repos/OWNER/REPO/branches/BRANCH/protection` returned `404 Branch not protected`, so `ci.yml`, the `pre-push` husky hook, and even an LLM review workflow were all advisory. The fix is a 30-minute GitHub settings change, but it is the single highest-ROI move in the whole harness, because every other gate is theater until it lands.

Two field caveats when you close this gap:

- **Aggregate before you require.** If your CI jobs use `paths-ignore` (so a docs-only PR skips them), marking those jobs directly as required status checks backfires: the check stays permanently "expected" and never satisfies, blocking the PR forever. Add one aggregator "gate" job that depends on the real jobs and exits 0 on the ignored paths, then require only that aggregator.
- **Deterministic blocker, LLM advisory.** A workflow that does `exit 1` when an LLM-filled table has any RED row is still LLM self-grading, just parsed deterministically. Keep the LLM review as a signal, but let the deterministic jobs (typecheck, tests) hold the merge authority. A PR with a red LLM table but green tests should be mergeable; a PR with broken types and a green LLM verdict should not.

### Spec drift: the open problem

The risk that matters most in production: when the spec and the code diverge, agents regenerate bugs that were already fixed. Mitigation patterns:

- Version the spec as a git artifact before any implementation commit.
- Cursor `/evolve` command: updates the spec when the implementation intentionally departs from it.
- Intent (agent): writes changes back to the spec during implementation, keeping both in sync.
- GitHub Spec Kit: stores specs in `.specify/` as versioned files that CI can read.

No tool has a reliable, widely-adopted mechanism for automated spec-code synchronization at long timescales. This is the primary open problem in SDD as of May 2026.

---

## See Also

- [workflows/agentic-software-factories.md](./agentic-software-factories.md): orientation map covering the full spectrum from a single session to a closed platform, plus the decision tree for when a closed factory actually beats the native stack
- [../core/methodologies.md](../core/methodologies.md) — SDD and other methodologies
- [Spec Kit Documentation](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [OpenSpec Documentation](https://github.com/Fission-AI/OpenSpec)
- [tdd-with-claude.md](./tdd-with-claude.md) — Combine with TDD
- [Spec-to-Code Factory](https://github.com/SylvainChabaud/spec-to-code-factory) — Implémentation référence complète avec enforcement outillé (6 gates via Node.js, invariants "No Spec No Code" + "No Task No Commit", ~900K tokens/projet)
- [Superpowers](https://github.com/obra/superpowers) — Plugin suite (95k+ stars) with a `brainstorming` skill that enforces spec-first as a mandatory gate: the agent refuses to write code until a spec has been reviewed and approved. Install: `/plugin install superpowers@claude-plugins-official`.
