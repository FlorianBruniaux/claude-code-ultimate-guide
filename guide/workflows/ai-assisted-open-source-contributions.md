---
title: "AI-Assisted Open Source Contributions"
description: "Prepare reviewable contributions with Claude Code: project policy, reproduction, independent evidence, author understanding, and follow-through"
tags: [guide, workflow, community, code-review]
---

# AI-Assisted Open Source Contributions

A maintainer needs enough evidence to decide whether a change belongs in the project. Generating a patch does not supply that evidence or commit its author to maintaining it. Use this workflow when Claude Code helps prepare a contribution to someone else's repository.

In [IFTTD episode 372](https://www.ifttd.io/episodes/dev-ai), Gabriel de Marmiesse describes the burden of unchecked generated issues and pull requests and predicts a loss of trust in open source. That prediction is a practitioner opinion. The workflow below is a proposed response, not a measured reduction in maintainer workload.

## 1. Check whether the project wants this contribution

Read the project's contribution guide, issue templates, security reporting policy, and any AI-assistance policy. If AI-generated submissions are prohibited, do not use this workflow to evade that rule. Follow its disclosure requirements without posting private prompts, credentials, or unrelated session logs.

Check for an existing issue or patch. If the project requires discussion before a feature, prepare the proposal before generating the implementation. A maintainer declining an unsolicited feature is not a failed code review. Keep suspected vulnerabilities within the project's designated security channel.

## 2. Establish the problem before editing

Record the affected version, environment, expected behavior, actual behavior, and minimal reproduction. Run the reproduction on the unchanged revision. For a documentation correction, identify the inaccurate passage and the authoritative source instead of manufacturing an executable test.

In [IFTTD episode 362](https://www.ifttd.io/episodes/le-lean-a-l-ere-de-l-ia), Yacine Hmito separates reproduction, investigation, correction, and validation into individually inspectable artifacts. Apply that separation to a contribution: if the problem cannot be reproduced or otherwise established, label it as an investigation and keep the patch unsubmitted.

## 3. Keep the patch and the claim narrow

Ask Claude Code to change only what is necessary for the established behavior. Exclude unrelated formatting, speculative refactoring, and generated files the project expects its build to produce. Review the full diff yourself, including dependency and test changes.

Use this prompt after identifying the relevant project commands and policy:

```text
Prepare a local patch for the reproduced issue below.
Read this project's contribution and AI-assistance policies first.
State the expected behavior and the minimal reproduction before editing.
Preserve unrelated changes. Do not change acceptance criteria to make a test pass.
Run the relevant checks allowed by the project; record commands, revision,
outcomes, and anything not verified. Explain the cause and the change.
Stop with a local diff and a draft contribution packet. Do not submit or push.
```

The prompt defines the requested work; it does not enforce permissions. Configure the actual tool and repository access separately. See [Production Safety](../security/production-safety.md).

## 4. Verify the change and explain it without the agent

For a bug fix, check that the regression test exposes the original defect and succeeds with the patch. Distinguish an expected assertion failure from a setup failure. Run the project's relevant regression checks and record the exact revision. If the patch changes, invalidate evidence affected by that change.

Explain the root cause, why the patch addresses it, what nearby behavior could regress, and which checks support the claim. If you cannot explain those points, continue the investigation before asking a maintainer to reconstruct them. A second agent can challenge the patch, but agreement between models is not independent proof of correctness.

Use the [contribution packet template](../../examples/templates/ai-assisted-contribution.md). Report unexecuted checks explicitly. Do not mark a checkbox because the model says it ran a command.

## 5. Submit only when the packet is ready, then own the follow-up

Follow the project's submission process and the user's authorization for external actions. Supply the smallest useful description, reproduction and evidence. Do not mass-submit generated patches to unrelated projects or let an agent answer maintainer feedback without understanding the requested change.

When feedback identifies a defect, reproduce it and update the patch and evidence. If the same correction recurs, consider a test, example or instruction in your own workflow. A maintainer remains free to reject a technically correct change because of product direction or maintenance cost.

## Worked readiness decision

**Constructed example, not an executed repository test:** a parser rejects a documented valid date. The contribution packet identifies the affected release, provides one input, and explains the boundary condition. Its regression test fails on the unchanged release with the expected assertion and passes on the patch; the relevant parser suite also passes. This is ready for maintainer review, not guaranteed acceptance or proof of every parser behavior.

Reject the same packet as unready if it only says “Claude fixed it; tests pass,” if the baseline failed because a dependency was missing, or if the patch changed the expected result to match the defect. Ask the author to supply or repair the missing evidence before submission.

## Related workflows

- [Code Review](code-review.md) for examining a patch
- [TDD with Claude](tdd-with-claude.md) for establishing a regression test
- [Learning with AI](../roles/learning-with-ai.md) for testing author comprehension
- [Review admission control](../core/loop-graph-engineering.md#limit-admission-to-verification-capacity) for a saturated shared review queue
