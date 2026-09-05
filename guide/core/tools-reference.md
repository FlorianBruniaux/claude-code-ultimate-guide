# Built-in Tools Reference

Claude Code ships with a set of built-in tools it uses to read, modify, and execute things in your environment. You do not install or configure them; they are always present.

Tool names are the exact strings you use in permission rules (`allow`/`deny`), subagent `tools` and `disallowedTools` frontmatter, hook `matcher` fields, and the CLI flags `--allowedTools`/`--disallowedTools`. To add custom tools, connect an [MCP server](../ecosystem/mcp-servers-ecosystem.md). To build reusable prompt-driven workflows, write a [skill](../../examples/skills/); they run through the existing `Skill` tool rather than adding a new tool entry. [Computer Use](./computer-use.md) is a separate built-in MCP server with a macOS desktop permission boundary.

---

## All built-in tools

The table below covers every built-in tool Claude Code ships with. "Permission Required" means a first-time prompt appears before the tool runs (in default and `acceptEdits` modes). Tools marked No run without prompting.

### File operations

| Tool | Description | Permission Required |
|------|-------------|:-------------------:|
| `Read` | Read file contents (text, images, PDFs, Jupyter notebooks) | No |
| `Write` | Create or overwrite a file (requires prior read if the file already exists) | Yes |
| `Edit` | Make targeted string replacements in an existing file | Yes |
| `NotebookEdit` | Modify Jupyter notebook cells by `cell_id` | Yes |
| `Glob` | Find files by name pattern (`**/*.ts`, `src/**`) | No |
| `Grep` | Search file contents with ripgrep regex | No |
| `LSP` | Code intelligence via language servers: jump to definition, find references, type errors | No |

### Execution

| Tool | Description | Permission Required |
|------|-------------|:-------------------:|
| `Bash` | Run shell commands in your environment | Yes |
| `PowerShell` | Run PowerShell commands natively (Windows first-class, opt-in elsewhere) | Yes |
| `Monitor` | Run a command in the background and feed each output line back to Claude (v2.1.98+) | Yes |

### Web

| Tool | Description | Permission Required |
|------|-------------|:-------------------:|
| `WebSearch` | Search the web and return result titles and URLs | Yes |
| `WebFetch` | Fetch a URL, convert HTML to Markdown, run an extraction prompt against it | Yes |

### Agents and orchestration

| Tool | Description | Permission Required |
|------|-------------|:-------------------:|
| `Agent` | Spawn a subagent with its own context window to handle a task | No |
| `Workflow` | Run a dynamic workflow: a script that orchestrates many subagents and returns one result | Yes |
| `TeamCreate` | Create an agent team with multiple teammates (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) | No |
| `TeamDelete` | Disband an agent team and clean up teammate processes | No |
| `ListAgents` | List every session this one can reach: subagents, agent-team teammates, other local Claude Code sessions on this machine, cloud sessions, Remote Control sessions on other machines (v2.1.224+) | No |
| `SendMessage` | Send a message to an agent-team teammate, resume a stopped subagent by ID, or message an independent session found via `ListAgents` (cross-session messaging, v2.1.224+) | No |

### Task management

| Tool | Description | Permission Required |
|------|-------------|:-------------------:|
| `TaskCreate` | Create a task in the session task list (v2.1.16+) | No |
| `TaskGet` | Retrieve full details for a specific task | No |
| `TaskList` | List all tasks with their current status | No |
| `TaskUpdate` | Update task status, dependencies, or details; can also delete tasks | No |
| `TaskStop` | Kill a running background task by ID | No |
| `TaskOutput` | Retrieve output from a background task (deprecated; prefer `Read` on the task output path) | No |
| `TodoWrite` | Manage the session checklist (disabled by default since v2.1.142; set `CLAUDE_CODE_ENABLE_TASKS=0` to re-enable) | No |

### Scheduling

| Tool | Description | Permission Required |
|------|-------------|:-------------------:|
| `CronCreate` | Schedule a recurring or one-shot prompt within the session | No |
| `CronDelete` | Cancel a scheduled task by ID | No |
| `CronList` | List all scheduled tasks in the session | No |
| `ScheduleWakeup` | Reschedule the next iteration of a self-paced `/loop` (called by Claude, not by you) | No |
| `RemoteTrigger` | Create, update, run, and list Routines on claude.ai (Pro/Max/Team/Enterprise) | No |
| `PushNotification` | Send a desktop notification and a phone push when Remote Control is connected | No |

### MCP integration

| Tool | Description | Permission Required |
|------|-------------|:-------------------:|
| `ToolSearch` | Load schemas for deferred MCP tools when tool search is enabled | No |
| `WaitForMcpServers` | Wait for MCP servers still connecting before using their tools (appears when tool search is disabled) | No |
| `ListMcpResourcesTool` | List resources exposed by connected MCP servers | No |
| `ReadMcpResourceTool` | Read a specific MCP resource by URI | No |

### Worktrees and control flow

| Tool | Description | Permission Required |
|------|-------------|:-------------------:|
| `EnterWorktree` | Create an isolated git worktree and switch into it (or switch into an existing one with `path`) | No |
| `ExitWorktree` | Exit a worktree session and return to the original directory | No |
| `EnterPlanMode` | Switch to plan mode to design an approach before coding | No |
| `ExitPlanMode` | Present a plan for approval and exit plan mode | Yes |
| `AskUserQuestion` | Ask multiple-choice questions to gather requirements or clarify ambiguity | No |
| `Skill` | Execute a skill within the main conversation | Yes |
| `ShareOnboardingGuide` | Upload `ONBOARDING.md` and return a share link (Pro/Max/Team/Enterprise) | Yes |

---

## Permission rule formats

Tool names appear in permission rules with an optional specifier:

| Rule format | Applies to | What it matches |
|-------------|------------|-----------------|
| `Bash(npm run *)` | `Bash`, `Monitor` | Shell commands by prefix/glob |
| `PowerShell(Get-ChildItem *)` | `PowerShell` | PowerShell commands |
| `Read(~/secrets/**)` | `Read`, `Grep`, `Glob`, `LSP` | File paths |
| `Edit(/src/**)` | `Edit`, `Write`, `NotebookEdit` | File paths |
| `Skill(deploy *)` | `Skill` | Skill name prefix |
| `Agent(Explore)` | `Agent` | Subagent type name |
| `WebFetch(domain:example.com)` | `WebFetch` | Domain name |
| `WebSearch` | `WebSearch` | No specifier; allow or deny the whole tool |

An `Edit(...)` allow rule also grants read access to the same path, so you do not need a matching `Read(...)` rule alongside it.

For the full syntax including path prefix forms (`//`, `~/`, `/`, `./`) and Bash wildcard semantics, see [Permission Rule Syntax in settings-reference.md](./settings-reference.md#permission-rule-syntax).

---

## Per-tool behaviors

### Bash

Each command runs in a separate process. Working directory changes made with `cd` carry over to later Bash calls in the main session (but not in subagents), as long as the target stays inside the project directory or an `--add-dir` path. Environment variables set with `export` do not persist between commands. Use `CLAUDE_ENV_FILE` or a `SessionStart` hook to propagate env state.

Default timeout is 2 minutes; Claude can request up to 10 minutes per command. Output is capped at 30,000 characters by default (configurable via `BASH_MAX_OUTPUT_LENGTH`, ceiling 150,000). When a command exceeds the cap, the full output is saved to a file in the session directory and Claude gets the path plus a short preview.

For long-running processes, Claude sets `run_in_background: true` to start as a background task. List and stop background tasks with `/tasks`.

### Edit

Performs exact string replacement. The `old_string` must appear exactly as written (character-for-character, including whitespace) and must appear only once. If it appears more than once, supply a longer string with enough surrounding context to pin down one occurrence, or use `replace_all: true`. Claude must have read the file in the current conversation before editing, and the file must not have changed on disk since that read.

### Glob

Finds files by name pattern with support for `**` recursive matching. Results are sorted by modification time, capped at 100 files. Glob does not respect `.gitignore` by default (unlike Grep, which does).

### Grep

Searches file contents using ripgrep. Patterns follow ripgrep regex syntax, which is not the same as POSIX grep. Metacharacters like `{` and `}` need escaping (for example, `interface\{\}` to find Go's `interface{}`). Grep respects `.gitignore` and skips gitignored files; pass a path directly to search a gitignored file. Three output modes: `files_with_matches` (default, paths only), `content` (matching lines with line numbers), `count` (match count per file).

### LSP

Inactive until you install a code intelligence plugin for your language. After each file edit, it automatically reports type errors and warnings. Can also be called directly to jump to definitions, find references, list symbols, trace call hierarchies, and get type information at a position.

### Monitor (v2.1.98+)

Lets Claude watch something in the background and react when it changes. Claude writes a watch script, runs it in the background, and receives each output line as it arrives. Useful for tailing logs, polling CI status, watching a directory for file changes, or tracking long-running script output. Uses the same permission rules as Bash. Not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry, and not available when `DISABLE_TELEMETRY` or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is set.

The command source accepts `timeout_ms` and `persistent`; stop an active monitor with `TaskStop`. Since v2.1.195, a Monitor can instead use a native WebSocket source: `ws.url` plus optional `ws.protocols`. `command` and `ws` are mutually exclusive. Text frames become events; binary frames become a placeholder; a frame over 1 MiB or a closed socket stops the monitor. The URL must be ASCII `ws://` or `wss://`, with no credentials or whitespace. WebSocket monitors require their own approval and refuse private, link-local, and metadata-service destinations.

An event is not authorization. Treat text from either source as untrusted data, never as a shell command or a permission grant. See [Monitor, Channels and Safe Delegation to Codex](../workflows/monitor-event-delegation.md) for a GitHub-to-WebSocket boundary and a least-privilege Codex workflow.

```text
# Ask Claude to set up a monitor like this:
"Tail /var/log/app.log and alert me when you see any ERROR line."
"Watch CI on PR #42 and tell me when it passes or fails."
```

### NotebookEdit

Modifies a Jupyter notebook one cell at a time by `cell_id`. Three modes: `replace` (overwrite cell source, default), `insert` (add a new cell after the target), `delete` (remove the target cell). Does not perform string replacement across the notebook the way Edit does on plain files.

### PowerShell

Available natively on Windows; opt-in on Linux/macOS via `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` (requires `pwsh` on `PATH`). Claude Code spawns PowerShell with `-ExecutionPolicy Bypass` at process scope only, so enterprise `MachinePolicy` or `UserPolicy` lockdowns still apply. See [the PowerShell Native Tool section](../ultimate-guide.md#powershell-native-tool) for full setup details.

### Read

Returns file contents with line numbers. Handles images (PNG and JPG, returned as visual content), PDFs (short files whole; for PDFs over 10 pages, reads in ranges of up to 20 pages with the `pages` parameter), and Jupyter notebooks (all cells with outputs). When a whole-file read would exceed the token limit, Read returns the first page with a notice and the offset needed to read more.

### WebFetch

Takes a URL and an extraction prompt. Fetches the page, converts HTML to Markdown, and runs the extraction prompt against the content using a small fast model. Claude receives that model's answer, not the raw page. This makes WebFetch lossy by design. The extraction prompt determines what reaches Claude. HTTP URLs are upgraded to HTTPS automatically. Responses are cached for 15 minutes. When a URL redirects to a different host, WebFetch returns a text result naming both URLs rather than following the redirect; Claude issues a second call for the new URL. For the raw unprocessed page, use `curl` via Bash.

### WebSearch

Runs a query and returns result titles and URLs. It does not fetch the result pages; Claude follows up with WebFetch to read a page it finds. May issue up to 8 backend searches per call to refine results internally.

### Write

Creates a new file or overwrites an existing one. If the target path already exists, Claude must have read it at least once in the current conversation before overwriting. For partial changes, Claude uses Edit rather than Write.

### Workflow (dynamic workflows, v2.1.154+)

Runs a JavaScript script that orchestrates many subagents in the background and returns one consolidated result. Claude uses the `ultracode` keyword (renamed from `workflow` in v2.1.160, a breaking change) to trigger multi-agent fan-out. Monitor running workflows with `/workflows`. Requires explicit user opt-in: Claude does not start a workflow unless asked.

The orchestrator script itself consumes zero tokens. All token cost comes from `agent()` calls. Workflow scripts use four primitives: `agent()` spawns individual subagents; `parallel()` runs a batch concurrently and waits for all (barrier); `pipeline()` fans items through stages without a global barrier between stages; `phase()` updates the UI progress label. The `meta` export at the top of the file declares the workflow name and phase headings.

Workflow scripts store progress as they run: an interrupted job resumes from the last completed unit rather than starting over. For this to work, the orchestrator must be deterministic: `Date.now()`, `Math.random()`, and Node.js APIs are unavailable inside the orchestrator. Pass timestamps and seeds via the `args` global.

For the full primitive reference, behavioral guarantees, and common patterns (adversarial verification, loop-until-dry, judge panels), see [Dynamic Workflows](../workflows/dynamic-workflows.md).

---

## Advanced tools: how to trigger them

### `/loop` and ScheduleWakeup

The `/loop [interval] [prompt]` command runs a prompt on a recurring interval. Omit the interval to let Claude self-pace; after each iteration it calls `ScheduleWakeup` to decide when the next one fires (between 1 minute and 1 hour). The pending wakeup shows up in `session_crons` in Stop hook input. Cancel with Esc or Ctrl+C.

```text
/loop 5m /ci-status        # check CI every 5 minutes
/loop /monitor-deploys     # self-paced monitoring loop
```

### Scheduled tasks: CronCreate / CronList / CronDelete

These tools schedule prompts within the current session. Tasks are session-scoped and restored on `--resume` or `--continue` if unexpired. Use `CronList` to see active tasks, `CronDelete` to cancel one by ID. You interact with them by asking Claude to schedule something:

```text
"Remind me to run the test suite in 30 minutes."
"Schedule a deploy check every hour until I cancel it."
```

### Remote routines: RemoteTrigger and /schedule

`RemoteTrigger` backs the `/schedule` command and creates Routines on claude.ai. Routines run outside the current session on a schedule, via API, or on GitHub events. Requires a Pro, Max, Team, or Enterprise plan; not available on Bedrock, Vertex AI, or Foundry. See [Routines](../ultimate-guide.md#routines-cloud-automation) for the full feature guide.

### Push notifications: PushNotification

Claude calls `PushNotification` to send a desktop notification and, when Remote Control is connected with "Push when Claude decides" enabled, a phone push. Useful for long tasks where you step away. Delivery runs through Anthropic-hosted infrastructure, so it is not available on Bedrock, Vertex AI, or Foundry. See [Remote Control](../ultimate-guide.md#remote-control).

### Agent teams: TeamCreate / TeamDelete / SendMessage

Experimental feature behind `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. `TeamCreate` spawns a team of named teammates; `SendMessage` sends a message to a teammate or resumes a stopped subagent by its agent ID; `TeamDelete` disbands the team. See the dedicated [Agent Teams guide](../workflows/agent-teams.md) for setup, patterns, and examples.

### Cross-session messaging: ListAgents / SendMessage

Distinct from Agent Teams above: this is messaging between sessions that were never spawned by each other, each already running independently, on the same machine or reachable through your account. `ListAgents` (`/list-agents`, alias `/peers`) lists every reachable session with its name; two Claude Code sessions running locally at the same time see each other automatically, no setup required. `SendMessage({to: "session-name"})` delivers text into the target session's own conversation under the sender's name; the receiving session replies the same way, no ID tracking needed. A message from a peer never carries authority: it cannot approve a permission prompt or change configuration on the receiving session's behalf, and the receiving session's own permission rules still apply to anything it asks for. Requires v2.1.224+ (macOS/Linux/WSL2) or v2.1.234+ (native Windows). Since v2.1.248, same-machine messaging also works on Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, Foundry, and with feature-flag fetching disabled; sessions beyond this machine still require a claude.ai sign-in and Remote Control. See the dedicated [Cross-Session Messaging guide](../workflows/cross-session-messaging.md) for discovery mechanics, the `crossSessionInbound`/`isolatePeerMachines` security controls, correlated-drift defenses, and coordination patterns.

### Tasks API: TaskCreate through TaskStop

The modern task management system (v2.1.16+, default since v2.1.142). The full tool set:

- `TaskCreate`: add a task
- `TaskList`: list all tasks (status overview; does not include full details)
- `TaskGet`: retrieve full details for one task
- `TaskUpdate`: change status, dependencies, or details; also deletes
- `TaskStop`: kill a running background task by ID

`TodoWrite` is the legacy alternative; it was disabled by default at v2.1.142. Set `CLAUDE_CODE_ENABLE_TASKS=0` to re-enable it instead. For patterns and cross-session persistence, see [the Tasks API section](../ultimate-guide.md#tasks-api).

---

## Provider availability

Some tools are only available when Claude Code connects through Anthropic's own infrastructure:

| Tool | Not available on |
|------|-----------------|
| `Monitor` | Amazon Bedrock, Google Vertex AI, Microsoft Foundry |
| `PushNotification` | Amazon Bedrock, Google Vertex AI, Microsoft Foundry |
| `ScheduleWakeup` | Amazon Bedrock, Google Vertex AI, Microsoft Foundry |
| `RemoteTrigger` | Amazon Bedrock, Google Vertex AI, Microsoft Foundry |
| `WebSearch` | Amazon Bedrock (not exposed) |

`Workflow` (the `ultracode` keyword) has behavioral differences across providers; check release notes for the current state.

---

## See also

- [Architecture internals](./architecture.md): master loop, tool selection logic, context budget
- [Permission Rule Syntax](./settings-reference.md#permission-rule-syntax): full `allow`/`deny` rule format with all specifier forms
- [Sub-agents](../ultimate-guide.md#sub-agents): how `Agent` spawns work, tool inheritance, foreground vs background
- [Cross-Session Messaging](../workflows/cross-session-messaging.md): full `ListAgents`/`SendMessage` mechanics between independent sessions
- [Monitor, Channels and Safe Delegation to Codex](../workflows/monitor-event-delegation.md): WebSocket sources, plugin monitors, Channels, Routines, and event-driven least privilege
- [Skills](../ultimate-guide.md#skills): how to build reusable prompt workflows using the `Skill` tool
- [MCP servers](../ecosystem/mcp-servers-ecosystem.md): how to add custom tools via MCP
- [Hooks](../ultimate-guide.md#hooks): run commands before or after tool execution
