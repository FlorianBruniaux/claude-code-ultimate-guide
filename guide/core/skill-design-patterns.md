---
title: "Skill Design Patterns"
description: "Architectural patterns for designing robust, token-efficient Claude Code skills with multi-agent pipelines"
tags: [skills, architecture, multi-agent, patterns, design]
---

# Skill Design Patterns

> **Related**: [Development Methodologies](./methodologies.md) | [Multi-Agent Coordination](../ultimate-guide.md#920-agent-teams-multi-agent-coordination)

Practical patterns for skills that go beyond a single-agent, single-file prompt. These patterns address specific failure modes: sub-agents that re-discover the same facts, rules that apply to the wrong files, skills that blur detection with remediation.

---

## Shared Ground Truth Injection

**Problem**: When you launch N parallel sub-agents to audit or analyze a set of artifacts, each agent independently discovers the same baseline facts (file list, nav structure, CLI commands, schema). That is N redundant reads, N independent facts to trust, and N chances for one agent to see a stale file state.

**Pattern**: The orchestrator computes a shared factual baseline once, then injects the same block verbatim into every sub-agent prompt.

```
Orchestrator (Phase 1)
  ├── Read nav structure → extract groups
  ├── Glob files → get current list
  ├── List CLI commands → get current commands
  └── Compile into "Ground Truth" string

Orchestrator (Phase 2)
  ├── Agent 1 prompt: "## Ground Truth\n{shared block}\n\n## Your Scope\nSection A"
  ├── Agent 2 prompt: "## Ground Truth\n{shared block}\n\n## Your Scope\nSection B"
  └── Agent 3 prompt: "## Ground Truth\n{shared block}\n\n## Your Scope\nSection C"
```

**What goes in the shared block**:
- Navigation or file hierarchy (so each agent knows what exists)
- Current CLI commands or API endpoints (to catch references to removed commands)
- Domain entity list (packages, modules, services)
- Current date (to catch version references that are now stale)

**Why it works**: Each agent starts from the same snapshot. An agent cannot hallucinate a CLI command that exists if the ground truth list shows it does not. The orchestrator is the single source of truth for structure; sub-agents are the single source of truth for their assigned section's content.

**Token trade-off**: The shared block adds tokens to every sub-agent prompt. For a 5-agent parallel audit, a 500-token ground truth block costs 2,500 tokens upfront. Eliminating per-agent re-discovery saves that cost, and then some. Size the block to what is actually needed, not everything you could include.

**Implementation note**: The ground truth block should be a string, not a file reference. If you point agents to "read `docs.json`", each agent reads it independently. Compile it once in the orchestrator and paste it in.

> Observed in the [Packmind doc-audit skill](https://github.com/packmind/packmind) (.claude/skills/doc-audit/SKILL.md, Phase 1). See [Credits](./credits.md).

---

## Pre-filtered References via Frontmatter Paths

**Problem**: You have a set of rules files (coding standards, security policies, style guides). Each one applies to a specific subset of files in the codebase. If you pass all rules to a review agent, the agent applies rules to files they were not written for, producing false positives and wasting context.

**Pattern**: Add a `paths:` frontmatter field to each rule file with a glob pattern. Before launching review agents, the orchestrator reads this frontmatter, matches the globs against the list of modified files, and passes each agent only the rules that apply.

```yaml
# .claude/rules/standard-testing-good-practices.md
---
name: Testing Good Practices
paths: "**/*.spec.ts,**/*.test.ts"
alwaysApply: false
description: Testing conventions for TypeScript unit and integration tests
---

## Rules
- Use `describe` blocks for grouping related tests
...
```

Orchestrator logic (plain steps):

```
1. Glob .claude/rules/**/*.md → list all rule files
2. For each rule file:
   a. Read YAML frontmatter → extract paths (glob pattern)
   b. If alwaysApply: true → include unconditionally
   c. If alwaysApply: false → match paths against modified files list
   d. Include if at least one modified file matches the glob
3. Pass the filtered rule set to each review agent
```

**Key benefits**:
- A test file is not checked against backend security rules
- A migration file is not checked against frontend style guides
- Each agent's context contains only actionable rules for what it is reviewing

**Scaling**: With 50 rules files, a typical PR touching 8 TypeScript spec files might match 3 rules. Without filtering, the agent reads 50 rules. With filtering, it reads 3. The signal-to-noise ratio for the agent improves proportionally.

**When to add `paths:` frontmatter**: Any rule that has a clear file-type scope (test files, migration files, frontend components, API routes). Rules that are truly global use `alwaysApply: true` and skip the matching step.

> Observed in the [Packmind qa-review skill](https://github.com/packmind/packmind) (.claude/skills/qa-review/SKILL.md, Phase 5). See [Credits](./credits.md).

---

## Detection-Only Scope Boundary

**Problem**: A skill that both detects issues and fixes them has two failure modes: false positives (detected and fixed something that was not a problem) and incomplete fixes (detected correctly but fixed wrong). Mixing the two makes both worse, and gives the user no review checkpoint.

**Pattern**: Explicitly scope skills to detection only. The skill produces a report. Remediation is a separate step, triggered by the user after reading the report.

State this at the top of the skill:

```markdown
**This skill only detects issues. It does not fix them.**
```

Then enforce it: no file writes, no edits, no git commits inside the skill. Output is always a markdown report or console findings.

**When to break this rule**: Skills that are specifically designed for automated remediation (codemod-style skills, dependency update skills) are the exception. They should be explicit that they write changes, and should include a dry-run mode.

**The practical value**: Detection-only skills are safe to run on main, in CI, and against production configs. A user can invoke one without fear of unintended changes, which makes them worth running more often and on more codebases.

> Recurring pattern across qa-review, playbook-audit, and doc-audit in the [Packmind repo](https://github.com/packmind/packmind) (Apache 2.0). See [Credits](./credits.md).

---

## Input-Handler Dispatch

**Problem**: A skill that handles two or more heterogeneous input types (images vs text, GitHub issues vs design mockups) either grows a complex branching main file or becomes too rigid for varied entry points.

**Pattern**: Store one input-handler file per input type in an `inputs/` subdirectory. The main SKILL.md asks the user which type applies, then loads the matching handler file.

```
.claude/skills/my-skill/
├── SKILL.md                 # Orchestrator: asks user, dispatches to input handler
└── inputs/
    ├── github-issue.md      # Handler for GitHub issue input
    └── visual-mockup.md     # Handler for screenshot/image input
```

SKILL.md (abridged):

```markdown
## Step 1: Identify Input Type

Ask the user: "Are you providing a GitHub issue or a visual mockup?"

- If GitHub issue → follow the instructions in `inputs/github-issue.md`
- If visual mockup → follow the instructions in `inputs/visual-mockup.md`
```

Each handler file contains the full parsing instructions for that input type, including field extraction, format normalization, and validation. The main file stays clean.

**When to use it**: When input types require substantially different parsing logic (not just different field names). If two inputs differ by less than 5 steps, handle them inline. The pattern pays off when handlers would each exceed 100 lines.

> Observed in the [Packmind create-em-spec skill](https://github.com/packmind/packmind) (.claude/skills/create-em-spec/inputs/). See [Credits](./credits.md).

---

## Versioned Sub-directories for Tool-Version Coupling

**Problem**: A skill wraps a CLI tool that changes behavior between versions. The skill needs to detect which version the user has and adapt its instructions accordingly.

**Pattern**: Store one subdirectory per tool version, each containing the version-specific instructions:

```
.claude/skills/update-playbook/
├── SKILL.md                         # Detects CLI version, dispatches
└── tool-versions/
    ├── v1.21/
    │   └── apply-changes.md         # Instructions for v1.21
    ├── v1.23/
    │   └── apply-changes.md         # Instructions for v1.23 (different API)
    └── v1.24/
        └── apply-changes.md         # Instructions for v1.24 (breaking change)
```

SKILL.md detects the version at runtime:

```markdown
## Step 1: Detect Tool Version

Run: `my-cli --version`

- If output starts with "1.21" → read `tool-versions/v1.21/apply-changes.md`
- If output starts with "1.23" → read `tool-versions/v1.23/apply-changes.md`
- If output starts with "1.24" → read `tool-versions/v1.24/apply-changes.md`
- If version not recognized → stop and tell the user which versions are supported
```

**Anti-pattern to avoid**: Do not create a `my-skill-v2/` directory alongside the original `my-skill/`. Version the *content inside* the skill, not the skill itself. Two near-identical skills are harder to maintain and confusing to invoke.

**When to use it**: When a CLI tool you wrap has breaking changes between versions and you need to support multiple versions simultaneously. If you only need to support the latest version, just update the skill in place.

> Observed in the [Packmind update-playbook skill](https://github.com/packmind/packmind) (.claude/skills/packmind-update-playbook/). See [Credits](./credits.md).

---

## Two-Tier Standards

**Problem**: A comprehensive coding standard is long (1,000-5,000 words). Loading the full standard into context for every file review inflates token cost and dilutes attention.

**Pattern**: Store a short summary (100-300 words, with a `paths:` frontmatter glob) in `.claude/rules/`. Keep the full canonical standard in a separate location that Claude can read on demand.

```
.claude/rules/standard-testing.md          # Summary + paths glob (200 words)
.standards/standard-testing-full.md        # Full canonical standard (2,000 words)
```

The summary in `.claude/rules/` includes:
- 3-5 prescriptive rules (imperative voice: "Use X", "Do not Y")
- `paths:` frontmatter so it only loads for matching files
- A link to the full standard for cases where detail is needed

The full canonical standard lives outside `.claude/rules/` so it does not auto-load.

**When to use it**: Teams with more than 10 rule files, or rule files that average more than 500 words. For smaller configurations, a single-tier approach is simpler.

**Maintenance**: When you update the canonical standard, update the summary too. The two-tier split creates a duplication risk. Mitigate it by keeping the summary to bullet-point rules only (no prose) so it changes infrequently.

> Observed in the [Packmind rules configuration](https://github.com/packmind/packmind) (.claude/rules/packmind/). See [Credits](./credits.md).

---

## Plans and Specs as Committed Artifacts

**Problem**: Session-scoped plans (`/plan` mode, scratchpad files) disappear when the session ends. The next session has no searchable record of why a design decision was made, which options were considered, or which implementation step was last completed.

**Pattern**: Commit plans and their associated design specs directly into `.claude/` as dated markdown pairs:

```
.claude/
├── plans/
│   └── 2026-03-15-auth-refactor.md        # High-level plan: phases, tasks, commit messages
└── specs/
    └── 2026-03-15-auth-refactor-design.md  # Companion spec: context, alternatives, rationale
```

The plan file contains the implementation breakdown with explicit commit messages per task:

```markdown
# Auth Refactor Plan

## Task 1: Extract token validation middleware
- Move validation logic from controller into `middleware/auth.ts`
- git commit -m "refactor(auth): extract token validation into middleware"

## Task 2: Add refresh token rotation
- Implement rotation logic with 7-day expiry
- git commit -m "feat(auth): add refresh token rotation with 7-day expiry"
```

The spec file captures what informed the plan: constraints, rejected alternatives, and the reasoning that will not be obvious from the code six months later:

```markdown
# Auth Refactor Design

## Context
Session token storage flagged by legal review (ISO 27001 compliance gap).
Rotation required per new internal security policy v2.3.

## Rejected approaches
- HttpOnly cookie approach: requires cross-domain config changes (deferred)
- Redis session store: ops team not ready to manage another stateful service
```

Both files are committed together and stay in the repo indefinitely.

**Why it is better than session-only plans**: Committed plans are greppable, diffable, and resume-able. A new session can read `.claude/plans/` to understand in-progress work without reconstructing it from git log. The spec captures the reasoning that disappears from memory but matters when revisiting a decision six months later.

**Naming convention**: `YYYY-MM-DD-<slug>.md` for the plan, `YYYY-MM-DD-<slug>-design.md` for the companion spec, both with the same date and slug. This keeps pairs visually associated in directory listings.

**When to use it**: Multi-session implementation tasks where continuity matters. Not worth the overhead for a single-session task that fits in one commit. The threshold is roughly: if the work spans more than one day or more than one Claude session, commit the plan.

> Observed in the [Packmind .claude/plans/](https://github.com/packmind/packmind) convention (Apache 2.0). See [Credits](./credits.md).

---

## Runtime Prompt Logging

**Problem**: When an AI provider call times out or crashes, the exact prompt that was sent is gone. If you are building a skill or evaluation pipeline with multiple agents running in parallel, you lose the ability to diagnose what each agent was told. The `--debug` flag only helps when you remember to pass it.

**Pattern**: Write the prompt to disk as a blocking operation BEFORE invoking the provider. Use a persistent directory with a timestamped filename. Never throw from the logging call.

```typescript
// Run BEFORE provider.invoke(), not after
await writeFile(
  `prompts/debug/${evaluatorName}-${timestamp}.md`,
  fullPrompt,
  "utf-8",
);
// Only now call the provider
const response = await provider.invoke(fullPrompt);
```

Three constraints make this pattern work:

1. **Blocking write** (`await`, not fire-and-forget): the file exists on disk before the provider call starts. A crash during the provider call leaves the prompt intact for inspection.
2. **Always-on** (not gated by a debug flag): the overhead is a single file write per agent. The benefit is that any unexpected result has a permanent record.
3. **Never throw**: logging failures must not break evaluations. Wrap the write in try/catch, log a warning on failure, continue.

**Directory convention**: Use a project-root-relative path (`prompts/debug/` or `claudedocs/debug/`) rather than a temp directory. Temp directories get cleaned up; you want these to persist across runs.

**Token cost**: Zero (disk I/O that happens outside the AI call). The prompt is already in memory, you are just persisting it.

**When to use it**: Any skill that calls an AI provider and where the prompt is assembled dynamically (not just a static string). The value is proportional to prompt complexity: if your prompt injects ground truth, evaluator instructions, and file content, a single write before the call is cheap insurance.

> Observed in [PackmindHub/context-evaluator](https://github.com/PackmindHub/context-evaluator) (`src/shared/evaluation/runtime-prompt-logger.ts`, MIT). See [Credits](./credits.md).

---

## Adaptive Unified/Parallel Mode

**Problem**: You have N files to evaluate and need to decide: send all files to one agent (better for cross-file issues, higher context cost) or send each file to its own parallel agent (cheaper, faster, but blind to contradictions across files)?

**Pattern**: Estimate the combined token count before committing to a strategy. If the total fits within a threshold, use unified mode (one agent sees everything). If it exceeds the threshold, fall back to independent parallel agents per file.

```typescript
const DEFAULT_MAX_UNIFIED_TOKENS = 100_000;

function canUseUnifiedMode(context: MultiFileContext, maxTokens = DEFAULT_MAX_UNIFIED_TOKENS) {
  if (context.totalTokenEstimate > maxTokens) {
    return {
      viable: false,
      reason: `Combined content (~${context.totalTokenEstimate} tokens) exceeds limit (${maxTokens})`,
    };
  }
  return { viable: true };
}
```

Call this before building your agent prompts. The decision gates the rest of the pipeline:

```
estimateTokens(all files)
  ↓
< 100K → runUnifiedEvaluation(allFiles)   // 1 agent, cross-file detection
> 100K → runAllEvaluators(file)           // N agents, per-file, parallel
```

**Why the threshold matters**: In unified mode, the agent can see contradictions between a root `CLAUDE.md` and a subdirectory `CLAUDE.md`. In parallel mode, each agent sees only one file and cannot detect those contradictions. The threshold preserves cross-file intelligence for smaller repos while staying within practical context limits for larger ones.

**Threshold calibration**: 100K tokens leaves room for the evaluator prompt (typically 2-5K) and the model's response buffer. For your own use case, set the threshold to `model_context_window - evaluator_prompt_tokens - response_buffer`. Pac's `DEFAULT_MAX_UNIFIED_TOKENS = 100_000` is a conservative default for most current models.

**Token estimation**: You do not need an exact count. A rough estimate (`chars / 4` for most English text) is sufficient for the mode decision. The cost of occasionally being 10% wrong on the estimate is much lower than the cost of the extra precision.

> Observed in [PackmindHub/context-evaluator](https://github.com/PackmindHub/context-evaluator) (`src/shared/evaluation/runner.ts` `canUseUnifiedMode()`, MIT). See [Credits](./credits.md).

---

## Multi-Directory Skill Discovery for Cross-CLI Compatibility

**Problem**: A repository is worked on with more than one AI coding CLI (Claude Code, plus Codex, Amp, or another harness). Each CLI expects skills or environment config in its own conventional directory. Consolidating everything into one directory means most CLIs never discover it; three near-duplicate directories look, at first glance, like disorganization.

**Pattern**: Keep one skill directory per CLI convention side by side at the repo root, each holding CLI-specific skills rather than copies of the same content: `.claude/skills/` for Claude Code, `.agents/skills/` for a shared or generic agent convention, `.skills/` for a project-level shared set any CLI can be pointed at, and `.codex/environments/` for Codex-specific environment config. Read as convergence on a multi-CLI repository, not clutter: each directory is a distinct, real discovery path, not a redundant copy.

```
.claude/skills/      # 3 skills, Claude Code's own convention
.agents/skills/       # shared/generic agent convention
.skills/              # 6 skills: cli-release, effect-atom-optimistic-updates,
                      #   effect-http-testing, effect-use-pattern, graphite,
                      #   warden-security-review
.codex/environments/  # Codex-specific environment config
```

**A related convention worth borrowing separately**: a curated "References" section in the project README, naming the codebases the team deliberately points its coding agent at as patterns to imitate (a plugin system, a storage adapter, a general code style). This is distinct from the skill directories above, a reading list for the agent rather than a discovery path, but it serves the same goal: making implicit "the agent already knows what good looks like here" knowledge explicit and versioned instead of tribal.

**When to use it**: Any repository worked on by more than one AI CLI where the CLIs do not share a skill-discovery convention. For a single-CLI repository, one directory is simpler and this pattern adds nothing.

> Observed in [UsefulSoftwareCo/executor](https://github.com/UsefulSoftwareCo/executor) (MIT). Full evaluation, including the repo's other agentic-engineering conventions: [`docs/resource-evaluations/executor-integration-governance-layer.md`](../../docs/resource-evaluations/executor-integration-governance-layer.md).

---

## See Also

- [Development Methodologies](./methodologies.md): TDD, SDD, BDD, multi-agent orchestration
- [§9.20 Agent Teams](../ultimate-guide.md#920-agent-teams-multi-agent-coordination): Agent Teams including Skeptical Reviewer Pattern
- [Credits](./credits.md): Full attribution for external sources
- `examples/skills/mcp-integration-reference/`: MCP Reference File Pattern template
