# Interactive Tools

Prompts and utilities for Claude Code setup and optimization.

## Contents

| File | Description | Usage |
|------|-------------|-------|
| [audit-prompt.md](./audit-prompt.md) | Comprehensive setup audit with personalized recommendations (8 dimensions, score /100) | `cat audit-prompt.md \| claude` |
| [permissions-audit-prompt.md](./permissions-audit-prompt.md) | Audit whether your permission rules still form a boundary: blanket execution grants, deny and ask coverage, sandbox posture (6 phases, score /100, fleet sweep included) | `cat permissions-audit-prompt.md \| claude` |
| [context-audit-prompt.md](./context-audit-prompt.md) | Measure and improve your context architecture | `cat context-audit-prompt.md \| claude` |
| [spec-completeness-audit.md](./spec-completeness-audit.md) | Audit how well a project is specified for safe agent delegation (5 spec layers, score /100) | `cat spec-completeness-audit.md \| claude` |
| [audit-cheatsheet-prompt.md](./audit-cheatsheet-prompt.md) | Evaluate whether a project needs a cheatsheet, and audit existing ones | `cat audit-cheatsheet-prompt.md \| claude` |
| [onboarding-prompt.md](./onboarding-prompt.md) | Personalized guided tour based on your profile | `cat onboarding-prompt.md \| claude` |
| [mobile-access.md](./mobile-access.md) | Setup guide for mobile access via ttyd + Tailscale | Step-by-step |

## Which audit when

| Question | Tool |
|----------|------|
| Is my whole setup healthy? | `audit-prompt.md` |
| Do my permission rules actually gate anything? | `permissions-audit-prompt.md` |
| Am I wasting context? | `context-audit-prompt.md` |
| Can I safely delegate work to an agent here? | `spec-completeness-audit.md` |
| Are there secrets or injection surfaces in this repo? | `/security-audit` (slash command) |

## Quick Audit

For a fast automated scan, use the script instead:

```bash
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/scripts/audit-scan.sh | bash
```

---

*Back to [main README](../README.md)*
