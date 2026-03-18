# Claude Code — For Tech Leads & Engineering Managers

> You've probably heard your devs talk about Claude Code. Maybe some are already using it. This page is for you — the person responsible for making that adoption consistent, secure, and scalable across the team.

---

## The core problem

Left to their own devices, each developer builds their own Claude Code setup. Different CLAUDE.md files, different permission configs, no shared hooks, no observability. The productivity gains are real but chaotic, and the security surface grows unchecked.

A team with a shared configuration is 3-5× more effective than the same devs working with individual setups.

---

## What you get from this guide

| Your concern | What's covered |
|---|---|
| **Standardizing config across the team** | WP05 — Deploying with a Team *(coming soon)* |
| **Security & compliance** | WP03 — Security in Production · WP06 — Privacy & GDPR *(coming soon)* |
| **CI/CD integration** | [Guide Ch.9.3](../guide/ultimate-guide.md#93-cicd-integration) |
| **Onboarding new devs** | [Guide Ch.3.5 — Team Configuration at Scale](../guide/ultimate-guide.md#35-team-configuration-at-scale) |
| **Understanding the architecture** | WP04 — Architecture Demystified *(coming soon)* |
| **Multi-agent workflows** | WP08 — Agent Teams *(coming soon)* |

---

## 30-minute reading path

> Whitepapers are currently in private access — public release coming soon.

1. **WP05 — Deploying with a Team** *(coming soon)* (25 min)
   - CLAUDE.md hierarchy (global / project / local)
   - Champions program: how to identify and empower early adopters
   - GitHub Actions for automated review + security scanning
   - Adoption phases: pilot → expansion → generalization

2. **[Guide Ch.3.5 — Team Configuration at Scale](../guide/ultimate-guide.md#35-team-configuration-at-scale)** (5 min)
   - How to version your team config in the repo
   - Shared vs personal settings

---

## The 3 things to do this week

**1. Version your CLAUDE.md in the repo**
Create a `CLAUDE.md` at the root of your main repo. It applies to everyone on the team automatically. Start with coding conventions, architecture decisions, and "never do X" rules.

**2. Identify one champion**
One engineer who's already effective with Claude Code. Give them time to document their setup and run a 1h team session.

**3. Add one security hook**
The minimum: a pre-tool hook that blocks writes to `.env` files and `**/secrets/**` paths. Takes 10 minutes to set up, covers a real threat vector.

```bash
# Example: hooks/block-sensitive-files.sh
if [[ "$TOOL_INPUT_PATH" =~ \.env$|secrets/ ]]; then
  echo "BLOCKED: sensitive file path"
  exit 2
fi
```

See [Guide Ch.7.4 — Security Hooks](../guide/ultimate-guide.md#74-security-hooks) for the full set.

---

## Security posture overview

This guide maintains the **only public threat database for Claude Code**: 15 vulnerabilities and 655 malicious skills catalogued. Key risks for teams:

- **Prompt injection** via untrusted file content or MCP servers
- **Overly permissive settings** — `allowedTools: ["*"]` in production
- **Unvetted MCP servers** — treat them like npm packages (supply chain risk)
- **Missing audit trail** — who did what, when

Full coverage in WP03 — Security and WP06 — Privacy *(whitepapers, coming soon)*.

---

## Training your team

If you want structured onboarding rather than self-learning:

- **Brown Bag Lunch, talk, or panel (1-3h, free)** — intro session, live demo, or speaker slot. Done for the pleasure of it: sharing, getting challenged, building network.
- **Config audit** — review your current setup against security and productivity best practices.
- **Team formation (1-2 days)** — hands-on, your codebase, your workflows. Not something I'm actively looking for, but open to the right conversation.

→ [Contact Florian Bruniaux](https://florian.bruniaux.com/) for availability and, depending on the mission, potentially pricing

---

## Quick links

- [Full Guide](../guide/ultimate-guide.md) — start at Ch.3.5 for team config
- Whitepapers — 10 focused deep-dives *(coming soon)*
- [Templates](../examples/) — ready-to-use hooks, agents, CLAUDE.md examples
- [Security Hardening](../guide/security/security-hardening.md) — threat database + mitigation guide
- [CHANGELOG](../CHANGELOG.md) — what changed recently

← [Back to main README](../README.md)
