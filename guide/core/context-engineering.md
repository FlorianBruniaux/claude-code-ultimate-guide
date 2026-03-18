---
title: "Context Engineering"
description: "Comprehensive guide to filling Claude's context window with the right information at the right time — configuration hierarchy, budget management, modular architecture, team assembly, and quality measurement"
tags: [context, configuration, architecture, team, advanced]
---

# Context Engineering

> **Confidence**: Tier 1 — Based on official documentation, measured production data, and community validation.
>
> **Last updated**: March 2026

"Context engineering is the art of filling the context window with the right information at the right time." — Andrej Karpathy

This guide covers everything from the token math behind context budgets to building modular, team-scale configuration systems. It is a companion to the broader configuration sections in the ultimate guide — where those sections show individual techniques, this document shows how to compose them into a coherent system.

---

## Table of Contents

1. [What is Context Engineering](#1-what-is-context-engineering)
2. [The Context Budget](#2-the-context-budget)
3. [Configuration Hierarchy](#3-configuration-hierarchy)
4. [Modular Architecture](#4-modular-architecture)
5. [Team Assembly](#5-team-assembly)
6. [Context Lifecycle](#6-context-lifecycle)
7. [Quality Measurement](#7-quality-measurement)
8. [Context Reduction Techniques](#8-context-reduction-techniques)
9. [Maturity Assessment](#9-maturity-assessment)

---

## 1. What is Context Engineering

### The Definition

Andrej Karpathy coined the phrase: **"Context engineering is the art of filling the context window with the right information at the right time."**

That single sentence contains three non-obvious requirements:

- **Filling**: the context window should be populated deliberately, not accidentally. Leaving it mostly empty wastes the model's capacity; leaving it chaotically full wastes your tokens and degrades output quality.
- **Right information**: not all information is equal. Architecture decisions are more valuable than linting preferences. Negative constraints ("never return raw SQL errors to the client") are more actionable than aspirational goals ("write clean code").
- **Right time**: path-scoped rules for backend code have no value when editing a frontend component. Loading everything always is the lazy approach that degrades adherence.

### Prompt Engineering vs. Context Engineering

These terms are often conflated. The distinction matters:

| Dimension | Prompt Engineering | Context Engineering |
|-----------|-------------------|---------------------|
| Scope | One request | Entire session or system |
| Duration | Single interaction | Persistent across interactions |
| Effort | Per-request crafting | Upfront system design |
| Scale | Individual | Team-wide or organization-wide |
| Artifact | A prompt string | A configuration system |

**Prompt engineering** is about crafting the right question for one task. **Context engineering** is the system that ensures Claude has the right background knowledge before any task begins. You can have excellent prompts on top of poor context engineering and still get mediocre results — because the model lacks the structural understanding of your project, conventions, and constraints.

A practical analogy: prompt engineering is writing a good email to a contractor. Context engineering is the onboarding process, code style guide, architecture documentation, and team norms that ensure the contractor understands the project before reading a single email.

### Why It Matters

LLMs are context-window computers. The quality of output is bounded by the quality of input. This is not a soft claim — it has a hard technical basis:

1. The model has no persistent memory between sessions (without explicit tooling). Every session starts from zero unless context is deliberately provided.
2. The model cannot infer unstated conventions. If you want TypeScript interfaces instead of `type` aliases, that must be stated. If you want errors logged before being thrown, that must be stated.
3. Models are sensitive to instruction placement and framing. An instruction buried in line 400 of a 500-line CLAUDE.md is less likely to be followed than one in the first 50 lines.

Teams that invest in context engineering consistently report fewer revision cycles, better adherence to conventions, and more predictable outputs. The investment is front-loaded (building the system), but the returns compound across every interaction.

A useful diagnostic reframe: **most AI output failures are context failures, not model failures.** When Claude generates a generic response, ignores a convention, or produces code that doesn't match your stack, the model is almost never broken — the context it received was incomplete, contradictory, or missing the right information at the right time. This reframe shifts troubleshooting from "the AI is bad at this" to "what is missing from the context?"

### The Three Layers

Context engineering in Claude Code operates across three distinct layers:

| Layer | Mechanism | Scope | When Loaded |
|-------|-----------|-------|-------------|
| **Global config** | `~/.claude/CLAUDE.md` | All projects | Always |
| **Project config** | `./CLAUDE.md` + path-scoped modules | Current project | Per session |
| **Session** | Inline instructions, `/add`, flags | Current session only | Runtime |

Each layer has different tradeoffs. Global config is always-on but cannot reference project-specific details. Session instructions are flexible but ephemeral. Project config is the workhorse: structured, versioned, reviewable.

Good context engineering means putting each piece of information in the right layer — not cramming everything into one file, and not leaving critical knowledge in the session layer where it evaporates after every conversation.

### Static vs. Dynamic Context

The three-layer system above is *static context* — configuration files that are assembled before a session begins and remain stable throughout. Claude Code is primarily a static context system, which is why CLAUDE.md structure and path-scoping matter so much.

As you move toward agent workflows, a second category appears: *dynamic context*, assembled at inference time as the agent operates.

| Type | How assembled | Examples in Claude Code |
|------|--------------|-------------------------|
| **Static** | Before session, from files | CLAUDE.md, path-scoped modules, skills |
| **Dynamic** | At runtime, from tools | Tool outputs, file reads, web fetches, MCP data |

In practice, every Claude Code session uses both. The static context (your configuration) sets the behavioral envelope; the dynamic context (files Claude reads, tool results it processes) provides the specific information for each task. Context engineering covers both, but the failure modes differ: static context problems manifest as consistent convention violations; dynamic context problems manifest as Claude acting on stale or incomplete information mid-task.

For teams building automated pipelines and agents, Anthropic's September 2025 engineering post ["Effective context engineering for AI agents"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) covers the dynamic side in depth.

---

## 2. The Context Budget

### Token Math

A concrete baseline for a mid-size project:

| Source | Typical Token Range |
|--------|---------------------|
| Global CLAUDE.md | 1,000 – 3,000 tokens |
| Project CLAUDE.md (root) | 2,000 – 8,000 tokens |
| Path-scoped modules (all active) | 1,000 – 5,000 tokens |
| Imported skills / commands | 500 – 3,000 tokens |
| **Total always-on context** | **~5,000 – 20,000 tokens** |

Claude Sonnet 4.6 has a 200K token context window. That means even a large always-on configuration budget (20K tokens) occupies about 10% of the window — leaving 180K tokens for actual work: code files, conversation history, tool outputs.

The practical rule: **always-on context should stay below 5% of the context window.** Beyond that, you are displacing actual task content, which matters more per token than standing instructions.

### The 150-Instruction Ceiling

Empirical observation from teams running large CLAUDE.md files: beyond approximately 150 distinct rules, models begin selectively ignoring some of them. This is not a hard cutoff — it depends on rule complexity, overlap, and placement — but it is a reliable signal that more rules does not equal better adherence.

The mechanism is attention diffusion: when a prompt contains hundreds of potentially relevant constraints, the model's attention is split across them. High-salience rules (recent, strongly worded, placed early) crowd out lower-salience ones.

HumanLayer's production data shows teams with structured context — fewer, more specific rules, organized hierarchically — see 15-25% better adherence than teams with undifferentiated long rule lists.

Implication: **rule quality beats rule quantity.** Twenty specific, actionable rules outperform 200 generic aspirational ones.

### Adherence Degradation by File Size

```
Lines in CLAUDE.md    Adherence (estimated)
─────────────────     ─────────────────────
1 – 100               ~95%
100 – 200             ~88%
200 – 400             ~75%
400 – 600             ~60%
600+                  ~45% and falling
```

These are estimated baselines, not guarantees. Path-scoping and modular architecture can maintain higher adherence at larger total rule counts by ensuring that only relevant rules are in context at any given time.

### Signs of Context Overload

When always-on context becomes too large or too noisy, you see predictable failure modes:

- **Rule silencing**: Claude follows 80% of conventions consistently but ignores specific rules that should apply.
- **Contradictory behavior**: Claude applies a rule in some files but not others, or applies contradictory rules depending on phrasing.
- **Slow first responses**: The model spends more time processing a large context before generating output (observable in longer latency for simple tasks).
- **Generic outputs**: Instead of applying project-specific patterns, Claude falls back to generic best practices — a sign that project context is not being retained.

When you see these patterns, the diagnostic is: run a context audit (see Section 7), not more instructions.

### Path-Scoping and Budget Efficiency

Path-scoping is the most effective single technique for reducing always-on context. Instead of loading all rules for all parts of the codebase, you load only the rules relevant to the files currently in context.

A typical project without path-scoping:

```
Always-on: root CLAUDE.md with backend + frontend + database + API rules = 8,000 tokens
```

The same project with path-scoping:

```
Always-on: root CLAUDE.md with shared rules = 2,000 tokens
Active when in src/api/: api module = +1,500 tokens
Active when in src/components/: frontend module = +1,200 tokens
Active when in prisma/: database module = +800 tokens
```

Result: 40-50% reduction in always-on context, with no loss of coverage. Each subsystem gets its full rule set, but only when working in that subsystem.

---

## 3. Configuration Hierarchy

### The Three-Layer Stack

```
┌──────────────────────────────────────────────┐
│  Global (~/.claude/CLAUDE.md)                │
│  Identity, tone, universal tools, cross-      │
│  project conventions                          │
├──────────────────────────────────────────────┤
│  Project (./CLAUDE.md + path modules)         │
│  Architecture decisions, stack conventions,   │
│  team rules, deployment procedures            │
├──────────────────────────────────────────────┤
│  Session (inline instructions, flags)         │
│  Ad-hoc overrides, experiment constraints,    │
│  one-off task parameters                      │
└──────────────────────────────────────────────┘
```

Later layers override earlier ones. A session instruction can override a project rule; a project rule can override a global default. This gives you escape hatches without requiring permanent changes to shared configuration.

### Global Configuration

**Location**: `~/.claude/CLAUDE.md`

**What belongs here**:
- Identity and communication style preferences
- Universal tool preferences (RTK, preferred CLI tools)
- Cross-project coding conventions (commit message format, PR style)
- Security constraints that apply everywhere
- Tone and output format defaults

**What does not belong here**:
- Project-specific architecture decisions
- Stack-specific rules (React hooks, Prisma patterns)
- Deployment or environment specifics
- Anything that changes per project

**Size target**: Keep global configuration under 200 lines. This is your always-on overhead for every session in every project. Bloating it hurts all projects equally.

```markdown
# Example: Minimal effective global CLAUDE.md

## Communication
- Respond in the same language the user writes in
- Prefer direct answers over preamble
- No em dashes in written output

## Git
- Commit messages: imperative mood, <72 chars subject line
- Never commit without being asked

## Code Style
- Prefer explicit error handling over silent failure
- Add TODO comments only when referencing a tracked issue
```

### Project Configuration

**Location**: `./CLAUDE.md` (project root)

**What belongs here**:
- Technology stack and versions in use
- Architecture decisions and their rationale
- Team conventions specific to this codebase
- File organization patterns
- Testing requirements and coverage targets
- Security constraints specific to this project
- Path-scope imports for subsystem modules

**Structure pattern**:

```markdown
# Project: [Name]

## Stack
- Language: TypeScript 5.3
- Framework: Next.js 14 (App Router)
- Database: PostgreSQL 16 via Prisma
- Testing: Vitest + React Testing Library

## Architecture
- Server Components by default; use `"use client"` only when interactivity requires it
- API routes in /app/api; no business logic in route handlers
- Business logic in /lib/services; each service is a plain function module

## Conventions
- File naming: kebab-case for files, PascalCase for React components
- Error handling: wrap service calls in Result<T, E> pattern (see lib/result.ts)
- Never expose raw database IDs in API responses; use UUIDs

## Path-Scoped Modules
@src/api/CLAUDE-api.md
@src/components/CLAUDE-components.md
@prisma/CLAUDE-db.md
```

### Session Configuration

**Mechanism**: Inline instructions, `/add-dir`, or system prompt flags for the current session.

**What belongs here**:
- One-off task constraints ("For this refactor, do not change the public API surface")
- Experiment parameters ("Use the new error format I'm testing in this file")
- Debug constraints ("Log every tool call for this session")
- Temporary overrides of project conventions

Session instructions are not persisted. They evaporate when the session ends. Any instruction that you find yourself repeating across sessions belongs in the project config, not the session layer.

### Decision Tree: Where Does This Rule Go?

```
Is this rule relevant to every project I work on?
├── Yes → Global CLAUDE.md
└── No ↓

Is this rule relevant to specific files or subsystems?
├── Yes → Path-scoped module (e.g., src/api/CLAUDE-api.md)
└── No ↓

Is this rule relevant to the whole project?
├── Yes → Project CLAUDE.md (root)
└── No ↓

Does this rule apply only to the current task or session?
├── Yes → Inline session instruction
└── No → Revisit: is it really a rule, or just a one-time preference?
```

### Import Chain and Override Semantics

The import chain flows: `global → project root → path-scoped modules → session`.

When conflicts exist:
- More specific overrides less specific (path-scoped beats root, root beats global)
- Later-declared beats earlier-declared at the same level
- Session instructions override all persistent config

**Practical example**: Your global config says "use two-space indentation." Your project config says "use four-space indentation for Python." Your session says "match the existing file style." The session instruction wins for this session, with four-space default for Python files, two-space for everything else.

Document your overrides explicitly. An undocumented override that contradicts a parent rule creates confusion during audits.

---

## 4. Modular Architecture

### The Problem with Monolithic Config

A 600-line CLAUDE.md with no structure is the most common failure mode in production contexts. Symptoms:

1. Rules from different domains mix together — a React component convention sits next to a database migration rule
2. Claude reads all 600 lines but the attention budget means rules on page 5 get less weight than rules on page 1
3. New team members can't find relevant rules quickly
4. Updates require scanning the entire file to find related rules before editing
5. Adherence degrades progressively as the file grows

The fix is architectural: decompose the monolith into focused modules, then use path-scoping to load each module only when relevant.

### Path-Scoping Pattern

**Mechanism**: Claude Code supports `@path/to/file.md` imports in CLAUDE.md. When a path-scoped import is active, rules from that module are added to context only when files under the specified path are in scope.

**File structure**:

```
project/
├── CLAUDE.md                       # Root config, shared rules + @imports
├── src/
│   ├── api/
│   │   └── CLAUDE-api.md           # API-specific rules
│   ├── components/
│   │   └── CLAUDE-components.md    # React/UI-specific rules
│   └── lib/
│       └── CLAUDE-lib.md           # Utility/shared library rules
├── prisma/
│   └── CLAUDE-db.md                # Database and migration rules
└── tests/
    └── CLAUDE-tests.md             # Testing conventions
```

**Root CLAUDE.md with imports**:

```markdown
# Project Config

## Shared Rules
[...shared rules here...]

## Subsystem Modules
@src/api/CLAUDE-api.md
@src/components/CLAUDE-components.md
@src/lib/CLAUDE-lib.md
@prisma/CLAUDE-db.md
@tests/CLAUDE-tests.md
```

**Example path-scoped module** (`src/api/CLAUDE-api.md`):

```markdown
# API Rules

- Route handlers in /app/api only; no business logic inline
- All endpoints must validate input with Zod before processing
- Error responses use the standard format: { error: string, code: string }
- Never log request bodies that may contain PII; log IDs only
- Rate limiting headers must be present on all public endpoints
- Authentication: verify JWT in middleware, not in individual handlers
```

This module's 6 rules are in context only when working in `src/api/`. They do not consume context budget when working in `src/components/`.

### Skills vs. Rules

This distinction is underused and matters:

| Dimension | Rules | Skills |
|-----------|-------|--------|
| Nature | Constraints, standards, conventions | Capabilities, procedures, workflows |
| When active | Always enforced | Invoked on demand |
| Example | "Never use `any` in TypeScript" | "How to add a new API endpoint" |
| Location | CLAUDE.md | `.claude/skills/` |
| Token cost | Always-on | Loaded only when invoked |

**Rules** define what Claude should and should not do by default. They set the boundaries of acceptable output.

**Skills** define how to do complex multi-step tasks that require specific knowledge of your project's patterns. They are loaded when Claude needs to perform a specific type of task, not always.

**Practical example**: A rule says "API endpoints must have Zod validation." A skill says "Here is the step-by-step pattern for creating a new API endpoint in this project, including the Zod schema pattern, the error handling wrapper, the auth middleware hook, and the test file structure."

Putting the endpoint creation procedure in a rule would mean loading 40 lines of procedural instructions for every session, even when you're not creating endpoints. Putting it in a skill means loading those 40 lines only when creating an endpoint.

**Rule**: `Never expose raw database IDs in API responses.`
**Skill**: `How to generate and use UUID-based public identifiers for entities.`

### Progressive Disclosure

The principle: don't load everything upfront. Load what is needed for the task at hand.

**Core config (always-on)**:
- Architecture decisions and their rationale
- Coding standards and naming conventions
- Security constraints
- Tool preferences

**Contextual modules (loaded per task)**:
- Deployment procedures (load when deploying)
- API patterns (load when working in API layer)
- Test templates (load when writing tests)
- Database migration procedures (load when touching schema)

**Implementation pattern using skills**:

```
.claude/
├── skills/
│   ├── deploy-production.md      # Loaded when: "deploy this"
│   ├── add-api-endpoint.md       # Loaded when: "add endpoint for X"
│   ├── write-migration.md        # Loaded when: "add DB column"
│   └── create-component.md      # Loaded when: "create component for X"
```

Each skill file contains the step-by-step procedure with project-specific patterns. Claude loads it when the task type is detected, not proactively.

### Anti-Pattern: The Monolithic CLAUDE.md

**What it looks like**:

```markdown
# CLAUDE.md (600 lines)

## Rules
1. Use TypeScript
2. No any types
3. Run tests before committing
4. API endpoints need auth
5. Use Prisma for DB queries
6. React components in PascalCase
7. Deploy with ./scripts/deploy.sh
8. Check OWASP Top 10 before shipping
[...492 more rules...]
```

**Why it fails**:

- Rules 1-20 get ~95% attention weight; rules 500+ get ~30%
- Frontend dev reads backend DB rules they don't need and vice versa
- No logical grouping means finding relevant rules requires reading everything
- Adding a new rule requires checking the entire file for conflicts
- Adherence degrades continuously as the file grows

**The fix**:

1. Extract rules by domain into path-scoped modules
2. Keep the root CLAUDE.md to shared rules + import declarations
3. Move procedural knowledge to skills
4. Target root CLAUDE.md at under 150 lines after extraction

---

## 5. Team Assembly

### The N × M × P Problem

At team scale, context engineering faces a combinatorial challenge:

- **N developers**: different roles, tools, communication preferences
- **M projects**: different stacks, conventions, deployment targets
- **P configurations**: each developer × each project needs a configuration

Maintaining N × M individual CLAUDE.md files manually is not sustainable. When a shared convention changes, you update N × M files. When a new project is created, you build from scratch. When a developer changes roles, you rebuild their configurations.

The solution is **profile-based assembly**: a single shared base of modules, with individual profiles that specify which modules to include and what personal preferences to overlay.

N × M × P becomes N profiles × 1 shared module base — manageable.

### Profile YAML Structure

Each team member has a profile YAML that declaratively specifies their configuration:

```yaml
# profiles/alice.yaml

profile:
  name: "Alice"
  role: "frontend"
  tools:
    - typescript
    - react
    - tailwind
  conventions:
    - atomic-design
    - accessibility-first
  communication:
    language: "en"
    verbosity: "concise"

modules:
  include:
    - shared/core-rules.md
    - shared/git-conventions.md
    - shared/security-baseline.md
    - frontend/react-patterns.md
    - frontend/tailwind-conventions.md
    - frontend/testing-rtl.md
    - frontend/accessibility-checklist.md
  exclude:
    - backend/database-rules.md
    - backend/api-design.md
    - devops/deployment-procedures.md

overrides:
  - "Prefer named exports over default exports"
  - "Use Radix UI primitives before writing custom components"
```

```yaml
# profiles/bob.yaml

profile:
  name: "Bob"
  role: "backend"
  tools:
    - typescript
    - nodejs
    - postgresql
    - prisma
  communication:
    language: "en"
    verbosity: "detailed"

modules:
  include:
    - shared/core-rules.md
    - shared/git-conventions.md
    - shared/security-baseline.md
    - backend/api-design.md
    - backend/database-rules.md
    - backend/error-handling.md
    - backend/performance-patterns.md
  exclude:
    - frontend/react-patterns.md
    - frontend/tailwind-conventions.md

overrides:
  - "Use structured logging (pino) with request context IDs"
  - "Always measure before optimizing; profile first"
```

### Module Library Structure

The shared module library lives in the repository and is version-controlled:

```
.claude/
├── modules/
│   ├── shared/
│   │   ├── core-rules.md           # Universal team standards
│   │   ├── git-conventions.md      # Commit and PR conventions
│   │   ├── security-baseline.md    # Non-negotiable security rules
│   │   └── testing-standards.md   # Coverage and test quality rules
│   ├── frontend/
│   │   ├── react-patterns.md
│   │   ├── tailwind-conventions.md
│   │   ├── testing-rtl.md
│   │   └── accessibility-checklist.md
│   ├── backend/
│   │   ├── api-design.md
│   │   ├── database-rules.md
│   │   ├── error-handling.md
│   │   └── performance-patterns.md
│   └── devops/
│       ├── deployment-procedures.md
│       ├── monitoring-conventions.md
│       └── infrastructure-rules.md
├── profiles/
│   ├── alice.yaml
│   ├── bob.yaml
│   └── carol.yaml
└── scripts/
    └── assemble-context.sh
```

### Assembly Script

The assembly script reads a profile and concatenates the specified modules into a CLAUDE.md:

```bash
#!/usr/bin/env bash
# scripts/assemble-context.sh

set -euo pipefail

PROFILE="${1:-}"
CHECK_MODE="${2:-}"

if [[ -z "$PROFILE" ]]; then
  echo "Usage: ./assemble-context.sh <profile-name> [--check]"
  exit 1
fi

PROFILE_FILE=".claude/profiles/${PROFILE}.yaml"
OUTPUT_FILE="CLAUDE.md"
MODULES_DIR=".claude/modules"

if [[ ! -f "$PROFILE_FILE" ]]; then
  echo "Profile not found: $PROFILE_FILE"
  exit 1
fi

# Parse profile with yq or python
MODULES=$(python3 -c "
import yaml
with open('$PROFILE_FILE') as f:
    profile = yaml.safe_load(f)
for m in profile['modules']['include']:
    print(m)
")

# Assemble output
ASSEMBLED=$(mktemp)

echo "# Claude Code Configuration" > "$ASSEMBLED"
echo "# Generated from profile: $PROFILE" >> "$ASSEMBLED"
echo "# Generated at: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$ASSEMBLED"
echo "" >> "$ASSEMBLED"

while IFS= read -r module; do
  MODULE_PATH="${MODULES_DIR}/${module}"
  if [[ -f "$MODULE_PATH" ]]; then
    echo "## From: ${module}" >> "$ASSEMBLED"
    cat "$MODULE_PATH" >> "$ASSEMBLED"
    echo "" >> "$ASSEMBLED"
  else
    echo "WARNING: module not found: $MODULE_PATH" >&2
  fi
done <<< "$MODULES"

# Append personal overrides
python3 -c "
import yaml
with open('$PROFILE_FILE') as f:
    profile = yaml.safe_load(f)
overrides = profile.get('overrides', [])
if overrides:
    print('## Personal Overrides')
    for o in overrides:
        print(f'- {o}')
" >> "$ASSEMBLED"

if [[ "$CHECK_MODE" == "--check" ]]; then
  if diff -q "$OUTPUT_FILE" "$ASSEMBLED" > /dev/null 2>&1; then
    echo "OK: CLAUDE.md matches profile $PROFILE"
    rm "$ASSEMBLED"
    exit 0
  else
    echo "DRIFT: CLAUDE.md does not match profile $PROFILE"
    diff "$OUTPUT_FILE" "$ASSEMBLED"
    rm "$ASSEMBLED"
    exit 1
  fi
fi

mv "$ASSEMBLED" "$OUTPUT_FILE"
echo "Assembled CLAUDE.md from profile: $PROFILE"
```

**Usage**:

```bash
# Generate CLAUDE.md from a profile
./scripts/assemble-context.sh alice

# Check for drift (used in CI)
./scripts/assemble-context.sh alice --check
```

### CI Drift Detection

Team members regenerate their CLAUDE.md from profiles, but base modules evolve over time. Without drift detection, a developer may be running an outdated configuration — one that predates a security rule addition or a convention update.

A GitHub Actions job detects this:

```yaml
# .github/workflows/context-drift.yml

name: Context Drift Detection

on:
  schedule:
    - cron: '0 9 * * 1'   # Weekly, Monday 9am UTC
  push:
    paths:
      - '.claude/modules/**'

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: pip install pyyaml

      - name: Check all profiles for drift
        run: |
          DRIFT=0
          for profile_file in .claude/profiles/*.yaml; do
            profile=$(basename "$profile_file" .yaml)
            echo "Checking profile: $profile"
            if ! ./scripts/assemble-context.sh "$profile" --check; then
              echo "DRIFT detected in profile: $profile"
              DRIFT=1
            fi
          done
          exit $DRIFT

      - name: Notify on drift
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Context drift detected — CLAUDE.md needs regeneration',
              body: 'One or more team profiles are out of sync with the current module library. Run `./scripts/assemble-context.sh <profile>` to regenerate.',
              labels: ['context-engineering']
            })
```

### Onboarding with Profiles

For new team members, the onboarding sequence becomes:

```bash
# 1. Copy a starter profile appropriate for your role
cp .claude/profiles/template-frontend.yaml .claude/profiles/yourname.yaml

# 2. Edit the profile for your preferences
vim .claude/profiles/yourname.yaml

# 3. Generate your CLAUDE.md
./scripts/assemble-context.sh yourname

# 4. Verify the output
cat CLAUDE.md

# 5. Commit your profile (not the generated CLAUDE.md — it's gitignored)
git add .claude/profiles/yourname.yaml
git commit -m "chore: add context profile for yourname"
```

Add `CLAUDE.md` to `.gitignore` at the project root. The profile YAML is the source of truth, not the generated file.

---

## 6. Context Lifecycle

### Instruction Debt

Rules accumulate. They are rarely removed. This is instruction debt: the gradual accumulation of rules that are outdated, redundant, or contradictory — each still consuming context budget.

Signs of instruction debt:

- A rule refers to a library you stopped using six months ago
- Two rules say opposite things about the same pattern
- A rule covers an edge case that only applied during a specific migration
- The same constraint is stated three times in different sections
- Developers comment out or ignore specific rules because they conflict with current practice

Instruction debt has compounding costs: each conflicting or irrelevant rule displaces a useful one, and models behave unpredictably when rules conflict.

**Quarterly audit rhythm**: Schedule a context audit every quarter (or after major project milestones). The audit prompt:

```
Review every rule in CLAUDE.md for:
1. Relevance: Does this still apply to the current stack and patterns?
2. Specificity: Is this actionable, or is it too vague to enforce?
3. Conflicts: Does this contradict another rule?
4. Coverage: Is this already covered by a more general rule?

For each rule, classify as: KEEP | UPDATE | ARCHIVE | DELETE
```

Run this as an actual Claude session, feeding the current CLAUDE.md and asking for a structured audit.

### The Update Loop

The most common mistake after a bad Claude output is to fix the output manually and move on. This is a wasted learning opportunity.

**Bad loop**:
```
Claude generates wrong pattern
→ Developer manually fixes it
→ Next session: Claude generates wrong pattern again
→ Developer manually fixes it again
→ Repeat indefinitely
```

**Good loop**:
```
Claude generates wrong pattern
→ Developer identifies the root cause (missing rule? vague rule? conflicting rules?)
→ Developer updates CLAUDE.md with a corrected or new rule
→ Next session: Claude generates correct pattern
→ Rule stays in config permanently
```

The update loop is how your configuration system learns from experience. Each bad output is a signal that something is missing or broken in your context engineering. Treat it as a bug report against CLAUDE.md, not just a one-off failure.

**Practical format for rule updates**:

When adding a rule from a failure, include the rationale inline:

```markdown
- Use the `Result<T, E>` type for service functions, not try/catch
  (Rationale: try/catch at service level hides error types from callers;
   Result forces explicit error handling at the call site)
```

The rationale serves two purposes: it helps future auditors understand why the rule exists, and it gives Claude better context for applying the rule correctly.

### Knowledge Feeding After Sprints

At the end of each sprint or release cycle, run a brief knowledge feeding session:

1. **New patterns**: "We standardized on X approach for Y type of problem in this sprint. Add this to CLAUDE.md."
2. **Anti-patterns discovered**: "We tried X and it caused Y. Add a rule to avoid it."
3. **Architecture decisions**: "We decided to use X over Y because Z. Document this so Claude doesn't suggest Y."
4. **Deprecated patterns**: "We're moving away from X. Add a rule to use Y instead and flag existing X usages."

This keeps the context system current without requiring large periodic overhauls.

### The ACE Pipeline

For teams that run Claude Code in automated or semi-automated workflows, the ACE pipeline provides a structured execution model:

```
Assemble → Check → Execute
```

**Assemble**: Build context from the team profile + project modules. Produces a CLAUDE.md specific to the developer and task context.

**Check**: Run canary validation — a set of 3-5 test prompts that verify key behaviors before the actual task. If canary checks fail, fix the context issue before proceeding.

**Execute**: Run Claude with the validated context on the actual task.

```bash
#!/usr/bin/env bash
# ace.sh — Assemble, Check, Execute

PROFILE="${1:-}"
TASK="${2:-}"

if [[ -z "$PROFILE" || -z "$TASK" ]]; then
  echo "Usage: ./ace.sh <profile> <task-description>"
  exit 1
fi

echo "=== ASSEMBLE ==="
./scripts/assemble-context.sh "$PROFILE"

echo "=== CHECK ==="
./scripts/run-canaries.sh
CANARY_EXIT=$?

if [[ $CANARY_EXIT -ne 0 ]]; then
  echo "Canary checks failed. Fix context issues before executing."
  exit 1
fi

echo "=== EXECUTE ==="
claude "$TASK"
```

### Session Retrospective

At the end of each Claude Code session, before closing, ask:

```
Looking at what we built or changed in this session:
1. What patterns did we use that aren't in CLAUDE.md?
2. What did I have to correct that could become a rule?
3. What decisions did we make that should be documented?

Generate 3-5 candidate rules for CLAUDE.md based on this session.
```

This takes 2-3 minutes and generates concrete improvement candidates. You review them and decide which to add. Over time, this is how configuration systems accumulate genuine project knowledge rather than just generic rules.

---

## 7. Quality Measurement

### Self-Evaluation Questions

Run these questions against your CLAUDE.md periodically (quarterly at minimum):

**Relevance**:
- Does this rule still apply to the current stack, libraries, and team practices?
- Was this rule written for a problem that no longer exists?
- Would a new team member understand why this rule exists?

**Specificity**:
- Is this rule specific enough for Claude to know when it applies?
- Does this rule have at least one concrete example or counter-example?
- Could two developers interpret this rule differently?

**Conflicts**:
- Does this rule contradict another rule in the same file?
- Does this rule contradict a rule in a path-scoped module?
- Does this rule contradict a global rule without explicitly overriding it?

**Coverage**:
- Is this rule a specific case of a more general rule that already exists?
- Is this rule already implied by the architecture decisions stated elsewhere?

A rule that fails more than one of these checks is a candidate for update or removal.

### Canary Checks

Canary checks are simple test prompts that verify Claude follows key conventions. Run them before and after major changes to CLAUDE.md to catch regressions.

**Structure**: 3-5 prompts that are simple enough to answer quickly, but specific enough to reveal adherence failures.

**Example canary set for a React/TypeScript project**:

```bash
# scripts/run-canaries.sh

PASS=0
FAIL=0

check() {
  local name="$1"
  local prompt="$2"
  local expected_pattern="$3"

  result=$(claude "$prompt" --output-format text 2>/dev/null)

  if echo "$result" | grep -qE "$expected_pattern"; then
    echo "PASS: $name"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $name"
    echo "  Expected pattern: $expected_pattern"
    echo "  Got: $(echo "$result" | head -5)"
    FAIL=$((FAIL + 1))
  fi
}

check "TypeScript interfaces" \
  "Generate a React component that accepts a name and age prop" \
  "interface.*Props"

check "Named exports" \
  "Create a utility function that formats a date" \
  "^export (function|const)"

check "No any type" \
  "Write a function that processes user data" \
  "^((?!: any).)*$"

check "Error result type" \
  "Write a service function that fetches user data from an API" \
  "Result<"

echo ""
echo "Canaries: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]]
```

**When to run canaries**:
- Before merging changes to CLAUDE.md
- After adding a new path-scoped module
- When a team member reports unexpected Claude behavior
- As part of the CI drift detection job

### Adherence Tracking

Informal but effective: for each key rule in CLAUDE.md, track how often Claude violates it across 10 consecutive interactions where the rule should apply.

| Rule | Violations / 10 | Status |
|------|----------------|--------|
| TypeScript interfaces for props | 1/10 | Healthy |
| Result type for service functions | 0/10 | Healthy |
| No raw database IDs in API responses | 3/10 | Review rule |
| Structured logging with request context | 5/10 | Rule too vague |
| OWASP Top 10 check before shipping | 8/10 | Not actionable as stated |

Rules with >20% violation rate are broken in one of three ways:
1. Too vague to apply consistently
2. Conflicting with another rule
3. Placed too late in the file to receive enough attention

**Fix for "too vague"**: Add a concrete example of compliance and a counter-example of violation.

**Fix for "conflicting"**: Find the conflict, decide which rule should win, update or remove the losing rule, and add an explicit note.

**Fix for "placed too late"**: Move the rule to the top third of the file, or to a more prominent position in its section.

### Context Debt Score

A single metric for the health of your context engineering system:

```
Context Debt Score = (total_rules / 150) × (conflicts_found / total_rules) × 100
```

Where:
- `total_rules` = count of distinct rules across all loaded config files
- `150` = the approximate attention ceiling
- `conflicts_found` = rules that contradict another rule

| Score Range | Status | Action |
|-------------|--------|--------|
| < 30 | Healthy | Standard quarterly audit |
| 30 – 60 | Degraded | Prune and deduplicate; fix conflicts |
| 60 – 80 | Poor | Major restructure needed |
| > 80 | Critical | Start from scratch with top 30 rules |

**Running the score calculation**:

```bash
# Count rules (approximate: lines starting with -)
TOTAL_RULES=$(grep -c "^- " CLAUDE.md 2>/dev/null || echo 0)

# Count conflicts requires manual review or an LLM audit pass
# Use: claude "Scan CLAUDE.md and count rules that contradict each other. Return the count."

echo "Total rules: $TOTAL_RULES"
echo "Run conflict audit manually or with Claude"
```

### Useful Metrics to Track Over Time

| Metric | How to Measure | Target |
|--------|---------------|--------|
| Always-on context size | `wc -w CLAUDE.md ~/.claude/CLAUDE.md` | < 5,000 words |
| Rule count | `grep -c "^- " CLAUDE.md` | < 150 |
| File age | `git log --follow -p CLAUDE.md | head -20` | Major review every 6 months |
| Violation rate per key rule | Manual spot checks | < 20% violation |
| Canary pass rate | `./scripts/run-canaries.sh` | 100% (all pass) |

---

## 8. Context Reduction Techniques

### Path-Scoping: The Highest-Leverage Technique

Path-scoping reduces always-on context by 40-50% with no loss of coverage. It is the single most impactful structural change for projects beyond ~200 lines of configuration.

Implementation steps:

1. Identify natural domain boundaries in your codebase (API, frontend, database, tests, infrastructure)
2. For each domain, create a `CLAUDE-{domain}.md` file in the domain directory
3. Move domain-specific rules from root CLAUDE.md to the appropriate module
4. Replace moved content in root CLAUDE.md with `@path/to/CLAUDE-domain.md` imports
5. Verify adherence with canary checks

Target after refactor: root CLAUDE.md at under 150 lines (shared rules + import declarations only).

### Negative Constraints

Empirically, negative constraints ("never do X") outperform positive instructions ("do X") by 15-25% for preventing bad patterns. This is counterintuitive — you might expect "do X" to be clearer. But in practice, the model needs to actively resist a temptation to do the wrong thing; explicitly naming the wrong thing and saying "never" is more salient.

| Pattern | Formulation | Adherence |
|---------|-------------|-----------|
| Positive (weaker) | "Use structured logging for all backend services" | ~75% |
| Negative (stronger) | "Never use console.log in backend services; use the structured logger (pino)" | ~90% |

**Technique**: For any rule where the wrong pattern is a common default (raw try/catch, console.log, default exports, any types), frame the rule as a negative constraint naming the specific pattern to avoid.

### Rule Compression

Long explanatory rules consume tokens and dilute attention. Compress explanations to their essence:

**Before** (verbose, 38 words):
```markdown
- When creating React components, always make sure to use TypeScript interfaces
  for props, and define them before the component declaration, not inline, to
  improve readability and enable reuse.
```

**After** (compressed, 9 words):
```markdown
- React props: TypeScript interface, declared before component, never inline.
```

The compressed version has higher adherence — shorter rules are processed with more attention weight per rule. Save explanations for the rationale format when they're truly needed for understanding.

**Compression heuristic**: If a rule takes more than one line, ask whether the extra content is a constraint or an explanation. Move explanations to comments (prefixed with `#` or a `>` blockquote) or rationale annotations. Keep the enforced constraint to one line.

### Deduplication

The same constraint stated multiple times (in different words) does not reinforce it — it dilutes the total attention budget. Find and remove semantic duplicates.

**Common sources of duplication**:
- One rule in a general section, one more specific version in a path-scoped module
- A rule added to fix a problem, without removing the vaguer original rule it supersedes
- Rules copied from different team members' configs during a merge

**Deduplication workflow**:

```
Scan CLAUDE.md for semantic duplicates. Two rules are duplicates if they
constrain the same behavior, even if worded differently. List all duplicate
pairs and recommend which version to keep based on specificity and clarity.
```

Run this as a Claude prompt against your CLAUDE.md. Review the suggestions and merge.

### The Archive Pattern

When removing a rule, you lose the knowledge of why it existed. That institutional memory can be valuable — six months later, someone may try to reintroduce the same pattern the rule was preventing.

Instead of deleting obsolete rules, archive them:

```
.claude/
├── CLAUDE.md              # Active rules
└── CLAUDE-archive.md      # Historical rules with retirement notes
```

**Archive entry format**:

```markdown
## Archived Rules

### [Retired 2026-01] Use MongoDB for session storage
Replaced by: Use PostgreSQL with the sessions table for session storage.
Reason: Standardized on single database; MongoDB was only used for sessions and added operational complexity.
```

The archive is not loaded by Claude — it is reference documentation for humans. It prevents the same debates and mistakes from recurring.

### The 80/20 Rule for Rules

Across most production configurations, 20% of rules account for 80% of Claude's consequential decisions. The other 80% of rules cover edge cases, stylistic preferences, and situations that rarely arise.

Identifying your top 20%:

1. List every rule in CLAUDE.md
2. For each rule, estimate: "How often does this rule meaningfully change Claude's output in a session?"
3. Rules that apply daily: keep, prioritize, place early
4. Rules that apply weekly: keep, place in middle
5. Rules that apply monthly: consider archiving or moving to a loaded-on-demand skill
6. Rules that apply rarely: archive

The goal is not to eliminate coverage — it's to ensure that the rules that matter most are not diluted by the rules that matter least.

**Placement matters**: Place your top 20% rules in the first third of CLAUDE.md. Attention weight is not uniform across a long document — early content has higher salience.

### Summary: Reduction Techniques by Impact

| Technique | Context Reduction | Effort | Adherence Impact |
|-----------|------------------|--------|-----------------|
| Path-scoping | 40-50% | Medium | +15-25% |
| Negative constraints | 0% (reformulation) | Low | +15-25% per rule |
| Rule compression | 20-30% | Low | +5-10% |
| Deduplication | 10-20% | Low | +5-15% |
| Archive pattern | 10-30% | Low | +5-10% |
| 80/20 prioritization | 0% (reordering) | Low | +10-20% |

The highest-leverage sequence for a project with context debt:

1. Path-scope (biggest structural win)
2. Deduplicate (removes noise)
3. Compress (sharpens remaining rules)
4. Archive (clears obsolete rules safely)
5. Reorder (prioritizes the rules that matter most)

---

## 9. Maturity Assessment

Context engineering capability develops in stages. Most teams reach Level 2 and stop — not because higher levels are complex, but because the failures at Level 2 are invisible. Output quality is acceptable, so the pressure to go further never appears. This assessment makes the gap visible.

### The Six Levels

| Level | Name | What exists | Failure mode |
|-------|------|-------------|--------------|
| **0** | No configuration | LLM with no CLAUDE.md | Generic outputs, zero project awareness |
| **1** | Flat config | Single CLAUDE.md, no structure | Rules pile up, adherence degrades after ~100 lines |
| **2** | Structured config | Sections, clear organization, global/project separation | Works solo, breaks at team scale |
| **3** | Modular config | Path-scoped modules, deliberate layering | Rules maintained but no verification |
| **4** | Measured config | Canary tests, adherence tracking, lifecycle management | System works but drifts silently over time |
| **5** | Engineered system | Profiles, CI drift detection, ACE pipeline, quarterly audit rhythm | — |

### Self-Assessment

Answer each question. Stop at the first "No" — that is your current level.

**Level 0 → 1**: Do you have a CLAUDE.md file in your project?

**Level 1 → 2**: Does your configuration distinguish between global conventions (in `~/.claude/CLAUDE.md`) and project-specific rules (in `./CLAUDE.md`)? Are sections clearly separated?

**Level 2 → 3**: Are subsystem-specific rules in path-scoped modules rather than the root CLAUDE.md? Does your root CLAUDE.md stay under 150 lines?

**Level 3 → 4**: Do you have canary checks that verify key conventions? Do you track violation rates for your most important rules? Do you run a context audit after major milestones?

**Level 4 → 5**: Do team members assemble their CLAUDE.md from profiles rather than editing it directly? Is there CI drift detection that alerts when configuration diverges from source modules? Do you run session retrospectives to feed new patterns back into configuration?

### What to Do at Each Level

| Your level | Next action |
|------------|-------------|
| 0 | Create a minimal CLAUDE.md with 5-10 rules. See §3 for what belongs there. |
| 1 | Split global and project config. Move cross-project preferences to `~/.claude/CLAUDE.md`. |
| 2 | Identify the 2-3 highest-traffic subsystems. Create path-scoped modules for them. |
| 3 | Write 3-5 canary prompts for your most violated rules. Automate them. |
| 4 | Introduce profiles for team members. Add CI drift detection. Start session retrospectives. |
| 5 | Maintain quarterly audits. The system is built — the work is ongoing calibration. |

Most teams move from Level 0 to Level 2 in a single afternoon. Moving from Level 3 to Level 4 requires a measurement habit, not more configuration. The bottleneck at the higher levels is not knowledge — it is the discipline to treat configuration as a living system rather than a one-time setup.

---

## Cross-References

- Architecture and project structure patterns: `guide/core/architecture.md`
- Methodology frameworks for AI-assisted development: `guide/core/methodologies.md`
- Hooks and automation for context management: `guide/ultimate-guide.md` §5 (Hooks)
- MCP server integration for extended context: `guide/ultimate-guide.md` §7 (MCP)
- Security considerations for context content: `guide/security/`
- Path-scoped module examples: `examples/` directory

---

*Part of the Claude Code Ultimate Guide. For the full reference, see `guide/ultimate-guide.md`.*
