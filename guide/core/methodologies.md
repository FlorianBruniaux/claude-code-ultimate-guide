---
title: "Development Methodologies Reference"
description: "Quick reference for 15 structured AI-assisted development methodologies including TDD, SDD, and BDD"
tags: [reference, tdd, design-patterns, workflows]
---

# Development Methodologies Reference

> **Confidence**: Tier 2 — Validated by multiple production reports and official documentation.
>
> **Last updated**: February 2026

This is a quick reference for 15 structured development methodologies that have emerged for AI-assisted development in 2025-2026. For hands-on practical workflows, see [workflows/](./workflows/).

---

## Table of Contents

1. [Decision Tree](#decision-tree-what-do-you-need)
2. [The 15 Methodologies](#the-15-methodologies)
3. [SDD Tools Reference](#sdd-tools-reference)
4. [Writing Effective Specs](#writing-effective-specs)
5. [Combination Patterns](#combination-patterns)
6. [Sources](#sources)

---

## Decision Tree: What Do You Need?

```
┌─ "I want quality code" ────────────→ workflows/tdd-with-claude.md
│
├─ "I want to spec before code" ─────→ workflows/spec-first.md
│
├─ "I need to plan architecture" ────→ workflows/plan-driven.md
│
├─ "I'm iterating on something" ─────→ workflows/iterative-refinement.md
│
└─ "I need methodology theory" ──────→ Continue reading below
```

---

## The 15 Methodologies

Organized in a 6-tier pyramid from strategic orchestration down to optimization techniques.

### Tier 1: Strategic Orchestration

| Name | What | Best For | Claude Fit |
|------|------|----------|------------|
| **BMAD** | Multi-agent governance with constitution as guardrail | Enterprise 10+ teams, long-term projects | ⭐⭐ Niche but powerful |
| **GSD** | Meta-prompting 6-phase workflow with fresh contexts per task | Solo devs, Claude Code CLI | ⭐⭐ Similar to patterns in guide |

**BMAD (Breakthrough Method for Agile AI-Driven Development)** inverts the traditional paradigm: documentation becomes the source of truth, not code. Uses specialized agents (Analyst, PM, Architect, Developer, QA) orchestrated with strict governance. *Note: BMAD's role-based agent naming reflects their methodology; see §9.17 Agent Anti-Patterns for scope-focused alternatives.*

- **Key concept**: Constitution.md as strategic guardrail
- **When to use**: Complex enterprise projects needing governance
- **When to avoid**: Small teams, MVPs, rapid prototyping

**GSD (Get Shit Done)** addresses context rot through systematic 6-phase workflow (Initialize → Discuss → Plan → Execute → Verify → Complete) with fresh 200k-token contexts per task. Core concepts (multi-agent orchestration, fresh context management) overlap significantly with existing patterns like Ralph Loop, Gas Town, and BMAD. See [resource evaluation](../docs/resource-evaluations/gsd-evaluation.md) for detailed comparison.

> **Emerging**: [Ralph Inferno](https://github.com/sandstream/ralph-inferno) implements autonomous multi-persona workflows (Analyst→PM→UX→Architect→Business) with VM-based execution and self-correcting E2E loops. Experimental but interesting for "vibe coding at scale".

---

### Foundational Discipline: Plan-First Workflow

> **"Once the plan is good, the code is good."**
> — Boris Cherny, creator of Claude Code

**Not just a feature (`/plan` command) — a systematic discipline.**

> **Context Engineering**: Thoughtworks designates this broader approach "Context Engineering" in their Technology Radar (Nov 2025)[^thoughtworks2025] — the systematic design of information provided to LLMs during inference. Three core techniques: context setup (minimal system prompts, few-shot examples), context management for long-horizon tasks (summarization, external memories, sub-agent architectures), and dynamic information retrieval (JIT context loading). Related patterns in Claude Code: AGENTS.md, MCP Context7, Plan Mode.

[^thoughtworks2025]: Thoughtworks Technology Radar Vol 33, Nov 2025. [PDF](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2025/11/tr_technology_radar_vol_33_en.pdf). See also: [Macro trends blog post](https://www.thoughtworks.com/insights/blog/technology-strategy/macro-trends-tech-industry-november-2025).

**The Mental Model**:

Planning isn't optional for complex tasks. It's the difference between:
- ❌ 8 iterations of "try → fix → retry → fix again"
- ✅ 1 iteration of "plan → validate → execute cleanly"

**When to plan first**:

| Task Complexity | Plan First? | Why |
|----------------|-------------|-----|
| >3 files modified | ✅ Yes | Cross-file dependencies need architecture |
| >50 lines changed | ✅ Yes | Enough complexity for mistakes |
| Architectural changes | ✅ Yes | Impact analysis required |
| Unfamiliar codebase | ✅ Yes | Need exploration before action |
| Typo/obvious fix | ❌ No | Planning overhead > task time |
| Single-line change | ❌ No | Just do it |

**How plan-first works**:

1. **Exploration phase** (Plan Mode via `Shift+Tab`):
   - Claude reads files, explores architecture
   - No edits allowed → forces thinking before action
   - Proposes approach with trade-offs

2. **Validation phase** (you review):
   - Plan exposes assumptions and gaps
   - Easier to correct direction now vs after 100 lines written
   - Plan becomes contract for execution

3. **Execution phase** (toggle back to Normal Mode with `Shift+Tab`):
   - Plan → code becomes mechanical translation
   - Fewer surprises, cleaner implementation
   - Faster overall despite "slower" start

**Boris Cherny workflow**:

> "I run many sessions, start in plan mode, then switch into execution once the plan looks right. The signature upgrade is verification—giving Claude a way to test and confirm its own output."

**Benefits over "just start coding"**:

- **Fewer correction iterations**: Plan catches issues before they become code
- **Better architecture**: Forced to think about structure first
- **Clearer communication**: Plan is shared understanding with team/Claude
- **Reduced cost**: One clean iteration < multiple messy iterations (even if plan phase costs tokens)

**Integration with CLAUDE.md**:

Document your team's plan-first triggers:
```markdown
## Planning Policy
- ALWAYS plan first: API changes, database migrations, new features
- OPTIONAL planning: Bug fixes <10 lines, test additions
- NEVER skip: Changes affecting >2 modules
```

**See also**: [Plan Mode documentation](./ultimate-guide.md#23-plan-mode) for `/plan` command usage.

> **Advanced pattern**: For an iterative annotation-based approach to plan-driven development, see [Custom Markdown Plans (Boris Tane Pattern)](./workflows/plan-driven.md#advanced-custom-markdown-plans-boris-tane-pattern).

---

### Tier 2: Specification & Architecture

| Name | What | Best For | Claude Fit |
|------|------|----------|------------|
| **SDD** | Specs before code | APIs, contracts | ⭐⭐⭐ Core pattern |
| **Doc-Driven** | Docs = source of truth | Cross-team alignment | ⭐⭐⭐ CLAUDE.md native |
| **Req-Driven** | Rich artifact context (20+ artifacts) | Complex requirements | ⭐⭐ Heavy setup |
| **DDD** | Domain language first | Business logic | ⭐⭐ Design-time |

**SDD (Spec-Driven Development)** — Specifications BEFORE code. One well-structured iteration equals 8 unstructured ones. CLAUDE.md IS your spec file.

**Doc-Driven Development** — Living documentation versioned in git becomes the single source of truth. Changes to specs trigger implementation.

**Requirements-Driven Development** — Uses CLAUDE.md as comprehensive implementation guide with 20+ structured artifacts.

**DDD (Domain-Driven Design)** — Aligns software with business language through:
- Ubiquitous Language: Shared vocabulary in code
- Bounded Contexts: Isolated domain boundaries
- Domain Distillation: Core vs Support vs Generic domains

---

### Tier 3: Behavior & Acceptance

| Name | What | Best For | Claude Fit |
|------|------|----------|------------|
| **BDD** | Given-When-Then scenarios | Stakeholder collaboration | ⭐⭐⭐ Tests & specs |
| **ATDD** | Acceptance criteria first | Compliance, regulated | ⭐⭐ Process-heavy |
| **CDD** | API contracts as interface | Microservices | ⭐⭐⭐ OpenAPI native |

**BDD (Behavior-Driven Development)** — Beyond testing: a collaboration process.
1. Discovery: Involve devs and business experts
2. Formulation: Write Given-When-Then examples
3. Automation: Convert to executable tests (Gherkin/Cucumber)

```gherkin
Feature: Order Management
  Scenario: Cannot buy without stock
    Given product with 0 stock
    When customer attempts purchase
    Then system refuses with error message
```

**ATDD (Acceptance Test-Driven Development)** — Acceptance criteria defined BEFORE coding, collaboratively ("Three Amigos": Business, Dev, Test).

In agentic development, ATDD is particularly effective because agents need unambiguous success conditions. The flow maps cleanly to agent tasks:

1. **Define acceptance criteria** in Gherkin (human-readable, machine-executable)
2. **Agent writes failing tests** based on scenarios (not implementation)
3. **Agent implements** until tests pass

```gherkin
Feature: Password Reset
  Scenario: User resets via email
    Given a registered user with email "user@example.com"
    When they request a password reset
    Then they receive a reset email within 60 seconds
    And the reset link expires after 24 hours
```

This Gherkin scenario is the contract between intent and implementation. The agent cannot misinterpret scope because done is defined before a line of code is written.

> **Applied to agents**: Pass the Gherkin file to Claude Code before implementing. "Write failing tests for this feature file, then implement until they pass." The scenario writer role (human or agent) forces explicit scope before execution starts.

**CDD (Contract-Driven Development)** — API contracts (OpenAPI specs) as executable interface between teams. Patterns: Contract as Test, Contract as Stub.

---

### Tier 4: Feature Delivery

| Name | What | Best For | Claude Fit |
|------|------|----------|------------|
| **FDD** | Feature-by-feature delivery | Large teams 10+ | ⭐⭐ Structure |
| **Context Eng.** | Context as first-class design | Long sessions | ⭐⭐⭐ Fundamental |

**FDD (Feature-Driven Development)** — Five processes:
1. Develop Overall Model
2. Build Features List
3. Plan by Feature
4. Design by Feature
5. Build by Feature

Strict iteration: 2 weeks max per feature.

**Context Engineering** — Treat context as design element:
- Progressive Disclosure: Let agent discover incrementally
- Memory Management: Conversation vs persistent memory
- Dynamic Refresh: Rewrite TODO list before response

---

### Tier 5: Implementation

| Name | What | Best For | Claude Fit |
|------|------|----------|------------|
| **TDD** | Red-Green-Refactor | Quality code | ⭐⭐⭐ Core workflow |
| **Eval-Driven** | Evals for LLM outputs | AI products | ⭐⭐⭐ Agents |
| **Multi-Agent** | Orchestrate sub-agents | Complex tasks | ⭐⭐⭐ Task tool |

**TDD (Test-Driven Development)** — The classic cycle:
1. **Red**: Write failing test
2. **Green**: Minimal code to pass
3. **Refactor**: Clean up, tests stay green

With Claude: Be explicit. "Write FAILING tests that don't exist yet."

> **Verification Loops** — A formalized pattern for autonomous iteration (broader than TDD):
>
> **Core principle**: Give Claude a mechanism to verify its own output.
>
> ```
> Code generated → Verification tool → Feedback loop → Improvement
> ```
>
> **Why it works** (Boris Cherny): *"An agent that can 'see' what it has done produces better results."*
>
> **Verification mechanisms by domain**:
>
> | Domain | Verification Tool | What Claude "Sees" |
> |--------|-------------------|-------------------|
> | **Frontend** | Browser preview (live reload) | Visual rendering, layout, interactions |
> | **Backend** | Tests (unit/integration) | Pass/fail status, error messages |
> | **Types** | TypeScript compiler | Type errors, incompatibilities |
> | **Style** | Linters (ESLint, Prettier) | Style violations, formatting issues |
> | **Performance** | Profilers, benchmarks | Execution time, memory usage |
> | **Accessibility** | axe-core, screen readers | WCAG violations, navigation issues |
> | **Security** | Static analyzers (Semgrep) | Vulnerability patterns |
> | **UX** | User testing, recordings | Usability problems, confusion points |
>
> **TDD as canonical example**:
> 1. Claude writes tests for the feature
> 2. Claude iterates code until tests pass
> 3. Continue until explicit completion criteria met
>
> **Official guidance**: *"Tell Claude to keep going until all tests pass. It will usually take a few iterations."* — [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
>
> **Implementation patterns**:
> - **Hooks**: PostToolUse hook runs verification after each edit
> - **Browser extension**: Claude in Chrome sees rendered output
> - **Test watchers**: Jest/Vitest watch mode provides instant feedback
> - **CI/CD gates**: GitHub Actions runs full validation suite
> - **Multi-Claude verification**: One Claude codes, another reviews
>
> **Anti-pattern**: Blind iteration without feedback. Without verification mechanism, Claude can't converge toward correct solution—it guesses.

**Eval-Driven Development** — TDD for LLMs. Test agent behaviors via evals:
- Code-based: `output == golden_answer`
- LLM-based: Another Claude evaluates
- Human grading: Reference, slow

> **Eval Harness** — The infrastructure that runs evaluations end-to-end: providing instructions and tools, running tasks concurrently, recording steps, grading outputs, and aggregating results.
>
> See Anthropic's comprehensive guide: [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

**Multi-Agent Orchestration** — From single assistant to orchestrated team:
```
Meta-Agent (Orchestrator)
├── Analyst (requirements)
├── Architect (design)
├── Developer (code)
└── Reviewer (validation)
```

### ADR-Driven Development

**Pattern**: Write plain English ADRs → Feed to implement-adr skill → Execute natively

Architecture Decision Records (ADRs) combined with Claude Code skills create a workflow where architectural decisions drive implementation directly.

**Workflow Steps**:
1. **Document decision** in ADR format (context, decision, consequences)
2. **Create implementation skill** (generic or `implement-adr` specialized)
3. **Feed ADR as prompt** to skill with clear acceptance criteria
4. **Claude executes** based on architectural guidance in ADR

**Example ADR Template**:
```
# ADR-001: Database Migration Strategy

## Context
Legacy MySQL schema needs migration to PostgreSQL for better JSON support.

## Decision
Use incremental dual-write pattern with feature flags.

## Consequences
- Positive: Zero-downtime migration
- Negative: Temporary code complexity during transition
```

**Implementation Workflow**:
```bash
# 1. Write ADR (plain English)
vim docs/adr/001-database-migration.md

# 2. Feed to implementation skill
/implement-adr docs/adr/001-database-migration.md

# 3. Claude executes based on ADR guidance
# → Creates migration scripts
# → Updates ORM configuration
# → Adds feature flags
# → Implements dual-write logic
```

**Benefits**:
- ✅ **Documentation-driven**: Architecture and code stay synchronized
- ✅ **Native execution**: No external frameworks needed
- ✅ **Traceable decisions**: Clear audit trail from decision to implementation
- ✅ **Team alignment**: ADRs communicate intent to both humans and AI

**Source**: [Gur Sannikov embedded engineering workflow](https://www.linkedin.com/posts/gursannikov_claudecode-embeddedengineering-aiagents-activity-7423851983331328001-DrFb)

---

### Tier 6: Optimization

| Name | What | Best For | Claude Fit |
|------|------|----------|------------|
| **Iterative Loops** | Autonomous refinement | Optimization | ⭐⭐⭐ Core |
| **Fresh Context** | Reset per task, state in files | Long autonomous sessions | ⭐⭐⭐ Power users |
| **Prompt Engineering** | Technique foundation | Everything | ⭐⭐⭐ Prerequisite |

**Iterative Refinement Loops** — Autonomous convergence:
1. Execute prompt
2. Observe result
3. If result ≠ "DONE" → refine and repeat

**Prompt Engineering** — Foundations for ALL Claude usage:
- Zero-Shot Chain of Thought: "Think step by step"
- Few-Shot Learning: 2-3 examples of expected pattern
- Structured Prompts: XML tags for organization
- Position Matters: For long docs, place question at end

**Fresh Context Pattern (Ralph Loop)** — Solves context rot by spawning fresh agent instances per task. State persists in git + progress files, not chat history. Ideal for long autonomous sessions (migrations, overnight runs). See [Ultimate Guide - Fresh Context Pattern](./ultimate-guide.md#fresh-context-pattern-ralph-loop) for implementation.

---

## SDD Tools Reference

Three tools have emerged to formalize Spec-Driven Development:

| Tool | Use Case | Official Docs | Claude Integration |
|------|----------|---------------|-------------------|
| **Spec Kit** | Greenfield, governance | [github.blog/spec-kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) | `/speckit.constitution`, `/speckit.specify`, `/speckit.plan` |
| **OpenSpec** | Brownfield, changes | [github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | `/openspec:proposal`, `/openspec:apply`, `/openspec:archive` |
| **Specmatic** | API contract testing | [specmatic.io](https://specmatic.io) | MCP agent available |
| **Spec-to-Code Factory** | Greenfield, enforcement outillé | [github.com/SylvainChabaud/spec-to-code-factory](https://github.com/SylvainChabaud/spec-to-code-factory) | Implémentation référence multi-agents (BREAK→MODEL→ACT→DEBRIEF) |

### Spec Kit (Greenfield)

5-phase workflow:
1. Constitution: `/speckit.constitution` → guardrails
2. Specify: `/speckit.specify` → requirements
3. Plan: `/speckit.plan` → architecture
4. Tasks: `/speckit.tasks` → decomposition
5. Implement: `/speckit.implement` → code

### OpenSpec (Brownfield)

Two-folder architecture:
```
openspec/
├── specs/      ← Current truth (stable)
└── changes/    ← Proposals (temporary)
```

Workflow: Proposal → Review → Apply → Archive

### Specmatic (API Contracts)

- **Contract as Test**: Auto-generates 1000s of tests from OpenAPI spec
- **Contract as Stub**: Mock server for parallel development
- **Backward Compatibility**: Detects breaking changes

---

## Writing Effective Specs

> Based on analysis of 2,500+ agent configuration files.
> Source: [Addy Osmani](https://addyosmani.com/blog/good-spec/)

### The Six Essential Components

| Component | What to Include | Example |
|-----------|-----------------|---------|
| **Commands** | Executable with flags | `npm test -- --coverage` |
| **Testing** | Framework, coverage, locations | `vitest, 80%, tests/` |
| **Project structure** | Explicit directories | `src/`, `lib/`, `tests/` |
| **Code style** | One example > paragraphs | Show a real function |
| **Git workflow** | Branch, commit, PR format | `feat/name`, conventional commits |
| **Boundaries** | Permission tiers | See below |

### Permission Tiers

| Tier | Symbol | Use For |
|------|--------|---------|
| Always do | ✅ | Safe actions, no approval (lint, format) |
| Ask first | ⚠️ | High-impact changes (delete, publish) |
| Never do | 🚫 | Hard stops (commit secrets, force push main) |

### Curse of Instructions

> ⚠️ Research shows **more instructions = worse adherence** to each one.
>
> Solution: Feed only relevant spec sections per task, not the entire document.

### Monolithic vs Modular Specs

| Project Size | Approach |
|--------------|----------|
| Small (<10 files) | Single spec file |
| Medium (10-50 files) | Sectioned spec, feed per task |
| Large (50+ files) | Sub-agent routing by domain |

---

## Combination Patterns

Recommended stacks by situation:

| Situation | Recommended Stack | Notes |
|-----------|-------------------|-------|
| Solo MVP | SDD + TDD | Minimal overhead, quality focus |
| Team 5-10, greenfield | Spec Kit + TDD + BDD | Governance + quality + collaboration |
| Microservices | CDD + Specmatic | Contract-first, parallel dev |
| Existing SaaS (100+ features) | OpenSpec + BDD | Change tracking, no spec drift |
| Enterprise 10+ | BMAD + Spec Kit + Specmatic | Full governance + contracts |
| LLM-native product | Eval-Driven + Multi-Agent | Self-improving systems |

---

## Quick Reference Table

| Methodology | Level | Primary Focus | Team Size | Learning Curve |
|-------------|-------|---------------|-----------|----------------|
| BMAD | Orchestration | Governance | 10+ | High |
| SDD | Specification | Contracts | Any | Medium |
| Doc-Driven | Specification | Alignment | Any | Low |
| Req-Driven | Specification | Context | 5+ | Medium |
| DDD | Specification | Domain | 5+ | Very High |
| BDD | Behavior | Collaboration | 5+ | Medium |
| ATDD | Behavior | Compliance | 5+ | Medium |
| CDD | Behavior | APIs | 5+ | Medium |
| FDD | Delivery | Features | 10+ | Medium |
| Context Eng. | Delivery | AI sessions | Any | Low |
| TDD | Implementation | Quality | Any | Low |
| Eval-Driven | Implementation | AI outputs | Any | Medium |
| Multi-Agent | Implementation | Complexity | Any | Medium |
| Iterative | Optimization | Refinement | Any | Low |
| Prompt Eng. | Optimization | Foundation | Any | Very Low |

---

## Sources

### Official Documentation (Tier 1)

- Anthropic: [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- Anthropic: [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic: [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- GitHub: [Spec-Driven Development Toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- Microsoft: [Spec-Driven Development with Spec Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)

### Methodology References (Tier 2)

**SDD & Spec-First**
- Addy Osmani: [How to Write Good Specs for AI Agents](https://addyosmani.com/blog/good-spec/)
- Addy Osmani: [My AI Coding Workflow in 2026](https://addyosmani.com/blog/ai-coding-workflow/) — End-to-end workflow: spec-first, context packing, TDD, git checkpoints
- Martin Fowler: [SDD Tools Analysis](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- InfoQ: [Spec-Driven Development](https://www.infoq.com/articles/spec-driven-development/)
- Kinde: [Beyond TDD - Why SDD is the Next Step](https://kinde.com/learn/ai-for-software-engineering/best-practice/beyond-tdd-why-spec-driven-development-is-the-next-step/)
- Tessl.io: [Spec-Driven Dev with Claude Code](https://tessl.io/blog/spec-driven-dev-with-claude-code/)

**BMAD**
- GMO Recruit: [The BMAD Method](https://recruit.group.gmo/engineer/jisedai/blog/the-bmad-method-a-framework-for-spec-oriented-ai-driven-development/)
- Benny Cheung: [BMAD - Reclaiming Control in AI Dev](https://bennycheung.github.io/bmad-reclaiming-control-in-ai-dev)
- GitHub: [BMAD-AT-CLAUDE](https://github.com/24601/BMAD-AT-CLAUDE)

**TDD with AI**
- Steve Kinney: [TDD with Claude](https://stevekinney.com/courses/ai-development/test-driven-development-with-claude)
- Nathan Fox: [Taming GenAI Agents](https://www.nathanfox.net/p/taming-genai-agents-like-claude-code)
- Alex Op: [Custom TDD Workflow Claude Code](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/)

**BDD & DDD**
- Alex Soyes: [BDD Behavior-Driven Development](https://alexsoyes.com/bdd-behavior-driven-development/)
- Alex Soyes: [DDD Domain-Driven Design](https://alexsoyes.com/ddd-domain-driven-design/)
- Inflectra: [Behavior-Driven Development](https://www.inflectra.com/Ideas/Topic/Behavior-Driven-Development.aspx)

**Context Engineering**
- Intuition Labs: [What is Context Engineering](https://intuitionlabs.ai/articles/what-is-context-engineering)
- Manus.im: [Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)

**Eval-Driven & Multi-Agent**
- Fireworks AI: [Eval-Driven Development with Claude Code](https://fireworks.ai/blog/eval-driven-development-with-claude-code)
- Brandon Casci: [Transform into a Dev Team using Claude Code Agents](https://www.brandoncasci.com/2025/09/21/how-to-transform-yourself-into-a-dev-team-using-claude-codes-ai-agents.html)
- The Unwind AI: [Claude Code's Multi-Agent Orchestration](https://www.theunwindai.com/p/claude-code-s-hidden-multi-agent-orchestration-now-open-source)

### Tools Documentation (Tier 1)

- OpenSpec: [github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
- Spec Kit: [github.com/github/spec-kit](https://github.com/github/spec-kit)
- Specmatic: [specmatic.io](https://specmatic.io)
- Specmatic Article: [Spec-Driven Development with GitHub Spec Kit and Specmatic MCP](https://specmatic.io/article/spec-driven-development-api-design-first-with-github-spec-kit-and-specmatic-mcp/)

### Additional References

- Talent500: [Claude Code TDD Guide](https://talent500.com/blog/claude-code-test-driven-development-guide/)
- Testlio: [Acceptance Test-Driven Development](https://testlio.com/blog/what-is-acceptance-test-driven-development/)
- Monday.com: [Feature-Driven Development](https://monday.com/blog/rnd/feature-driven-development-fdd/)
- Paddo.dev: [Ralph Wiggum Autonomous Loops](https://paddo.dev/blog/ralph-wiggum-autonomous-loops/)
- Walturn: [Prompt Engineering for Claude](https://www.walturn.com/insights/mastering-prompt-engineering-for-claude)
- AWS: [Prompt Engineering with Claude on Bedrock](https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-claude-3-on-amazon-bedrock/)

---

## See Also

- [workflows/tdd-with-claude.md](./workflows/tdd-with-claude.md) — Practical TDD guide
- [workflows/spec-first.md](./workflows/spec-first.md) — Spec-first development
- [workflows/plan-driven.md](./workflows/plan-driven.md) — Using /plan mode
- [workflows/iterative-refinement.md](./workflows/iterative-refinement.md) — Refinement loops
- [ultimate-guide.md#912](./ultimate-guide.md) — Section 9.12 summary
