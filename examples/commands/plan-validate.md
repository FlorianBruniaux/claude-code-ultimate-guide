---
name: plan-validate
description: "2-layer plan validation: instant structural checks + trigger-based specialist agents. Auto-fixes issues using ADRs and first principles. Every issue must be resolved before execution."
---

# Plan Validate — 2-Layer Validation

Independently validate the plan produced by `/plan-start`. No code is written. Run `/clear` after this command before running `/plan-execute`.

Validation is separate from planning by design: validators that didn't write the plan are not anchored to its assumptions.

---

## Prerequisite

A committed plan file must exist at `docs/plans/plan-{name}.md`. If multiple plans exist, list them and ask the user which to validate.

---

## Layer 1: Structural Validation

Run immediately, no agents required. Check the plan document for:

**Format & Completeness**
- [ ] All required sections present (Summary, Decisions, Architecture, Tasks, Test Plan, Out of Scope)
- [ ] Each task has: description, files affected, acceptance criteria, layer assignment

**Dependency Chain**
- [ ] No circular dependencies between tasks
- [ ] Tasks in higher layers only depend on tasks in lower layers
- [ ] All stated dependencies exist in the plan

**File Existence**
- [ ] Every file listed for modification actually exists in the codebase (use Glob)
- [ ] New files are in appropriate directories per project conventions

**ADR Consistency**
- [ ] Plan decisions align with ADRs created during `/plan-start`
- [ ] No contradiction with existing ADRs in `docs/adr/`

**CLAUDE.md Compliance**
- [ ] Plan respects all hard rules in CLAUDE.md
- [ ] No first principles violations (no workarounds, no backward-compat shims)

**Test Coverage**
- [ ] Every new function/component has a corresponding test task
- [ ] TDD-marked tasks have failing test written before implementation task

Record all Layer 1 issues with severity (BLOCKER / WARNING / INFO) before proceeding to Layer 2.

---

## Layer 2: Specialist Review

Select agents by applying trigger rules to the plan content. No user input needed — triggers are objective.

**Validation agent pool:**

| Agent | Trigger | Model |
|-------|---------|-------|
| `security-reviewer` | Auth, payments, PII, RBAC, new public APIs | Opus |
| `db-migration-reviewer` | New tables, columns, indexes, or migration files | Opus |
| `performance-reviewer` | New queries, resolvers, routes, or added dependencies | Sonnet |
| `design-system-reviewer` | New UI components or visual styling changes | Sonnet |
| `ux-reviewer` | New pages, forms, modals, or interaction patterns | Sonnet |
| `cross-platform-reviewer` | Changes touching both web and mobile, or shared packages | Sonnet |
| `native-app-reviewer` | Mobile screens, native UI package changes | Sonnet |
| `integration-reviewer` | New external services, libraries, or OTEL config | Opus |

Spawn triggered agents in parallel (Task tool, run_in_background: true). Each agent receives: the plan file, relevant ADRs, and targeted questions based on its domain.

Monitor via TaskOutput polling loop. Report progress to user.

Each agent must return structured findings:
```
FINDING: [BLOCKER|WARNING|INFO]
Location: [plan section or file reference]
Issue: [concrete description]
Risk: [what breaks if this isn't addressed]
Suggestion: [specific fix or alternative]
```

---

## Auto-Fix Phase

Merge Layer 1 structural issues + Layer 2 specialist findings into a single issue list. Every issue must be resolved. No skipping.

**Triage each issue:**

**Bucket A — Auto-resolve:**
- Issue matches an existing ADR decision → cite ADR, mark resolved
- Issue matches a confirmed pattern in PATTERNS.md → cite pattern, mark resolved
- Issue resolvable from first principles in CLAUDE.md → apply rule, mark resolved

**Bucket B — Needs human input:**
- Novel architectural question not covered by existing decisions
- Conflicting ADRs with no clear precedent
- Blocker with no obvious resolution

For Bucket B items: present the issue, explain why it can't be auto-resolved, propose options, wait for decision. Record the decision in the plan's `## Decisions` section and create a new ADR if it's architecturally significant.

**Apply all fixes in one batch** once all issues are triaged. Update the plan file. Commit the updated plan.

---

## Issue Persistence

Record every issue in `docs/plans/metrics/{name}.json` under `validation.issues`:

```json
{
  "id": "S-001",
  "layer": 1,
  "severity": "WARNING",
  "category": "test-coverage",
  "description": "No test task for the new webhook handler",
  "reporting_agent": "structural",
  "triage": "A",
  "resolution_source": "first-principles",
  "resolution": "Added test task in Layer 2 of the plan"
}
```

This data feeds `/plan-metrics` for pattern analysis over time.

---

## Auto-Transition

If all issues are auto-resolved (Bucket A only): auto-start `/plan-execute` without asking.

If any human input was required (Bucket B): ask "All issues resolved. Ready to execute?" before proceeding.

---

## Usage

```
/plan-validate
```

Picks up the most recent uncommitted plan automatically. Or specify:

```
/plan-validate plan-user-authentication
```

## Output

```
Layer 1: Structural validation...
  ✓ Format complete
  ✓ Dependencies valid
  ⚠ WARNING S-001: Missing test task for webhook handler
  ✓ CLAUDE.md compliant

Layer 2: Triggering specialist agents...
  → security-reviewer (auth changes detected) [Opus]
  → db-migration-reviewer (new users table) [Opus]
  → performance-reviewer (new query in /api/users) [Sonnet]
  Monitoring... 1/3 complete... 2/3 complete... done.

  BLOCKER B-001 [security-reviewer]: JWT expiry not validated on refresh endpoint
  WARNING B-002 [db-migration-reviewer]: Migration lacks rollback strategy

Auto-fix phase:
  S-001 → auto-resolved (first principles: test coverage rule)
  B-001 → NEEDS INPUT (no existing ADR for JWT refresh strategy)
  B-002 → auto-resolved (ADR-0003: migration rollback pattern)

[User input requested for B-001]
Decision recorded. ADR-0011 created.

All 3 issues resolved. Plan updated.
→ Auto-starting /plan-execute
```

## When to Use

Always — before any `/plan-execute` call. The cost of validation ($0.20-3.00) is negligible against the cost of discovering issues mid-execution.

## See Also

- [Plan-Validate-Execute Pipeline](../../guide/workflows/plan-pipeline.md)
- [Integration Reviewer Agent](../agents/integration-reviewer.md)
- [Plan Challenger Agent](../agents/plan-challenger.md)
