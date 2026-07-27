---
title: "Claude Code Release History"
description: "Condensed changelog of official Claude Code releases with highlights and breaking changes"
tags: [reference, release]
canonicalURL: "https://cc.bruniaux.com/releases/"
keywords:
  - "claude code release history"
  - "when was claude code released"
  - "what is the most recent version of claude code"
  - "anthropic claude changelog june 2026 release notes"
---

# Claude Code Release History

> Condensed changelog of Claude Code official releases.
> **Full details**: [github.com/anthropics/claude-code/CHANGELOG.md](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
> **Machine-readable**: [claude-code-releases.yaml](../../machine-readable/claude-code-releases.yaml)

**Latest**: v2.1.220 | **Updated**: 2026-07-25

---

## Quick Jump

- [2.1.x Series (January-July 2026)](#21x-series-january-july-2026): bug fixes (2.1.220), ⭐ Claude Opus 5 becomes the default Opus model with 1M context and fast mode at $10/$50 per Mtok + `DirectoryAdded` hook + `sandbox.network.strictAllowlist` + `workflowSizeGuideline` setting + subagent nesting restored to depth 3 + Opus 4.7 dropped from fast mode (2.1.219), ⭐ `/code-review` runs as a background subagent + agent frontmatter hooks require workspace trust + `context: fork` skills background by default + `/deep-research` manual-only + left-arrow conversation-discard fix (2.1.218), concurrent subagent cap (default 20) + `--max-budget-usd` halts background subagents + MCP truncated-output memory leak fix + emoji shortcode autocomplete + background-session symlink escape fix (2.1.217), `sandbox.filesystem.disabled` + quadratic message-normalization slowdown fix + auto-mode HTTP 401 classifier fix (2.1.216), `/verify` and `/code-review` skills no longer auto-invoked (2.1.215), ⭐ eight Bash permission-check security fixes + EndConversation tool + long-tool-call heartbeat + OTel message correlation attributes + hook `dir/**` matching narrowed to cwd (2.1.214), ⭐ `/fork` copies conversation into a background session + in-session subagent renamed `/subtask` + WebSearch/subagent-spawn session caps + MCP calls auto-background after 2min + plan-mode Bash permission-prompt security fix + Task tool `mode` param deprecated (2.1.212), `--forward-subagent-text` + permission-preview character-neutralization security fix + auto-mode PreToolUse `ask` floor + subagent model-override resume fix (2.1.211), live elapsed-time counter on tool calls + Agent tool prompt-injection hardening + `Write(path)`/`Glob(path)` permission rules deprecated (2.1.210), background-session dialog fix (2.1.209), ⭐ screen reader mode + `vimInsertModeRemaps` + `CLAUDE_CODE_PROCESS_WRAPPER` (2.1.208), ⭐ Bedrock/Vertex/AWS default to Opus 4.8 + terminal streaming perf fix + plugin shell-injection hardening (2.1.207), `/doctor` full setup checkup + `/commit-push-pr` push-remote auto-allow + background agents upgrade after update (2.1.206), ⭐ `/doctor` becomes full setup checkup (`/checkup` alias) + agent view classifier headlines + auto mode blocks transcript tampering (2.1.205), SessionStart hook streaming fix in headless sessions (2.1.204), login-expiry warning + manual-mode footer badge + background-agent stability fixes (2.1.203), dynamic workflow size setting + workflow OTel attributes (2.1.202), Sonnet 5 harness reminder role fix (2.1.201), ⭐ permission mode 'default' renamed 'Manual' + AskUserQuestion no longer auto-continues (2.1.200), retry hardening + subagent partial-work fixes + stacked slash-skill loading (2.1.199), ⭐ subagents background by default + Claude in Chrome GA (2.1.198), ⭐ Claude Sonnet 5 default model + native 1M context (2.1.197), org default models + clickable file attachments + security fix for self-approved `.mcp.json` servers (2.1.196), bug fixes: hook exact-match + voice dictation + background agents (2.1.195), ⭐ OTel response event + `autoMode.classifyAllShell` + bash path autocomplete (2.1.193), ⭐ `/rewind` after `/clear` + ~37% CPU streaming reduction + MCP reliability improvements (2.1.191), bug fixes (2.1.190), ⭐ `sandbox.credentials` + org model restrictions + MCP 5-min timeout (2.1.187), ⭐ `claude mcp login/logout` + `!` bash auto-response + background subagent permission prompts (2.1.186), stream-stall hint improved to 20s delay (2.1.185), ⭐ auto mode safety blocks destructive git/terraform ops (2.1.183), ⭐ `/config key=value` inline setting syntax + subagent panel improvements + 30+ bug fixes (2.1.181), bug fixes: connection drops + WSL2 scroll (2.1.179), ⭐ `Tool(param:value)` permission syntax + nested skills + auto mode classifier (2.1.178), ⭐ session titles in conversation language + `enforceAvailableModels` (2.1.176, 2.1.175), `wheelScrollAccelerationEnabled` + VS Code usage attribution (2.1.174), bug fixes (2.1.173), ⭐ sub-agents spawn sub-agents + Bedrock region auto-detection (2.1.172), ⭐ Claude Fable 5 (2.1.170), ⭐ `--safe-mode` + `/cd` command (2.1.169), bug fixes (2.1.168, 2.1.167, 2.1.165), `fallbackModel` + deny rule glob + thinking disable + hardened SendMessage (2.1.166), `requiredMinimumVersion`/`requiredMaximumVersion` + `/plugin list` + Stop hook additionalContext (2.1.163), Quieter startup + agents waitingFor + slash-command fill-in (2.1.162), OTEL custom dimensions + agents done/total + parallel tool-call isolation (2.1.161), `ultracode` keyword replaces `workflow` + security prompts for startup files + Edit after grep (2.1.160), internal infra (2.1.159), Auto mode on Bedrock/Vertex/Foundry for Opus 4.7/4.8 (2.1.158), plugin auto-load from `.claude/skills` + `claude plugin init` + 20+ bug fixes (2.1.157), Opus 4.8 thinking-blocks crash fix (2.1.156), Opus 4.8 + dynamic workflows + lean system prompt default (2.1.154), /model saves as default (IDE parity) + modelPicker keybinding rename (2.1.153), code-review fix applies to working tree, disallowed-tools frontmatter, MessageDisplay hook, auto mode opt-in removed, 35+ bug fixes (2.1.152), internal infra (2.1.150), /usage per-category breakdown (skills/subagents/plugins/MCP), GFM task list checkboxes, PowerShell permission bypass security fix, sandbox worktree write allowlist fix, allowAllClaudeAiMcps enterprise setting, 20+ bug fixes, pinned background sessions (Ctrl+T), /code-review --comment for inline GitHub PR comments, auto-updater improvements, Bash exit-127 hotfix, /code-review command (renamed from /simplify) with effort level, AskUserQuestion restored in auto mode, agents --json, /plugin previews before install, permission-prompt bypass security fix, /resume lists background sessions, /model session-only (d for default), usage credits rename, 75s startup hang fix, plugin dependency enforcement, projected context cost in /plugin, worktree.bgIsolation: "none", fast mode Opus 4.7 default, new claude agents dispatch flags, SKILL.md root-level plugin surfacing, hook terminalSequence, claude agents --cwd, Rewind summarize, subagent_type case-insensitive, plugin folder warnings, agent view (Research Preview), /goal command, hook args exec form + continueOnBlock, settings.autoMode.hard_deny, CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL, MCP /clear disappear fix, 40+ UI fixes, worktree.baseRef setting, effort level in hooks, CLAUDE_CODE_SESSION_ID in Bash env, CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN, MCP memory fix (10GB+ RSS), subagent skills fix, 40+ bug fixes, Worktree isolation, background agents, ConfigChange hook, Fast mode Opus 4.6, 1M context, claude.ai MCP connectors, remote-control, auto-memory, /copy command, HTTP hooks, worktree config sharing, ultrathink re-introduced, InstructionsLoaded hook, 4 security fixes, Agent model override restored, 12x SDK token cost reduction, /context actionable suggestions, modelOverrides setting, 1M context Opus 4.6 default for Max/Team/Enterprise, MCP elicitation, PostCompact hook, /effort command, Opus 4.6 64k/128k output tokens, allowRead sandbox setting, /branch command, StopFailure hook, streaming line-by-line, --console auth flag, SessionEnd fix, enterprise retry fix, rate_limits statusline field, effort frontmatter for skills, --channels MCP research preview, --bare flag, worktree session resume fix, MCP query collapsing, managed-settings.d/ drop-in, CwdChanged/FileChanged hooks, transcript search, credential scrubbing, PowerShell tool Windows preview, conditional hooks if field, MCP headersHelper multi-server env vars, headless AskUserQuestion hooks, X-Claude-Code-Session-Id header, Jujutsu/Sapling VCS exclusions, @ mention token reduction, Read tool compact format, Cowork Dispatch fix, PermissionDenied hook, thinking summaries off by default, "defer" PreToolUse permission, CLAUDE_CODE_NO_FLICKER, /powerup interactive lessons, PowerShell hardened permissions, SSE linear-time performance, MCP 500K result override, disableSkillShellExecution, plugin bin/ executables, Edit tool shorter anchors, interactive Bedrock wizard, forceRemoteSettingsRefresh, /cost per-model breakdown, interactive /release-notes, Linux sandbox apply-seccomp fix, Bedrock Mantle support, high effort default for API/enterprise users, Bedrock auth fix, NO_FLICKER focus view (Ctrl+O), refreshInterval status line, 30+ bug fixes, Vertex AI wizard, Monitor tool, CLAUDE_CODE_PERFORCE_MODE, Bash security hardening, subprocess PID namespace sandboxing, /team-onboarding command, OS CA cert store trust by default, /ultraplan auto-cloud-environment, 40+ bug fixes, PreCompact hook blocking, EnterWorktree path param, plugin monitors, /proactive alias, WebFetch CSS/JS stripping, /doctor status icons, thinking hints sooner, ENABLE_PROMPT_CACHING_1H, /recap session context, built-in slash commands via Skill tool, /undo alias, rotating extended-thinking indicator, /tui fullscreen command, push notification tool, --resume resurrects scheduled tasks, /focus command, autoScrollEnabled config, session recap for telemetry-disabled, 30+ bug fixes, Opus 4.7 xhigh effort, /ultrareview cloud code review, /less-permission-prompts skill, Auto mode for Max subscribers, plan files named after prompts, read-only bash glob patterns no prompt, interactive /effort slider, many bug fixes, native binary spawning, sandbox.network.deniedDomains, security hardening exec wrappers, crash fix permission dialog, /resume 67% faster, inline thinking progress, sandbox dangerous-path security fix, agent frontmatter hooks via --agent, many terminal and UI bug fixes, default effort high for Pro/Max on Opus 4.6+Sonnet 4.6, native bfs/ugrep on macOS/Linux, /model persistence across restarts, Opus 4.7 1M context fix, 15+ bug fixes, vim visual mode, /usage merged from /cost+/stats, custom named themes, hooks invoke MCP tools, DISABLE_UPDATES env var, wslInheritsWindowsSettings, 15+ bug fixes, /config settings persist to settings.json, --from-pr multi-platform support, agent frontmatter honors tools+permissionMode, blockedMarketplaces security fix, TaskList ordering fix, 30+ bug fixes, Windows no longer requires Git Bash (PowerShell fallback), claude ultrareview CI subcommand, ${CLAUDE_EFFORT} in skills, alwaysLoad MCP option, plugin prune, PostToolUse output replacement for all tools, ANTHROPIC_BEDROCK_SERVICE_TIER, PR URL in /resume search, OAuth 401 hotfix, gateway /v1/models listing in /model picker, claude project purge, OAuth paste code for WSL2/SSH/containers, security fix allowManagedDomainsOnly/allowManagedReadPathsOnly, Windows PowerShell 7 as primary shell, 40+ bug fixes, EnterWorktree branch from local HEAD fix, --plugin-dir .zip support, --channels console auth, /mcp tool count per server, parallel bash tool call fix, sub-agent prompt cache fix, 35+ bug fixes, --plugin-url flag, CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE, Ctrl+R all-projects history restored, skillOverrides fix, 1h cache TTL fix, OAuth refresh race fix, 20+ bug fixes, VS Code Windows activation fix, Mantle auth fix
- [2.0.x Series (Nov 2025 - Jan 2026)](#20x-series-november-2025---january-2026) — Opus 4.5, Claude in Chrome, Background agents
- [Breaking Changes Summary](#breaking-changes-summary)
- [Milestone Features](#milestone-features)

---

## 2.1.x Series (January-July 2026)

### v2.1.220 (2026-07-24)

- **Fixed**: Bug fixes and reliability improvements

### v2.1.219 (2026-07-24)

> Model release. Claude Opus 5 takes over as the default Opus model, and the subagent nesting limit lifted two releases ago comes back at depth 3.

- ⭐ **Added**: Claude Opus 5 (`claude-opus-5`), now the default Opus model, with 1M context and fast mode at $10/$50 per Mtok
- **Added**: `sandbox.network.strictAllowlist` to deny non-allowlisted hosts for sandboxed commands without prompting
- **Added**: The `DirectoryAdded` hook, firing after `/add-dir` or the SDK `register_repo_root` control request registers a new working directory mid-session
- **Added**: `mcp_server_errors` to the headless stream-json init event, listing `--mcp-config` entries skipped by config validation; terminal runs print a startup warning
- **Added**: The `workflowSizeGuideline` settings key, so the advisory Dynamic workflow size guideline can be set from any settings file (the `/config` row hides while one is set)
- **Added**: Nested subagent forwarding in stream-json, so subagents spawned at depth 2 and deeper appear when `--forward-subagent-text` is set, keyed by their spawning Agent `tool_use` id
- **Added**: The current default workflow size to the running-workflow status line, with a pointer to `/config`
- **Fixed**: `claude -p` text output dropping the answer already produced when a turn died on a mid-stream API error
- **Fixed**: The `/model` picker showing the merged Opus row as plain "Opus" instead of "Opus (1M context)", and the Fable model row showing "Requires usage credits" for plans that include it
- **Fixed**: Copy-on-select inside GNU screen printing base64 into the terminal instead of copying the selection
- **Fixed**: Remote Control clients keeping a stale fast-mode status after a model switch, reconnect, or failed org check
- **Fixed**: `CLAUDE_CODE_GIT_BASH_PATH` on Windows exiting or being used as bash when the path isn't a bash/sh binary; it is now ignored with a warning
- **Fixed**: Vim mode where pressing ← on an empty prompt returned to the agent view only from INSERT, not NORMAL mode
- **Fixed**: Screen-reader mode rewriting the entire input line on every keystroke instead of echoing only the typed character
- **Added**: HTTP status and error text to `claude mcp list` and `/mcp` when a server fails to connect, plus a warning for MCP config values with hidden leading or trailing whitespace
- **Changed**: Subagents spawn nested subagents up to depth 3 by default (was 1 since 2.1.217); set `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` to disable nesting
- **Changed**: Dynamic workflows default to a medium size guideline (aim for fewer than 15 agents); pick another size or unrestricted with Dynamic workflow size in `/config`
- **Changed**: Managed MCP allowlist/denylist `${VAR}` entries resolve from the startup environment and managed-settings env instead of settings-file env
- **Changed**: The `/model` picker highlights only the newest model's name, so the highlight marks the new release
- **Removed**: Opus 4.7 from fast mode; `/fast` now applies to Opus 5 and Opus 4.8
- **Changed**: The claude-api skill defaults to Claude Opus 5, with a migration path from Opus 4.8

### v2.1.218 (2026-07-22)

> Large bug-fix release, plus a change in how `/code-review` runs and a workspace-trust requirement for agent frontmatter hooks.

- **Changed**: `/code-review` runs as a background subagent, so review work no longer fills the conversation and stacked slash commands stay its review target
- **Security**: Agent frontmatter hooks now require the agent file's own folder to have accepted workspace trust, so hooks no longer run from untrusted folders
- **Fixed**: Windows paths with `\u`-prefixed segments (like `C:\Users\unicorn`) being corrupted into CJK characters in tool inputs, which made those files inaccessible
- **Fixed**: The left arrow key discarding the conversation with no undo; presses right after editing now ask to confirm, and Esc in the agent view returns to the conversation it backgrounded
- **Fixed**: Multi-line paste collapsing into one line with `j` in place of newlines in terminals that encode pasted newlines as Ctrl+J
- **Fixed**: `/context` reporting stale pre-compact token usage after compacting from the message picker
- **Fixed**: `/ultrareview` failing on descriptive arguments like "review my auth changes"; they now run a review of the current branch with the text applied as a note to the findings
- **Fixed**: `/code-review ultra` silently running a local review in non-interactive sessions instead of launching the cloud review
- **Fixed**: Gateway spend metering to price Bedrock application-inference-profile ARNs and other config-mapped upstream model IDs at the configured model's rates
- **Fixed**: Spurious "[Request interrupted by user]" messages after interrupted tool calls, and an unpaired `tool_use` block left in the transcript when a tool aborted mid-response
- **Fixed**: Crashes (maximum call stack exceeded) when a deeply nested watched directory tree was deleted or moved, and when rendering deeply nested UI trees
- **Fixed**: A retry loop re-sending identical doomed requests after a context-overflow error with a large thinking budget; `Ctrl+B` backgrounding now applies the same background-shell caps as other paths
- **Fixed**: Fork-session lineage being lost after compaction in headless and SDK sessions, and a resumed session failing every turn or crashing on resume when its history held a malformed delta attachment
- **Fixed**: The Bedrock setup wizard failing profile verification for assume-role profiles in partitioned AWS regions and on proxy-only networks
- **Fixed**: The "N MCP servers need authentication" startup notice over-counting claude.ai connectors that aren't connected in claude.ai
- **Fixed**: Prompt history entries being dropped or duplicated when history writes raced or failed
- **Fixed**: Remote sessions continuing to send heartbeats after their worker was replaced, leaving long-lived desktop and IDE processes retrying a rejected request every few seconds forever
- **Added**: Screen-reader announcements of deleted text for word and line deletions (`Option+Delete`, `Ctrl+W`, `Cmd+Backspace`, `Ctrl+U`, `Ctrl+K`) in `--ax-screen-reader` mode
- **Added**: An announcement when fast mode changes as a result of switching models via `/config model=<x>` or Remote Control
- **Changed**: Auto mode adjudicates the dangerous-rm, background-`&`, and suspicious-Windows-path checks instead of opening permission dialogs, and plan mode with auto no longer prompts for Bash commands the static analyzer can't prove read-only
- **Changed**: `/deep-research` starts only when invoked manually; Claude no longer launches it on its own
- **Changed**: Skills with `context: fork` run in the background by default; opt out per skill with `background: false`
- **Changed**: Agent markdown files reject agent names containing `:`, which is reserved for plugin namespacing
- **Changed**: Server-managed settings so benign feature and cost toggles no longer trigger the settings-approval prompt
- **Added**: `yes`/`no`/`on`/`off`/`1`/`0` (case-insensitive) as accepted values for skill and plugin frontmatter booleans, alongside `true`/`false`

### v2.1.217 (2026-07-21)

> Subagent fan-out gets budget guardrails: a concurrency cap, nesting off by default, and `--max-budget-usd` finally halting background agents.

- **Added**: A cap on concurrently-running subagents (default 20, override with `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) so one message can't fan out unbounded background agents
- **Changed**: Subagents no longer spawn nested subagents by default; set `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` to allow deeper nesting (restored to depth 3 in v2.1.219)
- **Fixed**: `--max-budget-usd` not stopping background subagents; once the cap is reached, new spawns are denied and running background agents are halted
- **Added**: Emoji shortcode autocomplete in the prompt input (type `:heart:` to insert ❤️, or `:hea` for suggestions), disabled with the `emojiCompletionEnabled` setting
- **Added**: Warnings when transcript writes are failing (disk full, for instance) or when session saving is off due to an inherited environment variable, instead of losing transcripts silently
- **Fixed**: A memory leak where truncated MCP tool outputs kept the full untruncated result in memory for the rest of the session
- **Security**: Background session isolation not canonicalizing symlinked working directories, which could let sessions escape their workspace folder
- **Fixed**: Windows auto-update failures that could leave `claude.exe` missing; failed updates now restore the preserved executable automatically
- **Fixed**: Auto-compact never triggering for Claude Opus 4.8 on Bedrock, and `/compact` failing once over the limit
- **Fixed**: Corporate mTLS, TLS-verify, OAuth scope, and proxy settings being ignored in Claude Desktop sessions
- **Fixed**: Managed settings that set `OTEL_EXPORTER_OTLP_ENDPOINT` not governing all signals; lower-scope signal-specific overrides no longer redirect telemetry away from the managed endpoint
- **Fixed**: `--resume`/`--continue` and `/resume` failing with a TypeError when a transcript has a malformed attachment entry
- **Fixed**: Remote Control sessions not showing a pending permission prompt or dialog to viewers that connected after it appeared
- **Fixed**: Background shells sometimes becoming impossible to stop after a session is sent to the background (`/background` or `←`) or when the session exits on a heavily loaded machine, most visible on Windows
- **Fixed**: A `CLAUDE.md` or `SKILL.md` `paths` frontmatter value with many brace groups OOM-killing or stalling the CLI at startup; brace expansion is now budget-bounded
- **Fixed**: Screen reader mode's startup announcement being cut off by the first prompt render, and the thinking status row re-rendering every few seconds
- **Improved**: Footer PR badge links are clickable hyperlinks even when terminal support can't be detected (over ssh or tmux); set `FORCE_HYPERLINK=0` to opt out
- **Changed**: The login-expiry warning appears 3 days before expiry instead of 5, and the frontend-design plugin suggestion tip is capped at 3 lifetime impressions

### v2.1.216 (2026-07-20)

- **Added**: `sandbox.filesystem.disabled` to skip filesystem isolation while keeping network egress control
- **Fixed**: A slowdown in long sessions where message normalization cost grew quadratically with the number of turns, causing multi-second stalls and slow resumes
- **Fixed**: Auto mode denying commands with "HTTP 401" classifier errors after the OAuth token expired or rotated mid-session
- **Fixed**: AskUserQuestion telling Claude to continue even when the answer asked it to wait or explain first; free-text answers now get neutral wording
- **Fixed**: Claude Code on the web re-asking the same question and dropping the answer after the session sat idle for a few minutes

### v2.1.215 (2026-07-19)

- **Changed**: Claude no longer runs the `/verify` and `/code-review` skills on its own; invoke them with `/verify` or `/code-review` when you want them

### v2.1.214 (2026-07-18)

> Security-heavy release. Eight separate Bash permission-check holes closed, plus a large sweep across background sessions, the PowerShell tool on Windows, and OpenTelemetry instrumentation.

- ⭐ **Security**: Fixed single-segment `dir/**` allow rules like `Edit(src/**)` auto-approving writes to nested `src/` directories anywhere in the tree instead of only `<cwd>/src`
- **Security**: Fixed a permission-check bypass affecting commands run in Windows PowerShell 5.1 sessions
- **Security**: Bash permission checks now fail closed on file-descriptor redirect forms that bash parses differently than the permission analyzer
- **Security**: Commands over 10,000 characters now always prompt instead of running automatically
- **Security**: zsh variable subscripts and modifiers in `[[ ]]` comparisons are no longer treated as inert text, so those commands prompt for approval
- **Security**: Certain `help` and `man` commands that could run unsafe options, command substitutions, or backslash paths are no longer auto-approved
- **Security**: Fixed permission prompts on remote sessions that could proceed before the local confirmation dialog
- **Added**: The EndConversation tool, letting Claude end sessions with highly abusive users or jailbreak attempts, as on claude.ai since 2025 ([research post](https://www.anthropic.com/research/end-subset-conversations))
- **Added**: A periodic progress heartbeat for long-running tool calls that previously went silent
- **Added**: `message.uuid`, `client_request_id`, and `tool_source` attributes to OpenTelemetry log events for message-level correlation and tool provenance
- **Added**: `CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH` to configure the 60 KB truncation limit on OpenTelemetry content attributes
- **Added**: Reasoning effort in the `subagentStatusLine` payload, so custom agent rows can render model and effort
- **Added**: An ISO `modified` timestamp to memory file frontmatter
- **Fixed**: Background sessions parked with `←` or `/background` and left idle keeping the daemon and a worker process alive indefinitely, completed sessions being impossible to remove via `claude rm`, and a displaced daemon deleting its successor's control socket on shutdown
- **Fixed**: PowerShell tool commands hanging until timeout when a child process waited on standard input, Python scripts crashing with UnicodeDecodeError or UnicodeEncodeError, and `>`/`>>` writing UTF-16LE files that other tools couldn't read (Windows)
- **Fixed**: Hooks with exit code 2 not blocking as documented when the hook's stdout JSON fails schema validation
- **Fixed**: Session cost and token telemetry double-counting on streams that emit multiple cumulative `message_delta` frames
- **Fixed**: Plugins enabled via the `--settings` CLI flag not loading (regression since v2.1.181)
- **Fixed**: Streaming turns failing with "Socket is closed" behind corporate proxies on Windows, and stream-json output truncating at exit for slow-reading SDK consumers
- **Fixed**: Unbounded memory growth when `--settings` points at a device file or multi-GB file; oversized (>2 MiB) settings files now fail at startup with a clear error
- **Fixed**: `/ultrareview` refusing to run in repos with no merge base, and scheduled tasks refusing their own configured prompt as untrusted input
- **Changed**: Single-segment `dir/**` hook `if:` conditions match only `<cwd>/dir`; write `**/dir/**` for any-depth matching (`deny`/`ask` permission rules keep their any-depth match)
- **Changed**: `file` commands using `-m`/`--magic-file` or `-f`/`--files-from` require permission instead of being auto-allowed as read-only
- **Changed**: `docker` commands (including the Podman `docker` shim) carrying daemon-redirect flags (`--url`, `--connection`, `--identity`, Podman remote mode) now prompt for permission
- **Changed**: SessionStart hooks report source `"fork"` when a session begins as a fork instead of `"resume"`

### v2.1.212 (2026-07-16)

> Runaway-loop guardrails plus two security fixes: WebSearch and subagent spawns get session budgets, slow MCP calls auto-background, and `/fork` becomes a real conversation copy.

- ⭐ **Changed**: `/fork` now copies your conversation into a new background session (its own row in `claude agents`) while you keep working; the in-session subagent it used to launch is now `/subtask`
- **Added**: A session-wide WebSearch cap (default 200, `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`) and a per-session subagent-spawn cap (default 200, `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`) to stop runaway loops; `/clear` resets the budget
- **Added**: `claude auto-mode reset` restores the default auto-mode configuration, with a confirmation prompt (`--yes` to skip)
- **Improved**: MCP tool calls running longer than 2 minutes move to the background automatically so the session stays usable (`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`)
- **Improved**: `/resume` in the agent view opens a picker of past sessions (including deleted ones) and resumes your pick as a background session
- **Security**: Fixed plan mode auto-running file-modifying Bash commands (e.g. `touch`, `rm`) without a permission prompt or SDK `canUseTool` callback
- **Security**: Fixed worktree creation following a repository-committed symlink at `.claude/worktrees`, which could create files outside the repository
- **Deprecated**: The Task tool's `mode` parameter (now ignored); subagents inherit the parent session's permission mode by default

### v2.1.211 (2026-07-15)

- **Added**: `--forward-subagent-text` flag and `CLAUDE_CODE_FORWARD_SUBAGENT_TEXT` environment variable to include subagent text and thinking in stream-json output
- **Security**: Permission previews relayed to chat channels now neutralize bidirectional-override, zero-width, and look-alike quote characters, so tool inputs cannot visually alter the approval message
- **Security**: Auto mode no longer overrides a PreToolUse hook's `ask` decision for unsandboxed Bash; a hook `ask` now floors the decision at a prompt
- **Fixed**: Subagents spawned with an explicit model override reverting to the parent's model when resumed or sent a follow-up message
- **Fixed**: Nested `.claude/rules/*.md` files loading even when setting sources exclude project settings
- **Fixed**: Parallel Claude Code sessions all logging out simultaneously after wake-from-sleep when many sessions share one credential store
- **Fixed**: Plugin MCP servers not reconnecting after an idle web session woke, leaving MCP calls failing until the next message

### v2.1.210 (2026-07-14)

> Broad maintenance release: 30+ fixes across the agent view, background sessions, worktree isolation, and plugin handling, plus two security hardenings.

- **New**: A live elapsed-time counter on the collapsed tool summary line, so long-running tool calls visibly tick instead of looking stuck
- **New**: The agents footer hint shows how many background agents are waiting on your input, with brief color emphasis when the count changes
- **Security**: The Agent tool is hardened against indirect prompt injection via content a subagent read
- **Security**: Fixed `isolation: 'worktree'` subagents being able to run git-mutating commands against the main repo checkout instead of their own worktree
- **Security**: Fixed the `ultracode` keyword opt-in firing on non-human-originated input such as webhook payloads and relayed PR comments
- **Deprecated**: `Write(path)`, `NotebookEdit(path)`, and `Glob(path)` permission rules now trigger a startup warning; use `Edit(path)` or `Read(path)` instead
- **Improved**: Auto mode's permission classifier defaults to Sonnet 5 for external sessions, validated on the session's first request and pinned for the session
- **Improved**: The Bash/PowerShell timeout message now lets the model distinguish a hang from an explicit background request
- **Improved**: Screen reader mode announces permission mode changes aloud when cycling with Shift+Tab
- **Fixed**: `claude attach` failing with "job not found" or "agent is still starting" during session transitions; attach now waits for the daemon to settle
- **Fixed**: A hook callback timeout being misreported to the model as a user rejection, which made unattended sessions stop and wait
- **Fixed**: Claude assuming a `cd` took effect after its command was moved to the background; the tool result now states the working directory is unchanged
- **Fixed**: Plugin-provided MCP servers being torn down when MCP servers are re-synced mid-session
- **Fixed**: Plan approvals without edits being labeled "(edited by user)" and overwriting the plan file with a stale snapshot
- **Fixed**: Unmatched `$1`/`$2` positional placeholders in skills and commands being silently stripped; they are now preserved verbatim
- **Fixed**: `claude agents --effort ultracode` not reaching dispatched sessions; the value was silently dropped
- **Fixed**: Killed background sessions leaving a permanent `git worktree lock` behind; the periodic sweep now releases locks whose owning process is gone
- **Fixed**: Paste markers leaking into external editors opened from Claude Code, appearing as stray È/É characters around pasted text
- **Fixed**: Grep content mode claiming "No matches found" when paginating past the end of results
- **Fixed**: Late-appearing `.claude/*` symlinks not being reconciled into the sandbox deny-write list
- **Changed**: Fable temporarily shows as unavailable in the advisor picker while a server-side issue is fixed

### v2.1.209 (2026-07-14)

- **Fixed**: `/model` and other dialogs being blocked in `claude agents` background sessions (reverts an overly broad guard from 2.1.208)

### v2.1.208 (2026-07-13)

- ⭐ **New**: Screen reader mode, an opt-in plain-text rendering for screen reader users. Run `claude --ax-screen-reader`, set `CLAUDE_AX_SCREEN_READER=1`, or add `"axScreenReader": true` to settings
- **New**: `vimInsertModeRemaps` setting, mapping two-key insert-mode sequences like `jj` to Escape in vim mode
- **New**: `CLAUDE_CODE_PROCESS_WRAPPER`, so the agent view and background service honor a corporate launcher by running every Claude Code self-spawn through a required wrapper executable
- **New**: Mouse-click support for multi-select menus and "Other" input rows in fullscreen mode
- **Fixed**: The context window and auto-compact indicator briefly resetting to 200k after the CLI auto-updates, causing a false "100% context used" when resuming long-context sessions
- **Fixed**: Very large markdown tables stalling rendering or using excessive memory; tables over 200 rows now show the first 200 with a "… N more rows" notice
- **Fixed**: Fast mode staying off after switching back to a model that supports it; it now restores automatically when enabled in settings
- **Fixed**: Replies typed to a background agent being lost when delivery fails; the text is saved and delivered when the session restarts
- **Fixed**: Background-session attach failing permanently ("Couldn't start the background daemon") after an update replaced the binary a running `claude agents` process was launched from
- **Fixed**: Supervised and background sessions crashing when a server closed an HTTP/2 connection with a GOAWAY while requests were in flight
- **Fixed**: Truncated stream-json/JSON output and missing result message when piping large responses from `claude -p`
- **Fixed**: `CLAUDE_CODE_MAX_OUTPUT_TOKENS` and similar env vars silently using the mantissa of scientific-notation values (`1e6` became `1`)
- **Fixed**: The Edit tool failing on files modified after reading when the target text still matches uniquely
- **Fixed**: Read reporting empty files as "shorter than offset", Grep silently returning "No files found" for invalid regex, Grep count mode under-reporting paginated totals, and Glob crashing on null bytes in the pattern or path
- **Fixed**: `apiKeyHelper` script failures being hidden behind a generic 401 after ~10 silent retries; the script's own error now shows within 3 attempts
- **Fixed**: Bedrock streaming failing with a misleading "Truncated event message received" when a gateway transforms the response; the error now names the content-type and points at the proxy
- **Fixed**: `/release-notes` adding viewed notes to the model's context ("Show all" previously injected the entire changelog into every subsequent request)
- **Fixed**: The Agent tool launching with no tools when a subagent's `tools` list resolves to nothing; it now returns a clear error naming the unrecognized entries
- **Fixed**: The workflow save dialog showing `~/.claude/workflows/` instead of the `CLAUDE_CONFIG_DIR` location for user-scope saves
- **Fixed**: Headless stream-json sessions hanging permanently on a `control_request` with a non-string `set_model` payload

### v2.1.207 (2026-07-11)

- ⭐ **Changed**: Bedrock, Vertex AI, and Claude Platform on AWS now default to Claude Opus 4.8
- **Fixed**: Terminal freezing and keystrokes lagging while streaming very long lists, tables, paragraphs, or code blocks
- **Added**: Auto mode now available without the `CLAUDE_CODE_ENABLE_AUTO_MODE` opt-in on Bedrock, Vertex AI, and Foundry (disable via `disableAutoMode`)
- **Security**: Remote managed settings from a non-interactive run (`claude -p`, the SDK) were being recorded as consented without ever showing the consent dialog, now fixed
- **Breaking (plugins)**: `${user_config.*}` in shell-form plugin hook/monitor/headersHelper commands is now rejected (shell-injection fix); use exec form or `$CLAUDE_PLUGIN_OPTION_<KEY>`
- **Breaking (plugins)**: Plugin option values (`pluginConfigs`) are no longer read from project-level `.claude/settings.json`; only user, `--settings`, and managed settings are honored

### v2.1.206 (2026-07-09)

- **Added**: A `/doctor` check that proposes trimming checked-in `CLAUDE.md` files by cutting content Claude can derive from the codebase
- **Added**: `/cd` directory path suggestions, matching `/add-dir` behavior
- **Changed**: `/commit-push-pr` now auto-allows `git push` to the repo's configured push remote (`remote.pushDefault`, or the sole remote), not just `origin`
- **Changed**: Background agents now upgrade in the background right after an update, instead of a slow stale-session upgrade on attach
- **Improved**: `/code-review` findings quality on claude-opus-4-8 across all effort levels
- **Changed**: `EnterWorktree` asks for confirmation before entering a git worktree outside `.claude/worktrees/`

### v2.1.205 (2026-07-08)

- ⭐ **Changed**: `/doctor` is now a full setup checkup that can diagnose and fix issues (`/checkup` is its alias)
- **Improved**: Agent view rows show a colored state word and a classifier-written headline instead of raw tool call text; blocked-session peeks open with the exact ask
- **Security**: Auto mode now blocks tampering with session transcript files, and asks before running `rm -rf` on a variable it can't resolve from context
- **Fixed**: `--json-schema` silently producing unstructured output when the schema was invalid, and schemas using the `format` keyword being rejected
- **Changed**: Background task notifications now state that no human input has occurred, preventing fabricated in-transcript approvals from being acted on

### v2.1.204 (2026-07-08)

- **Fixed**: Hook events not streaming during SessionStart hooks in headless sessions, which could cause remote workers to be idle-reaped mid-hook

### v2.1.203 (2026-07-07)

> Background-agent daemon hardening: macOS open/switch stalls, stale session tokens, crash-looping on deleted directories, and a silent auto-upgrade failure that killed every running session.

- **New**: A warning when your login is about to expire, so you can re-authenticate before background sessions are interrupted
- **New**: A grey ⏸ badge in the footer when in manual permission mode, making the active mode always visible
- **New**: The session's additional working directories are now sent to MCP `roots/list`, with `notifications/roots/list_changed` on changes
- **Fixed**: Opening or switching background agent sessions on macOS stalling 15-20 seconds due to a false low-memory detection (regression in 2.1.196)
- **Fixed**: Background sessions becoming permanently unresponsive to attach, replies, and stop when the daemon's session token went stale (they now recover automatically)
- **Fixed**: Returning to `claude agents` silently stopping running subagents and re-running the prompt from scratch, so their work now carries over
- **Fixed**: A memory and per-turn CPU regression where the context-usage indicator re-analyzed the entire transcript after every turn
- **Fixed**: Background agents inheriting a stale `PATH` from the daemon instead of the dispatching shell (missing tools on Windows)
- **Fixed**: Background and agent-view sessions dropping a shell-exported `ANTHROPIC_BASE_URL`, sending API keys to the default endpoint and failing with 401
- **Fixed**: Bash failing with "argument list too long" in repos with many git worktrees
- **Fixed**: Worktree-isolated subagents sometimes running shell commands in the parent checkout instead of their own worktree
- **Fixed**: A background daemon auto-upgrade failure silently killing all running background sessions
- **Fixed**: `TaskStop` and `TaskOutput` failing to find background agents spawned by another agent (errors now list running agents by id and description)
- **Improved**: Subagent behavior, agents are now less likely to re-delegate their entire task to another subagent
- **Improved**: Binary size reduced by ~7 MB and startup memory by ~7 MB by loading a large bundled dependency lazily instead of inlining it
- **Changed**: Left arrow no longer closes the background tasks, diff, and workflow detail views (press Esc instead)

### v2.1.202 (2026-07-06)

- **New**: A "Dynamic workflow size" setting in `/config` for controlling how large Claude generally makes dynamic workflows (small/medium/large agent counts), an advisory guideline, not an enforced cap
- **New**: `workflow.run_id` and `workflow.name` OpenTelemetry attributes on telemetry emitted by workflow-spawned agents, so a workflow run's activity can be reconstructed from OTel data
- **Fixed**: `/rename` on background sessions being reverted when the job restarts, which broke addressing the session by its new name
- **Fixed**: Commands sent from Remote Control (mobile/web) into an interactive session failing with "Unknown command"
- **Fixed**: Images and files sent from the Remote Control mobile or web app without a caption being silently dropped
- **Fixed**: Resuming a session by name, or opening the resume picker, taking minutes and using a large amount of memory in repositories with many git worktrees
- **Changed**: `/review <pr>` reverted to a fast single-pass review; use `/code-review <level> <pr#>` for the multi-agent review at a chosen effort level

### v2.1.201 (2026-07-03)

- **Fixed**: Claude Sonnet 5 sessions no longer use the mid-conversation system role for harness reminders

### v2.1.200 (2026-07-03)

> Permission mode terminology cleanup: "default" is now called "Manual" everywhere in the UI, and `AskUserQuestion` dialogs stop auto-continuing unless you opt in.

- **Changed**: `AskUserQuestion` dialogs no longer auto-continue by default; opt into an idle timeout via `/config`
- **Changed**: The "default" permission mode is now labeled "Manual" across the CLI, `--help`, VS Code, and JetBrains; `--permission-mode manual` and `"defaultMode": "manual"` are accepted alongside `default`
- **Fixed**: Background sessions silently stopping mid-turn after sleep/wake or when reopening a stalled session
- **Fixed**: Background agents never starting again after a crash left a stale `daemon.lock` whose PID the OS reused
- **Fixed**: Subagents cut off by a rate limit before producing any text output returning an empty result instead of failing cleanly
- **Fixed**: Project-scoped plugins not loading correctly from git worktrees of the same repository
- **Improved**: Screen-reader output, decorative glyphs hidden, transcript symbols read as short labels, nested tables read as `Header: value.` lines

### v2.1.199 (2026-07-02)

> Retry hardening across the board: transient 429s retried automatically for subscribers, streaming partials preserved on mid-stream errors, and subagents now return partial work instead of failing silently.

- **New**: Stacked slash-skill invocations like `/skill-a /skill-b do XYZ` now load all leading skills (up to 5), not just the first
- **New**: Transient server rate-limit errors (429s unrelated to your usage limit) are now retried automatically with backoff for subscribers instead of failing the turn
- **New**: `CLAUDE_CODE_RETRY_WATCHDOG` now raises the default retry count for non-capacity transient errors to 300 and lifts the cap of 15 on `CLAUDE_CODE_MAX_RETRIES`
- **Fixed**: Streaming responses being discarded when the API emits a mid-stream overloaded/server error after partial output; the partial is now kept with an incomplete-response notice
- **Fixed**: Subagents cut off by a rate limit or server error silently failing instead of returning their partial work to the parent
- **Fixed**: Subagents reporting API errors (e.g. usage limit reached) as successful results; the error is now reported to the parent agent
- **Fixed**: SSL certificate errors (TLS-inspecting proxies, missing `NODE_EXTRA_CA_CERTS`, expired certs) burning retries before showing actionable guidance; they now fail immediately with the fix hint
- **Fixed**: The background-agent daemon on Linux killing itself and every running agent every ~50 seconds after an unclean shutdown left a corrupted worker record
- **Fixed**: Background agents failing to cold-start over SSH on macOS with "Could not switch to audit session" (regression in 2.1.196)
- **Fixed**: `claude stop` being silently undone when it raced a background-agent respawn; the respawn now honors the stop
- **Fixed**: `SendMessage` silently misrouting when a re-spawned agent reuses a previous agent's name; the tool now detects the mismatch and asks the caller to retarget
- **Fixed**: `SessionStart`, `Setup`, and `SubagentStart` hooks silently hiding stderr when exiting with code 2; the error is now shown in the transcript
- **Fixed**: Resetting a corrupted config file from the startup recovery dialog destroying it unrecoverably; it now backs up the file first
- **Fixed**: Plan mode not prompting for state-changing browser tool calls; read-only `browser_batch` calls are now correctly auto-allowed
- **Improved**: Idle subagents no longer vanish from the agent panel while others are still working; surplus idle agents collapse into an expandable summary row

---

### v2.1.198 (2026-07-01)

> ⭐ Subagents now run in the background by default, and Claude in Chrome is generally available.

- **New**: ⭐ Subagents now run in the background by default, so Claude keeps working while they run and is notified when they finish (previously a gradual rollout)
- **New**: ⭐ Claude in Chrome is now generally available
- **New**: Background agent notifications in `claude agents`: sessions that need input or finish now fire the `Notification` hook (`agent_needs_input` / `agent_completed`)
- **New**: Background agents launched from `claude agents` now commit, push, and open a draft PR when they finish code work in a worktree, instead of stopping to ask
- **New**: `/dataviz` skill for chart and dashboard design guidance with a runnable color-palette validator
- **New**: Gateway: Claude Platform on AWS (anthropicAws) added as an upstream provider; model-not-found responses now advance the failover chain
- **Improved**: The built-in Explore agent now inherits the main session's model (capped at Opus) instead of running on Haiku
- **Improved**: Subagents and context compaction now inherit the session's extended thinking configuration, improving output quality on delegated tasks
- **Improved**: Subagents now treat messages from the agent that launched them as normal task direction; an agent's message is still never treated as the user's approval
- **Fixed**: Brief network drops mid-response aborting the turn; transient errors like ECONNRESET now retry with backoff instead of failing
- **Fixed**: Agent teams: a teammate that dies on an API error now reports "failed" to the lead, and messaging a stuck teammate wakes it to retry immediately
- **Fixed**: Background tasks in web, desktop, and VS Code task panels getting stuck on "Running" after they finish or after resuming a session
- **Fixed**: `.claude/rules/` conditional rules not loading when the target file is reached via a symlinked path
- **Fixed**: Plan mode not auto-allowing read-only tool calls when a session starts in plan mode
- **Removed**: The `/agents` wizard; ask Claude to create or manage subagents, or edit `.claude/agents/` directly

---

### v2.1.197 (2026-06-30)

> ⭐ Introducing Claude Sonnet 5: the new default model in Claude Code, with a native 1M-token context window and promotional pricing of $2/$10 per Mtok through August 31.

- **New**: Claude Sonnet 5 is now the default model, with a native 1M-token context window and promotional pricing of $2/$10 per Mtok through August 31

---

### v2.1.196 (2026-06-29)

> Org default models in `/model`, clickable file attachments, security fix for self-approved `.mcp.json` servers, streaming idle watchdog on by default.

- **New**: Organization default models, set by admins in the org console; shows as "Org default" (or "Role default") in `/model` when you haven't picked one yourself
- **New**: Readable default names for sessions at start, making them easier to identify and message
- **New**: Clickable file attachments in chat (Cmd/Ctrl-click reveals the file in Finder/Explorer)
- **Security**: `claude mcp list`/`get` no longer spawn `.mcp.json` servers that a repo self-approved via a committed `.claude/settings.json`; untrusted workspaces show `⏸ Pending approval`
- **Fixed**: Waking a background job permanently deleting its conversation and re-running the original prompt when the transcript probe misread a real transcript; the file is now set aside, never deleted
- **Fixed**: Rate-limit warning flickering off and rate-limit telemetry being over-counted when multiple parallel requests hit a usage limit at once
- **Fixed**: Duplicate recap lines after a background session's turn when a schema-rejected StructuredOutput attempt retried
- **Fixed**: PowerShell `git diff`/`git grep`, `egrep`/`fgrep`, and quoted search patterns containing `|` being reported as failures when they exit 1, matching Bash behavior
- **Fixed**: Multiple `claude agents` side panel issues: keyboard focus stuck when opening an agent, background jobs losing their subagent types on every open, sessions showing incorrect status while actively running
- **Fixed**: `claude agents --dangerously-skip-permissions` silently falling back to auto mode instead of showing the bypass disclaimer
- **Fixed**: Mid-turn crash recovery for Remote sessions, so sessions interrupted by a server restart now auto-resume on the next worker
- **Fixed**: Sessions moved with `/cd` reappearing in the old directory's resume list after a non-graceful exit when the old path contained special characters
- **Fixed**: `claude plugin validate` skipping local plugins whose source is "." and stopping after the first error class
- **Fixed**: Esc Esc at an idle prompt not opening the rewind menu (regression); use Ctrl+C or Ctrl+X Ctrl+K to stop background agents
- **Fixed**: MCP OAuth requesting the authorization server's full `scopes_supported` catalog when no scope is specified, causing `invalid_scope` failures on GitLab self-hosted and other enterprise IdPs
- **Fixed**: `/context` showing 0 tokens for all tool groups on Bedrock
- **Fixed**: `/deep-research` misreporting verifier failures as "all claims refuted" instead of `unverified`
- **Fixed**: Plugin dependency version pins not being honored when the marketplace was added as a local folder path backed by a git repo
- **Fixed**: Voice dictation swallowing spaces and spuriously starting a recording during very fast typing when voice mode is enabled
- **Improved**: Background session reliability, so long-running commands and workflows now survive the session's process being stopped, restarted, or updated, including on Windows where background shells are handed off instead of being killed
- **Improved**: Background agents killed by a daemon restart are automatically resumed from where they left off the next time the agents view opens
- **Improved**: `/code-review` workflow merged five cleanup finders into one, cutting token usage by roughly 25%
- **Improved**: Reduced per-frame rendering work in the terminal UI by skipping no-op subtree walks during streaming
- **Changed**: The streaming idle watchdog is now on by default for all providers, aborting and retrying when a response stream produces no events for 5 minutes (set `CLAUDE_ENABLE_STREAM_WATCHDOG=0` to disable)
- **Changed**: Remote Control is now disabled when `ANTHROPIC_BASE_URL` points at a non-Anthropic host, matching the existing behavior under `CLAUDE_CODE_USE_BEDROCK`/`_VERTEX`/`_FOUNDRY`
- **Changed**: Opening the agents view from a foreground session now requires a single `←` press instead of two, matching background sessions

---

### v2.1.195 (2026-06-26)

> Bug fixes: hook exact-match for hyphenated names, voice dictation, background agent daemons, plugin name mismatch; Remote provisioning checklist.

- **Fixed**: Hook matchers with hyphenated identifiers (e.g. `code-reviewer`, `mcp__brave-search`) accidentally substring-matching; they now exact-match. Use `mcp__brave-search__.*` to match all tools from a hyphenated MCP server
- **Fixed**: Voice dictation on macOS capturing silence in long sessions after default input device changes; auto-submit never firing for languages without spaces (Japanese, Chinese, Thai)
- **Fixed**: Linux voice mode now distinguishes "no microphone" from "SoX not installed" when SoX is present
- **Fixed**: External plugins enabled only by project `.claude/settings.json` not requiring install consent on every loader path
- **Fixed**: `/plugin` Enable/Disable not working when a plugin's `plugin.json` `name` differs from its marketplace entry name
- **Fixed**: Background jobs disappearing from `claude agents` or losing data when written by a newer Claude Code version; daemon socket failures blocking restarts
- **Fixed**: Reopening a crashed background task showing blank screen for up to 5 seconds instead of its restart
- **Added**: `CLAUDE_CODE_DISABLE_MOUSE_CLICKS` to disable mouse click/drag/hover in fullscreen mode while keeping wheel scroll
- **Improved**: Remote session startup shows a provisioning checklist while the container starts
- **Improved**: `claude agents` completed list fills available vertical space; short terminals compact the header so live sessions stay visible

---

### v2.1.193 (2026-06-25)

> ⭐ New `claude_code.assistant_response` OTel event (review if you log prompts); `autoMode.classifyAllShell`; live path autocomplete in bash mode.

- **New**: `claude_code.assistant_response` OpenTelemetry log event carries model response text; redacted unless `OTEL_LOG_ASSISTANT_RESPONSES=1`; deployments already logging prompt content start receiving response content on upgrade (set `OTEL_LOG_ASSISTANT_RESPONSES=0` to keep prompts-only)
- **New**: `autoMode.classifyAllShell` setting routes all Bash/PowerShell commands through the auto-mode classifier (not just arbitrary-code-execution patterns)
- **New**: Auto-mode denial reasons added to the transcript, the denial toast, and `/permissions` recent denials
- **New**: Live file path autocomplete in bash mode (`!`) commands
- **New**: Startup notice when MCP servers need authentication, pointing to `/mcp`
- **New**: Automatic memory-pressure reaping for idle background shell commands (disable: `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`)
- **Improved**: Background agents: launch result no longer instructs Claude to "end your response"; Claude keeps working on other tasks while the agent runs
- **Improved**: MCP `headersHelper` auth: the helper re-runs and reconnects automatically when a tool call returns 401/403
- **Improved**: Plugin auto-rename: marketplace `renames` maps are followed automatically, updating settings to the new name
- **Improved**: `/add-dir` message when the directory is already a working directory
- **Fixed**: `/model` and other client-data-gated UI showing stale/empty state immediately after `/login`; backgrounding spuriously cancelling; pinned background agents re-prompted after auto-update; phantom "general-purpose (resumed)" subagent re-running main conversation; agent panel hiding sibling agents when viewing a subagent

---

### v2.1.191 (2026-06-24)

> ⭐ `/rewind` now works after `/clear`; ~37% CPU reduction during streaming; MCP reliability improvements; 20+ bug fixes.

- **New**: `/rewind` can now resume a conversation from before `/clear` was run
- **Improved**: CPU usage during streaming reduced by ~37% by coalescing text updates to 100ms intervals instead of per-token
- **Improved**: Sandbox network permission dialog: hosts allowed with "Yes" are remembered for the rest of the session (no re-prompting per connection)
- **Improved**: MCP server capability discovery (`tools/list`, `prompts/list`, `resources/list`) retries transient network errors with short backoff
- **Improved**: MCP OAuth: discovery and token requests retry once after transient errors; headless environments skip the browser popup and go straight to paste-the-URL prompt
- **Improved**: MCP error messages: HTTP 404 errors now show the URL and point to your MCP config
- **Improved**: Vim mode prompt-history search (NORMAL `/`) hints how to reach slash commands
- **Fixed**: Background agents resurrecting after being stopped from the tasks panel; stopping is now permanent
- **Fixed**: Scroll position jumping to the bottom while reading earlier output during a streaming response
- **Fixed**: `/voice` showing a generic "not available" message when disabled by org policy, with a proper explanation of the restriction
- **Fixed**: Welcome splash art overflowing the default 80×24 macOS Terminal window; `/login` URL truncated in Windows Terminal wrap; Cmd+click links in fullscreen Ghostty over ssh/tmux
- **Fixed**: Hooks with comma-separated matchers (e.g. `"Bash,PowerShell"`) silently never firing
- **Fixed**: `/permissions` Recently-denied tab: approving a denial now persists on close
- **Fixed**: `claude agents` sending builtin slash commands like `/usage` to background sessions as prompt text; job rows showing full filesystem paths for pasted images instead of `[Image #N]`
- **Fixed**: Managed settings: `forceRemoteSettingsRefresh` now takes effect via MDM/file policy with `Cache-Control: no-cache` on fetch

---

### v2.1.190 (2026-06-24)

> Bug fixes and reliability improvements.

---

### v2.1.187 (2026-06-23)

> ⭐ `sandbox.credentials` blocks credential files from sandboxed commands; org model restrictions in all model selection surfaces; MCP 5-minute hang fixed; 15+ bug fixes.

- **New**: `sandbox.credentials` setting: when enabled, blocks sandboxed commands from reading credential files (`.aws/credentials`, `.ssh/`, etc.) and secret environment variables
- **New**: Org-configured model restrictions enforced in the model picker, `--model`, `/model`, and `ANTHROPIC_MODEL`; shows "restricted by your organization's settings" when a restricted model is selected
- **Fixed**: Remote MCP tool calls hanging with no response for 5 minutes now abort with an error; override with `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`
- **Fixed**: `--resume` failing with "No conversation found" when the original `-p` run produced no model turns
- **Fixed**: `--json-schema` and workflow `agent({schema})` structured output: model can no longer re-call `StructuredOutput` indefinitely after a successful call; follow-up turns now reliably return structured output
- **Fixed**: Remote sessions (Remote Control) taking ~2.7s longer to start after CA system-trust install
- **Fixed**: Pasted Korean/CJK text turning into mojibake in terminals delivering paste as per-byte extended-key events
- **Fixed**: Background jobs in the agents view stuck in "working" indefinitely when the agent ended a turn without structured output
- **Fixed**: Channel connections dropping after navigating to agents view and back, and after `/bg`, `/tui`, or `/update`
- **Fixed**: Agent stop notifications wording improved to "finished"/"stopped"; subagent depth tracking restored on resume; leaked agent worktree registrations cleaned up automatically
- **Fixed**: `claude --help` not listing `--bg`/`--background`; Esc/Ctrl-C/Ctrl-D not working while `/share` is uploading
- **Improved**: `/install-github-app`: GitHub Actions workflow setup is now optional; install just the app and skip the workflow/secret steps
- **Improved**: `/btw` with ←/→ arrow navigation through earlier answers; `/plugin` surfaces recently-unused plugins for cleanup

---

### v2.1.186 (2026-06-23)

> ⭐ `claude mcp login/logout` for CLI-based MCP auth; `!` bash commands now auto-trigger Claude; background subagents surface permission prompts instead of auto-denying; 25+ bug fixes.

- **New**: `claude mcp login <name>` and `claude mcp logout <name>` authenticate MCP servers directly from the CLI without opening the interactive `/mcp` menu; `--no-browser` flag supports stdin redirect for SSH sessions
- **New**: `!` bash commands now trigger Claude to respond to the output automatically; set `"respondToBashCommands": false` in settings.json to keep the previous context-only behavior
- **New**: Status filtering (press `f`) in the `/workflows` agent detail view; "Skills" section added to `/plugin` Installed tab
- **New**: `teammateMode: "iterm2"` setting with warning when auto mode cannot find the `it2` CLI; "Claude Platform on AWS - refresh credentials" option added to `/login`
- **Changed**: Background subagents now surface permission prompts in the main session instead of auto-denying; the dialog shows which agent is asking, and Esc denies just that tool
- **Changed**: `/review <pr>` now uses the same review engine as `/code-review medium`
- **Changed**: `CLAUDE_CODE_MAX_RETRIES` capped at 15; use `CLAUDE_CODE_RETRY_WATCHDOG` for unattended sessions
- **Fixed**: `Agent(type)` deny rules and `Agent(x,y)` allowed-types restrictions not being enforced for named subagent spawns
- **Fixed**: Streaming requests failing with "Content block not found" or JSON parse errors after machine wake from sleep
- **Fixed**: Workflow `agent({schema})` subagents looping forever on repeated schema validation failures instead of aborting after 5 attempts
- **Fixed**: Background session recaps being duplicated; background task previews flashing raw tool names before agent plan loaded
- **Fixed**: Esc and Ctrl+C not responding while background agents are still running after the main turn ends; 15+ additional UI bug fixes

---

### v2.1.185 (2026-06-22)

> Stream-stall hint UX improvement: clearer message and longer delay before triggering.

- **Improved**: Stream-stall hint now reads "Waiting for API response · will retry in …" instead of "No response from API · Retrying in …", and triggers after 20s of silence instead of 10s

---

### v2.1.183 (2026-06-19)

> ⭐ Auto mode safety improvements block destructive git/terraform commands unless explicitly requested; model deprecation warnings; `attribution.sessionUrl` setting; 10+ bug fixes.

- **New**: Auto mode now blocks destructive git commands (`reset --hard`, `checkout -- .`, `clean -fd`, `stash drop`) when you didn't ask to discard local work; `git commit --amend` is blocked when the commit wasn't made by the agent this session; `terraform destroy`/`pulumi destroy`/`cdk destroy` are blocked unless you asked for the specific stack
- **New**: Warning added when the requested model is deprecated or auto-updated to a newer model, shown on stderr in print mode (`-p`) and now covering models set in agent frontmatter
- **New**: `attribution.sessionUrl` setting omits the claude.ai session link from commits and PRs in web and Remote Control sessions
- **New**: `/config --help` lists all available shorthand keys for `/config key=value`
- **Changed**: `/config` toggle: Enter and Space both change the selected setting; Esc now saves and closes instead of reverting
- **Changed**: Startup "setup issues" line removed from under the logo; run `/doctor` or use `--debug` to surface configuration issues
- **Fixed**: `thinking.disabled.display: Extra inputs are not permitted` 400 errors on subagent spawns and session-title generation for affected configurations
- **Fixed**: WebSearch returning empty results in subagents
- **Fixed**: Terminal cursor stranded above the prompt after navigating history in vim mode with native cursor enabled
- **Fixed**: Fullscreen TUI corruption (statusline mid-screen, duplicated spinner rows, merged text) in Windows Terminal under heavy nested-subagent load
- **Fixed**: Turns silently completing with no visible output when the model returned only a thinking block; Claude now re-prompts once
- **Fixed**: User-level skills appearing multiple times in slash-command autocomplete when multiple plugins are enabled
- **Fixed**: MCP servers requiring authentication exposing auth-stub tools to the model in headless/SDK mode
- **Fixed**: tmux teammate panes failing to launch when the shell has slow rc-file initialization; keystrokes typed during agent spawn no longer leak into the new pane
- **Fixed**: Background tasks started by a teammate being killed when the teammate finishes a turn
- **Fixed**: Scheduled task and webhook trigger deliveries treated as keyboard input; they now classify as task notifications and can no longer approve a pending action or set the session title in auto mode
- **Fixed**: Focus mode showing "Ran N PostToolUse hooks" timing lines under each response

---

### v2.1.181 (2026-06-18)

> ⭐ `/config key=value` inline setting syntax, improved streaming + subagent panel, 30+ bug fixes.

- **New**: `/config key=value` syntax sets any setting inline from the prompt (e.g. `/config thinking=false`), works in interactive, `-p`, and Remote Control
- **New**: `sandbox.allowAppleEvents` opt-in lets sandboxed commands send Apple Events on macOS; `CLAUDE_CLIENT_PRESENCE_FILE` suppresses mobile push notifications while at the machine
- **Improved**: Streaming: long paragraphs now appear line-by-line instead of waiting for the first line break
- **Improved**: Subagent panel: idle agents auto-hide after 30s, list caps at 5 rows with scroll hints, keyboard hints now show in the footer
- **Improved**: Auto-retry: API connection drops mid-thinking now automatically retry instead of showing "Connection closed while thinking"
- **Changed**: Fullscreen mode URL opening now requires Cmd+click (macOS) / Ctrl+click, matching native terminal behavior
- **Fixed**: Prompt caching not reading on custom `ANTHROPIC_BASE_URL` and Foundry due to per-request attestation token changing every turn
- **Fixed**: Write/Edit producing 0-byte or truncated files on network drives and cloud-synced folders
- **Fixed**: Startup regression (~120ms per launch in fresh environments, introduced in 2.1.169); startup no longer blocks up to 15 seconds on degraded networks
- **Fixed**: macOS TUI freezing at session start (Ctrl+C unresponsive) when Spotlight is busy reindexing
- **Fixed**: `open`, `osascript`, and browser-based auth flows failing with error -600 on macOS (added Apple Events entitlement)
- **Fixed**: Foreground subagents spawning unbounded nested chains; they now respect the same 5-level depth limit as background subagents
- **Fixed**: `/recap` and conversation forks using the previous model immediately after a model switch
- **Fixed**: 20+ additional fixes: long-running idle session history loss, AWS credential refresh loop, `claude mcp get/list` showing wrong status, `/remote-control` stale "connecting…" line, `/stats` timezone off-by-one, `AskUserQuestion` word-wrap and multi-select free-text, tab-indented code preview indentation

---

### v2.1.179 (2026-06-17)

> Bug fixes: mid-stream connection drops, WSL2 mouse-wheel scrolling, sandbox glob performance, feedback survey, welcome banner.

- **Fixed**: Mid-stream connection drops now preserve partial responses instead of showing a raw error; the spinner no longer gets stuck at "running tool"
- **Fixed**: Mouse-wheel scrolling in WSL2 under Windows Terminal and VS Code (regression introduced in 2.1.172)
- **Fixed**: Sandbox `denyRead`/`allowRead` glob over a large directory tree making the Bash tool description enormous and the session unusable on Linux
- **Fixed**: Feedback survey capturing a single-digit reply as a session rating immediately after a turn completes
- **Fixed**: Welcome screen stacking multiple promotional banners; at most one promo now shows per session
- **Fixed**: Ctrl+O not showing the subagent's transcript when viewing a subagent
- **Fixed**: Clicking the prompt input not returning focus from the subagent/footer panel
- **Fixed**: Remote session background tasks appearing stuck as "still running" between turns
- **Improved**: Plugin loading performance in remote sessions

---

### v2.1.178 (2026-06-17)

> ⭐ `Tool(param:value)` permission syntax, nested `.claude/` directory improvements, auto mode subagent pre-classification, 10+ bug fixes.

- **New**: `Tool(param:value)` syntax for permission rules to match a tool's input parameters (with `*` wildcard), e.g. `Agent(model:opus)` to block Opus subagents
- **New**: Skills in nested `.claude/skills` directories now load when working on files there; on a name clash, the nested skill appears as `<dir>:<name>` so both stay available
- **New**: Nested `.claude/` directories: the agent, workflow, and output-style closest to the working directory wins on name collision; project-scope workflow saves now target the closest existing `.claude/workflows/`
- **Improved**: Auto mode: subagent spawns are now evaluated by the classifier before launch, closing a gap where a subagent could request a blocked action without review
- **Improved**: `/doctor` with consistent flat tree layout across all sections, clearer section status icons, and highlighted command names
- **Improved**: Skill listing truncation warning now shows how many skill descriptions are affected
- **Changed**: Workflow prompt keyword uses a purple shimmer highlight and triggers only on explicit phrases like "run a workflow" or "workflow:", not on any mention of the word
- **Improved**: Remote Control error messages: connection failures now show a persistent red "/rc failed" indicator in the footer; "not yet enabled" error explains whether it's a gate, check failure, stale entitlement, or org policy
- **Changed**: `/bug` now requires a description before submitting; no longer uses model-refusal text as the GitHub issue title
- **Fixed**: Crash (out-of-memory) when the CLI inherits a stale websocket/OAuth file-descriptor environment variable from a parent process
- **Fixed**: Claude in Chrome silently failing to connect when the OAuth token belongs to a different account than Claude Code
- **Fixed**: Nested `.claude/skills` with directory-qualified names blocked by permission prompts in non-interactive runs
- **Fixed**: Subagent transcript view now shows tool results and live progress; messages sent while it finishes are no longer dropped; backgrounding a running subagent (ctrl+b) no longer restarts it from scratch
- **Fixed**: `claude agents` workers failing with `401 Invalid bearer token` when started from a shell with a custom API gateway via `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN`
- **Fixed**: Compaction not honoring `--fallback-model`: compaction now falls back to the configured fallback model chain on overload or model-availability errors
- **Fixed**: Model requests continuing to fail with auth errors after credentials were refreshed outside the session (stale cached request configuration)
- **Fixed**: Background sessions created with `/bg` or `←←` after a turn finished showing "Working" forever in the agents list
- **Fixed**: Linux sandbox failing to start when `.claude/skills` or `.claude/hooks` is a symlink
- **Fixed**: `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` preventing fresh marketplace installs from cloning
- **Fixed**: MCP server-level specs (`mcp__server`, `mcp__server__*`, `mcp__*`) in subagent `disallowedTools` being silently ignored
- **Fixed**: Vim mode undo: `u` now steps through NORMAL/VISUAL-mode commands one at a time instead of merging quick-succession commands into a single undo step
- **Fixed**: Statusline links with custom URI schemes (e.g. `vscode://`) not opening when clicked in `claude agents`
- **Fixed**: [VSCode] Pressing Esc to dismiss a CJK IME candidate window canceling the running Claude task

---

### v2.1.176 (2026-06-15)

> ⭐ Session titles in conversation language, `footerLinksRegexes` setting, Bedrock credential caching improvement, 15+ bug fixes.

- **New**: Session titles are now generated in the language of your conversation; set the `language` setting to pin a specific language
- **New**: `footerLinksRegexes` setting for regex-matched link badges in the footer row, configurable via user or managed settings
- **Improved**: Bedrock credential caching: credentials from `awsCredentialExport` are now cached until their `Expiration` instead of a fixed 1 hour
- **Fixed**: `availableModels` enforcement: alias model picks can no longer be redirected to a blocked model via `ANTHROPIC_DEFAULT_*_MODEL` env vars; `/fast` now refuses to toggle when it would switch to a blocked model
- **Fixed**: Auto mode failing on Fable 5 for organizations without Opus 4.8 enabled (the classifier now falls back to the best available Opus model)
- **Fixed**: Hook `if` conditions for Read/Edit/Write tool paths: patterns like `Edit(src/**)`, `Read(~/.ssh/**)`, and `Read(.env)` now match correctly
- **Fixed**: Linux sandbox failing to start when `.claude/settings.json` is a symlink with an absolute target
- **Fixed**: `/copy` and mouse-selection copy not reaching the system clipboard inside tmux over SSH; tmux paste buffer not loading on versions older than 3.2
- **Fixed**: Remote Control connecting from web/mobile silently switching the session's model
- **Fixed**: Remote Control disconnect notifications showing a bare numeric code instead of a human-readable reason; connection failures adding a duplicate line to the transcript
- **Fixed**: Remote Control sessions not disconnecting when signing in to a different account
- **Fixed**: `/cd` and worktree moves leaving the session reporting the previous directory's git branch
- **Fixed**: `claude agents`: pressing back in one window no longer detaches other windows attached to the same session
- **Fixed**: Backgrounded sessions showing "Working" forever when `/bg` mid-turn had nothing left to continue
- **Fixed**: Background agent search by PR URL for PRs opened during scheduled wakeups or while a job was blocked
- **Fixed**: Agents view input showing no text cursor on Windows
- **Fixed**: `claude --bg -cn <name>` not seeding the session name
- **Fixed**: Background sessions to neutralize Windows network paths in persisted state before respawn
- **Fixed**: Background-session respawn rejecting malformed resume IDs from corrupted state files
- **Fixed**: Windows background-service daemon not starting when `~/.claude/daemon` has the ReadOnly attribute set
- **Fixed**: Cloud sessions failing with "Could not resolve authentication method" when idle for too long before being claimed
- **Improved**: Background sessions now show clearer guidance when a window left open across an auto-update can't submit a reply; `claude daemon status` explains version-skew behavior

---

### v2.1.175 (2026-06-15)

> ⭐ `enforceAvailableModels` managed setting for enterprise model control.

- **New**: `enforceAvailableModels` managed setting: when enabled, the `availableModels` allowlist also constrains the Default model (a Default that would resolve to a disallowed model now falls back to the first allowed model), and user or project settings can no longer widen a managed `availableModels` list

---

### v2.1.174 (2026-06-15)

> `wheelScrollAccelerationEnabled` setting, improved `/model` picker, VS Code usage attribution, 8+ bug fixes.

- **New**: `wheelScrollAccelerationEnabled` setting to disable mouse-wheel scroll acceleration in fullscreen mode
- **Fixed**: `/model` picker hiding the model family that Default resolves to. Opus now appears as its own row on Max/Team Premium/Enterprise plans, Sonnet on Pro/Team plans, and Opus on pay-as-you-go API accounts
- **Fixed**: `/model` picker showing a hardcoded Sonnet version label when `ANTHROPIC_DEFAULT_SONNET_MODEL` pins a different Sonnet
- **Fixed**: "Fable 5 is now consuming usage credits" banner incorrectly showing for enterprise accounts with usage-based billing
- **Fixed**: Bedrock GovCloud regions (`us-gov-*`) deriving the wrong inference profile prefix (`global` instead of `us-gov`), causing 400 errors on derived model IDs
- **Fixed**: Background sessions inheriting another session's `ANTHROPIC_*` provider env (gateway URL, custom headers, `/model` aliases) from the shell that started the background daemon
- **Fixed**: 1-2 second pause when exiting Claude Code shortly after a shell command was interrupted or killed on macOS and Linux
- **Fixed**: Git commit co-author attribution showing an incorrect model name for some models
- **Fixed**: `/advisor` dialog pre-selecting a saved advisor model that is blocked by the `availableModels` allowlist
- **Fixed**: Skill hot-reload re-sending the entire skill listing when a single skill changed (only changed skills are now re-announced)
- **Fixed**: Workflow tool `agent()` subagents missing per-agent attribution headers
- **Fixed**: Pre-warmed background workers failing with "Could not resolve authentication method" when claimed after sitting idle
- **New [VSCode]**: Usage attribution in the Account & usage dialog (`/usage`) showing cache misses, long context, subagents, and per-skill/agent/plugin/MCP breakdowns over the last 24h or 7d

---

### v2.1.173 (2026-06-11)

> Bug fixes: Fable 5 `[1m]` suffix normalization, Windows sandbox warning fix.

- **Fixed**: Fable 5 model names with a `[1m]` suffix not being normalized (Fable 5 includes 1M context by default, suffix now stripped automatically)
- **Fixed**: Spurious "sandbox dependencies missing" startup warning on Windows when sandbox was enabled in settings

---

### v2.1.172 (2026-06-11)

> ⭐ Sub-agents can spawn sub-agents (5 levels deep), Bedrock region auto-detection, plugin search bar, 20+ bug fixes.

- **New**: Sub-agents can now spawn their own sub-agents up to 5 levels deep
- **New**: Amazon Bedrock now reads the AWS region from `~/.aws` config files when `AWS_REGION` isn't set, matching AWS SDK precedence; `/status` shows where the region came from
- **New**: Added a search bar when browsing a marketplace's plugins in `/plugin`
- **New**: Added `model` attribute to the `claude_code.lines_of_code.count` OTEL metric
- **Fixed**: Sessions using 1M context without usage credits getting permanently stuck; the session now automatically compacts back under the standard context limit
- **Fixed**: Repeating "an image in the conversation could not be processed and was removed" error when the conversation contained multiple images
- **Fixed**: Agents view keeping a session under "Working" with a busy spinner for up to 30 seconds after the worker replied
- **Fixed**: Background agents potentially reading another directory's project settings when dispatched onto a pre-warmed worker
- **Fixed**: Background-session attach failing with EAUTH for sessions started on an older version after the daemon auto-updated
- **Fixed**: A background sub-agent staying stuck as "active" in the agent panel after a nested agent it spawned was stopped
- **Fixed**: `/model` suggestions rendering with a misleading slash prefix and showing models disabled for your org
- **Fixed**: `availableModels` restrictions not being applied to subagent model overrides, the agent dispatch model picker, and the advisor model
- **Fixed**: `availableModels` allowlists hiding the `/model` picker's Opus and Sonnet 1M rows when entries use version-specific IDs like `claude-opus-4-8`
- **Fixed**: `/model` picker on Bedrock offering models the provider doesn't serve — selecting one silently switched the session model and lit the selection marker on multiple rows
- **Fixed**: Model IDs getting a doubled 1M-context suffix (e.g. `[1M][1m]`) when `ANTHROPIC_DEFAULT_OPUS_MODEL` already includes one
- **Fixed**: `opusplan` model setting not shipping with 1M context in plan mode for entitled users; the `opusplan[1m]` workaround now also correctly switches to Opus in plan mode
- **Fixed**: `WebFetch(domain:*.example.com)` wildcard domain rules never matching subdomains; file permission rules with mid-pattern wildcards (e.g. `Read(secrets-*/config.json)`) rejected at startup
- **Fixed**: Up-arrow prompt history showing the main agent's prompts while a subagent's chat tab is open
- **Fixed**: Memory recall not finding mounted team memory stores (`CLAUDE_MEMORY_STORES`) in remote sessions
- **Fixed**: Workflow validation rejecting scripts whose prompt strings or comments mention `Date.now()`/`Math.random()`
- **Fixed**: Mouse tracking on Windows consoles that don't fully support it
- **Fixed**: `/plugin` marketplace list losing its cursor after backing out of a long list; Esc from the plugin browser returning to the wrong tab
- **Improved**: Performance in long conversations (removed redundant message normalization, fewer full message-history transforms)
- **Improved**: Reduced idle CPU usage — `/goal` status chip no longer re-renders the terminal at 5 Hz while idle
- **Improved**: Claude in Chrome browser tools now load in a single batched call instead of one per tool
- **Improved**: Non-interactive Usage Policy refusal message suggests starting a new session or changing the model
- **Improved**: `/code-review` keeps the `ultra` option visible when not signed in to claude.ai, with an explanation
- **Improved**: Remote Control footer indicator shortened to "/rc active", hidden on narrow terminals
- **Improved**: Stopped promoting `/loop` in remote sessions, where pending loops don't keep the container alive
- **Fixed [VSCode]**: PowerShell tool calls rendered as raw JSON instead of a proper command display; ANSI escape codes stripped from displayed shell output

---

### v2.1.170 (2026-06-09)

> ⭐ Claude Fable 5 (Mythos-class model) access, transcript fix for VS Code terminal sessions.

- **New**: Claude Fable 5 is now available: a Mythos-class model exceeding the capabilities of any previously generally available Anthropic model. See [announcement](https://www.anthropic.com/news/claude-fable-5-mythos-5).
- **Fixed**: Sessions launched from the VS Code integrated terminal (or any shell that inherited Claude Code environment variables) were not saving transcripts and not appearing in `--resume`

---

### v2.1.169 (2026-06-09)

> ⭐ `--safe-mode` flag, `/cd` command, `disableBundledSkills` setting, 15+ bug fixes.

- **New**: `--safe-mode` flag (and `CLAUDE_CODE_SAFE_MODE` env var): starts Claude Code with all customizations disabled (CLAUDE.md, plugins, skills, hooks, MCP servers) for troubleshooting
- **New**: `/cd` command: move a session to a new working directory without breaking the prompt cache mid-session
- **New**: `disableBundledSkills` setting and `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` env var to hide built-in skills, workflows, and slash commands from the model
- **Fixed**: Arrow keys jumping to command history past wrapped rows of a long input line; they now move through each visual row first
- **Fixed**: Enterprise managed MCP policies (`allowedMcpServers`/`deniedMcpServers`) not enforced on reconnect, IDE-typed configs, `--mcp-config` servers during first session after install, or before remote settings loaded
- **Fixed**: ~30-50ms UI stall at the start of each turn for macOS users logged in with claude.ai credentials
- **Fixed**: `claude -p` slow or hanging on Windows while waiting for slash-command/skill scan (regression since 2.1.161)
- **Fixed**: Remote Control getting stuck on "reconnecting" after OAuth token refresh during session resume
- **Fixed**: Git Credential Manager "Connect to GitHub" popup on Windows at startup
- **Fixed**: Footer hints (e.g. "esc to interrupt") not showing for users with a custom statusline
- **Fixed**: `claude agents --json` omitting blocked and just-dispatched background sessions; added `--all` to include completed sessions plus new `id` and `state` fields
- **Fixed**: Background agents ignoring project-level `env` values (e.g. `ANTHROPIC_MODEL`) when dispatched onto a pre-warmed worker
- **Improved**: `TaskCreate` reliability: malformed inputs are repaired automatically; validation errors for unloaded tools include the schema
- **Improved**: Reduced CPU usage while responses stream and during spinner animations
- **Improved**: `/workflows` now opens immediately even while a turn is in progress

---

### v2.1.168 (2026-06-06)

> Bug fixes and reliability improvements.

---

### v2.1.167 (2026-06-06)

> Bug fixes and reliability improvements.

---

### v2.1.166 (2026-06-06)

> `fallbackModel` setting, deny rule glob patterns, thinking disable on default-thinking models, hardened `SendMessage`, 15+ bug fixes.

- **New**: `fallbackModel` setting: configure up to 3 fallback models tried in order when the primary model is overloaded or unavailable; `--fallback-model` also works in interactive sessions
- **New**: Glob pattern support in deny rule tool-name position (`"*"` denies all tools); allow rules reject non-MCP globs; unknown tool names in deny rules warn at startup
- **Security**: Hardened cross-session messaging: messages relayed via `SendMessage` no longer carry user authority; receivers refuse relayed permission requests and auto mode blocks them
- **Changed**: `MAX_THINKING_TOKENS=0`, `--thinking disabled`, and per-model thinking toggle now disable thinking on models that think by default via the Claude API (3P providers unchanged)
- **Changed**: Claude Code retries a turn once on the fallback model when the API rejects unexpected non-retryable errors; auth, rate-limit, request-size, and transport errors still surface immediately
- **Changed**: `claude update` now announces the target version before downloading
- **New**: `claude agents`: typing a URL into the list filters to the session whose first prompt contained it
- **Fixed**: Background sessions becoming stuck when a backend disruption occurred during worker registration at startup
- **Fixed**: JetBrains IDE terminal flickering (IntelliJ, PyCharm, WebStorm) on 2026.1+, synchronized output enabled
- **Fixed**: Shift+non-ASCII characters (e.g. Shift+ä → Ä) dropped in terminals using the Kitty keyboard protocol (WezTerm, Ghostty, kitty)
- **Fixed**: PowerShell command validation hanging on Windows when a killed process's children held output pipes
- **Fixed**: Orphaned `claude --bg-pty-host` processes spinning at 100% CPU on macOS after daemon death
- **Fixed**: Managed settings with an invalid entry silently disabling remaining valid policies
- **Fixed**: `allowedMcpServers`/`deniedMcpServers` predicates not matching with `${VAR}` references
- **Fixed**: Background agent sessions in git worktrees crash-looping with "No conversation found" when reopened
- **Fixed**: Duplicated thinking text in the Ctrl+O transcript view while streaming

---

### v2.1.165 (2026-06-05)

> Bug fixes and reliability improvements.

---

### v2.1.163 (2026-06-04)

> `requiredMinimumVersion`/`requiredMaximumVersion` managed settings, `/plugin list`, Stop hook `additionalContext`, 10+ bug fixes.

- **New**: `requiredMinimumVersion` and `requiredMaximumVersion` managed settings: Claude Code refuses to start if its version is outside the allowed range and directs the user to an approved version
- **New**: `/plugin list` command to list installed plugins, with `--enabled`/`--disabled` filters
- **New**: Added "c to copy" shortcut to `/btw`, copies the raw markdown answer to the clipboard
- **Changed**: Stop and SubagentStop hooks can now return `hookSpecificOutput.additionalContext` to give Claude feedback and keep the turn going without being labeled a hook error
- **Changed**: Skills: added `\$` escape syntax to include a literal `$` before a digit in command bodies
- **Changed**: stdio MCP servers now receive the same `CLAUDE_CODE_SESSION_ID` as hooks/Bash on `--resume`
- **Fixed**: `claude -p` hanging forever after its final result when a backgrounded command never exits; background shells stopped ~5s after result once stdin closes
- **Fixed**: `claude -p` failing with "ANTHROPIC_API_KEY required" on Bedrock/Vertex/Foundry when `CI=true` and no Anthropic API key is set
- **Fixed**: Bash commands failing under bazel and EDR-protected Go workflows: `$TMPDIR` was overridden to `/tmp/claude-{uid}` for all commands, not just sandboxed ones (regression since 2.1.154)
- **Fixed**: Bash commands failing on Windows with "EEXIST: file already exists" on the session-env directory when inside OneDrive or with read-only attribute
- **Fixed**: Org-managed permission rules not applying when managed settings fetch completed during startup on a fresh config directory
- **Fixed**: Background sessions losing running background tasks when reattached after a Claude Code update
- **Fixed**: Terminal misalignment and multi-second hang when exiting the agent view with Esc
- **Fixed**: Hook `if: "Bash(...)"` conditions firing on every Bash command containing `$()` or `$VAR`

---

### v2.1.162 (2026-06-03)

> Quieter startup, agents `waitingFor`, slash-command fill-in, Windsurf renamed to Devin Desktop, 25+ bug fixes.

- **New**: `claude agents --json` now includes `waitingFor` showing what a waiting session is blocked on (e.g. permission prompt)
- **New**: `--tools`: explicitly listing `Grep`/`Glob` now provides the dedicated search tools on native builds with embedded search
- **New**: `/effort` now confirms when your chosen level will persist as the default for new sessions
- **Changed**: Clicking a slash command in the autocomplete menu fills it into the prompt instead of running it immediately; press Enter to run
- **Changed**: Remote Control now shows as a persistent footer pill (with a link to the session) instead of a startup message
- **Changed**: Renamed Windsurf to Devin Desktop in `/ide`, `/terminal-setup`, and `/scroll-speed`, following the editor's rebrand
- **Fixed**: Silent startup hang when config directory is read-only; Claude Code now starts with in-memory config and surfaces errors
- **Fixed**: `WebFetch` permission rules not applied to built-in preapproved domains; explicit `deny`/`ask`/`allow` rules now take precedence
- **Fixed**: Windows permission rules never matching backslash-spelled paths (`~\`, `\\server\share`) or case-variant paths
- **Fixed**: MCP per-server `timeout` values below 1000 ms being floored to a 1-second watchdog that aborted every tool call
- **Fixed**: LSP `workspaceSymbol` operation returning no results; now accepts a `query` parameter
- **Fixed**: `claude agents` cutting live status text at 60-120 columns on wide terminals; truncating session names at 40 columns
- **Fixed**: `claude agents` Ctrl+V image paste doing nothing in dispatch input and session reply box
- **Fixed**: Cross-session messaging (`SendMessage`) silently breaking with deep `CLAUDE_CODE_TMPDIR` or `$TMPDIR` paths
- **Improved**: Quieter startup: notices group by severity, session info and announcements share a single line per launch
- **Improved**: Background service startup and `claude update` verification wait out endpoint-security scanning instead of failing after 5 seconds
- **Removed**: "Claude in Chrome enabled" and "marketplace installed" startup messages; model auto-updates and team-onboarding tip now show as quiet notices

---

### v2.1.161 (2026-06-02)

> OTEL custom dimensions, `done/total` in agents view, parallel tool-call isolation, 20+ bug fixes.

- **New**: `OTEL_RESOURCE_ATTRIBUTES` values included as labels on metric datapoints for custom dimensions (team, repo)
- **New**: `claude agents` rows show `done/total` before the detail when work is fanned out; peek shows the longest-running item
- **New**: `/mcp` collapses claude.ai connectors you've never signed in to behind a "Show unused connectors" row
- **Changed**: Parallel tool calls: a failed Bash command no longer cancels other calls in the same batch; each tool returns its own result independently
- **Improved**: Fullscreen mode clipboard on Linux uses `wl-copy`/`xclip`/`xsel` when available; copies to clipboard and PRIMARY selection for middle-click paste
- **Improved**: Terminal rendering performance by stabilizing the layout engine's JIT compilation profile; rendering performance for large file writes
- **Fixed**: `/effort` dialog, workflow animations, and prompt keyword shimmer not honoring "Reduce motion" setting
- **Fixed**: `forceLoginOrgUUID`/`forceLoginMethod` managed-settings policies blocking third-party provider sessions (regression in 2.1.146)
- **Fixed**: Background subagent output corrupting `claude -p` stdout with `--output-format text` or `json`
- **Fixed**: `claude mcp` list/get/add printing secrets to terminal; `${VAR}` references no longer expanded, credential headers and URL secrets redacted
- **Fixed**: Workflow agents with `isolation: "worktree"` in background sessions blocked from editing files inside their own worktree
- **Fixed**: Background sessions dispatched from `claude agents` booting on stale model from daemon environment instead of `settings.json`
- **Fixed**: OpenTelemetry log events dropped when emitted before telemetry initialization completed
- **Fixed**: Completed subagents getting stuck showing as running when an error occurs while finalizing their result
- **Added**: [VSCode] Tip suggesting disabling terminal GPU acceleration (or running `/terminal-setup`) to fix garbled glyphs

---

### v2.1.160 (2026-06-01)

> `ultracode` replaces `workflow` keyword, security prompts for startup files, Edit after grep, 20+ bug fixes.

> **Breaking**: The dynamic-workflow trigger keyword changed from `workflow` to `ultracode`. The word "workflow" no longer triggers a run; asking for one in your own words still works. The trigger keyword is highlighted in violet in the prompt input.

- **Changed**: Renamed dynamic-workflow trigger keyword from `workflow` to `ultracode`; violet shimmer in prompt input; asking in your own words still works
- **Security**: Added prompt before writing to shell startup files (`.zshenv`, `.zlogin`, `.bash_login`) and `~/.config/git/`, which could otherwise lead to unintended command execution
- **Security**: `acceptEdits` mode now prompts before writing build-tool config files that grant code execution (`.npmrc`, `.yarnrc*`, `bunfig.toml`, `.bazelrc`, `.pre-commit-config.yaml`, `.devcontainer/`)
- **Improved**: Edit no longer requires a separate Read after viewing a file with `grep`; single-file `grep`/`egrep`/`fgrep` commands now satisfy the read-before-edit check
- **Improved**: Auto mode classifier latency reduced by lowering reasoning on routine actions; fewer "could not evaluate this action" blocks
- **Improved**: Background-session teardown sends SIGTERM to running shell subprocesses before SIGKILL so cleanup handlers run
- **Removed**: `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` (deprecated in 2.1.154; now a no-op)
- **Removed**: JetBrains plugin install suggestion from startup
- **Fixed**: 20+ bug fixes: WSL clipboard via PowerShell interop, completed sessions from `claude agents` dropping chat history, overnight retired sessions losing conversation, voice mode with non-ASCII project/branch names, auto mode unavailability message on third-party providers, past replies disappearing on brief mode resume, vim mode `p` paste position

---

### v2.1.159 (2026-05-31)

> Internal infrastructure improvements (no user-facing changes).

---

### v2.1.158 (2026-05-30)

> Auto mode on Bedrock, Vertex, and Foundry for Opus 4.7/4.8.

- **New**: Auto mode is now available on Bedrock, Vertex, and Foundry for Opus 4.7 and Opus 4.8; opt in by setting `CLAUDE_CODE_ENABLE_AUTO_MODE=1`

---

### v2.1.157 (2026-05-29)

> Plugin auto-loading from `.claude/skills` (no marketplace), `claude plugin init`, mid-session worktree switching, 20+ bug fixes.

- **New**: Plugins in `.claude/skills` directories are now automatically loaded, no marketplace required
- **New**: `claude plugin init <name>` scaffolds a new plugin directly in `.claude/skills`
- **New**: Autocomplete for `/plugin` arguments: subcommands, installed plugin names, and plugins from known marketplaces
- **New**: `claude agents`: the `agent` field in `settings.json` is now honored for dispatched sessions; use `--agent <name>` to override it
- **New**: `EnterWorktree` can now switch between Claude-managed worktrees mid-session
- **New**: `tool_decision` telemetry events now include `tool_parameters` (bash commands, MCP/skill names) when `OTEL_LOG_TOOL_DETAILS=1`
- **Improved**: Worktrees managed by Claude are left unlocked after the agent finishes, so `git worktree remove`/`prune` can clean them up
- **Improved**: Long and resumed conversations are faster due to eliminated redundant message-rendering recomputations
- **Improved**: `/terminal-setup` now disables GPU acceleration in VS Code/Cursor/Windsurf integrated terminals to prevent garbled-text rendering
- **Fixed**: Unprocessable images (zero-byte, corrupt) attached via paste, MCP, or dialog no longer crash the request; they become text placeholders
- **Fixed**: Sandbox network permission prompts no longer appear in auto and bypass-permissions mode for desktop app, IDE extensions, and SDK
- **Fixed**: Background agent worktrees under `.claude/worktrees/` no longer get orphaned after the 30-day job retention sweep
- **Fixed**: Background sessions re-attached after sleep/wake now report the correct date to the model
- **Fixed (regression 2.1.153)**: Copy-on-select in `claude agents` now reaches the system clipboard inside tmux with `set-clipboard on`
- **Fixed**: `--resume` now reports background subagents that were running when the previous Claude Code process exited
- **Fixed**: `--worktree` and `--worktree --tmux` now return to the correct linked worktree instead of the canonical repo root
- **Fixed**: `/model` picker no longer shows an incorrect "Newer version available" hint when the selected model is already the newest in its family
- **Fixed**: Right-click paste no longer duplicates the clipboard in VS Code, Cursor, and Windsurf integrated terminals
- **Fixed (WSL)**: Image paste (`alt+v`), screenshot paste on Windows 11, and dragging images from Windows Explorer now work correctly
- **Fixed**: Several `claude agents` issues: completed sessions not retiring, pressing Esc not cancelling "opening…", terminal freeze after managed-settings dialog
- **Fixed**: Literal markdown markers (backticks, asterisks) no longer appear in in-progress message text in fullscreen mode

---

### v2.1.156 (2026-05-28)

> Hotfix: Opus 4.8 API crash from modified thinking blocks.

- **Fixed**: An issue where thinking blocks were modified when using Opus 4.8, leading to API errors

---

### v2.1.154 (2026-05-28)

> Opus 4.8, dynamic workflows orchestrating hundreds of background agents, lean system prompt as default, 30+ bug fixes.

- **New (Model)**: Opus 4.8 is available and defaults to high effort; use `/effort xhigh` for your hardest tasks
- **New (Model)**: Fast mode on Opus 4.8 at 2x the standard rate for 2.5x the speed
- **New**: Dynamic workflows: Claude can orchestrate work across tens to hundreds of background agents in one session; run `/workflows` to monitor runs
- **New**: The lean system prompt is now the default for all models except Haiku, Sonnet, and Opus 4.7 and earlier
- **Changed**: `/simplify` now runs a cleanup-only review (reuse, simplification, efficiency, altitude) and applies the fixes, instead of running the full `/code-review --fix` bug-hunting review
- **Changed**: `/effort` slider labels renamed from "Speed"/"Intelligence" to "Faster"/"Smarter"
- **New**: `claude agents`: type `! <command>` to run a shell command as a background session you can attach and detach from; also available as `claude --bg --exec '<command>'`
- **New**: `claude agents`: `/logout` now signs you out instead of being sent to a background session
- **New**: `←←` to open the agents view now works on Bedrock, Vertex, Foundry, and with telemetry disabled
- **New**: Claude in Chrome: pick which connected browser to use via `/chrome` → "Select browser…", or in-chat when multiple browsers are connected
- **New**: Plugins can declare `defaultEnabled: false` in `plugin.json` or a marketplace entry; enable with `/plugin` or `claude plugin enable`
- **New**: The `/plugin` Discover tab pins plugins matching the current directory with a "suggested for this directory" annotation
- **New**: Streaming tool execution always enabled, including on Bedrock/Vertex/Foundry (previously behind a feature flag)
- **New**: Stdio MCP server subprocesses receive `CLAUDE_CODE_SESSION_ID` and `CLAUDECODE=1` in their environment
- **New**: `claude mcp list`/`get` now show unapproved `.mcp.json` servers as `⏸ Pending approval` instead of auto-approving
- **Improved**: Auto-mode classifier detection of data exfiltration improved, particularly for bulk repository transfers
- **Deprecated**: `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` (removed 2026-06-01); use `/model claude-opus-4-6[1m]` then `/fast on`
- **Fixed (VSCode)**: Claude Code processes not shutting down cleanly when VS Code closed on Windows
- **Fixed**: 30+ fixes including orphaned `--bg-pty-host` processes spinning at 100% CPU after daemon exit, number key shortcuts not working below the divider in option dialogs, `worktree.baseRef: "head"` resolving to wrong HEAD when spawning subagents from inside a linked worktree, intermittent rendering corruption in VS Code from thinking spinner colors, plan file names containing `[Image #N]`/`[Pasted text #N]` placeholders, phantom expand affordance on short ANSI-colored lines, invalid `allowedMcpServers`/`deniedMcpServers` entry discarding all managed-settings policy, API 400 errors on models without effort parameter when `CLAUDE_CODE_ALWAYS_ENABLE_EFFORT` is set, Windows update failure showing generic error, auto mode blocking actions when safety classifier ran out of output tokens while reasoning
- **Breaking**: `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` deprecated (removed 2026-06-01)
- **Breaking**: `/simplify` behavior changed: now cleanup-only review, not full code-review fix

---

### v2.1.153 (2026-05-28)

> `/model` saves as default by default (IDE parity), `skipLfs` for plugin marketplace, `claude agents` autocomplete improvements, 25+ bug fixes.

- **Changed**: `/model` now saves your selection as the default for new sessions (matching IDE behavior); press `s` in the picker to switch current session only, reversing the 2.1.144 behavior where session-only was the default and `d` set the default
- **New**: `skipLfs` option for `github`/`git` plugin marketplace sources to skip Git LFS downloads during clone and update
- **New**: Status line commands receive `COLUMNS` and `LINES` environment variables so scripts can size output to the terminal width
- **New**: `claude agents` dispatch input autocomplete now suggests native slash commands and bundled skills, not just project skills
- **New**: `claude agents` PR column shows `PR #N` for a single PR or `N PRs` for multiple
- **New**: `claude doctor` shows the result of your last update attempt; one-time notice when npm global install can't auto-update (with `/doctor` listing fixes)
- **Changed (macOS)**: Background agents now appear as "Claude Code" in Privacy & Security, keeping permission grants across upgrades
- **Fixed**: 25+ fixes including stateful MCP servers without optional GET SSE reconnect-looping (regression from 2.1.147), API gateway receiving user's Anthropic OAuth credential instead of gateway token, subagent `Agent` tool frontmatter MCP servers ignoring `--strict-mcp-config`/enterprise managed policies, `Agent` tool with `subagent_type: 'claude'` silently discarding outputs written to gitignored paths, Windows PowerShell installer reporting success when installation actually failed, `claude update` installing latest instead of configured release channel's version, excessive memory when resuming sessions by transcript file path, stream-json mode hang on stdin closed without EOF, malformed `file://` links not clickable, `--help` unwrapped on narrow terminals, MCP tool progress in collapsed view, `/bg` response continuing in background instead of dropping, multiple background session fixes (clipboard/copy in tmux, /rename immediate update, IME candidate window position, 256-color terminal background bleed, zombie session entries after exiting `claude agents` with Remote Control), Windows update rollback restoration
- **Breaking**: `modelPicker:setAsDefault` keybinding renamed to `modelPicker:thisSessionOnly` in `keybindings.json` (the `d` action was replaced by `s`)

---

### v2.1.152 (2026-05-27)

> `/code-review --fix`, `disallowed-tools` frontmatter for skills, `MessageDisplay` hook, auto mode opt-in removed, 35+ bug fixes.

- **New**: `/code-review --fix` now applies review findings to your working tree after the review; `/simplify` now invokes `/code-review --fix`
- **New**: Skills and slash commands can set `disallowed-tools` in frontmatter to remove tools from the model while the skill is active
- **New**: `/reload-skills` command re-scans skill directories without restarting the session
- **New**: `SessionStart` hooks can return `reloadSkills: true` to make newly installed skills available in the same session, and can set the session title via `hookSpecificOutput.sessionTitle` on startup and resume
- **New**: `MessageDisplay` hook event lets hooks transform or hide assistant message text as it is displayed
- **New**: `pluginSuggestionMarketplaces` managed setting so admins can allowlist org marketplaces whose plugins may be suggested via context-aware tips
- **New**: `--fallback-model` switches to a configured fallback for the rest of the session when the primary model is not found, instead of failing every request
- **New (Vim)**: `/` in NORMAL mode opens reverse history search (like Ctrl+R), matching bash/zsh vi-mode behavior
- **Improved**: `/usage` breakdown now includes large session files; files scanned with a streaming read so memory usage stays flat
- **Improved**: Thinking summaries in the collapsed group stay readable for at least 3 seconds, render as markdown, and cap at 10 lines (Ctrl+O shows full thinking)
- **Improved**: Fullscreen mode "Thinking for Ns" indicator counts up live while the model is thinking
- **Changed**: Auto mode no longer requires opt-in consent
- **Fixed**: 35+ fixes including terminal styling degrading in long sessions, sandbox warning missing in condensed startup, loading spinner state across tool calls, focus mode spurious hidden-message count, link click inside tool result collapsing the section, markdown table cell border color bleeding from inline code, plugin MCP servers with same command but different env vars being deduplicated, `/doctor` errors for stale `enabledPlugins` entries, plugin git-branch updates silently stopping, remote MCP servers failing with egress proxy, effort-change dialog appearing with no messages or same effective effort, Agent tool description with `--bare`, background worker crash after stale permission prompt cancellation, `cache_creation_input_tokens` reporting as 0 when API uses nested breakdown, `PushNotification` false negative in SDK-hosted sessions, sessions stuck after model/login switch left stale thinking-block signatures in history

---

### v2.1.150 (2026-05-23)

> Internal infrastructure improvements — no user-facing changes.

---

### v2.1.149 (2026-05-23)

> `/usage` per-category breakdown, GFM task list checkboxes, two security fixes, 20+ bug fixes.

- **New**: `/usage` now shows a per-category breakdown of what drives your limits usage — skills, subagents, plugins, and per-MCP-server cost
- **New**: Markdown output renders GFM task list checkboxes (`- [ ] todo` / `- [x] done`) natively instead of plain bullets
- **New (Enterprise)**: `allowAllClaudeAiMcps` managed setting to load claude.ai cloud MCP connectors alongside `managed-mcp.json`
- **Security**: PowerShell permission bypass fixed — built-in `cd` functions (`cd..`, `cd\`, `cd~`, `X:`) changed the working directory undetected, letting later commands read outside the workspace
- **Security**: Sandbox write allowlist in git worktrees was covering the entire main repository root instead of only the shared `.git` directory (with `hooks/` and `config` denied)
- **Fixed**: `/diff` detail view can now be scrolled with keyboard (arrows, `j`/`k`, `PgUp`/`PgDn`, `Space`, `Home`/`End`)
- **Fixed**: PowerShell prefix/wildcard allow rules (e.g. `PowerShell(dotnet.exe build *)`) now pre-approve native executables and scripts
- **Fixed**: Permission-analysis gap where parser trusted stale variable-tracking values for `PWD`/`OLDPWD`/`DIRSTACK` across `cd`/`pushd`/`popd`
- **Fixed**: `find` in Bash tool exhausting the macOS system file/vnode table on large directory trees
- **Fixed**: Managed-settings approval dialog leaving the terminal frozen after accepting at startup
- **Fixed**: `/ultraplan` and remote session creation failing with "Could not capture uncommitted changes" when the working tree has no real changes
- **Fixed**: `otelHeadersHelper` failing silently when the script path contains spaces; failures now reported in `/doctor` and debug log
- **Fixed**: Thinking spinner staying amber across tool calls and onto fresh thinking bursts
- **Fixed**: Collapsed Bash output reporting the wrong hidden-line count for outputs with many short lines
- **Fixed**: Slash-command argument-hint clipping trailing typed characters when the hint overflows the input box
- **Fixed**: Argument-hint and progressive arg suggestions not appearing after Tab-completing a skill whose frontmatter `name:` differs from its directory basename
- **Fixed**: Status bar showing the user's baseline `/effort` setting instead of the effort level applied by skill/agent `effort:` frontmatter
- **Fixed**: Ctrl+O transcript view freezing at the moment it was opened instead of tailing new messages
- **Fixed**: Editing a recalled prompt-history entry losing the edit when navigating further up/down
- **Fixed**: `/config` exit summary reporting phantom changes to auto-compact and theme when toggling unrelated settings
- **Fixed**: `/insights` crashing when cached session-meta files are missing optional fields
- **Fixed**: Renaming a Remote Control session from claude.ai or the Claude mobile app not updating the local session name for `claude --resume`
- **Fixed**: Race where a just-submitted prompt could appear twice in up-arrow history
- **Fixed**: "Jump to bottom" pill in fullscreen mode not dismissing immediately after tap
- **Improved**: `/feedback` reports now include the conversation before context compaction, making issues from earlier in long sessions easier to triage

---

### v2.1.148 (2026-05-22)

> Hotfix: Bash tool exit code 127 regression from 2.1.147.

- **Fixed**: Bash tool returning exit code 127 on every command (regression introduced in 2.1.147)

---

### v2.1.147 (2026-05-22)

> Pinned background sessions (Ctrl+T), /code-review --comment for inline GitHub PR comments, improved auto-updater, 30+ bug fixes.

- **New**: Pinned background sessions — `Ctrl+T` in `claude agents` pins a session so it stays alive when idle, auto-restarts in place to apply CC updates, and is shed under memory pressure only after non-pinned sessions
- **New**: `/code-review --comment` — post findings as inline GitHub PR comments
- **Improved**: Auto-updater now retries transient network failures, reports specific error categories and OS error codes on failure, and shows the current version when an update fails
- **Fixed**: Prompt history no longer records consecutive duplicate entries
- **Fixed**: Hook `if` conditions like `PowerShell(git push*)` now match correctly (only `PowerShell(*)` worked before)
- **Fixed**: Pasted text now delivered as actual content instead of `[Pasted text #N]` placeholder
- **Fixed**: Plugin component counts in `claude plugin details` and `/plugin` were doubled when paths overlapped default directories
- **Fixed**: Slash commands followed by a tab or newline no longer treated as unknown commands
- **Fixed**: Shell snapshot no longer drops user functions whose names start with a single underscore
- **Fixed**: Plugin agents declaring multiple `Agent(...)` types in `tools:` frontmatter now retain all entries
- **Fixed**: PowerShell tool no longer drops output for commands relying on the default formatter
- **Fixed**: Windows "Yes, and don't ask again" for PowerShell script invocations now writes a rule that matches on subsequent runs
- **Fixed**: Full-screen strobing in attached background sessions on Windows Terminal while streaming
- **Fixed**: On Windows, removing a background-job worktree no longer follows NTFS junctions into the main repo
- **Fixed**: `/effort` slider now opens at the current effort level (was always starting at wrong level)
- **Fixed**: Several spacing and layout glitches in `/plugin`, `/status`, `/mobile`, `/sandbox`, `/permissions` menus
- **Fixed**: 10+ additional fixes: stale/doubled rows in agent view with CJK on Windows, stripped images prompting repeated re-reads, rare scroll-settle hang on Windows, `&amp;` in `!` command output, unknown slash commands now show an error in headless/SDK mode, `/help` rendering on small terminals

---

### v2.1.146 (2026-05-21)

> /code-review command (renamed from /simplify), AskUserQuestion restored in auto mode, 15+ bug fixes.

- **Changed**: `/simplify` renamed to `/code-review` with optional effort level (e.g. `/code-review high`)
- **Fixed**: Auto mode no longer suppresses `AskUserQuestion` when the user or a skill explicitly relies on it
- **Fixed**: Windows PowerShell tool failing with "command line is invalid" when `pwsh` is installed via winget or Microsoft Store (regression in v2.1.124)
- **Fixed**: MCP `resources/list`, `resources/templates/list`, and `prompts/list` now return all pages on paginating servers
- **Fixed**: `/background` no longer refuses sessions whose only typed input was a skill or custom slash command
- **Fixed**: Backgrounded sessions no longer re-prompt for tool permissions already granted with "don't ask again"
- **Fixed**: `/theme` color editor and "New custom theme" dialogs now respond to Esc
- **Fixed**: `CLAUDE_CODE_SUBAGENT_MODEL` now forwarded to child processes in multi-agent sessions
- **Fixed**: `forceLoginOrgUUID` and `forceLoginMethod` managed-settings policies enforced against third-party-provider and API-key sessions
- **Fixed**: 10+ additional fixes: Windows GNOME Terminal paste, background daemon spawn fallback, Windows background session worktree removal, Agent SDK uncaught exception at end of streaming, diff rendering performance for large file edits

---

### v2.1.145 (2026-05-20)

> claude agents --json for scripting, /plugin previews before install, tab title shows awaiting-input count, security fix for Bash permission-prompt bypass, 20+ bug fixes.

- **New**: `claude agents --json` — list all live Claude sessions as JSON for scripting (tmux-resurrect, status bars, session pickers)
- **New**: `agent_id` and `parent_agent_id` attributes added to `claude_code.tool` OTEL spans; background subagent spans now nest under dispatching Agent tool span
- **New**: `/plugin` Discover and Browse screens now preview a plugin's commands, agents, skills, hooks, and MCP/LSP servers before installation
- **New**: `claude agents` terminal tab title shows awaiting-input count so an alt-tabbed window indicates when an agent needs attention
- **New**: Slash command and @-mention suggestion list supports mouse hover and click in fullscreen mode
- **New**: Stop and SubagentStop hook input now includes `background_tasks` and `session_crons` fields
- **New**: Status line JSON input now includes GitHub repo and PR information when detected
- **Security**: Fixed permission-prompt bypass where bare variable assignments to non-allowlisted environment variables in Bash commands were auto-approved
- **Fixed**: MCP paginated `resources/list`, `resources/templates/list`, and `prompts/list` dropping items past page 1
- **Fixed**: MCP prompt slash commands now show the missing argument name and expected usage instead of raw server validation errors
- **Fixed**: Read tool now returns a truncated first page with "PARTIAL view" notice instead of a hard error when whole-file read exceeds token limit
- **Fixed**: Task lists no longer rendered in random order when several tasks are created at once
- **Fixed**: Agent Teams teammates with non-ASCII names no longer fail every API call (invalid header encoding)
- **Fixed**: `/review` no longer errors on repos with Classic Projects (deprecated `projectCards` GraphQL query removed)
- **Fixed**: `claude plugin validate` now flags `skills:` entries pointing at a file instead of a directory
- **Fixed**: Skill with `context: fork` no longer repeatedly re-invokes itself in an infinite loop

---

### v2.1.144 (2026-05-19)

> /resume lists background sessions, /model session-only (d for default), usage credits rename, fixed 75s startup hang, terminal rendering fixes, 40+ bug fixes.

- **New**: `/resume` now lists background sessions started via `claude --bg` or agent view alongside interactive ones, marked with `bg`
- **New**: Elapsed duration shown in background subagent completion notifications (e.g. "Agent completed · 3h 2m 5s")
- **Changed**: `/model` now changes the model for the current session only — press `d` in the picker to set a default for new sessions
- **Changed**: "extra usage" renamed to "usage credits" across CLI copy; `/extra-usage` is now `/usage-credits` (old name still works)
- **Fixed**: Startup no longer hangs up to 75s when `api.anthropic.com` is unreachable — side-channel API calls now time out after 15s
- **Fixed**: Terminal rendering corruption self-heals on missed window-resize events; progressive glitch in long sessions cleared; VS Code spinner uses fewer colors to reduce glitches
- **Fixed**: macOS background sessions crashing with "exit 1 before init" under Full Disk Access-protected folders (regression in 2.1.143)
- **Fixed**: MCP servers with paginated `tools/list` now return all pages (was silently dropping tools past page 1)
- **Fixed**: File descriptor exhaustion in skill directories — non-`.md` files no longer trigger skill reloads
- **Fixed**: 40+ additional fixes: `/branch` after worktree entry, Escape in AskUserQuestion notes field, Bedrock/Vertex Opus 1M context picker, remote login with `forceLoginMethod`, background session scroll on Windows, and more

---

### v2.1.143 (2026-05-16)

> Plugin dependency enforcement, projected context cost in /plugin marketplace, worktree.bgIsolation: "none", PowerShell -ExecutionPolicy Bypass by default, stop hook block cap, 30+ bug fixes.

- **New**: Plugin dependency enforcement — `claude plugin disable` refuses when another enabled plugin depends on the target, with a copy-pasteable disable-chain hint; `claude plugin enable` force-enables transitive dependencies
- **New**: Projected context cost (per-turn and per-invocation token estimates) in the `/plugin` marketplace browse pane
- **New**: `worktree.bgIsolation: "none"` setting — lets background sessions edit the working copy directly without `EnterWorktree` (useful for repos where worktrees are impractical)
- **New**: PowerShell tool now passes `-ExecutionPolicy Bypass` by default — opt out with `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1`
- **Improved**: Background sessions now preserve the model and effort level set after waking from idle
- **Improved**: Shift+Tab in attached agent sessions now includes auto mode in the cycle
- **Fixed**: Stop hooks that block repeatedly no longer loop forever — turn ends with a warning after 8 consecutive blocks (override via `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`)
- **Fixed**: Esc/Ctrl+C now cancels a pending `/loop` wakeup while Claude is idle between iterations
- **Fixed**: `/goal` evaluator no longer fires while background shells or delegated subagents are still running
- **Fixed**: `NO_COLOR`/`FORCE_COLOR` in `settings.json` env now apply to subprocesses only (no longer strips Claude Code's own UI colors)
- **Fixed**: `claude agents --allow-dangerously-skip-permissions` now makes bypass mode available in the permission cycle (was incorrectly defaulting sessions to bypass mode)
- **Fixed**: 20+ additional fixes: background session model+effort preservation after retire/wake, Windows event-loop with network-drive working directories, `claude --bg --dangerously-skip-permissions` persisting across retire/wake, background color bleed on 256-color terminals, stale fragment rendering on Windows Terminal

---

### v2.1.142 (2026-05-15)

> Fast mode upgraded to Opus 4.7 by default, new claude agents dispatch flags, root-level SKILL.md plugin support, /plugin shows LSP servers, MCP_TOOL_TIMEOUT fix, 25+ bug fixes.

- **New**: Fast mode now uses **Opus 4.7** by default (previously Opus 4.6) — set `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1` to pin to Opus 4.6
- **New**: `claude agents` gains dispatch flags: `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--permission-mode`, `--model`, `--effort`, and `--dangerously-skip-permissions` to configure background sessions
- **New**: Plugins with a root-level `SKILL.md` and no `skills/` subdirectory are now automatically surfaced as a skill
- **New**: `/plugin` details pane and `claude plugin details` now show LSP servers a plugin provides
- **New**: `/web-setup` warns before replacing an existing GitHub App connection
- **Fixed**: `MCP_TOOL_TIMEOUT` now correctly raises the per-request fetch timeout for remote HTTP and SSE MCP servers (was capped at 60 seconds regardless of the configured value)
- **Fixed**: Background sessions now recognize pre-existing git worktrees (was blocking Edit while `EnterWorktree` refused to create a duplicate)
- **Fixed**: Daemon now exits cleanly after binary upgrade (e.g. `brew upgrade`) — was causing dispatched agents to crash-loop on the deleted path
- **Fixed**: Background agents no longer crash-loop when Claude-in-Chrome extension is connected without a shared tab
- **Fixed**: Clicking links in an attached `claude agents` session — headless browser shim no longer applies while attached
- **Fixed**: `claude agents` "v to open in editor" now uses your shell's `$EDITOR`/`$VISUAL` instead of the daemon's default editor
- **Fixed**: `claude agents` deadlock on Windows with network-drive working directories; Ctrl+C now works during startup
- **Fixed**: `claude --bg --dangerously-skip-permissions` now persists across retire/wake
- **Fixed**: Plugins using `skills: ["./"]` no longer show a false "path escapes plugin directory" error
- **Fixed**: Plugin cache cleanup no longer deletes the active plugin version directory when no installation metadata is present
- **Improved**: Reactive compaction: first summarize attempt seeds from the original request's overflow size, avoiding a wasted near-full-context retry
- **Improved**: Hook configuration error: configuring a prompt- or agent-type hook for `SessionStart`/`Setup`/`SubagentStart` now shows a clear "use a command-type hook instead" message

---

### v2.1.141 (2026-05-14)

> Hook terminalSequence output field, claude agents --cwd, Rewind "Summarize up to here", 50+ bug fixes.

- **New**: Hook `terminalSequence` field in JSON output — emit desktop notifications, window titles, and bells from hooks without needing a controlling terminal
- **New**: `CLAUDE_CODE_PLUGIN_PREFER_HTTPS` — clones GitHub plugin sources over HTTPS instead of SSH (useful in environments without a GitHub SSH key)
- **New**: `ANTHROPIC_WORKSPACE_ID` environment variable for workload identity federation — scopes the minted token to a specific workspace
- **New**: `claude agents --cwd <path>` — scope the session list to a specific directory
- **New**: `/feedback` can now include recent sessions (last 24h or 7 days) for issues spanning more than the current session
- **New**: Rewind menu: "Summarize up to here" — compress earlier context while keeping recent turns intact
- **Improved**: Auto mode permission dialog now explains when a `permissions.ask` rule caused the prompt
- **Improved**: "View diff in your IDE" option restored on file-edit permission prompts when an IDE is connected
- **Improved**: Background agents launched via `/bg` or `←←` now preserve current permission mode instead of reverting to default
- **Improved**: `claude agents` — agents that finish work but leave a background shell running now move to Completed
- **Improved**: Spinner warms to amber after 10 seconds to signal Claude is still working during long thinking periods
- **Improved**: Plugin menu navigation — `→`/Tab switch tabs, `↑` moves to the tab strip, tab headers and search box clickable in fullscreen
- **Fixed**: Bedrock `awsCredentialExport` now always runs when configured (was skipped when ambient AWS credentials resolved), fixing cross-account access
- **Fixed**: Plugin MCP servers with unset config variables now show a "config issue" message with a fix-it hint instead of a generic connection failure
- **Fixed**: MCP HTTP/SSE servers returning 403 on connect now show "needs auth" instead of "failed"
- **Fixed**: Remote MCP servers no longer disconnect unnecessarily when the optional server-events stream fails to reconnect — tool calls continue over POST
- **Fixed**: Remote Control MCP connectors failing with 401 when worker session token rotated mid-session
- **Fixed**: Remote Control no longer re-enrolls a trusted device when the server rejects a stale token — loops through `/login` properly
- **Fixed**: 40+ additional fixes: markdown table cell-wrap regression, Ctrl+C in vim INSERT/VISUAL mode, alternative `chat:submit` keybindings, `voice:pushToTalk` custom keybindings, Windows Alt+V image paste, `/tui` with running background shells, `/model` changing autocompact threshold in other sessions, transcript view letter shortcuts after mouse click

---

### v2.1.140 (2026-05-13)

> Agent tool subagent_type case-insensitive matching, plugin folder warnings, targeted bug fixes.

- **Improved**: `Agent` tool `subagent_type` matching now case- and separator-insensitive — `"Code Reviewer"` resolves to `code-reviewer`, `"backend_architect"` to `backend-architect`
- **Improved**: Updated agent color palette
- **Improved**: Plugins now warn when a default component folder (e.g. `commands/`) is silently ignored because `plugin.json` sets the matching key — shown in `/doctor`, `claude plugin list`, and `/plugin`
- **Fixed**: `/goal` silently hanging when `disableAllHooks` or `allowManagedHooksOnly` is set — now shows a clear message
- **Fixed**: Symlinked settings hot-reload regression — symlinked files caused misattributed change events and spurious `ConfigChange` hooks
- **Fixed**: `claude --bg` failing with "connection dropped mid-request" when the background service was about to idle-exit
- **Fixed**: Background service startup failing on machines with enterprise endpoint security (allows more startup time)
- **Fixed**: Remote managed settings not retrying on 401 — now retries once with a force-refreshed token
- **Fixed**: Managed `extraKnownMarketplaces` auto-update policy not being persisted to `known_marketplaces.json`
- **Fixed**: `/loop` scheduling redundant wakeups to poll for background tasks that already notify on completion
- **Fixed**: Windows event-loop stall when a missing executable (e.g. `gh`) triggered synchronous `where.exe` re-spawns on every check
- **Fixed**: `Read` tool calls failing validation when `offset` is passed as a whitespace-padded or `+`-prefixed string
- **Fixed**: Native terminal cursor not staying at the input caret when the terminal loses focus

---

### v2.1.139 (2026-05-12)

> Agent view (Research Preview), /goal command, hook exec form + continueOnBlock, 40+ bug fixes.

- **New**: Agent view (Research Preview) — `claude agents` opens a single list of all sessions (running, blocked on you, or done). Each row shows the session status, last response preview, and time since last interaction. Navigate with left arrow from any session or launch directly from the terminal. Select a session to peek at the last turn and reply inline without fully attaching; press Enter to attach. Background any session with `/bg`, or launch directly to the background with `claude --bg [task]`. Available on Pro, Max, Team, Enterprise, and API plans.
- **New**: `/goal` command — set a completion condition; Claude keeps working across turns until met, with live elapsed/turns/tokens overlay panel
- **New**: `/scroll-speed` command to tune mouse wheel scroll speed with live preview
- **New**: `claude plugin details <name>` — shows plugin component inventory and projected per-session token cost
- **New**: Transcript view navigation: `?` for shortcuts, `{`/`}` to jump between user prompts, `v` to toggle shortcut panel
- **New**: Hook `args: string[]` field (exec form) — spawns command directly without a shell, path placeholders need no quoting
- **New**: Hook `continueOnBlock` config option for `PostToolUse` — set `true` to feed rejection reason back to Claude and continue the turn
- **New**: MCP stdio servers now receive `CLAUDE_PROJECT_DIR` in environment; plugin configs can reference `${CLAUDE_PROJECT_DIR}` in commands
- **Improved**: Compaction prompt now asks the model to preserve sensitive user instructions
- **Fixed**: `/mcp` Reconnect picks up `.mcp.json` edits without a restart; shows HTTP status + URL when reconnect fails
- **Fixed**: Deadlock where expired credentials + `forceRemoteSettingsRefresh` blocked `claude auth login/logout/status`
- **Fixed**: `autoAllowBashIfSandboxed` not auto-approving commands with shell expansions like `$VAR` and `$(cmd)`
- **Fixed**: Unbounded MCP SSE memory growth — response bodies now capped at 16 MB per SSE frame
- **Fixed**: `Skill(name *)` wildcard permission rules now work as prefix match (matching `Bash(ls *)` behavior)
- **Fixed**: Settings hot-reload not detecting edits to symlinked `~/.claude/settings.json`
- **Fixed**: 30+ additional fixes: hook terminal corruption, plugin dependency stale count, mouse wheel speed in Cursor/VS Code, MCP resources from disconnected servers in autocomplete, CJK/emoji border overflow, bash history up-arrow, multi-image paste

---

### v2.1.138 (2026-05-11)

> Internal fixes.

- **Fixed**: Internal fixes (no user-visible changes)

---

### v2.1.137 (2026-05-11)

> [VSCode] Fixed extension failing to activate on Windows.

- **Fixed**: VS Code extension failing to activate on Windows

---

### v2.1.136 (2026-05-11)

> settings.autoMode.hard_deny, CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL, MCP /clear disappear fix, 40+ UI/terminal bug fixes.

- **New**: `settings.autoMode.hard_deny` — auto mode classifier rules that block unconditionally regardless of user intent or allow exceptions
- **New**: `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` to re-enable the session quality survey for enterprises capturing responses via OpenTelemetry
- **Fixed**: MCP servers (`.mcp.json`, plugins, claude.ai connectors) silently disappearing after `/clear` in VS Code extension, JetBrains plugin, and Agent SDK
- **Fixed**: MCP OAuth refresh tokens lost when multiple servers refresh concurrently — no more daily re-authentication for multi-server setups
- **Fixed**: Rare login loop where a concurrent credential write could overwrite a freshly-rotated OAuth token and force re-login
- **Fixed**: API error (400) when extended thinking emitted a redacted thinking block after a tool call
- **Fixed**: `--resume` / `--continue` not finding sessions when the project path contains underscores
- **Fixed**: Plan mode not blocking file writes when a matching `Edit(...)` allow rule exists
- **Fixed**: WSL2: image paste from Windows clipboard now works via PowerShell fallback when xclip/wl-paste cannot read image data
- **Fixed**: Plugin `Stop`/`UserPromptSubmit` hooks failing when cache cleanup deletes a version still in use
- **Improved**: Visual consistency across slash command dialogs — standardized footer hints, spacing, arrow-key styling; dialog frame appears immediately during loading
- **Fixed**: Colors appearing at wrong positions in bash command output and markdown code blocks
- **Fixed**: ReasonML diffs rendering corrupted "undefined" text artifacts at word-diff boundaries
- **Fixed**: `@` file picker not matching files created mid-session, and not finding files in directories with 100+ entries
- **Fixed**: 30+ additional UI/terminal fixes: failed tool calls expand in fullscreen, Backspace/Ctrl+Backspace swap fix, `/usage` weekly reset date display, CJK terminal overflow, `/insights` crash on malformed tool calls, renderer crash on collapsibility change, shell-integration lock files not respecting `CLAUDE_CONFIG_DIR`, trailing whitespace in copied output, plugin uninstall case-insensitivity, `AskUserQuestion` multi-select array fix, `CronList` missing qualifiers, MCP tool results invisible on content-block returns

---

### v2.1.133 (2026-05-08)

> worktree.baseRef setting, effort level in hooks, subagent skills fix, 15+ bug fixes.

> **Breaking**: `worktree.baseRef` defaults to `fresh` (branches from `origin/<default>`), reverting 2.1.128 behavior where `EnterWorktree` used local HEAD. Set `worktree.baseRef: "head"` in settings to restore prior behavior.

- **New**: `worktree.baseRef` setting (`fresh` | `head`) — `fresh` (default) branches from `origin/<default-branch>`; `head` keeps local HEAD including unpushed commits. Applies to `--worktree`, `EnterWorktree`, and agent-isolation worktrees
- **New**: `sandbox.bwrapPath` / `sandbox.socatPath` managed settings (Linux/WSL) to specify custom bubblewrap and socat binary locations
- **New**: `parentSettingsBehavior` admin-tier key (`first-wins` | `merge`) to let admins opt SDK `managedSettings` into policy merge
- **New**: Hooks receive active effort level via `effort.level` JSON field and `$CLAUDE_EFFORT` env var in Bash subcommands
- **Improved**: Focus mode behavior and memory usage (background workers released under memory pressure)
- **Fixed**: Subagents not discovering project/user/plugin skills via the Skill tool
- **Fixed**: Parallel sessions dead-ending at 401 after refresh-token race wiped shared credentials
- **Fixed**: `HTTP(S)_PROXY` / `NO_PROXY` / mTLS not respected for full MCP OAuth flow (discovery, client registration, token exchange, refresh)
- **Fixed**: Read/Write/Edit denied on mapped network drives via `--add-dir` / SDK `additionalDirectories`
- **Fixed**: Remote Control stop/interrupt from claude.ai not fully canceling the CLI session (queued messages stalled after interrupting stuck tool)
- **Fixed**: `/effort` in one session unexpectedly changing effort level of other concurrent sessions
- **Fixed**: `claude --help` now lists `--remote-control` flag
- **Fixed**: VS Code extension: `claudeCode.claudeProcessWrapper` failing with "Unsupported platform" when extension build doesn't bundle a Claude binary

---

### v2.1.132 (2026-05-08)

> CLAUDE_CODE_SESSION_ID in Bash env, CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN opt-out, MCP memory fix, 20+ terminal/TUI fixes.

- **New**: `CLAUDE_CODE_SESSION_ID` env var now passed to Bash tool subprocess environment (matches `session_id` in hook JSON input)
- **New**: `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` to opt out of the fullscreen alternate-screen renderer and keep output in the terminal's native scrollback
- **New**: "Pasting…" footer hint while a Ctrl+V image paste is being read from the clipboard
- **Fixed**: Unbounded memory growth (10GB+ RSS) when a stdio MCP server writes non-protocol data to stdout
- **Fixed**: External SIGINT (`kill -INT`, IDE stop button) not running graceful shutdown — terminal modes now restored and `--resume` hint printed
- **Fixed**: `--resume` failing with `no low surrogate in string` when tool error truncation split an emoji; pre-corrupted sessions sanitized on load
- **Fixed**: `--permission-mode` flag ignored when resuming a plan-mode session with `-p --continue`/`--resume`; plan mode not re-applied after `ExitPlanMode` within the same session
- **Fixed**: Fullscreen mode showing blank screen after laptop sleep/wake or Ctrl+Z/`fg` until next keystroke
- **Fixed**: Cursor landing mid-grapheme on Ctrl+E/A/K/U/arrow keys with Indic conjuncts or ZWJ emoji wrapping across lines
- **Fixed**: Vim operators corrupting text with decomposed (NFD) accented characters
- **Fixed**: Pasting text starting with `/` silently swallowing input or triggering unknown-command reply
- **Fixed**: Stray escape sequences in prompt when focus events or mouse-tracking reports interleave with bracketed paste
- **Fixed**: Mouse wheel scrolling too fast in Cursor and VS Code 1.92–1.104 (upstream xterm.js bug); scroll-wheel runaway in JetBrains IDE 2025.2
- **Fixed**: `/usage` Ctrl+S hanging when copying stats screenshot to clipboard on Linux/X11
- **Fixed**: `/terminal-setup` showing contradictory error in Windows Terminal (Shift+Enter is natively supported)
- **Fixed**: `/effort` picker not reflecting `CLAUDE_CODE_EFFORT_LEVEL` env var override
- **Fixed**: `/status` showing wrong default model for some users
- **Fixed**: Slash command autocomplete popup capped at ~3–5 visible commands instead of scaling with terminal height
- **Fixed**: Statusline `context_window` token counts showing cumulative session totals instead of current context usage
- **Fixed**: Alt+T (thinking toggle) not working on macOS without "Option as Meta" enabled (iTerm2, Terminal.app defaults)
- **Fixed**: Dead keyboard input on Windows after re-opening a background session from `claude agents`
- **Fixed**: MCP servers failing `tools/list` silently showing 0 tools — now retries once and shows "connected · tools fetch failed" in `/mcp`
- **Fixed**: Unauthorized claude.ai MCP connectors showing as "failed" instead of "needs auth"; headless `-p` mode no longer retries non-transient 4xx failures
- **Fixed**: Bedrock and Vertex 400 errors when `ENABLE_PROMPT_CACHING_1H` is set

---

### v2.1.131 (2026-05-06)

> VS Code extension Windows activation fix, Mantle auth fix.

- **Fixed**: VS Code extension failing to activate on Windows due to a hardcoded build path in the bundled SDK (`createRequire` polyfill bug)
- **Fixed**: Mantle endpoint authentication failing with missing `x-api-key` header

---

### v2.1.129 (2026-05-06)

> --plugin-url flag, CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE, Ctrl+R all-projects history restored, skillOverrides fix, 20+ bug fixes.

- **New**: `--plugin-url <url>` flag to fetch a plugin `.zip` archive from a URL for the current session
- **New**: `CLAUDE_CODE_FORCE_SYNC_OUTPUT=1` env var to force-enable synchronized output on terminals where auto-detection fails (e.g. Emacs `eat`)
- **New**: `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`: when set, Homebrew or WinGet installations run the upgrade command in the background and prompt to restart
- **Changed**: Plugin manifest `themes` and `monitors` declarations should now go under `"experimental": { ... }` — top-level still works but `claude plugin validate` will warn
- **Changed**: Gateway `/v1/models` discovery is now opt-in via `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` (was automatic in 2.1.126–2.1.128)
- **Improved**: Ctrl+R history picker defaults to all projects again (pre-2.1.124 behavior) — press Ctrl+S to narrow to current project or session
- **Improved**: Third-party deployments (Bedrock, Vertex, Foundry, `ANTHROPIC_BASE_URL` gateway) no longer see spinner tips pointing at first-party Anthropic surfaces
- **Fixed**: `skillOverrides` setting now works: `off` hides from model and `/`, `user-invocable-only` hides from model only, `name-only` collapses description
- **Fixed**: `claude_code.pull_request.count` OTel metric now counts PRs/MRs created via MCP tools (not just shell commands)
- **Fixed**: Policy refusal error messages now include API Request ID for easier support debugging
- **Fixed**: API errors with unrecognized 400 status codes showing raw JSON instead of the underlying error message
- **Fixed**: `/clear` not resetting the terminal tab title after a conversation
- **Fixed**: Session title chip from `/rename` disappearing while a permission or other dialog is active
- **Fixed**: Agent panel below the prompt hidden when subagents are running (regression in 2.1.122)
- **Fixed**: External-editor handoff (Ctrl+G) blanking the conversation history above the prompt
- **Fixed**: `/context` dumping its rendered ASCII visualization grid into the conversation (~1.6k tokens wasted per call)
- **Fixed**: `/agents` Library list arrow-key navigation — highlighted agent stays visible when list exceeds viewport
- **Fixed**: `/branch` success message not including the new branch's session id for `/resume`
- **Fixed**: Bold headers with keycap/ZWJ/skin-tone emoji losing trailing characters in fullscreen mode
- **Fixed**: Server-managed settings policy not applying for enterprise/team users with stored OAuth credentials lacking `user:inference` scope
- **Fixed**: OAuth refresh race after wake-from-sleep that could log out all running sessions
- **Fixed**: 1-hour prompt cache TTL being silently downgraded to 5 minutes
- **Fixed**: Cache-miss warning appearing spuriously after `/clear` or compaction when changing `/effort` or `/model`
- **Fixed**: `Bash(mkdir *)`, `Bash(touch *)` and similar allow rules not honored for in-project paths
- **Fixed**: `deniedMcpServers` patterns with `*://` scheme wildcard not matching mixed-case hostnames
- **Fixed**: Harmless WebSocket warning logged as error in `--debug` during voice mode
- **Fixed**: [VSCode] `/clear` not clearing the conversation context and displayed transcript

---

### v2.1.128 (2026-05-05)

> EnterWorktree branch from local HEAD, --plugin-dir .zip support, --channels console auth, /mcp tool count, parallel bash tool fix, sub-agent prompt cache fix, 35+ bug fixes.

- **Fixed**: `EnterWorktree` now creates the new branch from local HEAD as documented — unpushed commits are no longer dropped when branching
- **New**: `--plugin-dir` accepts `.zip` plugin archives in addition to directories
- **New**: `--channels` now works with console (API key) authentication — managed orgs must set `channelsEnabled: true` in managed settings
- **Improved**: `/mcp` shows tool count for each connected server and flags servers that connected with 0 tools
- **Improved**: Reconnecting MCP servers no longer flood the conversation with full tool-name lists on every reconnect — re-announced tools are summarized by server prefix
- **Improved**: SDK hosts receive a persistent `localSettings` suggestion for Bash permission prompts, so "Always allow" writes to `.claude/settings.local.json`
- **Improved**: Bare `/color` (no args) now picks a random session color
- **Improved**: `/model` picker collapses duplicate Opus 4.7 entries; current Opus shows as "Opus" instead of "Opus 4.7"
- **Improved**: Subprocesses (Bash, hooks, MCP, LSP) no longer inherit `OTEL_*` env vars — OTEL-instrumented apps run via Bash no longer pick up the CLI's own OTLP endpoint
- **Fixed**: Parallel shell tool calls — a failing read-only command (grep, git diff, ls) no longer cancels sibling calls
- **Fixed**: Sub-agent progress summaries missing the prompt cache (~3× `cache_creation` reduction)
- **Fixed**: Sessions on 1M-context models with a smaller autocompact window falsely blocked with "Prompt is too long"
- **Fixed**: MCP stdio servers receiving corrupted arguments when `CLAUDE_CODE_SHELL_PREFIX` is set and an argument contains spaces or shell metacharacters
- **Fixed**: `/plugin update` never detecting new versions of npm-sourced plugins
- **Fixed**: MCP: `workspace` is now a reserved server name — existing servers with that name are skipped with a warning
- **Fixed**: Markdown link labels lost on terminals without OSC 8 hyperlink support — links now render as `label (url)`
- **Fixed**: Tab navigation in `/config` stranding focus — the tab header stays focused so arrows and Esc keep working
- **Fixed**: Fenced code blocks inside list items carrying leading whitespace into the clipboard on copy-paste
- **Fixed**: MCP tool results dropping images when the server returns both structured content and content blocks
- **Fixed**: Terminal progress indicator (OSC 9;4) flickering off between tool calls
- **Fixed**: 20+ additional terminal, clipboard, and session management bug fixes

---

### v2.1.126 (2026-05-01)

> Gateway /v1/models listing in /model picker, claude project purge, OAuth paste code for WSL2/SSH, Windows PowerShell 7 as primary shell, security fix, 40+ bug fixes.

- **New**: `/model` picker now lists models from your gateway's `/v1/models` endpoint when `ANTHROPIC_BASE_URL` points at an Anthropic-compatible gateway
- **New**: `claude project purge [path]` deletes all Claude Code state for a project (transcripts, tasks, file history, config entry) — supports `--dry-run`, `-y/--yes`, `-i/--interactive`, and `--all`
- **Improved**: `--dangerously-skip-permissions` now bypasses prompts for writes to `.claude/`, `.git/`, `.vscode/`, shell config files, and other previously-protected paths (catastrophic removal commands still prompt as a safety net)
- **Improved**: `claude auth login` accepts the OAuth code pasted into the terminal when the browser callback can't reach localhost (WSL2, SSH, containers)
- **Improved**: `claude_code.skill_activated` OpenTelemetry event now fires for user-typed slash commands with a new `invocation_trigger` attribute (`"user-slash"`, `"claude-proactive"`, or `"nested-skill"`)
- **Improved**: Auto mode spinner now turns red when a permission check stalls, instead of looking like the tool is running
- **Improved**: Windows — PowerShell 7 installed via Microsoft Store, MSI without PATH, or `.NET global tool` is now detected; when PowerShell tool is enabled, Claude treats PowerShell as the primary shell instead of defaulting to Bash
- **Improved**: Read tool — removed the per-file malware-assessment reminder that caused spurious refusals on legacy models
- **Security**: Fixed `allowManagedDomainsOnly` / `allowManagedReadPathsOnly` being ignored when a higher-priority managed-settings source lacked a `sandbox` block
- **Fixed**: Pasting an image larger than 2000px no longer breaks the session — images are downscaled on paste, oversized images in history are automatically removed and the request retried
- **Fixed**: OAuth login failing with timeout on slow or proxied connections, in IPv6-only devcontainers, and when the browser callback can't reach localhost
- **Fixed**: "Stream idle timeout" error after waking Mac from sleep mid-request; background and remote sessions no longer falsely abort during long model thinking pauses
- **Fixed**: Japanese/Korean/Chinese text rendering as garbled characters on Windows in no-flicker mode
- **Fixed**: `Ctrl+L` clearing the prompt input — it now only forces a screen redraw, matching readline behavior
- **Fixed**: Deferred tools (WebSearch, WebFetch, etc.) not available to skills with `context: fork` on their first turn
- **Fixed**: Windows clipboard writes no longer expose copied content in process command-line arguments visible to EDR/SIEM telemetry; also fixes >22KB selections not reaching the clipboard
- **Fixed**: Agent SDK hang when the model emits a malformed tool name in a parallel tool call batch
- **Fixed**: `/plugin` Uninstall reporting "Enabled" instead of "Uninstalled"

---

### v2.1.123 (2026-04-29)

> Hotfix: OAuth 401 retry loop when CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1.

- **Fixed**: OAuth authentication failing with a 401 retry loop when `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` is set

---

### v2.1.122 (2026-04-28)

> ANTHROPIC_BEDROCK_SERVICE_TIER env var, PR URL in /resume search, Vertex AI/Bedrock fixes, image resize fix, many bug fixes.

- **New**: `ANTHROPIC_BEDROCK_SERVICE_TIER` environment variable to select a Bedrock service tier (`default`, `flex`, or `priority`) via `X-Amzn-Bedrock-Service-Tier` header
- **New**: Pasting a PR URL into the `/resume` search box now finds the session that created that PR (GitHub, GitHub Enterprise, GitLab, and Bitbucket)
- **Improved**: `/mcp` now shows claude.ai connectors hidden by a manually-added server with the same URL, with a hint to remove the duplicate
- **Fixed**: `/branch` producing forks that fail with "tool_use ids were found without tool_result blocks" from rewound timelines
- **Fixed**: `/model` not showing Effort option for Bedrock application inference profile ARNs
- **Fixed**: Vertex AI / Bedrock returning `invalid_request_error: output_config: Extra inputs are not permitted` on title generation and structured-output queries
- **Fixed**: Vertex AI `count_tokens` endpoint returning 400 errors for users behind proxy gateways
- **Fixed**: `!exit` / `!quit` in bash mode terminating the CLI instead of running as a shell command
- **Fixed**: Images sent to newer models being resized to 2576px instead of the correct 2000px maximum
- **Fixed**: Remote control session idle status redrawing twice per second, flooding `tmux -CC` control pipes
- **Fixed**: `ToolSearch` missing MCP tools that connected after session start in nonblocking mode
- **Fixed**: A malformed hooks entry in `settings.json` no longer invalidating the entire file
- **Fixed**: `spinnerTipsOverride.excludeDefault` not suppressing time-based spinner tips
- **Fixed**: Assistant messages appearing blank in some sessions due to a stale view preference

---

### v2.1.121 (2026-04-27)

> alwaysLoad MCP config, plugin prune, PostToolUse output replacement for all tools, critical memory leak fixes, many bug fixes.

- **New**: `alwaysLoad` option in MCP server config — when `true`, all tools from that server skip tool-search deferral and are always available
- **New**: `claude plugin prune` removes orphaned auto-installed plugin dependencies; `plugin uninstall --prune` cascades
- **New**: Type-to-filter search box in `/skills` for finding a skill without scrolling
- **New**: `PostToolUse` hooks can now replace tool output for all tools via `hookSpecificOutput.updatedToolOutput` (previously MCP-only)
- **New**: Vertex AI: support X.509 certificate-based Workload Identity Federation (mTLS ADC)
- **Improved**: Fullscreen mode: typing into the prompt no longer jumps scroll to the bottom after scrolling up
- **Improved**: Dialogs that overflow the terminal are now scrollable with arrow keys, PgUp/PgDn, home/end, and mouse wheel
- **Improved**: Clicking any line of a long URL wrapping across rows in fullscreen now opens the full URL
- **Improved**: `--dangerously-skip-permissions` no longer prompts for writes to `.claude/skills/`, `.claude/agents/`, and `.claude/commands/`
- **Improved**: `/terminal-setup` now enables iTerm2's "Applications in terminal may access clipboard" for `/copy` in tmux
- **Improved**: MCP servers that hit a transient startup error now auto-retry up to 3 times
- **Improved**: Terminal tab session title is now generated in your configured `language` setting
- **Improved**: Claude.ai connectors with the same upstream URL are now deduplicated
- **Improved**: LSP diagnostic summaries now expand on click/ctrl+o and show the expand hint
- **Improved**: OpenTelemetry: added `stop_reason`, `gen_i.response.finish_reasons`, and `user_system_prompt` (gated behind `OTEL_LOG_USER_PROMPTS`)
- **[VSCode]**: `/context` now opens a native token usage dialog; voice dictation respects `accessibility.voice.speechLanguage`
- **Fixed**: Unbounded memory growth (multi-GB RSS) when processing many images in a session
- **Fixed**: `/usage` leaking up to ~2GB of memory on machines with large transcript histories
- **Fixed**: Memory leak when long-running tools fail to emit a clear progress event
- **Fixed**: Bash tool becoming permanently unusable when the start directory is deleted or moved mid-session
- **Fixed**: `--resume` crashing on startup in external builds
- **Fixed**: `--resume` failing on large sessions when a transcript line was corrupted by an unclean shutdown
- **Fixed**: `thinking.type.enabled is not supported` error with Bedrock application inference profile ARNs
- **Fixed**: Microsoft 365 MCP OAuth failing with duplicate or unsupported `prompt` parameter
- **Fixed**: Scrollback duplication when pressing Ctrl+L in non-fullscreen mode on tmux, GNOME Terminal, Windows Terminal, Konsole
- **Fixed**: claude.ai MCP connectors silently disappearing on transient auth error at startup
- **Fixed**: "Always allow" rules for built-in tools in remote sessions not surviving worker restarts
- **Fixed**: `NO_PROXY` not respected for all HTTP clients when set via `managed-settings.json` on native build
- **Fixed**: Managed settings approval prompt exiting the session even when accepted

---

### v2.1.120 (2026-04-24)

> Windows no longer requires Git Bash, claude ultrareview CI subcommand, ${CLAUDE_EFFORT} in skills, many bug fixes.

- **New**: Windows: Git for Windows (Git Bash) is no longer required — when absent, Claude Code uses PowerShell as the shell tool
- **New**: `claude ultrareview [target]` subcommand to run `/ultrareview` non-interactively from CI or scripts; `--json` for raw output; exits 0 on completion or 1 on failure
- **New**: Skills can reference the current effort level with `${CLAUDE_EFFORT}` in their content
- **New**: `AI_AGENT` environment variable set for subprocesses so `gh` can attribute traffic to Claude Code
- **Improved**: Faster session start when many claude.ai connectors are configured but not authorized
- **Improved**: `claude plugin validate` now accepts `$schema`, `version`, and `description` at the top level of `marketplace.json`
- **Improved**: Auto-compact in auto mode now displays `auto` (lowercase) instead of a misleading token value
- **Improved**: Spinner tips recommending the desktop app or creating skills/agents are hidden when you already have them
- **Improved**: Show a "use PgUp/PgDn to scroll" hint when the terminal sends arrow keys instead of scroll events
- **Fixed**: Pressing Esc during a stdio MCP tool call closing the entire server connection (regression in 2.1.105)
- **Fixed**: `/rewind` and other interactive overlays not responding to keyboard input after `--resume`
- **Fixed**: Terminal scrollback duplication in non-fullscreen mode (resize, dialog dismiss, long sessions)
- **Fixed**: `DISABLE_TELEMETRY` / `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` not suppressing usage metrics telemetry for API and enterprise users
- **Fixed**: False-positive "Dangerous rm operation" permission prompts in auto mode for multi-line bash with pipe and redirect
- **Fixed**: Long selection menus clipping below the terminal in fullscreen mode
- **Fixed**: Write tool output collapsing instead of expanding when clicking "+N lines" in fullscreen
- **Fixed**: Slash command picker jumping while typing; highlight now only matches contiguous substrings
- **Fixed**: `/plugin` marketplace failing to load when one entry uses an unrecognized source format
- **Fixed**: `find` in the Bash tool exhausting open file descriptors on large directory trees, causing host-wide crashes (macOS/Linux native builds)
- **[VSCode]**: `/usage` now opens the native Account & Usage dialog; voice dictation respects the `language` setting

---

### v2.1.119 (2026-04-24)

> /config settings persist to settings.json with override precedence, --from-pr supports GitLab/Bitbucket/GitHub Enterprise, agent frontmatter improvements, security fix for blockedMarketplaces, 30+ bug fixes.

- **New**: `/config` settings (theme, editor mode, verbose, etc.) now persist to `~/.claude/settings.json` and participate in project/local/policy override precedence
- **New**: `prUrlTemplate` setting to point the footer PR badge at a custom code-review URL instead of github.com
- **New**: `CLAUDE_CODE_HIDE_CWD` environment variable to hide the working directory in the startup logo
- **New**: `--from-pr` now accepts GitLab merge-request, Bitbucket pull-request, and GitHub Enterprise PR URLs
- **Improved**: `--print` mode now honors the agent's `tools:` and `disallowedTools:` frontmatter, matching interactive-mode behavior
- **Improved**: `--agent <name>` now honors the agent definition's `permissionMode` for built-in agents
- **Improved**: PowerShell tool commands can now be auto-approved in permission mode, matching Bash behavior
- **Improved**: `PostToolUse` and `PostToolUseFailure` hook inputs now include `duration_ms` (tool execution time, excluding permission prompts and PreToolUse hooks)
- **Improved**: Subagent and SDK MCP server reconfiguration now connects servers in parallel instead of serially
- **Improved**: Plugins pinned by another plugin's version constraint now auto-update to the highest satisfying git tag
- **Improved**: Vim mode: Esc in INSERT no longer pulls a queued message back into the input; press Esc again to interrupt
- **Improved**: Slash command suggestions now highlight the characters that matched your query; picker wraps long descriptions instead of truncating
- **Improved**: `owner/repo#N` shorthand links now use your git remote's host instead of always pointing at github.com
- **Security**: `blockedMarketplaces` now correctly enforces `hostPattern` and `pathPattern` entries
- **Fixed**: Pasting CRLF content (Windows clipboards, Xcode console) inserting an extra blank line between every line
- **Fixed**: Glob and Grep tools disappearing on native macOS/Linux builds when Bash tool is denied via permissions
- **Fixed**: Scrolling up in fullscreen mode snapping back to the bottom every time a tool finishes
- **Fixed**: Auto mode overriding plan mode with conflicting "Execute immediately" instructions
- **Fixed**: `Agent` tool with `isolation: "worktree"` reusing stale worktrees from prior sessions
- **Fixed**: `TaskList` returning tasks in arbitrary filesystem order instead of sorted by ID
- **Fixed**: `/plan` and `/plan open` not acting on the existing plan when entering plan mode
- **Fixed**: Skills invoked before auto-compaction being re-executed against the next user message
- **Fixed**: Verbose output setting not persisting after restart; disabled MCP servers appearing as "failed" in `/status`
- **Fixed**: `${ENV_VAR}` placeholders in `headers` for HTTP/SSE/WebSocket MCP servers not being substituted
- **Fixed**: MCP OAuth `--client-secret` not sent during token exchange for `client_secret_post` servers
- **Fixed**: `/skills` Enter key closing dialog instead of pre-filling `/<skill-name>` in the prompt
- **Fixed**: Spurious "GitHub API rate limit exceeded" hints from PR titles mentioning "rate limit"
- **Fixed**: Async `PostToolUse` hooks emitting no response writing empty entries to session transcript
- **Fixed**: `@`-file Tab completion replacing the entire prompt when used inside a slash command with an absolute path

### v2.1.118 (2026-04-23)

> Vim visual mode, /usage merging /cost+/stats, custom named themes, hooks invoke MCP tools directly, many bug fixes.

- **New**: Vim visual mode (`v`) and visual-line mode (`V`) with selection, operators (d, y, c, >, <), and visual feedback
- **New**: `/cost` and `/stats` merged into `/usage` — both old commands remain as typing shortcuts that open the relevant tab
- **New**: Create and switch between named custom themes from `/theme`, or hand-edit JSON files in `~/.claude/themes/`; plugins can ship themes via a `themes/` directory
- **New**: Hooks can now invoke MCP tools directly via `type: "mcp_tool"` in hook configuration
- **New**: `DISABLE_UPDATES` env var completely blocks all update paths including manual `claude update` (stricter than `DISABLE_AUTOUPDATER`)
- **New**: WSL on Windows can inherit Windows-side managed settings via `wslInheritsWindowsSettings` policy key
- **Improved**: Auto mode `"$defaults"` sentinel — include in `autoMode.allow`, `autoMode.soft_deny`, or `autoMode.environment` to add custom rules alongside built-in list instead of replacing it
- **Improved**: "Don't ask again" option added to auto mode opt-in prompt
- **Improved**: `--continue`/`--resume` now find sessions that added the current directory via `/add-dir`
- **Improved**: `/color` syncs the session accent color to claude.ai/code when Remote Control is connected
- **Improved**: `/model` picker now honors `ANTHROPIC_DEFAULT_*_MODEL_NAME`/`_DESCRIPTION` overrides when using a custom `ANTHROPIC_BASE_URL` gateway
- **Improved**: `claude plugin tag` to create release git tags for plugins with version validation
- **Improved**: Auto-update skip due to version constraints now appears in `/doctor` and `/plugin` Errors tab
- **Fixed**: `/mcp` menu hiding OAuth Authenticate/Re-authenticate for servers with `headersHelper`, and HTTP/SSE servers stuck in "needs authentication" after a transient 401
- **Fixed**: MCP OAuth tokens with no `expires_in` in response requiring re-authentication every hour
- **Fixed**: MCP step-up authorization silently refreshing instead of prompting when `insufficient_scope` 403 names a scope already held
- **Fixed**: macOS keychain race where concurrent token refresh could overwrite a freshly-refreshed OAuth token
- **Fixed**: Credential save crash on Linux/Windows corrupting `~/.claude/.credentials.json`
- **Fixed**: `/login` having no effect in sessions launched with `CLAUDE_CODE_OAUTH_TOKEN` env var
- **Fixed**: Agent-type hooks failing with "Messages are required for agent hooks" for non-Stop events
- **Fixed**: `prompt` hooks re-firing on tool calls made by an agent-hook verifier subagent
- **Fixed**: `/fork` writing full parent conversation to disk per fork — now writes a pointer and hydrates on read
- **Fixed**: Alt+K / Alt+X / Alt+^ / Alt+_ freezing keyboard input
- **Fixed**: `plugin install` on an already-installed plugin not re-resolving a dependency at wrong version
- **Fixed**: Subagents resumed via `SendMessage` not restoring their explicit `cwd`

### v2.1.117 (2026-04-22)

> Default effort now `high` for Pro/Max on Opus 4.6 + Sonnet 4.6, native bfs/ugrep on macOS/Linux, Opus 4.7 1M context fix, /model persistence, 15+ bug fixes.

- **Changed**: Default effort level changed to `high` for Pro/Max subscribers on Opus 4.6 and Sonnet 4.6 (was `medium`)
- **Fixed**: Opus 4.7 sessions were computing `/context` percentage against a 200K window instead of the native 1M — causing inflated percentages and premature autocompact
- **New**: Native macOS/Linux builds now use embedded `bfs` (search) and `ugrep` (grep) replacing the Glob/Grep tools — faster without an extra tool round-trip (Windows and npm-installed builds unchanged)
- **Improved**: `/model` selections now persist across restarts even when the project pins a different model; startup header shows when the active model comes from a project or managed-settings pin
- **Improved**: `/resume` now offers to summarize stale, large sessions before re-reading them (matching existing `--resume` behavior)
- **Improved**: Faster startup when both local and claude.ai MCP servers are configured (concurrent connect now default)
- **Improved**: `plugin install` on an already-installed plugin now installs any missing dependencies instead of stopping at "already installed"; dependency errors say "not installed" with an install hint
- **Improved**: `cleanupPeriodDays` retention sweep now also covers `~/.claude/tasks/`, `~/.claude/shell-snapshots/`, and `~/.claude/backups/`
- **Improved**: Agent frontmatter `mcpServers` are now loaded for main-thread agent sessions via `--agent`
- **Improved**: OpenTelemetry `user_prompt` events now include `command_name` and `command_source` for slash commands; cost/token/API events include `effort` attribute when supported
- **Fixed**: Plain-CLI OAuth sessions dying with "Please run /login" when access token expires mid-session — token now refreshed reactively on 401
- **Fixed**: `WebFetch` hanging on very large HTML pages (truncates input before HTML-to-markdown conversion)
- **Fixed**: Crash when a proxy returns HTTP 204 No Content
- **Fixed**: `/login` having no effect when launched with `CLAUDE_CODE_OAUTH_TOKEN` env var and that token expires
- **Fixed**: Prompt-input undo (`Ctrl+_`) doing nothing immediately after typing, and skipping a state on each undo step
- **Fixed**: `NO_PROXY` not being respected for remote API requests when running under Bun
- **Fixed**: Bedrock application-inference-profile requests failing with 400 when backed by Opus 4.7 with thinking disabled

### v2.1.116 (2026-04-21)

> Regression fix release: ends the six-week Triple Harness Incident (Mar 4–Apr 20, 2026). Also: /resume up to 67% faster on large sessions, inline thinking progress spinner, sandbox security fix, many bug fixes.

- **Regression fix**: All three harness-level changes responsible for the six-week quality regression (effort defaults, thinking-budget clear, verbosity instruction) are reverted or fixed in this release — see [Triple Harness Incident](./known-issues.md#triple-harness-incident-effort-thinking-tokens-verbosity-mar-apr-2026) for the full timeline
- **Improved**: `/resume` is up to 67% faster on sessions 40MB+ and handles sessions with many dead-fork entries more efficiently
- **Improved**: Faster MCP startup when multiple stdio servers are configured; `resources/templates/list` is deferred to the first `@`-mention
- **Improved**: Smoother fullscreen scrolling in VS Code, Cursor, and Windsurf; `/terminal-setup` now configures the editor's scroll sensitivity
- **Improved**: Thinking spinner shows inline progress ("still thinking", "thinking more", "almost done thinking") replacing the separate hint row
- **Improved**: `/config` search now matches option values (e.g., searching "vim" finds the Editor mode setting)
- **Improved**: `/doctor` can now be opened while Claude is responding, without waiting for the current turn to finish
- **Improved**: `/reload-plugins` and background plugin auto-update now auto-install missing dependencies from already-added marketplaces
- **Improved**: Bash tool surfaces a hint when `gh` commands hit GitHub's API rate limit, so agents can back off instead of retrying
- **Improved**: Usage tab shows 5-hour and weekly usage immediately and no longer fails when the usage endpoint is rate-limited
- **Improved**: Agent frontmatter `hooks:` now fire when running as a main-thread agent via `--agent`
- **Improved**: Slash command menu shows "No commands match" when filter has zero results, instead of disappearing
- **Security**: Sandbox auto-allow no longer bypasses the dangerous-path safety check for `rm`/`rmdir` targeting `/`, `$HOME`, or other critical system directories
- **Fixed**: Devanagari and other Indic scripts rendering with broken column alignment in the terminal UI
- **Fixed**: `Ctrl+-` not triggering undo in terminals using the Kitty keyboard protocol (iTerm2, Ghostty, kitty, WezTerm, Windows Terminal)
- **Fixed**: `Cmd+Left/Right` not jumping to line start/end in Kitty protocol terminals (Warp fullscreen, kitty, Ghostty, WezTerm)
- **Fixed**: `Ctrl+Z` hanging the terminal when Claude Code is launched via a wrapper process (e.g., `npx`, `bun run`)
- **Fixed**: Scrollback duplication in inline mode where resizing the terminal or large output bursts would repeat earlier conversation history
- **Fixed**: Modal search dialogs overflowing the screen at short terminal heights, hiding the search box and keyboard hints
- **Fixed**: Scattered blank cells and disappearing composer chrome in the VS Code integrated terminal during scrolling
- **Fixed**: Intermittent API 400 error related to cache control TTL ordering that could occur when a parallel request completed during request setup
- **Fixed**: `/branch` rejecting conversations with transcripts larger than 50MB
- **Fixed**: `/resume` silently showing an empty conversation on large session files instead of reporting the load error
- **Fixed**: `/plugin` Installed tab showing the same item twice when it appears under Needs attention or Favorites
- **Fixed**: `/update` and `/tui` not working after entering a worktree mid-session

---

### v2.1.114 (2026-04-18)

> Fixed crash in permission dialog when an agent teams teammate requested tool permission.

- **Fixed**: Crash in the permission dialog when an agent teams teammate requested tool permission

---

### v2.1.113 (2026-04-18)

> Native Claude Code binary spawning, sandbox.network.deniedDomains setting, security hardening, many bug fixes.

- **New**: CLI now spawns a native Claude Code binary via a per-platform optional dependency instead of bundled JavaScript
- **New**: `sandbox.network.deniedDomains` setting — block specific domains even when a broader `allowedDomains` wildcard would otherwise permit them
- **Improved**: Fullscreen mode — `Shift+↑/↓` now scrolls the viewport when extending a selection past the visible edge
- **Improved**: `Ctrl+A` and `Ctrl+E` now move to the start/end of the current logical line in multiline input (readline behavior)
- **Improved**: Windows: `Ctrl+Backspace` now deletes the previous word
- **Improved**: Long URLs in responses and bash output stay clickable when they wrap across lines (in terminals with OSC 8 hyperlinks)
- **Improved**: `/loop` — pressing Esc now cancels pending wakeups; wakeups display as "Claude resuming /loop wakeup" for clarity
- **Improved**: `/extra-usage` now works from Remote Control (mobile/web) clients
- **Improved**: Remote Control clients can now query `@`-file autocomplete suggestions
- **Improved**: `/ultrareview` — faster launch with parallelized checks, diffstat in the launch dialog, animated launching state
- **Improved**: Subagents that stall mid-stream now fail with a clear error after 10 minutes instead of hanging silently
- **Improved**: Bash tool — multi-line commands whose first line is a comment now show the full command in the transcript, closing a UI-spoofing vector
- **Improved**: Running `cd <current-directory> && git …` no longer triggers a permission prompt when the `cd` is a no-op
- **Security**: On macOS, `/private/{etc,var,tmp,home}` paths are now treated as dangerous removal targets under `Bash(rm:*)` allow rules
- **Security**: Bash deny rules now match commands wrapped in `env`/`sudo`/`watch`/`ionice`/`setsid` and similar exec wrappers
- **Security**: `Bash(find:*)` allow rules no longer auto-approve `find -exec`/`-delete`
- **Fixed**: MCP concurrent-call timeout handling where a message for one tool call could silently disarm another call's watchdog
- **Fixed**: Cmd-backspace / `Ctrl+U` to once again delete from the cursor to the start of the line
- **Fixed**: Markdown tables breaking when a cell contains an inline code span with a pipe character
- **Fixed**: Session recap auto-firing while composing unsent text in the prompt
- **Fixed**: `/copy` "Full response" not aligning markdown table columns for pasting into GitHub, Notion, or Slack
- **Fixed**: Messages typed while viewing a running subagent hidden from its transcript and misattributed to the parent AI
- **Fixed**: `Bash dangerouslyDisableSandbox` running commands outside the sandbox without a permission prompt
- **Fixed**: `/effort auto` confirmation now says "Effort level set to max" to match the status bar label
- **Fixed**: The "copied N chars" toast overcounting emoji and other multi-code-unit characters
- **Fixed**: `/insights` crashing with `EBUSY` on Windows
- **Fixed**: Exit confirmation dialog mislabeling one-shot scheduled tasks as recurring — now shows a countdown
- **Fixed**: Slash/@ completion menu not sitting flush against the prompt border in fullscreen mode
- **Fixed**: `CLAUDE_CODE_EXTRA_BODY output_config.effort` causing 400 errors on subagent calls to models without effort support and on Vertex AI
- **Fixed**: Prompt cursor disappearing when `NO_COLOR` is set
- **Fixed**: `ToolSearch` ranking so pasted MCP tool names surface the actual tool instead of description-matching siblings
- **Fixed**: Compacting a resumed long-context session failing with "Extra usage is required for long context requests"
- **Fixed**: `plugin install` succeeding when a dependency version conflicts with an already-installed plugin — now reports `range-conflict`
- **Fixed**: "Refine with Ultraplan" not showing the remote session URL in the transcript
- **Fixed**: SDK image content blocks that fail to process crashing the session — now degrade to a text placeholder
- **Fixed**: Remote Control sessions not streaming subagent transcripts
- **Fixed**: Remote Control sessions not being archived when Claude Code exits
- **Fixed**: `thinking.type.enabled is not supported` 400 error when using Opus 4.7 via a Bedrock Application Inference Profile ARN

---

### v2.1.111 (2026-04-16)

> Claude Opus 4.7 xhigh effort level, /ultrareview cloud code review, /less-permission-prompts skill, Auto mode for Max subscribers.

- **New**: Claude Opus 4.7 `xhigh` effort level — between `high` and `max`; available via `/effort`, `--effort`, and the model picker; other models fall back to `high`
- **New**: Auto mode for Max subscribers on Opus 4.7 — no longer requires `--enable-auto-mode`
- **New**: `/ultrareview` skill — runs comprehensive code review in the cloud using parallel multi-agent analysis; invoke without arguments for current branch, or `/ultrareview <PR#>` for a specific GitHub PR
- **New**: `/less-permission-prompts` skill — scans transcripts for common read-only Bash and MCP tool calls, proposes a prioritized allowlist for `.claude/settings.json`
- **New**: "Auto (match terminal)" theme option — follows your terminal's dark/light mode; selectable via `/theme`
- **New**: `/effort` opens an interactive slider when called without arguments; arrow-key navigation + Enter to confirm
- **Improved**: Plan files now named after your prompt (e.g. `fix-auth-race-snug-otter.md`) instead of purely random words
- **Improved**: Read-only bash commands with glob patterns (e.g. `ls *.ts`) and commands starting with `cd <project-dir> &&` no longer trigger a permission prompt
- **Improved**: `/setup-vertex` and `/setup-bedrock` show the actual `settings.json` path when `CLAUDE_CONFIG_DIR` is set, seed model candidates from existing pins on re-run, offer a "with 1M context" option
- **Improved**: `/skills` menu now supports sorting by estimated token count — press `t` to toggle
- **Improved**: `Ctrl+U` clears the entire input buffer (`Ctrl+Y` restores); `Ctrl+L` forces full screen redraw
- **Improved**: Typo suggestions for near-miss `claude <word>` invocations (e.g. `claude udpate` → "Did you mean `claude update`?")
- **Improved**: Headless `--output-format stream-json` includes `plugin_errors` on the init event; `OTEL_LOG_RAW_API_BODIES` env var emits full API bodies as OpenTelemetry log events
- **Fixed**: Terminal display tearing (random characters, drifting input) in iTerm2 + tmux setups when terminal notifications are sent
- **Fixed**: `@` file suggestions re-scanning entire project on every turn in non-git directories; only config files shown in freshly-initialized git repos with no tracked files
- **Fixed**: LSP diagnostics from before an edit appearing after it, causing model to re-read already-edited files
- **Fixed**: Tab-completing `/resume` immediately resuming an arbitrary titled session instead of showing the session picker
- **Fixed**: `/clear` dropping the session name set by `/rename`, causing statusline to lose `session_name`
- **Fixed**: Claude calling non-existent `commit` skill showing "Unknown skill: commit" for users without a custom `/commit` command
- **Fixed**: 429 rate-limit errors on Bedrock/Vertex/Foundry incorrectly referencing status.claude.com
- **Fixed**: Multiple additional issues — bare URLs unclickable when terminal wraps them across lines, feedback surveys appearing back-to-back, Windows `CLAUDE_ENV_FILE` and SessionStart hook env files now apply, drive-letter path permission rules correctly root-anchored
- **Fixed**: Plugin error handling improvements — dependency errors distinguish conflicting/invalid/overly complex version requirements; stale resolved versions after `plugin update`; `plugin install` recovers from interrupted installs
- **Reverted**: v2.1.110 cap on non-streaming fallback retries — it traded long waits for more outright failures during API overload

---

### v2.1.110 (2026-04-16)

> /tui fullscreen command, push notification tool, --resume resurrects scheduled tasks, /focus command, 30+ bug fixes.

- **New**: `/tui` command and `tui` setting — run `/tui fullscreen` to switch to flicker-free rendering within the same conversation
- **New**: Push notification tool (`PushNotification`) — Claude can send mobile push notifications when Remote Control and "Push when Claude decides" config are enabled
- **New**: `--resume`/`--continue` now resurrects unexpired scheduled tasks
- **New**: `/focus` command — focus view is now toggled separately; `Ctrl+O` reverts to toggling between normal and verbose transcript only
- **New**: `autoScrollEnabled` config — disable conversation auto-scroll in fullscreen mode
- **New**: Option to show Claude's last response as commented context in the `Ctrl+G` external editor (enable via `/config`)
- **Improved**: `/plugin` Installed tab — items needing attention and favorites appear at the top; disabled items hidden behind a fold; `f` to favorite
- **Improved**: `/doctor` warns when an MCP server is defined in multiple config scopes with different endpoints
- **Improved**: Session recap now enabled for users with telemetry disabled (Bedrock, Vertex, Foundry, `DISABLE_TELEMETRY`); opt out via `/config` or `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0`
- **Improved**: Write tool informs the model when you edit proposed content in the IDE diff before accepting; Bash tool enforces documented maximum timeout
- **Fixed**: MCP tool calls hanging indefinitely when server connection drops mid-response on SSE/HTTP transports
- **Fixed**: Non-streaming fallback retries causing multi-minute hangs when API is unreachable
- **Fixed**: `PermissionRequest` hooks returning `updatedInput` not being re-checked against `permissions.deny` rules; `setMode:'bypassPermissions'` now respects `disableBypassPermissionsMode`
- **Fixed**: `PreToolUse` hook `additionalContext` dropped when the tool call fails
- **Fixed**: stdio MCP servers that print stray non-JSON lines to stdout being disconnected on first stray line (regression in 2.1.105)
- **Fixed**: Headless/SDK auto-title firing an extra Haiku request when `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` or `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` is set
- **Fixed**: Garbled startup rendering in macOS Terminal.app and other terminals without synchronized output support
- **Security**: Hardened "Open in editor" actions against command injection from untrusted filenames
- **Fixed**: Multiple additional issues — high CPU usage in fullscreen, dropped keystrokes after relaunch, `/skills` menu not scrolling, Remote Control session renames not persisting, session cleanup not removing subagent transcripts

---

### v2.1.109 (2026-04-15)

> Improved extended-thinking indicator with a rotating progress hint.

- **Improved**: Extended-thinking indicator now shows a rotating progress hint for better visibility during long thinking phases

---

### v2.1.108 (2026-04-15)

> 1-hour prompt cache TTL option, /recap session context feature, built-in slash commands discoverable via Skill tool, /undo alias for /rewind.

- **New**: `ENABLE_PROMPT_CACHING_1H` env var — opt into 1-hour prompt cache TTL on API key, Bedrock, Vertex, and Foundry (`ENABLE_PROMPT_CACHING_1H_BEDROCK` deprecated but still honored); `FORCE_PROMPT_CACHING_5M` to force 5-minute TTL
- **New**: `/recap` feature — provides context when returning to a session after a break; configurable in `/config`; force with `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` if telemetry disabled
- **New**: Model can now discover and invoke built-in slash commands like `/init`, `/review`, `/security-review` via the Skill tool
- **New**: `/undo` is now an alias for `/rewind`
- **New**: "verbose" indicator when viewing the detailed transcript (`Ctrl+O`)
- **New**: Startup warning when prompt caching is disabled via `DISABLE_PROMPT_CACHING*` environment variables
- **Improved**: `/model` now warns before switching models mid-conversation (next response re-reads full history uncached)
- **Improved**: `/resume` picker defaults to sessions from the current directory; press `Ctrl+A` to show all projects
- **Improved**: Error messages distinguish server rate limits from plan usage limits; 5xx/529 errors link to status.claude.com; unknown slash commands suggest closest match
- **Improved**: Memory footprint for file reads, edits, and syntax highlighting reduced by loading language grammars on demand
- **Fixed**: Paste not working in the `/login` code prompt (regression in 2.1.105)
- **Fixed**: `DISABLE_TELEMETRY` subscribers falling back to 5-minute prompt cache TTL instead of 1 hour
- **Fixed**: Bash tool producing no output when `CLAUDE_ENV_FILE` (e.g. `~/.zprofile`) ends with a `#` comment line
- **Fixed**: `--resume <session-id>` losing session's custom name and color set via `/rename`
- **Fixed**: Diacritical marks (accents, umlauts, cedillas) being dropped from responses when `language` setting is configured
- **Fixed**: `--teleport` and `--resume <id>` precondition errors (dirty git tree, session not found) exiting silently

---

### v2.1.107 (2026-04-14)

> Show thinking hints sooner during long operations.

- **Improved**: Thinking hints now appear sooner during long operations for better real-time feedback

---

### v2.1.105 (2026-04-13)

> EnterWorktree path parameter, PreCompact hook blocking, plugin background monitors, /proactive alias, WebFetch strips CSS/JS, /doctor with status icons and f-to-fix, and multiple bug fixes.

- **New**: `path` parameter on `EnterWorktree` tool — switch into an existing worktree of the current repository
- **New**: PreCompact hook support — hooks can block compaction by exiting with code 2 or returning `{"decision":"block"}`
- **New**: Background monitor support for plugins via a top-level `monitors` manifest key — auto-arms at session start or on skill invoke
- **New**: `/proactive` is now an alias for `/loop`
- **Improved**: Stalled API streams now abort after 5 minutes of no data and retry non-streaming instead of hanging indefinitely
- **Improved**: Network error messages show retry immediately instead of a silent spinner
- **Improved**: `/doctor` layout with status icons; press `f` to have Claude fix reported issues
- **Improved**: `WebFetch` strips `<style>` and `<script>` contents — CSS-heavy pages no longer exhaust content budget before reaching actual text
- **Improved**: Skill description listing cap raised from 250 to 1,536 characters; startup warning when descriptions are truncated
- **Improved**: Stale agent worktree cleanup now removes worktrees whose PR was squash-merged
- **Fixed**: Images attached to queued messages (sent while Claude is working) being dropped
- **Fixed**: Screen going blank when prompt input wraps to second line in long conversations
- **Fixed**: `/model` picker on Bedrock in non-US regions persisting invalid `us.*` model IDs when inference profile discovery is in-flight
- **Fixed**: 429 rate-limit errors showing raw JSON dump instead of clean message for API-key, Bedrock, and Vertex users
- **Fixed**: MCP tools missing on first turn of headless/remote-trigger sessions when MCP servers connect asynchronously
- **Fixed**: Various crash and `/resume` failures including malformed text blocks and `/help` layout at short terminal heights
- **Fixed**: `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` in one project settings permanently disabling usage metrics for all projects

---

### v2.1.101 (2026-04-10)

> /team-onboarding command for teammate ramp-up, OS CA certificate store trusted by default for enterprise TLS proxies, /ultraplan auto-creates cloud environment, and 40+ bug fixes including --resume context loss, Bedrock SigV4 auth, sub-agent worktree file access, and Grep ENOENT self-heal.

- **New**: `/team-onboarding` command — generates a teammate ramp-up guide from your local Claude Code usage patterns
- **New**: OS CA certificate store is now trusted by default — enterprise TLS proxies work without extra config; set `CLAUDE_CODE_CERT_STORE=bundled` to revert to bundled CAs only
- **New**: `/ultraplan` and other remote-session features now auto-create a default cloud environment instead of requiring web setup first
- **Improved**: `claude -p --resume <name>` now accepts session titles set via `/rename` or `--name`
- **Improved**: Unrecognized hook event names in `settings.json` no longer cause the entire file to be ignored
- **Improved**: Rate-limit retry messages show which limit was hit and when it resets (instead of opaque countdown)
- **Improved**: Brief mode retries once when Claude responds with plain text instead of a structured message
- **Fixed**: `--resume`/`--continue` losing conversation context on large sessions when the loader anchored on a dead-end branch
- **Fixed**: Bedrock SigV4 authentication failing with 403 when `ANTHROPIC_AUTH_TOKEN`, `apiKeyHelper`, or `ANTHROPIC_CUSTOM_HEADERS` set an Authorization header
- **Fixed**: Sub-agents running in isolated worktrees denied Read/Edit access to files inside their own worktree
- **Fixed**: `RemoteTrigger` tool's `run` action sending an empty body and being rejected by the server
- **Fixed**: Grep tool ENOENT when the embedded ripgrep binary path becomes stale (VS Code extension auto-update, macOS App Translocation) — now falls back to system `rg` and self-heals mid-session
- **Fixed**: Hardcoded 5-minute request timeout aborting slow backends (local LLMs, extended thinking, slow gateways) regardless of `API_TIMEOUT_MS`
- **Fixed**: Command injection vulnerability in POSIX `which` fallback used by LSP binary detection
- **Fixed**: `permissions.deny` rules not overriding a PreToolUse hook's `permissionDecision: "ask"`
- **Fixed**: Memory leak where long sessions retained dozens of historical copies of the message list in the virtual scroller
- **Fixed**: `/btw` writing a full conversation copy to disk on every use

### v2.1.98 (2026-04-10)

> Vertex AI interactive setup wizard, Monitor tool for background script streaming, major Bash security hardening (8+ permission bypasses fixed), and subprocess PID namespace sandboxing.

- **New**: Interactive Vertex AI setup wizard from the login screen (select "3rd-party platform") — guides through GCP authentication, project and region configuration, credential verification, and model pinning
- **New**: Monitor tool for streaming events from background scripts
- **New**: `CLAUDE_CODE_PERFORCE_MODE` env var — Edit/Write/NotebookEdit fail on read-only files with a `p4 edit` hint instead of silently overwriting
- **New**: Subprocess sandboxing with PID namespace isolation on Linux when `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` is set; `CLAUDE_CODE_SCRIPT_CAPS` env var to limit per-session script invocations
- **New**: `--exclude-dynamic-system-prompt-sections` flag in print mode for improved cross-user prompt caching
- **New**: W3C `TRACEPARENT` env var injected into Bash tool subprocesses when OTEL tracing is enabled
- **New**: LSP: Claude Code now identifies itself via `clientInfo` in the initialize request
- **Security (Bash)**: Fixed permission bypass where backslash-escaped flags could be auto-allowed as read-only and execute arbitrary code
- **Security (Bash)**: Fixed compound commands bypassing forced permission prompts in auto and bypass-permissions modes
- **Security (Bash)**: Fixed read-only commands with unknown env-var prefixes not prompting (only `LANG`, `TZ`, `NO_COLOR`, etc. are now safe-listed)
- **Security (Bash)**: Fixed `/dev/tcp/...` and `/dev/udp/...` redirects not prompting
- **Security (Bash)**: Fixed `grep -f FILE` / `rg -f FILE` not prompting when reading pattern files outside the working directory
- **Fixed**: Stalled streaming responses timing out instead of falling back to non-streaming mode
- **Fixed**: `--dangerously-skip-permissions` silently downgraded to accept-edits mode after approving a protected-path Bash write
- **Fixed**: Managed-settings allow rules remaining active after admin removal until process restart
- **Fixed**: `permissions.additionalDirectories` changes not applying mid-session; `--add-dir` access unaffected by removal
- **Fixed**: MCP OAuth `oauth.authServerMetadataUrl` not honored on token refresh — fixes ADFS and similar IdPs
- **Fixed**: 429 retries burning all attempts in ~13s with small `Retry-After` — exponential backoff now applies as minimum
- **Fixed**: Capital letters dropped to lowercase in xterm/VS Code integrated terminal with kitty keyboard protocol active
- **Fixed**: macOS text replacements deleting trigger word instead of inserting substitution
- **Fixed**: Agent team members not inheriting leader's permission mode with `--dangerously-skip-permissions`
- **Fixed**: `CLAUDE_CODE_MAX_CONTEXT_TOKENS` now honors `DISABLE_COMPACT`
- **Improved**: `/agents` with tabbed layout — Running tab shows live subagents, Library tab adds Run and View actions
- **Improved**: `/resume` filter hint labels; project/worktree/branch names in filter indicator
- **Improved**: Accept Edits mode auto-approves filesystem commands prefixed with safe env vars or process wrappers
- **Improved**: Write tool diff computation 60% faster on files with tabs/`&`/`$`

### v2.1.97 (2026-04-09)

> Major bug-fix release with 30+ fixes across NO_FLICKER mode, /resume, permissions, and MCP — plus focus view toggle and status line enhancements.

- **New**: Focus view toggle (`Ctrl+O`) in NO_FLICKER mode — shows prompt, one-line tool summary with edit diffstats, and final response
- **New**: `refreshInterval` status line setting — re-runs the status line command every N seconds
- **New**: `workspace.git_worktree` field added to status line JSON input, populated when inside a linked git worktree
- **New**: `● N running` indicator in `/agents` next to agent types with live subagent instances
- **New**: Syntax highlighting for Cedar policy files (`.cedar`, `.cedarpolicy`)
- **Fixed (permissions)**: `--dangerously-skip-permissions` silently downgraded to accept-edits mode after approving a write to a protected path
- **Fixed (permissions)**: Permission rules with names matching JS prototype properties (e.g. `toString`) causing `settings.json` to be silently ignored
- **Fixed (permissions)**: Managed-settings allow rules remaining active after admin removal until process restart
- **Fixed (permissions)**: `permissions.additionalDirectories` changes not applying mid-session; removing a dir now correctly revokes access without affecting `--add-dir` entries
- **Fixed (MCP)**: HTTP/SSE connections accumulating ~50 MB/hr of unreleased buffers on reconnect
- **Fixed (MCP)**: OAuth `oauth.authServerMetadataUrl` not honored on token refresh after restart — fixes ADFS and similar IdPs
- **Fixed (rate limits)**: 429 retries burning all attempts in ~13 s when server returns small `Retry-After` — exponential backoff now applies as minimum
- **Fixed (rate limits)**: Rate-limit upgrade options disappearing after context compaction
- **Fixed (/resume)**: 6 fixes — `--resume <name>` opened uneditable, Ctrl+A wiped search, empty list swallowed navigation, task-status replaced conversation summary, cross-project staleness, file-edit diffs disappearing for files >10 KB
- **Fixed (transcript)**: `--resume` cache misses from attachment messages not saved; messages typed during Claude's response not persisted
- **Fixed (hooks)**: `Stop`/`SubagentStop` hooks failing on long sessions; hook evaluator API errors showing "JSON validation failed" instead of actual message
- **Fixed (subagents)**: Worktree isolation / `cwd:` override leaking working directory back to parent Bash tool
- **Fixed (compaction)**: Duplicate multi-MB subagent transcript files on prompt-too-long retries
- **Fixed (plugins)**: `claude plugin update` reporting "already at latest" for git-based marketplace plugins with newer remote commits; slash command picker breaking when plugin frontmatter `name` is a YAML boolean keyword
- **Fixed (NO_FLICKER, 15 fixes)**: Wrapped URL spaces, zellij scroll artifacts, MCP result hover crash, API retry memory leak, slow Windows Terminal mouse-wheel, custom status line hidden on terminals <24 rows, Shift+Enter/Alt+arrow in Warp, CJK text garbled on Windows copy, footer indicator wrapping, blockquote left bar across wrapped lines, transient context-low notification
- **Fixed (Bedrock)**: SigV4 auth failing when `AWS_BEARER_TOKEN_BEDROCK` / `ANTHROPIC_BEDROCK_BASE_URL` set to empty strings (as GitHub Actions does for unset inputs)
- **Improved**: Accept Edits mode auto-approves filesystem commands prefixed with safe env vars or process wrappers (e.g. `LANG=C rm foo`, `timeout 5 mkdir out`)
- **Improved**: Auto mode and bypass-permissions mode auto-approve sandbox network access prompts; `sandbox.network.allowMachLookup` now takes effect on macOS
- **Improved**: Pasted and attached images compressed to same token budget as Read tool images
- **Improved**: Slash command and `@`-mention completion now triggers after CJK sentence punctuation — Japanese/Chinese input no longer requires a space before `/` or `@`
- **Improved**: Bridge sessions show local git repo, branch, and working directory on the claude.ai session card
- **Improved**: Session transcript size reduced by skipping empty hook entries and capping stored pre-edit file copies; per-block entries now carry final token usage
- **Updated**: `/claude-api` skill covers Managed Agents alongside the Claude API

---

### v2.1.96 (2026-04-08)

> Hotfix release addressing a Bedrock authentication regression introduced in v2.1.94.

- **Fixed**: Bedrock requests failing with `403 "Authorization header is missing"` when using `AWS_BEARER_TOKEN_BEDROCK` or `CLAUDE_CODE_SKIP_BEDROCK_AUTH` (regression from v2.1.94)

---

### v2.1.94 (2026-04-07)

> Feature release adding Amazon Bedrock Mantle support, raising the default effort level for professional users, and improving plugin skill naming.

- **New**: Amazon Bedrock powered by Mantle support — set `CLAUDE_CODE_USE_MANTLE=1`
- **New**: Default effort level changed from medium to **high** for API-key, Bedrock/Vertex/Foundry, Team, and Enterprise users (control with `/effort`)
- **New**: Plugin skills declared via `"skills": ["./"]` now use frontmatter `name` instead of directory basename — stable naming across install methods
- **New**: Compact `Slacked #channel` header with clickable link for Slack MCP send-message tool calls
- **New**: `keep-coding-instructions` frontmatter field support for plugin output styles
- **New**: `hookSpecificOutput.sessionTitle` on `UserPromptSubmit` hooks for setting session title programmatically
- **Fixed**: Agents stuck after 429 rate-limit with long Retry-After — error surfaces immediately instead of silently waiting
- **Fixed**: Console login on macOS silently failing with "Not logged in" when login keychain is locked — error now surfaced with `claude doctor` fix guidance
- **Fixed**: Plugin skill hooks defined in YAML frontmatter being silently ignored
- **Fixed**: Scrollback showing duplicate diffs and blank pages in long-running sessions

---

### v2.1.92 (2026-04-04)

> Feature release adding interactive Bedrock wizard, fail-closed managed settings enforcement, and /cost per-model breakdown.

- **New**: Interactive Bedrock setup wizard from the login screen ("3rd-party platform") — step-by-step AWS auth, region config, credential verification, and model pinning
- **New**: `forceRemoteSettingsRefresh` policy setting — blocks CLI startup until managed settings are freshly fetched, exits with error if fetch fails (fail-closed enforcement)
- **New**: Per-model and cache-hit cost breakdown in `/cost` for subscription users
- **New**: `/release-notes` is now an interactive version picker
- **New**: Remote Control session names use hostname as default prefix (e.g. `myhost-graceful-unicorn`), overridable with `--remote-control-session-name-prefix`
- **New**: Pro users see a footer hint when returning after prompt cache expiry, estimating uncached tokens for next turn
- **Fixed**: Subagent spawning permanently failing with "Could not determine pane count" after tmux windows are killed or renumbered
- **Fixed**: API 400 error when extended thinking produced a whitespace-only text block alongside real content
- **Fixed**: Linux sandbox `apply-seccomp` helper now shipped in both npm and native builds — restores unix-socket blocking for sandboxed commands
- **Improved**: Write tool diff computation 60% faster for large files with tabs/`&`/`$`
- **Removed**: `/tag` command
- **Removed**: `/vim` command — toggle vim mode via `/config` → Editor mode

---

### v2.1.91 (2026-04-03)

> Maintenance release with MCP result size override, plugin executable support, and Edit tool token reduction.

- **New**: MCP tool result size override via `_meta["anthropic/maxResultSizeChars"]` annotation (up to 500K) — large DB schemas and API payloads pass through without truncation
- **New**: `disableSkillShellExecution` setting — disable inline shell execution in skills, slash commands, and plugin commands
- **New**: Plugins can ship executables under `bin/` for direct Bash tool invocation without full path
- **New**: Multi-line prompts now supported in `claude-cli://open?q=` deep links (`%0A` encoded newlines accepted)
- **Fixed**: `--resume` losing conversation history when async transcript writes fail silently
- **Fixed**: `cmd+delete` not deleting to start of line in iTerm2, Kitty, WezTerm, Ghostty, Windows Terminal
- **Fixed**: Plan mode in remote sessions losing track of plan file after container restart
- **Fixed**: JSON schema validation for `permissions.defaultMode: "auto"` in settings.json
- **Improved**: Edit tool uses shorter `old_string` anchors — reduces output tokens
- **Improved**: `/claude-api` skill guidance expanded with agent design patterns (tool surface decisions, context management, caching strategy)
- **Improved**: `stripAnsi` ~2x faster on Bun via `Bun.stripANSI`

---

### v2.1.90 (2026-04-02)

> Feature release adding `/powerup` interactive lessons, PowerShell tool hardening, and key performance/reliability fixes.

- **New**: `/powerup` command — interactive animated lessons teaching Claude Code features with live terminal demos
- **Fixed**: Infinite loop crashing sessions when rate-limit options dialog repeatedly auto-opened after hitting usage limit
- **Fixed**: `--resume` causing full prompt-cache miss on first request for users with deferred tools, MCP servers, or custom agents (regression since v2.1.69)
- **Fixed**: `PreToolUse` hooks that emit JSON to stdout and exit with code 2 not correctly blocking the tool call
- **Fixed**: Collapsed search/read summary badge appearing multiple times in fullscreen scrollback during CLAUDE.md auto-load
- **Fixed**: Auto mode not respecting explicit user boundaries ("don't push", "wait for X before Y")
- **Fixed**: Headers disappearing when scrolling `/model`, `/config`, and other selection screens
- **Hardened**: PowerShell tool permissions — trailing `&` background job bypass, `-ErrorAction Break` debugger hang, archive-extraction TOCTOU, parse-fail fallback deny-rule degradation
- **Improved**: SSE transport handles large streamed frames in linear time (was quadratic)
- **Improved**: Eliminated per-turn JSON.stringify of MCP tool schemas on cache-key lookup
- **Improved**: `/resume` all-projects view loads project sessions in parallel
- **Changed**: `--resume` picker no longer shows sessions created by `claude -p` or SDK invocations

---

### v2.1.89 (2026-04-01)

> Large bugfix + feature release with new hook types, headless workflow improvements, and notable behavior changes.

- **New**: `"defer"` permission decision for `PreToolUse` hooks — headless sessions can pause at a tool call and resume with `-p --resume` to re-evaluate
- **New**: `PermissionDenied` hook — fires after auto mode classifier denials; return `{retry: true}` to let the model retry with an alternative approach
- **New**: Named subagents now appear in `@` mention typeahead suggestions for easier invocation
- **New**: `CLAUDE_CODE_NO_FLICKER=1` env var to opt into flicker-free alt-screen rendering with virtualized scrollback
- **New**: `MCP_CONNECTION_NONBLOCKING=true` for `-p` mode — skips MCP connection wait; `--mcp-config` servers bounded at 5s
- **New**: Auto mode denied commands now show a notification and appear in `/permissions` → Recent tab
- **Changed**: Thinking summaries are no longer generated by default in interactive sessions — add `showThinkingSummaries: true` to `settings.json` to restore
- **Improved**: `/env` now applies to PowerShell tool commands (previously only affected Bash)
- **Improved**: PowerShell tool prompt with version-appropriate syntax guidance (5.1 vs 7+)
- **Fixed**: `StructuredOutput` schema cache bug causing ~50% failure rate in workflows with multiple schemas
- **Fixed**: Edit/Write tools doubling CRLF on Windows and stripping Markdown hard line breaks (two trailing spaces)
- **Fixed**: Hooks `if` condition filtering not matching compound commands (`ls && git push`) or commands with env-var prefixes (`FOO=bar git push`)
- **Fixed**: Prompt cache misses in long sessions caused by tool schema bytes changing mid-session
- **Fixed**: Nested CLAUDE.md files being re-injected dozens of times in long sessions that read many files
- **Fixed**: Memory leaks: large JSON LRU cache key retention, LSP diagnostic data, StructuredOutput cache
- **Fixed**: Crashes: large file edits (>1 GiB), large session file removal (>50 MB), `--resume` with old tool results
- **Fixed**: Voice mode: macOS Apple Silicon microphone permission, Windows WebSocket 101 error, modifier-combo push-to-talk
- **Fixed**: `/stats` losing historical data beyond 30 days; `/stats` undercounting tokens from subagent/fork usage
- **Fixed**: Scrollback disappearing when scrolling up in long sessions; rendering artifacts on main-screen terminals
- **Fixed**: SDK error result messages (`error_during_execution`, `error_max_turns`) now correctly set `is_error: true`
- **Fixed**: PreToolUse/PostToolUse hooks not providing `file_path` as absolute path for Write/Edit/Read tools

> **Breaking**: Thinking summaries now off by default. Set `showThinkingSummaries: true` in settings.json to restore.

---

### v2.1.87 (2026-03-30)

- **Fixed**: Messages in Cowork Dispatch not getting delivered

---

### v2.1.86 (2026-03-28)

- **New**: `X-Claude-Code-Session-Id` header added to API requests — proxies can aggregate requests by session without parsing the body
- **New**: `.jj` and `.sl` added to VCS directory exclusion lists so Grep and file autocomplete don't descend into Jujutsu or Sapling metadata
- **Improved**: Reduced token overhead when mentioning files with `@` — raw string content no longer JSON-escaped
- **Improved**: Better prompt cache hit rate for Bedrock, Vertex, and Foundry users by removing dynamic content from tool descriptions
- **Improved**: Read tool now uses compact line-number format and deduplicates unchanged re-reads, reducing token usage
- **Improved**: Skill descriptions in `/skills` listing capped at 250 characters to reduce context usage; `/skills` menu now sorted alphabetically
- **Improved**: Reduced startup event-loop stalls when many claude.ai MCP connectors are configured (macOS keychain cache extended from 5s to 30s)
- **Fixed**: Official marketplace plugin scripts failing with "Permission denied" on macOS/Linux since v2.1.83
- **Fixed**: `--resume` failing with "tool_use ids were found without tool_result blocks" on sessions created before v2.1.85
- **Fixed**: Write/Edit/Read failing on files outside the project root (e.g., `~/.claude/CLAUDE.md`) when conditional skills or rules are configured
- **Fixed**: Unnecessary config disk writes on every skill invocation — could cause performance issues and config corruption on Windows
- **Fixed**: Potential out-of-memory crash when using `/feedback` on very long sessions with large transcript files
- **Fixed**: `--bare` mode dropping MCP tools in interactive sessions and silently discarding messages enqueued mid-turn
- **Fixed**: `c` shortcut copying only ~20 characters of the OAuth login URL instead of the full URL
- **Fixed**: Masked input (e.g., OAuth code paste) leaking the start of the token when wrapping across multiple lines on narrow terminals
- **Fixed**: Statusline showing another session's model when running multiple Claude Code instances and using `/model`
- **Fixed**: Scroll not following new messages after wheel scroll or click-to-select at bottom of a long conversation
- **Fixed**: `/plugin` uninstall dialog: pressing `n` now correctly uninstalls while preserving the plugin's data directory
- **Fixed**: Regression where pressing Enter after clicking could leave the transcript blank until the response arrived
- **Fixed**: `ultrathink` hint lingering after deleting the keyword
- **Fixed**: Memory growth in long sessions from markdown/highlight render caches retaining full content strings
- **Fixed (VSCode)**: Extension incorrectly showing "Not responding" during long-running operations
- **Fixed (VSCode)**: Extension defaulting Max plan users to Sonnet after OAuth token refresh (8 hours after login)

### v2.1.85 (2026-03-27)

- **New**: Conditional `if` field for hooks — filter when hooks run using permission rule syntax (e.g., `Bash(git *)`) to reduce unnecessary process spawning overhead
- **New**: `CLAUDE_CODE_MCP_SERVER_NAME` and `CLAUDE_CODE_MCP_SERVER_URL` env vars for MCP `headersHelper` scripts, allowing one helper script to serve multiple MCP servers
- **New**: PreToolUse hooks can now satisfy `AskUserQuestion` by returning `updatedInput` alongside `permissionDecision: "allow"` — enables headless integrations to collect answers via their own UI
- **New**: Timestamp markers in transcripts when scheduled tasks (`/loop`, `CronCreate`) fire
- **New**: Deep link queries (`claude-cli://open?q=…`) now support up to 5,000 characters with a "scroll to review" warning for long pre-filled prompts
- **New**: MCP OAuth now follows RFC 9728 Protected Resource Metadata discovery to find the authorization server
- **New**: Plugins blocked by organization policy (`managed-settings.json`) are now hidden from marketplace views and cannot be installed/enabled
- **New**: `tool_parameters` in OpenTelemetry `tool_result` events are now gated behind `OTEL_LOG_TOOL_DETAILS=1`
- **Improved**: Scroll performance with large transcripts — WASM yoga-layout replaced with pure TypeScript implementation
- **Improved**: `@`-mention file autocomplete performance on large repositories
- **Improved**: PowerShell dangerous command detection
- **Fixed**: `/compact` failing with "context exceeded" when the conversation itself was too large for the compact request to fit
- **Fixed**: `deniedMcpServers` setting not blocking claude.ai MCP servers
- **Fixed**: Terminal left in enhanced keyboard mode after exit in Ghostty, Kitty, WezTerm — Ctrl+C and Ctrl+D now work correctly after quitting
- **Fixed**: `--worktree` exiting with an error in non-git repositories before the `WorktreeCreate` hook could run
- **Fixed**: MCP step-up authorization failing when a refresh token exists (servers requesting elevated scopes via `403 insufficient_scope`)
- **Fixed**: Prompts getting stuck in queue after running certain slash commands (up-arrow unable to retrieve them)
- **Fixed**: Raw key sequences appearing in prompt when running over SSH or in VS Code integrated terminal
- **Fixed**: `shift+enter` and `meta+enter` being intercepted by typeahead suggestions instead of inserting newlines
- **Fixed**: Remote Control session status stuck on "Requires Action" after a permission is resolved
- **Fixed**: Memory leak in remote sessions when a streaming response is interrupted
- **Fixed**: Python Agent SDK: `type:'sdk'` MCP servers passed via `--mcp-config` no longer dropped during startup
- **Fixed**: Crash when `OTEL_LOGS_EXPORTER`, `OTEL_METRICS_EXPORTER`, or `OTEL_TRACES_EXPORTER` is set to `none`
- **Fixed**: Diff syntax highlighting not working in non-native builds
- **Fixed**: Stale content bleeding through when scrolling up during streaming

### v2.1.84 (2026-03-26)

- **New**: PowerShell tool for Windows (opt-in preview) — direct PowerShell access alongside Bash tool. Learn more at https://code.claude.com/docs/en/tools-reference#powershell-tool
- **New**: `TaskCreated` hook fires when a task is created via `TaskCreate`
- **New**: `WorktreeCreate` hook now supports `type: "http"` — return the created worktree path via `hookSpecificOutput.worktreePath` in the response JSON
- **New**: `allowedChannelPlugins` managed setting for team/enterprise admins to define a channel plugin allowlist
- **New**: `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL_SUPPORTS` env vars to override effort/thinking capability detection for pinned models on Bedrock, Vertex, Foundry; `_MODEL_NAME`/`_DESCRIPTION` to customize the `/model` picker label
- **New**: `CLAUDE_STREAM_IDLE_TIMEOUT_MS` env var to configure the streaming idle watchdog threshold (default 90s)
- **New**: Idle-return prompt nudging users back after 75+ minutes to `/clear`, reducing unnecessary token re-caching on stale sessions
- **New**: Deep links (`claude-cli://`) now open in your preferred terminal instead of whichever terminal is detected first
- **New**: `x-client-request-id` header added to API requests for debugging timeouts
- **New**: Rules and skills `paths:` frontmatter now accepts a YAML list of globs
- **New**: MCP tool descriptions and server instructions capped at 2KB to prevent OpenAPI-generated servers from bloating context
- **New**: `ANTHROPIC_CUSTOM_MODEL_OPTION` env var to add a custom entry to the `/model` picker
- **New**: Managed settings can now be set via macOS plist or Windows Registry
- **Improved**: Global system-prompt caching now works when `ToolSearch` is enabled, including for users with many MCP tools
- **Improved**: Better dangerous-removal detection for Windows drive roots (`C:\`, `C:\Windows`, etc.)
- **Improved**: Interactive startup ~30ms faster (parallel `setup()` with slash command/agent loading)
- **Improved**: Stats screenshot (Ctrl+S in `/stats`) now works in all builds and is 16x faster
- **Improved**: p90 prompt cache hit rate improved
- **Fixed**: `ANTHROPIC_BETAS` environment variable being silently ignored when using Haiku models
- **Fixed**: Startup performance issue on partial clone repositories (Scalar/GVFS) that triggered mass blob downloads
- **Fixed**: Spurious "Not logged in" errors on macOS caused by transient keychain read failures
- **Fixed**: Cold-start race where core tools could be deferred without their bypass active (Edit/Write failing with InputValidationError)
- **Fixed**: Native terminal cursor not tracking input caret (IME composition for CJK now renders inline)
- **Fixed**: Workflow subagents failing with API 400 when outer session uses `--json-schema` and subagent also specifies a schema
- **Fixed**: Hang when generating attachment snippets for large edited files; MCP tool/resource cache leak on reconnect
- **Fixed**: Voice push-to-talk leaking characters into text input; transcripts now insert at correct position
- **Fixed**: `Ctrl+U` (kill-to-line-start) being a no-op at line boundaries in multiline input
- **Fixed**: Null-unbinding a default chord binding still entering chord-wait mode instead of freeing the prefix key
- **Changed**: Issue/PR references only become clickable links when written as `owner/repo#123` — bare `#123` no longer auto-linked
- **Changed**: Slash commands unavailable for current auth setup (`/voice`, `/mobile`, `/chrome`, `/upgrade`, etc.) are now hidden instead of shown
- **VSCode**: Added rate limit warning banner with usage percentage and reset time
- **VSCode**: Fixed Windows PATH inheritance for Bash tool regression (regression from v2.1.78 fix)

### v2.1.83 (2026-03-25)

- **New**: `managed-settings.d/` drop-in directory alongside `managed-settings.json` — separate teams can deploy independent policy fragments that merge alphabetically
- **New**: `CwdChanged` and `FileChanged` hook events for reactive environment management (e.g., direnv, auto-toolchain switching)
- **New**: `sandbox.failIfUnavailable` setting — exits with an error when sandbox is enabled but cannot start, instead of running unsandboxed
- **New**: `disableDeepLinkRegistration` setting to prevent `claude-cli://` protocol handler registration
- **New**: `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` strips Anthropic and cloud provider credentials from Bash tool, hooks, and MCP stdio server subprocess environments
- **New**: Transcript search — press `/` in transcript mode (Ctrl+O) to search, `n`/`N` to step through matches
- **New**: `Ctrl+X Ctrl+E` as an alias for opening the external editor (readline-native binding; `Ctrl+G` still works)
- **New**: Pasted images now insert an `[Image #N]` chip at cursor for positional referencing in prompts
- **New**: Agents can declare `initialPrompt` in frontmatter to auto-submit a first turn
- **New**: `chat:killAgents` and `chat:fastMode` are now rebindable via `~/.claude/keybindings.json`
- **Security**: Fixed `--mcp-config` CLI flag bypassing `allowedMcpServers`/`deniedMcpServers` managed policy enforcement
- **Fixed**: Claude Code hanging on exit on macOS
- **Fixed**: Screen flashing blank after being idle for a few seconds
- **Fixed**: Mouse tracking escape sequences leaking to shell prompt after exit
- **Fixed**: Background subagents becoming invisible after context compaction (could cause duplicate agents)
- **Fixed**: `--mcp-config` CLI flag bypassing `allowedMcpServers`/`deniedMcpServers` managed policy
- **Fixed**: Native modules not loading on Amazon Linux 2 and glibc 2.26 systems; Linux sandbox failing with "ripgrep not found"
- **Fixed**: Sessions with `saved_hook_context` causing startup performance issues
- **Fixed**: Conditional `.claude/rules/*.md` and nested CLAUDE.md files not loading in print mode
- **Fixed**: Agents from `.claude/agents/` not discovered in git worktrees (now loads from main repo)
- **Improved**: `WebFetch` identifies as `Claude-User` in requests; binary content (PDFs, audio) saved to disk with correct extension
- **Improved**: Reduced scrollback resets from once per turn to once per ~50 messages
- **Improved**: Increased non-streaming fallback token cap (21k → 64k) and timeout (120s → 300s)
- **Changed**: "Stop all background agents" keybinding moved from `Ctrl+F` to `Ctrl+X Ctrl+K`

### v2.1.81 (2026-03-22)

- **New**: `--bare` flag for scripted `-p` calls — skips hooks, LSP, plugin sync, and skill directory walks; requires `ANTHROPIC_API_KEY` or `apiKeyHelper` via `--settings` (OAuth and keychain auth disabled); auto-memory fully disabled
- **New**: `--channels` permission relay — channel servers that declare the permission capability can now forward tool approval prompts to your phone
- **Changed**: Plan mode hides the "clear context" option by default (restore with `"showClearContextOnPlanAccept": true` in settings)
- **Improved**: MCP read/search tool calls collapse into a single "Queried {server}" line (expand with Ctrl+O)
- **Improved**: `!` bash mode discoverability — Claude now suggests it when you need to run an interactive command
- **Improved**: Plugin freshness — ref-tracked plugins re-clone on every load to pick up upstream changes
- **Improved**: Remote Control session titles refresh after your third message; `/rename` now syncs title for RC sessions
- **Improved**: MCP OAuth updated to support Client ID Metadata Document (CIMD / SEP-991) for servers without Dynamic Client Registration
- **Fixed**: Resuming a worktree session now switches back to that worktree automatically
- **Fixed**: Multiple concurrent sessions requiring repeated re-authentication when one session refreshes its OAuth token
- **Fixed**: Voice mode silently swallowing retry failures with misleading "check your network" message; voice audio not recovering when server silently drops WebSocket
- **Fixed**: `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` not suppressing the structured-outputs beta header (caused 400 errors on Vertex/Bedrock proxies)
- **Fixed**: Race condition where background agent task output could hang indefinitely when task completed between polling intervals
- **Fixed**: `/btw` not including pasted text when used during an active response
- **Fixed**: Plugin hooks blocking prompt submission when plugin directory is deleted mid-session
- **Fixed**: Remote Control `/exit` not reliably archiving the session
- **Fixed**: Node.js 18 crash
- **Fixed**: Unnecessary permission prompts for Bash commands containing dashes in strings
- **Disabled**: Line-by-line response streaming on Windows (including WSL in Windows Terminal) due to rendering issues
- **VSCode**: Fixed Windows PATH inheritance for Bash tool when using Git Bash (regression in v2.1.78)

### v2.1.80 (2026-03-20)

- **New**: `rate_limits` field in statusline scripts for displaying Claude.ai rate limit usage (5-hour and 7-day windows with `used_percentage` and `resets_at`)
- **New**: `source: 'settings'` plugin marketplace source — declare plugin entries inline in `settings.json`
- **New**: CLI tool usage detection to plugin tips, in addition to file pattern matching
- **New**: `effort` frontmatter support for skills and slash commands to override the model effort level when invoked
- **New**: `--channels` (research preview) — allow MCP servers to push messages into your session
- **Fixed**: `--resume` dropping parallel tool results — sessions with parallel tool calls now restore all tool_use/tool_result pairs instead of showing `[Tool result missing]` placeholders
- **Fixed**: Voice mode WebSocket failures caused by Cloudflare bot detection on non-browser TLS fingerprints
- **Fixed**: 400 errors when using fine-grained tool streaming through API proxies, Bedrock, or Vertex
- **Fixed**: `/remote-control` appearing for gateway and third-party provider deployments where it cannot function
- **Fixed**: Managed settings not being applied at startup when `remote-settings.json` was cached from a prior session
- **Performance**: ~80MB memory reduction on startup for large repositories (tested on 250k-file repos)
- **Improved**: Responsiveness of `@` file autocomplete in large git repos; `/effort` now shows what auto currently resolves to
- **Improved**: `/permissions` — Tab and arrow keys now switch tabs from within a list; background tasks panel left arrow closes list view

### v2.1.79 (2026-03-19)

- **New**: `--console` flag to `claude auth login` for Anthropic Console (API billing) authentication
- **New**: "Show turn duration" toggle added to the `/config` menu
- **Fixed**: `claude -p` hanging when spawned as a subprocess without explicit stdin (e.g. Python `subprocess.run`)
- **Fixed**: Ctrl+C not working in `-p` (print) mode
- **Fixed**: `/btw` returning the main agent's output instead of answering the side question when triggered during streaming
- **Fixed**: Voice mode not activating correctly on startup when `voiceEnabled: true` is set
- **Fixed**: Enterprise users unable to retry on rate limit (429) errors
- **Fixed**: `SessionEnd` hooks not firing when using interactive `/resume` to switch sessions
- **Fixed**: Custom status line showing nothing when workspace trust is blocking it
- **Fixed**: `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` not preventing terminal title from being set on startup
- **Performance**: Improved startup memory usage by ~18MB across all scenarios
- **Performance**: Non-streaming API fallback now has a 2-minute per-attempt timeout (prevents indefinite hangs)
- **VSCode**: Added `/remote-control` to bridge session to claude.ai/code for browser/phone continuation
- **VSCode**: Session tabs now get AI-generated titles based on first message
- **VSCode**: Fixed thinking pill showing "Thinking" instead of "Thought for Ns" after response completes

### v2.1.78 (2026-03-18)

- **New**: `StopFailure` hook event that fires when the turn ends due to an API error (rate limit, auth failure, etc.)
- **New**: `${CLAUDE_PLUGIN_DATA}` variable for plugin persistent state that survives plugin updates; `/plugin uninstall` now prompts before deleting plugin data
- **New**: `effort`, `maxTurns`, and `disallowedTools` frontmatter support for plugin-shipped agents
- **New**: `ANTHROPIC_CUSTOM_MODEL_OPTION` env var to add a custom entry to the `/model` picker (with optional `_NAME` and `_DESCRIPTION` suffixed vars)
- **New**: Terminal notifications (iTerm2/Kitty/Ghostty popups, progress bar) now reach the outer terminal when running inside tmux with `set -g allow-passthrough on`
- **New**: Response text now streams line-by-line as it's generated
- **Fixed**: ⚠️ **Security** — Silent sandbox disable when `sandbox.enabled: true` is set but dependencies are missing — now shows a visible startup warning
- **Fixed**: ⚠️ **Security** — `deny: ["mcp__servername"]` permission rules were not removing MCP server tools before sending to the model, allowing it to see and attempt blocked tools
- **Fixed**: ⚠️ **Security** — `.git`, `.claude`, and other protected directories were writable without a prompt in `bypassPermissions` mode
- **Fixed**: Infinite loop when API errors triggered stop hooks that re-fed blocking errors to the model
- **Fixed**: `cc log` and `--resume` silently truncating conversation history on large sessions (>5 MB) that used subagents
- **Fixed**: `sandbox.filesystem.allowWrite` not working with absolute paths (previously required `//` prefix)
- **Fixed**: `--worktree` flag not loading skills and hooks from the worktree directory
- **Fixed**: `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` and `includeGitInstructions` setting not suppressing git status section in system prompt
- **Fixed**: Bash tool not finding Homebrew and other PATH-dependent binaries when VS Code is launched from Dock/Spotlight
- **Fixed**: Voice mode modifier-combo push-to-talk keybindings requiring a hold instead of activating immediately
- **Fixed**: Voice mode not working on WSL2 with WSLg (Windows 11)
- **Fixed**: `ANTHROPIC_BETAS` environment variable being silently ignored when using Haiku models
- **VSCode**: Fixed "API Error: Rate limit reached" when selecting Opus — model dropdown no longer offers 1M context variant to subscribers whose plan tier is unknown
- **Performance**: Improved memory usage and startup time when resuming large sessions

### v2.1.77 (2026-03-17)

- **New**: ⭐ Opus 4.6 default maximum output tokens raised to 64k; upper bound for Opus 4.6 and Sonnet 4.6 raised to 128k tokens
- **New**: `allowRead` sandbox filesystem setting to re-allow read access within `denyRead` regions
- **New**: `/copy N` to copy the Nth-latest assistant response directly
- **New**: `/branch` command (replaces `/fork`; `/fork` still works as an alias)
- **New**: `SendMessage` now auto-resumes stopped agents in the background instead of returning an error
- **Fixed**: ⚠️ **Security** — `PreToolUse` hooks returning `"allow"` could bypass `deny` permission rules including enterprise managed settings
- **Fixed**: Auto-updater accumulating tens of gigabytes of memory when slash-command overlay repeatedly opened/closed, triggering overlapping binary downloads
- **Fixed**: `--resume` silently truncating recent conversation history due to a race between memory-extraction writes and the main transcript
- **Fixed**: "Always Allow" on compound bash commands (e.g. `cd src && npm test`) saving a single rule for the full string instead of per-subcommand, leading to dead rules and repeated permission prompts
- **Fixed**: Write tool silently converting line endings when overwriting CRLF files or creating files in CRLF directories
- **Fixed**: Cost and token usage not tracked when API falls back to non-streaming mode
- **Fixed**: `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` not stripping beta tool-schema fields, causing proxy gateways to reject requests
- **Fixed**: Bash tool reporting errors for successful commands when system temp directory path contains spaces
- **Fixed**: Paste being lost when typing immediately after pasting; Ctrl+D in `/feedback` deleting forward instead of exiting
- **Fixed**: Various rendering fixes: ordered list numbers, CJK bleeding, background colors in tmux, hyperlinks opening twice in VS Code
- **Fixed**: Teammate panes not closing when leader exits; iTerm2 session crash when selecting text inside tmux over SSH
- **Breaking**: `Agent` tool no longer accepts a `resume` parameter — use `SendMessage({to: agentId})` to continue a previously spawned agent
- **VSCode**: Fixed gitignore patterns with commas silently excluding filetypes from `@`-mention file picker; improved scroll wheel responsiveness; improved plan preview tab titles
- **Performance**: Faster startup on macOS (~60ms) by reading keychain credentials in parallel with module loading; faster `--resume` on fork-heavy sessions (up to 45% faster, 100-150MB less peak memory)

### v2.1.76 (2026-03-14)

- **New**: ⭐ MCP elicitation support — MCP servers can now request structured input mid-task via an interactive dialog (form fields or browser URL)
- **New**: `Elicitation` and `ElicitationResult` hooks to intercept and override MCP input responses before they're sent back to the server
- **New**: `PostCompact` hook that fires after compaction completes
- **New**: `-n` / `--name <name>` CLI flag to set a display name for the session at startup
- **New**: `worktree.sparsePaths` setting for `claude --worktree` in large monorepos — check out only needed directories via git sparse-checkout
- **New**: `/effort` slash command to set model effort level
- **Fixed**: Deferred tools (loaded via `ToolSearch`) losing their input schemas after conversation compaction — array and number parameters were being rejected with type errors
- **Fixed**: Auto-compaction retrying indefinitely after consecutive failures — circuit breaker now stops after 3 attempts
- **Fixed**: `Bash(cmd:*)` permission rules not matching when a quoted argument contains `#`
- **Fixed**: Slash commands showing "Unknown skill"
- **Fixed**: Plan mode asking for re-approval after the plan was already accepted
- **Fixed**: Voice mode swallowing keypresses while a permission dialog or plan editor was open
- **Fixed**: `/voice` not working on Windows when installed via npm
- **Fixed**: Bridge sessions failing to recover after extended WebSocket disconnects
- **Improved**: `--worktree` startup performance by reading git refs directly, skipping redundant `git fetch`
- **Improved**: Killing a background agent now preserves its partial results in the conversation context
- **Improved**: Model fallback notifications — now always visible with human-friendly model names
- **Improved**: Stale worktree cleanup — worktrees left behind after interrupted parallel runs are automatically cleaned up
- **Improved**: Blockquote readability on dark terminal themes — italic with left bar instead of dim
- **Updated**: `--plugin-dir` now accepts one path only; use repeated flags for multiple directories
- **VSCode**: Fixed gitignore patterns containing commas silently excluding entire filetypes from the `@`-mention file picker

### v2.1.75 (2026-03-13)

- **New**: ⭐ 1M context window for Opus 4.6 now enabled by default for Max, Team, and Enterprise plans (previously required extra usage)
- **New**: Session name display on the prompt bar when using `/rename`
- **New**: Last-modified timestamps on memory files — helps Claude reason about freshness of memories
- **New**: Hook source display (settings/plugin/skill) in permission prompts when a hook requires confirmation
- **New**: `/color` command available for all users to set a prompt-bar color
- **Fixed**: Token estimation over-counting for thinking and `tool_use` blocks (was causing premature context compaction)
- **Fixed**: Bash tool mangling `!` in piped commands (e.g. `jq 'select(.x != .y)'` now works correctly)
- **Fixed**: Voice mode not activating correctly on fresh installs without toggling `/voice` twice
- **Fixed**: Claude Code header not updating model name after switching with `/model` or Option+P
- **Fixed**: Session crash when attachment message computation returns undefined values
- **Fixed**: Managed-disabled plugins showing up in `/plugin` Installed tab
- **Fixed**: Corrupted marketplace config path handling
- **Fixed**: `/resume` losing session names after resuming a forked or continued session
- **Improved**: Startup performance on macOS non-MDM machines (skips unnecessary subprocess spawns)
- **Improved**: Async hook completion messages suppressed by default (visible with `--verbose` or transcript mode)

### v2.1.74 (2026-03-12)

- **New**: `/context` command shows actionable suggestions — identifies context-heavy tools, memory bloat, capacity warnings with optimization tips
- **New**: `autoMemoryDirectory` setting to configure custom directory for auto-memory storage
- **Fixed**: Memory leak in streaming API response buffers — unbounded RSS growth on Node.js/npm path resolved
- **Fixed**: Managed policy `ask` rules being bypassed by user `allow` rules or skill `allowed-tools`
- **Fixed**: MCP OAuth authentication hanging when callback port is already in use
- **Fixed**: MCP OAuth refresh (Slack) never prompting re-auth after refresh token expires
- **Fixed**: Voice mode on macOS native binary — binary now includes `audio-input` entitlement for microphone permission prompt
- **Fixed**: `SessionEnd` hooks killed after 1.5s regardless of `hook.timeout` (now configurable via `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`)
- **Changed**: `--plugin-dir` local dev copies now override installed marketplace plugins with same name
- **VSCode**: Fixed delete button not working for Untitled sessions

### v2.1.73 (2026-03-11)

- **New**: `modelOverrides` setting — map model picker entries to custom provider model IDs (Bedrock inference profile ARNs, etc.)
- **New**: Actionable guidance when OAuth login or connectivity checks fail due to SSL certificate errors (corporate proxies, `NODE_EXTRA_CA_CERTS`)
- **Fixed**: Freezes and 100% CPU loops triggered by permission prompts for complex bash commands
- **Fixed**: Deadlock when many skill files changed at once (e.g. `git pull` in repo with large `.claude/skills/` directory)
- **Fixed**: Bash tool output lost when running multiple Claude Code sessions in the same project directory
- **Fixed**: Subagents with `model: opus`/`sonnet`/`haiku` being silently downgraded on Bedrock, Vertex, Foundry
- **Fixed**: Background bash processes from subagents not cleaned up when agent exits
- **Fixed**: `SessionStart` hooks firing twice when resuming via `--resume` or `--continue`
- **Fixed**: JSON-output hooks injecting no-op system-reminder messages into the model's context on every turn
- **Fixed**: Linux sandbox failing with "ripgrep not found" on native builds
- **Fixed**: Linux native modules on Amazon Linux 2 (glibc 2.26 systems)
- **Changed**: Default Opus model on Bedrock, Vertex, Foundry → Opus 4.6 (was 4.1)
- **Changed**: Deprecated `/output-style` — use `/config` instead; output style fixed at session start for better prompt caching
- **VSCode**: Fixed HTTP 400 errors for users behind proxies or on Bedrock/Vertex with Claude 4.5 models

### v2.1.72 (2026-03-09)

- **New**: Restored `model` parameter on Agent tool — per-invocation model overrides are back
- **New**: `/plan` accepts optional description (e.g., `/plan fix the auth bug`) to enter plan mode and start immediately
- **New**: `ExitWorktree` tool to leave an `EnterWorktree` session
- **New**: `CLAUDE_CODE_DISABLE_CRON` env var to stop scheduled cron jobs mid-session
- **New**: `lsof`, `pgrep`, `tput`, `ss`, `fd`, `fdfind` added to bash auto-approval allowlist
- **New**: `/copy` `w` key writes selection directly to file, bypassing clipboard (useful over SSH)
- **Changed**: Simplified effort levels to low/medium/high (removed max), new symbols ○ ◐ ●; use `/effort auto` to reset
- **Changed**: CLAUDE.md HTML comments (`<!-- ... -->`) now hidden from Claude when auto-injected (visible via Read tool)
- **Changed**: `/config` — Escape cancels changes, Enter saves and closes, Space toggles settings
- **Fixed**: SDK `query()` prompt cache invalidation — up to 12x input token cost reduction
- **Fixed**: Tool search now activates with `ANTHROPIC_BASE_URL` when `ENABLE_TOOL_SEARCH` is set
- **Fixed**: Skill hooks firing twice per event when a hooks-enabled skill is invoked by the model
- **Fixed**: `/clear` killing background agent/bash tasks — only foreground tasks now cleared
- **Fixed**: Worktree isolation: Task tool resume not restoring cwd, background task notifications missing `worktreePath`/`worktreeBranch`
- **Fixed**: `--continue` not resuming from most recent point after `--compact`
- **Fixed**: Team agents now inherit the leader's model
- **Fixed**: Parallel tool calls — only Bash errors cascade to siblings (Read/WebFetch/Glob failures no longer cancel siblings)
- **Fixed**: Multiple hooks issues: `transcript_path` wrong for resumed/forked sessions, async hooks not receiving stdin, PostToolUse block reason displaying twice
- **Fixed**: Several sandbox permission, plugin installation (Windows/OneDrive), and voice mode issues
- **Perf**: Reduced bundle size by ~510 KB; improved CPU utilization in long sessions; faster bash init via native module

### v2.1.69 (2026-03-04)

- **Security**: Fixed nested skill discovery loading skills from gitignored directories like `node_modules` — critical security fix
- **Security**: Fixed symlink bypass allowing writes outside working directory in `acceptEdits` mode
- **Security**: Fixed trust dialog silently enabling all `.mcp.json` servers on first run (per-server approval now required)
- **Security**: Fixed sandbox not blocking non-allowed domains when `allowManagedDomainsOnly` is enabled
- **New**: `InstructionsLoaded` hook event fires when CLAUDE.md or `.claude/rules/*.md` files are loaded into context
- **New**: `agent_id`, `agent_type`, `worktree` fields added to all hook events (subagent tracking, worktree metadata)
- **New**: `${CLAUDE_SKILL_DIR}` variable for skills to reference their own installation directory in SKILL.md content
- **New**: `/reload-plugins` command to activate pending plugin changes without restarting Claude Code
- **New**: Voice STT expanded to 20 languages (+10: Russian, Polish, Turkish, Dutch, Ukrainian, Greek, Czech, Danish, Swedish, Norwegian)
- **New**: `sandbox.enableWeakerNetworkIsolation` setting (macOS) for Go tools (gh, gcloud, terraform) behind MITM proxy
- **New**: `includeGitInstructions` setting (and `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` env var) to remove built-in commit/PR instructions from system prompt
- **New**: `oauth.authServerMetadataUrl` config option for MCP servers with custom OAuth discovery
- **New**: `pluginTrustMessage` in managed settings for organization-specific plugin trust context
- **New**: Optional `--name` argument for `/remote-control` to set a custom session title visible in claude.ai/code
- **Changed**: Sonnet 4.5 users on Pro/Max/Team auto-migrated to Sonnet 4.6
- **Changed**: `/resume` picker now shows most recent prompt instead of first one
- **Fixed**: 15+ memory leaks — React Compiler memoCache, REPL render scopes (~35MB over 1000 turns), teammate history pinning, hook event accumulation
- **Fixed**: ~16MB baseline memory reduction (deferred Yoga WASM preloading)
- **Fixed**: MCP binary content (PDFs, Office docs, audio) now saved to disk with correct extension instead of raw base64 in context
- **Fixed**: Startup performance — skills/plugins loading, worktree git subprocess, macOS keychain, managed settings
- **Fixed**: Escape not interrupting running turn when input box has draft text
- **Fixed**: Duplicate CLAUDE.md, slash commands, agents, and rules when running from nested worktree
- **Fixed**: macOS keychain corruption with multiple OAuth MCP servers (stdin buffer overflow)

### v2.1.68 (2026-03-04)

- **Changed**: Opus 4.6 now defaults to medium effort for Max and Team subscribers (sweet spot between speed and thoroughness)
- **New**: Re-introduced `ultrathink` keyword to enable high effort for the next turn specifically
- **Breaking**: Opus 4 and Opus 4.1 removed from Claude Code on first-party API — users auto-migrated to Opus 4.6

### v2.1.66 (2026-03-04)

- **Fixed**: Reduced spurious error logging

### v2.1.63 (2026-02-27)

- **New**: HTTP hooks — hooks can now `POST` JSON to a URL and receive JSON back, instead of running a shell command. Useful for CI/CD integrations and stateless backend endpoints (v2.1.63+)
- **New**: Project configs & auto-memory now shared across all git worktrees of the same repository
- **New**: `/simplify` and `/batch` bundled slash commands
- **New**: `ENABLE_CLAUDEAI_MCP_SERVERS=false` env var to opt out of claude.ai MCP server exposure
- **Improved**: `/model` command shows currently active model in picker
- **Fixed**: Major wave of memory leaks — WebSocket listeners, MCP caches, git root detection cache, JSON parsing cache, bash prefix cache, subagent AppState after compaction, MCP server fetch caches on reconnect
- **Fixed**: VSCode remote sessions not appearing in conversation history
- **Fixed**: `/clear` not resetting cached skills (stale skill content persisted to new conversation)
- **Fixed**: Local slash command output (e.g. `/cost`) appearing as user messages in UI

### v2.1.62 (2026-02-27)

- **Fixed**: Prompt suggestion cache regression that reduced cache hit rates

### v2.1.61 (2026-02-27)

- **Fixed**: Concurrent writes corrupting config file on Windows

### v2.1.59 (2026-02-26)

- **New**: Auto-memory — Claude automatically saves useful context to memory; manage with `/memory`
- **New**: `/copy` command — interactive picker when code blocks are present, select individual blocks or full response
- **Improved**: Smarter "always allow" prefix suggestions for compound bash commands (per-subcommand prefixes instead of treating whole command as one)
- **Improved**: Memory usage in multi-agent sessions (releases completed subagent task state)
- **Improved**: Ordering of short task lists
- **Fixed**: MCP OAuth token refresh race condition when running multiple Claude Code instances simultaneously
- **Fixed**: Shell commands not showing clear error message when working directory has been deleted
- **Fixed**: Config file corruption that could wipe authentication when multiple Claude Code instances ran simultaneously

### v2.1.58 (2026-02-26)

- **Expanded**: Remote Control available to more users

### v2.1.56 (2026-02-25)

- **Fixed**: VSCode: Another cause of "command 'claude-vscode.editor.openLast' not found" crashes

### v2.1.55 (2026-02-25)

- **Fixed**: BashTool failing on Windows with EINVAL error

### v2.1.53 (2026-02-25)

- **Fixed**: UI flicker where user input briefly disappeared after submission before rendering
- **Fixed**: Bulk agent kill (ctrl+f) now sends single aggregate notification instead of one per agent, and properly clears command queue
- **Fixed**: Graceful shutdown sometimes leaving stale sessions when using Remote Control (parallelized teardown)
- **Fixed**: `--worktree` flag sometimes being ignored on first launch
- **Fixed**: Panic ("switch on corrupted value") on Windows
- **Fixed**: Crash when spawning many processes on Windows
- **Fixed**: Crash in WebAssembly interpreter on Linux x64 & Windows x64
- **Fixed**: Crash that sometimes occurred after 2 minutes on Windows ARM64

### v2.1.52 (2026-02-24)

- **Fixed**: VSCode extension crash on Windows ("command 'claude-vscode.editor.openLast' not found")

### v2.1.51 (2026-02-24)

- **New**: `claude remote-control` subcommand for external builds — enables local environment serving for all users
- **New**: Custom npm registries and specific version pinning when installing plugins from npm sources
- **New**: SDK: `CLAUDE_CODE_ACCOUNT_UUID`, `CLAUDE_CODE_USER_EMAIL`, `CLAUDE_CODE_ORGANIZATION_UUID` env vars to provide account info synchronously (eliminates race conditions in early telemetry)
- **Changed**: BashTool now skips login shell (`-l` flag) by default when shell snapshot is available — performance improvement (previously required `CLAUDE_BASH_NO_LOGIN=true`)
- **Changed**: Tool results larger than 50K characters now persisted to disk (previously 100K threshold)
- **Improved**: `/model` picker now shows human-readable labels (e.g., "Sonnet 4.5") instead of raw model IDs for pinned versions, with upgrade hint when newer version available
- **Fixed**: Security issue where `statusLine` and `fileSuggestion` hook commands could execute without workspace trust acceptance in interactive mode
- **Fixed**: Duplicate `control_response` messages from WebSocket reconnects causing API 400 errors
- **Fixed**: Slash command autocomplete crashing when a plugin's SKILL.md description is a YAML array or other non-string type

### v2.1.50 (2026-02-21)

- **New**: `WorktreeCreate` and `WorktreeRemove` hook events — custom VCS setup/teardown when agent worktree isolation creates or removes worktrees
- **New**: `isolation: worktree` in agent definitions for declarative worktree isolation (no longer requires setting in each call)
- **New**: `claude agents` CLI command to list all configured agents
- **New**: `startupTimeout` configuration for LSP servers
- **New**: `CLAUDE_CODE_DISABLE_1M_CONTEXT` env var to disable 1M context window support
- **New**: Pre-configured OAuth client credentials for MCP servers that don't support Dynamic Client Registration (Slack); use `--client-id` and `--client-secret` with `claude mcp add`
- **New**: VSCode `/extra-usage` command support
- **Changed**: Opus 4.6 (fast mode) now includes full 1M context window
- **Changed**: `CLAUDE_CODE_SIMPLE` mode now also disables MCP tools, attachments, hooks, and CLAUDE.md loading for fully minimal experience
- **Fixed**: Bug where resumed sessions could be invisible when working directory involved symlinks
- **Fixed**: `disableAllHooks` setting to respect managed settings hierarchy (non-managed settings can no longer disable managed hooks)
- **Fixed**: Linux: native modules not loading on systems with glibc older than 2.30 (RHEL 8)
- **Fixed**: Memory leak in agent teams where completed teammate tasks were never garbage collected
- **Fixed**: Memory leak where completed task state objects were never removed from AppState
- **Fixed**: Memory leak where LSP diagnostic data was never cleaned up after delivery
- **Fixed**: Unbounded memory growth in long sessions (file history snapshots capped; circular buffer fix; stream buffers released after use)
- **Fixed**: MCP tools not discovered when tool search is enabled and prompt passed as launch argument
- **Fixed**: Prompt suggestion cache regression that reduced cache hit rates
- **Improved**: Startup performance for headless mode (`-p`) by deferring Yoga WASM and UI component imports
- **Improved**: Memory usage during long sessions by clearing internal caches after compaction and clearing large tool results after processing

### v2.1.49 (2026-02-20)

- **New**: `--worktree` / `-w` CLI flag to start Claude in an isolated git worktree
- **New**: Subagents support `isolation: "worktree"` for working in a temporary git worktree
- **New**: `background: true` field in agent definitions to always run as a background task
- **New**: `ConfigChange` hook event — fires when configuration files change during a session (enterprise security auditing + blocking)
- **New**: Plugins can ship `settings.json` for default configuration
- **New**: `--from-pr` flag to resume sessions linked to a specific GitHub PR (+ sessions auto-linked when created via `gh pr create`)
- **New**: `PreToolUse` hooks can return `additionalContext` to the model
- **New**: `plansDirectory` setting to customize where plan files are stored
- **New**: `auto:N` syntax for configuring MCP tool search auto-enable threshold
- **New**: `Setup` hook event triggered via `--init`, `--init-only`, or `--maintenance` CLI flags
- **Changed**: Sonnet 4.5 1M context removed from Max plan — Sonnet 4.6 now has 1M context (switch in `/model`)
- **Changed**: Simple mode now includes file edit tool (not just Bash)
- **Fixed**: File-not-found errors now suggest corrected paths when model drops repo folder
- **Fixed**: Ctrl+C and ESC silently ignored when background agents running + main thread idle (double-press within 3s now kills all agents)
- **Fixed**: Plugin `enable`/`disable` auto-detects correct scope (no longer defaults to user scope)
- **Fixed**: Context window blocking limit calculated too aggressively (~65% instead of ~98%)
- **Fixed**: Memory issues causing crashes with parallel subagents
- **Fixed**: Memory leak in long sessions where stream resources not cleaned up
- **Fixed**: `@` symbol incorrectly triggering file autocomplete in bash mode
- **Fixed**: Background agent results returning raw transcript data instead of final answer
- **Fixed**: Slash command autocomplete selecting wrong command (e.g. `/context` vs `/compact`)
- **Improved**: `@` mention file suggestion speed (~3× faster in git repos)
- **Improved**: MCP connection: `list_changed` notification support for dynamic tool updates without reconnection
- **Improved**: Skills invoke progress display; skill suggestions prioritize recently/frequently used
- **Improved**: Incremental output for async agents; token count includes background agent tokens

### v2.1.47 (2026-02-19)

- **Improved**: VS Code plan preview auto-updates as Claude iterates; commenting enabled only when plan is ready for review; preview stays open when rejected for revision
- **New**: `ctrl+f` kills all background agents simultaneously (replaces double-ESC); ESC now cancels main thread only, background agents keep running
- **New**: `last_assistant_message` field added to Stop and SubagentStop hook inputs (access final response without parsing transcript files)
- **New**: `chat:newline` keybinding action; `added_dirs` in statusline JSON workspace section
- **Fixed**: Compaction failing when conversation contains many PDF documents (strips document blocks alongside images)
- **Fixed**: Edit tool corrupting Unicode curly quotes (`"` `"` `'` `'`) by replacing with straight quotes
- **Fixed**: Parallel file write/edit — single file failure no longer aborts sibling operations
- **Fixed**: OSC 8 hyperlinks only clickable on first line when link text wraps across multiple terminal lines
- **Fixed**: Bash permission classifier now validates match descriptions against actual input rules (prevents hallucinated permissions)
- **Fixed**: Config backups timestamped and rotated (5 most recent kept) instead of overwriting
- **Fixed**: Session name lost after context compaction; plan mode lost after compaction
- **Fixed**: Hooks (PreToolUse, PostToolUse) silently failing on Windows (now uses Git Bash)
- **Fixed**: Custom agents/skills not discovered in git worktrees (main repo `.claude/` now included)
- **Fixed**: 70+ additional rendering, session, permission, and platform fixes

### v2.1.46 (2026-02-19)

- **Fixed**: Orphaned Claude Code processes after terminal disconnect on macOS
- **New**: Support for using claude.ai MCP connectors in Claude Code

### v2.1.45 (2026-02-17)

- **New**: Claude Sonnet 4.6 model support
- **New**: `spinnerTipsOverride` setting — customize spinner tips via `tips` array, opt out of built-in tips with `excludeDefault: true`
- **New**: SDK `SDKRateLimitInfo` and `SDKRateLimitEvent` types for rate limit status tracking (utilization, reset times, overage)
- **Fixed**: Agent Teams teammates failing on Bedrock, Vertex, and Foundry (env vars now propagated to tmux-spawned processes)
- **Fixed**: Sandbox "operation not permitted" errors on macOS temp file writes
- **Fixed**: Task tool (backgrounded agents) crashing with `ReferenceError` on completion
- **Improved**: Memory usage for large shell command outputs (RSS no longer grows unboundedly)
- **Improved**: Startup performance (removed eager session history loading)
- **Improved**: Plugin-provided commands, agents, and hooks available immediately after install (no restart needed)

### v2.1.44 (2026-02-17)

- Fixed: Auth refresh errors

### v2.1.43 (2026-02-17)

- Fixed: AWS auth refresh hanging indefinitely (added 3-minute timeout)
- Fixed: Structured-outputs beta header being sent unconditionally on Vertex/Bedrock
- Fixed: Spurious warnings for non-agent markdown files in `.claude/agents/` directory

### v2.1.42 (2026-02-14)

- **Improved**: Startup performance via deferred Zod schema construction (faster on large projects)
- **Improved**: Prompt cache hit rate by moving date outside the system prompt (avoids daily cache invalidation)
- **New**: Opus 4.6 effort callout for eligible users (one-time onboarding)
- Fixed: `/resume` showing interrupt messages as session titles
- Fixed: Image dimension limit errors now suggest using `/compact` instead of opaque failure

### v2.1.41 (2026-02-13)

- **New**: Guard against launching Claude Code inside another Claude Code session
- **New**: `claude auth login`, `claude auth status`, `claude auth logout` CLI subcommands
- **New**: Windows ARM64 (win32-arm64) native binary support
- Added `speed` attribute to OTel events and trace spans for fast mode visibility
- **Improved**: `/rename` auto-generates session name from conversation context when called without arguments
- Improved narrow terminal layout for prompt footer
- Fixed: Agent Teams using wrong model identifier for Bedrock, Vertex, and Foundry customers
- Fixed: Crash when MCP tools return image content during streaming
- Fixed: `/resume` session previews showing raw XML tags instead of readable command names
- Fixed: Opus 4.6 launch announcement showing for Bedrock/Vertex/Foundry users
- Fixed: Hook blocking errors (exit code 2) not showing stderr to the user
- Fixed: Structured-outputs beta header sent unconditionally on Vertex/Bedrock
- Fixed: File resolution for @-mentions with anchor fragments (e.g., `@README.md#installation`)
- Fixed: FileReadTool blocking on FIFOs, `/dev/stdin`, and large files
- Fixed: Background task notifications not delivered in streaming Agent SDK mode
- Fixed: Auto-compact failure error notifications shown to users
- Fixed: Stale permission rules not clearing when settings change on disk
- Fixed: Permission wait time included in subagent elapsed time display
- Fixed: Proactive ticks firing while in plan mode
- Improved: Model error messages for Bedrock/Vertex/Foundry with fallback suggestions

### v2.1.39 (2026-02-10)

- Improved: Terminal rendering performance
- Fixed: Fatal errors being swallowed instead of displayed
- Fixed: Process hanging after session close
- Fixed: Character loss at terminal screen boundary
- Fixed: Blank lines in verbose transcript view

### v2.1.38 (2026-02-10)

- Fixed: VS Code terminal scroll-to-top regression introduced in 2.1.37
- Fixed: Tab key queueing slash commands instead of autocompleting
- Fixed: Bash permission matching for commands using environment variable wrappers
- Fixed: Text between tool uses disappearing when not using streaming
- **Security**: Improved heredoc delimiter parsing to prevent command smuggling
- **Security**: Blocked writes to `.claude/skills` directory in sandbox mode

### v2.1.37 (2026-02-08)

- Fixed `/fast` not immediately available after enabling `/extra-usage`

### v2.1.36 (2026-02-08) ⭐

- ⭐ **Fast mode now available for Opus 4.6** — Same model, faster output. Toggle with `/fast`. [Learn more](https://code.claude.com/docs/en/fast-mode)

### v2.1.34 (2026-02-07)

- Fixed a crash when agent teams setting changed between renders
- **Security fix**: Commands excluded from sandboxing (via `sandbox.excludedCommands` or `dangerouslyDisableSandbox`) could bypass the Bash ask permission rule when `autoAllowBashIfSandboxed` was enabled

### v2.1.33 (2026-02-06)

**Highlights**:
- **Agent teams fixes** — Improved tmux session handling and availability warnings
- **New hook events** — `TeammateIdle` and `TaskCompleted` for multi-agent workflows
- **Agent frontmatter enhancements**:
  - `memory` field for user/project/local scope memory selection
  - `Task(agent_type)` syntax to restrict sub-agent spawning in agent definitions
- **Plugin identification** — Plugin name now shown in skill descriptions and `/skills` menu
- **VSCode improvements** — Remote sessions support, branch/message count in session picker
- Fixed: Thinking interruption, streaming abort, proxy settings, `/resume` XML markup
- Improved: API connection errors show specific cause instead of generic message
- Improved: Invalid managed settings errors now surfaced properly
- Multiple stability fixes across agent workflows and tool interactions

### v2.1.32 (2026-02-05) ⭐ MAJOR

**Highlights**:
- ⭐ **Claude Opus 4.6 is now available!**
- ⭐ **Agent teams research preview** — Multi-agent collaboration for complex tasks (token-intensive, requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)
- ⭐ **Automatic memory recording and recall** — Claude now automatically records and recalls memories as it works
- **"Summarize from here"** — Message selector now allows partial conversation summarization
- Skills from `.claude/skills/` in `--add-dir` directories auto-load
- Fixed: `@` file completion showing incorrect relative paths from subdirectories
- Fixed: Bash tool no longer throws "Bad substitution" errors with JavaScript template literals (e.g., `${index + 1}`)
- Improved: Skill character budget now scales with context window (2% of context)
- Improved: `--resume` re-uses `--agent` value from previous conversation by default
- Fixed: Thai/Lao spacing vowels rendering issues
- [VSCode] Fixed slash commands incorrectly executing when pressing Enter with preceding text
- [VSCode] Added spinner when loading past conversations list

### v2.1.31 (2026-02-03)

- **Session resume hint** — Exit message now shows how to continue your conversation later
- **Full-width (zenkaku) space support** — Added Japanese IME checkbox selection support
- Fixed: PDF too large errors permanently locking sessions (now recoverable without starting new conversation)
- Fixed: Bash commands incorrectly reporting "Read-only file system" when sandbox enabled
- Fixed: Plan mode crash when project config missing default fields
- Fixed: `temperatureOverride` being silently ignored in streaming API path
- Fixed: LSP shutdown/exit compatibility with strict language servers
- Improved: System prompts now guide model toward Read/Edit/Glob/Grep tools instead of bash equivalents
- Improved: PDF and request size error messages show actual limits (100 pages, 20MB)
- Reduced: Layout jitter when spinner appears/disappears during streaming

### v2.1.30 (2026-02-02)

- **⭐ PDF page range support** — `pages` parameter in Read tool for PDFs (e.g., `pages: "1-5"`) with lightweight references for large PDFs (>10 pages)
- **⭐ Pre-configured OAuth for MCP servers** — Built-in client credentials for servers without Dynamic Client Registration (Slack support via `--client-id` and `--client-secret`)
- **⭐ New `/debug` command** — Claude can help troubleshoot current session issues
- **Additional git flags** — Support for `git log` and `git show` read-only flags (`--topo-order`, `--cherry-pick`, `--format`, `--raw`)
- **Task tool metrics** — Results now include token count, tool uses, and duration
- **Reduced motion mode** — New config option for accessibility
- Fixed: Phantom "(no content)" text blocks in API history (reduces token waste)
- Fixed: Prompt cache not invalidating when tool schemas changed
- Fixed: 400 errors after `/login` with thinking blocks
- Fixed: Session resume hang with corrupted `parentUuid` cycles
- Fixed: Rate limit showing wrong "/upgrade" for Max 20x users
- Fixed: Permission dialogs stealing focus while typing
- Fixed: Subagents unable to access SDK MCP tools
- Fixed: Windows users with `.bashrc` unable to run bash
- Improved: Memory usage for `--resume` (68% reduction for many sessions)
- Improved: TaskStop displays stopped command description instead of generic message
- Changed: `/model` executes immediately instead of queuing
- [VSCode] Added multiline input in "Other" text fields (Shift+Enter for new lines)
- [VSCode] Fixed duplicate sessions in session list

### v2.1.29 (2026-01-31)

- **Performance**: Fixed startup performance issues when resuming sessions with saved hook context
- Significantly improved session recovery speed for long-duration sessions

### v2.1.27 (2026-01-29)

- **New**: `--from-pr` flag to resume sessions linked to a specific GitHub PR number or URL
- **New**: Sessions automatically linked to PRs when created via `gh pr create`
- Added tool call failures and denials to debug logs
- Fixed context management validation error for Bedrock/Vertex gateway users
- Fixed `/context` command not displaying colored output
- Fixed status bar duplicating background task indicator when PR status was shown
- [Windows] Fixed bash command execution failing for users with `.bashrc` files
- [Windows] Fixed console windows flashing when spawning child processes
- [VSCode] Fixed OAuth token expiration causing 401 errors after extended sessions

### v2.1.25 (2026-01-30)

- Fixed beta header validation for Bedrock and Vertex gateway users — Ensures `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` environment variable works correctly

### v2.1.23 (2026-01-29)

- **Customizable spinner verbs** — New `spinnerVerbs` setting allows personalization of spinner action words
- mTLS and corporate proxy connectivity fixes — Improved support for users behind corporate proxies with client certificates
- Per-user temp directory isolation — Prevents permission conflicts on shared systems
- Improved terminal rendering performance — Optimized screen data layout for faster updates
- Fixed: Prompt caching race condition causing 400 errors
- Fixed: Async hooks not canceling when headless streaming ends
- Fixed: Tab completion not updating input field
- Fixed: Ripgrep search timeouts returning empty results instead of errors
- Changed: Bash commands show timeout duration alongside elapsed time
- Changed: Merged PRs show purple status indicator in prompt footer
- [IDE] Fixed: Model options displaying incorrect region strings for Bedrock users in headless mode

### v2.1.22 (2026-01-28)

- Improved task UI performance with virtualization — Task list now uses virtual scrolling for better responsiveness with many tasks
- Vim selection and deletion fixes — Fixed visual mode selections and `dw` command behavior
- LSP improvements: Kotlin support, UTF-16 range handling, better error recovery
- Tasks now consistently use `task-N` IDs instead of internal UUIDs
- Fixed: `#` keyboard shortcut not working in task creation fields
- Fixed: Compact tool use rendering in chat history
- Fixed: Session URL escaping in git commit messages
- Fixed: Command output handling improvements

### v2.1.21 (2026-01-28)

- **Skills/commands can specify required/recommended Claude Code version** — Use `minClaudeCodeVersion` and `recommendedClaudeCodeVersion` in frontmatter
- **New TaskCreate fields**: `category` (testing, implementation, documentation, etc.), `checklist` (subtasks as markdown list), `parentId` (task hierarchy)
- **Automatic Claude Code update checking** at session start (respects auto-update settings)
- Tasks appear in `/context` output with 'Disable tasks' shortcut for quick toggling
- Improved task UI: Delete button added, better empty state messaging
- Fixed: Task deletion now properly removes all related task data
- Fixed: Shell environment variables expanded correctly in hook commands
- Fixed: Pasted URLs with parentheses properly formatted in markdown
- Fixed: Bash output capture for commands with large output

### v2.1.20 (2026-01-27)

- **New**: TaskUpdate tool can delete tasks via `status="deleted"`
- **New**: PR review status indicator in prompt footer — Shows PR state (approved, changes requested, pending, draft) as colored dot with clickable link
- Arrow key history navigation in vim normal mode when cursor cannot move further
- External editor shortcut (Ctrl+G) added to help menu
- Support for loading CLAUDE.md from `--add-dir` directories (requires `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`)
- Fixed: Session compaction issues causing full history load instead of compact summary
- Fixed: Agents ignoring user messages while actively working
- Fixed: Wide character (emoji, CJK) rendering artifacts
- Improved: Task list dynamically adjusts to terminal height
- Changed: Background agents prompt for tool permissions before launching
- Changed: Config backups timestamped and rotated (keeps 5 most recent)

### v2.1.19 (2026-01-25)

- **New**: `CLAUDE_CODE_ENABLE_TASKS` environment variable — Set to `false` to temporarily revert to old task system
- **New**: Argument shorthand in custom commands — Use `$0`, `$1`, etc. instead of verbose syntax
- [VSCode] Session forking and rewind functionality enabled for all users
- Fixed: Crashes on processors without AVX instruction support
- Fixed: Dangling Claude Code processes when terminal closed (SIGKILL fallback)
- Fixed: `/rename` and `/tag` not updating correct session when resuming from different directory (git worktrees)
- Fixed: Resuming sessions by custom title from different directory
- Fixed: Pasted text lost when using prompt stash (Ctrl+S) and restore
- Fixed: Agent list displaying "Sonnet (default)" instead of "Inherit (default)" for agents without explicit model
- Fixed: Backgrounded hook commands blocking session instead of returning early
- Fixed: File write preview omitting empty lines
- Changed: Skills without additional permissions/hooks allowed without approval
- [SDK] Added replay of queued_command attachment messages when `replayUserMessages` enabled

**⚠️ Breaking**:
- Indexed argument syntax changed: `$ARGUMENTS.0` → `$ARGUMENTS[0]` (bracket syntax)

### v2.1.18 (2026-01-24) ⭐

- ⭐ **Customizable keyboard shortcuts** — Configure keybindings per context, create chord sequences, personalize workflow
- Run `/keybindings` to get started
- Learn more: [code.claude.com/docs/en/keybindings](https://code.claude.com/docs/en/keybindings)

### v2.1.17 (2026-01-23)

- Fix: Crashes on processors without AVX instruction support

### v2.1.16 (2026-01-22) ⭐

- ⭐ **New task management system** with dependency tracking
- [VSCode] Native plugin management support
- [VSCode] OAuth users can browse and resume remote sessions from Sessions dialog
- Fixed: Out-of-memory crashes when resuming sessions with heavy subagent usage
- Fixed: "Context remaining" warning not hidden after `/compact`
- [IDE] Fixed race condition on Windows where sidebar view container wouldn't appear

### v2.1.15 (2026-01-22)

- **⚠️ Deprecation notice for npm installations** — Run `claude install` or see [docs](https://docs.anthropic.com/en/docs/claude-code/getting-started)
- Improved UI rendering performance with React Compiler
- Fixed: MCP stdio server timeout not killing child process, which could cause UI freezes

### v2.1.14 (2026-01-21)

- **History-based autocomplete in bash mode** — Type `!` followed by a partial command and press Tab to complete from bash history
- Search functionality in installed plugins list
- Support for pinning plugins to specific git commit SHAs for exact version control
- Fixed: Context window blocking limit calculated too aggressively (~65% instead of ~98%)
- Fixed: Memory issues and leaks in long-running sessions with parallel subagents
- Fixed: `@` symbol incorrectly triggering file autocomplete in bash mode
- Fixed: Slash command autocomplete selecting wrong command for similar names
- Improved: Backspace deletes pasted text as single token

### v2.1.12 (2026-01-18)

- Bug fix: Message rendering

### v2.1.11 (2026-01-17)

- Fix: Excessive MCP connection requests for HTTP/SSE transports

### v2.1.10 (2026-01-17)

- New `Setup` hook event (--init, --init-only, --maintenance flags)
- Keyboard shortcut 'c' to copy OAuth URL
- File suggestions show as removable attachments
- [VSCode] Plugin install count + trust warnings

### v2.1.9 (2026-01-16)

- **`auto:N` syntax for MCP tool search threshold** — Configure when Tool Search activates: `ENABLE_TOOL_SEARCH=auto:5` (5% context), `auto:10` (default), `auto:20` (conservative). See [architecture.md](./architecture.md#mcp-tool-search-lazy-loading) for details.
- `plansDirectory` setting for custom plan file locations
- Session URL attribution to commits/PRs from web sessions
- PreToolUse hooks can return `additionalContext`
- `${CLAUDE_SESSION_ID}` string substitution for skills

### v2.1.7 (2026-01-15)

- `showTurnDuration` setting to hide turn duration messages
- **MCP Tool Search auto mode enabled by default** — Lazy loading for MCP tools when definitions exceed 10% of context. Based on Anthropic's [Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use) API feature. Result: **85% token reduction** on tool definitions, improved tool selection accuracy (Opus 4: 49%→74%, Opus 4.5: 79.5%→88.1%)
- Inline display of agent final response in task notifications

**⚠️ Breaking**:
- OAuth/API Console URLs changed: `console.anthropic.com` → `platform.claude.com`
- Security fix: Wildcard permission rules could match compound commands

### v2.1.6 (2026-01-14)

- Search functionality in `/config` command
- Date range filtering in `/stats` (press `r` to cycle)
- Auto-discovery of skills from nested `.claude/skills` directories
- Updates section in `/doctor` showing auto-update channel

**⚠️ Security Fix**: Permission bypass via shell line continuation

### v2.1.5 (2026-01-13)

- `CLAUDE_CODE_TMPDIR` environment variable for custom temp directory

### v2.1.4 (2026-01-12)

- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable

### v2.1.3 (2026-01-11)

- Merged slash commands and skills (simplified mental model)
- Release channel toggle (stable/latest) in `/config`
- `/doctor` warnings for unreachable permission rules

### v2.1.2 (2026-01-10)

- Windows Package Manager (winget) support
- Clickable hyperlinks for file paths (OSC 8 terminals)
- Shift+Tab shortcut in plan mode for auto-accept edits
- Large bash outputs saved to disk instead of truncated

**⚠️ Breaking**:
- Security fix: Command injection in bash command processing
- Deprecated: `C:\ProgramData\ClaudeCode` managed settings path

### v2.1.0 (2026-01-08) ⭐ MAJOR

**Highlights**:
- ⭐ **Automatic skill hot-reload** — Skills modified in `~/.claude/skills` or `.claude/skills` immediately available
- ⭐ **Shift+Enter works OOTB** in iTerm2, WezTerm, Ghostty, Kitty
- ⭐ **New Vim motions**: `;` `,` `y` `yy` `Y` `p` `P` text objects (`iw` `aw` `i"` etc.) `>>` `<<` `J`
- **Unified Ctrl+B** for backgrounding all running tasks
- `/plan` command shortcut to enable plan mode
- Slash command autocomplete anywhere in input
- `language` setting for response language (e.g., `language: "japanese"`)
- Skills `context: fork` support for forked sub-agent context
- Hooks support in agent/skill/command frontmatter
- MCP `list_changed` notifications support
- `/teleport` and `/remote-env` commands for web sessions
- Disable specific agents with `Task(AgentName)` syntax
- `--tools` flag in interactive mode
- YAML-style lists in frontmatter `allowed-tools`

**⚠️ Breaking**:
- OAuth URLs: `console.anthropic.com` → `platform.claude.com`
- Removed permission prompt for entering plan mode
- [SDK] Minimum zod peer dependency: `^4.0.0`

---

## 2.0.x Series (November 2025 - January 2026)

### v2.0.76 (2026-01-05)

- Fix: macOS code-sign warning with Claude in Chrome

### v2.0.74 (2026-01-04) ⭐

- ⭐ **LSP (Language Server Protocol) tool** for code intelligence (go-to-definition, find references, hover)
- `/terminal-setup` for Kitty, Alacritty, Zed, Warp
- Ctrl+T in `/theme` to toggle syntax highlighting
- Grouped skills/agents by source in `/context`

### v2.0.72 (2026-01-02) ⭐

- ⭐ **Claude in Chrome (Beta)** — Control browser directly from Claude Code
- Reduced terminal flickering
- QR code for mobile app download
- Thinking toggle changed: Tab → Alt+T

### v2.0.70 (2025-12-30)

- Enter key accepts/submits prompt suggestions immediately
- Wildcard syntax `mcp__server__*` for MCP tool permissions
- Auto-update toggle for plugin marketplaces
- 3x memory usage improvement for large conversations

**⚠️ Breaking**: Removed `#` shortcut for quick memory entry

### v2.0.67 (2025-12-26) ⭐

- ⭐ **Thinking mode enabled by default for Opus 4.5**
- Thinking config moved to `/config`
- Search in `/permissions` with `/` shortcut

### v2.0.64 (2025-12-22) ⭐

- ⭐ **Instant auto-compacting**
- ⭐ **Async agents and bash commands** with wake-up messages
- `/stats` with usage graphs, streaks, favorite model
- Named sessions: `/rename`, `/resume <name>`
- Support for `.claude/rules/` directory
- Image dimension metadata for coordinate mappings

### v2.0.60 (2025-12-18) ⭐

- ⭐ **Background agents** — Agents run while you work
- `--disable-slash-commands` CLI flag
- Model name in Co-Authored-By commits
- `/mcp enable|disable [server-name]`

### v2.0.51 (2025-12-10) ⭐ MAJOR

- ⭐ **Opus 4.5 released**
- ⭐ **Claude Code for Desktop**
- Updated usage limits for Opus 4.5
- Plan Mode builds more precise plans

### v2.0.45 (2025-12-05) ⭐

- ⭐ **Microsoft Foundry support**
- `PermissionRequest` hook for auto-approve/deny
- `&` prefix for background tasks to web

### v2.0.28 (2025-11-18) ⭐

- ⭐ **Plan mode: introduced Plan subagent**
- Subagents: resume capability
- Subagents: dynamic model selection
- `--max-budget-usd` flag (SDK)
- Git-based plugins branch/tag support (`#branch`)

### v2.0.24 (2025-11-10)

- Claude Code Web: Web → CLI teleport
- Sandbox mode for BashTool (Linux & Mac)
- Bedrock: `awsAuthRefresh` output display

---

## Breaking Changes Summary

### URLs

| Version | Change |
|---------|--------|
| v2.1.0, v2.1.7 | OAuth/API Console: `console.anthropic.com` → `platform.claude.com` |

### Windows

| Version | Change |
|---------|--------|
| v2.0.58 | Managed settings prefer `C:\Program Files\ClaudeCode` |
| v2.1.2 | Deprecated `C:\ProgramData\ClaudeCode` path |

### SDK / Agent Tool

| Version | Change |
|---------|--------|
| v2.0.25 | Removed legacy SDK entrypoint → `@anthropic-ai/claude-agent-sdk` |
| v2.1.0 | Minimum zod peer dependency: `^4.0.0` |
| v2.1.77 | `Agent` tool no longer accepts `resume` parameter (use `SendMessage({to: agentId})` instead) |
| v2.1.212 | Task tool's `mode` parameter deprecated (now ignored); subagents inherit the parent session's permission mode |
| v2.1.217 | Subagent nesting disabled by default, and concurrent subagents capped at 20 (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) |
| v2.1.219 | Subagent nesting restored to depth 3 by default; set `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` to disable |

### Models and Behavior

| Version | Change |
|---------|--------|
| v2.1.68 | Opus 4 and Opus 4.1 removed from the Claude Code first-party API, auto-migrated to Opus 4.6 |
| v2.1.218 | Skills with `context: fork` run in the background by default; opt out with `background: false` |
| v2.1.218 | Agent markdown files reject agent names containing `:`, reserved for plugin namespacing |
| v2.1.218 | `/deep-research` starts only when invoked manually; Claude no longer launches it on its own |
| v2.1.219 | Opus 4.7 removed from fast mode; `/fast` applies to Opus 5 and Opus 4.8 only |
| v2.1.219 | Dynamic workflows default to a medium size guideline (fewer than 15 agents); change with Dynamic workflow size in `/config` |

### API Ecosystem

| Date | Feature |
|------|---------|
| 2026-01-29 | **Structured Outputs GA**: `output_config.format` remplace `output_format`. [Docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) |
| 2026-04-30 | **1M context beta retired**: `context-1m-2025-08-07` header no longer accepted for Sonnet 4.5/4 — requests >200k tokens error. Migrate to Sonnet 4.6 or Opus 4.6. |

### Shortcuts

| Version | Change |
|---------|--------|
| v2.0.70 | Removed `#` shortcut for quick memory entry |
| v2.1.153 | `modelPicker:setAsDefault` keybinding renamed to `modelPicker:thisSessionOnly` in `keybindings.json` |

### Security Fixes

| Version | Issue |
|---------|-------|
| v2.1.2 | Command injection in bash command processing |
| v2.1.6 | Shell line continuation permission bypass |
| v2.1.7 | Wildcard permission rules compound commands |
| v2.1.38 | Heredoc delimiter command smuggling prevention |

### Syntax

| Version | Change |
|---------|--------|
| v2.1.19 | Indexed argument syntax changed: `$ARGUMENTS.0` → `$ARGUMENTS[0]` (bracket syntax) |
| v2.1.210 | `Write(path)`, `NotebookEdit(path)`, and `Glob(path)` permission rules now warn at startup. Use `Edit(path)` or `Read(path)` instead |
| v2.1.214 | Single-segment `dir/**` hook `if:` conditions match only `<cwd>/dir`. Write `**/dir/**` for any-depth matching (`deny`/`ask` permission rules keep any-depth) |
| v2.1.214 | `file -m`/`--magic-file`/`-f`/`--files-from` and `docker` daemon-redirect flags (`--url`, `--connection`, `--identity`) now require permission |

---

## Milestone Features

| Version | Key Features |
|---------|--------------|
| **v2.1.219** | Claude Opus 5 becomes the default Opus model (1M context, fast mode $10/$50 per Mtok), `DirectoryAdded` hook, `sandbox.network.strictAllowlist`, subagent nesting restored to depth 3 |
| **v2.1.218** | `/code-review` runs as a background subagent, agent frontmatter hooks require workspace trust, `context: fork` skills background by default |
| **v2.1.217** | Concurrent subagent cap (default 20), `--max-budget-usd` halts background subagents, MCP truncated-output memory leak fixed |
| **v2.1.214** | Eight Bash permission-check security fixes, EndConversation tool, heartbeat for long-running tool calls, OTel message-level correlation attributes |
| **v2.1.212** | `/fork` copies the conversation into a new background session (in-session subagent renamed `/subtask`), WebSearch + subagent-spawn session caps, MCP calls auto-background after 2 min |
| **v2.1.208** | Screen reader mode (opt-in plain-text rendering), `vimInsertModeRemaps`, `CLAUDE_CODE_PROCESS_WRAPPER` corporate launcher support |
| **v2.1.198** | Subagents run in the background by default, Claude in Chrome generally available |
| **v2.1.197** | Claude Sonnet 5 becomes the default model, native 1M-token context, promotional pricing $2/$10 per Mtok through August 31 |
| **v2.1.69** | InstructionsLoaded hook, 4 security fixes, 15+ memory fixes, Voice STT 20 languages |
| **v2.1.68** | ultrathink re-introduced, Opus 4.6 medium effort default, Opus 4/4.1 removed |
| **v2.1.63** | HTTP hooks, worktree config sharing, /simplify + /batch bundled commands |
| **v2.1.32** | Opus 4.6, Agent teams preview, Automatic memory |
| **v2.1.18** | Customizable keyboard shortcuts with /keybindings |
| **v2.1.16** | New task management system with dependency tracking |
| **v2.1.0** | Skill hot-reload, Shift+Enter OOTB, Vim motions, /plan command |
| **v2.0.74** | LSP tool for code intelligence |
| **v2.0.72** | Claude in Chrome (browser control) |
| **v2.0.67** | Thinking mode default for Opus 4.5 |
| **v2.0.64** | Instant auto-compact, async agents, named sessions |
| **v2.0.60** | Background agents |
| **v2.0.51** | Opus 4.5, Claude Code for Desktop |
| **v2.0.45** | Microsoft Foundry, PermissionRequest hook |
| **v2.0.28** | Plan subagent, subagent resume/model selection |
| **v2.0.24** | Web teleport, Sandbox mode |

---

## Updating This Document

1. **Watch**: [github.com/anthropics/claude-code/releases](https://github.com/anthropics/claude-code/releases)
2. **Update**: `machine-readable/claude-code-releases.yaml` (source of truth)
3. **Regenerate**: Update this markdown accordingly
4. **Sync landing**: Run `./scripts/check-landing-sync.sh`

---

*Last updated: 2026-03-05 | [Back to main guide](../ultimate-guide.md)*
