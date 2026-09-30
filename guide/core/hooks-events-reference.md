---
title: "Claude Code Hooks Events Reference: All 33 Events, Matchers & Schemas"
description: "Complete reference for all 33 Claude Code hook events: matcher fields, input schemas, decision control, and timeout defaults, with copy-paste JSON examples for each event."
tags: [reference, hooks]
---

# Hooks events reference

Complete reference for all 33 Claude Code hook events: matcher fields, input schemas, decision control, and timeout defaults. Source: official Anthropic documentation ([hooks reference](https://code.claude.com/docs/en/hooks)), checked against Claude Code v2.1.284.

For the audit skill, see `examples/skills/eval-hooks/SKILL.md`.

See also: [Event-Driven Agent Automation](../workflows/event-driven-agents.md) for building hook-driven workflows, and [Security Hardening: Startup Hooks](../security/security-hardening.md#16-startup-hooks-code-execution-before-your-first-prompt) for the risks of executing code via hooks.

---

## Quick reference

| Event | Fires when | Matcher field | Can block? | Default timeout |
|-------|-----------|---------------|------------|----------------|
| `SessionStart` | Session begins or resumes | `source` | No | 600s |
| `Setup` | `--init-only` or `-p --init/--maintenance` | `trigger` | No | 600s |
| `UserPromptSubmit` | User submits a prompt | none | Yes | **30s** |
| `UserPromptExpansion` | Slash command expands to prompt | `command_name` | Yes | 600s |
| `PreToolUse` | Before tool call executes | `tool_name` | Yes | 600s |
| `PermissionRequest` | Tool call needs a permission decision | `tool_name` | Not by exit 2; JSON `decision` object only | 600s |
| `PermissionDenied` | Auto-mode classifier denies a call | `tool_name` | No (retry only) | 600s |
| `PostToolUse` | After tool call succeeds | `tool_name` | No (stderr to Claude) | 600s |
| `PostToolUseFailure` | After tool call fails | `tool_name` | No | 600s |
| `PostToolBatch` | After full parallel batch resolves | none | Yes (stops loop) | 600s |
| `Notification` | Claude sends a notification | `notification_type` | No | 600s |
| `MessageDisplay` | Assistant message text streams | none | No | **10s** |
| `SubagentStart` | Subagent spawned via Agent tool | `agent_type` | No | 600s |
| `SubagentStop` | Subagent finishes | `agent_type` | Yes | 600s |
| `TaskCreated` | Task being created via TaskCreate | none | Yes | 600s |
| `TaskCompleted` | Task being marked as completed | none | Yes | 600s |
| `Stop` | Claude finishes responding | none | Yes (continues turn) | 600s |
| `StopFailure` | Turn ends due to API error | `error` | No (ignored) | 600s |
| `TeammateIdle` | Agent team teammate goes idle | none | Yes | 600s |
| `InstructionsLoaded` | CLAUDE.md or rules file loaded | `load_reason` | No | 600s |
| `ConfigChange` | Config file changes during session | `source` | Yes (not `policy_settings`) | 600s |
| `CwdChanged` | Working directory changes | none | No | 600s |
| `DirectoryAdded` | Directory added via `/add-dir` or SDK `register_repo_root` | `source` | No | 600s |
| `FileChanged` | Watched file changes on disk | filename (literal) | No | 600s |
| `WorktreeCreate` | Worktree being created | none | Yes (any non-zero) | 600s |
| `WorktreeRemove` | Worktree being removed | none | Yes (any non-zero fails removal if the directory remains) | 600s |
| `PreCompact` | Before context compaction | `trigger` | Yes | 600s |
| `PostCompact` | After compaction completes | `trigger` | No | 600s |
| `PreModelSwitch` | Before a requested model switch is applied | canonical target model | Yes | **30s** |
| `PostModelSwitch` | After the session model changes, including automatic changes | canonical target model | No | **30s** |
| `Elicitation` | MCP server requests user input | `mcp_server_name` | Yes | 600s |
| `ElicitationResult` | User responds to MCP elicitation | `mcp_server_name` | Yes | 600s |
| `SessionEnd` | Session terminates | `reason` | No | **1.5s budget** |

**Timeout exceptions**: the `command`, `http`, and `mcp_tool` default of 600s drops to 30s on `UserPromptSubmit`, `PreModelSwitch`, and `PostModelSwitch`, and to 10s on `MessageDisplay`. `prompt` hooks default to 30s. `agent` hooks default to 60s. `SessionEnd` has a 1.5s total budget; a per-hook `timeout` raises it to the highest configured value, up to 60s. Timeouts on plugin hooks do not raise the budget. A timed-out `command`, `http`, or `mcp_tool` hook on `PreToolUse` does not block the tool call; on `PreModelSwitch` it blocks the switch.

---

## Matcher values by event

The `matcher` field filters on a different field depending on the event type.

### Tool events: matcher filters on `tool_name`

Events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`

Values: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch`, `AskUserQuestion`, `ExitPlanMode`, and MCP tools as `mcp__<server>__<tool>`.

Matching rules (all events with matcher support):
- Only letters, digits, `_`, `-`, spaces, `,`, and `|`: exact string, or a list of exact strings separated by `|` or `,` (`Edit|Write`, `Edit, Write`). Hyphens in the exact set require v2.1.195 or later.
- Contains any other character: unanchored JavaScript regex (`mcp__memory__.*`). `Edit.*` also matches `NotebookEdit`; anchor with `^...$` for a whole-string match.
- `"*"`, `""`, or absent: matches all.
- `FileChanged` and `StopFailure` use a narrower exact set (letters, digits, `_`, `|` only); a hyphen, space, or comma there keeps the matcher on the regex path.

To match every tool from an MCP server: `mcp__memory__.*` (the `.*` is required; `mcp__memory` without it is an exact string and matches no tool).

### SessionStart: matcher filters on `source`

| Value | When |
|-------|------|
| `startup` | New session |
| `resume` | `--resume`, `--continue`, or `/resume` |
| `clear` | `/clear` |
| `compact` | Auto or manual compaction |
| `fork` | Forked session |

### Setup: matcher filters on `trigger`

| Value | When |
|-------|------|
| `init` | `claude --init-only` or `claude -p --init` |
| `maintenance` | `claude -p --maintenance` |

### SessionEnd: matcher filters on `reason`

| Value | When |
|-------|------|
| `clear` | `/clear` command |
| `resume` | Interactive `/resume` switch |
| `logout` | User logged out |
| `prompt_input_exit` | Exited while prompt input was visible |
| `other` | Other exit reasons |

`bypass_permissions_disabled` was removed in v2.1.234; drop it from `SessionEnd` matchers.

### Notification: matcher filters on `notification_type`

Values: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_url_dialog`, `elicitation_complete`, `elicitation_response`, `agent_needs_input`, `agent_completed`, `quota_auto_resume_fired`, `quota_auto_resume_stale`, `quota_auto_resume_disabled`

### SubagentStart / SubagentStop: matcher filters on `agent_type`

Values: `general-purpose`, `Explore`, `Plan`, or custom agent names (the `name` field from the agent's frontmatter, not the filename).

### PreCompact / PostCompact: matcher filters on `trigger`

Values: `manual` (from `/compact`), `auto` (automatic)

### InstructionsLoaded: matcher filters on `load_reason`

Values: `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`

### ConfigChange: matcher filters on `source`

Values: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`

### StopFailure: matcher filters on `error`

Values: `rate_limit`, `overloaded`, `authentication_failed`, `oauth_org_not_allowed`, `account_on_hold`, `billing_error`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, `cloud_credential_error` (v2.1.267+), `unknown`

### UserPromptExpansion: matcher filters on `command_name`

Your skill or command name as typed by the user (without the leading `/`).

### Elicitation / ElicitationResult: matcher filters on `mcp_server_name`

Your configured MCP server name.

### DirectoryAdded: matcher filters on `source`

Values: `slash_command` (`/add-dir`), `register_repo_root` (SDK control request)

### PreModelSwitch / PostModelSwitch: matcher filters on the canonical target model

The matcher is compared with the canonical name derived from `to_model`, ignoring any `[1m]` suffix: `claude-opus-5`, `claude-opus-4-6|claude-opus-5`, `.*opus.*`. When Claude Code cannot derive a canonical name (for example a gateway-only custom ID), every PreModelSwitch hook runs regardless of matcher, so a blocking hook should also check `to_model`.

### FileChanged: matcher = literal filenames

Split on `|`, each segment is registered as a literal filename watched in the current directory. Example: `".envrc|.env"`. Unlike other events, regex patterns are not applied here. The same value builds the watch list AND filters which hooks run.

### Events with no matcher support

`UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `CwdChanged`, `MessageDisplay`

Adding a `matcher` field to these events is silently ignored.

---

## Exit code 2 behavior per event

Exit code 2 is the only exit code that blocks through the code alone. Claude Code reads JSON output fields from stdout on every exit code, not only 0: for events that use the standard decision model, a valid JSON decision (for example `permissionDecision: "deny"` or `decision: "block"`) takes effect with exit 0 or any other non-2 code, and exit 2 still blocks even if the JSON says `allow`. Exit code 1 without valid JSON is a non-blocking error: the action proceeds and the first line of stderr appears in the transcript. `WorktreeCreate` and `WorktreeRemove` are the exceptions: any non-zero code fails them.

| Event | What happens on exit 2 |
|-------|------------------------|
| `PreToolUse` | Blocks the tool call; stderr fed to Claude |
| `PermissionRequest` | Not honored: the permission flow proceeds unchanged and stderr is discarded. Deny through the JSON `decision` object |
| `UserPromptSubmit` | Blocks prompt and erases it from context |
| `UserPromptExpansion` | Blocks the expansion |
| `Stop` | Prevents stopping; continues the turn |
| `SubagentStop` | Prevents subagent from stopping |
| `TeammateIdle` | Teammate continues working; stderr fed back |
| `TaskCreated` | Rolls back task creation; stderr fed back |
| `TaskCompleted` | Prevents completion; stderr fed back |
| `ConfigChange` | Blocks config change (not `policy_settings`) |
| `PostToolBatch` | Stops agentic loop before next model call |
| `PreCompact` | Blocks compaction |
| `Elicitation` | Denies the elicitation |
| `ElicitationResult` | Blocks response (effective action becomes decline) |
| `WorktreeCreate` | **Any** non-zero exit code fails creation |
| `WorktreeRemove` | **Any** non-zero exit code fails removal if the directory still exists afterward |
| `PreModelSwitch` | Blocks the model switch and shows stderr to the user |
| `PostModelSwitch` | Shows stderr to user only; the model already switched |
| `PostToolUse` | Shows stderr to Claude (tool already ran) |
| `PostToolUseFailure` | Shows stderr to Claude |
| `StopFailure` | Ignored entirely (output and exit code ignored) |
| `SessionEnd` | Shows stderr to user only |
| `SessionStart`, `Setup`, `SubagentStart` | Shows stderr to user only |
| `Notification` | Shows stderr to user only |
| `InstructionsLoaded` | Exit code ignored |
| `PermissionDenied` | Exit code and stderr ignored |
| `CwdChanged`, `FileChanged` | Shows stderr to user only |
| `DirectoryAdded` | Stderr goes to the debug log; the directory is already added |
| `PostCompact` | Shows stderr to user only |
| `MessageDisplay` | Original text displayed unchanged |

---

## Decision control format per event

### Top-level `decision` field

Used by: `UserPromptSubmit`, `UserPromptExpansion`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Stop`, `SubagentStop`, `ConfigChange`, `PreCompact`

```json
{ "decision": "block", "reason": "Explanation" }
```

Only `"block"` is valid. Omit `decision` to allow. For `Stop` and `SubagentStop`, the `reason` becomes Claude's next instruction.

### PreToolUse

Uses `hookSpecificOutput` for richer control. Precedence when hooks conflict: `deny > defer > ask > allow`.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow | deny | ask | defer",
    "permissionDecisionReason": "Shown to user (allow/ask) or to Claude (deny)",
    "updatedInput": { "field": "new value" },
    "additionalContext": "Context injected next to tool result"
  }
}
```

`defer` only works in `-p` (non-interactive) mode. Process exits with `stop_reason: "tool_deferred"` and the calling process can resume later. `defer` does not work when Claude makes several tool calls at once.

### PreModelSwitch

Exit code 2 or top-level `decision: "block"` cancels the switch. For finer control use `hookSpecificOutput.permissionDecision` with `allow`, `deny`, or `ask` (no `defer`, `updatedInput`, or `additionalContext`).

### TaskCreated

Exit code 2 or top-level `decision: "block"` cancels the task creation. `continue: false` is ignored.

### PermissionRequest

A hook that exits 2 without a `decision` object leaves the permission flow unchanged. Only the `decision` object grants or denies. `agent` hooks are skipped on this event. In sessions that cannot show a prompt, such as background subagents in `-p` mode, these hooks still run, and the call is denied if no hook decides.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow | deny",
      "updatedInput": {},
      "updatedPermissions": [],
      "message": "Reason for deny",
      "interrupt": false
    }
  }
}
```

### PermissionDenied

Exit code and stderr are ignored. To signal retry:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

### PostToolUse

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Context injected next to tool result",
    "updatedToolOutput": { "stdout": "...", "stderr": "", "interrupted": false, "isImage": false }
  }
}
```

`updatedToolOutput` changes what Claude sees, not what already executed. Must match the tool's output shape exactly. Built-in tools with incorrect shapes fall back to the original.

### WorktreeCreate

Command hooks print the absolute path on stdout. HTTP hooks return:

```json
{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/abs/path" } }
```

Any failure or missing path fails worktree creation.

### MessageDisplay

```json
{
  "hookSpecificOutput": {
    "hookEventName": "MessageDisplay",
    "displayContent": "Replacement text shown on screen"
  }
}
```

Changes only what appears on screen. Claude and the transcript keep the original.

### SessionStart (additional fields)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Context before first prompt",
    "sessionTitle": "branch-or-feature-name",
    "watchPaths": ["/absolute/path/to/watch"],
    "reloadSkills": true,
    "initialUserMessage": "First turn in -p mode"
  }
}
```

`reloadSkills: true` rescans skill directories after hooks complete, so skills installed by the hook are available immediately in the same session.

### Elicitation

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept | decline | cancel",
    "content": { "field_name": "value" }
  }
}
```

### ElicitationResult

Same format as Elicitation output. Overrides what the user submitted.

### Universal fields (all events)

```json
{
  "continue": false,
  "stopReason": "Message shown to user (not Claude)",
  "suppressOutput": true,
  "systemMessage": "Warning shown to user",
  "terminalSequence": "\033]777;notify;Title;Body\007"
}
```

`continue: false` stops Claude entirely, takes precedence over all decision fields.

`terminalSequence`: desktop notifications and window titles via OSC sequences. Restricted to OSC `0/1/2/9/99/777` and BEL. Writing to `/dev/tty` directly fails since v2.1.139 because hooks run without a controlling terminal.

---

## Key input fields per event

All events receive: `session_id`, `transcript_path`, `cwd`, `hook_event_name`, and usually `permission_mode`. Subagent hooks also receive `agent_id` and `agent_type`.

| Event | Event-specific extra input fields |
|-------|----------------------------------|
| `SessionStart` | `source`, `model`, optionally `agent_type`, `session_title` |
| `Setup` | `trigger` (`"init"` or `"maintenance"`) |
| `UserPromptSubmit` | `prompt` |
| `UserPromptExpansion` | `expansion_type`, `command_name`, `command_args`, `command_source`, `prompt` |
| `PreToolUse` | `tool_name`, `tool_input`, `tool_use_id` |
| `PermissionRequest` | `tool_name`, `tool_input`, `permission_suggestions` |
| `PermissionDenied` | `tool_name`, `tool_input`, `tool_use_id`, `reason` |
| `PostToolUse` | `tool_name`, `tool_input`, `tool_response`, `tool_use_id`, `duration_ms` |
| `PostToolUseFailure` | `tool_name`, `tool_input`, `tool_use_id`, `error`, `is_interrupt`, `duration_ms` |
| `PostToolBatch` | `tool_calls` (array with `tool_name`, `tool_input`, `tool_use_id`, `tool_response`) |
| `Notification` | `message`, `title`, `notification_type` |
| `MessageDisplay` | `turn_id`, `message_id`, `index`, `final`, `delta` |
| `SubagentStart` | `agent_id`, `agent_type` |
| `SubagentStop` | `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path`, `last_assistant_message` |
| `TaskCreated` | `task_id`, `task_subject`, `task_description`, `teammate_name`, `team_name` |
| `TaskCompleted` | `task_id`, `task_subject`, `task_description`, `teammate_name`, `team_name` |
| `Stop` | `stop_hook_active`, `last_assistant_message`, `background_tasks`, `session_crons` |
| `StopFailure` | `error`, `error_details`, `last_assistant_message` |
| `TeammateIdle` | `teammate_name`, `team_name` |
| `InstructionsLoaded` | `file_path`, `memory_type`, `load_reason`, `globs`, `trigger_file_path`, `parent_file_path` |
| `ConfigChange` | `source`, `file_path` |
| `CwdChanged` | `old_cwd`, `new_cwd` |
| `DirectoryAdded` | `directory`, `source` |
| `FileChanged` | `file_path`, `event` (`"change"`, `"add"`, `"unlink"`) |
| `WorktreeCreate` | `name` (slug for the new worktree) |
| `WorktreeRemove` | `worktree_path` |
| `PreCompact` | `trigger`, `custom_instructions` |
| `PostCompact` | `trigger`, `compact_summary` |
| `PreModelSwitch` | `from_model`, `to_model`, `requested_model`, `source`, `context_tokens`, `prompt_cache_warm`, `cache_ttl`, `estimated_cache_write_usd`, `pricing` |
| `PostModelSwitch` | Same as `PreModelSwitch`; `source` adds `auto` and `resume` |
| `Elicitation` | `mcp_server_name`, `message`, `mode`, `url`, `elicitation_id`, `requested_schema` |
| `ElicitationResult` | `mcp_server_name`, `action`, `mode`, `elicitation_id`, `content` |
| `SessionEnd` | `reason` |

---

## Hook handler fields

### Common fields (all types)

| Field | Description |
|-------|-------------|
| `type` | `command`, `http`, `mcp_tool`, `prompt`, or `agent` |
| `if` | Permission rule syntax to narrow the handler. Tool events only (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`). On any other event, a hook with `if` set never runs |
| `timeout` | Seconds before canceling. Not enforced on a running `async: true` command hook; still enforced with `asyncRewake` |
| `statusMessage` | Custom spinner message while hook runs |
| `once` | Run once per session then remove. Honored only in skill frontmatter, ignored in settings files |

### Command hook fields

| Field | Description |
|-------|-------------|
| `command` | Shell command or executable path |
| `args` | Argument vector: triggers exec form (no shell involved) |
| `async` | `true` to run in background without blocking |
| `asyncRewake` | Like `async: true` but wakes Claude on exit 2, showing stderr (or stdout if stderr is empty) as a system reminder |
| `shell` | `"bash"` (default) or `"powershell"` (Windows) |

**Shell form** (`args` absent): `command` passed to `sh -c`. Supports pipes, `&&`, globs.
**Exec form** (`args` present): `command` is the executable, each `args` element is one verbatim argument. Use for paths with spaces or when referencing `${CLAUDE_PROJECT_DIR}`.

### HTTP hook fields

| Field | Description |
|-------|-------------|
| `url` | POST endpoint URL |
| `headers` | Additional headers (supports `$VAR` interpolation) |
| `allowedEnvVars` | Env vars allowed to be interpolated in header values |

Non-2xx responses are non-blocking. To block, return 2xx with `decision: "block"` in the JSON body.

### MCP tool hook fields

| Field | Description |
|-------|-------------|
| `server` | Connected MCP server name |
| `tool` | Tool name on that server |
| `input` | Tool arguments. String values support `${path}` substitution from hook input |

Server must already be connected. `SessionStart` and `Setup` typically fire before servers finish connecting.

### Prompt hook fields

| Field | Description |
|-------|-------------|
| `prompt` | Prompt text. Use `$ARGUMENTS` for the hook's JSON input |
| `model` | Model override (default: fast model, typically Haiku) |
| `continueOnBlock` | When `ok: false`, feed the reason back to Claude and continue instead of stopping |

Returns `{ "ok": true/false, "reason": "..." }`. See [Hook type support per event](#hook-type-support-per-event) for the events that accept `prompt` hooks.

### Agent hook fields

| Field | Description |
|-------|-------------|
| `prompt` | Task description. Use `$ARGUMENTS` for the hook's JSON input |
| `model` | Model override |

Spawns a subagent that can use Read, Grep, Glob (up to 50 turns), then returns the same `{ "ok": true/false }` schema. Experimental.

### Hook type support per event

| Event group | Supported handler types |
|-------------|-------------------------|
| `PermissionDenied`, `PostToolBatch`, `PostToolUse`, `PostToolUseFailure`, `PreToolUse`, `Stop`, `SubagentStop`, `TaskCompleted`, `TaskCreated`, `TeammateIdle`, `UserPromptExpansion`, `UserPromptSubmit` | `command`, `http`, `mcp_tool`, `prompt`, `agent` |
| `PermissionRequest` | `command`, `http`, `mcp_tool`, `prompt` (an `agent` hook is skipped) |
| `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `Elicitation`, `ElicitationResult`, `FileChanged`, `InstructionsLoaded`, `MessageDisplay`, `Notification`, `PostCompact`, `PostModelSwitch`, `PreCompact`, `PreModelSwitch`, `SessionEnd`, `StopFailure`, `SubagentStart`, `WorktreeCreate`, `WorktreeRemove` | `command`, `http`, `mcp_tool` |
| `SessionStart`, `Setup` | `command`, `mcp_tool` |

On `PermissionDenied`, prompt and agent hooks run but their output is discarded.

---

## Path placeholders

| Placeholder | Resolves to |
|-------------|-------------|
| `${CLAUDE_PROJECT_DIR}` | Project root directory |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin installation directory (changes on update) |
| `${CLAUDE_PLUGIN_DATA}` | Plugin persistent data directory (survives updates) |

Prefer exec form for hooks referencing these: each `args` element is passed verbatim, no quoting needed for spaces or special chars.

---

## CLAUDE_ENV_FILE

Available in `SessionStart`, `Setup`, `CwdChanged`, and `FileChanged` hooks. Write `export VAR=value` lines to this path to persist variables into subsequent Bash commands for the session.

```bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
fi
```

Use append (`>>`) to preserve variables set by other hooks.

---

## Common gotchas

**Stop hook continuation cap**: both `decision: "block"` and `additionalContext` go through the `stop_hook_active` input and the 8-consecutive-continuation cap. Read `stop_hook_active` from stdin and exit 0 when it is `true` to let Claude stop cleanly.

**Exit 1 does not block**: without valid JSON output, only exit 2 blocks a PreToolUse call or UserPromptSubmit. Exit 1 is non-blocking: the action proceeds. A hook can also block with exit 0 plus a JSON decision such as `permissionDecision: "deny"`. A script path that does not exist fails with a code like 127, which is also non-blocking, so a mistyped path silently disables a policy gate.

**asyncRewake vs async**: `asyncRewake: true` runs the hook in the background AND wakes the session when the process exits with code 2, even if Claude is idle. Use when a long-running background check needs to report a failure mid-session.

**SessionEnd budget**: Total budget is 1.5s. Setting `timeout: 30` on a hook raises the budget to 30s (max 60s), but a hook without its own `timeout` keeps the 1.5s default. Plugin hook timeouts do not raise the budget. `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000` overrides the budget and, since v2.1.268, also sets the timeout of hooks without their own.

**MessageDisplay batching**: Fires multiple times per message (once per batch of lines) in interactive mode, once after the full message in `-p`/Agent SDK mode. `final: true` marks the last batch; don't rely on a non-empty `delta` as the end signal.

**WorktreeCreate replaces git entirely**: The hook must handle the full worktree setup. `.worktreeinclude` is not processed. Copy `.env` and other local files inside the hook.

**if field on non-tool events**: Adding `if` to `SessionStart`, `Stop`, or any non-tool event silently prevents the hook from running at all.

**Multiple PreToolUse hooks with updatedInput**: all matching hooks run in parallel. Conflicting decisions resolve as `deny > defer > ask > allow`, but the documentation does not define which `updatedInput` wins when several hooks rewrite the same call. Avoid having two hooks on the same matcher both returning `updatedInput`.

**PermissionRequest does not prevent via exit 2**: Use `hookSpecificOutput.decision.behavior: "deny"` in JSON output. Exit 2 is not honored on this event, and `agent` hooks are skipped on it since v2.1.280.

**Duplicate handlers**: the same handler defined in several settings files runs once. A plugin's or a skill's copy of the same handler stays separate.

**Prompt hooks on PermissionDenied**: Output is discarded. The only field this event reads is `hookSpecificOutput.retry`, which prompt and agent hooks cannot set. Use a command hook for retry signals.

**Hooks without a controlling terminal**: Since v2.1.139, hooks run without `/dev/tty`. Use `terminalSequence` in JSON output to emit desktop notifications or window titles instead of writing escape sequences directly.

**UserPromptSubmit default timeout**: 30s, not 600s. A stuck hook here blocks all user input. Set an explicit `timeout` if you need more time.
