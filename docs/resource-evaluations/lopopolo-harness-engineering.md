# Lopopolo: Harness Engineering anthology

**Reviewed**: 2026-10-17. **Editorial relevance**: 4/5, selective integration. This score measures usefulness to the guide, not runtime quality or productivity.

## Source and evidence boundary

[lopopolo/harness-engineering](https://github.com/lopopolo/harness-engineering/tree/226c8d35fb6ea3ed55467753dba6dea2b5fd5778) is an anthology and context corpus organized around twelve theses, cases, playbooks, and archived sources. It is not an agent runtime and is not added to the Agent Harness Map as one.

The review covered the twelve theses, architecture and routing documentation, both playbooks, evaluation methodology, the Artichoke case, and selected linked sources. The source manifest declares 91 sources; this is not a claim that every archived source was read. No agent benchmark or end-to-end playbook application was run.

The [playbook introduction](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/playbooks/README.md) identifies the procedures as editorial synthesis and includes no end-to-end application record. The [licensing statement](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/COPYING.md) distinguishes original CC BY 4.0 prose from third-party material. The guide adapts concepts with attribution rather than reproducing the archive.

## What adds value

| Concept | Existing coverage | Integration |
|---|---|---|
| Keep each kind of truth with its owner | External context already covered in Agent Harness Engineering; main guide incorrectly restricted knowledge to the repository | Correct the knowledge boundary and distinguish stable contracts, organizational knowledge, and live state |
| Recoverable nonfunctional requirements and one semantic owner | Architecture, linting, and anti-entropy already covered | Add requirement → owner → representation → evidence examples; distinguish derived representations from competing definitions |
| Code as a precedent for the next change | Canonical patterns and migrations already discussed | Explain why incomplete migrations leave competing examples; repair the scoped population and evaluate retiring redundant checks |
| MLD telemetry | Executor's three files and memory promotion already covered | Distinguish self-report, corroboration, candidate intervention, and active guidance |
| Curated-context publication | PR-based curation already covered | Isolate candidates, check persistence rights and audience, pin published revisions, separate self-feedback from approval, and define expiry |
| Worker epochs and four clocks | Model-harness evaluation and accepted-task cost already covered | Requalify after material changes; distinguish feedback, run duration, human attention, and time to accepted outcome |

Primary concept sources: [domain modeling](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/docs/domain-modeling/README.md), [truth ownership](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/docs/last-mile-deployment/README.md#keep-each-kind-of-truth-with-its-owner), [MLD](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/docs/feedback/mld.md), [context curation](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/docs/just-in-time-context/README.md#curate-the-route-beside-each-goal), [worker qualification](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/docs/fixed-worker/README.md), and [four clocks](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/docs/effectiveness/README.md#keep-four-clocks).

## Challenge and decision

The contribution is a clearer engineering model, not a new executable capability. Most foundations were already present, so integration extends existing sections rather than creating another general harness guide. Proposed curation architectures and self-reported cases do not establish reliability, security, or measured gains. MLD cannot prove honest or complete reporting or causal attribution. The historical Artichoke case is not an executed agent evaluation and is not used as capability evidence here.

The 4/5 score rests on correcting an internal contradiction and strengthening several existing contracts. A claim that the anthology demonstrates local performance gains would exceed the evidence.

A separate technical-writer review checked attribution, evidence limits, score justification, and integration links. It retained 4/5 and identified two navigation/template consistency issues, corrected in the integration. This documentary challenge does not validate runtime behavior.

## Integrated locations

- [Main guide: knowledge boundary](../../guide/ultimate-guide.md#9252-what-the-agent-cant-see-doesnt-exist) and [local quality bar](../../guide/ultimate-guide.md#make-the-local-quality-bar-recoverable).
- [Memory: MLD observations](../../guide/core/memory-systems.md#mld-observations-for-the-harness-builder).
- [Context update loop](../../guide/core/context-engineering.md#the-update-loop) and [publication contract](../../guide/core/context-engineering.md#publication-contract-for-curated-context).
- [Evaluation epochs and four clocks](../../guide/roles/agent-evaluation.md#evaluation-epochs-and-four-clocks).

Blog extensions remain separate editorial proposals. This evaluation does not establish that any portfolio article was changed or published.
