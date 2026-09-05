---
title: "Module 05: Skills & Automation"
description: "Learning Path Module 05: build scoped Claude Code skills with SKILL.md, progressive disclosure, invocation controls, evals, and retirement criteria. 1.5 hours, intermediate."
---

# Module 05: Skills & Automation

**Time**: 1.5 hours | **Complexity**: ⭐⭐ Intermediate

**Previous:** [Module 04: Agents & Specialization](04-agents.md)

## Goal

Create a project skill that gives Claude relevant knowledge or a reusable procedure without loading its full content into every session.

---

## What You'll Learn

- What skills load, and when
- How to create a valid `SKILL.md`
- How `description` controls model discovery
- How to control user and model invocation
- How to choose an ownership scope
- How to separate judgment from guaranteed orchestration
- How to evaluate, maintain, and retire a skill

---

## What Are Skills?

A **skill** is a directory containing a `SKILL.md` file and optional supporting files. Its description is advertised to Claude. The full instructions load only when you or Claude invoke the skill.

This makes skills useful for repeated procedures, checklists, and reference material that would be too costly or distracting in an always-loaded `CLAUDE.md`.

### Example: Testing Skill

Instead of explaining your testing approach in each session, create a project skill whose description says when it applies:

```markdown
---
name: testing-standards
description: Apply this project's Jest and Testing Library conventions when creating, reviewing, or debugging tests.
---

# Testing Standards

- Use descriptive test names.
- Follow Arrange, Act, Assert.
- Mock external boundaries, not implementation details.
- Run the relevant test file before the full suite.
```

Claude sees the name and description during the session. It loads the body when the current request matches the description, or when you type `/testing-standards`.

### Skills vs CLAUDE.md vs Agents vs Workflows

| Mechanism | Best for | Loading or execution |
|-----------|----------|----------------------|
| `CLAUDE.md` | Short facts and rules relevant to most sessions | Loaded at session start |
| Skill | Reusable knowledge, judgment, or an adaptable procedure | Description advertised; body loaded on invocation |
| Agent | Isolated context, specialized tools, or parallel work | Runs in a separate context |
| Hook or scripted workflow | Preconditions, ordering, retries, stop rules, and checks that must be enforced | Executed by code or the harness |

Numbered steps are not automatically a reason to leave the skill format. Move an operation into a hook, script, or workflow when correctness depends on guaranteed ordering, a required artifact, a retry policy, or a hard stop. Keep judgment in the skill, such as assessing ambiguity or choosing between acceptable trade-offs.

---

## Choose the Ownership Scope First

Sharing a skill does not require co-maintaining one universal copy. Frédéric Camblor's article [Un Skill n'est pas une librairie](https://devx.writizzy.blog/p/un-skill-nest-pas-une-lib) provides a useful warning: appropriation, local context, and silent behavioral drift can cost more than copying the file and specializing it.

Use one of four scopes:

| Scope | Location or channel | Maintenance contract |
|-------|---------------------|----------------------|
| Personal | `~/.claude/skills/` | Optimized for one person's habits; no compatibility promise |
| Project or team | `.claude/skills/` in Git | Shared conventions with a named owner and review path |
| Tool or vendor | Plugin or maintained repository | Versioned support for the tool's users |
| Marketplace or global | Registry or public repository | Discovery source by default; adopt only after review and local evaluation |

For security, treat any downloaded skill as an executable dependency because it can contain tool permissions, scripts, and instructions. For ownership, treat it as situated context: record its scope, owner, assumptions, and retirement signal. These are complementary rules.

---

## Creating Your First Skill

Skills live in directories named `.claude/skills/{skill-name}/`. The required file is `SKILL.md`.

### File Location

```text
my-project/
└── .claude/
    └── skills/
        └── testing-standards/
            └── SKILL.md
```

### Basic Structure

```markdown
---
name: testing-standards
description: Apply this project's Jest and Testing Library conventions when creating, reviewing, or debugging tests.
metadata:
  version: 1.0.0
---

# Testing Standards

## When to apply

Use for unit tests, component tests, mocks, fixtures, or coverage changes.
Do not use for end-to-end tests maintained by the QA repository.

## Test structure

1. Arrange the smallest realistic input.
2. Act through the public interface.
3. Assert behavior and user-visible effects.

## Verification

Run the changed test file, then the relevant package suite.
```

`name` and `description` are the core discovery fields. Custom metadata such as a version belongs under `metadata`. Fields such as `triggers`, `auto_invoke`, and `keywords` are not Claude Code skill frontmatter.

---

## Skill Discovery and Invocation

### Write the Description as a Routing Rule

Claude uses `description` to decide whether the skill is relevant. Include:

- What the skill does
- The situations where it should be used
- Important anti-triggers when adjacent tasks belong elsewhere

```yaml
description: Review PostgreSQL schema and query changes for indexes, locking, and migration safety. Use for SQL migrations and slow-query investigations; do not use for application-level API design.
```

### Control Who Can Invoke It

By default, both you and Claude can invoke a skill.

```yaml
# Manual only. Appropriate for deploy, commit, or message-sending workflows.
disable-model-invocation: true
```

```yaml
# Model only. Appropriate for background knowledge with no useful slash command.
user-invocable: false
```

There is no `auto_invoke: true` session-start mode. In a regular session, Claude receives available skill descriptions and loads a skill body only when invoked. An invoked body remains in the conversation; tool grants from `allowed-tools` last only for the invoking turn.

### Keep Tool Grants Narrow

`allowed-tools` pre-approves matching tools for the turn that invokes the skill. It does not remove other tools from Claude's toolset.

```yaml
allowed-tools: Read Grep Glob Bash(npm test *)
```

Review this field before using a third-party skill. A broad Bash grant can materially change its risk.

---

## Progressive Disclosure

Keep `SKILL.md` focused and move detailed material into supporting files:

```text
testing-standards/
├── SKILL.md
├── references/
│   ├── mocking.md
│   └── integration-tests.md
└── scripts/
    └── select-tests.sh
```

Link each supporting file from `SKILL.md` and say when to open or execute it. The official guidance recommends keeping `SKILL.md` under 500 lines.

---

## Common Skill Patterns

### Pattern 1: Project Conventions

Use a project skill when the advice depends on repository architecture, team decisions, or local tooling.

```markdown
---
name: python-standards
description: Apply this repository's Python typing, import, packaging, and pytest conventions when editing Python code.
---

# Python Standards

- Use type hints on public functions.
- Keep tests next to their package under `tests/`.
- Follow the repository's configured formatter and linter.
- Verify with the narrowest relevant pytest target first.
```

### Pattern 2: Domain Knowledge

```markdown
---
name: payment-processing
description: Apply this product's payment state machine, idempotency, and audit rules when changing checkout or refund flows.
user-invocable: false
---

# Payment Processing Rules

- Never log card data or payment secrets.
- Reuse the existing idempotency key at retry boundaries.
- Treat provider callbacks as untrusted and potentially duplicated.
- Verify state transitions against the canonical state machine.
```

### Pattern 3: Manual Workflow

```markdown
---
name: release-check
description: Prepare and verify a release candidate for this repository.
disable-model-invocation: true
---

# Release Check

1. Read the repository release instructions.
2. Verify the version and working tree.
3. Run the required checks.
4. Report blockers without publishing.
```

The model can adapt these steps. If publishing must never happen before a specific gate, enforce that gate in a script, hook, CI job, or workflow rather than relying on prose alone.

---

## Bundling and Sharing Skills

Project skills can be committed with the repository:

```text
my-project/
└── .claude/
    └── skills/
        ├── testing-standards/
        │   └── SKILL.md
        ├── api-design/
        │   └── SKILL.md
        └── security-checklist/
            └── SKILL.md
```

Teammates receive the files through Git, but discovery does not prove correct activation or output. Record the owner and assumptions in each skill, then run representative cases in fresh sessions.

Use public catalogs to discover patterns. Before adopting a third-party skill:

1. Read its full instructions, scripts, and tool grants.
2. Decide whether to consume it unchanged, fork it, or extract only the useful pattern.
3. State the local owner and support expectation.
4. Compare representative prompts with and without the skill.
5. Pin or record the reviewed version when updates could change behavior.

---

## Exercise: Create a Domain Skill

### Scenario

You are building an e-commerce site. Claude needs the project's product model when changing catalog and inventory code.

### Step 1: Create the Directory

```bash
mkdir -p .claude/skills/product-data-model
```

Save the following as `.claude/skills/product-data-model/SKILL.md`:

```markdown
---
name: product-data-model
description: Apply the product, SKU, price, and inventory model when changing catalog queries or stock behavior in this repository.
metadata:
  owner: commerce-team
  version: 1.0.0
---

# Product Data Model

## When to apply

Use for catalog, SKU, pricing, and inventory changes.

## Core rules

- A Product owns one or more SKUs.
- Price and inventory belong to the SKU, not Product.
- Inventory cannot become negative.
- Store monetary values using the repository's decimal type.

## Verification

- Check the schema and existing migrations before proposing SQL.
- Exercise out-of-stock and concurrent-order cases.
```

### Step 2: Test Discovery and Output Separately

Open fresh sessions for each case:

| Prompt | Expected routing |
|--------|------------------|
| "Add a query for products with fewer than five units" | Skill should invoke |
| "Change the marketing page headline" | Skill should not invoke |

For the positive case, inspect the result too: the skill should route correctly and the proposed change should follow the actual repository schema. Triggering alone is not success.

---

## Evaluation and Iteration

Test two independent properties:

1. **Trigger correctness**: does Claude invoke the skill on relevant prompts and avoid it on irrelevant prompts?
2. **Output quality**: when invoked, does the result satisfy explicit assertions?

Run each prompt in a fresh session with the skill enabled and disabled. The no-skill run is the baseline. Record the model, Claude Code version, prompt set, number of runs, assertions, pass counts, token use, and variance. A structural validator proves format, not behavioral quality.

The official `skill-creator` plugin can store cases in `evals/evals.json`, run isolated comparisons, produce grading evidence, benchmark with-skill against without-skill, compare versions blindly, and tune descriptions. LLM grading and self-critique remain evidence generators, not independent proof. Review important outputs with deterministic checks or a qualified human.

Choose acceptance thresholds from the risk and failure cost of the specific skill. A universal pass-rate target hides the denominator, variance, and severity of individual failures.

---

## Skill Lifecycle

1. **Scope**: choose personal, project/team, tool/vendor, or marketplace/global ownership.
2. **Baseline**: collect representative prompts before adding the skill.
3. **Create**: write the smallest useful `SKILL.md` and supporting files.
4. **Evaluate**: test routing and output quality in fresh sessions.
5. **Observe**: capture real misses, guesses, and wrong-context activations.
6. **Review**: propose changes, then re-run the baseline before accepting them.
7. **Retire**: turn off or remove skills that are unused, stale, redundant, or harmful.

Run `/skill-doctor` in the terminal to inspect context cost and unused skills. Its report excludes bundled and enterprise skills, is unavailable through Remote Control, and requires feature-flag fetching. Treat an unused flag as a review signal, not an automatic deletion order.

Do not archive a retired skill under `.claude/skills/`, because nested discovery can keep it visible. Preserve it in Git history or move it outside discovered skill directories with a dated retirement note.

---

## Best Practices

### Do

- Keep one clear responsibility per skill.
- Write the description as a routing rule.
- Record scope, owner, assumptions, and retirement criteria.
- Keep the main file short and link supporting material.
- Review third-party instructions, scripts, and permissions before use.
- Compare with and without the skill in fresh sessions.
- Put guaranteed gates in code, hooks, CI, or workflows.

### Don't

- Put temporary or one-time instructions in `CLAUDE.md`; use the current prompt.
- Treat a marketplace install as a maintenance contract.
- Infer output quality from successful invocation.
- Accept self-critique as validation without external checks.
- Keep dormant skills in discovered directories.
- Add generic branches that dilute the project's common case.

---

## Validation: You're Ready If...

✓ Your skill is stored at `.claude/skills/{name}/SKILL.md`

✓ Its `description` covers triggers and important anti-triggers

✓ You can explain its ownership scope and maintenance contract

✓ You tested relevant and irrelevant prompts in fresh sessions

✓ You compared output with and without the skill

✓ You know which guarantees belong in a hook, script, CI job, or workflow

✓ You defined how to review and retire the skill

---

## Sources

- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Agent Skills open standard](https://agentskills.io/)
- [Frédéric Camblor: Un Skill n'est pas une librairie](https://devx.writizzy.blog/p/un-skill-nest-pas-une-lib)

---

## What's Next?

**Module 06: Hooks & Events** covers:

- Automating responses to system events
- Pre-commit validation
- Post-action notifications
- Building enforceable automation

---

**Completed Module 05?** → Ready for [Module 06: Hooks & Events](06-hooks.md)
