---
title: "Best-of-N: Generate, Select, and Verify"
description: "A bounded protocol for generating independent candidates, selecting against a fixed rubric, and recording executable evidence"
tags: [workflow, evaluation, verification, agents, testing]
---

# Best-of-N: Generate, Select, and Verify

Best-of-N is useful when a task admits meaningfully different solutions, the cost of a wrong choice is material, and a reviewer or executable check can distinguish the candidates. Generate a small, independent set of candidates, score them against a rubric fixed before generation, verify the selected result, then record the evidence. It is a decision protocol, not a claim that more samples make an output correct.

Use one deterministic attempt when the acceptance test is already clear, the solution space is narrow, or the extra candidates would only repeat the same implementation. A formatting change with a checked fixture, a mechanical version update, and a one-line configuration repair normally do not justify Best-of-N.

## Decision rule

| Condition | Default | Reason |
| --- | --- | --- |
| One implementation path and a deterministic acceptance test | One attempt, then run the test | More candidates add review cost without useful search |
| Several plausible designs with different risks or trade-offs | Best-of-3 | The rubric can expose the trade-off before committing |
| High-impact change with an executable check and an independent reviewer available | Best-of-3 to Best-of-5 | Extra search is justified only if selection can be checked |
| Subjective writing, product direction, or architecture without a stable rubric | First define the decision and rubric | Candidate count cannot compensate for an undefined quality bar |
| Security, legal, medical, or irreversible action | Specialist review and domain-specific controls | Best-of-N is not an authorization or safety mechanism |

Start at three candidates. Increase to five only when the candidates remain materially different and the expected benefit exceeds the added generation, evaluation, and verification budget. Generate and score all candidates in the declared N before selection. A batched protocol may stop only between batches that were declared before generation, after every candidate in the completed batch has been scored and the predeclared stop condition is met. It cannot skip candidates within a declared batch. Do not extend the run merely because another answer might be better.

## The six operations are different

| Operation | Input | Output | It does not prove |
| --- | --- | --- | --- |
| Candidate generation | Same task contract | Independent proposals or patches | That any proposal meets requirements |
| Selection | Candidates and fixed rubric | A ranked candidate | That the ranking is factually or behaviorally correct |
| Synthesis | Explicitly chosen parts of candidates | A new combined candidate | That a majority endorsed the combination |
| Majority vote | Comparable answers to the same question | Most frequent answer | That the majority is correct or that its reasoning is sound |
| Executable verification | Selected candidate and a defined environment | Command output, exit status, and artifacts | Behavior outside the tested scope |
| Independent review | Candidate plus requirements, in fresh context | Reviewer verdict and findings | Independence if the reviewer shares hidden context or incentives |

Majority vote can be a selection signal for a question with a known answer. It is not a substitute for a rubric in a design task, nor a substitute for tests in a code task. Synthesis creates new behavior and must go back through selection and verification.

## Protocol

### 1. Freeze the task contract

Before generating anything, write down:

- scope and exclusions;
- repository revision, environment, permissions, and budget;
- acceptance criteria and mandatory failures;
- the rubric, its weights, and the minimum passing score;
- candidate count or predeclared batch schedule, time or token ceiling, and stop rule;
- the executable checks and the reviewer who owns any non-executable judgment.

Keep the rubric stable. A rubric changed after reading a candidate is a new experiment. Record the reason, version the rubric, and regenerate or rescore all candidates under the revised rubric.

### 2. Generate independent candidates

Give each generator the same frozen task contract, but do not show it other candidates, their scores, or a leader's reasoning. Assign every generated candidate an opaque identifier from the frozen ID scheme. The proof log must contain one line for every generated identifier, including rejected candidates. For patches, use isolated worktrees or separate diffs so one candidate cannot silently inherit another's changes.

Independence is operational, not mystical. Same model, prompt template, tools, and repository state may still produce correlated failures. Varying the model or prompting angle may improve diversity, but it does not establish independence. Record the actual controls used.

### 3. Score blind against the fixed rubric

Where practical, hide candidate provenance and order from the scorer. A useful implementation rubric separates correctness, requirement coverage, safety, maintainability, testability, and cost. Define observable anchors, not labels such as "good" or "clean".

| Criterion | Weight | Passing anchor |
| --- | ---: | --- |
| Required behavior | 40 | Each acceptance criterion maps to code and a check |
| Safety and scope | 25 | No unauthorized destructive, network, or permission expansion |
| Testability | 20 | Commands, environment, expected result, and artifacts are named |
| Maintainability | 15 | Smallest coherent change with explicit trade-offs |

Disqualify a candidate that fails a mandatory criterion even if its weighted score is high. Score every candidate in the declared N, or every candidate in a completed predeclared batch before applying its stop condition. Preserve raw scores and short evidence notes for every criterion. A score without a witness is a preference, not an audit trail.

### 4. Select, then synthesize only deliberately

Select the highest passing candidate. If scores tie, use the predeclared tie-breaker, such as lower change surface, lower runtime cost, or human adjudication. Do not merge attractive fragments informally. A synthesis has a new identifier, lists its parent candidates, and is scored and verified as a new candidate.

### 5. Verify outside the generation context

Run the declared executable checks in the recorded environment. Prefer tests, type checks, linters, contract checks, reproducible builds, fixture comparisons, or a proof-of-concept that can falsify the claim. A generator's statement that its own code works is not verification.

When no executable check exists, use a reviewer who did not generate the candidate and who receives the requirements and artifact without the generator's private reasoning. Record shared models, prompts, tools, repository state, incentives, and access as possible correlation. Fresh context reduces one source of leakage; it does not prove independence.

### 6. Publish the proof log

Copy the portable [`TESTING.md` template](../../examples/claude-md/TESTING.md) into the work item. Record the task contract, every generated candidate identifier and score, rubric version, commands, environment, results, failures, unknowns, reviewer provenance, and artifact links. Link the final entry to the selected diff, test output, and review record.

## Worked code-change pattern

1. Define an API behavior and write its failing test, following [TDD with Claude Code](./tdd-with-claude.md).
2. Freeze a three-candidate rubric that requires the test to pass, no public API expansion, and a bounded diff.
3. Generate three isolated patches from the same base commit.
4. Blind-score the diffs, select one, and run its tests, type check, and lint commands.
5. Ask a fresh-context reviewer to inspect the selected diff against the requirement. Use the [code-review workflow](./code-review.md) as a separate review layer when it is available.
6. Save the command output and verdict in `TESTING.md`; mark unrun integration or production checks as `UNKNOWN`.

For multiple stages and durable handoffs, encode the frozen contract, candidate IDs, schemas, and stop rule in [Dynamic Workflows](./dynamic-workflows.md). Measure candidate quality, selection errors, false accepts, false rejects, cost, and wall time using the [Agent Evaluation](../roles/agent-evaluation.md) protocol. Keep the evidence trail compatible with [AI traceability](../ops/ai-traceability.md), especially when the result is delivered to a reviewer or auditor.

## Evidence boundary

The research supports the narrow proposition that sampling several reasoning paths and selecting among them can improve results on particular evaluated tasks. Wang et al. sampled diverse reasoning paths and selected the most consistent answer, reporting benchmark gains for arithmetic and commonsense reasoning. That result does not establish that majority vote, self-review, or a generic Best-of-N prompt will improve a software change. [Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171) is the primary source.

Best-of-N also shifts cost to generation and selection. Chow et al. define BoN as a verifier selecting the best response from generated responses, and report task-specific results under their model, training, and benchmarks. Their paper supports treating the verifier as part of the method, not assuming the generator can grade itself. [Inference-Aware Fine-Tuning for Best-of-N Sampling](https://arxiv.org/abs/2412.15287) is the primary source.

Independent review remains a testable control rather than a guarantee. Kenton et al. found results varied by task when comparing oversight protocols, and reported that best-of-n sampling had little effect on judge accuracy in their setup. Do not generalize their result beyond that experiment. [On scalable oversight with weak LLMs judging strong LLMs](https://arxiv.org/abs/2407.04622) is the primary source.

## Failure modes

| Failure | Why it fails | Control |
| --- | --- | --- |
| Three paraphrases from one evolving conversation | Candidates share context and likely share mistakes | Isolate prompts, state, and artifacts before scoring |
| Rubric rewritten after a favored candidate appears | Selection becomes post-hoc rationalization | Freeze and version the rubric before generation |
| Majority vote over design proposals | Frequency hides untested requirements and shared bias | Score criteria and run executable checks |
| Generator approves its own patch | The same context can repeat the same blind spot | Use a deterministic gate or independent reviewer |
| Synthesis skips verification | The merge creates a new, unscored candidate | Assign a new ID and repeat selection and verification |
| Green unit tests presented as full proof | Tests cover only their declared environment and cases | Record coverage, failures, and `UNKNOWN` checks |

## Reusable skill and evidence record

Use the installable [Best-of-N skill](../../examples/skills/best-of-n/SKILL.md) to apply this protocol. The [verification evidence record](../../docs/resource-evaluations/best-of-n-verification-evidence.md) states the sources and local practitioner-evidence coverage used for this page.
