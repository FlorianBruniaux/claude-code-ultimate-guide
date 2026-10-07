---
title: "Enterprise AI Governance for Claude Code"
description: "Org-level governance for teams deploying Claude Code at scale: usage charters, MCP approval workflows, guardrail tiers, and compliance"
tags: [security, enterprise, governance, compliance]
---

# Enterprise AI governance for Claude Code

> **Audience**: Tech leads, engineering managers, security officers deploying Claude Code across teams.
>
> **Scope**: Org-level governance (policies, approval workflows, tiers, compliance). For individual dev security (injection defense, MCP vetting, CVEs), see [security-hardening.md](./security-hardening.md). For the 6 non-negotiable production rules, see [production-safety.md](./production-safety.md).

---

## TL;DR

**The governance gap**: Claude Code security docs cover what individual devs should do. They don't cover what happens when your entire organization is using it: 50 developers, different risk profiles, no shared policy.

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

## 1. Local vs shared: The governance split

Govern according to data access, credentials, actions, and execution environment. A local checkout can contain production credentials or customer data; a shared repository can contain only public examples. Location alone does not establish the risk level.

### 1.1 Risk matrix

| Dimension | Local usage | Shared usage |
|-----------|-------------|--------------|
| **Data exposure** | Any data reachable by the session | Any data reachable by the session |
| **Blast radius** | Depends on credentials, filesystem, network, and tools | Depends on credentials, filesystem, network, and tools |
| **Accountability** | Named operator and applicable org policy | Named owners and applicable org policy |
| **Reproducibility** | Saved sessions may exist; verify retention and access | Configure and verify the required audit trail |
| **Compliance scope** | Determined by data and processing obligations | Determined by data and processing obligations |
| **Config drift** | Inspect active personal, project, and managed sources | Inspect active sources and deployed policy |

### 1.2 What you can and can't control

**Repository configuration distributes a baseline**: share project instructions, supported settings, hooks, and project MCP definitions in `.mcp.json`. Keep CI checks as independent gates. A repository file is not an organization-wide policy lock.

**Managed controls enforce applicable policy inside Claude Code**: deploy supported managed settings and managed MCP restrictions to covered accounts or hosts. Verify which policy is active with `/status` and exercise blocked actions. Some values, such as a default model, remain defaults; use the documented restriction key when a choice must be limited. [Managed deployment](https://code.claude.com/docs/en/managed-settings#what-a-developer-can-change).

**Outside that boundary**: unmanaged devices, other API clients, and local administrators can require separate identity, endpoint, network, and credential controls. Do not claim governance of those surfaces from a committed file.

### 1.3 Decision framework: When to govern

The following is a proposed organizational framework, not product tiers. Apply controls according to the data and actions involved; validate the effective policy in each environment.

```
What are you governing?
│
├─ Personal dev workflow (local, throwaway code)
│   └─ Minimal: CLAUDE.md guidelines + basic hooks
│
├─ Team codebase (shared repo, not production)
│   └─ Standard: shared config + managed policy where required + PR gates
│
├─ Production system (customer-facing, real data)
│   └─ Strict: full tier config + approval workflow + audit log
│
└─ Regulated environment (HIPAA, SOC2, PCI, finance)
    └─ Regulated: all of above + compliance audit trail
```

---

## 2. AI usage charter

A usage charter answers the fundamental question: "What are we allowed to do with Claude Code at this company?" Without it, each team answers differently, creating inconsistent risk exposure.

This is an example policy to adapt with the owners responsible for your data, contracts, and systems. It does not establish a plan entitlement or a legal compliance requirement.

### 2.1 Lean charter template

Copy this into your org's `docs/ai-usage-charter.md` and adapt. Classification choices, review cadence, and approvals below are example organizational decisions:

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
| Organization-approved Claude Code account and processing route | Approved dev work | Approved classifications only |
| Personal accounts | Personal public work only | PUBLIC only |
| [Other approved tools] | [Scope] | [Classification] |

---

## Data Classification Rules

| Classification | Examples | Allowed with Claude Code? |
|----------------|----------|--------------------------|
| **PUBLIC** | Open source, public docs | Yes, subject to action permissions |
| **INTERNAL** | Internal tools, non-sensitive code | Only on an approved processing route |
| **CONFIDENTIAL** | Internal business secrets, non-regulated IP | Only when contracts, retention, and controls are approved |
| **RESTRICTED** | Customer PII, PCI card data, PHI, credentials | Prohibited under this example charter |

**Hard rule**: RESTRICTED data never enters an AI context window. Not in prompts, not in files Claude reads, not as examples. Remove restricted data from the execution environment and apply validated tool, filesystem, network, and credential controls. Instruction text alone is insufficient.

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

### 2.2 Data classification and Claude Code settings

These permission rules are a starting example for built-in tools, not complete data containment. Shell programs and MCP servers can access data through other routes. Use OS controls and narrowly scoped credentials, then test indirect reads and network egress. [Permission boundaries](https://code.claude.com/docs/en/permissions#how-permissions-interact-with-sandboxing).

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

### 2.3 Propagating settings to the team

Writing a charter is not enough: developers need to actually run with the right config. Use complementary mechanisms, each with a different scope:

**Shared settings.json in your team repo**

Commit supported project settings in `.claude/settings.json`. Check each key's scope and workspace-trust requirements; cloning a repository alone does not activate every possible setting. [Project settings scope](https://code.claude.com/docs/en/settings#a-committed-key-doesnt-reach-teammates).

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./**/*.key)",
      "Bash(curl *)",
      "Bash(wget *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/dangerous-actions-blocker.sh"
          }
        ]
      }
    ]
  }
}
```

Local settings can change ordinary project defaults without a tracked edit. Permission deny/ask rules combine across sources rather than following ordinary scalar precedence. Use managed policy for required restrictions and verify the result. The example assumes the referenced executable hook exists and has been tested; its Bash patterns do not block every network route. [Settings precedence](https://code.claude.com/docs/en/settings#settings-precedence), [hook configuration](https://code.claude.com/docs/en/hooks#hook-locations).

**Shared CLAUDE.md for behavior rules**

Use project `CLAUDE.md` to distribute coding standards and explain data-handling policy. It provides model guidance, not enforced tool restrictions. See §2.2 for the charter template.

**Anthropic Team and Enterprise admin controls**

Deploy the managed controls available for your organization and client. API Console administration, claude.ai organization settings, and host policy are different surfaces; check which one reaches the session. Organization restrictions need supported policy keys, delivery to the intended account or host, and runtime verification. [Deployment mechanisms](https://code.claude.com/docs/en/managed-settings).

Shared repository configuration remains useful for project defaults. It complements managed policy and execution-environment controls.

---

## 3. MCP governance workflow

Individual MCP vetting (the 5-minute audit) is covered in [security-hardening.md §1.1](./security-hardening.md#11-mcp-vetting-workflow). This section covers the organizational workflow: how new MCPs get approved, deployed, and monitored across your team.

### 3.1 Approval workflow

This is an example organizational process. A server name, popularity score, or absent advisory is not sufficient evidence of safety.

```
Developer requests MCP
        |
        v
[1] Record source, exact version, use case, data flow, credentials
        |
        v
[2] Review code/provenance, dependencies, advisories, permissions,
    tool descriptions, network access, and representative behavior
        |
        +-- Evidence insufficient --> Hold or reject
        |
        v
[3] Approve a bounded scope and reviewed version
    Record owner, decision evidence, and review triggers
        |
        v
[4] Distribute project definitions via .mcp.json
    Deploy managed MCP policy where restrictions must be enforced
    Verify the active policy and blocked actions
        |
        v
[5] Monitor advisories and behavior; re-review changes
    Update approval before deploying a changed version or scope
```

Choose review intervals and expiry rules as organizational policy. Do not automatically approve a patch merely because its version label suggests a small change. [Managed MCP configuration](https://code.claude.com/docs/en/mcp#managed-mcp-configuration).

### 3.2 MCP registry format

Maintain a registry such as `.claude/mcp-registry.yaml` in your shared config repo. Claude Code does not natively enforce this custom YAML. The values below are placeholders to replace with an actual review, not verified approvals or runnable version pins:

```yaml
# .claude/mcp-registry.yaml
# Approved MCP servers for [Organization Name]
# Last updated: [REVIEW_DATE]
# Reviewer: [Name, Role]

metadata:
  review_cycle: quarterly
  next_review: "NEXT_REVIEW_DATE"
  owner: "platform-team@company.com"

approved:
  - name: context7
    version: "REVIEWED_VERSION"
    source: "https://github.com/upstash/context7"
    approved_by: "john.doe@company.com"
    approved_date: "REVIEW_DATE"
    expires: "EXPIRY_DATE"
    data_scope: PUBLIC
    risk: LOW
    rationale: "Documentation lookup; review outbound queries and credentials."
    config:
      command: npx
      args: ["-y", "@upstash/context7-mcp@REVIEWED_VERSION"]

  - name: sequential-thinking
    version: "REVIEWED_VERSION"
    source: "https://github.com/modelcontextprotocol/servers"
    approved_by: "jane.smith@company.com"
    approved_date: "REVIEW_DATE"
    expires: "EXPIRY_DATE"
    data_scope: INTERNAL
    risk: LOW
    rationale: "Reference implementation; verify code and restrict network access."
    config:
      command: npx
      args: ["-y", "@modelcontextprotocol/server-sequential-thinking@REVIEWED_VERSION"]

  - name: internal-db-readonly
    version: "REVIEWED_VERSION"
    source: "internal"
    approved_by: "security@company.com"
    approved_date: "REVIEW_DATE"
    expires: "EXPIRY_DATE"  # shorter expiry for higher risk
    data_scope: CONFIDENTIAL
    risk: MEDIUM
    rationale: "Read-only replica access. No PII tables in allowlist."
    restrictions:
      - "Read-only credentials only"
      - "No access to users, payments, or audit tables"
    config:
      command: npx
      args: ["-y", "@company/db-mcp@REVIEWED_VERSION"]

pending_review:
  - name: github-mcp
    requested_by: "dev@company.com"
    requested_date: "REVIEW_DATE"
    use_case: "PR automation"
    status: under_review

denied:
  - name: browser-automation-mcp
    denied_date: "REVIEW_DATE"
    reason: "Full browser access with no scope restriction. Risk too high."
```

### 3.3 Enforcing the registry via hook

Use managed MCP configuration for enforced restrictions. The sample below is only a diagnostic warning for the top-level `mcpServers` map in `~/.claude.json`; it misses other scopes, project entries, plugins, connectors, and command-line definitions. It cannot validate the resolved active server set. Review and test any hook before use; the separate [governance hook example](../../examples/hooks/bash/governance-enforcement-hook.sh) also needs validation for your deployment.

```bash
#!/bin/bash
# .claude/hooks/governance-check.sh
# Event: SessionStart
# Warns on one stored MCP map; does not inventory active servers

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

**Note**: This example always continues the session, including when its dependencies are missing. It is not an enforcement or approval gate. Use deployed managed MCP controls and verify their coverage for the client surfaces in use.

### 3.4 Emerging: Runtime-level MCP tool isolation

Beyond approval workflows, an emerging approach sandboxes each MCP tool's OS access at runtime via WebAssembly. Tools like [Wassette](https://github.com/microsoft/wassette) run MCP servers as Wasm components with deny-by-default filesystem and network access, declared in YAML. None of these tools are production-ready as of mid-2026, but they are worth tracking if your risk model includes third-party MCP servers with unpredictable privilege scope. Full coverage: [sandbox-isolation.md §7b](./sandbox-isolation.md#7b-webassembly-based-mcp-tool-sandboxing-experimental).

### 3.5 Watch: Executor, the registry pattern as a product

The §3.1 to §3.3 workflow above (submit, review, register, enforce with a hook) is a manual answer to a question a growing category of tools tries to automate: a single catalog of approved integrations, shared across every agent that connects to it, instead of one registry per team or per tool.

[Executor](https://github.com/UsefulSoftwareCo/executor) (MIT, `1.4.0-beta.0`) is the clearest current example. It declares an integration once (an OpenAPI spec, a GraphQL endpoint, an existing MCP server), wraps it in a connection identified by `(scope, integration, name)` so one integration can hold several authenticated accounts, and gates every tool with the same three states this section already uses by name: allow, require approval, block. The mapping onto §3.2's registry format is close to one-to-one: an integration corresponds to a registry entry's `source` and `config`, a connection to a named authenticated instance of that entry, and the policy states to the registry's `risk` field generalized per tool rather than per server. Where it goes further than the hand-built version here is the credential itself: a connection never stores the raw secret, only a reference (`op://`, `keychain://`, `env://`, `vault://`) resolved by a provider at call time behind a proxy, so the secret cannot appear in a tool schema or an MCP response even by accident. §3.2's registry format has no equivalent field for this; the credential handling in that pattern still depends on whatever secrets manager sits underneath `.claude/settings.json`.

The trade-off is real and should be weighed against the registry's own maturity, not against Executor's marketing. A one-person project (93% of commits by a single contributor, measured 2026-07-29) at a pre-1.0 version is a different risk profile than a YAML file your own team owns and can read end to end in ten minutes. Treat Executor as what a hand-rolled registry eventually converges toward once it needs multi-agent sharing and credential indirection, not as a drop-in replacement for the workflow above. Full evaluation, including the vision-versus-shipped-code gap and the bus-factor detail: [`docs/resource-evaluations/executor-integration-governance-layer.md`](../../docs/resource-evaluations/executor-integration-governance-layer.md).

---

## 4. Guardrail tiers

Pre-configured guardrail tiers for four common scenarios. Adapt the relevant tier for your project's `.claude/settings.json` and `CLAUDE.md`. These examples require the referenced hook scripts to be installed and tested. Valid JSON and hook structure do not establish security behavior.

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
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/dangerous-actions-blocker.sh\""
          }
        ]
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

```json
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
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/dangerous-actions-blocker.sh\""
          }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/prompt-injection-detector.sh\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/output-secrets-scanner.sh\""
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/governance-check.sh\""
          }
        ]
      }
    ]
  }
}
```

```markdown
<!-- CLAUDE.md additions — Standard tier -->
## Production safety
- Infrastructure files (docker-compose, terraform, CI/CD) are locked.
  Request permission before modifying.
- New dependencies require Tech Lead approval. Do not run npm install <pkg>.
- Database destructive operations (DROP, DELETE, TRUNCATE) require backup confirmation.

## Code review gate
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
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/dangerous-actions-blocker.sh\""
          },
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/velocity-governor.sh\""
          }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/prompt-injection-detector.sh\""
          },
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/unicode-injection-scanner.sh\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/output-secrets-scanner.sh\""
          }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/session-logger.sh\""
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/governance-check.sh\""
          },
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/mcp-config-integrity.sh\""
          }
        ]
      }
    ]
  }
}
```

```markdown
<!-- CLAUDE.md additions — Strict tier -->
## Security posture: STRICT

You are operating in a strict security environment. Follow these rules without exception.

### Locked files
These files cannot be modified without explicit permission in this conversation:
- docker-compose.yml, Dockerfile, .github/workflows/**, terraform/**, kubernetes/**
- prisma/schema.prisma (database schema)
- Any file in /src/auth/, /src/payments/, /src/crypto/

### Dependency protocol
Before adding any dependency:
1. State the dependency name and purpose
2. List 2+ alternatives considered
3. Wait for explicit approval before running any install command

### Data access protocol
Before reading any file not in the project root:
1. State the file path and why you need it
2. Wait for approval if the path looks sensitive

### AI attribution
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
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/dangerous-actions-blocker.sh\""
          },
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/velocity-governor.sh\""
          }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/prompt-injection-detector.sh\""
          },
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/unicode-injection-scanner.sh\""
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
            "command": "bash \"$HOME/.claude/hooks/output-secrets-scanner.sh\""
          },
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/session-logger.sh\""
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/governance-check.sh\""
          },
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/hooks/mcp-config-integrity.sh\""
          }
        ]
      }
    ]
  }
}
```

```markdown
<!-- CLAUDE.md additions — Regulated tier -->
## Compliance mode: [HIPAA | SOC2 | PCI] — ACTIVE

You are operating under regulatory compliance requirements. These rules are non-negotiable.

### Prohibited data
NEVER include in your output, suggestions, or examples:
- PHI (patient health information), PII (names, emails, phones in customer context)
- Card numbers, CVVs, bank accounts
- SSNs, tax IDs, government IDs
- Raw authentication tokens, session cookies, API keys

### Mandatory review gates
These changes require human approval BEFORE code is committed:
- Any change to authentication or authorization logic
- Any change to encryption or key management
- Any database migration
- Any new external API integration

### Audit trail
Every session operating on regulated data must have:
- User ID noted at session start ("This session is for: [your-email]")
- Task description at session start ("Task: [brief description]")
- Checkpoint comment at natural breakpoints

### AI attribution (mandatory for regulated)
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
## Claude Code onboarding checklist

### Setup (30 minutes)
- [ ] Install Claude Code: `npm i -g @anthropic-ai/claude-code`
- [ ] Configure global safety hooks: `./scripts/install-global-hooks.sh`
- [ ] Verify project config loads: `claude` then ask "What tier is this project?"
- [ ] Read the AI Usage Charter (link to your doc)
- [ ] Review approved MCP list: `.claude/mcp-registry.yaml`

### Security basics
- [ ] Confirm `~/.claude/settings.json` has no `permissions.allow` overrides
  that bypass project's deny rules
- [ ] Confirm no personal MCP servers running that access production data
- [ ] Know how to report a data exposure: security@[company]

### First week
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
## Developer context

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

In CI/CD, check the active `settings.json` path at pipeline start to enforce the correct tier. Claude Code reads `.claude/settings.json` from the project root, so commit your strict-tier config there. CI always picks it up, regardless of what developers have locally.

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

**For full compliance audit trails with approval gates**, consider Entire CLI. It captures complete session context (prompts, reasoning, tool calls, file diffs) with cryptographic linking to git commits. See [AI Traceability §5.1](../ops/ai-traceability.md#51-entire-cli) for setup and evaluation criteria. This is one tool among several options; evaluate against your specific compliance requirements.

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
1. MCP registry review: anything to add, remove, or flag?
2. Incident review: any AI-related security events since last meeting?
3. Policy updates: any charter changes needed?
4. Metrics: governance audit results, compliance check status

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
| **Audited** | + External validation + traceability | None |

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

- [Security Hardening](./security-hardening.md): Individual dev security: MCP CVEs, injection defense, 5-min audit
- [Production Safety Rules](./production-safety.md): 6 non-negotiable rules for prod teams (ports, DB safety, infra lock)
- [Data Privacy Guide](./data-privacy.md): What data Claude Code sends to Anthropic, retention policies
- [AI Traceability](../ops/ai-traceability.md): Attribution policies, Entire CLI, git-ai, compliance frameworks
- [Observability](../ops/observability.md): Session monitoring, cost tracking, activity audit queries
- [Adoption Approaches](../roles/adoption-approaches.md): Team rollout patterns, CLAUDE.md strategies
- [MCP Registry Template](../../examples/scripts/mcp-registry-template.yaml): Ready-to-use registry format
- [Governance Hook](../../examples/hooks/bash/governance-enforcement-hook.sh): Hook validating config against policy
- [AI Usage Charter Template](../../examples/scripts/ai-usage-charter-template.md): Charter template ready to adapt

---

## References

- [Liminal AI Enterprise Governance Guide](https://www.liminal.ai/blog/enterprise-ai-governance-guide): Practical implementation
- [Databricks AI Governance Framework](https://www.databricks.com/blog/practical-ai-governance-framework-enterprises): Enterprise-scale framework
- [Augmentcode AI Code Governance](https://www.augmentcode.com/guides/ai-code-governance-framework-for-enterprise-dev-teams): Dev team specific
- [Partnership on AI: Six Governance Priorities 2026](https://partnershiponai.org/resource/six-ai-governance-priorities/): Evaluation frameworks, accountability
- [EU AI Act](https://www.europarl.europa.eu/doceo/document/TA-9-2024-0138_EN.html): Kill switch requirements for high-risk AI systems
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework): Risk management framework
- [SOC2 Trust Services Criteria](https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022): CC6.1, CC7.1, CC9.2

---

*Version 1.0.0 | March 2026 | Part of [Claude Code Ultimate Guide](../README.md)*
