---
title: "Claude Code: Architecture Internals Diagrams"
description: "Agentic loop, illustrative tool families, request context, and subagent boundaries"
tags: [architecture, internals, master-loop, tools]
---

# Architecture internals

Conceptual diagrams of the model-and-tool loop, tool families and context boundaries.

---

### The master loop

A simplified model-and-tool loop: Claude requests tools, permitted operations run, and their results return to the conversation. Turns can also end because of errors, cancellation or limits. Independent operations may run concurrently; no fixed concurrency limit is asserted.

```mermaid
flowchart TD
    A([User input]) --> B[Prepare request context<br/>Instructions, history, available tools]
    B --> C{{Model request}}
    C --> D{Tool calls?}
    D -->|Yes| PERM{Allowed?}
    PERM -->|Yes| E[Execute permitted tools]
    PERM -->|No| DENY[Return denial to conversation]
    E --> F[Append tool results]
    DENY --> F
    F --> C
    D -->|No| I[Display response]
    I --> J{Next user action?}
    J -->|New message| B
    J -->|Exit| K([Session ends])
    E -.->|Error, cancellation or limit| STOP[Handle interruption or failure]
    style A fill:#6DB3F2,color:#222
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
    style B fill:#6DB3F2,color:#222
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
    style C fill:#6DB3F2,color:#222
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
    style D fill:#6DB3F2,color:#222
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
    style PERM fill:#6DB3F2,color:#222
    click PERM href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
    style E fill:#6DB3F2,color:#222
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
    style DENY fill:#6DB3F2,color:#222
    click DENY href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
    style F fill:#6DB3F2,color:#222
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
    style I fill:#6DB3F2,color:#222
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
    style J fill:#6DB3F2,color:#222
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
    style K fill:#6DB3F2,color:#222
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
    style STOP fill:#6DB3F2,color:#222
    click STOP href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "The master loop"
```

<details>
<summary>ASCII version</summary>

```
User input -> request context -> model
                    ^             |
                    |        tool calls?
                    |          Yes -> permissions -> execute or deny -> append result
                    +-------------------------------------------------------------+
                               No -> display response -> next message or exit
Errors, cancellation and limits can interrupt the loop.
Independent operations may run concurrently.
```

</details>

> **Source**: [The master loop](../core/architecture.md#1-the-master-loop)
>
> **Official reference**: [Documented agentic loop](https://code.claude.com/docs/en/how-claude-code-works#the-agentic-loop).

---

### Tool categories & selection

These six author-defined categories organize examples from the documented tool inventory. Availability varies by Claude Code version, model, surface and configuration; this is not a complete tool list or a native six-category taxonomy.

```mermaid
flowchart TD
    ROOT[Illustrative tool families] --> READ[Read and search<br/>Glob, Grep, Read]
    ROOT --> WRITE[Modify files<br/>Write, Edit, NotebookEdit]
    ROOT --> EXEC[Execute and delegate<br/>Bash, Agent]
    ROOT --> WEB[Web access<br/>WebSearch, WebFetch]
    ROOT --> TRACK[Track tasks when available<br/>TaskCreate, TaskGet,<br/>TaskList, TaskUpdate]
    ROOT --> CONTROL[Control workflow<br/>EnterPlanMode, ExitPlanMode,<br/>EnterWorktree, ExitWorktree,<br/>AskUserQuestion]
    style ROOT fill:#6DB3F2,color:#222
    click ROOT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "The tool arsenal"
    style READ fill:#6DB3F2,color:#222
    click READ href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "The tool arsenal"
    style WRITE fill:#6DB3F2,color:#222
    click WRITE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "The tool arsenal"
    style EXEC fill:#6DB3F2,color:#222
    click EXEC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "The tool arsenal"
    style WEB fill:#6DB3F2,color:#222
    click WEB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "The tool arsenal"
    style TRACK fill:#6DB3F2,color:#222
    click TRACK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "The tool arsenal"
    style CONTROL fill:#6DB3F2,color:#222
    click CONTROL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "The tool arsenal"
```

<details>
<summary>ASCII version</summary>

```
READ / SEARCH : Glob, Grep, Read
MODIFY        : Write, Edit, NotebookEdit
EXECUTE       : Bash, Agent
WEB           : WebSearch, WebFetch
TASK TRACKING : TaskCreate, TaskGet, TaskList, TaskUpdate when available
CONTROL       : EnterPlanMode / ExitPlanMode, EnterWorktree / ExitWorktree,
                AskUserQuestion

Illustrative families, not a complete or universally available inventory.
List directories through a shell command; consult the current tools reference.
```

</details>

> **Source**: [The tool arsenal](../core/architecture.md#2-the-tool-arsenal)
>
> **Official reference**: [Current tools and availability](https://code.claude.com/docs/en/tools-reference).
>
> TodoWrite is an alternative checklist tool in supported configurations, not a universally active default. Agent is the current subagent tool name; Task remains an alias in settings and definitions.

---

### System prompt assembly

This conceptual request diagram groups stable instructions with changing conversation context. It does not specify the exact internal assembly order, cache breakpoints or when every input is reread. Instruction files and memory may enter conversation context; MCP definitions can load on demand.

```mermaid
flowchart TD
    S[System instructions] --> REQ[Model request]
    T[Available tool definitions<br/>MCP definitions loaded as needed] --> REQ
    U[User and project instructions<br/>Relevant rules and auto memory] --> CTX[Conversation context]
    W[Relevant environment and file context] --> CTX
    H[User messages and tool results] --> CTX
    CTX --> REQ
    REQ --> API[Claude API or configured provider]
    NOTE[Cache reuse depends on stable prefixes<br/>and the provider contract] -.-> API
    style S fill:#6DB3F2,color:#222
    click S href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#system-prompt-contents" "System prompt contents"
    style T fill:#6DB3F2,color:#222
    click T href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#system-prompt-contents" "System prompt contents"
    style U fill:#6DB3F2,color:#222
    click U href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#system-prompt-contents" "System prompt contents"
    style W fill:#6DB3F2,color:#222
    click W href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#system-prompt-contents" "System prompt contents"
    style H fill:#6DB3F2,color:#222
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#system-prompt-contents" "System prompt contents"
    style CTX fill:#6DB3F2,color:#222
    click CTX href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#system-prompt-contents" "System prompt contents"
    style REQ fill:#6DB3F2,color:#222
    click REQ href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#system-prompt-contents" "System prompt contents"
    style API fill:#6DB3F2,color:#222
    click API href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#system-prompt-contents" "System prompt contents"
    style NOTE fill:#6DB3F2,color:#222
    click NOTE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#system-prompt-contents" "System prompt contents"
```

<details>
<summary>ASCII version</summary>

```
System instructions --------------------+
Available / loaded tool definitions -----+--> Model request -> configured provider
Conversation context --------------------+
  - relevant instruction files, rules and available memory
  - environment and file information
  - messages and tool results

Conceptual grouping; not the literal prompt order or cache layout.
Cache isolation and reuse follow the provider contract.
```

</details>

> **Source**: [System prompt contents](../core/architecture.md#system-prompt-contents)
>
> **Official reference**: [Context loading](https://code.claude.com/docs/en/how-claude-code-works#context-claude-code-adds-on-its-own) and [cache isolation](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#cache-storage-and-sharing).
>
> Public Anthropic API caches are not shared across organizations. Workspace isolation also applies on providers identified in the caching documentation. No cross-user or cross-organization reuse of private CLAUDE.md content is asserted.

---

### Sub-Agent context isolation

Conversation isolation and filesystem isolation are different boundaries. An ordinary subagent has fresh context; a fork inherits the parent conversation. Both return a final result while permitted operations may affect shared files or external services.

```mermaid
flowchart TD
    P[Parent conversation] --> A{Agent delegation type}
    A -->|Ordinary subagent| F[Fresh context<br/>Task prompt and agent definition]
    A -->|Fork| INHERIT[Inherited conversation<br/>Parent prompt, tools and history]
    F --> S[Subagent tool operations]
    INHERIT --> S
    S --> SHARE[Shared checkout or external services<br/>Effects remain visible]
    S --> WT[Optional isolation: worktree<br/>Separate repository checkout]
    SHARE --> RESULT[Final result enters parent context]
    WT --> RESULT
    RESULT --> P
    style P fill:#6DB3F2,color:#222
    click P href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#4-sub-agent-architecture" "Sub-agent architecture"
    style A fill:#6DB3F2,color:#222
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#4-sub-agent-architecture" "Sub-agent architecture"
    style F fill:#6DB3F2,color:#222
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#4-sub-agent-architecture" "Sub-agent architecture"
    style INHERIT fill:#6DB3F2,color:#222
    click INHERIT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#4-sub-agent-architecture" "Sub-agent architecture"
    style S fill:#6DB3F2,color:#222
    click S href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#4-sub-agent-architecture" "Sub-agent architecture"
    style SHARE fill:#6DB3F2,color:#222
    click SHARE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#4-sub-agent-architecture" "Sub-agent architecture"
    style WT fill:#6DB3F2,color:#222
    click WT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#4-sub-agent-architecture" "Sub-agent architecture"
    style RESULT fill:#6DB3F2,color:#222
    click RESULT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#4-sub-agent-architecture" "Sub-agent architecture"
```

<details>
<summary>ASCII version</summary>

```
Parent -> Agent
  ordinary -> fresh context with delegated task and definition
  fork     -> inherited parent conversation and configuration
       |
       +-> shared files and external services: permitted effects persist
       +-> optional worktree: separate checkout for repository edits
       |
       +-> final result enters parent context

Intermediate tool calls stay out of parent context.
A worktree does not isolate external services.
```

</details>

> **Source**: [Sub-agent architecture](../core/architecture.md#4-sub-agent-architecture)
>
> **Official reference**: [Fork context and optional worktree isolation](https://code.claude.com/docs/en/sub-agents#how-forks-differ-from-other-subagents).
