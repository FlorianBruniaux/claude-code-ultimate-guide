---
title: "Module 04: Agents & Specialization"
description: "Learning Path Module 04: create specialized Claude Code subagents in .claude/agents/, restrict their tools, and decide when to use a subagent versus asking Claude directly. 1.5 hours, intermediate."
---

# Module 04: Agents & specialization

**Time**: 1.5 hours | **Complexity**: ⭐⭐ Intermediate

**Previous:** [Module 03: Memory & Config](03-memory.md)

## Goal

Create specialized agents for specific tasks. Learn how to focus AI capabilities on targeted problems.

---

## What you'll learn

- What agents are and why they're useful
- Creating custom agents (subagents) as `.claude/agents/<name>.md` files
- Restricting an agent's tools and permissions
- Using agents for specific tasks
- When to use agents vs Claude directly

---

## What are agents?

An **agent** (Claude Code calls it a **subagent**) is a specialized assistant with its own instructions and its own context window, configured for one specific task. Claude delegates a task to it and gets a result back.

### Example: Code reviewer agent

Instead of asking regular Claude for code reviews (which takes mental context-switching), you name the agent in your prompt:

```text
Use the code-reviewer subagent to review this function for bugs and performance issues
```

The code-reviewer agent:
- Only handles code review
- Has only the tools you gave it
- Follows the review checklist in its system prompt
- Doesn't get distracted by other tasks

There is no `/agent` slash command. You invoke a subagent three ways: by naming it in a prompt, by `@`-mentioning it, or by running the whole session as that agent with `claude --agent code-reviewer`. See [Invoke subagents explicitly](https://code.claude.com/docs/en/sub-agents#invoke-subagents-explicitly).

### Normal Claude vs agents

| Aspect | Normal Claude | Agent |
|--------|---------------|-------|
| Scope | General purpose | Specialized |
| Context | One shared conversation | Its own context window |
| Tools | All available | Restricted set (if you restrict it) |
| Speed | Multi-task capable | Fast at one thing |
| Use | Exploration, learning | Repetitive, specific tasks |

---

## Creating your first agent

A subagent is one Markdown file in `.claude/agents/` (project) or `~/.claude/agents/` (all your projects). The filename can be anything; the `name` field is the identifier. There is no `AGENT.md` file.

### Basic structure

YAML frontmatter configures the agent, and the Markdown body becomes its system prompt. Only `name` and `description` are required.

```markdown
---
name: code-reviewer
description: Reviews code for bugs, performance, and security. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a code reviewer.

## Purpose
Review code for:
- Bugs and logical errors
- Performance issues
- Security vulnerabilities
- Code style consistency
- Test coverage

## Instructions
When reviewing:
1. Run `git diff` to see the recent changes
2. Check for null pointers and edge cases
3. Look for performance bottlenecks (O(n²), nested loops)
4. Scan for security issues (SQL injection, XSS)
5. Verify tests cover the change
6. Suggest improvements without being harsh
```

The `description` tells Claude when to delegate; phrases like "use proactively" encourage automatic delegation. Field names are camelCase (`disallowedTools`, `maxTurns`) and must match exactly: Claude Code silently ignores a field it does not recognize. Fields such as `type`, `auto_invoke`, `requires_approval` and `capabilities` do not exist.

Other useful fields: `disallowedTools`, `model` (`sonnet`, `opus`, `haiku`, `fable`, a full ID, or `inherit`), `permissionMode`, `maxTurns`, `skills`, `memory`, `isolation`. See the [frontmatter reference](https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields).

### File location

Place it in your project:

```
my-project/
└── .claude/
    └── agents/
        └── code-reviewer.md
```

Claude Code watches these directories, so a new or edited file is picked up within a few seconds.

### Making it discoverable

Claude chooses subagents from their `description`. You can also list them in your project CLAUDE.md so teammates know they exist:

```markdown
## Available Subagents
Ask for them by name, for example: "Use the code-reviewer subagent on src/auth.js"

- **code-reviewer** - Code quality and security review
- **test-writer** - Generate tests for code
```

---

## Agent design patterns

The patterns below are agent templates for common jobs. For architectural patterns (Observer, Mediator, Circuit Breaker and others mapped to Claude Code mechanisms), see [AI Design Patterns](../core/ai-design-patterns.md).

### Pattern 1: Quality checker

```markdown
---
name: quality-auditor
description: Audits code quality metrics
tools: Read, Grep, Glob, Bash
---

# Quality Auditor

## Purpose
Check code for:
- Test coverage (<80% = fail)
- Type safety (TypeScript strict mode)
- Code duplication
- Cyclomatic complexity

## How to measure
- Run the project's coverage command via Bash
- Run the type checker
- Read the code for duplication and complexity

## Output Format
- ✅ Passed: [metric] = X
- ⚠️ Warning: [metric] = X
- ❌ Failed: [metric] = X

## Scoring
Score /100 based on all metrics.
```

### Pattern 2: Security specialist

```markdown
---
name: security-auditor
description: Scans code for vulnerabilities
tools: Read, Grep, Glob
---

# Security Auditor

## Purpose
Find security vulnerabilities:
- Injection attacks (SQL, NoSQL, command)
- Authentication/authorization issues
- Cryptography mistakes
- Data exposure risks
- OWASP Top 10

## Method
- Read the code paths that handle input, auth and secrets
- Grep for known risky patterns
- Report findings only; do not modify files

## Severity Levels
- CRITICAL: Stop work immediately
- HIGH: Fix before merge
- MEDIUM: Fix in next sprint
- LOW: Consider fixing
```

### Pattern 3: Documentation writer

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

## Agent capabilities & restrictions

### Default capabilities

A subagent inherits every tool available to the main conversation (including MCP tools) unless you narrow it with `tools` or `disallowedTools`. Without a restriction it can read files, edit files, and run shell commands, subject to your permission rules.

### Restricting tools

Use `tools` as an allowlist, or `disallowedTools` as a denylist:

```markdown
---
name: code-reviewer
description: Reviews code without modifying it
tools: Read, Grep, Glob
---
```

This agent can read and search but has no `Edit`, `Write` or `Bash`, so it cannot change anything.

### Common restrictions

```yaml
# Analyzer (read-only)
tools: Read, Grep, Glob
# No Bash, Edit or Write: cannot modify anything

# Refactoring agent (can edit and run tests, cannot touch the network tools)
tools: Read, Grep, Glob, Edit, Write, Bash
disallowedTools: WebFetch, WebSearch

# Full agent (inherits everything)
# omit `tools` entirely
# Can do anything the main session can (use with caution)
```

### Two traps

- Allowing `Bash` is allowing the shell: `tools: Read, Grep, Glob, Bash` still lets the agent change files and run `git push` through commands. The tool list controls tools, not commands.
- `disallowedTools: Bash(git push *)` does not block only pushes: an entry with a specifier removes the whole `Bash` tool. To block a specific command, add a deny rule in your settings (`permissions.deny: ["Bash(git push *)"]`) or enforce it with a `PreToolUse` hook (Module 06).

You can also set `permissionMode` in the frontmatter (`default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`). A subagent runs in `bypassPermissions` only when the main conversation does.

---

## Using agents in your workflow

### Calling an agent

```text
Use the code-reviewer subagent to review the changes I just made to src/auth.js
```

Or `@`-mention it from the typeahead:

```text
@"code-reviewer (agent)" look at the auth changes
```

Claude delegates to the subagent, which works in its own context window and returns a summary.

### Chaining agents

Use agents sequentially by asking for each step in turn:

```text
# Step 1: test-writer generates tests
Use the test-writer subagent to write tests for src/utils/validators.js

# Step 2: code-reviewer checks the tests
Use the code-reviewer subagent to review the tests that were just written

# Step 3: security-auditor scans
Use the security-auditor subagent to check the tests and code for vulnerabilities
```

You can also chain them in one prompt: "Use test-writer for validators.js, then code-reviewer on the result."

### Agent with plan mode

For risky operations, run the whole session as the agent and start in plan mode:

```bash
claude --agent refactoring-specialist
```

Then press `Shift+Tab` until plan mode is active (or type `/plan`) and describe the task:

```text
Refactor the payment processing module to use async/await
```

You can also pin `permissionMode: plan` in the agent's frontmatter.

---

## Exercise: Create a test-writer agent

### Step 1: Create the agent file

```bash
cat > .claude/agents/test-writer.md << 'EOF'
---
name: test-writer
description: Generates comprehensive tests. Use when asked to write or extend tests.
tools: Read, Grep, Glob, Edit, Write, Bash
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

## Tooling
- Use the project's existing test framework (Jest, pytest, etc)
- Run the new tests with Bash before reporting

## Output
- Tests in same directory as source
- Naming: [file].test.js or [file].spec.js
- Include setup/teardown code
EOF
```

### Step 2: Reference in CLAUDE.md

```markdown
## Available Subagents
- test-writer: Generate tests for any function or module
  Usage: "Use the test-writer subagent on <file path>"
```

### Step 3: Use it

```text
Use the test-writer subagent to write tests for src/utils/formatDate.js
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

## When to use agents

### Use agents when:

✅ You do the same task repeatedly (code review, testing, security audit)
✅ You want focused AI for one job
✅ You want to restrict tools (safety)
✅ You're building team workflows
✅ The task has clear success criteria

### Use regular Claude when:

✅ You're exploring/learning
✅ The task is novel
✅ You need general-purpose help
✅ You're debugging something complex
✅ You want conversational back-and-forth

---

## Best practices

### DO

✅ Give agents clear, narrow purposes

✅ Document output format in the agent definition

✅ Restrict tools you don't need

✅ Test agents on sample tasks first

✅ Version control your agents (in .claude/agents/)

### DON'T

❌ Create agents with overlapping purposes (confusing)

❌ Make agents too general (defeats the purpose)

❌ Trust an agent completely (always review)

❌ Create an agent for a one-off task (just use Claude)

---

## Validation: You're ready if...

✓ You've created at least one custom agent

✓ You understand the purpose of agents vs Claude

✓ You can restrict an agent's tools (and you know `Bash` access is not command-level control)

✓ You know how to call an agent (name it in a prompt, `@`-mention it, or `claude --agent <name>`)

✓ You've tested your agent on a real task

---

## What's next?

**Module 05: Skills & Automation** covers:
- Creating reusable skills (knowledge modules)
- Bundling capabilities for distribution
- Skill auto-invocation
- Building your custom knowledge base

This teaches you how to package knowledge so Claude remembers it across sessions.

---

**Completed Module 04?** → Ready for [Module 05: Skills & Automation](05-skills.md)
