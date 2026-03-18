---
name: plan-execute
description: "Execute a validated plan: worktree isolation, TDD scaffolding, level-based parallel agents, quality gate with smoke test, PR creation and merge. Handles everything through to merged PR."
---

# Plan Execute — Execution to Merged PR

Execute the validated plan in an isolated worktree. Spawn per-task agents, verify quality, create and merge the PR. Handles everything through to cleanup.

Run `/clear` before this command.

---

## Prerequisite

A validated plan must exist at `docs/plans/plan-{name}.md` with all issues resolved (output of `/plan-validate`).

---

## Step 1: Worktree Setup

Create an isolated git worktree:

```bash
git worktree add .worktrees/{plan-name} -b feature/{plan-name}
```

All execution happens inside the worktree. Main branch remains clean throughout.

---

## Step 2: TDD Scaffolding

*Only for tasks marked as TDD in the plan.*

For each TDD task, before any implementation:
1. Write the failing test(s) that define the acceptance criteria
2. Run tests to confirm they fail (red)
3. Commit the failing tests
4. Mark the test file in the task for the implementation agent to find

Do not write implementation code in this step.

---

## Step 3: Level-Based Parallel Execution

Parse the task list from the plan. Group tasks by layer (Layer 1 = foundation, Layer 2 = depends on Layer 1, etc.).

**For each layer:**
1. Identify all tasks in the layer
2. Spawn one agent per task in parallel (Task tool, run_in_background: true)
3. Each agent receives: its task description, files to modify, acceptance criteria, and relevant ADRs
4. Monitor all agents via TaskOutput polling loop
5. Each agent commits on task completion: `git commit -m "feat: {task-description}"`
6. Wait for all tasks in the layer to complete before starting the next layer

**Drift detection**: after each layer, diff the actual changes against the plan spec. If implementation deviates significantly from the plan (new files not in plan, plan files not touched), flag and ask how to proceed. Do not silently continue on drift.

**Agent instructions for each task:**
```
You are implementing one task from a validated plan.
Task: {description}
Files to modify: {file list}
Acceptance criteria: {criteria}
Relevant ADRs: {adr list}

First principles:
- Build state-of-the-art. No workarounds, no legacy patterns.
- Fix at the correct architectural level, never with component-level hacks.
- If you discover that the plan is wrong or missing context, stop and report — do not improvise architecture.

Commit your changes when complete with message: "feat: {task-description}"
```

---

## Step 4: Quality Gate

Run in parallel:
- Linter
- Type checker (if applicable)
- Full test suite

If all pass: proceed to smoke test.

If any fail: spawn a `quality-fixer` debug agent with the failure output. It gets up to **3 auto-fix attempts**. After each attempt, re-run the quality gate. If still failing after 3 attempts: stop, report the failure with the full error output, and wait for human intervention.

**Integration smoke test** *(skip for pure frontend or docs-only plans)*:

Run the smoke commands defined in the plan's `## Integration Verification` section. Additionally:
- If GraphQL: run an introspection probe to verify schema is accessible
- If Docker services: scan container logs for ERROR-level entries
- If new API routes: verify each returns expected status codes

Smoke test failures are debugged by a `quality-fixer-smoke` agent with the same 3-attempt limit.

---

## Step 5: Pre-PR Documentation

*In the worktree, before creating the PR.*

**PRD Reconciliation**: compare the implemented behavior against the original PRD. Note any deviations or additions discovered during implementation. Update the PRD with actuals. These updates ship in the same PR as the feature.

**Plan Archival**: move `docs/plans/plan-{name}.md` to `docs/plans/completed/plan-{name}.md`. Update the status header.

Commit documentation updates: `docs: reconcile PRD and archive plan for {feature-name}`.

---

## Step 6: Push and PR

Push the worktree branch and create the PR:

```bash
git push origin feature/{plan-name}
gh pr create \
  --title "{feature-name}: {one-line summary from plan}" \
  --body "$(cat .pr-body.md)"
```

PR body template:
```markdown
## Summary
{plan summary paragraph}

## Changes
{auto-generated from task list: bullet per task with files affected}

## ADRs
{list of ADRs created during this plan}

## Test Plan
{from plan test plan section}

## Smoke Test Results
{output from integration verification}
```

Merge using squash:
```bash
gh pr merge --squash --delete-branch
```

---

## Step 7: Post-Merge Metrics

Switch back to develop/main. Update `docs/plans/metrics/{name}.json` with execution data:
- Task count and per-layer breakdown
- TDD task count
- Diff stats (files changed, lines added/removed)
- Quality gate results (pass/fail, fix attempts)
- Smoke test results
- Drift score (0-1, how closely implementation matched plan)
- PR data (number, merge commit, timestamp)

Commit metrics update.

---

## Step 8: Worktree Cleanup

```bash
git worktree remove .worktrees/{plan-name}
```

---

## Usage

```
/plan-execute
```

Picks up the most recent validated plan. Or specify:

```
/plan-execute plan-user-authentication
```

## Output

```
Setting up worktree: .worktrees/user-authentication
Branch: feature/user-authentication

TDD scaffolding: 2 tasks marked TDD
  ✓ Written failing tests for: auth-token-validation
  ✓ Written failing tests for: refresh-token-rotation
  Committed: "test: failing tests for auth pipeline (TDD)"

Executing Layer 1 (3 tasks, parallel)...
  [agent-1] Implementing: JWT token generation service
  [agent-2] Implementing: User session model
  [agent-3] Implementing: Auth middleware
  ✓ Layer 1 complete. 3 commits.

Drift check: Layer 1... ✓ No drift detected.

Executing Layer 2 (2 tasks, parallel)...
  [agent-4] Implementing: Login endpoint
  [agent-5] Implementing: Refresh endpoint
  ✓ Layer 2 complete. 2 commits.

Quality gate...
  ✓ Lint passed
  ✓ Type check passed
  ✓ Tests: 47 passed, 0 failed

Smoke test...
  ✓ GraphQL introspection: OK
  ✓ POST /api/auth/login: 200
  ✓ POST /api/auth/refresh: 200

Pre-PR docs...
  ✓ PRD reconciled (1 minor deviation noted)
  ✓ Plan archived to docs/plans/completed/

PR created: #142 "user-authentication: JWT auth with refresh token rotation"
PR merged (squash). Branch deleted.

Metrics committed. Worktree cleaned.
✅ Feature complete.
```

## When to Use

After `/plan-validate` confirms all issues are resolved. Never skip validation — executing an unvalidated plan skips the independent review that catches ~18 issues on average.

## See Also

- [Plan-Validate-Execute Pipeline](../../guide/workflows/plan-pipeline.md)
- [Git Worktree Command](./git-worktree.md)
- [TDD with Claude](../guide/workflows/tdd-with-claude.md)
