---
name: audit-agents-skills
description: Comprehensive quality audit for Claude Code agents, skills, and commands with comparative analysis
allowed-tools: Read, Grep, Glob, Bash, Write
context: inherit
agent: specialist
version: 1.0.0
tags: [quality, audit, agents, skills, validation, production-readiness]
---

# Audit Agents/Skills/Commands (Advanced Skill)

Comprehensive quality audit system for Claude Code agents, skills, and commands. Provides quantitative scoring, comparative analysis, and production readiness grading based on industry best practices.

## Purpose

**Problem**: Manual validation of agents/skills is error-prone and inconsistent. According to the LangChain Agent Report 2026, 29.5% of organizations deploy agents without systematic evaluation, leading to "agent bugs" as the top challenge (18% of teams).

**Solution**: Automated quality scoring across 16 weighted criteria with production readiness thresholds (80% = Grade B minimum for production deployment).

**Key Features**:
- Quantitative scoring (32 points for agents/skills, 20 for commands)
- Weighted criteria (Identity 3x, Prompt 2x, Validation 1x, Design 2x)
- Production readiness grading (A-F scale with 80% threshold)
- Comparative analysis vs reference templates
- JSON/Markdown dual output for programmatic integration
- Fix suggestions for failing criteria

---

## Modes

| Mode | Usage | Output |
|------|-------|--------|
| **Quick Audit** | Top-5 critical criteria only | Fast pass/fail (3-5 min for 20 files) |
| **Full Audit** | All 16 criteria per file | Detailed scores + recommendations (10-15 min) |
| **Comparative** | Full + benchmark vs templates | Analysis + gap identification (15-20 min) |

**Default**: Full Audit (recommended for first run)

---

## Methodology

### Why These Criteria?

The 16-criteria framework is derived from:
1. **Claude Code Best Practices** (Ultimate Guide line 4921: Agent Validation Checklist)
2. **Industry Data** (LangChain Agent Report 2026: evaluation gaps)
3. **Production Failures** (Community feedback on hardcoded paths, missing error handling)
4. **Composition Patterns** (Skills should reference other skills, agents should be modular)

### Scoring Philosophy

**Weight Rationale**:
- **Identity (3x)**: If users can't find/invoke the agent, quality is irrelevant (discoverability > quality)
- **Prompt (2x)**: Determines reliability and accuracy of outputs
- **Validation (1x)**: Improves robustness but is secondary to core functionality
- **Design (2x)**: Impacts long-term maintainability and scalability

**Grade Standards**:
- **A (90-100%)**: Production-ready, minimal risk
- **B (80-89%)**: Good, meets production threshold
- **C (70-79%)**: Needs improvement before production
- **D (60-69%)**: Significant gaps, not production-ready
- **F (<60%)**: Critical issues, requires major refactoring

**Industry Alignment**: The 80% threshold aligns with software engineering best practices for production deployment (e.g., code coverage >80%, security scan pass rates).

---

## Workflow

### Phase 1: Discovery

1. **Scan directories**:
   ```
   .claude/agents/
   .claude/skills/
   .claude/commands/
   examples/agents/      (if exists)
   examples/skills/      (if exists)
   examples/commands/    (if exists)
   ```

2. **Classify files** by type (agent/skill/command)

3. **Load reference templates** (for Comparative mode):
   ```
   guide/examples/agents/     (benchmark files)
   guide/examples/skills/     (benchmark files)
   guide/examples/commands/   (benchmark files)
   ```

### Phase 2: Scoring Engine

Load scoring criteria from `scoring/criteria.yaml`:

```yaml
agents:
  max_points: 32
  categories:
    identity:
      weight: 3
      criteria:
        - id: A1.1
          name: "Clear name"
          points: 3
          detection: "frontmatter.name exists and is descriptive"
        # ... (16 total criteria)
```

For each file:
1. Parse frontmatter (YAML)
2. Extract content sections
3. Run detection patterns (regex, keyword search)
4. Calculate score: `(points / max_points) × 100`
5. Assign grade (A-F)

### Phase 3: Comparative Analysis (Comparative Mode Only)

For each project file:
1. Find closest matching template (by description similarity)
2. Compare scores per criterion
3. Identify gaps: `template_score - project_score`
4. Flag significant gaps (>10 points difference)

**Example**:
```
Project file: .claude/agents/debugging-specialist.md (Score: 78%, Grade C)
Closest template: examples/agents/debugging-specialist.md (Score: 94%, Grade A)

Gaps:
- Anti-hallucination measures: -2 points (template has, project missing)
- Edge cases documented: -1 point (template has 5 examples, project has 1)
- Integration documented: -1 point (template references 3 skills, project none)

Total gap: 16 points (explains C vs A difference)
```

### Phase 4: Report Generation

**Markdown Report** (`audit-report.md`):
- Summary table (overall + by type)
- Individual scores with top issues
- Detailed breakdown per file (collapsible)
- Prioritized recommendations

**JSON Output** (`audit-report.json`):
```json
{
  "metadata": {
    "project_path": "/path/to/project",
    "audit_date": "2026-02-07",
    "mode": "full",
    "version": "1.0.0"
  },
  "summary": {
    "overall_score": 82.5,
    "overall_grade": "B",
    "total_files": 15,
    "production_ready_count": 10,
    "production_ready_percentage": 66.7
  },
  "by_type": {
    "agents": { "count": 5, "avg_score": 85.2, "grade": "B" },
    "skills": { "count": 8, "avg_score": 78.9, "grade": "C" },
    "commands": { "count": 2, "avg_score": 92.0, "grade": "A" }
  },
  "files": [
    {
      "path": ".claude/agents/debugging-specialist.md",
      "type": "agent",
      "score": 78.1,
      "grade": "C",
      "points_obtained": 25,
      "points_max": 32,
      "failed_criteria": [
        {
          "id": "A2.4",
          "name": "Anti-hallucination measures",
          "points_lost": 2,
          "recommendation": "Add section on source verification"
        }
      ]
    }
  ],
  "top_issues": [
    {
      "issue": "Missing error handling",
      "affected_files": 8,
      "impact": "Runtime failures unhandled",
      "priority": "high"
    }
  ]
}
```

### Phase 5: Fix Suggestions (Optional)

For each failing criterion, generate **actionable fix**:

```markdown
### File: .claude/agents/debugging-specialist.md
**Issue**: Missing anti-hallucination measures (2 points lost)

**Fix**:
Add this section after "Methodology":

## Source Verification

- Always cite sources for technical claims
- Use phrases: "According to [documentation]...", "Based on [tool output]..."
- If uncertain, state: "I don't have verified information on..."
- Never invent: statistics, version numbers, API signatures, stack traces

**Detection**: Grep for keywords: "verify", "cite", "source", "evidence"
```

---

## Scoring Criteria

See `scoring/criteria.yaml` for complete definitions. Summary:

### Agents (32 points max)

| Category | Weight | Criteria Count | Max Points |
|----------|--------|----------------|------------|
| Identity | 3x | 4 | 12 |
| Prompt Quality | 2x | 4 | 8 |
| Validation | 1x | 4 | 4 |
| Design | 2x | 4 | 8 |

**Key Criteria**:
- Clear name (3 pts): Not generic like "agent1"
- Description with triggers (3 pts): Contains "when"/"use"
- Role defined (2 pts): "You are..." statement
- 3+ examples (1 pt): Usage scenarios documented
- Single responsibility (2 pts): Focused, not "general purpose"

### Skills (32 points max)

| Category | Weight | Criteria Count | Max Points |
|----------|--------|----------------|------------|
| Structure | 3x | 4 | 12 |
| Content | 2x | 4 | 8 |
| Technical | 1x | 4 | 4 |
| Design | 2x | 4 | 8 |

**Key Criteria**:
- Valid SKILL.md (3 pts): Proper naming
- Name valid (3 pts): Lowercase, 1-64 chars, no spaces
- Methodology described (2 pts): Workflow section exists
- No hardcoded paths (1 pt): No `/Users/`, `/home/`
- Clear triggers (2 pts): "When to use" section

### Commands (20 points max)

| Category | Weight | Criteria Count | Max Points |
|----------|--------|----------------|------------|
| Structure | 3x | 4 | 12 |
| Quality | 2x | 4 | 8 |

**Key Criteria**:
- Valid frontmatter (3 pts): name + description
- Argument hint (3 pts): If uses `$ARGUMENTS`
- Step-by-step workflow (3 pts): Numbered sections
- Error handling (2 pts): Mentions failure modes

---

## Detection Patterns

### Frontmatter Parsing

```python
import yaml
import re

def parse_frontmatter(content):
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return None
```

### Keyword Detection

```python
def has_keywords(text, keywords):
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)

# Example
has_trigger = has_keywords(description, ['when', 'use', 'trigger'])
has_error_handling = has_keywords(content, ['error', 'failure', 'fallback'])
```

### Overlap Detection (Duplication Check)

```python
def jaccard_similarity(text1, text2):
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union) if union else 0

# Flag if similarity > 0.5 (50% keyword overlap)
if jaccard_similarity(desc1, desc2) > 0.5:
    issues.append("High overlap with another file")
```

### Token Counting (Approximate)

```python
def estimate_tokens(text):
    # Rough estimate: 1 token ≈ 0.75 words
    word_count = len(text.split())
    return int(word_count * 1.3)

# Check budget
tokens = estimate_tokens(file_content)
if tokens > 5000:
    issues.append("File too large (>5K tokens)")
```

---

## Industry Context

**Source**: LangChain Agent Report 2026 (public report, page 14-22)

**Key Findings**:
- **29.5%** of organizations deploy agents without systematic evaluation
- **18%** cite "agent bugs" as their primary challenge
- **Only 12%** use automated quality checks (88% manual or none)
- **43%** report difficulty maintaining agent quality over time
- **Top issues**: Hallucinations (31%), poor error handling (28%), unclear triggers (22%)

**Implications**:
1. **Automation gap**: Most teams rely on manual checklists (error-prone at scale)
2. **Quality debt**: Agents deployed without validation accumulate technical debt
3. **Maintenance burden**: 43% struggle with quality over time (no tracking system)

**This skill addresses**:
- Automation: Replaces manual checklists with quantitative scoring
- Tracking: JSON output enables trend analysis over time
- Standards: 80% threshold provides clear production gate

---

## Output Examples

### Quick Audit (Top-5 Criteria)

```markdown
# Quick Audit: Agents/Skills/Commands

**Files**: 15 (5 agents, 8 skills, 2 commands)
**Critical Issues**: 3 files fail top-5 criteria

## Top-5 Criteria (Pass/Fail)

| File | Valid Name | Has Triggers | Error Handling | No Hardcoded Paths | Examples |
|------|------------|--------------|----------------|--------------------|----------|
| agent1.md | ✅ | ✅ | ❌ | ✅ | ❌ |
| skill2/ | ✅ | ❌ | ✅ | ❌ | ✅ |

## Action Required

1. **Add error handling**: 5 files
2. **Remove hardcoded paths**: 3 files
3. **Add usage examples**: 4 files
```

### Full Audit

See Phase 4: Report Generation above for full structure.

### Comparative (Full + Benchmarks)

```markdown
# Comparative Audit

## Project vs Templates

| File | Project Score | Template Score | Gap | Top Missing |
|------|---------------|----------------|-----|-------------|
| debugging-specialist.md | 78% (C) | 94% (A) | -16 pts | Anti-hallucination, edge cases |
| testing-expert/ | 85% (B) | 91% (A) | -6 pts | Integration docs |

## Recommendations

Focus on these gaps to reach template quality:
1. **Anti-hallucination measures** (8 files): Add source verification sections
2. **Edge case documentation** (5 files): Add failure scenario examples
3. **Integration documentation** (4 files): List compatible agents/skills
```

---

## Usage

### Basic (Full Audit)

```bash
# In Claude Code
Use skill: audit-agents-skills

# Specify path
Use skill: audit-agents-skills for ~/projects/my-app
```

### With Options

```bash
# Quick audit (fast)
Use skill: audit-agents-skills with mode=quick

# Comparative (benchmark analysis)
Use skill: audit-agents-skills with mode=comparative

# Generate fixes
Use skill: audit-agents-skills with fixes=true

# Custom output path
Use skill: audit-agents-skills with output=~/Desktop/audit.json
```

### JSON Output Only

```bash
# For programmatic integration
Use skill: audit-agents-skills with format=json output=audit.json
```

---

## Integration with CI/CD

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run quick audit on changed agent/skill/command files
changed_files=$(git diff --cached --name-only | grep -E "^\.claude/(agents|skills|commands)/")

if [ -n "$changed_files" ]; then
    echo "Running quick audit on changed files..."
    # Run audit (requires Claude Code CLI wrapper)
    # Exit with 1 if any file scores <80%
fi
```

### GitHub Actions

```yaml
name: Audit Agents/Skills
on: [pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run quality audit
        run: |
          # Run audit skill
          # Parse JSON output
          # Fail if overall_score < 80
```

---

## Comparison: Command vs Skill

| Aspect | Command (`/audit-agents-skills`) | Skill (this file) |
|--------|----------------------------------|-------------------|
| **Scope** | Current project only | Multi-project, comparative |
| **Output** | Markdown report | Markdown + JSON |
| **Speed** | Fast (5-10 min) | Slower (10-20 min with comparative) |
| **Depth** | Standard 16 criteria | Same + benchmark analysis |
| **Fix suggestions** | Via `--fix` flag | Built-in with recommendations |
| **Programmatic** | Terminal output | JSON for CI/CD integration |
| **Best for** | Quick checks, dev workflow | Deep audits, quality tracking |

**Recommendation**: Use command for daily checks, skill for release gates and quality tracking.

---

## Maintenance

### Updating Criteria

Edit `scoring/criteria.yaml`:
```yaml
agents:
  categories:
    identity:
      criteria:
        - id: A1.5  # New criterion
          name: "API versioning specified"
          points: 3
          detection: "mentions API version or compatibility"
```

Version bump: Increment `version` in frontmatter when criteria change.

### Adding File Types

To support new file types (e.g., "workflows"):
1. Add to `scoring/criteria.yaml`:
   ```yaml
   workflows:
     max_points: 24
     categories: [...]
   ```
2. Update detection logic (file path patterns)
3. Update report templates

---

## Related

- **Command version**: `.claude/commands/audit-agents-skills.md`
- **Agent Validation Checklist**: guide line 4921 (manual 16 criteria)
- **Skill Validation**: guide line 5491 (spec documentation)
- **Reference templates**: `examples/agents/`, `examples/skills/`, `examples/commands/`

---

## Changelog

**v1.0.0** (2026-02-07):
- Initial release
- 16-criteria framework (agents/skills/commands)
- 3 audit modes (quick/full/comparative)
- JSON + Markdown output
- Fix suggestions
- Industry context (LangChain 2026 report)

---

**Skill ready for use**: `audit-agents-skills`
