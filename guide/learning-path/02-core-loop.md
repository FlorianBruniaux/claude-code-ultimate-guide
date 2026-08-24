# Module 02: Core Loop

**Time**: 45 minutes | **Complexity**: ⭐ Beginner

## Goal

Understand how Claude Code actually works: the decision loop, context, and how to structure requests effectively.

---

## What You'll Learn

- The complete interaction loop (prompt → analysis → decision → action)
- How Claude reads and understands your project
- How context works and why it matters
- Modes: Normal, Plan, and Think modes
- How to structure effective requests

---

## The Complete Loop (Deep Dive)

Every interaction with Claude Code follows this sequence:

```
┌──────────────────────────────────────────────────────────────┐
│ 1. YOU PROMPT                                                │
│    "Fix the bug in auth.js on line 45"                      │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 2. CLAUDE READS                                              │
│    - Reads auth.js (full file)                              │
│    - Reads related files (auth-test.js, config.js, etc)     │
│    - Understands the error context                          │
│    - Analyzes call sites where auth.js is used              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 3. CLAUDE ANALYZES                                           │
│    - Identifies the root cause                              │
│    - Considers side effects                                 │
│    - Plans minimal changes                                  │
│    - Checks for tests                                       │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 4. CLAUDE DECIDES                                            │
│    Does the change need tests? → Suggest test updates       │
│    Is the change safe? → Proceed or ask for confirmation    │
│    Should multiple files change? → Show full scope           │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 5. CLAUDE PROPOSES                                           │
│    Shows you:                                               │
│    - Description of changes                                 │
│    - diff view (what's changing)                            │
│    - Reasoning                                              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 6. YOU REVIEW                                                │
│    - Read the diff carefully                                │
│    - Ask questions if unclear                               │
│    - Accept or reject the changes                           │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 7. CHANGES APPLIED                                           │
│    - Files updated on disk                                  │
│    - You can now test/run the code                          │
│    - Next iteration begins                                  │
└──────────────────────────────────────────────────────────────┘
```

---

## How Claude Reads Your Project

Claude doesn't read everything. It's **intelligent about scope**.

### Example: You ask "Fix the login bug"

Claude will:

1. **Search for "login"** in your codebase
2. **Find auth.js, login.js, auth-controller.js**
3. **Read those files first** (full content)
4. **Find callers** (what calls these files?)
5. **Read tests** (if they exist)
6. **Find related config** (environment variables, constants)

Claude **won't** read:
- node_modules (excluded automatically)
- .git history (too much data)
- Every file in the project (too slow)
- Your entire codebase unless relevant

### Pro Tip

Be specific about scope:
- ❌ "Fix the bugs" → Claude has to guess which files
- ✅ "Fix the login bug in auth.js on line 45" → Claude reads exactly what matters

---

## Context: The Key Concept

**Context** is how much of your conversation Claude remembers. It's finite (~200K tokens).

### What Uses Context?

```
Your prompt:           50 tokens
Claude's response:     500 tokens
File reads:            2000 tokens per file
Previous messages:     accumulated tokens
```

### The Context Meter

```bash
/status
```

Shows:
```
Context: 67%
```

This means:
- 0-50%: Lots of room remaining, work freely
- 50-70%: Half-used, be mindful
- 70-90%: Getting tight, use `/compact`
- 90%+: Critical, you must clean up

### `/compact` - Your Safety Valve

When context reaches 70%+, use:

```bash
/compact
```

This:
1. Summarizes previous conversation
2. Discards old messages
3. Frees up ~40% context
4. Keeps you working in the same session

You can compact multiple times in one session.

---

## Modes: Normal vs Plan vs Think

Claude Code has three interaction modes.

### Normal Mode (Default)

Claude makes changes immediately after analyzing. Use for:
- Simple bug fixes
- Small feature additions
- Refactoring small sections

**Flow**: Ask → Analyze (1-2 sec) → Propose → Apply

### Plan Mode (`/plan`)

Claude thinks first, proposes a plan, waits for approval before making changes. Use for:
- Complex features
- Risky changes
- System-wide refactors
- When you're unsure about approach

**Flow**: Ask → Think → Propose plan → You approve → Analyze → Apply

**Example**:
```bash
/plan
Refactor the authentication system to use JWT instead of sessions
```

Claude responds with a step-by-step plan for you to review.

### Think Mode (`/think`)

Claude shows extended reasoning, thinking through the problem step-by-step. Use for:
- Understanding complex bugs
- Architectural decisions
- Security analysis
- Performance optimization

**Flow**: Ask → Extended reasoning → Analysis → Proposal

---

## Structuring Effective Requests

### The Framework: WHAT, WHERE, HOW, VERIFY

Good requests follow this pattern:

| Part | Purpose | Example |
|------|---------|---------|
| **WHAT** | The goal | "Fix the null pointer bug" |
| **WHERE** | The scope | "in `src/auth/login.js` on line 45" |
| **HOW** | Constraints | "without changing the API signature" |
| **VERIFY** | Expected result | "All existing tests should pass" |

### Example Good Request

```
Fix the bug where login fails for emails with + symbols
WHERE: src/controllers/auth.js, line 78 (email validation regex)
HOW: Update the regex to allow + in emails, but keep existing validation otherwise
VERIFY: Existing tests in tests/auth.test.js should pass
```

### Example Poor Request

```
Fix the bugs
```

Claude has to ask follow-up questions instead of solving immediately.

---

## Session Context

A **session** is your current conversation with Claude.

### Session Facts

- Starts when you run `claude`
- Ends when you exit or run `/clear`
- Not saved by default
- Scoped to one project
- Can be managed with `/rewind` (go back N steps)

### Checkpoint Sessions

To save a session (optional):
```bash
/checkpoint save "fixed login, added tests"
```

Later, restore:
```bash
/checkpoint load "fixed login, added tests"
```

---

## Exercise: The Complete Loop

### Task: Create a simple utility function

1. **Ask with WHAT/WHERE/HOW/VERIFY:**

```
Create a utility function to validate email addresses
WHERE: in src/utils/validators.js
HOW: export as validateEmail(email), return boolean, handle edge cases
VERIFY: Write tests in tests/validators.test.js
```

2. **Claude analyzes:**
   - Finds src/utils/
   - Reads existing validators
   - Checks tests directory structure
   - Proposes solution

3. **Review the diff:**
   - Check the function signature
   - Check the validation logic
   - Review the test cases

4. **Accept or iterate:**
   ```
   Looks good, but make the regex more permissive for + symbols
   ```

5. **Claude updates** and you review again

6. **Done:** You have a tested, working function

---

## Key Takeaways

✓ Every request follows: read → analyze → decide → propose → apply

✓ Be specific (WHAT/WHERE/HOW/VERIFY) for faster results

✓ Context is finite, watch your percentage and `/compact` at 70%+

✓ `/plan` for risky changes, normal mode for safe ones

✓ Sessions are temporary, use `/checkpoint` to save important work

---

## Validation: You're Ready If...

✓ You can explain the 7-step loop to someone else
✓ You understand what "context" means and why it matters
✓ You know the difference between Plan and Normal modes
✓ You've used `/plan` for a complex task
✓ You can check `/status` and understand the output

---

## What's Next?

**Module 03: Memory & Config** covers:
- Creating your first CLAUDE.md
- How Claude remembers preferences
- Project vs global settings
- Custom configuration

This will teach you how to make Claude Code remember your style and preferences.

---

**Completed Module 02?** → Ready for Module 03: Memory & Config
