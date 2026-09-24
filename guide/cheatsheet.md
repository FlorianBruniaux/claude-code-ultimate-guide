---
title: "Claude Code Cheatsheet"
description: "One-page printable daily essentials for maximum Claude Code productivity"
tags: [cheatsheet, reference]
---

# Claude Code Cheatsheet

**Daily reference**. For compact printable editions, use the [English and French cheatsheets](../whitepapers/README.md).

**Author**: Florian BRUNIAUX | Founding Engineer [@Méthode Aristote](https://methode-aristote.fr)

**Written with**: Claude (Anthropic)

**Version**: 3.43.0 | **Last Updated**: Sep 24, 2026

---

## Essential Commands

These are selected daily commands. Availability depends on your version, provider, and plan: the complete list is in [§10.1 of the guide](./ultimate-guide.md#101-commands-table), and the always-current official reference is [code.claude.com/docs/en/commands](https://code.claude.com/docs/en/commands).

| Command | Action |
|---------|--------|
| `/help` | Contextual help |
| `/powerup` | Interactive animated lessons teaching Claude Code features |
| `/clear` | Reset conversation |
| `/compact` | Free up context |
| `/status` | Session state + context usage |
| `/context` | Detailed token breakdown |
| `/plan` | Enter Plan Mode (no changes). Exit by approving the plan or `Shift+Tab` |
| `/model` | Select model and save the default; press `s` in the picker for this session only |
| `/autocompact [auto\|500k]` | Choose the auto-compaction window or restore the model default |
| `/output-style [style]` | Select Default, Proactive, Concise, Explanatory, Learning, or a custom style |
| `/insights` | Usage analytics + optimization report |
| `/code-review [level]` | Review the diff for correctness bugs, `--fix` applies them, `ultra` runs it in the cloud |
| `/simplify` | Cleanup-only review of changed code: reuse, simplification, efficiency (applies cleanup fixes; use `/code-review` for correctness bugs) |
| `/security-review` | Scan the branch diff for injection, auth, and data-exposure risks |
| `/batch` | Large-scale refactors via 5–30 parallel worktree agents |
| `/subtask <task>` | Hand a side task to a forked subagent that reports back here (v2.1.212+) |
| `/teleport` | Teleport session from web |
| `/tasks` | Monitor background tasks |
| `/remote-env` | Configure cloud environment |
| `/remote-control` (`/rc`) | Connect this local session to web/mobile; Team/Enterprise require owner enablement |
| `/mobile` | Get Claude mobile app download links |
| `/fast` | Toggle faster Opus output; Opus 5.5 costs $8/$40 per MTok in fast mode |
| `/voice` | Toggle voice input (hold Space to speak, release to send) |
| `/recap` | Session context summary on return to a break (v2.1.108) |
| `/effort [level]` | Thinking depth: low/medium/high/xhigh/max/ultracode; no arg = interactive slider (v2.1.111) |
| `/tui [fullscreen]` | Full-screen flicker-free TUI rendering (v2.1.110) |
| `/focus` | Toggle minimal focus view, separate from Ctrl+O (v2.1.110) |
| `/fewer-permission-prompts` | Scan transcripts and propose a read-only tool allowlist (shipped as `/less-permission-prompts` in v2.1.111) |
| `/btw [question]` | Side question overlay: read-only ephemeral agent, no history pollution, no tools |
| `/loop [interval] [prompt]` | Repeat on a fixed interval, or let Claude choose the interval when omitted; recurring tasks expire after 7 days (see scheduling reference) |
| `/usage` (`/cost`, `/stats`) | Token + cost usage per model, plan limits, activity graph (merged in v2.1.118) |
| `/ultrareview` | Multi-agent cloud code review, now an alias of `/code-review ultra` (v2.1.114) |
| `/goal [condition]` | Autonomous multi-turn mode: Claude works until condition is met, live overlay shows elapsed/turns/tokens (v2.1.139) |
| `/scroll-speed` | Tune mouse wheel scroll speed with interactive live-preview slider (v2.1.139) |
| `/rename [name]` | Name or rename the current session |
| `/copy` | Interactive picker to copy a code block or full response |
| `/doctor` | Full setup checkup: install, settings, hooks, `CLAUDE.md` bloat, unused skills (v2.1.205+) |
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
| `Ctrl+X Ctrl+K` | Stop running background subagents |
| `Ctrl+Enter` / `Ctrl+X Ctrl+S` | Send queued messages now, interrupting the current turn |
| `Option+T` / `Alt+T` | Toggle thinking where supported; no effect on Opus 5.5 or Fable |
| `Space` (hold) | Voice input (requires `/voice` enabled) |
| `Ctrl+D` | Exit |

---

## File References

```
@path/to/file.ts    → Reference a file
@agent-name         → Call an agent
@session-name       → Message another live Claude session (v2.1.232+)
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
| **Tasks API** | v2.1.16 | Persistent task lists with dependencies; opt in on newer models with `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` |
| **Background Agents** | v2.0.60 | Sub-agents work while you code. Since v2.1.232 forking is the default: a `subagent_type: "fork"` agent inherits the full conversation and prompt cache, and non-teammate spawns go background on their own |
| **Agent Teams** | v2.1.32 | Multi-agent coordination (TeamCreate/SendMessage) |
| **Cross-Session Messaging** | v2.1.224 | Sessions message each other across all your machines. `ListAgents` to discover, `SendMessage` to talk, `@name` to mention (v2.1.232). macOS, Linux, Windows (v2.1.234+). [Full guide →](./workflows/cross-session-messaging.md) |
| **Self-Hosted Environments** | v2.1.224 | `claude self-hosted-runner` makes your own machine or container the place web, mobile, and desktop sessions execute. Team and Enterprise |
| **Auto-Memories** | v2.1.32 | Automatic cross-session context capture |
| **Session Forking** | v2.1.19 | Rewind + create parallel timeline |
| **LSP Tool** | v2.0.74 | IDE-like navigation: symbols, types, refs. ~50ms vs 45s with grep. 11 languages |
| **Voice Mode** | v2.1.x | Native voice input, free transcription, no rate limit impact |
| **Remote Control** | v2.1.51 | Control a local session from phone/browser; subscription required, with owner enablement on Team/Enterprise |
| **`/loop`** | v2.1.71 | Session-scoped recurring scheduler: `/loop 5m check the deploy` (stops when session ends). Min 1 min, max 50 tasks/session |
| **`/goal`** | v2.1.139 | Autonomous completion loop: set a condition, Claude works across turns until a separate evaluator (Haiku by default on the Claude API) judges the surfaced evidence. Live overlay shows elapsed time, turns, and tokens. Three-element formula: measurable end state + verification mechanism + constraints. |
| **Cloud Scheduled Tasks** | 2026 | Machine-off scheduling via `/schedule` or `claude.ai/code/scheduled`. Runs on Anthropic infra, clones repo fresh each run, min 1h interval. Pro/Max/Team/Enterprise |
| **Desktop Scheduled Tasks** | 2026 | Local machine scheduling via Desktop app. Min 1 min, full local file access, no session required |
| **Skill Evals** | Mar 2026 | Two skill types: Capability Uplift (fills model gap, fades) / Encoded Preference (encodes workflow, stays). Benchmark Mode, A/B testing, Trigger Tuning. |
| **Output Styles** | v2.1.269 command | `/output-style` selects Default, Proactive, Concise, Explanatory, Learning, or a custom style. Coding-oriented custom styles need `keep-coding-instructions: true`. |

**Activate LSP**: Add to `~/.claude/settings.json` → `{ "env": { "ENABLE_LSP_TOOL": "1" } }` (requires LSP server installed for your language: `tsserver`, `pylsp`, `gopls`, `rust-analyzer`, `sourcekit-lsp`...)

**Pro tip**: These are public, documented in the [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md). Read it!

---

## Permission Modes

| Mode | Editing | Execution |
|------|---------|-----------|
| Manual (`default`) | Permission rules apply | Permission rules apply |
| acceptEdits | Auto | Asks |
| Plan Mode | No file changes | Read-only exploration tools allowed |
| auto | Classifier decides | Classifier decides |
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
├── hooks/              # Event scripts
├── rules/              # Auto-loaded rules
└── skills/             # Slash commands + knowledge modules (unified)
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
| **Master Loop** | Model/tool loop; permissions and auto-mode review are separate controls |
| **Tools** | Bash, Read, Edit, Write, Grep, Glob, Agent and more ([tool reference](./core/tools-reference.md)) |
| **Context** | Model-dependent: native 1M on current Opus, Sonnet and Fable; 200K on Haiku 4.5. Inspect `/context` |
| **Sub-agents** | Isolated context, max depth=1 |
| **Philosophy** | "Less scaffolding, more model" (trust Claude's reasoning) |

**Deep dive**: [Architecture & Internals](./core/architecture.md)

---

## Harness Choice in Four Layers

| Layer | Owns | Start here |
|-------|------|------------|
| Model | Reasoning and tool-call proposals | [Glossary](https://cc.bruniaux.com/guide/glossary/) |
| Runtime harness | Tool loop, permissions, and recovery | [Agent Harness Engineering](https://cc.bruniaux.com/guide/agent-harness/) |
| Repository harness | Instructions, task state, and verification | [Repository Harness Engineering](https://cc.bruniaux.com/guide/ultimate-guide/09-advanced-patterns/#925-harness-engineering) |
| Orchestrator | Coordination between runtimes or sessions | [Agent Tools](https://cc.bruniaux.com/guide/agentic-tools/) |

Choose the smallest control structure that safely solves the need: a bounded loop for one repeated task; an explicit graph for routing, joins, parallelism, interruption, or durable recovery; a repository harness for repeatable project behavior; and an orchestrator for several runs or queues. Specify success, failure, timeout, budget, and escalation before execution. See [Loop & Graph Engineering](https://cc.bruniaux.com/guide/loop-graph-engineering/) and compare products in the [Agent Harness Map](https://cc.bruniaux.com/guide/agent-harness-landscape/).

Evaluate the exact model-harness pair for a bounded coding task. Introduce orchestration only when coordination is the constraint. A harness optimizer sits outside the four operating layers and changes candidate harnesses under a separate evaluation protocol.

---

## Plan Mode & Thinking

| Feature | Activation | Usage |
|---------|------------|-------|
| **Plan Mode** | `Shift+Tab × 2` or `/plan` | Explore without modifying |
| **OpusPlan** | `/model opusplan` | Opus for planning, Sonnet for execution |

> **Verified September 24, 2026**: Opus 5.5 defaults to `medium`; Sonnet 5 and Fable 5.1 default to `high`. Haiku 4.5 has no effort parameter. `ultrathink` adds a reasoning instruction for the turn without changing API effort.

| Control | Action | Persistence |
|---------|--------|-------------|
| **Option+T / Alt+T** | Toggle thinking on supported models; Opus 5.5 and Fable always think | Session |
| **`/effort` or `/model` slider** | Choose a supported level; `Enter` saves per model, `s` applies once | Per model or session |
| **`/effort max`** | Highest supported effort | Session |
| **`CLAUDE_CODE_EFFORT_LEVEL`** | Override effort in the launching environment | Process environment |
| **`modelSettings` / `effortLevel`** | Persist `low`, `medium`, `high`, or `xhigh`; not `max` | Settings |
| **`effort` in skill frontmatter** | Override effort while the skill runs | Invocation |

**Cost tip**: try a lower supported effort for bounded tasks, then verify the result. On Opus 5.5, changing effort is the control; disabling thinking has no effect.

**Per-skill effort**: add `effort: low` to mechanical skills (commit, sync, scaffold) and `effort: high` to analytical ones (security-audit, architecture-review). Overrides session setting automatically.

**OpusPlan workflow**: `/model opusplan` → `Shift+Tab × 2` (plan with Opus) → `Shift+Tab` (execute with Sonnet)

**Required for**: features >3 files, architecture, complex debugging

### Quick Model Selection

| Task | Model | Effort |
|------|-------|--------|
| Rename, boilerplate, test gen | Haiku 4.5 | Not supported |
| Feature dev, debug, refactor | Sonnet 5 or Opus 5.5 | Start at the model default |
| Architecture, security audit | Opus 5.5; evaluate Fable 5.1 if needed | Increase with evidence |

> Full decision table and pricing boundaries: [Section 2.5 Model Selection & Thinking Guide](ultimate-guide.md#25-model-selection--thinking-guide)

### Dynamic Model Switching (Mid-Session)

**Pattern**: Start Sonnet (speed) → swap Opus (complexity) → back Sonnet

**Workflow**:
```bash
# Select Sonnet explicitly for this session
claude --model sonnet

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
- Model switches keep conversation history but can invalidate prompt caches; switch at a useful task boundary.

**Standard Anthropic API rates**, USD per million tokens, checked September 24, 2026:

| Model | Input | Output | Context |
|-------|-------|--------|---------|
| Opus 5.5 | $4 | $20 | 1M |
| Sonnet 5 | $2 | $10 | 1M |
| Haiku 4.5 | $1 | $5 | 200K |
| Fable 5.1 | $10 | $50 | 1M |

Opus 5.5 fast mode costs $8/$40. Subscription allowances, usage credits, cache tokens, and cloud-provider pricing are separate. [Official pricing](https://platform.claude.com/docs/en/about-claude/pricing).

On the direct Anthropic service, the account default and `opus` select Opus 5.5; `sonnet` selects Sonnet 5. Provider aliases differ: check the [provider table](ultimate-guide.md#model-aliases). `fable` normally selects Fable 5.1, while Claude apps gateway sessions resolve it to Fable 5.

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

### Skill: user-invocable (`.claude/skills/my-command/SKILL.md`)
```markdown
---
description: Brief description
argument-hint: "<required_arg> [--flag]"
disable-model-invocation: true
---
# Command Name
Instructions for what to do...
$ARGUMENTS[0] $ARGUMENTS[1] (or $0 $1) - user args
```

### Dynamic Workflow (`.claude/workflows/name.js`)

```js
export const meta = {
  name: 'my-workflow',
  description: 'What this orchestrates',
  phases: [{ title: 'Analyze' }, { title: 'Verify' }],
};
// meta must be the first statement, a pure literal (no variables/spreads)

export default async function ({ agent, parallel, pipeline, phase, log, args, budget }) {
  phase('Analyze');
  const results = await parallel(
    ITEMS.map((item) => () => agent(`Analyze ${item}.`, { schema: MY_SCHEMA }))
  );
  return results.filter(Boolean);
}
```

Trigger: type `ultracode` in the prompt (or ask in your own words). Monitor: `/workflows`.

| Primitive | Behavior |
|-----------|----------|
| `agent(prompt, { schema })` | Spawn one subagent; returns text or validated JSON |
| `parallel([() => agent(...)])` | Barrier: all run concurrently, return when slowest finishes |
| `pipeline(items, stage1, stage2)` | No barrier: items flow through stages independently |
| `phase(title)` | Update progress label in `/workflows` UI |
| `log(msg)` | Emit progress message |
| `budget.remaining()` | Guard open-ended loops (budget hits 1000-agent cap otherwise) |

Key rules: orchestrator consumes 0 tokens; `Date.now()`/`Math.random()` unavailable (breaks resume); filter `parallel()` results with `.filter(Boolean)`.

Full reference: [Dynamic Workflows](./workflows/dynamic-workflows.md)

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
| `--system-prompt "..."` | Replace the entire default system prompt |
| `--append-system-prompt "..."` | Append text to the default system prompt |
| `--worktree` / `-w` | Run in isolated git worktree |
| `--dangerously-skip-permissions` | Auto-accept (use carefully) |
| `--debug` | Debug output |
| `--allowedTools "Edit,Read"` | Allow these tools without prompting; use `--tools` to restrict availability |
| `--effort medium` | Choose session effort on a supported model |
| `--system-prompt-file ./prompt.txt` | Replace the prompt from a file |
| `--append-system-prompt-file ./rules.txt` | Append prompt text from a file |

> Use the [official CLI reference](https://code.claude.com/docs/en/cli-reference) for the full flag list. Self-hosted runners and command hooks must use the file-based system-prompt flags.

## Key CLI Subcommands

| Command | Description |
|---------|-------------|
| `claude project purge [path]` | Delete all Claude Code state for a project (transcripts, tasks, config). `--dry-run` for preview. (v2.1.126) |
| `claude ultrareview [target]` | Non-interactive cloud code review for CI. `--json` output. Exits 0/1. (v2.1.120) |
| `claude plugin prune` | Remove orphaned auto-installed plugin deps. (v2.1.121) |
| `claude plugin details <name>` | Show plugin inventory and token cost estimate. (v2.1.139) |
| `claude --plugin-url <url>` | Load plugin `.zip` from URL for this session. (v2.1.129) |
| `claude self-hosted-runner` | Run web/mobile/desktop sessions on your own machine or container. Windows needs an explicit `--base-dir`. Team and Enterprise. (v2.1.224) |

---

## Debug Commands

```bash
claude --version     # Version
claude update        # Check/install updates
claude doctor        # Diagnostic
claude --debug       # Verbose mode
claude --debug='mcp' # Debug MCP connections
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

## Remote Control: Mobile Access

Available with Pro, Max, Team, and Enterprise subscriptions. Team and Enterprise owners must enable it first. API keys and third-party provider connections are not supported.

```bash
# Start a server in the project directory
claude remote-control

# Or connect an existing session
/remote-control
```

Open the displayed URL or scan the QR code from a browser or the Claude mobile app. The local process must keep running; the files and tools stay on your machine. Server mode can run multiple sessions with `--spawn worktree` and `--capacity`; `/remote-control` connects the current session. Available commands vary by client, so check the [current limitations](https://code.claude.com/docs/en/remote-control#limitations).

**Full doc**: [Remote Control](ultimate-guide.md#922-remote-control-mobile-access) | [Security notes](security/security-hardening.md#remote-control-security)

---

## Task Management (v2.1.16+)

**Availability**: newer models, including Opus 5.5, Sonnet 5, and Fable, do not receive task-tracking tools by default. Start with `CLAUDE_CODE_ENABLE_TODO_TOOLS=1 claude` to opt in. `CLAUDE_CODE_ENABLE_TASKS=0` selects legacy TodoWrite only where task tools are enabled. [Official tool availability](https://code.claude.com/docs/en/tools-reference#task-tool-availability).

**Two systems available:**

| System | When to Use | Persistence |
|--------|-------------|-------------|
| **Tasks API** (v2.1.16+) | Multi-session projects, dependencies | ✅ Disk (`~/.claude/tasks/`) |
| **TodoWrite** (Legacy) | Simple single-session | ❌ Session only |

### Tasks API Commands

```bash
# Enable persistence across sessions
export CLAUDE_CODE_TASK_LIST_ID="project-name"
CLAUDE_CODE_ENABLE_TODO_TOOLS=1 claude

# Inside Claude: Create task hierarchy
> "Create tasks for auth system with dependencies"

# Resume later (new session)
export CLAUDE_CODE_TASK_LIST_ID="project-name"
CLAUDE_CODE_ENABLE_TODO_TOOLS=1 claude
> "TaskList to see current state"
```

**Key capabilities:**
- 📁 **Persistent**: Survives session end, context compaction
- 🔗 **Dependencies**: Task A blocks Task B
- 🔄 **Multi-session**: Broadcast state to multiple terminals
- 📊 **Status**: pending → in_progress → completed

**⚠️ Limitation**: TaskList shows `id`, `subject`, `status`, `blockedBy` only.
For `description`/`metadata` → use `TaskGet(taskId)` per task.

**Tip**: Store key info in `subject` for quick scanning.

**Migration flag** (v2.1.19+):
```bash
# Revert to old TodoWrite system
CLAUDE_CODE_ENABLE_TODO_TOOLS=1 CLAUDE_CODE_ENABLE_TASKS=0 claude
```

**→ Full workflow**: [guide/workflows/task-management.md](workflows/task-management.md)

---

## The Golden Rules

1. **Always review diffs** before accepting
2. **Use `/compact`** before context gets critical (>70%)
3. **Be specific** in requests (WHAT, WHERE, HOW, VERIFY)
4. **Plan Mode first** for complex/risky tasks
5. **Create CLAUDE.md** for every project
6. **Commit frequently** after each completed task
7. **Know what's sent**: prompts, files, MCP results → Anthropic ([opt-out training](https://claude.ai/settings/data-privacy-controls))

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
- **Whitepapers (FR + EN)**: [cc.bruniaux.com/whitepapers](https://cc.bruniaux.com/whitepapers/), 13 focused PDFs
- **Project memory**: Create `CLAUDE.md` at project root
- **DeepSeek (cost-effective)**: Configure via `ANTHROPIC_BASE_URL`

---

**Author**: Florian BRUNIAUX | [@Méthode Aristote](https://methode-aristote.fr) | Written with Claude

*Last updated: Sep 24, 2026 | Version 3.43.0*
