---
title: "Claude Code Privacy: What Gets Sent to Anthropic & How to Control It"
description: "What Claude Code sends to Anthropic servers: code context, shell commands, MCP logs. Data usage and retention by plan (Consumer 5 yr, ZDR 0 days), whether your code trains models, and how to control it."
tags: [privacy, security, guide]
keywords:
  - "anthropic api data retention official docs"
  - "anthropic api zero data retention official docs"
  - "anthropic claude api data privacy policy"
  - "anthropic api data retention policy 30 days"
  - "anthropic api data usage privacy"
---

# Claude Code Data Privacy: What the Official Docs Don't Cover

The Anthropic privacy page documents retention tiers (Consumer 5 years, ZDR 0 days, etc.). That's useful background, but it doesn't cover the risks that are specific to Claude Code as a local CLI tool. This guide focuses on those: the six data exposure vectors that exist because Claude Code runs with filesystem access, spawns subprocesses, and calls MCP servers, and how to block each one.

> **Quick reference**: Anthropic retention tiers are summarized in the table below. Full official policy at [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls).

## TL;DR - Retention Summary

| Configuration | Retention Period | Training | How to Enable |
|---------------|------------------|----------|---------------|
| **Consumer (default)** | 5 years | Yes | (default state) |
| **Consumer (opt-out)** | 30 days | No | [claude.ai/settings](https://claude.ai/settings/data-privacy-controls) |
| **Team / Enterprise / API** | 30 days | No (default) | Use Team, Enterprise plan, or API keys |
| **ZDR (Zero Data Retention)** | 0 days server-side | No | Appropriately configured API keys |

**Immediate action**: [Disable training data usage](https://claude.ai/settings/data-privacy-controls) to reduce retention from 5 years to 30 days.

---

## 1. Understanding the Data Flow

### What Leaves Your Machine

When you use Claude Code, the following data is sent to Anthropic:

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR LOCAL MACHINE                       │
├─────────────────────────────────────────────────────────────┤
│  • Prompts you type                                         │
│  • Files Claude reads (including .env if not excluded!)     │
│  • MCP server results (SQL queries, API responses)          │
│  • Bash command outputs                                     │
│  • Error messages and stack traces                          │
└───────────┬──────────────────┬──────────────┬───────────────┘
            │                  │              │
            ▼ HTTPS/TLS       ▼ HTTPS        ▼ HTTPS
┌───────────────────┐ ┌──────────────┐ ┌─────────────────────┐
│   ANTHROPIC API   │ │   STATSIG    │ │       SENTRY        │
├───────────────────┤ ├──────────────┤ ├─────────────────────┤
│ • Your prompts    │ │ • Latency,   │ │ • Error logs        │
│ • Model responses │ │   reliability│ │ • No code or        │
│ • Retention per   │ │ • No code or │ │   file paths        │
│   your tier       │ │   file paths │ │                     │
└───────────────────┘ └──────────────┘ └─────────────────────┘
                       (opt-out:        (opt-out:
                       DISABLE_         DISABLE_ERROR_
                       TELEMETRY=1)     REPORTING=1)
```

### What This Means in Practice

| Scenario | Data Sent to Anthropic |
|----------|------------------------|
| You ask Claude to read `src/app.ts` | Full file contents |
| You run `git status` via Claude | Command output |
| MCP executes `SELECT * FROM users` | Query results with user data |
| Claude reads `.env` file | API keys, passwords, secrets |
| Error occurs in your code | Full stack trace with paths |

---

## 2. Known Risks

### Risk 1: Automatic File Reading

Claude Code reads files to understand context. By default, this includes:

- `.env` and `.env.local` files (API keys, passwords)
- `credentials.json`, `secrets.yaml` (service accounts)
- SSH keys if in workspace scope
- Database connection strings

**Mitigation**: Configure `excludePatterns` (see Section 4).

### Risk 2: MCP Database Access

When you configure database MCP servers (Neon, Supabase, PlanetScale):

```
Your Query: "Show me recent orders"
            ↓
MCP Executes: SELECT * FROM orders LIMIT 100
            ↓
Results Sent: 100 rows with customer names, emails, addresses
            ↓
Stored at Anthropic: According to your retention tier
```

**Mitigation**: Never connect production databases. Use dev/staging with anonymized data.

### Risk 3: Shell Command Output

Bash commands and their output are included in context:

```bash
# This output goes to Anthropic:
$ env | grep API
OPENAI_API_KEY=sk-abc123...
STRIPE_SECRET_KEY=sk_live_...
```

**Mitigation**: Use hooks to filter sensitive command outputs.

### Risk 4: The `/bug` Command Sends Everything (Retained 5 Years)

When you run `/bug` in Claude Code, your **full conversation history** (including all code, file contents, and potentially secrets) is sent to Anthropic for bug triage. This data is retained for **5 years**, regardless of your training opt-out setting.

This is independent of your privacy preferences: even with training disabled and 30-day retention, bug reports follow their own 5-year retention policy. The distinction matters because `/bug` is easy to trigger accidentally, and because its retention period is longer than any other data sent during normal Claude Code usage.

What gets included in a bug report: your entire session context at the time of `/bug` invocation. File paths, file contents Claude read during the session, bash command outputs, MCP server results, and any secrets that appeared in any of those. There is no scrubbing or filtering before submission.

**Verify if you have already disabled it:**

```bash
echo $DISABLE_BUG_COMMAND
```

If empty, the command is active. To disable permanently:

```bash
# Add to ~/.zshrc or ~/.bashrc
export DISABLE_BUG_COMMAND=1
```

If you work on multiple machines or share dotfiles via a repo, adding this to your profile is the only way to keep it off across environments. Environment variables set in `.claude/settings.json` do not persist across shell sessions.

### Risk 5: Documented Community Incidents

| Incident | Source |
|----------|--------|
| Claude reads `.env` by default | r/ClaudeAI, GitHub issues |
| DROP TABLE attempts on poorly configured MCP | r/ClaudeAI |
| Credentials exposed via environment variables | GitHub issues |
| Prompt injection via malicious MCP servers | r/programming |

### Risk 6: Claude Desktop Browser Integration: Silent Native Messaging Host Installation

Claude Desktop installs native messaging host manifest files into browsers' `NativeMessagingHosts` directories to enable its "Claude in Chrome" feature. As of April 2026, this happens without an explicit opt-in prompt from the user.

**What gets installed:**

```
~/Library/Application Support/Google/Chrome/NativeMessagingHosts/
  com.anthropic.claude_browser_extension.json

/Applications/Claude.app/Contents/MacOS/
  claude_browser_native_host  (helper binary)
```

Claude Desktop writes these files to **all Chromium-based browsers found on the system** (Chrome, Brave, Edge, Arc, Vivaldi, Opera, Chromium), including browsers not installed at the time of Claude Desktop's installation. The "Don't ask" opt-out in Claude Desktop's preferences does not reliably prevent this ([GitHub #53864](https://github.com/anthropics/claude-code/issues/53864), April 2026).

**What native messaging actually does (and doesn't do):**

Native messaging is a standard Chrome mechanism used by password managers, VPNs, and many other legitimate apps. The native host can only receive messages sent by a Chrome extension that explicitly targets it. It cannot initiate connections to the browser, read tabs, or access browser data unsolicited. This is architecturally different from spyware.

The real issue is the **consent failure**, not the mechanism itself. An application silently modifying another vendor's application directories violates the principle of least surprise, regardless of intent.

**What to check if you're concerned:**

```bash
# List all native messaging hosts installed for Chrome
ls ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/

# Check if Anthropic's host is present
cat ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_browser_extension.json

# Check other browsers
ls ~/Library/Application\ Support/BraveSoftware/Brave-Browser/NativeMessagingHosts/
ls ~/Library/Application\ Support/Microsoft\ Edge/NativeMessagingHosts/
```

**To remove:**

```bash
# Remove from Chrome (repeat for each browser as needed)
rm ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_browser_extension.json

# Restart Chrome after deletion
```

Uninstalling Claude Desktop removes the helper binary but may leave stale manifest files in some browser directories. Restart the affected browsers after cleanup.

**Conflict with Claude Code:** When both Claude Desktop and Claude Code CLI are installed, the Chrome extension always binds to Claude Desktop's native host, making Claude Code's `claude-in-chrome` MCP tools unreachable ([GitHub #51949](https://github.com/anthropics/claude-code/issues/51949)). This is a known bug with no workaround as of April 2026 other than uninstalling Claude Desktop.

**Mitigation:**

If you don't use the browser integration feature, you can safely delete the manifest files. Anthropic has not yet provided an official opt-out mechanism that reliably prevents installation. Monitor [GitHub #53864](https://github.com/anthropics/claude-code/issues/53864) for updates.

---

### Risk 7: The Local-Looking Network Client

A CLI or MCP server can advertise "zero dependencies, no signup, no telemetry" and still send every input you give it to a server you do not control. Those three claims are about the *package*, not about the *data*. A thin HTTP client genuinely has zero dependencies, because it contains nothing.

The tell is arithmetic. Compare the unpacked size against the advertised functionality before installing anything:

```bash
npm view <package> --json | grep -E '"unpackedSize"|"fileCount"|"dependencies"'
```

A package advertising 148 analysis tools in 17 KB across 3 files is not carrying 148 tools. It is carrying a `fetch` call. Real local implementations of tokenizers, scanners, or embedding math have a size floor that a network client does not. When the numbers do not add up, read the source before running it; at that size it takes minutes:

```bash
curl -sL $(npm view <package> dist.tarball) | tar -xzO package/index.js | head -50
```

Honest projects often say so plainly in a header comment or README. The problem is that the marketing copy and the architecture live in different places, and only one of them ends up in a LinkedIn post.

**Why MCP mode makes this categorically worse:**

In CLI mode, a human chooses each input. That is a discipline problem, and a careful team can live with a hosted tool by simply never pasting anything sensitive into it.

In MCP mode, the agent chooses the input, and the agent has your codebase in context. It will pass a proprietary source file to a hosted `count_tokens` helper because that is a reasonable thing to do with a token counter. Nobody approved that specific call, because nobody was asked. The tool's own safety engineering does not help here: temp-file hardening and secret-parameter warnings protect against argv leaks and local attacks, not against an agent deciding on its own what to send.

This converts a rule that a team can hold ("don't paste customer data into that tool") into one it cannot ("don't let the agent read the wrong file"). For regulated data, minors' data, or client source under NDA, that is disqualifying regardless of how well the client is written.

**The check that matters:**

For any hosted MCP server, ask whether there is a local execution path at all. If every tool call is a network call, then adding the server to `.mcp.json` means granting a third party read access to whatever your agent decides is relevant. "No signup" makes this worse rather than better: no account means no data processing agreement, no named subprocessor, and no retention policy you can point at during an audit.

---

## 3. Protective Measures

### Immediate Actions

#### 3.1 Configure File Exclusions

In `.claude/settings.json`, use `permissions.deny` to block access to sensitive files:

```json
{
  "permissions": {
    "deny": [
      "Read(./.env*)",
      "Edit(./.env*)",
      "Write(./.env*)",
      "Bash(cat .env*)",
      "Bash(head .env*)",
      "Read(./secrets/**)",
      "Read(./**/credentials*)",
      "Read(./**/*.pem)",
      "Read(./**/*.key)",
      "Read(./**/service-account*.json)"
    ]
  }
}
```

> **Note**: The old `excludePatterns` and `ignorePatterns` settings were deprecated in October 2025. Use `permissions.deny` instead.

> **Warning**: `permissions.deny` has [known limitations](./security-hardening.md#known-limitations-of-permissionsdeny). For defense-in-depth, combine with security hooks and external secrets management.

#### 3.2 Use Security Hooks

Create `.claude/hooks/PreToolUse.sh`:

```bash
#!/bin/bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool.name')

if [[ "$TOOL_NAME" == "Read" ]]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool.input.file_path')

    # Block reading sensitive files
    if [[ "$FILE_PATH" =~ \.env|credentials|secrets|\.pem|\.key ]]; then
        echo "BLOCKED: Attempted to read sensitive file: $FILE_PATH" >&2
        exit 2  # Block the operation
    fi
fi
```

#### 3.3 Opt-Out of Telemetry and Error Reporting

Claude Code connects to third-party services for operational metrics (Statsig) and error logging (Sentry). These do not include your code or file paths, but you can disable them entirely:

| Variable | What it Disables |
|----------|-----------------|
| `DISABLE_TELEMETRY=1` | Statsig operational metrics (latency, reliability, usage patterns) |
| `DISABLE_ERROR_REPORTING=1` | Sentry error logging |
| `DISABLE_BUG_COMMAND=1` | The `/bug` command (prevents sending full conversation history) |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` | All non-essential network traffic at once |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` | Session quality surveys (note: surveys only send your numeric rating, never transcripts) |

Add these to your shell profile for permanent effect:

```bash
# In ~/.zshrc or ~/.bashrc
export DISABLE_TELEMETRY=1
export DISABLE_ERROR_REPORTING=1
export DISABLE_BUG_COMMAND=1
```

> **Note**: When using Bedrock, Vertex, or Foundry providers, all non-essential traffic (telemetry, error reporting, bug command, surveys) is disabled by default.

### MCP Best Practices

| Rule | Rationale |
|------|-----------|
| **Never connect production databases** | All query results sent to Anthropic |
| **Use read-only database users** | Prevents DROP/DELETE/UPDATE accidents |
| **Anonymize development data** | Reduces PII exposure risk |
| **Create minimal test datasets** | Less data = less risk |
| **Audit MCP server sources** | Third-party MCPs may have vulnerabilities |

### For Teams

| Environment | Recommendation |
|-------------|----------------|
| **Development** | Opt-out + exclusions + anonymized data |
| **Staging** | Consider Enterprise API if handling real data |
| **Production** | NEVER connect Claude Code directly |

---

## 4. Comparison with Other Tools

| Feature | Claude Code + MCP | Cursor | GitHub Copilot |
|---------|-------------------|--------|----------------|
| Data scope sent | Full SQL results, files | Code snippets | Code snippets |
| Production DB access | Yes (via MCP) | Limited | Not designed for |
| Default retention | 5 years | Variable | 30 days |
| Training by default | Yes | Opt-in | Opt-in |

**Key difference**: MCP creates a unique attack surface because MCP servers are separate processes with independent network/filesystem access.

---

## 5. Enterprise Considerations

### When to Use Enterprise API (ZDR)

- Handling PII (names, emails, addresses)
- Regulated industries (HIPAA, GDPR, PCI-DSS)
- Client data processing
- Government contracts
- Financial services

### Evaluation Checklist

- [ ] Data classification policy exists for your organization
- [ ] API tier matches data sensitivity requirements
- [ ] Team trained on privacy controls
- [ ] Incident response plan for potential data exposure
- [ ] Legal/compliance review completed

---

## 6. Quick Reference

### Links

| Resource | URL |
|----------|-----|
| Privacy settings | https://claude.ai/settings/data-privacy-controls |
| Anthropic usage policy | https://www.anthropic.com/policies |
| Enterprise information | https://www.anthropic.com/enterprise |
| Terms of service | https://www.anthropic.com/legal/consumer-terms |

### Commands

```bash
# Check current Claude config
claude /config

# Verify exclusions are loaded
claude /status

# Run privacy audit
./examples/scripts/audit-scan.sh
```

### Quick Audit Checklist

Run these checks today. Each takes under two minutes.

**1. Training opt-out**
Go to [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls) and verify "Allow model training on your conversations" is OFF. If it is ON, your data is retained 5 years and used for training.

**2. `/bug` command disabled**

```bash
echo $DISABLE_BUG_COMMAND
# Should print: 1
# If empty: add "export DISABLE_BUG_COMMAND=1" to your ~/.zshrc
```

**3. `.env` files blocked**
Check your `.claude/settings.json`: it should contain at minimum `"Read(./.env*)"` in `permissions.deny`. If the file does not exist yet, Claude can read your `.env` right now.

**4. Native messaging host presence (macOS)**

```bash
ls ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/ 2>/dev/null | grep anthropic
# Nothing should appear if you don't use Claude Desktop
```

**5. MCP server inventory**
Open `~/.claude/claude.json` (or `.mcp.json` in your project root) and list every configured MCP server. For each database server, confirm it points to a dev or staging connection string, not production.

**6. Telemetry env vars**

```bash
echo $DISABLE_TELEMETRY
echo $DISABLE_ERROR_REPORTING
# Both should print: 1
```

**7. Shell command exposure**
Run `env | grep -iE 'key|secret|token|pass'` to see what environment variables are currently set. Any that appear here will be visible to Claude if it runs a bash command in that shell session.

## Go further

- [Whitepapers](/whitepapers/) - in-depth security and privacy analyses
- [Security](./security-hardening.md) - CVE tracking, threat campaigns, and hardening

---

## Changelog

- 2026-06: Reframed around CLI-specific risks. Removed policy paraphrase sections (retention tiers detail, Constitutional AI, IP considerations). Enriched /bug section with verification commands. Added 7-point Quick Audit Checklist.
- 2026-02: Fixed retention model (3 tiers to 4 tiers), added /bug command warning, telemetry opt-out variables, encryption-at-rest disclosure, updated ZDR conditions
- 2026-01: Initial version
