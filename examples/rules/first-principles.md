---
description: "Session invariant template - hard constraints, quality thresholds, and anti-patterns that Claude must respect throughout a session"
---

# First Principles: Session Invariants

This is a template for the "Contract" layer of your Claude Code rules. These are constraints that must hold true for the entire session, regardless of which task is active or how much context has accumulated.

Customize the sections below to match your team's standards. Replace the example values with your own thresholds.

> **Why this matters**: As conversation context grows, earlier instructions lose influence on Claude's behavior. This is called "context decay." Session invariants placed in CLAUDE.md or rules files act as compression anchors that resist this decay, because they're injected at the start of every context window.

## Hard Constraints

These rules never have exceptions. If Claude is about to violate one, it must stop and flag the conflict rather than proceeding.

```markdown
# Hard Constraints (never-break rules)

## Data Safety
- Never delete production data without explicit user confirmation in the same message
- Never store secrets (API keys, passwords, tokens) in code files or commit them
- Never run DROP, TRUNCATE, or DELETE without WHERE on production databases

## Code Safety
- Never disable TypeScript strict mode or ESLint rules to make code compile
- Never catch errors silently (empty catch blocks, swallowed promises)
- Never use `any` type in TypeScript except in test fixtures

## Process Safety
- Never force-push to main/master
- Never skip pre-commit hooks (no --no-verify)
- Never amend a commit that has been pushed to a shared branch

## Scope Safety
- Never modify files outside the directories specified in the current task
- Never add dependencies without stating the reason and checking bundle size impact
- Never refactor code that isn't part of the current task (note it for later instead)
```

## Quality Thresholds

Thresholds beat vague adjectives. "Good coverage" means different things to different people; "80% line coverage" is unambiguous. Define your numbers here.

```markdown
# Quality Thresholds

## Testing
- Minimum test coverage: 80% line coverage for new code
- Every public function must have at least one test
- Every bug fix must include a regression test
- Integration tests required for any endpoint that touches the database

## Performance
- API response time: p95 < 200ms for read endpoints, < 500ms for writes
- Bundle size: Total JS < 250KB gzipped (check with `npx bundlesize`)
- No N+1 queries (use DataLoader or equivalent for batch fetching)
- Database queries: no query > 100ms in development (enable slow query log)

## Code Quality
- Cyclomatic complexity: no function > 15 (enforce via ESLint rule)
- File length: no file > 400 lines (split when approaching limit)
- Function length: no function > 50 lines
- Nesting depth: no code > 4 levels of indentation

## Dependencies
- No dependency with known critical CVE
- No dependency abandoned > 2 years (check last publish date)
- Maximum 3 direct dependencies per feature module
```

## Workflow Invariants

Process constraints that ensure consistency across the session, especially when switching between tasks or when sub-agents are involved.

```markdown
# Workflow Invariants

## Commit Discipline
- Every commit must pass all existing tests before being created
- Commit messages follow Conventional Commits format (feat:, fix:, docs:, etc.)
- One logical change per commit (don't mix refactor with feature)

## Review Before Action
- Read a file before modifying it (no blind edits)
- Run tests after every significant change (not just at the end)
- Verify imports after adding/removing dependencies

## Communication
- When uncertain between two approaches, present both with trade-offs (don't pick silently)
- When a task will take more than 5 tool calls, outline the plan first
- When hitting an unexpected error, diagnose before retrying
```

## Anti-Patterns to Detect

Patterns Claude should flag when it encounters them in the codebase or in its own output. These work like automated code review rules, but for the AI's behavior during a session.

```markdown
# Anti-Patterns to Detect

## Code Smells to Flag
- God objects: classes with >10 public methods or >5 injected dependencies
- Feature envy: a function that references another module's internals more than its own
- Primitive obsession: passing >3 related primitives instead of a typed object
- Temporal coupling: functions that must be called in a specific order without enforcement

## Process Smells to Flag
- Yak shaving: spending >3 tool calls on something tangential to the task
- Gold plating: adding features, abstractions, or error handling not requested
- Shotgun surgery: a single change requiring edits in >5 files (suggests missing abstraction)
- Copy-paste programming: duplicating >5 lines instead of extracting a function

## AI-Specific Anti-Patterns
- Hallucinated APIs: calling a method that doesn't exist in the current version
- Stale context: referencing file contents from earlier in the conversation that may have changed
- Over-apology: spending tokens on apologies instead of fixing the issue
- Premature optimization: adding caching, lazy loading, or memoization without evidence of a perf problem
```

## Mitigating Context Decay

Three practical strategies to keep these invariants effective across long sessions:

1. **Place in CLAUDE.md**: Rules in CLAUDE.md are injected at the start of every context window, surviving auto-compaction. This is the strongest position for invariants.

2. **Use rules files for domain-specific constraints**: Put testing thresholds in `.claude/rules/testing.md`, security rules in `.claude/rules/security.md`. They load with CLAUDE.md but keep each file focused.

3. **LEARNINGS.md hook pattern**: Configure a hook that injects accumulated session learnings into sub-agents, so constraints discovered mid-session propagate to delegated work:

```json
// .claude/settings.json (hooks section)
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Task",
      "command": "cat .claude/LEARNINGS.md 2>/dev/null || true"
    }]
  }
}
```

This ensures that when Claude spawns sub-agents via the Task tool, they receive the same session-specific learnings and constraints.

---

**Sources**:
- 3-layer context model (Contract / Working Set / Noise): codeaholicguy.com (Feb 2026)
- CLAUDE.md as "context compression anchors": Craig Johnston (imti.co)
- "Thresholds, not vibes" pattern: specific numbers over vague adjectives
- LEARNINGS.md hook pattern: community practice for propagating context to sub-agents
