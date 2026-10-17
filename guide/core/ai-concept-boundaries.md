---
title: "AI Concept Boundaries"
description: "Seven practical distinctions for Claude Code, from context and memory to model architecture, size, modality, and task labels."
tags: [guide, concepts, learning]
---

# AI concept boundaries

When a system forgets a preference, calls the wrong tool, or passes a test, identify which component owns that behavior before changing the model or adding instructions. These seven distinctions give you a question to ask, an example, and a route to the detailed reference.

The comparison format and selected distinctions are adapted from Anthony Capirchio's [Lexigraph](https://www.lexigraph.org), published by The Operating Shift under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Explanations and exercises are rewritten for repository work, with product-specific limits added. [Sources and adaptation](#sources-and-adaptation) records the scope.

## Context, context window, and memory

**Context** is the information supplied for the current model call: messages, instructions, tool descriptions, retrieved material, and tool results. The **context window** is the model's capacity for that information and generation, subject to its input/output limits. **Memory** is information retained so the system can retrieve or load it into a later context.

Ask **what is available now, what could fit, and what will be retained?** A preference written in `CLAUDE.md` can be loaded in another session. A test log seen in one session is current context; it does not thereby become a durable project instruction. A larger window does not decide which logs or preferences the runtime will include.

Closing a chat is not a reliable memory test: a product may save and resume the conversation. Check the stored artifact, loading rules, and new session's available context. Storage, retrieval, and model training are separate operations. Text-only examples also simplify multimodal contexts, which can include images and other supported inputs.

Continue with [Context Engineering](./context-engineering.md) and [Memory Systems](./memory-systems.md).

## Model, product, and harness

A **model** generates outputs from its inputs. A **product** combines a model with an interface and operating behavior. A **runtime harness** assembles context, mediates tools and permissions, manages state, and runs the agent loop. A **repository harness** supplies project-specific instructions, setup, and verification gates.

Ask **which component could change the behavior, and how would you isolate its effect?** If an agent edits the wrong generated file because the repository has no source-of-truth instruction, improving that instruction is a candidate intervention. If the instruction was supplied correctly but misunderstood, model behavior is also a candidate. Inspect the trace before assigning the cause.

Switching models can change tool choices, reasoning, and instruction following. Switching harnesses can change what the model sees and is allowed to do. Evaluate the actual combination; neither swap alone diagnoses the fault. Lexigraph's model/harness/agent/organisation floors help locate concepts, while this guide's operating layers distinguish runtime, repository, and orchestration responsibilities.

Continue with [Four Layers, Four Responsibilities](./agent-harness.md#0-four-layers-four-responsibilities) and the [Harness Glossary](./glossary.md).

## Assistant, workflow, and agent

An **assistant** describes a user-facing role. A **workflow** defines steps and branches in advance. An **agent** lets a model select actions within an iterative process that observes results and works toward an objective. One product can combine all three.

Ask **who chooses the next action at this point?** A pipeline that runs the formatter, tests, and report in a fixed order is a workflow. Claude choosing which file to inspect after a failing test is an agent decision. A workflow can invoke that agent at one step and still control the surrounding sequence.

An approval pause does not turn an agent into a non-agent. Conversely, running unattended does not make a fixed script an agent. The name "assistant" alone says nothing about whether the underlying system uses an agent loop. Identify the actual decision boundary, stopping rule, and permission scope.

Continue with [Loop & Graph Engineering](./loop-graph-engineering.md) and [Architecture](./architecture.md).

## Tool and MCP

A **tool** exposes an operation to the agent, with inputs and a result. **MCP** standardizes communication between a host and servers that expose tools, resources, or prompts. The protocol connects capabilities; it does not establish that a particular service is trustworthy or that its operations are authorized.

Ask **what operation is exposed, who executes it, and under whose credentials?** A local file reader and an MCP server that reads an issue are both capabilities the agent can use. The server may execute remotely, and the host decides how its exposed tools enter the agent's session. Inspect credentials and side effects for each operation, even when the transport is familiar.

A connected tool need not be allowed to run without approval. A successful connection also says nothing about the correctness of its results or the instructions embedded in returned content.

Continue with [Tools Reference](./tools-reference.md), [MCP Integration](../ultimate-guide.md#8-mcp-servers), and the [MCP server ecosystem](../ecosystem/mcp-servers-ecosystem.md).

## Instructions, permissions, and sandbox

**Instructions** tell the model how to behave. **Permissions** determine which tool requests may execute or require approval. A **sandbox** restricts access at the execution environment boundary, according to its configuration. These controls have different owners and failure modes.

Ask **what stops the action if the model requests it anyway?** "Do not read credentials" in `CLAUDE.md` is a behavioral instruction. An enforced read restriction is an access control. A network restriction limits reachable destinations. Test the relevant control with synthetic data in a disposable environment, including both an allowed operation and a prohibited one.

A separate Git worktree separates working files and branches; it is not a filesystem or network sandbox. Sandbox coverage and escape paths depend on the runtime, platform, tools, and configuration. Instructions still matter, but a written prohibition is not evidence of enforcement.

Continue with [Native Sandbox](../security/sandbox-native.md), [Sandbox Isolation](../security/sandbox-isolation.md), and [Production Safety](../security/production-safety.md).

## Evaluation and production evidence

An **evaluation** measures a specified system on selected cases, using defined criteria and judges. **Production evidence** comes from observed use in the deployed environment. A passing evaluation establishes results for its cases and conditions; production observations also remain bounded by what was measured.

Ask **what was tested, against which criterion, and what remains outside that observation?** A patch can pass a unit test while a live integration fails because of credentials, permissions, or a different response schema. A mocked provider check establishes behavior against the mock, not a successful call to the real provider.

Evaluate the path as well as the final answer: unauthorized side effects, retries, cost, and recovery can change whether a task counts as successful. Vocabulary questions test recognition of concepts. They do not establish coding ability, security enforcement, or safe operation of an agent.

Continue with [Agent Evaluation](../roles/agent-evaluation.md) and the [Best-of-N verification workflow](../workflows/best-of-n.md).

## Architecture, size class, modality, and task

Model names mix several **axes**. A **model class** such as a large language model (LLM) says what kind of system it is: a language model trained on large text corpora. An **architecture** describes the internal design: a dense decoder transformer runs all its parameters for each token, while a mixture-of-experts (MoE) model routes each token to a few expert sub-networks. A **size class** such as a small language model (SLM) is a loose label for a model small enough for constrained hardware. An **input modality** describes what the model accepts: a vision-language model (VLM) takes images as well as text. A **training objective** describes how the model learned: masked language modeling (MLM) predicts hidden tokens from both sides. A **task or product label** describes what the system is for: "large action model" (LAM) and image segmentation, as in the Segment Anything Model (SAM). A **representation unit** describes what the model predicts: a large concept model (LCM) predicts sentence embeddings instead of tokens.

Ask **which axis does this term describe, and does it change anything you configure or observe in Claude Code?** A post that lists eight model "architectures" side by side mixes axes. MoE, SLM, and VLM are not alternatives: one model can be a small, MoE, vision-language model. Two axes show up in your sessions: input modality, through image context cost, and architecture, when you choose local models.

[![Eight terms, seven axes: LLM is a model class, MoE an architecture, SLM a size class, VLM an input modality, MLM a training objective, LAM and SAM task or product labels, and LCM a representation unit. One model can be small, MoE and vision-language at once.](../images/model-axes/model-axes-en-gemini.webp)](../images/model-axes/model-axes-en-gemini.webp)

*The eight terms sit on seven different axes, so they are not alternatives to choose between. Open the image for full size. [Image provenance](../images/model-axes/README.md).*

| Term | Axis | What changes for a Claude Code user | Read next |
|------|------|-------------------------------------|-----------|
| LLM | Model class: a language model trained on large text corpora, typically a transformer that generates one token at a time | Claude's underlying model is autoregressive, so output is generated token by token ([Anthropic glossary](https://platform.claude.com/docs/en/about-claude/glossary)) | [Context Engineering](./context-engineering.md) |
| MoE | Architecture: expert feed-forward blocks chosen per token by a router | Anthropic does not document Claude's architecture, so do not assume either way. It matters when you pick local models: memory follows total parameters, compute follows active ones ([Mixtral](https://arxiv.org/html/2401.04088)) | [Local vs cloud inference](../ecosystem/local-vs-cloud-inference.md#what-actually-fits-named-models) |
| SLM | Size class: the Phi-3 report sets no threshold and describes its model by parameter count and on-device deployability ([Phi-3 report](https://ar5iv.labs.arxiv.org/html/2404.14219)) | Matters for local deployment. Quantization is a separate technique that lowers weight precision; llama.cpp applies it to models from 8B to 405B parameters ([llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md)) | [Local vs cloud inference](../ecosystem/local-vs-cloud-inference.md#what-actually-fits-named-models) |
| VLM | Modality: in LLaVA's design, a vision encoder, a projection, and a language model ([LLaVA](https://arxiv.org/abs/2304.08485)); Anthropic does not describe Claude's vision pipeline | Screenshots and images consume context tokens ([Anthropic vision docs](https://platform.claude.com/docs/en/build-with-claude/vision)) | [Images and screenshots](../ultimate-guide.md#working-with-images-and-screenshots) |
| MLM | Training objective: predict masked tokens, used to pre-train encoder models such as [BERT](https://arxiv.org/abs/1810.04805) | Not how Claude generates text. It is a pre-training objective, not a product feature | None |
| LAM | Task or product label with competing meanings: a product concept ([Rabbit r1](https://en.wikipedia.org/wiki/Rabbit_r1)) and language models tuned for function calling ([xLAM](https://arxiv.org/abs/2409.03215)) | In Claude Code, actions come from tool use in the agent loop, bounded by permissions | [Computer use](./computer-use.md), [The master loop](../diagrams/04-architecture-internals.md#the-master-loop) |
| LCM | Representation unit: sentence-level SONAR representations, continuous embeddings in most variants and discrete units in the quantized one ([LCM paper](https://arxiv.org/html/2412.08821)) | No direct Claude Code use | None |
| SAM | Task or product label: promptable image segmentation ([SAM paper](https://arxiv.org/abs/2304.02643)) | No direct Claude Code use | None |

These labels are not exclusive categories, and the table simplifies each one. Vendor labels such as LAM lack a shared specification, so ask what the system does and which components it contains. Token costs for images and the supported image sizes depend on the model and can change, so check the vision documentation for current figures.

Continue with [Local vs cloud inference](../ecosystem/local-vs-cloud-inference.md) and [Three model pipelines](../diagrams/04-architecture-internals.md#three-model-pipelines-dense-moe-and-vlm).

## Check your understanding

These seven original scenarios check the distinctions above. They are reading exercises, not a validated assessment or a measurement of practical proficiency. Explain your answer before opening the correction.

1. You enlarge the context window, start a new session, and a coding preference is still missing. What must you inspect?
2. A model switch makes a previously working tool sequence fail. Can you conclude that the harness is correct because its code did not change?
3. A fixed CI pipeline invokes an agent to investigate a failure, then pauses for review. Which parts are workflow, agent, and human judgment?
4. An MCP server connects successfully. Does that authorize its tool to send an email?
5. An agent works in a separate Git worktree. Does that prevent it from reading a sibling directory or reaching the network?
6. A mocked integration test and all vocabulary exercises pass. What can you report about production readiness?
7. A teammate proposes replacing Claude with "a LAM instead of an LLM" to get tool execution. What should you ask first?

<details>
<summary>Corrections and what to inspect next</summary>

1. Inspect whether the preference was stored, where it lives, and whether the new session loaded it. Window capacity is separate from persistence and selection. Revisit [context and memory](#context-context-window-and-memory).
2. No. The model-harness combination changed. Inspect the supplied schemas, tool requests, execution results, and failure traces before assigning responsibility. Revisit [model and harness](#model-product-and-harness).
3. The fixed pipeline is the workflow, the model's adaptive investigation is the agent loop, and the reviewer supplies the approval judgment. The pause preserves an authority boundary. Revisit [workflow and agent](#assistant-workflow-and-agent).
4. No. Connectivity, operation availability, credentials, and authorization are separate checks. Sending requires the applicable permissions and user authorization. Revisit [tool and MCP](#tool-and-mcp).
5. No. A worktree does not itself restrict operating-system access. Inspect the actual filesystem, network, and credential restrictions. Revisit [execution controls](#instructions-permissions-and-sandbox).
6. Report the mock behavior and conceptual understanding checks that passed. Live-provider behavior and deployed operation remain unverified by those checks. Revisit [evaluation evidence](#evaluation-and-production-evidence).
7. Ask which axis "LAM" describes. The label has competing meanings and no shared architecture. In Claude Code, actions come from tool use and permissions in the harness, so check which tools and permissions the harness grants. Revisit [model axes](#architecture-size-class-modality-and-task).

</details>

## Sources and adaptation

- **Attribution:** Anthony Capirchio / The Operating Shift, [Lexigraph corpus v1.0.0](https://github.com/TheOperatingShift/lexigraph-corpus), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Selected distinctions and the definition/comparison/exercise teaching structure are adapted; wording and repository examples are rewritten here, and all exercises are written for this guide. Product-dependent generalizations are qualified. This attribution does not imply endorsement.
- **Lexigraph reading:** [Context or Memory](https://www.lexigraph.org/en/vs/context-memory/), [Model or Product](https://www.lexigraph.org/en/vs/model-product/), and [Workflow or Agent](https://www.lexigraph.org/en/vs/workflow-agent/). The English and French corpus can support further learning; its four floors are a teaching taxonomy, not an implementation specification.
- **Product references:** Anthropic's [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works), [Memory](https://code.claude.com/docs/en/memory), [Permissions](https://code.claude.com/docs/en/permissions), and [Sandboxing](https://code.claude.com/docs/en/sandboxing). Protocol roles are described in the [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture).
- **Seventh distinction:** The architecture, size class, modality, and task section and its exercise are original to this guide and are not adapted from Lexigraph. Sources are linked in its table.
- **Reuse limits:** See the [Lexigraph evaluation](../../docs/resource-evaluations/lexigraph-ai-lexicon.md) for export gaps, answer-position bias, and the reasons for selective adaptation. No source quiz bank, infographic, or site code is imported into this page.
