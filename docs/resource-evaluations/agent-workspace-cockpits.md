# Desktop agent workspaces: selective cockpit evaluation

**Reviewed:** October 17, 2026; Escouade runtime follow-up on October 22, 2026; Orca documentation follow-up on October 27, 2026. **Decision:** refresh Conductor and Vibe Kanban; add short comparative mentions of Emdash, Superset, Escouade, and Orca. Keep Opcode in this evaluation without another guide profile. Escouade's editorial score remains 3/5 after the trial.

Scores measure editorial value for this guide, not product reliability, security, or expected productivity. The October 17 review used official documentation, pinned repository READMEs and licences, and a targeted Escouade helper probe. The October 22 follow-up ran Escouade 1.8.8 locally with Claude Code and an existing Claude Max subscription. Other desktop applications, other providers, remote integrations, and the complete upstream test suites were not exercised.

## Existing coverage and duplicate control

| Subject | Existing canonical coverage | Treatment |
|---|---|---|
| Conductor | [Community tools](../../guide/ecosystem/third-party-tools.md#conductor) | Replace the dated two-agent/local-only description with the documented four agents and local/cloud workflow; remove unsupported productivity and comparative-polish claims |
| Vibe Kanban | [Harness landscape](../../guide/ecosystem/agent-harness-landscape.md#vibe-kanban-maintenance-status), generated control-plane and catalog rows | Add a dated maintenance note; preserve the provenance and date of the historical generated snapshot |
| Nimbalyst | [Agentic tools §4.7](../../guide/ecosystem/agentic-tools.md#47-nimbalyst) | Link to its existing visual editing profile |
| Claudio | [Multi-session landscape evaluation](./082-multi-session-management-landscape.md) | Preserve existing coverage; do not present its historical recommendation as a current comparative ranking |
| Session, cost, and configuration tooling | [Session management](../../guide/ecosystem/third-party-tools.md#session-management), [cost tracking](../../guide/ecosystem/third-party-tools.md#token--cost-tracking), [configuration management](../../guide/ecosystem/third-party-tools.md#configuration-management) | Use these overlaps when deciding whether Opcode needs another profile |

The additions share one [desktop workspace comparison](../../guide/ecosystem/third-party-tools.md#desktop-agent-workspace-comparison). The AI ecosystem and harness landscape link to it. No additional runtime entry, separate product guide, or duplicate feature inventory was created. A workspace coordinator can be useful while delegating the model/tool loop to Claude Code or another agent runtime.

## Candidate decisions

| Candidate | Initial score | Final score after technical challenge | Distinct contribution | Decision |
|---|---|---|---|---|
| Emdash | 3/5 | 3/5 | Existing agent CLIs on local projects or the user's SSH/SFTP machines; lifecycle-hook configuration boundary | Add one comparative row |
| Superset | 3/5 | 3/5 | Worktree-specific browser previews, UI-element context, and PR-line feedback to agent sessions | Add one comparative row |
| Escouade | 3/5 | 3/5 | FR/EN ticket workflow; local trial verified worktrees, dependency scheduling, restart/resume, and test-gated delivery through MCP | Retain one row; document the bounded trial and its limits without a productivity ranking |
| Opcode | 2/5 | 2/5 | Consolidates existing session, cost, MCP, instruction, and checkpoint functions | Retain evaluation; no extra profile |
| Orca (Stably, October 27 addition) | 3/5 | 3/5 | Codex workspace integration, hosted reviews and CI feedback, with documented session-sharing and permission defaults | Add one comparative row and the adoption boundaries below; no runtime claim |

### Orca

**Documentation review: October 27, 2026. No application trial.** This evaluation concerns [stablyai/orca](https://github.com/stablyai/orca), the MIT-licensed desktop environment, not other repositories named Orca. It hosts existing agent CLIs in worktrees, with diff annotations, browser element context, SSH execution, and a mobile companion. These overlap with the existing workspace profiles; they do not justify a second feature catalog.

The useful comparison is a concrete delivery loop. Orca's [hosted review documentation](https://www.onorca.dev/docs/review/github) links worktrees to PRs/MRs and exposes checks and review threads. For a failing GitHub PR, **Fix broken checks** passes failed check names and links to an agent. That documents a feedback action, not proof of unattended repair, correct commit attribution, or successful CI. GitLab review support is documented too; this evaluation exercised neither provider.

Two defaults affect adoption with an existing Codex desktop workflow:

- [Codex integration](https://www.onorca.dev/docs/agents/codex) documents a separate background server per Codex terminal on Codex 0.157 and later. Shared-server features and sessions opened through the Codex desktop app or an IDE do not see those Orca sessions by default. The per-terminal-server setting can be disabled before opening new terminals. A handoff to another agent starts a fresh session with bounded prior context; it is not a native resume. Cross-application continuity remains untested here.
- [Agent permissions](https://www.onorca.dev/docs/agents/supported) prefill permission-bypass arguments for new terminal launches, including bypassing both approvals and sandbox for Codex. The terminal **Agent Permissions** setting supports Manual mode; native chats have a separate default applied to new chats, and custom agent arguments remain overrides. Inspect the effective launch settings before a trial. Worktree separation is not process confinement.

The [pinned orchestration documentation](https://github.com/stablyai/orca/blob/3ddaa8df6f61e77ef095fba03532b2a13b3b2fdf/docs/site/content/docs/cli/orchestration.mdx), checked on October 27, labels its tasks, dependencies, supervised workers, messages, and decision gates experimental. A durable Run is described as a coordination namespace, not an automatic scheduler by itself.

**Editorial score: 3/5.** Integrate the review-feedback mechanism and Codex adoption boundaries in the shared comparison. Test Orca when a unified daily workspace is the problem; compare AO when project-level PR/CI/review coordination is the problem. Both overlap, so this is a test-selection hypothesis, not a product ranking. Escouade's local dependency/test-gate trial does not establish either alternative's behavior. No measured productivity, security, usability, or reliability advantage is claimed.

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

The [1.8.8 README](https://github.com/guillaume-gagnaire/escouade/blob/9383ada96cf91190fc719a1fcac7ac72ab00c7c4/README.md) documents Windows, macOS, and Linux, a French/English interface, a Svelte 5 frontend, a Tauri 2/Rust backend, and support for Claude Code, Codex, OpenCode, and GitHub Copilot CLI. The trial below exercised only Claude Code, whose processes use `stream-json`; it does not verify the other adapters or cross-provider handover.

Its contribution is the ticket workflow: acceptance criteria, dependencies, worktrees, repeated agent attempts, and configurable test/delivery actions. An MCP server exposes operation of the workspace to agents. This is a workflow-control layer; a report that criteria are met is not independent acceptance evidence. The current MCP description includes ticket validation, test/merge actions, ticket deletion, and permission responses. Human approval is therefore not an unconditional invariant of every path.

The licence is [GPL-3.0-or-later](https://github.com/guillaume-gagnaire/escouade/blob/9383ada96cf91190fc719a1fcac7ac72ab00c7c4/README.md#licence); the README explicitly preserves MIT licensing for versions through 1.7.7. An older MIT snapshot must not determine the licence label for the current project.

#### Escouade runtime trial: October 22, 2026

**Scope and method.** Escouade [1.8.8](https://github.com/guillaume-gagnaire/escouade/releases/tag/v1.8.8) was compiled from the unmodified release source and launched on Apple Silicon macOS in development mode. The evaluator operated the desktop application's official MCP server, whose ticket operations call the same core functions as the UI. This tested the application workflow, not mouse navigation or visual usability. A disposable Git repository, separate application data, disabled automatic file copying, and an explicit pre-merge test command bounded the trial. No remote publication took place.

The task was a small documentation checker using Python's standard library and synthetic Markdown documents. Two Claude Sonnet agents worked in parallel: one extracted headings outside fenced code, the other checked relative file links. A third ticket depended on both and assembled a JSON CLI. Each ticket owned separate implementation and test files. The final branch passed **19 pilot-project tests** (18 written by the agents and one initial fixture check), plus **3 evaluator-authored acceptance tests** created before the agents ran. These are not Escouade's upstream test-suite counts or an independent product audit. The acceptance tests checked heading lines, fenced-code exclusion, encoded paths and fragments, JSON output, and exit codes for valid and broken links.

| Behavior exercised | Observed result |
|---|---|
| Dependency enforcement | Starting the integration ticket before its prerequisites finished was refused, with both dependencies named |
| Parallel work | Two agents ran in separate automatically created worktrees and branches |
| Interruption and restart | After interrupting both agents and restarting the application, the tickets, branches, and resumable sessions remained available |
| Permission handling | Command requests appeared in the shared MCP request list and received one-time approvals |
| Negative test gate | An evaluator-injected failing test prevented the first merge; the target branch remained unchanged. Escouade returned the ticket to the agent for correction even with autopilot off |
| Delivery and scheduling | After the evaluator removed the deliberate failure and reviewed the results, tests and merges completed. With autopilot enabled, the integration ticket then started automatically from a base containing both prerequisites |
| Final state | All three tickets were done and merged locally, with no agents or permission requests listed; autopilot was switched off |

The resulting CLI reported the deliberately missing file, ignored a link inside fenced code, and returned the expected exit codes. This was a limited prototype for exercising orchestration, not a replacement for the guide's existing documentation checks.

**Limits encountered.** One ticket stopped with “Bilan des critères manquant” despite an agent-supplied report. A JSON string contained three backticks: [`last_block`](https://github.com/guillaume-gagnaire/escouade/blob/9383ada96cf91190fc719a1fcac7ac72ab00c7c4/src-tauri/src/board.rs#L137-L143) ends the report at their first occurrence, including inside a string. Reissuing the report without those characters unblocked review. This is an observed reporting failure, not a failed implementation test.

- **Tests need explicit configuration.** [`BoardSettings::default`](https://github.com/guillaume-gagnaire/escouade/blob/9383ada96cf91190fc719a1fcac7ac72ab00c7c4/src-tauri/src/model.rs#L924-L946) disables tests before delivery and supplies no test command. Both were configured for the trial; an agent's checked criteria alone do not provide this gate.
- **File summaries need a Git cross-check.** The MCP agent summary returned `touchedFiles: []` while Git showed new files written through Bash. The desktop Git pane was not evaluated, so this observation applies to that summary only.
- **Distribution verification failed on the test machine.** `codesign --verify --deep --strict` reported an invalid arm64 signature for the applications extracted from both official macOS downloads, tar.gz and DMG. Building the release source, with CMake added to a temporary build environment, allowed the trial to proceed. The signature failure's cause and behavior on other machines were not established.
- **The evaluator's launch setup required correction.** A custom launcher initially loaded personal hooks. Both agents were interrupted before editing project files; the launcher was corrected and its effective process options checked before resuming. This setup error is not an Escouade defect, and the isolated MCP/account setup is not representative of ordinary installation effort.

**Adoption judgment.** The verified contribution is a persistent workflow linking tickets, worktrees, review, and delivery, with enforced dependencies. In the evaluator's current Codex workflow, those steps are coordinated through conversations and explicit Git operations. That makes Escouade a candidate for a queue of separable tasks followed by integration. This small prototype could also have been completed in one session: the trial does not establish that this decomposition, or switching tools for a single change, is worthwhile.

There was no equivalent Codex A/B run, measured time or cost advantage, deliberate merge-conflict exercise, provider switch, quota-exhaustion scenario, or OS-confinement test. Runtime records and the pilot repository were retained locally but are not published with this evaluation; the observations above are an evaluator report, not a publicly reproducible benchmark. Public source permalinks support the parser and default-setting findings, not the execution results.

**Earlier file-copy finding, not retested on 1.8.8:** the October 17 probe of the [pinned `copy_one` helper](https://github.com/guillaume-gagnaire/escouade/blob/b74b6526b3ba94df049a9a8ad1466e37706fe175/src-tauri/src/testlaunch.rs#L126) found that it creates destination parents and calls `std::fs::copy` without rejecting a destination symlink. A standalone Rust probe using that exact function and dummy files reproduced an overwrite outside the worktree. The calling `copy_worktree_files` function copies ignored files matching configured patterns such as `.env*`. Automatic copying was disabled in the October 22 runtime trial, so that trial neither revalidates this finding nor demonstrates a fix.

To reproduce the narrow result on Unix in a temporary directory:

1. Create `project/`, `worktree/`, and an `outside-sentinel` containing dummy text.
2. Put different dummy text in `project/dummy.env`.
3. Make `worktree/dummy.env` a symlink to the sentinel outside `worktree/`.
4. Compile the pinned `copy_one` function unchanged in a standalone Rust program and call it with those two directory paths and `dummy.env`.
5. Observe that the outside sentinel now contains the source text, then remove the temporary directory.

This verifies the helper's destination-link behavior, not an end-to-end exploit, Windows junction behavior, or every application entry path. No real secret or repository was used. Earlier test counts from a different Escouade revision were not carried forward as current evidence.

Keep the editorial score at 3/5: the bounded runtime trial confirms useful ticket/MCP behavior but provides no comparative productivity or security evidence. Use a disposable repository and dummy configuration for a trial, with automatic secret copying disabled; verify tests and delivery permissions before applying it to important work. The mention is not a security recommendation.

### Opcode

The [pinned README](https://github.com/winfunc/opcode/blob/d1ca30a3c0c39fff01fde2f86c2d5af6a1db658b/README.md) describes a Tauri 2 GUI for Claude Code project/session history, custom background agents, usage analytics, MCP configuration, checkpoints, and instruction editing. Its [licence](https://github.com/winfunc/opcode/blob/d1ca30a3c0c39fff01fde2f86c2d5af6a1db658b/LICENSE) is AGPL-3.0.

Consolidating these operations can be useful. It does not establish a distinct ticket-to-worktree-to-review mechanism in the consulted material, and the guide already covers the underlying session, cost, and configuration jobs. The README also mixes future binary-release wording with installation links under a different repository owner. This review did not resolve every distribution path and does not infer abandonment from that inconsistency.

Score: 2/5. Keep this traceable evaluation and qualify the previous absolute “no unified admin panel” gap, without adding another full GUI profile or installation instructions.

## Maintenance corrections

**Conductor:** official [introduction](https://www.conductor.build/docs), [cloud documentation](https://www.conductor.build/docs/cloud), [diff viewer](https://www.conductor.build/docs/reference/diff-viewer), and [Checks documentation](https://www.conductor.build/docs/reference/checks) support the refreshed profile. The product documents Claude Code, Codex, Cursor, and OpenCode, with a macOS client and cloud Linux execution. Local worktrees are development separation, not a security boundary; cloud-to-local access can be explicitly enabled. See [security and permissions](https://www.conductor.build/docs/reference/security-and-permissions). The neighboring AO comparison no longer says Conductor supports only two agents or claims better polish without evidence.

**Vibe Kanban:** the official [April 10 shutdown announcement](https://www.vibekanban.com/blog/shutdown) distinguishes Bloop's closure from the intended open-source/community continuation. It planned removal of remote services after 30 days and said local workspaces would continue. This is not a current service probe or proof of active community maintenance. The guide keeps the generated historical catalog intact and puts the dated lifecycle note beside its control-plane entry; no upstream snapshot or global freshness date was rewritten.

**Windows:** Piebald's “only native Windows GUI” claim was removed because Emdash and Escouade document Windows builds. No replacement claim of exclusivity was introduced.

## Independent technical challenge

A separate technical-writer agent reviewed the October 17 candidate decisions and primary sources without editing the guide. It retained the 3/3/3/2 scores and challenged the initial framing on four points: Superset's restrictive licence and hybrid surfaces; Escouade's current GPL licence and MCP authority; Conductor's changed agent/cloud support and stale adjacent comparisons; and the difference between Vibe Kanban's shutdown plan and observed service state. Those corrections are reflected above. The October 17 Escouade helper probe was performed after that review; it is reported separately from the agent's documentary challenge.

For the October 22 follow-up, a separate technical-writer agent checked the revision against retained trial records and pinned source. It retained Escouade's 3/5 score and requested clearer test authorship, the enabled-autopilot condition for scheduling, and narrower wording about the retained records. Those clarifications are incorporated above. This was an evidence review, not an independent rerun of the application trial.

On October 27, a separate technical-writer agent checked the Orca additions against the linked official documentation. It retained 3/5, confirmed the terminal/chat permission distinction and Codex session-sharing limitation, and requested explicit score attribution in the evaluation index. This was a documentary challenge, not an Orca runtime test.

## What further comparative trials need to establish

Use the same small repository and bounded task for any shortlisted tool. Record whether the user can locate the working branch, agent awaiting input, changed files, actual test command/result, and next delivery action. Include interruption/resume and a conflicting-change case. For SSH/cloud, inspect where code, credentials, hooks, and processes live. The Escouade follow-up exercised part of this protocol through MCP, including interruption/resume, but did not compare equivalent runs or evaluate visual usability and conflicts. Those gaps remain before asserting a comparative benefit.
