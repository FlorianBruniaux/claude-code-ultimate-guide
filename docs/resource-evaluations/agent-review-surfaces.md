# Local review surfaces for agent-written changes (glassbox, diffo, hunk, drift, ai-pr-review, guidedreview)

**Reviewed**: 2026-11-08. **Scores**: diffo 4/5, glassbox 3/5, hunk 3/5, drift 3/5, ai-pr-review 2/5, guidedreview 2/5. Integrated in [Multi-provider code review](../../guide/workflows/multi-provider-code-review.md#local-review-surfaces-for-agent-written-changes) and as a diagram in [Development workflows](../../guide/diagrams/06-development-workflows.md#three-places-an-agent-change-gets-explained). Related: [Resisting Cognitive Surrender](knlb-cognitive-surrender.md), [agent provenance traces](agent-provenance-traces.md).

These tools sit between the agent and the forge: a developer runs them locally to read an agent's change before or during review. Five were read statically from a clone; guidedreview was read from its README only. Nothing was installed or run, so every behavior below is what the code or the documentation says, not an observed result.

## Sources and SHAs

| Tool | Licence | Read at | HEAD on 2026-11-08 | Changes since the reading |
|---|---|---|---|---|
| [glassbox](https://github.com/brianwestphal/glassbox/tree/e6a418288144cf0b73511c2279c4d03036f3442c) | MIT | `e6a4182` | same | none |
| [diffo](https://github.com/DiffoHQ/diffo/tree/fc42503632e466f0c5196d603882fdf9f8f98c4c) | Apache-2.0 | `d7535ec` | `fc42503` | 4 commits: dependency bumps; release 0.21.0 lets a layer cover part of a file by hunk range |
| [hunk](https://github.com/modem-dev/hunk/tree/a3c2592c4c38f3b8060cc9c9885c2c775a1c6d40) | MIT | `544bc40` | `a3c2592` | 8 commits, including GitHub Enterprise Cloud (`ghe.com`) hosts and a third-party `hunk-glab` extension listed in its extension marketplace on 2026-11-07 (not read) |
| [drift](https://github.com/tothalex/drift/tree/a4dcf341ed95347ea9d5aef2b0db3c93f9f74a30) | MIT | `a4dcf34` | same | none |
| [ai-pr-review](https://github.com/houshuang/ai-pr-review/tree/c8da8d5bf5f219ea03d1249e684412c9fc9cf21f) | MIT stated in the README; no LICENSE file in the tree read | `0cc95cc` | `c8da8d5` | 4 commits: stale-review banner, reuse of earlier review work after a force push, de-duplicated file lines |
| [guidedreview](https://github.com/nshntarora/guidedreview/tree/61360c0b9252bcf74fec749423e7f0a03874dc24) | not checked | README at `61360c0` | same | n/a |

The commit lists between the reading SHA and HEAD come from the GitHub compare API. The changed code was not re-read.

## What each tool does

**diffo (4/5).** The agent writes its own rationale through the CLI (`diffo comment`, `diffo layers`, `diffo reply`) and posts an ordered list of layers (title, summary, files, decisions). Comments anchor on a hunk id addressed by content (truncated SHA-256 of path, changed lines and occurrence), falling back to the line, the file, then the whole change. `diffo poll` returns the reviewer's threads to the agent, each typed Change or Question, with a different reply contract. GitHub only, through `gh`. Anonymous PostHog telemetry is on by default. Storage is one SQLite database through Node's experimental `node:sqlite`. It is the only tool read that closes the loop with typed feedback.

**glassbox (3/5).** The agent records notes with `glassbox note add`, following instructions the tool injects into its context; no hook forces it. Notes carry a kind (rationale, proof, assumption, alternative considered, risk and others) and are stored as SARIF 2.1.0, one file per source file under `.pr-notes/`, versioned with the code. Anchoring is per line: a note is re-anchored by matching the first line of its stored snippet within 50 lines. The written fingerprint hash is not used for re-anchoring. Notes render under the anchored line. Human annotations are exported to a review file the agent reads. No forge integration.

**hunk (3/5).** A terminal diff viewer. The agent comments in a live session (`hunk session comment add`) or through a JSON sidecar with `oldRange`, `newRange`, `summary`, `rationale`, `confidence`. Anchors resolve permissively to the current hunk so a note is never lost; there is no line-shift tracking. The agent can read human notes and reply, not edit them. Reads GitHub diffs; posts nothing to a forge. Extensions passed by flag or user config run without a trust prompt.

**drift (3/5).** A Rust terminal UI that shows no AI explanation at all; the text beside the diff is the forge discussion. It is the only tool read with GitLab support (through `glab api`): it rebuilds the discussion `position` from the merge request's `diff_refs` (added line `new_line`, removed line `old_line`, context both) and marks a discussion whose `position.head_sha` differs from the current head as outdated instead of dropping it. It sends a selected code range plus an instruction to an agent running in another tmux, herdr or cmux pane.

**ai-pr-review (2/5).** A model writes a structured walkthrough after the fact, from the diff, commits, description and comments; the authoring agent's reasoning is not available to it. Code checks the output: line ranges against the diff, `path:line` citations against the tree at the head commit, with up to 3 repair rounds. At the SHA read, verifying review tips launched Codex with `workspace-write`, `network_access=true` and approval policy `never` on the pull request's code, so untrusted code could run on the reviewer's machine.

**guidedreview (2/5).** From the README: a Chrome extension for GitHub pull requests and a local CLI that group related hunks into ordered review units with short LLM commentary, on request. Comments attach to the real diff lines. "Generate Prompt" builds a prompt for a coding agent from the reviewer's notes and copies it; the tool does not send it.

## What the six have in common

- None places the agent's explanation in a column beside the diff. glassbox and hunk insert it under the anchored line; ai-pr-review and guidedreview generate it after the fact.
- Only drift reads and writes GitLab merge request discussions. diffo, ai-pr-review and guidedreview are GitHub only; glassbox has no forge layer.
- Only diffo types the reviewer's feedback, so the agent can tell a question from a requested change.
- None reports a measurement of review quality, time or defects found.

## Not verified here

- Runtime behavior of every tool; nothing was run.
- Changes after the reading SHA for diffo, hunk and ai-pr-review, and the third-party `hunk-glab` extension.
- guidedreview's code, licence and data flows beyond the README.
- Whether ai-pr-review still runs Codex with network access at `c8da8d5`.

## Decision

Add a comparison table to "Interactive companions vs. CI" in the multi-provider review page, with the security caveat for ai-pr-review, and a diagram of the three places an agent change gets explained. Recommend none of them as a CI gate.
