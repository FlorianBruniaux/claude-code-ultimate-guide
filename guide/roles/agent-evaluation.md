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

---

## Evaluating Probabilistic Systems

Standard unit tests do not apply to LLM outputs. A test that passes or fails deterministically cannot capture the behavior of a system whose outputs vary across runs with the same input. Production teams working with agentic pipelines have converged on a different evaluation model.

### Temperature Zero Does Not Guarantee Determinism

Setting temperature to 0 is often assumed to make an LLM's output deterministic. It does not. Floating-point arithmetic on GPUs is not strictly associative, and batching, kernel scheduling, and Mixture-of-Experts routing introduce run-to-run variance even when sampling is disabled. Determinism, when it matters, has to be engineered around the model rather than expected from the model: pin the API version, lock the exact model checkpoint used in production, and version prompts explicitly so a silent upstream change does not shift behavior underneath an evaluation suite.

The same caution applies across time, not just across runs. A prompt that returns a stable answer today can return a different one two days later, even with temperature held constant, because providers update models, routing, and infrastructure without changing the version string a team relies on. This is an argument against single-pass evaluation: a suite that passed once tells you about that one moment, not about the system going forward. Re-running the evaluation suite on a recurring basis, not just after a deliberate prompt change, is the only way to catch this kind of silent drift.

*Sources: Alexandre Balmes, Dev With AI Meetup, 2026; Brian Vermeer, Devoxx, 2026*

---

### Build a Scored Dataset, Not a Test Suite

The foundational shift is treating evaluation as: build a dataset of inputs paired with expected outputs, run a scoring function over agent responses, and track the score over time. The metric is a percentage, not a boolean. Moving from 85% to 87% to 89% is success; having a test suite that was green last week and is still green this week tells you nothing about the direction of travel.

This means collecting real inputs from production, labeling expected outputs (manually or with a larger LLM), and running the scoring function after every significant change to the agent prompt, model, or tool configuration.

*Source: Louis Pinsard (CTO, Dialogue), [IFTTD ep 338 "Evaluation de GenAI"](https://www.ifttd.io/episodes/evaluation-de-genai)*

---

### Match the Metric to the Pipeline Stage

Not every phase of an agent's lifecycle should be evaluated with the same rigor or cost. In the development loop, a fast and cheap metric is enough to catch obvious regressions quickly. During model selection, the evaluation can afford to be slower and more qualitative, since the decision is infrequent and the cost of getting it wrong is high. In production, the metric needs to be reliable and stable over long periods, since it is the signal a team trusts to detect real drift rather than noise.

Two additional defaults help avoid inflated confidence. Test out-of-distribution by default, not only on cases that resemble the training data; an agent that scores well on familiar inputs and fails on unfamiliar ones has an evaluation gap, not a working evaluation. And avoid benchmarks that may already be contaminated by the training data of the model under test, since a high score there measures memorization more than capability.

When evaluation relies on human raters or an LLM-as-judge, measuring raw percent agreement between evaluators overstates reliability, since two raters can agree by chance a large share of the time. Cohen's kappa corrects for that chance agreement and gives a more honest read on whether the evaluation criteria are actually well-defined.

*Source: Yann Dubois, Stanford CS224N, 2024 (cross-referenced in CS336 Lecture 12, 2026)*

---

### Statistical CI/CD: Replay, Do Not Assert

Because LLM outputs are non-deterministic, a single run of a test scenario proves nothing about reliability. The statistical CI/CD approach replays each key scenario 10 to 100 times in parallel and measures the success rate with a confidence interval. A regression is detected when the success rate drops below a threshold across many runs, not when a single run fails.

```bash
# Conceptual structure for a statistical eval run
for i in $(seq 1 50); do
  response=$(run_agent_task "create a migration for adding user_id to orders table")
  score=$(score_response "$response" "$EXPECTED_OUTPUT")
  echo "$score" >> eval_runs.txt
done

# Compute success rate
awk '{ total++; if ($1 >= 0.8) pass++ } END { print pass/total*100 "% pass rate" }' eval_runs.txt
```

Set a pass-rate threshold for each scenario (for example, 90% of runs must score above 0.8). Monitor threshold drift across agent versions and model updates.

*Source: Frédéric Barthelet (engineer), [IFTTD ep 329 "Front agentique"](https://www.ifttd.io/episodes/front-agentique)*

---

### Combine Frameworks and Force Structured Output

No single evaluation framework covers every metric a production system needs; one might handle factual accuracy well but say nothing useful about latency, cost, or tool-call correctness. Combining several frameworks, each covering the dimensions it is strongest at, gives a more complete picture than standardizing on one.

On the output side, forcing the model to return a structured schema (a Pydantic model or equivalent) rather than parsing free text pays off directly in evaluation quality. A scoring function that operates on typed fields is far less fragile than one built around regexes or string matching against loosely formatted prose, and it removes an entire class of evaluation bugs caused by output format drift rather than actual behavior change.

*Source: Mete Atamel, Devoxx, 2025*

---

### LLM-as-Judge: Run Asynchronously

LLM-as-judge uses a larger or more capable model to evaluate the output of the agent model. Running this synchronously on every user request penalizes all users for the failure rate of a minority of interactions. The pattern that works in production:

1. Serve the agent response immediately.
2. Log the input, output, and full context.
3. Run the judge model asynchronously on the logged data.
4. Use judge verdicts to update the dataset, adjust prompt thresholds, and flag regressions.

The judge model is typically larger than the production model (for example, using Opus 5 to judge outputs from Sonnet 5). It evaluates on dimensions like factual accuracy, instruction adherence, and hallucination presence. Over time the judge dataset becomes the primary signal for prompt iteration.

*Sources: Samy Lastmann (CTO, Smart Tribune), [IFTTD ep 311 "IA Agentique"](https://www.ifttd.io/episodes/ia-agentique); Louis Pinsard (CTO, Dialogue), [IFTTD ep 338 "Evaluation de GenAI"](https://www.ifttd.io/episodes/evaluation-de-genai)*

---

### Hallucination as a Trade-Off, Not a Bug

Hallucination is a structural feature of how LLMs are trained, not a defect that can be eliminated. The training process rewards confident answers over abstentions, which means models sometimes fabricate plausible-sounding content rather than saying they do not know.

The evaluation question is therefore: what balance of correct answers, abstentions, and hallucinations fits your use case? A system that is 85% correct, 10% abstaining, and 5% hallucinating may be preferable to one that is 80% correct, 19% abstaining, and 1% hallucinating, or vice versa, depending on the cost of each error type in context.

Tuning this balance involves adjusting confidence thresholds in the system prompt, providing retrieval context that anchors the model to factual material, and using the judge model to detect and flag hallucinated responses. The target is not zero hallucination; it is a calibrated and monitored rate that fits the application's risk tolerance.

*Source: Louis Pinsard (CTO, Dialogue), [IFTTD ep 338 "Evaluation de GenAI"](https://www.ifttd.io/episodes/evaluation-de-genai)*

---

### Observability: OpenTelemetry and Langfuse

For agentic pipelines, treat observability as a first-class requirement from day one. The standard approach uses OpenTelemetry for trace instrumentation and Langfuse (or a similar LLM observability platform) for storage, visualization, and alerting.

A basic trace structure for an agent interaction:

```
Trace: user_request_id
  Span: user_input          (latency, token count)
  Span: context_retrieval   (latency, sources_found)
  Span: llm_call_1          (model, input_tokens, output_tokens, latency)
    Span: tool_call         (tool_name, success, latency)
  Span: llm_call_2          (model, input_tokens, output_tokens, latency)
  Span: response            (output_tokens, total_latency)
```

This mirrors the Sentry span model and gives you the same observability for an LLM pipeline as for a conventional service. Key metrics to surface: p50/p95/p99 latency per span, token costs per interaction, tool call success rates, and judge scores over time.

Adding instrumentation retroactively is expensive and disruptive. Instrument before the first deployment.

*Source: Louis Pinsard (CTO, Dialogue), [IFTTD ep 338 "Evaluation de GenAI"](https://www.ifttd.io/episodes/evaluation-de-genai)*

---

### Workflow vs. Pure Agent: Evaluation Implications

Agentic workflows where the sequence of steps is predetermined are easier to evaluate than pure agents where the model decides its own path. In a workflow, each step has a defined expected output and can be evaluated independently. In a pure agent, the path to the result varies and you can only evaluate the final output.

If latency and cost are constraints (they almost always are), a deterministic workflow with LLM components at decision points evaluates more cheaply and reliably than an open-ended agent loop. Reserve the pure agent pattern for tasks where the sequence of actions is genuinely unknowable in advance.

*Source: Louis Pinsard (CTO, Dialogue), [IFTTD ep 338 "Evaluation de GenAI"](https://www.ifttd.io/episodes/evaluation-de-genai)*

---

### Evaluate Confidence, Not Coverage

A common trap in agent evaluation is treating test coverage (how many scenarios are scripted) as a proxy for how trustworthy the agent is. A more useful frame is confidence: how sure can you be that the agent behaves correctly, not just on the scenarios you tested, but on the ones you did not think to write.

Building that confidence requires evaluating at two levels simultaneously: each component in isolation (does the retrieval step return the right documents, does the tool call use the right parameters), and the complete system behavior including its guardrails, since a system built from individually correct components can still misbehave once the pieces interact. One practical structure organizes this around three pillars: principle (what the agent is fundamentally meant to do), policy (the explicit rules and guardrails constraining its behavior), and personality (the tone and interaction style users actually experience). Evaluating against all three catches failures that a purely functional test suite misses.

*Source: Jettro Coenradie & Daniël Spee, Devoxx, 2026*

---

### Skill Self-Improvement as Reinforcement Learning

Iterating on a skill (the instructions and structure that shape how an agent performs a task) can be treated as a lightweight reinforcement learning loop: make an incremental change, score the result against a binary or numeric criterion, keep the change if the score improves, discard it otherwise. This turns skill refinement into a repeatable, measurable process instead of an ad hoc round of prompt tweaking.

That evaluation needs to happen on two distinct layers. The first is activation: does the skill trigger at the right moment, given the right context and phrasing. The second is output quality: once triggered, does the skill produce a good result. A skill can fail on either layer independently, so scoring only the output misses activation failures, and scoring only activation misses cases where the skill fires correctly but produces a weak answer. Edge cases on either layer still benefit from human review rather than being folded automatically into the scoring loop.

*Sources: Emmanuel Sciara, Dev With AI Meetup, 2026; Negouai & Drode, 2026*

---

### Scope the Problem Before You Evaluate It

Before adding an LLM to a pipeline, or expanding what a model is asked to do, it is worth confirming that the LLM is actually solving a problem simpler methods cannot. Academic work on model selection makes the same point that practitioners report from production: added sophistication has to demonstrate a real marginal gain, an LLM remains hard to control precisely even in well-resourced teams, and prompting or retrieval-augmented generation is often preferable to costly fine-tuning when the simpler approach reaches comparable quality.

This scoping question also applies to what a single agent call should be trusted to do end to end. Combinatorial optimization problems (route planning, scheduling, bin-packing) are not something an LLM solves reliably by itself. The pattern that holds up better couples the model with a classical solver: the LLM interprets the problem and formats constraints, the solver computes the actual optimal or near-optimal solution. Asking the model to produce the full solution directly is a common source of confidently wrong output that no amount of prompt tuning fully fixes.

*Sources: Stanford ISLR (Hastie & Tibshirani) and CS230 Lecture 8, 2025; Tom Cools, Devoxx, 2026*

---

## Related Sections

- **[Agents](#4-agents)**: Creating custom agents
- **[Hooks](#7-hooks)**: Automation with event hooks
- **[Observability](../ops/observability.md)**: Logging and monitoring strategies
- **[AI Ecosystem](../ecosystem/ai-ecosystem.md#82-domain-specific-agent-frameworks)**: External frameworks like nao
- **[Practitioner Insights](../ecosystem/practitioner-insights.md)**: Field reports on evaluation practices from production teams

---

**Next steps**:
1. Add logging hook to your most-used agent
2. Collect 1 week of metrics
3. Analyze and refine agent based on data

**Template**: See `examples/agents/analytics-with-eval/` for complete implementation with hooks, scripts, and report template
