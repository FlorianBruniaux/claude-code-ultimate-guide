---
title: "Cross-Session Messaging"
description: "How independent Claude Code sessions discover and message each other with ListAgents and SendMessage: mechanics, security model, and coordination patterns"
tags: [multi-agent, sessions, security, tools-reference]
---

# Cross-Session Messaging

Cross-session messaging lets one Claude Code session deliver a short text message to another, independently launched Claude Code session, without you copy-pasting between terminals. Two tools carry the whole feature: `ListAgents` discovers which sessions are reachable, `SendMessage` delivers text to one of them by name. Neither tool is something you call yourself; Claude decides when to use them, on its own or because you asked it to.

**Official docs**: [code.claude.com/docs/en/cross-session-messaging](https://code.claude.com/docs/en/cross-session-messaging)

> **See also**: [Tools Reference](../core/tools-reference.md#cross-session-messaging-listagents--sendmessage) for the tool table entry, [Agent Teams](./agent-teams.md) for the related but distinct teammate-mailbox mechanism, [Security Hardening: Cross-Session Messaging](../security/security-hardening.md#cross-session-messaging-threat-model) for the full threat model.

---

## 1. What it solves, and what it isn't

Anthropic's framing: "when a change in one session breaks what another is building on, Claude can warn that session before you notice. When one session settles a question another is blocked on, Claude can send the answer across." A message is defined narrowly: a piece of text one Claude writes to another, never conversation history and never files. Moving a whole conversation or its context is a different feature, [resuming a session](../ultimate-guide.md#916-session-teleportation).

Claude Code has a dedicated feature for each way of running or reaching multiple sessions, and cross-session messaging is the right one only for one of them:

| You want to... | Use this instead |
|---|---|
| Continue one conversation in another terminal, or share its context with a new session | [Resume the session](../ultimate-guide.md#916-session-teleportation) |
| A coordinated team of sessions Claude spawns and supervises itself | [Agent Teams](./agent-teams.md) |
| Watch and steer many sessions from one place | Agent view (background sessions) |
| Steer a session yourself from your phone or another device | [Remote Control](../ultimate-guide.md#922-remote-control-mobile-access) |
| Push external events (CI results, chat messages) into a session | [Channels](./monitor-event-delegation.md#plugin-monitors-and-channels) |
| **Message between independent sessions you start and steer yourself** | **Cross-session messaging** |

This last row is the case the rest of this page covers: sessions with no spawn relationship to each other, each open in its own terminal, each with its own context window, permissions, and working directory.

---

## 2. Discovery: `ListAgents`

Run `/list-agents` (alias `/peers`) in any session to see what Claude can reach. The first row is the session's own name (the one peers use to address it); the rows below list every reachable agent, grouped by kind:

- **Subagents**: agents running inside the current session.
- **Teammates**: this session's own [agent team](./agent-teams.md) teammates. Before v2.1.239 they didn't appear in the listing, even though `SendMessage` could already reach them by name.
- **Your other local sessions**: Claude Code sessions running on the same machine, including background sessions. A session appears only once it binds an inbox socket (see §5); the idle worker process a background-session supervisor keeps ready appears only once you dispatch work to it.
- **Your cloud sessions**: your Claude Code on the web sessions, shown while the current session is connected to Remote Control. Labeled `cloud`.
- **Your Remote Control sessions on other machines**: shown under the same condition, labeled `Remote Control`. A session whose Remote Control connection dropped shows as `offline`.

The current session is never a row in its own listing. If Claude addresses a message to its own name, Claude Code refuses it and tells Claude so, rather than the pre-v2.1.239 behavior of reporting "no agent named …".

A session answers to the name set via `/rename` or `--name`, or an auto-generated one otherwise. When a rename or a new session would collide with a name already in use, Claude Code keeps the name with the session that already has it and assigns the new one a variant. Two sessions can therefore legitimately share a name (an older Claude Code version, or an auto-generated collision); `/list-agents` shows each local session's working directory so you can tell them apart, and when several live sessions share a name Claude asks you which one you mean before sending.

Claude Code reads cloud and Remote Control session lists newest first and stops after a bounded number of pages. A session that falls past that window isn't listed and can't be messaged by name; Claude Code says so, and Claude sees the same note when it tries.

---

## 3. Delivery: `SendMessage`

You can leave the message's wording to Claude:

```text
Ask the session running in my other terminal whether the migration finished
```

```text
Explain what we just did to the session working on the payments API
```

Or name the target yourself with an `@`-mention, the same mechanism used to [address a subagent](../core/tools-reference.md#agent) explicitly. Type `@` followed by the first letters of the session's name and pick it from the typeahead (requires v2.1.232+):

```text
Let @api-worker know the schema migration finished
```

A bare `@` shows no session rows; type at least one more letter to trigger the suggestions. A cloud or Remote Control session only appears in the typeahead after Claude has already listed or messaged your sessions beyond the current machine.

### What the receiving session sees

The message appears in the recipient's conversation under the sender's session name and stays there:

```text
Schema migration finished: the new column is tenant_id, and rebasing on main is safe now.
```

The receiving session gets the sender's name and, except for the one-way cross-machine case (§4), a reply address; it never gets the sender's conversation history or files. Once delivered, the message counts toward usage like a prompt you typed.

### Timing

The receiving Claude reads the message between tool calls during an active turn, so a running tool is never interrupted. When the recipient is idle, Claude Code starts a new turn with the message right away.

### When a send is refused outright

Claude Code refuses to send, before the message leaves the sender, in four cases:

1. The message is over the size cap (§7).
2. A rapid burst to a same-machine session has already reached what that session's inbox accepts.
3. The reply target on this machine fails a safety check: a symlinked socket path, or a connected endpoint that isn't the expected process. See [Refusing to send a cross-session message](https://code.claude.com/docs/en/errors#refusing-to-send-a-cross-session-message).
4. Claude addresses the message to the sending session's own name.

---

## 4. Same-machine vs. cross-machine delivery

Whether a message ever touches Anthropic's infrastructure depends entirely on where the target session runs:

| Where the other session runs | How the message travels |
|---|---|
| On this machine | Over a per-session Unix domain socket (macOS/Linux/WSL2) or named pipe (native Windows). Never through Anthropic servers. |
| On another of your machines | Through Anthropic servers, arriving over that machine's Remote Control connection. |
| On Claude Code on the web | Through Anthropic servers, straight to the cloud session. |

Same-machine delivery is entirely local: each session registers itself in files on disk, and `ListAgents`/`SendMessage` read those files. Two sessions can reach each other only when they can see the same registration files, which is why a container and its host can't message each other (separate filesystems), and why a WSL2 session and a native Windows session on the same computer can't either (different home directories, different socket types).

Starting a conversation with a session on another of your machines requires v2.1.225 or later, and the target must already appear in the listing. Before v2.1.225, a session could only reply to a message that had arrived, never open one.

While the sending session is connected to Remote Control, a message to another of your machines shows up there under the sender's Remote Control name, and the recipient can reply to that name. If the sender isn't connected to Remote Control when it sends beyond the current machine, the message still goes through but carries no reply address: the receiving Claude sees it but can't answer, and the sender is told as much.

To require your explicit approval before any message leaves the machine at all, set `isolatePeerMachines: true` (§6).

---

## 5. The session's inbox socket

Relevant when a session you expect isn't in the listing, when a hook or script needs to post into a session, or when a sandboxed command can't reach the socket.

Claude Code binds an inbox socket for every session with messaging enabled: a Unix domain socket on macOS/Linux/WSL2, a named pipe on native Windows. Its path shows in the `Peer address` row of `/status` (prefixed `uds:`), and is exported to hooks and Bash commands as `CLAUDE_CODE_MESSAGING_SOCKET`. A per-session `CLAUDE_CODE_MESSAGING_TOKEN` is exported alongside it; a script posting to its own session's socket can send `{"type":"auth","token":"<token>"}` as the connection's first line. Native Windows requires that line; macOS/Linux/WSL2 accept a connection with or without it.

The socket is restricted to the operating-system user on macOS/Linux; on Windows, each connection must authenticate with a key only that user can read. Either way, a session started as one OS user can't reach a session started as another, even on the same machine, even in the same tmux server.

`claude -p` sessions bind an inbox like interactive ones. Sessions started in [bare mode](../ultimate-guide.md#headless-mode) don't bind a socket and never appear in the agent list.

---

## 6. Security model

Anthropic's design keeps three properties in tension: sessions coordinate freely, but neither can control the other, and permissions never travel with the message.

### What an incoming message cannot do

When session A messages session B, Claude Code tells B's Claude explicitly that the text came from another session, not from the user, and constrains it accordingly:

- **It can't approve anything.** A message from a peer never counts as your consent; it cannot answer a pending permission prompt on your behalf.
- **It can't change configuration.** The receiving Claude is instructed never to change permission settings, `CLAUDE.md`, or any other configuration because another session asked.
- **Commands don't run.** A command embedded in the message's text, `/compact` for instance, arrives as plain text. Claude Code never executes it.
- **Permission prompts still fire.** If acting on the message needs a permission the receiving session doesn't have, the user sees the same prompt as for any other request.

Claude is also instructed, on the sending side, never to ask another session for an action its own session already denied, blocked, or would block under its own permission rules; that work routes back to the user instead.

### Controlling what arrives: `crossSessionInbound`

Each session decides what to do with inbound peer messages via the `crossSessionInbound` setting:

| Value | Behavior |
|---|---|
| `accept` | Claude Code delivers every message to Claude. |
| `hold` | Claude Code shows a notice for each message without delivering it. **Approve** delivers that one message; **Deny** or dismissing drops it. Unanswered past the `dialogExpiry` deadline (5 minutes by default), Claude Code closes the dialog and drops the message. |
| `refuse` | Claude Code drops every message without delivering it. |

Editable via `/config` → **Messages from your other sessions** (v2.1.232+; hidden when managed settings or `--settings` already sets the key). When no value applies from any settings scope, Claude Code decides per message from both sessions' permission-mode class: sessions that bypass permission prompts form one class, every other session (including plan mode where bypass is available, and `auto`/`acceptEdits`/`dontAsk`, which count as prompting) forms the other. A prompting recipient delivers by default and only holds a message from a bypassing sender; a bypassing recipient holds by default and only delivers from another bypassing sender.

Claude Code holds at most 100 messages, separately from the delivery queue, dropping the oldest past that.

### Locking it down further

`isolatePeerMachines: true` forces your explicit approval before any `SendMessage` reaches a session beyond the current machine, even in `bypassPermissions` mode. It never prompts for same-machine sends. A `true` set anywhere (including a checked-in project file) applies; there's no way to override it back to `false` from a weaker scope.

To turn a direction off entirely: `crossSessionInbound: "refuse"` stops receiving, and a permission deny rule naming `SendMessage` and `ListAgents` (bare tool names, no specifier) stops sending and listing. Denying `SendMessage` also removes messaging to subagents and agent-team teammates, since they share the tool. An organization-wide lockdown in managed settings combines both:

```json
{
  "permissions": {
    "deny": ["SendMessage", "ListAgents"]
  },
  "crossSessionInbound": "refuse"
}
```

With this in place the session still binds its inbox socket, but drops everything that arrives on it. Nothing in `/status` or in a peer's `/list-agents` reveals that a session is locked down this way; confirm it by reading the settings that apply, not by observing behavior.

### Endpoint spoofing checks

Before delivering to a same-machine target, `SendMessage` verifies the endpoint is what it claims to be, and refuses rather than sends when it isn't: a symlinked reply target, an endpoint that connects but isn't the expected process, or an endpoint whose identity can't be read all produce a refusal instead of a silent send to the wrong place. See [Refusing to send a cross-session message](https://code.claude.com/docs/en/errors#refusing-to-send-a-cross-session-message).

---

## 7. Limitations

These are properties of the channel itself, independent of platform or provider (§8 covers those separately):

- **Plain text only.** Structured agent-team protocol messages stay inside a team; cross-session messages carry text alone.
- **Same-machine size cap around 1,048,576 characters.** Over that, `SendMessage` refuses the send before it leaves; nothing reaches the recipient. Put bulk content in a file and send its path instead, summarize, or split across several messages.
- **Rapid bursts to one session are refused at the sender.** Once a burst to a same-machine session reaches what that session's inbox accepts, further sends are refused at the sending session, which is told to batch what's left into one message or wait. Before v2.1.236, a burst that exceeded this was reported as sent while the receiving session silently dropped it.
- **Message loops are throttled at the recipient.** Claude Code rate-limits repeated messages per sender, drops identical repeats arriving in a short window, and queues at most 50 accepted messages for Claude to read, which stops a message loop between two sessions on its own.

---

## 8. Availability

| Requirement | Value |
|---|---|
| macOS / Linux / WSL2 | v2.1.224+ |
| Native Windows | v2.1.234+ |
| `@`-mention targeting, `/config` row | v2.1.232+ |
| Starting a conversation with another machine | v2.1.225+ |
| `notify_when_idle` (§9) | v2.1.236+ |
| Teammates appear in `/list-agents`; own-name self-messaging fixed | v2.1.239+ |
| Provider | Not available on Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, or Microsoft Foundry |
| Kill switch | Any of `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `DISABLE_TELEMETRY`, `DO_NOT_TRACK`, `DISABLE_GROWTHBOOK` turning off feature-flag evaluation keeps messaging off |

When a session meets the version, platform, and provider requirements, messaging is on with nothing to enable.

To check a session: `/list-agents` not recognized at all means the session lacks the feature (start with `claude --version`). `/list-agents` working but a send not arriving usually means one of: a deny rule on `SendMessage`/`ListAgents`, the receiving session's inbound controls holding or dropping it, a cloud or other-machine session that isn't currently connected via Remote Control, or a session that fell past the bounded listing window.

---

## 9. Get a notice when another session goes idle (v2.1.236+)

Instead of polling, ask Claude to subscribe to one notice from a same-machine session:

```text
Tell me when the migration session finishes what it's working on
```

Claude subscribes via `SendMessage`'s `notify_when_idle` input, either attached to a message it's already sending or on its own (which costs nothing in the watched session and fires immediately if that session is already idle). The notice is one-shot and neither session polls the other; if none arrives within 12 hours, the subscription is dropped and Claude is told so it stops waiting. Only the main conversation can subscribe, and only to sessions on the current machine; a subagent, teammate, or a session beyond the current machine that tries gets refused outright, message included.

---

## 10. Version timeline

| Version | What changed |
|---|---|
| v2.1.224 | Cross-session messaging introduced on macOS, Linux, WSL2. `ListAgents`/`SendMessage`, inbox sockets, `crossSessionInbound` setting. |
| v2.1.225 | Starting a conversation with a session on another machine (previously reply-only in that direction). |
| v2.1.232 | `@`-mention targeting syntax. `/config` row for `crossSessionInbound`. |
| v2.1.234 | Native Windows support, named-pipe inbox. |
| v2.1.236 | `notify_when_idle`. Burst-refusal fix: previously over-limit sends reported as sent while silently dropped. |
| v2.1.239 | Agent-team teammates appear in `/list-agents` (could already be messaged by name before). Own session name shown and self-messages handled correctly. |

---

## 11. Practical patterns

**Hand over a finding.** A session that discovers a breaking change or makes a decision has Claude summarize it for the session working on the affected area, instead of the human re-explaining it there.

**Coordinate parallel worktrees.** Sessions working the same repository in separate [worktrees](../ultimate-guide.md#912-git-best-practices--workflows) get told what landed in a sibling worktree, without a human relaying it.

**Division of labor across roles.** One session on database migrations, one on backend, one on frontend, one on documentation, each running in its own terminal. When the migration finishes, that session messages the backend session so it can proceed without polling; when the docs session resolves a question blocking the frontend, the answer crosses the same way.

**Cross-device continuation.** A long build running in a desktop terminal messages a summary to a documentation session reached from a phone via Remote Control, once the build finishes.

None of these need `TeamCreate`. Reach for [Agent Teams](./agent-teams.md) instead when you want a lead session to spawn and supervise teammates itself, with structured task assignment; reach for cross-session messaging when the sessions already exist independently and you're just cutting the human out of the relay.
