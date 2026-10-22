# Grill me: interview-first patterns (Cherny, Shihipar, Pocock)

## Evaluation metadata

| Field | Value |
|---|---|
| Resources | Boris Cherny's "Grill me on these changes" tip ([X thread](https://x.com/bcherny/status/2017742752566632544)); Anthropic best practices, [Let Claude interview you](https://code.claude.com/docs/en/best-practices); Matt Pocock's `grill-me` and `grilling` skills ([mattpocock/skills](https://github.com/mattpocock/skills), MIT) |
| Published | 2026-01-31 (Cherny thread); `grill-me` first commit 2026-02-25, `grilling` primitive 2026-05-31; official docs read 2026-10-22 |
| Evaluated | 2026-10-22 |
| Resource type | Practitioner tip, official documentation, open-source skill with its documentation and issue tracker |
| Decision | Integrate |
| Score | 4/5 |

## Verdict

The guide covered only one of the three practices that share the "grill me" name: Boris Cherny's gatekeeper prompt in `guide/ultimate-guide.md` §2.8.1, where Claude examines the user on a finished diff. It had nothing on interviewing before a spec, although the official best practices now recommend it, and nothing on Pocock's open-source skill. The three differ in direction (who questions whom) and timing (before or after implementation): the gatekeeper prompt cannot help before code exists, and an interview cannot review a diff.

The score stops at 4/5. No controlled measurement of either interview workflow exists; the benefit rests on practitioner reports and on adjacent research about clarifying questions in code generation, which supports the premise but not the size of the gain.

## Verified facts used for integration

| Claim | Status | Used in |
|---|---|---|
| "Grill me on these changes and don't make a PR until I pass your test" is from a thread posted on 2026-01-31 (UTC) | Date decoded from the status ID; the guide cited "Feb 2026" in three places, corrected to Jan 2026 | `guide/ultimate-guide.md` §2.8.1 and two other citations of the same thread |
| Official prompt: interview with `AskUserQuestion`, then write `SPEC.md`, then a fresh session to implement | Quoted verbatim from `https://code.claude.com/docs/llms-full.txt`, section "Let Claude interview you" | `guide/workflows/spec-first.md` |
| First `grill-me` text: "Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one." | Read in the raw file at commit [`78649baa`](https://github.com/mattpocock/skills/commit/78649baa) (2026-02-25) | `guide/workflows/spec-first.md` |
| Current mechanisms: recommended answer, facts looked up by the agent, frontier rounds, confirmation gate | Read in `skills/productivity/grilling/SKILL.md` and `docs/productivity/grilling.md` on `main` | `guide/workflows/spec-first.md` |
| `grill-me` writes no files; leave plan mode off because it "makes the agent hurry to produce a plan" | Read in `docs/productivity/grill-me.md` | `guide/workflows/spec-first.md` |
| Failure modes: passive agreement ("A session with no pushback from you is a session you didn't need"), questions that need a prototype, scope too large, "Weaker and faster models still skip the gate" | Read in the repository docs and the author's post "9 Things People Get Wrong With /grill-me and /grill-with-docs" | `guide/workflows/spec-first.md` |
| Some users (slow readers, second-language users) report that one question at a time works better; opt-out line `When grilling, ask one question at a time.` | Read in `docs/productivity/grilling.md` | `guide/workflows/spec-first.md` |
| ClarifyGPT: GPT-4 Pass@1 on MBPP-sanitized from 70.96% to 80.80% with ten participants | Read in the project README | `guide/workflows/spec-first.md` |
| HumanEvalComm: ChatGPT Pass@1 65.58% on HumanEval (HmEval column), 31.34% on the modified problems (HmEvalComm column), communication rate 14.21% | Read in the project README results table, column headers checked | `guide/workflows/spec-first.md` |

## Not integrated

| Claim | Reason |
|---|---|
| About 1.4 million installs of `grill-me` on skills.sh | Not re-verified; installs are not active use |
| Session sizes from individual reports (18 to 46 questions, about 45 minutes) | Single-user anecdotes; the guide keeps only the author's qualitative "split when it runs to hundreds of questions" |
| Reddit, dev.to and blog anecdotes ("~90% exactly what I want", "zero rework") | Not verified at source; no comparison baseline |
| Long sessions degrade after about 120k tokens | The author's estimate, not measured here |
| `AskUserQuestion` introduced in Claude Code v2.0.21 | Not re-verified against the release notes |
| Batched rounds push users to accept every recommendation at once (discussion #771) and the request to restore the old mode (issue #831) | Number of participants not re-checked; the guide cites the author's own documentation of the opt-out instead |
| The author's advice not to clear context before writing the spec | Not found in the current docs re-read for this evaluation |
| Codex `request_user_input` and Cursor Plan Mode as equivalents | Not re-read at source for this evaluation |

## Challenge

**Objection**: grilling is plan mode with extra steps. **Answer**: no. Grilling settles what and why through the user's decisions; plan mode turns settled decisions into how. The author's docs recommend leaving plan mode off while grilling because it "makes the agent hurry to produce a plan, when you want it to keep asking questions."

**Objection**: the official prompt writes `SPEC.md`, while `grill-me` writes nothing. **Answer**: they serve different ends. The official prompt produces a spec for a fresh implementation session; `grill-me` settles decisions and leaves the artifact to a later request. The guide tells readers to ask for the spec in the same session if they want to keep the decisions.

**Objection**: without measurements, this is fashion. **Answer**: the guide says so explicitly in an "Evidence" paragraph and limits the recommendation to ambiguous, costly decisions, with an explicit "skip it" case for small or reversible changes.
