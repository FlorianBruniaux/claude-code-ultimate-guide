# Resource Evaluation: nao Framework

**URL**: https://github.com/getnao/nao/
**Type**: Open-source framework for building analytics agents
**Evaluation Date**: 2026-02-10
**Evaluator**: Claude Code (with technical-writer challenge)
**Target Guide**: Claude Code Ultimate Guide

---

## Summary

**nao** is an open-source framework for building and deploying analytics agents with a two-step architecture: build agent context via CLI tools, then deploy chat UI for end users to query data conversationally.

**Key Features**:
- Context builder supporting flexible data, metadata, documentation, and tool integrations
- Database agnostic (PostgreSQL, BigQuery, Snowflake, Databricks)
- Built-in evaluation framework with unit testing capabilities
- Self-hosted deployment with Docker containerization
- Native data visualization within chat interface
- Tech stack: Fastify, Drizzle ORM, tRPC, React, shadcn UI (TypeScript 58.9%, Python 38.5%)

---

## Relevance Score: 3/5 (Moderate - Useful Complement)

### Initial Score: 2/5 → Adjusted to 3/5 after technical challenge

**Justification for 3/5**:

**Relevance (+2 points)**:
- ✅ **Transposable architecture patterns** to Claude Code agents (.claude/agents/)
- ✅ **Evaluation framework** addresses critical gap in guide (no section on agent evaluation)
- ✅ **Database context patterns** applicable to agents with DB integrations

**Limitations (-2 points)**:
- ❌ No direct integration with Claude Code CLI (not a plugin/MCP server)
- ❌ Deployment scope (production chat UI) differs from guide's dev CLI focus

**Partial overlap**: Agent concepts and evaluation patterns are transposable, but final product (deployed analytics UI) is not guide's focus.

---

## Comparative Analysis

| Aspect | nao | Current Guide | Gap? |
|--------|-----|---------------|------|
| **Custom Agents** | ✅ Complete build + deploy framework | ✅ Extensive docs (.claude/agents/) | ➖ No |
| **Agent Architecture** | ➕ Structured context builder pattern | ⚠️ No complex context patterns | ✅ **Minor gap** |
| **Agent Evaluation** | ➕ Integrated framework (metrics, unit tests, feedback) | ❌ No mention | ✅ **Critical gap** |
| **Database Integrations** | ➕ Native support: BigQuery, Snowflake, Databricks, PostgreSQL | ✅ Mentioned (database-branch-setup.md) | ➖ No |
| **Agent Deployment** | ➕ Deployable chat UI with visualizations | ❌ Not covered (CLI focus) | ⚠️ Out of scope |
| **Analytics-Specific** | ➕ Specialized for conversational analytics | ❌ No analytics focus | ➖ No |
| **Context Management** | ✅ Context builder with docs/metadata | ✅ CLAUDE.md, .claude/rules/ | ➖ No |
| **Self-Hosted** | ✅ Docker + deployment guides | ✅ Mentioned (security-hardening.md) | ➖ No |

---

## Integration Recommendations

**Score 3/5 → Integrate (3 approaches)**

### ✅ Priority 1: Dedicated Section (Recommended)

**Create**: `guide/agent-evaluation.md` (~800 tokens)

**Content**:
- **Why Evaluate?**: Measure quality, track usage, identify bottlenecks
- **Metrics to Track**: Response time, tool call success rate, context relevance, error rate
- **Implementation Patterns**: Logging hooks, metrics aggregation, A/B testing, feedback collection
- **Reference**: Mention nao as complete evaluation framework

**Estimated tokens**: 500-800
**Suggested timeline**: Week 1
**Insertion point**: After `guide/ultimate-guide.md` section 4 (Agents)

---

### ✅ Priority 2: Agent Template with Evaluation (Optional)

**Create**: `examples/agents/analytics-with-eval/`

**Structure**:
```
analytics-with-eval/
├── config.yaml          # Agent config
├── context.md           # Agent instructions
├── eval/
│   ├── metrics.sh       # Collect metrics
│   └── report.md        # Example report
└── hooks/
    └── post_response.sh # Log response metrics
```

**Estimated tokens**: 300-400 (code + README)
**Suggested timeline**: Week 2-3
**Value**: Demonstrates concrete evaluation patterns

---

### ✅ Priority 3: Ecosystem Mention (Minimal)

**Add**: Section "Domain-Specific Agent Frameworks" in `guide/ai-ecosystem.md`

**Content**: 1 paragraph + link to nao

**Estimated tokens**: 100-150
**Suggested timeline**: Immediate
**Suggested line**: After orchestration frameworks section (~line 2200)

---

## Technical Challenge Results

The technical-writer agent identified several biases in the initial evaluation:

### Missed Points in Initial Evaluation

1. **Transposable agent architecture**: nao's `context builder` pattern applicable to Claude Code agents
2. **Evaluation framework = critical gap**: Guide has NO mention of agent evaluation (metrics, testing, feedback)
3. **Database context patterns**: Patterns for context injection from databases not documented

### Score Justification

**Correction**: 2/5 → **3/5** (Moderate)

**Arguments for 3/5**:
- Transposable architecture patterns (+1)
- Evaluation framework addresses identified gap (+1)
- Usable database context patterns (+0.5)
- Open-source, well-documented (+0.5)

### Gap "Agent Evaluation" Must Be Addressed

**YES, the guide MUST have this section** because:
- Devs create agents without knowing how to measure quality
- Anthropic docs mention evaluations but not in Claude Code context
- nao proves this is feasible and useful (production-ready)

### Risks of Non-Integration

1. **Evaluation gap remains undocumented** → Devs don't know how to measure agent quality
2. **Database context patterns undocumented** → Devs reinvent already-proven patterns
3. **Loss of credibility** → If evaluation becomes standard, guide will be behind

### Why Initial Evaluation Was Biased

1. **Confusion between scope and relevance**: Different scope ≠ not relevant
2. **Focus on final product**: Evaluated nao as *competing product*, not *pattern source*
3. **Underestimation of gaps**: Agent evaluation = critical gap not previously identified
4. **Premature rejection**: "Don't integrate" despite identifying 2 major gaps

**Lesson**: Evaluate resources for *transposable patterns*, not just direct integration.

---

## Fact-Check Results

All technical claims verified by re-fetching GitHub repository:

| Claim | Verified | Source |
|-------|----------|--------|
| TypeScript 58.9%, Python 38.5% | ✅ | Repository footer |
| Stack: Fastify, Drizzle, tRPC, React, shadcn, TanStack Query | ✅ | "Stack" section |
| Databases: PostgreSQL, BigQuery, Snowflake, Databricks | ✅ | Repository topics |
| Evaluation framework with unit testing | ✅ | "Evaluation framework" section |
| GitHub repo integration + Slack bot | ✅ | Quickstart + topics |
| Docker containerization + self-hosted | ✅ | "Docker" section + docs |

**Corrections made**: None (all initial claims were accurate)

**Stats requiring external research**: None (all verifiable on GitHub page)

---

## Final Decision

- **Final Score**: **3/5 (Moderate - Useful Complement)**
- **Action**: **Integrate** via 3 approaches (priority 1 + 2 + 3)
- **Confidence**: **High** (all claims fact-checked ✅)

### Concrete Action Plan

1. **Immediate** (today): Add mention in `guide/ai-ecosystem.md` section "Domain-Specific Agent Frameworks"
2. **Week 1**: Create `guide/agent-evaluation.md` with patterns inspired by nao
3. **Week 2-3**: Create template `examples/agents/analytics-with-eval/` with metrics

### Added Value for Guide

- ✅ Addresses critical gap (agent evaluation)
- ✅ Adds transposable patterns (context builder, DB integrations)
- ✅ Demonstrates complete lifecycle (build → eval → iterate)
- ✅ References production-ready framework in specific domain

---

## Metadata

**Evaluation performed with**: WebFetch (2×), Grep (3×), Task (technical-writer challenge)
**Evaluation time**: ~15 minutes
**Quality**: Complete challenge + fact-check ✅
**Follow-up**: Implement integration recommendations (A, B, C)
