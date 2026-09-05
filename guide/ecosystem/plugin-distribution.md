---
title: "Plugin Distribution and Recommendation Hints"
description: "Distribute Claude Code plugins through marketplaces and use official recommendation hints without bypassing user consent"
tags: [plugins, marketplace, distribution, security, guide]
---

# Plugin Distribution and Recommendation Hints

A plugin packages reusable Claude Code skills, agents, hooks, MCP servers, LSP servers, monitors, and settings. Use standalone `.claude/` configuration for local or project-specific iteration; use a plugin when the same extension needs a versioned, shareable distribution unit. [Anthropic's plugin documentation](https://code.claude.com/docs/en/plugins) is the authority for supported structure and loading behavior.

This page separates distribution from recommendation. A marketplace makes a plugin available. A `<claude-code-hint />` marker can ask the user whether to install an eligible official plugin after a CLI command runs. Neither mechanism removes the need to inspect code that can run hooks, commands, MCP servers, or executables.

## Distribute through a marketplace

An official marketplace is a catalog of plugins and their sources. Its `marketplace.json` can refer to local relative paths, GitHub or other Git URLs, git subdirectories, npm packages, HTTPS archives, and command-produced plugin directories. The source type determines how Claude Code obtains the plugin; it does not establish that the plugin is safe for a particular organization.

For a team or community distribution, create the plugins, list them in `marketplace.json`, host that catalog in a Git repository or other supported source, then have users add the marketplace and install an individual plugin. Users update their local marketplace copy with `/plugin marketplace update`. [Anthropic's marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces) defines the manifest, source types, version behavior, and reserved official marketplace names.

Test a plugin before publishing with a local directory:

```bash
claude --plugin-dir ./my-plugin
```

The local test shows that Claude Code can load the plugin. It does not prove that its hooks, MCP servers, dependencies, or executable paths are appropriate for another user's machine. Review those components under the same supply-chain controls used for other executable dependencies.

## The `<claude-code-hint />` recommendation channel

The hint protocol lets a command from a CLI or SDK maintainer recommend its official Anthropic-marketplace plugin. When the command runs through Claude Code's Bash or PowerShell tool, it emits one self-closing tag on its own line. Claude Code removes the marker from command output before that output reaches the model, validates the targeted plugin, and may show an install prompt in the main interactive terminal session.

```text
<claude-code-hint v="1" type="plugin" value="example-cli@claude-plugins-official" />
```

The documented validation boundary is narrow and specific:

| Check or behavior | What it establishes | What it does not establish |
|---|---|---|
| The marker occupies its own line | Claude Code recognizes the protocol syntax. | The command's output is trustworthy. |
| The target is in an Anthropic-controlled marketplace | Claude Code accepts only an eligible official marketplace target. | The emitting command and plugin are the same publisher. |
| The prompt names the emitting command | The user can see which command requested the recommendation. | The command's recommendation is necessary or suitable. |
| The marker is removed before model input | The model does not receive the marker line as command output. | Other command output or on-screen instructions are safe. |
| User confirmation | Claude Code does not install automatically. | A user-approved plugin is safe to enable. |

The last column is an operational inference from the documented controls, not a claim that the protocol verifies provenance between the CLI and plugin publisher. Treat the prompt as a recommendation with a named producer, then inspect the plugin and its marketplace entry before approval.

## User control and prompt limits

Claude Code shows at most one hint prompt per session and at most one prompt for a given plugin. It does not prompt in subagents, `claude -p`, or Agent SDK runs, although it still strips hint lines there. The prompt times out as **No** after 30 seconds. A user can decline one prompt, or choose the option that disables future plugin-installation hints.

Hints do not trigger when analytics is disabled, including documented telemetry opt-out variables and provider situations with automatic telemetry opt-out. In hook commands, Claude Code strips and ignores the tag. A hint is therefore not a dependable automation channel or a policy-enforcement mechanism.

## Guidance for CLI and SDK maintainers

Only emit a hint for a plugin that is listed in an official Anthropic marketplace. The documented protocol supports version `1`, type `plugin`, and a `name@marketplace` value. Write it to stderr on its own line and gate its emission on a Claude Code environment variable.

Choose the gate intentionally:

| Variable | Documented scope | Trade-off |
|---|---|---|
| `CLAUDECODE` | Present for commands Claude Code runs, and also in some integrated terminals, tmux sessions, and stdio MCP subprocesses. | Broad reach, but a human terminal can see the raw tag. |
| `CLAUDE_CODE_CHILD_SESSION` | Present for subprocesses Claude Code itself starts. Requires Claude Code v2.1.172 or later. | Usually avoids a human terminal, but older sessions do not receive the hint and long-lived child processes can retain the variable. |

Emit from a useful, user-comprehensible touchpoint such as `--help`, an unknown-subcommand error, successful authentication, or a first-run message. Do not emit a tag in the expectation that it will influence the model or force installation. The official [plugin-hints reference](https://code.claude.com/docs/en/plugin-hints) is the protocol source.

## Distribution security boundary

An official-marketplace target is a protocol requirement for hints, not a general safety verdict for a plugin's executable behavior. Before enabling a distributed plugin, identify its manifest, components, source, dependency installation behavior, and scope. Apply [plugin and marketplace settings](../core/settings-reference.md#plugins-and-marketplaces) and [security hardening guidance](../security/security-hardening.md) before distributing hooks, MCP configuration, or executables.

## Related pages

- [Computer Use in Claude Code](../core/computer-use.md) covers a separate local desktop permission boundary.
- [API gateway operations](../ops/api-gateway.md) cover organization-level identity, model, and telemetry controls.
- [Anthropic marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces) is the current source for marketplace implementation.
