# logseq-wiki (LLM Wiki pattern ported to Logseq)

## Evaluation metadata

| Field | Value |
|---|---|
| Resource | [ystreibel/logseq-wiki](https://github.com/ystreibel/logseq-wiki) |
| Type | Skill collection for building a Logseq knowledge base with coding agents |
| License | MIT (the vendored `skill-creator` skill keeps its Apache 2.0 license) |
| Evaluated | 2026-09-29, at commit [`339072e`](https://github.com/ystreibel/logseq-wiki/tree/339072e5d10db29a07d611b611e1122c74b3ac02) |
| Upstream | [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki), MIT |
| Decision | Mention, as a security case study in `guide/core/memory-systems.md` §7.1 |
| Score | 2/5 |

## Verdict

logseq-wiki is a Logseq-native port of obsidian-wiki, itself an implementation of Andrej Karpathy's LLM Wiki pattern: the agent compiles sources once into interlinked pages and keeps them current, instead of re-deriving answers through RAG on every question. The port changes the format (Logseq `key:: value` properties instead of YAML frontmatter, `[[wiki/...]]` namespace links) and keeps the pipeline: ingest, extract, resolve, schema.

As a tool, it does not earn a place in the guide. It is a single-author port with minimal adoption, and the pattern it implements is already covered by the OKF section of the main guide. What it does earn is a place as a case study. Its autonomous ingest job combines, in one scheduled run, every factor that turns a personal knowledge base into a prompt-injection sink. The guide's memory-poisoning section only covered the team-shared case.

## Measured facts

All figures from the GitHub API and a clone of the repository, 2026-09-29.

| Metric | Value |
|---|---|
| Stars / forks | 5 / 1 |
| Commits | 36, one author, 2026-04-24 to 2026-09-28 |
| Skills | 39 in `.skills/`, exposed to 17 agents through committed symlinks |
| Upstream obsidian-wiki | 3,505 stars, 350 forks, created 2026-04-06, last push 2026-09-28 |

## What the code does, with sources

1. **An autonomous run with every permission granted, fed by third-party content.** [`run_auto.sh` line 79](https://github.com/ystreibel/logseq-wiki/blob/339072e5d10db29a07d611b611e1122c74b3ac02/.skills/ingest-youtube-history/scripts/run_auto.sh#L79) runs `claude -p "$PROMPT" --dangerously-skip-permissions`. The script header states "No human in the loop". Its input is the user's scraped YouTube watch history, and the session then fetches transcripts of third-party videos. The [prompt](https://github.com/ystreibel/logseq-wiki/blob/339072e5d10db29a07d611b611e1122c74b3ac02/.skills/ingest-youtube-history/scripts/auto-prompt.md) instructs the session to write pages, commit and push to the vault's remote.
2. **Agent authorship deliberately removed.** The same prompt forbids a `Co-Authored-By: Claude` trailer on the vault commits. Provenance of agent-written pages is lost at the git level.
3. **A browser debug endpoint opened to any origin.** [`run_auto.sh` line 47](https://github.com/ystreibel/logseq-wiki/blob/339072e5d10db29a07d611b611e1122c74b3ac02/.skills/ingest-youtube-history/scripts/run_auto.sh#L47) starts Chrome with `--remote-debugging-port=9222 --remote-allow-origins='*'` on a dedicated profile that holds a logged-in YouTube session. The wildcard disables the origin check Chrome applies to DevTools WebSocket connections. Exploitability from a web page was not tested here.
4. **A mitigation that exists but is not on the exposed path.** `wiki-ingest` supports a staging mode (`WIKI_STAGED_WRITES=true`) that sends LLM-written pages and patches to `wiki/_staging/` for review through `wiki-stage-commit`. The variable is absent from `.env.example`, so staging is off by default, and the autonomous prompt writes directly to `wiki/<theme>/`.
5. **Documentation that contradicts the code.** The [launchd plist comment](https://github.com/ystreibel/logseq-wiki/blob/339072e5d10db29a07d611b611e1122c74b3ac02/.skills/ingest-youtube-history/scripts/com.logseq-wiki.yt-history.plist#L7) describes the job as "semi-auto, no ingest". The script it launches runs the full ingest, commit and push.
6. **Secret filtering by prompt only.** [`claude-history-ingest` line 254](https://github.com/ystreibel/logseq-wiki/blob/339072e5d10db29a07d611b611e1122c74b3ac02/.skills/claude-history-ingest/SKILL.md#L254) reads Claude Code transcripts (`~/.claude/projects/*/*.jsonl`) and relies on the instruction "Skip anything that looks like secrets". No deterministic scanner runs before pages are written to the vault.

## Ideas worth noting, not integrated

- **Cross-tool provenance diff** (`memory-bridge`): pages are tagged with the agent history they came from, and a diff mode lists what one tool's history knows that another's does not. Novel, but one repository with no usage evidence.
- **Token-bounded context packs** (`wiki-context-pack`): relevance-ranked pages packed under a token budget for a downstream agent. Already covered in principle by progressive disclosure in `memory-systems.md`.

## Comparison with existing guide coverage

| Aspect | Guide before | Action |
|---|---|---|
| LLM Wiki pattern | Covered through OKF, `ultimate-guide.md` §9.18.5 | None |
| Memory poisoning | `memory-systems.md` §7.1, team-shared memory only | Added a single-user, ingestion-time variant with this repository as the example and four controls |
| Risk matrix | No row for single-user compiled wikis | Added one row |
| obsidian-wiki | Not referenced anywhere in `guide/` | Not integrated: its code was not reviewed in this pass. Candidate for a separate evaluation |

## Fact-check

| Claim | Verified against |
|---|---|
| Stars, forks, license, dates for both repositories | `gh api repos/...`, 2026-09-29 |
| Commit count and single author | `git log` and `git shortlog` on the clone |
| `--dangerously-skip-permissions`, `--remote-allow-origins='*'`, "No human in the loop" | `run_auto.sh` at the evaluated commit, lines 4, 47, 79 |
| No co-author trailer instruction, direct writes to `wiki/<theme>/` | `auto-prompt.md` at the evaluated commit |
| Staging is opt-in and absent from the example config | `wiki-ingest/SKILL.md` lines 26 and 169, `wiki-stage-commit/SKILL.md` line 18, `.env.example` |
| Plist comment contradicts the script | plist line 7 against `run_auto.sh` |

Not verified: whether the autonomous job has run in production, and whether any exploit path through the transcript input or the debug port works in practice.
