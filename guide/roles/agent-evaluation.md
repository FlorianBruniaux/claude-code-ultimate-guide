---
title: "Agent Evaluation"
description: "Metrics, patterns, and tools for measuring custom agent effectiveness"
tags: [agents, testing, guide]
---

# Agent Evaluation

**Quick nav**: [Why Evaluate?](#why-evaluate-agents) · [Metrics to Track](#metrics-to-track) · [Implementation](#implementation-patterns) · [Example](#example-agent-with-evaluation) · [Tools](#tools--references)

---

## Why Evaluate Agents?

When you create custom agents in `.claude/agents/`, you're encoding specialized expertise into reusable workflows. But how do you know if your agents are actually effective?

**Without evaluation**, you're building blind:
- ❌ No way to measure if agent responses are improving or degrading over time
- ❌ Can't compare different agent configurations objectively
- ❌ Difficult to identify which aspects of agent context/instructions need refinement
- ❌ No data to justify investment in agent development

**With evaluation**, you iterate with confidence:
- ✅ Quantify agent quality through metrics (response time, accuracy, tool usage)
- ✅ A/B test different agent configurations with measurable outcomes
- ✅ Identify patterns in successful vs failed interactions
- ✅ Build feedback loops for continuous improvement

**Core principle**: Agents are code. Like all code, they need tests, metrics, and observability.

---

## Metrics to Track

### 1. Response Quality Metrics

**What to measure**:
- **Task completion rate**: Did the agent accomplish the stated goal?
- **Correctness**: Were the agent's outputs factually accurate?
- **Relevance**: Did the response stay on-topic and address the actual question?
- **Hallucination rate**: How often did the agent invent information?

**How to track**:
```bash
# Post-response hook: .claude/hooks/log-response-quality.sh
# Triggered after each agent response

# Log structure:
{
  "timestamp": "2026-02-10T14:32:00Z",
  "agent_id": "backend-architect",
  "task_completed": true,
  "correctness_score": 4.5,  # User rating 1-5
  "hallucinations": 0,
  "response_tokens": 1250
}
```

**Implementation tip**: Use user feedback prompts (thumbs up/down) or automated checks (test suite passing after agent code generation).

---

### 2. Tool Usage Metrics

**What to measure**:
- **Tool call success rate**: Percentage of tool calls that executed without errors
- **Tool selection accuracy**: Did agent choose the right tool for the task?
- **Tool call efficiency**: Minimum calls to achieve goal (avoid unnecessary reads/searches)
- **Error recovery**: Did agent handle tool failures gracefully?

**How to track**:
```bash
# Post-tool-use hook: .claude/hooks/log-tool-usage.sh
# Triggered after each tool call

# Log structure:
{
  "timestamp": "2026-02-10T14:32:05Z",
  "agent_id": "backend-architect",
  "tool_name": "Read",
  "tool_success": true,
  "tool_parameters": {"file_path": "src/auth.ts"},
  "execution_time_ms": 45
}
```

**Implementation tip**: Use Claude Code hooks system (see `examples/hooks/`) to automatically log tool calls.

---

### 3. Performance Metrics

**What to measure**:
- **Response time**: Total time from user prompt to complete response
- **Token efficiency**: Input/output tokens used per task
- **Context utilization**: How much of context window was used?
- **Cost per task**: API cost for the full interaction

**How to track**:
```bash
# Session-end hook: .claude/hooks/log-performance.sh
# Triggered at end of session

# Log structure:
{
  "timestamp": "2026-02-10T14:35:00Z",
  "agent_id": "backend-architect",
  "session_duration_s": 180,
  "input_tokens": 3500,
  "output_tokens": 2800,
  "total_cost_usd": 0.15,
  "context_utilization": 0.42
}
```

**Implementation tip**: Parse Claude Code session logs or use MCP observability tools.

---

### 4. User Satisfaction Metrics

**What to measure**:
- **Explicit feedback**: User ratings, comments, bug reports
- **Implicit signals**: Did user accept agent's suggestions? Did they retry the prompt?
- **Adoption rate**: How often is this agent used vs alternatives?
- **Retention**: Do users return to this agent for similar tasks?

**How to track**:
```bash
# Manual feedback collection
# After agent completes task, prompt user:
"Rate this agent's performance (1-5): _"

# Log:
{
  "timestamp": "2026-02-10T14:35:10Z",
  "agent_id": "backend-architect",
  "user_rating": 5,
  "user_comment": "Perfect analysis of auth flow",
  "would_use_again": true
}
```

**Implementation tip**: Add feedback prompts to agent templates or use post-session surveys.

---

## Implementation Patterns

### Pattern 1: Logging Hook System

**Use Case**: Automatically track all agent interactions without manual intervention

**Setup**:
```bash
# .claude/hooks/post-tool-use.sh
#!/bin/bash
# Triggered after every tool call

AGENT_ID=$(echo "$CLAUDE_AGENT_ID" | jq -r)
TOOL_NAME=$(echo "$CLAUDE_TOOL_NAME" | jq -r)
TOOL_SUCCESS=$(echo "$CLAUDE_TOOL_SUCCESS" | jq -r)

# Append to metrics log
echo "{\"timestamp\":\"$(date -Iseconds)\",\"agent\":\"$AGENT_ID\",\"tool\":\"$TOOL_NAME\",\"success\":$TOOL_SUCCESS}" \
  >> .claude/logs/agent-metrics.jsonl
```

**Pros**: Zero manual overhead, complete coverage, time-series data
**Cons**: Requires parsing Claude Code environment variables (may change across versions)

---

### Pattern 2: Agent Unit Tests

**Use Case**: Regression testing to ensure agent improvements don't break existing capabilities

**Setup**:
```bash
# tests/agents/backend-architect.test.sh
#!/bin/bash

# Test 1: Agent correctly identifies hexagonal architecture layers
echo "Test: Hexagonal architecture analysis"
RESULT=$(claude agent backend-architect "Analyze src/auth.ts for layer violations")
if echo "$RESULT" | grep -q "domain layer"; then
  echo "✅ PASS: Identified layers"
else
  echo "❌ FAIL: Did not identify layers"
  exit 1
fi

# Test 2: Agent recommends correct patterns
echo "Test: Pattern recommendations"
RESULT=$(claude agent backend-architect "Improve error handling in src/api.ts")
if echo "$RESULT" | grep -q "Result<T, E>"; then
  echo "✅ PASS: Recommended Result pattern"
else
  echo "❌ FAIL: Incorrect pattern"
  exit 1
fi
```

**Pros**: Automated, catches regressions, CI/CD integration
**Cons**: Requires maintenance, may have false positives/negatives

---

### Pattern 3: A/B Testing Configurations

**Use Case**: Compare two versions of agent to determine which performs better

**Setup**:
```yaml
# .claude/agents/backend-architect-v1.md (control)
name: backend-architect
version: 1.0
instructions: |
  You are a backend architect specializing in...
  [original instructions]

# .claude/agents/backend-architect-v2.md (experiment)
name: backend-architect-v2
version: 2.0
instructions: |
  You are a backend architect specializing in...
  [modified instructions with new pattern emphasis]
```

**Evaluation**:
```bash
# Run same task with both agents, compare metrics
# Task: "Analyze src/auth.ts for security issues"

# Version 1 metrics:
# - Response time: 45s
# - Issues found: 3
# - User rating: 4/5

# Version 2 metrics:
# - Response time: 38s
# - Issues found: 5 (2 additional critical issues)
# - User rating: 5/5

# Conclusion: Version 2 is more thorough and faster → promote to production
```

**Pros**: Data-driven decisions, quantifiable improvements
**Cons**: Requires discipline to run controlled experiments

---

### Pattern 4: Feedback Loop Integration

**Use Case**: Continuously improve agent based on real-world usage data

**Setup**:
```bash
# After agent completes task
echo "How would you rate this response? (1-5, or 'skip'): "
read RATING

if [ "$RATING" != "skip" ]; then
  echo "Any specific feedback?: "
  read COMMENT

  # Log feedback
  echo "{\"timestamp\":\"$(date -Iseconds)\",\"agent\":\"$AGENT_ID\",\"rating\":$RATING,\"comment\":\"$COMMENT\"}" \
    >> .claude/logs/agent-feedback.jsonl
fi

# Weekly: Review feedback.jsonl, identify patterns
# Monthly: Update agent instructions based on aggregated feedback
```

**Pros**: Aligns agent with actual user needs, identifies edge cases
**Cons**: Requires manual review and action on feedback

---

## Example: Agent with Evaluation

**Full template available**: [`examples/agents/analytics-with-eval/`](../../examples/agents/analytics-with-eval/) includes complete agent definition, hooks, analysis scripts, and report template.

### Setup: Analytics Agent with Built-in Metrics

```yaml
# .claude/agents/analytics-agent.md
---
name: analytics-agent
description: SQL query generator with evaluation hooks
version: 1.0
tools:
  - Read
  - Write
  - Bash
hooks:
  post_response: .claude/hooks/log-analytics-metrics.sh
---

# Analytics Agent

You are an expert SQL analyst helping users query databases.

## Evaluation Criteria

After each query:
1. **Correctness**: Does query produce expected results?
2. **Performance**: Query execution time < 5s?
3. **Safety**: No destructive operations (DELETE, DROP, TRUNCATE)?
4. **Best practices**: Uses proper JOINs, indexes, parameterized queries?

## Instructions

[... agent instructions ...]
```

### Metrics Hook

```bash
# .claude/hooks/log-analytics-metrics.sh
#!/bin/bash
# Triggered after analytics-agent response

# Extract query from response (naive grep, improve with jq)
QUERY=$(echo "$CLAUDE_RESPONSE" | grep -oP 'SELECT.*?;')

if [ -n "$QUERY" ]; then
  # Test query (requires database connection)
  EXEC_TIME=$( (time psql -U user -d db -c "$QUERY") 2>&1 | grep real | awk '{print $2}')

  # Check for destructive operations
  if echo "$QUERY" | grep -iE 'DELETE|DROP|TRUNCATE'; then
    SAFETY="FAIL"
  else
    SAFETY="PASS"
  fi

  # Log metrics
  echo "{\"timestamp\":\"$(date -Iseconds)\",\"query\":\"$QUERY\",\"exec_time\":\"$EXEC_TIME\",\"safety\":\"$SAFETY\"}" \
    >> .claude/logs/analytics-metrics.jsonl
fi
```

### Analysis

```bash
# Monthly review: Analyze metrics
jq -s 'group_by(.safety) | map({safety: .[0].safety, count: length})' \
  .claude/logs/analytics-metrics.jsonl

# Output:
# [
#   {"safety": "PASS", "count": 127},
#   {"safety": "FAIL", "count": 3}
# ]

# Action: Review 3 failed queries, update agent instructions to prevent future violations
```

---

## Tools & References

### Open-Source Evaluation Frameworks

#### nao (Analytics Agents)

**URL**: [github.com/getnao/nao](https://github.com/getnao/nao/)

**What it provides**:
- Built-in evaluation framework for analytics agents
- Unit testing capabilities for agent responses
- Metrics collection (response quality, tool usage, performance)
- Feedback loop integration

**How to adapt for Claude Code**:
- **Context builder pattern**: Apply nao's structured context approach to `.claude/agents/` config
- **Evaluation hooks**: Translate nao's evaluation framework to Claude Code hooks system
- **Metrics schema**: Use nao's metrics schema as template for your logs

**Status**: Production-ready, actively maintained, TypeScript + Python

---

### Claude Code Native Patterns

**Hooks system**: `.claude/hooks/` for automated logging (see `examples/hooks/README.md`)

**Agents directory**: `.claude/agents/` for custom agent definitions (see `guide/ultimate-guide.md` Section 4)

**MCP observability**: Use MCP servers for advanced logging and metrics aggregation

---

## Best Practices

### Start Simple

**Week 1**: Add basic logging hook (tool calls only)
**Week 2**: Add user feedback prompt (manual ratings)
**Week 3**: Build dashboard to visualize metrics
**Week 4**: Run first A/B test on agent configuration

### Focus on Actionable Metrics

Don't track metrics you won't act on. Prioritize:
1. **Task completion rate** → Refine agent instructions
2. **Tool call errors** → Improve context or add examples
3. **User ratings** → Identify confusing or unhelpful responses

### Automate Where Possible

Manual evaluation doesn't scale. Use:
- Hooks for automatic logging
- CI/CD integration for agent unit tests
- Scripts for periodic metric aggregation

### Build Feedback Loops

Metrics are useless without action:
- Weekly: Review metrics, identify patterns
- Monthly: Update agent instructions based on data
- Quarterly: Major agent refactoring if needed

---

## Related Sections

- **[Agents](./ultimate-guide.md#4-agents)**: Creating custom agents
- **[Hooks](./ultimate-guide.md#5-hooks)**: Automation with event hooks
- **[Observability](../ops/observability.md)**: Logging and monitoring strategies
- **[AI Ecosystem](../ecosystem/ai-ecosystem.md#82-domain-specific-agent-frameworks)**: External frameworks like nao

---

**Next steps**:
1. Add logging hook to your most-used agent
2. Collect 1 week of metrics
3. Analyze and refine agent based on data

**Template**: See `examples/agents/analytics-with-eval/` for complete implementation with hooks, scripts, and report template
