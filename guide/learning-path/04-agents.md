---
title: "Module 04: Agents & Specialization"
description: "Learning Path Module 04: create specialized Claude Code agents with AGENT.md, restrict their capabilities, and decide when to use an agent versus asking Claude directly. 1.5 hours, intermediate."
---

# Module 04: Agents & Specialization

**Time**: 1.5 hours | **Complexity**: ⭐⭐ Intermediate

## Goal

Create specialized agents for specific tasks. Learn how to focus AI capabilities on targeted problems.

---

## What You'll Learn

- What agents are and why they're useful
- Creating custom agents with AGENT.md
- Restricting agent capabilities (sandboxing)
- Using agents for specific tasks
- When to use agents vs Claude directly

---

## What Are Agents?

An **agent** is a specialized version of Claude Code configured for one specific task.

### Example: Code Reviewer Agent

Instead of asking regular Claude for code reviews (which takes mental context-switching), you use:

```bash
/agent code-reviewer
Review this function for bugs and performance issues
```

The code-reviewer agent:
- Only handles code review
- Has review-specific tools
- Knows security vulnerability patterns
- Doesn't get distracted by other tasks

### Normal Claude vs Agents

| Aspect | Normal Claude | Agent |
|--------|---------------|-------|
| Scope | General purpose | Specialized |
| Context | Remembers everything | Focused task memory |
| Tools | All available | Restricted set |
| Speed | Multi-task capable | Fast at one thing |
| Use | Exploration, learning | Repetitive, specific tasks |

---

## Creating Your First Agent

Agents are defined in `.claude/agents/AGENT.md` files.

### Basic Structure

```markdown
---
name: code-reviewer
type: agent
description: Reviews code for bugs, performance, and security
auto_invoke: false
requires_approval: true
---

# Code Reviewer Agent

## Purpose
Review code for:
- Bugs and logical errors
- Performance issues
- Security vulnerabilities
- Code style consistency
- Test coverage

## Tools
- Code analysis
- Git diff viewer
- Test runner
- Linting tools

## Instructions
When reviewing:
1. Check for null pointers and edge cases
2. Look for performance bottlenecks (O(n²), nested loops)
3. Scan for security issues (SQL injection, XSS)
4. Verify tests cover the change
5. Suggest improvements without being harsh

## Example Usage
/agent code-reviewer
Review src/auth.js for security issues
```

### File Location

Place it in your project:

```
my-project/
└── .claude/
    └── agents/
        └── code-reviewer.md
```

### Making It Available

In your project CLAUDE.md, reference it:

```markdown
## Available Agents
Run agents with: /agent [name]

- **code-reviewer** - Code quality and security review
  Usage: /agent code-reviewer <description>
  
- **test-writer** - Generate tests for code
  Usage: /agent test-writer <file path>
```

---

## Agent Design Patterns

### Pattern 1: Quality Checker

```markdown
---
name: quality-auditor
description: Audits code quality metrics
---

# Quality Auditor

## Purpose
Check code for:
- Test coverage (<80% = fail)
- Type safety (TypeScript strict mode)
- Code duplication
- Cyclomatic complexity

## Tools
- Code analysis
- Coverage reporter
- Type checker

## Output Format
- ✅ Passed: [metric] = X
- ⚠️ Warning: [metric] = X
- ❌ Failed: [metric] = X

## Scoring
Score /100 based on all metrics.
```

### Pattern 2: Security Specialist

```markdown
---
name: security-auditor
description: Scans code for vulnerabilities
requires_approval: true
---

# Security Auditor

## Purpose
Find security vulnerabilities:
- Injection attacks (SQL, NoSQL, command)
- Authentication/authorization issues
- Cryptography mistakes
- Data exposure risks
- OWASP Top 10

## Tools
- Static analysis
- Dependency checker
- Secret detection

## Severity Levels
- CRITICAL: Stop work immediately
- HIGH: Fix before merge
- MEDIUM: Fix in next sprint
- LOW: Consider fixing
```

### Pattern 3: Documentation Writer

```markdown
---
name: doc-writer
description: Generates documentation
---

# Documentation Writer

## Purpose
Create or improve:
- README files
- API documentation
- Architecture docs
- User guides
- CHANGELOG entries

## Output Format
- Clear headings
- Code examples for each feature
- Link to related docs
- Numbered lists for sequences

## Style
- Beginner-friendly
- No jargon without explanation
- Show before/after examples
```

---

## Agent Capabilities & Restrictions

### Default Capabilities

All agents can:
- Read files (git-aware)
- Analyze code
- Write documentation
- Check syntax
- Run tests

### Restricting Capabilities

Use `capabilities` to sandbox an agent:

```markdown
---
name: code-reviewer
capabilities:
  - read_files      # Can read code
  - run_tests       # Can run test suites
  - check_syntax    # Can lint
  - write_comments  # Can suggest changes but...
  - NO: commit      # ...cannot commit
  - NO: push        # ...cannot push to git
---
```

This agent can review but can't accidentally push broken code.

### Common Restrictions

```markdown
# Analyzer (read-only)
capabilities:
  - read_files
  - run_tests
# Can't modify anything

# Refactoring Agent (write, no push)
capabilities:
  - read_files
  - write_files
  - run_tests
  - NO: commit
  - NO: push
# Can change code but you review before pushing

# Full Agent (unrestricted)
capabilities:
  - all
# Can do anything (use with caution)
```

---

## Using Agents in Your Workflow

### Calling an Agent

```bash
/agent code-reviewer
Review the changes I just made to src/auth.js
```

Claude switches to the code-reviewer agent and responds.

### Chaining Agents

Use agents sequentially:

```bash
# Step 1: Test Writer generates tests
/agent test-writer
Write tests for src/utils/validators.js

# Step 2: Code Reviewer checks the tests
/agent code-reviewer
Review the tests that were just written

# Step 3: Security Auditor scans
/agent security-auditor
Check the tests and code for vulnerabilities
```

### Agent with Plan Mode

For risky operations, use `/plan` within an agent:

```bash
/agent refactoring-specialist
/plan
Refactor the payment processing module to use async/await
```

---

## Exercise: Create a Test-Writer Agent

### Step 1: Create the Agent File

```bash
cat > .claude/agents/test-writer.md << 'EOF'
---
name: test-writer
description: Generates comprehensive tests
capabilities:
  - read_files
  - write_files
  - run_tests
---

# Test Writer Agent

## Purpose
Generate high-quality tests for:
- Unit tests (pure functions)
- Integration tests (component interactions)
- Edge cases and error conditions
- Performance tests

## Style
- Arrange-Act-Assert pattern
- Descriptive test names
- Each test focuses on ONE behavior
- 70%+ code coverage target

## Tools
- Test framework (Jest, pytest, etc)
- Mock libraries
- Assertion libraries

## Output
- Tests in same directory as source
- Naming: [file].test.js or [file].spec.js
- Include setup/teardown code
EOF
```

### Step 2: Reference in CLAUDE.md

```markdown
## Available Agents
- test-writer: Generate tests for any function or module
  Usage: /agent test-writer <file path>
```

### Step 3: Use It

```bash
/agent test-writer
Write tests for src/utils/formatDate.js
```

The agent will:
1. Read formatDate.js
2. Understand what it does
3. Generate comprehensive tests
4. Show you the test file

### Step 4: Review

Check the tests before accepting:
- Do they cover edge cases?
- Is naming clear?
- Do they actually run?

---

## When to Use Agents

### Use Agents When:

✅ You do the same task repeatedly (code review, testing, security audit)
✅ You want focused AI for one job
✅ You want to restrict capabilities (safety)
✅ You're building team workflows
✅ The task has clear success criteria

### Use Regular Claude When:

✅ You're exploring/learning
✅ The task is novel
✅ You need general-purpose help
✅ You're debugging something complex
✅ You want conversational back-and-forth

---

## Best Practices

### DO

✅ Give agents clear, narrow purposes

✅ Document output format in the agent definition

✅ Restrict capabilities you don't need

✅ Test agents on sample tasks first

✅ Version control your agents (in .claude/agents/)

### DON'T

❌ Create agents with overlapping purposes (confusing)

❌ Make agents too general (defeats the purpose)

❌ Trust an agent completely (always review)

❌ Create an agent for a one-off task (just use Claude)

---

## Validation: You're Ready If...

✓ You've created at least one custom agent

✓ You understand the purpose of agents vs Claude

✓ You can restrict agent capabilities

✓ You know how to call an agent (/agent name)

✓ You've tested your agent on a real task

---

## What's Next?

**Module 05: Skills & Automation** covers:
- Creating reusable skills (knowledge modules)
- Bundling capabilities for distribution
- Skill auto-invocation
- Building your custom knowledge base

This teaches you how to package knowledge so Claude remembers it across sessions.

---

**Completed Module 04?** → Ready for Module 05: Skills & Automation
