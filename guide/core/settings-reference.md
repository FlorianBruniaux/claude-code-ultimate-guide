# Claude Code Settings Reference

> Complete reference for `settings.json` configuration and environment variables. Covers all confirmed settings as of Claude Code v2.1.162.

**Sources:** [Official settings docs](https://code.claude.com/docs/en/settings) · [Official env-vars docs](https://code.claude.com/docs/en/env-vars) · [JSON Schema](https://json.schemastore.org/claude-code-settings.json)

**Legend:**
- No badge = confirmed in official documentation
- `📋 Schema only` = present in JSON schema but not on official settings page — still valid
- `⚠️ Unverified` = not confirmed in official sources

---

## Scope and Precedence

Claude Code uses four settings scopes, applied from highest to lowest priority:

| Priority | Scope | Location | Shared? | Purpose |
|----------|-------|----------|---------|---------|
| 1 | **Managed** | Server, MDM profile, registry, or system `managed-settings.json` | Yes (IT-deployed) | Org-wide policies, cannot be overridden |
| 2 | **Command line** | `--` flags at startup | No | Temporary session overrides |
| 3 | **Local** | `.claude/settings.local.json` | No (gitignored) | Personal project-specific |
| 4 | **Project** | `.claude/settings.json` | Yes (committed) | Team-shared settings |
| 5 | **User** | `~/.claude/settings.json` | No | Global personal defaults |

**Array merging:** Settings like `permissions.allow`, `sandbox.filesystem.allowWrite`, and `allowedHttpHookUrls` are concatenated and deduplicated across scopes — not replaced.

**Deny precedence:** `permissions.deny` rules always take effect regardless of allow/ask rules at any scope.

**Managed settings delivery methods:**
- Server-managed (Claude.ai admin console)
- macOS MDM: `com.anthropic.claudecode` plist
- Windows registry: `HKLM\SOFTWARE\Policies\ClaudeCode`
- File: `managed-settings.json` at `/Library/Application Support/ClaudeCode/` (macOS), `/etc/claude-code/` (Linux/WSL), `C:\Program Files\ClaudeCode\` (Windows)
- Drop-in directory: `managed-settings.d/*.json` alongside `managed-settings.json`, merged alphabetically

**Other config:** `~/.claude.json` stores OAuth session, MCP server configs, per-project trust state, and preferences like `editorMode`. Do not put `~/.claude.json` keys into `settings.json` — it will trigger schema validation errors.

---

## Settings Keys

### Core Configuration

#### `$schema`
**Type:** string
**Scope:** all
**Default:** none

JSON Schema URL for IDE validation and autocomplete. Add `"https://json.schemastore.org/claude-code-settings.json"` to enable inline validation in VS Code, Cursor, and other editors.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json"
}
```

#### `model`
**Type:** string
**Scope:** all
**Default:** `"default"`

Override the default model for all sessions. Accepts aliases (`"sonnet"`, `"opus"`, `"haiku"`, `"opusplan"`) or full model IDs like `"claude-sonnet-4-6"`. The `ANTHROPIC_MODEL` environment variable takes precedence.

```json
{ "model": "opus" }
```

#### `agent`
**Type:** string
**Scope:** all
**Default:** none

Run the main thread as a named subagent. Applies that agent's system prompt, tool restrictions, and model. Value must match an agent defined in `.claude/agents/`. Also available via `--agent` CLI flag.

```json
{ "agent": "code-reviewer" }
```

#### `language`
**Type:** string
**Scope:** all
**Default:** `"english"`

Claude's preferred response language. Also sets the voice dictation language. Examples: `"japanese"`, `"spanish"`, `"french"`.

#### `cleanupPeriodDays`
**Type:** number
**Scope:** all
**Default:** `30`

Sessions inactive longer than this number of days are deleted at startup. Setting to `0` deletes all existing transcripts at startup and disables session persistence entirely — no `.jsonl` files are written, `/resume` shows no conversations, and hooks receive an empty `transcript_path`.

#### `autoUpdatesChannel`
**Type:** string
**Scope:** all
**Default:** `"latest"`
**Values:** `"latest"` | `"stable"`

Release channel to follow. `"stable"` is typically about one week behind `"latest"` and skips versions with major regressions.

#### `alwaysThinkingEnabled`
**Type:** boolean
**Scope:** all
**Default:** `false`

Enable extended thinking by default for all sessions. Usually configured via `/config` rather than editing directly.

#### `includeGitInstructions`
**Type:** boolean
**Scope:** all
**Default:** `true`

Include built-in commit and PR workflow instructions and a git status snapshot in the system prompt. Set to `false` when using a custom git workflow skill. The `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` env var takes precedence.

#### `voiceEnabled`
**Type:** boolean
**Scope:** user
**Default:** none

Enable push-to-talk voice dictation. Written automatically when you run `/voice`. Requires a Claude.ai account.

#### `companyAnnouncements`
**Type:** array of strings
**Scope:** all
**Default:** none

Announcements displayed to users at startup. Multiple announcements are cycled through at random.

```json
{
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review code guidelines at docs.acme.com",
    "All PRs require code review before merge"
  ]
}
```

#### `availableModels`
**Type:** array of strings
**Scope:** all
**Default:** none

Restrict which models users can select via `/model`, `--model`, Config tool, or `ANTHROPIC_MODEL`. Does not affect the Default option.

```json
{ "availableModels": ["sonnet", "haiku"] }
```

#### `fastModePerSessionOptIn`
**Type:** boolean
**Scope:** all
**Default:** `false`

When `true`, fast mode does not persist across sessions. Each session starts with fast mode off, requiring users to enable it with `/fast`. The user's preference is still saved.

#### `teammateMode`
**Type:** string
**Scope:** all
**Default:** `"auto"`
**Values:** `"auto"` | `"in-process"` | `"tmux"`

How agent team teammates display. `"auto"` uses split panes in tmux or iTerm2, in-process otherwise.

#### `showClearContextOnPlanAccept`
**Type:** boolean
**Scope:** all
**Default:** `false`

Show the "clear context" option on the plan accept screen. Set to `true` to restore the option, which was hidden by default starting in v2.1.81.

#### `feedbackSurveyRate`
**Type:** number
**Scope:** all
**Default:** none

Probability (0–1) that the session quality survey appears when eligible. Set to `0` to suppress entirely. Useful when using Bedrock, Vertex, or Foundry.

#### `disableAutoMode`
**Type:** string
**Scope:** all
**Default:** none
**Values:** `"disable"`

Set to `"disable"` to prevent auto mode from being activated. Removes `auto` from the `Shift+Tab` cycle and rejects `--permission-mode auto` at startup.

#### `useAutoModeDuringPlan`
**Type:** boolean
**Scope:** user / local
**Default:** `true`

Whether plan mode uses auto mode semantics when auto mode is available. Not read from shared project settings.

#### `autoMode`
**Type:** object
**Scope:** user / local
**Default:** none

Customize the auto mode classifier. Contains `environment`, `allow`, and `soft_deny` arrays of prose rules. Not read from shared project settings.

#### `defaultShell`
**Type:** string
**Scope:** all
**Default:** `"bash"`
**Values:** `"bash"` | `"powershell"`

Default shell for input-box `!` commands. `"powershell"` requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`.

#### `skipWebFetchPreflight` `📋 Schema only`
**Type:** boolean
**Scope:** all
**Default:** `false`

Skip the WebFetch blocklist check before fetching URLs.

#### `env`
**Type:** object
**Scope:** all
**Default:** none

Environment variables applied to every session. Use this instead of wrapper scripts to set variables. See the [Environment Variables](#environment-variables) section for all supported keys.

```json
{
  "env": {
    "NODE_ENV": "development",
    "CLAUDE_CODE_EFFORT_LEVEL": "medium"
  }
}
```

---

### Plans and Memory

#### `plansDirectory`
**Type:** string
**Scope:** all
**Default:** `"~/.claude/plans"`

Directory where `/plan` outputs are stored. Path is relative to the project root.

#### `autoMemoryEnabled`
**Type:** boolean
**Scope:** all
**Default:** `true`

Enable or disable the auto-memory feature that automatically saves context across sessions.

#### `autoMemoryDirectory`
**Type:** string
**Scope:** user / local / managed
**Default:** none

Custom directory for auto-memory storage. Accepts `~/`-expanded paths. Not accepted in project settings (`.claude/settings.json`) to prevent shared repos from redirecting memory writes to sensitive locations.

---

### Permissions

Control what tools and operations Claude can perform.

#### `permissions.allow`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Permission rules that allow tool use without prompting. Arrays are concatenated across scopes. See [Permission Rule Syntax](#permission-rule-syntax) below.

#### `permissions.ask`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Permission rules requiring user confirmation before tool use.

#### `permissions.deny`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Permission rules blocking tool use. Highest safety precedence — cannot be overridden by allow/ask rules at any scope.

#### `permissions.additionalDirectories`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Additional working directories that Claude has access to, beyond the current project root.

```json
{ "permissions": { "additionalDirectories": ["../shared-libs/"] } }
```

#### `permissions.defaultMode`
**Type:** string
**Scope:** all
**Default:** `"default"`
**Values:** `"default"` | `"acceptEdits"` | `"plan"` | `"bypassPermissions"`

Default permission mode when opening Claude Code. In Remote environments, only `"acceptEdits"` and `"plan"` are honored.

#### `permissions.disableBypassPermissionsMode`
**Type:** string
**Scope:** all
**Default:** none
**Values:** `"disable"`

Set to `"disable"` to prevent `bypassPermissions` mode from being activated. Disables the `--dangerously-skip-permissions` flag. Most useful in managed settings.

#### `allowManagedPermissionRulesOnly`
**Type:** boolean
**Scope:** managed only
**Default:** `false`

When `true`, user and project `allow`, `ask`, and `deny` rules are ignored. Only managed permission rules apply.

### Permission Rule Syntax

Rules follow the format `Tool` or `Tool(specifier)`. Evaluation order: deny first, then ask, then allow. The first matching rule wins.

| Tool | Pattern | Example |
|------|---------|---------|
| `Bash` | Command pattern with wildcards | `Bash(npm run *)`, `Bash(git *)` |
| `Read` | File path pattern | `Read(.env)`, `Read(./secrets/**)` |
| `Edit` | File path pattern | `Edit(src/**)`, `Edit(*.ts)` |
| `Write` | File path pattern | `Write(*.md)` |
| `WebFetch` | `domain:hostname` | `WebFetch(domain:example.com)` |
| `WebSearch` | No specifier | `WebSearch` |
| `Task` | Agent name | `Task(Explore)` |
| `Agent` | Agent name | `Agent(researcher)` |
| `MCP` | `mcp__server__tool` or `MCP(server:tool)` | `mcp__memory__*` |

**Path prefixes for Read/Edit rules:**

| Prefix | Meaning |
|--------|---------|
| `//` | Absolute path from filesystem root |
| `~/` | Relative to home directory |
| `/` | Relative to project root |
| `./` or none | Relative path (current directory) |

**Bash wildcard notes:** `*` matches at any position. `Bash(ls *)` (space before `*`) matches `ls -la` but NOT `lsof`. `Bash(*)` is equivalent to `Bash` (matches all commands). The legacy `:*` suffix (e.g., `Bash(npm:*)`) is deprecated.

```json
{
  "permissions": {
    "allow": ["Edit(*)", "Bash(npm run *)", "Bash(git *)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Read(.env)", "Read(./secrets/**)"],
    "defaultMode": "acceptEdits"
  }
}
```

---

### Hooks

#### `hooks`
**Type:** object
**Scope:** all
**Default:** none

Configure custom commands to run at lifecycle events. See the [hooks documentation](https://code.claude.com/docs/en/hooks) and [§7.1 of the guide](../ultimate-guide.md#71-the-event-system) for the full set of 30 hook events, exit codes, and environment variables.

#### `disableAllHooks`
**Type:** boolean
**Scope:** all
**Default:** `false`

Disable all hooks and any custom status line.

#### `allowManagedHooksOnly`
**Type:** boolean
**Scope:** managed only
**Default:** `false`

When `true`, only managed hooks and SDK hooks are loaded. User, project, and plugin hooks are blocked.

#### `allowedHttpHookUrls`
**Type:** array of strings
**Scope:** all
**Default:** none (no restriction)

Allowlist of URL patterns that HTTP hooks may target. Supports `*` as a wildcard. When defined, hooks with non-matching URLs are silently blocked. Empty array blocks all HTTP hooks. Arrays merge across settings sources.

```json
{ "allowedHttpHookUrls": ["https://hooks.example.com/*"] }
```

#### `httpHookAllowedEnvVars`
**Type:** array of strings
**Scope:** all
**Default:** none (no restriction)

Allowlist of environment variable names that HTTP hooks can interpolate into header values. Each hook's effective `allowedEnvVars` is the intersection with this list. Arrays merge across settings sources.

---

### MCP Servers

#### `enableAllProjectMcpServers`
**Type:** boolean
**Scope:** all
**Default:** `false`

Automatically approve all MCP servers defined in project `.mcp.json` files. Avoids per-server confirmation prompts.

#### `enabledMcpjsonServers`
**Type:** array of strings
**Scope:** all
**Default:** none

Allowlist of specific server names from `.mcp.json` files to approve.

#### `disabledMcpjsonServers`
**Type:** array of strings
**Scope:** all
**Default:** none

Blocklist of specific server names from `.mcp.json` files to reject.

#### `allowedMcpServers`
**Type:** array
**Scope:** managed only
**Default:** none (no restrictions)

Allowlist of MCP servers users can configure. Each entry matches by `serverName`, `serverCommand`, or `serverUrl`. Undefined = no restrictions, empty array = lockdown.

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverCommand": "npx @modelcontextprotocol/*" },
    { "serverUrl": "https://mcp.company.com/*" }
  ]
}
```

#### `deniedMcpServers`
**Type:** array
**Scope:** managed only
**Default:** none

Blocklist of MCP servers that are explicitly blocked. Applies to all scopes including managed servers. Takes precedence over `allowedMcpServers`.

#### `allowManagedMcpServersOnly`
**Type:** boolean
**Scope:** managed only
**Default:** `false`

When `true`, only `allowedMcpServers` from managed settings are respected. Users can still add MCP servers, but only admin-defined servers are usable. `deniedMcpServers` still merges from all sources.

#### `channelsEnabled`
**Type:** boolean
**Scope:** managed only
**Default:** `false`

Allow channels for Team and Enterprise users. When unset or `false`, channel message delivery is blocked regardless of what users pass to `--channels`.

#### `allowedChannelPlugins`
**Type:** array
**Scope:** managed only
**Default:** none (uses default Anthropic allowlist)

Allowlist of channel plugins that may push messages. Replaces the default Anthropic allowlist when set. Requires `channelsEnabled: true`. Empty array blocks all channel plugins.

---

### Sandbox

Configure bash command sandboxing for security. Available on macOS, Linux, and WSL2.

#### `sandbox.enabled`
**Type:** boolean
**Scope:** all
**Default:** `false`

Enable bash sandboxing. Isolates bash commands from your filesystem and network.

#### `sandbox.failIfUnavailable`
**Type:** boolean
**Scope:** all
**Default:** `false`

Exit with an error at startup if `sandbox.enabled` is `true` but the sandbox cannot start (missing dependencies, unsupported platform). When `false`, a warning is shown and commands run unsandboxed. Useful in managed deployments that require sandboxing as a hard gate.

#### `sandbox.autoAllowBashIfSandboxed`
**Type:** boolean
**Scope:** all
**Default:** `true`

Auto-approve bash commands when sandboxed. When the sandbox is active, bash commands that would normally require confirmation are automatically approved.

#### `sandbox.excludedCommands`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Commands that bypass the sandbox and run directly in your environment.

> **Use the glob form, not the bare name.** A bare entry such as `"git"` matches only the zero-argument string `git`, so it never fires on a real invocation and the command stays sandboxed. Write `"git *"` instead. The bare form is what the published JSON schema suggests, which is why this is easy to get wrong: you configure something that does nothing, notice the command is still sandboxed, and only then find the glob form ([anthropics/claude-code#10524](https://github.com/anthropics/claude-code/issues/10524)). Verified on 2.1.220: `"git"` had no effect, `"git *"` worked immediately.

> **A match unsandboxes the entire Bash invocation.** When an entry matches anywhere in a compound command, every other command in that same call runs unsandboxed too, including commands that execute *before* the excluded one. With `"git *"` present, `git status && cat ~/.ssh/id_ed25519` reads the key, because `filesystem.denyRead`, `credentials`, and the network allowlist are all suspended for that call ([anthropics/claude-code#81157](https://github.com/anthropics/claude-code/issues/81157), open as of 2026-07-25 on 2.1.220).
>
> Scope entries to the subcommands that genuinely need to leave the sandbox rather than the whole binary. Git over SSH is the common case: only the network operations need an exception, so list those and leave local git confined.
>
> ```json
> "excludedCommands": [
>   "git push *", "git pull *", "git fetch *",
>   "git clone *", "git ls-remote *", "git remote *", "git submodule *"
> ]
> ```
>
> This keeps `git status`, `git diff`, `git log`, `git add`, and `git commit` inside the sandbox, so the bypass window only opens on the calls that actually talk to a remote.

#### `sandbox.allowUnsandboxedCommands`
**Type:** boolean
**Scope:** all
**Default:** `true`

Allow commands to opt out of the sandbox via the `dangerouslyDisableSandbox` parameter. Set to `false` for strict sandboxing where all commands must run inside the sandbox or be in `excludedCommands`.

#### `sandbox.enableWeakerNestedSandbox`
**Type:** boolean
**Scope:** all
**Default:** `false`

Enable a weaker sandbox for unprivileged Docker environments (Linux and WSL2 only). Reduces security.

#### `sandbox.enableWeakerNetworkIsolation`
**Type:** boolean
**Scope:** all
**Default:** `false`

(macOS only) Allow access to the system TLS trust service (`com.apple.trustd.agent`). Required for Go-based tools like `gh`, `gcloud`, and `terraform` when using `httpProxyPort` with a MITM proxy and custom CA. Reduces security.

#### `sandbox.network.allowUnixSockets`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Specific Unix socket paths accessible in the sandbox (for SSH agents, Docker, etc.).

#### `sandbox.network.allowAllUnixSockets`
**Type:** boolean
**Scope:** all
**Default:** `false`

Allow all Unix socket connections in the sandbox. Overrides `allowUnixSockets`.

#### `sandbox.network.allowLocalBinding`
**Type:** boolean
**Scope:** all
**Default:** `false`

Allow binding to localhost ports (macOS only).

#### `sandbox.network.allowedDomains`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Domains allowed for outbound network traffic. Supports wildcards like `*.example.com`.

#### `sandbox.network.allowManagedDomainsOnly`
**Type:** boolean
**Scope:** managed only
**Default:** `false`

When `true`, only `allowedDomains` and `WebFetch(domain:...)` allow rules from managed settings are respected. Non-allowed domains are blocked without prompting. Denied domains are still respected from all sources.

#### `sandbox.network.httpProxyPort`
**Type:** number
**Scope:** all
**Default:** none

HTTP proxy port for a custom proxy (1–65535). If not specified, Claude runs its own proxy.

#### `sandbox.network.socksProxyPort`
**Type:** number
**Scope:** all
**Default:** none

SOCKS5 proxy port for a custom proxy (1–65535).

#### `sandbox.network.deniedDomains` `⚠️ Unverified`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Network domain denylist for the sandbox. Not confirmed in official documentation.

#### `sandbox.filesystem.allowWrite`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Additional paths where sandboxed commands can write. Merged across all settings scopes. Also merged with paths from `Edit(...)` allow permission rules.

**Path prefix conventions:** `/` = absolute, `~/` = home-relative, `./` or no prefix = project-relative in project settings / `~/.claude`-relative in user settings.

#### `sandbox.filesystem.denyWrite`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Paths where sandboxed commands cannot write. Merged with `Edit(...)` deny rules.

#### `sandbox.filesystem.denyRead`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Paths where sandboxed commands cannot read. Merged with `Read(...)` deny rules.

#### `sandbox.filesystem.allowRead`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Paths to re-allow read access within `denyRead` regions. Takes precedence over `denyRead`. Arrays merge across all settings scopes.

When read rules overlap, the more specific path wins in both directions: `denyRead: ["~/"]` with `allowRead: ["~/projects"]` opens only that subtree, and `allowRead: ["~/"]` with `denyRead: ["~/.env"]` keeps that one file blocked. A broad allow cannot silently re-expose a secret an exact deny covers.

#### `sandbox.filesystem.disabled`
**Type:** boolean
**Scope:** user, managed, `--settings` (project settings ignored)
**Default:** `false`
**Since:** v2.1.216

Skip filesystem isolation while keeping network isolation. Sandboxed commands get unrestricted read and write access to the host, and their egress stays confined to `allowedDomains`. Use when the point of sandboxing is controlling where commands connect rather than what they write.

Turning the layer off also disables `filesystem.denyRead`, `credentials.files`, and the protection on Claude Code's own settings files, and stops the `$TMPDIR` override. `credentials.envVars` still applies, since environment scrubbing is independent of the filesystem layer.

Project settings cannot set it, so a checked-out repository cannot switch filesystem isolation off. When managed settings configure `sandbox.filesystem` at all, or list any `credentials.files` entry, only managed settings can set it. `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` makes Claude Code ignore it from every source.

> With the filesystem layer off and commands auto-allowed, a sandboxed command can write shell startup files, executables on `$PATH`, or `~/.claude/settings.json`, and use them to widen its own access on the next run. Set it only for workloads you trust not to escalate.

#### `sandbox.credentials.files`
**Type:** array of `{ path, mode }`
**Scope:** all (`deny` narrows only, so any scope may add one)
**Default:** `[]`
**Since:** v2.1.187

Credential files to hide from sandboxed commands. `mode` accepts only `"deny"`, which blocks reads the same way `filesystem.denyRead` does.

This matters more than its placement suggests. The sandbox's default read policy covers the **entire machine**, and there is no built-in credential denylist, so `~/.ssh` and `~/.aws/credentials` are readable by every sandboxed command until you list them. Paths follow the same prefix rules as `sandbox.filesystem.*`, and `deny` entries merge across every scope: any scope can add one, no scope can remove one another scope added.

```json
{
  "sandbox": {
    "credentials": {
      "files": [
        { "path": "~/.ssh", "mode": "deny" },
        { "path": "~/.aws", "mode": "deny" },
        { "path": "~/.gnupg", "mode": "deny" },
        { "path": "~/.config/gh", "mode": "deny" }
      ]
    }
  }
}
```

Verified on 2.1.220: with the entry in place, `ls ~/.ssh` from a sandboxed command returns `Operation not permitted` while the directory still appears in a listing of the home directory.

#### `sandbox.credentials.envVars`
**Type:** array of `{ name, mode, injectHosts? }`
**Scope:** `deny` from all scopes; `mask` from user, managed, `--settings` only
**Default:** `[]`
**Since:** v2.1.187 (`deny`), v2.1.199 (`mask`)

Environment variables to withhold from sandboxed commands. Sandboxed commands otherwise inherit the parent environment as-is, credentials included, which is the gap a `credentials.files` entry alone leaves open.

`deny` unsets the variable before each sandboxed command runs. It affects sandboxed Bash only, so MCP servers keep their credentials: they run as separate processes, not as sandboxed commands.

`mask` protects the credential while keeping the tool that authenticates with it working. The command sees a per-session sentinel; when a request leaves the sandbox for one of the credential's `injectHosts`, the proxy substitutes the real value. The command and anything it logs never hold the real credential. Each `injectHosts` entry must itself be covered by `allowedDomains`, and `network.tlsTerminate` is required because the proxy has to see request contents to substitute. Without it, masking fails closed: the sentinel reaches the server unchanged and authentication fails, and Claude Code reports the misconfiguration at startup.

```json
{
  "sandbox": {
    "network": { "tlsTerminate": {}, "allowedDomains": ["*.github.com"] },
    "credentials": {
      "envVars": [
        { "name": "ANTHROPIC_API_KEY", "mode": "deny" },
        { "name": "GH_TOKEN", "mode": "mask", "injectHosts": ["api.github.com"] }
      ]
    }
  }
}
```

`deny` wins when the same variable appears with both modes in any scope. Start with `deny` and move a variable to `mask` only when a CLI actually breaks without it, since `mask` requires TLS termination and authorizes the proxy to send the real credential to the listed hosts.

To strip Anthropic and cloud provider credentials from **all** subprocesses regardless of sandboxing, set `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` instead.

#### `sandbox.network.tlsTerminate` `⚠️ Experimental`
**Type:** object
**Scope:** user, managed, `--settings` (project settings ignored)
**Since:** v2.1.199

Make the built-in proxy terminate TLS itself. Required by `credentials.envVars` `mask` entries. It enables credential substitution; it does not add content filtering.

#### `sandbox.network.strictAllowlist`
**Type:** boolean
**Scope:** user, managed, `--settings` (project settings ignored)
**Default:** `false`
**Since:** v2.1.219

Deny sandboxed commands any host outside the allowlist instead of prompting. The allowlist is `allowedDomains` plus domains from `WebFetch(domain:...)` allow rules, or only the managed entries when `allowManagedDomainsOnly` is set. Applies to sandboxed commands only: in-process tools such as `WebFetch` still follow their permission rules.

Enable it last, once the domain list has survived a week of real work. Before that it converts every missing domain from a one-time prompt into a hard failure.

#### `sandbox.allowAppleEvents`
**Type:** boolean
**Scope:** user, managed, `--settings` (project settings ignored)
**Default:** `false`

Allow Apple Events on macOS, which the sandbox blocks by default. Fixes `open`, `osascript`, and browser-based auth flows failing with error `-600`.

> Enabling it removes code-execution isolation: sandboxed commands can launch other applications unsandboxed with no prompt, and send AppleScript to running applications, subject to the macOS automation-consent prompt. Prefer adding the specific command to `excludedCommands`.

#### `sandbox.filesystem.allowManagedReadPathsOnly`
**Type:** boolean
**Scope:** managed only
**Default:** `false`

When `true`, only `allowRead` paths from managed settings are respected. `allowRead` entries from user, project, and local settings are ignored.

**Sandbox example:**
```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["git push *", "git fetch *", "docker *"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true
    }
  }
}
```

---

### Plugins and Marketplaces

#### `enabledPlugins`
**Type:** object
**Scope:** all
**Default:** none

Enable or disable specific plugins by key (format: `plugin-name@marketplace-name`).

```json
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "experimental@acme-tools": false
  }
}
```

#### `extraKnownMarketplaces`
**Type:** object
**Scope:** project
**Default:** none

Add custom plugin marketplaces. Use `source: "settings"` to declare plugins inline without hosting a repository.

#### `strictKnownMarketplaces`
**Type:** array
**Scope:** managed only
**Default:** none (no restrictions)

Allowlist of permitted plugin marketplaces. When set, users can only add plugins from listed marketplaces. Empty array blocks all additions.

#### `blockedMarketplaces`
**Type:** array
**Scope:** managed only
**Default:** none

Block specific plugin marketplace sources. Blocked sources are checked before downloading, so they never touch the filesystem.

#### `pluginTrustMessage`
**Type:** string
**Scope:** managed only
**Default:** none

Custom message appended to the plugin trust warning shown before installation. Use for org-specific context like confirming plugins from an internal marketplace are vetted.

#### `skippedMarketplaces` `📋 Schema only`
**Type:** array
**Scope:** all
**Default:** none

Marketplaces the user declined to install (stored automatically).

#### `skippedPlugins` `📋 Schema only`
**Type:** array
**Scope:** all
**Default:** none

Plugins the user declined to install (stored automatically).

#### `pluginConfigs` `📋 Schema only`
**Type:** object
**Scope:** all
**Default:** none

Per-plugin MCP server configurations, keyed by `plugin@marketplace`.

---

### Model Configuration

#### `effortLevel`
**Type:** string
**Scope:** all
**Default:** `"medium"`
**Values:** `"low"` | `"medium"` | `"high"`

Persist the effort level across sessions. Controls reasoning depth. Written automatically when you run `/effort low|medium|high`. Supported on Opus 4.6+ and Sonnet 4.6+. The `CLAUDE_CODE_EFFORT_LEVEL` env var takes precedence.

#### `modelOverrides`
**Type:** object
**Scope:** all
**Default:** none

Map Anthropic model IDs to provider-specific model IDs (e.g., Bedrock inference profile ARNs). Each key is a model picker entry name; each value is the provider model ID.

```json
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-1:123456789:inference-profile/anthropic.claude-opus-4-6-v1:0"
  }
}
```

**Model aliases reference:**

| Alias | Description |
|-------|-------------|
| `"default"` | Recommended model for your account type |
| `"sonnet"` | Latest Sonnet (Claude Sonnet 5) |
| `"opus"` | Latest Opus (Claude Opus 5) |
| `"haiku"` | Fast Haiku model |
| `"sonnet[1m]"` | Sonnet with 1M token context |
| `"opusplan"` | Opus for planning, Sonnet for execution |

---

### Display and UX

#### `statusLine`
**Type:** object
**Scope:** all
**Default:** none

Configure a custom status line. The command receives a JSON object on stdin with fields like `context_window.used_percentage`, `rate_limits.five_hour.used_percentage`, etc.

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

#### `fileSuggestion`
**Type:** object
**Scope:** all
**Default:** none

Configure a custom script for `@` file path autocomplete. The command receives JSON on stdin with a `query` field and outputs newline-separated file paths (max 15).

```json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

#### `outputStyle`
**Type:** string
**Scope:** all
**Default:** `"Default"`

Controls how Claude communicates throughout the session. Equivalent to selecting a style via `/config` → "Preferred output style".

**Built-in values:**
- `"Default"` — concise, task-focused responses optimized for speed
- `"Explanatory"` — adds reasoning blocks explaining design choices, trade-offs, and codebase patterns
- `"Learning"` — pauses at key steps, inserts `TODO(human)` markers, asks you to write the meaningful pieces (pair-programming mode)

**Custom styles:** reference any filename (without `.md`) from `.claude/styles/`.

```json
{ "outputStyle": "Explanatory" }
```

```json
{ "outputStyle": "strict-reviewer" }
```

Setting persists across sessions. Explanatory and Learning increase output tokens; prompt caching offsets the cost after the first request. See [Section 9.7](../ultimate-guide.md#97-output-styles) for full documentation and custom style examples.

#### `spinnerTipsEnabled`
**Type:** boolean
**Scope:** all
**Default:** `true`

Show tips in the spinner while Claude is working.

#### `spinnerVerbs`
**Type:** object
**Scope:** all
**Default:** none

Customize the action verbs shown in the spinner and turn duration messages. Set `mode` to `"replace"` to use only your verbs, or `"append"` to add to defaults.

```json
{
  "spinnerVerbs": {
    "mode": "replace",
    "verbs": ["Cooking", "Brewing", "Crafting", "Conjuring"]
  }
}
```

#### `spinnerTipsOverride`
**Type:** object
**Scope:** all
**Default:** none

Override spinner tips with custom strings. `tips`: array of strings. `excludeDefault`: when `true`, only show custom tips.

```json
{
  "spinnerTipsOverride": {
    "tips": ["Use /compact at 50% context", "Plan mode helps for complex tasks"],
    "excludeDefault": true
  }
}
```

#### `respectGitignore`
**Type:** boolean
**Scope:** all
**Default:** `true`

Control whether the `@` file picker respects `.gitignore` patterns.

#### `prefersReducedMotion`
**Type:** boolean
**Scope:** all
**Default:** `false`

Reduce or disable UI animations (spinners, shimmer, flash effects) for accessibility.

---

### Authentication

#### `apiKeyHelper`
**Type:** string
**Scope:** all
**Default:** none

Shell script path (executed in `/bin/sh`) that outputs an auth token sent as `X-Api-Key` and `Authorization: Bearer` headers for model requests. Useful for short-lived credentials.

```json
{ "apiKeyHelper": "/bin/generate_temp_api_key.sh" }
```

#### `forceLoginMethod`
**Type:** string
**Scope:** all
**Default:** none
**Values:** `"claudeai"` | `"console"`

Restrict login to Claude.ai accounts (`"claudeai"`) or Claude Console API-billing accounts (`"console"`).

#### `forceLoginOrgUUID`
**Type:** string
**Scope:** all
**Default:** none

UUID of an organization to automatically select during login, bypassing the org selection step. Requires `forceLoginMethod` to be set.

---

### Attribution

#### `attribution.commit`
**Type:** string
**Scope:** all
**Default:** Git trailer with co-authored-by line

Attribution text added to git commits. Supports git trailers. Set to empty string to disable commit attribution entirely.

#### `attribution.pr`
**Type:** string
**Scope:** all
**Default:** Generated message with Claude Code link

Attribution text added to pull request descriptions. Set to empty string to disable.

#### `includeCoAuthoredBy`
**Type:** boolean
**Scope:** all
**Default:** `true`
**Status:** DEPRECATED — use `attribution` instead

Whether to include the `Co-Authored-By` byline. Superseded by the `attribution` object.

```json
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

---

### Worktrees

#### `worktree.symlinkDirectories`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Directories to symlink from the main repository into each worktree, avoiding large duplicated directories on disk (e.g., `node_modules`).

#### `worktree.sparsePaths`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

Directories to check out in each worktree via git sparse-checkout (cone mode). Only listed paths are written to disk — useful for large monorepos.

```json
{
  "worktree": {
    "symlinkDirectories": ["node_modules", ".cache"],
    "sparsePaths": ["packages/my-app", "shared/utils"]
  }
}
```

---

### AWS and Cloud

#### `awsAuthRefresh`
**Type:** string
**Scope:** all
**Default:** none

Custom script that modifies the `.aws` directory. Runs to refresh AWS credentials before API calls.

```json
{ "awsAuthRefresh": "aws sso login --profile myprofile" }
```

#### `awsCredentialExport`
**Type:** string
**Scope:** all
**Default:** none

Custom script that outputs JSON with AWS credentials. Used for non-standard credential sources.

#### `otelHeadersHelper`
**Type:** string
**Scope:** all
**Default:** none

Script to generate dynamic OpenTelemetry headers. Runs at startup and periodically. See the monitoring docs for the expected output format.

---

### Global Config (`~/.claude.json`)

These settings are stored in `~/.claude.json`, not `settings.json`. Adding them to `settings.json` triggers a schema validation error.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `autoConnectIde` | boolean | `false` | Auto-connect to a running IDE when Claude Code starts from an external terminal |
| `autoInstallIdeExtension` | boolean | `true` | Auto-install the Claude Code IDE extension when running from a VS Code terminal |
| `editorMode` | string | `"normal"` | Key binding mode: `"normal"` or `"vim"`. Written automatically by `/vim` |
| `showTurnDuration` | boolean | `true` | Show turn duration messages after responses (e.g., "Cooked for 1m 6s") |
| `terminalProgressBarEnabled` | boolean | `true` | Show terminal progress bar in ConEmu, Ghostty 1.2.0+, and iTerm2 3.6.6+ |

---

### Additional Schema-Only Keys

Keys confirmed in the JSON schema not covered in the sections above:

| Key | Type | Description |
|-----|------|-------------|
| `claudeMdExcludes` `📋 Schema only` | array | Glob patterns for CLAUDE.md files to exclude from loading |
| `allowManagedMcpServersOnly` | boolean | (Managed) Only managed MCP servers are usable |
| `allowManagedHooksOnly` | boolean | (Managed) Only managed and SDK hooks are loaded |
| `autoMemoryEnabled` | boolean | Enable/disable auto-memory feature |
| `feedbackSurveyRate` | number | Survey appearance probability (0–1) |

---

## Environment Variables

Set in your shell before launching `claude`, or configure under the `env` key in `settings.json` to apply to every session. When an env var and an equivalent settings field both apply, the env var takes precedence (e.g. `ANTHROPIC_MODEL` overrides the `model` setting). Changes take effect on the next `claude` launch.

### Authentication

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | API key for Anthropic API access. When set, used instead of your Claude subscription even if logged in |
| `ANTHROPIC_AUTH_TOKEN` | Custom `Authorization` header value (prefixed with `Bearer `) |
| `ANTHROPIC_BASE_URL` | Custom API endpoint for proxies or LLM gateways |
| `ANTHROPIC_CUSTOM_HEADERS` | Custom headers added to API requests. Format: `Name: Value`, newline-separated for multiple |
| `ANTHROPIC_BETAS` | Comma-separated extra `anthropic-beta` header values. Works with all auth methods including Claude.ai subscription |
| `ANTHROPIC_WORKSPACE_ID` | Workspace ID for workload identity federation when a federation rule covers more than one workspace |
| `CLAUDE_CODE_OAUTH_TOKEN` | OAuth access token for Claude.ai authentication. Alternative to `/login` for SDK and automated environments |
| `CLAUDE_CODE_OAUTH_REFRESH_TOKEN` | OAuth refresh token for headless auth. `claude auth login` exchanges this directly instead of opening a browser. Requires `CLAUDE_CODE_OAUTH_SCOPES` |
| `CLAUDE_CODE_OAUTH_SCOPES` | Space-separated OAuth scopes the refresh token was issued with. Required when `CLAUDE_CODE_OAUTH_REFRESH_TOKEN` is set |
| `CLAUDE_CONFIG_DIR` | Override the configuration directory (default: `~/.claude`) |

### Model Selection

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_MODEL` | Model to use. Accepts aliases (`sonnet`, `opus`, `haiku`) or full model IDs. Overrides the `model` setting |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Override the Haiku model alias with a custom model ID |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME` | Display name for the Haiku model override |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL_DESCRIPTION` | Description for the Haiku model override |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL_SUPPORTED_CAPABILITIES` | Capabilities for the Haiku model override |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Override the Sonnet model alias |
| `ANTHROPIC_DEFAULT_SONNET_MODEL_NAME` | Display name for the Sonnet model override |
| `ANTHROPIC_DEFAULT_SONNET_MODEL_DESCRIPTION` | Description for the Sonnet model override |
| `ANTHROPIC_DEFAULT_SONNET_MODEL_SUPPORTED_CAPABILITIES` | Capabilities for the Sonnet model override |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Override the Opus model alias (e.g. `claude-opus-4-6[1m]`) |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME` | Display name for the Opus model override |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION` | Description for the Opus model override |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | Capabilities for the Opus model override |
| `ANTHROPIC_CUSTOM_MODEL_OPTION` | Model ID to add as a custom entry in the `/model` picker |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` | Display name for the custom model entry |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` | Display description for the custom model entry |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_SUPPORTED_CAPABILITIES` | Capabilities for the custom model entry |
| `ANTHROPIC_SMALL_FAST_MODEL` | **DEPRECATED.** Use `ANTHROPIC_DEFAULT_HAIKU_MODEL` instead |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | AWS region for the Haiku-class model on Bedrock when `ANTHROPIC_DEFAULT_HAIKU_MODEL` is also set |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Override model for subagents (e.g. `haiku`) |
| `CLAUDE_CODE_EFFORT_LEVEL` | Effort level: `low`, `medium`, `high`, `xhigh`, `max`, or `auto`. Takes precedence over `/effort` and the `effortLevel` setting |
| `FALLBACK_FOR_ALL_PRIMARY_MODELS` | Any non-empty value triggers fallback to `--fallback-model` after repeated overload errors on any primary model, not just Opus |
| `CLAUDE_CODE_DISABLE_LEGACY_MODEL_REMAP` | Set to `1` to prevent automatic remapping of Opus 4.0 and 4.1 to the current Opus version on the Anthropic API |

### Cloud Providers

#### Amazon Bedrock

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_USE_BEDROCK` | Use Amazon Bedrock (`1` to enable) |
| `AWS_BEARER_TOKEN_BEDROCK` | Bedrock API key for authentication |
| `ANTHROPIC_BEDROCK_BASE_URL` | Override the Bedrock endpoint URL. Use for custom regions or when routing through an LLM gateway |
| `ANTHROPIC_BEDROCK_SERVICE_TIER` | Bedrock service tier: `default`, `flex`, or `priority`. Sent as `X-Amzn-Bedrock-Service-Tier` |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH` | Skip AWS auth for Bedrock (e.g. when using an LLM gateway) |
| `CLAUDE_ENABLE_BYTE_WATCHDOG_BEDROCK` | Set to `1` to enable byte-level streaming idle watchdog on Bedrock |

#### Bedrock Mantle

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_USE_MANTLE` | Use the Bedrock Mantle endpoint |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL` | Override the Bedrock Mantle endpoint URL |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH` | Skip AWS auth for Bedrock Mantle |

#### Google Vertex AI

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI (`1` to enable) |
| `ANTHROPIC_VERTEX_BASE_URL` | Override the Vertex AI endpoint URL |
| `ANTHROPIC_VERTEX_PROJECT_ID` | GCP project ID for Vertex AI requests (overridden by `GCLOUD_PROJECT` or `GOOGLE_CLOUD_PROJECT`) |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH` | Skip Google auth for Vertex |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU` | Region override for Claude 3.5 Haiku on Vertex AI |
| `VERTEX_REGION_CLAUDE_3_5_SONNET` | Region override for Claude 3.5 Sonnet on Vertex AI |
| `VERTEX_REGION_CLAUDE_3_7_SONNET` | Region override for Claude 3.7 Sonnet on Vertex AI |
| `VERTEX_REGION_CLAUDE_4_0_OPUS` | Region override for Claude 4.0 Opus on Vertex AI |
| `VERTEX_REGION_CLAUDE_4_0_SONNET` | Region override for Claude 4.0 Sonnet on Vertex AI |
| `VERTEX_REGION_CLAUDE_4_1_OPUS` | Region override for Claude 4.1 Opus on Vertex AI |
| `VERTEX_REGION_CLAUDE_4_5_OPUS` | Region override for Claude Opus 4.5 on Vertex AI |
| `VERTEX_REGION_CLAUDE_4_5_SONNET` | Region override for Claude Sonnet 4.5 on Vertex AI |
| `VERTEX_REGION_CLAUDE_4_6_OPUS` | Region override for Claude Opus 4.6 on Vertex AI |
| `VERTEX_REGION_CLAUDE_4_6_SONNET` | Region override for Claude Sonnet 4.6 on Vertex AI |
| `VERTEX_REGION_CLAUDE_4_7_OPUS` | Region override for Claude Opus 4.7 on Vertex AI. Added in v2.1.111 |
| `VERTEX_REGION_CLAUDE_4_8_OPUS` | Region override for Claude Opus 4.8 on Vertex AI |
| `VERTEX_REGION_CLAUDE_HAIKU_4_5` | Region override for Claude Haiku 4.5 on Vertex AI |

#### Microsoft Foundry

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_USE_FOUNDRY` | Use Microsoft Foundry (`1` to enable) |
| `ANTHROPIC_FOUNDRY_API_KEY` | API key for Microsoft Foundry authentication |
| `ANTHROPIC_FOUNDRY_BASE_URL` | Full base URL for the Foundry resource (alternative to `ANTHROPIC_FOUNDRY_RESOURCE`) |
| `ANTHROPIC_FOUNDRY_RESOURCE` | Foundry resource name. Required if `ANTHROPIC_FOUNDRY_BASE_URL` is not set |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH` | Skip Azure auth for Foundry |

#### Claude Platform on AWS

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_USE_ANTHROPIC_AWS` | Use Claude Platform on AWS |
| `ANTHROPIC_AWS_API_KEY` | Workspace API key for Claude Platform on AWS, generated in the AWS Console |
| `ANTHROPIC_AWS_BASE_URL` | Override the Claude Platform on AWS endpoint URL |
| `ANTHROPIC_AWS_WORKSPACE_ID` | Required workspace ID. Sent as the `anthropic-workspace-id` header on every request |
| `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH` | Skip client-side authentication for Claude Platform on AWS |

#### Multi-cloud

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_ENABLE_AUTO_MODE` | Set to `1` to make auto mode available on Bedrock, Vertex AI, and Foundry. Added in v2.1.158. No effect on Anthropic API |
| `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` | Set by host platforms managing model provider routing. When set, provider-selection and auth variables in settings files are ignored |

### Timeouts and Limits

| Variable | Description |
|----------|-------------|
| `API_TIMEOUT_MS` | API request timeout in milliseconds (default: 600000). Maximum: 2147483647 |
| `BASH_DEFAULT_TIMEOUT_MS` | Default bash command timeout in milliseconds (default: 120000) |
| `BASH_MAX_TIMEOUT_MS` | Maximum bash command timeout in milliseconds (default: 600000) |
| `BASH_MAX_OUTPUT_LENGTH` | Maximum characters in bash output before saving to a file and sending the path |
| `MAX_THINKING_TOKENS` | Extended thinking token budget. Set to `0` to disable. Ignored on models with adaptive reasoning unless `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` is set |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max output tokens per response (default: 32,000; up to 128,000 on Opus 5, Sonnet 5, Opus 4.8, and Sonnet 4.6) |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | Override default file read token limit |
| `CLAUDE_CODE_MAX_CONTEXT_TOKENS` | Override context window size Claude Code assumes for the active model. Only takes effect when `DISABLE_COMPACT` is also set |
| `CLAUDE_CODE_MAX_TURNS` | Cap the number of agentic turns per session. Equivalent to `--max-turns` (the flag takes precedence when both are set) |
| `CLAUDE_CODE_MAX_RETRIES` | Override the number of retries for failed API requests (default: 10) |
| `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY` | Maximum read-only tools and subagents executing in parallel (default: 10) |
| `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` | Stall timeout in milliseconds for background subagents (default: 600000) |
| `TASK_MAX_OUTPUT_LENGTH` | Maximum characters in subagent output before truncation (default: 32000, max: 160000) |
| `MAX_STRUCTURED_OUTPUT_RETRIES` | Retries when model response fails `--json-schema` validation in non-interactive mode (default: 5) |
| `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` | Maximum consecutive times a Stop hook may block the turn from ending before Claude Code overrides it (default: 8) |
| `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` | SessionEnd hook time budget in ms. Default: 1.5s, raised to the highest configured per-hook timeout up to 60s |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` | Credential refresh interval in ms for `apiKeyHelper` |
| `MCP_TIMEOUT` | MCP server startup timeout in ms (default: 30000) |
| `MCP_TOOL_TIMEOUT` | MCP tool execution timeout in ms (default: 100000000) |

### Behavior Control

| Variable | Description |
|----------|-------------|
| `CLAUDECODE` | Set to `1` in subprocesses Claude Code spawns (Bash/PowerShell tools, tmux sessions, hook commands, status line commands, stdio MCP subprocesses). Use to detect when a script runs inside Claude Code |
| `DEBUG` | Set to `1` (or `true`/`yes`/`on`) to enable debug mode. Logs written to `~/.claude/debug/<session-id>.txt`. Namespace patterns like `DEBUG=express:*` do not trigger it |
| `CLAUDE_CODE_DEBUG_LOGS_DIR` | Override the debug log file path (file path, not a directory). Requires debug mode enabled separately |
| `CLAUDE_CODE_DEBUG_LOG_LEVEL` | Minimum log level for the debug file: `verbose`, `debug` (default), `info`, `warn`, `error` |
| `CLAUDE_CODE_SHELL` | Override automatic shell detection |
| `CLAUDE_CODE_SHELL_PREFIX` | Command prefix prepended to all shell commands Claude Code spawns |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | Return to the original working directory after each Bash command in the main session (`1` to enable) |
| `CLAUDE_CODE_NEW_INIT` | Set to `1` to make `/init` run an interactive setup flow asking which files to generate |
| `CLAUDE_CODE_SIMPLE` | Run with minimal system prompt and only Bash, file read, and file edit tools. Equivalent to `--bare` |
| `CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT` | Set to `1` to use a shorter system prompt and abbreviated tool descriptions. Set to `0`/`false`/`no`/`off` to opt out |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | Set to `1` to strip Anthropic and cloud provider credentials from subprocess environments (Bash, hooks, MCP stdio servers) |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Set to `1` to load CLAUDE.md files from directories specified with `--add-dir` |
| `CLAUDE_CODE_TMPDIR` | Override the temp directory used for internal temp files |
| `CLAUDE_CODE_GIT_BASH_PATH` | Windows only: path to Git Bash executable when not in PATH |
| `CLAUDE_CODE_GLOB_HIDDEN` | Set to `false` to exclude dotfiles from Glob tool results (dotfiles included by default) |
| `CLAUDE_CODE_GLOB_NO_IGNORE` | Set to `false` to make the Glob tool respect `.gitignore` patterns |
| `CLAUDE_CODE_GLOB_TIMEOUT_SECONDS` | Glob tool file discovery timeout in seconds (default: 20, 60 on WSL) |
| `CLAUDE_CODE_USE_NATIVE_FILE_SEARCH` | Set to `1` to discover commands/subagents using Node.js file APIs instead of ripgrep |
| `CLAUDE_CODE_PERFORCE_MODE` | Set to `1` to enable Perforce-aware write protection (edits fail on files lacking owner-write bit) |
| `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY` | Set to `1` to stop Claude Code from passing `-ExecutionPolicy Bypass` when spawning PowerShell |
| `CLAUDE_CODE_FORK_SUBAGENT` | Set to `1` to make forked subagents the default: spawned agents inherit full conversation context instead of starting fresh |
| `CLAUDE_CODE_AUTO_BACKGROUND_TASKS` | Set to `1` to force-enable automatic backgrounding of long-running agent tasks |
| `CLAUDE_CODE_REMOTE` | Set automatically to `true` when running as a cloud session |
| `CLAUDE_CODE_REMOTE_SESSION_ID` | Set automatically in cloud sessions to the current session ID |
| `CLAUDE_CODE_SESSION_ID` | Set automatically to the current session ID in Bash/PowerShell subprocesses, hook commands, and MCP stdio subprocesses |
| `CLAUDE_EFFORT` | Set automatically in Bash/hook subprocesses to the active effort level: `low`, `medium`, `high`, `xhigh`, or `max` |
| `CLAUDE_ENV_FILE` | Path to a shell script run before each Bash command. Also populated dynamically by SessionStart, Setup, CwdChanged, and FileChanged hooks |
| `USE_BUILTIN_RIPGREP` | Set to `0` to use system-installed `rg` instead of the one bundled with Claude Code |

### Context Window and Compaction

| Variable | Description |
|----------|-------------|
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | Auto-compact trigger threshold as a percentage (1-100). Default ~95%. Lower values trigger compaction earlier |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | Context capacity in tokens used for compaction calculations. Defaults to model's context window (200K standard, 1M for extended). Lower value on a 1M model treats it as smaller for compaction purposes |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | Set to `1` to disable 1M token context window support |
| `DISABLE_AUTO_COMPACT` | Set to `1` to disable automatic compaction when approaching the context limit. Manual `/compact` remains available |
| `DISABLE_COMPACT` | Set to `1` to disable all compaction, including manual `/compact` |
| `CLAUDE_CODE_DISABLE_THINKING` | Set to `1` to force-disable extended thinking regardless of model support |
| `DISABLE_INTERLEAVED_THINKING` | Set to `1` to prevent sending the interleaved-thinking beta header. Use when your gateway does not support it |

### Telemetry and Observability

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Enable OpenTelemetry data collection (`1` to enable). Required before configuring OTel exporters |
| `DISABLE_TELEMETRY` | Disable telemetry (`1` to disable) |
| `DO_NOT_TRACK` | Set to `1` to opt out of telemetry. Equivalent to `DISABLE_TELEMETRY` |
| `DISABLE_ERROR_REPORTING` | Disable Sentry error reporting (`1` to disable) |
| `DISABLE_GROWTHBOOK` | Set to `1` to disable GrowthBook feature-flag fetching and use code defaults for every flag |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Equivalent to setting `DISABLE_AUTOUPDATER`, `DISABLE_FEEDBACK_COMMAND`, `DISABLE_ERROR_REPORTING`, and `DISABLE_TELEMETRY` |

### OpenTelemetry

Standard OTEL exporter variables (`OTEL_METRICS_EXPORTER`, `OTEL_LOGS_EXPORTER`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL`, `OTEL_EXPORTER_OTLP_HEADERS`, `OTEL_METRIC_EXPORT_INTERVAL`, `OTEL_RESOURCE_ATTRIBUTES`, and signal-specific variants) are supported. `CLAUDE_CODE_ENABLE_TELEMETRY=1` is required to activate OTel collection.

| Variable | Description |
|----------|-------------|
| `OTEL_LOG_RAW_API_BODIES` | Emit API request/response JSON as log events. Set to `1` for inline bodies (truncated at 60 KB), or `file:<dir>` to write full bodies to disk |
| `OTEL_LOG_TOOL_CONTENT` | Set to `1` to include tool input/output content in OTel span events. Disabled by default |
| `OTEL_LOG_TOOL_DETAILS` | Set to `1` to include tool input arguments, MCP server names, and raw error strings in OTel traces. Disabled by default |
| `OTEL_LOG_USER_PROMPTS` | Set to `1` to include user prompt text in OTel traces. Disabled by default |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Set to `false` to exclude account UUID from metrics attributes (default: included) |
| `OTEL_METRICS_INCLUDE_ENTRYPOINT` | Set to `true` to include session entrypoint in metrics attributes (default: excluded). Added in v2.1.152 |
| `OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES` | Set to `false` to exclude `OTEL_RESOURCE_ATTRIBUTES` keys from metric datapoint labels (default: included). Added in v2.1.161 |
| `OTEL_METRICS_INCLUDE_SESSION_ID` | Set to `false` to exclude session ID from metrics attributes (default: included) |
| `OTEL_METRICS_INCLUDE_VERSION` | Set to `true` to include Claude Code version in metrics attributes (default: excluded) |
| `CLAUDE_CODE_OTEL_FLUSH_TIMEOUT_MS` | Timeout in ms for flushing pending OTel spans on shutdown (default: 5000) |
| `CLAUDE_CODE_OTEL_SHUTDOWN_TIMEOUT_MS` | Timeout in ms for the OTel exporter to finish on exit (default: 2000) |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` | Refresh interval in ms for dynamic OTel headers (default: 1740000, 29 minutes) |
| `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` | Set to `1` to route session quality survey ratings to your OTel collector instead of Anthropic |
| `CLAUDE_CODE_PROPAGATE_TRACEPARENT` | Set to `1` to propagate W3C trace context when `ANTHROPIC_BASE_URL` points at a custom proxy. Added in v2.1.152 |

### Feature Toggles

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` | Disable adaptive reasoning on supported models (`1` to disable). No effect on Opus 4.7 and later |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | Strip `anthropic-beta` request headers and beta tool-schema fields. Use when a proxy rejects unknown beta headers |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Disable all background task functionality including `run_in_background`, auto-backgrounding, and Ctrl+B |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | Set to `1` to disable auto memory. Set to `0` to force it on when `--bare` mode would disable it |
| `CLAUDE_CODE_DISABLE_FAST_MODE` | Disable fast mode entirely (`1` to disable) |
| `CLAUDE_CODE_DISABLE_CRON` | Disable scheduled/cron tasks (`1` to disable) |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | Remove built-in commit/PR instructions from system prompt. Takes precedence over `includeGitInstructions` |
| `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK` | Disable the non-streaming fallback for failed streaming requests |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` | Disable session quality survey prompts (`1` to disable) |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` | Disable automatic terminal title updates and background title-generation requests |
| `CLAUDE_CODE_DISABLE_AGENT_VIEW` | Set to `1` to disable background agents and agent view (`claude agents`, `--bg`, `/background`) |
| `CLAUDE_CODE_DISABLE_WORKFLOWS` | Set to `1` to disable workflows |
| `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING` | Set to `1` to disable file checkpointing. `/rewind` will not restore code changes |
| `CLAUDE_CODE_DISABLE_CLAUDE_MDS` | Set to `1` to prevent loading any CLAUDE.md memory files, including auto-memory |
| `CLAUDE_CODE_DISABLE_ATTACHMENTS` | Set to `1` to disable attachment processing. `@` file mentions sent as plain text |
| `CLAUDE_CODE_DISABLE_POLICY_SKILLS` | Set to `1` to skip loading skills from the system-wide managed skills directory |
| `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL` | Set to `1` to skip automatic addition of the official plugin marketplace on first run |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION` | Set to `false` to disable prompt suggestions in the input area |
| `CLAUDE_CODE_ENABLE_TASKS` | As of v2.1.142, Task tools are the default. Set to `0` to revert to `TodoWrite` |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | Enable experimental agent teams feature (`1` to enable) |
| `ENABLE_CLAUDEAI_MCP_SERVERS` | Set to `false` to disable Claude.ai MCP servers (enabled by default for logged-in users) |
| `CLAUDE_CODE_USE_POWERSHELL_TOOL` | Control the PowerShell tool. Auto-enabled on Windows without Git Bash. Set `0` to disable, `1` to opt in |
| `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` | Override session recap availability: `0` to force off, `1` to force on |
| `CLAUDE_CODE_ENABLE_FINE_GRAINED_TOOL_STREAMING` | Control streaming of tool call inputs. Set `0` to opt out, `1` to force on via proxy |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` | Set to `1` to populate the `/model` picker from your gateway's `/v1/models` endpoint |
| `DISABLE_DOCTOR_COMMAND` | Set to `1` to hide the `/doctor` command |
| `DISABLE_LOGIN_COMMAND` | Set to `1` to hide the `/login` command |
| `DISABLE_LOGOUT_COMMAND` | Set to `1` to hide the `/logout` command |
| `DISABLE_UPGRADE_COMMAND` | Set to `1` to hide the `/upgrade` command |
| `DISABLE_EXTRA_USAGE_COMMAND` | Set to `1` to hide the `/usage-credits` command |
| `DISABLE_INSTALL_GITHUB_APP_COMMAND` | Set to `1` to hide the `/install-github-app` command |
| `DISABLE_UPDATES` | Set to `1` to block all updates including manual `claude update` and `claude install` |
| `IS_DEMO` | Enable demo mode: hides email/org info, skips onboarding. Useful when screensharing |

### Prompt Caching

| Variable | Description |
|----------|-------------|
| `DISABLE_PROMPT_CACHING` | Disable all prompt caching (`1` to disable, takes precedence over per-model settings) |
| `DISABLE_PROMPT_CACHING_HAIKU` | Disable prompt caching for Haiku model requests |
| `DISABLE_PROMPT_CACHING_SONNET` | Disable prompt caching for Sonnet model requests |
| `DISABLE_PROMPT_CACHING_OPUS` | Disable prompt caching for Opus model requests |
| `ENABLE_PROMPT_CACHING_1H` | Set to `1` to request a 1-hour prompt cache TTL instead of the default 5 minutes |
| `ENABLE_PROMPT_CACHING_1H_BEDROCK` | **DEPRECATED.** Use `ENABLE_PROMPT_CACHING_1H` instead |
| `FORCE_PROMPT_CACHING_5M` | Set to `1` to force the 5-minute cache TTL even when 1-hour TTL would otherwise apply |
| `CLAUDE_CODE_ATTRIBUTION_HEADER` | Set to `0` to omit the attribution block from the system prompt. Improves prompt-cache hit rates through LLM gateways |

### MCP Configuration

| Variable | Description |
|----------|-------------|
| `MAX_MCP_OUTPUT_TOKENS` | Max MCP output tokens per call (default: 25000). Warning shown when output exceeds 10,000 tokens |
| `ENABLE_TOOL_SEARCH` | MCP tool search mode: `auto:N` activates when tool count exceeds N% of context, `true` always defers, `false` loads all upfront |
| `MCP_CLIENT_SECRET` | MCP OAuth client secret. Avoids the interactive prompt when adding a server with `--client-secret` |
| `MCP_OAUTH_CALLBACK_PORT` | Fixed port for the MCP OAuth redirect callback |
| `MCP_CONNECTION_NONBLOCKING` | As of v2.1.142, MCP startup is non-blocking by default. Set to `0` to restore the blocking 5-second wait |
| `MCP_CONNECT_TIMEOUT_MS` | How long blocking MCP startup waits before snapshotting the tool list (default: 5000) |
| `MCP_SERVER_CONNECTION_BATCH_SIZE` | Maximum stdio MCP servers connected in parallel during startup (default: 3) |
| `MCP_REMOTE_SERVER_CONNECTION_BATCH_SIZE` | Maximum remote (HTTP/SSE) MCP servers connected in parallel during startup (default: 20) |
| `CLAUDE_CODE_MCP_ALLOWLIST_ENV` | Set to `1` to spawn stdio MCP servers with only a safe baseline environment plus the server's configured `env` |
| `CLAUDE_AGENT_SDK_MCP_NO_PREFIX` | Set to `1` to skip the `mcp__<server>__` prefix on tool names from SDK-created MCP servers |

### Proxy and Network

| Variable | Description |
|----------|-------------|
| `HTTP_PROXY` | HTTP proxy URL for network requests |
| `HTTPS_PROXY` | HTTPS proxy URL for network requests |
| `NO_PROXY` | Comma-separated hosts that bypass the proxy |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS` | Allow the proxy to perform DNS resolution (`1` to enable) |
| `CLAUDE_CODE_CERT_STORE` | Comma-separated CA certificate sources: `bundled` (Mozilla CA set) and/or `system` (OS trust store). Default: `bundled,system` |
| `CLAUDE_CODE_CLIENT_CERT` | Client certificate path for mTLS |
| `CLAUDE_CODE_CLIENT_KEY` | Client private key path for mTLS |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE` | Passphrase for an encrypted mTLS key |
| `CLAUDE_CODE_EXTRA_BODY` | JSON object merged into the top level of every API request body. Useful for provider-specific parameters |
| `CLAUDE_ENABLE_STREAM_WATCHDOG` | Set to `1` to enable event-level streaming idle watchdog. Off by default |
| `CLAUDE_ENABLE_BYTE_WATCHDOG` | Force-enable byte-level streaming idle watchdog. Default on for Anthropic API connections. Set `0` to disable |
| `CLAUDE_STREAM_IDLE_TIMEOUT_MS` | Timeout in ms before the streaming watchdog closes a stalled connection (default minimum: 300000) |

### UI and Display

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_NO_FLICKER` | Set to `1` to enable fullscreen rendering (reduces flicker, keeps memory flat in long conversations). Equivalent to the `tui` setting |
| `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN` | Set to `1` to disable fullscreen rendering and use the classic main-screen renderer |
| `CLAUDE_CODE_ALT_SCREEN_FULL_REPAINT` | Set to `1` to repaint the entire screen on every frame instead of incremental updates. Use if fullscreen mode shows stale text |
| `CLAUDE_CODE_DISABLE_VIRTUAL_SCROLL` | Set to `1` to disable virtual scrolling in fullscreen mode. Use if scrolling shows blank regions |
| `CLAUDE_CODE_DISABLE_MOUSE` | Set to `1` to disable mouse tracking in fullscreen mode. Keeps terminal native copy-on-select behavior |
| `CLAUDE_CODE_SCROLL_SPEED` | Mouse wheel scroll multiplier in fullscreen mode (1-20) |
| `CLAUDE_CODE_NATIVE_CURSOR` | Set to `1` to show the terminal's own cursor at the input caret instead of a drawn block |
| `CLAUDE_CODE_ACCESSIBILITY` | Set to `1` to keep the native terminal cursor visible and disable the inverted-text cursor indicator |
| `CLAUDE_CODE_HIDE_CWD` | Set to `1` to hide the working directory in the startup logo |
| `CLAUDE_CODE_TMUX_TRUECOLOR` | Set to `1` to allow 24-bit truecolor output inside tmux |
| `CLAUDE_CODE_FORCE_SYNC_OUTPUT` | Set to `1` to force-enable synchronized output (DEC private mode 2026) when your terminal supports it but is not auto-detected |
| `CLAUDE_CODE_SYNTAX_HIGHLIGHT` | Set to `false` to disable syntax highlighting in diff output |
| `CLAUDE_CODE_AUTO_CONNECT_IDE` | Override automatic IDE connection. Set to `false` to prevent it, `true` to force a connection attempt |
| `CLAUDE_CODE_IDE_HOST_OVERRIDE` | Override the host address used to connect to the IDE extension |
| `CLAUDE_CODE_IDE_SKIP_VALID_CHECK` | Set to `1` to skip validation of IDE lockfile entries during connection |
| `DISABLE_COST_WARNINGS` | Disable cost warning messages |
| `DISABLE_INSTALLATION_CHECKS` | Disable installation warnings |
| `DISABLE_AUTOUPDATER` | Disable the auto-updater. Manual `claude update` still works |
| `DISABLE_FEEDBACK_COMMAND` | Disable the `/feedback` command. Also accepted as `DISABLE_BUG_COMMAND` |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL` | Skip automatic IDE extension installation (`1` to skip) |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | Character budget for skill metadata shown to the Skill tool. Scales dynamically at 1% of the context window |

### Plugins

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_PLUGIN_CACHE_DIR` | Override the plugins root directory (default: `~/.claude/plugins`) |
| `CLAUDE_CODE_PLUGIN_SEED_DIR` | Path(s) to read-only plugin seed directories, separated by `:` on Unix or `;` on Windows. Use to bundle plugins into container images |
| `CLAUDE_CODE_PLUGIN_PREFER_HTTPS` | Set to `1` to clone GitHub `owner/repo` sources over HTTPS instead of SSH |
| `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` | Set to `1` to keep existing marketplace cache when a `git pull` fails. Useful in offline environments |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` | Timeout in ms for git operations during plugin install/update (default: 120000) |
| `CLAUDE_CODE_SYNC_PLUGIN_INSTALL` | Set to `1` in non-interactive mode (`-p` flag) to wait for plugin installation before the first query |
| `CLAUDE_CODE_SYNC_PLUGIN_INSTALL_TIMEOUT_MS` | Timeout in ms for synchronous plugin installation. No default (waits until complete without this var) |
| `CLAUDE_CODE_ENABLE_BACKGROUND_PLUGIN_REFRESH` | Set to `1` to refresh plugin state at turn boundaries in non-interactive mode after a background install |
| `FORCE_AUTOUPDATE_PLUGINS` | Set to `1` to force plugin auto-updates even when the main auto-updater is disabled |

### SDK and Headless

| Variable | Description |
|----------|-------------|
| `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS` | Set to `1` to disable all built-in subagent types (Explore, Plan) in non-interactive mode only |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` | Time in ms to wait after the query loop becomes idle before automatically exiting. Useful for SDK/scripted sessions |
| `CLAUDE_CODE_RESUME_INTERRUPTED_TURN` | Set to `1` to automatically resume if the previous session ended mid-turn. For SDK use |
| `CLAUDE_CODE_RESUME_PROMPT` | Override the continuation message injected when resuming a mid-turn session (default: `Continue from where you left off.`) |
| `CLAUDE_CODE_SKIP_PROMPT_HISTORY` | Set to `1` to skip writing prompt history and session transcripts to disk |
| `CLAUDE_CODE_SYNC_SKILLS` | Set to `1` to download enabled Claude.ai skills before the first query and resync every 10 minutes. Non-interactive mode only |
| `CLAUDE_CODE_SYNC_SKILLS_WAIT_TIMEOUT_MS` | Timeout in ms for initial skills sync when `CLAUDE_CODE_SYNC_SKILLS` is set (default: 5000) |
| `CLAUDE_CODE_SCRIPT_CAPS` | JSON object limiting invocations of specific scripts per session when `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` is set |
| `CCR_FORCE_BUNDLE` | Set to `1` to force `claude --remote` to bundle and upload the local repo even when GitHub access is available |
| `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` | Prefix for auto-generated Remote Control session names. Defaults to machine hostname |

### Agent Teams and Tasks

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_TEAM_NAME` | Team name for agent teams. Set automatically on agent team members |
| `CLAUDE_CODE_TASK_LIST_ID` | Share a task list across sessions. Set the same ID in multiple Claude Code instances to coordinate on a shared task list |

### Unverified Variables

These appear in community sources or older documentation but are not confirmed in current official docs.

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_USER_EMAIL` `⚠️ Unverified` | Provide user email synchronously for authentication |
| `CLAUDE_CODE_ORGANIZATION_UUID` `⚠️ Unverified` | Provide organization UUID synchronously for authentication |
| `CLAUDE_CODE_ACCOUNT_UUID` `⚠️ Unverified` | Override account UUID for authentication |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED` `⚠️ Unverified` | Require plan mode for sessions |
| `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS` `⚠️ Unverified` | Allow fast mode when org status check fails due to network error |
| `CLAUDE_CODE_SKIP_SETTINGS_SETUP` `⚠️ Unverified` | Skip first-run settings setup flow |
| `CLAUDE_CODE_DISABLE_TOOLS` `⚠️ Unverified` | Comma-separated list of tools to disable |
| `CLAUDE_CODE_DISABLE_MCP` `⚠️ Unverified` | Disable all MCP servers (`1` to disable) |
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO` `⚠️ Unverified` | Hide email/org info from UI |
| `CLAUDE_CODE_PROMPT_CACHING_ENABLED` `⚠️ Unverified` | Override prompt caching behavior |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS` `⚠️ Unverified` | Disable flavor text and non-essential model calls |

---

## Complete Example

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "sonnet",
  "language": "english",
  "cleanupPeriodDays": 30,
  "autoUpdatesChannel": "stable",
  "alwaysThinkingEnabled": false,
  "includeGitInstructions": true,
  "effortLevel": "medium",
  "plansDirectory": "./plans",

  "worktree": {
    "symlinkDirectories": ["node_modules"],
    "sparsePaths": ["packages/my-app", "shared/utils"]
  },

  "permissions": {
    "allow": [
      "Edit(*)",
      "Write(*)",
      "Bash(npm run *)",
      "Bash(git *)",
      "WebFetch(domain:*)",
      "mcp__*"
    ],
    "ask": ["Bash(git push *)"],
    "deny": [
      "Read(.env)",
      "Read(./secrets/**)"
    ],
    "additionalDirectories": ["../shared/"],
    "defaultMode": "acceptEdits"
  },

  "enableAllProjectMcpServers": true,

  "sandbox": {
    "enabled": true,
    "excludedCommands": ["git push *", "git fetch *", "docker *"],
    "filesystem": {
      "allowWrite": ["/tmp/build"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "allowUnixSockets": ["/var/run/docker.sock"]
    }
  },

  "attribution": {
    "commit": "Generated with Claude Code",
    "pr": ""
  },

  "statusLine": {
    "type": "command",
    "command": "git branch --show-current"
  },

  "spinnerTipsEnabled": true,
  "prefersReducedMotion": false,

  "env": {
    "NODE_ENV": "development",
    "CLAUDE_CODE_EFFORT_LEVEL": "medium"
  }
}
```

---

## Quick Reference

| Task | Setting / Variable |
|------|--------------------|
| Set default model | `model` in settings or `ANTHROPIC_MODEL` env var |
| Lock model choices | `availableModels` array |
| Silence telemetry | `DISABLE_TELEMETRY=1` or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` |
| Auto-approve bash | `permissions.defaultMode: "acceptEdits"` |
| Block sensitive files | `permissions.deny: ["Read(.env)"]` |
| Reduce context compaction | `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` |
| Set response language | `language: "japanese"` |
| Custom spinner text | `spinnerVerbs` + `spinnerTipsOverride` |
| Remove attribution | `attribution.commit: ""`, `attribution.pr: ""` |
| Pin to stable releases | `autoUpdatesChannel: "stable"` |
| Dynamic auth token | `apiKeyHelper: "/path/to/script.sh"` |
| Large monorepo | `worktree.symlinkDirectories` + `worktree.sparsePaths` |
| Enable sandboxing | `sandbox.enabled: true` |
| Trust all project MCP servers | `enableAllProjectMcpServers: true` |
