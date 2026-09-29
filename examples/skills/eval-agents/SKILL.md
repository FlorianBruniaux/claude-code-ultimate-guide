---
name: eval-agents
description: "Audit custom subagent definitions for Claude Code (.claude/agents/*.md) and Codex (.codex/agents/*.toml): loadability against the native schema, description overlap, model tier, tool scope, and headless-safe instructions. Use when onboarding to a project with agents, after adding or importing agents, or when the parent agent delegates to the wrong agent."
allowed-tools: Read Glob Bash Edit
effort: medium
argument-hint: "[path to agents dir, default: .claude/agents/ and .codex/agents/]"
---

# Agent Evaluator

Discover every custom agent in scope, validate it against the native schema of its host, score it, then review it with the user one agent at a time.

Agents are selected by the parent agent from their `description`. A vague or overlapping description makes delegation unpredictable, so overlap is a correctness defect, not a style issue. The goal is to leave every agent loadable, distinct, correctly modeled, and safe to delegate to.

## When to Use

- Auditing an agent fleet before wiring it into a delegation or orchestration workflow
- The parent agent keeps delegating to the wrong agent, or never delegates
- After copying agents from another project or installing a plugin
- A new agent was added and may collide with existing ones
- Periodic hygiene: do all these agents still do something distinct?

Not for: skills (`eval-skills`), hooks (`eval-hooks`), Claude Code rules (`eval-rules`), or a cross-host configuration health report (`eval-agent-config`).

## Host Reference

### Claude Code: where agents load

Claude Code picks the definition from the highest-priority location when several share a `name`:

| Priority | Location | Scope |
|---|---|---|
| 1 | Managed settings directory, `.claude/agents/` | Organization |
| 2 | `--agents` CLI flag (JSON, or a JSON file path with `-p`) | Current session |
| 3 | `.claude/agents/` | Project |
| 4 | `~/.claude/agents/` | User |
| 5 | Plugin `agents/` directory | Where the plugin is enabled |

- `.claude/agents/` and `~/.claude/agents/` are scanned recursively. Subfolders do not change identity.
- Project agents are discovered by walking up from the working directory; every `.claude/agents/` up to the repository root is scanned, and the definition closest to the working directory wins.
- Directories added with `--add-dir` or `/add-dir` also contribute their `.claude/agents/`.
- Plugin subfolders become part of the scoped identifier: `agents/review/security.md` in plugin `my-plugin` registers as `my-plugin:review:security`.

### Claude Code: files the runtime skips silently

- No `name`: treated as documentation kept beside the agents.
- Opening `---` not on the first line: read as having no frontmatter.
- `name` starting with `-` or containing `:`: skipped, error in the debug log.
- `name` without `description`: skipped.
- YAML that does not parse: skipped. A plugin agent without `name`, or with unparseable frontmatter, still loads under its filename.

Two files in the same agents tree that declare the same `name`: only one loads, chosen by filesystem read order, not by a documented precedence. `/doctor` reports them.

### Claude Code: frontmatter fields

Only `name` and `description` are required. Field names are camelCase and must match exactly; an unknown field is ignored without an error.

| Field | Notes |
|---|---|
| `name` | Required. Unique identity; hooks receive it as `agent_type`. The filename does not have to match. |
| `description` | Required. When the parent should delegate. |
| `tools` | Comma-separated string or YAML list. Omitted: inherits every tool available to subagents. No resolvable entry: the agent usually fails to launch. |
| `disallowedTools` | Removed from the inherited or declared list. A specifier such as `Bash(git push *)` removes the whole tool. |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, a full model ID, or `inherit`. |
| `permissionMode` | `default` (alias `manual`), `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`. Ignored when the main conversation runs in `bypassPermissions`, `acceptEdits` or auto mode. |
| `maxTurns` | Agentic turn cap; output is returned marked partial. |
| `skills` | Skills preloaded in full at startup. |
| `mcpServers` | Server names or inline server definitions. |
| `hooks` | Hooks active while this agent runs; `Stop` becomes `SubagentStop`. Project agent hooks run only after workspace trust is accepted. |
| `memory` | Persistent memory scope: `user`, `project`, or `local`. |
| `background` | `true` keeps the agent in the background. |
| `omitClaudeMd` | `true` launches without user, project and local CLAUDE.md files. |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max`; available levels depend on the model. |
| `isolation` | `worktree` runs the agent in a temporary git worktree. |
| `color` | Display color. |
| `initialPrompt` | First user turn when the agent runs as the main session agent. |
| `experimental` | Map; only `cacheTtl: 5m` or `1h` is read, and only from agent files. |

Plugin agents ignore `hooks`, `mcpServers` and `permissionMode`; `initialPrompt` is also ignored for plugin agents.

Flag as unrecognized (silently ignored by Claude Code): `allowed-tools`, `disallowed-tools`, `context`, `argument-hint`, and any other key not in the table. These are skill fields, not agent fields.

### Claude Code: model resolution

1. The per-invocation `model` parameter passed by the parent
2. The agent's `model` frontmatter (`inherit` selects the main conversation's model)
3. `CLAUDE_CODE_SUBAGENT_MODEL`, when set to an alias or model ID
4. The main conversation's model

`CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` makes every agent ignore its `model` field. A family alias resolves to the main conversation's exact model when that model belongs to the same family. A value blocked by the organization's `availableModels` is substituted.

### Claude Code: tools a subagent never gets

The runtime removes these tools from every non-fork subagent, even when listed in `tools`: `AskUserQuestion`, `EndConversation`, `EnterPlanMode`, `ExitPlanMode` (unless `permissionMode: plan`), `ScheduleWakeup`, `WaitForMcpServers`, and `Agent` at the depth limit.

### Codex: custom agents

| Item | Rule |
|---|---|
| Location | One TOML file per agent in `~/.codex/agents/` (personal) or `.codex/agents/` (project) |
| Required keys | `name`, `description`, `developer_instructions` |
| Identity | `name` is the source of truth; the filename is only a convention |
| Optional keys | Any supported `config.toml` key, such as `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`; omitted keys inherit from the parent session |
| Built-in agents | `default`, `worker`, `explorer`; a custom agent with the same name takes precedence |
| Global settings | `[agents]` in `config.toml`: `enabled`, `max_concurrent_threads_per_session` (legacy `max_threads`), `default_subagent_model`, `default_subagent_reasoning_effort`, `interrupt_message` |

A Markdown agent with YAML frontmatter, or a TOML file using `prompt` instead of `developer_instructions`, is a Claude-shaped definition and does not satisfy the Codex schema.

## Scoring Criteria

### Claude Code agents (15 pts)

| # | Criterion | Max | What is checked |
|---|---|---|---|
| 1 | **loadable** | 2 | Frontmatter parses and `name` is valid: present, no `:`, no leading `-` (1); `description` present (1). A 0 here means the runtime skips the file: stop scoring and report it as a blocker. |
| 2 | **description** | 3 | States when to delegate (1); distinguishable from every other agent in the same scope (1); concise, since combined descriptions above 15,000 tokens trigger a startup warning (1) |
| 3 | **model** | 2 | Declared or deliberately inherited (1); tier fits the task (1) |
| 4 | **tools** | 3 | `tools` explicit (1); no write-capable tool (`Bash`, `Edit`, `Write`, `NotebookEdit`) unless the task mutates files or runs commands (1); `disallowedTools` or `tools` excludes `Agent` when the agent must not delegate further (1) |
| 5 | **system prompt** | 5 | Role and scope in the first paragraph (1); what it does and does not do (1); output or return contract (1); no placeholder or TODO (1); no instruction that requires a tool the runtime removes, such as asking the user a question (1) |
| Bonus | **field hygiene** | +1 | No unrecognized field, and no field that the agent's source ignores (for example `hooks` in a plugin agent) |

### Codex agents (12 pts)

| # | Criterion | Max | What is checked |
|---|---|---|---|
| 1 | **loadable** | 3 | TOML parses (1); `name` and `description` present (1); `developer_instructions` present and non-empty (1) |
| 2 | **description** | 3 | Same checks as Claude Code, against other Codex agents and the built-ins |
| 3 | **model and effort** | 2 | `model` and `model_reasoning_effort` set together when the model is overridden (1); tier fits the task (1) |
| 4 | **instructions** | 4 | Role and scope (1); boundaries (1); return contract (1); no placeholder (1) |

**Thresholds:** Good >= 80%, Needs work 60-79%, Fix < 60%.

### Model tier signals

| Work | Claude Code | Codex (per the Codex subagent docs) |
|---|---|---|
| Mechanical: lookup, extraction, binary verification | `haiku` | lighter model such as `gpt-6-luna` |
| Bounded judgment: review, debugging, tests, documentation | `sonnet` | `gpt-6-sol`, `medium` effort |
| Cross-cutting synthesis: architecture, threat model, multi-system trade-offs | `opus` | `gpt-6-sol`, `high` or above |

Flag both directions: an under-powered model for judgment work, and an over-powered model for mechanical work that runs many times. State cost from published prices instead of a fixed multiplier; for example the guide lists Opus 5.5 at $4/$20 and Haiku 4.5 at $1/$5 per million input/output tokens. Haiku 4.5 has no effort parameter, so an `effort` field on a Haiku agent has no effect.

### Human-in-the-loop anti-pattern

Subagents do not get `AskUserQuestion` or plan-mode tools, and by default they run in the background. Any system prompt instruction such as "ask the user", "confirm before deleting", or "wait for approval" cannot be carried out. Safe alternative: "If context is insufficient, return `{ "status": "needs_context", "missing": [...] }` and stop."

## Execution Instructions

### Step 1: Discovery

Resolve the scope from the argument, or default to the project plus user scope of each requested host.

```bash
# Claude Code: every .md file, recursively
find .claude/agents -name "*.md" 2>/dev/null
find ~/.claude/agents -name "*.md" 2>/dev/null   # user scope, when requested

# Codex: one TOML file per agent
find .codex/agents -name "*.toml" 2>/dev/null
find ~/.codex/agents -name "*.toml" 2>/dev/null  # user scope, when requested
```

Also list nested `.claude/agents/` directories between the working directory and the repository root.

Done when: every candidate file is listed with its host and scope, or the report states that no agent directory exists and stops.

### Step 2: Parse and check loadability

For each file, read it in full and record: host, scope, `name`, `description` length, `model`, `tools` or `(inherits)`, every other key, body or `developer_instructions` line count.

For Claude Code, `claude plugin validate .claude/agents` (v2.1.233 or later) reports files whose frontmatter does not parse; it does not flag a parseable file with no `name`, so check that separately.

Done when: each file is classified as loadable, skipped by the runtime (with the reason from the host reference above), or unreadable.

### Step 3: Check collisions and overlap

- Same `name` twice in one Claude Code agents tree, or a Codex custom agent that shadows a built-in: report which file wins or that the choice is undefined.
- Compare descriptions pairwise within each host and scope. Flag pairs that claim the same kind of request without a stated boundary.

Done when: every collision and overlapping pair is listed with both file paths.

### Step 4: Score

Apply the host's scoring table. Infer the model tier from the system prompt and flag mismatches.

Done when: every loadable agent has a score, a status, and at most three priority fixes.

### Step 5: Interactive review

Process agents one by one. Show host, scope, `name`, model, tools, score, and flagged issues, then ask:

1. Is the description specific enough to distinguish this agent? (y / rewrite)
2. Is the model tier right? (y / change)
3. Are the tools correctly scoped? (y / add / remove)
4. Anything to change in the system prompt or instructions? (describe / skip)

Apply confirmed edits with the file editing capability and confirm each one. For an agent the user marks as stale, ask for an explicit "yes, remove it" before deleting the file.

Done when: every agent has a recorded answer (confirmed, edited, flagged stale, or skipped).

### Step 6: Report

```
# Agents Audit: [scope]
Date: [today] | Scanned: N agents (Claude Code: X, Codex: Y) | Skipped by runtime: Z

| Status | Count |
|--------|-------|
| Good | N |
| Needs work | N |
| Fix | N |
| Skipped by runtime (blocker) | N |
| Name collisions | N |
| Overlapping descriptions | N pairs |
| Unrecognized fields | N |

### code-reviewer.md [Claude Code, project] (12/15)
model: sonnet (inferred: sonnet) | tools: Read, Grep, Glob

| Criterion | Score | Notes |
|---|---|---|
| loadable | 2/2 | ok |
| description | 2/3 | overlaps integration-reviewer.md on "quality checks" |
| model | 2/2 | ok |
| tools | 3/3 | read-only |
| system prompt | 3/5 | no return contract; asks the user to confirm |

Priority fixes:
1. Separate the description from integration-reviewer.md
2. Replace the confirmation step with a structured "needs_context" return
```

End with a change summary: files edited, agents flagged stale (not deleted without confirmation), collisions resolved.

Done when: the report lists every scanned file, including skipped ones.

## Edge Cases

- **`tools` omitted**: the agent inherits the subagent tool pool. Not a load error; flag it for review when the agent does not need write or shell access.
- **`model` omitted**: resolution falls through to `CLAUDE_CODE_SUBAGENT_MODEL` or the main conversation's model. Report the effective source.
- **`allowed-tools` present instead of `tools`**: ignored by Claude Code, so the agent inherits every tool. Flag as a high-priority fix.
- **`effort` on a Haiku agent**: no effect; suggest removing it.
- **Plugin agent with `hooks`, `mcpServers` or `permissionMode`**: ignored; the user must copy the agent to `.claude/agents/` or `~/.claude/agents/` to use them.
- **Agent file in a directory created after the session started**: Claude Code does not watch it until restart; report this when a new agent "does not appear".
- **Codex TOML that uses `prompt`**: not a Codex field; `developer_instructions` is required.
- **Description saying "use for everything"**: acceptable only for an intentional catch-all; flag others.
