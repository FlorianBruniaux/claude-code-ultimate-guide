# Claude Code Knowledge Quiz

Test your understanding of Claude Code with interactive multiple-choice questions.

[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)]()

## Quick Start

```bash
# Navigate to quiz directory
cd quiz

# Install dependencies
npm install

# Run the quiz
npm start

# Or run directly
node src/index.js
```

## Features

- **4 User Profiles**: Junior, Senior, Power User, Product Manager
- **17 Topic Categories**: From Quick Start to Advanced Patterns
- **473 Curated Questions**: Practical knowledge, not trivia
- **Immediate Feedback**: Learn from mistakes with explanations
- **Documentation Links**: Direct references to guide sections
- **Score Tracking**: See strengths and weak areas
- **Session Persistence**: History saved to `~/.claude-quiz/`
- **Cross-Platform**: Works on macOS, Linux, and Windows

## Usage

### Interactive Mode (Recommended)

```bash
npm start
```

You'll be prompted to:
1. Select your profile (Junior/Senior/Power User/PM)
2. Choose topics (all or specific sections)
3. Answer questions with A/B/C/D

### Command Line Options

```bash
node src/index.js [options]

Options:
  -p, --profile <type>   Pre-select profile (junior|senior|power|pm)
  -t, --topics <list>    Quiz specific sections (1-17, comma-separated)
  -c, --count <n>        Limit number of questions (1-50)
  -d, --dynamic          Enable dynamic question generation via claude -p
  -h, --help             Show help message
  -v, --version          Show version
```

### Examples

```bash
# Interactive mode
npm start

# Senior profile, default topics
node src/index.js -p senior

# Power user, specific topics (Agents, Hooks, MCP)
node src/index.js -p power -t 4,7,8

# Quick 10-question quiz
node src/index.js -c 10

# Junior profile with dynamic generation
node src/index.js -p junior -d
```

## Example Session

Here's what a typical quiz session looks like:

```
============================================================
   CLAUDE CODE KNOWLEDGE QUIZ
   Master Claude Code: The Complete Guide
============================================================

? Select your profile: Senior Developer (40 min to mastery)
? Select topics to quiz: Custom selection...
? Select topics (space to toggle, enter to confirm):
  ◉ [2] Core Concepts
  ◉ [4] Agents
  ◉ [7] Hooks

------------------------------------------------------------
Starting quiz: 20 questions for senior profile
------------------------------------------------------------

------------------------------------------------------------
Question 1/20 [Core Concepts]

At what context percentage should you use /compact?

  A) 0-50%
  B) 50-70%
  C) 70-90%
  D) Only at 100%

? Your answer: C

✓ CORRECT!

Progress: █░░░░░░░░░░░░░░░░░░░ 1/20 | Score: 1/1 (100%)

------------------------------------------------------------
Question 2/20 [Hooks]

What exit code should a PreToolUse hook return to BLOCK an operation?

  A) 0
  B) 1
  C) 2
  D) -1

? Your answer: A

✗ INCORRECT. The correct answer is C) 2

Explanation:
Exit code 2 blocks the operation. Exit code 0 allows it to proceed.
Other exit codes are treated as errors and logged but don't block.

See: https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#72-creating-hooks
     (Line 4164)

Progress: ██░░░░░░░░░░░░░░░░░░ 2/20 | Score: 1/2 (50%)
? Continue to next question? Yes

... (more questions) ...

============================================================
   QUIZ COMPLETE
============================================================

Overall Score: 16/20 (80%)

By Category:
  Core Concepts       6/7  (86%)  [████████░░]
  Agents              5/7  (71%)  [███████░░░]
  Hooks               5/6  (83%)  [████████░░]

Weak Areas (< 75%):
  - Agents: Review section 4 in the guide

Recommended Reading:
  4. guide/ultimate-guide.md#4-agents

Time: 9 minutes 2 seconds

------------------------------------------------------------
? What would you like to do? (Use arrow keys)
❯ Retry wrong questions only
  New quiz (different questions)
  Exit
```

## Profiles

| Profile | Questions | Focus Areas |
|---------|-----------|-------------|
| **Junior Developer** | 15 | Sections 1-3, 6 (essentials) |
| **Senior Developer** | 20 | Sections 2-4, 7, 9 (architecture, automation) |
| **Power User** | 25 | All sections |
| **Product Manager** | 10 | Sections 1-3, 16-17 (conceptual and team overview) |

## Topics

| # | Topic | Key Concepts |
|---|-------|--------------|
| 1 | Quick Start & Installation | Installation, first workflow, essential commands |
| 2 | Core Concepts | Context management, Plan Mode, interaction loop |
| 3 | Memory & Settings | CLAUDE.md, .claude/ folder, permissions |
| 4 | Agents | Custom agents, specialization, orchestration |
| 5 | Skills | Reusable knowledge, skill composition |
| 6 | Commands | Slash commands, custom commands |
| 7 | Hooks | Event system, security hooks, exit codes |
| 8 | MCP Servers | Context7, Serena, Sequential, plugins |
| 9 | Advanced Patterns | The Trinity, CI/CD, composition |
| 10 | Reference | Shortcuts, troubleshooting, daily workflow |
| 11 | Learning with AI | Learning workflows, review habits, skill development |
| 12 | Architecture Internals | Runtime architecture, context, tools, and execution |
| 13 | Security Hardening | Threat models, safe configuration, and security checks |
| 14 | Privacy & Observability | Data handling, privacy controls, and telemetry |
| 15 | AI Ecosystem | Complementary tools and integration patterns |
| 16 | Agent Harness & Context | Agent execution environments and context engineering |
| 17 | Team Metrics for AI-Augmented Engineering | DORA, SPACE, and AI delivery metrics |

## Quiz Flow

```
┌─────────────────────────────────────────────┐
│          CLAUDE CODE KNOWLEDGE QUIZ         │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  Select Profile (Junior/Senior/Power/PM)    │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  Select Topics (All or Specific 1-17)       │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  Question 1/20 [Category]                   │
│                                             │
│  What is the recommended action when...?    │
│                                             │
│    A) Option A                              │
│    B) Option B                              │
│    C) Option C                              │
│    D) Option D                              │
└─────────────────────────────────────────────┘
                     │
            ┌────────┴────────┐
            ▼                 ▼
     ┌──────────┐      ┌──────────────────┐
     │ CORRECT! │      │ INCORRECT        │
     │          │      │ Correct: C       │
     │          │      │ Explanation...   │
     │          │      │ See: guide#...   │
     └──────────┘      └──────────────────┘
            │                 │
            └────────┬────────┘
                     ▼
              (Next Question)
                     │
                     ▼
┌─────────────────────────────────────────────┐
│           QUIZ COMPLETE                     │
│                                             │
│  Overall Score: 16/20 (80%)                 │
│                                             │
│  By Category:                               │
│    Core Concepts:  6/7  (86%)  [████████░░] │
│    Agents:         5/7  (71%)  [███████░░░] │
│    Hooks:          5/6  (83%)  [████████░░] │
│                                             │
│  Weak Areas: Agents (review section 4)      │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  [R] Retry wrong questions only             │
│  [N] New quiz (different questions)         │
│  [E] Exit                                   │
└─────────────────────────────────────────────┘
```

## Session Persistence

Quiz sessions are automatically saved to `~/.claude-quiz/`:

```
~/.claude-quiz/
  sessions/
    2026-01-12_143052.json   # Individual session data
    2026-01-12_150623.json
  stats.json                  # Aggregate statistics
```

### Session Data Includes:
- Profile and topics selected
- Questions answered (correct/incorrect/skipped)
- Time taken
- Category breakdown
- Wrong questions with correct answers

## Dynamic Question Generation

When the `--dynamic` flag is enabled and the Claude CLI is installed, the quiz can generate additional questions on-the-fly using `claude -p`:

```bash
node src/index.js -d
```

This requires:
- Claude CLI installed (`npm install -g @anthropic-ai/claude-code`)
- Active API key configured

Dynamic questions supplement the static pool when:
- Static pool is exhausted for selected topics
- User requests fresh questions
- Variety is needed for repeated quizzes

## Question bank: source of truth

The files under `questions/*.yaml` are **generated, not hand-edited**. The single
source of truth for quiz questions is the web quiz in the landing repo, one
Markdown file per question under `src/content/questions/`. The CLI YAML is
regenerated from it.

This is deliberate. The CLI bank and the web bank once drifted into two separate
question sets (different totals, different answers in the same id slots). One
canonical source plus a generator is what stops that from happening again.

### Regenerating the CLI YAML

From this `quiz/` directory:

```bash
# Rewrite questions/*.yaml from the web bank (sibling landing repo)
pnpm sync-from-web

# CI / pre-push guard: fail if the YAML is out of sync with the web bank
pnpm sync-from-web:check
```

The generator lives at [`scripts/generate-from-web.mjs`](./scripts/generate-from-web.mjs).
By default it reads `../../claude-code-ultimate-guide-landing/src/content/questions`;
pass `--web <dir>` to point elsewhere. It preserves each category's header
(name, `source_file`) and replaces only the questions.

## Contributing Questions

Add or edit questions in the **web bank** (`src/content/questions/<NN-slug>/`),
then regenerate the CLI YAML. Do not edit `questions/*.yaml` by hand; the next
`sync-from-web` will overwrite your change.

### Quality Guidelines

**Good questions test:**
- Practical application ("When should you...")
- Decision-making ("Which approach is best for...")
- Understanding ("Why does Claude...")
- Troubleshooting ("What would you do if...")

**Avoid:**
- Trivia ("What is the exact command syntax...")
- Pure memorization ("List all keyboard shortcuts...")
- Version-specific details that may change

### Submitting Questions

1. Fork the landing repository
2. Add a Markdown question under `src/content/questions/<NN-category-slug>/`
3. Ensure `doc_reference` points to a valid guide section
4. Run `pnpm sync-from-web` in `quiz/` to regenerate the CLI YAML
5. Submit a PR with both the new Markdown and the regenerated YAML

## Troubleshooting

### "No questions available"

- Check that selected topics have questions in `questions/` directory
- Verify YAML files are valid (use a YAML validator)
- Try selecting different topics or "All topics"

### "Cannot find module 'yaml'"

```bash
cd quiz
npm install
```

### Quiz hangs on input

- Ensure you're running in an interactive terminal
- Try pressing Enter if stuck
- Use Ctrl+C to exit and restart

## License

Same as parent repository: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

---

**Part of**: [claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)
