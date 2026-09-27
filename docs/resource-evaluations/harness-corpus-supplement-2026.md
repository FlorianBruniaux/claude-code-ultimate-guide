# Harness evidence: review constraints, memory migration and tool recovery

**Reviewed:** 2026-09-27. **Decision:** selective integration; technical challenge completed.

This supplement adds six sources to the existing harness coverage. Video passages were checked against timestamped transcripts. Three research preprints were checked in their primary texts. None of the reported experiments was reproduced for this guide.

## Research papers

| Source | Initial / final score | Contribution and boundary | Integration |
|---|---|---|---|
| [SWE-Gate](https://arxiv.org/html/2609.04167v1) | 4/5 / 4/5 | Separates functional repair from review constraints using 303 synthesized instances from 75 Python repositories. Four model backends; results are not a production PR failure rate. [Replication repository](https://github.com/DeepSoftwareAnalytics/SWE-Gate) inspected, not executed. | [Test review constraints separately](../../guide/core/agent-harness.md#test-review-constraints-separately) |
| [Does Your Agent's Memory Survive a Model Upgrade?](https://arxiv.org/html/2609.05339v1) | 3/5 / 3/5 | Controlled migration of memory writers, readers and embedding models. Synthetic histories, two small open-weight language models, directional effects; code and histories available on request. No universal best memory format established. | [Test memory migration](../../guide/core/memory-systems.md#test-memory-migration) |
| [Necessary or Sufficient?](https://arxiv.org/html/2609.05385v1) | 3/5 / 3/5 | Tests cited explanation features through input interventions across eight model configurations and two synthetic decision tasks. The data are not released. This is not a code-review or human-learning experiment. | [Verify](../../guide/roles/learning-with-ai.md#v-verify-explain-it-back) |

## Practitioner videos

These AI Engineer talks describe their speakers' methods. They do not independently establish gains in review accuracy, recovery reliability or cost.

| Source and date | Initial / final score | Checked passage | Integration |
|---|---|---|---|
| **Will Bond and Ameya Ketkar, Uber**, *Building uReview*, 2026-08-28 | 3/5 / 3/5 | [05:11](https://www.youtube.com/watch?v=EL123UNokkI&t=311s): reply sentiment and address-rate tracking. [07:03](https://www.youtube.com/watch?v=EL123UNokkI&t=423s): bounded review time, team customization and single-file/multi-file roles. | [Role separation](../../guide/workflows/multi-provider-code-review.md#role-separation), [review metrics](../../guide/roles/agent-evaluation.md#separate-review-uptake-from-correctness) |
| **Ishaan Sehgal, Omnara**, *The Log Is The Agent*, 2026-06-25 | 3/5 / 3/5 | [04:19](https://www.youtube.com/watch?v=UPwGaM2MKHY&t=259s) and [04:57](https://www.youtube.com/watch?v=UPwGaM2MKHY&t=297s): compacted context is a lossy view of recorded history. | [History and compaction](../../guide/core/memory-systems.md#keep-history-distinct-from-compaction); retaining a log does not reconstruct external effects or authorize indefinite retention. |
| **Michael Hablich, Google**, *Building Agent Interfaces: Lessons from Chrome DevTools (MCP) for Agents*, 2026-06-05 | 3/5 / 3/5 | [13:14](https://www.youtube.com/watch?v=_B4Pv9ttFgY&t=794s): useful tool errors. [21:56](https://www.youtube.com/watch?v=_B4Pv9ttFgY&t=1316s): recovery playbooks and tokens per successful outcome. | [Actionable tool failures](../../guide/core/loop-graph-engineering.md#make-tool-failures-actionable); the guide's proposed error fields require adapter tests. |

## Selection and interpretation

The search was targeted, not systematic: seven video queries with bounded result limits and a 120-paper metadata snapshot, followed by full-text inspection of the three retained papers. Earlier videos already cited in the harness guide were excluded from this supplement. Metadata matches alone did not qualify a paper for integration.

The additions support concrete evaluation questions: did the patch satisfy its constraints; did migration preserve retrieval; did an explanation predict behavior; did a review lead to a verified correction? The guide's examples and proposed practices remain distinct from the source authors' experimental results.

## Technical challenge

An independent technical-writer review checked the six additions against the primary papers and resolved video passages. No blocking finding remained. Its precision correction was applied: the explanation result concerns feature scores under tested input interventions, without access to internal reasoning. Final scores remain 4/5 for SWE-Gate and 3/5 for the other five sources. These are editorial integration scores, not production validation.
