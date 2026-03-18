---
title: "TDD with Claude Code"
description: "Test-Driven Development workflow with explicit prompting for red-green-refactor cycles"
tags: [workflow, tdd, testing]
---

# TDD with Claude Code

> **Confidence**: Tier 1 — Based on official Anthropic best practices and extensive community validation.

Test-Driven Development with Claude requires explicit prompting. Claude naturally writes implementation first, then tests. TDD requires the inverse.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [The Problem](#the-problem)
3. [Setup](#setup)
4. [The Red-Green-Refactor Cycle](#the-red-green-refactor-cycle)
5. [Integration with Claude Code Features](#integration-with-claude-code-features)
6. [Anti-Patterns](#anti-patterns)
7. [Advanced Patterns](#advanced-patterns)
8. [See Also](#see-also)

---

## TL;DR

```
Red → Green → Refactor

But you MUST prompt Claude explicitly:
"Write a FAILING test for [feature]. Do NOT write implementation yet."
```

---

## The Problem

Without explicit instruction, Claude will:
1. Write implementation code
2. Then write tests that pass against that implementation

This defeats TDD's purpose: tests should drive design, not validate existing code.

---

## Setup

### CLAUDE.md Configuration

Add to your project's CLAUDE.md:

```markdown
## Testing Conventions

### TDD Workflow
- Always write failing tests BEFORE implementation
- Use AAA pattern: Arrange-Act-Assert
- One assertion per test when possible
- Test names describe behavior: "should_return_empty_when_no_items"

### Test-First Rules
- When I ask for a feature, write tests first
- Tests should FAIL initially (no implementation exists)
- Only after tests are written, implement minimal code to pass
```

### Hook for Auto-Run Tests (Optional)

Create `.claude/hooks/test-on-save.sh`:

```bash
#!/bin/bash
# Auto-run tests when test files change
if [[ "$1" == *test* ]] || [[ "$1" == *spec* ]]; then
  npm test --watchAll=false 2>&1 | head -20
fi
```

---

## The Red-Green-Refactor Cycle

### Phase 1: Red (Write Failing Test)

**Prompt**:
```
Write a failing test for [feature description].
Do NOT write the implementation yet.
The test should fail because the function/method doesn't exist.
```

**Example**:
```
Write a failing test for a function that calculates the total price
of items in a cart, applying a 10% discount if total exceeds $100.
Do NOT implement the function yet.
```

**Expected Claude behavior**:
- Creates test file with test cases
- Tests reference function that doesn't exist
- Running tests would fail with "function not defined" or similar

**Verification**:
```bash
npm test  # Should fail with "calculateCartTotal is not defined"
```

### Phase 2: Green (Minimal Implementation)

**Prompt**:
```
Now implement the minimum code to make these tests pass.
Only write enough code to pass the current tests, nothing more.
```

**Expected Claude behavior**:
- Creates implementation file
- Writes minimal code to satisfy tests
- Avoids over-engineering

**Verification**:
```bash
npm test  # Should pass
```

### Phase 3: Refactor (Clean Up)

**Prompt**:
```
Refactor the implementation to improve code quality.
Tests must stay green after refactoring.
Focus on: [readability / performance / removing duplication]
```

**Expected Claude behavior**:
- Improves code without changing behavior
- Runs tests to verify they still pass
- Documents any significant changes

---

## Integration with Claude Code Features

### With TodoWrite

Track TDD phases in your task list:

```
User: "Implement user authentication with TDD"

Claude creates todos:
- [ ] RED: Write failing tests for login
- [ ] GREEN: Implement login to pass tests
- [ ] REFACTOR: Clean up login implementation
- [ ] RED: Write failing tests for logout
- [ ] GREEN: Implement logout
- [ ] REFACTOR: Clean up
```

### With Plan Mode

Use planning for test strategy:

```
[Press Shift+Tab to enter Plan Mode]

I need to implement a shopping cart with TDD.
Plan the test cases before we start writing any code.
```

Claude will explore codebase in read-only mode, then propose test plan before any implementation.

### With Hooks

Auto-run tests after edits using a PostToolUse hook:

```json
// In .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "npm test --watchAll=false 2>&1 | head -20"
      }
    ]
  }
}
```

### With Sub-Agents

Delegate test writing to scope-focused agent:

```
Use the test-writer agent to create comprehensive tests for
the UserService class, covering all edge cases.
Then I'll implement to pass those tests.
```

---

## Anti-Patterns

### What NOT to do

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| "Write tests for this feature" | Claude implements first | "Write FAILING tests that don't exist yet" |
| "Add tests and implementation" | Loses test-first benefit | Separate into two prompts |
| "Make sure tests pass" | Encourages implementation-first | "Write tests, then implement minimally" |
| Skipping refactor phase | Accumulates technical debt | Always refactor after green |
| Multiple features at once | Loses focus | One feature per TDD cycle |

### Common Mistakes

**Mistake**: Asking Claude to "test" existing code.
```
# Wrong
"Write tests for the existing calculateTotal function"

# Right
"Write tests for calculateTotal behavior, assuming function doesn't exist.
Then we'll verify the existing implementation passes."
```

**Mistake**: Combining red and green phases.
```
# Wrong
"Implement calculateTotal with tests"

# Right
"Write failing tests for calculateTotal. Stop there."
[After tests written]
"Now implement to pass those tests."
```

---

## Advanced Patterns

### Property-Based Testing

```
Write property-based tests for the sort function.
Properties to test:
- Output length equals input length
- All input elements exist in output
- Output is ordered
Use fast-check or similar library.
```

### Mutation Testing

```
After tests pass, run mutation testing to find weak spots.
Identify tests that don't catch mutations.
```

### TDD with Legacy Code

```
I need to refactor legacyFunction.
First, write characterization tests that capture current behavior.
Then we'll refactor with confidence.
```

---

## Example Session

### User Request
```
Implement a URL shortener service with TDD.
```

### Phase 1: Red
```
Let's use TDD. First, write failing tests for:
1. Shortening a URL returns a short code
2. Retrieving a short code returns original URL
3. Invalid URLs are rejected
4. Expired links return error

Do NOT implement anything yet.
```

### Phase 2: Green
```
Tests are written and failing. Now implement the minimum
code to make them pass. Use an in-memory store for now.
```

### Phase 3: Refactor
```
Tests pass. Now refactor:
- Extract URL validation to separate function
- Add proper error types
- Improve variable names

Run tests after each change to ensure they stay green.
```

---

## See Also

- [../core/methodologies.md](../core/methodologies.md) — Full methodology reference
- [Tight Feedback Loops](../ultimate-guide.md) — Section 9.5
- [examples/skills/tdd-workflow.md](../../examples/skills/tdd-workflow.md) — TDD skill template
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [task-management.md](./task-management.md) — Track TDD cycles across sessions with Tasks API
