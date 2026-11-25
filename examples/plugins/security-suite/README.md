# Security suite plugin

**Complete security hardening for Claude Code workflows in 5 minutes.**

This plugin bundles everything you need to secure your Claude Code setup: automated security scanning, pre-commit gates, threat tracking, compliance checks, and configuration audits.

## What's included

✓ **Security Auditor Agent**: Specialist for threat modeling and CVE analysis
✓ **Quick Security Check**: 30-second configuration scan
✓ **Full Security Audit**: 6-phase deep dive with score /100
✓ **Security Hooks**: PreToolUse checks that block risky code patterns and secrets in commands
✓ **Configuration Audits**: Verify agents, skills, and commands quality
✓ **Compliance Checklist**: A `security-checklist` skill for governance

## Quick install

```bash
# From a clone of this repository:
bash examples/plugins/security-suite/install.sh

# Verify installation:
/security-check
/security-audit
/audit-agents-skills
```

No external dependencies beyond `jq` for the hooks. The installer copies components from `examples/` into `.claude/` and never overwrites existing files.

## Components

### 1. Security auditor agent

Specialist agent focused exclusively on security analysis.

```bash
# Ask Claude to delegate:
Use the security-auditor agent to analyze this multi-agent setup for supply chain risks
```

**Capabilities:**
- CVE tracking and impact assessment
- Supply chain vulnerability detection
- MCP server security vetting
- Custom skill/hook risk analysis
- Compliance requirement mapping

### 2. Quick security check (`/security-check`)

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

### 3. Full security audit (`/security-audit`)

6-phase deep dive, 2-5 minutes. Comprehensive threat assessment.

```bash
/security-audit
```

**6 Phases:**
1. **Configuration Audit**: Settings, permissions, secrets
2. **Agent Security**: Tool restrictions, isolation, capabilities
3. **Skill/Hook Analysis**: Code quality, dangerous patterns
4. **MCP Vetting**: Server permissions, token handling
5. **Supply Chain**: Dependency analysis, external integrations
6. **Compliance Check**: Enterprise requirements, governance

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

### 4. Configuration audit (`/audit-agents-skills`)

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

### 5. Security hooks

Both hooks are `PreToolUse` hooks.

**`security-gate.sh`** (matcher `Write|Edit`) detects vulnerable code patterns before they are written to source files.

**`security-check.sh`** (matcher `Bash`) blocks commands that contain secrets.

See the header comment of each script for the exact patterns.

## Usage scenarios

### Scenario 1: Securing a team setup

```
1. Run: /security-audit
2. Review report and fix Critical issues
3. Run: /audit-agents-skills --fix
4. Share results with team
5. Monthly re-audits to track improvement
```

### Scenario 2: Evaluating a third-party skill

```
1. Copy the skill folder into `.claude/skills/`
2. Run: /audit-agents-skills
3. Review tool restrictions and code patterns
4. If safe, integrate; otherwise reject
```

### Scenario 3: Hardening for production

```
1. Run: /security-audit (current posture baseline)
2. Address all Critical issues
3. Read: guide/security/production-safety/
4. Implement recommended patterns
5. Re-audit until 90+ score achieved
```

### Scenario 4: Compliance verification

```
1. Run: /security-audit
2. Check Compliance phase (item 6)
3. Map gaps to regulatory requirements
4. Create compliance.md documenting adherence
5. Audit quarterly
```

## Configuration

### Hook enablement

The installer copies the scripts but does not register them. Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/bash/security-gate.sh",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/bash/security-check.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

## Learning path

**After installing:**

1. **Understand threats** → Read `guide/security/security-hardening/`
2. **Assess your setup** → Run `/security-check`
3. **Get detailed report** → Run `/security-audit`
4. **Fix issues** → Follow recommendations
5. **Deep dive** → Use `/self-assessment` to identify security knowledge gaps
6. **Verify** → Re-audit until you hit your target score (85+/100 recommended)

This bundle is a project-level installer, not a plugin package: `.claude-plugin/plugin.json` carries metadata only. To ship it as a real plugin, copy the components under the plugin root (`skills/<name>/SKILL.md`, `agents/<name>.md`, `hooks/hooks.json`) and run `claude plugin validate`.

## Uninstall

Delete the copied files from `.claude/` (agents, skills, hooks) and remove the hook entries from `settings.json`.

## Getting help

- **Questions?** → See `guide/security/` for threat patterns and mitigations
- **Specific audit questions?** → Use the Security Auditor agent
- **Need threat intelligence?** → Check `guide/core/known-issues/` for active CVEs
- **Team adoption?** → Run audit across team, aggregate results, identify common gaps

## Version

- **Bundle version:** 1.1.0

## License

CC BY-SA 4.0 — Use freely, modify as needed, share improvements.

---

**Ready to harden your setup?** Run `/security-check` now.
