# Desktop agent workspaces: selective cockpit evaluation

**Reviewed:** October 17, 2026. **Decision:** refresh Conductor and Vibe Kanban; add short comparative mentions of Emdash, Superset, and Escouade. Keep Opcode in this evaluation without another guide profile.

Scores measure editorial value for this guide, not product reliability, security, or expected productivity. The review used official documentation, pinned repository READMEs and licences, and a targeted Escouade helper probe. No desktop application, provider account, remote integration, paid service, or complete upstream test suite was exercised in this refresh.

## Existing coverage and duplicate control

| Subject | Existing canonical coverage | Treatment |
|---|---|---|
| Conductor | [Community tools](../../guide/ecosystem/third-party-tools.md#conductor) | Replace the dated two-agent/local-only description with the documented four agents and local/cloud workflow; remove unsupported productivity and comparative-polish claims |
| Vibe Kanban | [Harness landscape](../../guide/ecosystem/agent-harness-landscape.md#vibe-kanban-maintenance-status), generated control-plane and catalog rows | Add a dated maintenance note; preserve the provenance and date of the historical generated snapshot |
| Nimbalyst | [Agentic tools §4.7](../../guide/ecosystem/agentic-tools.md#47-nimbalyst) | Link to its existing visual editing profile |
| Claudio | [Multi-session landscape evaluation](./082-multi-session-management-landscape.md) | Preserve existing coverage; do not present its historical recommendation as a current comparative ranking |
| Session, cost, and configuration tooling | [Session management](../../guide/ecosystem/third-party-tools.md#session-management), [cost tracking](../../guide/ecosystem/third-party-tools.md#token--cost-tracking), [configuration management](../../guide/ecosystem/third-party-tools.md#configuration-management) | Use these overlaps when deciding whether Opcode needs another profile |

The three additions share one [desktop workspace comparison](../../guide/ecosystem/third-party-tools.md#desktop-agent-workspace-comparison). The AI ecosystem and harness landscape link to it. No additional runtime entry, separate product guide, or duplicate feature inventory was created. A workspace coordinator can be useful while delegating the model/tool loop to Claude Code or another agent runtime.

## Candidate decisions

| Candidate | Initial score | Final score after technical challenge | Distinct contribution | Decision |
|---|---|---|---|---|
| Emdash | 3/5 | 3/5 | Existing agent CLIs on local projects or the user's SSH/SFTP machines; lifecycle-hook configuration boundary | Add one comparative row |
| Superset | 3/5 | 3/5 | Worktree-specific browser previews, UI-element context, and PR-line feedback to agent sessions | Add one comparative row |
| Escouade | 3/5 | 3/5 | FR/EN workflow, dependent tickets with acceptance criteria and retries, MCP operation of agents/tickets | Add one row with permission and file-copy caveats |
| Opcode | 2/5 | 2/5 | Consolidates existing session, cost, MCP, instruction, and checkpoint functions | Retain evaluation; no extra profile |

### Emdash

The [pinned README](https://github.com/generalaction/emdash/blob/761520624f1cafa740f5c88ddaf083b4fde2cc59/README.md) documents a desktop app for macOS, Windows, and Linux, using installed coding-agent CLIs and a worktree per task. Its local/SSH workflow is a useful selection criterion for readers who already operate their own remote machine. It is licensed under [Apache-2.0](https://github.com/generalaction/emdash/blob/761520624f1cafa740f5c88ddaf083b4fde2cc59/LICENSE.md).

Adoption has a configuration effect: for agents with lifecycle-hook support, Emdash installs marker-tagged hooks in user-level configuration for status, notifications, and resumable sessions. The README says they do nothing outside Emdash sessions; this review did not test that behavior or compatibility with existing hooks. Agent CLIs may send prompts, code, and context to their providers even though Emdash documents local SQLite storage and optional telemetry.

The score stays at 3/5 because this is a useful workflow distinction, with no measured advantage over existing profiles. Avoid claiming unique SSH support across the entire market.

### Superset

The [pinned README](https://github.com/superset-sh/superset/blob/e547103d8570a39327c051b80144e45c59203052/README.md) describes worktrees with terminals, diff review, per-workspace port detection and browser previews. Design mode sends selected UI-element context to an agent. PR diff-line feedback can go to a running or new agent session; posting that feedback to GitHub is optional. These mechanisms supply a concrete UI-development example beyond another parallel-terminal list.

The same source describes remote access, cloud workspaces, mobile Pro, scheduling, CLI, SDK, and MCP surfaces. The integration therefore does not call the whole product local-only or free. macOS is the primary target, Linux AppImage support is experimental, and Windows is not available in this snapshot.

The current [licence is Elastic License 2.0](https://github.com/superset-sh/superset/blob/e547103d8570a39327c051b80144e45c59203052/LICENSE.md). The guide uses **source-available** rather than a generic open-source label. Its terms restrict hosted/managed provision of substantial functionality and interference with licence-key functionality; consult the licence for any redistribution or service offering.

The score stays at 3/5: integrate the browser/review mechanism, not an exhaustive second product profile or a usability ranking.

### Escouade

The [pinned README](https://github.com/guillaume-gagnaire/escouade/blob/b74b6526b3ba94df049a9a8ad1466e37706fe175/README.md) documents Windows, macOS, and Linux, a French/English interface, a Svelte 5 frontend, a Tauri 2/Rust backend, and Claude Code processes using `stream-json`. Other agent engines are an architectural direction, not established current support.

Its contribution is the ticket workflow: acceptance criteria, dependencies, worktrees, repeated agent attempts, and configurable test/delivery actions. An MCP server exposes operation of the workspace to agents. This is a workflow-control layer; a report that criteria are met is not independent acceptance evidence. The current MCP description includes ticket validation, test/merge actions, ticket deletion, and permission responses. Human approval is therefore not an unconditional invariant of every path.

The licence is [GPL-3.0-or-later](https://github.com/guillaume-gagnaire/escouade/blob/b74b6526b3ba94df049a9a8ad1466e37706fe175/README.md#licence); the README explicitly preserves MIT licensing for versions through 1.7.7. An older MIT snapshot must not determine the licence label for the current project.

**File-copy limitation verified on the current helper:** [`copy_one`](https://github.com/guillaume-gagnaire/escouade/blob/b74b6526b3ba94df049a9a8ad1466e37706fe175/src-tauri/src/testlaunch.rs#L126) creates destination parents and calls `std::fs::copy` without rejecting a destination symlink. A standalone Rust probe using that exact function and dummy files reproduced an overwrite outside the worktree. The calling `copy_worktree_files` function copies ignored files matching configured patterns such as `.env*`.

To reproduce the narrow result on Unix in a temporary directory:

1. Create `project/`, `worktree/`, and an `outside-sentinel` containing dummy text.
2. Put different dummy text in `project/dummy.env`.
3. Make `worktree/dummy.env` a symlink to the sentinel outside `worktree/`.
4. Compile the pinned `copy_one` function unchanged in a standalone Rust program and call it with those two directory paths and `dummy.env`.
5. Observe that the outside sentinel now contains the source text, then remove the temporary directory.

This verifies the helper's destination-link behavior, not an end-to-end exploit, Windows junction behavior, or every application entry path. No real secret or repository was used. Earlier test counts from a different Escouade revision were not carried forward as current evidence.

Keep the editorial score at 3/5 because the ticket/MCP mechanisms add explanatory value. Use a disposable repository and dummy configuration for a trial, with automatic secret copying disabled; verify tests and delivery permissions before applying it to important work. The mention is not a security recommendation.

### Opcode

The [pinned README](https://github.com/winfunc/opcode/blob/d1ca30a3c0c39fff01fde2f86c2d5af6a1db658b/README.md) describes a Tauri 2 GUI for Claude Code project/session history, custom background agents, usage analytics, MCP configuration, checkpoints, and instruction editing. Its [licence](https://github.com/winfunc/opcode/blob/d1ca30a3c0c39fff01fde2f86c2d5af6a1db658b/LICENSE) is AGPL-3.0.

Consolidating these operations can be useful. It does not establish a distinct ticket-to-worktree-to-review mechanism in the consulted material, and the guide already covers the underlying session, cost, and configuration jobs. The README also mixes future binary-release wording with installation links under a different repository owner. This review did not resolve every distribution path and does not infer abandonment from that inconsistency.

Score: 2/5. Keep this traceable evaluation and qualify the previous absolute “no unified admin panel” gap, without adding another full GUI profile or installation instructions.

## Maintenance corrections

**Conductor:** official [introduction](https://www.conductor.build/docs), [cloud documentation](https://www.conductor.build/docs/cloud), [diff viewer](https://www.conductor.build/docs/reference/diff-viewer), and [Checks documentation](https://www.conductor.build/docs/reference/checks) support the refreshed profile. The product documents Claude Code, Codex, Cursor, and OpenCode, with a macOS client and cloud Linux execution. Local worktrees are development separation, not a security boundary; cloud-to-local access can be explicitly enabled. See [security and permissions](https://www.conductor.build/docs/reference/security-and-permissions). The neighboring AO comparison no longer says Conductor supports only two agents or claims better polish without evidence.

**Vibe Kanban:** the official [April 10 shutdown announcement](https://www.vibekanban.com/blog/shutdown) distinguishes Bloop's closure from the intended open-source/community continuation. It planned removal of remote services after 30 days and said local workspaces would continue. This is not a current service probe or proof of active community maintenance. The guide keeps the generated historical catalog intact and puts the dated lifecycle note beside its control-plane entry; no upstream snapshot or global freshness date was rewritten.

**Windows:** Piebald's “only native Windows GUI” claim was removed because Emdash and Escouade document Windows builds. No replacement claim of exclusivity was introduced.

## Independent technical challenge

A separate technical-writer agent reviewed the candidate decisions and primary sources without editing the guide. It retained the 3/3/3/2 scores and challenged the initial framing on four points: Superset's restrictive licence and hybrid surfaces; Escouade's current GPL licence and MCP authority; Conductor's changed agent/cloud support and stale adjacent comparisons; and the difference between Vibe Kanban's shutdown plan and observed service state. Those corrections are reflected above. The current Escouade helper probe was performed after that review; it is reported separately from the agent's documentary challenge.

## What a trial would need to establish

Use the same small repository and bounded task for any shortlisted tool. Record whether the user can locate the working branch, agent awaiting input, changed files, actual test command/result, and next delivery action. Include interruption/resume and a conflicting-change case. For SSH/cloud, inspect where code, credentials, hooks, and processes live. Compare those observations with the current workflow before asserting a benefit. No such comparative application trial was run for this evaluation.
