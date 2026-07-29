---
title: "Community Patterns & Reference"
description: "Community-coined patterns, AI engineering concepts, workflow terms, and Claude Code configuration reference"
tags: [reference, community, patterns, ai-engineering]
---

# Community Patterns & Reference

Quick-reference for Claude Code community patterns, workflow terms, and AI engineering vocabulary. Standard CS/DevOps terms (JWT, CI/CD, REST) are excluded; look those up elsewhere.

**Format**: Term | Definition | Category | Subcategory

---

| Term | Definition | Category | Subcategory |
|------|-----------|----------|-------------|
| ! (shell prefix) | Prefix to run shell commands directly without Claude's involvement, e.g., `! git status`. Output lands in the conversation. | Claude Code | Interaction |
| @ (file reference) | Syntax to reference specific files in prompts, e.g., `@src/auth.tsx`. Claude loads that file into context immediately. | Claude Code | Interaction |
| .claude/ folder | Project-level directory containing agents, skills, commands, hooks, rules, and settings. `settings.local.json` is gitignored by convention. | Claude Code | Configuration |
| .mcp.json | Project-level file for MCP server configuration, committed to the repo so the whole team shares the same server setup. | Claude Code | Configuration |
| /clear | Slash command that resets the session entirely, discarding all conversation history. Context drops to 0%. | Claude Code | Commands |
| /compact | Slash command that compresses conversation context by summarizing prior exchanges, freeing up context headroom without losing state. | Claude Code | Commands |
| 150K ceiling | Practical effective context limit where output quality degrades, even when the nominal window is larger. See [context-engineering.md](./context-engineering.md). | Architecture | Context |
| ACE pipeline | Assemble, Check, Execute: the three-phase config-persistence loop for intentional context management across sessions. Distinct from arXiv:2510.04618 (same acronym, inference-time context evolution, different concept). ACE-v2 adds signal taxonomy, PR-based loop closure, and ejection. See [context-engineering.md §§10-14](./context-engineering.md#10-signal-taxonomy-and-causal-attribution). | AI Engineering | Context |
| Act Mode | Normal execution mode where Claude can read, write, and run commands. Opposite of Plan Mode. | Claude Code | Modes |
| Adaptive thinking | Opus 4.6+ feature: dynamically adjusts reasoning depth based on detected task complexity, without manual configuration. | Models | Thinking |
| Agent | A specialized AI persona defined in a markdown file with a role, tool list, and behavioral instructions. Stored in `.claude/agents/`. | Claude Code | Extensibility |
| Agent teams | Experimental feature (v2.1.32+) enabling multi-agent coordination and messaging within a single Claude Code session. | Claude Code | Multi-Agent |
| Agentic coding | Development style where AI agents perform multi-step tasks autonomously with minimal per-step human intervention. | AI Engineering | Paradigm |
| AI traceability | Practices for documenting and disclosing AI involvement in code, commits, and content (git trailers, PR labels, audit logs). See [ops/ai-traceability.md](../ops/ai-traceability.md). | Operations | Compliance |
| allowedTools | Settings key providing fine-grained tool permission control: allow or deny individual tools or by argument pattern. | Claude Code | Configuration |
| Annotation cycle | Boris Tane's workflow pattern: annotate a custom markdown plan with implementation notes before Claude executes, creating a living spec. | Workflow | Planning |
| Anti-hallucination protocol | Explicit instructions requiring Claude to verify claims against actual code or documentation before stating them as fact. | AI Engineering | Safety |
| Artifact Paradox | Anthropic research finding (AI Fluency Index, 2026) that users who produce AI artifacts are less likely to question the reasoning behind them. | AI Engineering | Research |
| Auto-accept Mode | Permission mode (`acceptEdits`) that auto-approves file edits while still prompting for shell commands. Good middle ground for trusted sessions. | Claude Code | Permissions |
| Auto-compaction | Built-in mechanism that automatically compresses conversation context (~75% threshold in VS Code extensions, ~95% in CLI). Triggered silently unless you use `/compact` first. | Architecture | Context |
| Auto-memories | Feature (v2.1.32+) where Claude automatically stores learned project context into a persistent memory file across sessions. | Claude Code | Memory |
| autoApproveTools | Settings array listing tools that are auto-approved without interactive prompts. More granular than permission modes. | Claude Code | Configuration |
| awesome-claude-code | Community-curated list of Claude Code resources, tools, and examples with 51K+ stars on GitHub (verified 2026-07-27, was 20K+). | Ecosystem | Community |
| BMAD | Business-driven, Methodical AI Development: a structured planning framework for agentic AI projects (community methodology). | Methodology | Planning |
| Boris Cherny pattern | Horizontal scaling approach: run multiple Claude Code instances in parallel, each on a git worktree, then merge. Named after Boris Cherny, creator of Claude Code and Head of Claude Code at Anthropic. | Workflow | Multi-Agent |
| Bypass Permissions Mode | Maximum autonomy mode via `--dangerously-skip-permissions`: auto-approves all tools. Use only in isolated/sandboxed environments. | Claude Code | Permissions |
| Capability Uplift | Skill type that teaches Claude a new capability it does not have natively, as opposed to enforcing a style preference. | Claude Code | Skills |
| ccusage | Community CLI tool for tracking Claude Code token consumption, cost per session, and model breakdown. | Ecosystem | Tools |
| Chain of Verification (CoVe) | Independent verifier pattern: a second agent re-checks the first agent's output to prevent confirmation bias. arXiv:2309.11495. | Workflow | Verification |
| Checkpoint | A saved session state that can be restored via Esc x2 then /rewind. Created automatically before risky operations. | Claude Code | Session |
| Claude Haiku 4.5 | Anthropic's fastest and cheapest model. Best for high-volume tasks, simple lookups, and cost-sensitive CI workflows. | Models | Tier |
| Claude Opus 5 | Anthropic's current flagship Opus model, default since Claude Code v2.1.219. Supersedes Opus 4.8, still current on Bedrock/Vertex/Claude Platform on AWS. Best for deep reasoning, architecture decisions, and complex multi-step analysis. | Models | Tier |
| Claude Fable 5 | Mythos-class model, exceeding any previously GA Anthropic model. See anthropic.com/pricing for specs. | Models | Tier |
| Claude Sonnet 5 | Anthropic's balanced default model since v2.1.197, with a native 1M-token context window. Best mix of speed and capability for daily development work. | Models | Tier |
| CLAUDE.md | Persistent memory file loaded automatically at session start. Contains project rules, conventions, and context. The foundation of Claude Code configuration. | Claude Code | Memory |
| Co-Authored-By | Git trailer convention (`Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`) for attributing AI-assisted commits. | Operations | Attribution |
| Comprehension debt | The growing gap between code an AI produces and the developer's actual understanding of what it does and why. | AI Engineering | Risk |
| Config hierarchy | Three-tier precedence for CLAUDE.md: Local (`.claude/`, gitignored) > Project (committed) > Global (`~/.claude/CLAUDE.md`). More specific always wins over more general. | Claude Code | Configuration |
| Constitutional AI | Anthropic's value framework (per published system prompt) defining Claude's priority order: safety > ethics > Anthropic principles > user utility. | AI Engineering | Framework |
| Context budget | The finite token allocation that must be distributed across instructions, code, conversation history, and tool results in a single session. | AI Engineering | Context |
| Context engineering | The discipline of intentionally designing what goes into an AI model's context window to maximize output quality. See [context-engineering.md](./context-engineering.md). | AI Engineering | Context |
| Context maturity model | Framework measuring how well a team's context engineering practices have evolved, from ad-hoc prompts to measured pipelines. | AI Engineering | Context |
| Context packing | Technique of densely encoding information (structured markdown, symbols, tables) to maximize useful signal per token. | AI Engineering | Context |
| Context rot | The gradual degradation of Claude's situational awareness in long-running sessions as relevant context gets pushed out or buried. | AI Engineering | Context |
| Context triage | The deliberate decision about what information is worth putting in context upfront vs. loading on demand via tools. | AI Engineering | Context |
| Context window | Total amount of text (in tokens) Claude can process in a single session. Claude Sonnet 5 has a native 1M-token window; Sonnet 4.6 topped out at 200K (1M only via the extended API). | Models | Capacity |
| Ctrl+B | Keyboard shortcut to background a running task, keeping it alive while you continue other work in the session. | Claude Code | Shortcuts |
| dangerouslyDisableSandbox | Flag that bypasses Claude Code's native OS-level sandboxing. Should only be used in already-isolated environments. | Security | Configuration |
| Default Mode | Base permission mode requiring explicit user approval for all file edits, shell commands, and commits. | Claude Code | Permissions |
| Desloppify | Community tool ([@peteromaller](https://github.com/peteromaller), Feb 2026) that installs a workflow skill into Claude Code and runs a scan-fix-score loop to raise code quality. [github.com/peteromaller/desloppify](https://github.com/peteromaller/desloppify) | Ecosystem | Tools |
| Diff review | The practice of reading Claude's proposed file changes before accepting or rejecting. One of the Five Golden Rules. | Claude Code | Workflow |
| disallowedTools | Settings key that blocks specific tools from being invoked in a session or globally. | Claude Code | Configuration |
| Docker sandbox | Container-based isolation for running Claude Code with strict resource and filesystem limits. See [security/sandbox-isolation.md](../security/sandbox-isolation.md). | Security | Sandbox |
| Don't Ask Mode | Permission mode (`dontAsk`) that silently denies tools not in the pre-approved list, without prompting. | Claude Code | Permissions |
| Dual-instance planning | Pattern by Jon Williams: one Claude instance creates a detailed plan, a separate instance executes it, preventing context contamination. | Workflow | Planning |
| Encoded Preference | Skill type that enforces specific conventions, style choices, or constraints Claude would not apply by default. | Claude Code | Skills |
| Enterprise AI governance | Org-level policies for AI tool usage: usage charter, MCP server registry, guardrail tiers, and audit trail. See [security/enterprise-governance.md](../security/enterprise-governance.md). | Security | Enterprise |
| Eval harness | Testing framework for systematically measuring agent behavior, output quality, and skill effectiveness against defined criteria. | Methodology | Testing |
| Event-driven agents | Pattern where external events (Linear tickets, GitHub PRs, Jira webhooks) automatically trigger Claude Code agent workflows. | Workflow | Architecture |
| Extended thinking | Model feature enabling deeper reasoning via dedicated "thinking tokens" processed before the visible response. Activated with `--thinking`. | Models | Thinking |
| Fast Mode | Mode (v2.1.36+) running 2.5x faster at 6x the token cost, on the same underlying model. Toggle with `/fast`. | Claude Code | Modes |
| FIRE framework | Find, Isolate, Remediate, Evaluate: a DevOps/SRE troubleshooting methodology for incident response with Claude Code. See [ops/devops-sre.md](../ops/devops-sre.md). | Methodology | Operations |
| Fresh context pattern | Deliberately starting a new session when the current one has accumulated irrelevant context or its output quality has degraded. | Workflow | Context |
| Gas Town | Steve Yegge's multi-agent workspace manager for running multiple coordinated Claude Code instances with a shared task queue. | Ecosystem | Orchestration |
| Git worktree | Git feature creating parallel working directories from the same repo. Used for multi-instance Claude Code workflows without branch switching. | Workflow | Infrastructure |
| GSD (Get Shit Done) | Pragmatic, outcome-focused development methodology: ship fast, validate with real usage, iterate based on feedback. | Methodology | Paradigm |
| gstack | Garry Tan's 6-skill workflow suite: strategic gate + architecture review + code review + release notes + browser QA + retrospective. | Workflow | Framework |
| Guardrail tiers | Four enterprise security enforcement levels: Starter (awareness), Standard (review gates), Strict (approval flows), Regulated (full audit). | Security | Enterprise |
| Hallucination | When an AI model generates plausible-sounding but factually incorrect information, often with high apparent confidence. | AI Engineering | Risk |
| Hook | An automation script triggered by Claude Code lifecycle events. Defined in `settings.json`. Runs synchronously before or after tool execution. | Claude Code | Extensibility |
| Hook types | Five execution types: `command` (shell script), `http` (POST webhook), `mcp_tool` (MCP server tool), `prompt` (single-turn LLM call), `agent` (full multi-turn sub-agent). | Claude Code | Hooks |
| Infisical | Open-source secrets manager used for injecting credentials into Claude Code sessions without storing them in CLAUDE.md or env files. | Ecosystem | Security |
| JSONL transcript | Session history stored as JSON Lines files in `~/.claude/projects/`. Can be searched, replayed, and analyzed programmatically. | Architecture | Storage |
| llms.txt | Standard file format (placed at site root) for AI-optimized documentation. Claude Code reads `llms.txt` files from project roots. | AI Engineering | Standard |
| Master loop | Claude Code's core execution cycle: receive input → select tools → execute → observe results → respond. Repeats until task complete. | Architecture | Internals |
| MCP (Model Context Protocol) | Open protocol developed by Anthropic for connecting AI models to external tools, databases, and APIs in a standardized way. | Architecture | Protocol |
| Mechanic Stacking | Pattern of layering multiple Claude Code mechanisms (Plan Mode + extended thinking + MCP) for maximum reasoning on critical decisions. | Workflow | Pattern |
| Memory hierarchy | Three-tier CLAUDE.md precedence: Local > Project > Global. Each level extends the one below and can override it for its own scope. | Claude Code | Memory |
| Model aliases | Shorthand names that resolve to current model versions: `default`, `sonnet`, `opus`, `haiku`, `sonnet[1m]`, `opusplan`. | Models | Configuration |
| Modular context architecture | Pattern of splitting CLAUDE.md into focused modules loaded dynamically via path-scoped rules, reducing per-session token overhead. | AI Engineering | Context |
| multiclaude | Community self-hosted multi-agent spawner using tmux + git worktrees. Runs N Claude Code instances in parallel. | Ecosystem | Orchestration |
| Native sandbox | Claude Code's built-in OS-level sandboxing: Seatbelt on macOS, bubblewrap on Linux. Limits filesystem and network access. | Security | Sandbox |
| OpusPlan | Hybrid mode: Opus 5 handles planning (with thinking), Sonnet executes. Activates with `/model opusplan`. | Models | Configuration |
| Packmind | Tool that distributes coding standards as `CLAUDE.md` files, slash commands, and skills across repositories and AI tools (Claude Code, Cursor, Copilot). | Ecosystem | Tools |
| Permission modes | Five autonomy levels: Default, Auto-accept, Plan, Don't Ask, Bypass Permissions. Set per session or in `settings.json`. | Claude Code | Permissions |
| Plan Mode | Read-only mode where Claude can analyze, search, and propose but cannot modify files. Activated with Shift+Tab or `/plan`. | Claude Code | Modes |
| Plugin | A distributable package bundling agents, skills, commands, and hooks under a `plugin.json` manifest. Installable from the marketplace. | Claude Code | Extensibility |
| PostToolUse | Hook event fired after a tool completes execution. Used for post-processing, formatting, validation, and logging. | Claude Code | Hooks |
| PreToolUse | Hook event fired before Claude executes a tool. Can block, allow, or modify the tool call based on arguments. | Claude Code | Hooks |
| Prompt injection | Attack where malicious text in files or external inputs attempts to override Claude's instructions or exfiltrate information. | Security | Attack |
| Ralph Loop | Also "Ralph Wiggum Loop" (Geoffrey Huntley). Iterative refinement cycle: generate → review → correct → repeat, until output meets quality bar. | Workflow | Quality |
| Recovery ladder | Three levels of undo: reject change inline, /rewind to session checkpoint, `git restore` as nuclear reset. | Claude Code | Safety |
| Rev the Engine | Pattern of running multiple rounds of deep analysis and planning before executing, to surface edge cases and failure modes early. | Workflow | Pattern |
| Rewind | Claude Code's undo mechanism. Reverts file changes and/or conversation state to a prior checkpoint. Trigger: Esc x2. | Claude Code | Session |
| RTK (Rust Token Killer) | CLI proxy that reduces token consumption 60-90% by filtering and compressing command output before it reaches Claude. | Ecosystem | Tools |
| Rules (.claude/rules/) | Auto-loaded markdown files providing always-on instructions. Loaded at every session start, independent of which skills are active. | Claude Code | Configuration |
| SE-CoVe (Software Engineering Chain-of-Verification) | Community plugin implementing Chain-of-Verification with independent review agents for automated output validation. Based on Meta's CoVe research (arXiv:2309.11495). | Ecosystem | Plugins |
| Semantic anchors | Named reference patterns in CLAUDE.md (e.g., `## Architecture`) that Claude reliably finds and follows across sessions. | AI Engineering | Context |
| Session | A single Claude Code conversation with its own context window, history, checkpoints, and tool state. | Claude Code | Core |
| Session handoff | Manually starting a new session and passing a summarized context document from an exhausted or degraded previous session. | Workflow | Context |
| SessionStart / SessionEnd | Hook events fired when a session begins or closes. Used for setup scripts, logging, and cleanup automation. | Claude Code | Hooks |
| Shift+Tab | Keyboard shortcut to toggle between Plan Mode and Act Mode. | Claude Code | Shortcuts |
| Skeleton project | A minimal but fully working project template generated by Claude to establish architecture patterns before full implementation begins. | Workflow | Scaffolding |
| Skill | A reusable knowledge module (folder + SKILL.md entry point) providing domain expertise or behavioral instructions on demand. | Claude Code | Extensibility |
| Skill evals | Automated evaluation criteria that measure skill quality, invocation reliability, and output consistency. Part of Skills 2.0. | Claude Code | Skills |
| Skills 2.0 | Evolution of the skills system introducing Capability Uplift types, Encoded Preference types, evals, and lifecycle management. | Claude Code | Skills |
| Slash command | Custom commands defined as markdown files in `.claude/commands/`, invoked with `/command-name`. Support `$ARGUMENTS` substitution. | Claude Code | Extensibility |
| Slop | Unwanted, unreviewed AI-generated content: the AI equivalent of spam. Term coined by Simon Willison in May 2024. | AI Engineering | Quality |
| SonnetPlan | Community remapping of OpusPlan: Sonnet handles planning, Haiku handles execution. Cheaper than OpusPlan for lighter tasks. | Models | Configuration |
| Spec-first development | Addy Osmani's pattern: write a detailed specification document before any implementation begins. Reduces scope creep and clarifies edge cases. | Workflow | Planning |
| Stop | Hook event fired when Claude is about to stop responding. Used for quality gates, cleanup tasks, and completion notifications. | Claude Code | Hooks |
| Strategic gate | Pre-implementation product review step in the gstack workflow. Ensures the feature is worth building before any code is written. | Workflow | Quality |
| Sub-agent | A child Claude instance spawned by the main session to handle a delegated task in isolation, with its own context. | Claude Code | Multi-Agent |
| Supply chain attack | Exploiting trusted dependencies (MCP servers, plugins, community skills) to inject malicious behavior or exfiltrate data. | Security | Attack |
| Tasks API | Built-in task management system (v2.1.16+) with dependency tracking, status management, and cross-session persistence. Replaces TodoWrite. | Claude Code | Core |
| The 20% Rule | Decision framework: patterns in >20% of sessions → CLAUDE.md rules; 5-20% → skills; <5% → commands. | Claude Code | Decision |
| The 56% Reliability Warning | Vercel engineering blog finding (Gao, 2026) that agents invoke on-demand skills only 56% of the time, defaulting to native knowledge instead. | AI Engineering | Research |
| The 80% Problem | Addy Osmani's observation: AI reliably handles 80% of a task; the remaining 20% is where human expertise and judgment determine success. | AI Engineering | Research |
| The Trinity | Core advanced pattern combining Plan Mode + Extended Thinking + Sequential MCP for maximum reasoning depth on critical decisions. | Workflow | Pattern |
| Thinking tokens | Internal reasoning tokens consumed during extended thinking. Not visible in Claude's response but counted toward the context budget. | Models | Thinking |
| Token | The basic unit of text that language models process. Roughly 3/4 of an English word, or ~4 characters. 1K tokens ≈ 750 words. | Models | Core |
| Token efficiency | Minimizing token consumption while maintaining output quality. Key for cost management, context headroom, and session longevity. | AI Engineering | Optimization |
| Tool shadowing | Attack where a malicious MCP server registers tools with names matching Claude Code's built-in tools to intercept or hijack calls. | Security | Attack |
| Tool-qualified deny | Permission pattern blocking a tool based on argument values, e.g., `Read(file_path:*.env*)` to prevent reading secrets files. | Security | Permissions |
| Trust calibration | Framework for matching verification effort to the actual risk level of AI-generated code, avoiding both blind acceptance and paranoid review. | AI Engineering | Quality |
| UserPromptSubmit | Hook event fired when the user submits a prompt, before Claude begins processing. Used for prompt enrichment, logging, and validation. | Claude Code | Hooks |
| Verification debt | The accumulated risk of AI-generated code that was not reviewed at the time of creation, compounding over successive sessions. | AI Engineering | Risk |
| Verification paradox | The tension between needing rigorous verification of AI code while increasingly relying on AI tools to perform the verification. | AI Engineering | Risk |
| Vertical slice | A task scoped to one user-facing behavior, crossing all architectural layers (UI → API → DB). Preferred unit for AI-assisted implementation. | Methodology | Architecture |
| Vibe coding | Style of development where you describe high-level intent and iterate rapidly on AI output, prioritizing shipping speed over precision. | Workflow | Paradigm |
| Vibe Review | Intermediate verification layer between blind acceptance and full line-by-line review. Faster for low-risk changes, still catches obvious issues. | Workflow | Quality |
| Vitals | Community plugin for codebase hotspot detection via a combined score of git churn x complexity x module coupling centrality. | Ecosystem | Plugins |
| WHAT/WHERE/HOW/VERIFY | Structured prompt format: what to do, where in the codebase, how to approach it, how to verify success. Reduces ambiguity in agentic tasks. | AI Engineering | Prompting |

---

*This reference covers ~130 terms. For official Claude Code terminology, see [glossary.md](./glossary.md). For the full guide, see [ultimate-guide.md](../ultimate-guide.md). To suggest a missing term, open an issue on [GitHub](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/issues).*
