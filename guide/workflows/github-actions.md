---
title: "GitHub Actions Workflows with Claude Code"
description: "Production-ready patterns for automating PR reviews, issue triage, and quality gates with claude-code-action"
tags: [workflow, ci-cd, github-actions, automation]
---

# GitHub Actions Workflows with Claude Code

> **Confidence**: Tier 1 — Official Anthropic action (`anthropics/claude-code-action`, 6.2k stars, v1.0).

Automate code reviews, issue triage, and quality gates by connecting Claude directly to your GitHub workflow. Two trigger models: `@claude` mentions (human-initiated) and scheduled/event automations (fully autonomous).

---

## Table of Contents

1. [TL;DR](#tldr)
2. [Two Models](#two-models)
3. [Setup](#setup)
4. [Pattern 1: PR Code Review on @claude Mention](#pattern-1-pr-code-review-on-claude-mention)
5. [Pattern 2: Automatic PR Review on Push](#pattern-2-automatic-pr-review-on-push)
6. [Pattern 3: Issue Triage and Labeling](#pattern-3-issue-triage-and-labeling)
7. [Pattern 4: Security-Focused Review](#pattern-4-security-focused-review)
8. [Pattern 5: Scheduled Repo Maintenance](#pattern-5-scheduled-repo-maintenance)
9. [Authentication Alternatives](#authentication-alternatives)
10. [Cost Control](#cost-control)
11. [Security Checklist](#security-checklist)
12. [See Also](#see-also)

---

## TL;DR

```yaml
# Minimal working example — paste into .github/workflows/claude.yml
name: Claude Code Review
on:
  issue_comment:
    types: [created]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

Comment `@claude review this PR` on any PR → Claude reads the diff and posts a review.

---

## Two Models

| Model | Trigger | Use case |
|-------|---------|----------|
| **Interactive** | `@claude` mention in PR/issue comment | On-demand reviews, questions, fixes |
| **Automated** | Push, PR open, schedule, label | Continuous quality gates, triage |

Both use the same action — the difference is the `on:` block and whether you include an `if:` condition.

---

## Setup

### Quickstart (30 seconds)

In your Claude Code terminal, inside any project connected to a GitHub repo:

```
/install-github-app
```

This guides you through creating the GitHub App, adding `ANTHROPIC_API_KEY` to your repo secrets, and generating the base `claude.yml` workflow.

### Manual Setup

1. Add `ANTHROPIC_API_KEY` to your GitHub repository secrets
2. Create `.github/workflows/claude.yml` (see patterns below)
3. Grant the workflow permissions: `contents: write`, `pull-requests: write`, `issues: write`

---

## Pattern 1: PR Code Review on @claude Mention

Human-initiated. A developer comments `@claude review this PR` and Claude responds inline.

```yaml
# .github/workflows/claude-review.yml
name: Claude Interactive Review
on:
  issue_comment:
    types: [created, edited]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    if: |
      contains(github.event.comment.body, '@claude') ||
      contains(github.event.review_comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          claude_env: |
            GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}
```

**Usage examples:**
- `@claude review this PR` — full diff analysis with suggestions
- `@claude is this change backwards compatible?` — targeted question
- `@claude fix the failing test in src/auth.test.ts` — Claude opens a follow-up PR with the fix

---

## Pattern 2: Automatic PR Review on Push

Every PR gets a review the moment it opens or updates. No mention required.

```yaml
# .github/workflows/claude-auto-review.yml
name: Claude Auto PR Review
on:
  pull_request:
    types: [opened, synchronize]
    # Optional: only trigger on specific paths
    # paths:
    #   - 'src/**'
    #   - '!**/*.md'

jobs:
  claude-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Review this pull request. Focus on:
            - Logic errors and edge cases
            - Security issues (injection, auth, secrets)
            - Performance regressions
            - Missing error handling

            Format your response as:
            ## Summary
            One paragraph describing the change.

            ## Issues Found
            Numbered list, severity (Critical/Major/Minor), file:line reference.

            ## Suggestions
            Optional improvements.

            Keep it under 400 words. Be direct.
```

**Tip**: Add `paths:` to avoid triggering on doc-only PRs, or `if: github.event.pull_request.draft == false` to skip drafts.

---

## Pattern 3: Issue Triage and Labeling

Claude reads new issues, assigns labels, and posts a structured triage comment.

```yaml
# .github/workflows/claude-triage.yml
name: Issue Triage
on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      contents: read
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Triage this GitHub issue:

            1. Assign one label from: bug, enhancement, question, documentation, performance, security
            2. Assign a priority label: priority:critical, priority:high, priority:medium, priority:low
            3. Post a comment with:
               - Issue type classification
               - Which component is likely affected (based on the issue description)
               - Next step recommendation for the reporter (reproduce steps needed? version info missing?)

            Be brief. One sentence per point.
```

---

## Pattern 4: Security-Focused Review

Runs specifically for PRs touching sensitive paths (auth, payments, config).

```yaml
# .github/workflows/claude-security.yml
name: Security Review
on:
  pull_request:
    paths:
      - 'src/auth/**'
      - 'src/payments/**'
      - '**/config/**'
      - '**/.env*'
      - '**/secrets/**'

jobs:
  security-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Perform a security-focused review of this PR. Check for:

            - Injection vulnerabilities (SQL, command, LDAP)
            - Authentication and authorization bypasses
            - Secrets or credentials in code or comments
            - Insecure direct object references
            - Missing input validation
            - Unsafe deserialization
            - OWASP Top 10 patterns

            Rate overall risk: Low / Medium / High / Critical.
            If High or Critical, add the label 'security-review-required'.
            List each finding with: file:line, vulnerability type, and recommended fix.
```

---

## Pattern 5: Scheduled Repo Maintenance

Weekly health check — runs without any human trigger.

```yaml
# .github/workflows/claude-maintenance.yml
name: Weekly Repo Health Check
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am UTC
  workflow_dispatch:       # Also allows manual trigger

jobs:
  maintenance:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Perform a weekly repository health check:

            1. Scan package.json (or equivalent) for outdated major dependencies
            2. Check for TODO/FIXME comments older than 30 days in src/
            3. Identify any test files without corresponding implementation files
            4. List any documentation files that reference deleted or renamed files

            Open a GitHub issue titled "Weekly Health Check - [date]" with your findings.
            If nothing requires attention, post a comment "Health check passed — no issues found."
```

---

## Authentication Alternatives

The examples above use `ANTHROPIC_API_KEY` directly. For teams using cloud providers:

**Amazon Bedrock:**
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    use_bedrock: 'true'
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    AWS_REGION: us-east-1
    ANTHROPIC_MODEL: 'anthropic.claude-3-5-sonnet-20241022-v2:0'
```

**Google Vertex AI:**
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    use_vertex: 'true'
  env:
    ANTHROPIC_VERTEX_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
    CLOUD_ML_REGION: us-east5
    ANTHROPIC_MODEL: 'claude-3-5-sonnet-v2@20241022'
```

Cloud providers benefit from data residency compliance and can leverage existing IAM policies instead of managing a separate API key.

---

## Cost Control

Automated workflows run without a human in the loop — set explicit limits.

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    # Cap spend per workflow run
    claude_args: '--max-budget-usd 0.50'
    # Use Haiku for triage, Sonnet for reviews — don't default to Opus
    prompt: |
      ...
```

**Budget guidance by pattern:**

| Pattern | Model | Approx. cost / run |
|---------|-------|--------------------|
| PR review (medium PR) | Sonnet | $0.05–0.15 |
| Issue triage | Haiku | $0.01–0.03 |
| Security review (large PR) | Sonnet | $0.10–0.25 |
| Scheduled maintenance | Sonnet | $0.05–0.20 |

Monitor actual spend with `ccusage` or the Anthropic Console usage dashboard.

**Prevent runaway costs:**
- Use `paths:` filters to avoid triggering on irrelevant changes
- Add `if: github.event.pull_request.draft == false` to skip draft PRs
- Set `concurrency:` to prevent parallel runs on the same PR

```yaml
jobs:
  claude-review:
    concurrency:
      group: claude-${{ github.event.pull_request.number }}
      cancel-in-progress: true
```

---

## Security Checklist

Before deploying to a team repo:

- [ ] `ANTHROPIC_API_KEY` stored as a GitHub secret, never in workflow YAML
- [ ] Workflow permissions are minimal — use `contents: read` unless writes are required
- [ ] For public repos: add `if: github.event.pull_request.head.repo.full_name == github.repository` to prevent fork PRs from triggering API calls
- [ ] Review what the workflow posts publicly — Claude's comments are visible to all contributors
- [ ] Use `pull_request_target` with caution — it runs with write permissions even from forks

**Fork safety pattern (public repos):**
```yaml
jobs:
  claude:
    # Only run on PRs from the same repo, not forks
    if: github.event.pull_request.head.repo.full_name == github.repository
```

---

## See Also

- [Section 9.3 CI/CD Integration](../ultimate-guide.md#93-cicd-integration) — headless mode, Unix piping, `--output-format json`
- [Production Safety](../security/production-safety.md) — guardrails for automated agents
- [Security Hardening](../security/security-hardening.md) — MCP and webhook security
- [Official action docs](https://github.com/anthropics/claude-code-action) — solutions guide, migration, cloud providers
- [Community workflow blueprint](https://github.com/alirezarezvani/claude-code-github-workflow) — 8 workflows + 4 autonomous agents for advanced teams