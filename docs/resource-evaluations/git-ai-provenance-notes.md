# git-ai: line-level AI attribution in git notes, tested across rewrites

**Reviewed**: 2026-11-08. **Score**: 4/5, integrated in [AI Traceability §3.4 and §3.5](../../guide/ops/ai-traceability.md#35-provenance-in-git-notes) and as a diagram in [Enterprise Governance](../../guide/diagrams/12-enterprise-governance.md#ai-attribution-through-history-rewrites). Related: [agent provenance traces](agent-provenance-traces.md), [Entire CLI](entire-cli.md).

[git-ai](https://github.com/git-ai-project/git-ai/tree/5420ab9081d2cd57ffdafced09a8028d6dabf4bd) records which lines an agent wrote, stores that attribution in git notes under `refs/notes/ai`, and moves it when history is rewritten. This evaluation built version 1.7.7 from source at `5420ab9` (2026-11-05) and ran a rewrite test. Of the provenance tools evaluated this cycle, it is the only one that was run.

## Sources

| Source | Contribution | Limit |
|---|---|---|
| [Repository at `5420ab9`](https://github.com/git-ai-project/git-ai/tree/5420ab9081d2cd57ffdafced09a8028d6dabf4bd), README and `src/` read 2026-11-08 | Command set, `checkpoint` usage, daemon design, sandbox guard, rewrite support table | Project documentation; only the paths below were executed |
| Rewrite test, run 2026-11-08, and a plain git notes test with git 2.56.0 (scripts and logs kept with this evaluation's working notes) | Note content and `git-ai blame` before and after amend, rebase and `git merge --squash` | One file, the `mock_ai` test preset, local repository, git 2.56.0, macOS |
| [Aidan Cunniffe, "Tracking AI generated code with Git"](https://www.youtube.com/watch?v=irK4G2SzhpA), DevCon Fall 2025, 2025-11-27 | Author's demo and claims | The speaker is the tool's author |

## How it works, from the code and README

- Agents call `git-ai checkpoint <preset> [--hook-input <json|stdin>] [files...]` when they write files; presets include `claude`, `codex`, `cursor` and a `mock_ai` test preset (`src/commands/git_ai_handlers.rs`). There are no `--tool` or `--session` flags.
- On commit, line-level attribution goes into a note on `refs/notes/ai` (schema `authorship/3.0.0`): per file, line ranges mapped to a session, and per session the tool, an id and the model.
- Rewrites are followed by a background daemon that reads git's trace2 events through `trace2.eventTarget`, not by git hooks or a git wrapper. The README: "Git AI analyzes the final state of the code after the operation completes and copies/merges the attributions into a Git Note for any updated commits. The entire system is eventually consistent".
- `git-ai install-hooks` installs agent hooks and sets the global trace2 target; it can also install editor extensions (`code --install-extension` in `src/mdm/utils.rs`). `git-ai stats [commit]` shows statistics for one commit.
- The daemon refuses to start inside agent sandboxes (`src/sandbox.rs`: `CURSOR_SANDBOX`, `SANDBOX_RUNTIME`, `CODEX_SANDBOX`).

## Rewrite test

Setup: isolated `HOME` and global git config, `trace2.eventTarget` set by hand to the daemon socket (`install-hooks` was not run because it would also touch real editors), daemon started with `git-ai bg start`, two AI lines written and checkpointed with `mock_ai`, then a third.

| Step | HEAD after the step | Note on HEAD | `git-ai blame ai.txt` |
|---|---|---|---|
| 1. AI commit (2 lines) | `cf0f5d1` | session `s_0527…` lines 1-2 | lines 1-2 `mock_ai` |
| 2. `git commit --amend`, third AI line checkpointed | `c234f08` | session `s_0527…` lines 1-2, session `s_74c7…` line 3 | lines 1-3 `mock_ai` |
| 3. `git rebase main` onto a new main commit | `7b8655a` | same two sessions and ranges | lines 1-3 `mock_ai` |
| 4. `git merge --squash feature` then commit on main | `3dbe89d` | same two sessions and ranges | lines 1-3 `mock_ai` |

Each rewrite produced a new SHA, and the note followed it, keeping the earlier ranges (step 2 added the checkpointed line 3). The author's integration tests for amend, rebase and squash (`cargo test --test integration -- amend:: rebase:: squash_merge:: ci_squash_rebase::`) could not start their daemon inside the Claude Code sandbox; every failure reported that guard, so it says nothing about attribution.

**Not covered by the test**: cherry-pick, stash, reset; several files and partial staging; real agent presets; pushing and fetching notes; a squash or rebase done by the forge (a GitLab or GitHub merge button), where no local daemon sees the rewrite. The README points to [CI workflows](https://usegitai.com/docs/guides/ci-workflows) for that case; not read.

## Claims from the author's talk

- [201 s](https://www.youtube.com/watch?v=irK4G2SzhpA&t=201): "it'll go through merges rebases cherrypicks all the nasty evil stuff that you can do to commits and diffs. Um, Git AI will preserve the authorship through all those real world workflows." The test above confirms rebase and squash merge locally, not cherry-pick.
- [295 s](https://www.youtube.com/watch?v=irK4G2SzhpA&t=295): "it's doing this by attaching git notes um to every single commit."
- [520 s](https://www.youtube.com/watch?v=irK4G2SzhpA&t=520): users "review code differently based on whether an AI wrote it or whether a human wrote it", and running blame showed "what the prompt was and what the intent was behind this block of code". Reported by the author; no count.

## Corrections to the guide made with this evaluation

- The "AI Code Halflife of 3.33 years" stated in `ai-traceability.md` had no source. On 2026-11-08 the git-ai repository had no occurrence of "half-life", and a web search returned only this guide and its copies. The figure is withdrawn, as the recap cards already did.
- "Survive rebase, squash, and cherry-pick" becomes what was tested, with cherry-pick left as the author's claim.
- `git-ai stats [commit]` shows "AI authorship statistics for a commit" according to its help text; `git-ai stats HEAD` on the test repository showed the squashed commit as 100% AI. It is not a "project-wide metrics" command.
- The [Entire CLI evaluation](entire-cli.md) recorded git-ai as a 404 in February 2026; the repository at `git-ai-project/git-ai` was reachable on 2026-11-08.

## Score: 4/5

The core mechanism works as documented on the paths tested, it stores attribution in the repository rather than a vendor service, and the Agent Trace specification lists it among the partners that helped shape the format. It records who wrote which lines, not why: the note carries sessions and line ranges; its `prompts` field was empty in the test, and prompt capture with real agents was not checked.

## Decision

Rewrite §3.4 with the tested facts, add §3.5 "Provenance in git notes" comparing git-ai with the other recorders read, and add a diagram of the attribution path through amend, rebase, squash and a forge merge. Withdraw the halflife figure.
