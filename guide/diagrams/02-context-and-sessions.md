---
title: "Claude Code — Context & Sessions Diagrams"
description: "Context zones, memory hierarchy, session management, and fresh context patterns"
tags: [context, sessions, memory, optimization]
---

# Context & Sessions

How Claude Code manages context, memory, and sessions across your work.

---

### Context Management Zones

Your context window has 4 distinct zones, each requiring different strategies. Knowing which zone you're in prevents context bloat and maintains response quality throughout long sessions.

```mermaid
flowchart LR
    subgraph GREEN["🟢 0–50% — Comfortable"]
        G1(Full capabilities<br/>available)
        G2(All tools active)
        G3(Rich responses)
    end

    subgraph BLUE["🔵 50–75% — Normal"]
        B1(Monitor usage)
        B2(Consider /compact<br/>for old threads)
        B3(Normal operation)
    end

    subgraph ORANGE["🟠 75–85% — Caution"]
        O1(Suggest /compact<br/>proactively)
        O2(Reduce verbosity)
        O3(Defer non-critical<br/>operations)
    end

    subgraph RED["🔴 85–100% — Critical"]
        R1(Auto-compact<br/>triggered at 80%)
        R2(Essential ops only)
        R3(Start new session<br/>for new tasks)
    end

    GREEN --> BLUE --> ORANGE --> RED

    style G1 fill:#7BC47F,color:#333
    style G2 fill:#7BC47F,color:#333
    style G3 fill:#7BC47F,color:#333
    style B1 fill:#6DB3F2,color:#fff
    style B2 fill:#6DB3F2,color:#fff
    style B3 fill:#6DB3F2,color:#fff
    style O1 fill:#E87E2F,color:#fff
    style O2 fill:#E87E2F,color:#fff
    style O3 fill:#E87E2F,color:#fff
    style R1 fill:#E85D5D,color:#fff
    style R2 fill:#E85D5D,color:#fff
    style R3 fill:#E85D5D,color:#fff

    click G1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "0-50%: Full capabilities"
    click G2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "0-50%: All tools active"
    click G3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "0-50%: Rich responses"
    click B1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "50-75%: Monitor usage"
    click B2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "50-75%: Consider /compact"
    click B3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "50-75%: Normal operation"
    click O1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "75-85%: Suggest /compact"
    click O2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "75-85%: Reduce verbosity"
    click O3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "75-85%: Defer non-critical"
    click R1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "85-100%: Auto-compact"
    click R2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "85-100%: Essential ops only"
    click R3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "85-100%: Start new session"
```

<details>
<summary>ASCII version</summary>

```
0%──────50%──────75%──85%──100%
│  Green  │  Blue  │ Orange│ Red│
│ Full    │ Normal │Suggest│Auto│
│ access  │Monitor │compact│cmp │
│         │        │Reduce │Ess.│
│         │        │verbos.│only│
```

</details>

> **Source**: [Context Management](../ultimate-guide.md#context-management) — Line ~1335

---

### Memory Hierarchy — 6 Types

Claude Code has 6 distinct memory types with different scopes and persistence. Knowing which memory type to use for each piece of information is key to effective sessions.

```mermaid
flowchart TD
    A["🌍 Global CLAUDE.md<br/>~/.claude/CLAUDE.md"] --> B["📁 Project CLAUDE.md<br/>/project-root/CLAUDE.md"]
    B --> C["📂 Subdirectory CLAUDE.md<br/>/src/CLAUDE.md, /tests/CLAUDE.md"]
    C --> AM["🧠 Auto-Memory Native<br/>~/.claude/projects/*/memory/MEMORY.md<br/>v2.1.59+"]
    AM --> D["💬 In-Conversation Context<br/>Messages + tool results this session"]
    D --> E["⚡ Ephemeral State<br/>MCP server state, tool cache"]

    A1["Scope: ALL projects<br/>Persists: Always<br/>Use: Global prefs, API keys"] --> A
    B1["Scope: This project<br/>Persists: Always<br/>Use: Project conventions"] --> B
    C1["Scope: This directory<br/>Persists: Always<br/>Use: Module-specific rules"] --> C
    AM1["Scope: Per project<br/>Persists: Cross-session<br/>Use: Auto-saved memories, /memory"] --> AM
    D1["Scope: This session<br/>Persists: Session only<br/>Use: Task context"] --> D
    E1["Scope: This session<br/>Persists: Session only<br/>Use: Computed results"] --> E

    style A fill:#E87E2F,color:#fff
    style B fill:#6DB3F2,color:#fff
    style C fill:#6DB3F2,color:#fff
    style AM fill:#7BC47F,color:#333
    style D fill:#F5E6D3,color:#333
    style E fill:#B8B8B8,color:#333
    style A1 fill:#B8B8B8,color:#333
    style B1 fill:#B8B8B8,color:#333
    style C1 fill:#B8B8B8,color:#333
    style AM1 fill:#B8B8B8,color:#333
    style D1 fill:#B8B8B8,color:#333
    style E1 fill:#B8B8B8,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Global CLAUDE.md"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Project CLAUDE.md"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Subdirectory CLAUDE.md"
    click AM href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Auto-Memory Native"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "In-Conversation Context"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#3-context-management-internals" "Ephemeral State"
    click A1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Global scope — always persists"
    click B1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Project scope — always persists"
    click C1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Directory scope — always persists"
    click AM1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Cross-session auto-memory"
    click D1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Session scope only"
    click E1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#3-context-management-internals" "Session scope only"
```

<details>
<summary>ASCII version</summary>

```
PERMANENT ──────────────────────────────── SESSION ONLY

~/.claude/CLAUDE.md              In-conversation context
      │                                      │
/project/CLAUDE.md               Ephemeral MCP state
      │
/subdir/CLAUDE.md
      │
Auto-Memory (MEMORY.md)  ← cross-session, per project

Higher = broader scope, always persists
Lower = narrower scope, survives restarts
Auto-Memory = persists cross-session, scoped per project
```

</details>

> **Source**: [Memory System](../ultimate-guide.md#memory-system) — Line ~3160 & ~3986 | Auto-Memory: v2.1.59+ (v3.30.0)

---

### Session Continuity — Saving and Resuming State

Sessions don't automatically persist context between terminals. This diagram shows how to save state and resume it in a new session or terminal, enabling async workflows.

```mermaid
sequenceDiagram
    participant U as User
    participant CC as Claude Code
    participant CM as CLAUDE.md
    participant NI as New Session

    U->>CC: Work on feature X
    CC->>CC: Executes tasks, tools
    U->>CC: Save progress to CLAUDE.md
    CC->>CM: Write: task status, decisions, next steps
    Note over CM: Persists after session ends

    U->>NI: Open new terminal
    U->>NI: claude (new session)
    NI->>CM: Auto-loads CLAUDE.md
    CM->>NI: Injects: saved context
    NI->>U: Ready — context restored ✓

    Note over CC,NI: Conversation history NOT restored<br/>Only CLAUDE.md content persists
```

<details>
<summary>ASCII version</summary>

```
Session 1                    CLAUDE.md         Session 2
─────────                    ─────────         ─────────
Work on task                    │               Open terminal
     │                          │                    │
Save progress ──────────────► Write             Load CLAUDE.md
                             status,           ◄── Auto-injected
                             decisions,
                             next steps
```

</details>

> **Source**: [Session Management](../ultimate-guide.md#session-management) — Line ~9477

---

### Fresh Context Anti-Pattern vs. Best Practice

Long sessions accumulate noise that degrades response quality. This diagram shows the degradation pattern and the recommended "focused sessions" approach that maintains performance.

```mermaid
flowchart TD
    subgraph BAD["❌ Anti-Pattern: Monolith Session"]
        B1([Start big session]) --> B2(Add task A)
        B2 --> B3(Add task B)
        B3 --> B4(Add task C)
        B4 --> B5{Context bloated<br/>>75%}
        B5 --> B6(Response quality<br/>degrades)
        B6 --> B7(Force-restart<br/>loses all context)
        style B1 fill:#E85D5D,color:#fff
        style B5 fill:#E85D5D,color:#fff
        style B6 fill:#E85D5D,color:#fff
        style B7 fill:#E85D5D,color:#fff
    end

    subgraph GOOD["✅ Best Practice: Focused Sessions"]
        G1([Start focused session]) --> G2(Complete task A)
        G2 --> G3{Natural<br/>checkpoint?}
        G3 -->|Yes| G4(Save to CLAUDE.md)
        G4 --> G5([New session for task B])
        G3 -->|No| G6{Context >75%?}
        G6 -->|Yes| G7(/compact)
        G7 --> G2
        G6 -->|No| G2
        style G1 fill:#7BC47F,color:#333
        style G4 fill:#7BC47F,color:#333
        style G5 fill:#7BC47F,color:#333
        style G3 fill:#E87E2F,color:#fff
        style G6 fill:#E87E2F,color:#fff
        style G7 fill:#6DB3F2,color:#fff
    end

    click B1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Anti-Pattern: Monolith Session"
    click B2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Add task A"
    click B3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Add task B"
    click B4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Add task C"
    click B5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Context bloated >75%"
    click B6 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Response quality degrades"
    click B7 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Force-restart — loses context"
    click G1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Best Practice: Focused Sessions"
    click G2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Complete task A"
    click G3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Natural checkpoint?"
    click G4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Save to CLAUDE.md"
    click G5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "New session for task B"
    click G6 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Context >75%?"
    click G7 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "/compact"
```

<details>
<summary>ASCII version</summary>

```
BAD: One giant session
Task A → Task B → Task C → Context bloat → Quality drop → Restart → Lost!

GOOD: Focused sessions
Task A ──► Checkpoint? ──Yes──► Save CLAUDE.md ──► New session for B
           │
           No
           │
         Context >75%? ──Yes──► /compact ──► Continue
           │
           No
           │
         Continue task
```

</details>

> **Source**: [Context Best Practices](../ultimate-guide.md#context-best-practices) — Line ~1525
