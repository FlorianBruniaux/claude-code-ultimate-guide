---
title: "Claude Code: Context Engineering Diagrams"
description: "Instruction scopes, context budget checks, conditional rules, rule placement"
tags: [context-engineering, configuration, architecture, modular, adherence]
---

# Context Engineering

Load relevant instructions and evidence, then measure whether Claude follows the required constraints on real tasks. Shorter context alone does not prove better results.

---

### The 3-layer context system

This teaching view separates global, project and session instructions. It is not a complete inventory of organization policy, auto memory or runtime tool context. Instruction files become model context, not enforced security settings.

```mermaid
flowchart TD
    G[Global: ~/.claude/CLAUDE.md<br/>Cross-project preferences] --> P
    P[Project: ./CLAUDE.md or .claude/CLAUDE.md<br/>Shared stack and conventions] --> S
    S[Session: task instructions<br/>Recorded in the conversation]
    P --> R[Conditional rules<br/>.claude/rules/*.md with paths]
    P --> I[Root @imports<br/>Expanded at launch]
    R --> T[Load on matching Read, Write or Edit]
    O[Organization managed settings<br/>Enforced policy is a separate mechanism] -.-> P
    C[Instructions concatenate<br/>Remove conflicts; no guaranteed override order] -.-> S

    classDef diagramNode fill:#F5E6D3,color:#333,stroke:#A64B00
    class G,P,S,R,I,T,O,C diagramNode
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click P href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click S href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click R href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click T href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click O href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
```

<details>
<summary>ASCII version</summary>

```text
GLOBAL: ~/.claude/CLAUDE.md -> cross-project preferences
PROJECT: ./CLAUDE.md or .claude/CLAUDE.md -> shared stack and conventions
SESSION: task instructions -> recorded in the conversation

Root @imports -> expanded at launch
.claude/rules/*.md + paths -> conditional Read/Write/Edit loading
Instructions concatenate; keep them consistent
Organization managed settings -> separate enforced policy mechanism
Session instructions do not become durable project/global policy
```

</details>

> **Source**: [Configuration hierarchy](../core/context-engineering.md#3-configuration-hierarchy)

> Native loading distinguishes imports from conditional rules. Conflicting instruction text has no guaranteed override order. [Instruction loading](https://code.claude.com/docs/en/memory#how-claude-md-files-load), [Imports](https://code.claude.com/docs/en/memory#import-additional-files), [Conditional rules](https://code.claude.com/docs/en/memory#path-specific-rules).

> `/add-dir` extends working-directory access for the session; it is not an instruction-import command. [Command reference](https://code.claude.com/docs/en/commands).


---

### Context budget & adherence checks

There is no universal adherence percentage for a given line count. Review relevance and conflicts, measure the context actually loaded, then compare violations and task outcomes before and after a change.

```mermaid
flowchart LR
    A[Inventory loaded instructions] --> B[Find irrelevant or conflicting rules]
    B --> C[Keep shared instructions concise]
    C --> D[Scope subsystem rules to matching files]
    D --> E[Replay representative acceptance checks]
    E --> F[Compare loaded context, violations and rework]
    F --> G([Keep the change only when the evidence supports it])

    classDef diagramNode fill:#F5E6D3,color:#333,stroke:#A64B00
    class A,B,C,D,E,F,G diagramNode
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "View in guide"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "View in guide"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "View in guide"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "View in guide"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "View in guide"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "View in guide"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#2-the-context-budget" "View in guide"
```

<details>
<summary>ASCII version</summary>

```text
Inventory loaded instructions
  -> review irrelevant/conflicting rules
  -> concise shared instructions
  -> scope subsystem rules
  -> replay representative acceptance checks
  -> compare context size, violations and rework
  -> keep changes supported by evidence

No fixed adherence curve or universal context-reduction gain is asserted
```

</details>

> **Source**: [The context budget](../core/context-engineering.md#2-the-context-budget)

> Anthropic recommends short, organized and consistent CLAUDE.md files, with a target under 200 lines per file. This is guidance, not a guaranteed adherence rate. Imports help organization but still load context. [Writing effective instructions](https://code.claude.com/docs/en/memory#write-effective-instructions).


---

### Monolithic vs. modular architecture

Move subsystem-specific instructions out of an always-loaded root into native conditional rules or nested CLAUDE.md files. Splitting root imports into more files changes organization but does not itself reduce startup context.

```mermaid
flowchart TD
    A[Always-loaded root<br/>API, DB, UI and deployment rules mixed] --> B[Every task receives irrelevant subsystem context]
    C[Concise root CLAUDE.md<br/>Shared instructions only] --> D[.claude/rules/api.md<br/>paths: src/api/**]
    C --> E[.claude/rules/ui.md<br/>paths: src/components/**]
    C --> F[.claude/rules/db.md<br/>paths: prisma/**]
    D --> G[Load when matching files are read, written or edited]
    E --> G
    F --> G
    H[Alternative: src/api/CLAUDE.md<br/>Native nested instruction file] --> G
    G --> I([Measure loaded context and task adherence])
    J[Root @imports load at launch<br/>No automatic token reduction] -.-> C

    classDef diagramNode fill:#F5E6D3,color:#333,stroke:#A64B00
    class A,B,C,D,E,F,G,H,I,J diagramNode
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "View in guide"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "View in guide"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "View in guide"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "View in guide"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "View in guide"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "View in guide"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "View in guide"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "View in guide"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "View in guide"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "View in guide"
```

<details>
<summary>ASCII version</summary>

```text
Always-loaded monolith -> irrelevant subsystem rules on every task

Concise root CLAUDE.md: shared instructions
  .claude/rules/api.md [paths: src/api/**]
  .claude/rules/ui.md  [paths: src/components/**]
  .claude/rules/db.md  [paths: prisma/**]
    -> load on matching Read/Write/Edit
Alternative: src/api/CLAUDE.md -> loads when that subtree is accessed

Root @imports expand at launch
Measure context and adherence; no fixed percentage gain is promised
```

</details>

> **Source**: [Modular architecture](../core/context-engineering.md#4-modular-architecture)

> Arbitrary names such as `CLAUDE-api.md` are not automatically discovered as nested instruction files. Use the native names or a conditional rules file. [Native project-memory loading and rules](https://code.claude.com/docs/en/memory).


---

### Rule placement decision tree

Decide whether a requirement needs enforcement before choosing the scope of its instructional text. A skill provides reusable guidance; a permission rule, hook, script or CI gate must implement and verify any required hard stop.

```mermaid
flowchart TD
    A([New instruction or requirement]) --> B{Requires an enforced stop,<br/>ordering or retries?}
    B -->|Yes| C[Managed permission or sandbox policy,<br/>hook, script, CI or workflow<br/>Test the enforcement]
    B -->|No| D{Reusable procedure,<br/>reference or judgment?}
    D -->|Yes| E[Skill directory<br/>SKILL.md loaded when invoked or relevant]
    D -->|No| F{Relevant across projects?}
    F -->|Yes| G[User CLAUDE.md<br/>Cross-project guidance]
    F -->|No| H{Specific files or subsystem?}
    H -->|Yes| I[.claude/rules/area.md with paths<br/>or nested area/CLAUDE.md]
    H -->|No| J{Stable project guidance?}
    J -->|Yes| K[Project root CLAUDE.md]
    J -->|No| L[Session instruction]
    M[Repeated and stable content<br/>is a candidate for a durable layer] -.-> L

    classDef diagramNode fill:#F5E6D3,color:#333,stroke:#A64B00
    class A,B,C,D,E,F,G,H,I,J,K,L,M diagramNode
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#72-creating-hooks" "View in guide"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "View in guide"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "View in guide"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#4-modular-architecture" "View in guide"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "View in guide"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
    click M href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/context-engineering.md#3-configuration-hierarchy" "View in guide"
```

<details>
<summary>ASCII version</summary>

```text
Needs an enforced stop/order/retries?
  Yes -> managed permissions/sandbox, hook/script/CI/workflow; test it
  No -> reusable procedure/reference/judgment?
    Yes -> skill
    No -> cross-project? -> user CLAUDE.md
      Otherwise -> subsystem? -> rules file with paths or nested CLAUDE.md
        Otherwise -> stable project guidance? -> root CLAUDE.md
          Otherwise -> session instruction

Repeated AND stable content is a candidate for a durable layer
```

</details>

> **Source**: [Configuration hierarchy](../core/context-engineering.md#3-configuration-hierarchy)

> Instruction text shapes model behavior; it does not replace enforcement. Hook decisions and permissions have their own behavior and scope. [Hooks](https://code.claude.com/docs/en/hooks), [Permissions and sandboxing](https://code.claude.com/docs/en/permissions#how-permissions-interact-with-sandboxing).
