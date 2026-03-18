---
title: "Data Privacy & Retention Guide"
description: "What data Claude Code sends to Anthropic servers and how to protect sensitive information"
tags: [privacy, security, guide]
---

# Data Privacy & Retention Guide

> **Critical**: Everything you share with Claude Code is sent to Anthropic servers. This guide explains what data leaves your machine and how to protect sensitive information.

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

## 2. Anthropic Retention Policies

### Tier 1: Consumer Default (Training Enabled)

- **Retention**: 5 years
- **Usage**: Model improvement, training data
- **Applies to**: Free, Pro, Max plans with training setting ON

### Tier 2: Consumer Opt-Out (Training Disabled)

- **Retention**: 30 days
- **Usage**: Safety monitoring, abuse prevention only
- **How to enable**:
  1. Go to https://claude.ai/settings/data-privacy-controls
  2. Disable "Allow model training on your conversations"
  3. Changes apply immediately

### Tier 3: Commercial (Team / Enterprise / API)

- **Retention**: 30 days
- **Usage**: Safety monitoring, abuse prevention only
- **Training**: Not used for training by default (no opt-out needed)
- **Applies to**: Team plans, Enterprise plans, API users, third-party platforms, Claude Gov

### Tier 4: Zero Data Retention (ZDR)

- **Retention**: 0 days server-side (local client cache may persist up to 30 days)
- **Usage**: None retained on Anthropic servers
- **Requires**: Appropriately configured API keys (see [Anthropic documentation](https://www.anthropic.com/enterprise))
- **Use cases**: HIPAA (requires separate BAA), GDPR, PCI-DSS compliance, government contracts

> **Important**: Data is encrypted in transit via TLS but is **not encrypted at rest** on Anthropic servers. Factor this into your security assessments.

---

## 3. Known Risks

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

This is independent of your privacy preferences: even with training disabled and 30-day retention, bug reports follow their own 5-year retention policy.

**Mitigation**: Disable the command entirely if you work with sensitive codebases:

```bash
export DISABLE_BUG_COMMAND=1
```

Or add it to your shell profile (`~/.zshrc`, `~/.bashrc`) to make it permanent.

### Risk 5: Documented Community Incidents

| Incident | Source |
|----------|--------|
| Claude reads `.env` by default | r/ClaudeAI, GitHub issues |
| DROP TABLE attempts on poorly configured MCP | r/ClaudeAI |
| Credentials exposed via environment variables | GitHub issues |
| Prompt injection via malicious MCP servers | r/programming |

---

## 4. Protective Measures

### Immediate Actions

#### 4.1 Opt-Out of Training

1. Visit https://claude.ai/settings/data-privacy-controls
2. Toggle OFF "Allow model training"
3. Retention reduces from 5 years to 30 days

#### 4.2 Configure File Exclusions

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

#### 4.3 Use Security Hooks

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

#### 4.4 Opt-Out of Telemetry and Error Reporting

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

## 5. Comparison with Other Tools

| Feature | Claude Code + MCP | Cursor | GitHub Copilot |
|---------|-------------------|--------|----------------|
| Data scope sent | Full SQL results, files | Code snippets | Code snippets |
| Production DB access | Yes (via MCP) | Limited | Not designed for |
| Default retention | 5 years | Variable | 30 days |
| Training by default | Yes | Opt-in | Opt-in |

**Key difference**: MCP creates a unique attack surface because MCP servers are separate processes with independent network/filesystem access.

---

## 6. Enterprise Considerations

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

## 7. Quick Reference

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

### Quick Checklist

- [ ] Training opt-out enabled at claude.ai/settings
- [ ] `.env*` files blocked via `permissions.deny` in settings.json
- [ ] No production database connections via MCP
- [ ] Security hooks installed for sensitive file access
- [ ] Team aware of data flow to Anthropic

---

## 8. Intellectual Property Considerations

> **Disclaimer**: This is not legal advice. Consult a qualified attorney for your specific situation.

When using AI code generation tools, discuss these points with your legal team:

| Consideration | What to Discuss |
|---------------|-----------------|
| **Ownership** | Copyright status of AI-generated code remains legally unsettled in most jurisdictions |
| **License contamination** | Training data may include open-source code with copyleft licenses (GPL, AGPL) that could affect your codebase |
| **Vendor indemnification** | Some enterprise plans offer legal protection (e.g., Microsoft Copilot Enterprise includes IP indemnification) |
| **Sector compliance** | Regulated industries (healthcare, finance, government) may have additional IP requirements |

This guide focuses on Claude Code usage—not legal strategy. For IP guidance, consult specialized legal resources or your organization's legal counsel.

---

## 9. Claude's Governance & Values

### Constitutional AI Framework

Anthropic published Claude's constitution in January 2026 (CC0 license - public domain). This document defines the value hierarchy that guides Claude's behavior:

**Priority Order** (used to resolve conflicts):

1. **Broadly safe** - Never compromise human supervision and control
2. **Broadly ethical** - Honesty, harm avoidance, good conduct
3. **Anthropic compliance** - Internal guidelines and policies
4. **Genuinely helpful** - Real utility for users and society

### What This Means for Claude Code Users

| Scenario | Expected Behavior |
|----------|-------------------|
| Security-sensitive requests | Claude prioritizes safety over helpfulness (may be more conservative) |
| Borderline biology/chemistry | May decline or ask for context to assess safety implications |
| Ethical conflicts | Will follow hierarchy: safety > ethics > compliance > utility |

### Why This Matters

- **Training data source**: Constitution is used to generate synthetic training examples
- **Behavior specification**: Reference document explaining intended vs. accidental outputs
- **Audit & governance**: Provides legal/ethical foundation for compliance reviews
- **Your own agents**: CC0 license allows reuse/adaptation for custom models

### Resources

- Constitution full text: https://www.anthropic.com/constitution
- PDF version: https://www-cdn.anthropic.com/.../claudes-constitution.pdf
- Announcement: https://www.anthropic.com/news/claude-new-constitution
- Alignment research: https://alignment.anthropic.com/

---

## Changelog

- 2026-02: Fixed retention model (3 tiers to 4 tiers), added /bug command warning, telemetry opt-out variables, encryption-at-rest disclosure, updated ZDR conditions
- 2026-01: Added Claude's governance & constitutional AI framework section
- 2026-01: Added intellectual property considerations section
- 2026-01: Initial version - documenting retention policies and protective measures
