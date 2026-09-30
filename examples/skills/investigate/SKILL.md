---
name: investigate
description: "Systematic root-cause debugging: find the cause before writing any fix"
argument-hint: <issue_description>
effort: medium
disable-model-invocation: true
---

# Investigate: Root-Cause debugging

Systematic debugging with mandatory root cause investigation before any code changes.

**Iron Law: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Fixing symptoms creates whack-a-mole debugging. Every fix that doesn't address root cause makes the next bug harder to find.

## Instructions

### Phase 1: Collect symptoms

Gather all available context before forming any hypothesis.

1. Read the error messages, stack traces, and reproduction steps in full
2. Ask ONE targeted question if the user hasn't provided enough context:
   - "What exact error message do you see?"
   - "Can you reproduce this consistently?"
   - "When did this start happening?"
3. Identify the affected component and its boundaries

**Output**: A precise symptom statement: what fails, when, with what error.

---

### Phase 2: Read the code

Trace the code path from symptom back to potential causes. Do not guess.

```bash
# Find all references to the failing component
grep -rn "ComponentName\|function_name\|error_string" src/ --include="*.{ts,js,py,rb,go}" | head -30

# Check recent changes to affected files
git log --oneline -15 -- <affected-file>

# Read the actual diff for each recent commit
git show <commit-hash> -- <affected-file>
```

Use Grep to find all references, Read to understand the logic. Never skip reading the code.

---

### Phase 3: Check recent changes

```bash
# What changed recently across the whole repo
git log --oneline -20

# Changes to files related to the symptom
git log --oneline -20 -- <affected-files>

# Full diff of the last N commits
git diff HEAD~3..HEAD -- <affected-directory>
```

**Key question**: Was this working before? If yes, the root cause is in the recent diff.

- Regression = root cause is in the changes, not the original code
- Always-broken = architectural issue or incorrect assumption

---

### Phase 4: Reproduce

Before fixing anything, confirm you can trigger the bug deterministically.

```bash
# Run the test suite targeting the affected area
npm test -- --testPathPattern="affected-module" 2>/dev/null || \
pnpm test -- --testPathPattern="affected-module" 2>/dev/null || \
pytest tests/test_affected.py -v 2>/dev/null

# Check logs if available
tail -50 logs/error.log 2>/dev/null || \
journalctl -u app-service --lines=50 2>/dev/null
```

If you cannot reproduce: gather more evidence. Do not fix what you cannot verify is broken.

---

### Phase 5: Pattern analysis

Match the symptom against known bug patterns:

| Pattern | Signature | Where to look |
|---------|-----------|---------------|
| Race condition | Intermittent, timing-dependent failures | Concurrent access to shared state, async/await ordering |
| Null propagation | TypeError, undefined is not a function | Missing guards on optional values, unchecked API responses |
| State corruption | Inconsistent data, partial updates | Transactions, callbacks, mutation of shared objects |
| Integration failure | Timeout, unexpected response shape | External API calls, service boundaries, schema changes |
| Configuration drift | Works locally, fails in staging/prod | Env vars, feature flags, database state, missing secrets |
| Stale cache | Shows old data, fixes on restart/clear | Redis, CDN, browser cache, memoization |
| Import/module error | "Cannot find module", "is not a function" | Package versions, circular imports, build artifacts |

Also check:
- `TODOS.md` or issue tracker for known issues in the same area
- `git log` for prior fixes in the same files; recurring bugs in the same location are an architectural smell

**External search:** If the pattern doesn't match, search for:
`{framework} {sanitized-error-type}` (strip hostnames, file paths, internal data). Search the error category, not the raw message.

**Form a hypothesis**: "Root cause hypothesis: [specific, testable claim about what is wrong and why]"

---

### Phase 6: Hypothesis testing

Before writing any fix, verify your hypothesis.

1. **Confirm the hypothesis**: Add a temporary log statement, assertion, or debug output at the suspected root cause. Run the reproduction. Does the evidence match?

```javascript
// Example: temporary diagnostic
console.log('[DEBUG investigate]', { value, expected, type: typeof value });
```

```python
# Example: temporary diagnostic
import sys; print(f'[DEBUG investigate] value={value!r} type={type(value)}', file=sys.stderr)
```

2. **If hypothesis is wrong**: Gather more evidence. Return to Phase 2. Do not guess.

3. **3-strike rule**: If 3 hypotheses fail, STOP. This may be an architectural issue.

   Present this to the user:
   ```
   3 hypotheses tested, none confirmed. This likely requires deeper investigation.

   Options:
   A) I have a new hypothesis: [describe], continue investigating
   B) Add instrumentation and wait: capture the bug in the act next time
   C) Escalate: this needs someone with deeper system knowledge
   ```

**Red flags, slow down immediately:**
- "Quick fix for now": there is no "for now"
- Proposing a fix before tracing data flow: that's guessing
- Each fix reveals a new problem elsewhere: wrong layer, not wrong code

---

### Phase 7: Implementation

Once root cause is confirmed:

1. **Fix the root cause, not the symptom.** The smallest change that eliminates the actual problem.

2. **Minimal diff**: Fewest files touched, fewest lines changed. Resist refactoring adjacent code.

3. **Write a regression test** that:
   - **Fails** without the fix (proves the test is meaningful)
   - **Passes** with the fix (proves the fix works)

4. **Run the full test suite** and paste the output. No regressions allowed.

5. **Blast radius check**: If the fix touches more than 5 files, stop and confirm:

   ```
   This fix touches N files. That's a large blast radius for a bug fix.

   A) Proceed: the root cause genuinely spans these files
   B) Split: fix the critical path now, defer the broader cleanup
   C) Rethink: there may be a more targeted approach
   ```

---

## Output format

```
DEBUG REPORT
════════════════════════════════════════════════════
Symptom:          [what the user observed]
Root cause:       [what was actually wrong, specific not vague]
Fix:              [what was changed, with file:line references]
Evidence:         [test output or reproduction showing fix works]
Regression test:  [file:line of the new test]
Related:          [known issues, prior bugs in same area, architectural notes]
Status:           DONE | DONE_WITH_CONCERNS | BLOCKED
════════════════════════════════════════════════════
```

**Status definitions:**
- **DONE**: root cause found, fix applied, regression test written, all tests pass
- **DONE_WITH_CONCERNS**: fixed but cannot fully verify (intermittent, requires staging)
- **BLOCKED**: root cause unclear after full investigation

**Escalation format (when BLOCKED):**
```
STATUS: BLOCKED
REASON: [1-2 sentences explaining what was tried and why it failed]
ATTEMPTED: [list of hypotheses tested]
RECOMMENDATION: [what the user should do next: add logging, escalate, or request an architectural review]
```

## Important rules

- **Never apply a fix you cannot verify.** If you can't reproduce and confirm, don't ship it.
- **Never say "this should fix it."** Verify and prove it. Run the tests.
- **Never fix >3 unrelated things in one investigation.** If you find other bugs, note them but stay focused.
- **Remove all debug log statements** before committing the fix.
- **3+ failed hypotheses → question the architecture**, not your hypothesis skills.

## Usage

```
/investigate TypeError: Cannot read properties of undefined (reading 'map')
/investigate the payment flow is silently dropping some transactions
/investigate
```

## Related commands

- `/review-pr`: review the fix before merging
- `/qa`: run browser QA on the affected feature after fixing
- `/ship`: pre-deploy checklist after investigation is complete

$ARGUMENTS
