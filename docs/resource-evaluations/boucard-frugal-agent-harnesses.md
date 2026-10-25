# Bruno Boucard: frugal agent harnesses

**Reviewed**: 2026-10-24. **Initial and final score**: 3/5 for selective integration into existing pages.

## Sources and evidence

| Source | Contribution | Limit |
|---|---|---|
| [Bruno Boucard, Harnais agentiques (1/2)](https://blog.octo.com/harnais-agentiques-%2812%29--pourquoi-les-bonnes-pratiques-d%27hier-coutent-cher-aujourd%27hui), OCTO, 2026-10-23 | Clear comparison between cached input, generated artifacts, and correction overhead | Practitioner synthesis with illustrative token volumes; no controlled generation-to-generation comparison or measured gain from removing a component |
| [Anthropic API pricing](https://platform.claude.com/docs/en/about-claude/pricing), checked 2026-10-24 | Opus 5.5 input/output/cache rates of $4/$20/$0.20 per million tokens; Sonnet 5.5 cache reads at $0.10 | Standard API pricing, not a subscription invoice or whole-task cost |
| [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#structuring-your-prompt), checked 2026-10-24 | Stable prefixes, breakpoint placement, bounded lookback, writes and reads | Documentary support; no live cache experiment performed |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices#explore-first-then-plan-then-code), checked 2026-10-24 | Skip planning overhead for small, clear changes while retaining appropriate verification | Product guidance, not comparative evidence for every repository |

## Decision

Integrate the marginal-cost example and qualify existing recommendations in [Agent Harness Engineering](../../guide/core/agent-harness.md#price-generated-artifacts-against-cached-context), [Context Engineering](../../guide/core/context-engineering.md#scratchpad-pattern), and the [English](../../guide/ultimate-guide.md#925-repository-harness-engineering) and [French](../../guide/ultimate-guide.fr.md#925-repository-harness-engineering) full guides. The existing smallest-sufficient-harness, progressive-disclosure, ejection, and evaluation-epoch sections already cover most of the thesis.

Do not infer that output dominates every bill, shorter instructions guarantee better quality, or stronger models make verification and permissions unnecessary. Plans and handoff notes can serve people, durable decisions, and recovery. Evaluate their removal against the same acceptance criteria and include failed attempts, coordination, human review, and rework.

The numerical example checks arithmetic at published rates. It excludes initial cache creation and does not demonstrate a cheaper accepted task. The working-state example demonstrates message assembly; persistence, state validity, and live cache behavior require separate tests. This update does not refresh every historical price, product claim, or translated passage.

## Technical challenge

A separate technical-writer review found no actionable issue in the scoped C1-C4 and A1 changes and confirmed the 3/5 score. It checked the English/French additions, the supplied article, and current official cache documentation. It did not audit historical passages, validate discovery indexes, call a billed API, or measure live cache behavior.
