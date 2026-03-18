---
title: "Claude Code — Foundations Diagrams"
description: "Core concepts: 4-layer model, workflow pipeline, decision tree, 5 permission modes"
tags: [foundations, architecture, getting-started]
---

# Foundations

Core concepts that explain what Claude Code is and how it fundamentally operates.

---

### "Chatbot to Context System" — 4-Layer Model

Claude Code isn't a chatbot — it's a context system that transforms your message into a rich multi-layer prompt before calling the API. This diagram shows the 4-layer augmentation that happens invisibly with every request.

```mermaid
flowchart TD
    A([User Message]) --> B[[Layer 1: System Prompt]]
    B --> C[[Layer 2: Context Injection]]
    C --> D[[Layer 3: Tool Definitions]]
    D --> E[[Layer 4: Conversation History]]
    E --> F{{Claude API}}
    F --> G([Claude Response])

    B1[CLAUDE.md files<br/>global + project + subdir] --> B
    C1[Working directory<br/>Git status<br/>Project files] --> C
    D1[Glob, Grep, Read,<br/>Bash, Task, MCP tools] --> D
    E1[Previous messages<br/>+ tool results] --> E

    style A fill:#F5E6D3,color:#333
    style B fill:#6DB3F2,color:#fff
    style C fill:#6DB3F2,color:#fff
    style D fill:#6DB3F2,color:#fff
    style E fill:#6DB3F2,color:#fff
    style F fill:#E87E2F,color:#fff
    style G fill:#7BC47F,color:#333
    style B1 fill:#B8B8B8,color:#333
    style C1 fill:#B8B8B8,color:#333
    style D1 fill:#B8B8B8,color:#333
    style E1 fill:#B8B8B8,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "First Workflow"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Layer 1: System Prompt"
    click B1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Memory Files (CLAUDE.md)"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Layer 2: Context Injection"
    click C1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Context Management"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Layer 3: Tool Definitions"
    click D1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Tool Arsenal"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Layer 4: Conversation History"
    click E1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Context Management"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Claude API — Master Loop"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Claude Response"
```

<details>
<summary>ASCII version</summary>

```
User Message
     │
     ▼
┌─────────────────────────────────┐
│ Layer 1: System Prompt          │ ← CLAUDE.md files
│ Layer 2: Context Injection      │ ← Working dir, git status
│ Layer 3: Tool Definitions       │ ← All available tools
│ Layer 4: Conversation History   │ ← Previous messages
└─────────────────┬───────────────┘
                  │
                  ▼
           Claude API Call
                  │
                  ▼
           Claude Response
```

</details>

> **Source**: [How Claude Code Works](../ultimate-guide.md#how-claude-code-works) — Line ~2360

---

### 9-Step Workflow Pipeline

Every request to Claude Code goes through this pipeline — from parsing your intent to displaying the final response. Understanding this loop helps you write better instructions and diagnose issues faster.

```mermaid
flowchart LR
    A([User Message]) --> B(Parse Intent)
    B --> C(Load Context)
    C --> D(Plan Actions)
    D --> E(Execute Tools)
    E --> F{More tools<br/>needed?}
    F -->|Yes| G(Collect Results)
    G --> E
    F -->|No| H(Update Context)
    H --> I(Generate Response)
    I --> J([Display to User])

    style A fill:#F5E6D3,color:#333
    style B fill:#6DB3F2,color:#fff
    style C fill:#6DB3F2,color:#fff
    style D fill:#E87E2F,color:#fff
    style E fill:#E87E2F,color:#fff
    style F fill:#E87E2F,color:#fff
    style G fill:#B8B8B8,color:#333
    style H fill:#B8B8B8,color:#333
    style I fill:#6DB3F2,color:#fff
    style J fill:#7BC47F,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "First Workflow"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Parse Intent — Master Loop"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Load Context"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#23-plan-mode" "Plan Actions — Plan Mode"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Execute Tools"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "More Tools? — Master Loop"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Collect Results"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Update Context"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Generate Response"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Display to User"
```

<details>
<summary>ASCII version</summary>

```
User Message → Parse Intent → Load Context → Plan Actions
                                                   │
                          ┌────────────────────────┘
                          ▼
                    Execute Tools ◄─────────────────┐
                          │                          │
                    More tools?  ──── Yes ─── Collect Results
                          │ No
                          ▼
                   Update Context → Generate Response → Display
```

</details>

> **Source**: [Getting Started](../ultimate-guide.md#getting-started) — Line ~277

---

### Quick Decision Tree — "Should I use Claude Code?"

Not every task needs Claude Code. This decision tree helps you route the right tasks to the right tool — Claude Code CLI vs Claude.ai vs clipboard-based approaches.

```mermaid
flowchart TD
    A([Start: I have a task]) --> B{Involves<br/>codebase?}
    B -->|No| C{Pure writing<br/>or analysis?}
    B -->|Yes| D{Repetitive or<br/>>30 min manual?}

    C -->|Yes| E([Use Claude.ai<br/>or API])
    C -->|No| F([Clipboard +<br/>Claude.ai])

    D -->|No| G{Single file,<br/>simple change?}
    D -->|Yes| H([Claude Code<br/>✓ Best choice])

    G -->|Yes| I{Need file<br/>access?}
    G -->|No| H

    I -->|No| F
    I -->|Yes| H

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style C fill:#E87E2F,color:#fff
    style D fill:#E87E2F,color:#fff
    style G fill:#E87E2F,color:#fff
    style I fill:#E87E2F,color:#fff
    style E fill:#6DB3F2,color:#fff
    style F fill:#6DB3F2,color:#fff
    style H fill:#7BC47F,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "When to Use Claude Code"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Involves codebase?"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Pure writing or analysis?"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Repetitive or long manual task?"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Use Claude.ai"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Clipboard + Claude.ai"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Single file, simple change?"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#11-installation" "Claude Code — Best choice"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Need file access?"
```

<details>
<summary>ASCII version</summary>

```
Task involves codebase?
├── No → Pure writing/analysis? → Yes → Claude.ai
│                              → No  → Clipboard + Claude.ai
└── Yes → Repetitive or >30min?
          ├── Yes → ✓ Claude Code
          └── No  → Single file, simple?
                    ├── Yes → Need file access? → No → Clipboard
                    │                            → Yes → Claude Code
                    └── No  → ✓ Claude Code
```

</details>

> **Source**: [Quick Start Decision](../ultimate-guide.md#quick-start) — See also `machine-readable/reference.yaml` (decide section)

---

### Permission Modes Comparison

Claude Code has 5 permission modes that control what it can do automatically vs. what requires your approval. Choosing the wrong mode is the #1 safety mistake.

```mermaid
flowchart TD
    subgraph DEFAULT["🔒 Default Mode (Recommended)"]
        D1(File reads) --> D2([Auto-approved])
        D3(File writes) --> D4([Prompt required])
        D5(Shell commands) --> D6([Prompt required])
        D7(Risky ops) --> D8([Prompt required])
    end

    subgraph ACCEPT["✏️ acceptEdits Mode"]
        A1(File reads) --> A2([Auto-approved])
        A3(File writes) --> A4([Auto-approved])
        A5(Shell commands) --> A6([Prompt required])
        A7(Risky ops) --> A8([Prompt required])
    end

    subgraph BYPASS["⚠️ bypassPermissions Mode"]
        B1(ALL operations) --> B2([Auto-approved])
        B3["Use only in:<br/>CI/CD, sandboxed<br/>environments"] --> B2
    end

    subgraph PLAN["🔍 Plan Mode (Read-Only)"]
        PL1(File reads) --> PL2([Auto-approved])
        PL3(File writes) --> PL4([Blocked])
        PL5(Shell commands) --> PL6([Blocked])
        PL7["Exit with /execute<br/>or Shift+Tab"] --> PL2
    end

    subgraph DONTASK["🚫 dontAsk Mode"]
        DA1(ALL operations) --> DA2([Auto-denied])
        DA3["Unless pre-approved<br/>via /permissions add"] --> DA2
    end

    style D2 fill:#7BC47F,color:#333
    style D4 fill:#E87E2F,color:#fff
    style D6 fill:#E87E2F,color:#fff
    style D8 fill:#E87E2F,color:#fff
    style A2 fill:#7BC47F,color:#333
    style A4 fill:#7BC47F,color:#333
    style A6 fill:#E87E2F,color:#fff
    style A8 fill:#E87E2F,color:#fff
    style B2 fill:#E85D5D,color:#fff
    style B3 fill:#F5E6D3,color:#333
    style PL2 fill:#7BC47F,color:#333
    style PL4 fill:#E85D5D,color:#fff
    style PL6 fill:#E85D5D,color:#fff
    style DA2 fill:#E85D5D,color:#fff
    style DA3 fill:#F5E6D3,color:#333

    click D1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Default Mode — Permission Modes"
    click D2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-approved"
    click D3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "File writes"
    click D4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Prompt required"
    click D5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Shell commands"
    click D6 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Prompt required"
    click D7 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Risky ops"
    click D8 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Prompt required"
    click A1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "acceptEdits Mode"
    click A2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-approved"
    click A3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "File writes — auto"
    click A4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-approved"
    click A5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Shell commands"
    click A6 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Prompt required"
    click A7 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Risky ops"
    click A8 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Prompt required"
    click B1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "bypassPermissions Mode"
    click B2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-approved (all)"
    click B3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "CI/CD, sandboxed only"
    click PL1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Plan Mode — File reads"
    click PL2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-approved"
    click PL3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Plan Mode — File writes blocked"
    click PL4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Blocked"
    click PL5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Plan Mode — Shell commands blocked"
    click PL6 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Blocked"
    click PL7 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Exit Plan Mode"
    click DA1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "dontAsk Mode — All operations"
    click DA2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-denied"
    click DA3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Pre-approve via /permissions add"
```

<details>
<summary>ASCII version</summary>

```
DEFAULT (Recommended)        acceptEdits               bypassPermissions
─────────────────────        ───────────               ─────────────────
File reads    → AUTO ✓       File reads    → AUTO ✓    ALL ops → AUTO ⚠️
File writes   → PROMPT       File writes   → AUTO ✓
Shell cmds    → PROMPT       Shell cmds    → PROMPT    Use: CI/CD only,
Risky ops     → PROMPT       Risky ops     → PROMPT    sandboxed env

Plan Mode (Read-Only)        dontAsk Mode
─────────────────────        ────────────
File reads    → AUTO ✓       ALL ops → AUTO DENIED ✗
File writes   → BLOCKED ✗    Unless pre-approved via
Shell cmds    → BLOCKED ✗    /permissions add
Exit: /execute or Shift+Tab
```

</details>

> **Source**: [Permission System](../ultimate-guide.md#permission-system) — Line ~760
