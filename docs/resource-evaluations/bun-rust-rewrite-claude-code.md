# Rewriting Bun in Rust (jarred sumner, jul 2026)

## Evaluation metadata

| Field | Value |
|---|---|
| Resource | [Rewriting Bun in Rust](https://bun.com/blog/bun-in-rust) |
| Author | Jarred Sumner, Bun |
| Published | 2026-07-08 |
| Evaluated | 2026-09-29 |
| Resource type | First-party operator account of a Claude Code migration |
| Found via | [Brownfield Agentic Engineering](./osmani-brownfield-agentic-engineering.md), which cites it; figures below are taken from the primary post, not from that citation |
| Decision | Integrate as a case study |
| Score | 4/5 |

## Verdict

The guide had no worked example of a large migration run with Claude Code. This post is one: a mechanical Zig-to-Rust port of 535,496 lines across 1,448 files in 11 days, with the workflow design, the false starts and the resulting rules written down by the operator. The transferable part is the structure (rulebook first, pilot on three files, oracle outside the change, two adversarial reviewers, failures turned into rules), which is what the guide integrates.

The score stops at 4/5. It is a self-report by the person who knows the codebase best, supervised by him for most of the run, on the most favorable migration shape for agents: behavior-preserving, against a test suite that does not depend on the implementation language. It publishes no post-release defect rate.

## Verified facts used for integration

All read on the primary post on 2026-09-29.

| Fact | Used in |
|---|---|
| 535,496 lines of Zig, 1,448 `.zig` files, 11 days (May 3 to 14, 2026) | §9.21 case study |
| About 50 dynamic workflows, about 64 concurrent Claude instances at peak, pre-release Claude Fable 5 | §9.21 case study |
| 5.9 billion uncached input tokens, 690 million output tokens, 72 billion cached input token reads, "around $165,000 at API pricing" | §9.21 case study |
| About 3 hours producing `PORTING.md`; lifetime analysis written to `LIFETIMES.tsv` | §9.21 case study |
| Trial on 3 files: 1 implementer, 2 adversarial reviewers, then a fixer | §9.21 case study |
| Merge gate: 1,386,826 `expect()` calls, 60,624 tests on one platform, "0 tests skipped or deleted"; author "manually verified the tests were in fact running and not being skipped" | §9.21 case study |
| False starts: agents ran `git stash` and `git reset` over each other's work; agents stubbed functions with compilation errors | §9.21 case study, worktree note in "Git Worktrees for Parallel Development" |
| "This rewrite introduced 19 known regressions, each of which has been fixed." | §9.21 evidence limits |

## Not integrated

| Item | Reason |
|---|---|
| Commit count | The post and secondary coverage give both 6,502 and 6,778; not needed for any recommendation |
| "About 1,300 lines of code per minute" at peak | Throughput figure with no quality counterpart; adds nothing a reader can act on |
| Secondary claims (performance gain, binary size) from third-party write-ups | Not about the agent workflow |

## Challenge

**Objection**: one exceptional engineer with an exceptional test suite is not a reference architecture. **Answer**: agreed, and the guide says so. The integration pairs the case with SWE Refactor Bench, where language rewrites were the weakest category, and states that the result does not transfer without an equivalent oracle. What does transfer is cheap to copy at any scale: write the rulebook first, pilot on three units, keep the tests outside the change, and turn every false start into a rule.
