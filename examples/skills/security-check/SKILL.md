---
name: security-check
description: Quick configuration security check against known threats database
argument-hint: "[path]"
effort: medium
disable-model-invocation: true
---

# Security Check

Quick configuration security check against known threats database. Verifies your Claude Code setup for known malicious skills, vulnerable MCPs, dangerous patterns, and exposed secrets.

**Time**: ~30 seconds | **Scope**: Claude Code configuration only

## Instructions

You are a security analyst. Check the user's Claude Code configuration against the threat intelligence database bundled at `examples/skills/update-threat-db/threat-db.yaml`. Produce a concise, actionable report.

### Phase 1: Load Threat Database

Read `examples/skills/update-threat-db/threat-db.yaml` from this repository to load:
- Known malicious authors and skills
- CVE database for MCP servers
- Suspicious patterns for hooks, agents, and config

### Phase 2: MCP Server Audit

Read the user's MCP configuration:

```bash
# Global MCP config
cat ~/.claude.json 2>/dev/null | jq '.mcpServers // empty'

# Project MCP config
cat .mcp.json 2>/dev/null
```

**Check against threat-db.yaml:**
- [ ] Any MCP server matching a CVE entry? → CRITICAL
- [ ] Version pinning: are all MCP servers pinned to exact versions (not `@latest`)? → HIGH if unpinned
- [ ] Any `--dangerous-*` flags in MCP args? → CRITICAL
- [ ] Any MCP servers not on the Safe List (see `guide/security/security-hardening.md` §1.1)? → MEDIUM (flag for manual review)

### Phase 3: Skills & Agents Audit

```bash
# List installed skills
ls -la .claude/skills/ 2>/dev/null
ls -la ~/.claude/skills/ 2>/dev/null

# List agents
ls -la .claude/agents/ 2>/dev/null
ls -la ~/.claude/agents/ 2>/dev/null

# Check agent tools field
grep -r "^tools:" .claude/agents/ 2>/dev/null
grep -r "^tools:" ~/.claude/agents/ 2>/dev/null
```

**Check against threat-db.yaml:**
- [ ] Any skill/agent name matching `malicious_skills` entries? → CRITICAL
- [ ] Any skill/agent author matching `malicious_authors` entries? → CRITICAL
- [ ] Any agent with `tools: Bash` only? → HIGH
- [ ] Any agent with overly broad tool access + vague description? → MEDIUM

**Deep skill content analysis (SkillSpector-inspired patterns):**

```bash
# Hidden instructions: HTML comments, zero-width chars, large base64 blobs
grep -rn '<!--' .claude/skills/ ~/.claude/skills/ 2>/dev/null | grep -iv 'example\|comment\|html'
grep -rPn '[\x{200B}-\x{200D}\x{FEFF}\x{00AD}]' .claude/skills/ ~/.claude/skills/ 2>/dev/null
grep -rn -E '[A-Za-z0-9+/]{40,}={0,2}' .claude/skills/ ~/.claude/skills/ 2>/dev/null | grep -v 'sha\|hash\|checksum' | head -10

# Unicode deception: RTL override characters
grep -rPn '[\x{202E}\x{202D}\x{200F}]' .claude/skills/ ~/.claude/skills/ 2>/dev/null

# Trigger abuse: generic keywords that shadow built-in commands
grep -rn "trigger\|keyword\|when.*user" .claude/skills/ ~/.claude/skills/ 2>/dev/null | \
  grep -iE '\b(help|run|go|do|yes|ok|the|a |an |it)\b' | head -10

# Supply chain: remote execution patterns in skill scripts
find .claude/skills/ ~/.claude/skills/ \( -name "*.sh" -o -name "*.py" \) 2>/dev/null | \
  xargs grep -l "curl.*|\|wget.*|\|bash.*http\|eval.*curl" 2>/dev/null

# Rogue agent: cron/startup persistence written by skill scripts
find .claude/skills/ ~/.claude/skills/ -type f 2>/dev/null | \
  xargs grep -l "crontab\|launchctl\|systemctl\|~/.bashrc\|~/.zshrc\|autostart" 2>/dev/null

# Data exfiltration: env harvesting combined with network calls
find .claude/skills/ ~/.claude/skills/ -type f 2>/dev/null | \
  xargs grep -l "os.environ\|process.env\|getenv\|printenv" 2>/dev/null | \
  xargs grep -l "curl\|requests\|fetch\|http" 2>/dev/null
```

- [ ] Hidden HTML comments or zero-width characters in skill files? → HIGH
- [ ] Base64 blobs over 40 chars in skill content? → HIGH (verify: may be a legitimate hash)
- [ ] RTL unicode override characters? → HIGH
- [ ] Skill trigger keyword shadows a built-in (help, run, clear…)? → HIGH
- [ ] Executable scripts with `curl | bash` or remote eval? → CRITICAL
- [ ] Skill writes to crontab, launchctl, or shell rc files? → CRITICAL
- [ ] Skill reads env vars AND makes outbound network calls? → CRITICAL

### Phase 4: Hook Security

```bash
# List all hooks
find .claude/hooks/ -type f 2>/dev/null
find ~/.claude/hooks/ -type f 2>/dev/null

# Scan hooks for suspicious patterns
grep -rn "curl\|wget\|nc \|ncat\|netcat\|base64\|eval\|exec\|/dev/tcp\|/dev/udp" .claude/hooks/ 2>/dev/null
grep -rn "curl\|wget\|nc \|ncat\|netcat\|base64\|eval\|exec\|/dev/tcp\|/dev/udp" ~/.claude/hooks/ 2>/dev/null

# Check for credential access in hooks
grep -rn "ssh\|id_rsa\|id_ed25519\|\.env\|credentials\|secret\|password\|token\|api.key" .claude/hooks/ 2>/dev/null
grep -rn "ssh\|id_rsa\|id_ed25519\|\.env\|credentials\|secret\|password\|token\|api.key" ~/.claude/hooks/ 2>/dev/null
```

**Check against threat-db.yaml `suspicious_patterns.hooks`:**
- [ ] Network calls (`curl`, `wget`) → HIGH
- [ ] Reverse shell indicators (`nc`, `/dev/tcp`) → CRITICAL
- [ ] Credential access (`ssh`, `.env`, `password`) → CRITICAL
- [ ] Base64 encoding → MEDIUM (review context)

### Phase 5: Memory Poisoning Check

```bash
# Check for suspicious instructions in memory/config files
grep -in "ignore\|forget\|override\|disregard\|you are now\|new role\|system prompt" \
  CLAUDE.md .claude/CLAUDE.md SOUL.md .claude/SOUL.md MEMORY.md .claude/MEMORY.md \
  ~/.claude/CLAUDE.md ~/.claude/MEMORY.md 2>/dev/null
```

- [ ] Prompt injection patterns in CLAUDE.md / SOUL.md / MEMORY.md? → HIGH
- [ ] Instructions to disable security, skip reviews, or grant broad permissions? → CRITICAL

### Phase 6: Permissions & Settings

```bash
# Check settings
cat .claude/settings.json 2>/dev/null
cat ~/.claude/settings.json 2>/dev/null
```

- [ ] `permissions.deny` exists and covers `.env*`, `*.pem`, `*.key`, secrets? → MEDIUM if missing
- [ ] No wildcard `permissions.allow` for Bash or Write? → HIGH if present
- [ ] No `dangerouslySkipPermissions` or similar flags? → CRITICAL if present

### Phase 7: Exposed Secrets in Config

```bash
# Check for secrets in .claude/ directory
grep -rn "sk-[a-zA-Z0-9]\{20,\}\|sk-ant-[a-zA-Z0-9]\{20,\}\|ghp_[a-zA-Z0-9]\{36\}\|AKIA[A-Z0-9]\{16\}" \
  .claude/ ~/.claude/ 2>/dev/null

# Check for private keys
grep -rn "BEGIN.*PRIVATE KEY" .claude/ ~/.claude/ 2>/dev/null
```

- [ ] API keys or tokens in config files? → CRITICAL
- [ ] Private keys in config? → CRITICAL

## Output Format

```
## 🛡️ Security Check Report

**Date**: [timestamp]
**Scope**: Claude Code configuration

### Results Summary

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 CRITICAL | X | [PASS/FAIL] |
| 🟠 HIGH | X | [PASS/FAIL] |
| 🟡 MEDIUM | X | [PASS/FAIL] |
| 🟢 LOW | X | [PASS/FAIL] |

### 🔴 Critical Issues
[List each critical finding with location and fix]

### 🟠 High Issues
[List each high finding with location and fix]

### 🟡 Medium Issues
[List each medium finding with location and fix]

### ✅ Passed Checks
[List what passed, important for confidence]

### 🔧 Recommended Actions (Priority Order)
1. [Most urgent fix with exact command]
2. [Second priority]
3. [...]

### 📚 References
- Full security guide: guide/security/security-hardening.md
- Threat database: examples/skills/update-threat-db/threat-db.yaml
- MCP scan: `npx mcp-scan` (Snyk)
```

If ALL checks pass, output:

```
## 🛡️ Security Check Report: ALL CLEAR ✅

**Date**: [timestamp]
No known threats detected in your Claude Code configuration.

**Recommendations for continued security:**
- Re-run `/security-check` after installing new skills or MCP servers
- Run `/security-audit` for a comprehensive project + config audit
- Keep Claude Code updated (current security fixes in v2.1.34+)
```

$ARGUMENTS
