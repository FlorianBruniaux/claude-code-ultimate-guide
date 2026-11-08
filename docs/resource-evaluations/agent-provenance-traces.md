# Agent provenance traces: AgentNote, docket and the Agent Trace specification

**Reviewed**: 2026-11-08. **Scores**: Agent Trace specification 3/5, docket 3/5, AgentNote 2/5. Integrated in [AI Traceability §3.5](../../guide/ops/ai-traceability.md#35-provenance-in-git-notes), next to git-ai, which was tested; these three were read, not run.

All three record which agent session produced which lines, so that a reviewer can get back from a line to the conversation or the intent behind it. The code of AgentNote and docket was read statically at the SHAs below; nothing was installed or run. Attribution rates and survival claims are the authors' unless stated otherwise.

## Not the same project as the earlier "agent-trace" evaluation

[`Siddhant-K-code/agent-trace`](https://github.com/Siddhant-K-code/agent-trace), evaluated on 2026-03-16 ([2/5](2026-03-16-agent-trace-siddhant-github.md)), is a Python session recorder and replayer with an OpenTelemetry export. This evaluation scores the **Agent Trace specification**, a data format for line-level attribution published at [agent-trace.dev](https://agent-trace.dev/) and mirrored at [`superhq-dev/agent-trace`](https://github.com/superhq-dev/agent-trace/tree/f7577a60e2f720ac83fab825fa3903e932d90bcb). They share a name; their scope and format differ.

## Sources

| Project | Read at | Licence | Position |
|---|---|---|---|
| Agent Trace specification, [mirror README](https://github.com/superhq-dev/agent-trace/blob/f7577a60e2f720ac83fab825fa3903e932d90bcb/README.md) | `f7577a6`, read 2026-11-08 | CC BY 4.0 (stated in the README) | Version 0.1.0, status RFC, dated January 2026 |
| [`wasabeef/AgentNote`](https://github.com/wasabeef/AgentNote/tree/bf51ac657c7a8f41dcfedf84d0521a1c66b9e450) | `bf51ac6`, HEAD on 2026-11-08 | MIT | TypeScript CLI and GitHub Action |
| [`Dillonsmart/docket`](https://github.com/Dillonsmart/docket/tree/41af24af8a30dc43236b2d15abe6dbb93be22db3) | `41af24a`, HEAD on 2026-11-08 | Apache-2.0 | Go CLI and GitHub Action, version 0.0.7 |

The specification's own pages name [`cursor/agent-trace`](https://github.com/cursor/agent-trace) as the place to send suggestions. On 2026-11-08 that repository returned "Repository not found" to `git ls-remote` and 404 to the GitHub API. The `superhq-dev` copy is not marked as a fork and has 1 star; it is the only public copy of the text found in this review.

## Agent Trace specification (3/5)

- A **trace record** carries a version, an id, a timestamp, an optional VCS revision and tool, and a list of files. Each file lists **conversations**, each with an optional `url`, a contributor (`human`, `ai`, `mixed` or `unknown`, with a `model_id`) and line **ranges**.
- A range may carry a `content_hash` "for position-independent tracking", so attribution can follow code that moves within or between files.
- Line numbers refer to the recorded revision. To find who wrote line N today, the spec says to blame the line, then look up the trace for that revision.
- The spec does not define storage ("local files, git notes, a database, or anything else") and leaves rebases and merge commits open: "We expect to see different implementations in open source."
- The README thanks Amp, Cloudflare, Cognition, git-ai, Jules, OpenCode and Vercel for helping shape it. Whether any of them ships the format was not checked.

**What it adds**: a vendor-neutral record shape to compare tools against, with the content hash as the key idea for surviving edits. **Limit**: an RFC at 0.1.0 whose canonical repository is not reachable today; rewrites left to implementations (only the jj `revision`, a change ID, is described as "stable across amend/rebase operations"); no field for intent or rationale, only a conversation link.

## docket (3/5)

- Records are built at commit time from the agent's session transcripts (Claude Code, Codex, opencode), signed with ed25519 and stored on the orphan ref `refs/docket/records`.
- Intent is the last assistant text before the edit, falling back to the thinking block, truncated to 200 characters and passed through secret redaction. It is recovered from the transcript, not written for a reviewer.
- Attribution is anchored on content: a line is credited only if its text appears in the recorded output of the edit (high confidence), otherwise medium or none.
- Each hunk gets an evidence density from 0 to 1 and a `human_contact` field (`none`, `edited`, `approved`). Hunks at or below 0.15 are labelled "no evidence", and the pull request comment orders hunks by a risk score built from that density, unknown origin and missing human contact.
- A rebase or cherry-pick does not rerun `prepare-commit-msg`, so the commit trailer is copied onto a diff it was not built for, and the by-commit index keeps pointing at the old SHA. GitHub only; GitLab is on the README's "not yet built" list.
- The README's attribution rates (98.1%, 94.7%, 92.9%, 59.2%) are the author's, measured on the author's own sessions, and were not reproduced.

**What it adds**: of the three read, the design nearest to a reviewer view: per-hunk intent, explicit "no evidence" hunks, risk ordering, content anchoring. **Limit**: a single-author project at 0.0.7 with 23 commits; partial survival of history rewrites; records exist only if each developer pushes them.

## AgentNote (2/5)

- Claude Code hooks (SessionStart, Stop, UserPromptSubmit, PreToolUse and PostToolUse on edit tools and `git commit`) capture the conversation and attach it to each commit under `refs/notes/agentnote`. A trailer `Agentnote-Session` links commits to sessions.
- `agent-note why file:line` runs `git blame`, finds the commit and its note, and selects interactions whose touched files include that file. The grain is the file, not the hunk.
- A GitHub Action renders a table into the pull request description between HTML markers.
- **Privacy**: full prompts and agent replies are stored as is in the note and pushed by the `pre-push` hook, without secret redaction. The project's architecture document says so.
- **History rewrites**: `notes.rewriteRef` is documented as planned and set by no code read, so notes indexed by SHA are orphaned after an amend, rebase or squash.
- The generated hooks call `npx --yes agent-note hook` without a pinned version, so every agent event runs whatever version npm resolves.

**What it adds**: a working example of hook-based capture into git notes and a blame-to-conversation lookup. **Limit**: unredacted transcripts pushed to the remote by default and no survival across rewrites. Mention as a design reference only.

## Attribution signals in commits are weak evidence

Sachin Gupta (eBay) [checked textual signals](https://www.youtube.com/watch?v=TJPInBjhE4Q&t=636) (co-authored footer, branch prefixes, "generated by" phrases) on "three public repos, which comprised of 524 PRs"; on repo C the lowest-scoring signal "was 0% on the repo C. Even though it was done by coding agent", and the speaker adds that the repository "might have blocked it". The repositories are not named, the signal is not identified and agent authorship is the speaker's statement. Read with the [talk evaluation](reviewable-agent-changes-talks.md): a missing trailer does not show that a human wrote the code, which is the gap these three projects try to close.

## Not verified here

- Runtime behavior of AgentNote and docket, including docket's attribution rates and AgentNote's transcript lookup.
- Survival of docket records or AgentNote notes after amend, rebase or squash; concluded from code and documentation, not tested.
- Adoption of the Agent Trace format by the partners named in its README, and where its canonical repository moved.

## Decision

Used in §3.5 "Provenance in git notes", after the [git-ai rewrite test](git-ai-provenance-notes.md): the Agent Trace record shape and content hash as the reference format, docket as the reviewer-facing design, AgentNote as a cautionary example on privacy and rewrites. Do not recommend installing AgentNote as configured. Survival claims for AgentNote and docket remain untested; only git-ai was run.
