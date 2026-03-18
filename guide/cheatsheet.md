---
title: "Claude Code Cheatsheet"
description: "One-page printable daily essentials for maximum Claude Code productivity"
tags: [cheatsheet, reference]
---

# Claude Code Cheatsheet

**1 printable page** - Daily essentials for maximum productivity

**Author**: Florian BRUNIAUX | Founding Engineer [@Méthode Aristote](https://methode-aristote.fr)

**Written with**: Claude (Anthropic)

**Version**: 3.37.0 | **Last Updated**: March 2026

---

## Essential Commands

| Command | Action |
|---------|--------|
| `/help` | Contextual help |
| `/clear` | Reset conversation |
| `/compact` | Free up context |
| `/status` | Session state + context usage |
| `/context` | Detailed token breakdown |
| `/plan` | Enter Plan Mode (no changes) |
| `/execute` | Exit Plan Mode (apply changes) |
| `/model` | Switch model (sonnet/opus/opusplan) |
| `/insights` | Usage analytics + optimization report |
| `/simplify` | Detect over-engineering in changed code + auto-fix |
| `/batch` | Large-scale refactors via 5–30 parallel worktree agents |
| `/teleport` | Teleport session from web |
| `/tasks` | Monitor background tasks |
| `/remote-env` | Configure cloud environment |
| `/remote-control` | Start remote control session (Research Preview, Pro/Max) |
| `/rc` | Alias for /remote-control |
| `/mobile` | Get Claude mobile app download links |
| `/fast` | Toggle fast mode (2.5x speed, 6x cost) |
| `/voice` | Toggle voice input (hold Space to speak, release to send) |
| `/btw [question]` | Side question overlay — read-only ephemeral agent, no history pollution, no tools |
| `/loop [interval] [prompt]` | Run a prompt on repeat (ex: `/loop 5m check the deploy`, default 10m) |
| `/stats` | Usage graph, favorite model, streak |
| `/rename [name]` | Name or rename the current session |
| `/copy` | Interactive picker to copy a code block or full response |
| `/debug` | Systematic troubleshooting |
| `/exit` | Quit (or Ctrl+D) |

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Cycle permission modes |
| `Esc` × 2 | Rewind (undo) |
| `Ctrl+C` | Interrupt |
| `Ctrl+R` | Search command history |
| `Ctrl+L` | Clear screen (keeps context) |
| `Tab` | Autocomplete |
| `Shift+Enter` | New line |
| `Ctrl+B` | Background tasks |
| `Ctrl+F` | Kill all background agents (double press) |
| `Alt+T` | Toggle thinking |
| `Space` (hold) | Voice input (requires `/voice` enabled) |
| `Ctrl+D` | Exit |

---

## File References

```
@path/to/file.ts    → Reference a file
@agent-name         → Call an agent
!shell-command      → Run shell command
```

| IDE | Shortcut |
|-----|----------|
| VS Code | `Alt+K` |
| JetBrains | `Cmd+Option+K` |

---

## Features Méconnues (But Official!)

| Feature | Since | What It Does |
|---------|-------|--------------|
| **Tasks API** | v2.1.16 | Persistent task lists with dependencies |
| **Background Agents** | v2.0.60 | Sub-agents work while you code |
| **Agent Teams** | v2.1.32 | Multi-agent coordination (TeamCreate/SendMessage) |
| **Auto-Memories** | v2.1.32 | Automatic cross-session context capture |
| **Session Forking** | v2.1.19 | Rewind + create parallel timeline |
| **LSP Tool** | v2.0.74 | IDE-like navigation: symbols, types, refs. ~50ms vs 45s with grep. 11 languages |
| **Voice Mode** | v2.1.x | Native voice input, free transcription, no rate limit impact |
| **Remote Control** | v2.1.51 | Control local session from phone/browser (Research Preview, Pro/Max) |
| **`/loop`** | v2.1.71 | Recurring scheduler: `/loop 5m check the deploy` — runs in background while you work |
| **Skill Evals** | Mar 2026 | Two skill types: Capability Uplift (fills model gap, fades) / Encoded Preference (encodes workflow, stays). Benchmark Mode, A/B testing, Trigger Tuning. |

**Activate LSP**: Add to `~/.claude/settings.json` → `{ "env": { "ENABLE_LSP_TOOL": "1" } }` (requires LSP server installed for your language: `tsserver`, `pylsp`, `gopls`, `rust-analyzer`, `sourcekit-lsp`...)

**Pro tip**: These aren't "secrets"—they're in the [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md). Read it!

---

## Permission Modes

| Mode | Editing | Execution |
|------|---------|-----------|
| Default | Asks | Asks |
| acceptEdits | Auto | Asks |
| Plan Mode | ❌ | ❌ |
| dontAsk | Only if in allow rules | Only if in allow rules |
| bypassPermissions | Auto | Auto (CI/CD only) |

**Shift+Tab** to switch modes

---

## Memory & Settings (2 levels)

| Level | macOS/Linux | Windows | Scope | Git |
|-------|-------------|---------|-------|-----|
| **Project** | `.claude/` | `.claude\` | Team | ✅ |
| **Personal** | `~/.claude/` | `%USERPROFILE%\.claude\` | You (all projects) | ❌ |

**Priority**: Project overrides Personal

| File | Where | Usage |
|------|-------|-------|
| `CLAUDE.md` | Project root | Team memory (instructions) |
| `settings.json` | `.claude/` | Team settings (hooks) |
| `settings.local.json` | `.claude/` | Your setting overrides |
| `CLAUDE.md` | `~/.claude/` (Win: `%USERPROFILE%\.claude\`) | Personal memory |

---

## .claude/ Folder Structure

```
.claude/
├── CLAUDE.md           # Local memory (gitignored)
├── settings.json       # Hooks (committed)
├── settings.local.json # Permissions (not committed)
├── agents/             # Custom agents
├── commands/           # Slash commands
├── hooks/              # Event scripts
├── rules/              # Auto-loaded rules
└── skills/             # Knowledge modules
```

---

## Typical Workflow

```
1. Start session      → claude
2. Check context      → /status
3. Plan Mode          → Shift+Tab × 2 (for complex tasks)
4. Describe task      → Clear, specific prompt
5. Review changes     → Always read the diff!
6. Accept/Reject      → y/n
7. Verify             → Run tests
8. Commit             → When task complete
9. /compact           → When context >70%
```

---

## Context Management (CRITICAL)

### Statusline

```
Model: Sonnet | Ctx: 89.5k | Cost: $2.11 | Ctx(u): 56.0%
```
**Watch `Ctx(u):`** → >70% = `/compact`, >85% = `/clear`

**Enhanced statusline ([ccstatusline](https://github.com/sirmalloc/ccstatusline)):** Add to `~/.claude/settings.json`:
```json
{ "statusLine": { "type": "command", "command": "npx -y ccstatusline@latest", "padding": 0 } }
```

### Context Thresholds

| Context % | Status | Action |
|-----------|--------|--------|
| 0-50% | Green | Work freely |
| 50-70% | Yellow | Be selective |
| 70-90% | Orange | `/compact` now |
| 90%+ | Red | `/clear` required |

### Actions by Symptom

| Sign | Action |
|------|--------|
| Short responses | `/compact` |
| Frequent forgetting | `/clear` |
| >70% context | `/compact` |
| Task complete | `/clear` |

### Context Recovery Commands

| Command | Usage |
|---------|-------|
| `/compact` | Summarize and free context |
| `/clear` | Fresh start |
| `/rewind` | Undo recent changes |
| `claude -c` | Resume last session (CLI flag) |
| `claude -r <id>` | Resume specific session (CLI flag) |

---

## Under the Hood (Quick Facts)

| Concept | Key Point |
|---------|-----------|
| **Master Loop** | Simple `while(tool_call)` — no DAGs, no classifiers |
| **Tools** | 8 core: Bash, Read, Edit, Write, Grep, Glob, Task, TodoWrite |
| **Context** | ~200K tokens, auto-compacts at 75-92% |
| **Sub-agents** | Isolated context, max depth=1 |
| **Philosophy** | "Less scaffolding, more model" — trust Claude's reasoning |

**Deep dive**: [Architecture & Internals](./core/architecture.md)

---

## Plan Mode & Thinking

| Feature | Activation | Usage |
|---------|------------|-------|
| **Plan Mode** | `Shift+Tab × 2` or `/plan` | Explore without modifying |
| **OpusPlan** | `/model opusplan` | Opus for planning, Sonnet for execution |

> **Opus 4.6** (v2.1.68+): Default effort = **medium** for Max/Team. Use `ultrathink` to force high effort for the next turn. "think hard" remains cosmetic.

| Control | Action | Persistence |
|---------|--------|-------------|
| **Alt+T** | Toggle thinking on/off | Session |
| **/config** | Enable/disable globally | Permanent |
| **`/model` slider** | Left/right arrows: `low\|medium\|high` | Session |
| **`CLAUDE_CODE_EFFORT_LEVEL`** | Env var: `low\|medium\|high` | Shell session |
| **`effortLevel` setting** | In settings.json: `low\|medium\|high` | Permanent |

**Cost tip**: For simple tasks, Alt+T to disable thinking → faster & cheaper.

**OpusPlan workflow**: `/model opusplan` → `Shift+Tab × 2` (plan with Opus) → `Shift+Tab` (execute with Sonnet)

**Required for**: features >3 files, architecture, complex debugging

### Quick Model Selection

| Task | Model | Effort |
|------|-------|--------|
| Rename, boilerplate, test gen | Haiku | low |
| Feature dev, debug, refactor | Sonnet | medium–high |
| Architecture, security audit | Opus | high–max |

> Full decision table with cost estimates: [Section 2.5 Model Selection & Thinking Guide](ultimate-guide.md#25-model-selection--thinking-guide)

### Dynamic Model Switching (Mid-Session)

**Pattern**: Start Sonnet (speed) → swap Opus (complexity) → back Sonnet

**Workflow**:
```bash
# Session start (default Sonnet)
claude

# Complex feature encountered
> "Implement OAuth2 flow with PKCE"
/model opus                    # Switch to deep reasoning

# Feature complete, back to routine
/model sonnet                  # Speed + cost optimization
```

**Best Practices**:
- ✅ Swap **on task boundaries**, not mid-task
- ✅ Use Opus for: architecture decisions, complex debugging, security-critical code
- ✅ Use Sonnet for: routine edits, refactoring, test writing
- ✅ Use Haiku for: simple fixes, typos, validation checks
- ❌ Don't swap mid-implementation (context loss)

**Cost Impact**:
| Model | Input | Output | Use Case |
|-------|--------|--------|----------|
| Opus  | $15/MTok | $75/MTok | Complex reasoning (10-20% of tasks) |
| Sonnet | $3/MTok | $15/MTok | Most development (70-80% of tasks) |
| Haiku | $0.25/MTok | $1.25/MTok | Simple validation (5-10% of tasks) |

**Dynamic switching** optimizes cost while maintaining quality on complex tasks.

**Source**: [Gur Sannikov embedded engineering workflow](https://www.linkedin.com/posts/gursannikov_claudecode-embeddedengineering-aiagents-activity-7423851983331328001-DrFb)

---

## MCP Servers

| Server | Purpose |
|--------|---------|
| **Serena** | Indexation + session memory + symbol search |
| **grepai** | Semantic search + call graph analysis |
| **Context7** | Library documentation |
| **Sequential** | Structured reasoning |
| **Playwright** | Browser automation |
| **Postgres** | Database queries |
| **doobidoo** | Semantic memory + multi-client + Knowledge Graph |

**Serena memory**: `write_memory()` / `read_memory()` / `list_memories()`

**Serena indexation**:
```bash
# Initial index
uvx --from git+https://github.com/oraios/serena serena project index

# Force rebuild
serena project index --force-full

# Incremental update (faster)
serena project index --incremental --parallel 4
```

Check status: `/mcp`

---

## Creating Custom Components

### Agent (`.claude/agents/my-agent.md`)
```yaml
---
name: my-agent
description: Use when [trigger]
model: sonnet
tools: Read, Write, Edit, Bash
---
# Instructions here
```

### Command (`.claude/commands/my-command.md`)
```markdown
# Command Name
Instructions for what to do...
$ARGUMENTS[0] $ARGUMENTS[1] (or $0 $1) - user args
```

### Hook (macOS/Linux: `.sh` | Windows: `.ps1`)

**Bash** (macOS/Linux):
```bash
#!/bin/bash
INPUT=$(cat)
# Process JSON input
exit 0  # 0=continue, 2=block
```

**PowerShell** (Windows):
```powershell
$input = [Console]::In.ReadToEnd() | ConvertFrom-Json
# Process JSON input
exit 0  # 0=continue, 2=block
```

---

## Anti-patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Vague prompts | Specify file + line with @references |
| Accept without reading | Read every diff |
| Ignore warnings | Use `/compact` at 70% |
| Skip permissions | Never in production |
| Negative constraints only | Provide alternatives |

---

## Quick Prompting Formula

```
WHAT: [Concrete deliverable]
WHERE: [File paths]
HOW: [Constraints, approach]
VERIFY: [Success criteria]
```

**Example:**
```
Add input validation to the login form.
WHERE: src/components/LoginForm.tsx
HOW: Use Zod schema, show inline errors
VERIFY: Empty email shows error, invalid format shows error
```

---

## CLI Flags Quick Reference

| Flag | Usage |
|------|-------|
| `-p "query"` | Non-interactive mode (CI/CD) |
| `-c` / `--continue` | Continue last session |
| `-r` / `--resume <id>` | Resume specific session |
| `--teleport` | Teleport session from web |
| `remote-control` | Subcommand: start remote control session |
| `--model sonnet` | Change model |
| `--add-dir ../lib` | Allow access outside CWD |
| `--permission-mode plan` | Plan mode |
| `--tools "Tool1,Tool2"` | Enable specific tools for session |
| `--max-budget-usd 5.00` | Max API spend limit (print mode) |
| `--system-prompt "..."` | Append custom system prompt |
| `--worktree` / `-w` | Run in isolated git worktree |
| `--dangerously-skip-permissions` | Auto-accept (use carefully) |
| `--debug` | Debug output |
| `--allowedTools "Edit,Read"` | Whitelist tools |

> Full CLI reference (~45 flags): see [cli-reference on code.claude.com](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

---

## Debug Commands

```bash
claude --version     # Version
claude update        # Check/install updates
claude doctor        # Diagnostic
claude --debug       # Verbose mode
claude --mcp-debug   # Debug MCPs
/mcp                 # MCP status (inside Claude)
```

---

## CI/CD Mode (Headless)

```bash
# Non-interactive execution
claude -p "analyze this file" src/api.ts

# JSON output
claude -p "review" --output-format json

# Economic model
claude -p "lint" --model haiku

# With auto-accept
claude -p "fix typos" --dangerously-skip-permissions
```

---

## Remote Control — Mobile Access (v2.1.51+, Research Preview)

> **Pro/Max only** — not available on Team, Enterprise, or API keys

```bash
# Start from terminal (new session)
claude remote-control

# Or from inside an active session:
/rc        # (or /remote-control)
```

**Connect from phone/tablet/browser:**
1. Scan the **QR code** (press spacebar after start)
2. Or open **session URL** in browser / Claude mobile app
3. Or: `/mobile` → shows App Store + Play Store links

| ⚠️ Known Limitation | Detail |
|--------------------|--------|
| 1 session at a time | Only one remote session active |
| Slash commands broken | `/new`, `/compact` = plain text remotely → use from local terminal |
| Terminal must stay open | Closing local terminal ends session |
| Network timeout | ~10 min disconnect → session expires |

**Advanced: tmux multi-session** (bypass 1-session limit)
```bash
tmux new-session -s dev
# Each pane = its own claude session
# Run /rc in the pane you want to control remotely
```

**Auto-enable:** `/config` → toggle "Remote Control: auto-enable"

**Full doc**: [§9.22 Remote Control](ultimate-guide.md#922-remote-control-mobile-access) | [Security notes](security-hardening.md#remote-control-security)

---

## Task Management (v2.1.16+)

**Two systems available:**

| System | When to Use | Persistence |
|--------|-------------|-------------|
| **Tasks API** (v2.1.16+) | Multi-session projects, dependencies | ✅ Disk (`~/.claude/tasks/`) |
| **TodoWrite** (Legacy) | Simple single-session | ❌ Session only |

### Tasks API Commands

```bash
# Enable persistence across sessions
export CLAUDE_CODE_TASK_LIST_ID="project-name"
claude

# Inside Claude: Create task hierarchy
> "Create tasks for auth system with dependencies"

# Resume later (new session)
export CLAUDE_CODE_TASK_LIST_ID="project-name"
claude
> "TaskList to see current state"
```

**Key capabilities:**
- 📁 **Persistent**: Survives session end, context compaction
- 🔗 **Dependencies**: Task A blocks Task B
- 🔄 **Multi-session**: Broadcast state to multiple terminals
- 📊 **Status**: pending → in_progress → completed/failed

**⚠️ Limitation**: TaskList shows `id`, `subject`, `status`, `blockedBy` only.
For `description`/`metadata` → use `TaskGet(taskId)` per task.

**Tip**: Store key info in `subject` for quick scanning.

**Migration flag** (v2.1.19+):
```bash
# Revert to old TodoWrite system
CLAUDE_CODE_ENABLE_TASKS=false claude
```

**→ Full workflow**: [guide/workflows/task-management.md](../workflows/task-management.md)

---

## The Golden Rules

1. **Always review diffs** before accepting
2. **Use `/compact`** before context gets critical (>70%)
3. **Be specific** in requests (WHAT, WHERE, HOW, VERIFY)
4. **Plan Mode first** for complex/risky tasks
5. **Create CLAUDE.md** for every project
6. **Commit frequently** after each completed task
7. **Know what's sent** — prompts, files, MCP results → Anthropic ([opt-out training](https://claude.ai/settings/data-privacy-controls))

---

## Quick Decision Tree

```
Simple task       → Just ask Claude
Complex task      → Tasks API to plan first
Risky change      → Plan Mode first
Repeating task    → Create agent or command
Context full      → /compact or /clear
Need docs         → Use Context7 MCP
Deep analysis     → Use Opus (thinking on by default)
```

---

## Common Issues Quick Fix

| Problem | Solution |
|---------|----------|
| "Command not found" | Check PATH, reinstall: `curl -fsSL https://claude.ai/install.sh \| sh` |
| Context too high (>70%) | `/compact` immediately |
| Slow responses | `/compact` or `/clear` |
| MCP not working | `claude mcp list`, check config |
| Permission denied | Check `settings.local.json` |
| Hook blocking | Check hook exit code, review logic |

**Health Check Script** (save & run):
```bash
# macOS/Linux
which claude && claude doctor && claude mcp list

# Windows PowerShell
where.exe claude; claude doctor; claude mcp list
```

---

## Cost Optimization

| Model | Use For | Cost |
|-------|---------|------|
| Haiku | Simple fixes, reviews | $ |
| Sonnet | Most development | $$ |
| Opus | Architecture, complex bugs | $$$ |
| OpusPlan | Plan (Opus) + Execute (Sonnet) | $$ |

**Tip**: Use `--add-dir` to allow tool access to directories outside your current working directory

---

## Community Tools

| Tool | Purpose | Install |
|------|---------|---------|
| **ccusage** | Cost tracking & reports | `bunx ccusage daily` |
| **RTK** | Token reduction (60-90%) | `brew install rtk-ai/tap/rtk` or `cargo install rtk` · [Site](https://www.rtk-ai.app/) |
| **claude-code-viewer** | Session history UI | `npx @kimuson/claude-code-viewer` |
| **Entire CLI** | Session checkpoints + governance | [entire.io](https://entire.io) (Feb 2026) |

> **Entire CLI**: Agent-native platform by ex-GitHub CEO with rewindable checkpoints, approval gates, audit trails. For compliance (SOC2, HIPAA) or multi-agent workflows.

---

## Search Tools Quick Reference

Quick decision (5 seconds): exact text → `rg` | exact name → `rg`/Serena | concept → grepai | structure → ast-grep

| Task | Tool | Command |
|------|------|---------|
| "Find TODO comments" | `rg` | `rg "TODO"` |
| "Find auth code" | `grepai` | `grepai search "authentication"` |
| "Who calls login?" | `grepai` | `grepai trace callers "login"` |
| "Get file structure" | `Serena` | `serena get_symbols_overview` |
| "Async without try/catch" | `ast-grep` | `ast-grep "async function $F"` |

Speed: `rg` (~20ms) → Serena (~100ms) → ast-grep (~200ms) → grepai (~500ms)

> Full workflows: [workflows/search-tools-mastery.md](./workflows/search-tools-mastery.md)

---

## Resources

- **Official docs**: [docs.anthropic.com/claude-code](https://docs.anthropic.com/en/docs/claude-code)
- **Advanced guide**: [Claudelog.com](https://claudelog.com/) - Tips & patterns
- **Full guide**: `ultimate-guide.md` (this repo)
- **Whitepapers (FR + EN)**: [florian.bruniaux.com/guides](https://www.florian.bruniaux.com/guides) — 9 focused PDFs
- **Project memory**: Create `CLAUDE.md` at project root
- **DeepSeek (cost-effective)**: Configure via `ANTHROPIC_BASE_URL`

---

**Author**: Florian BRUNIAUX | [@Méthode Aristote](https://methode-aristote.fr) | Written with Claude

*Last updated: March 2026 | Version 3.37.0*
