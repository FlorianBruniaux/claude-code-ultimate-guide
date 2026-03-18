---
title: "Analytics Agent Evaluation Report"
description: "Monthly evaluation template for scoring analytics agent performance and accuracy"
tags: [template, agents, testing]
---

# Analytics Agent Evaluation Report

**Month**: [YYYY-MM]
**Report Date**: [YYYY-MM-DD]
**Evaluator**: [Your Name]
**Agent Version**: 1.0

---

## Executive Summary

[2-3 sentence overview of agent performance this month]

**Key Metrics**:
- Total queries: [X]
- Safety pass rate: [Y]%
- Avg execution time: [Z]s

**Status**: 🟢 Healthy / 🟡 Needs Attention / 🔴 Critical

---

## Metrics Overview

### Volume

| Metric | Value |
|--------|-------|
| Total queries generated | [X] |
| Unique users/sessions | [Y] |
| Queries per day (avg) | [Z] |
| Growth vs last month | [+/-]% |

### Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Safety pass rate | >95% | [X]% | 🟢/🟡/🔴 |
| Query correctness | >90% | [Y]% | 🟢/🟡/🔴 |
| User satisfaction | >4.0/5 | [Z]/5 | 🟢/🟡/🔴 |

### Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Mean execution time | <3s | [X]s | 🟢/🟡/🔴 |
| P95 execution time | <5s | [Y]s | 🟢/🟡/🔴 |
| P99 execution time | <10s | [Z]s | 🟢/🟡/🔴 |

---

## Safety Analysis

### Safety Check Results

```
Total: [X] queries
- PASS: [Y] ([Z]%)
- FAIL: [A] ([B]%)
```

### Top Safety Failures

1. **[Failure Type]** - [X] occurrences
   - Example: `[SQL query snippet]`
   - Root cause: [Brief explanation]
   - Action: [What was done to fix]

2. **[Failure Type]** - [Y] occurrences
   - Example: `[SQL query snippet]`
   - Root cause: [Brief explanation]
   - Action: [What was done to fix]

### Trends

[Graph or description showing safety pass rate over time]

---

## Performance Analysis

### Execution Time Distribution

```
Mean:   [X]s
Median: [Y]s
P95:    [Z]s
P99:    [A]s
Max:    [B]s
```

### Slowest Queries

1. **[Query description]** - [X]s
   ```sql
   [SQL query]
   ```
   - Reason: [Why slow]
   - Optimization: [What could improve it]

2. **[Query description]** - [Y]s
   ```sql
   [SQL query]
   ```
   - Reason: [Why slow]
   - Optimization: [What could improve it]

---

## User Feedback

### Explicit Feedback

- **Positive**: [X] responses
  - Common praise: "[Theme 1]", "[Theme 2]"
- **Negative**: [Y] responses
  - Common complaints: "[Theme 1]", "[Theme 2]"

### Implicit Signals

- **Query retry rate**: [X]% (users re-running queries)
- **Query modification rate**: [Y]% (users editing generated queries)
- **Adoption rate**: [Z] queries/user/week

### Notable Feedback

> "[User quote 1]"
— [User name/role, if available]

> "[User quote 2]"
— [User name/role, if available]

---

## Incident Log

### Critical Issues

| Date | Issue | Impact | Resolution |
|------|-------|--------|------------|
| [YYYY-MM-DD] | [Brief description] | [High/Medium/Low] | [What was done] |

### Near-Misses

[List of queries that almost caused problems but were caught by safety checks]

---

## Improvements Made

### Agent Instruction Updates

1. **[Update 1]**
   - **Reason**: [Why needed]
   - **Change**: [What was modified in agent instructions]
   - **Impact**: [Expected improvement]

2. **[Update 2]**
   - **Reason**: [Why needed]
   - **Change**: [What was modified]
   - **Impact**: [Expected improvement]

### Hook/Metrics Updates

- [Any changes to metrics collection or analysis]

---

## A/B Test Results (if applicable)

### Test: [Description]

**Period**: [Start date] to [End date]

**Variants**:
- **Control (A)**: [Description]
- **Experiment (B)**: [Description]

**Metrics**:

| Metric | Control (A) | Experiment (B) | Change |
|--------|-------------|----------------|--------|
| Safety pass rate | [X]% | [Y]% | [+/-]% |
| Avg exec time | [X]s | [Y]s | [+/-]s |
| User satisfaction | [X]/5 | [Y]/5 | [+/-] |

**Decision**: ✅ Promote B / ❌ Keep A / ⏸️ Needs more data

**Rationale**: [Why this decision]

---

## Recommendations

### High Priority

1. **[Recommendation 1]**
   - **Current state**: [Problem description]
   - **Proposed change**: [What to do]
   - **Expected impact**: [Improvement estimate]
   - **Effort**: Low/Medium/High

### Medium Priority

1. **[Recommendation 2]**
   - **Current state**: [Problem description]
   - **Proposed change**: [What to do]
   - **Expected impact**: [Improvement estimate]
   - **Effort**: Low/Medium/High

### Low Priority / Future

- [Quick list of nice-to-have improvements]

---

## Next Month Goals

1. **[Goal 1]**: [Specific, measurable target]
2. **[Goal 2]**: [Specific, measurable target]
3. **[Goal 3]**: [Specific, measurable target]

---

## Appendix

### Methodology

**Data sources**:
- `.claude/logs/analytics-metrics.jsonl` (automated metrics)
- User feedback forms
- Manual query reviews

**Analysis tools**:
- `eval/metrics.sh` for automated reporting
- SQL queries for deep-dive analysis
- Manual review of safety failures

**Limitations**:
- [Any known gaps in data collection]
- [Potential biases in analysis]

### Raw Data

**Export**: `analytics-metrics-[YYYY-MM].json`

**Query**:
```bash
jq 'select(.timestamp >= "2026-MM-01" and .timestamp < "2026-MM+1-01")' \
  .claude/logs/analytics-metrics.jsonl > analytics-metrics-2026-MM.json
```

---

**Previous Reports**: [Link to folder with past reports]

**Questions?** Contact [evaluation team email/slack]
