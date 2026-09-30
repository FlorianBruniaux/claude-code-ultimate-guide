# PR workflow plugin

Automated pull request review and validation system.

## Install

```bash
bash install.sh
```

## Components

- **code-reviewer agent**: Automated code quality and security checks
- **/review-pr command**: Analyze PRs and provide detailed feedback
- **/pr command**: Quick PR preparation workflow
- **pre-pr-check hook**: Validate changes before PR creation

## Quick start

```bash
# Review an existing PR
/review-pr 123

# Prepare a new PR
/pr

# Check what will be submitted
/validate-changes
```

## Features

✓ Code quality analysis
✓ Security scanning
✓ Test coverage verification
✓ Compliance checks
✓ Automated suggestions
✓ Team notifications

## See also

- `guide/workflows/code-review.md` — Full review workflow documentation
- `/security-check` — Security-specific PR review
