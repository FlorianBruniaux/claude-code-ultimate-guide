---
title: "Code Review (Claude Code feature)"
description: "Automated multi-agent PR review for Teams and Enterprise — setup, triggers, REVIEW.md configuration, and cost management"
tags: [feature, teams, enterprise, github, code-review]
---

# Code Review

> **Availability**: Research preview — Teams and Enterprise plans only. Not available on Free/Pro accounts, nor for organizations with Zero Data Retention (ZDR) enabled.
> **Launched**: March 9, 2026

Claude Code's Code Review feature runs a multi-agent review on every GitHub pull request. A fleet of specialized agents examines the diff in the context of the full codebase, each looking for a different class of issue (logic errors, security vulnerabilities, edge cases, regressions), followed by a verification pass that filters false positives.

Findings are posted as inline PR comments on the specific lines where issues were found, tagged by severity. Reviews don't approve or block PRs, so existing review workflows stay intact.

---

## How it works

1. Trigger fires (PR opened, push, or manual `@claude review` comment)
2. Multiple agents analyze the diff and surrounding code in parallel on Anthropic infrastructure
3. Each agent targets a different class of issue
4. A verification step checks candidates against actual code behavior to remove false positives
5. Results are deduplicated, ranked by severity, and posted as inline PR comments
6. If no issues are found, Claude posts a short confirmation comment

Reviews complete in **20 minutes on average**, scaling with PR size and complexity.

### Severity levels

| Marker | Severity | Meaning |
|:-------|:---------|:--------|
| 🔴 | Normal | A bug that should be fixed before merging |
| 🟡 | Nit | Minor issue, worth fixing but not blocking |
| 🟣 | Pre-existing | A bug in the codebase not introduced by this PR |

Each finding includes a collapsible extended reasoning section explaining why Claude flagged the issue and how it verified the problem.

---

## Setup

An admin enables Code Review once for the organization and selects which repositories to include.

### 1. Open admin settings

Go to [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) and find the **Code Review** section. Requires admin access to both your Claude organization and permission to install GitHub Apps in your GitHub organization.

### 2. Click Setup

This begins the GitHub App installation flow.

### 3. Install the Claude GitHub App

Follow the prompts to install the Claude GitHub App on your GitHub organization. The app requests:

- **Contents**: read and write
- **Issues**: read and write
- **Pull requests**: read and write

Code Review uses read access to contents and write access to pull requests. This permission set also supports [GitHub Actions](/en/github-actions) if you enable that later.

### 4. Select repositories

Choose which repositories to enable. If a repo is missing, ensure you granted the GitHub App access during installation. You can add more repositories later from the admin settings table.

### 5. Set review triggers per repo

For each repository, choose when reviews run:

| Trigger | When it runs | Cost profile |
|---------|-------------|--------------|
| **Once after PR creation** | Once when PR opens or is marked ready | Lowest |
| **After every push** | On every push to the PR branch | Highest (multiplied by push count) |
| **Manual** | Only when someone comments `@claude review` | Controlled |

After the `@claude review` comment, subsequent pushes to that PR trigger reviews automatically regardless of the configured trigger.

**Manual mode** is useful for high-traffic repos where you want to opt specific PRs into review, or only start reviewing when the PR is ready for review.

---

## Manual trigger

Comment `@claude review` on any open, non-draft PR to start a review immediately. Requirements:

- Top-level PR comment (not an inline diff comment)
- `@claude review` at the start of the comment
- Owner, member, or collaborator access on the repository

If a review is already running, the request queues until the in-progress review completes.

---

## Configure reviews

Two files control what Claude flags. Both are additive on top of the default correctness checks.

### CLAUDE.md

Claude reads all `CLAUDE.md` files in your directory hierarchy. Newly-introduced violations are flagged as nit-level findings. Bidirectional: if a PR makes a `CLAUDE.md` statement outdated, Claude flags that the docs need updating too.

Use `CLAUDE.md` for guidance that also applies to interactive Claude Code sessions.

### REVIEW.md

Add `REVIEW.md` to your **repository root** for review-only rules. Auto-discovered, no configuration needed.

```markdown
# Code Review Guidelines

## Always check
- New API endpoints have corresponding integration tests
- Database migrations are backward-compatible
- Error messages don't leak internal details to users

## Style
- Prefer early returns over nested conditionals
- Use structured logging, not f-string interpolation in log calls

## Skip
- Generated files under `src/gen/`
- Formatting-only changes in `*.lock` files
- Migration files in `db/migrations/`
```

Use `REVIEW.md` for rules that would clutter `CLAUDE.md` for general sessions (linter conventions, skip lists, team-specific patterns).

---

## Pricing

Code Review is billed on token usage, **separately from your plan's included usage** (via [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)).

- Average cost: **$15–25 per review**, scaling with PR size, codebase complexity, and the number of issues requiring verification
- "After every push" multiplies cost by push count
- To set a monthly spend cap: [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) → configure limit for the "Claude Code Review" service
- Monitor spend: [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) (daily PR count, weekly spend, per-repo breakdown)

---

## Cross-reference

For manual code review workflows (CLI, no Teams/Enterprise required):
- [Multi-agent code review workflow](../ultimate-guide.md#multi-agent-code-review) — DIY agent teams via CLI
- [GitHub Actions integration](./github-actions.md) — custom CI/CD automation (self-hosted alternative to this managed service)
- [GitLab CI/CD](/en/gitlab-ci-cd) — self-hosted Claude integration for GitLab pipelines
- Code Review plugin — on-demand local reviews before pushing (available in the plugin marketplace)

---

## Known limitations (research preview)

- Teams and Enterprise only — no Free/Pro access
- Not available for organizations with Zero Data Retention (ZDR) enabled
- GitHub only for the managed service (GitLab supported via CI/CD integration, not this feature)
- Full-repo indexing latency on first activation for large repos
- Anthropic internal stats: ~7.5 issues found per PR >1000 lines, <1% false positive rate — self-reported, not independently verified
