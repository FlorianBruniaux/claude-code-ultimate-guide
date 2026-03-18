# Cyber Defense Agent Team

A 4-agent pipeline that detects security threats in log files. Built natively with Claude Code Agent Teams.

**This example exists to compare two approaches**: LangGraph (the Python framework) vs Claude Code Agent Teams (native). Same system, two architectures. The delta tells you when to use which.

---

## Architecture

```
log-ingestor (haiku)
      ↓
anomaly-detector (sonnet)
      ↓
risk-classifier (sonnet)
      ↓
threat-reporter (sonnet)
      ↓
cyber-defense-report.md
```

Each agent has a single responsibility and passes data to the next via shared JSON files. The orchestration skill (`/cyber-defense-team`) sequences the spawns and reports results.

**Usage**: `/cyber-defense-team /var/log/nginx/access.log`

---

## LangGraph vs Claude Code Agent Teams

Same system built twice. Here's the full comparison.

### The LangGraph Version (~150 lines of Python)

```python
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import json

# ─── State Definition ─────────────────────────────────────────────────────────
class DefenseState(TypedDict):
    raw_logs: str
    parsed_events: List[dict]
    anomalies: List[dict]
    risk_level: str      # LOW | MEDIUM | HIGH | CRITICAL
    report: str

# ─── Tools (Python functions the LLM can call) ────────────────────────────────
@tool
def detect_patterns(logs: str) -> List[dict]:
    """Extract structured events from raw log text."""
    events = []
    for line in logs.split("\n"):
        if any(k in line for k in ["ERROR", "FAILED", "UNAUTHORIZED"]):
            events.append({"type": "security_event", "raw": line})
        elif "WARNING" in line:
            events.append({"type": "warning", "raw": line})
    return events

@tool
def detect_anomalies(events: List[dict]) -> List[dict]:
    """Detect statistical anomalies in event patterns."""
    anomalies = []
    error_count = sum(1 for e in events if e["type"] == "security_event")
    if error_count > 5:
        anomalies.append({"type": "high_error_rate", "count": error_count, "severity": "HIGH"})
    return anomalies

@tool
def lookup_threat(event_type: str) -> dict:
    """Look up known threat signatures."""
    db = {
        "UNAUTHORIZED": {"description": "Auth bypass attempt"},
        "SQL_INJECTION": {"cve": "CVE-2021-1234", "description": "SQLi pattern"}
    }
    return db.get(event_type, {"description": "Unknown threat"})

# ─── LLM Setup ────────────────────────────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools([detect_patterns, detect_anomalies, lookup_threat])

# ─── Nodes (one function per agent role) ──────────────────────────────────────
def ingest_node(state: DefenseState) -> DefenseState:
    events = detect_patterns.invoke(state["raw_logs"])
    return {**state, "parsed_events": events}

def detect_node(state: DefenseState) -> DefenseState:
    anomalies = detect_anomalies.invoke(state["parsed_events"])
    return {**state, "anomalies": anomalies}

def classify_node(state: DefenseState) -> DefenseState:
    result = llm_with_tools.invoke([
        SystemMessage("Classify risk as LOW/MEDIUM/HIGH/CRITICAL."),
        HumanMessage(f"Anomalies: {json.dumps(state['anomalies'])}")
    ])
    risk = "HIGH" if state["anomalies"] else "LOW"
    return {**state, "risk_level": risk}

def report_node(state: DefenseState) -> DefenseState:
    result = llm_with_tools.invoke([
        SystemMessage("You are a Senior Security Analyst. Write a Markdown incident report."),
        HumanMessage(f"Risk: {state['risk_level']}\nAnomalies: {json.dumps(state['anomalies'])}")
    ])
    return {**state, "report": result.content}

# ─── Conditional Edge ─────────────────────────────────────────────────────────
def should_report(state: DefenseState) -> str:
    return "report" if state["anomalies"] else END

# ─── Graph Assembly ───────────────────────────────────────────────────────────
builder = StateGraph(DefenseState)
builder.add_node("ingest", ingest_node)
builder.add_node("detect", detect_node)
builder.add_node("classify", classify_node)
builder.add_node("report", report_node)

builder.set_entry_point("ingest")
builder.add_edge("ingest", "detect")
builder.add_edge("detect", "classify")
builder.add_conditional_edges("classify", should_report)
builder.add_edge("report", END)

# ─── Memory ───────────────────────────────────────────────────────────────────
checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)

# ─── Entry Point ──────────────────────────────────────────────────────────────
def analyze_logs(logs: str) -> str:
    config = {"configurable": {"thread_id": "security-session-1"}}
    result = app.invoke(
        {"raw_logs": logs, "parsed_events": [], "anomalies": [], "risk_level": "", "report": ""},
        config
    )
    return result.get("report", "No threats detected.")
```

### The Claude Code Version (~60 lines of YAML/Markdown)

Four agent files, one skill file. No graph assembly, no TypedDict, no boilerplate.

```
examples/agents/cyber-defense/
├── log-ingestor.md       (~40 lines)
├── anomaly-detector.md   (~50 lines)
├── risk-classifier.md    (~55 lines)
└── threat-reporter.md    (~45 lines)

examples/skills/cyber-defense-team/
└── SKILL.md              (~70 lines)
```

Each agent file is a YAML frontmatter (name, model, tools) + a plain English system prompt describing role, inputs, outputs, and constraints. The skill file sequences the agents with `Agent tool` calls.

---

## Side-by-Side Comparison

| Dimension | LangGraph | Claude Code Agent Teams |
|-----------|-----------|------------------------|
| **Total code** | ~150 lines Python | ~60 lines YAML/Markdown |
| **State management** | Explicit `TypedDict` definition | Implicit — JSON files between agents |
| **Memory** | Manual `MemorySaver` setup | Native (files persist by default) |
| **Tool definition** | `@tool` decorated Python functions | MCP servers or built-in tools |
| **Conditional logic** | `add_conditional_edges()` | Natural language in skill ("if no anomalies, skip to Step 5") |
| **Model selection** | One model for all nodes | Per-agent (haiku for parsing, sonnet for reasoning) |
| **Debugging** | `print()` + LangSmith (paid) | Native Claude Code UI |
| **New agent role** | New function + `add_node()` + `add_edge()` | New `.md` file |
| **Onboarding** | Learn LangGraph API | Read a Markdown file |
| **Deployment** | FastAPI or Gradio (~50 more lines) | `claude` CLI, done |
| **Dependencies** | `langgraph`, `langchain`, `langchain-openai` | None (built into Claude Code) |

---

## When to Use Which

**Use Claude Code Agent Teams when:**
- You want to move fast — prototype to working system in 30 minutes
- Your team includes non-developers who may read or edit agent prompts
- The pipeline is internal tooling (not a public API endpoint)
- You need to iterate on agent behavior frequently (edit a `.md` file, done)

**Use LangGraph when:**
- You need to embed the system inside a larger Python application
- You want to expose the pipeline as a REST API for external consumers
- You need deterministic state transitions that must be unit-tested
- Your team is already Python-native and has LangGraph expertise

**The honest tradeoff**: LangGraph gives you more programmatic control and Python ecosystem access. Claude Code Agent Teams give you less boilerplate, faster iteration, and no infrastructure to maintain. For internal tooling and knowledge work pipelines, the Claude Code approach typically wins on total cost of ownership.

---

## Files in This Example

| File | Agent Role | Model | Responsibility |
|------|-----------|-------|----------------|
| `log-ingestor.md` | Stage 1 | haiku | Parse raw logs → `cyber-defense-events.json` |
| `anomaly-detector.md` | Stage 2 | sonnet | Detect patterns → `cyber-defense-anomalies.json` |
| `risk-classifier.md` | Stage 3 | sonnet | Score risk → `cyber-defense-risk.json` |
| `threat-reporter.md` | Stage 4 | sonnet | Generate → `cyber-defense-report.md` |
| `../skills/cyber-defense-team/SKILL.md` | Orchestrator | — | Sequence agents, handle errors, summarize |

---

**Inspired by**: Maryam Miradi's SMART COMPASS framework — same system, different stack.
