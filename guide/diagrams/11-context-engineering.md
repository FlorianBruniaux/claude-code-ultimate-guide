---
title: "Claude Code — Context Engineering Diagrams"
description: "3-layer context system, adherence degradation, modular architecture, rule placement decision tree"
tags: [context-engineering, configuration, architecture, modular, adherence]
---

# Context Engineering

How to fill Claude's context window with the right information at the right time — and how architectural choices determine whether Claude consistently follows your conventions.

> "Context engineering is the art of filling the context window with the right information at the right time." — Andrej Karpathy

---

### The 3-Layer Context System

Context engineering operates across 3 distinct layers with different scopes and persistence. Understanding which layer to use prevents the most common mistake: cramming everything into one file.

```mermaid
flowchart TD
    subgraph GLOBAL["🌍 Layer 1: Global — ~/.claude/CLAUDE.md"]
        G1["Identity & tone preferences"]
        G2["Universal tool preferences"]
        G3["Cross-project coding conventions"]
        G4["Target: under 200 lines"]
    end

    subgraph PROJECT["📁 Layer 2: Project — ./CLAUDE.md + path modules"]
        P1["Stack & architecture decisions"]
        P2["Team conventions + deployment rules"]
        P3["Path-scoped @imports for subsystems"]
        P4["Target: under 150 lines (root) + modules"]
    end

    subgraph SESSION["⚡ Layer 3: Session — inline instructions, /add, flags"]
        S1["One-off task constraints"]
        S2["Temporary overrides"]
        S3["Ephemeral — not persisted after session"]
    end

    GLOBAL --> PROJECT --> SESSION

    OVR["Override order: Session > Project > Global<br/>More specific beats less specific<br/>Later-declared beats earlier at same level"] -.-> SESSION

    style G1 fill:#E87E2F,color:#fff
    style G2 fill:#E87E2F,color:#fff
    style G3 fill:#E87E2F,color:#fff
    style G4 fill:#B8B8B8,color:#333
    style P1 fill:#6DB3F2,color:#fff
    style P2 fill:#6DB3F2,color:#fff
    style P3 fill:#6DB3F2,color:#fff
    style P4 fill:#B8B8B8,color:#333
    style S1 fill:#F5E6D3,color:#333
    style S2 fill:#F5E6D3,color:#333
    style S3 fill:#B8B8B8,color:#333
    style OVR fill:#7BC47F,color:#333

    click G1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Identity & tone"
    click G2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Universal tools"
    click G3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Cross-project conventions"
    click G4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Target: under 200 lines"
    click P1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Stack & architecture"
    click P2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Team conventions"
    click P3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Path-scoped imports"
    click P4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "Target: under 150 lines"
    click S1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "One-off constraints"
    click S2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Temporary overrides"
    click S3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Ephemeral"
    click OVR href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Override semantics"
```

<details>
<summary>ASCII version</summary>

```
GLOBAL ~/.claude/CLAUDE.md     → Identity, universal tools, cross-project conventions (<200 lines)
    │ overridden by ↓
PROJECT ./CLAUDE.md + modules  → Stack, architecture, team rules, path-scoped @imports (<150 lines root)
    │ overridden by ↓
SESSION inline / /add / flags  → One-off constraints, temporary overrides (ephemeral)

Override order: Session > Project > Global
More specific beats less specific at the same level
```

</details>

> **Source**: [Context Engineering — Configuration Hierarchy](../core/context-engineering.md#3-configuration-hierarchy)

---

### Context Budget & Adherence Degradation

Adherence to CLAUDE.md rules degrades predictably as file size grows. Beyond ~150 rules, models begin selectively ignoring instructions. Path-scoping is the primary fix — it reduces always-on context by 40-50% without losing coverage.

```mermaid
flowchart LR
    subgraph ZONES["Adherence by CLAUDE.md lines"]
        Z1["1–100 lines<br/>~95% adherence ✓"]
        Z2["100–200 lines<br/>~88% adherence"]
        Z3["200–400 lines<br/>~75% adherence ⚠️"]
        Z4["400–600 lines<br/>~60% adherence"]
        Z5["600+ lines<br/>~45% and falling ✗"]
    end

    Z1 --> Z2 --> Z3 --> Z4 --> Z5

    FIX["✅ Path-scoping fix:<br/>Root CLAUDE.md: shared rules only (~2K tokens)<br/>Per subsystem: module loaded on demand<br/>Result: 40–50% always-on reduction<br/>Adherence stays in green zone"] -.-> Z1

    SIGNALS["🔴 Signs of context overload:<br/>Rule silencing (80% followed, some ignored)<br/>Contradictory behavior across files<br/>Generic outputs instead of project-specific<br/>Slow first responses"] -.-> Z5

    style Z1 fill:#7BC47F,color:#333
    style Z2 fill:#7BC47F,color:#333
    style Z3 fill:#E87E2F,color:#fff
    style Z4 fill:#E85D5D,color:#fff
    style Z5 fill:#E85D5D,color:#fff
    style FIX fill:#7BC47F,color:#333
    style SIGNALS fill:#E85D5D,color:#fff

    click Z1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "1-100 lines: ~95%"
    click Z2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "100-200 lines: ~88%"
    click Z3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "200-400 lines: ~75%"
    click Z4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "400-600 lines: ~60%"
    click Z5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "600+ lines: ~45%"
    click FIX href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "Path-scoping fix"
    click SIGNALS href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "Signs of overload"
```

<details>
<summary>ASCII version</summary>

```
Lines in CLAUDE.md    Adherence    Status
──────────────────    ─────────    ──────
1 – 100               ~95%         ✓ Green zone
100 – 200             ~88%         ✓ Acceptable
200 – 400             ~75%         ⚠️ Caution
400 – 600             ~60%         ✗ Degraded
600+                  ~45% ↓       ✗ Critical

Fix: path-scope by subsystem → root CLAUDE.md stays <150 lines
Result: 40-50% always-on context reduction, adherence back in green zone
```

</details>

> **Source**: [Context Budget](../core/context-engineering.md#2-the-context-budget) — Adherence data: HumanLayer production data (15-25% improvement with structured context)

---

### Monolithic vs. Modular Architecture

The monolithic CLAUDE.md is the most common failure mode in team contexts. Path-scoped modules fix it by loading only what's relevant for the current task.

```mermaid
flowchart TD
    subgraph BAD["❌ Anti-Pattern: Monolithic CLAUDE.md"]
        B1(["CLAUDE.md (600 lines)<br/>API rules + DB rules + UI rules<br/>+ Deploy rules — all mixed together"])
        B2("All 600 lines loaded<br/>for every session, every file")
        B3("Rules 1–20 get ~95% attention<br/>Rules 500+ get ~30% attention")
        B4(["Adherence degrades continuously"])
        B1 --> B2 --> B3 --> B4
        style B1 fill:#E85D5D,color:#fff
        style B2 fill:#E85D5D,color:#fff
        style B3 fill:#E87E2F,color:#fff
        style B4 fill:#E85D5D,color:#fff
    end

    subgraph GOOD["✅ Best Practice: Path-Scoped Modules"]
        G1(["CLAUDE.md root (~100 lines)<br/>Shared rules only + @import declarations"])
        G2["src/api/CLAUDE-api.md<br/>Loaded ONLY when in src/api/"]
        G3["src/components/CLAUDE-components.md<br/>Loaded ONLY when in src/components/"]
        G4["prisma/CLAUDE-db.md<br/>Loaded ONLY when in prisma/"]
        G5(["Each module: full coverage<br/>Always-on: 40–50% smaller"])
        G1 --> G2
        G1 --> G3
        G1 --> G4
        G2 & G3 & G4 --> G5
        style G1 fill:#7BC47F,color:#333
        style G2 fill:#6DB3F2,color:#fff
        style G3 fill:#6DB3F2,color:#fff
        style G4 fill:#6DB3F2,color:#fff
        style G5 fill:#7BC47F,color:#333
    end

    click B1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "Anti-pattern: monolith"
    click B4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "Adherence degradation"
    click G1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "Root CLAUDE.md"
    click G2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "API module"
    click G3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "Components module"
    click G4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "DB module"
    click G5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "Result: coverage with less bloat"
```

<details>
<summary>ASCII version</summary>

```
BAD: CLAUDE.md (600 lines, everything mixed)
  → All 600 lines loaded every session
  → Rules 500+ get ~30% attention weight
  → Adherence degrades continuously

GOOD: Root CLAUDE.md (~100 lines, shared only)
  + src/api/CLAUDE-api.md      ← loaded only when editing API files
  + src/components/CLAUDE-*.md ← loaded only when editing components
  + prisma/CLAUDE-db.md        ← loaded only when editing DB files

Result: 40-50% reduction in always-on tokens, full coverage per subsystem
```

</details>

> **Source**: [Modular Architecture](../core/context-engineering.md#4-modular-architecture) — Path-scoping pattern

---

### Rule Placement Decision Tree

Every new instruction or convention needs to land in the right layer. Wrong placement wastes tokens (too global) or loses coverage (too scoped). This tree makes the decision explicit.

```mermaid
flowchart TD
    A([New rule or instruction to place]) --> B{Relevant to\nevery project\nyou work on?}
    B -->|Yes| C([Global CLAUDE.md<br/>~/.claude/CLAUDE.md])

    B -->|No| D{Specific to\ncertain files\nor subsystems?}
    D -->|Yes| E([Path-scoped module<br/>e.g. src/api/CLAUDE-api.md])

    D -->|No| F{Procedural<br/>step-by-step\nworkflow?}
    F -->|Yes: how to do something| G([Skill file<br/>.claude/skills/task-name.md<br/>Loaded on demand, not always-on])

    F -->|No: constraint or standard| H{Applies to<br/>whole project?}
    H -->|Yes| I([Project CLAUDE.md root<br/>./CLAUDE.md])
    H -->|No: one task only| J([Session inline instruction<br/>Tell Claude directly this session])

    RULE["Rule of thumb:<br/>If you write it more than once<br/>it belongs in a permanent layer"] -.-> J

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style D fill:#E87E2F,color:#fff
    style F fill:#E87E2F,color:#fff
    style H fill:#E87E2F,color:#fff
    style C fill:#E87E2F,color:#fff
    style E fill:#6DB3F2,color:#fff
    style G fill:#6DB3F2,color:#fff
    style I fill:#6DB3F2,color:#fff
    style J fill:#F5E6D3,color:#333
    style RULE fill:#7BC47F,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "New rule to place"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Relevant to every project?"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Global CLAUDE.md"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "Specific to certain files?"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "Path-scoped module"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "Procedural workflow?"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Skill file"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Whole project?"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Project CLAUDE.md root"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Session inline"
    click RULE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "Rule of thumb"
```

<details>
<summary>ASCII version</summary>

```
New rule to place
│
Relevant to every project? ──Yes──► Global CLAUDE.md (~/.claude/CLAUDE.md)
│ No
Specific to certain files/subsystems? ──Yes──► Path-scoped module (src/area/CLAUDE-area.md)
│ No
Procedural step-by-step? ──Yes──► Skill file (.claude/skills/) [loaded on demand]
│ No
Applies to whole project? ──Yes──► Project CLAUDE.md root (./CLAUDE.md)
│ No
└──► Session inline instruction (ephemeral)

Rule of thumb: if you say it more than once, promote it to a permanent layer.
```

</details>

> **Source**: [Rule Placement](../core/context-engineering.md#3-configuration-hierarchy) — Decision tree from §3
