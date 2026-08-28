---
title: "Glossary"
description: "Definitions for Claude Code terminology"
---

# Glossary

Definitions for terms used throughout this guide. For model-level concepts (tokens, temperature, RAG), see the [Anthropic platform glossary](https://platform.claude.com/docs/en/about-claude/glossary).

---

## A

### Agent teams

Multiple independent Claude Code sessions coordinated by a team lead, with a shared task list and peer-to-peer messaging. Unlike subagents, which run within a single session, teammates each have their own context window and you can interact with any of them directly. This is an experimental feature; it requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` to enable. See [§4 Agents](../ultimate-guide.md#4-agents).

### Agentic loop

The cycle Claude works through for every task: gather context, take action, verify results, repeat until done. Each tool use returns information that informs the next step. Most extension points (hooks, skills, MCP) plug into specific phases of this loop. See [§1 How Claude Code Works](../ultimate-guide.md#1-how-claude-code-works).

### Agent-computer interface

The commands, observations, feedback format, and interaction rules through which a model acts on a computer. A better interface can improve an agent without changing the model. [SWE-agent](https://arxiv.org/abs/2405.15793) uses this term for its repository-oriented command and feedback design. The interface is one component of a runtime harness, not only its visual UI.

### Auto memory

Notes Claude writes for itself based on your corrections and preferences, stored per git repository under `~/.claude/projects/`. The first 200 lines or 25 KB of `MEMORY.md` loads at session start. All worktrees of the same repository share one auto memory directory. See [§3 Memory](../ultimate-guide.md#3-configuration--memory).

### Auto mode

A permission mode where a separate classifier model reviews each action in the background instead of showing you approval prompts. The classifier blocks scope escalation, untrusted infrastructure, and prompt injection attempts. It never sees tool results, making it immune to injected instructions. This is a research preview. See [§3 Permission Modes](../ultimate-guide.md#3-configuration--memory).

---

## B

### Bare mode

A startup flag (`--bare`) that skips auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md. Only flags you pass explicitly take effect. Recommended for CI and scripted calls where you need identical behavior across machines. Available since v2.1.81. See [§9 Headless/Non-interactive Mode](../ultimate-guide.md#9-advanced-features).

### Bundled skills

Prompt-based playbooks included with Claude Code, such as `/batch`, `/code-review`, `/debug`, and `/loop`. Unlike built-in commands (which execute fixed logic), bundled skills give Claude a detailed prompt and let it orchestrate the work. They can spawn agents, read files, and adapt to your codebase. See [§5 Skills](../ultimate-guide.md#5-skills).

---

## C

### Channel

An MCP server that pushes events into your running session so Claude can react to things that happen while you're away from the terminal. Channels can be two-way: Claude reads an inbound event and replies back through the same channel. Telegram, Discord, and iMessage are included in the research preview. See [§8 MCP](../ultimate-guide.md#8-mcp).

### Checkpoint

A restore point created at each prompt you send. Claude Code snapshots files before every edit, so you can revert code, conversation, or both to an earlier state. Press `Esc` twice or run `/rewind` to restore. Checkpoints are local to the session, separate from git, and do not track changes made through the Bash tool. See [§9 Checkpointing](../ultimate-guide.md#9-advanced-features).

### `.claude` directory

The directory where Claude Code reads project-scoped configuration: settings, hooks, skills, subagents, rules, and auto memory. A project has `.claude/` at its root; your user-level defaults live at `~/.claude/`. See [§3 Configuration](../ultimate-guide.md#3-configuration--memory).

### CLAUDE.md

A markdown file of persistent instructions you write for Claude, loaded at the start of every session as a user message after the system prompt. Put project conventions, architecture notes, and behavioral rules here. CLAUDE.md survives compaction and is re-read fresh from disk afterward. See [§3.1 Memory Files](../ultimate-guide.md#31-memory-files-claudemd).

### Compaction

Automatic summarization of your conversation when the context window approaches its limit. Older tool outputs clear first, then the conversation is summarized. CLAUDE.md and auto memory survive compaction and reload from disk; instructions given only in conversation may be lost. Run `/compact` to trigger manually. See [§2 Context Window](../ultimate-guide.md#2-core-concepts).

---

## D

### Dispatch

A phone-initiated task router that spawns a Claude Code session in the Desktop app when you send a coding task from the Claude mobile app. Your prompt routes to the right tool automatically. Available on Pro and Max plans. See [§9 Desktop Features](../ultimate-guide.md#9-advanced-features).

---

## E

### Effort level

A setting that controls how much of the adaptive-reasoning thinking budget Claude uses per turn. Higher effort means more thinking tokens and deeper reasoning; lower effort is faster and cheaper. Supported on Opus 4.6+ and Sonnet 4.6+. Skills can override the session effort level in their frontmatter. See [§2.5 Model Selection](../ultimate-guide.md#25-model-selection--thinking-guide).

### Extended thinking

Visible step-by-step reasoning the model performs before responding. You can cap thinking tokens with `MAX_THINKING_TOKENS` or adjust the effort level. Thinking appears in gray italic text in the terminal. See [§2.5 Model Selection](../ultimate-guide.md#25-model-selection--thinking-guide).

---

## H

### Agent harness

The runtime around a model that executes an agent loop: it assembles context, exposes tools, applies permissions, preserves or restores state, and feeds tool results back to the model. Claude Code is a runtime harness; Claude is the model it runs. Do not confuse it with the repository harness, which is the project-specific layer of instructions, setup, state, and verification gates. See [Agent Harness Engineering](./agent-harness.md), the [Agent Harness Landscape](../ecosystem/agent-harness-landscape.md), and [§9.25 Repository Harness Engineering](../ultimate-guide.md#925-harness-engineering).

### Evaluation harness

A repeatable setup that runs an agent or model against defined tasks and records outcomes, costs, traces, or scores. An evaluation harness measures a system; it does not need to own the system's interactive tool loop or act on a repository. SWE-bench tooling is an evaluation harness, while SWE-agent is a coding runtime that can be evaluated with one. See [Agent Evaluation](../roles/agent-evaluation.md).

### Harness-model pair

The exact combination of model, runtime harness, configuration, tool set, repository environment, and budget used for a run. Evaluate this pair as one unit: changing the harness can change accuracy, cost, and failure modes even when the model stays fixed. [The Scaffold Effect](https://arxiv.org/abs/2607.22585) provides controlled evidence for this effect across two models and three coding harnesses. See [Agent Harness Engineering](./agent-harness.md#the-core-claim) and the [Agent Harness Landscape](../ecosystem/agent-harness-landscape.md).

### Harness optimizer

An outer-loop system that proposes changes to a target harness, evaluates candidate versions, and retains or rejects those changes against defined metrics. Its search target may include prompts, context rules, tools, control flow, verification, or memory policy. A harness optimizer does not replace the runtime loop it evaluates. See [Harness Optimizers and Meta-Harnesses](./agent-harness.md#11-harness-optimizers-and-meta-harnesses).

### Hook

A user-defined handler that executes automatically at a specific point in Claude Code's lifecycle, such as before a tool runs, after a file edit, or at session start. A hook configuration has three levels: the hook event (which lifecycle point), the matcher (which events fire it), and the hook handler (what runs). Handlers can be a shell command, HTTP endpoint, MCP tool, LLM prompt, or subagent. Hooks are deterministic: they fire at fixed lifecycle points, not at the model's discretion. See [§7 Hooks](../ultimate-guide.md#7-hooks).

---

## M

### Managed settings

A settings file enforced org-wide by IT or DevOps, placed at an OS-level path outside `~/.claude`. Users cannot override or exclude managed settings. Use this for security policies, compliance requirements, or standardized tooling across a fleet. See [§3.3 Settings](../ultimate-guide.md#33-settings--permissions).

### Meta-harness

A system around one or more target harnesses that can generate or modify candidate harnesses, run evaluations, and use the results to guide another optimization step. This is an outer optimization loop, distinct from a runtime harness that owns one task loop and from an orchestrator that coordinates runs. [Meta-Harness](https://arxiv.org/abs/2603.28052) and [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850) are current research examples; both are preprints and need independent replication.

### MCP (Model Context Protocol)

An open standard for connecting AI tools to external data sources and services. MCP servers give Claude new tools for Slack, Jira, databases, browsers, and hundreds of other integrations. Connect servers via `/mcp` or by adding them to `.mcp.json`. See [§8 MCP](../ultimate-guide.md#8-mcp).

### MCP Tool Search

A context-saving mechanism that defers MCP tool schemas until needed. Only tool names load at startup; Claude fetches the full schema on demand when it decides to use a specific tool. This keeps idle MCP servers from consuming context. See [§8 MCP](../ultimate-guide.md#8-mcp).

---

## N

### Non-interactive mode

A mode that executes a single prompt and exits without a conversational session, invoked with `-p` or `--print`. Used for CI, scripts, and piping. The `--bare` flag extends this for clean-slate automation. Formerly called "headless mode." See [§9 Non-interactive Mode](../ultimate-guide.md#9-advanced-features).

---

## O

### Orchestrator

A system that coordinates runs, workspaces, queues, budgets, handoffs, or human approvals across one or more agents. An orchestrator may call a separate runtime harness without owning the model-tool-observation loop itself. See [Orchestrators: Products Above the Runtime](../ecosystem/agent-harness-landscape.md#orchestrators-products-above-the-runtime).

### Output style

A configuration that modifies Claude's system prompt to change response behavior, tone, or format. Output styles turn off the software-engineering-specific parts of the default system prompt, unlike CLAUDE.md (which is delivered as a user message). Built-in styles include Default, Proactive, Explanatory, and Learning. See [§3 Configuration](../ultimate-guide.md#3-configuration--memory).

---

## P

### Permission mode

The baseline approval behavior for the session. Available modes are `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, and `bypassPermissions`. Cycle with `Shift+Tab` in the CLI or use the mode selector in VS Code, Desktop, and claude.ai. See [§3.3 Settings](../ultimate-guide.md#33-settings--permissions).

### Permission rule

A settings entry that allows, asks about, or denies a tool invocation based on the tool name and argument pattern. Rules evaluate in deny-then-ask-then-allow order, so the first match wins. Permission rules are fine-grained controls layered on top of the broader permission mode. See [§3.3 Settings](../ultimate-guide.md#33-settings--permissions).

### Plan mode

A permission mode where Claude researches and proposes changes without editing your source files. It can read, search, and run exploration commands, then presents a plan for approval before touching anything. Enter plan mode with `/plan` or by pressing `Shift+Tab`. See [§3.3 Settings](../ultimate-guide.md#33-settings--permissions).

### Plugin

A bundle of skills, hooks, subagents, and MCP servers packaged as a single installable unit. Plugin skills are namespaced as `plugin-name:skill-name` so multiple plugins coexist without conflicts. Distribute plugins across teams via a marketplace. See [§5 Skills](../ultimate-guide.md#5-skills).

### Project trust

A dialog that accepts a directory before Claude Code loads its configuration. Acceptance is saved per project directory, except your home directory (where trust is per-session only). Trust gates auto-installation of marketplace plugins and execution of project-defined hooks. See [§3 Configuration](../ultimate-guide.md#3-configuration--memory).

### Prompt injection

Hostile instructions embedded in a file, web page, or tool result that attempt to redirect Claude toward actions you never requested. Claude Code's defenses include the permission system, command blocklists, and trust verification. Auto mode adds a server-side classifier that never sees tool results, so injected text cannot influence its approval decisions. See [§10 Security](../ultimate-guide.md#10-security).

---

## R

### Repository harness

The project-specific layer that makes an agent run repeatably inside a repository: instructions, environment setup, durable state, test commands, verification gates, and recovery conventions. It grounds and checks a runtime harness but does not replace the runtime's model-tool loop. See [§9.25 Repository Harness Engineering](../ultimate-guide.md#925-harness-engineering) and [Four Layers, Four Responsibilities](./agent-harness.md#0-four-layers-four-responsibilities).

### Remote Control

A way to continue a local Claude Code session from your phone or browser via claude.ai. Your code stays on your machine; only the UI is remote. Different from Claude Code on the web, which runs in a cloud sandbox. See [§9.22 Remote Control](../ultimate-guide.md#922-remote-control-mobile-access).

### Rules

Modular instruction files in `.claude/rules/` that load alongside CLAUDE.md. A rule can be path-scoped with YAML `paths:` frontmatter so it only loads when Claude reads a matching file, keeping context lean until relevant. See [§3.1 Memory Files](../ultimate-guide.md#31-memory-files-claudemd).

---

## S

### Sandboxing

OS-level filesystem and network isolation for the Bash tool. Commands run inside a boundary you define upfront, so Claude can work freely within it without per-command approval prompts. Sandboxing is a separate layer from permission rules. See [§10 Security](../ultimate-guide.md#10-security).

### Scaffold effect

The variation in outcome, token use, and failure mode caused by the surrounding agent scaffold or harness while the model is held fixed. In one controlled coding study, harness choice changed token use per solved task by up to 40 times while pass-rate differences stayed between 0 and 8 percentage points and were mostly not statistically significant. Treat this as evidence from a bounded experiment, not a universal ranking. See [The Scaffold Effect](https://arxiv.org/abs/2607.22585).

### Session

A conversation tied to your current directory, with its own independent context window. Sessions can be resumed with `claude -c`, forked with `--fork-session`, or run in parallel across terminals. Each session's transcript is stored under `~/.claude/projects/`. See [§1 How Claude Code Works](../ultimate-guide.md#1-how-claude-code-works).

### Settings layers

The hierarchy Claude Code reads configuration from, in precedence order from highest to lowest: managed policy, command-line arguments, local settings at `.claude/settings.local.json`, project settings at `.claude/settings.json`, then user settings at `~/.claude/settings.json`. Arrays merge across layers; scalars at a higher layer override lower ones. See [§3.3 Settings](../ultimate-guide.md#33-settings--permissions).

### Skill

A `SKILL.md` file containing instructions, knowledge, or a workflow that Claude adds to its toolkit. Invoke directly with `/skill-name`. Skills follow the Agent Skills open standard; Claude Code extends it with invocation control and subagent execution. Skills are the recommended successor to custom commands: `.claude/commands/` files continue to work, but `.claude/skills/` is the preferred location. See [§5 Skills](../ultimate-guide.md#5-skills).

### Subagent

A specialized AI assistant that runs in its own context window with a custom system prompt, specific tool access, and independent permissions. It works on a delegated task and returns a summary to the main conversation. Unlike agent teams (where each agent is a full independent session), subagents run within and report to the parent session. See [§4 Agents](../ultimate-guide.md#4-agents).

### Surface

Any place you access Claude Code: the CLI, VS Code, JetBrains, Desktop, or claude.ai. All surfaces share the same engine, so your CLAUDE.md, settings, and skills work identically across them. Slack and the Chrome extension are integrations that connect to a surface rather than surfaces themselves.

---

## T

### Teleport

A command (`/teleport`) that pulls a cloud Claude Code session into your local terminal. Claude fetches the branch, loads the conversation history, and resumes from the web session's last state. The reverse direction is `--remote`, which sends a local task to run on the web. See [§9.16 Session Teleportation](../ultimate-guide.md#916-session-teleportation).

### Tool

An action Claude can take: read a file, edit code, run a shell command, search the web, spawn a subagent. Tools are what make Claude Code agentic. Without them, Claude can only respond with text. Each tool use returns a result that informs Claude's next decision in the agentic loop. See [§1 How Claude Code Works](../ultimate-guide.md#1-how-claude-code-works).

### Turn

One complete response from Claude within a session. A turn begins when you send a message and ends when Claude finishes responding, with any number of tool calls in between. Stop hooks fire at the end of each turn. See [§7 Hooks](../ultimate-guide.md#7-hooks).

---

## V

### Verification loop

A session pattern where you give Claude a check it can run (a test suite, a build, or a screenshot comparison) and Claude iterates until the check passes instead of stopping after one attempt. A verification loop is the prerequisite for `/goal`, unattended runs, and dynamic workflows: without one, the only signal that the agent is finished is the agent itself. See [§9 Advanced Features](../ultimate-guide.md#9-advanced-features).

---

## W

### Worktree isolation

An isolation mode that runs Claude in a separate git worktree under `.claude/worktrees/`, enabled with the `-w` flag or `isolation: worktree` in subagent config. Changes stay on a separate branch and directory, so parallel agents cannot overwrite each other's files. See [§4 Agents](../ultimate-guide.md#4-agents).

---

## Deprecated and renamed terms

These terms appear in older documentation and community content. Use the current name when searching this guide.

| Old term | Now called | Notes |
|----------|-----------|-------|
| Headless mode | Non-interactive mode | Same `-p` flag, same behavior |
| Custom commands | Skills | `.claude/commands/` files still work |
| Slash commands | Commands | "Slash" dropped from product copy |
