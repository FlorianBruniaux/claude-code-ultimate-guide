# Lexigraph: AI vocabulary and selective teaching adaptation

**Reviewed:** 2026-10-17. **Initial score:** 3/5. **Decision:** selective integration into [AI Concept Boundaries](../../guide/core/ai-concept-boundaries.md), with glossary and discovery links. The source is useful for explaining concepts, not evidence of an agent's measured performance or security.

## Source and scope

[Lexigraph](https://www.lexigraph.org/fr/) is directed by Anthony Capirchio and published by The Operating Shift. Its [editorial method](https://www.lexigraph.org/fr/a-propos/) discloses substantial model-assisted drafting under human-defined vocabulary, taxonomy, and writing rules, with named editorial responsibility.

The official [lexigraph-corpus repository](https://github.com/TheOperatingShift/lexigraph-corpus) exports the content as data under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Its README explicitly excludes the website's source code. `CITATION.cff` identifies version 1.0.0, released August 27, 2026. The archive downloaded for this review contains:

| Content | Verified records | Export |
|---|---:|---|
| Bilingual terms | 88 | `data/termes.jsonl` |
| Typed term relations | 260 | Term relation fields; also represented in `data/graphe.json` |
| Comparisons | 19 | `data/frontieres.jsonl` |
| Multiple-choice questions | 321 per language, 642 total | `data/qcm/fr.jsonl`, `data/qcm/en.jsonl`; CSV also supplied |
| Roles | 15 | `data/metiers.jsonl` |
| Practices | 15 | `data/pratiques.jsonl` |

Counts are observations of the downloaded export, not a claim that every website component is represented or every definition is technically correct. The review covers its structure and selected relevant entries, not an exhaustive factual audit of all 88 terms.

## What adds value to the guide

Lexigraph places terms on four floors: model, harness, agent, organisation. Its entries combine a short definition, a discussion of frequent confusion, technical explanation, dated examples, relations, and questions. The comparison pages connect that vocabulary to concrete decisions.

This complements the guide's [product-specific glossary](../../guide/core/glossary.md) and [operating layers](../../guide/core/agent-harness.md#0-four-layers-four-responsibilities). It does not replace them: runtime harness, repository harness, and orchestrator answer different engineering questions from Lexigraph's teaching floors.

The useful addition is a compact entry point for readers who need to distinguish concepts before following the detailed references. The existing guide already covers their implementations. Copying the full glossary would duplicate that coverage and import qualifications the source does not always make.

## Findings that limit direct reuse

### The export does not reproduce the full website

All 19 French comparison objects have empty `criteres` arrays. The inspected [Agent or Assistant page](https://www.lexigraph.org/fr/vs/agent-assistant/) includes a comparison table and four situations absent from that object's exported fields. The archive also has no infographic assets or guided-path exports. The site's [infographic collection](https://www.lexigraph.org/fr/infographies/) is a separate reuse route; the [harness planche](https://www.lexigraph.org/fr/infographies/le-harnais/) offers SVG, PNG, a slide-format PNG, and an interactive embed.

### Answer positions carry a shortcut

In the French question file, answer indices occur 59 times at index 0, 209 at index 1, and 53 at index 2. Always choosing the second option therefore gives 209/321, or **65.1%**, without reading the question. This is a property of the exported ordering; the site's display-time ordering was not tested.

Before using this bank as an assessment, verify the answers, shuffle choices while preserving the correct-answer mapping, and examine the distractors. These vocabulary questions are not a benchmark for coding agents or production safety. No Lexigraph questions are imported in this change.

To reproduce the structural findings, clone the public repository and run from its root:

```python
import json
from collections import Counter
from pathlib import Path

def records(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]

questions = records("data/qcm/fr.jsonl")
counts = Counter(q["answer"] for q in questions)
print("Questions:", len(questions), "Correct-answer positions:", dict(sorted(counts.items())))
print("Always second:", f"{counts[1] / len(questions):.1%}")
comparisons = records("data/frontieres.jsonl")
print("Empty French criteria:", sum(not row["fr"]["criteres"] for row in comparisons))
```

### Useful simplifications need boundaries

- The [Subagent entry](https://www.lexigraph.org/fr/sous-agent/) treats an initially empty context and the absence of communication/shared state as general properties. Context inheritance, transcript access, storage, and communication depend on the runtime and configuration. Do not transfer these claims as universal definitions.
- The [Context or Memory comparison](https://www.lexigraph.org/en/vs/context-memory/) suggests closing and reopening the conversation to distinguish persistence. Saved/resumed history can survive that operation without demonstrating a separate durable-memory mechanism. Inspect storage and loading behavior instead.
- The [Model or Product comparison](https://www.lexigraph.org/en/vs/model-product/) uses a supplier swap as a diagnostic boundary. Model and harness behavior interact; a model swap alone cannot establish ownership of a failure. Preserve the guide's model-harness evaluation unit.
- The [Workflow or Agent comparison](https://www.lexigraph.org/en/vs/workflow-agent/) helps identify adaptive action selection, but a prewritten workflow can contain an agent step. An approval pause does not remove agency, and "assistant" is also a product role. Classify the actual decision, not the name.
- A claim that the harness is deterministic needs component-level qualification: it may invoke probabilistic model-based routing, selection, or review. Written rules also do not acquire deterministic enforcement merely by being placed outside the model.

These observations justify rewriting the explanations rather than copying the source's tests verbatim. Product statements are checked against Anthropic's [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) and [Permissions](https://code.claude.com/docs/en/permissions); protocol roles use the [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture). Detailed security and evaluation guidance remains in this guide's existing references.

## Integration and attribution

| Destination | Integrated material |
|---|---|
| [AI Concept Boundaries](../../guide/core/ai-concept-boundaries.md) | Six practical distinctions, repository examples, inspection questions, and six original exercises with corrections |
| [Glossary](../../guide/core/glossary.md) | Pointer to the comparison guide without duplicating its explanations |
| [Guide index](../../guide/README.md), [repository README](../../README.md) | Beginner and engineering entry points |
| [Machine-readable index](../../machine-readable/reference.yaml) | Page and section routing, source evaluation |
| [Machine-readable README](../../machine-readable/README.md), [LLM overview](../../machine-readable/llms.txt) | Discovery and scope of the adaptation |

Credit Anthony Capirchio / The Operating Shift and link to Lexigraph and CC BY 4.0. State that explanations, examples, and exercises were rewritten and qualifications added. The source licence permits adaptation and commercial reuse with its attribution conditions; it does not imply that Lexigraph endorses the guide. See [Lexigraph's citation guidance](https://www.lexigraph.org/fr/citer/).

No corpus ingestion pipeline, imported question bank, copied infographic, or new runtime behavior is part of this integration. No human learning outcome, model performance, or live sandbox behavior was measured.

## Review decision

**Final score: 3/5.** A separate technical-writer reviewed the adapted guide, attribution, and machine-readable placement, retained the selective-integration score, and identified a broken MCP chapter anchor, which was corrected. That review did not independently remeasure the corpus. Useful teaching structure and reusable bilingual data remain balanced by limited novelty over the existing technical chapters, incomplete exports, and runtime-dependent generalizations.
