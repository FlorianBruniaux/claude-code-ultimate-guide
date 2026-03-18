---
name: audit-agents-skills
description: Audit quality of agents, skills, and commands in a Claude Code project
argument-hint: "[path] [--fix] [--verbose]"
---

# Audit Agents/Skills/Commands Quality

Comprehensive quality audit for Claude Code agents, skills, and commands. Scores each file on weighted criteria with production readiness grading.

## Arguments

- `[path]` - Directory to audit (default: current project `.claude/`)
- `--fix` - Generate fix suggestions for failing criteria
- `--verbose` - Show details for all criteria (not just failures)

## Usage

```bash
/audit-agents-skills              # Audit current project
/audit-agents-skills --fix        # Audit + fix suggestions
/audit-agents-skills ~/other-repo # Audit another project
/audit-agents-skills --verbose    # Full details for all criteria
```

---

## Phase 1: Discovery

**Objective**: Locate and classify all agents, skills, and commands

### Steps

1. **Scan directories**:
   ```
   .claude/agents/
   .claude/skills/
   .claude/commands/
   examples/agents/      (if exists)
   examples/skills/      (if exists)
   examples/commands/    (if exists)
   ```

2. **Classify files**:
   - **Agent**: File in `agents/` directory with YAML frontmatter containing `tools:` field
   - **Skill**: File in `skills/` directory OR has `SKILL.md` name OR frontmatter with `allowed-tools:` field
   - **Command**: File in `commands/` directory with frontmatter containing `name:` and `description:`

3. **Display summary**:
   ```
   Found: X agents, Y skills, Z commands
   ```

---

## Phase 2: Audit Individual Files

Each file type is scored on **weighted criteria**. Maximum scores:
- **Agents**: 32 points
- **Skills**: 32 points
- **Commands**: 20 points

### Agents (32 points max)

#### Identity (weight: 3x) - 12 points

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Clear `name` field | 3 | Frontmatter YAML has `name:` field that's descriptive (not generic like "agent1") |
| `description` with triggers | 3 | Description contains "when", "use", or "trigger" keywords indicating activation context |
| `model` specified | 3 | Frontmatter has `model:` field (sonnet/haiku/opus) |
| `tools` restricted appropriately | 3 | Tools list doesn't include Bash unless justified, or includes explanation for risky tools |

**Rationale**: Identity determines **discoverability** and **activation**. If users can't locate or invoke the agent, downstream quality is irrelevant.

#### Prompt Quality (weight: 2x) - 8 points

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Role defined | 2 | Contains "You are" or "Your role" statement defining agent persona |
| Output format specified | 2 | Has section titled "Output", "Format", or "Deliverables" specifying expected structure |
| Scope/limits defined | 2 | Has section defining scope, triggers, or when NOT to use the agent |
| Anti-hallucination measures | 2 | Contains keywords: "verify", "cite", "source", "evidence", or warnings against hallucination |

**Rationale**: Prompt quality determines **reliability** and **accuracy** of agent responses.

#### Validation (weight: 1x) - 4 points

| Criterion | Points | Detection |
|-----------|--------|-----------|
| 3+ usage examples | 1 | Has "Examples", "Usage", or "Scenarios" section with at least 3 distinct examples |
| Edge cases documented | 1 | Mentions "edge case", "error", "failure", or "limitation" scenarios |
| Integration documented | 1 | References other agents, skills, or tools it works with |
| Error handling described | 1 | Mentions "fallback", "recovery", "error handling", or failure modes |

**Rationale**: Validation ensures **robustness** through comprehensive testing scenarios.

#### Design (weight: 2x) - 8 points

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Single responsibility | 2 | File size <5000 tokens AND description is focused (not "general purpose" or multiple verbs) |
| No duplication | 2 | Description doesn't overlap significantly with other agents (>50% keyword similarity check) |
| Composable (skills references) | 2 | References skills or other agents it can invoke, showing modularity |
| Reasonable token budget | 2 | File size <8000 tokens (avoids context bloat) |

**Rationale**: Design patterns determine **maintainability** and **scalability** of agent architecture.

---

### Skills (32 points max)

#### Structure (weight: 3x) - 12 points

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Valid SKILL.md or frontmatter | 3 | File named `SKILL.md` OR has YAML frontmatter with `name:` field |
| `name` valid | 3 | Name is lowercase, 1-64 chars, matches pattern `[a-z0-9-]+` (no spaces/special chars) |
| `description` non-empty | 3 | Description field exists and is >20 characters |
| `allowed-tools` specified | 3 | Frontmatter has `allowed-tools:` field listing tool permissions |

**Rationale**: Structure compliance ensures **spec compatibility** with Claude Code runtime.

#### Content (weight: 2x) - 8 points

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Methodology/workflow described | 2 | Has section titled "Methodology", "Workflow", "Process", or numbered steps |
| Output format specified | 2 | Has section specifying deliverable format (Markdown, JSON, report structure) |
| Examples provided | 2 | Has "Examples", "Usage", or "Scenarios" section with concrete instances |
| Checklists included | 2 | Contains Markdown checkbox syntax `- [ ]` or `- [x]` for actionable items |

**Rationale**: Content richness determines **usability** and **learning curve**.

#### Technical (weight: 1x) - 4 points

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Scripts have error handling | 1 | If bundled scripts exist, contain `set -e`, `trap`, or `|| exit` patterns |
| No hardcoded paths | 1 | No absolute paths like `/Users/`, `/home/`, `C:\` in code or instructions |
| No secrets | 1 | No keywords: "password", "secret", "token", "api_key", "credentials" in plaintext |
| Dependencies documented | 1 | If external tools required, has "Requirements", "Dependencies", or "Prerequisites" section |

**Rationale**: Technical hygiene prevents **portability issues** and **security risks**.

#### Design (weight: 2x) - 8 points

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Single responsibility | 2 | Description is focused on one domain (not "general" or multi-purpose) |
| Clear triggers | 2 | Has section defining "When to use", "Triggers", or "Activation criteria" |
| No overlap with other skills | 2 | Description doesn't duplicate >50% of keywords from other skills in project |
| Portable | 2 | No Claude Code-specific extensions that break portability (check for custom APIs) |

**Rationale**: Design determines **findability** and **maintainability** across projects.

---

### Commands (20 points max)

#### Structure (weight: 3x) - 12 points

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Valid frontmatter | 3 | Has YAML frontmatter with both `name:` and `description:` fields |
| `argument-hint` if takes args | 3 | If `$ARGUMENTS` variable is used in body, frontmatter has `argument-hint:` field |
| Step-by-step workflow | 3 | Body contains numbered sections (1., 2., 3.) or clear phase structure |
| Usage examples | 3 | Has section titled "Usage", "Examples", or shows invocation patterns |

**Rationale**: Structure determines **usability** and **learnability** for command users.

#### Quality (weight: 2x) - 8 points

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Error handling | 2 | Mentions "error", "failure", "fallback", or conditional paths for failures |
| Output format defined | 2 | Specifies what command outputs (report, file, summary) and its structure |
| Validation gates | 2 | Contains checkpoints, verification steps, or "before proceeding" checks |
| Arguments parsed properly | 2 | If takes args, shows how to parse/validate `$ARGUMENTS` (default values, validation) |

**Rationale**: Quality determines **reliability** and **production readiness**.

---

## Phase 3: Scoring

### Individual File Score

```
Score = (Points Obtained / Max Points) × 100
```

**Example**: Agent scores 26/32 points → 81% score

### Grade Assignment

| Grade | Score Range | Status |
|-------|-------------|--------|
| A | 90-100% | Production-ready ✅ |
| B | 80-89% | Good (production threshold) ⚠️ |
| C | 70-79% | Needs improvement 🔧 |
| D | 60-69% | Significant gaps ⚠️ |
| F | <60% | Critical issues ❌ |

**Production Threshold**: 80% (Grade B or higher)

### Overall Project Score

Weighted average by file type:
```
Overall = (Σ Agent Scores × Agent Count + Σ Skill Scores × Skill Count + Σ Command Scores × Command Count) / Total Files
```

---

## Phase 4: Report Generation

### Report Structure

```markdown
# Audit: Agents/Skills/Commands

**Project**: {path}
**Date**: {date}
**Overall Score**: {score}% ({grade})
**Files Audited**: {total} ({n} agents, {n} skills, {n} commands)
**Production Ready**: {count} files ({percentage}%)

---

## Summary

| Type | Files | Avg Score | Grade | Production Ready |
|------|-------|-----------|-------|------------------|
| Agents | X | Y% | Z | N/X (%) |
| Skills | X | Y% | Z | N/X (%) |
| Commands | X | Y% | Z | N/X (%) |

---

## Individual Scores

| File | Type | Score | Grade | Top Issues |
|------|------|-------|-------|------------|
| agent-name.md | Agent | 85% | B | Missing anti-hallucination measures, no edge cases |
| skill-name/ | Skill | 72% | C | Hardcoded paths, no error handling |
| command.md | Command | 95% | A | None |

---

## Top Issues (Across All Files)

1. **Missing error handling** (8 files affected)
   - Impact: Runtime failures unhandled
   - Fix: Add error handling sections, fallback strategies

2. **Hardcoded paths** (5 files affected)
   - Impact: Portability broken across systems
   - Fix: Use relative paths or environment variables

3. **No usage examples** (4 files affected)
   - Impact: Poor learnability, unclear invocation
   - Fix: Add "Examples" section with 3+ scenarios

---

## Detailed Breakdown

<details>
<summary>agent-name.md (Agent, 85%, Grade B)</summary>

### Scores by Category

| Category | Points | Max | Pass |
|----------|--------|-----|------|
| Identity | 12 | 12 | ✅ |
| Prompt Quality | 6 | 8 | ⚠️ |
| Validation | 2 | 4 | ❌ |
| Design | 6 | 8 | ⚠️ |

### Failed Criteria

- ❌ **Anti-hallucination measures** (2 pts): No keywords found for source verification
- ❌ **Edge cases documented** (1 pt): No mention of failure scenarios
- ❌ **Integration documented** (1 pt): No references to other agents/skills

### Recommendations

1. Add "Source Verification" section requiring citation of claims
2. Document edge cases: API failures, timeout scenarios, invalid input
3. List compatible skills/agents for composition patterns

</details>

---

## Recommendations (Prioritized)

### High Priority (Critical for production)

1. **Add error handling to 8 files**
   - Files: [list]
   - Action: Add error handling sections, define fallback behaviors

2. **Remove hardcoded paths from 5 files**
   - Files: [list]
   - Action: Replace with `$HOME`, relative paths, or env vars

### Medium Priority (Improves quality)

3. **Add usage examples to 4 files**
   - Files: [list]
   - Action: Create "Examples" section with 3+ scenarios

4. **Define output formats in 3 files**
   - Files: [list]
   - Action: Specify deliverable structure (Markdown/JSON/report)

### Low Priority (Polish)

5. **Add integration docs to 2 files**
   - Files: [list]
   - Action: List compatible agents/skills for composition

---

## Next Steps

1. Review failures: Focus on Grade D/F files first
2. Run with `--fix` for automated suggestions
3. Re-audit after improvements to track progress
4. Aim for 80%+ (Grade B) across all files for production readiness
```

---

## Phase 5: Fix Mode (Optional)

**Trigger**: `--fix` flag

For each failing criterion, generate specific fix suggestion:

### Example Fix Suggestions

**File**: `agent-name.md`
**Issue**: Missing anti-hallucination measures (2 pts lost)

**Suggested Fix**:
```markdown
Add this section after the "Methodology" section:

## Source Verification

- Always cite sources for factual claims
- Use phrases like "According to [source]..." or "Based on [documentation]..."
- If uncertain, explicitly state "I don't have verified information on..."
- Never invent statistics, version numbers, or API details
```

**File**: `skill-debugging/scripts/analyze.sh`
**Issue**: No error handling (1 pt lost)

**Suggested Fix**:
```bash
Add to top of script:

set -e  # Exit on error
trap 'echo "Error on line $LINENO"' ERR

# Replace risky commands:
curl https://api.example.com        # ❌ No error check
curl https://api.example.com || {   # ✅ Error handled
    echo "API call failed"
    exit 1
}
```

---

## Verbose Mode (Optional)

**Trigger**: `--verbose` flag

By default, report shows only **failed criteria**. Verbose mode shows **all criteria** with pass/fail status:

```markdown
### All Criteria (Verbose)

| Criterion | Status | Points | Notes |
|-----------|--------|--------|-------|
| Clear name | ✅ Pass | 3/3 | Name is "debugging-specialist" (descriptive) |
| Description with triggers | ✅ Pass | 3/3 | Contains "Use when debugging..." |
| Model specified | ❌ Fail | 0/3 | No `model:` field in frontmatter |
| Tools restricted | ⚠️ Partial | 2/3 | Includes Bash but no justification |
| ... | ... | ... | ... |
```

---

## Industry Context

**Source**: LangChain Agent Report 2026 (verified)

**Key Statistics**:
- 29.5% of organizations deploy agents without systematic evaluation
- 18% cite "agent bugs" as their top challenge
- Only 12% use automated quality checks

**Implication**: This audit addresses a **real industry gap**. Most teams deploy agents/skills without validation, leading to production issues. The 80% threshold (Grade B) aligns with industry best practices for production readiness.

**Comparison**: Manual checklists (like the Guide's Agent Validation Checklist on line 4921) are comprehensive but error-prone. Automated scoring reduces human error and provides quantitative metrics for tracking improvements over time.

---

## Related

- **Agent Validation Checklist** (guide line 4921): Manual 16-criteria checklist
- **Skill Validation** (guide line 5491): Spec compliance documentation
- **Examples**: `examples/agents/`, `examples/skills/`, `examples/commands/`
- **Advanced Audit**: Use `audit-agents-skills` skill (see `examples/skills/`) for comparative analysis vs templates

---

## Implementation Notes

### Detection Patterns

**Frontmatter Parsing**:
```python
import re
yaml_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
if yaml_match:
    import yaml
    frontmatter = yaml.safe_load(yaml_match.group(1))
```

**Keyword Detection** (case-insensitive):
```python
has_trigger = any(word in description.lower() for word in ['when', 'use', 'trigger'])
```

**Token Counting** (approximate):
```python
tokens = len(content.split()) * 1.3  # Rough estimate: 1 token ≈ 0.75 words
```

### Overlap Detection

Compare descriptions using Jaccard similarity:
```python
def jaccard_similarity(desc1, desc2):
    words1 = set(desc1.lower().split())
    words2 = set(desc2.lower().split())
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union) if union else 0

# Flag if similarity > 0.5 (50% keyword overlap)
```

### Grade Color Coding (Terminal Output)

```python
COLORS = {
    'A': '\033[92m',  # Green
    'B': '\033[93m',  # Yellow
    'C': '\033[93m',  # Yellow
    'D': '\033[91m',  # Red
    'F': '\033[91m'   # Red
}
```

---

**Command ready for use**: `/audit-agents-skills`
