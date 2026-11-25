---
title: "Module 03: Memory & config"
description: "Learning Path Module 03: make Claude Code remember your preferences and project rules, and build your first CLAUDE.md file. 1 hour, intermediate."
---

# Module 03: Memory & config

**Time**: 1 hour | **Complexity**: ⭐⭐ Intermediate

## Goal

Configure Claude Code to remember your preferences and project-specific rules. Build your first CLAUDE.md file.

---

## What you'll learn

- How Claude Code's memory hierarchy works
- Creating and structuring CLAUDE.md files
- Settings and their precedence
- Custom instructions and agent definitions
- Project vs global configuration

---

## The memory hierarchy

Claude Code loads instructions from several CLAUDE.md files, from the broadest scope to the most specific:

```
┌──────────────────────────────────────────┐
│ 1. USER (~/.claude/CLAUDE.md)            │
│    Applies to ALL your projects          │
│    Example: Your coding style, timezone  │
└──────────────────────────────────────────┘
                    │
                    ▼ (project instructions load after)
┌──────────────────────────────────────────┐
│ 2. PROJECT (/your-project/CLAUDE.md)     │
│    Shared with the team through git      │
│    Example: Team standards, tech stack   │
└──────────────────────────────────────────┘
                    │
                    ▼ (local instructions load after)
┌──────────────────────────────────────────┐
│ 3. LOCAL (/your-project/CLAUDE.local.md) │
│    Your private notes for THIS project   │
│    Gitignored, not shared                │
│    Example: sandbox URLs, test data      │
└──────────────────────────────────────────┘
```

Organizations can also deploy a managed policy CLAUDE.md that applies to every user (for example `/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS).

### Rule
All applicable files are loaded and combined, with the more specific file placed after the broader one. They are instructions, not enforced settings, so avoid contradicting yourself between levels. Strict precedence exists for **settings** (see `settings.json` below), not for CLAUDE.md text.

`CLAUDE.md` files in the directories above your working directory load at launch. Files in subdirectories load on demand.

---

## Creating your first CLAUDE.md

CLAUDE.md is a simple markdown file that tells Claude Code your rules.

### Basic structure

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

### Minimal example (start here)

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

Claude Code loads this file at session start and treats it as instructions for the session.

---

## What can go in CLAUDE.md?

You can configure almost anything. Common sections:

### 1. Project overview
```markdown
## Purpose
This is our payment processing backend.
It handles credit card validation and transaction logging.

## Important
- Handles PCI-DSS compliance critical code
- Must never log card numbers
- All changes need security review
```

### 2. Tech stack
```markdown
## Stack
- Language: Python 3.10+
- Framework: Django 4.0
- Database: PostgreSQL 13
- Cache: Redis
- Task queue: Celery
```

### 3. Coding standards
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

### 5. Current work
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

Claude loads this at startup and combines it with your project CLAUDE.md.

---

## Project-specific vs global

### Use global for:
- Your general coding style (naming conventions, approach)
- Tools you always use
- Communication preferences
- General principles

### Use project for:
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
Security critical: use /plan for all changes.
Must handle PCI compliance.
```

Claude combines both: your style + project rules.

---

## Exercise: Create your CLAUDE.md

### Step 1: Choose a project

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

Run `/memory` to see which CLAUDE.md files are loaded.

### Step 4: Test it

Ask Claude to do something. It should follow your rules.

```
Add a function called greet that returns "Hello, World!"
```

Claude should:
1. Mention your tech stack
2. Follow your coding standards
3. Respect your preferences

---

## .claude/ directory

Project configuration lives in `.claude/`. Most of it is meant to be committed so the team shares it; only personal files stay local:

```
my-project/
├── CLAUDE.md                 (committed - team rules)
├── CLAUDE.local.md           (NOT committed - your private notes)
├── .claude/
│   ├── settings.json         (committed - shared project settings)
│   ├── settings.local.json   (NOT committed - your personal overrides)
│   ├── agents/               (committed - project subagents)
│   ├── skills/               (committed - project skills)
│   └── hooks/                (committed - automation scripts)
```

Add only the personal files to `.gitignore`:
```
.claude/settings.local.json
CLAUDE.local.md
```

Do not ignore the whole `.claude/` directory: that would hide the shared settings, agents and skills from your teammates. Claude Code adds `.claude/settings.local.json` to your global gitignore when it saves a setting there, but `CLAUDE.local.md` you create by hand, so ignore it yourself.

---

## Settings.json (Optional)

For fine-grained control, create `.claude/settings.json` (shared) or `.claude/settings.local.json` (personal):

```json
{
  "model": "opus",
  "autoCompactEnabled": true,
  "permissions": {
    "defaultMode": "default",
    "allow": ["Bash(npm test *)"]
  }
}
```

Common settings:
- **model**: Which Claude model to use (an alias such as `opus` or `sonnet`, or a full model ID)
- **autoCompactEnabled**: Automatic compaction near the context limit (also toggled in `/config`)
- **permissions.defaultMode**: The permission mode a session starts in (`default` prompts before edits)
- **permissions.allow / permissions.deny**: Rules that approve or block specific tool calls

Keys such as `temperature`, `context_threshold`, `auto_compact` or `require_diff_review` are not Claude Code settings. Unknown keys do nothing, so check names against the [settings reference](https://code.claude.com/docs/en/settings).

Settings precedence, from highest to lowest: managed settings, command-line arguments, `.claude/settings.local.json`, `.claude/settings.json`, then `~/.claude/settings.json`.

---

## Agents & skills (preview)

In CLAUDE.md, you can tell Claude which subagents exist and when to use them:

```markdown
## Available Subagents
- code-reviewer: Reviews code for quality
- security-auditor: Scans for vulnerabilities
- test-writer: Generates test cases

Ask for one by name: "Use the code-reviewer subagent on my last change"
```

Subagents are defined in `.claude/agents/` (covered in Module 04). They are not slash commands.

---

## Best practices

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

❌ Assume Claude remembers a preference from a previous session unless it is written in CLAUDE.md (or saved by auto memory)

---

## Validation: You're ready if...

✓ You've created a CLAUDE.md file in a project

✓ You can explain the CLAUDE.md levels (user, project, local) and why `.claude/` is mostly committed

✓ You know which files to gitignore: `.claude/settings.local.json` and `CLAUDE.local.md`

✓ You've started Claude and confirmed with `/memory` that it loaded your CLAUDE.md

✓ Claude followed at least one rule from your CLAUDE.md

---

## What's next?

**Module 04: Agents & Specialization** covers:
- Creating specialized agents for specific tasks
- Restricting agent capabilities
- Orchestrating multiple agents
- Team workflows with agents

This teaches you how to create focused AI personas instead of using one general Claude.

---

**Completed Module 03?** → Ready for Module 04: Agents & Specialization

---

## Going further: Cross-Session and team memory

The sections above cover the foundational CLAUDE.md patterns. When you're ready to go deeper, the ecosystem has more:

**Auto memory (native) and Auto Dream (community-discovered)**

Claude Code can write its own MEMORY.md between sessions (auto memory, documented by Anthropic). Use `/memory` to enable or disable it and to view stored entries. Auto Dream, a background consolidation pass over that memory, is not in Anthropic's documentation: it was reverse-engineered by the community and may be gated or change. See [Memory Systems: Auto Memory](../core/memory-systems.md#22-auto-memory-v2159) and [Auto Dream](../core/memory-systems.md#23-auto-dream-memory-consolidation).

**Cross-session tools for individual developers**

- **claude-mem** (111K stars, verified 2026-11-03) automatic session compression via hooks, no manual calls needed. Turn on secret redaction, which is off by default. Install: `/plugin marketplace add thedotmack/claude-mem`
- **agentmemory** (30K stars, verified 2026-11-03) BM25 + vector + graph hybrid retrieval, 12 hooks that capture by default (context injection is opt-in), self-reported 95.2% R@5 on LongMemEval-S
- **ICM** (Rust binary): episodic decay + permanent knowledge graph, `brew install icm`, 14 IDE clients

**Team sharing**

- The Trinity pattern: CLAUDE.md + `.mcp.json` + `/skills` all committed to the repo. Zero infra, zero cost.
- **Mem0 Cloud MCP**: shared memory pool via `npx mcp-add --url https://mcp.mem0.ai/mcp`, free tier
- **doobidoo**: semantic search across 13+ IDEs, local SQLite or Cloudflare D1 backend

Full coverage of all tools, architecture patterns, risks, and a decision flowchart: [Memory Systems guide](../core/memory-systems.md).
