# From SDLC to ADLC (rakesh Gohel, LinkedIn, sep 2026)

## Evaluation metadata

| Field | Value |
|---|---|
| Resource | LinkedIn post and infographic "The SDLC is dead. Long live the ADLC." (no stable public URL recorded) |
| Author | Rakesh Gohel |
| Published | Week of 2026-09-21 |
| Evaluated | 2026-09-29 |
| Resource type | Social post summarizing a vendor playbook |
| Primary source | Anthropic, [The AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), already evaluated in [2026-08-26-anthropic-ai-native-sdlc-playbook.md](./2026-08-26-anthropic-ai-native-sdlc-playbook.md) |
| Decision | Do not integrate the post; two corrections made from the primary source it summarizes |
| Score | 2/5 |

## Verdict

The post restates the Anthropic playbook stage by stage (intent.md, skills, CLAUDE.md, hooks, continuous evals, layered review, Maintain looping back to Plan) under a new label, "ADLC". The guide integrated the playbook's two gaps on 2026-08-26. The post adds no mechanism, measurement or example beyond its source.

Re-reading the primary source to check the post surfaced two improvements, both sourced to the playbook, not to the post:

1. **The Maintain loop has a human triage step.** The guide's diagram sent a production anomaly straight to a product approval. The playbook says a trigger invokes Claude "with no person in the invocation path", then "the service owner or on-call engineer triages the queue", with "Fix now, schedule, or dismiss", and routes only product-facing findings to the product owner. Fixed in `guide/diagrams/06-development-workflows.md`.
2. **The document chain is an audit trail.** The playbook: "Together, the intent, the spec, the plan, the diff and the review findings are the audit trail." The guide's traceability page covered only the execution trail (session logs). Added in `guide/ops/ai-traceability.md`.

A naming note was added to `guide/workflows/spec-first.md`: the playbook treats agentic SDLC, AI SDLC and agentic software development as synonyms, and "ADLC" already names a different thing, the *Agent* Development Lifecycle used by [Salesforce](https://architect.salesforce.com/docs/architect/fundamentals/guide/agent-development-lifecycle.html) and [IBM](https://www.ibm.com/think/topics/agent-development-lifecycle-adlc) for building and operating agents as products.

## Claims rejected

| Claim in the post | Reason |
|---|---|
| "The SDLC is dead" | Opinion framing. The playbook keeps a human gate at every stage. See also the earlier rejection of the same thesis in [2026-02-26-boristane-sdlc-dead.md](./2026-02-26-boristane-sdlc-dead.md) |
| "Every gate in that process existed for one reason: writing code was slow and expensive" | Unsupported. Gates also exist for risk, compliance and accountability, and operator accounts in the guide show verification, not code, becoming the bottleneck (`guide/workflows/agentic-software-factories.md` §5) |
| "The build phase collapses to hours" | No measurement given |
| "No human starts it" (Maintain) | Accurate for the invocation only; omits the triage gate the source describes |
