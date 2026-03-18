---
description: "Code quality review criteria for plan and code reviews"
---

# Code Quality Review Criteria

When reviewing code quality, evaluate these dimensions:

## Organization
- Is the module structure logical and consistent?
- Are files in the right directories?
- Is the naming convention consistent across the codebase?

## DRY Violations
- Flag any duplicated logic (be aggressive)
- Identify copy-paste patterns that should be abstracted
- Check for repeated configuration or magic values

## Error Handling
- Are errors handled at the right level (not swallowed, not over-caught)?
- Are edge cases explicitly handled or documented as out-of-scope?
- Do error messages provide enough context for debugging?
- Are there silent failures (empty catch blocks, ignored return values)?

## Technical Debt
- Which areas have the highest maintenance burden?
- Are there TODO/FIXME comments that should be addressed now?
- Is there dead code that should be removed?

## Engineering Balance
- Are there areas that are over-engineered (premature abstraction, unnecessary complexity)?
- Are there areas that are under-engineered (fragile, hacky, missing validation)?
- Does the complexity match the actual requirements?
