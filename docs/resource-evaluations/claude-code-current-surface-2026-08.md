---
title: "Claude Code Current Surface: Computer Use, Plugin Hints, Apps Gateway, and Artifacts"
date: 2026-08-31
status: verified-current-official-docs
sources: official Claude Code documentation
---

# Claude Code Current Surface: Computer Use, Plugin Hints, Apps Gateway, and Artifacts

## Verdict

The current official Claude Code documentation confirms four product surfaces that affect the guide's learning priorities: Computer Use from the macOS CLI, plugin recommendation hints, Claude apps gateway, and artifact publishing. This evaluation reports documented behavior as read on 2026-08-31. It does not claim a local runtime validation, plan entitlement beyond the stated documentation, or compatibility beyond the sources listed below.

## Official evidence read

| Surface | Official source | Status | Evidence boundary |
|---|---|---|---|
| Computer Use | [Let Claude use your computer from the CLI](https://code.claude.com/docs/en/computer-use) | Confirmed | Research preview on macOS CLI, Pro and Max, interactive claude.ai-authenticated sessions. |
| Plugin recommendation hints | [Recommend your plugin from your CLI](https://code.claude.com/docs/en/plugin-hints) | Confirmed | CLI and SDK maintainer protocol for eligible official-marketplace plugins. |
| Plugin distribution | [Create plugins](https://code.claude.com/docs/en/plugins) and [plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) | Confirmed | Plugin structure, marketplace catalog, and supported source types. |
| Claude apps gateway | [Claude apps gateway](https://code.claude.com/docs/en/claude-apps-gateway) and [gateway overview](https://code.claude.com/docs/en/gateways) | Confirmed | Self-hosted gateway behavior and documented limitations. |
| Artifact publishing | [Share session output as artifacts](https://code.claude.com/docs/en/artifacts) | Confirmed | Current official page explicitly documents private, organization, and public-link sharing subject to plan and feature conditions. |

The official [documentation index](https://code.claude.com/docs/llms.txt) was read first to locate the current Markdown pages. No community source, release summary, local generated index, or unverified product claim is evidence for this evaluation.

## Current product implications

### Computer Use

Computer Use is distinct from Bash, browser automation, and MCP. The official order prefers an MCP server, Bash, or Claude in Chrome before screen control. Its operation on the actual desktop creates a separate trust boundary: per-application approval and `Esc` stopping reduce risk, but they do not sandbox the approved application or its visible data. The dedicated guide page is [Computer Use in Claude Code](../../guide/core/computer-use.md).

### Plugin hints

The `<claude-code-hint />` marker is a one-line CLI-output protocol, not a model prompt. Claude Code strips it before model input, accepts only an eligible official-marketplace plugin target, and asks the user before installation. The protocol identifies the emitting command in the prompt but does not document a publisher-identity proof between that command and the plugin. The dedicated guide page is [Plugin Distribution and Recommendation Hints](../../guide/ecosystem/plugin-distribution.md).

### Claude apps gateway

Claude apps gateway is a self-hosted service included in the `claude` binary. The documentation describes corporate SSO, IdP-group policy, upstream credential handling, OTLP telemetry, and upstream routing. It must use a private address because it can deliver client settings. Its device-flow sign-in has no service-token path for unattended CI. The gateway section in [API Gateway for Enterprise Claude Code](../../guide/ops/api-gateway.md) documents the confirmed scope and the verification boundary.

### Artifact publishing

Artifact publishing is **CONFIRMED**, not `UNKNOWN`. The current official artifact page says Claude Code can publish a session's output as a live page on claude.ai; a new artifact is initially private, and sharing can be within an organization or through a public link depending on plan and configured controls. Publishing depends on session permission mode, and a connector-backed artifact cannot be publicly shared. This evaluation does not assess suitability for confidential data, organization-specific retention, or local availability. Those questions need the applicable plan, settings, and data-governance evidence.

## Exclusions and follow-up evidence

| Question | Status | Reason |
|---|---|---|
| Local execution on a specific device or account | UNKNOWN | Documentation is not a runtime witness. |
| Organization policy and entitlement configuration | UNKNOWN | The official behavior depends on plan, managed settings, and administrator choices. |
| Safety of a particular plugin or marketplace entry | UNKNOWN | Marketplace eligibility does not audit the plugin's executable behavior for a local threat model. |
| Artifact retention and confidentiality for a specific organization | UNKNOWN | This requires organization policy, configured sharing controls, and data-classification review. |

## Guide decision

The four official pages now have stable guide routes for focused navigation. A navigation or machine-readable-index change remains a separate task because this worktree was limited to current-surface documentation and did not modify repository-wide indexes.
