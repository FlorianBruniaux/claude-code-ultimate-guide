---
title: "Dynamic Workflows"
description: "JavaScript-orchestrated multi-agent pipelines with deterministic control flow, parallel fan-out, and automatic resume"
tags: [workflow, agents, orchestration, parallel, ultracode]
---

# Dynamic Workflows

> **JavaScript scripts that orchestrate tens to hundreds of subagents in one session**
> **Introduced**: v2.1.154 (2026-05-28) | **Trigger keyword**: `ultracode` (renamed from `workflow` in v2.1.160, breaking change) | **Monitor**: `/workflows`

**What**: A dynamic workflow is a JavaScript file that orchestrates multiple subagents using a small set of primitives (`agent`, `parallel`, `pipeline`, `phase`). The script itself runs as the orchestrator and consumes zero tokens; all token cost comes from the `agent()` calls it makes. The runtime handles concurrency caps, schema validation, progress reporting, and resume on interruption.

**When introduced**: v2.1.154 (2026-05-28). The trigger keyword was `workflow` until v2.1.160, where it was renamed to `ultracode` (breaking change; existing scripts using the old keyword must be updated).
**Reading time**: ~40 min
**Prerequisites**: Familiarity with the [Agent tool](../core/tools-reference.md#agent), basic JavaScript async/await

---

## Table of Contents

1. [When to use workflows (vs Agent tool vs Skills)](#1-when-to-use-workflows-vs-agent-tool-vs-skills)
2. [Primitive reference](#2-primitive-reference)
3. [Behavioral guarantees](#3-behavioral-guarantees)
4. [pipeline() vs parallel(): when and why](#4-pipeline-vs-parallel--when-and-why)
5. [Schema-structured outputs across phases](#5-schema-structured-outputs-across-phases)
6. [Common patterns](#6-common-patterns)
7. [Real workflow example: dev-flow (Issue to PR)](#7-real-workflow-example-dev-flow-issue-to-pr)
8. [When NOT to use workflows](#8-when-not-to-use-workflows)
9. [Cost and performance notes](#9-cost-and-performance-notes)
10. [See also](#10-see-also)

---

## 1. When to use workflows (vs Agent tool vs Skills)

Three tools in Claude Code can spawn subagents: the Agent tool, Skills, and dynamic workflows. Picking the wrong one adds overhead without benefit, so the choice matters.

**Use the Agent tool directly** when the task is a single subagent doing one thing. The Agent tool is the building block. Wrapping a single `agent()` call in a workflow file adds a round-trip and a script to maintain for no gain.

**Use a Skill** when the procedure is reusable across projects and Claude should choose the steps dynamically based on context. Skills are prompt-driven and load into the conversation. They do not provide parallelism, resume, or structured handoffs between stages.

**Use a dynamic workflow** when three or more of these conditions hold: the task has multiple stages that feed into each other, some stages can run in parallel, the job is long enough that resume-on-interruption matters, you want reproducible output (the same inputs always produce the same orchestration path), or you need structured JSON schemas to reliably pass data between stages.

The official guidance distills to: single subagent, one task, use the Agent tool; reusable procedure where Claude picks steps, use a Skill; multi-stage, parallelizable, reproducible, or long-running, use a Workflow.

| Criterion | Agent tool | Skill | Dynamic Workflow |
|-----------|-----------|-------|-----------------|
| Parallelism | No | No | Yes (parallel / pipeline) |
| Resume on interruption | No | No | Yes (deterministic replay) |
| Structured data handoff | Manual | Manual | Built-in (schema validation) |
| Orchestrator token cost | Moderate | Moderate | Zero |
| Setup overhead | None | Low | One JS file |
| Reusable across projects | No | Yes | Via workflow() nesting |

---

## 2. Primitive reference

A workflow file is a JavaScript module with two mandatory parts: a `meta` export (the structural backbone) and a default export function (the execution body). The runtime injects a small set of globals into the function's scope.

### meta (mandatory, pure literal)

`meta` must be the first statement in the file. It declares the workflow's identity and, optionally, the named phases that appear in the `/workflows` UI.

```js
export const meta = {
  name: 'audit-and-verify',
  description: 'Review every changed file, then verify each finding',
  phases: [
    { title: 'Review' },
    { title: 'Verify' },
  ],
};
```

The `name` and `description` fields are required. `phases` is optional but recommended: it populates the progress sidebar in `/workflows` so you can see which phase is running at a glance.

`meta` must be a pure literal. No variables, no template strings, no function calls, no spread operators. This constraint exists because the runtime extracts `meta` statically before executing the script, which is what makes phase headers visible in the UI before the workflow starts. Any expression that requires evaluation breaks static extraction.

The `meta` and the `phase()` calls form the "warp" (the fixed structural backbone of the run). The `agent()`, `parallel()`, and `pipeline()` calls are the "weft" that does the actual work woven through that backbone.

### agent(prompt, options?)

`agent()` is the core building block. Every call creates a separate subagent with its own isolated context window. Subagents do not share state; all information must be passed explicitly via the prompt.

```js
export default async function ({ agent, parallel, pipeline, phase, log, args, budget }) {
  const summary = await agent('Summarize the diff in src/api/ added since yesterday.', {
    label: 'API diff summary',
    phase: 'Analyze',
    model: 'claude-sonnet-5',
  });

  return summary;
}
```

`agent()` returns plain text by default. When `opts.schema` is provided (a JSON Schema object), the runtime validates the response and retries automatically until the output matches the schema. This is the mechanism that makes structured multi-phase pipelines reliable: downstream stages can depend on field names without fragile regex parsing.

Key options:

| Option | Type | Purpose |
|--------|------|---------|
| `schema` | JSON Schema object | Structured output. Runtime validates and retries on mismatch. |
| `phase` | string | Groups this call under a named phase in the `/workflows` UI. |
| `label` | string | Short progress label displayed while the agent runs. |
| `model` | string | Override model for this specific call. |
| `isolation` | `'worktree'` | Run agent in an isolated git worktree copy of the repo. Expensive; use only when agents mutate files in parallel and would conflict. |

### parallel(thunks[])

`parallel()` takes an array of zero-argument functions (thunks), launches all of them concurrently, and returns when the slowest one finishes. Results come back in input order regardless of completion order.

```js
const MODULES = ['auth', 'payments', 'notifications'];

const reviews = await parallel(
  MODULES.map((mod) => () =>
    agent(`Review the ${mod} module for security issues.`, {
      phase: 'Review',
      label: mod,
    })
  )
);
```

`parallel()` is a barrier primitive. Nothing after it runs until every agent in the array has returned. Failed agents return `null`, so filter before use:

```js
const valid = reviews.filter(Boolean);
```

Use `parallel()` when all results must be available before the next step can begin: synthesizing across all findings, deduplicating across outputs, or making an early-exit decision based on the total count.

### pipeline(items, ...stages)

`pipeline()` processes an array of items through a sequence of transformation stages. Each item passes through every stage in order, but different items can be at different stages simultaneously. A pipeline with 10 items and 3 stages can have item 1 in stage 3 while item 7 is still in stage 1.

```js
const DIMENSIONS = [
  { id: 'security', prompt: 'Review for injection and auth issues.' },
  { id: 'performance', prompt: 'Review for N+1 queries and slow paths.' },
  { id: 'accessibility', prompt: 'Review for WCAG 2.1 AA compliance.' },
];

const results = await pipeline(
  DIMENSIONS,
  // Stage 1: generate findings
  (dim) =>
    agent(dim.prompt, {
      phase: 'Review',
      label: dim.id,
      schema: FINDINGS_SCHEMA,
    }),
  // Stage 2: verify each finding
  (findings) =>
    parallel(
      findings.issues.map((issue) => () =>
        agent(`Try to refute this finding: "${issue.title}". Is it a real problem?`, {
          phase: 'Verify',
          label: issue.title,
          schema: VERDICT_SCHEMA,
        })
      )
    )
);
```

Stage functions receive three arguments: `(previousStageResult, originalItem, index)`. Using `originalItem` in later stages is common when the prompt for stage 2 needs both the stage 1 result and the original input.

There is no global barrier between stages across different items. This is what makes `pipeline()` efficient for independent items that share the same stage sequence.

### phase(title)

`phase()` is an observability primitive. It updates the active phase header in the `/workflows` UI for all subsequent `agent()` calls that do not specify their own `opts.phase`.

```js
phase('Discovery');
const files = await agent('Find all TypeScript files modified in the last 24 hours.');

phase('Analysis');
const issues = await parallel(/* ... */);

phase('Report');
const report = await agent('Synthesize these findings into an executive summary.');
```

For fine-grained grouping within `pipeline()` or `parallel()`, pass `phase` as an option directly to `agent()` rather than calling the global `phase()` function, which would race with concurrent calls.

### Other injected globals

Beyond `agent`, `parallel`, `pipeline`, and `phase`, the runtime injects four more globals:

**`log(message)`** emits a workflow-level progress message visible in the `/workflows` UI and in the terminal. Use it to mark major transitions or report intermediate counts.

```js
log(`Found ${specs.length} specs in approved status. Starting analysis.`);
```

**`args`** contains runtime inputs passed by the user or by a parent workflow. Treat it as a plain object; its shape depends on what the caller provided.

```js
const { issueNumber, targetBranch = 'main' } = args;
```

**`budget`** exposes token accounting for the running workflow. `budget.total` is the configured maximum; `budget.spent()` returns current usage; `budget.remaining()` returns headroom. Guard open-ended loops with this:

```js
while (budget.remaining() > 50_000) {
  const batch = await agent('Find the next 10 unreviewed specs.');
  if (!batch.length) break;
  // process batch...
}
```

**`workflow(nameOrRef, args?)`** runs a named sub-workflow inline. One level of nesting is supported. Pass the sub-workflow's name string or import reference:

```js
const auditResult = await workflow('security-audit', { target: 'src/api' });
```

---

## 3. Behavioral guarantees

### Determinism constraints

The orchestrator script must be pure. Several constructs are unavailable or throw:

- `Date.now()`, `Math.random()`, and `new Date()` without arguments are blocked. Pass timestamps and seeds through `args` instead.
- `require`, `fs`, `process`, and any network call are unavailable in the orchestrator scope. All interaction with the environment happens inside `agent()` prompts, where the agent has full tool access.

The reason for these constraints is resume. When an interrupted workflow restarts, the runtime replays the orchestrator script from the top and replays cached results for already-completed `agent()` calls. If the orchestrator contained `Date.now()` or `Math.random()`, replay would produce different branch decisions, making the cached results inconsistent with the new execution path. Determinism is what makes resume safe.

### Schema validation and retry

When `agent()` is called with `opts.schema`, the runtime validates the returned text as JSON against that schema. If validation fails, the runtime retries the agent call with an automatic correction prompt. This retry loop is invisible to the orchestrator: `agent()` only resolves when the output is valid. The practical effect is that downstream stages can destructure `result.fieldName` without defensive checks, because the runtime guarantees the shape.

### Concurrency caps and queue

Concurrent `agent()` calls are capped at `min(16, cpu_cores - 2)`. Calls beyond the cap are queued automatically and drain as running agents complete. This means you can safely write `parallel(items.map(...))` for large arrays; the runtime prevents thundering-herd without any manual batching in the orchestrator.

Two hard limits protect against runaway scripts:

- Total `agent()` calls across a workflow: capped at 1000.
- Items per single `parallel()` or `pipeline()` call: capped at 4096.

If your workflow design would exceed 1000 agents, the task needs decomposition into sub-workflows or a different approach.

### Resume and result caching

Progress is checkpointed continuously. When a workflow is interrupted (Ctrl+C, network drop, machine restart), resuming it replays the orchestrator script but serves cached results for every `agent()` call that completed before the interruption. Cold-path agents run; warm-path agents return instantly. For a 200-agent workflow interrupted at agent 150, the resume cost is only the remaining 50 agents.

---

## 4. pipeline() vs parallel(): when and why

This is the most common source of performance problems in workflow design. The two primitives look similar but have fundamentally different semantics.

**`parallel()` is a barrier.** It launches N agents concurrently and blocks until the last one finishes. Nothing runs after the `await parallel(...)` line until every agent in the array has returned. Wall-clock time equals the slowest agent's time.

**`pipeline()` is streaming.** Items flow through stages without a global barrier between stages across items. Item 3 can enter stage 2 while item 7 is still in stage 1. Wall-clock time depends on pipeline depth and individual stage durations, not on the slowest item completing all stages before any other item starts.

The conceptual question to ask: "does step N need all results from step N-1 before it can start?" If yes, `parallel()` is correct. If items are independent and each one just needs its own previous-stage result, `pipeline()` is correct.

### Performance data

A community benchmark comparing the two primitives on equivalent work (3 items, 2 stages each) produced these numbers:

| Design | Token cost | Wall-clock |
|--------|-----------|-----------|
| `parallel()` barrier, 3 concurrent agents | ~78,844 tokens | ~8.4s |
| Mis-designed `pipeline()`, 3 items x 2 stages | ~158,982 tokens | ~26.7s |

The underlying work was identical. The `pipeline()` version added 2x tokens and 3x latency because the design forced a barrier at stage boundaries that the data did not require.

### Decision rule

Start every multi-item workflow with `pipeline()`. Only introduce a `parallel()` barrier when you can articulate a specific reason: "stage 2's prompt references all of stage 1's outputs" or "I need to early-exit if the total count across all items is zero."

Concrete examples where a `parallel()` barrier is justified:
- Deduplication across all findings before presenting results to the user
- A synthesis stage whose prompt literally says "given all the findings from the previous stage..."
- An early-exit check: if no item in stage 1 returned findings, skip stage 2 entirely

Concrete examples where `pipeline()` is the right choice:
- Review each file for security issues, then verify each finding per file independently
- Generate a summary for each spec, then format each summary into a report card
- Analyze each module, then produce a scorecard per module

### Misuse patterns to avoid

**Using `pipeline()` for independent dimensions that belong in `parallel()`**: If the dimensions are truly orthogonal (security review vs. performance review vs. accessibility review) and no stage needs cross-dimension data, `parallel()` gives a barrier once at the end and is simpler.

**Using `parallel()` when items are independent**: If 50 files each go through review + verify independently, wrapping all 100 agent calls in one `parallel([...50 reviews, ...50 verifies])` collapses the stage structure and makes the code unreadable. `pipeline()` keeps the stages explicit.

**Open-ended loops without a `budget` guard**: A `while(true)` discovery loop that keeps spawning agents until it "finds no more items" will hit the 1000-agent cap and fail. Guard every loop:

```js
while (dry < 3 && budget.remaining() > 30_000) {
  // ...
}
```

---

## 5. Schema-structured outputs across phases

Schemas are what turn a multi-phase pipeline from a chain of text-to-text transformations into a typed pipeline with reliable field access at every stage.

### Defining schemas

JSON Schema objects inline in the workflow file:

```js
const FINDINGS_SCHEMA = {
  type: 'object',
  required: ['issues'],
  properties: {
    issues: {
      type: 'array',
      items: {
        type: 'object',
        required: ['title', 'description', 'severity'],
        properties: {
          title: { type: 'string' },
          description: { type: 'string' },
          severity: { type: 'string', enum: ['low', 'medium', 'high', 'critical'] },
        },
      },
    },
  },
};

const VERDICT_SCHEMA = {
  type: 'object',
  required: ['isReal', 'reason'],
  properties: {
    isReal: { type: 'boolean' },
    reason: { type: 'string' },
  },
};
```

### Discovery → Understand → Plan

A three-phase pipeline where each phase builds on the previous:

```js
export const meta = {
  name: 'spec-processor',
  description: 'Discover approved specs, understand each one, produce implementation plan',
  phases: [
    { title: 'Discovery' },
    { title: 'Understand' },
    { title: 'Plan' },
  ],
};

const DISCOVERY_SCHEMA = {
  type: 'object',
  required: ['specs'],
  properties: {
    specs: {
      type: 'array',
      items: {
        type: 'object',
        required: ['id', 'title', 'path'],
        properties: {
          id: { type: 'string' },
          title: { type: 'string' },
          path: { type: 'string' },
        },
      },
    },
  },
};

const UNDERSTANDING_SCHEMA = {
  type: 'object',
  required: ['id', 'summary', 'dependencies', 'estimatedComplexity'],
  properties: {
    id: { type: 'string' },
    summary: { type: 'string' },
    dependencies: { type: 'array', items: { type: 'string' } },
    estimatedComplexity: { type: 'string', enum: ['low', 'medium', 'high'] },
  },
};

export default async function ({ agent, parallel, phase, log }) {
  phase('Discovery');
  const discovery = await agent(
    'Find every spec file in docs/specs/ with status: approved in its frontmatter.',
    { schema: DISCOVERY_SCHEMA, label: 'Scanning specs' }
  );

  log(`Found ${discovery.specs.length} approved specs.`);

  phase('Understand');
  const understood = await parallel(
    discovery.specs.map((spec) => () =>
      agent(
        `Read the spec at ${spec.path} and identify its dependencies on other specs and modules.`,
        { schema: UNDERSTANDING_SCHEMA, label: spec.id }
      )
    )
  );

  const validUnderstood = understood.filter(Boolean);

  phase('Plan');
  const plan = await agent(
    `Given these ${validUnderstood.length} understood specs with their dependencies, 
    produce a topologically sorted implementation order. Specs with no dependencies come first.
    Specs: ${JSON.stringify(validUnderstood, null, 2)}`,
    { label: 'Building implementation plan' }
  );

  return plan;
}
```

### The audit-and-verify pattern

Two chained schemas implement adversarial verification: a first wave generates findings, a second wave tries to refute each one:

```js
export default async function ({ agent, parallel, pipeline }) {
  const DIMENSIONS = [
    { id: 'security', prompt: 'Review the changed files for injection, auth, and access control issues.' },
    { id: 'performance', prompt: 'Review the changed files for slow queries, N+1 patterns, and unbounded loops.' },
    { id: 'data-integrity', prompt: 'Review the changed files for missing validations and race conditions.' },
  ];

  const results = await pipeline(
    DIMENSIONS,
    // Stage 1: generate findings per dimension
    (dim) =>
      agent(dim.prompt, {
        phase: 'Review',
        label: dim.id,
        schema: FINDINGS_SCHEMA,
      }),
    // Stage 2: verify each finding independently
    (findings) =>
      parallel(
        findings.issues.map((issue) => () =>
          agent(
            `A reviewer found this issue: "${issue.title}" (${issue.description}). 
            Try your hardest to refute it. Is it a real problem or a false positive?`,
            {
              phase: 'Verify',
              label: issue.title,
              schema: VERDICT_SCHEMA,
            }
          )
        )
      )
  );

  // Flatten and keep only confirmed findings
  const confirmed = results
    .flat()
    .filter((verdicts) => verdicts !== null)
    .flat()
    .filter((v) => v?.isReal);

  return confirmed;
}
```

A real PR review run with this pattern reduced 26 initial findings to 16 after the adversarial verification pass eliminated 10 false positives.

---

## 6. Common patterns

### Adversarial verification

A second wave of agents is tasked with refuting the outputs of the first wave. This works because the first-wave agents were asked to find problems, not to assess their severity or validity. A dedicated refutation agent, given nothing but the finding and the source material, catches assumptions the reviewer made that do not hold in context.

The pattern generalizes beyond code review: any situation where the first pass generates candidates (bugs, keywords, architectural risks, translation errors) benefits from a dedicated refutation pass before the results are acted on.

### Loop-until-dry

Discovery continues until K consecutive rounds yield no new items. Combining `seen` set deduplication with a `dry` counter and a `budget` guard produces a safe exploration loop:

```js
const seen = new Set();
const confirmed = [];
let dry = 0;

while (dry < 2 && budget.remaining() > 30_000) {
  const raw = await agent(
    `Find up to 10 TypeScript files that are not yet covered by a test. 
    Already found: ${JSON.stringify([...seen])}. 
    Return an empty array if none remain.`,
    { schema: BATCH_SCHEMA }
  );

  const fresh = raw.files.filter((f) => !seen.has(f.path));

  if (!fresh.length) {
    dry++;
    continue;
  }

  dry = 0;
  fresh.forEach((f) => seen.add(f.path));
  confirmed.push(...fresh);
}
```

The deduplication set must track items rejected in previous rounds, not just items confirmed. Tracking only `confirmed` means items rejected once will surface again in the next round, preventing the loop from ever going dry.

### Judge panels

Multiple independent agents score or evaluate the same output, followed by a synthesis step. This is useful when a single agent's judgment is insufficiently reliable for a high-stakes decision (architecture approval, security sign-off, quality gate for automated deployment).

```js
const JUDGE_SCHEMA = {
  type: 'object',
  required: ['score', 'confidence', 'rationale'],
  properties: {
    score: { type: 'number', minimum: 0, maximum: 10 },
    confidence: { type: 'string', enum: ['low', 'medium', 'high'] },
    rationale: { type: 'string' },
  },
};

export default async function ({ agent, parallel, log, budget }) {
  const artifact = await agent('Summarize the implementation in src/payments/ in detail.');

  const judges = await parallel([
    () => agent(`Judge this implementation for correctness: ${artifact}`, { schema: JUDGE_SCHEMA, label: 'judge-correctness' }),
    () => agent(`Judge this implementation for security: ${artifact}`, { schema: JUDGE_SCHEMA, label: 'judge-security' }),
    () => agent(`Judge this implementation for maintainability: ${artifact}`, { schema: JUDGE_SCHEMA, label: 'judge-maintainability' }),
  ]);

  const valid = judges.filter(Boolean);
  const avgScore = valid.reduce((sum, j) => sum + j.score, 0) / valid.length;
  log(`Panel scores: ${valid.map((j) => j.score).join(', ')} → avg ${avgScore.toFixed(1)}`);

  const synthesis = await agent(
    `Three judges reviewed the same implementation with these results: 
    ${JSON.stringify(valid, null, 2)}. 
    Produce a final verdict. Where judges disagree, explain the tension. 
    Recommend approve or request-changes with specific action items.`
  );

  return synthesis;
}
```

The budget-guard version runs judge panels in a loop until consensus is reached or budget is exhausted:

```js
while (budget.total && budget.remaining() > 50_000) {
  const panel = await parallel([/* judges */]);
  const scores = panel.filter(Boolean).map((j) => j.score);
  const spread = Math.max(...scores) - Math.min(...scores);
  if (spread <= 1.5) break; // consensus reached
  // otherwise, run another round with the previous rationales as context
}
```

### Multi-strategy sweep

`parallel()` runs multiple agents approaching the same problem with different strategies or sources. The outputs are synthesized with cross-source verification. Common uses: research tasks (official docs + GitHub issues + blog posts), analysis tasks (strict critic + optimistic reader + domain expert).

```js
const strategies = [
  { label: 'official-docs', prompt: `Based only on official Anthropic documentation, explain...` },
  { label: 'community-reports', prompt: `Based only on GitHub issues and community reports, explain...` },
  { label: 'academic', prompt: `Based only on academic papers and benchmarks, explain...` },
];

const perspectives = await parallel(
  strategies.map((s) => () => agent(s.prompt, { label: s.label, schema: PERSPECTIVE_SCHEMA }))
);

const synthesis = await agent(
  `You have ${perspectives.filter(Boolean).length} independent perspectives on the same question. 
  Identify where they agree (high confidence), where they contradict (flag explicitly), 
  and produce a synthesis that is honest about uncertainty.
  Perspectives: ${JSON.stringify(perspectives.filter(Boolean), null, 2)}`
);
```

### Plan–execute–review

A three-phase structure where the first phase designs the approach (typically fast and cheap), the second phase implements per file or module (typically the expensive parallel phase), and the third phase verifies the result.

```js
// Phase 1: Plan (small cluster of agents or a single structured agent)
phase('Plan');
const plan = await agent(
  'Given the failing tests in __tests__/, design a step-by-step fix plan. Return a structured list of files to change and why.',
  { schema: PLAN_SCHEMA }
);

// Phase 2: Execute (implement per file in parallel where safe)
phase('Execute');
const changes = await parallel(
  plan.changes
    .filter((c) => !c.requiresSequentialOrder)
    .map((change) => () =>
      agent(`Apply this specific change: ${change.description}. File: ${change.file}. Do not touch other files.`, {
        label: change.file,
        isolation: 'worktree', // each agent gets isolated repo copy
      })
    )
);

// Phase 3: Review (adversarial check on the implemented changes)
phase('Review');
const verdict = await agent(
  'Run the test suite and review every changed file. Report pass/fail with specifics.',
  { schema: VERDICT_SCHEMA }
);
```

Note the `isolation: 'worktree'` option in the execute phase. When multiple agents will write to the same repository in parallel, each needs an isolated copy to avoid conflicts. Worktree isolation is expensive (full repo copy per agent) and should only be used when agents genuinely mutate files simultaneously.

---

## 7. Real workflow example: dev-flow (Issue to PR)

A complete workflow that takes a GitHub issue number and produces a ready-to-merge pull request. Six phases covering the full dev cycle:

```js
export const meta = {
  name: 'dev-flow',
  description: 'Issue to LGTM: analyze → plan → implement → test → evaluate → PR',
  phases: [
    { title: 'Setup' },
    { title: 'Analyze' },
    { title: 'Plan' },
    { title: 'Implement' },
    { title: 'Validate' },
    { title: 'Evaluate' },
    { title: 'PR' },
  ],
};

const ANALYSIS_SCHEMA = {
  type: 'object',
  required: ['summary', 'affectedModules', 'acceptanceCriteria', 'estimatedComplexity'],
  properties: {
    summary: { type: 'string' },
    affectedModules: { type: 'array', items: { type: 'string' } },
    acceptanceCriteria: { type: 'array', items: { type: 'string' } },
    estimatedComplexity: { type: 'string', enum: ['low', 'medium', 'high'] },
  },
};

const PLAN_SCHEMA = {
  type: 'object',
  required: ['steps'],
  properties: {
    steps: {
      type: 'array',
      items: {
        type: 'object',
        required: ['file', 'description', 'canParallelize'],
        properties: {
          file: { type: 'string' },
          description: { type: 'string' },
          canParallelize: { type: 'boolean' },
        },
      },
    },
  },
};

const VALIDATION_SCHEMA = {
  type: 'object',
  required: ['passed', 'failedTests', 'summary'],
  properties: {
    passed: { type: 'boolean' },
    failedTests: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
};

export default async function ({ agent, parallel, phase, log, args }) {
  const { issueNumber, targetBranch = 'main' } = args;

  // Setup: read current state
  phase('Setup');
  const context = await agent(
    `Read the GitHub issue #${issueNumber} and the current state of the codebase. 
    Summarize the repo structure relevant to this issue.`,
    { label: `Issue #${issueNumber}` }
  );

  // Analyze: understand scope and acceptance criteria
  phase('Analyze');
  const analysis = await agent(
    `Given this context: ${context}
    Analyze issue #${issueNumber} in depth. 
    Identify every file that will need to change, define acceptance criteria, and estimate complexity.`,
    { schema: ANALYSIS_SCHEMA, label: 'Deep analysis' }
  );

  log(`Scope: ${analysis.affectedModules.length} modules, complexity: ${analysis.estimatedComplexity}`);

  // Plan: produce file-level implementation steps
  phase('Plan');
  const plan = await agent(
    `Based on this analysis: ${JSON.stringify(analysis, null, 2)}
    Produce a concrete, file-level implementation plan. 
    Mark which steps can be parallelized (no shared state) and which must be sequential.`,
    { schema: PLAN_SCHEMA, label: 'Implementation plan' }
  );

  // Implement: parallel where safe, sequential where not
  phase('Implement');
  const parallelSteps = plan.steps.filter((s) => s.canParallelize);
  const sequentialSteps = plan.steps.filter((s) => !s.canParallelize);

  if (parallelSteps.length > 0) {
    await parallel(
      parallelSteps.map((step) => () =>
        agent(
          `Implement this change: ${step.description}. 
          Only modify ${step.file}. Do not change any other file.`,
          { label: step.file, isolation: 'worktree' }
        )
      )
    );
  }

  for (const step of sequentialSteps) {
    await agent(
      `Implement this change: ${step.description}. File: ${step.file}.`,
      { label: step.file, phase: 'Implement' }
    );
  }

  // Validate: run tests and check acceptance criteria
  phase('Validate');
  const validation = await agent(
    `Run the full test suite. Then check each acceptance criterion: 
    ${analysis.acceptanceCriteria.map((c, i) => `${i + 1}. ${c}`).join('\n')}
    Report pass/fail per criterion.`,
    { schema: VALIDATION_SCHEMA, label: 'Test + AC check' }
  );

  log(`Tests: ${validation.passed ? 'PASS' : 'FAIL'}. Failed: ${validation.failedTests.length}`);

  if (!validation.passed) {
    // Attempt automated fix for failed tests
    phase('Evaluate');
    await agent(
      `These tests are failing: ${validation.failedTests.join(', ')}. 
      Diagnose and fix them without changing the acceptance criteria behavior.`
    );
  }

  // PR: open the pull request
  phase('PR');
  const pr = await agent(
    `Create a pull request from the current branch to ${targetBranch}.
    Title: derived from issue #${issueNumber} title.
    Body: summary of changes, acceptance criteria status, test results.
    Use gh pr create.`,
    { label: 'Opening PR' }
  );

  return pr;
}
```

Running this workflow: tell Claude "ultracode dev-flow with issueNumber=42" and it handles the full cycle autonomously. The `/workflows` panel shows each phase as it progresses.

---

## 8. When NOT to use workflows

Dynamic workflows carry real overhead: one JS file to write and maintain, a terminal panel to monitor, and a slightly longer startup time as the runtime initializes. Several situations do not justify this overhead.

**Single agent, one task.** If the work can be expressed as a single Agent tool call, do that. A workflow wrapping one `agent()` call adds nothing.

**Simple refactors and bug fixes.** Renaming a variable across 20 files, fixing a typo in a config, adding a missing import: these are single-agent tasks even if they touch multiple files. The orchestration overhead adds seconds and noise to the logs.

**Reusable procedures where Claude picks the steps.** If you want Claude to adapt the approach based on what it finds at runtime (not a fixed graph of stages), a Skill is the right tool. Skills are prompt-driven and composable; workflows are code-driven and structural.

**Open-ended exploration without budget discipline.** A workflow that runs `agent()` in a loop without a `budget` guard will burn through the 1000-agent cap unpredictably. If the task genuinely does not have a bounded stopping condition, a monitored interactive session is safer.

**Nondeterministic orchestration logic.** If the workflow script uses `Math.random()` or `Date.now()`, resume will not work correctly. Scripts that cannot be made deterministic should not be workflows.

**Weak or absent schemas across phases.** Schemas are not technically mandatory, but workflows without them degrade back to brittle text parsing. If you cannot define what data each phase should hand to the next, the task is probably better handled in a single conversational session where Claude synthesizes everything.

| Situation | Better approach |
|-----------|----------------|
| Single agent, one clear task | Agent tool directly |
| Reusable, prompt-driven procedure | Skill |
| Simple edit across many files | Single agent with multi-file edit |
| Open-ended chat and exploration | Interactive session |
| Complex coordinated work, multiple teams | Agent Teams (experimental) |
| Multi-stage, parallelizable, reproducible | Dynamic Workflow |

---

## 9. Cost and performance notes

The orchestrator script itself costs zero tokens. All token cost comes from `agent()` calls. This has a useful implication: you can make the orchestrator as complex as needed (loops, conditionals, schema definitions, helper functions) without incurring any extra cost.

Parallel fan-out reduces wall-clock time dramatically for independent subtasks. A verified example from the community cookbook: 6 parallel agents corrected 5 READMEs in 37 seconds, where sequential execution would have taken approximately 3 to 5 minutes for the same work.

Sequential stages in `pipeline()` add necessary per-stage latency. The cost is justified when stages have genuine data dependencies. It is not justified when the stages are independent dimensions that happen to share a code structure; in that case, `parallel()` with a single barrier at the end is cheaper.

Practical cost model for a typical workflow:

| Component | Token cost | Wall-clock contribution |
|-----------|-----------|------------------------|
| Orchestrator JS | 0 | Milliseconds |
| Each `agent()` call | 2K–20K depending on prompt and context | Sequential: dominant; Parallel: amortized |
| Schema validation retry | 1–2x per failed validation | Rare with well-designed schemas |
| `isolation: 'worktree'` | Git copy overhead | +2–5s per agent on large repos |

Rule of thumb from the Anthropic community: "If you can sketch a non-trivial flowchart with parallel branches, loops, and data handoffs between stages, dynamic workflows are likely appropriate." The flowchart test keeps you from reaching for workflows on tasks that are genuinely simple.

### Monitoring and debugging

Open `/workflows` in any Claude Code session to see:
- All running and recently completed workflows
- Current phase and active agent label for running workflows
- Per-phase agent counts and completion status
- `log()` messages emitted by the orchestrator

When a workflow produces unexpected results, the most effective debugging approach is to add `log()` calls before and after major stages to confirm intermediate data, then add or tighten schemas to catch malformed intermediate outputs early rather than letting them propagate to the final phase.

---

## 10. See also

- **[Tools Reference, Workflow section](../core/tools-reference.md#workflow-dynamic-workflows-v21154)**: canonical tool description, trigger keyword, and CLI flags
- **[Agent Teams](./agent-teams.md)**: experimental multi-agent coordination for read-heavy tasks with peer-to-peer messaging; different from workflows (no JS orchestrator, git-based coordination)
- **[Plan-Driven Workflow](./plan-driven.md)**: human-in-the-loop plan-then-execute pattern; appropriate when you want to review the plan before execution starts
- **[Task Management](./task-management.md)**: Tasks API for cross-session persistence; complements workflows by tracking high-level status outside the session
- **[Spec-First](./spec-first.md)**: writing specs before code; the discovery phase of many workflows benefits from pre-existing structured specs
