# Evaluating AGENTS.md: corrected evidence boundary

**Source**: [Gloaguen et al., Evaluating AGENTS.md, v1](https://arxiv.org/html/2602.11988v1).
**Reviewed**: 2026-09-26. **Relevance**: 4/5, selective integration.

## What changed in this evaluation

This revision replaces the February evaluation's overgeneralized cost, success and file-length claims. The previous record called the arXiv paper peer-reviewed without establishing a venue and treated a scoped experiment as validation of a universal short-file rule. Those claims are withdrawn; this evaluation treats the cited version as a preprint.

The study compares context-file conditions on Python repository tasks. The human-written condition exists only on AGENTbench. Results vary by agent and dataset. Consult sections 4.1 to 4.3 for the specific configuration behind each number; inference cost and reasoning-token overhead are separate measures.

## Integration decision

Keep the guide's practical recommendation to inspect instruction relevance and test a smaller candidate. Do not present a line count, a fixed cost surcharge or harm from every generated file as experimentally established.

The comparison motivates an evaluation of a repository's own instructions. It does not supply measurements for the guide reader's configuration, current model versions or a refactored file that the study did not test. Describe a proposed cleanup as a hypothesis until its task outcomes are observed.

## Review and remaining work

The related [harness evidence evaluation](./harness-evidence-marmelab-2026.md) records the integration and technical challenge. This correction changes the current recommendation; older resource evaluations quoting the previous figures remain historical records and should not substitute for the cited primary version.

No local agent campaign was executed. The study's dataset and experiments were not independently reproduced during this editorial revision.
