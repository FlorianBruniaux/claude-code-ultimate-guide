---
title: "Monitor, Channels and Safe Delegation to Codex"
description: "Choose Monitor, plugin monitors, MCP Channels, or Routines, then route GitHub events to Codex without turning untrusted input into authority."
tags: [workflow, monitoring, websocket, channels, routines, codex, security]
---

# Monitor, Channels and Safe Delegation to Codex

External events are data, not instructions and never authorization. A GitHub webhook, log line, WebSocket frame, or Channel message can tell Claude Code that something happened. It cannot approve a tool call, widen a sandbox, or authorize a write to your repository.

**Official references**: [Monitor](https://code.claude.com/docs/en/tools-reference#monitor-tool), [WebSocket source](https://code.claude.com/docs/en/tools-reference#websocket-source), [plugin monitors](https://code.claude.com/docs/en/plugins-reference#monitors), [Channels](https://code.claude.com/docs/en/channels-reference), [Routines](https://code.claude.com/docs/en/routines), [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode), [GitHub webhook validation](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries), and [failed webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries).

## Choose the delivery mechanism

| Need | Use | Boundary to keep |
|---|---|---|
| Stream output from one local process | `Monitor` command source (v2.1.98+) | The command follows Bash permissions. |
| Receive a narrow real-time event from a local relay | `Monitor` WebSocket source (v2.1.195+) | The relay validates the original event before it reaches Claude. |
| Start a trusted persistent watcher with a plugin or skill | Plugin monitor (v2.1.105+) | It is unsandboxed and trusted like a hook. |
| Let an MCP integration send or exchange messages | Channels (v2.1.80+, research preview) | Sender allowlisting is required; delivery does not grant tool permissions. |
| Run scheduled, API, or GitHub-triggered cloud automation | [Routines](../ultimate-guide.md#routines-cloud-automation) | Each matching event starts a separate cloud session. |

Do not use a Monitor as a public webhook endpoint. Put a small verifier or event relay in front of it.

## Monitor sources

### Command source

The original `Monitor` source runs a background command and feeds each output line back to Claude. It supports `timeout_ms` and `persistent`; stop an active monitor with `TaskStop`. The command source and the WebSocket source are mutually exclusive.

Use it for a bounded local producer: tailing an application log, watching a test runner, or turning a trusted polling script into events. It is not a reason to auto-execute the content of a line.

### WebSocket source

The native WebSocket source takes `ws.url` and optional `ws.protocols`, instead of `command`. Text frames become events. Binary frames are represented by a placeholder; a frame over 1 MiB, or closing the socket, stops the monitor.

Claude Code accepts only ASCII `ws://` or `wss://` URLs without credentials or whitespace. It requests a dedicated approval and refuses private, link-local, and metadata-service destinations. These checks narrow the client-side attack surface; they do not authenticate the event producer.

For a GitHub event relay, forward a small typed record, not the webhook body:

```json
{
  "delivery_id": "uuid",
  "repository": "owner/repo",
  "event": "workflow_run",
  "sha": "full-commit-sha",
  "pr_number": 42,
  "url": "https://github.com/owner/repo/actions/runs/123"
}
```

Raw issue text, pull request bodies, review comments, and log output remain untrusted data. Do not interpolate them into a task prompt or shell command.

## Plugin monitors and Channels

Plugin monitors are experimental, interactive-CLI-only persistent shell commands. The default declaration is `monitors/monitors.json`; a plugin can instead set `experimental.monitors` in `plugin.json` to an inline array or a relative JSON path. `when: "always"` is the default; `when: "on-skill-invoke:<skill-name>"` starts the monitor when that named plugin skill is first dispatched. Treat one as a hook: it runs unsandboxed and therefore deserves the same publisher review, code review, and trust boundary.

Channels are an MCP stdio extension: servers emit `notifications/claude/channel` notifications into a session. They can be one-way or two-way, can relay permission prompts, and remain a research preview. Claude.ai Team and Enterprise organizations must explicitly enable Channels, then may restrict delivery with `channelsEnabled` and `allowedChannelPlugins`. For Console API-key deployments, follow the Console default and managed controls rather than assuming the claude.ai Team/Enterprise policy; see [Settings Reference](../core/settings-reference.md#channelsenabled).

Allowlisting a Channel plugin decides which plugin may deliver a message. It does not grant that plugin, its message, or its sender any Bash, filesystem, GitHub, or Codex permission. Gate senders and normalize displayed content because messages can carry prompt-injection attempts.

## GitHub to Monitor to Codex: a safe pipeline

```text
GitHub webhook
  -> verifier: signature, allowlisted repo and event, schema, delivery dedupe
  -> narrow WebSocket event
  -> approved local Monitor
  -> read-only, classify-only Codex run
  -> explicit human or policy gate
  -> isolated write-capable Codex task and pull request
```

The verifier checks the GitHub signature before parsing or using the payload, accepts only the repositories and event types it owns, and validates the expected schema. It then atomically writes an outbox record keyed by `X-GitHub-Delivery` in state `received`; the relay atomically moves it to `enqueued` before sending the narrow event and to `processed` only after the downstream outcome is recorded. A duplicate delivery returns the existing record, never a second task. A crash leaves a recoverable `received` or `enqueued` record rather than silently dropping the event. GitHub does not automatically redeliver failed webhooks, so this durable state machine is required, not optional.

### Stage 1: classify without writes

Use `codex exec` in its default read-only sandbox. `--ephemeral` avoids persisting the rollout; `--json` emits JSONL events for an audit trail; `--output-schema` constrains the final result for a policy check.

```bash
codex exec --ephemeral --json --output-schema ./triage-schema.json \
  "Classify this verified event using only its typed fields. Return whether a human review is required. Do not edit files."
```

Treat the schema result as an input to a deterministic policy, not as authorization by itself. Confirm the repository, commit SHA, event type, and reviewer or policy decision before proceeding.

### Stage 2: write only after a gate

After an explicit human approval or a documented policy gate, run a separate task in an isolated worktree with the smallest write scope required. The gate must record the approved absolute worktree path and commit SHA. Refuse to run if the path is relative, is not a linked Git worktree, is not at the approved SHA, or does not match the approval record:

```bash
: "${APPROVED_WORKTREE:?absolute approved worktree path required}"
: "${APPROVAL_RECORD:?absolute approval record path required}"
: "${APPROVED_SHA:?approved commit SHA required}"

case "$APPROVED_WORKTREE" in /*) ;; *) echo "refusing relative worktree path" >&2; exit 1 ;; esac
case "$APPROVAL_RECORD" in /*) ;; *) echo "refusing relative approval record path" >&2; exit 1 ;; esac
test -f "$APPROVED_WORKTREE/.git" || { echo "refusing non-linked worktree" >&2; exit 1; }
test -f "$APPROVAL_RECORD" || { echo "missing approval record" >&2; exit 1; }
test "$(git -C "$APPROVED_WORKTREE" rev-parse --show-toplevel)" = "$APPROVED_WORKTREE" || exit 1
test "$(git -C "$APPROVED_WORKTREE" rev-parse HEAD)" = "$APPROVED_SHA" || exit 1
jq -e --arg worktree "$APPROVED_WORKTREE" --arg sha "$APPROVED_SHA" \
  '.approved == true and .worktree == $worktree and .sha == $sha' "$APPROVAL_RECORD" >/dev/null || exit 1

(
  cd -- "$APPROVED_WORKTREE" || exit 1
  codex exec --ephemeral --sandbox workspace-write \
    "Implement the approved task in this isolated worktree, run the stated checks, and prepare a bounded diff for review."
)
```

Review the diff and test evidence before opening or merging a pull request. Never attach `--sandbox workspace-write` directly to an inbound event.

## GitHub Actions is a separate path

For GitHub Actions, prefer [`openai/codex-action@v1`](https://github.com/openai/codex-action) over installing Codex and passing the key to a shell step: the action starts a secure proxy while receiving `openai-api-key` as an action input. Keep the Codex analysis job read-only, serialize a patch artifact, then apply it and open a pull request in a separate write-permitted job. Do not put `OPENAI_API_KEY` or `CODEX_API_KEY` in a job-level environment where checked-out code, build scripts, tests, lifecycle hooks, or a compromised action could read it.

This GitHub Actions pattern is separate from a local Monitor. A hosted runner cannot safely assume it can reach your local WebSocket service.

## Routines: useful, but not a local Monitor

Routines run on Anthropic-managed cloud infrastructure or an organization's self-hosted environment. They can react to schedules, API calls, and GitHub events, but every matching event creates a separate session. Use them when that environment, not a local session, is the intended execution boundary. Use a local Monitor when a local, explicitly approved session must observe a trusted local relay.

See [Event-Driven Agent Automation](./event-driven-agents.md) for the generic architecture and [GitHub Actions Workflows](./github-actions.md) for Claude Code-specific CI patterns.
