---
name: review-comprehension-exercise
description: "Assess explanation, diagnosis and escalation separately from delivery output"
complexity: beginner
time: varies
domain: testing
status: experimental
keywords: [learning, comprehension, review, mentoring]
---

# Explain, perturb, diagnose, escalate

Use a disposable local exercise with synthetic data and a known behavior. This worksheet proposes an assessment; it has not established that review-based training produces the same learning as writing code.

1. **Explain.** Before asking an assistant, describe the input, output, invariant and one boundary case of a small change. The mentor records mistakes and prompts needed.
2. **Perturb.** The mentor changes one assumption, such as an empty input or a duplicate identifier. Predict the result, then run a relevant check. Distinguish a wrong prediction from a broken test environment.
3. **Diagnose.** Investigate one seeded defect. Produce reproduction steps, a causal explanation and a minimal correction. An assistant may be enabled for this round, but record its interventions separately from the learner's reasoning.
4. **Escalate.** Introduce a requirement outside the agreed scope, such as a change to authorization. The learner must identify the missing decision and request the appropriate review rather than silently broaden the patch.

| Observation | Independent | With prompt/help | Not demonstrated |
|---|---|---|---|
| Explains the invariant and its source | | | |
| Predicts the changed boundary case | | | |
| Reproduces and diagnoses the defect | | | |
| Identifies an authority or knowledge boundary | | | |

Repeat with a different but comparable task and reverse assisted/unassisted order across learners where practical. Record prior familiarity and mentor interventions. Do not reuse the same solution as proof of transfer. A correct escalation is a successful boundary decision, not a failed coding task.

Save the assessment separately from delivery metrics. A merged change does not establish independent understanding, and one exercise does not qualify someone for unrestricted production access.
