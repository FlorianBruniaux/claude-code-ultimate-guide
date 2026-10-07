---
title: "Claude Code: Multi-Agent Patterns Diagrams"
description: "Conceptual topologies, isolated worktrees, planning, delegation and messaging"
tags: [multi-agent, patterns, worktrees, orchestration, scaling]
---

# Multi-agent patterns

Coordinate independent work with clear ownership and integration checks. Native features, conceptual patterns and measured outcomes are distinct.

---

### Agent teams: Conceptual orchestration topologies

Orchestrator, pipeline and specialist routing are conceptual patterns, not three native Agent Teams modes. Native Agent Teams uses a lead and communicating teammates; it is experimental and disabled by default. It adds coordination and token cost. Sequential tasks and edits to the same files often suit a single session or focused subagents better.

```mermaid
flowchart TD
    CHOOSE["Choose a coordination pattern"] --> ORCH["Orchestrator + workers<br/>Native teams: lead + teammates<br/>Experimental, opt-in"]
    CHOOSE --> PIPE["Pipeline pattern<br/>Stages depend on prior results"]
    CHOOSE --> ROUTE["Specialist routing pattern<br/>Choose worker by task"]
    ORCH --> FRONT["Worker owns frontend files"]
    ORCH --> BACK["Worker owns backend files"]
    FRONT --> INTEG["Lead integrates and verifies"]
    BACK --> INTEG
    PIPE --> REQ["Requirements"]
    REQ --> IMPL["Implementation"]
    IMPL --> REVIEW["Review against criteria"]
    ROUTE --> SELECT{"Needed expertise?"}
    SELECT --> CODE["Code worker"]
    SELECT --> TEST["Test worker"]
    SELECT --> DOC["Documentation worker"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click CHOOSE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click ORCH href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click PIPE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click ROUTE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click FRONT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click BACK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click INTEG href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click REQ href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click IMPL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click REVIEW href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click SELECT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click CODE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click TEST href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click DOC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
```

<details>
<summary>ASCII version</summary>

```
Conceptual coordination patterns
├─ Orchestrator → workers with explicit ownership → integration checks
│  Native Agent Teams: lead + communicating teammates, experimental opt-in
├─ Pipeline → requirements → implementation → review
│  Workflow pattern; often a single session or subagents suffices
└─ Router → needed specialist (code / tests / docs)
   Workflow pattern, not a dedicated native team mode

Teams cost more tokens and require coordination.
```

</details>

> **Source**: [Guide: Agent teams: Conceptual orchestration topologies](../workflows/agent-teams.md); [Agent Teams availability and trade-offs](https://code.claude.com/docs/en/agent-teams)

---

### Git worktree multi-instance pattern

Worktrees give concurrent instances separate checked-out files and branches. Some repository metadata remains shared, and integrating their changes can still produce merge conflicts. Commands below assume the cloned repository root; each command creates the displayed path.

```mermaid
flowchart TD
    REPO["Repository root"] --> WA["git worktree add -b feature-A<br/>../worktrees/feature-A"]
    REPO --> WB["git worktree add -b feature-B<br/>../worktrees/feature-B"]
    REPO --> WC["git worktree add -b bugfix-C<br/>../worktrees/bugfix-C"]
    WA --> CA["Claude 1: ../worktrees/feature-A<br/>Commits to feature-A"]
    WB --> CB["Claude 2: ../worktrees/feature-B<br/>Commits to feature-B"]
    WC --> CC["Claude 3: ../worktrees/bugfix-C<br/>Commits to bugfix-C"]
    CA --> INTEGRATE["Integrate changes<br/>Resolve conflicts if present"]
    CB --> INTEGRATE
    CC --> INTEGRATE
    INTEGRATE --> CHECK["Run integration checks and review"]
    CHECK --> MERGE["Merge when criteria pass"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click REPO href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click WA href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click WB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click WC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click CA href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click CB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click CC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click INTEGRATE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click CHECK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click MERGE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
```

<details>
<summary>ASCII version</summary>

```
From the cloned repository root:
git worktree add -b feature-A ../worktrees/feature-A
git worktree add -b feature-B ../worktrees/feature-B
git worktree add -b bugfix-C ../worktrees/bugfix-C

Each path → its Claude instance → commits on its own branch
         → integrate → resolve conflicts if present
         → integration checks + review → merge

Separate working files; shared repository metadata.
Concurrent editing is isolated, merge conflicts remain possible.
```

</details>

> **Source**: [Guide: Git worktree multi-instance pattern](../ultimate-guide.md#912-git-best-practices--workflows); [Git worktree semantics](https://git-scm.com/docs/git-worktree)

---

### Dual-Instance planning pattern

Use two sessions when a separate planning boundary is useful. A planner with no tools needs the relevant documents supplied in its prompt. Alternatively, Plan mode permits exploration with restricted actions. Configure the restriction explicitly; launching a second session does not disable tools. The executor needs the approved plan and required context, rather than inheriting the planner conversation automatically.

```mermaid
flowchart TD
    DOCS["User supplies requirements<br/>and relevant documents"] --> PLANNER["Planner session<br/>No tools explicitly configured<br/>or restricted Plan mode"]
    PLANNER --> PLAN["Plan: files, steps, checks<br/>and rollback constraints"]
    PLAN --> REVIEW{"Human approves?"}
    REVIEW -->|No| PLANNER
    REVIEW -->|Yes| TRANSFER["Transfer approved plan<br/>and required context"]
    TRANSFER --> EXEC["Executor session<br/>Configured tool permissions"]
    EXEC --> VERIFY["Run checks and compare with plan"]
    VERIFY --> REPORT["Report results and evidence limits"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click DOCS href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click PLANNER href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click PLAN href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click REVIEW href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click TRANSFER href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click EXEC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click VERIFY href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click REPORT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
```

<details>
<summary>ASCII version</summary>

```
Supplied documents → planner
                     (explicit no-tools configuration,
                      or restricted Plan mode for exploration)
                   → plan → human review
                            ├─ Revise → planner
                            └─ Approve → transfer plan + required context
                                       → executor with configured tools
                                       → checks + result report

Two sessions alone do not enforce tool restrictions or transfer context.
```

</details>

> **Source**: [Guide: Dual-Instance planning pattern](../workflows/dual-instance-planning.md); [Plan permission mode](https://code.claude.com/docs/en/permissions), [Subagent tool restrictions](https://code.claude.com/docs/en/sub-agents)

---

### Horizontal scaling pattern

Parallelize independent work with explicit file ownership, then measure the result after coordination and integration. More instances do not guarantee proportional speedup; costs and dependencies can outweigh the benefit. Measure speedup and cost on the workload before making a performance claim.

```mermaid
flowchart TD
    TASK["Large task"] --> SPLIT["Identify independent subtasks<br/>and file ownership"]
    SPLIT --> A["Worker A<br/>Owned files and criteria"]
    SPLIT --> B["Worker B<br/>Owned files and criteria"]
    SPLIT --> C["Worker C<br/>Owned files and criteria"]
    A --> AGG["Aggregate outputs and evidence"]
    B --> AGG
    C --> AGG
    AGG --> REVIEW["Resolve dependencies/conflicts<br/>and run integration checks"]
    REVIEW --> MEASURE["Measure elapsed benefit and token cost<br/>for this workload"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click TASK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click SPLIT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click AGG href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click REVIEW href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click MEASURE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
```

<details>
<summary>ASCII version</summary>

```
Large task → independent subtasks with explicit ownership
            → parallel workers A / B / C
            → aggregate evidence
            → resolve dependencies and conflicts
            → integration checks
            → measure elapsed benefit and token cost

No guaranteed multiplier; coordination reduces gains.
```

</details>

> **Source**: [Guide: Horizontal scaling pattern](../ultimate-guide.md#917-scaling-patterns-multi-instance-workflows); [Team size, cost and diminishing returns](https://code.claude.com/docs/en/agent-teams)

---

### Multi-Instance decision matrix

Choose by dependency, communication and isolation needs before choosing a worker count. The native delegation tool is Agent; Task was its former name and remains a compatibility alias in settings and definitions. There is no four-instance prerequisite for using subagents.

```mermaid
flowchart TD
    TASK["Task to complete"] --> INDEP{"Independent work worth delegating?"}
    INDEP -->|No| SINGLE["Single session<br/>Plan and execute stages as needed"]
    INDEP -->|Yes| COMM{"Workers need discussion<br/>and shared coordination?"}
    COMM -->|No| SUB["Agent tool<br/>Focused subagents return results<br/>Former name: Task"]
    COMM -->|Yes| TEAM["Experimental Agent Teams<br/>Lead + communicating teammates"]
    SUB --> EDIT{"Concurrent file edits?"}
    TEAM --> EDIT
    EDIT -->|Yes| WT["Separate ownership<br/>Worktrees for checkout isolation"]
    EDIT -->|No| READ["Parallel research or review"]
    WT --> SIZE["Choose size by task independence<br/>cost and coordination"]
    READ --> SIZE
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click TASK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click INDEP href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click SINGLE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click COMM href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click SUB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click TEAM href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click EDIT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click WT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click READ href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click SIZE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
```

<details>
<summary>ASCII version</summary>

```
Worth delegating independent work?
├─ No → single session, stages as needed
└─ Yes → need peer discussion / shared coordination?
         ├─ No → Agent tool subagents return results
         │       (Task is the historical compatibility alias)
         └─ Yes → experimental Agent Teams
                    │
         Concurrent file edits?
         ├─ Yes → file ownership + separate worktrees
         └─ No → parallel research/review
                    │
         Size by independence, cost and coordination, not a 4+ rule.
```

</details>

> **Source**: [Guide: Multi-Instance decision matrix](../ultimate-guide.md#917-scaling-patterns-multi-instance-workflows); [Agent tool rename and delegation](https://code.claude.com/docs/en/sub-agents), [Teams versus subagents](https://code.claude.com/docs/en/agent-teams)

---

### Cross-Session messaging: Discovery & delivery

Eligible independent sessions can discover peers with ListAgents and send text with SendMessage. Same-machine delivery uses local sockets or named pipes; other-machine and cloud delivery uses Anthropic infrastructure. Explicit crossSessionInbound hold retains messages until an applicable accept releases them. Approval dialogs belong to some permission-mode defaults in supported terminals, not to the explicit hold setting. Availability depends on version, provider and Remote Control requirements.

```mermaid
flowchart TD
    SESSIONS["Eligible sessions<br/>Bind inbox and register locally"] --> LIST["ListAgents / list-agents<br/>Reachable peers and agents"]
    LIST --> SEND["SendMessage text<br/>Target identified"]
    SEND --> WHERE{"Target location?"}
    WHERE -->|Same machine| LOCAL["Unix socket / named pipe<br/>Local delivery"]
    WHERE -->|Other machine or cloud| REMOTE["Anthropic infrastructure<br/>Remote Control or cloud session"]
    LOCAL --> SETTING{"Explicit inbound setting?"}
    REMOTE --> SETTING
    SETTING -->|accept| DELIVER["Delivered to receiving Claude"]
    SETTING -->|hold| HOLD["Undelivered<br/>Later applicable accept releases"]
    SETTING -->|refuse| DROP["Dropped"]
    SETTING -->|Unset| DEFAULT["Permission-mode default<br/>Deliver or hold for approval<br/>where dialog is supported"]
    DEFAULT --> DELIVER
    DEFAULT --> WAIT["Approval/default-held queue<br/>Subject to surface and expiry"]
    DELIVER --> BOUND["Recipient permissions still apply<br/>Peer text cannot approve permissions<br/>or authorize config changes"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click SESSIONS href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click LIST href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click SEND href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click WHERE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click LOCAL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click REMOTE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click SETTING href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click DELIVER href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click HOLD href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click DROP href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click DEFAULT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click WAIT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click BOUND href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
```

<details>
<summary>ASCII version</summary>

```
Eligible sessions → registry/inbox → ListAgents → SendMessage
Target location?
├─ Same machine → Unix socket / named pipe, local delivery
└─ Other machine/cloud → Anthropic infrastructure
                               │
Explicit crossSessionInbound?
├─ accept → delivered
├─ hold   → undelivered; later applicable accept releases
├─ refuse → dropped
└─ unset  → mode-dependent default
            ├─ deliver
            └─ approval hold, depending on terminal/surface and expiry

Peer text does not approve permissions or authorize configuration changes.
Version/provider/Remote Control requirements govern availability.
```

</details>

> **Source**: [Guide: Cross-Session messaging: Discovery & delivery](../workflows/cross-session-messaging.md); [Messaging controls and availability](https://code.claude.com/docs/en/cross-session-messaging)
