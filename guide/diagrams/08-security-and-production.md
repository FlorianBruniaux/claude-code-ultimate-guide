---
title: "Claude Code — Security & Production Diagrams"
description: "3-layer defense, sandbox decision, verification paradox, CI/CD pipeline"
tags: [security, production, sandbox, ci-cd, defense]
---

# Security & Production

Patterns for safely running Claude Code in sensitive and production environments.

---

### Security 3-Layer Defense Model

Defense in depth for Claude Code: prevention stops most threats, detection catches what slips through, and response limits blast radius. No single layer is sufficient.

```mermaid
flowchart LR
    THREAT([Threat / Attack]) --> L1

    subgraph L1["🛡️ Layer 1: Prevention"]
        P1[MCP server vetting<br/>read source before install]
        P2[CLAUDE.md restrictions<br/>define forbidden actions]
        P3[.claudeignore<br/>hide sensitive files]
        P4[Minimal permissions<br/>bypassPermissions only in CI]
    end

    subgraph L2["🔍 Layer 2: Detection"]
        D1[PreToolUse hooks<br/>log all tool calls]
        D2[Audit logs<br/>complete history]
        D3[Anomaly alerts<br/>unexpected file access]
    end

    subgraph L3["🔒 Layer 3: Response"]
        R1[Sandbox isolation<br/>Docker / Firecracker]
        R2[Permission gates<br/>human approval on risk]
        R3[Rollback capability<br/>git revert, backups]
    end

    L1 -->|Bypassed| L2
    L2 -->|Bypassed| L3
    L3 --> BLOCKED([Threat contained])

    style THREAT fill:#E85D5D,color:#fff
    style P1 fill:#7BC47F,color:#333
    style P2 fill:#7BC47F,color:#333
    style P3 fill:#7BC47F,color:#333
    style P4 fill:#7BC47F,color:#333
    style D1 fill:#6DB3F2,color:#fff
    style D2 fill:#6DB3F2,color:#fff
    style D3 fill:#6DB3F2,color:#fff
    style R1 fill:#E87E2F,color:#fff
    style R2 fill:#E87E2F,color:#fff
    style R3 fill:#E87E2F,color:#fff
    style BLOCKED fill:#7BC47F,color:#333

    click THREAT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "Threat / Attack"
    click P1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md#part-1-prevention-before-you-start" "MCP server vetting"
    click P2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md#part-1-prevention-before-you-start" "CLAUDE.md restrictions"
    click P3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md#part-1-prevention-before-you-start" ".claudeignore"
    click P4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md#part-1-prevention-before-you-start" "Minimal permissions"
    click D1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md#part-2-detection-while-you-work" "PreToolUse hooks"
    click D2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md#part-2-detection-while-you-work" "Audit logs"
    click D3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md#part-2-detection-while-you-work" "Anomaly alerts"
    click R1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md#part-3-response-when-things-go-wrong" "Sandbox isolation"
    click R2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md#part-3-response-when-things-go-wrong" "Permission gates"
    click R3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md#part-3-response-when-things-go-wrong" "Rollback capability"
    click BLOCKED href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "Threat contained"
```

<details>
<summary>ASCII version</summary>

```
Threat
  │
Layer 1: PREVENTION
  - MCP vetting + CLAUDE.md restrictions + .claudeignore
  │ (bypassed) →
Layer 2: DETECTION
  - Hooks logging + audit logs + anomaly alerts
  │ (bypassed) →
Layer 3: RESPONSE
  - Sandbox + permission gates + rollback
  │
Contained
```

</details>

> **Source**: [Security Hardening](../security/security-hardening.md) — Full guide

---

### Sandbox Decision Tree

Sandboxing adds overhead. Use this tree to decide when it's mandatory, recommended, or optional for your situation.

```mermaid
flowchart TD
    A([Using Claude Code]) --> B{Running on<br/>production server?}
    B -->|Yes| C([ALWAYS sandbox<br/>Docker / Firecracker])
    B -->|No| D{Executing untrusted<br/>code or unknown MCP?}

    D -->|Yes| E{What platform?}
    E -->|macOS| F([macOS Sandbox<br/>built-in, free])
    E -->|Linux| G([Docker sandbox<br/>recommended])
    E -->|CI/CD| H([Ephemeral container<br/>best practice])

    D -->|No| I{Personal project<br/>known codebase?}
    I -->|Yes| J{Comfortable with<br/>default permissions?}
    J -->|Yes| K([Default mode<br/>sandbox optional])
    J -->|No| L([acceptEdits mode<br/>manual file review])

    I -->|No / Unsure| M([Sandbox recommended<br/>err on side of caution])

    NOTE["Rule of thumb:<br/>If in doubt → sandbox it<br/>Cost: low. Risk without it: high."] --> A

    style C fill:#E85D5D,color:#fff
    style F fill:#7BC47F,color:#333
    style G fill:#7BC47F,color:#333
    style H fill:#7BC47F,color:#333
    style K fill:#7BC47F,color:#333
    style L fill:#6DB3F2,color:#fff
    style M fill:#E87E2F,color:#fff
    style B fill:#E87E2F,color:#fff
    style D fill:#E87E2F,color:#fff
    style E fill:#E87E2F,color:#fff
    style I fill:#E87E2F,color:#fff
    style J fill:#E87E2F,color:#fff
    style NOTE fill:#F5E6D3,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "Using Claude Code"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "Running on production server?"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "ALWAYS sandbox"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "Executing untrusted code?"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "What platform?"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "macOS Sandbox"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "Docker sandbox"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "Ephemeral container"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "Personal project?"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "Comfortable with defaults?"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "Default mode"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "acceptEdits mode"
    click M href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "Sandbox recommended"
    click NOTE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "Rule of thumb"
```

<details>
<summary>ASCII version</summary>

```
Production server? → YES → ALWAYS sandbox (Docker/Firecracker)
     │ No
Untrusted code or unknown MCP?
  ├─ Yes → macOS sandbox / Docker / ephemeral container
  └─ No  → Personal project with known codebase?
            ├─ Yes → Default or acceptEdits (sandbox optional)
            └─ No  → Sandbox recommended

Rule: When in doubt, sandbox it.
```

</details>

> **Source**: [Sandbox Native](../security/sandbox-native.md) — Line ~512

---

### The Verification Paradox

Asking Claude to verify its own work is circular. The same model that produced the bug will often miss it during review. This anti-pattern causes production incidents.

```mermaid
flowchart TD
    subgraph BAD["❌ Anti-Pattern: Circular Verification"]
        BA([Claude writes code]) --> BB(Ask Claude:<br/>'Is this correct?')
        BB --> BC{Claude says:<br/>'Yes, looks good!'}
        BC -->|Deploy| BD([Bug in production])
        BC --> BE["Why it fails:<br/>Same model<br/>Same training biases<br/>Same blind spots"]
        style BA fill:#E85D5D,color:#fff
        style BD fill:#E85D5D,color:#fff
        style BE fill:#E85D5D,color:#fff
        style BC fill:#E87E2F,color:#fff
    end

    subgraph GOOD["✅ Best Practice: Independent Verification"]
        GA([Claude writes code]) --> GB(Human reviews<br/>critical sections)
        GA --> GC(Automated test suite<br/>runs independently)
        GA --> GD(Different tool validates<br/>Semgrep, ESLint, etc.)
        GB & GC & GD --> GE{All checks<br/>pass?}
        GE -->|Yes| GF([Safe to deploy])
        GE -->|No| GG([Fix before deploy])
        style GA fill:#7BC47F,color:#333
        style GB fill:#7BC47F,color:#333
        style GC fill:#7BC47F,color:#333
        style GD fill:#7BC47F,color:#333
        style GF fill:#7BC47F,color:#333
        style GE fill:#E87E2F,color:#fff
        style GG fill:#6DB3F2,color:#fff
    end

    click BA href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "Claude writes code (anti-pattern)"
    click BB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "Ask Claude to verify"
    click BC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "Claude says looks good"
    click BD href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "Bug in production"
    click BE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "Why it fails"
    click GA href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "Claude writes code (best practice)"
    click GB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "Human reviews critical sections"
    click GC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "Automated test suite"
    click GD href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "Different tool validates"
    click GE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "All checks pass?"
    click GF href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "Safe to deploy"
    click GG href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "Fix before deploy"
```

<details>
<summary>ASCII version</summary>

```
BAD: Claude writes → Claude checks → "Looks good" → Deploy → Bug
     (same model, same biases, circular)

GOOD: Claude writes → Human reviews (critical sections)
                    → Automated tests (independent)
                    → Static analysis (different tool)
                    → All pass? → Deploy ✓
```

</details>

> **Source**: [Production Safety](../security/production-safety.md) — Line ~639

---

### CI/CD Integration Pipeline

Claude Code can run in non-interactive mode inside CI/CD pipelines for automated code review, documentation, and quality checks on every PR.

```mermaid
flowchart LR
    PR([PR Created]) --> GH{GitHub Actions<br/>trigger}
    GH --> ENV[Set up environment<br/>ANTHROPIC_API_KEY secret]
    ENV --> CC[claude --print --headless<br/>'Run quality checks']

    CC --> subgraph TASKS["Parallel Checks"]
        T1[Lint check<br/>ESLint / Prettier]
        T2[Test suite<br/>Vitest / Jest]
        T3[Security scan<br/>Semgrep MCP]
        T4[Doc completeness<br/>check exports]
    end

    T1 & T2 & T3 & T4 --> AGG{All<br/>checks pass?}
    AGG -->|Yes| OK([✓ Checks green<br/>human review next])
    AGG -->|No| FAIL([✗ Report failures<br/>on PR])
    FAIL --> FIX([Developer fixes<br/>re-trigger CI])
    FIX --> CC

    style PR fill:#F5E6D3,color:#333
    style GH fill:#B8B8B8,color:#333
    style CC fill:#E87E2F,color:#fff
    style T1 fill:#6DB3F2,color:#fff
    style T2 fill:#6DB3F2,color:#fff
    style T3 fill:#6DB3F2,color:#fff
    style T4 fill:#6DB3F2,color:#fff
    style AGG fill:#E87E2F,color:#fff
    style OK fill:#7BC47F,color:#333
    style FAIL fill:#E85D5D,color:#fff
    style FIX fill:#F5E6D3,color:#333

    click PR href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "PR Created"
    click GH href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "GitHub Actions trigger"
    click ENV href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "Set up environment"
    click CC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "claude --print --headless"
    click T1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "Lint check"
    click T2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "Test suite"
    click T3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "Security scan"
    click T4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "Doc completeness"
    click AGG href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "All checks pass?"
    click OK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "Checks green"
    click FAIL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "Report failures on PR"
    click FIX href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "Developer fixes"
```

<details>
<summary>ASCII version</summary>

```
PR created → GitHub Actions → setup ANTHROPIC_API_KEY
                                    │
                          claude --print --headless
                                    │
                    ┌───────────────┼────────────────┐
                   Lint           Tests           Security
                                    │
                          All pass? ──No──► Fail PR + report
                            │ Yes
                          ✓ Green → human review → merge
```

</details>

> **Source**: [CI/CD Integration](../ultimate-guide.md#cicd-integration) — Line ~6835
