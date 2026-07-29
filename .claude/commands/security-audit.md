# Security Audit

Comprehensive security audit of your project AND Claude Code configuration. Analyzes secrets exposure, injection surfaces, dependencies, hook security, and produces a scored security posture assessment.

**Time**: 2-5 minutes | **Scope**: Full project + Claude Code config

> For a quick config-only check, use `/security-check` instead.

## Instructions

You are a senior application security engineer. Perform a 6-phase security audit and produce a scored report with prioritized remediation plan.

---

### Phase 1: Configuration Security (via /security-check)

Execute all checks from `/security-check` (the `examples/commands/security-check.md` command). This covers:
- MCP server audit against CVE database
- Skills & agents against known malicious entries
- Hook exfiltration patterns
- Memory poisoning detection
- Permissions & settings review
- Exposed secrets in Claude Code config

Record findings — they contribute to the final score.

---

### Phase 2: Project Secrets Scan

Scan the entire project for exposed secrets and credentials:

```bash
# API keys and tokens
grep -rn --include="*.{js,ts,py,go,java,rb,php,yaml,yml,json,toml,env,cfg,ini,conf}" \
  -E '(?i)(api[_-]?key|apikey|secret|password|passwd|token|bearer|auth)\s*[=:]\s*["'\''"][^"'\'']{8,}["'\''"]\s' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target,__pycache__,.venv} . 2>/dev/null | head -30

# Known provider key patterns
grep -rn -E 'sk-[a-zA-Z0-9]{20,}|sk-ant-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|AKIA[A-Z0-9]{16}|xox[bps]-[a-zA-Z0-9\-]{20,}' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target} . 2>/dev/null | head -20

# Private keys
grep -rn 'BEGIN.*PRIVATE KEY' --exclude-dir={node_modules,vendor,.git} . 2>/dev/null

# .env files that might be committed
find . -name ".env*" -not -path "*/node_modules/*" -not -path "*/.git/*" -type f 2>/dev/null

# Check .gitignore coverage
[ -f ".gitignore" ] && {
  grep -q "\.env" .gitignore && echo "✅ .env in .gitignore" || echo "⚠️ .env NOT in .gitignore"
  grep -q "\.pem" .gitignore && echo "✅ .pem in .gitignore" || echo "⚠️ .pem NOT in .gitignore"
  grep -q "\.key" .gitignore && echo "✅ .key in .gitignore" || echo "⚠️ .key NOT in .gitignore"
}
```

**Scoring:**
- 0 secrets found → +20 points
- 1-3 secrets → +10 points
- 4+ secrets → 0 points
- Private key committed → -10 points

---

### Phase 3: Prompt Injection Surface

Analyze markdown and config files for injection vectors:

```bash
# Zero-width characters (invisible instructions)
grep -rPn '[\x{200B}-\x{200D}\x{FEFF}]' --include="*.md" --include="*.yaml" --include="*.json" . 2>/dev/null

# Hidden HTML comments with instructions
grep -rn '<!--' --include="*.md" . 2>/dev/null | grep -i 'ignore\|system\|admin\|instruction\|override\|forget'

# Base64 in comments (potential hidden payloads)
grep -rn -E '[#;].*[A-Za-z0-9+/]{20,}={0,2}' --include="*.py" --include="*.js" --include="*.ts" --include="*.md" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10

# ANSI escape sequences
grep -rPn '\x1b\[|\x1b\]|\x1b\(' --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10

# Null bytes
grep -rPn '\x00' --exclude-dir={node_modules,vendor,.git,dist} . 2>/dev/null | head -5

# Nested command execution in markdown/config
grep -rn -E '\$\([^)]+\)|`[^`]+`' --include="*.md" --include="*.yaml" --include="*.json" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10
```

**Scoring:**
- 0 injection vectors → +15 points
- 1-2 vectors (likely false positives) → +10 points
- 3+ vectors → +5 points
- Confirmed injection in CLAUDE.md → 0 points

---

### Phase 4: Dependency Audit

Run the appropriate package audit for the project:

```bash
# Node.js
[ -f "package-lock.json" ] && npm audit --json 2>/dev/null | jq '{total: .metadata.vulnerabilities.total, critical: .metadata.vulnerabilities.critical, high: .metadata.vulnerabilities.high}' 2>/dev/null

# Python
[ -f "requirements.txt" ] && pip-audit -r requirements.txt 2>/dev/null || [ -f "pyproject.toml" ] && pip-audit 2>/dev/null

# Rust
[ -f "Cargo.toml" ] && cargo audit 2>/dev/null

# Go
[ -f "go.mod" ] && govulncheck ./... 2>/dev/null
```

If no package manager detected, note it and skip (no penalty).

**Scoring:**
- 0 vulnerabilities → +20 points
- 0 critical + 0 high → +15 points
- 1-3 high → +10 points
- Any critical → +5 points
- 10+ high or 3+ critical → 0 points

---

### Phase 5: Hook Security Assessment

Verify security hooks from `guide/security-hardening.md` are properly installed:

```bash
# Check for recommended security hooks
echo "=== Checking security hooks ==="

# PreToolUse hooks (should block dangerous patterns)
ls .claude/hooks/PreToolUse* 2>/dev/null || echo "⚠️ No PreToolUse hooks found"

# PostToolUse hooks (should monitor output)
ls .claude/hooks/PostToolUse* 2>/dev/null || echo "⚠️ No PostToolUse hooks found"

# Check if prompt injection detector exists
find . -path "*/hooks/*injection*" -o -path "*/hooks/*security*" -o -path "*/hooks/*scanner*" 2>/dev/null

# Check settings for hook configuration
grep -c "hooks" .claude/settings.json 2>/dev/null || echo "No hooks in settings.json"
```

**Scoring:**
- PreToolUse security hooks installed → +10 points
- PostToolUse output scanner installed → +5 points
- Prompt injection detector hook → +5 points
- No hooks at all → 0 points

---

### Phase 6: Posture Score & Report

Calculate total score and generate report.

**Scoring Breakdown:**

| Category | Max Points | Source |
|----------|-----------|--------|
| Config Security (Phase 1) | 30 | /security-check results |
| Secrets Scan (Phase 2) | 20 | Secrets found in project |
| Injection Surface (Phase 3) | 15 | Injection vectors found |
| Dependencies (Phase 4) | 20 | Vulnerability audit |
| Hook Security (Phase 5) | 15 | Security hooks installed |
| **Total** | **100** | |

**Phase 1 scoring detail:**
- 0 CRITICAL findings → +15 points
- 0 HIGH findings → +10 points
- 0 MEDIUM findings → +5 points
- Any CRITICAL → 0 for that sub-score

**Grade Scale:**

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Excellent — production-ready security posture |
| 75-89 | B | Good — minor improvements recommended |
| 60-74 | C | Acceptable — address HIGH issues before production |
| 40-59 | D | Poor — significant security gaps |
| 0-39 | F | Critical — do not deploy, address CRITICAL issues immediately |

## Output Format

```
## 🛡️ Security Audit Report

**Date**: [timestamp]
**Project**: [directory name]
**Scope**: Full project + Claude Code configuration

### Security Posture Score: [XX]/100 (Grade [X])

[1-sentence assessment]

### Phase Results

| Phase | Score | Max | Key Finding |
|-------|-------|-----|-------------|
| 1. Config Security | XX | 30 | [summary] |
| 2. Secrets Scan | XX | 20 | [summary] |
| 3. Injection Surface | XX | 15 | [summary] |
| 4. Dependencies | XX | 20 | [summary] |
| 5. Hook Security | XX | 15 | [summary] |
| **Total** | **XX** | **100** | |

### 🔴 Critical Findings
[Each finding with location, description, and exact fix]

### 🟠 High Findings
[Each finding with location, description, and fix]

### 🟡 Medium Findings
[Each finding with location, description, and fix]

### 🔧 Remediation Plan (Priority Order)

| # | Action | Severity | Effort | Command/Steps |
|---|--------|----------|--------|---------------|
| 1 | [action] | CRITICAL | [time] | [how] |
| 2 | [action] | HIGH | [time] | [how] |
| ... | | | | |

### 📊 Benchmark

Your score vs security-hardening.md recommendations:
- [X] items from the guide are implemented
- [X] items are missing
- Top 3 missing items to implement next: [...]

### 📚 References
- Security hardening guide: guide/security-hardening.md
- Threat database: examples/commands/resources/threat-db.yaml
- Quick check: `/security-check`
- MCP scan tool: `npx mcp-scan` (Snyk)
```

$ARGUMENTS
