---
name: validate-changes
description: Evaluate staged changes using LLM-as-a-Judge before committing
---

# Validate Changes Before Commit

Evaluate staged git changes using the output-evaluator agent to catch issues before committing.

## Process

### Step 1: Check for Staged Changes

Run `git diff --cached --stat` to see what's staged. If nothing is staged, inform the user and exit.

### Step 2: Get the Full Diff

Run `git diff --cached` to get the complete diff of all staged changes.

### Step 3: Invoke the Evaluator

Use the Task tool to launch the `output-evaluator` agent with the diff:

```
Evaluate these staged changes for correctness, completeness, and safety.
Return a JSON verdict with scores and issues.

Changes:
[paste the git diff here]
```

### Step 4: Parse and Act on Verdict

Based on the evaluation result:

**If APPROVE:**
- Tell the user the changes passed evaluation
- Show the summary and scores
- Ask if they want to proceed with commit

**If NEEDS_REVIEW:**
- Show all issues found (grouped by severity)
- Show the suggestion from the evaluator
- Ask the user how to proceed:
  - Fix issues and re-evaluate
  - Commit anyway (acknowledge risks)
  - Abort

**If REJECT:**
- Clearly state the changes were rejected
- Show critical issues that caused rejection
- Do NOT offer to commit anyway
- Suggest specific fixes

### Step 5: Commit (if approved)

If user confirms, create the commit using the standard commit flow.

## Usage Examples

```
/validate-changes
```

Output:
```
Evaluating 3 staged files...

VERDICT: NEEDS_REVIEW

Scores:
  Correctness:  8/10
  Completeness: 6/10
  Safety:       9/10

Issues Found:
  [MEDIUM] src/api/handler.ts:45
    Missing error handling for network failures

  [LOW] src/utils/format.ts:12
    Consider adding input validation

Suggestion: Add try-catch around the fetch call in handler.ts

How would you like to proceed?
  1. Fix issues and re-evaluate
  2. Commit anyway (1 medium issue)
  3. Abort
```

## Cost Awareness

This command invokes an LLM evaluation, which uses API tokens:
- **Typical cost**: $0.01-0.05 per evaluation (using Haiku)
- **Larger diffs**: May cost more due to increased token usage

## When to Use

- After significant code changes before committing
- When working on unfamiliar parts of the codebase
- For changes that affect security-sensitive code
- Before pushing to shared branches

## When to Skip

- Trivial changes (typos, formatting)
- Documentation-only changes
- When you've already manually reviewed thoroughly
- When iterating quickly on a feature branch

## Integration with Git Hooks

For automatic evaluation on every commit, see `pre-commit-evaluator.sh` hook.
This command is the manual alternative when you want control over when evaluation runs.
