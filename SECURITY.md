# Security Policy

## Scope

This repository contains **documentation and educational templates** for Claude Code. It does not include executable code that processes user input or runs in production environments.

**Security concerns specific to this repository:**
- Documentation accuracy for security practices
- Template code quality and security patterns
- Threat database integrity ([`machine-readable/threat-db.yaml`](./machine-readable/threat-db.yaml))

**Out of scope:**
- Security vulnerabilities in Claude Code CLI itself → Report to [Anthropic](https://github.com/anthropics/claude-code/security)
- Security issues in MCP servers → Report to respective server maintainers

## Reporting a Security Issue

If you discover a security concern related to this guide (examples: malicious template, incorrect security advice, threat database inaccuracies), please:

1. **Email**: florian.bruniaux@methode-aristote.fr
   - Subject: `[SECURITY] Claude Code Guide - Brief Description`
   - Include: Affected file/section, description, impact assessment

2. **GitHub Private Disclosure**: Use [Security Advisories](../../security/advisories/new) for sensitive issues

**Response SLA**: We aim to respond within 48 hours and issue fixes within 7 days for critical issues.

## Security Resources

This guide maintains comprehensive security documentation:

- **[Security Hardening Guide](./guide/security-hardening.md)** — MCP vetting, injection defense, audit workflows
- **[Threat Database](./machine-readable/threat-db.yaml)** — 18 CVEs, 341 malicious skills
- **[Security Hooks](./examples/hooks/)** — 30 production hooks (bash + PowerShell)
- **[Security Commands](./examples/commands/)** — `/security-check`, `/security-audit`, `/update-threat-db`

## Security Maintenance

**Threat Database Updates**: The threat intelligence database is updated based on:
- CVE announcements and security advisories
- Community reports of malicious skills/MCP servers
- Anthropic security bulletins
- Academic research (e.g., prompt injection papers)

**Audit Schedule**:
- Weekly review of new MCP servers and skills
- Monthly audit of security documentation accuracy
- Quarterly full threat database refresh

**Last Updated**: 2026-02-11 (v3.26.0)

## Coordinated Disclosure

If you're a security researcher and find issues affecting multiple repositories in the Claude Code ecosystem:

1. Email us first (coordinated disclosure preferred)
2. We'll coordinate with other maintainers if needed
3. Public disclosure timing: 90 days or after fix, whichever comes first

## Acknowledgments

We thank security researchers who have contributed to improving this guide's security content through responsible disclosure.

---

**Author**: [Florian BRUNIAUX](https://github.com/FlorianBruniaux) | Founding Engineer [@Méthode Aristote](https://methode-aristote.fr)

**Guide License**: [CC BY-SA 4.0](./LICENSE)
