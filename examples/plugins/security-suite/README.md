# Security Suite Plugin

**Complete security hardening for Claude Code workflows in 5 minutes.**

This plugin bundles everything you need to secure your Claude Code setup: automated security scanning, pre-commit gates, threat tracking, compliance checks, and configuration audits.

## What's Included

✓ **Security Auditor Agent** — Specialist for threat modeling and CVE analysis
✓ **Quick Security Check** — 30-second configuration scan
✓ **Full Security Audit** — 6-phase deep dive with score /100
✓ **Pre-Commit Security Gates** — Block dangerous operations before execution
✓ **Configuration Audits** — Verify agents, skills, commands quality
✓ **Compliance Templates** — Automated checklists for governance

## Quick Install

```bash
# From this directory:
bash install.sh

# Verify installation:
/security-check
/security-audit
/audit-agents-skills
```

**Time:** 5 minutes. No external dependencies.

## Components

### 1. Security Auditor Agent

Specialist agent focused exclusively on security analysis.

```bash
# Assign to a complex threat modeling task:
@security-auditor Analyze this multi-agent setup for supply chain risks
```

**Capabilities:**
- CVE tracking and impact assessment
- Supply chain vulnerability detection
- MCP server security vetting
- Custom skill/hook risk analysis
- Compliance requirement mapping

### 2. Quick Security Check (`/security-check`)

30-second scan. Run before commits or deployments.

```bash
/security-check
```

**What it checks:**
- ✓ CLAUDE.md isolation (no secrets exposed)
- ✓ MCP server configurations (dangerous permissions?)
- ✓ Hook execution scope (too permissive?)
- ✓ Agent tool restrictions (properly sandboxed?)
- ✓ Settings.json permissions (locked down?)

**Output:**
```
Security Check: 87/100 ✓ PASS
- Agents properly isolated ✓
- No dangerous MCP configs ⚠️ REVIEW: 1 issue
- Hooks validated ✓
- CLAUDE.md secure ✓
```

### 3. Full Security Audit (`/security-audit`)

6-phase deep dive, 2-5 minutes. Comprehensive threat assessment.

```bash
/security-audit
```

**6 Phases:**
1. **Configuration Audit** — Settings, permissions, secrets
2. **Agent Security** — Tool restrictions, isolation, capabilities
3. **Skill/Hook Analysis** — Code quality, dangerous patterns
4. **MCP Vetting** — Server permissions, token handling
5. **Supply Chain** — Dependency analysis, external integrations
6. **Compliance Check** — Enterprise requirements, governance

**Output:**
```
Security Audit Report
════════════════════════════════════════════
Config Audit:      ████░░░░░░  80/100
Agent Security:    ██████░░░░  85/100
Skill/Hook Review: ██░░░░░░░░  20/100  ⚠️ ACTION REQUIRED
MCP Vetting:       ███░░░░░░░  65/100  ⚠️ WARNINGS
Supply Chain:      ████░░░░░░  78/100
Compliance:        ██████░░░░  88/100

OVERALL: 72/100 — Intermediate Security Posture

Critical Issues (fix immediately):
  • 3 skills use eval() — Replace with safe parsing
  • GitHub MCP has write access to all repos — Scope to specific repos
  • Hook security-check.sh runs as root — Drop privileges

Warnings (fix within 2 weeks):
  • CLAUDE.md stores test API keys — Use environment variables
  • Agent tool permissions not clearly documented

Recommendations:
  • Read: guide/security/security-hardening/
  • Reference: guide/security/ for threat patterns
  • Use: /self-assessment → identify security gaps → take training
```

### 4. Configuration Audit (`/audit-agents-skills`)

Verify quality of your custom agents, skills, commands.

```bash
/audit-agents-skills
/audit-agents-skills --fix          # Get fix suggestions
/audit-agents-skills ~/other-dir    # Audit another project
```

**Checks:**
- ✓ Agents have proper tool restrictions
- ✓ Skills use correct frontmatter structure
- ✓ Commands have clear descriptions
- ✓ No hardcoded secrets or API keys
- ✓ All tool invocations are safe

### 5. Security Hooks

**Pre-commit Hook:** `security-gate.sh`
Blocks dangerous operations before they execute:
- Prevents `eval()` in custom code
- Stops secret exposure (API keys, tokens)
- Validates hook syntax
- Checks for command injection patterns

**Post-execution Hook:** `security-check.sh`
Validates outputs for security issues:
- Detects accidental secret exposure
- Checks for path traversal attempts
- Monitors resource usage (DoS detection)
- Flags dangerous patterns

## Usage Scenarios

### Scenario 1: Securing a Team Setup

```
1. Run: /security-audit
2. Review report and fix Critical issues
3. Run: /audit-agents-skills --fix
4. Share results with team
5. Monthly re-audits to track improvement
```

### Scenario 2: Evaluating a Third-Party Skill

```
1. Download skill to examples/skills/
2. Run: /audit-agents-skills
3. Review tool restrictions and code patterns
4. If safe, integrate; otherwise reject
```

### Scenario 3: Hardening for Production

```
1. Run: /security-audit (current posture baseline)
2. Address all Critical issues
3. Read: guide/security/production-safety/
4. Implement recommended patterns
5. Re-audit until 90+ score achieved
```

### Scenario 4: Compliance Verification

```
1. Run: /security-audit
2. Check Compliance phase (item 6)
3. Map gaps to regulatory requirements
4. Create compliance.md documenting adherence
5. Audit quarterly
```

## Configuration

### Hook Enablement

If hooks don't auto-enable, add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/bash/security-gate.sh",
            "timeout": 3000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/bash/security-check.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

### Environment Variables

Configure security parameters:

```bash
# Maximum tool timeouts (prevent DoS)
export CLAUDE_SECURITY_TIMEOUT=30000

# Enable strict mode (block all unreviewed code)
export CLAUDE_SECURITY_STRICT=true

# Security audit level (quick|standard|paranoid)
export CLAUDE_SECURITY_LEVEL=standard
```

## Learning Path

**After installing:**

1. **Understand threats** → Read `guide/security/security-hardening/`
2. **Assess your setup** → Run `/security-check`
3. **Get detailed report** → Run `/security-audit`
4. **Fix issues** → Follow recommendations
5. **Deep dive** → Use `/self-assessment` to identify security knowledge gaps
6. **Verify** → Re-audit until you hit your target score (85+/100 recommended)

## Uninstall

```bash
bash uninstall.sh
```

This removes all Security Suite components but preserves your backups (`.bak` files).

## Getting Help

- **Questions?** → See `guide/security/` for threat patterns and mitigations
- **Specific audit questions?** → Use the Security Auditor agent
- **Need threat intelligence?** → Check `guide/core/known-issues/` for active CVEs
- **Team adoption?** → Run audit across team, aggregate results, identify common gaps

## Version

- **Plugin Version:** 1.0.0
- **Requires:** Claude Code 2.1.0+
- **Compatible Models:** Opus 5, Sonnet 5, Haiku 4.5

## License

CC BY-SA 4.0 — Use freely, modify as needed, share improvements.

---

**Ready to harden your setup?** Run `/security-check` now.
