---
title: "Iterative Refinement"
description: "Prompt, observe, and reprompt until satisfied — the core loop of AI-assisted development"
tags: [workflow, guide, design-patterns]
---

# Iterative Refinement

> **Confidence**: Tier 2 — Validated pattern observed across many Claude Code users.

Prompt, observe, reprompt until satisfied. The core loop of effective AI-assisted development.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [The Loop](#the-loop)
3. [Feedback Patterns](#feedback-patterns)
4. [Autonomous Loops](#autonomous-loops)
5. [Integration with Claude Code](#integration-with-claude-code)
6. [Script Generation Workflow](#script-generation-workflow)
7. [Iteration Strategies](#iteration-strategies)
8. [Anti-Patterns](#anti-patterns)
9. [Community Patterns & Known Limitations](#community-patterns--known-limitations)
10. [See Also](#see-also)

---

## TL;DR

```
1. Initial prompt with clear goal
2. Claude produces output
3. Evaluate against criteria
4. Specific feedback: "Change X because Y"
5. Repeat until done
```

Key insight: **Specific feedback > vague feedback**

---

## The Loop

### Step 1: Initial Prompt

Start with clear intent and constraints:

```
Create a React component for a user profile card.
- Show avatar, name, bio
- Include edit button
- Use Tailwind CSS
- Mobile-responsive
```

### Step 2: Evaluate Output

Claude produces code. Evaluate:
- Does it meet requirements?
- What's missing?
- What's wrong?
- What could be better?

### Step 3: Specific Feedback

Provide targeted corrections:

```
Good start. Changes needed:
1. Avatar should be circular, not square
2. Edit button should only show for own profile (add isOwner prop)
3. Bio should truncate after 3 lines with "Show more"
```

### Step 4: Repeat

Continue until satisfied:

```
Better. One more thing:
- Add loading skeleton state for when data is fetching
```

---

## Feedback Patterns

### Effective Feedback

| Pattern | Example |
|---------|---------|
| **Specific location** | "Line 23: change `===` to `==`" |
| **Clear action** | "Add error boundary around the form" |
| **Reason given** | "Remove the console.log because it leaks user data" |
| **Priority marked** | "Critical: fix the SQL injection. Nice-to-have: add pagination." |

### Ineffective Feedback

| Anti-Pattern | Why It Fails | Better Alternative |
|--------------|--------------|-------------------|
| "Make it better" | No direction | "Improve readability by extracting the validation logic" |
| "This is wrong" | No specifics | "The date format should be ISO 8601, not Unix timestamp" |
| "I don't like it" | Subjective | "Use functional components instead of class components" |
| "Fix the bugs" | Too vague | "Fix: 1) null check on line 12, 2) off-by-one in loop" |

---

## Autonomous Loops

Claude can self-iterate with clear completion criteria.

### The Ralph Wiggum Pattern

Named after the self-improvement loop pattern:

```
Keep improving the code quality until:
1. All tests pass
2. No TypeScript errors
3. ESLint shows zero warnings

After each iteration, run the checks and fix any issues.
Stop when all criteria are met.
```

### Completion Criteria Examples

```
Iterate until:
- Response time < 100ms for 95th percentile
- Test coverage > 80%
- All accessibility checks pass
- Bundle size < 200KB
```

### Iteration Limits

Always set limits to prevent infinite loops:

```
Improve the algorithm performance.
Maximum 5 iterations.
Stop early if improvement < 5% between iterations.
```

---

## Integration with Claude Code

### With Task Tool

Track refinement iterations using `TaskCreate` and `TaskUpdate`:

```
TaskCreate: "Implement initial version"
TaskCreate: "Fix: handle empty arrays"
TaskCreate: "Fix: add input validation"
TaskCreate: "Optimization: memoize expensive calculations"
# Mark completed as you progress with TaskUpdate
```

### With Hooks

Auto-validate after each change using Claude Code hooks (configured via `/hooks` command or `settings.json`). For example, a `PostToolUse` hook on the `Edit` tool can run linting and tests automatically. Claude sees failures and can self-correct.

### With /compact

When context grows during iterations:

```
/compact

Continue refining the search algorithm.
We've made good progress, focus on the remaining issues.
```

### Checkpointing

After significant progress:

```
Good progress. Let's checkpoint:
- Commit what we have
- List remaining issues
- Continue with the next priority
```

---

## Script Generation Workflow

Script and automation generation delivers the highest ROI for iterative refinement—70-90% time savings in practitioner reports. Scripts are self-contained, testable in isolation, and yield immediate value.

### The 3-7 Iteration Pattern

Most production-ready scripts emerge after 3-7 iterations:

| Iteration | Focus | Prompt Pattern |
|-----------|-------|----------------|
| 1 | Basic functionality | "Create a script that [goal]" |
| 2-3 | Constraints + edge cases | "Add [constraint]. Handle [edge case]." |
| 4-5 | Hardening | "Add error handling, logging, input validation" |
| 6-7 | Polish | "Optimize for [metric]. Add usage docs." |

### Example: Kubernetes Pod Manager (PowerShell)

**Iteration 1 — Basic**
```
Create a PowerShell function to list pods in a Kubernetes namespace.
```

**Iteration 2 — Add filtering**
```
Add: filter by label selector and pod status.
Show: pod name, status, age, restarts.
```

**Iteration 3 — Add actions**
```
Add: ability to delete pods matching filter.
Require: confirmation before deletion.
```

**Iteration 4 — Error handling**
```
Handle: kubectl not found, invalid namespace, permission denied.
Add: verbose logging with -Verbose flag.
```

**Iteration 5 — Production ready**
```
Add: dry-run mode, output to JSON for piping, help documentation.
Ensure: works on Windows, Linux, macOS.
```

### Common Pitfalls

| Pitfall | Example | Mitigation |
|---------|---------|------------|
| Hallucinated commands | `apt-get` on macOS | Specify OS: "Ubuntu 22.04 only" |
| Security gaps | No input validation | Always request: "validate all user inputs" |
| Over-engineering | Adds unnecessary libs | Request: "minimal dependencies, stdlib preferred" |
| Context drift | Forgets requirements after iteration 5 | Checkpoint prompt: "Recap current requirements before next change" |
| Platform assumptions | Assumes bash features in sh | Specify: "POSIX-compliant" or "bash 4+" |

### Script Iteration Template

```
Current script: [paste or reference]

Iteration goal: [specific improvement]

Constraints:
- Must preserve: [existing behavior to keep]
- Must not: [things to avoid]
- Target environment: [OS, shell, runtime]

Success criteria: [how to verify this iteration works]
```

---

## Iteration Strategies

### Breadth-First

Fix all issues at same level before going deeper:

```
First pass: Fix all type errors
Second pass: Fix all lint warnings
Third pass: Improve test coverage
Fourth pass: Optimize performance
```

### Depth-First

Complete one area fully before moving on:

```
1. Perfect the authentication flow (all aspects)
2. Then move to user management
3. Then move to settings
```

### Priority-Based

Address by importance:

```
Iterate in this order:
1. Security issues (critical)
2. Data integrity bugs (high)
3. UX problems (medium)
4. Code style (low)
```

---

## Anti-Patterns

### Moving Target

```
# Wrong
"Actually, let's change the approach entirely..."
(Repeated 5 times)

# Right
Commit to an approach, iterate within it.
If approach is wrong, explicitly restart.
```

### Perfectionism Loop

```
# Wrong
Keep improving forever

# Right
Set clear "good enough" criteria:
- Tests pass
- Handles main use cases
- No critical issues
→ Ship it, improve later
```

### Lost Context

```
# Wrong
After 50 iterations, forget what the goal was

# Right
Periodically restate the goal:
"Reminder: we're building a rate limiter.
Current state: basic implementation works.
Next: add Redis backend."
```

---

## Review Auto-Correction Loop

Specialized iterative pattern for code review where Claude reviews → fixes → re-reviews until convergence.

### Pattern

```
┌─────────────────────────────────────────┐
│   Review Auto-Correction Loop           │
│                                          │
│   Review (identify issues)               │
│        ↓                                 │
│   Fix (apply corrections)                │
│        ↓                                 │
│   Re-Review (verify fixes)               │
│        ↓                                 │
│   Converge (minimal changes) → Done      │
│        ↑                                 │
│        └──── Repeat (max iterations)     │
└─────────────────────────────────────────┘
```

### Prompt Template

```
Review this PR with auto-correction:
1. Multi-agent review (3 scope-focused agents)
2. Fix all 🔴 Must Fix issues
3. Re-review to verify fixes didn't introduce new issues
4. Fix all 🟡 Should Fix issues
5. Re-review one final time
6. Stop when only 🟢 Can Skip remain

Max iterations: 3
Stop early if iteration produces <5 lines changed
```

### Safeguards

| Safeguard | Purpose | Implementation |
|-----------|---------|----------------|
| **Max iterations** | Prevent infinite loops | Hard limit: 3 iterations |
| **Quality gates** | Ensure fixes are valid | Run `tsc && lint` before each iteration |
| **Protected files** | Prevent risky changes | Skip auto-fix for: package.json, migrations, .env |
| **Change threshold** | Stop when converged | Exit if iteration changes <5 lines |
| **Rollback capability** | Recover from bad fixes | Git commit before each iteration |

### Example Session

**Iteration 1: Initial Review**
```
Claude: Found 8 issues:
- 🔴 3 Must Fix (SQL injection, empty catch, missing auth)
- 🟡 4 Should Fix (DRY violations, N+1 query)
- 🟢 1 Can Skip (naming style)
```

**Iteration 2: Fix Must Fix + Re-Review**
```
Claude: Fixed 3 Must Fix issues.
Re-review: All 🔴 resolved. No new issues introduced.
Remaining: 4 🟡 Should Fix, 1 🟢 Can Skip
```

**Iteration 3: Fix Should Fix + Re-Review**
```
Claude: Fixed 4 Should Fix issues.
Re-review: All 🟡 resolved. No new issues.
Remaining: 1 🟢 Can Skip (optional improvement)
```

**Convergence**
```
Claude: Converged. Only optional improvements remain.
Changes this iteration: 2 lines (below threshold).
Review complete. ✅
```

### Comparison: One-Pass vs Convergence Loop

| Aspect | One-Pass Review | Convergence Loop |
|--------|-----------------|------------------|
| **Detection** | Find all issues once | Find issues → fix → verify → repeat |
| **Follow-up awareness** | Check git log for "Co-Authored-By: Claude" | Each iteration is aware of previous |
| **False positives** | Can suggest fixes for already-fixed code | Re-review catches this |
| **Confidence** | Single validation | Multiple validation passes |
| **Time cost** | Fastest (1 review) | Slower (3+ reviews) |
| **Quality** | Good for experienced devs | Better for critical code |

**When to use**:
- **One-pass**: Simple PRs, experienced team, time-sensitive
- **Convergence loop**: Security-critical code, junior team, high-stakes production

### Integration with Multi-Agent Review

Combine convergence loop with multi-agent review for maximum quality:

```
Each iteration:
├─ Agent 1: Consistency Auditor
├─ Agent 2: SOLID Principles Analyst
└─ Agent 3: Defensive Code Auditor
     ↓
  Fix issues
     ↓
  Re-run 3 agents
     ↓
  Verify fixes + check for new issues
     ↓
  Repeat until convergence
```

### Convergence Criteria

Stop iterating when ANY of these is true:

1. **No issues remaining** (ideal outcome)
2. **Max iterations reached** (3 iterations default)
3. **Change threshold** (iteration changed <5 lines)
4. **Quality gate failure** (tsc/lint fails after fix)
5. **Manual stop** (user requests halt)

### Anti-Patterns in Review Loops

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Infinite loop** | No convergence criteria | Set max iterations + change threshold |
| **Scope creep** | Each iteration adds new requirements | Lock scope before starting loop |
| **Breaking fixes** | Fix introduces new bugs | Re-review after each fix + quality gates |
| **Protected file changes** | Modifies package.json, migrations | Explicit skip list for protected files |
| **Context loss** | Forgets original issues after iteration 3 | Maintain issue tracker across iterations |

---

## Example Session

### Initial Request
```
Create a debounce function in TypeScript.
```

### Iteration 1
```
Looks good. Add:
- Generic type support for any function signature
- Option to execute on leading edge
```

### Iteration 2
```
Better. Issues:
- The return type should preserve the original function's return type
- Add cancellation support
```

### Iteration 3
```
Almost there. Final polish:
- Add JSDoc comments
- Export the types separately
- Add unit tests
```

### Completion
```
Perfect. Commit this as "feat: add debounce utility with full TypeScript support"
```

---

## Community Patterns & Known Limitations

The community has built several patterns on top of Claude Code's iterative loop. Some solve real pain points, others expose current limitations worth knowing about.

### Ralph Loop (Test-Driven Autonomous Iteration)

Source: nathanonn.com, February 2026.

The Ralph Loop constrains autonomous iteration to one test case per cycle instead of running the full suite every time. This keeps each cycle focused and prevents the agent from chasing multiple failures at once.

How it works:

1. Pick one failing test case
2. Fix it, verify it passes
3. Save progress to a JSON state file
4. Move to the next failing test case
5. After 3 failed attempts on the same case, mark it as `known_issue` and skip it

```json
{
  "current_case": "test_auth_token_refresh",
  "attempts": 2,
  "known_issues": ["test_legacy_migration_edge_case"],
  "completed": ["test_login", "test_logout", "test_session_timeout"]
}
```

The state file is the key innovation here. It survives context resets, `/compact` operations, and even full session restarts. The agent reads the file at the start of each cycle to know exactly where it left off, which cases are done, and which ones to skip.

The 3-attempt limit prevents the infinite loop trap that plagues naive autonomous loops. Rather than burning tokens on a stubborn test case, the agent moves forward and flags the issue for human review later.

### Auto-Continue Skill

Source: mcpmarket.com.

A confidence-based continuation system that decides whether the agent should keep going or stop for human input. Instead of a fixed iteration count, it evaluates the situation after each cycle:

**Auto-continues when**:
- Tests pass
- Build succeeds
- No new error types detected
- Confidence score remains above threshold

**Stops for human input when**:
- Confidence drops below threshold
- A new category of error appears (not just a new instance of a known error)
- Build or type-check fails in a way the agent hasn't seen before

This pairs well with Claude Code's Stop hooks. The skill can trigger post-task verification and decide whether to resume based on the results.

### Stop Hooks for Automatic Verification

A pattern that turns Claude Code's hook system into an automatic quality gate between iterations:

1. Claude finishes a task (or an iteration)
2. A `PostToolUse` hook on `TodoWrite` triggers a verification script
3. The script runs type-check, lint, and tests
4. Errors get piped back to Claude automatically
5. Claude fixes the issues without human intervention

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "TodoWrite",
        "command": "bash -c 'npm run typecheck 2>&1; npm run lint 2>&1; npm test 2>&1'"
      }
    ]
  }
}
```

The hook fires every time Claude marks a task as done. If the verification catches something, Claude sees the output and can self-correct before moving to the next task.

### Escalation Strategy

What to do when 3 iterations fail on the same problem. Instead of looping forever or giving up, follow a structured escalation path:

1. **Decompose**: Break the failing task into 2-3 smaller sub-tasks that can be tackled independently
2. **Collect context**: Dump all error messages, stack traces, and attempted fixes into a structured file
3. **Model escalation**: If using Sonnet, retry the specific failing case with Opus for deeper reasoning
4. **Human escalation**: If the model upgrade doesn't help, create a GitHub issue with the full error context and mark the task as `known_issue`

```bash
# Escalation in practice
if [ "$ATTEMPT_COUNT" -ge 3 ]; then
    # Collect context
    cat errors.log attempts.log > escalation-context.md

    # Try with Opus
    claude --model claude-opus-4-6 \
        "Fix this failing test. Context: $(cat escalation-context.md)"

    # If still failing, create issue
    if [ $? -ne 0 ]; then
        gh issue create \
            --title "Auto-escalation: $TEST_NAME fails after 3 attempts" \
            --body "$(cat escalation-context.md)" \
            --label "known_issue,needs-human"
    fi
fi
```

The goal is never to silently drop work. Every failure either gets resolved, escalated, or explicitly tracked.

### Known Limitations

Being honest about what doesn't work yet, so you don't waste time reinventing solutions that don't exist.

**No built-in retry/verify/resume** (GitHub issue #28489): Headless automation in Claude Code lacks native support for retry logic, verification gates, and session resumption. Every team implementing autonomous loops builds their own version of this. State files, hook-based verification, and escalation scripts are all community workarounds for a gap in the platform.

**Agent iterations can be lost** (GitHub issue #28843): In multi-day workflows, agent iterations and their accumulated context can be destroyed. If you're running a workflow that spans multiple sessions or days, save explicit state files every N iterations. Do not rely on Claude's conversation memory as your only source of truth.

**Multi-day workflow fragility**: Long-running automation needs checkpointing discipline. Save state to disk (JSON files, git commits, issue comments) at regular intervals. The pattern is simple but easy to forget: if you can't reconstruct the agent's progress from files on disk alone, your workflow will break on session boundaries.

---

## See Also

- [exploration-workflow.md](./exploration-workflow.md) — Explore alternatives before iterating
- [tdd-with-claude.md](./tdd-with-claude.md) — TDD is iterative refinement with tests
- [plan-driven.md](./plan-driven.md) — Plan before iterating
- [../core/methodologies.md](../core/methodologies.md) — Iterative Loops methodology
