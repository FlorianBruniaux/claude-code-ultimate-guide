---
title: "Enterprise AI Governance for Claude Code"
description: "Org-level governance for teams deploying Claude Code at scale: usage charters, MCP approval workflows, guardrail tiers, and compliance"
tags: [security, enterprise, governance, compliance]
---

# Enterprise AI Governance for Claude Code

> **Audience**: Tech leads, engineering managers, security officers deploying Claude Code across teams.
>
> **Scope**: Org-level governance (policies, approval workflows, tiers, compliance). For individual dev security (injection defense, MCP vetting, CVEs), see [security-hardening.md](./security-hardening.md). For the 6 non-negotiable production rules, see [production-safety.md](./production-safety.md).

---

## TL;DR

**The governance gap**: Claude Code security docs cover what individual devs should do. They don't cover what happens when your entire organization is using it — 50 developers, different risk profiles, no shared policy.

**What this covers**:

| Section | What it gives you |
|---------|------------------|
| [Local vs Shared](#1-local-vs-shared-the-governance-split) | Risk matrix + decision framework |
| [Usage Charter](#2-ai-usage-charter) | Lean template, ready to adapt |
| [MCP Governance](#3-mcp-governance-workflow) | Approval workflow + YAML registry |
| [Guardrail Tiers](#4-guardrail-tiers) | 4 pre-configured tiers, copy-paste settings.json |
| [Policy at Scale](#5-policy-enforcement-at-scale) | Rollout, onboarding, CI/CD gates |
| [Audit & Compliance](#6-audit-compliance--governance-structure) | What SOC2/ISO27001 auditors actually ask |

---

## 1. Local vs Shared: The Governance Split

The biggest mistake in enterprise AI governance is applying the same rules to everything. Local usage and shared usage have fundamentally different risk profiles.

### 1.1 Risk Matrix

| Dimension | Local usage | Shared usage |
|-----------|-------------|--------------|
| **Data exposure** | Developer's own files | Customer data, shared codebases, secrets |
| **Blast radius** | One machine | Entire repo, CI/CD, production |
| **Accountability** | Individual | Team / org |
| **Reproducibility** | Session ends, history gone | Needs audit trail |
| **Compliance scope** | Usually none | SOC2, ISO27001, HIPAA (if applicable) |
| **Config drift** | Personal preference | Team consistency matters |

### 1.2 What You Can and Can't Control

**You CAN control** (via committed config):
- Which MCP servers are approved (`settings.json` in repo)
- Which tools Claude can use (`permissions.deny`)
- What CLAUDE.md says about project conventions
- Hook scripts that run pre/post tool use
- CI/CD gates that validate AI-generated code

**You CANNOT directly control**:
- Which personal `~/.claude/settings.json` developers have
- Which models they use on personal API keys
- What they do in personal projects outside your repos
- Memory / session content between sessions

**The practical implication**: Focus governance on what's committed to your repos and deployed in shared environments. Personal dev workflow is the developer's responsibility.

### 1.3 Decision Framework: When to Govern

Not everything needs heavy governance. Apply controls proportionally.

```
What are you governing?
│
├─ Personal dev workflow (local, throwaway code)
│   └─ Minimal: CLAUDE.md guidelines + basic hooks
│
├─ Team codebase (shared repo, not production)
│   └─ Standard: shared settings.json + MCP registry + PR gates
│
├─ Production system (customer-facing, real data)
│   └─ Strict: full tier config + approval workflow + audit log
│
└─ Regulated environment (HIPAA, SOC2, PCI, finance)
    └─ Regulated: all of above + compliance audit trail
```

---

## 2. AI Usage Charter

A usage charter answers the fundamental question: "What are we allowed to do with Claude Code at this company?" Without it, each team answers differently, creating inconsistent risk exposure.

This is the lean version. For a full charter with legal considerations, see [Whitepaper #11: Enterprise AI Governance](../../whitepapers/en/11-enterprise-ai-governance.qmd) (when available).

### 2.1 Lean Charter Template

Copy this into your org's `docs/ai-usage-charter.md` and adapt:

```markdown
# AI Coding Tools Usage Charter

**Applies to**: Claude Code (and any AI coding assistant)
**Effective date**: [DATE]
**Owner**: Engineering Lead / CTO
**Review cadence**: Quarterly

---

## Approved Tools

| Tool | Scope | Data Classification |
|------|-------|---------------------|
| Claude Code (Pro/Team/Enterprise) | All dev work | Up to CONFIDENTIAL |
| Claude Code (personal accounts) | Personal dev only | PUBLIC/INTERNAL only |
| [Other approved tools] | [Scope] | [Classification] |

---

## Data Classification Rules

| Classification | Examples | Allowed with Claude Code? |
|----------------|----------|--------------------------|
| **PUBLIC** | Open source, public docs | Yes, no restrictions |
| **INTERNAL** | Internal tools, non-sensitive code | Yes, standard config |
| **CONFIDENTIAL** | Internal business secrets, non-regulated IP | Yes, Enterprise plan only |
| **RESTRICTED** | Customer PII, PCI card data, PHI, credentials | No — never in AI context without legal/compliance sign-off |

**Hard rule**: RESTRICTED data never enters an AI context window. Not in prompts, not in files Claude reads, not as examples. Configure `permissions.deny` to block access to restricted files.

---

## Approved Use Cases

- Code completion, review, refactoring
- Test generation
- Documentation drafting
- Debugging and root cause analysis
- Architecture analysis (internal systems only)
- CLI scripting and automation

---

## Prohibited Use Cases

- Processing payment card data (PCI scope)
- Generating code that handles raw PHI without security review
- Autonomous deployment to production without human approval
- Using personal AI accounts for CONFIDENTIAL or higher data
- Sharing customer data in prompts as examples

---

## Who Approves What

| Action | Approver |
|--------|---------|
| Add new MCP server to team config | Tech Lead + Security review |
| Enable Claude Code in new project | Team Lead |
| Use Enterprise features (Zero Trust, SSO) | IT/Security team |
| Exception to any charter rule | Engineering Director |

---

## Compliance Obligations

By using Claude Code on company systems, you agree to:
1. Follow this charter
2. Report suspected data exposure to security@[company] within 24h
3. Not circumvent governance controls (hooks, permission deny rules)
4. Participate in quarterly access reviews

---

**Charter violations**: Follow standard disciplinary process. First occurrence: coaching. Repeated or severe: escalation.
```

### 2.2 Data Classification and Claude Code Settings

Translate data classification into actual configuration:

```json
{
  "permissions": {
    "deny": [
      "Read(./**/*.pem)",
      "Read(./**/*.key)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(**/credentials*)",
      "Bash(cat .env*)",
      "Bash(printenv*)",
      "Bash(env)"
    ]
  }
}
```

```markdown
<!-- CLAUDE.md — data handling rules -->
## Data Handling

**NEVER** read, reference, or include in output:
- Files matching: .env, *.pem, *.key, credentials.*, secrets/
- Customer PII fields (fields named: email, phone, ssn, dob, card_*)
- Credentials or API keys (even masked/redacted examples)

If you encounter restricted data while reading a file, stop and inform the user.
Do not proceed until explicitly told to skip that content.
```

---

## 3. MCP Governance Workflow

Individual MCP vetting (the 5-minute audit) is covered in [security-hardening.md §1.1](./security-hardening.md#11-mcp-vetting-workflow). This section covers the organizational workflow: how new MCPs get approved, deployed, and monitored across your team.

### 3.1 Approval Workflow

```
Developer wants new MCP
        │
        ▼
[1] Submit MCP Request
    - Name, source URL, version
    - Proposed use case
    - Data scope (what will it access?)
        │
        ▼
[2] Security Review (Tech Lead + optionally Security team)
    - 5-min MCP audit (see security-hardening.md)
    - Check: Stars >50, recent commits, no dangerous flags
    - Check: No CVEs (search NVD + GitHub security advisories)
    - Classify risk: LOW / MEDIUM / HIGH
        │
     ┌──┴──┐
   LOW   MED/HIGH
     │      │
     ▼      ▼
  Approve  Extended review
           (2-week trial in sandbox)
           + approval from Security team
        │
        ▼
[3] Add to Approved Registry
    - Pin exact version
    - Document approved scope
    - Set expiry date (6 months)
        │
        ▼
[4] Deploy via shared settings.json
    - Committed to repo
    - No local overrides for approved MCPs
        │
        ▼
[5] Monitor + Periodic Re-review
    - Check for security advisories every 30 days
    - Re-approve at version bumps (patch: auto, minor+: manual)
    - Quarterly full registry review
```

### 3.2 MCP Registry Format

Maintain an approved MCP registry at `.claude/mcp-registry.yaml` in your team's shared config repo:

```yaml
# .claude/mcp-registry.yaml
# Approved MCP servers for [Organization Name]
# Last updated: 2026-03-10
# Reviewer: [Name, Role]

metadata:
  review_cycle: quarterly
  next_review: "2026-06-10"
  owner: "platform-team@company.com"

approved:
  - name: context7
    version: "1.2.3"
    source: "https://github.com/context7/mcp-server"
    approved_by: "john.doe@company.com"
    approved_date: "2026-01-15"
    expires: "2026-07-15"
    data_scope: PUBLIC
    risk: LOW
    rationale: "Read-only documentation lookup. No data egress."
    config:
      command: npx
      args: ["-y", "@context7/mcp-server@1.2.3"]

  - name: sequential-thinking
    version: "0.6.2"
    source: "https://github.com/modelcontextprotocol/servers"
    approved_by: "jane.smith@company.com"
    approved_date: "2026-01-15"
    expires: "2026-07-15"
    data_scope: INTERNAL
    risk: LOW
    rationale: "Local reasoning only. No network access."
    config:
      command: npx
      args: ["-y", "@modelcontextprotocol/server-sequential-thinking@0.6.2"]

  - name: internal-db-readonly
    version: "2.1.0"
    source: "internal"
    approved_by: "security@company.com"
    approved_date: "2026-02-01"
    expires: "2026-05-01"  # shorter expiry for higher risk
    data_scope: CONFIDENTIAL
    risk: MEDIUM
    rationale: "Read-only replica access. No PII tables in allowlist."
    restrictions:
      - "Read-only credentials only"
      - "No access to users, payments, or audit tables"
    config:
      command: npx
      args: ["-y", "@company/db-mcp@2.1.0"]

pending_review:
  - name: github-mcp
    requested_by: "dev@company.com"
    requested_date: "2026-03-05"
    use_case: "PR automation"
    status: under_review

denied:
  - name: browser-automation-mcp
    denied_date: "2026-02-10"
    reason: "Full browser access with no scope restriction. Risk too high."
```

### 3.3 Enforcing the Registry via Hook

Use a governance hook to validate that only approved MCPs are in use. The script below is a minimal inline version you can drop into `.claude/hooks/governance-check.sh`. For a more complete implementation with additional checks (deny list enforcement, dangerous allow-list detection), see [`examples/hooks/bash/governance-enforcement-hook.sh`](../../examples/hooks/bash/governance-enforcement-hook.sh).

```bash
#!/bin/bash
# .claude/hooks/governance-check.sh
# Event: SessionStart
# Validates active MCP config against approved registry

REGISTRY=".claude/mcp-registry.yaml"
SETTINGS="${HOME}/.claude.json"

if [[ ! -f "$REGISTRY" ]]; then
  exit 0  # No registry = no enforcement (opt-in governance)
fi

# Check for unapproved MCPs (requires yq and jq)
if command -v jq &>/dev/null && command -v yq &>/dev/null; then
  ACTIVE=$(jq -r '.mcpServers | keys[]' "$SETTINGS" 2>/dev/null)
  APPROVED=$(yq e '.approved[].name' "$REGISTRY" 2>/dev/null)

  for mcp in $ACTIVE; do
    if ! echo "$APPROVED" | grep -q "^${mcp}$"; then
      echo "GOVERNANCE WARNING: MCP '${mcp}' is not in approved registry."
      echo "Submit a request at: https://your-internal-wiki/mcp-requests"
      echo "Session continues — please remediate within 48 hours."
    fi
  done
fi

exit 0
```

**Note**: This hook warns, it does not block. Blocking at session start creates too much friction. Use periodic compliance checks instead (see §5.3).

---

## 4. Guardrail Tiers

Pre-configured guardrail tiers for four common scenarios. Copy the relevant tier into your project's `.claude/settings.json` and `CLAUDE.md`.

### Tier 1: Starter

**When**: Small team (<5), internal projects, no production data, low compliance requirements.

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./**/*.key)",
      "Read(./**/*.pem)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": ["~/.claude/hooks/dangerous-actions-blocker.sh"]
      }
    ]
  }
}
```

```markdown
<!-- CLAUDE.md additions — Starter tier -->
## Security Basics
- Never read .env files or credential files
- Ask before running destructive commands (DROP, DELETE, rm -rf)
- Follow the codebase's existing patterns
```

**Investment**: 10 minutes setup. Covers basics.

### Tier 2: Standard

**When**: Team 5–20, production-adjacent code, some sensitive data, no hard compliance requirements.

{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./**/*.key)",
      "Read(./**/*.pem)",
      "Read(./secrets/**)",
      "Bash(cat .env*)",
      "Bash(printenv*)",
      "Edit(docker-compose.yml)",
      "Edit(.github/workflows/**)",
      "Edit(terraform/**)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          "~/.claude/hooks/dangerous-actions-blocker.sh"
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [".claude/hooks/prompt-injection-detector.sh"]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": ["~/.claude/hooks/output-secrets-scanner.sh"]
      }
    ],
    "SessionStart": [
      ".claude/hooks/governance-check.sh"
    ]
  }
}
```

```markdown
<!-- CLAUDE.md additions — Standard tier -->
## Production Safety
- Infrastructure files (docker-compose, terraform, CI/CD) are locked.
  Request permission before modifying.
- New dependencies require Tech Lead approval. Do not run npm install <pkg>.
- Database destructive operations (DROP, DELETE, TRUNCATE) require backup confirmation.

## Code Review Gate
- All AI-generated code touching auth, payments, or data access must be flagged
  with a "AI-generated: review required" comment in the PR description.
```

**Investment**: 30–45 minutes setup. Covers most teams.

### Tier 3: Strict

**When**: Team 20+, production-critical systems, customer data, informal compliance expectations.

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./.env.local)",
      "Read(./**/*.key)",
      "Read(./**/*.pem)",
      "Read(./secrets/**)",
      "Read(**/credentials*)",
      "Bash(cat .env*)",
      "Bash(printenv*)",
      "Bash(env)",
      "Bash(npm install *)",
      "Bash(pnpm add *)",
      "Bash(pip install *)",
      "Edit(docker-compose.yml)",
      "Edit(docker-compose.prod.yml)",
      "Edit(.github/workflows/**)",
      "Edit(terraform/**)",
      "Edit(kubernetes/**)",
      "Edit(prisma/schema.prisma)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          "~/.claude/hooks/dangerous-actions-blocker.sh",
          "~/.claude/hooks/velocity-governor.sh"
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          ".claude/hooks/prompt-injection-detector.sh",
          ".claude/hooks/unicode-injection-scanner.sh"
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": ["~/.claude/hooks/output-secrets-scanner.sh"]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [".claude/hooks/session-logger.sh"]
      }
    ],
    "SessionStart": [
      ".claude/hooks/governance-check.sh",
      "~/.claude/hooks/mcp-config-integrity.sh"
    ]
  }
}
```

```markdown
<!-- CLAUDE.md additions — Strict tier -->
## Security Posture: STRICT

You are operating in a strict security environment. Follow these rules without exception.

### Locked Files
These files cannot be modified without explicit permission in this conversation:
- docker-compose.yml, Dockerfile, .github/workflows/**, terraform/**, kubernetes/**
- prisma/schema.prisma (database schema)
- Any file in /src/auth/, /src/payments/, /src/crypto/

### Dependency Protocol
Before adding any dependency:
1. State the dependency name and purpose
2. List 2+ alternatives considered
3. Wait for explicit approval before running any install command

### Data Access Protocol
Before reading any file not in the project root:
1. State the file path and why you need it
2. Wait for approval if the path looks sensitive

### AI Attribution
All code blocks you generate must be prefixed with `// AI-generated` in PRs.
Tests generated by AI must include `// AI-generated test` comment.
```

**Investment**: 1–2 hours setup. Suitable for most production teams.

### Tier 4: Regulated

**When**: Finance, healthcare, regulated industries. HIPAA, SOC2, PCI, ISO27001 compliance required.

This tier adds compliance-specific controls on top of Strict.

```json
{
  "permissions": {
    "deny": [
      "Read(./.env*)",
      "Read(./**/*.key)",
      "Read(./**/*.pem)",
      "Read(./secrets/**)",
      "Read(**/credentials*)",
      "Read(**/patient*)",
      "Read(**/phi*)",
      "Read(**/pii*)",
      "Read(**/card*)",
      "Read(**/ssn*)",
      "Bash(cat .env*)",
      "Bash(printenv*)",
      "Bash(env)",
      "Bash(npm install *)",
      "Bash(pnpm add *)",
      "Bash(pip install *)",
      "Bash(curl *)",
      "Bash(wget *)",
      "Edit(docker-compose*.yml)",
      "Edit(.github/workflows/**)",
      "Edit(terraform/**)",
      "Edit(kubernetes/**)",
      "Edit(prisma/schema.prisma)",
      "Edit(**/auth/**)",
      "Edit(**/crypto/**)",
      "Edit(**/encryption/**)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          "~/.claude/hooks/dangerous-actions-blocker.sh",
          "~/.claude/hooks/velocity-governor.sh"
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          ".claude/hooks/prompt-injection-detector.sh",
          ".claude/hooks/unicode-injection-scanner.sh"
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          "~/.claude/hooks/output-secrets-scanner.sh",
          ".claude/hooks/session-logger.sh"
        ]
      }
    ],
    "SessionStart": [
      ".claude/hooks/governance-check.sh",
      "~/.claude/hooks/mcp-config-integrity.sh"
    ]
  }
}
```

```markdown
<!-- CLAUDE.md additions — Regulated tier -->
## Compliance Mode: [HIPAA | SOC2 | PCI] — ACTIVE

You are operating under regulatory compliance requirements. These rules are non-negotiable.

### Prohibited Data
NEVER include in your output, suggestions, or examples:
- PHI (patient health information), PII (names, emails, phones in customer context)
- Card numbers, CVVs, bank accounts
- SSNs, tax IDs, government IDs
- Raw authentication tokens, session cookies, API keys

### Mandatory Review Gates
These changes require human approval BEFORE code is committed:
- Any change to authentication or authorization logic
- Any change to encryption or key management
- Any database migration
- Any new external API integration

### Audit Trail
Every session operating on regulated data must have:
- User ID noted at session start ("This session is for: [your-email]")
- Task description at session start ("Task: [brief description]")
- Checkpoint comment at natural breakpoints

### AI Attribution (Mandatory for Regulated)
All AI-generated code must include:
- `// AI-generated: [date] [model] [reviewer]` comment
- PR description must include AI disclosure section
```

**Additional tool for regulated environments**: Consider Entire CLI for full session audit trails with approval gates. See [AI Traceability §5.1](../ops/ai-traceability.md#51-entire-cli) for details and a go/no-go evaluation checklist.

---

## 5. Policy Enforcement at Scale

Having a policy is not the same as enforcing it. This section covers how to actually get governance to stick across a team of 10–100 developers.

### 5.1 Config Distribution

**The core principle**: Governance config lives in the repo, not on individual machines.

```
your-org-config/                 ← separate "platform config" repo
├── .claude/
│   ├── settings.json            ← shared settings (tier-based)
│   ├── mcp-registry.yaml        ← approved MCPs
│   ├── hooks/
│   │   ├── governance-check.sh  ← MCP registry check
│   │   ├── session-logger.sh    ← audit trail
│   │   └── velocity-governor.sh ← rate limiting
│   └── agents/
│       └── security-reviewer.md ← shared agent for code review
├── templates/
│   ├── CLAUDE.md.starter        ← per-tier CLAUDE.md templates
│   ├── CLAUDE.md.standard
│   ├── CLAUDE.md.strict
│   └── CLAUDE.md.regulated
└── scripts/
    └── setup-project.sh         ← bootstraps new project with correct tier
```

**Bootstrapping a new project**:

```bash
#!/bin/bash
# scripts/setup-project.sh
# Usage: ./setup-project.sh [starter|standard|strict|regulated]

TIER=${1:-standard}
CONFIG_REPO="https://github.com/your-org/claude-code-config"

echo "Setting up Claude Code governance: $TIER tier"

# Create .claude directory
mkdir -p .claude/hooks

# Copy tier config
curl -s "$CONFIG_REPO/raw/main/templates/.claude/settings.${TIER}.json" \
  -o .claude/settings.json

# Copy CLAUDE.md template
curl -s "$CONFIG_REPO/raw/main/templates/CLAUDE.md.${TIER}" \
  -o CLAUDE.md

# Copy governance hooks
curl -s "$CONFIG_REPO/raw/main/hooks/governance-check.sh" \
  -o .claude/hooks/governance-check.sh
chmod +x .claude/hooks/governance-check.sh

echo "Done. Commit .claude/ and CLAUDE.md to your repo."
```

### 5.2 Onboarding Checklist

New developer joining a team that uses Claude Code should complete this checklist:

```markdown
## Claude Code Onboarding Checklist

### Setup (30 minutes)
- [ ] Install Claude Code: `npm i -g @anthropic-ai/claude-code`
- [ ] Configure global safety hooks: `./scripts/install-global-hooks.sh`
- [ ] Verify project config loads: `claude` then ask "What tier is this project?"
- [ ] Read the AI Usage Charter (link to your doc)
- [ ] Review approved MCP list: `.claude/mcp-registry.yaml`

### Security Basics
- [ ] Confirm `~/.claude/settings.json` has no `permissions.allow` overrides
  that bypass project's deny rules
- [ ] Confirm no personal MCP servers running that access production data
- [ ] Know how to report a data exposure: security@[company]

### First Week
- [ ] Complete one task with Claude Code (bug fix, small feature)
- [ ] Submit at least one PR with proper AI attribution section
- [ ] Flag any friction points to Tech Lead for config improvement

### Quarterly
- [ ] Participate in MCP registry review
- [ ] Review AI Usage Charter updates
- [ ] Confirm no personal config overrides in place
```

### 5.3 Compliance Checking

Automated periodic compliance check to detect configuration drift:

```bash
#!/bin/bash
# scripts/claude-governance-audit.sh
# Run weekly via CI/CD or cron

PASS=0
FAIL=0
WARN=0

check() {
  local name="$1"
  local result="$2"
  local severity="${3:-FAIL}"

  if [[ "$result" == "OK" ]]; then
    echo "  PASS: $name"
    ((PASS++))
  else
    echo "  $severity: $name — $result"
    [[ "$severity" == "FAIL" ]] && ((FAIL++)) || ((WARN++))
  fi
}

echo "=== Claude Code Governance Audit ==="
echo ""

# Check: settings.json present and committed
echo "1. Repository Config"
[[ -f ".claude/settings.json" ]] \
  && check "settings.json present" "OK" \
  || check "settings.json present" "Missing — team config not enforced" "FAIL"

git ls-files --error-unmatch .claude/settings.json &>/dev/null \
  && check "settings.json committed" "OK" \
  || check "settings.json committed" "Not tracked by git — won't apply to team" "WARN"

# Check: deny rules for secrets
echo ""
echo "2. Secret Protection"
if [[ -f ".claude/settings.json" ]]; then
  jq -e '.permissions.deny[]? | select(test("env|pem|key"))' \
    .claude/settings.json &>/dev/null \
    && check ".env protection rules" "OK" \
    || check ".env protection rules" "No deny rules for .env or key files" "FAIL"
fi

# Check: hooks installed and executable
echo ""
echo "3. Hook Stack"
for hook in ".claude/hooks/governance-check.sh"; do
  if [[ -f "$hook" ]]; then
    [[ -x "$hook" ]] \
      && check "$hook executable" "OK" \
      || check "$hook executable" "Not executable — run chmod +x $hook" "FAIL"
  else
    check "$hook present" "Missing" "WARN"
  fi
done

# Check: MCP registry present
echo ""
echo "4. MCP Governance"
[[ -f ".claude/mcp-registry.yaml" ]] \
  && check "MCP registry present" "OK" \
  || check "MCP registry present" "No registry — MCP usage ungoverned" "WARN"

# Check: CLAUDE.md present and committed
echo ""
echo "5. Documentation"
[[ -f "CLAUDE.md" ]] || [[ -f ".claude/CLAUDE.md" ]] \
  && check "CLAUDE.md present" "OK" \
  || check "CLAUDE.md present" "Missing — no project context for AI" "WARN"

echo ""
echo "=== Summary ==="
echo "  Passed:   $PASS"
echo "  Failed:   $FAIL (must fix)"
echo "  Warnings: $WARN (should fix)"
echo ""

[[ $FAIL -gt 0 ]] && exit 1 || exit 0
```

### 5.4 Role-Based Guardrails

Different developers have different risk profiles. Tailor Claude Code settings accordingly.

**Approach: tier by experience/role in CLAUDE.md**

```markdown
<!-- CLAUDE.md — role-aware guidelines -->
## Developer Context

This is a [JUNIOR|SENIOR|LEAD] developer project context.

### If JUNIOR (< 1 year at company)
- Always confirm architecture decisions before implementing
- Do not modify database schemas, migrations, or auth code without pairing with a senior
- Every PR must have a human reviewer check the AI-generated sections explicitly
- Use /plan mode before implementing anything > 50 lines

### If SENIOR (1+ years at company)
- Standard review applies
- Can modify most files, but auth/payment/crypto still require lead review
- AI attribution in PRs required

### If LEAD/PRINCIPAL
- Full access, judgment-based restrictions
- Responsible for setting guardrail tier for their team projects
- Must conduct quarterly MCP registry review
```

**Approach: different settings.json per environment**

In CI/CD, check the active `settings.json` path at pipeline start to enforce the correct tier. Claude Code reads `.claude/settings.json` from the project root — commit your strict-tier config there so CI always picks it up, regardless of what developers have locally.

```bash
# In your CI pipeline setup step, verify the correct tier is committed
if ! grep -q '"Bash(curl \*)"' .claude/settings.json; then
  echo "ERROR: CI requires Regulated-tier settings.json (curl must be denied)"
  exit 1
fi
```

### 5.5 CI/CD Gates

Block non-compliant AI usage from reaching production:

```yaml
# .github/workflows/ai-governance.yml
name: AI Governance Check

on: [pull_request]

jobs:
  governance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check governance config present
        run: |
          if [[ ! -f ".claude/settings.json" ]]; then
            echo "::error::Missing .claude/settings.json — governance config required"
            exit 1
          fi

      - name: Check no credential access permissions
        run: |
          if jq -e '.permissions.allow[]? | select(test("env|pem|key|secret"))' \
            .claude/settings.json 2>/dev/null; then
            echo "::error::Dangerous permissions.allow detected — credentials may be exposed"
            exit 1
          fi

      - name: Run governance audit
        run: |
          chmod +x scripts/claude-governance-audit.sh
          ./scripts/claude-governance-audit.sh

      - name: Check AI attribution in PR description
        if: ${{ env.REQUIRE_AI_ATTRIBUTION == 'true' }}
        uses: actions/github-script@v7
        with:
          script: |
            const body = context.payload.pull_request.body || '';
            const hasAttribution = body.includes('AI') ||
                                   body.includes('Claude') ||
                                   body.includes('AI-generated');
            if (!hasAttribution) {
              core.warning('No AI attribution section found. Please disclose AI usage.');
            }
```

---

## 6. Audit, Compliance & Governance Structure

### 6.1 What SOC2 and ISO27001 Auditors Actually Ask

When auditors review AI coding tool usage, they typically look for evidence of these controls:

| Auditor question | What they want to see | Claude Code implementation |
|-----------------|----------------------|---------------------------|
| "Do you have a policy for AI tool usage?" | Written charter, signed/acknowledged | `docs/ai-usage-charter.md` + onboarding checklist |
| "How do you control data sent to AI vendors?" | Data classification + technical controls | `permissions.deny` for sensitive files |
| "How do you vet third-party AI components?" | Approval workflow + registry | MCP registry + approval process |
| "Do you have an audit trail of AI actions?" | Log of tool calls, files accessed | Session JSONL logs + `compliance-audit-logger.sh` |
| "How do you review AI-generated code?" | Code review process with AI disclosure | PR template + attribution policy |
| "What happens when an incident occurs?" | Incident response procedure | Existing IR process + AI-specific additions |

**For SOC2 specifically**: The relevant Trust Services Criteria are CC6.1 (logical access controls), CC6.3 (access removal), CC7.1 (monitoring), and CC9.2 (vendor risk). Your Claude Code governance should map to these.

**For ISO27001 specifically**: Relevant Annex A controls include A.8.3 (information access restriction), A.8.24 (use of cryptography), A.8.25 (secure development lifecycle), and A.5.23 (information security for use of cloud services).

### 6.2 Audit Trail Setup

Claude Code sessions are already logged to `~/.claude/projects/<project>/*.jsonl`. The challenge is making them:
1. Accessible after the fact (not lost when developer leaves)
2. Tamper-evident (can't be retroactively edited)
3. Queryable for audit purposes

**Minimal audit trail (no additional tools)**:

```bash
#!/bin/bash
# .claude/hooks/compliance-audit-logger.sh
# Event: PostToolUse (all tools)
# Appends structured audit entries to a shared log

LOG_DIR="${COMPLIANCE_LOG_DIR:-/var/log/claude-audit}"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).jsonl"

mkdir -p "$LOG_DIR"

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool.name // "unknown"')
USER=$(whoami)
PROJECT=$(basename "$PWD")
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "{\"timestamp\":\"$TIMESTAMP\",\"user\":\"$USER\",\"project\":\"$PROJECT\",\"tool\":\"$TOOL\"}" \
  >> "$LOG_FILE"
```

**Shipping logs to immutable storage** (recommended for regulated environments):

```bash
# Daily: sync session logs to immutable bucket
aws s3 sync ~/.claude/projects/ \
  s3://your-audit-bucket/claude-sessions/$(whoami)/ \
  --storage-class GLACIER_INSTANT_RETRIEVAL \
  --exclude "*.tmp"
```

**For full compliance audit trails with approval gates**, consider Entire CLI — it captures complete session context (prompts, reasoning, tool calls, file diffs) with cryptographic linking to git commits. See [AI Traceability §5.1](../ops/ai-traceability.md#51-entire-cli) for setup and evaluation criteria. This is one tool among several options; evaluate against your specific compliance requirements.

### 6.3 AI Governance Committee (Compact Reference)

For organizations managing AI risk at scale, a lightweight AI Governance Committee provides the accountability structure auditors expect. This is a coordination mechanism, not a bottleneck.

**Minimal structure** (works for 10–100 developers):

| Role | Person | Responsibility |
|------|--------|----------------|
| **Governance Lead** | Engineering Manager or Lead | Policy updates, quarterly review, escalations |
| **Security Rep** | SecEng or DevSecOps | MCP risk review, incident response |
| **Dev Rep** | Senior dev rotation (3-month term) | Developer feedback, usability balance |
| **Compliance Rep** | Legal/Compliance (regulated only) | Charter, regulatory mapping |

**Meeting cadence**: Quarterly (30 min). Standing agenda:
1. MCP registry review — anything to add, remove, or flag?
2. Incident review — any AI-related security events since last meeting?
3. Policy updates — any charter changes needed?
4. Metrics — governance audit results, compliance check status

For detailed AI governance committee structures, RACI matrices, and compliance mapping, see Whitepaper #11: Enterprise AI Governance (FR/EN).

### 6.4 Monitoring for Compliance

The observability layer for governance is covered in [observability.md](../ops/observability.md). For compliance specifically, these monitoring queries are most relevant:

```bash
# Which files did Claude access in the last 30 days?
# macOS: date -v-30d; Linux: date -d '30 days ago'
if [[ "$OSTYPE" == "darwin"* ]]; then
  SINCE=$(date -v-30d +%Y-%m-%d)
else
  SINCE=$(date -d '30 days ago' +%Y-%m-%d)
fi

find ~/.claude/projects/ -name "*.jsonl" -newer "$SINCE" | \
  xargs jq -r 'select(.type == "assistant") |
    .message.content[]? |
    select(.type == "tool_use" and .name == "Read") |
    .input.file_path' 2>/dev/null | sort -u

# Any access to sensitive patterns?
# (Run after the above, pipe through grep)
grep -E '\.(env|pem|key)$|secrets/|credentials'

# Bash commands run by Claude this week
if [[ "$OSTYPE" == "darwin"* ]]; then
  SINCE_WEEK=$(date -v-7d +%Y-%m-%d)
else
  SINCE_WEEK=$(date -d '7 days ago' +%Y-%m-%d)
fi

find ~/.claude/projects/ -name "*.jsonl" -newer "$SINCE_WEEK" | \
  xargs jq -r 'select(.type == "assistant") |
    .message.content[]? |
    select(.type == "tool_use" and .name == "Bash") |
    .input.command' 2>/dev/null | sort
```

---

## Quick Reference

### Tier Selection

| Your situation | Tier | Setup time |
|----------------|------|------------|
| Side project, personal use | Starter | 10 min |
| Small team, internal project | Starter | 10 min |
| Team 5–20, any production code | Standard | 45 min |
| Team 20+, customer data | Strict | 2 hours |
| Regulated industry (HIPAA/SOC2/PCI) | Regulated | Half day |

### Governance Maturity Levels

| Maturity | What you have | What's missing |
|----------|---------------|----------------|
| **Ad hoc** | Each dev configures own setup | Consistency, accountability |
| **Basic** | Shared CLAUDE.md + settings.json | MCP governance, audit trail |
| **Managed** | + MCP registry + hooks | Compliance reporting |
| **Compliant** | + Audit logs + charter + review cycle | Nothing critical |
| **Audited** | + External validation + traceability | — |

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Governance only in `~/.claude` (personal) | Move to `.claude/` in repo |
| `permissions.allow` overrides team's `deny` | Review personal config quarterly |
| No MCP registry → every dev adds different MCPs | Start registry even if just 3 entries |
| CLAUDE.md too long → Claude ignores rules | Keep under 8KB, prioritize critical rules |
| Auditors ask for AI logs → nothing saved | Set up session log sync to S3 |

---

## See Also

- [Security Hardening](./security-hardening.md) — Individual dev security: MCP CVEs, injection defense, 5-min audit
- [Production Safety Rules](./production-safety.md) — 6 non-negotiable rules for prod teams (ports, DB safety, infra lock)
- [Data Privacy Guide](./data-privacy.md) — What data Claude Code sends to Anthropic, retention policies
- [AI Traceability](../ops/ai-traceability.md) — Attribution policies, Entire CLI, git-ai, compliance frameworks
- [Observability](../ops/observability.md) — Session monitoring, cost tracking, activity audit queries
- [Adoption Approaches](../roles/adoption-approaches.md) — Team rollout patterns, CLAUDE.md strategies
- [MCP Registry Template](../../examples/scripts/mcp-registry-template.yaml) — Ready-to-use registry format
- [Governance Hook](../../examples/hooks/bash/governance-enforcement-hook.sh) — Hook validating config against policy
- [AI Usage Charter Template](../../examples/scripts/ai-usage-charter-template.md) — Charter template ready to adapt

---

## References

- [Liminal AI Enterprise Governance Guide](https://www.liminal.ai/blog/enterprise-ai-governance-guide) — Practical implementation
- [Databricks AI Governance Framework](https://www.databricks.com/blog/practical-ai-governance-framework-enterprises) — Enterprise-scale framework
- [Augmentcode AI Code Governance](https://www.augmentcode.com/guides/ai-code-governance-framework-for-enterprise-dev-teams) — Dev team specific
- [Partnership on AI — Six Governance Priorities 2026](https://partnershiponai.org/resource/six-governance-priorities/) — Evaluation frameworks, accountability
- [EU AI Act](https://www.europarl.europa.eu/doceo/document/TA-9-2024-0138_EN.html) — Kill switch requirements for high-risk AI systems
- [NIST AI RMF](https://airc.nist.gov/RMF/Overview) — Risk management framework
- [SOC2 Trust Services Criteria](https://www.aicpa.org/resources/article/soc-2-trust-services-criteria) — CC6.1, CC7.1, CC9.2

---

*Version 1.0.0 | March 2026 | Part of [Claude Code Ultimate Guide](../README.md)*
