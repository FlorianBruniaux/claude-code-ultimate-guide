---
name: eval-hooks
description: "Audit Claude Code and Codex hooks for validity, safety, and correctness across settings.json, hooks.json, config.toml, plugin, and skill or agent frontmatter hooks. Resolves each command, checks event names, handler types, matchers, exit-code and JSON decision strategy, and timeouts against each host's documented rules, then reviews hooks one by one. Use when setting up hooks, debugging a hook that never fires, never blocks, or hangs the agent, or doing a periodic hooks hygiene pass. Not for writing a new hook from scratch."
allowed-tools: Read Glob Bash Edit
effort: medium
argument-hint: "[claude | codex | path to a hooks or settings file; default: all locations]"
---

# Hooks Evaluator

Discover every Claude Code and Codex hook in scope, validate each one against the filesystem and the host's documented hook semantics, then run an interactive session to confirm or improve them.

The goal is not just to score; it is to leave every hook working, correctly scoped, and safe to run.

Sources of truth: the official Claude Code hooks reference (https://code.claude.com/docs/en/hooks) and the Codex hooks documentation (https://developers.openai.com/codex/hooks). When a rule below and the live documentation disagree, the documentation wins; report the disagreement instead of scoring against stale text.

## When to Use

- First time adding hooks (validate before committing)
- A hook never fires, or fires on every tool call
- The agent hangs noticeably before executing a tool
- A policy hook is supposed to block but doesn't
- After copying hooks from another project, machine, or host
- Periodic hygiene: "are all these hooks still doing something useful?"

## Scope

| Argument | Audit |
|---|---|
| none | Every Claude Code and Codex location listed below that exists |
| `claude` or `codex` | That host only |
| a file path | That file only (settings JSON, `hooks.json`, `config.toml`, skill or agent file) |
| `audit-only`, or the user asks for no changes | Steps 1-4 and 6 only: list each proposed change instead of asking or editing, and omit the user-feedback lines from the report |

Audit each host with its own rules. Never score a Codex hook against Claude Code semantics or the reverse.

When a `ctxharness doctor --format json` report generated during this task is available, reconcile against it: every hook-layer finding it reports must appear in the audit, and every extra finding needs `file:line` evidence.

---

## Claude Code: Key Concepts

### Event types (33)

| Event | When it fires | Exit 2 effect |
|---|---|---|
| `SessionStart` | Session begins or resumes | Stderr to user only |
| `Setup` | `--init-only`, or `--init` / `--maintenance` in `-p` mode | Ignored |
| `UserPromptSubmit` | Prompt submitted, before processing | Blocks and erases the prompt |
| `UserPromptExpansion` | A typed command expands into a prompt | Blocks the expansion |
| `PreToolUse` | Before a tool call executes | Blocks the tool call |
| `PermissionRequest` | A tool call needs a permission decision | **Not honored**: deny through the JSON `decision` object |
| `PermissionDenied` | Auto mode denies a tool call | Ignored (only `hookSpecificOutput.retry` is read) |
| `PostToolUse` | After a tool call succeeds | Stderr to Claude; the tool already ran |
| `PostToolUseFailure` | After a tool call fails | Stderr to Claude |
| `PostToolBatch` | After a full batch of parallel tool calls | Stops the agentic loop |
| `Notification` | Claude Code sends a notification | Ignored |
| `MessageDisplay` | While assistant text is displayed | Original text displayed |
| `SubagentStart` | A subagent is spawned | Stderr to user only |
| `SubagentStop` | A subagent finishes | Prevents the subagent from stopping |
| `TaskCreated` | A task is being created | Rolls back the creation |
| `TaskCompleted` | A task is being marked completed | Prevents completion |
| `Stop` | Claude finishes responding | Prevents stopping, continues the turn |
| `StopFailure` | The turn ends on an API error | Ignored (except `terminalSequence`) |
| `TeammateIdle` | An agent team teammate is about to go idle | Keeps the teammate working |
| `InstructionsLoaded` | A CLAUDE.md or `.claude/rules/*.md` file loads | Ignored |
| `ConfigChange` | A configuration file changes mid-session | Blocks the change (except `policy_settings`) |
| `CwdChanged` | The working directory changes | Stderr to user only |
| `DirectoryAdded` | A directory is added via `/add-dir` or SDK `register_repo_root` | Stderr to debug log; already added |
| `FileChanged` | A watched file changes on disk | Stderr to user only |
| `WorktreeCreate` | A worktree is being created | Any non-zero exit fails creation |
| `WorktreeRemove` | A worktree is being removed | Any non-zero exit fails removal if the directory remains |
| `PreCompact` | Before compaction | Blocks compaction |
| `PostCompact` | After compaction | Stderr to user only |
| `PreModelSwitch` | Before a requested model switch | Blocks the switch |
| `PostModelSwitch` | After the session model changes | Stderr to user only |
| `Elicitation` | An MCP server requests user input | Denies the elicitation |
| `ElicitationResult` | After the user answers an elicitation | Blocks the response (becomes decline) |
| `SessionEnd` | Session terminates | Stderr to user only |

### Exit codes and JSON output

- **Exit 2** blocks on the events whose row says so. No JSON can override it, not even `permissionDecision: "allow"`.
- **JSON is read on every exit code**, not only 0. For events with a standard decision model, a valid JSON decision takes effect on exit 0 or any other non-2 code: `hookSpecificOutput.permissionDecision: "deny"` (PreToolUse, PreModelSwitch), `hookSpecificOutput.decision.behavior: "deny"` (PermissionRequest), top-level `decision: "block"` (UserPromptSubmit, UserPromptExpansion, PostToolUse, PostToolUseFailure, PostToolBatch, Stop, SubagentStop, ConfigChange, PreCompact, TaskCreated, PreModelSwitch).
- **Any other non-zero code without valid JSON** is a non-blocking error: the action proceeds and the transcript shows the first stderr line. A missing or non-executable script exits with a code like 127 and lands in this bucket, so a mistyped path silently disables a policy gate.
- **Exit 0 stdout** becomes context only on `UserPromptSubmit`, `UserPromptExpansion`, `SessionStart`, and `PostModelSwitch`; elsewhere it goes to the debug log.

A policy hook is correctly built when it uses **either** exit 2 **or** a JSON decision supported by its event. Exit 1 alone is the defect.

### Timeout defaults (seconds)

| Handler | Default |
|---|---|
| `command`, `http`, `mcp_tool` | 600 |
| same, on `UserPromptSubmit`, `PreModelSwitch`, `PostModelSwitch` | 30 |
| same, on `MessageDisplay` | 10 |
| `prompt` | 30 |
| `agent` | 60 |
| `SessionEnd` | 1.5 total budget; a per-hook `timeout` raises it to the highest configured value, up to 60. Plugin hook timeouts do not raise it. `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` overrides it |

A timed-out `command`, `http`, or `mcp_tool` hook on `PreToolUse` does **not** block the tool call; on `PreModelSwitch` it blocks the switch. `timeout` is not enforced on a running `async: true` hook; it is enforced with `asyncRewake`.

### Handler types and where they are allowed

| Handler type | Allowed on |
|---|---|
| `command`, `mcp_tool` | Every event |
| `http` | Every event except `SessionStart` and `Setup` |
| `prompt` | `PermissionDenied`, `PostToolBatch`, `PostToolUse`, `PostToolUseFailure`, `PreToolUse`, `Stop`, `SubagentStop`, `TaskCompleted`, `TaskCreated`, `TeammateIdle`, `UserPromptExpansion`, `UserPromptSubmit`, `PermissionRequest` |
| `agent` (experimental) | Same as `prompt`, except `PermissionRequest`, where an agent hook is skipped |

On `PermissionDenied`, prompt and agent hooks run but their output is discarded.

### Handler fields

| Field | Applies to | Notes |
|---|---|---|
| `type` | all | `command`, `http`, `mcp_tool`, `prompt`, `agent` |
| `if` | all | One permission rule, such as `Bash(git *)`. Evaluated only on `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`; on any other event the hook never runs. Best-effort filter, not an enforcement mechanism |
| `timeout` | all | Seconds |
| `statusMessage` | all | Spinner text |
| `once` | all | Honored only in skill frontmatter; ignored in settings files and agent frontmatter |
| `command` | command | Shell string, or the executable when `args` is set |
| `args` | command | Exec form: no shell, each element one argument. Preferred when referencing `${CLAUDE_PROJECT_DIR}` or `${CLAUDE_PLUGIN_ROOT}` |
| `shell` | command | `bash` or `powershell`; ignored when `args` is set |
| `async` | command | Runs in the background; cannot block or decide |
| `asyncRewake` | command | Background, and wakes Claude when the process exits 2 |
| `url`, `headers`, `allowedEnvVars` | http | Blocks only through a 2xx JSON body; status codes alone never block |
| `server`, `tool`, `input` | mcp_tool | Uses an already connected server |
| `prompt`, `model` | prompt, agent | `$ARGUMENTS` receives the hook input |

### Matchers

| Matcher value | Evaluated as |
|---|---|
| `"*"`, `""`, or omitted | Match all |
| Only letters, digits, `_`, `-`, spaces, `,`, `\|` | Exact string, or a list separated by `\|` or `,` (hyphens need v2.1.195+) |
| Any other character | Unanchored JavaScript regex (`Edit.*` also matches `NotebookEdit`; anchor with `^...$`) |

`FileChanged` and `StopFailure` use a narrower exact set (letters, digits, `_`, `|`). Each event filters a different field:

| Event | Matcher filters |
|---|---|
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` | tool name (`Bash`, `Edit\|Write`, `mcp__server__.*`) |
| `SessionStart` | `startup`, `resume`, `clear`, `compact`, `fork` |
| `Setup` | `init`, `maintenance` |
| `SessionEnd` | `clear`, `resume`, `logout`, `prompt_input_exit`, `other` |
| `Notification` | notification type |
| `SubagentStart`, `SubagentStop` | agent type |
| `PreCompact`, `PostCompact` | `manual`, `auto` |
| `PreModelSwitch`, `PostModelSwitch` | canonical target model name |
| `ConfigChange` | configuration source |
| `DirectoryAdded` | `slash_command`, `register_repo_root` |
| `FileChanged` | literal filenames to watch |
| `StopFailure` | error type |
| `InstructionsLoaded` | load reason |
| `UserPromptExpansion` | command name |
| `Elicitation`, `ElicitationResult` | MCP server name |

**No matcher support** (a matcher is silently ignored): `UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `CwdChanged`, `MessageDisplay`.

### Execution model

- All matching hooks run **in parallel**.
- The same handler defined in more than one settings file runs **once**. A plugin's or a skill's copy of the same handler stays separate.
- `PermissionRequest` hooks also run in sessions that cannot show a prompt, such as background subagents in `-p` mode; if no hook decides, the call is denied.
- Several `PreToolUse` decisions resolve as `deny > defer > ask > allow`. The documentation does not define which `updatedInput` wins when several hooks rewrite the same call.
- `Stop` and `SubagentStop` continuations, through `decision: "block"` or `additionalContext`, are bounded by the `stop_hook_active` input and an 8-consecutive-continuation cap.
- Command hooks run without a controlling terminal: interactive commands (`read`, `fzf`, `gum`, any TUI) cannot get input. Use `terminalSequence` in JSON output for notifications.

---

## Claude Code: Locations Scanned

| Location | Scope | Notes |
|---|---|---|
| Managed policy settings | Organization | Cannot be disabled by user, project, or local `disableAllHooks` |
| `~/.claude/settings.json` | User | Not read by cloud sessions |
| `.claude/settings.json` | Project, committed | |
| `.claude/settings.local.json` | Project, personal | |
| Plugin `hooks/hooks.json` | While the plugin is enabled | |
| Skill frontmatter `hooks:` | Rest of the session once the skill is invoked | `once: true` honored here only |
| Subagent frontmatter `hooks:` | While that subagent runs | `Stop` becomes `SubagentStop`. Project subagent hooks run only after workspace trust is accepted, including in `-p` |

`~/.claude/settings.local.json` is **not** a documented settings location. If it exists, report it as undocumented and do not score its hooks as active.

Also record, from the effective settings:

- `disableAllHooks: true` disables every non-managed hook; only a managed-level value disables managed hooks.
- `allowManagedHooksOnly` blocks user, project, local, and plugin hooks (plugins force-enabled in managed `enabledPlugins` are exempt).
- `allowedHttpHookUrls` and `httpHookAllowedEnvVars` restrict HTTP hooks from every source.
- Interactive sessions hold back every settings-file hook until workspace trust is accepted; `-p` and SDK sessions treat the folder as trusted.

---

## Codex: Key Concepts

### Locations

| Location | Notes |
|---|---|
| `~/.codex/hooks.json` | User |
| `~/.codex/config.toml` inline `[hooks]` | User |
| `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml` | Loaded only when the project `.codex/` layer is trusted |
| Plugin `hooks/hooks.json`, or a `hooks` entry in `.codex-plugin/plugin.json` | Manifest paths must stay inside the plugin root |
| Managed `requirements.toml` `[hooks]` | Trusted by policy; `allow_managed_hooks_only = true` skips user, project, session, and plugin hooks |

Every source loads; higher layers do not replace lower ones. A layer holding both `hooks.json` and inline `[hooks]` is merged with a startup warning: flag it and recommend one representation per layer. `[features] hooks = false` turns hooks off (`codex_hooks` is a deprecated alias).

### Trust review

Every non-managed hook, plugin hooks included, must be reviewed and trusted in `/hooks` before it runs. Trust is recorded against the hook's current hash, so an edited hook is skipped until trusted again. When auditing, report that a changed hook needs review; do not assume it runs. The `/hooks` browser is the authoritative view of trust. Current Codex builds also persist it under `[hooks.state]` in `config.toml`, which is undocumented: report what you observe there without printing hash values, and never treat `[hooks.state]` as an event. `--dangerously-bypass-hook-trust` bypasses the check for one invocation only: flag any automation that relies on it.

### Events (12) and matchers

| Event | Matcher filters |
|---|---|
| `PreToolUse`, `PostToolUse`, `PermissionRequest` | tool name (`Bash`, `apply_patch`, MCP names; `Edit` or `Write` also match `apply_patch`) |
| `SessionStart` | `startup`, `resume`, `clear`, `compact` |
| `SessionEnd` | currently only `other` |
| `PreCompact`, `PostCompact` | `manual`, `auto` |
| `SubagentStart`, `SubagentStop` | subagent type |
| `UserPromptSubmit`, `Stop`, `Interrupt` | not supported (matcher ignored) |

Codex matchers are regex strings. `Interrupt` and `SessionEnd` do not run for subagents.

### Handlers and output

- Only `command` and `mcp_tool` handlers run. `prompt` and `agent` handlers are parsed and skipped: flag them as dead configuration.
- `timeout` is in seconds, default 600. `SessionEnd` and `Interrupt` default to 1 and allow at most 3.
- Optional fields: `statusMessage`, `async`, `additionalContextLimit` (default 2,500 tokens; `0` passes everything and can flood the context), `commandWindows` / `command_windows`.
- Commands run with the session `cwd`. For repo-local scripts, resolve from the git root rather than a relative `.codex/hooks/...` path.
- `PreToolUse` ignores plain-text stdout. It blocks with `permissionDecision: "deny"`, legacy `decision: "block"`, or exit 2 with the reason on stderr. It rewrites a call with `permissionDecision: "allow"` plus `updatedInput` (a string `command` for `Bash` and `apply_patch`, the replacement arguments for MCP tools), the same shape Claude Code uses. `permissionDecision: "ask"`, `continue`, `stopReason`, and `suppressOutput` are not supported there: Codex marks the hook run as failed and **continues the tool call**. Flag any Codex policy hook that relies on them.
- Background (`async`) hooks cannot block, approve, or rewrite; at most eight run concurrently; `SessionEnd` always runs synchronously.
- `SessionEnd` does not support MCP tool hooks.

---

## Scoring Criteria (10 pts per hook)

| # | Criterion | Max | What is checked |
|---|-----------|-----|-----------------|
| 1 | **event and handler type** | 1 | The event exists for this host, and the handler type is allowed on it (a Claude `agent` hook on `PermissionRequest` or a Codex `prompt` hook scores 0) |
| 2 | **matcher** | 2 | No matcher on an event without matcher support, or a matcher using that event's documented values (1); not a match-all or broad regex on a tool event paired with a slow command (1) |
| 3 | **command** | 3 | Non-empty (1); the script or binary resolves on disk, after substituting `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, or the git root (1); the script is executable, or it is passed to an interpreter (`bash script.sh`, `python3 script.py`) or run in exec form with a resolvable executable (1) |
| 4 | **timeout** | 2 | The effective timeout (explicit or documented default) fits the event: interactive-path hooks (`PreToolUse`, `PermissionRequest`, `UserPromptSubmit`, `PreModelSwitch`, `Stop`) under 30 s or backed by an internal timeout guard (1); no explicit value that exceeds a documented cap or budget, such as a Codex `SessionEnd` above 3 or a Claude `SessionEnd` above 60 (1) |
| 5 | **blocking awareness** | 2 | For a hook meant to enforce a policy: blocks through exit 2 or a JSON decision supported by the event and host, not exit 1 (1); no interactive command, no reliance on a timeout to block `PreToolUse`, no unsupported Codex output field (1) |
| Bonus | **hygiene** | +1 | No redundant copy of the same handler within one scope, and `$CLAUDE_PROJECT_DIR` or a git-root path instead of a hardcoded project-local absolute path |

**Thresholds:**
- ✅ Good: ≥8/10 (≥80%)
- ⚠️ Needs work: 5-7/10 (50-79%)
- ❌ Fix: <5/10 (<50%)

**Observational hooks** (logging, context injection, formatting, events that cannot block): skip criterion 5 and score on 8 pts max. Flag with 🔵. Decide "meant to enforce a policy" from the script and the user's answer, not from the event name alone.

---

## Execution Instructions

### Step 1: Discovery

List the locations that exist for each host in scope. Claude Code:

```bash
ls ~/.claude/settings.json .claude/settings.json .claude/settings.local.json 2>/dev/null
ls ~/.claude/settings.local.json 2>/dev/null && echo "undocumented location"
```

Codex:

```bash
ls ~/.codex/hooks.json ~/.codex/config.toml .codex/hooks.json .codex/config.toml 2>/dev/null
```

Plugins are part of the default scope because their hooks run while the plugin is enabled. For Claude Code, take enabled plugins from `enabledPlugins` in the effective settings and the installed version of each from `~/.claude/plugins/installed_plugins.json`; the plugin cache may hold several versions and temporary checkouts, so read only the installed one. List every plugin hook; score them only when the user asks, since the user does not own that code. For Codex, read plugin `hooks/hooks.json` or the `hooks` entry of `.codex-plugin/plugin.json`.

Also read `hooks:` blocks in `.claude/skills/**/SKILL.md` and `.claude/agents/**/*.md`, following symlinked skill directories. Managed settings and `requirements.toml` are read-only for this audit: report them, never edit them.

Note which hooks an external installer owns (for example a tool with an `install-hooks` or `upgrade` command). Such an installer can restore its entries after a manual cleanup, so recommend a change through that tool, or record the drift risk next to the proposal.

Build a flat list of hook records:
- `host`: `claude` or `codex`
- `source_file` and `scope`
- `event_type`, `matcher` (or absent)
- `type` and its type-specific fields (`command`, `args`, `url`, `server`/`tool`, `prompt`)
- `timeout` (seconds, explicit or default), `async`, `asyncRewake`, `if`, `once`

If no hooks are found in any location, report it and stop.

Done when: every existing location is listed with its host and scope, and each hook has a record (or the audit stopped with "no hooks found").

### Step 2: Resolve commands (command hooks only)

Split a shell-form `command` into shell words before resolving it. A first-word split with `awk` is wrong: it keeps quotes and splits `"$CLAUDE_PROJECT_DIR"/.claude/hooks/x.sh` into two words. Use a shell-word parser:

```bash
python3 - "$command" "$PROJECT_ROOT" <<'EOF'
import os, shlex, shutil, sys
cmd, root = sys.argv[1], sys.argv[2]
words = shlex.split(cmd.split(';')[-1].split('&&')[-1])
words = [os.path.expanduser(w.replace('${CLAUDE_PROJECT_DIR}', root).replace('$CLAUDE_PROJECT_DIR', root)) for w in words]
while words and (words[0] == 'env' or '=' in words[0].split('/')[0]):
    words.pop(0)  # skip env and VAR=value prefixes
exe = words[0] if words else ''
path = exe if '/' in exe else (shutil.which(exe) or '')
print('executable', exe, 'found' if path and os.path.exists(path) else 'not found', 'x' if path and os.access(path, os.X_OK) else '-')
if os.path.basename(exe) in {'bash', 'sh', 'zsh', 'node', 'python3', 'python', 'deno', 'bun'}:
    script = next((w for w in words[1:] if not w.startswith('-')), '')
    print('script', script, 'found' if os.path.isfile(script) else 'not found', 'readable' if os.access(script, os.R_OK) else '-')
EOF
```

- With `args` (exec form), `command` is resolved on `PATH` or as a path; `args` elements are literal.
- For `bash script.sh`, `node script.js`, `python3 script.py`, check that the script exists and is readable; it does not need `chmod +x`.
- Substitute `${CLAUDE_PROJECT_DIR}` with the project root and `$(git rev-parse --show-toplevel)` with the repository root before testing.
- For a command chain such as `export PATH=...; tool ...`, resolve the last command that does the work, and note the chain.
- A name resolved on `PATH` now proves only the current shell's `PATH`, not the environment the host gives hooks. Mark it resolved, and say that the runtime `PATH` is not verified.

Flag:
- **Not found**: nothing exists at that path; for a policy hook this silently disables the gate
- **Not executable**: a directly executed script without `chmod +x`
- **Relative path**: resolves from the session `cwd`, which varies
- **Interactive command** (`read`, `fzf`, `gum`, TUI): hooks have no controlling terminal

Done when: every command hook is marked found or not found, executable or not, with the resolved path.

### Step 3: Check blocking strategy

For hooks on events that can block (see the tables above) whose command is a local script:

1. Read the script.
2. Classify:
   - **exit 2 on the block path**: ✅
   - **JSON decision supported by the event and host** (`permissionDecision: "deny"`, `decision.behavior: "deny"`, `decision: "block"`): ✅, whatever the exit code
   - **exit 1 or a generic non-zero code on the block path, without JSON**: ⚠️ the action proceeds
   - **exit 2 on `PermissionRequest`** (Claude Code): ⚠️ not honored; use the `decision` object
   - **Codex `permissionDecision: "ask"` or `continue: false` on `PreToolUse`**: ⚠️ unsupported, the tool call continues
   - **No decision at all**: 🔵 observational, fine when intended
3. Flag slow operations (`curl`, `sleep`, network calls) without an internal timeout guard in hooks on the interactive path.
4. Before flagging a slow operation against a short `timeout`, check whether it runs detached (`( ... ) &` with `disown`, `nohup`, `setsid`). Detached work outlives the hook, so a short timeout is correct there; report the detached work instead.
5. For a compiled binary or a script too large to read in full, do not guess its decision logic. Record the version (`--version` or `--help`), classify the blocking strategy as `UNKNOWN`, and propose a behavior canary (a sample payload on stdin, then the exit code and stdout).
6. Before recommending a host-specific variant of a hook (for example a `codex` subcommand in place of a `claude` one), run both on the same sample payload and compare their outputs against the host's output contract. A Claude-named handler under Codex is not a defect when its output shape is one Codex supports.

Done when: every script-backed hook on a blocking event has one of the classifications above, or `UNKNOWN` with a proposed canary.

### Step 4: Check duplicates and dead configuration

- Claude Code: the same handler in several settings files runs once. Report it as redundant configuration to clean up, not as double execution. A plugin or skill copy of the same handler runs separately: report that one as a real duplicate.
- A matcher on an event without matcher support (silently ignored).
- `if` on a non-tool event (the hook never runs).
- `once` outside skill frontmatter (ignored).
- A handler type not allowed on its event (skipped).
- `async: true` combined with a decision field (no effect).
- Two or more `PreToolUse` hooks on the same matcher returning `updatedInput` (winner undocumented).
- A Stop hook that always continues without reading `stop_hook_active`.
- Codex: a layer with both `hooks.json` and inline `[hooks]`; hooks awaiting trust review. When both representations run the same tool on the same event, even through different command strings (a wrapper script and the binary it calls), report a real double run, and name the installer that owns each entry.
- Secrets in hook sources or settings: token-like literals, credentials in `headers` or `env`. Report the file and line with the value redacted, and recommend moving the value out of the source and rotating it.

Done when: each finding is attached to a hook record, or the list is explicitly empty.

### Step 5: Interactive review (core of the skill)

Process hooks **one by one**. Do not batch and skip the interaction.

**For each hook:**

Show:
```
Hook: PreToolUse → Bash [claude, project settings]
type: command
command: ${CLAUDE_PROJECT_DIR}/.claude/hooks/confirm-git-push.sh
timeout: (none, default 600s)
Script: found (executable ✅)
Blocking strategy: JSON permissionDecision "deny" ✅
```

Ask three questions:
1. "Does this hook fire at the right time and scope? (y = yes / n = adjust matcher or event)"
2. "Is the command still working correctly? (y / broken / unsure)"
3. "Anything to change (matcher, command, timeout, remove it)? (describe or skip)"

**For lifecycle hooks (no matcher):**

Show:
```
Hook: SessionEnd [claude, user settings]
type: command
command: ~/.claude/hooks/session-summary.sh
timeout: (none, 1.5s SessionEnd budget)
Script: found (executable ✅)
```

Ask:
1. "Does this hook still serve a useful purpose? (y / n)"
2. "Is the command working within the timeout? (y / broken / unsure)"

**If the user provides changes during the interaction**: apply them using Edit, confirm each change, then move to the next hook. Never edit managed settings or `requirements.toml`. After editing a Codex hook, remind the user that it must be trusted again in `/hooks`.

Done when: every hook has the user's three answers (or two for lifecycle hooks) and every agreed edit is applied and confirmed.

### Step 6: Output report

After all hooks are reviewed:

```
# Hooks Audit: [project or global]
Date: [today] | Scanned: N hooks across M files (Claude Code: X, Codex: Y)

## Summary

| Status | Count |
|--------|-------|
| ✅ Good (≥80%) | N |
| ⚠️ Needs work (50-79%) | N |
| ❌ Fix (<50%) | N |
| 🔵 Observational | N |
| ✅ User confirmed useful | N |
| ⚠️ User flagged for update | N |
| 🗑️ User marked as stale | N |

---

## Per-Hook Results

### PreToolUse → Bash [claude, user settings] (7/10 ⚠️)

type: command
command: `~/.claude/hooks/confirm-git-push.sh`
timeout: (none, default 600s)

| Criterion | Score | Notes |
|-----------|-------|-------|
| event and handler type | ✅ 1/1 | PreToolUse, command |
| matcher | ✅ 2/2 | scoped to Bash |
| command | ✅ 3/3 | found, executable |
| timeout | ⚠️ 1/2 | 600s default on the interactive path, script calls the network without a guard |
| blocking awareness | ⚠️ 0/2 | block path exits 1 without JSON: the tool call proceeds |

**Priority fixes:**
1. Replace `exit 1` with `exit 2`, or print a `permissionDecision: "deny"` JSON object
2. Add `"timeout": 10` or an internal timeout around the network call

User feedback: ✅ scope correct
Content: exit strategy fixed ✅

---

### PostToolUse → Edit|Write [claude, user settings] (8/8 ✅) 🔵

type: command
command: `~/.claude/hooks/anti-ai-markers.sh`
timeout: 2

Observational hook: exit 2 would only show stderr to Claude. All applicable criteria pass. User confirmed still useful.

---
```

Done when: the report lists every scanned hook with its score and criterion notes.

### Step 7: Fix Summary

```
## What Changed This Session

confirm-git-push.sh hook:
  - Exit strategy changed to exit 2
  - Added timeout: 10

session-summary.sh hook:
  - User confirmed useful, no changes

rtk-baseline.sh hook (codex):
  - Edited; needs re-trust in /hooks
  - User flagged as stale (awaiting explicit deletion confirmation)

---
N hooks audited · N edits applied · N flagged as stale · N redundant copies · N awaiting Codex trust review
```

For any hook the user marked as stale: ask for explicit confirmation before removing it. Never delete without a clear "yes, remove it".

Done when: the summary line counts match the per-hook results and no deletion happened without explicit confirmation.

---

## Edge Cases

- **Inline one-liner** (e.g. `rtk hook claude`): skip script-level checks, verify the binary is on `PATH`
- **`bash -c '...'` inline**: parse the inner script for interactive commands and exit logic
- **`exit 1` in a policy hook without JSON**: ⚠️ non-blocking, the action proceeds
- **Same hook in user and project settings (Claude Code)**: runs once; note both locations as redundant configuration
- **`timeout: 0`**: flag as likely invalid
- **Unknown event** (e.g. `PreToolCall`): ❌, report the exact string and suggest the documented name for that host
- **Claude-only event in a Codex file** (e.g. `PostToolUseFailure`, `PreModelSwitch`) or the reverse (`Interrupt` in Claude settings): ❌ never fires on that host
- **Script not executable and run directly**: fails with a non-blocking error; suggest `chmod +x`
- **Matcher on a no-matcher event**: silently ignored, suggest removing it
- **`async: true` with `decision` or `permissionDecision`**: ⚠️ no effect
- **`asyncRewake: true`**: background, wakes Claude on exit 2 with stderr (or stdout); use it instead of `async` when a background failure must reach Claude
- **`prompt` or `agent` hook**: no command to resolve; check that `prompt` is present and that the event allows the type
- **SessionEnd hook doing heavy work**: 1.5 s default budget on Claude Code, 1 s default and 3 s maximum on Codex; warn that it may be killed
- **`PermissionRequest` in `-p` or background subagents (Claude Code)**: hooks still run; if none decides, the call is denied. Do not recommend migrating to `PreToolUse` for that reason
- **`if` on a non-tool event**: the hook never runs; remove `if` or change the event
- **Stop hook without a `stop_hook_active` check**: continuations stop at the 8-consecutive cap; read the field and exit 0 when it is `true`
- **Hardcoded project-local absolute path**: suggest `${CLAUDE_PROJECT_DIR}/...` (Claude Code, exec form preferred) or a git-root-based path (Codex)
- **Hooks not firing as expected**: Claude Code: open `/hooks` (read-only browser showing each hook's source) and run with `--debug`. Codex: open `/hooks` to see sources, pending trust reviews, and disabled hooks
