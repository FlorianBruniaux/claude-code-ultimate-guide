# WikiSkill: persistent knowledge for skill evolution

Evaluated October 15, 2026. **Score: 4/5, selective integration.**

Primary source: Liyan Tang, Cyrus Rashtchian, Chun-Sung Ferng, Andrew Tomkins, Da-Cheng Juan and Tu Vu, [WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution](https://arxiv.org/abs/2608.27454v1), submitted August 27, 2026. This evaluation concerns v1, not a verified Claude Code implementation.

## Decision

Retain the distinction between execution traces, accumulated knowledge and active procedures. The useful addition beyond the guide's existing meta loop is **keeping rejected proposal diffs and outcomes available to the next proposer while restoring the active skill**. Skill authoring and skill execution also need separate evaluation on the intended model.

The paper is evidence for a bounded research method. It does not establish automatic skill improvement in Claude Code, deployment safety, lower total cost, or a replacement for fine-tuning across all tasks.

## Source access and method

Paper Insights access was unsuccessful; this evaluation uses the [arXiv abstract](https://arxiv.org/abs/2608.27454v1) and [primary HTML text](https://arxiv.org/html/2608.27454v1). The review covers the method, result tables, ablations, limitations and implementation appendices. No benchmark replication was performed.

## What the method changes

The [method](https://arxiv.org/html/2608.27454v1#S3) has three layers:

| Layer | Stored material | Who uses it |
|---|---|---|
| Raw | Immutable training execution traces | Wiki maintainer and skill proposer |
| Wiki | Revisable pattern pages, evolution log, proposal diffs, validation scores and acceptance outcomes | Maintainer and proposer |
| Skills | Active procedural instructions, with a separate file linking them to motivating patterns | Inference agent receives active skill content |

Each proposal targets one skill. The outer harness accepts only a score strictly above the best validation score; a tie is rejected. On rejection, the previous skill set returns and the wiki persists. This keeps the unsuccessful intervention available for later diagnosis without promoting it into the executing agent's instructions.

The inference agent receives the full active skills in its system prompt. This deliberately removes activation and retrieval failures from the experiment. It does not reproduce a native on-demand skill loader.

## Check the circulated claims

| Circulated claim | Primary-source finding | Editorial decision |
|---|---|---|
| The wiki is append-only | Pattern pages support append, replace and insert edits; logs and impact records accumulate | Say persistent and revisable, with retained intervention history |
| Skills roll back when accuracy drops | Acceptance requires strict improvement over the best validation score | Include ties in rejection |
| Keeping the wiki away prevents hallucinations | The ablation measures final skill quality after varying wiki access during development | Do not infer a hallucination or security guarantee |
| Small context and verified skills | Full skill injection bypasses retrieval and activation; validation is benchmark scoring | Do not claim bounded prompt size or general correctness |
| Other optimizers discard all history | EvoSkill's description includes a flat proposal-outcome history | Attribute the richer, separate knowledge representation; avoid claiming all baselines forget everything |
| Frozen weights make fine-tuning unnecessary | These experiments improve performance through procedures without weight updates | Do not generalize into cost, risk or universal substitution claims |

## Reported results and counterexamples

[Table 1](https://arxiv.org/html/2608.27454v1#S4.SS2) reports average test performance across three independent full evolution runs on five benchmarks: LiveMath, SealQA, SpreadsheetBench, OfficeQA and ALFWorld. These are not five production coding evaluations.

| Model and scope | Without skills | WikiSkill | Difference |
|---|---:|---:|---:|
| Gemini-3.5-Flash, five-benchmark mean | 49.5% | 68.1% | +18.6 percentage points |
| Qwen-3.6-27B, five-benchmark mean | 39.4% | 63.3% | +23.9 percentage points |
| Qwen-3.6-27B, SpreadsheetBench | 40.8% | 81.7% | +40.9 percentage points |

The strongest competing mean for Gemini in that table is 56.1%. These are paper-reported results, not a local replication.

[Table 2](https://arxiv.org/html/2608.27454v1#S4.SS2.SSS2) separates skill source and executor. Qwen-3.5-9B reaches 70.2% on ALFWorld with Qwen-3.6-27B skills, versus 63.4% with its own. Across the five benchmarks, the 9B model with self-evolved skills averages 47.4%, above the 27B no-skill mean of 39.4%. The cross-model ALFWorld comparison and the five-benchmark mean have different scopes.

Transfer can also hurt: Qwen-3.5-4B skills lower Gemini-3.5-Flash's SpreadsheetBench performance from 50.5% to 18.1%. The authors identify restrictive workarounds and fragmented diagnostics that consume the interaction budget. A skill's portability as text does not establish useful transfer.

The [wiki ablation](https://arxiv.org/html/2608.27454v1#S5.SS1) uses Gemini on four benchmarks, excluding ALFWorld. Giving the proposer wiki access, with inference access disabled, raises the mean from 48.7% to 63.7%. Allowing inference wiki access during development lowers it to 60.9%. The comparison without proposer access also removes the maintainer, so it does not isolate storage alone.

## Limits that change adoption

The paper's [limitations and appendices](https://arxiv.org/html/2608.27454v1) leave several boundaries explicit:

- Validation sets contain 10 to 40 tasks and are reused for candidate gating. Strict improvement can select noise; three final runs and bootstrap tests do not turn each promotion into a reliable production decision.
- The wiki has no automated pruning. Persistence over the measured evolution process does not prove sustainable long-term maintenance.
- Full skill injection leaves routing, activation and progressive disclosure unevaluated. The wiki restriction is an experimental boundary, not a prompt-injection defense.
- The benchmark suite does not cover very long execution horizons. OfficeQA starts with oracle reference pages, constraining the interpretation of document retrieval performance.
- Optimizer API-call complexity excludes the full resource accounting needed for a cost-per-accepted-task comparison. Rollouts, validation, tokens, retries and human review still cost resources.

## Integration decisions

| ID | Placement | Existing coverage | Addition and boundary |
|---|---|---|---|
| W1 | [Memory systems, architecture patterns](../../guide/core/memory-systems.md#68-compile-experience-into-skills-wikiskill) | File playbooks, consolidation, provenance and rule promotion | Separate revisable knowledge from active skills; retain rejected proposal evidence |
| W2 | [Harness optimizers](../../guide/core/agent-harness.md#11-harness-optimizers-and-meta-harnesses) | Held-out evaluation, candidate versions, budgets and rollback | Persistent proposal history plus positive and negative model transfer |
| W3 | Portfolio draft, *Turn recurring review comments into tested controls*, in its existing Engineering the Review Loop series | Rule promotion and separate author/reviewer improvement loops | Retain rejected candidates outside active instructions, link evidence to procedures and evaluate the executor; keep draft status |
| W4 | Existing Flow Lean article | Two documented rejected wording changes and historical evaluation limits | Do not add a second retrospective or relabel those historical tests as WikiSkill evidence |
| W5 | BM25 routing content | Skill selection and activation | No research-performance claim: the paper bypasses this mechanism |

The guide discovery files and reference/MCP mirrors need W1/W2 links. The portfolio's generated catalog must be rebuilt from the edited draft; its separate enriched reference needs targeted metadata updates. No new portfolio article, runtime optimizer, shared skill or global configuration change is needed for this integration.

## Proposed local experiment, not executed

Choose one repeated failure class and freeze the executor, tools, permissions, grader and resource limits. Preserve authorized, redacted source traces. Compare the existing maintenance process with a process that also supplies the proposer a structured history of accepted and rejected diffs. Keep the final test tasks hidden from both processes.

Record source references, candidate versions, validation decisions, repeated-run outcomes, severe failures, false blocks and complete accepted-task cost. Reject candidates that violate mandatory protections regardless of average score. Re-run on the intended executor before distributing a transferred skill. If a rejection is reconsidered, name the changed task, environment or new evidence.

Acceptance requires a declared decision rule and inspected final-test evidence, not merely more patterns or fewer repeated proposals. No such experiment or production benefit was measured in this evaluation.

## Technical challenge

A separate technical-writer review retained the 4/5 score, checked the numerical scopes and method against the primary text, and requested two corrections: distinguish retrieval/activation from skill discovery through evolution, and remove local research bookkeeping from public prose. Both were applied. The review was documentary; no independent replication of the paper is claimed.
