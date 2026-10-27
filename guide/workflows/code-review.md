---
title: "Code Review (Claude Code feature)"
description: "Managed multi-agent PR review for Team and Enterprise: setup, review levels, triggers, comment commands, REVIEW.md configuration, and cost management"
tags: [feature, teams, enterprise, github, code-review]
---

# Code review

> **Availability**: Generally available since October 15, 2026 (research preview from March 9, 2026). Team and Enterprise plans only, on GitHub repositories (including GitHub Enterprise Server and GitHub Enterprise Cloud with data residency). Not available with Zero Data Retention, the HIPAA configuration, or customer-managed encryption keys (CMEK). Facts on this page were checked against the [official Code Review documentation](https://code.claude.com/docs/en/code-review) on October 27, 2026.

Claude Code's Code Review feature runs a multi-agent review on GitHub pull requests. Several agents examine the diff in the context of the surrounding code, each looking for a different class of issue (logic errors, security vulnerabilities, broken edge cases), followed by a verification pass that filters false positives.

Findings are posted as inline PR comments on the lines concerned, tagged by severity, with a summary in the review body and a check run named **Claude Code Review**. Reviews never approve or block a PR, and the check run never concludes as a failure, so existing review workflows stay intact.

Code Review is the managed option. On any plan you can also run [`/code-review`](https://code.claude.com/docs/en/code-review-local) locally, start an ultrareview from Claude Code, or run Claude in your own CI.

---

## How it works

1. **Find**: several agents examine the diff and the surrounding code in parallel on Anthropic infrastructure
2. **Verify**: a verification step checks candidate findings against the code and removes false positives
3. **Rank**: remaining findings are deduplicated and ranked by severity
4. **Post**: inline comments, a summary, and the **Claude Code Review** check run appear on the PR

A review reads the diff and surrounding code without building or running it, and its access to the repository is read-only: it does not push commits. Anthropic reported at GA that most reviews finish in 6 to 10 minutes, about three times faster than the roughly 20 minutes of the preview ([GA announcement](https://claude.com/resources/articles/code-review-is-now-generally-available)). Treat this as a vendor figure, not a guarantee.

### Review levels

An Owner sets one default level for the organization and can override it per repository:

| Level | Trade-off |
|-------|-----------|
| **Quick** | A lighter pass. Fastest, lowest cost |
| **Standard** | Balanced depth, speed, and cost. The default |
| **Deep** | The most thorough pass. Slowest, highest cost |

Code Review chooses the models itself; the admin settings offer no model choice. The level is the thoroughness control.

### Severity levels

| Marker | Severity | Meaning |
|:-------|:---------|:--------|
| 🔴 | Important | A bug that should be fixed before merging |
| 🟡 | Nit | Minor issue, worth fixing but not blocking |
| 🟣 | Pre-existing | A bug in the codebase not introduced by this PR |

When the review recorded its reasoning, the finding has a collapsed **Why this was flagged** section explaining why Claude flagged it and how it verified the problem.

---

## Setup

An **Owner** of the Claude organization turns on Code Review in **Admin settings > Claude Code** ([claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code#code-review)). Reviews run on Anthropic infrastructure, so no workflow files are added to repositories.

Required access:

- Owner role in the Claude organization, for every step on the admin page
- Owner of the GitHub organization, to install the Claude GitHub App and link it to the Claude organization
- Write access to each repository you add, from the GitHub account connected to Claude

Steps:

1. Click the **Allow code review** switch
2. Connect your GitHub account (select your GitHub Enterprise Server instance first if applicable)
3. Install the Claude GitHub App on the GitHub organization and choose the repositories it can access. The app's permission set is broader than a review uses because it is shared with other Claude features such as [GitHub Actions](./github-actions.md)
4. Choose repositories, then click **Continue**
5. Click **Finish** in the **Code review is set up** dialog. Closing it another way leaves **Allow code review** off
6. Open a non-draft test PR and check that a **Claude Code Review** check run appears

### Set when reviews run

Each repository has its own **Review runs** setting:

| Option | When it runs | Cost profile |
|--------|-------------|--------------|
| **Once after PR creation** | When a PR is opened, reopened, or marked ready for review | Lowest automatic option |
| **After every push** | On each push to the PR branch, auto-resolving threads when flagged issues are fixed | Highest (multiplied by push count) |
| **Manual (@claude review)** | Only on a comment command | Controlled |

A repository added from the **Add a repository** dialog **starts at After every push**, the most expensive option. Change it right after setup if you want fewer reviews. Automatic reviews skip draft PRs and PRs from forks whatever the setting.

An Owner can also cover a whole github.com organization from its row in the **Repositories** table, which requires a monthly spend limit and applies the chosen option to every repository there, including ones added later.

---

## Comment commands

Post the command as a new top-level PR comment, on one line at the start of the comment. You need write, maintain, or admin permission on the repository; bot comments do not start reviews.

| Command | Effect |
|---------|--------|
| `@claude review` or `@claude review once` | Starts one review of the whole PR, **without** subscribing it to future pushes |
| `@claude review always` | Starts a review and subscribes the PR to push-triggered reviews |
| `@claude review stop` (also `off`, `pause`) | Ends the subscription without starting or canceling a review |

Before a July 2026 update, `@claude review` subscribed the PR to push-triggered reviews. Use `@claude review always` for that behavior now. In a repository set to **After every push**, a comment cannot stop reviews; convert the PR to a draft instead.

A comment command works on drafts and on PRs from forks, which automatic reviews skip. For a fork, the write access required is to the base repository. If a review is already running on the latest commit, a new request does not start a second one.

If the repository also runs the [Claude Code GitHub Action](./github-actions.md) with its default `@claude` trigger phrase, `@claude review` starts the Action too. Set the Action's `trigger_phrase` input to another phrase to keep them apart.

### Re-reviews and kept results

A review that starts after a push focuses on what changed since the last review and posts fewer nits and pre-existing findings; the review body states how many it left out. Comment `@claude review` for a full re-review.

After a push that leaves the added and removed lines unchanged (an empty commit, a clean merge of the base branch, or a clean rebase), Code Review can keep the earlier result instead of starting a review. The check run title then starts with **Code review skipped** (no Important finding still open) or **Code review not repeated** (earlier Important findings still open).

### Gate a merge from your own CI

The check run concludes as neutral, never as a failure. To gate a merge, read the severity counts that the check run's Details text ends with, an HTML comment such as `<!-- bughunter-severity: {"nit":1,"normal":2,"pre_existing":0} -->`, where `normal` counts Important findings. A missing line means no verdict, not zero findings. The [official procedure](https://code.claude.com/docs/en/code-review-pull-requests#read-the-result-from-a-script) gives the `gh api` and `jq` commands and the title checks to run first.

---

## Configure reviews

Two files control what Claude flags. Both are additive on top of the default correctness checks.

### CLAUDE.md

Claude reads all `CLAUDE.md` files in your directory hierarchy. Newly-introduced violations are flagged as nit-level findings. Bidirectional: if a PR makes a `CLAUDE.md` statement outdated, Claude flags that the docs need updating too.

Use `CLAUDE.md` for guidance that also applies to interactive Claude Code sessions.

### REVIEW.md

Add `REVIEW.md` to your **repository root** for review-only rules. Auto-discovered, no configuration needed. Code Review reads it from the base or default branch, never from the PR's own changes, so a PR cannot loosen its own review rules.

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

Code Review is billed on token usage through usage credits, **separately from your plan's included usage**, and billed to the organization rather than to the developer who opened or requested the review. Costs appear on the Anthropic bill even when the organization uses Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry for other Claude Code features ([costs and usage](https://code.claude.com/docs/en/code-review-costs)).

- No flat per-review price: cost scales with the review level, change size, surrounding-code complexity, and the number of candidate issues to verify. The [support article](https://support.claude.com/en/articles/14233555-set-up-code-review-for-claude-code) gives an average of **$15-25 per review**
- "After every push" multiplies cost by push count, and it is the starting setting for new repositories
- Monthly spend limit: **Organization settings > Usage**, for the Claude Code Review service
- Average cost per review per repository: **Average cost** column of the **Repositories** table in **Admin settings > Claude Code**; analytics figures are estimated at list price and can differ from the invoice
- Enterprise promotion at GA: eligible Claude Enterprise organizations can claim at least $10,000 in Code Review credits by January 15, 2027; credits expire 30 days after claiming ([terms in the GA announcement](https://claude.com/resources/articles/code-review-is-now-generally-available))

---

## Cross-reference

For manual code review workflows (CLI, no Team/Enterprise required):
- [Multi-agent code review workflow](#split-role-sub-agents): DIY agent teams via CLI
- [GitHub Actions integration](./github-actions.md): custom CI/CD automation (self-hosted alternative to this managed service)
- [Multi-provider code review](./multi-provider-code-review.md): running Claude alongside CodeRabbit/Greptile without redundant findings, self-hosted
- GitLab CI/CD: self-hosted Claude integration for GitLab pipelines
- Code Review plugin: on-demand local reviews before pushing (available in the plugin marketplace)

---

## A review informs the acceptance policy

A posted review is evidence to qualify, not permission to merge. Confirm the reviewed revision, actual execution and covered scope, then apply the repository's required checks and authorized decision process. Preserve unresolved findings and disagreements when summarizing. The [multi-provider workflow](./multi-provider-code-review.md#blocking-merge-the-ci-gate) covers these boundaries and a local control exercise; it does not establish the managed service's runtime behavior.

## Known limitations

- Team and Enterprise only, no Free/Pro access
- Not available with Zero Data Retention, the HIPAA configuration (not covered by Anthropic's BAA), or customer-managed encryption keys
- GitHub only for the managed service (GitLab supported via CI/CD integration, not this feature)
- Reviews do not run in self-hosted environments and do not build or execute your code
- Automatic reviews skip drafts and PRs from forks; request those with a comment command
- Anthropic internal stats from the preview: ~7.5 issues found per PR >1000 lines, <1% false positive rate (self-reported, not independently verified)
