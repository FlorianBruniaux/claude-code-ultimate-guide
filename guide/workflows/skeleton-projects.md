---
title: "Skeleton Projects Workflow"
description: "Use existing battle-tested repositories as scaffolding for new projects"
tags: [workflow, architecture, template]
---

# Skeleton Projects Workflow

Use existing, battle-tested repositories as scaffolding for new projects instead of starting from scratch.

---

## When to Use

- **Starting a new project** with known technology stack
- **Standardizing team patterns** across multiple services
- **Rapid prototyping** where architecture decisions are already made
- **Onboarding** new team members via a working reference

**Don't use when**: Exploring unknown tech (use [Vibe Coding](../ultimate-guide.md#98-vibe-coding--skeleton-projects) instead), or when requirements are too unique for existing templates.

---

## Prerequisites

- Claude Code installed and configured
- Git access to reference repositories
- Clear understanding of target project requirements

---

## Step-by-Step Guide

### Phase 1: Find and Evaluate a Skeleton

Don't build from zero. Find an existing repo that matches your target architecture.

**Step 1: Search for candidates**

```bash
# Ask Claude to help find reference repos
claude -p "I need a skeleton for a Next.js 15 app with:
- App Router
- Prisma ORM with PostgreSQL
- tRPC for type-safe API
- Tailwind CSS
- Jest + Playwright testing

Search GitHub for well-maintained starter templates.
Evaluate the top 3 by: last commit date, stars, dependency freshness, test coverage."
```

**Step 2: Clone and audit**

```bash
git clone <candidate-repo> skeleton-eval
cd skeleton-eval
claude
```

```markdown
User: Audit this repository as a potential skeleton for our project:
1. List all dependencies and their versions (flag outdated ones)
2. Assess code quality: patterns, consistency, test coverage
3. Identify what we'd keep vs. what we'd remove
4. Flag any security concerns (vulnerable deps, exposed secrets)
5. Rate overall suitability (1-5) with specific justification
```

**Step 3: Evaluate with sub-agents** (for thorough analysis)

```markdown
User: Run a multi-perspective evaluation of this skeleton:

Agent 1 (Security): Check for vulnerabilities, hardcoded secrets, unsafe patterns
Agent 2 (Architecture): Assess modularity, separation of concerns, scalability
Agent 3 (DX): Evaluate developer experience - setup time, documentation, tooling

Synthesize findings into a go/no-go recommendation.
```

### Phase 2: Fork and Customize

**Step 4: Create your project from the skeleton**

```bash
# Create new repo from skeleton
mkdir my-project
cp -r skeleton-eval/. my-project/
cd my-project
rm -rf .git
git init
```

**Step 5: Strip and adapt with Claude**

```markdown
User: Customize this skeleton for our project "Acme Dashboard":

1. Remove: example routes, demo data, sample tests
2. Keep: config structure, auth setup, database schema pattern, CI pipeline
3. Update: package.json (name, description, version 0.1.0)
4. Add: our CLAUDE.md with project conventions
5. Verify: `pnpm install && pnpm build && pnpm test` all pass after changes

Important: Don't break the working skeleton. Each removal should be followed
by a build check.
```

### Phase 3: Expand from Skeleton to MVP

**Step 6: Build the first real feature**

```markdown
User: Using the patterns established in this skeleton, implement our first feature:
User Authentication (login + registration + password reset)

Follow the skeleton's existing patterns for:
- Route structure (match the example routes pattern)
- Service layer (match the existing service pattern)
- Test structure (match the example test pattern)
- Error handling (match the existing error pattern)

Create a task plan before starting implementation.
```

**Step 7: Validate skeleton integrity**

```markdown
User: Now that we have one real feature, verify the skeleton still works:
1. Run full test suite
2. Check that the CI pipeline passes
3. Verify no skeleton patterns were broken
4. Confirm new code follows skeleton conventions consistently
```

### Phase 4: Document and Iterate

**Step 8: Document decisions in CLAUDE.md**

```markdown
User: Update CLAUDE.md with:
1. Which skeleton we started from (repo URL, commit hash)
2. What we kept and why
3. What we removed and why
4. Any pattern deviations from the original skeleton
5. Conventions we've added on top
```

---

## Skeleton Expansion Timeline

```
Skeleton (Day 1)     →    MVP (Week 1)      →    Production (Month 1)
──────────────────────────────────────────────────────────────────────
1 example route      →    5 real routes      →    20+ routes
1 example test       →    30 tests           →    200+ tests
Basic config         →    Env-based config   →    Multi-env + secrets
SQLite/local DB      →    Docker PostgreSQL  →    Managed DB + migrations
No CI                →    Basic CI           →    Full CI/CD pipeline
README only          →    CLAUDE.md + ADRs   →    Full documentation
```

---

## Real-World Example: Microservice from Skeleton

```bash
# 1. Clone proven skeleton
git clone https://github.com/example/express-prisma-starter skeleton
cd skeleton && claude

# 2. Audit (2 minutes)
User: "Audit this skeleton. Is it suitable for a billing microservice?"
# Claude: Reports deps, patterns, suitability score

# 3. Customize (5 minutes)
User: "Strip examples, rename to billing-service, add our CLAUDE.md"
# Claude: Removes demo code, updates config, adds project context

# 4. First feature (30 minutes)
User: "Implement invoice creation endpoint following skeleton patterns"
# Claude: Creates route, service, repo, tests matching skeleton conventions

# 5. Verify (2 minutes)
User: "Run all tests, verify build, check skeleton patterns preserved"
# Claude: All green, patterns consistent
```

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Skeleton too complex | Spending more time stripping than building | Choose simpler skeleton, or build minimal one yourself |
| Outdated dependencies | Security warnings on install | Check last commit date before cloning (< 6 months ideal) |
| Breaking skeleton patterns | New code diverges from skeleton conventions | Add skeleton patterns to CLAUDE.md as constraints |
| Keeping dead code | Unused example code cluttering the project | Strip ruthlessly in Phase 2, verify build after each removal |
| No documentation | Forgetting why skeleton was chosen | Document in CLAUDE.md immediately (Phase 4) |

---

## Related Workflows

- **[Vibe Coding](../ultimate-guide.md#98-vibe-coding--skeleton-projects)**: Explore before choosing a skeleton
- **[Plan-Driven Development](./plan-driven.md)**: Plan skeleton customization before executing
- **[TDD with Claude](./tdd-with-claude.md)**: Test-first expansion of skeleton features
- **[Permutation Frameworks](../ultimate-guide.md#919-permutation-frameworks)**: Test multiple skeleton variants before committing

---

**Last updated**: January 2026
