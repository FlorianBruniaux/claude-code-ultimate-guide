# Module 03: Memory & Config

**Time**: 1 hour | **Complexity**: ⭐⭐ Intermediate

## Goal

Configure Claude Code to remember your preferences and project-specific rules. Build your first CLAUDE.md file.

---

## What You'll Learn

- How Claude Code's memory hierarchy works
- Creating and structuring CLAUDE.md files
- Settings and their precedence
- Custom instructions and agent definitions
- Project vs global configuration

---

## The Memory Hierarchy

Claude Code remembers preferences at three levels:

```
┌──────────────────────────────────────────┐
│ 1. GLOBAL (~/.claude/CLAUDE.md)          │
│    Applies to ALL your projects          │
│    Example: Your coding style, timezone  │
└──────────────────────────────────────────┘
                    ▲
                    │ (overridden by)
                    │
┌──────────────────────────────────────────┐
│ 2. PROJECT (/your-project/CLAUDE.md)    │
│    Applies to THIS project only          │
│    Example: Team standards, tech stack   │
└──────────────────────────────────────────┘
                    ▲
                    │ (overridden by)
                    │
┌──────────────────────────────────────────┐
│ 3. PERSONAL (/your-project/.claude/)    │
│    Local settings, not committed to git  │
│    Example: API keys, personal prefs     │
└──────────────────────────────────────────┘
```

### Rule
Settings at level 3 override level 2, which overrides level 1.

---

## Creating Your First CLAUDE.md

CLAUDE.md is a simple markdown file that tells Claude Code your rules.

### Basic Structure

```markdown
# My Project

## Purpose
Brief description of what this project does.

## Tech Stack
- TypeScript
- React 18
- Next.js
- PostgreSQL

## Coding Standards
- Use functional components only
- All exports must be typed
- Max 300 lines per file
- Use meaningful variable names (no `x`, `temp`)

## Behavioral Rules
Always review diffs before accepting.
Use /plan for any breaking changes.

## Git Workflow
- All work on feature branches
- PRs require 1 approval
- Commits must be squashed

## Current Status
What you're currently working on.
```

### Minimal Example (Start Here)

Create `/your-project/CLAUDE.md`:

```markdown
# My Project

## Quick Context
- Frontend: React with TypeScript
- Backend: Node.js with Express
- Database: PostgreSQL
- Package manager: pnpm

## Coding Rules
- Functional programming preferred
- All functions must have type signatures
- Tests are required for features
- No console.log in production code

## My Preferences
- Use /plan for architectural changes
- Be verbose in comments, not code
- Ask before making cross-file refactors
```

Claude will automatically read this file at session start and follow your rules.

---

## What Can Go in CLAUDE.md?

You can configure almost anything. Common sections:

### 1. Project Overview
```markdown
## Purpose
This is our payment processing backend.
It handles credit card validation and transaction logging.

## Important
- Handles PCI-DSS compliance critical code
- Must never log card numbers
- All changes need security review
```

### 2. Tech Stack
```markdown
## Stack
- Language: Python 3.10+
- Framework: Django 4.0
- Database: PostgreSQL 13
- Cache: Redis
- Task queue: Celery
```

### 3. Coding Standards
```markdown
## Code Style
- Follow PEP 8
- Type hints on all functions
- Docstrings in Google format
- No wildcard imports
- Max line length: 100 chars

## Testing
- Minimum 80% coverage
- Unit + integration tests
- Use pytest
```

### 4. Rules
```markdown
## Rules
- All PRs require review
- No direct pushes to main
- Database migrations need approval
- Security changes flagged automatically
- /plan mode for refactors >100 lines
```

### 5. Current Work
```markdown
## Current Task
Building the checkout flow.
Working on: src/checkout/payment-form.tsx
Dependencies: stripe-js library, payment API
```

---

## Global CLAUDE.md

For settings that apply to **all your projects**, create `~/.claude/CLAUDE.md`:

```markdown
# My Global Preferences

## Communication Style
- Be direct and factual
- Show working in steps
- Suggest alternatives when unclear

## Tools I Use
- TypeScript for all JS projects
- Python for data/scripts
- Docker for deployment
- Git for all version control

## My Timezone
America/New_York

## Work Hours
Mon-Fri 9am-5pm (UTC-5)
```

Claude will load this at startup and combine it with your project CLAUDE.md.

---

## Project-Specific vs Global

### Use Global for:
- Your general coding style (naming conventions, approach)
- Tools you always use
- Communication preferences
- General principles

### Use Project for:
- Team standards (if different from your global)
- Project-specific tech stack
- Business rules (PCI compliance, etc)
- Current work context

### Example

**Global** (~/.claude/CLAUDE.md):
```markdown
## My Style
Functional programming, clear variable names, typed functions
```

**Project** (my-payment-app/CLAUDE.md):
```markdown
## Special Rules
Security critical—use /plan for all changes.
Must handle PCI compliance.
```

Claude combines both: your style + project rules.

---

## Exercise: Create Your CLAUDE.md

### Step 1: Choose a Project

Use an existing project or create a test directory:

```bash
mkdir test-claude-config
cd test-claude-config
git init
```

### Step 2: Create CLAUDE.md

```bash
cat > CLAUDE.md << 'EOF'
# My Test Project

## Tech Stack
- Language: [your main language]
- Framework: [what you use]
- Database: [if applicable]

## Coding Standards
- [Rule 1]
- [Rule 2]

## My Preferences
- [Preference 1]
- [Preference 2]
EOF
```

### Step 3: Start Claude

```bash
claude
```

Claude will show that it loaded CLAUDE.md at startup.

### Step 4: Test It

Ask Claude to do something. It should follow your rules.

```
Add a function called greet that returns "Hello, World!"
```

Claude should:
1. Mention your tech stack
2. Follow your coding standards
3. Respect your preferences

---

## .claude/ Directory

For local settings (not committed), use `.claude/`:

```
my-project/
├── CLAUDE.md           (committed - team rules)
├── .claude/
│   ├── settings.json   (not committed - personal settings)
│   ├── agents/         (custom agents)
│   ├── skills/         (custom skills)
│   └── hooks/          (automation scripts)
```

Add to `.gitignore`:
```
.claude/
.claude/settings.json
```

Exception: You can commit `.claude/agents/` if they're team-wide.

---

## Settings.json (Optional)

For fine-grained control, create `.claude/settings.json`:

```json
{
  "model": "claude-opus-5",
  "temperature": 0.7,
  "context_threshold": 0.75,
  "auto_compact": true,
  "require_diff_review": true,
  "max_file_size": 10000
}
```

Common settings:
- **model**: Which Claude model to use
- **context_threshold**: When to warn about context (0.7 = 70%)
- **auto_compact**: Automatically compact when threshold reached
- **require_diff_review**: Force review of all changes (safe default)

---

## Agents & Skills (Preview)

In CLAUDE.md, you can reference custom agents:

```markdown
## Available Agents
- /code-reviewer: Reviews code for quality
- /security-auditor: Scans for vulnerabilities
- /test-writer: Generates test cases

Use with: /agent code-reviewer
```

These are defined in `.claude/agents/` (covered in Module 04).

---

## Best Practices

### DO

✅ Keep CLAUDE.md updated as your project evolves

✅ Version control your project CLAUDE.md (helps teammates)

✅ Be specific about requirements (not vague)

✅ Include "Current Status" section so Claude has context

✅ Document important business rules

### DON'T

❌ Store passwords or secrets in CLAUDE.md (use .env or secrets manager)

❌ Make it too long (>500 lines is overwhelming)

❌ Use conflicting rules between global and project

❌ Assume Claude will remember previous sessions' preferences

---

## Validation: You're Ready If...

✓ You've created a CLAUDE.md file in a project

✓ You can explain the three-level hierarchy (global, project, personal)

✓ You understand what should go in committed CLAUDE.md vs .claude/

✓ You've started Claude and seen it load your CLAUDE.md

✓ Claude followed at least one rule from your CLAUDE.md

---

## What's Next?

**Module 04: Agents & Specialization** covers:
- Creating specialized agents for specific tasks
- Restricting agent capabilities
- Orchestrating multiple agents
- Team workflows with agents

This teaches you how to create focused AI personas instead of using one general Claude.

---

**Completed Module 03?** → Ready for Module 04: Agents & Specialization

---

## Going Further: Cross-Session and Team Memory

The sections above cover the foundational CLAUDE.md patterns. When you're ready to go deeper, the ecosystem has more:

**Auto Memory and Auto Dream (native, v2.1.59+)**

Claude Code can write its own MEMORY.md between sessions (Auto Memory) and consolidate it in the background (Auto Dream). Both work out-of-the-box with `/memory` to manage stored entries. See [Memory Systems: Auto Memory](../core/memory-systems.md#22-auto-memory-v21594) and [Auto Dream](../core/memory-systems.md#23-auto-dream-background-consolidation).

**Cross-session tools for individual developers**

- **claude-mem** (89K stars, verified 2026-07-27) automatic session compression via hooks, no manual calls needed. Install: `/plugin marketplace add thedotmack/claude-mem`
- **agentmemory** (26K stars, verified 2026-07-27) BM25 + vector + graph hybrid retrieval, 12 auto-wired hooks, 95.2% R@5 on LongMemEval-S
- **ICM** (Rust binary) — episodic decay + permanent knowledge graph, `brew install icm`, 14 IDE clients

**Team sharing**

- The Trinity pattern: CLAUDE.md + `.mcp.json` + `/skills` all committed to the repo — zero infra, zero cost
- **Mem0 Cloud MCP** — shared memory pool via `npx mcp-add --url https://mcp.mem0.ai/mcp`, free tier
- **doobidoo** — semantic search across 13+ IDEs, local SQLite or Cloudflare D1 backend

Full coverage of all tools, architecture patterns, risks, and a decision flowchart: [Memory Systems guide](../core/memory-systems.md).
