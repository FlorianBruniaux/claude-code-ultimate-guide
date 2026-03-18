---
title: "Claude Code — Adoption & Learning Diagrams"
description: "Onboarding paths, UVAL learning protocol, trust calibration matrix"
tags: [adoption, learning, onboarding, teams, trust]
---

# Adoption & Learning

How individuals and teams successfully adopt Claude Code without losing skills or control.

---

### Onboarding Adaptive Learning Paths

Different backgrounds require different onboarding approaches. Forcing developers through a beginner path wastes time; dropping non-technical users into advanced features causes frustration.

```mermaid
flowchart TD
    A([Start: New to Claude Code]) --> B{Your background?}

    B -->|Developer| C["🧑‍💻 Developer Path<br/>~2 days to productivity"]
    C --> C1(Quick Start: first session)
    C1 --> C2(Workflows: TDD, spec-first, plan-driven)
    C2 --> C3(Advanced: agents, hooks, MCP servers)
    C3 --> C4([Productive developer ✓])

    B -->|Non-technical| D["👤 Non-Tech Path<br/>~1 week to basic usage"]
    D --> D1(What is Claude Code?<br/>Key concepts only)
    D1 --> D2(Basic usage: editing,<br/>explaining, simple tasks)
    D2 --> D3(Limited scope: no<br/>production deployments)
    D3 --> D4([Safe basic user ✓])

    B -->|Team lead| E["👔 Team Lead Path<br/>~2 weeks to team adoption"]
    E --> E1(ROI assessment<br/>value vs cost analysis)
    E1 --> E2(CLAUDE.md strategy<br/>team conventions)
    E2 --> E3(Pilot with 2-3 devs<br/>collect feedback)
    E3 --> E4(Gradual rollout<br/>with guardrails)
    E4 --> E5([Team adoption ✓])

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style C fill:#6DB3F2,color:#fff
    style D fill:#6DB3F2,color:#fff
    style E fill:#6DB3F2,color:#fff
    style C4 fill:#7BC47F,color:#333
    style D4 fill:#7BC47F,color:#333
    style E5 fill:#7BC47F,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "Start: New to Claude Code"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "Your background?"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Developer Path"
    click C1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Quick Start: first session"
    click C2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Workflows: TDD, spec-first, plan-driven"
    click C3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Advanced: agents, hooks, MCP"
    click C4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "Productive developer"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "Non-Tech Path"
    click D1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "What is Claude Code?"
    click D2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "Basic usage"
    click D3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "Limited scope"
    click D4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "Safe basic user"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "Team Lead Path"
    click E1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "ROI assessment"
    click E2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "CLAUDE.md strategy"
    click E3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "Pilot with 2-3 devs"
    click E4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "Gradual rollout"
    click E5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md" "Team adoption"
```

<details>
<summary>ASCII version</summary>

```
Your background?
├─ Developer (~2 days):
│  Quick Start → Workflows (TDD/spec/plan) → Advanced (agents/hooks/MCP)
│
├─ Non-technical (~1 week):
│  What is CC? → Basic usage → Limited scope (no prod deploys)
│
└─ Team lead (~2 weeks):
   ROI assessment → CLAUDE.md strategy → Pilot 2-3 devs → Gradual rollout
```

</details>

> **Source**: [Adoption Approaches](../roles/adoption-approaches.md)

---

### UVAL Learning Protocol

The UVAL protocol prevents the "copy-paste trap" — where you use Claude Code without understanding what it did. Each cycle builds real competency that survives tool unavailability.

```mermaid
flowchart LR
    U([U — Use It<br/>Try the feature<br/>yourself first]) --> V

    V([V — Verify<br/>Understand what<br/>Claude did and why]) --> A

    A([A — Adapt<br/>Modify the approach,<br/>experiment with variants]) --> L

    L([L — Learn<br/>Note the pattern<br/>for future use]) --> NEXT

    NEXT{More tasks<br/>using this pattern?} -->|Yes| U
    NEXT -->|No| DONE([Pattern internalized ✓])

    TRAP["❌ Copy-Paste Trap:<br/>Accept output →<br/>Deploy → Bug →<br/>'Claude broke it'"] -.->|avoid| V

    style U fill:#6DB3F2,color:#fff
    style V fill:#E87E2F,color:#fff
    style A fill:#E87E2F,color:#fff
    style L fill:#7BC47F,color:#333
    style NEXT fill:#E87E2F,color:#fff
    style DONE fill:#7BC47F,color:#333
    style TRAP fill:#E85D5D,color:#fff

    click U href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md" "Use It"
    click V href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md" "Verify"
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md" "Adapt"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md" "Learn"
    click NEXT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md" "More tasks using this pattern?"
    click DONE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md" "Pattern internalized"
    click TRAP href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md" "Copy-Paste Trap"
```

<details>
<summary>ASCII version</summary>

```
USE → VERIFY → ADAPT → LEARN → (repeat with next task)

U: Try the feature yourself first
V: Understand what Claude did and why ← (anti: just copy-paste)
A: Modify the approach, experiment
L: Note pattern for future use

Anti-pattern (AVOID): Accept output → Deploy → Bug → "Claude broke it"
```

</details>

> **Source**: [Learning with AI](../roles/learning-with-ai.md) — Line ~127

---

### Trust Calibration Matrix

Knowing when to trust Claude's output and when to verify is the most important skill in AI-assisted development. Over-trust causes bugs; under-trust eliminates productivity gains.

```mermaid
flowchart TD
    A([Claude produces output]) --> B{Can I test<br/>this output?}

    B -->|Yes| C{Do the tests<br/>actually pass?}
    C -->|Yes| D([Trust with test coverage ✓])
    C -->|No| E([Fix before using])

    B -->|No| F{Do I understand<br/>what it did?}
    F -->|No| G(Ask Claude to explain<br/>step by step)
    G --> F

    F -->|Yes| H{Is this<br/>reversible?}
    H -->|Yes, easily| I([Trust with git safety net ✓])
    H -->|No: hard to undo| J(Extra review required<br/>check before applying)
    J --> K{Is it<br/>security-critical?}

    K -->|Yes: auth, crypto, perms| L([Human expert review<br/>never trust blindly])
    K -->|No| M{Familiar<br/>domain?}
    M -->|Yes| I
    M -->|No| N([Pair with domain expert<br/>or verify by testing])

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style C fill:#E87E2F,color:#fff
    style F fill:#E87E2F,color:#fff
    style H fill:#E87E2F,color:#fff
    style K fill:#E87E2F,color:#fff
    style M fill:#E87E2F,color:#fff
    style D fill:#7BC47F,color:#333
    style I fill:#7BC47F,color:#333
    style E fill:#E85D5D,color:#fff
    style L fill:#E85D5D,color:#fff
    style N fill:#6DB3F2,color:#fff
    style J fill:#F5E6D3,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Claude produces output"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Can I test this output?"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Do the tests pass?"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Trust with test coverage"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Fix before using"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Do I understand what it did?"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Ask Claude to explain"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Is this reversible?"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Trust with git safety net"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Extra review required"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Is it security-critical?"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Human expert review"
    click M href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Familiar domain?"
    click N href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "Pair with domain expert"
```

<details>
<summary>ASCII version</summary>

```
Can I test it?
├─ Yes → Tests pass? → Yes → Trust with tests ✓
│                  → No  → Fix before using
└─ No  → Do I understand it?
         ├─ No  → Ask Claude to explain → understand → continue
         └─ Yes → Is it reversible?
                  ├─ Yes     → Trust with git safety net ✓
                  └─ No      → Security-critical?
                               ├─ Yes → Human expert review (never skip)
                               └─ No  → Familiar domain?
                                        ├─ Yes → Trust with care ✓
                                        └─ No  → Pair with expert
```

</details>

> **Source**: [Trust and Verification](../ultimate-guide.md#trust-verification) — Line ~1039

---

*Back to [diagrams/README.md](./README.md) | Next: [Cost Optimization](./09-cost-and-optimization.md)*
