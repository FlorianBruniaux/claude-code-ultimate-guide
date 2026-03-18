---
name: security
description: "Rapid security assessment focused on OWASP Top 10 vulnerabilities"
---

# Security Quick Audit

Rapid security assessment focused on OWASP Top 10 vulnerabilities.

## Purpose

Perform a quick security scan to identify common vulnerabilities:
- Hardcoded secrets and credentials
- SQL injection risks
- XSS vulnerabilities
- Insecure dependencies
- Authentication/authorization issues

## Instructions

### Step 1: Secrets Scan

```bash
# Common secret patterns
grep -rn --include="*.{js,ts,py,go,java,rb,php,env}" \
  -E "(password|secret|api_key|apikey|token|auth|credential).*[=:].*['\"][^'\"]{8,}['\"]" \
  --exclude-dir={node_modules,vendor,.git,dist,build} . 2>/dev/null | head -20

# .env files that might be committed
find . -name ".env*" -not -path "*/node_modules/*" -type f 2>/dev/null

# Check if secrets are gitignored
[ -f ".gitignore" ] && grep -q "\.env" .gitignore && echo "✅ .env in .gitignore" || echo "⚠️ .env NOT in .gitignore"
```

### Step 2: Injection Vulnerabilities

```bash
# SQL injection patterns (raw queries with string concat)
grep -rn --include="*.{js,ts,py,go,java,php}" \
  -E "(query|execute|raw|sql).*\+.*\$|f['\"].*SELECT|\.format\(.*SELECT" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -15

# Command injection patterns
grep -rn --include="*.{js,ts,py,go,rb,php}" \
  -E "(exec|spawn|system|shell_exec|popen)\s*\(" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -15
```

### Step 3: XSS Patterns

```bash
# Dangerous innerHTML/dangerouslySetInnerHTML usage
grep -rn --include="*.{js,ts,jsx,tsx,vue}" \
  -E "(innerHTML|dangerouslySetInnerHTML|v-html)" \
  --exclude-dir={node_modules,.git,dist} . 2>/dev/null | head -15

# Unescaped template literals in HTML context
grep -rn --include="*.{js,ts,jsx,tsx}" \
  -E "\`.*\$\{.*\}.*<" \
  --exclude-dir={node_modules,.git,dist} . 2>/dev/null | head -10
```

### Step 4: Dependency Check

```bash
# Check for known vulnerabilities in npm packages
[ -f "package-lock.json" ] && npm audit --json 2>/dev/null | jq '{vulnerabilities: .metadata.vulnerabilities}' 2>/dev/null

# Check for outdated packages with security issues
[ -f "package.json" ] && npm outdated --json 2>/dev/null | jq 'to_entries | map(select(.value.current != .value.latest)) | length' 2>/dev/null
```

### Step 5: Auth & Session Issues

```bash
# Hardcoded JWT secrets
grep -rn --include="*.{js,ts,py,go}" \
  -E "(jwt|JWT).*secret.*[=:].*['\"].{8,}['\"]" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null

# Missing CSRF protection patterns
grep -rn --include="*.{js,ts,py}" \
  -E "(POST|PUT|DELETE|PATCH).*fetch|axios\.(post|put|delete|patch)" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10
```

## Output Format

---

### 🛡️ Security Audit Report

**Scan Date**: [timestamp]
**Scope**: [directory scanned]

### 🔴 Critical Issues

| Issue | Location | Description |
|-------|----------|-------------|
| [type] | [file:line] | [brief description] |

### 🟠 High Severity

| Issue | Location | Recommendation |
|-------|----------|----------------|
| [type] | [file:line] | [fix suggestion] |

### 🟡 Medium Severity

| Issue | Location | Note |
|-------|----------|------|
| [type] | [file:line] | [context] |

### 📊 Summary

- **Critical**: X issues
- **High**: X issues
- **Medium**: X issues
- **Dependencies**: X vulnerabilities

### 🔧 Quick Fixes

1. [Highest priority fix with command/code]
2. [Second priority]
3. [Third priority]

---

## Severity Levels

| Level | Examples | Action |
|-------|----------|--------|
| 🔴 Critical | Hardcoded prod secrets, SQL injection | Fix immediately |
| 🟠 High | Missing auth, XSS vectors | Fix before deploy |
| 🟡 Medium | Outdated deps, missing CSRF | Plan remediation |
| 🟢 Low | Best practice violations | Track for improvement |

## Usage

**Full audit:**
```
/security
```

**Focus on specific area:**
```
/security auth
/security deps
/security injection
```

**Specific file/directory:**
```
/security src/api/
```

## Notes

- This is a quick heuristic scan, not a comprehensive security audit
- For production systems, complement with dedicated tools (Snyk, SonarQube, OWASP ZAP)
- False positives are possible - verify findings manually
- See `examples/hooks/security-hooks.sh` for automated pre-commit security checks

$ARGUMENTS
