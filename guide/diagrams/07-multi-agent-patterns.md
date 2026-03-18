---
title: "Claude Code — Multi-Agent Patterns Diagrams"
description: "Agent topologies, worktrees, dual-instance planning, horizontal scaling, decision matrix"
tags: [multi-agent, patterns, worktrees, orchestration, scaling]
---

# Multi-Agent Patterns

Patterns for coordinating multiple Claude instances for parallel and complex work.

---

### Agent Teams — 3 Orchestration Topologies

Three proven topologies for multi-agent coordination. Choose based on task independence, ordering requirements, and specialization needs.

```mermaid
flowchart TD
    subgraph ORCH["Pattern 1: Orchestrator + Workers"]
        OL[Lead Orchestrator] --> OW1[Worker 1<br/>Frontend]
        OL --> OW2[Worker 2<br/>Backend]
        OL --> OW3[Worker 3<br/>Tests]
        OW1 & OW2 & OW3 --> OR([Results aggregated])
    end

    subgraph PIPE["Pattern 2: Pipeline"]
        PA[Agent A<br/>Requirements] --> PB[Agent B<br/>Implementation]
        PB --> PC[Agent C<br/>Review]
        PC --> PD([Final output])
    end

    subgraph ROUTE["Pattern 3: Specialist Router"]
        RR{Router Agent<br/>analyzes task} --> RC[Code Agent]
        RR --> RT[Test Agent]
        RR --> RD[Docs Agent]
        RC & RT & RD --> RO([Specialized result])
    end

    style OL fill:#E87E2F,color:#fff
    style OW1 fill:#6DB3F2,color:#fff
    style OW2 fill:#6DB3F2,color:#fff
    style OW3 fill:#6DB3F2,color:#fff
    style OR fill:#7BC47F,color:#333
    style PA fill:#F5E6D3,color:#333
    style PB fill:#F5E6D3,color:#333
    style PC fill:#F5E6D3,color:#333
    style PD fill:#7BC47F,color:#333
    style RR fill:#E87E2F,color:#fff
    style RC fill:#6DB3F2,color:#fff
    style RT fill:#6DB3F2,color:#fff
    style RD fill:#6DB3F2,color:#fff
    style RO fill:#7BC47F,color:#333

    click OL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Lead Orchestrator"
    click OW1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Worker: Frontend"
    click OW2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Worker: Backend"
    click OW3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Worker: Tests"
    click OR href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Results aggregated"
    click PA href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Agent A: Requirements"
    click PB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Agent B: Implementation"
    click PC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Agent C: Review"
    click PD href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Final output"
    click RR href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Router Agent"
    click RC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Code Agent"
    click RT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Test Agent"
    click RD href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Docs Agent"
    click RO href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Specialized result"
```

<details>
<summary>ASCII version</summary>

```
ORCHESTRATOR + WORKERS:      PIPELINE:               ROUTER:

   Lead Agent                Agent A (requirements)   Router
  /    |     \                    │                  /  |  \
W1    W2     W3              Agent B (implement)   Code Test Docs
  \   |     /                    │                  \  |  /
   Aggregate                Agent C (review)        Result
                                 │
                             Final output
```

</details>

> **Source**: [Agent Teams](../workflows/agent-teams.md) — Line ~59

---

### Git Worktree Multi-Instance Pattern

Git worktrees enable true parallel development: each Claude instance works in an isolated branch with its own working tree. No conflicts, no context mixing.

```mermaid
flowchart LR
    MB[(Main Branch<br/>git repository)] --> WA[git worktree add<br/>feature-A]
    MB --> WB[git worktree add<br/>feature-B]
    MB --> WC[git worktree add<br/>bugfix-C]

    WA --> CA[Claude Instance 1<br/>/worktrees/feature-A]
    WB --> CB[Claude Instance 2<br/>/worktrees/feature-B]
    WC --> CC[Claude Instance 3<br/>/worktrees/bugfix-C]

    CA --> CA1([Commits to feature-A])
    CB --> CB1([Commits to feature-B])
    CC --> CC1([Commits to bugfix-C])

    CA1 & CB1 & CC1 --> MERGE([Merge to main<br/>when ready])

    style MB fill:#E87E2F,color:#fff
    style CA fill:#6DB3F2,color:#fff
    style CB fill:#6DB3F2,color:#fff
    style CC fill:#6DB3F2,color:#fff
    style CA1 fill:#7BC47F,color:#333
    style CB1 fill:#7BC47F,color:#333
    style CC1 fill:#7BC47F,color:#333
    style MERGE fill:#7BC47F,color:#333
    style WA fill:#F5E6D3,color:#333
    style WB fill:#F5E6D3,color:#333
    style WC fill:#F5E6D3,color:#333

    click MB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Main Branch"
    click WA href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Worktree: feature-A"
    click WB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Worktree: feature-B"
    click WC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Worktree: bugfix-C"
    click CA href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Claude Instance 1"
    click CB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Claude Instance 2"
    click CC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Claude Instance 3"
    click CA1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Commits to feature-A"
    click CB1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Commits to feature-B"
    click CC1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Commits to bugfix-C"
    click MERGE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Merge to main"
```

<details>
<summary>ASCII version</summary>

```
Main repo
├── git worktree add feature-A → Claude 1 → commits to feature-A
├── git worktree add feature-B → Claude 2 → commits to feature-B
└── git worktree add bugfix-C  → Claude 3 → commits to bugfix-C

No conflicts: separate working trees, separate branches
All merge back to main when done
```

</details>

> **Source**: [Git Worktrees](../ultimate-guide.md#git-worktrees) — Line ~10634

---

### Dual-Instance Planning Pattern (Jon Williams)

Separating planning from execution using two Claude instances prevents costly mistakes: the planner Claude has no tools, so it can't accidentally execute anything during analysis.

```mermaid
sequenceDiagram
    participant U as User
    participant PL as Planner Claude<br/>(no tools)
    participant EX as Executor Claude<br/>(full tools)

    U->>PL: "Plan how to refactor auth module"
    Note over PL: Reads docs, analyzes requirements<br/>No execution risk — no tools

    PL->>U: Detailed plan:<br/>1. Files to change<br/>2. Order of operations<br/>3. Risk points<br/>4. Rollback strategy

    U->>U: Review plan carefully
    Note over U: Human checkpoint:<br/>approve or adjust

    U->>EX: "Execute this plan: [plan text]"
    EX->>EX: Implements step by step
    EX->>U: Progress updates + results

    Note over PL,EX: Key insight: planner can be<br/>more thorough without execution anxiety
```

<details>
<summary>ASCII version</summary>

```
User → Planner (no tools): "Plan X"
         │
    [safe analysis, no execution risk]
         │
Planner → User: detailed plan
         │
User reviews + approves
         │
User → Executor (full tools): "Execute: [plan]"
         │
    [implements with full context]
         │
Executor → User: results
```

</details>

> **Source**: [Dual-Instance Planning](../workflows/dual-instance-planning.md)

---

### Boris Cherny Horizontal Scaling Pattern

When tasks can be parallelized, spawn N Claude instances simultaneously instead of running them sequentially. The speedup is proportional to task independence.

```mermaid
flowchart LR
    BT([Large Task:<br/>Refactor 50 files]) --> DEC{Decompose<br/>into N subtasks}

    DEC --> T1["Subtask 1<br/>Files 1-10"]
    DEC --> T2["Subtask 2<br/>Files 11-20"]
    DEC --> T3["Subtask 3<br/>Files 21-30"]
    DEC --> TN["Subtask N<br/>..."]

    T1 --> CI1[Claude<br/>Instance 1]
    T2 --> CI2[Claude<br/>Instance 2]
    T3 --> CI3[Claude<br/>Instance 3]
    TN --> CIN[Claude<br/>Instance N]

    CI1 & CI2 & CI3 & CIN --> AGG(Aggregate<br/>results)
    AGG --> REV([Integration review<br/>~10x faster than sequential])

    style BT fill:#F5E6D3,color:#333
    style DEC fill:#E87E2F,color:#fff
    style CI1 fill:#6DB3F2,color:#fff
    style CI2 fill:#6DB3F2,color:#fff
    style CI3 fill:#6DB3F2,color:#fff
    style CIN fill:#6DB3F2,color:#fff
    style AGG fill:#B8B8B8,color:#333
    style REV fill:#7BC47F,color:#333

    click BT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Large Task"
    click DEC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Decompose into subtasks"
    click T1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Subtask 1"
    click T2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Subtask 2"
    click T3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Subtask 3"
    click TN href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Subtask N"
    click CI1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Claude Instance 1"
    click CI2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Claude Instance 2"
    click CI3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Claude Instance 3"
    click CIN href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Claude Instance N"
    click AGG href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Aggregate results"
    click REV href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Integration review"
```

<details>
<summary>ASCII version</summary>

```
Large task
     │
Decompose into N independent subtasks
     │
┌────┼────┐
│    │    │
I1  I2  I3... (parallel)
│    │    │
└────┼────┘
     │
Aggregate → Integration review
(~10x faster than sequential)
```

</details>

> **Source**: [Horizontal Scaling](../ultimate-guide.md#horizontal-scaling) — Line ~9617

---

### Multi-Instance Decision Matrix

Not every task needs multiple instances. This decision tree guides you to the right pattern based on task characteristics.

```mermaid
flowchart TD
    A([Task to complete]) --> B{Need multiple<br/>Claude instances?}
    B -->|No| C([Single session<br/>Standard usage])
    B -->|Yes| D{How many<br/>instances?}
    B -->|"Planning separation?"| B2{Need planning<br/>separation?}

    D -->|2-3| E{Need branch<br/>isolation?}
    E -->|Yes| F([Git worktrees<br/>Separate branches])
    E -->|No| G([Multiple terminals<br/>Same repo])

    D -->|4+| H{Task structure?}
    H -->|Independent tasks| I([Task tool<br/>Sub-agents in parallel])
    H -->|Sequential pipeline| J([Agent pipeline<br/>A → B → C])
    H -->|Mixed expertise| K([Specialist router<br/>Route by task type])

    B2 --> L([Dual-instance<br/>Planner + Executor])

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style D fill:#E87E2F,color:#fff
    style E fill:#E87E2F,color:#fff
    style H fill:#E87E2F,color:#fff
    style B2 fill:#E87E2F,color:#fff
    style C fill:#B8B8B8,color:#333
    style F fill:#7BC47F,color:#333
    style G fill:#7BC47F,color:#333
    style I fill:#7BC47F,color:#333
    style J fill:#7BC47F,color:#333
    style K fill:#7BC47F,color:#333
    style L fill:#6DB3F2,color:#fff

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Task to complete"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Need multiple instances?"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Single session"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "How many instances?"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Need branch isolation?"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "Git worktrees"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Multiple terminals"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "Task structure?"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Task tool sub-agents"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Agent pipeline"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "Specialist router"
    click B2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "Need planning separation?"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "Dual-instance: Planner + Executor"
```

<details>
<summary>ASCII version</summary>

```
Need multiple instances?
├─ No → Single session
├─ Yes → How many?
│        ├─ 2-3 → Need branch isolation?
│        │        ├─ Yes → Git worktrees
│        │        └─ No  → Multiple terminals
│        └─ 4+  → Task structure?
│                 ├─ Independent → Task tool (parallel sub-agents)
│                 ├─ Sequential  → Agent pipeline A→B→C
│                 └─ Mixed       → Specialist router
└─ Planning separation? → Dual-instance (Planner + Executor)
```

</details>

> **Source**: [Multi-Instance Patterns](../ultimate-guide.md#multi-instance-patterns) — Line ~11176
