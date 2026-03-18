---
title: "Exploration Before Implementation"
description: "Ask Claude for multiple approaches with trade-offs before coding to prevent anchoring bias"
tags: [workflow, architecture, design-patterns]
---

# Exploration Before Implementation

> **Confidence**: Tier 2 — Validated by practitioner studies (+20-30% decision quality, +40% alternatives identified).
> **Source**: [MetalBear Engineering Blog](https://metalbear.com/blog/engineering-ai-use/), arXiv practitioner studies

Before coding, ask Claude for multiple approaches with trade-offs. This prevents anchoring bias—the tendency to fixate on the first solution proposed.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [The Pattern](#the-pattern)
3. [Anti-Anchoring Prompts](#anti-anchoring-prompts)
4. [When to Use](#when-to-use)
5. [Integration with Claude Code](#integration-with-claude-code)
6. [Anti-Patterns](#anti-patterns)
7. [See Also](#see-also)

---

## TL;DR

```
1. Describe problem (no code, no preconception)
2. Request 3-5 approaches with trade-offs
3. Ask for quantified comparison
4. Choose approach
5. Then implement
```

Key insight: **Once a model proposes a concrete solution, it can unintentionally narrow your thinking.**

---

## The Pattern

### Step 1: Problem Statement Only

Start with the problem, not a solution direction:

```
I need to handle user sessions in a Node.js API.
Requirements:
- Support 10K concurrent users
- Session data: user ID, permissions, preferences
- Must survive server restarts
```

**Not this** (anchors on Redis):
```
I'm thinking of using Redis for sessions. How should I implement it?
```

### Step 2: Request Multiple Approaches

```
Give me 4 different approaches to solve this.
For each, include:
- Architecture overview
- Pros and cons
- Performance characteristics
- Complexity to implement
```

### Step 3: Quantified Comparison

```
Now rank these approaches on a 1-10 scale for:
- Latency (lower is better)
- Scalability (10K → 100K users)
- Operational complexity
- Development time
```

### Step 4: Choose, Then Implement

```
I'll go with approach B (JWT + Redis hybrid).
Now implement it following our existing patterns in src/auth/.
```

---

## Anti-Anchoring Prompts

LLMs can fixate on their first suggestion. These prompts combat that:

| Prompt Type | Template | Effect |
|-------------|----------|--------|
| **Fresh start** | "Ignore any prior ideas. Generate 4 novel approaches to [X]" | Forces diversity |
| **Reflection loop** | "Generate 3 options, then critique each, then recommend" | Self-correction (-25% anchoring bias) |
| **Quantified trade-offs** | "Rank by [metric1], [metric2], [metric3] with scores 1-10" | Objective comparison |
| **Devil's advocate** | "What are the strongest arguments against your recommendation?" | Surface hidden trade-offs |
| **Constraint variation** | "Now solve the same problem with [opposite constraint]" | Expand solution space |

### Example: Anti-Anchoring Prompt

```
I need pagination for a REST API with 1M+ records.

IMPORTANT: Don't suggest offset-based pagination first.
Generate 4 different pagination strategies, including at least one
unconventional approach. For each:

1. How it works (2-3 sentences)
2. Best use case
3. Worst use case
4. Performance at 1M records

Then recommend one, explaining why it beats the others for my use case.
```

### Reflection Loop Prompt

```
For implementing real-time notifications:

Phase 1: Generate 3 approaches (WebSockets, SSE, Long Polling)
Phase 2: For each, list 2 things that could go wrong in production
Phase 3: Based on Phase 2, which approach is most resilient?

Show your reasoning for each phase.
```

---

## When to Use

### Use Exploration

| Scenario | Why |
|----------|-----|
| Greenfield features | No existing pattern to follow |
| Architecture decisions | High impact, hard to reverse |
| Multiple valid approaches | Need informed choice |
| Unfamiliar domain | Don't know what you don't know |
| Team disagreement | Get neutral analysis of options |

### Skip Exploration

| Scenario | Why |
|----------|-----|
| Bug fixes | Solution usually obvious from symptoms |
| Single valid approach | No real choice to make |
| Time-critical hotfixes | Speed > perfection |
| Following existing pattern | Decision already made |
| Trivial changes | Overhead not worth it |

---

## Integration with Claude Code

### With Plan Mode

Exploration happens **before** entering Plan Mode:

```
# Step 1: Explore (not in Plan Mode yet)
I need to add caching to the API. What are my options?

# Claude responds with 4 approaches

# Step 2: Choose
Let's go with approach C (edge caching with Cloudflare).

# Step 3: Plan (press Shift+Tab twice to enter Plan Mode)
Implement edge caching using Cloudflare Workers.
Follow the patterns in our existing middleware.
```

### With CLAUDE.md

Add exploration triggers to your project instructions:

```markdown
## Workflow Preferences

### Before New Features
When implementing new features, first explore 3-4 approaches
with trade-offs before committing to implementation.
Use quantified comparison (1-10 scale) for:
- Performance
- Maintainability
- Time to implement
```

### With Task Tool

Track exploration as tasks:

```
TaskCreate: "Explore caching approaches"
TaskCreate: "Choose approach based on analysis"
TaskCreate: "Implement cache invalidation"
TaskCreate: "Add cache headers to responses"
# Mark completed as you progress with TaskUpdate
```

---

## Anti-Patterns

### Premature Anchoring

```
# Wrong
"I want to use Redis for caching. How do I set it up?"

# Right
"I need caching for API responses. What are my options?"
```

You've eliminated 90% of solutions before exploring.

### Shallow Comparison

```
# Wrong
"Which is better: Redis or Memcached?"

# Right
"Compare Redis, Memcached, and in-process caching for:
- 50MB cache size
- Read-heavy workload (95% reads)
- Single server deployment
Include latency, memory overhead, and operational complexity."
```

### Ignoring Trade-offs

```
# Wrong
"Just tell me the best approach"

# Right
"What would I give up by choosing approach A over B?
What scenarios would make me regret this choice?"
```

### Analysis Paralysis

```
# Wrong
Exploring 10 options for a simple feature

# Right
Set a limit: "Give me your top 3 approaches, no more"
Make a decision and iterate if needed
```

---

## Example Session

### Initial Exploration

```
User: I need to implement real-time updates in our React dashboard.
      The dashboard shows ~50 metrics that update every 5 seconds.
      Currently we poll, but users complain about stale data.

Claude: Here are 4 approaches:

**A) WebSockets**
- Full duplex, server can push anytime
- Pros: Lowest latency, true real-time
- Cons: Connection management, scaling complexity
- Best for: Sub-second updates, bidirectional communication

**B) Server-Sent Events (SSE)**
- Unidirectional server → client stream
- Pros: Simple, HTTP-based, auto-reconnect
- Cons: One-way only, limited browser connections
- Best for: Dashboard feeds, notifications

**C) Long Polling**
- Client holds request until data ready
- Pros: Works everywhere, simple fallback
- Cons: Higher latency, more server load
- Best for: Legacy compatibility

**D) GraphQL Subscriptions**
- WebSocket-based with GraphQL schema
- Pros: Type-safe, selective updates
- Cons: Requires GraphQL infrastructure
- Best for: Existing GraphQL APIs

User: Rank these for our use case (React, 50 metrics, 5s refresh,
      team has no WebSocket experience).

Claude: Scores (1-10, higher is better):

| Approach | Latency | Complexity | Team Fit | Scalability |
|----------|---------|------------|----------|-------------|
| WebSockets | 10 | 4 | 3 | 7 |
| SSE | 8 | 8 | 8 | 8 |
| Long Polling | 5 | 9 | 9 | 5 |
| GraphQL Subs | 9 | 3 | 2 | 7 |

**Recommendation: SSE**
Best balance of simplicity and real-time capability.
Your team can implement it in a day, and it handles your
50 metrics × 5s updates easily. Upgrade to WebSockets later
if you need bidirectional or sub-second updates.

User: Let's go with SSE. Now implement it.
```

---

## See Also

- [plan-driven.md](./plan-driven.md) — For codebase exploration (/plan mode)
- [iterative-refinement.md](./iterative-refinement.md) — Refine after choosing approach
- [../examples/semantic-anchors/anchor-catalog.md](../../examples/semantic-anchors/anchor-catalog.md) — Precision vocabulary for prompts
- [spec-first.md](./spec-first.md) — Define requirements before exploring
