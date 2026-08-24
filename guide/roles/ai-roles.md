---
title: "AI Roles & Career Paths: The New Engineering Landscape"
description: "Comprehensive map of emerging AI roles, from Prompt Engineer to Harness Engineer, with responsibilities, required skills, and career trajectories"
tags: [roles, careers, ai-engineer, prompt-engineer, harness-engineer, context-engineer, guide]
---

# AI Roles & Career Paths: The New Engineering Landscape

> **Last updated**: March 2026
>
> **Confidence**: Tier 2, based on job market data, industry publications, and emerging field research
>
> **Reading time**: ~20 minutes

The AI wave didn't just create new tools. It created new jobs that didn't exist 3 years ago and is reshaping what existing roles mean. This guide maps the full landscape: what each role does, what skills it requires, how they relate to each other, and where each one is heading.

---

## Table of Contents

1. [The Landscape in One View](#1-the-landscape-in-one-view)
2. [Prompt Engineer](#2-prompt-engineer)
3. [Context Engineer](#3-context-engineer)
4. [AI Engineer](#4-ai-engineer)
5. [LLM Engineer](#5-llm-engineer)
6. [AI Agent Engineer](#6-ai-agent-engineer)
7. [Founding AI Engineer](#7-founding-ai-engineer)
8. [AI Architect](#8-ai-architect)
9. [Platform Engineer (AI context)](#9-platform-engineer-ai-context)
10. [Harness Engineer](#10-harness-engineer)
11. [AI Product Manager](#11-ai-product-manager)
12. [AI Safety & Eval Engineer](#12-ai-safety--eval-engineer)
13. [ML Engineer](#13-ml-engineer)
14. [MLOps Engineer](#14-mlops-engineer)
15. [AI Developer Advocate](#15-ai-developer-advocate)
16. [AI Orchestration Engineer](#16-ai-orchestration-engineer)
17. [Spec Engineer](#17-spec-engineer)
18. [Agent Identity Architect](#18-agent-identity-architect)
19. [AI Eval Engineer](#19-ai-eval-engineer)
20. [Career Decision Matrix](#20-career-decision-matrix)
21. [Salary Benchmarks (2025-2026)](#21-salary-benchmarks-2025-2026)
22. [What's Not a Role (Yet)](#22-whats-not-a-role-yet)
23. [Job Listings](#23-job-listings)

---

## 1. The Landscape in One View

Two axes structure this landscape: **proximity to the model** (are you training it, prompting it, or building infrastructure around it?) and **proximity to production** (research vs. shipped product).

```
              ← Closer to the model          Closer to infrastructure →

Research    ML Engineer ←────────────────────────── AI Architect
            AI Safety Engineer                       Platform Engineer
                  │                                        │
                  │                                        │
Production   LLM Engineer ──── AI Engineer ──── AI Agent Engineer
             Context Engineer                    Harness Engineer
             Prompt Engineer                     Founding AI Engineer
                                                 AI Product Manager
```

Most new job demand sits in the **bottom-right**: building reliable AI systems that ship and stay reliable in production. The "pure research" quadrant remains competitive and specialized. The highest growth is in the applied, product-facing roles.

---

## 2. Prompt Engineer

**Status**: First wave (2022-2023), partially commoditized but still relevant in specialized contexts.

### What they do

Craft and optimize the instructions sent to AI models to get reliable, high-quality outputs. The scope ranges from one-shot prompts to complex multi-step prompt chains for production systems.

### Responsibilities

- Design prompt templates for specific use cases (customer support, code generation, document analysis)
- Run systematic A/B tests to measure prompt performance
- Document prompt libraries and version them
- Optimize prompts for cost (fewer tokens, same quality)
- Work with domain experts to encode knowledge into prompts

### Required skills

| Technical | Soft |
|-----------|------|
| Understanding of LLM behavior and failure modes | Communication with non-technical stakeholders |
| Basic Python (for automation and testing) | Systematic experimentation mindset |
| Familiarity with evaluation frameworks | Attention to edge cases |
| Versioning practices | Documentation discipline |

### Where it's heading

The "prompt engineer" title as a standalone role is consolidating into broader AI Engineer or Context Engineer roles. Where it persists: companies with very specific, high-stakes prompt domains (legal, medical, financial compliance). Upskill toward context engineering or AI engineering if you're in this role.

### Entry paths

Technical writer, QA engineer, domain expert (law, medicine, finance), content strategist.

---

## 3. Context Engineer

**Status**: Emerging, one of the fastest-growing specializations in 2025.

### What they do

Context engineering is the evolution of prompt engineering. Where prompt engineers craft instructions, context engineers design **systems** that give AI models the right information, at the right time, in the right format. Andrej Karpathy explicitly moved from "vibe coding" framing to "context engineering" as the more precise description of this work.

See the [Context Engineering reference](../core/context-engineering.md) for the full discipline, including the ACE pipeline (Section 6), the L0→L5 maturity model (Section 9), and the operational mechanisms that separate a Level 4 from a Level 5 system: signal taxonomy and causal attribution (Section 10), PR-based loop closure (Section 11), ejection of dormant rules (Section 12), constitutional audits (Section 13), and multi-dev profile reconciliation (Section 14).

> "Context Engineering is providing the right information and tools, in the right format, at the right time." (Philipp Schmid, Google)

### Responsibilities

- Design RAG (Retrieval-Augmented Generation) systems and knowledge bases
- Manage context windows across multi-turn interactions and long-horizon tasks
- Define what agents remember, retrieve, or forget during task execution
- Structure information hierarchies (system prompts, conversation history, retrieved docs, tool definitions, safety constraints)
- Optimize context for accuracy and cost simultaneously
- Measure context quality through systematic evals

### Required skills

| Technical | Soft |
|-----------|------|
| Python (context pipeline automation) | Systems thinking |
| Vector databases (Pinecone, Chroma, Weaviate) | Information architecture instinct |
| SQL and NoSQL (context retrieval) | Cross-functional collaboration |
| Cloud platforms (AWS/Azure/GCP) | Curiosity and continuous learning |
| RAG architectures, embedding models | Precision in documentation |

### Relationship to other roles

Context engineers work upstream of AI engineers (they define what context is available) and downstream of domain experts (they encode domain knowledge into retrievable structures). Closely related to platform engineers in large organizations.

### Entry paths

Data engineer, backend engineer, ML engineer, information architect.

---

## 4. AI Engineer

**Status**: Mainstream, the generalist role for building AI-powered products.

### What they do

Build end-to-end AI systems. Not researchers (they don't train models from scratch), but not just integrators either. They take LLMs and orchestration frameworks and build systems that ship. Think of them as software engineers who've added LLM integration, evals, and AI product intuition to their stack.

### Responsibilities

- Design and implement LLM-powered applications (chatbots, agents, pipelines)
- Build evaluation frameworks to measure model output quality
- Integrate AI capabilities into existing software systems
- Monitor AI systems in production (latency, cost, quality drift)
- Select appropriate models for specific tasks (capability vs. cost tradeoffs)
- Implement fine-tuning or RAG when base models aren't sufficient

### Required skills

| Technical | Soft |
|-----------|------|
| Strong software engineering foundations | Product judgment |
| Python (primary), JavaScript (often needed) | Pragmatism over research purity |
| Familiarity with major LLM APIs (Anthropic, OpenAI, Gemini) | Fast iteration mindset |
| Eval design and measurement | Ability to work with ambiguous requirements |
| Understanding of embeddings, RAG, agent frameworks | Communication of AI limitations to stakeholders |
| MLOps basics (deployment, monitoring, versioning) | |

### The critical distinction from ML Engineer

AI engineers work with existing models. ML engineers build and train models. In practice, most companies hiring in 2025-2026 need AI engineers (apply the models) not ML engineers (build the models).

### Entry paths

Software engineer (most common), backend engineer, data engineer, ML engineer transitioning to applied work.

---

## 5. LLM Engineer

**Status**: Specialized variant of AI Engineer, prominent in model-heavy companies.

### What they do

Deep specialization in large language model integration and optimization. Where AI engineers are generalists, LLM engineers go deep on the model layer: fine-tuning, RLHF, model selection, prompt optimization at scale, and evaluation infrastructure.

### Responsibilities

- Fine-tuning base models for domain-specific tasks
- Designing and running systematic model evaluations (evals)
- Implementing RLHF or similar feedback mechanisms
- Model performance benchmarking and regression testing
- Managing model versions and A/B testing new model releases
- Building tooling for model monitoring and drift detection

### Required skills

| Technical | Soft |
|-----------|------|
| Python (fluent) | Scientific rigor |
| PyTorch or JAX | Statistical thinking |
| Transformers architecture knowledge | Patience with slow feedback loops |
| Evaluation framework design | Documentation of experiments |
| Distributed training basics | |

### Where it's heading

Strong demand at AI companies (Anthropic, OpenAI, scale-ups) and in large enterprises building proprietary models. Distinct from AI engineer in its proximity to the model itself. Expect this role to bifurcate: pure research at labs vs. applied fine-tuning at enterprises.

---

## 6. AI Agent Engineer

**Status**: High growth, one of the most in-demand specialized roles in 2025-2026.

### What they do

Design and build autonomous agent systems. While AI engineers build general AI products, agent engineers specialize in systems that plan, reason, use tools, and execute multi-step tasks without constant human intervention.

### Responsibilities

- Design multi-agent architectures (orchestrator + specialist agents)
- Build agent memory systems (short-term, long-term, episodic)
- Implement tool use and API integrations for agents
- Design guardrails and safety mechanisms for autonomous systems
- Build human-in-the-loop checkpoints for high-risk decisions
- Monitor agent behavior in production (reliability, cost, anomaly detection)
- Test agent systems systematically (agentic eval is a distinct discipline)

### Required skills

| Technical | Soft |
|-----------|------|
| Agent frameworks (LangChain, AutoGen, Claude Agent SDK, CrewAI) | Systems thinking |
| Orchestration patterns | Risk judgment (when to let agents act autonomously) |
| Tool/API integration | User experience intuition |
| Async programming | Debugging patience (agents fail in non-deterministic ways) |
| Observability and tracing (LangSmith, Langfuse, etc.) | |

### Key challenge specific to this role

Non-determinism. Agent systems fail in ways that are hard to reproduce. Observability tooling (tracing every agent step) is as critical as the agent code itself. Engineers who treat agent debugging like debugging traditional code struggle.

---

## 7. Founding AI Engineer

**Status**: Highly sought after in AI-native startups and seed-to-Series A companies.

### What they do

A hybrid role unique to early-stage companies: part AI engineer, part product engineer, part technical co-founder. They own core product functionality end-to-end, from architecture decisions to customer interactions, while building on top of AI capabilities.

> Typically targets engineers with 0-4 years of experience who are comfortable with ambiguity, figure things out independently, and already use AI tools daily in their workflow.

### Responsibilities

- Build entire product features from architecture to deployment, not just assigned tickets
- Make foundational technical decisions that will shape the company's stack for years
- Work directly with founders on product strategy and prioritization
- Use AI coding tools as force multipliers to ship at startup speed
- Interact directly with early customers to understand problems
- Define engineering culture before it calcifies

### What makes this role different

Scope of ownership and ambiguity. A senior engineer at a large company works within defined systems. A founding engineer defines the systems. The leverage is massive in both directions: great decisions compound, bad ones become technical debt that's hard to escape.

### Required profile

- Bias toward action over analysis paralysis
- Comfort shipping imperfect things and iterating
- Product intuition alongside technical skills
- Already fluent with AI coding tools (Claude Code, Cursor, Copilot)
- Able to context-switch from infra to product to customer research in the same day

### Entry paths

Strong mid-level engineers at established companies who want more ownership. Common source: engineers who've been quietly building side projects with AI tools.

---

## 8. AI Architect

**Status**: Senior/Staff level, emerging role in larger organizations.

### What they do

Design enterprise AI systems at the system level. Where AI engineers ship features, AI architects define the patterns, platforms, and decision frameworks that multiple teams use. They make the technology choices that others live with for years.

### Responsibilities

- Define AI technology strategy and stack decisions (which models, which frameworks, which providers)
- Design enterprise AI reference architectures
- Set standards for AI system observability, security, and governance
- Evaluate build vs. buy decisions for AI capabilities
- Ensure AI systems are scalable, cost-effective, and auditable
- Bridge between business requirements and technical AI implementation

### Required skills

- Deep experience across AI/ML stack (models, infrastructure, MLOps)
- Strong communication skills (presenting to C-suite, working with legal/compliance)
- Understanding of cloud provider AI offerings (AWS Bedrock, Azure OpenAI, Vertex AI)
- Security and compliance awareness (GDPR, AI Act, SOC2)
- Experience designing distributed systems at scale

### Entry paths

Senior AI engineer → Staff → Architect. Often takes 5-8 years in AI-adjacent roles. Alternatively: cloud architect + strong AI self-study.

---

## 9. Platform Engineer (AI context)

**Status**: Established role, significantly reshaped by AI.

### What they do

Build and maintain the internal developer platform. With AI, this role has expanded to include the "golden path" for AI development: standardized ways for teams to integrate LLMs, common observability infrastructure, cost controls, and guardrails so individual teams don't reinvent the wheel or create security risks.

### AI-specific responsibilities added to traditional platform work

- Provide standardized LLM integration patterns (internal SDKs, proxies, abstractions)
- Manage API keys, rate limits, and cost allocation across teams
- Build AI observability infrastructure (tracing, logging, alerting)
- Enforce security policies for AI outputs (PII filtering, output validation)
- Maintain model registries and versioning systems
- Create "paved roads" for RAG patterns, agent architectures, eval pipelines

### Why this role matters more with AI

When every team is building their own LLM integrations, you get: duplicated cost, inconsistent security, no centralized observability, and no shared learnings. Platform engineers who understand AI prevent this fragmentation. They're the reason the AI investment in a company scales instead of sprawling.

**Operational ownership of AI works best sitting with the business experts themselves, not a centralized innovation cell.** Two independent corporate field reports converge against the instinct to centralize: routing every initiative through an innovation lab or an isolated IT department slows adoption and dilutes domain judgment. The counterintuitive position, relative to the classic "innovation cell" model, is to hand the tool to the people who already own the problem.

*The Product Crew, enterprise field reports, 2026*

### Required skills (AI additions)

MLOps tooling, LLM gateway products (LiteLLM, Portkey), cloud AI services, cost optimization patterns, security for AI (prompt injection mitigation, output filtering).

---

## 10. Harness Engineer

**Status**: Emerging, formalized by Martin Fowler in 2025, not yet institutionalized as a standalone title.

### What they do

Build the infrastructure that keeps AI agents "under harness," under control. As agentic AI systems generate code, take actions, and operate with increasing autonomy, harness engineers build the systems that ensure they stay within architectural constraints, produce coherent output, and don't accumulate entropy over time.

> Source: [Martin Fowler, Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)

### The three pillars

**1. Context engineering (knowledge infrastructure)**
Not one-off prompts, but a continuously updated knowledge base embedded in the codebase. Agents know your conventions, architecture decisions, and domain context. Dynamic access to observability data and documentation.

**2. Architectural constraints (agent guardrails)**
- LLM-based watchdog agents that review generated code
- Custom deterministic linters enforcing your specific architectural patterns
- Structural tests (ArchUnit-style) that run automatically
- Pre-commit hooks that reject code violating established constraints

**3. Entropy management (drift prevention)**
Periodic agents that scan the codebase for: outdated documentation, architectural violations that slipped through, abandoned patterns that reappeared, inconsistencies introduced by multiple agents working in parallel.

### The core insight

Without a harness, AI agents produce code that individually looks fine but collectively drifts away from your architecture, your patterns, and your documentation. The harness is what makes "AI generates most of the code" sustainable at scale rather than a path to unmaintainable systems.

### The formal framework (arXiv 2605.18747, May 2026)

"Code as Agent Harness" (arXiv 2605.18747) formalizes three properties that a production harness must satisfy. These serve as evaluation criteria when choosing between harness frameworks or assessing whether an internal toolchain qualifies as a harness rather than a wrapper.

**Executability.** The harness actually runs the code the model produces and verifies the result objectively. Text or code generation alone does not qualify. A harness that validates syntax but not behavior fails this property. Anthropic SDK, OpenAI Agents SDK, and LangGraph each implement the while-loop execution engine that makes executability concrete.

**Inspectability.** Every step the agent takes is traceable for diagnosis and feedback generation. OpenInference (maintained by Arize) and OpenLLMetry (Traceloop) are the two instrumentation layers that standardize this property within the OpenTelemetry ecosystem. The OTel GenAI SIG defines `gen_ai.client` spans as stable and `gen_ai.agent` spans as experimental as of May 2026.

**Statefulness.** The harness maintains continuity between sessions and sequential tool calls. Without statefulness, each agent interaction starts blind, forcing re-discovery of context that was already established. E2B and Northflank implement this at the infrastructure level; Anthropic Claude Managed Agents and AWS Bedrock AgentCore implement it at the product level.

Martin Fowler summarizes the distinction precisely: "A raw model is not an agent. It becomes one when connected to a harness." O'Reilly characterizes the harness as "the new frontier of reliable AI systems" (2026). Nine concrete components make up a prod-grade harness: while-loop engine, context management, tool registry, sub-agent management, built-in skills, session persistence, dynamic prompt assembly, lifecycle hooks, and permission enforcement.

### Organizational impact

This role pushes toward **intentional technological convergence**: organizations with 2-3 primary tech stacks benefit far more from standardized harnesses than organizations with 10 different stacks. It's a deliberate trade of technical freedom for reliability.

> "Ce n'est pas quelque chose dans lequel vous pouvez vous lancer pour des résultats rapides." (Martin Fowler)

### Where this role will emerge

Currently absorbed by: platform engineers, staff/principal engineers, architecture guilds. Likely to become an explicit role in:
- Companies running autonomous coding agents at scale
- Large enterprises with 50+ engineers using AI coding tools
- Organizations that've experienced "AI entropy" firsthand (code that works but nobody understands anymore)

### Required skills

Software architecture, linter/static analysis tooling, LLM orchestration, observability, codebase knowledge management, entropy detection patterns.

---

## 11. AI Product Manager

**Status**: Mainstream and growing, with significant premium over traditional PM roles.

### What they do

Product management with deep AI fluency. They understand what AI can and can't do, manage the unique product challenges of AI systems (non-determinism, latency, hallucinations, cost), and translate between business needs and AI capabilities.

### Responsibilities

- Define product requirements for AI features with technical constraints in mind
- Work with AI engineers on evaluation criteria (what does "good" look like?)
- Manage the unique UX challenges of AI: uncertainty, latency, error handling
- Own the cost/quality/speed tradeoffs for AI features
- Communicate AI limitations and risks to stakeholders
- Run A/B tests on model versions, prompt changes, feature changes

### What makes AI PM different from traditional PM

Traditional PM ships features that behave deterministically. AI PMs ship systems where outputs vary. They need to think probabilistically: not "will this work?" but "what % of the time will this work, and what happens in the other cases?" Quality measurement is continuous, not binary.

### Required skills

Standard PM skills (roadmapping, prioritization, user research) plus: LLM API familiarity, eval design, basic Python for running experiments, understanding of model tradeoffs (accuracy vs. cost vs. latency), AI UX patterns.

### Salary context

FAANG-level: $160K-$200K+ entry-level AI PM. Senior: $200K-$300K+ total compensation.

---

## 12. AI Safety & Eval Engineer

**Status**: Specialized, primarily at AI labs and companies with regulated AI deployments.

### What they do

Ensure AI systems behave safely, reliably, and in alignment with intended values. Two related but distinct specializations: **Eval Engineers** (build systems to measure model behavior) and **AI Safety Engineers** (identify and mitigate risks in AI systems).

### Eval Engineer responsibilities

- Design evaluation frameworks (evals) to measure model quality, safety, and capabilities
- Build automated eval pipelines that run on every model version change
- Define metrics that capture real-world performance (not just benchmark gaming)
- Implement human evaluation workflows for subjective quality dimensions
- Detect regressions before they reach production

### AI Safety Engineer responsibilities

- Red-team AI systems to find failure modes, jailbreaks, and harmful outputs
- Implement content filtering, output validation, and guardrail systems
- Design human-in-the-loop checkpoints for high-risk decisions
- Monitor production systems for harmful outputs or unexpected behavior
- Work with legal/compliance on AI governance

### Required skills

Rigorous experimental design, statistics, Python, strong understanding of LLM failure modes, communication skills for risk reporting.

### Where to find these roles

Primarily: Anthropic, OpenAI, Google DeepMind, Meta AI, Microsoft AI. Growing in: healthcare, finance, legal tech, regulated industries where AI errors have serious consequences.

---

## 13. ML Engineer

**Status**: Established, the most traditional of the AI engineering roles.

### What they do

Develop, train, deploy, and maintain machine learning models. In the LLM era, many ML engineers have pivoted toward fine-tuning and applied AI work rather than building models from scratch. That work is increasingly concentrated at a small number of frontier labs.

### Responsibilities

- Data pipeline development (collection, cleaning, transformation)
- Model training and fine-tuning
- Feature engineering
- Model serving and deployment (MLOps)
- Performance optimization and model compression
- Production monitoring for model drift

### How the role is evolving

The "build a model from scratch" path is increasingly rare outside frontier labs. ML engineers in most companies now work on: fine-tuning existing models, building RAG systems, deploying and monitoring models in production, and bridging between AI engineers and data infrastructure. The practical overlap with AI engineer is large.

### Required skills

Python (fluent), PyTorch or TensorFlow, distributed computing, data pipeline tools (Spark, Airflow, dbt), cloud ML platforms (SageMaker, Vertex AI, Azure ML), statistical foundations.

---

## 14. MLOps Engineer

**Status**: Established, distinct from ML Engineer, growing in enterprises deploying models at scale.

### What they do

Bridge the gap between model development and production infrastructure. While ML engineers build and fine-tune models and AI engineers build applications, MLOps engineers own the operational layer: CI/CD pipelines for models, deployment infrastructure, monitoring for drift and degradation, and the systems that keep models reliable in production over time.

### Responsibilities

- Build and maintain CI/CD pipelines for model training, evaluation, and deployment
- Monitor production models for performance drift, data drift, and prediction quality degradation
- Design feature stores and model registries
- Implement A/B testing and canary deployments for new model versions
- Manage compute infrastructure for training and inference (cost optimization)
- Build observability tooling: metrics, logging, alerting for model behavior in production
- Establish model versioning and rollback procedures

### Required skills

| Technical | Soft |
|-----------|------|
| Python (fluent) | Infrastructure mindset |
| Cloud ML platforms (SageMaker, Vertex AI, Azure ML) | Cross-team collaboration (ML + Infra) |
| Kubernetes, Docker, infrastructure as code | Reliability engineering instinct |
| MLflow, Weights & Biases, or similar experiment tracking | Incident response discipline |
| Data pipeline tools (Airflow, Prefect, dbt) | |
| Monitoring and observability (Prometheus, Grafana) | |

### The distinction that matters

ML engineers ask: "Does the model work?" MLOps engineers ask: "Does the model keep working?" The operational lifecycle of a model (monitoring, retraining triggers, rollback procedures, cost per inference) is entirely separate from building it. Companies that skip this role discover it when a model silently degrades in production and nobody notices until user complaints spike.

### Entry paths

DevOps/platform engineer adding ML knowledge, ML engineer who gravitates toward infrastructure, data engineer moving toward model operations.

---

## 15. AI Developer Advocate

**Status**: High growth, actively hiring at all major AI companies in 2025-2026.

### What they do

Build the bridge between an AI platform and the developers who use it. Part engineer, part educator, part community builder. They go deep enough technically to build real things with the platform, then turn that knowledge into tutorials, documentation, sample projects, and public presence that helps other developers succeed.

### Responsibilities

- Build technical demos, sample projects, and integrations using the platform's APIs
- Create developer content: tutorials, blog posts, video walkthroughs, conference talks
- Represent developer needs and pain points to the product and engineering teams
- Engage with developer communities (Discord, GitHub, forums, social)
- Speak at conferences and run workshops
- Onboard strategic partners and enterprise developers
- Gather and synthesize developer feedback into product improvements

### Required skills

| Technical | Soft |
|-----------|------|
| Solid software engineering foundations | Clear technical writing |
| Deep familiarity with the platform/API | Public speaking confidence |
| Ability to build quick, illustrative prototypes | Community instinct |
| Understanding of developer experience (DX) | Empathy for confused users |
| Familiarity with AI concepts (prompting, RAG, agents) | Curiosity and continuous learning |

### What makes this role different

The audience is other developers, not end users. DevRel success measures developer activation (do developers try the product?), retention (do they keep using it?), and advocacy (do they tell others?). Credibility is the core asset, which means you have to actually build things, not just talk about them. A DevRel who hasn't shipped real production code with the platform has no credibility with the audience they're trying to reach.

### Salary context

$120K-$180K base (US), senior/lead roles $150K-$250K+. Total compensation includes equity at most AI companies.

### Where these roles are

Actively hiring: Anthropic, OpenAI, Together AI, Mistral, Cohere, Hugging Face, LangChain, and any company building developer-facing AI products. The role is expanding beyond AI labs as enterprise software companies add AI capabilities and need someone to help developers adopt them.

### Entry paths

Software engineer with a public presence (blog, open source, conference talks), technical writer with engineering background, early AI community member who builds in public.

---

## 16. AI Orchestration Engineer

**Status**: Emerging, real job postings in 2025, distinct from AI Agent Engineer in scope.

### What they do

Design and build intelligent workflows that connect AI capabilities with existing systems, data sources, and business processes. Where AI agent engineers build autonomous reasoning systems, AI orchestration engineers focus on the integration layer: connecting AI to enterprise tools, designing multi-step automation flows, and making AI reliably operable within existing infrastructure.

### Responsibilities

- Design end-to-end automation architectures using orchestration tools (n8n, LangChain, Power Automate, Zapier)
- Integrate AI capabilities with CRMs, ERPs, data warehouses, and communication platforms
- Build retrieval and synthesis stacks (RAG + answer grounding) for enterprise knowledge systems
- Define workflow reliability patterns: retries, fallbacks, human escalation triggers
- Set up observability for orchestrated workflows (tracing every step, cost tracking)
- Operationalize AI across cross-functional systems spanning engineering, product, and domain teams

### Required skills

| Technical | Soft |
|-----------|------|
| Orchestration platforms (n8n, LangChain, LlamaIndex) | Process analysis |
| API integration (REST, GraphQL, webhooks) | Cross-functional collaboration |
| Python or JavaScript (workflow scripting) | Systems thinking |
| Data transformation and mapping | Business process intuition |
| Observability and tracing (LangSmith, Langfuse) | |

### Distinction from AI Agent Engineer

| AI Agent Engineer | AI Orchestration Engineer |
|-------------------|--------------------------|
| Builds autonomous reasoning systems | Builds integration workflows connecting AI to existing systems |
| Focus: planning, memory, multi-step reasoning | Focus: connectivity, reliability, process automation |
| Core challenge: non-determinism | Core challenge: integration complexity |
| Primarily product-facing | Primarily internal/enterprise-facing |

### Where this role appears in job postings

Title varies significantly: "AI-First Orchestration Engineer" (Vista Equity Partners), "Staff AI Engineer (Orchestration)" (Heidi Health), "Sr. Software Engineer (AI Orchestration Zone)" (Zapier), "AI Engineer, AI Orchestration" (Adobe). The function is consistent even when the title isn't.

### Entry paths

Integration engineer, backend engineer with workflow automation experience, DevOps engineer adding AI tooling, business process automation specialist who's moved into code.

---

## 17. Spec Engineer

**Status**: Emerging in 2026, growing alongside Spec-Driven Development adoption.

### What they do

Write the structured specifications that AI agents use to plan, implement, and validate code. As organizations move from L2 (assistant) to L3 (orchestrated agents) on the Shapiro scale, spec quality becomes the primary determinant of output quality. Spec Engineers are the "requirements analysts" of the agentic era: they bridge business intent and machine-executable contracts.

### Core responsibility

Writing specifications that satisfy three conditions simultaneously: precise enough for an agent to generate correct code from them, human-readable enough for a product manager to approve them, and stable enough to serve as the diff-able ground truth when the implementation drifts.

GitHub Spec Kit formalizes this as a four-phase pipeline (Constitution, Specify, Plan, Tasks) where the spec file in `.specify/` is the governing artifact. Factory.ai Missions extends this with behavioral validation contracts written before any implementation begins. On a Slack clone, 81 problems were caught by independent validator agents from spec alone, generating 34% of the implementation work as "fix features."

### Required skills

| Technical | Soft |
|-----------|------|
| Structured writing (Gherkin-style Given-When-Then or equivalent) | Precision under ambiguity |
| Understanding of agent failure modes (multi-file tasks fail at 19.4% pass@1 without spec) | Negotiation with product, engineering, and LLMs simultaneously |
| Familiarity with SDD tools (Spec Kit, Kiro, Augment, Factory.ai) | Ability to distinguish what the spec must constrain vs what it should leave open |
| Version control discipline (specs versioned before code) | |

### Entry paths

Technical writer with engineering background, QA engineer who understands requirements, product engineer frustrated by low signal-to-noise in AI outputs, business analyst moving into AI-adjacent work.

---

## 18. Agent Identity Architect

**Status**: Critical gap. 77% of organizations have no formal agent identity strategy as of 2026.

### What they do

Design and enforce the identity layer for AI agents: how agents authenticate to services, what permissions they hold, how those permissions are scoped and audited, and how privilege escalation is prevented when agents chain tool calls across services.

### Why this role exists now

The Lethal Trifecta (Simon Willison, 2025): access to private data + exposure to untrusted content + capability for external communication = documented exfiltration vector. Most organizations understand the threat but have not built the defense. Strata Identity Research 2026 shows 44% of organizations are still using static API keys for agent authentication, 23% have a formal strategy, 18% rely on IAM trust inheritance with no per-agent scoping.

### What the role covers

- **Per-agent service principals**: Microsoft Entra Agent ID provides dedicated service principal types with OAuth On-Behalf-Of (OBO) flows scoped to specific session contexts. Not shared API keys, not team credentials.
- **MCP gateway governance**: Every MCP tool call passes through an identity enforcement point that validates the calling agent's permissions against the current task scope.
- **Session tracing**: Each action is attributable to a specific agent session, not just "the AI system."
- **Privilege escalation prevention**: Sub-agents spawned by orchestrators cannot inherit parent permissions by default; they receive only the minimum scope for their task.

### Required skills

IAM and OAuth/OIDC expertise, zero-trust architecture, Kubernetes RBAC, understanding of MCP security model, incident response for non-deterministic systems.

### Entry paths

Cloud security engineer, identity/access management specialist, platform engineer with security focus.

---

## 19. AI Eval Engineer

**Status**: Distinct from AI Safety & Eval (Section 12). This role focuses on production measurement, not lab safety.

### What they do

Build and operate the continuous measurement layer that tells the organization whether its AI systems are getting better or worse. Not red-teaming (that's AI Safety), not fine-tuning (that's LLM Engineer). Pure measurement: does the output quality hold up over time, across model upgrades, across traffic distribution shifts?

### The structural problem they solve

Anthropic's own data shows 93% of permission requests in production are approved without adequate review. JudgeBiasBench (arXiv 2604.23178) documents that LLM-as-judge systems have style bias scores of 0.76-0.92 and true negative rates below 25%, meaning they approve most incorrect outputs. These two facts together mean that relying on human review and LLM-as-judge alone is not a quality strategy. The Eval Engineer builds the third layer: structured evaluation pipelines with explicit pass/fail criteria that do not depend on human attention or LLM approval bias.

### Responsibilities

- Design evaluation frameworks with explicit metrics (task completion rate, tool correctness rate, hallucination rate)
- Build canary pipelines that run A/B comparisons on 1-2% of production traffic before promoting model changes
- Implement the creator-verifier pattern (independent agent checks agent outputs) for high-stakes workflows; independent verification improves correctness by +12 to +26% versus self-verification
- Monitor for silent degradation: code generation quality that declines after a model update without any alarm firing
- Maintain eval benchmarks that don't overfit to the current model's tendencies

### Required skills

Statistical experiment design, Python, understanding of LLM failure modes and bias patterns, CI/CD pipeline integration, working knowledge of OTel GenAI conventions (gen_ai.client spans are stable, gen_ai.agent spans are experimental as of May 2026).

### Tools

Arize Phoenix (1 trillion spans/month in production, self-hostable ELv2), Langfuse (OTel-native v3, MIT open-source), DeepEval (Python-native pytest integration), LangWatch Scenario SDK (multi-turn simulation), AWS Bedrock AgentCore (eval on 1-2% of live traffic).

---

## 20. Career Decision Matrix

Which role fits your current background and goals?

| Your current profile | Best next role | Timeline |
|---------------------|---------------|----------|
| Software engineer (3+ years) who wants to work with AI | AI Engineer | 3-6 months upskill |
| Software engineer at early startup who wants ownership | Founding AI Engineer | Now, if opportunity exists |
| Backend engineer interested in infra + AI | Platform Engineer (AI) | 6-12 months |
| Senior engineer who thinks in systems | AI Architect or Harness Engineer | 1-2 years experience accumulation |
| Engineer who likes research and rigor | LLM Engineer or AI Safety/Eval | +ML foundations needed |
| Non-technical who works with AI daily | Prompt Engineer → Context Engineer | 6-18 months |
| PM who wants to stay PM but be more relevant | AI Product Manager | 3-6 months upskill |
| Engineer obsessed with reliability and architecture | Harness Engineer (emerging) | Pioneers' territory |
| DevOps/platform engineer who wants to work with models | MLOps Engineer | 3-6 months upskill |
| Engineer with public presence and community instincts | AI Developer Advocate | 6-12 months |
| Integration or automation engineer adding AI | AI Orchestration Engineer | 3-6 months |
| Technical writer or QA engineer with engineering background | Spec Engineer | 3-6 months |
| Cloud/IAM security engineer moving into AI | Agent Identity Architect | 6-12 months |
| Engineer who wants to measure AI quality rigorously | AI Eval Engineer | 3-6 months upskill |

### The fastest path to AI employment in 2025-2026

1. Build something with AI APIs (Claude, OpenAI): a real project, not a tutorial
2. Write about what you built (blog post, GitHub README, LinkedIn)
3. Add evaluation: measure your system's quality, show the numbers
4. Apply for AI Engineer roles: the bar is demonstrated building, not credentials

Note: 76% of candidates claiming AI expertise lack production-level deployment experience (LangChain State of Agent Engineering 2025). The bar is lower than it appears if you've actually shipped something.

---

## 21. Salary Benchmarks (2025-2026)

> **Indicative only, large variance applies.** These figures are US market base salaries (2025-2026). Europe runs 30-50% lower, other markets 40-60% lower. Total compensation (equity, bonus, RSUs) can significantly exceed base, especially at startups and FAANG. Experience level, location within a country, company stage, and negotiation all create wide variance. Use these as orientation, not negotiation anchors.

| Role | Entry | Mid | Senior | Notes |
|------|-------|-----|--------|-------|
| Prompt Engineer | $80K-$110K | $110K-$150K | $150K-$180K | Shrinking standalone market |
| Context Engineer | $100K-$140K | $140K-$180K | $180K-$230K | Growing fast |
| AI Engineer | $120K-$160K | $160K-$220K | $220K-$300K | Highest volume of open roles |
| LLM Engineer | $130K-$170K | $170K-$250K | $250K-$350K | Lab-level roles higher |
| AI Agent Engineer | $130K-$170K | $170K-$240K | $240K-$320K | Strong demand 2025-2026 |
| Founding AI Engineer | $100K-$150K + equity | N/A | N/A | Equity makes total comp wide-ranging |
| AI Architect | N/A | $180K-$260K | $260K-$380K | Senior/Staff only |
| Platform Engineer (AI) | $110K-$150K | $150K-$210K | $210K-$280K | |
| Harness Engineer | Not yet standardized | N/A | N/A | Absorbed into other roles |
| AI Product Manager | $130K-$170K | $170K-$230K | $230K-$350K | FAANG premium significant |
| AI Safety/Eval Engineer | $140K-$180K | $180K-$250K | $250K-$400K | Lab compensation highest |
| ML Engineer | $100K-$140K | $140K-$200K | $200K-$280K | Lower demand outside labs |
| MLOps Engineer | $110K-$150K | $150K-$200K | $200K-$270K | High demand in enterprises deploying at scale |
| AI Developer Advocate | $120K-$160K | $160K-$220K | $220K-$300K | Active hiring at AI platforms |
| AI Orchestration Engineer | $100K-$140K | $140K-$190K | $190K-$260K | Emerging, title varies across companies |
| Spec Engineer | $90K-$130K | $130K-$180K | $180K-$250K | Often embedded in engineering teams, not standalone |
| Agent Identity Architect | N/A | $170K-$240K | $240K-$340K | Senior only; deep IAM expertise required |
| AI Eval Engineer | $110K-$150K | $150K-$210K | $210K-$290K | Growing rapidly as agentic systems reach production |

> **Sources**: FinalRoundAI (2025), Alcor AI Salary Report (2025), RiseWorks AI Talent Report (2025), job postings analysis. New roles (Spec Engineer, Agent Identity Architect, AI Eval Engineer) are estimated from adjacent role benchmarks and emerging job postings. Treat with wider margin.

---

## 22. What's Not a Role (Yet)

Some terms you'll hear that describe practices or methodologies, not job titles:

**Vibe coder**: a methodology (use AI coding assistants to handle implementation while you focus on design), not a job. Andrej Karpathy coined the term then himself pivoted toward "context engineering" as more precise. No serious company has "Vibe Coder" on a job description.

**AI-native engineer**: describes a quality expected of all engineers increasingly, not a specialized role. It means: you use AI tools fluently in your daily workflow. It's the bar, not the title.

These terms are worth knowing (you'll encounter them in job descriptions and articles) but don't represent distinct career paths, at least not yet.

---

## 23. Job Listings

> **Coming soon**: curated listings for AI roles at companies building seriously with Claude Code and agentic AI.

If you're hiring for any of the roles described in this guide, [reach out](https://florian.bruniaux.com) to discuss featuring your opportunity here.

---

## See Also

- [Learning to Code with AI](./learning-with-ai.md): skill development for developers using AI
- [AI Ecosystem: Tools & Integrations](../ecosystem/ai-ecosystem.md): which tools each role uses
- [Methodologies](../core/methodologies.md): TDD, SDD, BDD workflows relevant to AI engineers
- [Architecture](../core/architecture.md): how Claude Code works, relevant for AI agent engineers
- [Security Hardening](../security/security-hardening.md): critical reading for AI Safety engineers and Platform engineers