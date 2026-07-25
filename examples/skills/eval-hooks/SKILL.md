---
name: eval-hooks
description: "Audit Claude Code hooks defined in settings.json files for validity, performance safety, and correctness. Resolves each command against the filesystem, checks exit-code strategy for blocking hooks, flags missing timeouts, and reviews interactive vs async patterns. Use when setting up hooks for the first time, debugging a hook that never fires or hangs the agent, or doing a periodic hooks hygiene pass."
allowed-tools: Read Glob Bash Edit
effort: medium
argument-hint: "[path to settings file or dir, default: all settings files]"
---

# Hooks Evaluator

Discover all Claude Code hooks across every settings file in scope, validate each one against the filesystem and hook semantics, then run an interactive session to confirm or improve them.

The goal is not just to score; it is to leave every hook working, correctly scoped, and safe to run.

## When to Use

- First time adding hooks (validate before committing)
- A hook never fires, or fires on every tool call
- The agent hangs noticeably before executing a tool
- A PreToolUse hook is supposed to block but doesn't
- After copying hooks from another project or machine
- Periodic hygiene: "are all these hooks still doing something useful?"

## Key Concepts

### Event types

| Event | When it fires | Can block? (exit 2) |
|---|---|---|
| `PreToolUse` | Before any tool call | Yes |
| `PermissionRequest` | When a permission dialog appears | Yes |
| `PostToolUse` | After tool completes successfully | No (shows stderr to Claude) |
| `PostToolUseFailure` | After a tool fails | No |
| `PostToolBatch` | After a full batch of parallel tool calls resolves | Yes (stops agentic loop) |
| `UserPromptSubmit` | When user submits a prompt | Yes |
| `UserPromptExpansion` | When a slash command expands | Yes |
| `Stop` | When Claude finishes responding | Yes (continues the turn) |
| `SubagentStop` | When a subagent finishes | Yes (continues the subagent) |
| `TeammateIdle` | When an agent team teammate goes idle | Yes |
| `TaskCreated` | When a task is being created | Yes |
| `TaskCompleted` | When a task is being marked as completed | Yes |
| `PreCompact` | Before context compaction | Yes |
| `ConfigChange` | When a configuration file changes | Yes (except policy_settings) |
| `PermissionDenied` | When auto-mode classifier denies a tool call | No |
| `SessionStart` | When a session starts or resumes | No |
| `Setup` | On --init-only or -p --init/--maintenance | No |
| `StopFailure` | When the turn ends due to API error | No |
| `Notification` | When Claude sends a notification | No |
| `MessageDisplay` | While assistant message streams | No |
| `SubagentStart` | When a subagent is spawned | No |
| `InstructionsLoaded` | When a CLAUDE.md or rules file is loaded | No |
| `CwdChanged` | When working directory changes | No |
| `FileChanged` | When a watched file changes on disk | No |
| `WorktreeCreate` | When a worktree is created (replaces default git behavior) | Yes (any non-zero fails) |
| `WorktreeRemove` | When a worktree is removed | No |
| `PostCompact` | After compaction completes | No |
| `SessionEnd` | When a session terminates | No |
| `ElicitationResult` | After user responds to MCP elicitation | Yes |
| `Elicitation` | When MCP server requests user input | Yes |

**Events that do NOT support matchers**: UserPromptSubmit, PostToolBatch, Stop, TeammateIdle, TaskCreated, TaskCompleted, WorktreeCreate, WorktreeRemove, CwdChanged, MessageDisplay.

### Exit codes (command hooks)

- **Exit 0**: success. Claude Code parses stdout for JSON output. JSON is only processed on exit 0.
- **Exit 2**: blocking error. Stderr is fed to Claude as error message. The tool call or action is prevented on events that support blocking.
- **Any other non-zero**: non-blocking error. Shows a hook error notice in the transcript (first line of stderr). Execution continues.

> Warning: only exit code 2 blocks. Exit code 1 is a non-blocking error and proceeds with the action. Use exit 2 for policy enforcement.

### Timeout defaults

| Hook type | Default timeout |
|---|---|
| `command`, `http`, `mcp_tool` | 600s |
| `UserPromptSubmit` (command/http/mcp_tool) | 30s |
| `MessageDisplay` (command/http/mcp_tool) | 10s |
| `prompt` | 30s |
| `agent` | 60s |
| `SessionEnd` | 1.5s (overall budget) |

### Hook types

- **command**: shell command, receives JSON on stdin, communicates via exit codes and stdout
- **http**: POST request to a URL, same JSON, response body as output
- **mcp_tool**: calls a tool on a connected MCP server
- **prompt**: sends prompt to a Claude model, returns `{ "ok": true/false }` decision
- **agent**: spawns a subagent with tool access (experimental)

### Matcher patterns

For `PreToolUse`, `PostToolUse`, and related tool events, the matcher filters on tool name:
- Letters/digits/underscores/pipe only: exact match or pipe-separated list (`Edit|Write`)
- Contains any other character: treated as JavaScript regex (`mcp__memory__.*`)
- `"*"`, `""`, or absent: matches all tool calls

Other events match different fields (e.g. `SessionStart` matches on `source: startup|resume|clear|compact`). For the complete per-event matcher field reference, see `guide/core/hooks-events-reference.md`.

### The `if` field (v2.1.85+)

The `if` field narrows a handler further by tool name AND arguments together, using [permission rule syntax](../../../guide/core/tools-reference.md#permission-rule-formats). Evaluated per handler (not per matcher group), so the process only spawns when both match.

```json
{
  "matcher": "Bash",
  "hooks": [
    { "type": "command", "if": "Bash(git *)", "command": "my-git-policy.sh" }
  ]
}
```

Flag: `if` only works on tool events (PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, PermissionDenied). Adding it to any other event type prevents the hook from running.

---

## Settings Files Scanned

| File | Scope | Committed? |
|---|---|---|
| `~/.claude/settings.json` | Global user | No |
| `~/.claude/settings.local.json` | Global local | No |
| `.claude/settings.json` | Project | Yes |
| `.claude/settings.local.json` | Project local | No |
| Plugin `hooks/hooks.json` | Per plugin | Yes (in plugin) |
| Skill/agent frontmatter `hooks:` | Per component | Yes |

If an argument is provided (e.g. `/eval-hooks .claude/settings.local.json`), audit only that file. Otherwise scan the four standard locations.

---

## Scoring Criteria (10 pts per hook)

| # | Criterion | Max | What is checked |
|---|-----------|-----|-----------------|
| 1 | **valid event type** | 1 | Type is one of the 30 known event types listed above |
| 2 | **matcher** | 2 | Absent for events that don't support matchers (1pt); not an overly broad pattern with a heavy command (1pt) |
| 3 | **command** | 3 | Non-empty (1pt); referenced script or binary resolves on disk (1pt); script is executable (chmod +x) (1pt) |
| 4 | **timeout** | 2 | Blocking hooks (PreToolUse, UserPromptSubmit) have explicit `timeout` field (1pt); value is ≤ 30s for interactive hooks (1pt) |
| 5 | **blocking awareness** | 2 | Blocking hooks: exit 2 used (not exit 1) for policy enforcement (1pt); no interactive commands that would hang (1pt) |
| Bonus | **hygiene** | +1 | No duplicate (event + matcher + command) combination found across all scanned files |

**Thresholds:**
- ✅ Good: ≥8/10 (≥80%)
- ⚠️ Needs work: 5-7/10 (50-79%)
- ❌ Fix: <5/10 (<50%)

**Non-blocking events** (PostToolUse, SessionEnd, Notification, etc.): skip criterion 5 (blocking awareness). Score on 8 pts max. Flag with 🔵.

---

## Execution Instructions

### Step 1: Discovery

Parse each settings file found:

```bash
ls ~/.claude/settings.json ~/.claude/settings.local.json \
   .claude/settings.json .claude/settings.local.json 2>/dev/null
```

For each file that exists, extract the `hooks` object. Parse every entry across all event types.

Build a flat list of hook records:
- `source_file`: which settings file it came from
- `event_type`: e.g. `PreToolUse`
- `matcher`: string or absent
- `type`: command / http / mcp_tool / prompt / agent
- `command`: shell command string (command hooks only)
- `timeout`: seconds or absent (note: JSON uses seconds, not ms)
- `async`: boolean

If no hooks are found in any file, report it and stop.

### Step 2: Resolve commands (command hooks only)

For each command hook, resolve the first token to a binary or script:

```bash
CMD=$(echo "$command" | awk '{print $1}')
CMD="${CMD/#\~/$HOME}"
which "$CMD" 2>/dev/null || test -f "$CMD" && echo "found" || echo "not found"
test -x "$CMD" && echo "executable" || echo "not executable"
```

Flag:
- **Not found**: script or binary does not exist at that path
- **Not executable**: file exists but `chmod +x` was never run (most common source of silent failures)
- **Tilde path**: command starts with `~` (usually safe since hooks run via shell, but absolute paths are preferred)
- **Relative path**: path does not start with `/` or `~` (resolves from working directory, which may vary)

Also flag patterns that indicate the hook will hang:
- `read`, `fzf`, `gum`, any interactive TUI command: flag as ❌ (hangs the agent, hooks run without a controlling terminal since v2.1.139)

### Step 3: Check blocking hooks for exit code strategy

For PreToolUse, UserPromptSubmit, UserPromptExpansion, Stop, SubagentStop hooks whose command is a local script:

1. Read the script file
2. Check for `exit 2` statements vs `exit 1` or generic `exit $?`
3. Classify:
   - **Uses exit 2 for blocking**: ✅ correct pattern
   - **Uses exit 1 for blocking**: ⚠️ exit 1 is non-blocking, action will proceed
   - **No explicit exit**: the last command's exit code propagates, may not block as intended
   - **Always exits 0**: will never block (may be intentional for context-only hooks)

Flag any PreToolUse script that contains slow operations (`curl`, `sleep`, network calls) without a surrounding timeout guard.

### Step 4: Check for duplicates

Compare all hook records by (event_type + matcher + command). Report exact duplicates across files: they fire twice and consume double the latency.

Also flag: a matcher field on an event that doesn't support matchers (silently ignored by Claude Code).

### Step 5: Interactive review (core of the skill)

Process hooks **one by one**. Do not batch and skip the interaction.

**For each hook:**

Show:
```
Hook: PreToolUse → Bash [~/.claude/settings.json]
type: command
command: /Users/me/.claude/hooks/confirm-git-push.sh
timeout: (none, default 600s)
Script: found (executable ✅)
Exit strategy: uses exit 2 ✅
```

Ask three questions:
1. "Does this hook fire at the right time and scope? (y = yes / n = adjust matcher or event)"
2. "Is the command still working correctly? (y / broken / unsure)"
3. "Anything to change (matcher, command, timeout, remove it)? (describe or skip)"

**For lifecycle hooks (no matcher):**

Show:
```
Hook: SessionEnd [~/.claude/settings.local.json]
type: command
command: ~/.claude/hooks/session-summary.sh
timeout: (none, default 1.5s for SessionEnd, very short!)
Script: found (executable ✅)
```

Ask:
1. "Does this hook still serve a useful purpose? (y / n)"
2. "Is the command working within the timeout? (y / broken / unsure)"

**If the user provides changes during the interaction**: apply them using Edit, confirm each change, then move to the next hook.

### Step 6: Output report

After all hooks are reviewed:

```
# Hooks Audit: [project or global]
Date: [today] | Scanned: N hooks across M settings files

## Summary

| Status | Count |
|--------|-------|
| ✅ Good (≥80%) | N |
| ⚠️ Needs work (50-79%) | N |
| ❌ Fix (<50%) | N |
| 🔵 Non-blocking event | N |
| ✅ User confirmed useful | N |
| ⚠️ User flagged for update | N |
| 🗑️ User marked as stale | N |

---

## Per-Hook Results

### PreToolUse → Bash [~/.claude/settings.json] (7/10 ⚠️)

type: command
command: `~/.claude/hooks/confirm-git-push.sh`
timeout: (none)

| Criterion | Score | Notes |
|-----------|-------|-------|
| valid event type | ✅ 1/1 | PreToolUse |
| matcher | ✅ 2/2 | scoped to Bash |
| command | ✅ 3/3 | found, executable, absolute path |
| timeout | ❌ 0/2 | no timeout (UserPromptSubmit default is 30s, others 600s) |
| blocking awareness | ✅ 2/2 | exit 2 used for blocking ✅ |

**Priority fixes:**
1. Add `"timeout": 10` to cap blocking time
2. Verify script doesn't block on network calls without internal timeout

User feedback: ✅ scope correct
Content: timeout added ✅

---

### PostToolUse → Edit|Write [~/.claude/settings.json] (10/10 ✅) 🔵

type: command
command: `~/.claude/hooks/anti-ai-markers.sh`
timeout: 2

Non-blocking event: exit 2 shows stderr to Claude but doesn't prevent the action. All criteria pass. User confirmed still useful.

---
```

### Step 7: Fix Summary

```
## What Changed This Session

confirm-git-push.sh hook:
  - Added timeout: 10

session-summary.sh hook:
  - User confirmed useful, no changes

rtk-baseline.sh hook:
  - User flagged as stale (awaiting explicit deletion confirmation)

---
N hooks audited · N edits applied · N flagged as stale · N duplicates found
```

For any hook the user marked as stale: ask for explicit confirmation before removing it from the settings file. Never delete without a clear "yes, remove it".

---

## Edge Cases

- **Command is a one-liner inline** (e.g. `rtk hook claude`): skip script-level checks, verify the binary `rtk` exists in PATH
- **Command uses `bash -c '...'` inline**: parse the inner script string for interactive commands and exit code logic
- **`exit 1` in a PreToolUse hook**: flag as ⚠️ (exit 1 is a non-blocking error, the tool call will proceed even if the intent was to block)
- **Same hook in both global and project settings**: not a duplicate (each fires in its own scope), but note both locations in the report
- **`timeout: 0`**: flag as likely invalid (may be treated as no timeout)
- **Unknown event type** (e.g. `PreToolCall` typo): flag as ❌, report exact string, suggest the correct name
- **Script not executable**: hook fails silently on most systems, suggest `chmod +x` immediately
- **Matcher on non-matcher event** (e.g. `UserPromptSubmit` with a matcher): flag as silently ignored, suggest removing it
- **`async: true` hook returning `decision: "block"`**: flag as ⚠️ (async hooks cannot block, decision fields have no effect)
- **`asyncRewake: true` hook**: implies `async: true` but additionally wakes Claude when the background process exits with code 2. The hook's stderr (or stdout if stderr is empty) is shown to Claude as a system reminder. Flag hooks that need to signal background failures back to Claude but use `async` instead of `asyncRewake`
- **`prompt` or `agent` type hook**: these don't have a command to resolve; check that the `prompt` field is present and non-empty
- **SessionEnd hooks**: the default timeout budget is 1.5s. Even if a hook declares `timeout: 30`, it may be cut off. Flag any SessionEnd hook without an explicit timeout, and warn that heavy work here risks being killed
- **Hooks not firing as expected**: advise using `/hooks` menu in Claude Code to verify configuration, and checking `~/.claude/logs/` or running with `--debug`
- **`PermissionRequest` hook in `-p` mode**: these hooks don't fire in non-interactive mode. Flag and suggest migrating to `PreToolUse` instead
- **`if` field on non-tool event**: hook never runs silently. Flag and suggest removing `if` or changing the event type
- **Multiple PreToolUse hooks with `updatedInput`**: when several hooks modify tool input, the last to finish wins (execution is parallel, order is non-deterministic). Flag when more than one PreToolUse hook on the same matcher returns `updatedInput`
- **Stop hook without `stop_hook_active` check**: a Stop hook that always blocks will hit the 8-consecutive-blocks cap and be overridden. Check that the script reads the `stop_hook_active` field from stdin JSON and exits 0 when it is `true`, to let Claude stop once it has already continued
- **`$CLAUDE_PROJECT_DIR` in command**: preferred over hardcoded absolute paths for project scripts. Flag any command containing an absolute path that looks project-local and suggest replacing with `${CLAUDE_PROJECT_DIR}/...`
