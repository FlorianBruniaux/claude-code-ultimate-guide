---
title: "Claude Code: Adoption & Learning Diagrams"
description: "Onboarding paths, proposed UVAL comprehension practice, trust calibration"
tags: [adoption, learning, onboarding, teams, trust]
---

# Adoption & Learning

Adopt Claude Code through scoped tasks, relevant verification and explicit checks of human understanding. Learning and productivity gains require evidence from the people and tasks involved.

---

### Onboarding adaptive learning paths

Choose a starting path based on responsibilities and existing skills. Progress when the observable criteria pass; no fixed training or team-adoption duration is implied.

```mermaid
flowchart TD
    A([New to Claude Code]) --> B{Your responsibilities?}
    B -->|Developer| C[First scoped task]
    C --> D[Practice a workflow with relevant verification]
    D --> E[Add agents, hooks or MCP when the task needs them]
    E --> F([Explain and verify the change; recover safely])
    B -->|Non-technical user| G[Learn concepts and access boundaries]
    G --> H[Practice reversible edits and explanations]
    H --> I[Use a scope appropriate to skills and permissions]
    I --> J([Explain the result and respect access boundaries])
    B -->|Team lead| K[Define acceptance criteria and a cost baseline]
    K --> L[Share concise conventions and controls]
    L --> M[Run a small pilot and collect evidence]
    M --> N[Review quality, rework, cost and feedback]
    N --> O([Expand only when pilot criteria pass])

    classDef diagramNode fill:#F5E6D3,color:#333,stroke:#A64B00
    class A,B,C,D,E,F,G,H,I,J,K,L,M,N,O diagramNode
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#41-what-are-agents" "View in guide"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "View in guide"
    click M href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click N href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
    click O href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer" "View in guide"
```

<details>
<summary>ASCII version</summary>

```text
Developer:
  Scoped task -> verified workflow -> add needed capabilities
  Gate: explain/verify the change and recover safely

Non-technical user:
  Concepts/access boundaries -> reversible practice -> suitable scope
  Gate: explain the result and respect access boundaries

Team lead:
  Acceptance/cost baseline -> shared conventions -> small pilot
  Gate: review quality, rework, cost and feedback before expansion
```

</details>

> **Source**: [Adoption approaches](../roles/adoption-approaches.md#start--build--scale-a-practical-navigation-layer)

> These are proposed paths, not measured completion times. The official quickstart covers installation, supported accounts and first tasks; the organization must evaluate its own pilot outcomes. [Official quickstart](https://code.claude.com/docs/en/quickstart).


---

### UVAL learning protocol

UVAL is a proposed practice for checking comprehension during AI-assisted work. It does not establish a retention benefit or replace the policy for accepting a change.

```mermaid
flowchart LR
    U[U: Understand First<br/>State the problem and identify gaps] --> V
    V[V: Verify<br/>Check explanation and prediction against evidence] --> A
    A[A: Apply<br/>Test a requirement or diagnose a defect] --> L
    L[L: Learn<br/>Record an insight] --> N{Assess later recall or transfer}
    N -->|Needs more practice| U
    N -->|Assessment recorded| R([Keep evidence; do not assume internalization])

    classDef diagramNode fill:#F5E6D3,color:#333,stroke:#A64B00
    class U,V,A,L,N,R diagramNode
    click U href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md#the-uval-protocol" "View in guide"
    click V href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md#the-uval-protocol" "View in guide"
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md#the-uval-protocol" "View in guide"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md#the-uval-protocol" "View in guide"
    click N href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md#the-uval-protocol" "View in guide"
    click R href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/learning-with-ai.md#the-uval-protocol" "View in guide"
```

<details>
<summary>ASCII version</summary>

```text
UNDERSTAND -> VERIFY -> APPLY -> LEARN
U: State the problem and identify knowledge gaps
V: Check explanation and prediction against evidence
A: Test a requirement or diagnose a defect; adapt when needed
L: Record an insight

Assess later recall/transfer -> practice further or record the result
Retention benefit remains to be evaluated
```

</details>

> **Source**: [The UVAL protocol](../roles/learning-with-ai.md#the-uval-protocol)


---

### Trust calibration matrix

Assess data sensitivity, security and external effects before accepting an output. Tests and rollback establish only their verified scope; a Git revert cannot reverse data disclosure or every external action.

```mermaid
flowchart TD
    A([Claude proposes output or an action]) --> B{Sensitive data, security<br/>or external effect?}
    B -->|Yes| C[Qualified review and relevant authorization]
    C --> D{Can the behavior be verified?}
    B -->|No| D
    D -->|Yes| E[Run checks that cover the required behavior]
    E --> F{Evidence meets acceptance criteria?}
    F -->|No| G[Fix, narrow scope or stop]
    F -->|Yes| H{Effects and recovery understood?}
    D -->|No| I[Review with a domain expert<br/>or find another verification method]
    I --> F
    H -->|No| I
    H -->|Yes| J([Accept only within the verified scope])
    K[Claude explanations are hypotheses<br/>check against independent evidence] -.-> I

    classDef diagramNode fill:#F5E6D3,color:#333,stroke:#A64B00
    class A,B,C,D,E,F,G,H,I,J,K diagramNode
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "View in guide"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "View in guide"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "View in guide"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "View in guide"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "View in guide"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "View in guide"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "View in guide"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "View in guide"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "View in guide"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "View in guide"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify" "View in guide"
```

<details>
<summary>ASCII version</summary>

```text
Sensitive data/security/external effect?
  Yes -> qualified review and relevant authorization
  No -> continue to verification
      |
Can behavior be verified?
  Yes -> run relevant checks
  No -> domain review or another verification method
      |
Evidence meets acceptance criteria?
  No -> fix, narrow scope or stop
  Yes -> understand effects and recovery
      -> accept only within the verified scope

An explanation is a hypothesis; Git rollback does not undo disclosure
```

</details>

> **Source**: [Trust calibration](../ultimate-guide.md#17-trust-calibration-when-and-how-much-to-verify)

> The reviewer remains responsible for the safety of proposed code and commands. Review requirements depend on the action and its effects. [Anthropic security guidance](https://code.claude.com/docs/en/security#user-responsibility).
