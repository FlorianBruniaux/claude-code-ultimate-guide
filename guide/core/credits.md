---
title: "Credits and External Inspirations"
description: "Open-source projects and engineering teams whose work informed specific patterns in this guide"
tags: [credits, attribution, open-source]
---

# Credits and External Inspirations

This guide documents patterns from the Claude Code community. Some sections are directly inspired by open-source repos, blog posts, or public engineering work. This page consolidates attributions in one place.

---

## Packmind Engineering Team

**Repo**: [github.com/packmind/packmind](https://github.com/packmind/packmind)
**Author**: Cédric Teyton (CTO, Packmind)
**License**: Apache 2.0

Packmind maintains a production Claude Code configuration in their open-source repo. Several patterns documented in this guide were inspired by their `.claude/` setup:

### Pattern 1: MCP Reference File

**Guide section**: [Documenting an MCP for Claude](../ecosystem/mcp-servers-ecosystem.md#documenting-an-mcp-for-claude-the-reference-file-pattern)
**Source**: `.claude/skills/datadog-analysis/references/datadog_mcp.md`

A `references/<mcp-name>.md` file read by the skill before any MCP call. Captures query syntax gotchas, required parameter combinations, working examples, and noise exclusion rules specific to one MCP server.

### Pattern 2: Skeptical Reviewer Sub-Agent

**Guide section**: [Pattern: Skeptical Reviewer Sub-Agent](../ultimate-guide.md#pattern-skeptical-reviewer-sub-agent)
**Source**: `.claude/skills/playbook-audit/references/report-agent.md`

A fourth agent in a multi-agent audit pipeline whose job is to reject false positives from the first three agents. Operates with explicit false-positive criteria and requires evidence from both artifacts before keeping any finding.

### Pattern 3: Shared Ground Truth Injection

**Guide section**: [Skill Design Patterns](./skill-design-patterns.md#shared-ground-truth-injection)
**Source**: `.claude/skills/doc-audit/SKILL.md`

The orchestrator computes a shared factual baseline (nav structure, CLI commands, file list) once, then injects the same block into all parallel sub-agent prompts. Prevents each sub-agent from re-discovering the same facts independently.

### Pattern 4: Pre-filtered References via Frontmatter Paths

**Guide section**: [Skill Design Patterns](./skill-design-patterns.md#pre-filtered-references-via-frontmatter-paths)
**Source**: `.claude/skills/qa-review/SKILL.md`

The orchestrator reads rules files, parses `paths:` frontmatter glob patterns, matches them against modified files, and passes only applicable rules to each review agent. Progressive disclosure applied to standards, not just documentation.

### Pattern 5: Handoff Triad with Merge Semantics

**Guide section**: [Session Handoff Pattern](../ultimate-guide.md#session-handoff-pattern) and templates at `examples/commands/handoff/`
**Source**: `.claude/commands/create-handoff.md`, `resume-handoff.md`, `update-handoff.md`

A three-command protocol for session continuity: `create-handoff` initializes a structured document, `update-handoff` applies section-specific merge rules (append-only for work log, replace for status), and `resume-handoff` loads the latest document into context.

### Pattern 6: Recipe Template with Context Validation Checkpoints

**Guide section**: [Skill Design Patterns](./skill-design-patterns.md#recipe-template-and-context-validation-checkpoints) and template at `examples/commands/recipe-template.md`
**Source**: recurring pattern across Packmind command files

A command template structure where a "Context Validation Checkpoints" section lists preconditions Claude must verify before executing the recipe steps. Reduces errors caused by missing context or wrong environment.

---

## Packmind context-evaluator

**Repo**: [github.com/PackmindHub/context-evaluator](https://github.com/PackmindHub/context-evaluator)
**Author**: Packmind engineering team
**License**: MIT

context-evaluator is an OSS CLAUDE.md / AGENTS.md quality analyzer. Two patterns from its source were extracted for the guide:

### Pattern 7: Runtime Prompt Logging

**Guide section**: [Skill Design Patterns](./skill-design-patterns.md#runtime-prompt-logging)
**Source**: `src/shared/evaluation/runtime-prompt-logger.ts`

Always-on blocking write of the full evaluator prompt to `prompts/debug/` before invoking the AI provider. Survives provider crashes and timeouts. Never throws. Separate from the `--debug` flag.

### Pattern 8: Adaptive Unified/Parallel Mode

**Guide section**: [Skill Design Patterns](./skill-design-patterns.md#adaptive-unifiedparallel-mode)
**Source**: `src/shared/evaluation/runner.ts` — `canUseUnifiedMode()`

Token-threshold switching between single-agent unified evaluation (cross-file detection) and parallel independent agents per file. Threshold default: 100K tokens.

---

## Anthropic Engineering Team

**skill-creator**: The `skill-creator` skill vendored in the Packmind repo (and referenced in this guide's skill evaluation section) was originally published by Anthropic. It contains the canonical evaluation harness for testing skills: evals filesystem convention, blind A/B comparator, description optimization loop, and benchmark aggregation scripts.

---

---

## Guillaume Laforge (Open Reasoning Format)

**Blog**: [glaforge.dev](https://glaforge.dev/posts/2026/07/21/open-reasoning-format-encoding-and-remembering-agentic-behavior/)
**Author**: Guillaume Laforge, Developer Advocate at Google Cloud, co-founder of Apache Groovy
**License**: open spec (Markdown + YAML), reference CLI in Python

The Open Reasoning Format (ORF) shaped the file-based experience-playbook track in [memory-systems.md §3.7](memory-systems.md#37-file-based-experience-playbooks-orf-diffmem). ORF's three-tier progressive disclosure for memory retrieval and its Abstracted-Insight / Validated-Path schema split are documented there, along with the ReasoningBank paper (arXiv 2509.25140) that ORF cites as its academic anchor.

---

## Growth Kinetics (DiffMem)

**Repo**: [github.com/Growth-Kinetics/DiffMem](https://github.com/Growth-Kinetics/DiffMem)
**License**: MIT claimed in the pyproject classifier (no LICENSE file present)

DiffMem is documented as a case study in [memory-systems.md §3.7](memory-systems.md#37-file-based-experience-playbooks-orf-diffmem). Its LLM-agentic git-shell retrieval (an LLM that greps and blames the repo instead of querying an index) and its orphan-branch-per-user isolation are the extracted ideas. Its removal of BM25 in favor of full-LLM retrieval anchors the guide's "match retrieval to query shape" teaching point.

---

## IFTTD (If This Then Dev) Podcast

**Podcast**: [ifttd.io](https://www.ifttd.io/)
**Host**: Bruno Soulez
**License**: Editorial citation (no code)

IFTTD is a French tech podcast (360+ episodes, 2020-2026) covering practical software engineering. Transcripts from episodes 290 to 361 were analyzed and their practitioner insights paraphrased into the guide. No direct quotes appear in the guide; all material is reformulated in English and attributed by episode.

### Sections drawing on IFTTD

**Guide section**: [Practitioner Insights](../ecosystem/practitioner-insights.md)
**Source episodes**: 311, 326, 329, 338, 341, 346, 349, 351, 357, 360, 361
Consolidated digest of paraphrased insights organized by theme (context engineering, agentic patterns, LLM evaluation, agent security, DevX and adoption).

**Guide section**: [§6 RAG Optimization: Query-Side Indexing](../ecosystem/context-engineering-tools.md#query-side-indexing-semantic-chunking-and-synthetic-questions)
**Source**: ep 361, Guillaume Laforge (Developer Advocate, Google Cloud)
Practitioner perspective on semantic chunking and synthetic-question generation at index time, supplementing the existing Anthropic Contextual Retrieval documentation.

**Guide section**: [§17 Attention Mechanics: Lost-in-the-Middle](../core/context-engineering.md#the-lost-in-the-middle-problem)
**Source**: ep 361, Guillaume Laforge
Practitioner note on large context window anti-patterns, added to the existing Liu et al. research citation.

**Guide section**: [Evaluating Probabilistic Systems](../roles/agent-evaluation.md#evaluating-probabilistic-systems)
**Source**: ep 338 (Louis Pinsard), ep 329 (Frédéric Barthelet), ep 311 (Samy Lastmann)
Consolidated section on scored-dataset evaluation, statistical CI/CD, LLM-as-judge (async), hallucination calibration, and OpenTelemetry/Langfuse observability.

**Guide section**: [Why Sandboxing Matters: Field Incidents](../security/sandbox-native.md#why-sandboxing-matters-field-incidents)
**Source**: ep 326 (Zineb Bendhiba), ep 360 (Guillaume Lours)
Documented incidents on guardrail evasion and unsupervised agent data loss.

**Guide section**: [MCP Vetting Workflow](../security/security-hardening.md#11-mcp-vetting-workflow)
**Source**: ep 346, Jocelyn N'takpe (Head of Engineering & Architecture, ManoMano)
Command allowlist recommendation, illustrated with a real incident.

**Guide section**: [Usage Principles](../ecosystem/mcp-servers-ecosystem.md#usage-principles-beyond-the-evaluation-checklist)
**Source**: ep 326 (Zineb Bendhiba), ep 329 (Frédéric Barthelet)
Tool count, tool design principles, and LLM statefulness notes.

**Guide section**: [Practitioner Testimonials](../workflows/agent-teams.md#practitioner-testimonials)
**Source**: ep 311, 341, 346, 361
Four new testimonials on micro-agent architectures, harness engineering, multi-model orchestration, and production MCP stacks.

**Guide section**: [Adoption Approaches: What We Do Know](../roles/adoption-approaches.md#what-we-do-know-empirical-data)
**Source**: ep 346, 349, 351
Practitioner notes on documentation-as-onboarding, typed language safety nets, and sustainable development pace.

---

## Devoxx

**Conference**: [Devoxx](https://devoxx.com/) (Java/JVM, architecture, DevOps, AI tracks)
**License**: Editorial citation (no code)

Devoxx talks from 2025 and 2026 were analyzed and paraphrased into the guide's practitioner insights. No direct quotes appear; all material is reformulated in English and attributed by speaker and year.

### Sections drawing on Devoxx

**Guide section**: [Practitioner Insights](../ecosystem/practitioner-insights.md#devoxx)
**Speakers**: Brian Vermeer, Max Sumrall, Tom Cools, Christoph Bühler, Daniel Garnier-Moiroux, Annie Freeman, Mete Atamel, Jettro Coenradie, Daniël Spee, and others (see the Devoxx table on that page)
Consolidated digest of paraphrased insights on prompt injection testing, the spec paradox, LLM-as-judge design, and MCP access control.

**Guide section**: [security-hardening.md](../security/security-hardening.md)
**Source**: Brian Vermeer, 2026
Prompt injection testing and LLM session secrecy.

**Guide section**: [sandbox-isolation.md](../security/sandbox-isolation.md)
**Source**: Christoph Bühler, Daniel Garnier-Moiroux, 2025-2026
MCP access control patterns (OAuth, OpenFGA) and MCP server hardening.

**Guide section**: [Evaluating Probabilistic Systems](../roles/agent-evaluation.md#evaluating-probabilistic-systems)
**Source**: Brian Vermeer, Mete Atamel, Jettro Coenradie, Daniël Spee, Tom Cools, 2025-2026
Determinism, evaluation framework combination, confidence-based agent evaluation.

**Guide section**: [observability.md](../ops/observability.md)
**Source**: Annie Freeman, 2026
Instrumenting coding assistants with OpenTelemetry.

**Guide section**: [agent-teams.md](../workflows/agent-teams.md#practitioner-testimonials)
**Source**: Max Sumrall, 2026
The spec paradox and the Picnic productivity REX.

**Guide section**: [context-engineering.md](../core/context-engineering.md)
**Source**: Alex Gavrilescu, Konstantin Pavlov, 2025
Markdown as shared persistent memory paired with a conventions file.

---

## Dev With AI Meetup

**Meetup**: Dev With AI (French AI-native development meetup)
**License**: Editorial citation (no code)

Dev With AI Meetup talks from 2026 were analyzed and paraphrased into the guide's practitioner insights. No direct quotes appear; all material is reformulated in English and attributed by speaker and year.

### Sections drawing on Dev With AI Meetup

**Guide section**: [Practitioner Insights](../ecosystem/practitioner-insights.md#dev-with-ai-meetup)
**Speakers**: Emmanuel Sciara, Florian Allainmat, Luis Iglesias Hernandez, Alexandre Balmes, Vyncke, Samuel Gallet, Geslain Dahan, Geoffrey Graveaud, and others (see the Dev With AI Meetup table on that page)
Consolidated digest of paraphrased insights on context degradation thresholds, exit criteria for agents, and skill self-improvement.

**Guide section**: [context-engineering.md](../core/context-engineering.md)
**Source**: Emmanuel Sciara, Florian Allainmat, 2026
The 70% context degradation threshold, CLAUDE.md growth hurting performance, and the research-plan-implement handoff pattern.

**Guide section**: [Evaluating Probabilistic Systems](../roles/agent-evaluation.md#evaluating-probabilistic-systems)
**Source**: Alexandre Balmes, Emmanuel Sciara, Negouai, Drode, 2026
Temperature-zero determinism myths and skill self-improvement as reinforcement learning.

**Guide section**: [sandbox-native.md](../security/sandbox-native.md)
**Source**: Bolin, Vyncke, Florian Allainmat, 2026
Production agent isolation pattern (ephemeral container, read-only repo, network allowlist).

**Guide section**: [Adoption Approaches: What We Do Know](../roles/adoption-approaches.md#what-we-do-know-empirical-data)
**Source**: Geoffrey Graveaud, Samuel Gallet, Geslain Dahan, 2026
Practice amplification (good and bad) and a documented velocity-loss REX from unsupervised agent delegation.

---

## ByteByteGo

**Channel**: [ByteByteGo](https://bytebytego.com/) (system design)
**License**: Editorial citation (no code)

ByteByteGo videos were analyzed and paraphrased into the guide, filtered strictly for relevance to agentic AI and Claude Code workflows. No direct quotes appear.

### Sections drawing on ByteByteGo

**Guide section**: [Practitioner Insights](../ecosystem/practitioner-insights.md#bytebytego)
**Source**: ByteByteGo, "7 System Design Concepts," 2025
Start-simple-measure-then-complexify, applied to agentic setups.

**Guide section**: [Usage Principles](../ecosystem/mcp-servers-ecosystem.md#usage-principles-beyond-the-evaluation-checklist)
**Source**: ByteByteGo, "MCP" (2025), "Back-of-the-Envelope Estimation" (2022), "URL Shortener" (2025)
MCP as a standardized integration layer, and QPS-based capacity estimation for agent-driven traffic.

---

## Stanford Online

**Channel**: [Stanford Online](https://www.youtube.com/@stanfordonline) (academic ML/LLM coursework)
**License**: Editorial citation (no code)

Stanford Online lectures were analyzed and paraphrased into the guide, filtered strictly for direct, actionable relevance to Claude Code practice. No direct quotes appear.

### Sections drawing on Stanford Online

**Guide section**: [Practitioner Insights](../ecosystem/practitioner-insights.md#stanford-online)
**Source**: Denny Zhou (Google DeepMind), Stanford CS25 V5, 2025; Yann Dubois, CS224N, 2024; Mehran Sahami, "It's Never Too Late," 2025; ISLR (Hastie & Tibshirani); CS230; CS25 2026
Reasoning as intermediate tokens with a formal Boolean-circuit bound, evaluation design (Cohen's kappa, out-of-distribution testing), the shift toward verifying AI-generated code, and the necessity check before adding a model.

**Guide section**: [context-engineering.md](../core/context-engineering.md)
**Source**: Denny Zhou, Stanford CS25 V5, 2025; CS25 2026; CS230 Lecture 8, 2025
Chain-of-thought as a formal compute extension, and in-context generation versus fine-tuning.

**Guide section**: [Evaluating Probabilistic Systems](../roles/agent-evaluation.md#evaluating-probabilistic-systems)
**Source**: Yann Dubois, CS224N, 2024; ISLR; CS230
Evaluation metric selection by pipeline stage and the necessity check before adding a model.

**Guide section**: [learning-with-ai.md](../roles/learning-with-ai.md)
**Source**: Mehran Sahami, "It's Never Too Late," 2025
Verifying AI-generated code as the emerging critical skill.

---

## The Product Crew

**Podcast**: The Product Crew (French product management podcast)
**License**: Editorial citation (no code)

The Product Crew episodes were analyzed and paraphrased into the guide's adoption, roles, and ops pages, filtered strictly for relevance to AI adoption decisions. No direct quotes appear. The cited Ask For The Moon field report is a single-instance 2026 account, not established industry data, and is presented as such.

### Sections drawing on The Product Crew

**Guide section**: [Adoption Approaches: What We Do Know](../roles/adoption-approaches.md#what-we-do-know-empirical-data)
**Source**: The Product Crew, 2024-2026 (contexts: Alan, Payfit, Joko)
AI ownership by domain experts, adoption through practice rather than top-down rollout, and leadership buy-in as a prerequisite.

**Guide section**: [ai-roles.md](../roles/ai-roles.md)
**Source**: The Product Crew, 2026
AI ownership by domain experts over a centralized innovation cell.

**Guide section**: [ai-unit-economics.md](../ops/ai-unit-economics.md)
**Source**: The Product Crew, AI transformation field report, 2026 (context: Ask For The Moon)
The "tokens into ROI" framing used to introduce the stakes of unit economics.

---

## Adding to This File

When a guide section is directly inspired by or adapted from external open-source work, add an entry here. Include:
- Repository URL
- Author / organization name
- License
- Which pattern was borrowed and from which source file
- Which guide section it appears in
