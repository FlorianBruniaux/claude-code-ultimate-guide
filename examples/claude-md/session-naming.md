---
title: "Session Auto-Rename"
description: "CLAUDE.md snippet to make Claude automatically name sessions with descriptive titles"
tags: [session, resume, productivity, workflow]
---

# Session Auto-Rename — CLAUDE.md Snippet

Add this block to your global `~/.claude/CLAUDE.md` to make Claude automatically rename sessions with descriptive titles after 2-3 exchanges. Helps enormously when running parallel sessions (WebStorm, split terminals, multiple projects).

## The Problem

When running multiple Claude Code sessions in parallel, they all appear as "claude" or a truncated first prompt in session pickers. Finding the right session to `/resume` becomes guesswork.

## The Solution

A behavioral instruction in CLAUDE.md — no scripts, no hooks, no plugins. Claude understands the session subject early and calls `/rename` proactively.

## Snippet

```markdown
# Session Naming (auto-rename)

## Expected behavior

1. **Early rename**: Once the session's main subject is clear (after 2-3 exchanges),
   run `/rename` with a short, descriptive title (max 50 chars)
2. **End-of-session update**: If scope shifted significantly from the initial rename,
   propose a re-rename before closing

## Title format

`[action] [subject]` — examples:
- "fix whitepaper PDF build"
- "add auth middleware + tests"
- "refactor hook system"
- "research terminal tab rename"
- "update CC releases v2.2.0"

## Rules

- Max 50 characters
- No "Session:" prefix, no date
- Action verb first (fix, add, refactor, update, research, debug...)
- Multi-topic: use the dominant subject, not an exhaustive list
- Do NOT ask for confirmation on the early rename (just do it)
- Only propose confirmation for end-of-session re-rename if title changed
```

## Usage

**Global** (all projects): Add to `~/.claude/CLAUDE.md`

**Project-level**: Add to `.claude/CLAUDE.md` or `CLAUDE.md` in the project root

## How it works

This is a pure behavioral instruction — no tooling required. Claude:
1. Infers the session's main subject from the first 2-3 exchanges
2. Calls `/rename "fix auth middleware"` automatically (no confirmation prompt)
3. If the work pivots significantly, proposes a re-rename at end of session

Named sessions appear in the `/resume` picker with their descriptive titles, making it easy to find and continue the right session.

## Limitations

- **Tab renaming**: Terminal tab names (WebStorm, iTerm2) are NOT renamed. JetBrains filters ANSI escape sequences used for tab title changes. The Claude session itself gets renamed, not the terminal tab.
- **Timing**: Claude renames after understanding the subject, not immediately on first message.

## Verification

```bash
# After a session with this configured:
claude --resume
# → Session list shows descriptive names like "fix auth middleware"
# instead of timestamps or truncated prompts
```

## Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| This (behavioral instruction) | Zero tooling, works everywhere | Claude must infer timing |
| Manual `/rename` | Full control | Requires user action |
| Hook (Stop event) | Automatic | No access to conversation context |

The behavioral instruction wins on simplicity and portability.
