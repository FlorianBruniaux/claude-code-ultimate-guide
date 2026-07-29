---
name: methodology-advisor
description: "Analyzes your codebase and asks 3 targeted questions to recommend the right AI-assisted development methodology stack"
---

# Methodology Advisor

Analyze this project and recommend the best AI-assisted development methodology stack. Read what you can from the codebase first, then ask only what you cannot infer.

**Time**: 2-4 minutes | **Output**: One recommended stack + contextual quick start

---

## Phase 1 — Silent codebase analysis

Run these reads silently. Do not output results yet — build an internal picture only.

### 1.1 Project identity

```bash
# Config files
cat CLAUDE.md 2>/dev/null || cat claude.md 2>/dev/null
cat package.json 2>/dev/null | grep -E '"name"|"description"|"scripts"' | head -10
cat Cargo.toml 2>/dev/null | grep -E '^name|^description' | head -5
cat pyproject.toml 2>/dev/null | grep -E '^name|^description' | head -5
cat go.mod 2>/dev/null | head -3
```

### 1.2 Team size

```bash
# Unique contributors in last 90 days
git log --since="90 days ago" --format="%ae" 2>/dev/null | sort -u | wc -l
# Total commits
git log --oneline 2>/dev/null | wc -l
```

### 1.3 Test maturity

```bash
# Test files exist?
find . -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" -o -name "test_*.py" \
  2>/dev/null | grep -v node_modules | grep -v ".git" | wc -l
# Test framework hints
grep -rn --include="*.json" --include="*.toml" --include="*.yaml" \
  -l "jest\|vitest\|pytest\|rspec\|mocha\|cypress\|playwright" \
  2>/dev/null | grep -v node_modules | head -5
# CI config
ls .github/workflows/*.yml 2>/dev/null | wc -l
ls .gitlab-ci.yml .circleci/config.yml 2>/dev/null | wc -l
```

### 1.4 Spec and documentation signals

```bash
# Spec files
find . -name "*.spec.md" -o -name "SPEC*.md" -o -name "spec.md" -o -name "DESIGN*.md" \
  -o -name "ADR*.md" -o -name "RFC*.md" \
  2>/dev/null | grep -v node_modules | grep -v ".git" | head -10
# OpenAPI / contract files
find . -name "openapi*.yaml" -o -name "openapi*.json" -o -name "swagger*.yaml" \
  -o -name "*.proto" \
  2>/dev/null | grep -v node_modules | head -5
# BDD feature files
find . -name "*.feature" 2>/dev/null | grep -v node_modules | wc -l
```

### 1.5 Codebase size and structure

```bash
# File count (rough)
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.py" \
  -o -name "*.rs" -o -name "*.go" -o -name "*.java" -o -name "*.rb" \) \
  2>/dev/null | grep -v node_modules | grep -v ".git" | wc -l
# Services / packages (monorepo signal)
ls packages/ apps/ services/ 2>/dev/null | head -10
```

### 1.6 AI and LLM signals

```bash
# LLM API usage in code
grep -rn --include="*.ts" --include="*.py" --include="*.js" \
  -l "anthropic\|openai\|groq\|mistral\|langchain\|llm\|ChatCompletion\|claude" \
  2>/dev/null | grep -v node_modules | grep -v ".git" | head -5
# Eval framework hints
find . -name "evals*" -o -name "*eval*" -type d 2>/dev/null | grep -v node_modules | head -5
```

---

## Phase 2 — Score the 8 stacks

Using what you found, score each stack 0-10 based on fit signals:

| Stack | Key signals that boost the score |
|-------|----------------------------------|
| **solo-mvp** | 1 contributor, few files, no CI yet, greenfield |
| **team-greenfield** | 2-10 contributors, new project, no legacy files |
| **microservices** | `packages/`, `services/`, OpenAPI files, `.proto` |
| **brownfield-saas** | High commit count, large file count, few test files |
| **enterprise-gov** | 10+ contributors, CI, ADR files, `AGENTS.md` |
| **llm-native** | LLM imports, eval dirs, AI product signals |
| **power-solo** | 1 contributor, high commit rate, iterative commits |
| **plan-moderate** | Mixed signals, CLAUDE.md present, moderate size |

---

## Phase 3 — Ask only what you cannot infer

After the silent analysis, present your preliminary picture to the user in 2-3 lines, then ask exactly 3 questions. No more.

Format:

```
From your codebase I can see: [2-3 concrete observations].
Before recommending, 3 quick questions:

1. [Pain point question — pick the most relevant from below]
2. [Deploy frequency — if not inferable from CI/CD signals]
3. [Setup appetite — how much ceremony are you willing to invest?]
```

**Question bank — pick the 3 most relevant given what you found:**

- Pain: "What slows you down most right now — regressions, unclear requirements, context rot between sessions, or no traceability?"
- Pain: "When Claude generates a large chunk of code, what is your biggest worry — quality, drift from spec, or losing track of what was built?"
- Deploy: "How often do you ship to production — multiple times a day, weekly, or on longer release cycles?"
- Deploy: "Is this a product with real users today, a prototype, or an internal tool?"
- Governance: "How much initial setup are you willing to invest — none (just start), 30 minutes, or half a day?"
- Governance: "Does anyone outside your dev team (PM, QA, compliance) need to validate what gets built?"
- AI product: "Does your product expose AI-generated outputs directly to end users?"
- Scale: "Do multiple services or teams need to agree on API contracts before implementing?"

---

## Phase 4 — Recommendation

Output the recommendation in this structure:

---

### Your Stack: [Stack Name] [icon]

**Why this fits your project:**
- [Finding from Phase 1] → [explains this stack choice]
- [Finding from Phase 1] → [explains this stack choice]
- [Answer to question N] → [explains this stack choice]

**Methodologies included:** `[Method A]` + `[Method B]` (+ `[Method C]` if applicable)

**What this looks like in practice:**
[2-3 sentences describing the concrete workflow for THIS project, using actual file names or paths found.]

**Quick start for your project:**
1. [Concrete first step using actual project context]
2. [Second step]
3. [Third step]

**Before you start, note:**
- [One honest trade-off or limitation of this stack]
- [One thing to watch out for given what you found]

**Go deeper:** https://cc.bruniaux.com/methodologies/ — interactive quiz and full stack comparison
**Full methodology guide:** https://cc.bruniaux.com/guide/methodologies/

---

## Stack reference (internal)

Use this to map your scoring to quick-start language:

**solo-mvp** (SDD + TDD): Write feature spec in CLAUDE.md → `"Write failing tests for this spec, then implement until green."`

**team-greenfield** (Spec Kit + TDD + BDD): `/speckit.constitution` → Given/When/Then scenarios with PM → TDD each scenario.

**microservices** (CDD + Specmatic + TDD): Write OpenAPI spec first → Specmatic for contract tests → TDD implementation.

**brownfield-saas** (OpenSpec + BDD + JiTTesting): OpenSpec captures current state → BDD for changed behavior → pre-merge: `"Generate tests that catch regressions in this diff."`

**enterprise-gov** (BMAD + Spec Kit + Specmatic): `constitution.md` → agent role definitions → Spec Kit requirements → Specmatic contract enforcement.

**llm-native** (Eval-Driven + Multi-Agent): Define eval criteria (accuracy, safety, format) → build eval harness → iterate until evals pass.

**power-solo** (TDD + Ralph Loop + Iterative): Tight test loop → fresh context per task via git stash + progress files → `"Keep iterating until all tests pass and lint is clean."`

**plan-moderate** (Plan-First + SDD + Context Engineering): Every complex task starts in Plan Mode (Shift+Tab) → validate → write spec in CLAUDE.md → execute with progressive context loading.
