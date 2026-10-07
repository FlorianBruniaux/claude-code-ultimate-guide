---
title: "Claude Code: Security & Production Diagrams"
description: "Enforced defenses, sandbox boundaries, evidence and CI release gates"
tags: [security, production, sandbox, ci-cd, defense]
---

# Security & production

Use enforced execution boundaries and observed evidence when running Claude Code in sensitive environments. No diagram establishes universal containment or deployment safety.

---

### Security 3-layer defense model

Prevention, detection and response reduce different risks. Put enforced permissions and process isolation in place before running untrusted work. CLAUDE.md guides the model but does not enforce a security boundary. Sensitive-file protection needs file-tool permission rules and operating-system restrictions, not an assumed ignore-file feature. Logs must be configured and their coverage checked. Bypass permissions is appropriate only in an isolated environment, not merely because a job is labelled CI.

```mermaid
flowchart TD
    THREAT["Untrusted code or content"] --> PREV["Prevention before execution"]
    PREV --> VET["Vet MCP/skills/plugins<br/>review updates and pin versions"]
    PREV --> PERM["Minimal tool permissions<br/>managed deny/ask policies"]
    PREV --> FILES["Protect sensitive files<br/>file-tool denies + OS access restrictions"]
    PREV --> ISOLATE["Isolate whole process when needed<br/>container / VM, limited network"]
    VET --> RUN["Run within configured boundaries"]
    PERM --> RUN
    FILES --> RUN
    ISOLATE --> RUN
    RUN --> DETECT["Detection<br/>hooks + audit collection + alerts<br/>verify logging coverage"]
    DETECT --> INCIDENT{"Suspicious action or exposure?"}
    INCIDENT -->|No| CONTINUE["Continue monitoring<br/>Residual risk remains"]
    INCIDENT -->|Yes| RESP["Response<br/>stop access, preserve evidence<br/>rollback and rotate exposed secrets"]
    RESP --> REVIEW["Investigate exposure<br/>and strengthen controls"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click THREAT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
    click PREV href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
    click VET href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
    click PERM href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
    click FILES href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
    click ISOLATE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
    click RUN href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
    click DETECT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
    click INCIDENT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
    click CONTINUE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
    click RESP href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
    click REVIEW href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md" "View this pattern in the guide"
```

<details>
<summary>ASCII version</summary>

```
PREVENTION (before execution)
  Vet servers and updates; minimal permissions; managed policies
  File-tool denies + OS sensitive-file restrictions
  Whole-process isolation and limited network where needed
                        │
DETECTION
  Configured hooks/log collection/alerts; verify coverage
                        │
Suspicious action or exposure?
├─ No → monitor residual risk
└─ Yes → RESPONSE: stop access, preserve evidence,
                  rollback, rotate exposed secrets, investigate

CLAUDE.md guides behavior; it does not enforce a security boundary.
Bypass only in an isolated environment, not simply any CI job.
```

</details>

> **Source**: [Guide: Security 3-layer defense model](../security/security-hardening.md); [CLAUDE.md compliance limits](https://code.claude.com/docs/en/memory), [Permissions](https://code.claude.com/docs/en/permissions), [MCP security](https://code.claude.com/docs/en/security)

---

### Sandbox decision tree

Choose the boundary that covers the process at risk. The native shell sandbox supports macOS (Seatbelt) and Linux/WSL2 (bubblewrap and socat); native Windows needs WSL2 or another isolation environment. File tools, local MCP servers and hooks run outside the shell sandbox. Unknown MCP or hooks require vetting and, where needed, isolation of the entire Claude Code process. acceptEdits auto-approves edits, so it is not a stricter alternative to manual permissions. Native sandbox default reads can include credentials unless explicitly restricted.

```mermaid
flowchart TD
    START["Choose execution boundary"] --> PROCESS{"Untrusted MCP, hooks<br/>or whole-process access?"}
    PROCESS -->|Yes| WHOLE["Vet first, then isolate whole process<br/>container / VM or dedicated runtime<br/>restrict credentials and network"]
    PROCESS -->|No, shell commands only| PLATFORM{"Platform?"}
    PLATFORM -->|macOS| MAC["Native shell sandbox<br/>Seatbelt, enable via /sandbox"]
    PLATFORM -->|Linux or WSL2| LINUX["Native shell sandbox<br/>bubblewrap + socat dependencies"]
    PLATFORM -->|Native Windows| WIN["Use WSL2, container or VM<br/>no native shell sandbox"]
    MAC --> CONFIG["Restrict filesystem and network<br/>verify actual boundaries"]
    LINUX --> CONFIG
    WIN --> CONFIG
    WHOLE --> CONFIG
    CONFIG --> PERM["Keep appropriate permissions<br/>manual + narrow allowlist when needed<br/>review changes and evidence"]
    PERM --> PROD{"Production or CI environment?"}
    PROD -->|Yes| CI["Ephemeral/isolated execution<br/>limited secrets and deployment gates"]
    PROD -->|No| LOCAL["Apply boundary for project risk<br/>monitor residual exposure"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click START href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
    click PROCESS href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
    click WHOLE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
    click PLATFORM href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
    click MAC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
    click LINUX href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
    click WIN href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
    click CONFIG href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
    click PERM href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
    click PROD href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
    click CI href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
    click LOCAL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/sandbox-native.md" "View this pattern in the guide"
```

<details>
<summary>ASCII version</summary>

```
What needs isolation?
├─ Untrusted MCP/hooks/full process → vet first + whole-process isolation
│                                    restrict secrets and network
└─ Shell commands → native sandbox by platform
   ├─ macOS → Seatbelt, /sandbox
   ├─ Linux/WSL2 → bubblewrap + socat, /sandbox
   └─ Native Windows → WSL2/container/VM
               │
Restrict filesystem/network; verify enforced boundary
Keep appropriate permissions and review changes
├─ Production/CI → isolated execution + limited secrets + release gates
└─ Local project → boundary suited to project risk

Shell sandbox does not contain file tools, MCP servers or hooks.
acceptEdits automatically accepts edits, not stronger pre-edit review.
Credential reads need explicit restrictions.
```

</details>

> **Source**: [Guide: Sandbox decision tree](../security/sandbox-native.md); [Native sandbox scope and platforms](https://code.claude.com/docs/en/sandboxing), [Permission modes](https://code.claude.com/docs/en/permissions)

---

### The verification paradox

Asking the generator for an unsupported opinion does not verify its work. Claude can run deterministic tests and show results; those checks prove only what they exercise. Review critical behavior independently and distinguish code checks from deployment readiness and observed runtime behavior. Passing checks alone do not guarantee a safe release.

```mermaid
flowchart TD
    CODE["Claude writes code"] --> OPINION["Opinion-only self-review<br/>No runnable evidence"]
    OPINION --> RISK["Defects may remain undetected"]
    CODE --> TEST["Run behavior/regression tests<br/>inspect assertions and output"]
    CODE --> STATIC["Run relevant static/security checks"]
    CODE --> HUMAN["Independent review of critical behavior"]
    TEST --> GATE{"Evidence meets acceptance criteria?"}
    STATIC --> GATE
    HUMAN --> GATE
    GATE -->|No| FIX["Fix and rerun relevant checks"]
    FIX --> TEST
    GATE -->|Yes| RELEASE["Release decision<br/>known evidence scope and residual risks"]
    RELEASE --> RUNTIME["Deployment checks<br/>runtime verification and monitoring"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click CODE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "View this pattern in the guide"
    click OPINION href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "View this pattern in the guide"
    click RISK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "View this pattern in the guide"
    click TEST href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "View this pattern in the guide"
    click STATIC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "View this pattern in the guide"
    click HUMAN href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "View this pattern in the guide"
    click GATE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "View this pattern in the guide"
    click FIX href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "View this pattern in the guide"
    click RELEASE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "View this pattern in the guide"
    click RUNTIME href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/production-safety.md" "View this pattern in the guide"
```

<details>
<summary>ASCII version</summary>

```
Opinion only: generated code → "looks good" → defects may remain

Evidence: generated code → behavior tests + relevant static checks
                         → independent review of critical sections
                         → acceptance criteria met?
                           ├─ No → fix and rerun checks
                           └─ Yes → release decision for known scope
                                    → deployment checks
                                    → runtime verification/monitoring

A runnable check executed by Claude is evidence within its coverage.
Passing checks does not guarantee a safe release.
```

</details>

> **Source**: [Guide: The verification paradox](../security/production-safety.md); [Runnable verification and adversarial review](https://code.claude.com/docs/en/best-practices)

---

### CI/CD integration pipeline

CI should run lint, tests and security checks as explicit jobs and use their statuses as gates. Claude Code can read that evidence and produce an advisory review in non-interactive print mode, using claude -p or --print. A prompt does not itself guarantee parallel execution or trustworthy pass/fail aggregation. Configure authentication, tool permissions and job outputs explicitly; enforce release decisions through CI and human review rather than an agent opinion.

```mermaid
flowchart TD
    PR["PR created or updated"] --> ENV["CI configures isolated runner<br/>auth secret + minimal permissions"]
    ENV --> LINT["CI lint job<br/>record exit status"]
    ENV --> TEST["CI test job<br/>record assertions and exit status"]
    ENV --> SCAN["CI security scan job<br/>record findings and exit status"]
    LINT --> GATE{"Required CI jobs pass?"}
    TEST --> GATE
    SCAN --> GATE
    GATE -->|No| FAIL["Report failing jobs<br/>developer fixes and reruns CI"]
    FAIL --> ENV
    LINT --> EVIDENCE["Collect job evidence"]
    TEST --> EVIDENCE
    SCAN --> EVIDENCE
    EVIDENCE --> CLAUDE["claude -p<br/>Review quality-check evidence"]
    CLAUDE --> REPORT["Advisory agent review<br/>not a replacement for CI status"]
    GATE -->|Yes| HUMAN["Human review and branch rules"]
    REPORT --> HUMAN
    HUMAN --> RELEASE["Merge/release gate<br/>deployment and runtime checks"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click PR href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
    click ENV href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
    click LINT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
    click TEST href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
    click SCAN href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
    click GATE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
    click FAIL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
    click EVIDENCE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
    click CLAUDE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
    click REPORT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
    click HUMAN href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
    click RELEASE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#93-cicd-integration" "View this pattern in the guide"
```

<details>
<summary>ASCII version</summary>

```
PR → isolated CI runner + auth secret + minimal permissions
   → configured jobs (parallel only if CI declares it)
     ├─ Lint → exit status
     ├─ Tests → assertion results + exit status
     └─ Security scan → findings + exit status
           │
           ├─ Required CI jobs pass?
           │  ├─ No → report failure → fix → rerun CI
           │  └─ Yes → human review + branch rules → release gate
           │                                      → runtime checks
           └─ Job evidence → claude -p "Review quality-check evidence"
                           → advisory review for human

CI job status is the gate; an agent's opinion is not that status.
```

</details>

> **Source**: [Guide: CI/CD integration pipeline](../ultimate-guide.md#93-cicd-integration); [Print-mode CLI](https://code.claude.com/docs/en/cli-reference), [Runnable verification](https://code.claude.com/docs/en/best-practices)
