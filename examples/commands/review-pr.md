---
name: review-pr
description: "Perform a comprehensive code review of a pull request"
---

# Review Pull Request

Perform a comprehensive code review of a pull request.

## Instructions

1. Get PR information: `gh pr view $ARGUMENTS --json title,body,files,additions,deletions`
2. Review each changed file
3. Provide structured feedback

## Review Checklist

### Code Quality
- [ ] Code is readable and well-organized
- [ ] Functions are appropriately sized
- [ ] No code duplication
- [ ] Meaningful variable/function names

### Functionality
- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Error handling is comprehensive
- [ ] No obvious bugs

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] No injection vulnerabilities
- [ ] Authorization checks in place

### Testing
- [ ] Tests added for new code
- [ ] Existing tests still pass
- [ ] Edge cases tested

### Documentation
- [ ] Code is self-documenting or commented
- [ ] README updated if needed
- [ ] API changes documented

## Output Format

```markdown
## PR Review: #[number] - [title]

### Summary
[1-2 sentence overview]

### Approval Status
[ ] Approved
[ ] Approved with suggestions
[ ] Changes requested

### Findings

#### Critical (Must Fix)
- [ ] [Issue description] - `file:line`

#### Suggestions (Should Consider)
- [ ] [Improvement] - `file:line`

#### Nitpicks (Optional)
- [ ] [Minor suggestion] - `file:line`

### Positive Highlights
- [What's done well]

### Questions
- [Clarifications needed]
```

## Usage

```
/review-pr 123
/review-pr https://github.com/owner/repo/pull/123
```

---

## Advanced: Multi-Agent Review

For production-grade reviews requiring specialized perspectives and anti-hallucination safeguards.

### Pre-flight Check

Before reviewing, check if this is a follow-up pass to avoid repeating suggestions:

```bash
# Detect if Claude already reviewed this PR
git log --oneline -10 | grep "Co-Authored-By: Claude"
```

If detected, note: "This appears to be a follow-up pass. I'll focus on new issues and avoid repeating previous suggestions."

### Multi-Agent Specialization

Launch 3 parallel specialized agents (see [Split Role Sub-Agents](../../guide/ultimate-guide.md#split-role-sub-agents)):

**Agent 1: Consistency Auditor**
```
Focus: DRY violations, duplicate logic, pattern inconsistencies
Check for:
- Duplicated code blocks (>5 lines similar)
- Inconsistent naming conventions
- Pattern violations (if project uses X pattern, enforce it)
```

**Agent 2: SOLID Principles Analyst**
```
Focus: Single Responsibility Principle violations, complexity
Check for:
- Functions >50 lines (likely doing too much)
- Nested conditionals >3 levels deep
- Cyclomatic complexity >10
- Mixed concerns in single component
```

**Agent 3: Defensive Code Auditor**
```
Focus: Silent failures, masked bugs, hidden fallbacks
Check for:
- Empty catch blocks: try { } catch (e) { } // swallows error
- Silent fallbacks: return data || DEFAULT // hides missing data
- Unchecked null/undefined: user.name without validation
- Ignored promise rejections: async fn without .catch()
```

### Anti-Hallucination Rules

**Verify before asserting**:
- Use `Grep` or `Glob` to verify patterns before recommending them
- If suggesting "use existing UserService pattern", confirm UserService exists first
- Never claim "project uses X" without checking actual codebase

**Occurrence rule**:
- Pattern with >10 occurrences = established (Suggestion level)
- Pattern with <3 occurrences = not established (Can Skip or ask maintainer)
- Read full file context, not just diff lines

**Uncertainty markers**:
- Use "❓ To verify:" when unsure about project conventions
- Use "💡 Consider:" for optional improvements
- Use "🔴 Must fix:" only for critical bugs/security

### Reconciliation

After agents report findings:

1. **Deduplicate**: Remove overlapping suggestions across agents
2. **Prioritize existing patterns**: If codebase uses pattern X, recommend X (not ideal pattern Y)
3. **Mark skipped suggestions**: "Skipping [suggestion] because project uses [alternative pattern]"
4. **Track reasoning**: Document why suggestion was kept or skipped

### Severity Classification

```
🔴 Must Fix (Blockers)
- Security vulnerabilities
- Data loss risks
- Breaking changes without migration
- Silent failures masking bugs

🟡 Should Fix (Improvements)
- SOLID violations causing maintenance issues
- DRY violations (>3 duplicates)
- Performance bottlenecks (N+1 queries)
- Missing error handling for critical paths

🟢 Can Skip (Nice-to-haves)
- Style inconsistencies (if no linter)
- Minor naming improvements
- Overly nested code (if <3 levels)
- Documentation gaps (if code self-documenting)
```

### Auto-Fix Loop (Optional)

For automated convergence:

```
Review → Identify issues → Fix → Re-review → Repeat until minimal changes

Safeguards:
- Max 3 iterations to prevent infinite loops
- Run tsc/lint check before each iteration
- Skip auto-fix for protected files (package.json, migrations, etc.)
```

**Example prompt**:
```
Review this PR with auto-fix enabled:
1. Review using 3 agents above
2. Fix all 🔴 Must Fix issues
3. Re-review to verify fixes
4. Repeat for 🟡 Should Fix (max 2 more iterations)
5. Stop when only 🟢 Can Skip remain
```

### Conditional Context Loading

Load additional context based on diff content (stack-agnostic):

| If diff contains... | Then check... |
|---------------------|---------------|
| Database queries | Indexes, N+1 patterns, query optimization |
| API endpoints | Auth middleware, input validation, rate limiting |
| Authentication logic | Password hashing, session management, CSRF tokens |
| File uploads | Size limits, MIME validation, storage security |
| Date/time operations | Timezone handling, DST edge cases |
| External API calls | Timeout configs, retry logic, error handling |
| Environment variables | Presence in .env.example, validation at startup |

### Integration with Existing Tools

**SE-CoVe Plugin**: Use for general fact-checking of review claims (complementary to anti-hallucination rules above)

**Worktrunk**: For codebase-wide pattern analysis before suggesting changes

**AST-grep**: For structural pattern matching (e.g., find all similar try/catch blocks)

---

## Sources

- Base template: Claude Code Ultimate Guide
- Multi-agent review: [Pat Cullen](https://gist.github.com/patyearone/c9a091b97e756f5ed361f7514d88ef0b) (Jan 2026)
- Anti-hallucination patterns: [Méthode Aristote](https://github.com/FlorianBruniaux) code review system

$ARGUMENTS
