---
title: "Production Reliability Patterns"
description: "Escalation design, circuit breakers, structured error propagation, graceful degradation, human handoff, and source conflict resolution for Claude-powered systems"
tags: [workflow, reliability, production, escalation, circuit-breaker, error-handling]
---

# Production Reliability Patterns

> **Confidence**: Tier 2. Patterns derived from production deployments. Core design principles are stable; specific thresholds and field names will vary by system.

Claude-powered systems fail in ways that differ from traditional software. The model may produce syntactically valid output that is semantically wrong, may refuse to continue when it cannot make progress, or may produce partial results when source data is incomplete. The patterns below address each of these failure modes in production.

---

## Table of Contents

1. [Escalation Design](#escalation-design)
2. [Circuit Breaker Pattern](#circuit-breaker-pattern)
3. [Structured Error Propagation](#structured-error-propagation)
4. [Partial Results and Coverage Annotations](#partial-results-and-coverage-annotations)
5. [Structured Human Handoff](#structured-human-handoff)
6. [Source Conflict Resolution](#source-conflict-resolution)
7. [Anti-Patterns](#anti-patterns)
8. [See Also](#see-also)

---

## Escalation Design

The single most common reliability mistake is using LLM confidence scores as the primary escalation signal. Confidence scores are not calibrated probabilities: a model can output a high confidence value while being factually wrong. Production escalation should be driven by programmatic signals, not by numeric confidence values.

### The Three Canonical Escalation Triggers

In a well-designed system, escalation occurs when exactly one of three conditions is met.

**1. Explicit user request:** The customer explicitly asks for a human. This is non-negotiable and takes priority over every other signal, including frustration detection. "I want to speak to a human" is a different signal from an angry tone, and it requires immediate handoff regardless of what the AI could have done next.

**2. Policy gap:** The request falls outside the system's defined scope and cannot be handled by any available tool or knowledge. This is not a model failure; it is a scope boundary. The correct response is a structured escalation with context, not an apology loop.

**3. Inability to make progress:** After a defined number of attempts or tool calls, the system has not produced a valid result. This is measured programmatically: retry budget exhausted, circuit breaker open, or validation loop failed.

### Programmatic Escalation Signals

```python
from enum import Enum
from dataclasses import dataclass

class EscalationReason(Enum):
    EXPLICIT_REQUEST = "explicit_request"
    POLICY_GAP = "policy_gap"
    MAX_RETRIES_EXCEEDED = "max_retries_exceeded"
    CIRCUIT_BREAKER_OPEN = "circuit_breaker_open"
    MISSING_REQUIRED_TOOL = "missing_required_tool"

@dataclass
class EscalationSignal:
    should_escalate: bool
    reason: EscalationReason | None
    context: dict

def evaluate_escalation(
    user_message: str,
    attempt_count: int,
    policy_coverage: str,  # "covered" | "gap" | "out_of_scope"
    max_attempts: int = 3
) -> EscalationSignal:

    # Priority 1: explicit user request, check first, unconditionally
    if contains_explicit_escalation_request(user_message):
        return EscalationSignal(
            should_escalate=True,
            reason=EscalationReason.EXPLICIT_REQUEST,
            context={"trigger": "user_stated_intent"}
        )

    # Priority 2: policy gap
    if policy_coverage in ("gap", "out_of_scope"):
        return EscalationSignal(
            should_escalate=True,
            reason=EscalationReason.POLICY_GAP,
            context={"coverage": policy_coverage}
        )

    # Priority 3: inability to progress
    if attempt_count >= max_attempts:
        return EscalationSignal(
            should_escalate=True,
            reason=EscalationReason.MAX_RETRIES_EXCEEDED,
            context={"attempts": attempt_count, "max": max_attempts}
        )

    return EscalationSignal(should_escalate=False, reason=None, context={})

def contains_explicit_escalation_request(message: str) -> bool:
    explicit_phrases = [
        "speak to a human", "talk to a person", "real agent",
        "human agent", "transfer me", "escalate this",
        "supervisor", "manager"
    ]
    message_lower = message.lower()
    return any(phrase in message_lower for phrase in explicit_phrases)
```

### Frustration vs Explicit Escalation

These are two completely different signals that require opposite responses. Frustration (angry tone, repeated questions, "this is useless") is a signal to acknowledge empathetically and try a different approach. An explicit escalation request ("I want to talk to a person") is a signal to hand off immediately.

Conflating them is a common mistake with real consequences: routing frustrated users to humans when they just wanted a better answer, or continuing to try harder when the user has already decided they want a human agent.

```python
def classify_user_signal(message: str) -> dict:
    # These patterns can coexist: check both independently
    frustration_markers = [
        "this is ridiculous", "not helpful", "keep asking",
        "not answering", "useless", "terrible", "waste"
    ]
    escalation_markers = [
        "speak to a human", "real person", "agent", "transfer",
        "supervisor", "escalate", "don't want ai"
    ]

    message_lower = message.lower()

    return {
        "frustrated": any(m in message_lower for m in frustration_markers),
        "wants_escalation": any(m in message_lower for m in escalation_markers)
    }

# Usage:
signals = classify_user_signal(user_message)

if signals["wants_escalation"]:
    initiate_human_handoff(context)   # immediate, unconditional
elif signals["frustrated"]:
    adjust_response_approach()        # more empathetic, different angle
```

### Rule-Based Routing from Structured Output

Where possible, derive escalation decisions from structured output fields rather than from model-level confidence. If the model produces a structured result with `policy_gap: true` or `requires_human_review: true`, those fields are deterministic routing signals, with no confidence score interpretation needed.

```python
@dataclass
class AgentDecision:
    response_text: str
    policy_gap: bool
    requires_human_review: bool
    coverage_level: str  # "full" | "partial" | "none"
    missing_information: list[str]

def route_from_structured_output(decision: AgentDecision) -> str:
    if decision.policy_gap or decision.coverage_level == "none":
        return "escalate"
    if decision.requires_human_review or decision.coverage_level == "partial":
        return "queue_for_review"
    return "respond"
```

---

## Circuit Breaker Pattern

A circuit breaker prevents a failing dependency (API, tool, external service) from creating cascading failures. Without it, every agent call that touches a failing service will hang until timeout, consuming resources and degrading the entire pipeline.

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"        # normal operation
    OPEN = "open"            # failing, reject calls immediately
    HALF_OPEN = "half_open"  # testing recovery

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: float | None = None

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitOpenError(
                    f"Circuit open since {self.last_failure_time:.0f}. "
                    f"Recovery in {self._time_until_recovery():.0f}s"
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_recovery(self) -> bool:
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.recovery_timeout

    def _time_until_recovery(self) -> float:
        if self.last_failure_time is None:
            return 0.0
        return max(0.0, self.recovery_timeout - (time.time() - self.last_failure_time))

class CircuitOpenError(Exception):
    pass
```

### Per-Document Isolation in Batch Pipelines

In batch processing pipelines, each document should have its own error boundary. One document's failure should not abort the remaining batch.

```python
def process_document_batch(documents: list[str], processor) -> list[dict]:
    results = []
    circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30.0)

    for doc_id, document in enumerate(documents):
        try:
            result = circuit_breaker.call(processor, document)
            results.append({"doc_id": doc_id, "status": "success", "result": result})
        except CircuitOpenError as e:
            # Circuit open: skip remaining docs and surface the condition upstream
            results.append({"doc_id": doc_id, "status": "circuit_open", "error": str(e)})
            for remaining_id in range(doc_id + 1, len(documents)):
                results.append({
                    "doc_id": remaining_id,
                    "status": "skipped",
                    "reason": "circuit_open"
                })
            break
        except Exception as e:
            results.append({"doc_id": doc_id, "status": "error", "error": str(e)})

    return results
```

The circuit breaker closes at the batch level, not the document level. When it opens, you want to know that the underlying service is unavailable, not that three individual documents happened to fail in sequence.

---

## Structured Error Propagation

In multi-agent systems, errors passed as generic exception strings lose the context needed for recovery. Structured errors carry the information the upstream orchestrator needs to decide whether to retry, reroute, or escalate.

```python
from dataclasses import dataclass

@dataclass
class StructuredAgentError:
    error_category: str           # "tool_failure" | "validation_error" | "policy_gap" | "timeout"
    is_retryable: bool
    failure_type: str             # specific subtype within the category
    attempted_query: str | None   # what was tried (useful for debugging)
    partial_results: dict | None  # any usable output produced before the failure
    alternative_approach: str | None  # suggestion for the orchestrator
    error_message: str
    attempt_count: int = 1

    def to_dict(self) -> dict:
        return {
            "error_category": self.error_category,
            "is_retryable": self.is_retryable,
            "failure_type": self.failure_type,
            "attempted_query": self.attempted_query,
            "has_partial_results": self.partial_results is not None,
            "alternative_approach": self.alternative_approach,
            "error_message": self.error_message,
            "attempt_count": self.attempt_count
        }

# Usage in a sub-agent:
def search_database(query: str) -> dict:
    try:
        return db.search(query)
    except DatabaseTimeoutError:
        raise StructuredAgentError(
            error_category="tool_failure",
            is_retryable=True,
            failure_type="database_timeout",
            attempted_query=query,
            partial_results=None,
            alternative_approach="retry with narrower query or use cached results",
            error_message="Database query timed out after 30s"
        )
    except NoResultsError:
        raise StructuredAgentError(
            error_category="tool_failure",
            is_retryable=False,
            failure_type="no_results",
            attempted_query=query,
            partial_results=None,
            alternative_approach="try broader search terms or escalate to human",
            error_message=f"No results found for query: {query}"
        )

# Orchestrator handling:
def orchestrate_with_recovery(agent_fn, query: str, max_retries: int = 2) -> dict:
    for attempt in range(max_retries + 1):
        try:
            return agent_fn(query)
        except StructuredAgentError as e:
            if not e.is_retryable or attempt == max_retries:
                return {
                    "status": "failed",
                    "error": e.to_dict(),
                    "partial_results": e.partial_results,
                    "requires_escalation": not e.is_retryable
                }
            # Retryable: apply the suggested alternative approach if present
            if e.alternative_approach:
                query = refine_query(query, e.alternative_approach)
```

The key field is `is_retryable`. An orchestrator that cannot tell whether to retry or escalate will default to retrying everything, which wastes budget on non-retryable errors and misses the window on transient ones.

---

## Partial Results and Coverage Annotations

When a pipeline cannot fully complete a task, returning partial results with explicit coverage annotations is more useful than returning nothing. The consumer can then decide whether the partial result is actionable without needing to understand the internals of what failed.

```python
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    full_analysis: str | None
    section_results: dict[str, dict]  # section_id -> result
    coverage_summary: dict

def annotate_coverage(section_results: dict) -> dict:
    coverage_map = {}
    for section_id, result in section_results.items():
        if result.get("status") == "success" and result.get("confidence", 0) >= 0.8:
            coverage_map[section_id] = "well-supported"
        elif result.get("status") == "success":
            coverage_map[section_id] = "partially-supported"
        else:
            coverage_map[section_id] = "gap"

    counts = {"well-supported": 0, "partially-supported": 0, "gap": 0}
    for v in coverage_map.values():
        counts[v] += 1

    return {
        "sections": coverage_map,
        "counts": counts,
        "overall_coverage": counts["well-supported"] / len(coverage_map) if coverage_map else 0.0,
        "has_gaps": counts["gap"] > 0
    }
```

Surface coverage annotations in the response so downstream consumers can act on them without parsing internal state:

```
CONTRACT ANALYSIS SUMMARY

Section 1 (Payment Terms): well-supported (full analysis available)
Section 2 (Liability Clauses): partially-supported (analysis based on partial text; recommend manual review)
Section 3 (Termination Rights): gap (source text was unreadable; human review required)

Overall coverage: 67% (2 of 3 sections fully analyzed)
```

This pattern applies anywhere a pipeline may produce incomplete output: document extraction, multi-source research, batch translation, or regulatory compliance checks where some clauses lack supporting data.

---

## Structured Human Handoff

When escalation occurs, the human agent receives a structured payload rather than raw conversation history. The goal is that the human can begin working within 30 seconds, without reading back through an entire conversation log.

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class HandoffPayload:
    customer_id: str
    session_id: str
    escalation_reason: str        # from EscalationReason enum
    original_request: str         # verbatim first user message
    conversation_summary: str     # 3-5 sentence summary of what happened
    root_cause: str               # why the AI could not resolve this
    actions_taken: list[str]      # what was tried
    recommended_next_action: str  # specific suggestion for the human agent
    partial_results: dict | None  # any useful output produced
    urgency: str                  # "high" | "medium" | "low"
    created_at: str               # ISO 8601

def build_handoff(
    session: dict,
    escalation_signal: EscalationSignal,
    conversation_history: list[dict]
) -> HandoffPayload:
    return HandoffPayload(
        customer_id=session["customer_id"],
        session_id=session["session_id"],
        escalation_reason=escalation_signal.reason.value,
        original_request=conversation_history[0]["content"] if conversation_history else "",
        conversation_summary=summarize_conversation(conversation_history),
        root_cause=derive_root_cause(escalation_signal),
        actions_taken=extract_actions_taken(session),
        recommended_next_action=suggest_next_action(escalation_signal),
        partial_results=session.get("partial_results"),
        urgency="high" if escalation_signal.reason == EscalationReason.EXPLICIT_REQUEST else "medium",
        created_at=datetime.utcnow().isoformat()
    )
```

### Handoff Display Format

What the human agent actually sees should read as a structured brief, not a data dump:

```
ESCALATION BRIEF: Session a1b2c3d4
Reason: Customer requested human agent
Urgency: HIGH

ORIGINAL REQUEST
"I need to cancel my subscription and get a refund for last month's charge"

WHAT HAPPENED
The customer asked to cancel their subscription and requested a refund for the
charge processed on May 18. The AI confirmed account details and found the charge
($49.00) but hit a policy gap: refund approval for charges older than 7 days
requires manual authorization. Two escalation attempts were made; the customer
then explicitly requested a human agent.

ACTIONS TAKEN
- Account verified (customer_id: 88821)
- Charge located: $49.00 on 2026-05-18
- Subscription status: active

RECOMMENDED NEXT ACTION
Authorize refund for $49.00 (charge is 6 days old, within 7-day window) and
process cancellation. No additional verification needed.
```

The `recommended_next_action` field is the most valuable part. A human agent who receives a specific recommendation resolves the case faster and is less likely to ask the customer to repeat information.

---

## Source Conflict Resolution

When multiple sources disagree, the resolution strategy depends on why they disagree. Temporal differences (one source is newer than another) call for a different approach than factual conflicts (sources about the same time period disagree on the facts).

```python
@dataclass
class Source:
    source_id: str
    content: str
    publication_date: str | None  # ISO 8601, mandatory for temporal disambiguation
    source_type: str              # "official" | "news" | "user_generated" | "internal"
    authority_score: float        # 0.0-1.0, domain-specific

def resolve_conflict(sources: list[Source], field: str) -> dict:
    values = [s for s in sources if get_field_value(s, field) is not None]

    if len(values) <= 1:
        return {"resolved": values[0] if values else None, "conflict": False}

    # Check for temporal difference first
    dated = [s for s in values if s.publication_date is not None]
    if len(dated) == len(values):
        sorted_by_date = sorted(dated, key=lambda s: s.publication_date, reverse=True)
        newest = sorted_by_date[0]
        second_newest = sorted_by_date[1] if len(sorted_by_date) > 1 else None

        if (second_newest is not None and
                get_field_value(newest, field) == get_field_value(second_newest, field)):
            # Two most recent sources agree: likely a correct update
            return {
                "resolved": newest,
                "conflict": False,
                "resolution_method": "temporal_precedence"
            }

    # Genuine factual conflict: do not resolve automatically
    return {
        "resolved": None,
        "conflict": True,
        "conflict_type": "factual",
        "conflicting_sources": [s.source_id for s in values],
        "requires_human_review": True
    }
```

Always include `publication_date` in source metadata. Without it, temporal disambiguation is impossible and what looks like a factual conflict may simply be an outdated source that hasn't been retired.

### Surfacing Conflicts in Output

When a genuine conflict cannot be resolved automatically, surface it explicitly rather than silently picking one source:

```
FIELD: regulatory_status

SOURCE A (internal-policy-doc, 2026-01-15): "Approved for EU markets"
SOURCE B (legal-review-2026, 2026-03-22): "Pending re-approval: EU regulatory update in progress"

CONFLICT TYPE: factual (same field, same jurisdiction, different values)
RESOLUTION: Cannot auto-resolve. Human review required before using this field.
```

This is better than returning a single answer without attribution. A consumer who sees a confident answer without knowing it was contested cannot make an informed decision about whether to act on it.

---

## Anti-Patterns

**Using confidence scores as routing logic.** Confidence scores from LLMs are not calibrated probabilities. Use programmatic signals instead: retry count, circuit state, structured output fields.

**Conflating frustration with escalation intent.** Frustrated users often want a better answer, not a human. Users who say "I want a human" always want a human. Treat them as distinct signals with distinct responses.

**Passing unstructured exceptions between agents.** A string like `"DatabaseError: connection refused"` tells the orchestrator nothing about whether to retry or escalate. Use structured error types with `is_retryable`, `error_category`, and `alternative_approach`.

**Returning nothing when partial results exist.** A partial result with a clear coverage annotation is almost always more useful than an empty response with an error message. The consumer can decide what to do with "67% coverage"; they cannot decide anything from "analysis failed".

**Skipping `publication_date` in source metadata.** Without dates, temporal conflicts look like factual conflicts. Every source ingested into a pipeline should carry a date, even an approximate one.

**Building handoffs as conversation dumps.** Pasting the last 20 turns of conversation into a ticket is not a handoff; it is work-transfer. A structured handoff payload with `recommended_next_action` is what separates a good escalation system from a slow one.

---

## See Also

- [Agent Teams](agent-teams.md): orchestrator/subagent architecture and tool routing
- [Event-Driven Agents](event-driven-agents.md): trigger-based automation and retry loops
- [Task Management](task-management.md): persistent state for multi-step agent workflows
- [Plan-Driven Workflow](plan-driven.md): planning phase before execution to reduce mid-task failures
