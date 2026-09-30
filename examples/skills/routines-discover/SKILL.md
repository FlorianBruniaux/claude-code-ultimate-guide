---
name: routines-discover
description: "Analyzes the current project to surface high-value Routines use cases across the three trigger types (schedule, API, GitHub events). Usage: /routines-discover"
effort: medium
disable-model-invocation: true
---

# Routines use case discovery

Analyzes this codebase and surfaces actionable Routine candidates across the three trigger types.

**Usage**: `/routines-discover` - no arguments needed. Run it in the root of any project.

---

## What are Routines

A Routine is an autonomous Claude Code session running on Anthropic-managed cloud infrastructure, triggered in three ways:

| Trigger | How it fires |
|---------|-------------|
| **Schedule** | Recurring cron cadence (min 1 hour) |
| **API** | HTTP POST to a per-routine endpoint with bearer token |
| **GitHub events** | Repository events: PR opened/merged, push, issue, workflow run, etc. |

Each run clones a fresh copy of the GitHub repository, runs a full Claude Code session with configured MCP connectors (Slack, Linear, GitHub, Google Drive…), and can create branches, open PRs, post messages, and call external APIs. No local machine required.

**Daily limits**: Pro 5/day · Max 15/day · Team/Enterprise 25/day.

---

## Instructions

### Step 1: Read the codebase

Before generating any output, silently read:
- `README.md` or `CLAUDE.md` to understand the project purpose and stack
- `package.json`, `Cargo.toml`, `pyproject.toml`, or equivalent for dependencies
- `.github/workflows/` to understand existing CI/CD automation
- Any monitoring, deploy, or ops configuration you find

If MCP connectors are configured in `.claude/settings.json`, note which external services are connected.

### Step 2: Analyze against five dimensions

For each dimension, think concretely about this specific project before writing anything.

**1. Scheduled maintenance**
What recurring work currently requires a human to run manually or remember to do?
Think: dependency audits, stale issue/PR triage, test flakiness reports, coverage drift, TODO comment tracking, dead code detection, daily or weekly summaries.

**2. Event-driven reactions**
What should happen automatically when a PR is opened, merged, or closed, but doesn't today because no one gets to it?
Think: review checklists, changelog updates, cross-repo sync, Slack notifications with context, label enforcement, docs updates on API changes.

**3. Alert and incident response**
What monitoring signals exist? When something breaks, what is the first thing a developer does?
Think: correlating an alert with recent commits, triaging a failing build, drafting a postmortem skeleton, routing an error to the right team.

**4. Cross-system sync**
What drifts today because the sync between two systems is manual?
Think: keeping two SDKs in sync, updating a doc site when an API changes, syncing GitHub issues with Linear, keeping a README stats section current.

**5. Release and deploy automation**
What steps happen before or after a deploy that a human runs by hand?
Think: smoke tests, release notes, version bumps, stakeholder notifications, go/no-go summaries.

### Step 3: Output

For each use case identified, produce a card in this format:

---

**[Name]** · `schedule` / `api` / `github`

*Trigger*: [what fires it: cron expression, which event, which external system]

*Input*: [what Claude receives: repo state, event payload, alert body]

*Output*: [what Claude produces: PR opened, message posted, file updated, issue created]

*Value*: [time saved or risk reduced, be specific]

*Blockers*: [missing connector, secrets needed, GitHub App required, etc., or "none"]

---

Sort cards by **value-to-effort ratio**, highest first.

After all cards, add a **Quick Wins** section: the two or three use cases that could be set up in under 15 minutes with the current repo and connector configuration.

---

## Example Output (for reference only, do not copy, analyze the actual project)

**Nightly stale PR report** · `schedule`

*Trigger*: Every weekday at 8am

*Input*: Repo state: all open PRs older than 5 days

*Output*: Slack message to #engineering with list of stale PRs, assignee, and last activity

*Value*: Saves ~15min of manual triage each morning, reduces PR rot

*Blockers*: Requires Slack MCP connector
