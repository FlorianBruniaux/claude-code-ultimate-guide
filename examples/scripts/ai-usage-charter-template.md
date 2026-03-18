# AI Coding Tools Usage Charter

> **Template** — Copy to `docs/ai-usage-charter.md` in your organization's docs repo.
> Adapt sections marked with `[BRACKETS]`.
>
> Related: guide/security/enterprise-governance.md §2

---

**Organization**: [Your Organization]
**Applies to**: Claude Code and all AI coding assistants
**Effective date**: [DATE]
**Owner**: [Engineering Lead / CTO / CISO]
**Review cadence**: Quarterly
**Version**: 1.0.0

---

## 1. Purpose

This charter defines how [Organization] employees may use AI coding assistants, which tools are approved, what data can be used with them, and who is accountable for compliance. The goal is to enable productive AI-assisted development while managing security, privacy, and regulatory risk.

---

## 2. Approved Tools

| Tool | Plan / Tier | Scope | Administered by |
|------|-------------|-------|----------------|
| Claude Code | Team/Enterprise | All engineering work | Platform Team |
| Claude Code | Personal Pro | Personal dev only (no company data above INTERNAL) | Individual |
| [Other Tool] | [Plan] | [Scope] | [Team] |

**Using non-approved AI coding tools on company systems is prohibited.** If you believe an additional tool would benefit your work, submit an approval request to [engineering-lead@company.com].

---

## 3. Data Classification Rules

All data at [Organization] is classified into four levels. Your use of AI tools must comply with this classification.

| Classification | Examples | Claude Code permitted? | Notes |
|----------------|----------|----------------------|-------|
| **PUBLIC** | Open-source code, public documentation | Yes — no restrictions | |
| **INTERNAL** | Internal tools, non-sensitive business code | Yes — standard config | Use company accounts |
| **CONFIDENTIAL** | Customer data (non-PII), business secrets, proprietary algorithms | Yes — Enterprise plan only, with approved config | |
| **RESTRICTED** | PCI card data, PHI, credentials, auth tokens, encryption keys | **Never** | No exceptions |

### Hard Rules

- RESTRICTED data **never** enters an AI context window — not in prompts, not in files Claude reads, not as examples.
- Personal AI accounts (personal Pro subscriptions) may only be used with PUBLIC or INTERNAL data.
- Company credentials and API keys are RESTRICTED. Never paste them into prompts.

### Technical Enforcement

Projects handling CONFIDENTIAL or RESTRICTED data must configure `permissions.deny` in `.claude/settings.json` to block AI access to sensitive files. See the [Standard or Regulated tier config](../security/enterprise-governance.md#4-guardrail-tiers) for ready-to-use configurations.

---

## 4. Approved Use Cases

The following uses of AI coding assistants are approved without additional review:

- Code completion and generation for approved data classifications
- Code review and quality analysis
- Test generation and mutation testing
- Documentation drafting and updating
- Debugging, root cause analysis, log analysis
- Architecture analysis of internal systems
- CLI scripting, automation, build tooling
- Refactoring and code cleanup

---

## 5. Prohibited Use Cases

The following are **not permitted** without explicit written approval:

| Prohibited use | Reason | Exception process |
|----------------|--------|------------------|
| Processing raw PCI cardholder data | Regulatory (PCI DSS) | None — technically enforced |
| Generating code handling unencrypted PHI without security review | Regulatory (HIPAA) | Security review required |
| Autonomous deployment to production | Human oversight requirement | Approval from Eng Director |
| Using personal AI accounts for CONFIDENTIAL data | Data residency/privacy | Upgrade to company account |
| Sharing customer data as examples in prompts | Privacy, data handling | Use synthetic data |
| Bypassing governance controls (hooks, deny rules) | Policy violation | None |

---

## 6. MCP Server Governance

Model Context Protocol (MCP) servers extend Claude Code's capabilities and introduce additional risk surface. All MCP servers used on company projects must be:

1. Listed in the approved registry (`.claude/mcp-registry.yaml` in the platform config repo)
2. Pinned to an exact version (never `@latest`)
3. Re-reviewed every 6 months or on major version bumps

**Approval process**: Submit a request with server name, source URL, intended use case, and data scope to [platform-team@company.com] or [#claude-code-requests Slack channel].

Unapproved MCPs detected in project configs will be flagged at session start. Developers have 48 hours to remove or seek approval.

---

## 7. Code Review and Attribution

### AI Attribution

All pull requests where AI assisted in writing code must include an AI disclosure section:

```markdown
## AI Assistance
- AI tool used: Claude Code
- Scope: [e.g., "Generated tests for auth module", "Refactored payment handler"]
- Human review: Reviewer checked logic, security implications, and edge cases
```

The standard `Co-Authored-By: Claude <noreply@anthropic.com>` commit trailer (added automatically by Claude Code) satisfies attribution for routine changes. Explicit PR disclosure is required for:
- Any change to authentication or authorization
- Any change to payment or financial logic
- Any database schema change
- Any new external API integration

### Code Review Expectations

AI-generated code is not exempt from code review. Reviewers should apply the same — or stricter — scrutiny to AI-generated sections, particularly for:
- Security-sensitive paths (auth, crypto, access control)
- Data handling (PII, financial data)
- Edge cases and error conditions that AI tools often miss

---

## 8. Accountability

### Developer Responsibilities

By using Claude Code on company systems, you agree to:
- Follow this charter
- Report suspected data exposure to [security@company.com] within 24 hours
- Participate in quarterly access reviews
- Complete AI tools onboarding checklist when joining or switching teams
- Not circumvent governance controls (hooks, deny rules, registry)

### Team Lead Responsibilities

- Ensure projects are configured with the appropriate guardrail tier
- Review MCP registry quarterly
- Include AI charter in team onboarding
- Escalate charter violations per §9

### Platform Team Responsibilities

- Maintain shared governance config (settings.json templates, hooks)
- Review MCP approval requests within 1 week
- Update charter when tools, tiers, or risks change
- Conduct semi-annual governance audit

---

## 9. Incident Response

### If you suspect data exposure

1. **Stop** the current AI session immediately
2. **Document** what data may have been included in the context (which files, what prompts)
3. **Report** to [security@company.com] with "AI Data Exposure" in subject, within 24 hours
4. **Do not** attempt to investigate or remediate without security guidance

### Charter violations

| Severity | Examples | Response |
|----------|----------|---------|
| **Minor** | Forgot AI attribution in PR, used unapproved MCP briefly | Coaching, remediation |
| **Moderate** | Used personal account with CONFIDENTIAL data, bypassed a hook | Formal warning, re-training |
| **Severe** | Processed RESTRICTED data with AI, persistent bypass of controls | HR/legal involvement |

---

## 10. Compliance Mapping

This charter addresses the following compliance requirements:

| Framework | Relevant Controls | This Charter Addresses |
|-----------|------------------|----------------------|
| **SOC 2** | CC6.1 (Logical access), CC7.1 (Monitoring), CC9.2 (Vendor risk) | Data classification, MCP registry, audit logging |
| **ISO 27001** | A.8.3 (Access restriction), A.8.25 (Secure dev lifecycle), A.5.23 (Cloud services) | Approved tools, governance tiers, data handling |
| **HIPAA** (if applicable) | Security Rule §164.312 (Access control, Audit controls) | RESTRICTED data prohibition, compliance-mode logging |
| **PCI DSS** (if applicable) | Req 6.3 (Security vulnerabilities), Req 12 (Policy) | PCI data prohibition, code review requirements |
| **GDPR/CCPA** | Data minimization, purpose limitation | CONFIDENTIAL/RESTRICTED classification, data scope rules |

---

## 11. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | [DATE] | [Name] | Initial version |

---

*Questions or exceptions: [engineering-lead@company.com] | Slack: [#ai-tools-governance]*
