---
title: "Computer Use in Claude Code"
description: "Enable, constrain, and verify Claude Code computer use from an interactive macOS CLI session"
tags: [computer-use, permissions, macos, security, guide]
---

# Computer Use in Claude Code

Computer use lets Claude Code control approved macOS applications and inspect their visible screen content from an interactive CLI session. It is a research preview for Pro and Max users. It is unavailable on Team and Enterprise plans, in `claude -p`, and in the CLI on Linux or Windows. [Anthropic's current Computer Use documentation](https://code.claude.com/docs/en/computer-use) is the product authority for this page.

Use it for a native app, simulator, or GUI-only tool that has no more precise integration. For a browser task, prefer [Claude in Chrome](https://code.claude.com/docs/en/chrome); for a service with an API, prefer an MCP server. The official tool-selection order is MCP, Bash, Chrome, then computer use.

## Enable the built-in server

Computer use is a built-in MCP server named `computer-use`, disabled until enabled for a project.

1. Start an interactive Claude Code session and run `/mcp`.
2. Select `computer-use` and choose **Enable**. The project keeps that setting.
3. When macOS asks, grant **Accessibility** for click, type, and scroll, and **Screen Recording** for screen capture. A Screen Recording grant can require restarting Claude Code.

The server appears only on an eligible macOS, Pro or Max, claude.ai-authenticated, interactive session. `/status` helps verify the plan. A third-party-provider-only login, including Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry, does not make the CLI surface available.

## What Claude can control

The first request for an application in a session presents an approval prompt. It names the applications, any additional permission such as clipboard access, and the number of other applications that will be hidden. Approval lasts only for that session.

| Application class | Documented control level | Review before approving |
|---|---|---|
| Browsers and trading platforms | View only | Visible data can still reach the model through screenshots. |
| Terminals and IDEs | Click only | The prompt warns that the application is equivalent to shell access. |
| Finder | Full control | The prompt warns that it can read or write any file. |
| System Settings | Full control | The prompt warns that it can change system settings. |
| Other approved applications | Full control | Confirm the application and task are within the intended boundary. |

Claude hides other visible applications while it controls the screen, then restores them after the turn. The terminal stays visible and is excluded from screenshots. Only one Claude Code session can use computer use at once: its machine-wide lock remains until the session exits, even after the immediate task finishes.

## Data exposure and safety boundary

Computer use runs on the actual desktop, not inside the [sandboxed Bash boundary](../security/sandbox-isolation.md). Claude Code automatically downsizes screenshots before sending them to the model, but that does not make visible application data safe to expose. Treat every approved application and its visible content as part of the model's input boundary.

Claude Code documents per-application approval, warnings for broad-reach applications, terminal screenshot exclusion, a single-session lock, and `Esc` as a global stop. It also says Claude checks actions and flags possible prompt injection from on-screen content. Those controls reduce risk; they do not convert a desktop application into an isolated sandbox.

Before enabling the server for a sensitive workflow:

- close applications that do not belong to the task;
- use a dedicated local account or fixture data when production data is unnecessary;
- approve the smallest useful set of applications;
- keep a person at the terminal for any flow that can change data, money, credentials, or system configuration;
- use [Tool and permission reference](./tools-reference.md) and [security hardening guidance](../security/security-hardening.md) for controls outside this feature.

## Operate and stop safely

Give the task a concrete success condition, such as opening a specific screen, reproducing a layout defect at a named size, or recording the state of a simulator flow. Ask for screenshots or a written result when that is the evidence you need. Computer use can combine GUI steps with Bash, but the screenshot is evidence of the visible state only, not proof of a backend effect.

Press `Esc` anywhere to abort the current computer-use action. `Ctrl+C` in the terminal also stops it. Both restore hidden applications, but the computer-use lock remains until that Claude Code session exits. Do not start a second session expecting it to take over the desktop.

## Failure modes and verification

| Symptom | Documented cause or limit | Verification or response |
|---|---|---|
| `computer-use` is absent from `/mcp` | The platform, plan, authentication, or interactive-session requirement is not met. | Check macOS, `/status`, claude.ai authentication, and that the session was not started with `-p`. |
| Another session holds the feature | The machine-wide lock lasts until its session exits. | Exit the named session. A crashed process releases its lock after Claude Code detects it is gone. |
| macOS repeats the permission request | Screen Recording can need a requesting-process restart. | Quit Claude Code, start a new session, and confirm Screen Recording for the terminal application in macOS settings. |
| Text or controls are hard to read | Screenshots are downscaled automatically and the target size is not configurable. | Increase text or control size in the application, then repeat the visible-state check. |
| A GUI step appears successful | A screen state does not prove a persisted change or downstream outcome. | Verify with the application's own confirmation, a read-back, test, or other task-specific evidence. |

## Related pages

- [Plugin distribution and recommendation hints](../ecosystem/plugin-distribution.md) cover a separate extension-distribution surface.
- [API gateway operations](../ops/api-gateway.md) cover organization-level model routing rather than desktop control.
- [Anthropic Computer Use documentation](https://code.claude.com/docs/en/computer-use) contains the current eligibility, permission, and troubleshooting reference.
