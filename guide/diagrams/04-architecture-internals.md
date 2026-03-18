---
title: "Claude Code — Architecture Internals Diagrams"
description: "Master loop, tool categories, system prompt assembly, sub-agent isolation"
tags: [architecture, internals, master-loop, tools]
---

# Architecture Internals

What happens under the hood when Claude Code runs.

---

### The Master Loop

Claude Code's core execution is a single loop: parse → build prompt → call API → execute tools → loop until done. The agentic behavior emerges from this simple cycle.

```mermaid
flowchart TD
    A([User Input]) --> B(Build System Prompt<br/>+ context + tools)
    B --> C{{Claude API Call}}
    C --> D{Response<br/>contains tool calls?}
    D -->|Yes| E(Parse tool calls)
    E --> F(Execute each tool<br/>Glob, Grep, Bash...)
    F --> G(Append tool results<br/>to conversation)
    G --> C
    D -->|No| H(Extract text response)
    H --> I([Display to User])
    I --> J{User sends<br/>next message?}
    J -->|Yes| A
    J -->|No| K([Session ends])

    style A fill:#F5E6D3,color:#333
    style C fill:#E87E2F,color:#fff
    style D fill:#E87E2F,color:#fff
    style F fill:#6DB3F2,color:#fff
    style I fill:#7BC47F,color:#333
    style J fill:#E87E2F,color:#fff
    style K fill:#B8B8B8,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "User Input"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Build System Prompt"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Claude API Call"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Response contains tool calls?"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Parse tool calls"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Execute each tool"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Append tool results"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Extract text response"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Display to User"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "User sends next message?"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Session ends"
```

<details>
<summary>ASCII version</summary>

```
User Input
     │
Build prompt (system + context + tools)
     │
 Claude API ◄────────────────────────┐
     │                               │
Tool calls?                          │
 ├─ Yes → Execute tools → Append results ──┘
 └─ No  → Display response
               │
         User next msg? ──► Yes → loop
               └─ No → Session ends
```

</details>

> **Source**: [Architecture: Master Loop](../core/architecture.md#master-loop) — Line ~72

---

### Tool Categories & Selection

Claude Code has 6 tool categories, each optimized for different operations. Understanding which tool Claude chooses (and why) helps you write instructions that guide better tool selection.

```mermaid
flowchart TD
    ROOT["Claude Code Tools"] --> READ
    ROOT --> WRITE
    ROOT --> EXECUTE
    ROOT --> WEB
    ROOT --> WORKFLOW
    ROOT --> CONTROL

    subgraph READ["📖 Read Tools"]
        R1[Glob<br/>Find files by pattern]
        R2[Grep<br/>Search file content]
        R3[Read<br/>Read file content]
        R4[LS<br/>List directory]
    end

    subgraph WRITE["✏️ Write Tools"]
        W1[Write<br/>Create new file]
        W2[Edit<br/>Modify existing file]
        W3[MultiEdit<br/>Batch modifications]
    end

    subgraph EXECUTE["⚙️ Execute Tools"]
        E1[Bash<br/>Shell commands]
        E2[Task<br/>Spawn sub-agent]
    end

    subgraph WEB["🌐 Web Tools"]
        WB1[WebSearch<br/>Search the web]
        WB2[WebFetch<br/>Fetch URL content]
    end

    subgraph WORKFLOW["📋 Workflow Tools"]
        WF1[TodoWrite<br/>Manage task list]
        WF2[NotebookEdit<br/>Jupyter notebooks]
    end

    subgraph CONTROL["🎛️ Control Flow Tools"]
        CF1[EnterPlanMode / ExitPlanMode<br/>Toggle plan mode]
        CF2[EnterWorktree / ExitWorktree<br/>Worktree navigation]
        CF3[AskUserQuestion<br/>Request human input]
    end

    style ROOT fill:#E87E2F,color:#fff
    style R1 fill:#6DB3F2,color:#fff
    style R2 fill:#6DB3F2,color:#fff
    style R3 fill:#6DB3F2,color:#fff
    style R4 fill:#6DB3F2,color:#fff
    style W1 fill:#F5E6D3,color:#333
    style W2 fill:#F5E6D3,color:#333
    style W3 fill:#F5E6D3,color:#333
    style E1 fill:#E85D5D,color:#fff
    style E2 fill:#E87E2F,color:#fff
    style WB1 fill:#7BC47F,color:#333
    style WB2 fill:#7BC47F,color:#333
    style WF1 fill:#B8B8B8,color:#333
    style WF2 fill:#B8B8B8,color:#333
    style CF1 fill:#B8B8B8,color:#333
    style CF2 fill:#B8B8B8,color:#333
    style CF3 fill:#B8B8B8,color:#333

    click ROOT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Claude Code Tools"
    click R1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Glob — Find files by pattern"
    click R2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Grep — Search file content"
    click R3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Read — Read file content"
    click R4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "LS — List directory"
    click W1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Write — Create new file"
    click W2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Edit — Modify existing file"
    click W3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "MultiEdit — Batch modifications"
    click E1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Bash — Shell commands"
    click E2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Task — Spawn sub-agent"
    click WB1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "WebSearch"
    click WB2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "WebFetch"
    click WF1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "TodoWrite — Task list"
    click WF2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "NotebookEdit — Jupyter"
    click CONTROL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Control Flow Tools"
    click CF1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "EnterPlanMode / ExitPlanMode"
    click CF2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "EnterWorktree / ExitWorktree"
    click CF3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "AskUserQuestion"
```

<details>
<summary>ASCII version</summary>

```
READ:     Glob (find), Grep (search), Read (content), LS (list)
WRITE:    Write (create), Edit (modify), MultiEdit (batch)
EXECUTE:  Bash (shell), Task (sub-agent)  ← most powerful/risky
WEB:      WebSearch, WebFetch
WORKFLOW: TodoWrite, NotebookEdit
CONTROL:  EnterPlanMode/ExitPlanMode, EnterWorktree/ExitWorktree, AskUserQuestion
```

</details>

> **Source**: [Architecture: Tools](../core/architecture.md#tools) — Line ~213

> *Simplified — additional tools available. See [Architecture: Tool Arsenal](../core/architecture.md#tools) for the full list.*

---

### System Prompt Assembly

Before every API call, Claude Code assembles a system prompt from multiple sources in a specific order. This explains why your CLAUDE.md instructions actually work and where they appear.

```mermaid
sequenceDiagram
    participant CC as Claude Code
    participant G as Global CLAUDE.md
    participant P as Project CLAUDE.md
    participant T as Tool Registry
    participant A as Claude API

    CC->>CC: 1. Load base instructions
    CC->>G: 2. Read ~/.claude/CLAUDE.md
    G->>CC: Global preferences, rules
    CC->>P: 3. Read project CLAUDE.md(s)
    P->>CC: Project conventions, context
    CC->>T: 4. Get available tools list
    T->>CC: Tool schemas (Glob, Grep, Bash...)
    CC->>CC: 5. Add working directory + git info
    CC->>CC: 6. Add MCP server capabilities
    CC->>A: System prompt (assembled)<br/>+ User message
    Note over A: One large call with<br/>all context embedded
```

<details>
<summary>ASCII version</summary>

```
System prompt assembly order:
1. Base instructions (hardcoded)
2. ~/.claude/CLAUDE.md
3. /project/CLAUDE.md + subdirs
4. Tool definitions list
5. Working directory + git status
6. MCP server capabilities
──────────────────────────────────
→ All combined → Claude API call
```

</details>

> **Source**: [Architecture: System Prompt](../core/architecture.md#system-prompt) — Line ~354

---

### Sub-Agent Context Isolation

Sub-agents are completely isolated from the parent — they can't read the parent's conversation or modify parent state. This isolation is a feature (safety) and a constraint (intentional design).

```mermaid
sequenceDiagram
    participant P as Parent Claude
    participant T as Task Tool
    participant S as Sub-Agent
    participant EXT as External Services

    Note over P: Has full conversation history
    P->>T: Task(prompt="do X", tools=[Read,Write,Bash])
    Note over T: Creates new Claude instance
    T->>S: spawn(prompt + tool grants ONLY)
    Note over S: Does NOT receive:<br/>- Parent conversation<br/>- Parent tool results<br/>- Parent state

    S->>EXT: read files, bash, web (as granted)
    EXT->>S: Results

    Note over S: Independent reasoning<br/>with limited context

    S->>T: return "task complete: details..."
    Note over T: Only text passes back
    T->>P: Result string
    Note over P: Parent gets text only<br/>No shared state
```

<details>
<summary>ASCII version</summary>

```
Parent (full context)
    │
    Task(prompt, tools=[...])
    │
    ▼
Sub-Agent (ISOLATED)
  Input: prompt + tool grants only
  Can: use granted tools independently
  Cannot: see parent conversation, modify parent state
  Output: text result ONLY
    │
    ▼
Parent receives: text string
```

</details>

> **Source**: [Architecture: Sub-Agents](../core/architecture.md#sub-agents) — Line ~444
