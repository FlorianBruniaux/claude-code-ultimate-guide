---
title: "Module 01: Installation & setup"
description: "Learning Path Module 01: install Claude Code, verify that it runs, and send your first command. 15 minutes, beginner."
---

# Module 01: Installation & setup

**Time**: 15 minutes | **Complexity**: ⭐ Beginner

## Goal

Get Claude Code installed and running on your system. Verify it works with your first command.

---

## What you'll learn

- Install Claude Code for your platform (macOS / Linux / Windows)
- Understand the basic prompt → response loop
- Run your first command
- Access the help system

---

## Installation

### macOS, Linux, WSL (native installer, recommended)

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Open a new terminal window, then verify:
```bash
claude --version
```

The native installer updates itself in the background.

### macOS (Homebrew)

```bash
brew install --cask claude-code
```

Homebrew installs do not auto-update. Run `brew upgrade claude-code` periodically.

### Windows

PowerShell:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Or with WinGet:

```powershell
winget install Anthropic.ClaudeCode
```

WinGet installs do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically. [Git for Windows](https://git-scm.com/downloads/win) is recommended on native Windows so Claude Code can use the Bash tool; WSL setups do not need it.

Debian, Fedora, RHEL, and Alpine users can also install with apt, dnf, or apk. See the official [setup page](https://code.claude.com/docs/en/setup).

---

## First run

Navigate to any project directory and start Claude:

```bash
cd ~/my-project
claude
```

The first time, Claude Code asks you to sign in. After that it opens an interactive session in your terminal: a welcome screen with the version, the active model and the working directory, then a prompt where you type. The exact layout changes between versions.

---

## Essential commands

| Command | Purpose |
|---------|---------|
| `/help` | Show all available commands |
| `/context` | Visualize current context usage |
| `/clear` | Start a new conversation with empty context |
| `/resume` | Resume a previous conversation |
| `Ctrl+C` | Cancel the current operation |
| `/exit` | Close Claude Code |

---

## Your first 5 minutes

### Exercise 1: View available commands
```bash
/help
```

Review the command list. Notice:
- **Workflow**: `/plan`, `/rewind`, `/effort`
- **Sessions**: `/resume`, `/clear`, `/compact`
- **Memory**: `/memory`, `/init`
- **Advanced**: `/model`, `/permissions`

### Exercise 2: Check context usage
```bash
/context
```

You'll see a colored grid of what currently fills the context window, plus optimization suggestions when something is heavy. (`/status` is a different command: it opens the settings screen on a tab showing version, model, account and connectivity.)

### Exercise 3: Ask Claude something

```
What files are in my project?
```

Claude will read the project structure and respond. This is the core loop:

```
Your prompt → Claude reads files → Claude suggests changes → You review → Apply
```

### Exercise 4: Review a suggested change

If Claude suggests code changes, you'll see:
1. A description of the change
2. A `diff` view (what's being added/removed)
3. A prompt to accept or reject

**Rule**: Always review diffs before accepting. This protects you from unexpected changes.

---

## The core concept: The loop

Every interaction follows this pattern:

```
┌─────────────┐
│ You ask     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Claude      │
│ reads files │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Claude      │
│ suggests    │
│ changes     │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ You review diff  │
│ and approve      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Changes applied  │
│ to your files    │
└──────────────────┘
```

---

## Key concepts

### Sessions

Each time you run `claude`, you start a new **session**. A session is a conversation with Claude that persists while you're using Claude Code.

- Claude Code **saves every conversation locally**. Resume the latest one in the current directory with `claude --continue`, or pick one with `claude --resume` or `/resume`
- Sessions are **scoped to one project** at a time
- Your context grows as you ask more questions, up to the model's context window (1M tokens on most current models)

### Context

**Context** is how much of the conversation Claude can see at once. Run `/context` to see how full it is.

Working rules of thumb:
- Plenty of room: work freely
- Getting full: be selective, `/compact` optional
- Close to the limit: run `/compact` to free space (Claude Code also compacts automatically near the top of the window)
- Switching to an unrelated task: `/clear` instead of carrying old context along

### Git awareness

Claude Code works with git through ordinary git commands. It can:
- Read your current branch and uncommitted changes
- Help with commits and reviews
- Ask for your approval before running commands or editing files (in the default permission mode)

---

## Validation: You're ready if...

✓ You can run `claude --version` and see your installed version
✓ You can start Claude in a project with `claude`
✓ You understand the prompt → response loop
✓ You can run `/context` and understand what it shows
✓ You've reviewed at least one diff from Claude

---

## What's next?

Once you're comfortable with this module, move to **Module 02: Core Loop** to understand:
- How Claude reads your project
- How context works in depth
- How to structure requests for better results
- Plan mode, permission modes and effort levels

**Time to next module**: Ready immediately (no prerequisites beyond running Claude once)

---

## Troubleshooting

### "claude: command not found"
The install directory is probably not on your PATH yet. Try:
- Open a new terminal window: the installer may have added the install directory to your PATH only for new shells
- Re-run the install command for your platform
- See [Fix your PATH](https://code.claude.com/docs/en/troubleshoot-install#command-not-found-claude-after-installation) in the official troubleshooting page

### Install command fails with a syntax error, a 403 or another error
Match the error to a fix in [Troubleshoot installation](https://code.claude.com/docs/en/troubleshoot-install#find-your-error), which also lists alternative install methods.

### The command works in PowerShell but not in CMD (or the reverse)
`irm ... | iex` is PowerShell only. In CMD, use `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`.

---

## Resources

- **Official Docs**: https://code.claude.com/docs
- **FAQ**: See `guide/ultimate-guide.md` Appendix B
- **Examples**: `examples/` directory in this guide

---

**Completed Module 01?** → Ready for [Module 02: Core Loop](02-core-loop.md)
