---
title: "Task Management Workflow"
description: "Multi-session task coordination using Tasks API and TodoWrite for complex projects"
tags: [workflow, guide, agents]
---

# Task Management Workflow

**Version**: Claude Code v2.1.16+
**Prerequisites**: Understanding of multi-session workflows, basic CLI proficiency
**Time**: 15-30 min to learn, applies to all complex projects

## Overview

Task management in Claude Code evolved significantly in v2.1.16 with the introduction of the **Tasks API**, complementing the original **TodoWrite** tool. This workflow teaches you when to use each system and how to leverage multi-session task coordination for complex projects.

**When to use this workflow:**
- Projects spanning multiple coding sessions
- Multi-agent coordination scenarios
- Complex task hierarchies with dependencies
- Need to resume work after context compaction or session interruption

**When NOT to use:**
- Single-session, straightforward implementations
- Quick fixes or exploratory coding
- Tasks completable in <10 minutes

---

## System Comparison Quick Reference

| Feature | TodoWrite (Legacy) | Tasks API (v2.1.16+) |
|---------|-------------------|---------------------|
| **Persistence** | Session memory only | Disk storage (`~/.claude/tasks/`) |
| **Multi-session** | ❌ Lost on session end | ✅ Survives across sessions |
| **Dependencies** | ❌ Manual ordering | ✅ Task blocking (A blocks B) |
| **Coordination** | Single agent | ✅ Multi-agent with broadcast |
| **Status tracking** | pending/in_progress/completed | pending/in_progress/completed |
| **When to use** | Simple single-session todos | Complex multi-session projects |

**Migration flag** (v2.1.19+):
```bash
# Use old system (TodoWrite)
CLAUDE_CODE_ENABLE_TASKS=false claude

# Use new system (Tasks API) - default since v2.1.19
claude
```

---

## Workflow Phase 1: Task Planning

**Goal**: Decompose complex work into trackable, executable units

### Step 1: Analyze Scope

Before creating tasks, understand what you're building:

```bash
# Discovery pattern
claude
> "Analyze this codebase for implementing JWT authentication:
  - Glob for existing auth patterns
  - Grep for security-related code
  - Identify integration points"
```

### Step 2: Design Task Hierarchy

Break work into logical phases with dependencies:

**Example: Authentication System**
```
Authentication System (parent)
├── 1. Login endpoint (no dependencies)
├── 2. Token refresh (depends on #1)
├── 3. Logout endpoint (depends on #1)
└── 4. Integration tests (depends on #1, #2, #3)
```

### Step 3: Create Task Structure

Use `TaskCreate` to materialize your plan:

```bash
# Session 1: Planning phase
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

# Inside Claude session:
> "Create a task hierarchy for JWT authentication:

  Parent task: 'Implement JWT authentication system'
  - Description: Add JWT-based auth with refresh tokens and secure storage

  Child tasks:
  1. 'Create login endpoint' (no dependencies)
  2. 'Implement token refresh logic' (depends on task 1)
  3. 'Create logout endpoint' (depends on task 1)
  4. 'Write integration tests' (depends on tasks 1, 2, 3)

  Use TaskCreate with proper metadata."
```

**Expected output from Claude:**
```json
{
  "tasks": [
    {
      "id": "task-auth-parent",
      "title": "Implement JWT authentication system",
      "status": "pending",
      "children": ["task-login", "task-refresh", "task-logout", "task-tests"]
    },
    {
      "id": "task-login",
      "title": "Create login endpoint",
      "status": "pending",
      "dependencies": [],
      "metadata": {"priority": "high", "estimated_duration": "2h"}
    },
    {
      "id": "task-refresh",
      "title": "Implement token refresh logic",
      "status": "pending",
      "dependencies": ["task-login"],
      "metadata": {"priority": "high", "estimated_duration": "1h"}
    }
    // ... other tasks
  ]
}
```

---

## Workflow Phase 2: Task Execution

**Goal**: Execute tasks systematically with progress tracking

### Execution Pattern

```
TaskList → TaskGet (next pending) → Execute → TaskUpdate → Validate → Repeat
```

### Step 1: Discover Next Task

```bash
# Session 2: Start implementation
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

> "TaskList to show all pending tasks"
```

**Output:**
```
Tasks for 'auth-system-v2':
✅ task-login: Create login endpoint [completed]
⏳ task-refresh: Implement token refresh logic [pending, blocked by: none]
⏳ task-logout: Create logout endpoint [pending, blocked by: none]
⏳ task-tests: Write integration tests [pending, blocked by: task-refresh, task-logout]
```

### Step 2: Get Task Details

```bash
> "TaskGet task-refresh to see full requirements"
```

**Output:**
```json
{
  "id": "task-refresh",
  "title": "Implement token refresh logic",
  "description": "Create endpoint POST /auth/refresh that validates refresh token and issues new access token",
  "status": "pending",
  "dependencies": ["task-login"],
  "metadata": {
    "priority": "high",
    "estimated_duration": "1h",
    "files": ["src/auth/refresh.ts", "src/middleware/auth.ts"]
  }
}
```

### Step 3: Execute & Update

```bash
> "Mark task-refresh as in_progress, then implement the token refresh endpoint according to requirements"

# Claude executes: TaskUpdate task-refresh status=in_progress
# Claude implements the feature...
# Upon completion:

> "Mark task-refresh as completed"
# Claude executes: TaskUpdate task-refresh status=completed
```

### Step 4: Validate

```bash
> "Run tests for token refresh functionality"

# If tests pass:
# ✅ Task remains completed

# If tests fail:
> "TaskUpdate task-refresh status=in_progress, add error details to metadata and fix issues"
```

---

## Workflow Phase 3: Session Management

**Goal**: Seamlessly resume work across sessions and context boundaries

### Persistence Mechanism

**Storage location**: `~/.claude/tasks/<task-list-id>/`

Tasks survive:
- Session termination
- Context compaction (`/compact`)
- System restarts
- Multiple days of interruption

#### ⚠️ Field Visibility Limitations

**TaskList returns only**: `id`, `subject`, `status`, `owner`, `blockedBy`

**Missing in TaskList output**:
- `description` (requires TaskGet per task)
- `metadata` (custom fields like priority, estimates)
- `activeForm` (progress spinner text)

**Workflow adjustment**:

```bash
# DON'T: Assume you can scan all descriptions
TaskList  # Shows subjects only

# DO: Fetch selectively
TaskList                    # Get overview (which tasks exist, statuses)
TaskGet(task-auth-login)    # Get full details for specific task
TaskGet(task-auth-tests)    # Get details for next task
```

**When this matters**:
- Complex projects with detailed task descriptions (>50 words per task)
- Multi-agent coordination requiring shared context visibility
- Need to quickly scan all task notes to decide resumption point

**Cost awareness**:
- TaskList = 1 API call
- Fetching descriptions for N tasks = 1 + N calls
- For 20 tasks, that's 20x overhead if you need all descriptions

**Mitigation**:
- Use `subject` field for critical info (visible in TaskList)
- Keep `description` concise (50-100 words max)
- Store detailed plans in markdown files (`docs/plan-*.md`)

### Resume Pattern

```bash
# Days later, different terminal session
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

> "TaskList to show current state"

# Output shows exactly where you left off:
# ✅ task-login [completed]
# ✅ task-refresh [completed]
# ⏳ task-logout [pending]
# ⏳ task-tests [pending, blocked by: task-logout]

> "Continue with next pending task that isn't blocked"
```

### Multi-Terminal Coordination

**Use case**: Run multiple Claude instances working on the same project

```bash
# Terminal 1: Frontend work
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude
> "Work on task-logout endpoint"

# Terminal 2: Test writing (simultaneous)
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude
> "TaskList - check what's completed so I can write tests"

# Both terminals see real-time state updates
```

**⚠️ Warning**: Use repository-specific task list IDs to avoid cross-project contamination:
```bash
# ❌ BAD: Generic ID used across multiple repos
export CLAUDE_CODE_TASK_LIST_ID="my-project"

# ✅ GOOD: Repo-specific with context
export CLAUDE_CODE_TASK_LIST_ID="mycompany-api-auth-refactor"
```

---

## Integration: TDD + Task Management

Combine Test-Driven Development with task tracking for systematic test coverage.

### Pattern: Test-First Task Execution

```bash
export CLAUDE_CODE_TASK_LIST_ID="tdd-feature-x"
claude

# Create tasks with test-first approach
> "Create task hierarchy for feature X:

  For each feature component:
  1. Task: 'Write failing tests for [component]'
  2. Task: 'Implement [component] to pass tests' (depends on #1)
  3. Task: 'Refactor [component]' (depends on #2)

  Use TDD red-green-refactor cycle per task."
```

### Example: Login Feature with TDD

```bash
# Phase 1: Red (failing tests)
TaskCreate: {
  title: "Write failing tests for login endpoint",
  description: "Test cases: valid credentials, invalid password, user not found, rate limiting",
  status: "pending"
}

# Execute test writing
> "Implement task-login-tests, ensure all tests fail initially"

# Phase 2: Green (minimal implementation)
TaskCreate: {
  title: "Implement login endpoint (minimal)",
  description: "Make tests pass with simplest possible implementation",
  dependencies: ["task-login-tests"],
  status: "pending"
}

# Phase 3: Refactor
TaskCreate: {
  title: "Refactor login endpoint",
  description: "Optimize, remove duplication, improve readability",
  dependencies: ["task-login-impl"],
  status: "pending"
}
```

**Full workflow reference**: See [TDD with Claude](tdd-with-claude.md#task-management-integration)

---

## Integration: Plan-Driven + Task Management

Convert strategic plans into executable task hierarchies.

### Pattern: Plan-to-Tasks Transformation

```bash
# Step 1: Enter plan mode
claude
> [Press Shift+Tab to enter Plan Mode]

# Step 2: Create architectural plan
> "Design architecture for microservices migration:
  - Identify service boundaries
  - Plan data migration strategy
  - Design API contracts"

# Step 3: Exit plan mode with task creation
> "Convert this plan into a task hierarchy using TaskCreate"
```

### Example: Microservices Migration

**Plan output:**
```
Phase 1: Analysis (Week 1)
- Map monolith dependencies
- Identify bounded contexts
- Design service boundaries

Phase 2: Infrastructure (Week 2)
- Set up service templates
- Configure API gateway
- Establish monitoring

Phase 3: Migration (Week 3-6)
- Extract user service
- Extract order service
- Migrate database schemas
```

**Tasks transformation:**
```bash
TaskCreate: {
  title: "Microservices migration",
  children: [
    {
      title: "Phase 1: Analysis",
      children: [
        {title: "Map monolith dependencies", priority: "critical"},
        {title: "Identify bounded contexts", dependencies: ["map-deps"]},
        {title: "Design service boundaries", dependencies: ["bounded-contexts"]}
      ]
    },
    {
      title: "Phase 2: Infrastructure",
      dependencies: ["phase-1"],
      children: [
        {title: "Set up service templates"},
        {title: "Configure API gateway", dependencies: ["templates"]},
        {title: "Establish monitoring"}
      ]
    }
    // ... Phase 3
  ]
}
```

**Full workflow reference**: See [Plan-Driven Development](plan-driven.md#task-hierarchy-design)

---

## TodoWrite Migration Guide

### When to Migrate

**Stay with TodoWrite if:**
- ✅ All work completes in a single session
- ✅ No multi-agent coordination needed
- ✅ Simple linear task lists (no dependencies)
- ✅ Using Claude Code < v2.1.16

**Migrate to Tasks API if:**
- ✅ Work spans multiple sessions
- ✅ Need task persistence across days/weeks
- ✅ Complex dependency graphs
- ✅ Multi-terminal collaboration
- ✅ Want to resume after context compaction

### Migration Steps

#### Step 1: Identify TodoWrite Usage

```bash
# Find existing TodoWrite usage in your CLAUDE.md or workflows
grep -r "TodoWrite" .claude/
```

#### Step 2: Convert TodoWrite Lists to Tasks

**Before (TodoWrite):**
```markdown
- [ ] Implement user authentication
- [ ] Add password hashing
- [ ] Create session management
- [ ] Write tests
```

**After (Tasks API):**
```bash
export CLAUDE_CODE_TASK_LIST_ID="user-auth-2026"
claude

> "Create tasks:
  1. 'Implement user authentication' (parent)
     - Child: 'Add password hashing'
     - Child: 'Create session management' (depends on hashing)
     - Child: 'Write tests' (depends on auth, hashing, sessions)"
```

#### Step 3: Update CLAUDE.md Instructions

**Before:**
```markdown
For complex tasks:
- Use TodoWrite to create task list
- Execute tasks sequentially
```

**After:**
```markdown
For complex tasks:
- Set CLAUDE_CODE_TASK_LIST_ID=<project-name>
- Use TaskCreate for hierarchical planning
- Execute with TaskUpdate status tracking
- Resume with TaskList in new sessions
```

#### Step 4: Test Migration

```bash
# Create test task list
export CLAUDE_CODE_TASK_LIST_ID="migration-test"
claude

> "Create 3 test tasks with dependencies, mark one completed, then exit"

# Relaunch in new session
export CLAUDE_CODE_TASK_LIST_ID="migration-test"
claude

> "TaskList - verify tasks persisted correctly"

# Expected: See all 3 tasks with correct states
```

---

## Patterns & Anti-Patterns

### ✅ Good Patterns

#### 1. Hierarchical Task Decomposition

```bash
Project (parent)
└── Feature A (child of project)
    ├── Component A1 (child of Feature A)
    │   ├── Implementation (leaf task)
    │   └── Tests (leaf task, depends on Implementation)
    └── Component A2
        └── ...
```

**Why it works**: Mirrors natural project structure, makes dependencies explicit

#### 2. Dependency-First Ordering

```bash
# Always define dependencies when creating tasks
TaskCreate: {
  title: "Deploy to production",
  dependencies: ["run-tests", "code-review", "backup-database"],
  metadata: {blocking_reason: "Safety checks required"}
}
```

**Why it works**: Prevents premature execution, enforces quality gates

#### 3. Granular Status Updates

```bash
# Bad: Large task marked completed without intermediate updates
TaskCreate: {title: "Build entire auth system"}
# ... hours later ...
TaskUpdate: {id: "auth-system", status: "completed"}

# Good: Frequent status updates as work progresses
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "25%"}
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "50%"}
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "75%"}
TaskUpdate: {id: "auth-system", status: "completed"}
```

**Why it works**: Provides visibility, enables context-aware resumption

#### 4. Metadata-Rich Tasks

```bash
TaskCreate: {
  title: "Optimize database queries",
  description: "Reduce query time for user dashboard from 2s to <200ms",
  metadata: {
    priority: "high",
    estimated_duration: "3h",
    related_files: ["src/db/queries.ts", "src/db/indexes.sql"],
    performance_baseline: "2000ms",
    performance_target: "200ms",
    related_issue: "https://github.com/org/repo/issues/123"
  }
}
```

**Why it works**: Context-rich resumption, easier delegation, better documentation

### ❌ Anti-Patterns

#### 1. Monolithic Tasks (>10 steps)

```bash
# ❌ BAD: Task too large, hard to track progress
TaskCreate: {
  title: "Implement entire payment system",
  description: "Stripe integration, webhooks, refunds, disputes, reporting, admin UI, ..."
}

# ✅ GOOD: Break into phases
TaskCreate: {
  title: "Payment system - Phase 1: Core integration",
  children: [
    {title: "Stripe SDK setup"},
    {title: "Payment intent creation"},
    {title: "Webhook handling"}
  ]
}
```

#### 2. Missing Dependencies

```bash
# ❌ BAD: Tasks can execute in wrong order
TaskCreate: {title: "Deploy to production"} # No dependencies
TaskCreate: {title: "Write tests"} # No dependencies

# ✅ GOOD: Explicit ordering
TaskCreate: {
  title: "Deploy to production",
  dependencies: ["write-tests", "run-tests", "code-review"]
}
```

#### 3. Orphan Tasks Without Context

```bash
# ❌ BAD: Future you won't remember what this means
TaskCreate: {
  title: "Fix the bug",
  description: "That one from yesterday"
}

# ✅ GOOD: Self-contained context
TaskCreate: {
  title: "Fix login timeout on Safari",
  description: "Users on Safari 17.2+ experience session timeout after 5min. Expected: 30min timeout. Root cause: cookie SameSite=Strict not supported.",
  metadata: {
    browser: "Safari 17.2+",
    error_message: "Session expired",
    related_commit: "a1b2c3d",
    slack_thread: "https://slack.com/archives/C123/p456"
  }
}
```

#### 4. Status Mismatch

```bash
# ❌ BAD: Task marked completed but tests fail
TaskUpdate: {id: "login-feature", status: "completed"}
# Tests run later: 3 failures

# ✅ GOOD: Validation before completion
> "Run tests for login feature"
# If tests pass:
TaskUpdate: {id: "login-feature", status: "completed", metadata: {test_results: "pass"}}
# If tests fail:
TaskUpdate: {id: "login-feature", status: "in_progress", metadata: {test_results: "3 failures", error_log: "..."}}
```

---

## Troubleshooting

### Q: Tasks don't persist across sessions

**Symptom**: `TaskList` shows empty after restarting Claude

**Solution**:
```bash
# Ensure CLAUDE_CODE_TASK_LIST_ID is set before launching
export CLAUDE_CODE_TASK_LIST_ID="your-project-name"
claude

# Verify storage directory exists
ls ~/.claude/tasks/your-project-name/
```

### Q: Multiple projects sharing task lists

**Symptom**: Seeing tasks from Project A when working on Project B

**Cause**: Using same task list ID across different repositories

**Solution**:
```bash
# Use repo-specific IDs with context
cd ~/projects/api
export CLAUDE_CODE_TASK_LIST_ID="api-v2-migration"
claude

cd ~/projects/frontend
export CLAUDE_CODE_TASK_LIST_ID="frontend-redesign"
claude
```

### Q: TodoWrite still used instead of Tasks API

**Symptom**: Tasks not persisting even with task list ID set

**Cause**: `CLAUDE_CODE_ENABLE_TASKS=false` set in environment

**Solution**:
```bash
# Check environment
env | grep CLAUDE_CODE_ENABLE_TASKS

# Unset if present
unset CLAUDE_CODE_ENABLE_TASKS

# Or explicitly enable (v2.1.19+ defaults to enabled)
export CLAUDE_CODE_ENABLE_TASKS=true
```

### Q: Task dependencies not enforced

**Symptom**: Claude executes blocked tasks before dependencies complete

**Cause**: Dependencies not properly defined in TaskCreate

**Solution**:
```bash
# Ensure dependencies use correct task IDs
TaskCreate: {
  title: "Task B",
  dependencies: ["task-a-id"], # ✅ Use actual task ID
  # NOT dependencies: ["Task A"] # ❌ Task title won't work
}

# Verify dependencies:
TaskGet task-b-id
# Should show: "blockedBy": ["task-a-id"]
```

---

## Advanced: Custom Task Metadata

Extend tasks with domain-specific metadata for enhanced workflows.

### Metadata Conventions

**Performance optimization tasks:**
```json
{
  "metadata": {
    "type": "performance",
    "baseline_metric": "2000ms",
    "target_metric": "200ms",
    "profiling_tool": "Chrome DevTools",
    "measurement_location": "dashboard load time"
  }
}
```

**Security tasks:**
```json
{
  "metadata": {
    "type": "security",
    "severity": "critical",
    "cve_id": "CVE-2024-1234",
    "affected_versions": "< 2.1.0",
    "mitigation": "Update package X to v3.0+"
  }
}
```

**Bug fix tasks:**
```json
{
  "metadata": {
    "type": "bugfix",
    "issue_url": "https://github.com/org/repo/issues/456",
    "reported_by": "user@example.com",
    "reproduction_steps": "1. Login 2. Navigate to dashboard 3. Click export",
    "error_message": "TypeError: Cannot read property 'map' of undefined"
  }
}
```

### Querying by Metadata

```bash
# Filter tasks by type (requires scripting, not built-in)
TaskList | jq '.tasks[] | select(.metadata.type == "security")'

# Find high-priority pending tasks
TaskList | jq '.tasks[] | select(.metadata.priority == "high" and .status == "pending")'
```

---

## Related Workflows

- **[TDD with Claude](tdd-with-claude.md)** - Test-first development with task tracking
- **[Plan-Driven Development](plan-driven.md)** - Strategic planning to task hierarchies
- **[Iterative Refinement](iterative-refinement.md)** - Incremental improvements with tasks
- **[Exploration Workflow](exploration-workflow.md)** - Discovery phase before task creation

---

## Reference

**Tool documentation**: See [Ultimate Guide Section 5.X](../ultimate-guide.md#5x-task-management-system)

**Sources:**
- Official: [Claude Code CHANGELOG v2.1.16](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- Official: [System Prompts - TaskCreate](https://github.com/Piebald-AI/claude-code-system-prompts)
- Community: [paddo.dev - From Beads to Tasks](https://paddo.dev/blog/from-beads-to-tasks/)
- Community: [llbbl.blog - Two Changes in Claude Code](https://llbbl.blog/2026/01/25/two-changes-in-claude-code.html)

**Version tracking**: This workflow documents Claude Code v2.1.16+ (released 2026-01-22). Verify latest changes in [claude-code-releases.yaml](../../machine-readable/claude-code-releases.yaml).