---
name: qa
description: "Systematic QA testing of a web application: diff-aware, tiered, with fix-and-verify loop"
argument-hint: "[path] [--thorough]"
effort: high
disable-model-invocation: true
---

# QA: Web application testing

Systematically test a web application for bugs, then fix and verify each issue found.

Three tiers of thoroughness. Diff-aware scoping tests what actually changed.

## Instructions

### Step 1: Scope detection

Determine which pages and features to test.

**Diff-aware mode (default):** Identify affected routes from the current branch changes.

```bash
# Files changed in this branch
git diff --name-only origin/main...HEAD 2>/dev/null || git diff --name-only HEAD~5

# Identify affected routes from changed files
# e.g., changes in src/pages/dashboard/ → test /dashboard
# changes in api/payments/ → test payment flows
```

**Full mode** (`/qa --full`): Test the entire application, starting with critical paths.

**Explicit scope** (`/qa /dashboard /settings`): Test specified pages only.

---

### Step 2: Tier selection

| Tier | Flag | Scope | Use when |
|------|------|-------|----------|
| Quick | `--quick` | Critical + High severity only | Pre-commit fast check |
| Standard | *(default)* | + Medium severity | Pre-PR review |
| Exhaustive | `--exhaustive` | + Low + cosmetic | Release candidate |

---

### Step 3: Clean working tree

Before testing, ensure you can commit fixes atomically.

```bash
git status --short
```

If there are uncommitted changes: stash them first (`git stash`), or commit them. Testing on a dirty tree makes it impossible to isolate fix commits.

---

### Step 4: Testing

For each page in scope, systematically check all categories relevant to the selected tier.

#### How to test

Use whatever browser tooling is available:
- **MCP browser tools** (if configured): automated navigation and screenshots
- **Playwright/Puppeteer** (if in the project): scripted test runs
- **Manual testing**: navigate to the URL, document findings systematically

For each page, cover:

```
1. Load the page: does it render without errors?
2. Check console: any uncaught errors, failed requests, warnings?
3. Test primary user action: the core thing this page is for
4. Test empty state: what shows when there's no data?
5. Test error state: what happens when an action fails?
6. Test on narrow viewport: does it break below 375px?
```

#### Issue taxonomy

**Visual** (layout, spacing, typography, colors, responsiveness)
**Functional** (broken interactions, missing features, wrong behavior)
**UX** (confusing flows, missing feedback, poor error messages)
**Content** (typos, wrong copy, placeholder text in production)
**Performance** (slow page loads, layout shifts, unoptimized images)
**Console** (JavaScript errors, failed network requests, deprecation warnings)
**Accessibility** (missing alt text, keyboard traps, missing labels, contrast)

#### Severity levels

| Severity | Criteria | Examples |
|----------|----------|---------|
| **Critical** | Feature completely broken or data loss risk | 500 error, blank page, form that loses data |
| **High** | Major feature degraded, significant UX harm | Wrong data shown, broken primary CTA, mobile layout broken |
| **Medium** | Minor feature issue, noticeable but workaround exists | Visual glitch, confusing empty state, slow load |
| **Low** | Cosmetic, barely noticeable | Minor spacing, minor copy issue, low-severity console warning |

**Quick tier**: Critical + High only
**Standard tier**: Critical + High + Medium
**Exhaustive tier**: All severities

---

### Step 5: Document findings

Track each issue with a unique ID.

```
ISSUE-001
  Severity:  [Critical / High / Medium / Low]
  Category:  [Visual / Functional / UX / Content / Performance / Console / Accessibility]
  Page:      [URL or route]
  Finding:   [What is wrong, specific not vague]
  Steps:     [How to reproduce]
  Expected:  [What should happen]
  Evidence:  [Screenshot path or console output]
```

---

### Step 6: Fix and verify loop

For each Critical and High issue (and Medium/Low in Standard/Exhaustive tiers):

1. **Fix the issue** in source code
2. **Commit atomically**: one commit per fix

```bash
git add <changed-files>
git commit -m "fix: <brief description of what was fixed>"
```

3. **Re-verify**: navigate to the same page and confirm the issue is resolved
4. **Update the issue status** to FIXED with the commit hash

Do not batch multiple fixes in one commit. Each fix must be individually revertable.

---

## Output format

```
QA REPORT
════════════════════════════════════════
Branch:    [current branch]
Scope:     [pages tested]
Tier:      [Quick / Standard / Exhaustive]
Duration:  [time taken]

HEALTH SCORES
─────────────────────────────────────────
  Visual        [PASS / WARN / FAIL]  [N issues]
  Functional    [PASS / WARN / FAIL]  [N issues]
  UX            [PASS / WARN / FAIL]  [N issues]
  Content       [PASS / WARN / FAIL]  [N issues]
  Performance   [PASS / WARN / FAIL]  [N issues]
  Console       [PASS / WARN / FAIL]  [N issues]
  Accessibility [PASS / WARN / FAIL]  [N issues]

ISSUES FOUND: N (X critical, Y high, Z medium, W low)
ISSUES FIXED: N
ISSUES REMAINING: N

─────────────────────────────────────────
ISSUE-001 [FIXED | OPEN]
  Severity:  High
  Category:  Functional
  Page:      /dashboard
  Finding:   Save button does nothing when form has validation errors, no feedback shown
  Fix:       Added error toast notification (commit abc1234)

ISSUE-002 [OPEN]
  Severity:  Medium
  Category:  Visual
  Page:      /settings
  Finding:   Input fields overflow container below 375px viewport
  ...

─────────────────────────────────────────
SHIP READINESS
  Critical issues:  [0 remaining / N remaining (BLOCKER)]
  High issues:      [0 remaining / N remaining (CONCERN)]

VERDICT: [READY TO SHIP / NOT READY: address critical and high issues first]
════════════════════════════════════════
```

## Usage

```
/qa                          # Standard tier, diff-aware scope
/qa --quick                  # Quick tier (critical + high only)
/qa --exhaustive             # Full coverage including cosmetic issues
/qa --full                   # Standard tier, test entire app (not just diff)
/qa /dashboard /settings     # Test specific pages
/qa https://staging.app.com  # Test a specific URL
```

## Tips

1. **Run after every significant feature**, not just before shipping
2. **Diff-aware first**: test what changed before expanding scope
3. **Fix critical and high before continuing**: don't pile up unfixed issues
4. **Screenshot evidence**: always capture before/after for critical fixes
5. **Check mobile**: most visual bugs appear at 375px width

## Related commands

- `/investigate`: root-cause analysis when QA finds a complex bug
- `/ship`: pre-deploy checklist (run after QA passes)
- `/canary`: post-deploy monitoring (run after shipping)

$ARGUMENTS
