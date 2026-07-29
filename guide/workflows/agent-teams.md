---
title: "Agent Teams Workflow"
description: "Multi-agent parallel coordination for complex tasks with autonomous team lead"
tags: [workflow, agents, architecture]
---

# Agent Teams Workflow

> **Multi-agent parallel coordination for complex tasks**
> **Status**: Experimental (v2.1.32+) | **Model**: Opus 5 required (Opus 4.6+ compatible) | **Flag**: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

**What**: Multiple Claude instances work in parallel on a shared codebase, coordinating autonomously without active human intervention. One session acts as team lead to break down tasks and synthesize findings from teammates.

**When introduced**: v2.1.32 (2026-02-05) as research preview
**Reading time**: ~30 min
**Prerequisites**: Opus 5 model (Opus 4.6+ compatible), understanding of [Sub-Agents](#split-role-sub-agents), familiarity with Task Tool

**🚀 Want to get started fast?** See **[Agent Teams Quick Start Guide](./agent-teams-quick-start.md)** (8-10 min, copy-paste patterns for your projects)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture Deep-Dive](#2-architecture-deep-dive)
3. [Setup & Configuration](#3-setup--configuration)
4. [Production Use Cases](#4-production-use-cases)
5. [Workflow Impact Analysis](#5-workflow-impact-analysis)
6. [Limitations & Gotchas](#6-limitations--gotchas)
7. [Decision Framework](#7-decision-framework)
8. [Best Practices](#8-best-practices)
9. [Troubleshooting](#9-troubleshooting)
10. [Sources](#10-sources)

---

## 1. Overview

### What Are Agent Teams?

Agent teams enable **multiple Claude instances to work in parallel** on different subtasks while coordinating through a git-based system. Unlike manual multi-instance workflows where you orchestrate separate Claude sessions yourself, agent teams provide built-in coordination where agents claim tasks, merge changes continuously, and resolve conflicts automatically.

**Key characteristics**:
- ✅ **Autonomous coordination** — Team lead delegates, teammates communicate via mailbox
- ✅ **Peer-to-peer messaging** — Direct communication between agents (not just hierarchical)
- ✅ **Git-based locking** — Agents claim tasks by writing to shared directory
- ✅ **Continuous merge** — Changes pulled/pushed without manual intervention
- ✅ **Independent context** — Each agent has own 1M token context window (isolated)
- ⚠️ **Experimental** — Research preview, stability not guaranteed
- ⚠️ **Token-intensive** — Multiple simultaneous model calls = high cost

### When Introduced

**Version**: v2.1.32 (2026-02-05)
**Model**: Opus 5 required (Opus 4.6+ compatible)
**Status**: Research preview (experimental feature flag required)

**Official announcement**:
> "We've introduced agent teams in Claude Code as a research preview. You can now spin up multiple agents that work in parallel as a team and coordinate autonomously on shared codebases."
> — [Anthropic, Introducing Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6)

> **📝 Documentation Update (2026-02-09)**: Architecture section corrected based on [Addy Osmani's research](https://addyosmani.com/blog/claude-code-agent-teams/). Key clarification: Agents communicate via **peer-to-peer messaging** through a mailbox system, not only through team lead synthesis. Context windows remain isolated (1M tokens per agent), but explicit messaging enables direct coordination between teammates.

### Agent Teams vs Other Patterns

| Pattern | Coordination | Setup | Best For |
|---------|--------------|-------|----------|
| **Agent Teams** | Automatic (built-in) | Experimental flag | Complex read-heavy tasks requiring coordination |
| **Multi-Instance** | Manual (human orchestration) | Multiple terminals | Independent parallel tasks, no coordination needed |
| **Dual-Instance** | Manual (human oversight) | 2 terminals | Quality assurance, plan-execute separation |
| **Task Tool** | Automatic (sub-agents) | Native feature | Single-agent task delegation, sequential work |

**Key distinction**:
- **Multi-Instance** = You manage coordination (separate projects, no shared state)
- **Agent Teams** = Claude manages coordination (shared codebase, git-based communication)

---

## 📊 Industry Adoption Data (Anthropic 2026)

> **Source**: [2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)

### Enterprise Adoption Timeline

Agent teams represent the evolution from "single agent" to "coordinated teams" pattern documented by Anthropic across 5000+ organizations:

| Adoption Phase | Timeline | Characteristics | Success Rate |
|---------------|----------|-----------------|--------------|
| **Pilot** | Month 1-2 | 1-2 teams, experimental flag | 60-70% |
| **Expansion** | Month 3-4 | 3-5 teams, process refinement | 75-85% |
| **Production** | Month 5-6 | Team-wide, integrated CI/CD | 85-90% |

**Critical success factors**:
- ✅ Modular architecture (enables parallel work without conflicts)
- ✅ Comprehensive tests (agents verify changes autonomously)
- ✅ Clear task decomposition (well-defined subtask boundaries)
- ❌ **Blocker**: Monolithic codebase, weak test coverage

### Real-World Performance

**Fountain** (frontline workforce platform):
- **50% faster screening** via hierarchical multi-agent orchestration
- **40% faster onboarding** for new fulfillment centers
- **2x candidate conversions** through automated workflows
- **Timeline compression**: Staffing new center from 1+ week → 72 hours

**Anthropic Internal** (from research team):
- **67% more PRs merged** per engineer per day
- **0-20% "fully delegated"** tasks (collaboration remains central)
- **27% new work** (tasks wouldn't be done without AI)

### Anti-Patterns Observed

| Anti-Pattern | Symptom | Fix |
|-------------|---------|-----|
| **Too many agents** | >5 agents = coordination overhead > productivity | Start 2-3, scale progressively |
| **Over-delegation** | Context switching cost exceeds gains | Active human oversight on critical decisions |
| **Premature automation** | Automating workflow not mastered manually | Manual → Semi-auto → Full-auto (progressive) |

### When Large Teams ARE Justified

The ">5 agents" rule above is a sensible default, but it breaks down in specific scenarios where the math favors larger teams. The real question is not "how many agents?" but "is the coordination overhead less costly than the context overflow?"

**Context window as the deciding factor**: A single Claude Code agent on a 50K+ line codebase fills 80-90% of its context window just loading the relevant files (source: atcyrus.com). At that point, the agent has almost no room left for reasoning. Splitting across multiple agents keeps each one at ~40% context usage, which leaves headroom for actual problem-solving.

| Scenario | Single Agent | 3-Agent Team | 5-Agent Team |
|----------|-------------|--------------|--------------|
| 10K line codebase | ~30% context, comfortable | Overkill | Overkill |
| 50K line codebase | 80-90% context, degraded reasoning | Ideal split | Justified if truly parallel modules |
| 100K+ line codebase | Context overflow, agent misses files | May still overflow per agent | Justified, consider even more |

**When more agents make sense**:
- Independent modules with zero shared state (no coordination overhead to pay)
- Parallel refactoring across isolated file trees (frontend vs backend vs infra)
- Read-heavy analysis where each agent covers a different subsystem
- The codebase physically cannot fit in one agent's context with room to spare

**When more agents hurt**: If agents constantly need to read each other's output or modify shared files, adding agents adds merge conflicts and coordination messages that eat into the very context you were trying to save.

> **Note on model selection per role**: As of March 2026, all agents in a team run the same model (Opus 5, required for Agent Teams). The community has requested role-based model selection where the team lead runs Opus for planning, implementation agents run Sonnet for speed, and test agents run Haiku for cost efficiency. This is not yet supported. The current workaround is spawning separate Claude Code processes with explicit `--model` flags, but you lose the built-in coordination and shared task list. Track this as a community feature request.

For broader industry context: Gartner predicts 40% of enterprise applications will incorporate task-specific agents by end of 2026. The team coordination patterns being established now in Claude Code and similar tools will likely become standard practice.

### Cost-Benefit Analysis

**Agent Teams** vs **Multi-Instance Manual**:

| Aspect | Agent Teams | Multi-Instance (Manual) |
|--------|-------------|------------------------|
| **Setup time** | 30-60 min (flag + git config) | 5-10 min (new terminals) |
| **Coordination** | Automatic (git-based) | Manual (human orchestration) |
| **Token cost** | High (continuous messaging) | Medium (isolated sessions) |
| **Best for** | Complex read-heavy tasks | Independent parallel features |
| **Adoption timeline** | 3-6 months to production | 1-2 months to proficiency |

**When Agent Teams win**: Complex refactoring, large-scale analysis, coordinated multi-file changes
**When Multi-Instance wins**: Independent features, prototype exploration, simple parallelization

---

## 2. Architecture Deep-Dive

### Lead-Teammate Architecture

```
┌─────────────────────────────────────────────────┐
│         Team Lead (Main Session)                │
│  - Breaks tasks into subtasks                   │
│  - Spawns teammate sessions                     │
│  - Synthesizes findings from all agents         │
│  - Coordinates via shared task list + mailbox   │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌───────▼────────┐
│  Teammate 1    │◄─┼────────────────►│  Teammate 2    │
│                │  │ Peer-to-peer    │                │
│ - Own context  │  │ messaging via   │ - Own context  │
│   (1M tokens)  │  │ mailbox system  │   (1M tokens)  │
│ - Claims tasks │  │                 │ - Claims tasks │
│ - Messages     │  │                 │ - Messages     │
│   team/peers   │  │                 │   team/peers   │
└────────────────┘  └─────────────────┘────────────────┘
```

### Git-Based Coordination

**How it works**:

1. **Task claiming**: Agents write lock files to shared directory (`.claude/tasks/`)
2. **Work execution**: Each agent works independently in its context
3. **Continuous merge**: Agents pull/push changes to shared git repository
4. **Conflict resolution**: Automatic merge (with limitations, see [§6](#6-limitations--gotchas))
5. **Result synthesis**: Team lead collects findings and presents unified response

**Example lock file structure**:
```
.claude/tasks/
├── task-1.lock        # Agent A claimed
├── task-2.lock        # Agent B claimed
└── task-3.pending     # Not yet claimed
```

### Communication Architecture

**Key distinction from sub-agents**: Agent teams implement **true peer-to-peer messaging** via a mailbox system, not just hierarchical reporting.

**Architecture components** (Source: [Addy Osmani](https://addyosmani.com/blog/claude-code-agent-teams/), Feb 2026):

1. **Team lead**: Creates team, spawns teammates, coordinates work
2. **Teammates**: Independent Claude Code instances with own context (1M tokens each)
3. **Task list**: Shared work items with dependency tracking and auto-unblocking
4. **Mailbox**: Inbox-based messaging system enabling direct communication between agents

**Communication patterns**:
- **Lead → Teammate**: Direct messages or broadcasts to all
- **Teammate → Lead**: Progress updates, questions, findings
- **Teammate ↔ Teammate**: Direct peer-to-peer messaging (challenge approaches, debate solutions)
- **Final synthesis**: Team lead aggregates all findings for user

**Example messaging flow**:
```
Team Lead: "Review this PR for security issues"
├─ Teammate 1 (Security): Analyzes → Messages Teammate 2: "Found auth issue in line 45"
├─ Teammate 2 (Code Quality): Reviews → Messages back: "Confirmed, also see OWASP violation"
└─ Team Lead: Synthesizes findings → Presents unified response to user
```

**What this enables**:
- ✅ Agents actively challenge each other's approaches
- ✅ Debate solutions without human intervention
- ✅ Coordinate independently (self-organization)
- ✅ Share discoveries mid-workflow (via messages, not context)

**Limitation**: Context isolation remains—agents don't share their full context window, only explicit messages.

### Navigation Between Agents

**Built-in navigation**:
- **Shift+Down**: Cycle through teammates in in-process mode
- **tmux/iTerm2**: Split pane mode with `teammateMode: "tmux"` (requires tmux or iTerm2 with `it2` CLI)
- **Direct takeover**: You can take control of any agent's work when needed

**Example**:
```bash
# Terminal 1: Team lead (with env var set)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude

# Claude spawns teammates automatically
# You can navigate with Shift+Down to cycle through teammates (in-process mode)
```

### Context Management

**Per-agent context**:
- Each agent has **1M token context window** (Opus 5)
- ~30,000 lines of code per session
- **Context isolation**: Agents don't share their full context window
- **Communication**: Via mailbox system (peer-to-peer + team lead synthesis)

**Total context capacity** (3 agents example):
- Team lead: 1M tokens
- Teammate 1: 1M tokens
- Teammate 2: 1M tokens
- **Total**: 3M tokens across team (context isolated, but communicating via messages)

**Important distinction**:
- ❌ **Context NOT shared**: Agent 1's full 1M token context invisible to Agent 2
- ✅ **Messages ARE shared**: Agents send explicit messages via mailbox (findings, questions, debates)

---

## 3. Setup & Configuration

### Prerequisites

**Required**:
- ✅ Claude Code v2.1.32 or later
- ✅ Opus 5 model (`/model opus`)
- ✅ Git repository (for coordination)

**Recommended**:
- ✅ Understanding of [Sub-Agents](#split-role-sub-agents)
- ✅ Familiarity with git workflows
- ✅ Budget awareness (token-intensive feature)

### Method 1: Environment Variable

**Simplest approach** — Set env var before starting Claude Code:

```bash
# Enable agent teams for this session
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Start Claude Code
claude
```

**Persistent setup** (bash/zsh):
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1' >> ~/.bashrc
source ~/.bashrc
```

### Method 2: Settings File

**Persistent configuration** — Edit `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**Advantages**:
- ✅ Persistent across sessions
- ✅ No need to remember env var
- ✅ Can be version-controlled in dotfiles

**After editing**, restart Claude Code for changes to take effect.

### Verification

**Check if enabled**:

```bash
# In Claude Code session
> Are agent teams enabled?
```

Claude should confirm:
> "Yes, agent teams are enabled (experimental feature). I can spawn multiple agents to work in parallel when appropriate."

**Alternative verification** (check env var):
```bash
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
# Should output: 1
```

### Multi-Terminal Setup

**Pattern** (from practitioner reports):

```bash
# Terminal 1: Research + bugfix
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude

# Terminal 2: Business ops
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude

# Terminal 3: Infrastructure
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

**Benefits**:
- Isolation of contexts (research vs execution vs setup)
- Parallel progress on independent workstreams
- Reduced context switching cognitive load

**Note**: This is different from automatic teammate spawning — here you're manually creating multiple team lead sessions. Each can spawn its own teammates.

---

## 4. Production Use Cases

### Overview of Validated Cases

| Use Case | Source | Metrics | Best For |
|----------|--------|---------|----------|
| **Multi-layer code review** | Fountain (Anthropic Report) | 50% faster screening | Security + API + Frontend simultaneous review |
| **Full dev lifecycle** | CRED (Anthropic Report) | 2x execution speed | 15M users, financial services compliance |
| **Autonomous C compiler** | Anthropic Research | Project completion | Complex multi-phase projects |
| **Job search app** | Paul Rayner (LinkedIn) | "Pretty impressive" | Design research + bug fixing |
| **Business ops automation** | Paul Rayner (LinkedIn) | N/A | Operating system + conference planning |

### 4.1 Multi-Layer Code Review (Fountain)

**Organization**: Fountain (frontline workforce management platform)
**Challenge**: Comprehensive codebase review across multiple concerns (security, API design, frontend)
**Solution**: Deployed hierarchical multi-agent orchestration with scope-focused sub-agents

**Agent scopes** (Fountain's approach):
- **Scope 1 (Security)**: Scan for vulnerabilities, auth issues, data exposure
- **Scope 2 (API)**: Review endpoint design, request/response validation, error handling
- **Scope 3 (Frontend)**: Check UI patterns, accessibility, performance

**Results**:
- ✅ **50% faster** candidate screening
- ✅ **40% quicker** onboarding
- ✅ **2x candidate conversions**

**Why it worked**:
- **Read-heavy task**: Code review = primarily reading/analyzing (no write conflicts)
- **Clear domain separation**: Security, API, Frontend have minimal overlap
- **Independent analysis**: Each agent can work without waiting for others

**Example prompt** (team lead):
```
Review this PR comprehensively with scope-focused analysis:
- Security Scope: Check for vulnerabilities and auth issues (context: auth code, input validation)
- API Design Scope: Review endpoint design and error handling (context: API routes, controllers)
- Frontend Scope: Check UI patterns and accessibility (context: components, styles)

PR: https://github.com/company/repo/pull/123
```

**Source**: [2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf), Anthropic, Jan 2026

### 4.2 Full Development Lifecycle (CRED)

**Organization**: CRED (15M+ users, financial services, India)
**Challenge**: Accelerate delivery while maintaining quality standards essential for financial services
**Solution**: Implemented Claude Code across entire development lifecycle with agent teams for complex tasks

**Results**:
- ✅ **2x execution speed** across development lifecycle
- ✅ Maintained compliance (financial services standards)
- ✅ Quality assurance preserved

**Why it worked**:
- **Large codebase**: 15M users = complex system requiring parallel analysis
- **Quality critical**: Financial services = need multiple validation layers
- **Tight deadlines**: Speed requirement justified token cost

**Workflow pattern**:
1. **Planning phase**: Team lead breaks down feature
2. **Implementation**: Teammate 1 = backend, Teammate 2 = frontend, Teammate 3 = tests
3. **Quality assurance**: Team lead synthesizes + runs validation
4. **Compliance check**: Final review against financial standards

**Source**: [2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf), Anthropic, Jan 2026

### 4.3 Autonomous C Compiler (Anthropic Research)

**Project**: Build an entire C compiler autonomously
**Challenge**: Multi-phase project (lexer, parser, AST, code generation, optimization) requiring coordination
**Solution**: Agent teams with task decomposition and progress tracking

**Phases completed**:
1. **Lexer**: Tokenization logic
2. **Parser**: Syntax tree construction
3. **AST**: Abstract syntax tree implementation
4. **Code generation**: Assembly output
5. **Optimization**: Performance improvements
6. **Testing**: Compiler test suite

**Results**:
- ✅ **Project completed** without human intervention
- ✅ All phases coordinated successfully
- ✅ Tests passing at completion

**Why it worked**:
- **Clear phases**: Each compiler phase is well-defined (lexer → parser → codegen)
- **Minimal dependencies**: Phases have clear interfaces (tokens → AST → assembly)
- **Testable milestones**: Each phase verifiable independently

**Architecture insight**:
> "Individual agents break the project into small pieces, track progress, and determine next steps until completion."
> — [Building a C compiler with agent teams](https://www.anthropic.com/engineering/building-c-compiler), Anthropic Engineering, Feb 2026

**Key learnings**:
- ⚠️ **Tests passing ≠ correctness**: Human oversight still important for quality assurance
- ⚠️ **Verification required**: Automated success doesn't guarantee error-free code
- ✅ **Feasibility proven**: Complex multi-phase projects achievable with agent teams

**Source**: [Building a C compiler with agent teams](https://www.anthropic.com/engineering/building-c-compiler), Anthropic Engineering, Feb 2026

### 4.4 Job Search App Development (Paul Rayner)

**Practitioner**: Paul Rayner (CEO Virtual Genius, EventStorming Handbook author, Explore DDD founder)
**Setup**: 3 concurrent agent team sessions across separate terminals
**Date**: Feb 2026 (v2.1.32 release day)

**Workflow 1 - Job Search App**:
- **Context**: Custom job search application development
- **Tasks**:
  - Design options research (explore UI/UX patterns)
  - Bug fixing in existing codebase
- **Pattern**: Research + execution in same workflow

**Workflow 2 - Business Operations**:
- **Context**: Operating system development + conference planning
- **Tasks**:
  - Business operating system automation
  - Conference planning resources (Explore DDD)
- **Pattern**: Multi-domain business tooling

**Workflow 3 - Infrastructure + Framework**:
- **Context**: Testing infrastructure + framework integration
- **Tasks**:
  - Playwright MCP instances setup
  - Beads framework management (Steve Yegge)
- **Pattern**: Infrastructure + framework coordination

**Results**:
- ✅ "Pretty impressive" (subjective, no metrics)
- ✅ Better than previous multi-terminal workflows without coordination
- ✅ 3 independent contexts running simultaneously

**Why notable**:
- **Real-world validation**: Production usage by experienced practitioner
- **Multi-context**: 3 different domains (product, business, infra) simultaneously
- **Early adoption**: Posted same day as v2.1.32 release (early adopter signal)

**Open question raised**:
> "I'm not sure about Claude's guidance on when to use beads versus agent team sessions. Any thoughts?"
> — Paul Rayner, LinkedIn, Feb 2026

**Source**: [Paul Rayner LinkedIn](https://www.linkedin.com/posts/thepaulrayner_this-is-wild-i-just-upgraded-claude-code-activity-7425635159678414850-MNyv), Feb 2026

### 4.5 Parallel Hypothesis Testing (Pattern)

**Scenario**: Debugging a complex production issue with multiple potential root causes

**Setup**:
```
Team lead prompt:
"Production API is slow. Test these hypotheses in parallel:
- Hypothesis 1 (DB): Query performance issue
- Hypothesis 2 (Network): Latency spikes
- Hypothesis 3 (Cache): Invalidation problem
Each agent: profile, reproduce, report findings"
```

**Agent assignments**:
- **Agent 1**: Database profiling (slow query log, explain plans)
- **Agent 2**: Network analysis (latency metrics, trace routes)
- **Agent 3**: Cache behavior (hit rates, invalidation patterns)

**Benefits**:
- ✅ **Parallel investigation**: 3 hypotheses tested simultaneously (vs sequential)
- ✅ **Time savings**: 1/3 of sequential debugging time
- ✅ **Comprehensive**: No hypothesis ignored due to time constraints

**When to use**:
- Multiple plausible explanations for observed behavior
- Each hypothesis testable independently
- Time-critical debugging (production issues)

### 4.6 Large-Scale Refactoring (Pattern)

**Scenario**: Refactor authentication system across 47 files (frontend + backend + tests)

**Setup**:
```
Team lead prompt:
"Refactor auth system from JWT to OAuth2:
- Agent 1: Backend endpoints (/api/auth/*)
- Agent 2: Frontend components (src/components/auth/*)
- Agent 3: Integration tests (tests/auth/)
Coordinate changes via shared interfaces"
```

**Agent assignments**:
- **Agent 1**: Backend implementation (15 files)
- **Agent 2**: Frontend UI update (20 files)
- **Agent 3**: Test suite update (12 files)

**Benefits**:
- ✅ **Context preservation**: All 47 files in one coordinated session (vs losing context after ~15)
- ✅ **Interface consistency**: Shared contracts enforced across agents
- ✅ **Atomic migration**: All layers updated in coordination

**Gotcha**:
- ⚠️ **Merge conflicts**: If agents modify same files (e.g., shared types)
- ⚠️ **Mitigation**: Clear interface boundaries, minimize shared file modifications

---

## 5. Workflow Impact Analysis

### Before/After Comparison

**Context**: What changes when using agent teams vs single-agent sessions?

| Task | Single Agent (Before) | Agent Teams (After) |
|------|-----------------------|---------------------|
| **Bug tracing** | Feed files one by one, re-explain architecture each time | See entire codebase at once, trace full data flow across all layers |
| **Code review** | Manually summarize PR yourself, explain context in prompt | Feed entire diff + surrounding code, agents read directly |
| **New feature** | Describe codebase structure in prompt (limited by your understanding) | Let agents read codebase directly, discover patterns themselves |
| **Refactoring** | Lose context after ~15 files, split into multiple sessions | All 47+ files live in one coordinated session |
| **Multi-service debugging** | Debug one service at a time, manually track cross-service flows | Parallel investigation across all involved services |

**Source**: [Claude Opus 4.6 for Developers](https://dev.to/thegdsks/claude-opus-46-for-developers-agent-teams-1m-context-and-what-actually-matters-4h8c), dev.to, Feb 2026

### Context Management Improvements

**Single agent limitations**:
- ~15 files before context management becomes challenging
- Manual summarization required for large codebases
- Sequential analysis of independent components

**Agent teams capabilities**:
- **1M tokens per agent** = ~30,000 lines of code
- **3 agents** = effectively 90,000 lines across team (isolated contexts)
- **Parallel reading**: Agents consume codebase sections simultaneously
- **Synthesis**: Team lead combines findings without context loss

**Example**:
```
Scenario: Analyze 28,000-line TypeScript service

Single agent:
- Read files sequentially
- Context pressure at ~15 files
- Manual summarization
- ~2-3 hours

Agent teams:
- Agent 1: Controllers layer (10K lines)
- Agent 2: Services layer (10K lines)
- Agent 3: Data layer (8K lines)
- Team lead: Synthesize architecture
- ~45 minutes
```

### Coordination Benefits

**Built-in vs manual coordination**:

| Aspect | Manual Multi-Instance | Agent Teams |
|--------|----------------------|-------------|
| **Task delegation** | You decide splits | Team lead decides |
| **Progress tracking** | Manual check-ins | Automatic reporting |
| **Merge conflicts** | You resolve | Automatic (with limitations) |
| **Context sharing** | Copy-paste findings | Git-based coordination |
| **Cognitive load** | High (orchestrator role) | Low (observer role) |

**When coordination matters**:
- ✅ Tasks with dependencies (Feature A needs API from Feature B)
- ✅ Shared interfaces (multiple agents modify same contract)
- ✅ Quality gates (all agents must pass before merge)

**When coordination unnecessary**:
- ❌ Completely independent tasks (separate projects)
- ❌ No shared state (different repositories)
- ❌ Simple parallelization (run same script on different data)

### Cost Trade-offs

**Token consumption comparison** (estimated):

| Workflow | Single Agent | Agent Teams (3) | Multiplier |
|----------|-------------|-----------------|------------|
| **Code review (small PR)** | 10K tokens | 25K tokens | 2.5x |
| **Code review (large PR)** | 50K tokens | 90K tokens | 1.8x |
| **Bug investigation** | 30K tokens | 70K tokens | 2.3x |
| **Feature implementation** | 100K tokens | 200K tokens | 2x |
| **Refactoring (large)** | 150K tokens | 250K tokens | 1.7x |

**Cost justification scenarios**:
- ✅ **Time-critical**: Production issues requiring fast resolution
- ✅ **Complexity**: Multi-layer analysis (security + performance + architecture)
- ✅ **Quality**: High-stakes changes requiring multiple verification layers
- ❌ **Simple tasks**: Straightforward implementations (overkill)
- ❌ **Budget-constrained**: Personal projects with tight token limits

**Rule of thumb**: Agent teams justified when time saved > 2x token cost increase.

---

## 6. Limitations & Gotchas

### Read-Heavy vs Write-Heavy Trade-off

**Core limitation**: Agent teams excel at read-heavy tasks but struggle with write-heavy tasks where multiple agents modify the same files.

**Why this matters**:
```
Read-heavy (✅ Good for teams):
- Code review: Agents read code, provide analysis
- Bug tracing: Agents read logs, trace execution
- Architecture analysis: Agents read structure, identify patterns

Write-heavy (⚠️ Risky for teams):
- Refactoring shared types: Multiple agents modify same file → merge conflicts
- Database schema changes: Coordinated migrations across files
- API contract updates: Interface changes require synchronization
```

**Mitigation strategies**:
1. **Clear boundaries**: Assign non-overlapping file sets to agents
2. **Interface-first**: Define contracts before parallel implementation
3. **Single-writer pattern**: One agent writes shared files, others read only
4. **Human review**: Manually resolve merge conflicts when they occur

### Merge Conflict Scenarios

**Automatic resolution works**:
- ✅ Different files modified by different agents
- ✅ Different functions in same file (clean git merges)
- ✅ Additive changes (new functions, no edits)

**Automatic resolution struggles**:
- ❌ Same lines modified (classic merge conflict)
- ❌ Conflicting logic (Agent A removes validation, Agent B adds it)
- ❌ Circular dependencies (Agent A needs Agent B's output, vice versa)

**Example conflict**:
```typescript
// Agent 1 changes:
function processUser(user: User) {
  validateEmail(user.email); // Added validation
  return save(user);
}

// Agent 2 changes (same time):
function processUser(user: User) {
  return save(sanitize(user)); // Added sanitization
}

// Conflict: Both modified same function
// Resolution: Human decides order (validate → sanitize → save)
```

### Token Intensity Implications

**Why token-intensive**:
- Each agent runs **separate model inference** (3 agents = 3x base cost)
- Context loading for each agent (1M tokens × 3 = 3M token capacity)
- Coordination overhead (team lead synthesis)

**Budget impact example** (Opus 5 pricing):
```
Single agent session:
- Input: 50K tokens @ $5/M = $0.25
- Output: 5K tokens @ $25/M = $0.13
- Total: $0.38

Agent teams (3 agents):
- Input: 150K tokens @ $5/M = $0.75
- Output: 15K tokens @ $25/M = $0.38
- Total: $1.13

Cost multiplier: 3x
```

**Justification required**:
- ✅ Time saved > cost increase (production issues)
- ✅ Quality critical (financial services, healthcare)
- ✅ Complexity justifies parallelization (multi-layer analysis)
- ❌ Simple tasks (use single agent)
- ❌ Personal learning projects (budget-constrained)

### Experimental Status Caveats

**What "experimental" means**:
- ⚠️ **No stability guarantee**: Feature may change or be removed
- ⚠️ **Bugs expected**: Report issues to Anthropic (GitHub Issues)
- ⚠️ **Performance variability**: Coordination speed may fluctuate
- ⚠️ **Documentation evolving**: Official docs still minimal

**Production usage considerations**:
1. **Fallback plan**: Be ready to revert to single-agent if issues arise
2. **Monitoring**: Track token costs carefully (can escalate quickly)
3. **Validation**: Human review of agent team outputs (don't trust blindly)
4. **Feedback**: Report bugs/experiences to help Anthropic improve feature

**Practitioner reports** (as of Feb 2026):
- ✅ Paul Rayner: "Pretty impressive" (production usage validated)
- ✅ Fountain: 50% faster (deployed in production)
- ✅ CRED: 2x speed (15M users, financial services)
- ⚠️ Community: Mixed reports (some merge conflict issues)

### Context Isolation

**What agents can't do**:
- ❌ **Share context windows**: Agent 1's full context (1M tokens) not visible to Agent 2
- ❌ **Auto-sync discoveries**: Agent 2 won't see Agent 1's findings unless explicitly messaged
- ❌ **Coordinate timing**: Agents work independently, may finish at different times

**What agents CAN do**:
- ✅ **Send messages**: Via mailbox system (peer-to-peer or via team lead)
- ✅ **Challenge approaches**: Debate solutions, ask questions to each other
- ✅ **Share findings**: Explicit messaging (not automatic context sharing)

**Implications**:
```
Scenario: Agent 1 discovers critical bug that affects Agent 2's work

Without messaging:
- Agent 2 doesn't see Agent 1's discovery automatically
- Agent 2 may continue with flawed assumption

With messaging (built-in):
- Agent 1 messages Agent 2: "Found auth issue in line 45"
- Agent 2 adjusts approach based on message
- Team lead synthesizes all findings at end

Mitigation:
- Agents can message each other via mailbox system
- Team lead synthesizes findings after all agents complete
- Human can interrupt and redirect agents mid-workflow (Shift+Down to cycle teammates)
- Design tasks with minimal inter-agent dependencies
```

### When NOT to Use Agent Teams

**Single agent is better for**:
- ❌ **Simple tasks**: Straightforward implementations (overkill)
- ❌ **Small codebases**: <5 files affected (coordination overhead not justified)
- ❌ **Write-heavy tasks**: Lots of shared file modifications (merge conflict risk)
- ❌ **Sequential dependencies**: Task B requires Task A completion (no parallelization benefit)
- ❌ **Budget constraints**: Personal projects, learning (token cost multiplier)
- ❌ **Tight interdependencies**: Circular dependencies between tasks

**Example of poor fit**:
```
Task: Update authentication logic in shared auth.ts file

Why single agent better:
- One file modified (no parallelization benefit)
- Write-heavy (multiple changes to same file)
- No clear subtask boundaries (logic intertwined)
- Sequential flow (test after each change)

Result: Agent teams would create merge conflicts, no time savings
```

---

## 7. Decision Framework

### Teams vs Multi-Instance vs Dual-Instance

**Comparison table**:

| Criterion | Agent Teams | Multi-Instance | Dual-Instance |
|-----------|-------------|----------------|---------------|
| **Coordination** | Automatic (git-based + mailbox) | Manual (human) | Manual (human) |
| **Setup** | Experimental flag | Multiple terminals | 2 terminals |
| **Best for** | Read-heavy tasks needing coordination | Independent parallel tasks | Quality assurance (plan-execute split) |
| **Communication** | Peer-to-peer messaging + team lead synthesis | Manual copy-paste | Manual synchronization |
| **Context sharing** | Isolated (1M per agent, no auto-sync) | Isolated (separate sessions) | Isolated (2 sessions) |
| **Cost** | High (3x+ tokens) | Medium (2x tokens) | Medium (2x tokens) |
| **Cognitive load** | Low (observer) | High (orchestrator) | Medium (reviewer) |
| **Merge conflicts** | Automatic resolution (limited) | N/A (separate repos) | Manual resolution |
| **Maturity** | Experimental (v2.1.32+) | Stable | Stable |

### Decision Tree: When to Use Agent Teams

```
Start
  │
  ├─ Task is simple (<5 files)? ──YES──> Single agent
  │
  ├─ NO
  │
  ├─ Tasks completely independent? ──YES──> Multi-Instance
  │
  ├─ NO
  │
  ├─ Need quality assurance split? ──YES──> Dual-Instance
  │
  ├─ NO
  │
  ├─ Read-heavy (analysis, review)? ──YES──> Agent Teams ✓
  │
  ├─ NO
  │
  ├─ Write-heavy (many file mods)? ──YES──> Single agent
  │
  ├─ NO
  │
  ├─ Budget-constrained? ──YES──> Single agent
  │
  ├─ NO
  │
  └─ Complex coordination needed? ──YES──> Agent Teams ✓
                                   ──NO──> Single agent
```

### Use Case Mapping

**Agent Teams (✅ Use)**:
- Multi-layer code review (security + API + frontend)
- Parallel hypothesis testing (debugging)
- Large-scale refactoring (clear boundaries)
- Full codebase analysis (architecture review)
- Complex feature research (explore multiple approaches)

**Multi-Instance (✅ Use)**:
- Separate projects (frontend repo + backend repo)
- Independent features (no shared state)
- Different technologies (Python microservice + React app)
- Parallel experimentation (try 3 different architectures)

**Dual-Instance (✅ Use)**:
- Plan-execute pattern (planning session + execution session)
- Quality review (implementation + code review)
- Test-first development (write tests + implement)

**Single Agent (✅ Use)**:
- Simple implementations (<5 files)
- Write-heavy tasks (shared file modifications)
- Sequential workflows (step-by-step tutorials)
- Budget-constrained projects

### Teams vs Beads Framework

**Beads Framework** (Steve Yegge):
- **Architecture**: Event-sourced MCP server (Gas Town) + SQLite database (beads.db)
- **Coordination**: Persistent message storage, historical replay
- **Maturity**: Community-maintained, experimental
- **Setup**: Requires Gas Town installation + agent-chat UI
- **Use case**: On-prem/airgap environments, full control over orchestration

**Agent Teams** (Anthropic):
- **Architecture**: Native Claude Code feature, git-based coordination
- **Coordination**: Real-time git locking, automatic merge
- **Maturity**: Official Anthropic feature (experimental)
- **Setup**: Feature flag only (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)
- **Use case**: Rapid prototyping, cloud-based development

**Comparison**:

| Aspect | Beads Framework | Agent Teams |
|--------|----------------|-------------|
| **Control** | Full (event sourcing, replay) | Limited (black-box coordination) |
| **Setup** | Complex (Gas Town + agent-chat) | Simple (feature flag) |
| **Persistence** | SQLite (beads.db) | Git commits |
| **Visibility** | agent-chat UI (Slack-like) | Native Claude Code interface |
| **Environment** | On-prem friendly | Cloud-first |
| **Maturity** | Community-driven | Anthropic official |

**When to use Beads**:
- ✅ On-prem/airgap requirements (no cloud API calls)
- ✅ Need event replay (debugging orchestration)
- ✅ Custom orchestration logic (beyond git-based)
- ✅ Persistent agent communications (audit trail)

**When to use Agent Teams**:
- ✅ Cloud development (Anthropic API access)
- ✅ Rapid setup (no infrastructure required)
- ✅ Git-native workflows (already using git)
- ✅ Official support path (Anthropic-maintained)

**Open question** (as of Feb 2026):
> "I'm not sure about Claude's guidance on when to use beads versus agent team sessions."
> — Paul Rayner, Feb 2026

**Community feedback needed**: Anthropic has not published official guidance on this choice. Practitioners are invited to share experiences in [GitHub Discussions](https://github.com/anthropics/claude-code/discussions).

---

## 8. Best Practices

### Task Decomposition Strategies

**Clear boundaries principle**:
```
Good decomposition:
- Agent 1: Backend API endpoints (/api/users/*)
- Agent 2: Frontend components (src/components/users/*)
- Agent 3: Database migrations (db/migrations/users/)

Why good:
- Non-overlapping file sets (no merge conflicts)
- Clear interfaces (API contracts)
- Independent testing (each layer testable)
```

```
Bad decomposition:
- Agent 1: User authentication
- Agent 2: User authorization
- Agent 3: User session management

Why bad:
- Overlapping files (auth.ts touched by all 3)
- Interdependencies (auth needs sessions, sessions need auth)
- Sequential coupling (can't parallelize effectively)
```

**Interface-first approach**:
1. **Define contracts**: Agree on function signatures, API schemas before parallel work
2. **Type stubs**: Create TypeScript types/interfaces first, implement separately
3. **Mock boundaries**: Each agent works with mocked dependencies initially
4. **Integration phase**: Team lead coordinates final integration

**Example**:
```typescript
// Team lead defines interface first
interface UserService {
  authenticate(email: string, password: string): Promise<User>;
  authorize(user: User, resource: string): Promise<boolean>;
}

// Agent 1 implements authenticate
// Agent 2 implements authorize
// No merge conflicts (different functions)
```

### Coordination Patterns

**Fan-out, fan-in**:
```
Team lead
  │
  ├─ Agent 1: Task A ──┐
  ├─ Agent 2: Task B ──┼──> Team lead synthesizes
  └─ Agent 3: Task C ──┘
```

**Sequential phases with parallelization**:
```
Phase 1 (Sequential):
  Team lead: Define architecture

Phase 2 (Parallel):
  ├─ Agent 1: Implement backend
  ├─ Agent 2: Implement frontend
  └─ Agent 3: Write tests

Phase 3 (Sequential):
  Team lead: Integration + validation
```

**Hierarchical delegation**:
```
Team lead
  │
  ├─ Agent 1 (Backend lead)
  │   ├─ Agent 1a: Controllers
  │   └─ Agent 1b: Services
  │
  └─ Agent 2 (Frontend lead)
      ├─ Agent 2a: Components
      └─ Agent 2b: State management
```

### AGENTS.md for Compound Learning

Agent teams benefit from a shared context file that accumulates cross-session learnings — patterns that worked, pitfalls to avoid, codebase-specific gotchas. This file is called `AGENTS.md` (analogous to `CLAUDE.md` but scoped to agentic workflows).

**What to put in AGENTS.md**:
```markdown
## Proven Patterns
- Use Interface-First decomposition for this codebase (see src/types/)
- Backend agent must run `db:migrate` before tests — env is not auto-seeded

## Pitfalls
- Do NOT modify auth.ts and session.ts in parallel — circular imports cause test failures
- Linter runs on save; do not commit with lint errors, the CI gate is strict

## Style
- All API responses must follow the ApiResponse<T> wrapper type
- Error codes live in src/constants/errors.ts — always reuse, never hardcode strings
```

**Critical rule — never let agents write AGENTS.md directly**. ETH Zürich research (Gloaguen et al., 2026) confirms that LLM-generated context files reduce task success by ~3% and increase inference costs by 20%+, compared to a ~4% improvement from developer-written files. The mechanism: agents generate generic, bloated context that creates cognitive overhead for every subsequent agent reading it.

Every line in AGENTS.md should be approved by a human. If a teammate identifies a new pattern worth documenting, it sends a suggestion to the team lead — the lead decides whether to add it.

**Maintenance**: Review AGENTS.md after each team session (Retro step of the Factory Model). Remove entries that are no longer relevant — stale instructions are actively harmful, not neutral.

### Git Worktree Management

**Why worktrees matter**:
- Each agent works in separate git worktree (isolated file system)
- Prevents file locking conflicts
- Enables parallel file modifications

**Setup**:
```bash
# Main repository
git worktree add ../project-agent1 main

# Agent 1 works in project-agent1/
# Agent 2 works in project-agent2/
# Team lead works in project/

# All sync via git commits
```

**Best practices**:
- ✅ One worktree per agent
- ✅ Frequent commits (continuous merge)
- ✅ Descriptive branch names (`agent1-backend-api`, `agent2-frontend-ui`)
- ❌ Don't modify same files across worktrees without coordination

### Cost Optimization

**Token-saving strategies**:

1. **Lazy spawning**: Only spawn agents when parallelization clearly benefits
   ```
   Bad: "Spawn 3 agents to implement this button"
   Good: "Spawn agents for multi-layer security review"
   ```

2. **Context pruning**: Remove irrelevant files from agent context
   ```
   # Tell agent what to ignore
   "Review backend API, ignore frontend files"
   ```

3. **Progressive escalation**: Start with single agent, escalate to teams if needed
   ```
   Step 1: Single agent attempts task
   Step 2: If complexity high, spawn team
   ```

4. **Result caching**: Reuse agent findings across similar tasks
   ```
   "Agent 1 found security issues in auth.ts.
   Agent 2, check if user.ts has same patterns."
   ```

5. **Hard token budgets per agent**: Assign domain-specific limits to prevent runaway consumption
   ```bash
   # In task brief to each teammate
   "Frontend agent: stay under 180k tokens total.
   Backend agent: stay under 280k tokens total.
   Auto-pause and report status at 85% of your budget."
   ```
   Token costs scale linearly with team size — a 5-agent team can consume 5× the tokens of a single session. Caps prevent one agent's rabbit hole from blowing the entire session budget.

### Quality Assurance

**Validation checklist**:
- [ ] **All agents completed**: No hanging tasks
- [ ] **Merge conflicts resolved**: Clean git history
- [ ] **Tests passing**: Automated test suite green
- [ ] **Human review**: Code inspection (don't trust blindly)
- [ ] **Cross-agent consistency**: Naming, patterns aligned

**Red flags**:
- ⚠️ Agents finished at very different times (imbalanced load)
- ⚠️ Many merge conflicts (poor task decomposition)
- ⚠️ Tests failing after merge (integration issues)
- ⚠️ Inconsistent code style (agents didn't follow shared standards)

**Mitigation**:
```bash
# After agent teams complete
git diff main..agent-teams-branch  # Review all changes
npm test                           # Run full test suite
npm run lint                       # Check code style
```

### Loop Guardrails

Agent teams can get stuck in unproductive retry cycles without hard iteration limits. Two mechanisms prevent this:

**MAX_ITERATIONS per teammate**:

Set a hard cap in the task brief for each teammate:
```
"Maximum 8 attempts on any single failing task.
Before retrying, answer: What specifically failed? What one change would fix it?
If still blocked after 8 attempts, stop and report to team lead."
```

The mandatory reflection prompt ("What failed? What specific change would fix it?") reduces stuck agents substantially — it forces the agent to change approach rather than repeat the same failing action with minor variations.

**Kill and reassign criteria**:
- Stuck 3+ iterations on the same blocker → kill the task, reassign with more specific context
- Task consumed >85% of its token budget with no commit → pause and report
- No progress after 2 reflection cycles → escalate to team lead

### Dedicated Reviewer Teammate

For production agent teams, adding a read-only reviewer agent improves output quality without slowing throughput:

**Setup**:
```
Reviewer brief:
- Model: Claude Opus 5 (for thoroughness)
- Tools available: lint, run tests, security-scan only — no file writes
- Trigger: automatically review on every TaskCompleted event
- Scope: the specific files changed in that task, not the full codebase
- Output: structured findings (blocking / non-blocking) added to shared task list
```

**Ratio**: 1 reviewer per 3-4 builders. With fewer builders, the reviewer becomes a bottleneck; with more, the review queue backs up.

**Why read-only matters**: a reviewer with write access will start fixing issues itself, which creates merge conflicts and defeats the purpose of parallel isolation.

---

## 9. Troubleshooting

### Common Issues

#### Issue: Agents not spawning

**Symptoms**:
- Agent teams prompt accepted but no teammates created
- Only team lead session running

**Causes**:
1. Feature flag not set correctly
2. Model not Opus 5 (teams require Opus)
3. Task not complex enough (Claude decided single agent sufficient)

**Solutions**:
```bash
# Verify flag
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS  # Should output "1" or "true"

# Check settings
cat ~/.claude/settings.json | grep agentTeams  # Should be true

# Force model
/model opus

# Explicit request
"Spawn 3 agents for this task (team lead + 2 teammates)"
```

#### Issue: Merge conflicts overwhelming

**Symptoms**:
- Many git conflicts after agents complete
- Manual resolution required frequently

**Causes**:
- Poor task decomposition (overlapping file sets)
- Write-heavy task (multiple agents modifying shared files)

**Solutions**:
```
Prevention:
1. Clear boundaries: Non-overlapping file assignments
2. Interface-first: Define contracts before implementation
3. Single-writer: One agent writes shared files, others read

Recovery:
1. Revert: git reset --hard before-agent-teams
2. Sequential: Re-implement with single agent
3. Human merge: Manually resolve conflicts (git mergetool)
```

#### Issue: High token costs

**Symptoms**:
- Token usage 3x+ higher than expected
- Budget exhausted quickly

**Causes**:
- Over-spawning agents (3+ agents for simple tasks)
- Long-running sessions (agents idle)
- Large context per agent (1M tokens × 3)

**Solutions**:
```
Immediate:
1. Kill extra agents: Shift+Down, exit agent session
2. Reduce scope: Narrow task boundaries
3. Switch to single agent: /model sonnet (cheaper)

Long-term:
1. Cost monitoring: Track token usage per session
2. Lazy spawning: Only spawn when needed
3. Progressive escalation: Start small, scale up if needed
```

#### Issue: Agents stuck/hanging

**Symptoms**:
- One agent finishes, others still processing for long time
- No progress updates

**Causes**:
- Imbalanced task distribution (one agent has 80% of work)
- Agent waiting for dependency (sequential coupling)
- Bug in git coordination (rare)

**Solutions**:
```bash
# Navigate to stuck agent
Shift+Down  # Switch to agent

# Check status
"What are you working on? Progress update?"

# Manual takeover if needed
"Stop current task, report findings so far"

# Kill and redistribute
Exit agent → Team lead redistributes task
```

#### Issue: Inconsistent results across agents

**Symptoms**:
- Agent 1 says "No issues", Agent 2 finds 10 bugs (same codebase)
- Conflicting recommendations

**Causes**:
- Different context windows (agents saw different files)
- Ambiguous instructions (agents interpreted differently)
- Model variability (stochastic outputs)

**Solutions**:
```
Prevention:
1. Explicit instructions: "All agents: Check for SQL injection"
2. Shared context: Point all agents to same reference docs
3. Validation: Human reviews all agent outputs

Recovery:
1. Reconciliation: "Compare Agent 1 and Agent 2 findings, resolve conflicts"
2. Third opinion: Spawn Agent 3 to arbitrate
3. Human decision: You choose which agent's recommendation to follow
```

### Navigation Problems

**Can't find agent sessions**:
```bash
# List all sessions
claude --list

# Filter for agent sessions
claude --list | grep agent

# Resume specific agent
claude --resume <session-id>
```

**Lost track of which agent is which**:
```
Solution: Name agents explicitly in team lead prompt

Good:
"Spawn 3 agents:
- Agent Security: Check vulnerabilities
- Agent Performance: Profile bottlenecks
- Agent Tests: Write test suite"

Bad:
"Spawn 3 agents for this codebase review"
```

**tmux navigation not working**:
```bash
# Verify tmux session
tmux list-sessions

# Attach to session
tmux attach -t claude-agents

# Navigate
Ctrl+b, n  # Next window
Ctrl+b, p  # Previous window
```

### Performance Optimization

**Slow coordination**:
```bash
# Check git repo size
du -sh .git/  # If >1GB, consider cleanup

# Clean up git objects
git gc --aggressive --prune=now

# Use shallow clone for agents
git clone --depth 1 <repo>
```

**Context loading delays**:
```
# Reduce context per agent
"Agent 1: Only load src/backend/* files"
"Agent 2: Only load src/frontend/* files"

# Prune irrelevant files
echo "node_modules/" >> .gitignore
echo "dist/" >> .gitignore
```

---

## 9. Iterative Retrieval for Sub-Agents

When a sub-agent lacks context to complete its task accurately, the default failure mode is: it makes assumptions and generates plausible-but-wrong output. The output looks reasonable enough to pass a quick review, but breaks downstream.

**The pattern**: give sub-agents a retrieval budget — they can request more context up to N cycles before committing to a response. Three cycles covers most cases while bounding cost and latency.

### Structure

```
Cycle 1: Agent receives task + initial context
         → If confident: produce output
         → If uncertain: identify what's missing, request specific files or symbols

Cycle 2: Agent receives requested context
         → If confident: produce output
         → If still uncertain: one final targeted request

Cycle 3: Agent receives final context
         → Produce best output regardless of remaining uncertainty
         → Flag explicit assumptions made
```

### What to Pass Sub-Agents

The most common mistake: giving a sub-agent the WHAT without the WHY. An agent that knows it's "implementing a retry mechanism for the payment service" has context that saves correction cycles:

```markdown
## Objective
[WHY this task exists — the problem being solved, the constraint being met]

## Task
[WHAT to do, specifically]

## Context
Files you have access to: [...]
Known constraints: [...]
What NOT to touch: [...]

## If you need more information
You may request up to 2 additional context cycles. Be specific:
- Name the exact files or symbols you need
- Explain why they're required to complete the task accurately
State explicitly: "I need [X] because [Y]" — not "I might need more context"

## Output format
[...]
```

### When to Apply This

| Situation | Use iterative retrieval? |
|-----------|------------------------|
| Sub-agent modifies 1–2 known files | No — provide the files directly |
| Sub-agent needs to understand system behavior | Yes — it may need to trace call graphs |
| Sub-agent makes architectural decisions | Yes — always |
| Sub-agent writes tests for existing code | Often — it needs to read what it's testing |

The overhead is real (each cycle costs tokens and latency). Apply it to tasks where wrong assumptions would cost more than the retrieval — typically anything touching interfaces, contracts, or public APIs.

> **Credit**: Iterative retrieval pattern for sub-agents from [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) (Affaan Mustafa). The max-3-cycles bound and the WHY/WHAT separation are documented in their longform guide.

---

## 10. Sources

### Official Anthropic Sources

1. **[Introducing Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6)**
   Anthropic, Feb 2026
   Official announcement of Opus 4.6 and agent teams research preview

2. **[Building a C compiler with agent teams](https://www.anthropic.com/engineering/building-c-compiler)**
   Anthropic Engineering, Feb 2026
   Technical deep-dive: git-based coordination, autonomous C compiler case study

3. **[2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)**
   Anthropic, Jan 2026
   Production metrics: Fountain (50% faster), CRED (2x speed)

### Community Sources

4. **[Claude Opus 4.6 for Developers: Agent Teams, 1M Context](https://dev.to/thegdsks/claude-opus-46-for-developers-agent-teams-1m-context-and-what-actually-matters-4h8c)**
   dev.to, Feb 2026
   Setup instructions, workflow impact table, read/write trade-offs

5. **[The best way to do agentic development in 2026](https://dev.to/chand1012/the-best-way-to-do-agentic-development-in-2026-14mn)**
   dev.to, Jan 2026
   Integration patterns: Claude Code + plugins (Conductor, Superpowers, Context7)

### Community Tools

6. **[Claude Agent Teams UI](https://github.com/777genius/claude_agent_teams_ui)**
   Open-source desktop app (Electron + React + TypeScript) for managing Claude Code agent teams.
   Kanban board with real-time task tracking, code review diffs, cross-team communication, deep session analysis, and context monitoring. 100% free, runs locally.

### Practitioner Testimonials

7. **[Paul Rayner LinkedIn Post](https://www.linkedin.com/posts/thepaulrayner_this-is-wild-i-just-upgraded-claude-code-activity-7425635159678414850-MNyv)**
   Paul Rayner (CEO Virtual Genius, EventStorming Handbook author), Feb 2026
   Production usage: 3 concurrent workflows (job search app, business ops, infrastructure)

8. **[IFTTD ep 311 "IA Agentique"](https://www.ifttd.io/episodes/ia-agentique)**
   Samy Lastmann (CTO, Smart Tribune), 2024
   Production multi-agent system: micro-agents replacing one mega-prompt. Each agent has a single task and the corresponding tools. Scalability, explainability, and measurability all improve when agents are split by responsibility. Not every agent in the pipeline needs an LLM; deterministic steps (regex, BM25, SQL lookups) belong to code, not to a reasoning model.

9. **[IFTTD ep 361 "Pourquoi le RAG n'est pas mort"](https://www.ifttd.io/episodes/rag)**
   Guillaume Laforge (Developer Advocate, Google Cloud), 2025
   Introduced "harness engineering" as the discipline of managing context flow across a multi-agent pipeline. Orchestrating isolated sub-agents is as much a context architecture problem as it is a task decomposition problem: each agent receives only the slice of context it needs, and the harness controls what gets passed where.

10. **[IFTTD ep 341 "Bilan 2025"](https://www.ifttd.io/episodes/bilan-2025)**
    Quentin Adam (CEO, Clever Cloud), 2025
    Multi-model orchestration pattern: Claude decomposes a task and orchestrates Gemini (larger context window) to execute large codebase rewrites that would exceed Claude's window. Planning and task formulation stay with the stronger reasoner; bulk context ingestion goes to the model built for it.

11. **[IFTTD ep 346 "IA & DevX"](https://www.ifttd.io/episodes/ia-devx)**
    Jocelyn N'takpe (Head of Engineering & Architecture, ManoMano), 2025
    At scale (250 engineers, 400+ microservices): a dedicated platform team maintains skills and rules encoding internal architecture conventions (database connection patterns, Kafka message encoding, naming standards). Agents are treated as new developers who need onboarding. Agent-facing documentation is now better maintained than Confluence. MCP stack in production: Serena (semantic code search via LSP), Playwright, Context7.

12. **Devoxx, 2026: "The Spec Paradox"**
    Max Sumrall, 2026
    Restricting an agent's task too tightly degrades output quality nearly as much as giving it no specification at all; broader, more ambitious goals sometimes pull more creative results out of the agent than a narrow brief does. A documented case at Picnic showed the same pattern at team level: perceived productivity rose sharply in the first weeks of AI-assisted development, then declined once code shipped faster than it could be reviewed, forcing repeated rework on the same features.

### Related Documentation

- [Claude Code Releases](../core/claude-code-releases.md) — v2.1.32, v2.1.33 release notes
- [Sub-Agents](#split-role-sub-agents) — Single-agent task delegation
- [Multi-Instance Workflows](#917-scaling-patterns-multi-instance-workflows) — Manual parallel coordination
- [Dual-Instance Pattern](#alternative-pattern-dual-instance-planning-vertical-separation) — Plan-execute split
- [AI Ecosystem: Beads Framework](../ecosystem/ai-ecosystem.md#beads-framework) — Alternative orchestration (Gas Town)

---

## Feedback & Contributions

**Experiencing issues?** Report to [Anthropic GitHub Issues](https://github.com/anthropics/claude-code/issues)

**Production learnings?** Share in [GitHub Discussions](https://github.com/anthropics/claude-code/discussions)

**Questions?** Ask in [Dev With AI Community](https://www.devw.ai/) (1500+ devs, Slack)

---

## Advanced Orchestration Patterns

These patterns address the failure modes that emerge at scale in multi-agent pipelines: coordinators that do too much work themselves, agents that proceed without prerequisites, and pipelines that cannot recover from mid-run failures.

---

### Hub-and-Spoke Coordinator

The hub-and-spoke pattern separates coordination from execution. The coordinator agent decomposes the task, selects subagents, dispatches work, monitors results, and aggregates outputs. It does no domain work itself — no research, no analysis, no generation. This separation is what makes the coordinator reusable across different task types.

```python
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class SubagentResult:
    agent_id: str
    task: str
    result: Any
    success: bool
    error: str | None = None

class ResearchCoordinator:
    def __init__(self, subagents: dict[str, Callable]):
        self.subagents = subagents  # name -> callable

    def run(self, research_question: str) -> dict:
        # Decompose into parallel subtasks
        subtasks = self.decompose(research_question)

        # Dispatch to appropriate subagents
        results = []
        for subtask in subtasks:
            agent_name = self.select_agent(subtask)
            if agent_name not in self.subagents:
                results.append(SubagentResult(
                    agent_id=agent_name, task=subtask,
                    result=None, success=False,
                    error=f"No agent available for: {agent_name}"
                ))
                continue

            try:
                result = self.subagents[agent_name](subtask)
                results.append(SubagentResult(
                    agent_id=agent_name, task=subtask,
                    result=result, success=True
                ))
            except Exception as e:
                results.append(SubagentResult(
                    agent_id=agent_name, task=subtask,
                    result=None, success=False, error=str(e)
                ))

        # Aggregate — coordinator's only domain responsibility
        return self.aggregate(research_question, results)

    def decompose(self, question: str) -> list[str]:
        # Returns subtasks — coordinator decides structure, not domain content
        raise NotImplementedError

    def select_agent(self, subtask: str) -> str:
        # Routing logic — pattern matching or LLM-based selection
        raise NotImplementedError

    def aggregate(self, original_question: str, results: list[SubagentResult]) -> dict:
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        return {
            "question": original_question,
            "findings": [r.result for r in successful],
            "coverage": len(successful) / len(results) if results else 0.0,
            "failures": [{"task": r.task, "error": r.error} for r in failed]
        }
```

The coordinator never touches the content of results, only routes them, counts them, and passes them to an aggregation step. If you find coordinator code that contains analysis logic, business rules, or domain-specific processing, that logic belongs in a subagent.

---

### Programmatic Prerequisites

Prerequisite checks should be deterministic gates, not prompt instructions. Telling a model "make sure the data is ready before proceeding" is not a prerequisite, it is a suggestion. A programmatic prerequisite is a state check that either allows execution to continue or returns a structured error.

**Pattern 1: State-flag gate**

```python
@dataclass
class PipelineState:
    data_ingested: bool = False
    schema_validated: bool = False
    permissions_checked: bool = False

    def can_proceed_to_analysis(self) -> tuple[bool, list[str]]:
        missing = []
        if not self.data_ingested:
            missing.append("data_ingested")
        if not self.schema_validated:
            missing.append("schema_validated")
        if not self.permissions_checked:
            missing.append("permissions_checked")
        return len(missing) == 0, missing

def run_analysis_phase(state: PipelineState, data: dict) -> dict:
    can_proceed, missing = state.can_proceed_to_analysis()
    if not can_proceed:
        return {
            "status": "blocked",
            "reason": f"Prerequisites not met: {', '.join(missing)}",
            "required": missing
        }

    # Proceed with analysis — all prerequisites confirmed
    return perform_analysis(data)
```

**Pattern 2: Phase-based dispatch**

For pipelines with sequential phases, the orchestrator dispatches based on completed phases rather than on elapsed time or turn count:

```python
from enum import Enum

class PipelinePhase(Enum):
    INIT = "init"
    INGESTION = "ingestion"
    VALIDATION = "validation"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"

@dataclass
class PipelineContext:
    phase: PipelinePhase = PipelinePhase.INIT
    phase_results: dict = None

    def __post_init__(self):
        if self.phase_results is None:
            self.phase_results = {}

def dispatch_next_phase(context: PipelineContext, agents: dict) -> PipelineContext:
    next_phase_map = {
        PipelinePhase.INIT: PipelinePhase.INGESTION,
        PipelinePhase.INGESTION: PipelinePhase.VALIDATION,
        PipelinePhase.VALIDATION: PipelinePhase.PROCESSING,
        PipelinePhase.PROCESSING: PipelinePhase.COMPLETE
    }

    next_phase = next_phase_map.get(context.phase)
    if next_phase is None:
        return context

    agent = agents.get(next_phase.value)
    if agent is None:
        context.phase = PipelinePhase.FAILED
        return context

    try:
        result = agent(context.phase_results)
        context.phase_results[next_phase.value] = result
        context.phase = next_phase
    except Exception as e:
        context.phase = PipelinePhase.FAILED
        context.phase_results["error"] = str(e)

    return context
```

---

### Dynamic Subagent Selection

Instead of hardcoding which agent handles which task, a coordinator can select subagents dynamically based on task characteristics. This allows the same coordinator to handle new task types without code changes.

```python
@dataclass
class AgentCapability:
    name: str
    handles: list[str]  # task type keywords
    cost: float          # relative cost (1.0 = baseline)
    latency: float       # expected seconds

class DynamicSelector:
    def __init__(self, agents: list[AgentCapability]):
        self.agents = agents

    def select(self, task: str, budget_tier: str = "standard") -> str:
        candidates = [
            a for a in self.agents
            if any(keyword in task.lower() for keyword in a.handles)
        ]

        if not candidates:
            return "general"  # fallback agent

        if budget_tier == "economy":
            # Cheapest capable agent
            return min(candidates, key=lambda a: a.cost).name
        elif budget_tier == "performance":
            # Fastest capable agent
            return min(candidates, key=lambda a: a.latency).name
        else:
            # Balanced: cheapest among the fast agents
            fast = [a for a in candidates if a.latency < 10.0]
            pool = fast if fast else candidates
            return min(pool, key=lambda a: a.cost).name
```

---

### Research Space Partitioning

When multiple agents research the same broad topic, they will return overlapping results unless the coordinator explicitly partitions the search space. Overlap wastes budget and makes aggregation harder.

```python
def partition_research_space(
    topic: str,
    num_agents: int,
    partition_dimensions: list[str]
) -> list[dict]:
    """
    Divide a research topic into non-overlapping partitions.
    Each agent receives a partition with explicit scope boundaries.
    """
    if len(partition_dimensions) >= num_agents:
        dimensions = partition_dimensions[:num_agents]
    else:
        # Create additional partitions if not enough thematic dimensions
        dimensions = partition_dimensions + [
            f"recent_{i}" for i in range(num_agents - len(partition_dimensions))
        ]

    return [
        {
            "agent_id": f"researcher_{i}",
            "topic": topic,
            "scope": dimension,
            "exclusions": [d for j, d in enumerate(dimensions) if j != i],
            "instruction": (
                f"Research '{topic}' focusing exclusively on '{dimension}'. "
                f"Do NOT cover: {', '.join(dimensions[:i] + dimensions[i+1:])}. "
                f"This constraint prevents duplication with parallel researchers."
            )
        }
        for i, dimension in enumerate(dimensions)
    ]

# Example: 3-agent research on "vector database performance"
partitions = partition_research_space(
    topic="vector database performance",
    num_agents=3,
    partition_dimensions=["indexing algorithms", "query optimization", "hardware scaling"]
)
```

---

### Crash Recovery Manifest

Long-running agent pipelines (hours, overnight jobs) need crash recovery. A manifest records completed work at phase boundaries so that a restart can continue from the last checkpoint rather than starting over.

```python
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime

@dataclass
class PipelineManifest:
    pipeline_id: str
    created_at: str
    task_description: str
    total_items: int
    completed_items: list[str] = field(default_factory=list)
    failed_items: list[dict] = field(default_factory=list)
    phase_checkpoints: dict = field(default_factory=dict)
    status: str = "in_progress"  # "in_progress" | "complete" | "failed"

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, path: str) -> "PipelineManifest":
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

    def checkpoint(self, phase: str, result: dict, manifest_path: str):
        self.phase_checkpoints[phase] = {
            "completed_at": datetime.utcnow().isoformat(),
            "result_summary": result.get("summary", "")
        }
        self.save(manifest_path)

    def mark_item_complete(self, item_id: str, manifest_path: str):
        self.completed_items.append(item_id)
        self.save(manifest_path)  # write after every item

class RecoverableOrchestrator:
    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path

    def run(self, pipeline_id: str, items: list[str], processor) -> PipelineManifest:
        # Load or create manifest
        if os.path.exists(self.manifest_path):
            manifest = PipelineManifest.load(self.manifest_path)
            print(f"Resuming: {len(manifest.completed_items)}/{manifest.total_items} done")
        else:
            manifest = PipelineManifest(
                pipeline_id=pipeline_id,
                created_at=datetime.utcnow().isoformat(),
                task_description=f"Processing {len(items)} items",
                total_items=len(items)
            )

        for item_id in items:
            if item_id in manifest.completed_items:
                continue  # skip completed items

            try:
                processor(item_id)
                manifest.mark_item_complete(item_id, self.manifest_path)
            except Exception as e:
                manifest.failed_items.append({"id": item_id, "error": str(e)})
                manifest.save(self.manifest_path)

        manifest.status = "complete" if not manifest.failed_items else "partial"
        manifest.save(self.manifest_path)
        return manifest
```

Checkpoint at phase boundaries, not just at task completion. For a 3-phase pipeline (ingest, analyze, report), a crash mid-analysis should resume from the start of analysis, not from the start of ingest.

---

### Iterative Refinement Loop

Some tasks require multiple passes to reach acceptable quality. The coordinator drives iteration, not the subagent. This separation means the subagent stays stateless and the coordinator controls stopping criteria.

```python
@dataclass
class RefinementState:
    iteration: int
    current_output: str
    quality_score: float
    feedback: str | None
    max_iterations: int = 5
    target_quality: float = 0.85

    def should_continue(self) -> bool:
        return (
            self.iteration < self.max_iterations
            and self.quality_score < self.target_quality
        )

def iterative_refine(
    initial_task: str,
    generator_fn,
    evaluator_fn,
    max_iterations: int = 5
) -> RefinementState:
    state = RefinementState(
        iteration=0,
        current_output="",
        quality_score=0.0,
        feedback=None,
        max_iterations=max_iterations
    )

    while True:
        # Generate (or refine based on feedback)
        if state.iteration == 0:
            state.current_output = generator_fn(initial_task)
        else:
            state.current_output = generator_fn(
                f"{initial_task}\n\nPrevious attempt:\n{state.current_output}\n\n"
                f"Feedback to address:\n{state.feedback}"
            )

        # Evaluate — separate pass with fresh context
        evaluation = evaluator_fn(state.current_output, initial_task)
        state.quality_score = evaluation["score"]
        state.feedback = evaluation["feedback"]
        state.iteration += 1

        if not state.should_continue():
            break

    return state
```

Stopping criteria matter. "Keep going until it's perfect" is not a stopping criterion. Define `target_quality` as a numeric threshold based on a validation set, and `max_iterations` as a hard budget. Without both, the loop either terminates too early or runs indefinitely.

---

### Narrow Task Decomposition

Broad task decomposition produces subagents with unclear success criteria. Use the SPEC test to validate each subtask before dispatching:

**SPEC test for subtasks:**
- **S**pecific: the task description leaves no ambiguity about what to produce
- **P**rogrammatically evaluable: success or failure can be checked without human judgment
- **E**xplicit scope: what is in and out of scope is stated, not implied
- **C**onstrained: the task has a defined output format, length, or schema

A subtask that fails the SPEC test should be decomposed further or clarified before dispatch.

| Subtask | SPEC pass? | Issue |
|---|---|---|
| "Research the topic" | No | Not specific, not programmatically evaluable |
| "Find 3 peer-reviewed papers on vector indexing published 2022-2024" | Yes | Specific, countable, scoped, constrained format |
| "Analyze the data" | No | Not specific, no output schema |
| "Extract vendor names from invoices 001-050, output as JSON array" | Yes | Specific, schema-constrained, scoped |
| "Write something good" | No | No quality criteria, not evaluable |
| "Write a 150-word executive summary with: problem, approach, outcome" | Yes | Word count, structure, and content all specified |

When a subtask cannot be expressed in a way that passes the SPEC test, that is usually a signal that the coordinator does not yet have enough information to decompose that portion of the work. Gather more context before decomposing further.

---

*Version 1.0.0 | Created: 2026-02-07 | Agent Teams (v2.1.32+, Experimental)*
