---
title: "AI Roles & Career Paths: The New Engineering Landscape"
description: "Evidence-bounded map of current AI role families, emerging specializations, and capabilities absorbed into broader engineering jobs"
tags: [roles, careers, ai-engineer, applied-ai-engineer, ai-platform-engineer, ai-security, ai-governance, guide]
---

# AI Roles & Career Paths: The New Engineering Landscape

> **Last updated**: August 31, 2026
>
> **Confidence**: Tier 2. Current employer postings establish that a title exists, but not its market share, growth rate, or durability.
>
> **Reading time**: ~30 minutes

AI adoption has created new job families and changed the scope of established engineering roles. This guide maps what each family owns, how adjacent roles differ, and how much evidence supports each title.

Read the profiles as a **capability map**, not an organization chart with one seat per section. New specialist titles are appearing while product teams ask fewer people to own a wider path from business intent to production. A title can disappear inside a broader role while the underlying capability remains necessary.

---

## Table of Contents

1. [The Landscape in One View](#1-the-landscape-in-one-view)
2. [Prompt Engineer](#2-prompt-engineer)
3. [Context Engineer](#3-context-engineer)
4. [AI Engineer](#4-ai-engineer)
5. [Applied AI Engineer](#5-applied-ai-engineer)
6. [LLM Engineer](#6-llm-engineer)
7. [AI Agent Engineer](#7-ai-agent-engineer)
8. [Founding AI Engineer](#8-founding-ai-engineer)
9. [AI Architect](#9-ai-architect)
10. [AI Platform Engineer](#10-ai-platform-engineer)
11. [Harness Engineer](#11-harness-engineer)
12. [AI Product Manager](#12-ai-product-manager)
13. [AI Safety Engineer](#13-ai-safety-engineer)
14. [ML Engineer](#14-ml-engineer)
15. [MLOps Engineer](#15-mlops-engineer)
16. [AI Developer Advocate](#16-ai-developer-advocate)
17. [AI Orchestration Engineer](#17-ai-orchestration-engineer)
18. [Spec Engineer](#18-spec-engineer)
19. [Agent Identity Architect](#19-agent-identity-architect)
20. [AI Evaluation Engineer](#20-ai-evaluation-engineer)
21. [Forward-Deployed Engineer (FDE)](#21-forward-deployed-engineer-fde)
22. [AI Security Engineer](#22-ai-security-engineer)
23. [AI Governance Engineer](#23-ai-governance-engineer)
24. [Career Decision Matrix](#24-career-decision-matrix)
25. [Compensation Evidence](#25-compensation-evidence)
26. [Capabilities and Title Qualifiers](#26-capabilities-and-title-qualifiers)
27. [Evidence Snapshot](#27-evidence-snapshot)
28. [Job Listings](#28-job-listings)

---

## 1. The Landscape in One View

The market separates more reliably by **ownership boundary** than by title. Current postings support five broad families:

| Ownership boundary | Current role families | Typical outcome |
|--------------------|-----------------------|-----------------|
| Model and research | ML Engineer, LLM Engineer, AI Safety Engineer | Train, adapt, study, or stress-test models |
| Application and product | AI Engineer, Applied AI Engineer, AI Agent Engineer, AI Product Manager | Turn model capability into a measurable product behavior |
| Shared production platform | AI Platform Engineer, MLOps Engineer, AI Architect | Give product teams reusable, governed paths to deploy and operate AI |
| Customer deployment | Forward-Deployed Engineer, AI Developer Advocate | Move a platform into customer workflows or developer adoption |
| Assurance and control | AI Evaluation Engineer, AI Security Engineer, AI Governance Engineer | Measure behavior, reduce technical risk, and encode policy as controls and evidence |

This page uses four evidence labels:

| Label | Meaning |
|-------|---------|
| **Role family** | Current official postings at three or more unrelated employers use the title or a close variant with a consistent ownership boundary |
| **Specialization or qualifier** | Real work and some current titles exist, but employers place it under several broader job families |
| **Capability** | The work is necessary, but current evidence does not support a stable standalone job family |
| **Forecasted team shape** | An analyst or employer proposes an operating model; this does not prove a labor-market title |

This is a dated source snapshot, not a census. It does not infer market volume from search-result counts, expired postings, title aggregators, or salary-estimate sites.

### Role titles multiply while team boundaries compress

Gartner's July 2026 forecast gives the organizational counterpoint to the role catalog above. It predicts that [60% of organizations will adopt smaller software engineering teams at scale by 2029](https://www.gartner.com/en/newsroom/press-releases/2026-07-07-gartner-predicts-60-percent-of-organizations-will-adopt-smaller-software-engineering-teams-by-2029), up from 15% in 2026. Gartner describes today's "tiny teams" as typically four or five people, with two or three becoming more common as skills and AI capabilities mature. This is a forecast, not a measured productivity result, and Gartner explicitly rejects interpreting it as a cost-cutting tactic.

The [role-compression research accompanying that forecast](https://www.gartner.com/en/documents/7929609) groups existing capabilities into three operating shapes. Treat these as ownership patterns rather than mandatory job titles:

| Team shape | Capabilities brought together | Primary ownership |
|------------|-------------------------------|-------------------|
| **Product engineers** | Product management, software engineering, UX/AX, QA, and delivery | Carry a product outcome from problem framing through design, implementation, verification, and operation |
| **Forward-deployed engineers** | Business analysis, requirements, service delivery, architecture, and implementation | Work close to a customer or domain, translate operational needs into a deployed system, and close the feedback loop |
| **AI platform team** | Platform engineering, DevOps/SRE, agent operations, data science, ML engineering, and AI engineering | Provide shared models, agent infrastructure, identities, evals, observability, security controls, and paved roads |

Compression removes handoffs, not expertise or accountability. A product engineer still needs credible UX research and verification. A forward-deployed engineer still needs architectural and domain judgment. A small product team can own more surface area only when a platform team absorbs repeated infrastructure work and supplies enforceable guardrails.

Use four gates before combining roles:

1. **Name the retained capability.** If the QA title disappears, specify who designs tests, owns release evidence, and can block a deployment.
2. **Preserve independent review where failure matters.** Security, privacy, accessibility, financial controls, and safety-critical changes may require a reviewer who did not produce the work.
3. **Fund the shared platform.** Self-service agents without identity, eval, observability, cost, and rollback controls move coordination cost into incidents.
4. **Keep an apprenticeship path.** Gartner separately predicts that organizations using AI to cut junior roles will hollow out their software engineering talent pipeline by 2028. Smaller teams still need supervised work, knowledge transfer, and progression from junior to independent ownership.

The career consequence is breadth around a technical spine. Build deep judgment in one capability, then add enough product, verification, and agent supervision skill to own a wider outcome. Choose openings by the decisions and evidence you will own, not by whether the title exactly matches one profile on this page.

### Front-end expertise persists as titles broaden

The available evidence supports a change in labels and ownership boundaries, not the disappearance of front-end work. Stack Overflow fielded its 2025 survey from May 29 to June 23 and asked respondents which role described their current job, or the job they held for the longest period during the previous year. Its [published role dataset](https://github.com/StackExchange/Survey/blob/main/packages/archive/2025/json/developer-profile.json) reports 26.96% for full-stack developer and 4.25% for front-end developer. In the France subset, the corresponding figures are 25.21% and 3.48%. The survey recorded 43,560 answers to the role question, but it measures self-identification among respondents rather than employer demand. Stack Overflow also added an architect category in 2025, and its [recruitment method](https://survey.stackoverflow.co/2025/methodology) overrepresents people who engage with its channels. Treat the figures as a dated classification signal, not a count of job openings or a clean causal time series.

LinkedIn's [2026 US Software Engineer talent report](https://economicgraph.linkedin.com/content/dam/me/economicgraph/en-us/PDF/us-software-engineer-talent-landscape-2026.pdf) provides a separate hiring signal based on aggregated LinkedIn profiles and job postings, with 2025 data running through October. React and JavaScript remain among the leading skills of recent software-engineering hires, and Tailwind CSS appears among the fastest-growing skills. The same report records stronger demand for Python, cloud platforms, and AI. That combination is consistent with employers retaining front-end capabilities inside broader engineering scopes. It does not establish that AI caused a decline in front-end titles. LinkedIn's [Jobs on the Rise 2026 analysis](https://www.linkedin.com/pulse/linkedin-jobs-rise-2026-fastest-growing-roles-europe-gabvc/), based on job starts from January 2023 through July 2025, also places AI Engineer among the growing roles in France and identifies Software Engineer, Data Scientist, and ML Engineer as common prior roles. This documents movement from established roles into AI work, not the displacement of a specific front-end population.

Job titles vary enough that a front-end specialist should search by ownership boundary as well as label:

| Search family | Scope to verify in the job description | Front-end depth that may remain central |
|---------------|----------------------------------------|-----------------------------------------|
| Front-end Engineer or Frontend Engineer | Browser architecture, interfaces, state, and client delivery | Accessibility, interaction quality, performance, and framework judgment |
| Software Engineer, Product or Product Engineer | A user-facing outcome from problem framing through operation | Product discovery, interface implementation, instrumentation, and iteration |
| Full-Stack Engineer | Interface, API or service logic, data, and deployment | A production UI plus credible ownership beyond the browser |
| UI Engineer or Design Engineer | Interaction design, prototyping, visual systems, and implementation | Design systems, responsive behavior, motion, and accessibility |
| Frontend Platform Engineer | Shared browser tooling and paved roads for product teams | Build systems, component infrastructure, performance, testing, and developer experience |

These labels are search families, not universal equivalences. Employers can use the same title for different work. Read the decisions, production surface, and evidence expected in the posting before choosing a label for a CV or profile.

For career positioning, use a broad family plus a demonstrated technical spine: **Software Engineer or Product Engineer with a front-end specialization**. Keep Front-end Engineer when the target role requires deep browser ownership. Use Full-Stack Engineer only when shipped work demonstrates meaningful ownership on both sides of the interface. Using an AI coding agent does not by itself justify an AI Engineer title.

A portfolio can establish that broader scope with one production-grade vertical slice. Show the user problem, accessible interaction, state and data flow, API and authentication boundary, tests, performance evidence, observability, deployment path, and rollback or failure handling. An AI-enabled feature also needs evals and behavior-specific failure handling. The goal is to expose the ownership boundary and its limits, not to claim equal expertise in every layer.

Python is a useful expansion path because current hiring data connects it to back-end, cloud, data, and AI work. It is not a universal requirement. TypeScript and Node.js, Java, Go, C#, and other stacks can provide the same service-side evidence when they match the target market. Choose one credible path beyond the browser and prove it through shipped behavior.

> **Measure title drift without manufacturing a trend**
>
> Record the platform, geography, query, filters, and collection dates. Deduplicate reposted vacancies by employer, role, location, and source identifier. Report both the count for each title family and the total number of unique postings. Measure required skills separately from titles, since a React position may appear under Product Engineer or Software Engineer. Compare periods only when the collection method is stable. Unless the study identifies a causal mechanism and controls for the broader hiring cycle, record AI attribution as **UNKNOWN**.

---

## 2. Prompt Engineer

**Evidence label**: Capability. Prompt design appears inside broader product, applied AI, evaluation, and domain roles; the evidence reviewed in August 2026 does not support treating Prompt Engineer as a durable standalone family.

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

Prompt design remains necessary, but production ownership now usually includes context, evaluation, data, integration, and monitoring. Treat prompt engineering as one skill in an AI Engineer, Applied AI Engineer, domain specialist, or evaluation role unless an employer's scope says otherwise.

### Entry paths

Technical writer, QA engineer, domain expert (law, medicine, finance), content strategist.

---

## 3. Context Engineer

**Evidence label**: Specialization. Current postings use Context Engineer and adjacent titles, but employers also assign the same work to AI, applied AI, platform, and developer-productivity engineers.

### What they do

Context engineers design **systems** that give models the right information, tools, and constraints at the right time. That scope includes retrieval, memory, tool descriptions, repository instructions, and context-budget management. The discipline is broader than prompt wording, but current evidence does not establish one standard organizational boundary for the title.

See the [Context Engineering reference](../core/context-engineering.md) for the full discipline, including the ACE pipeline (Section 6), the L0→L5 maturity model (Section 9), and the operational mechanisms that separate a Level 4 from a Level 5 system: signal taxonomy and causal attribution (Section 10), PR-based loop closure (Section 11), ejection of dormant rules (Section 12), constitutional audits (Section 13), and multi-dev profile reconciliation (Section 14).

> "Context Engineering is providing the right information and tools, in the right format, at the right time." (Philipp Schmid, Google)

The article [Context engineering became a job title](https://www.florian.bruniaux.com/blog/articles/context-engineering-the-new-roles/) documents early title adoption. Treat it as evidence of emergence, not proof of market volume.

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

**Evidence label**: Role family. AI Engineer is the broad application-engineering title; employer scope still ranges from model adaptation to full-stack product delivery.

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

## 5. Applied AI Engineer

**Evidence label**: Role family. Current official postings from OpenAI, Cohere, Cognition, Console, and other employers use the exact title, but they do not all place the role at the same customer boundary.

### What they do

Turn available models into production behavior for a defined product or workflow. Applied AI Engineers spend less time on foundation-model research than LLM or ML Engineers and more time on application architecture, context, evals, tool use, data integration, guardrails, and iteration with users.

The title does **not** imply customer-facing deployment. [OpenAI describes Applied AI Engineering](https://openai.com/careers/applied-ai-engineer-enterprise-san-francisco/) around safe, reliable production systems. [Cohere's Agentic Workflows role](https://jobs.ashbyhq.com/cohere/5e488a01-f015-48e8-8d25-a41cf19ab45a) includes enterprise agents and customer collaboration, while [Console's posting](https://jobs.ashbyhq.com/console/7d8114fa-4cbd-4c23-a6ba-5154b31c1d80) places the same title inside product engineering. Read the ownership boundary in the job description, not the title alone.

### Responsibilities

- Build AI product features and workflows against existing model APIs or open models
- Design context, retrieval, tool-use, and agent-control paths
- Create eval datasets and regression gates tied to user outcomes
- Instrument latency, cost, errors, model behavior, and fallbacks in production
- Work with product, domain, security, and platform peers to close the loop from observed failure to system change

### Distinction from adjacent roles

| Role | Primary ownership |
|------|-------------------|
| **AI Engineer** | Broad umbrella for AI-enabled software systems |
| **Applied AI Engineer** | Application behavior and measurable workflow outcomes using available models |
| **LLM Engineer** | Model adaptation, fine-tuning, inference, and model-level evaluation |
| **Forward-Deployed Engineer** | Deployment and adoption inside a customer's environment |
| **AI Platform Engineer** | Shared services and controls used by multiple AI product teams |

### Required skills

Strong software engineering, Python or TypeScript, model APIs, RAG and tool integration, evaluation design, observability, production debugging, and product judgment under non-deterministic behavior.

### Entry paths

Backend, full-stack, product, data, or ML engineer with evidence of shipping and measuring an AI workflow in production.

---

## 6. LLM Engineer

**Evidence label**: Specialization or role family, depending on the employer. The title is current, but its scope overlaps ML Engineer, Research Engineer, and AI Engineer.

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

## 7. AI Agent Engineer

**Evidence label**: Emerging role family. Current employers use AI Agent Engineer and close variants, while many others place the same scope under Software Engineer or Applied AI Engineer.

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

## 8. Founding AI Engineer

**Evidence label**: Title qualifier. Founding describes company stage and ownership breadth more reliably than a distinct technical discipline.

### What they do

A hybrid role unique to early-stage companies: part AI engineer, part product engineer, part technical co-founder. They own core product functionality end-to-end, from architecture decisions to customer interactions, while building on top of AI capabilities.

Seniority varies by startup. The stable signal is early ownership of product, architecture, delivery, and customer feedback, not an experience range inferred from the word "founding."

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

## 9. AI Architect

**Evidence label**: Role family, usually senior or staff level. AI Architect, Applied AI Architect, and Enterprise AI Architect postings share system-level decision ownership but differ in how hands-on they are.

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

Senior or staff AI engineer moving into cross-team architecture. Another path is a cloud or platform architect who adds model, evaluation, and AI-governance depth.

---

## 10. AI Platform Engineer

**Evidence label**: Role family. AI Platform Engineer now appears as an exact title across finance, media, healthcare, consulting, and software employers.

### What they do

Build and operate the shared services that product teams use to create, evaluate, deploy, govern, and observe AI applications. Current postings make the AI scope explicit rather than treating it as a minor extension of generic platform engineering.

[BlackRock's current description](https://careers.blackrock.com/job/budapest/senior-ai-platform-engineer-vice-president-director/45831/99445872944) covers shared APIs, SDKs, agent runtimes, evaluation systems, observability, retrieval, guardrails, and governance. [Realtor.com](https://job-boards.greenhouse.io/rdccareers/jobs/7808378003?gh_jid=7808378003), [Absa](https://absa.wd3.myworkdayjobs.com/en-GB/ABSAcareersite/job/Senior-AI-Platform-Engineer--Cloud----KE_R-15989910), and [Alcon](https://alcon.wd5.myworkdayjobs.com/en-US/careers_alcon/job/Senior-AI-Platform-Engineer_R-2026-47897) show the same ownership boundary with different cloud, cost, and regulatory constraints.

### Responsibilities

- Provide standardized LLM integration patterns (internal SDKs, proxies, abstractions)
- Manage API keys, rate limits, and cost allocation across teams
- Build AI observability infrastructure (tracing, logging, alerting)
- Enforce security policies for AI outputs (PII filtering, output validation)
- Maintain model registries and versioning systems
- Create "paved roads" for RAG patterns, agent architectures, eval pipelines

### Organizational boundary

The platform team owns reusable infrastructure, developer experience, and enforceable controls. Product or domain teams own each use case, acceptance criteria, and operational outcome. Centralizing use-case decisions in the platform team creates a queue; decentralizing credentials, observability, and guardrails creates inconsistent controls. The boundary should separate shared mechanisms from product accountability.

### Required skills (AI additions)

MLOps tooling, LLM gateway products (LiteLLM, Portkey), cloud AI services, cost optimization patterns, security for AI (prompt injection mitigation, output filtering).

---

## 11. Harness Engineer

**Evidence label**: Capability. Harness engineering names a production discipline; the evidence reviewed does not support a stable standalone Harness Engineer job family.

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

### Organizational home

Platform engineers, staff engineers, developer-productivity teams, and architecture groups currently own this work. Treat Harness Engineer as a search keyword and capability profile, not as a forecast that every organization will create the title.

### Required skills

Software architecture, linter/static analysis tooling, LLM orchestration, observability, codebase knowledge management, entropy detection patterns.

---

## 12. AI Product Manager

**Evidence label**: Role family. AI Product Manager and product-manager titles scoped to AI are current, but compensation premiums require employer- and level-specific evidence.

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

---

## 13. AI Safety Engineer

**Evidence label**: Role family. Safety work appears under Software Engineer, Research Engineer, ML/Research Engineer, red-team, safeguards, and alignment titles. Evaluation is separated in Section 20 because it has a different production boundary.

### What they do

Identify, measure, and reduce safety-relevant model or system behavior. The role can sit close to research, safeguards engineering, alignment, policy enforcement, or adversarial testing. It differs from AI Security Engineering: safety asks whether the system causes unacceptable behavior or harm; security asks how an attacker or compromised component can violate confidentiality, integrity, authorization, or availability.

### Responsibilities

- Red-team AI systems to find failure modes, jailbreaks, and harmful outputs
- Build or validate safeguards, classifiers, output controls, and escalation paths
- Design human-in-the-loop checkpoints for high-risk decisions
- Define threat models and evaluations for misuse, alignment, or domain-specific harm
- Monitor deployed systems for safety regressions and emerging abuse patterns
- Translate findings into model, product, policy, or deployment changes

### Required skills

Experimental design, statistics, Python, adversarial testing, model-behavior analysis, and clear risk reporting. Research-facing roles may require deeper ML or publication experience; production-facing safeguards roles may require stronger backend and incident-response skills.

### Where to find these roles

[Anthropic's current careers page](https://www.anthropic.com/careers/jobs) includes safeguards, alignment, frontier red-team, and safety-research engineering titles. OpenAI and Google DeepMind also divide safety work across research and software-engineering families. These examples establish the work and title family, not a market-wide hiring rate.

---

## 14. ML Engineer

**Evidence label**: Established role family.

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

## 15. MLOps Engineer

**Evidence label**: Established role family, with substantial overlap with AI Platform Engineer in some organizations.

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

## 16. AI Developer Advocate

**Evidence label**: Role family, often posted as Developer Advocate, Developer Relations Engineer, or Technical Evangelist for an AI platform.

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

### Where these roles are

AI labs, model providers, agent frameworks, and developer-facing platforms use Developer Advocate or Developer Relations titles. Confirm the current employer and product scope before treating an old listing as evidence of an open role.

### Entry paths

Software engineer with a public presence (blog, open source, conference talks), technical writer with engineering background, early AI community member who builds in public.

---

## 17. AI Orchestration Engineer

**Evidence label**: Specialization. Current titles vary, and many employers place orchestration inside Applied AI, AI Agent, integration, or platform engineering.

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

## 18. Spec Engineer

**Evidence label**: Capability. Spec-driven development is an observable practice, but current evidence does not establish Spec Engineer as a durable standalone title.

### What they do

Write the structured specifications that AI agents use to plan, implement, and validate code. This capability bridges business intent, human review, and machine-executable acceptance criteria. It can belong to a product engineer, requirements analyst, QA engineer, technical writer, or domain expert.

### Core responsibility

Writing specifications that satisfy three conditions simultaneously: precise enough for an agent to generate correct code from them, human-readable enough for a product manager to approve them, and stable enough to serve as the diff-able ground truth when the implementation drifts.

[GitHub Spec Kit](https://github.com/github/spec-kit) formalizes a Constitution, Specify, Plan, and Tasks workflow around versioned artifacts. Tool adoption does not establish Spec Engineer as a market title.

### Required skills

| Technical | Soft |
|-----------|------|
| Structured writing (Gherkin-style Given-When-Then or equivalent) | Precision under ambiguity |
| Understanding of agent failure modes on multi-file and long-horizon tasks | Negotiation across product, engineering, and domain constraints |
| Familiarity with SDD tools (Spec Kit, Kiro, Augment, Factory.ai) | Ability to distinguish what the spec must constrain vs what it should leave open |
| Version control discipline (specs versioned before code) | |

### Entry paths

Technical writer with engineering background, QA engineer who understands requirements, product engineer frustrated by low signal-to-noise in AI outputs, business analyst moving into AI-adjacent work.

---

## 19. Agent Identity Architect

**Evidence label**: Capability. Agent identity is a distinct control problem, but current postings usually assign it to AI Security, IAM, platform security, or AI Platform roles rather than an Agent Identity Architect family.

### What they do

Design and enforce the identity layer for AI agents: how agents authenticate to services, what permissions they hold, how those permissions are scoped and audited, and how privilege escalation is prevented when agents chain tool calls across services.

### Why the capability matters

Agents combine delegated authority, access to private data, exposure to untrusted content, and external actions. Shared credentials or inherited permissions make attribution and least privilege difficult. The control boundary therefore needs an identity per workload or session, scoped authorization, auditable delegation, and explicit handling of sub-agent privileges.

### What the role covers

- **Workload identity**: issue identities per agent workload or session instead of sharing team credentials.
- **Delegated authorization**: bind each action to a user, service, task, and allowed scope with expiry and revocation.
- **Tool enforcement**: validate tool calls against the current task scope at an identity-aware gateway or equivalent policy point.
- **Session tracing**: attribute each action to a specific agent session and delegation chain, not just "the AI system."
- **Sub-agent controls**: define permission inheritance explicitly and reduce child scope to the minimum required for the delegated task.

### Required skills

IAM and OAuth/OIDC expertise, zero-trust architecture, Kubernetes RBAC, understanding of MCP security model, incident response for non-deterministic systems.

### Entry paths

Cloud security engineer, identity/access management specialist, platform engineer with security focus.

---

## 20. AI Evaluation Engineer

**Evidence label**: Role family with unstable naming. Current titles include Research Engineer, Model Evaluations; Backend Software Engineer (Evals); evaluation-infrastructure leadership; and product-specific AI evaluation engineering.

### What they do

Build and operate the measurement layer that tells an organization whether model or system behavior meets explicit criteria over time. Evaluation can target model capabilities, safety, a product workflow, an agent trajectory, or the infrastructure that runs those tests.

### Why the title varies

[Anthropic currently lists Research Engineer, Model Evaluations and Evals Infrastructure leadership](https://www.anthropic.com/careers/jobs). [OpenAI's Backend Software Engineer (Evals)](https://openai.com/careers/backend-software-engineer-%28evals%29-san-francisco/) builds reproducible pipelines, golden datasets, drift monitoring, and evaluation services for a product domain. These postings confirm a role family but also show that research, infrastructure, and product evaluation require different profiles.

### Responsibilities

- Design evaluation frameworks with explicit metrics (task completion rate, tool correctness rate, hallucination rate)
- Build reproducible datasets, runners, and comparison pipelines
- Combine deterministic checks, human review, and model-based graders with documented limitations
- Detect regressions across model, prompt, context, tool, or traffic changes
- Maintain benchmark provenance and test for contamination or overfitting
- Connect evaluation results to release gates, incident analysis, and product decisions

### Required skills

Statistical experiment design, Python, task and failure-mode analysis, dataset curation, grader validation, CI/CD integration, and reproducible reporting.

### Tools

Tool choice depends on the boundary: test runners for deterministic checks, experiment stores for datasets and versions, tracing for agent trajectories, human-review interfaces, and model-based graders whose error rates are measured against labeled samples.

---

## 21. Forward-Deployed Engineer (FDE)

**Evidence label**: Role family. Current official postings at OpenAI, Anthropic, ServiceNow, and other AI vendors use Forward-Deployed Engineer or a close variant.

### What they do

Own the technical deployment of an AI system inside a customer's real environment. FDEs work between the customer's domain and the vendor's product, taking a problem through discovery, architecture, implementation, evaluation, production rollout, adoption, and handoff. Field evidence then feeds back into reusable product capabilities and deployment standards.

[OpenAI's current FDE description](https://openai.com/careers/forward-deployed-engineer-%28fde%29-sf-san-francisco/) measures the role through production adoption, workflow impact, and eval-driven feedback rather than prototype delivery. [Anthropic also lists FDE positions](https://www.anthropic.com/careers/jobs) in the United States, France, and Germany as of August 2026. Current vacancies establish that the title is real; they do not establish how common it is across the broader market.

### Responsibilities

- Translate ambiguous customer workflows, data constraints, and domain rules into technical requirements and measurable outcomes
- Design and build the integration, evaluation, security, and production architecture
- Work directly with customer engineers, operators, and domain experts through rollout and adoption
- Make scope, speed, and quality trade-offs while retaining launch evidence and rollback paths
- Turn one deployment's lessons into reusable tools, playbooks, evals, or product improvements

### Distinction from adjacent roles

| Role | Primary boundary |
|------|------------------|
| **Solutions engineer** | Proves technical fit, often before or during a sale |
| **Forward-deployed engineer** | Owns hands-on technical delivery and production adoption in the customer's environment |
| **Product engineer** | Owns a reusable product surface for many customers |
| **AI architect** | Defines reference architecture and standards across deployments |

The boundary varies by employer. OpenAI's general posting explicitly separates technical solution ownership from the commercial or executive relationship, while domain-specific FDE roles can require regulated-industry knowledge and substantial travel.

### Required skills

Senior software or AI engineering, systems architecture, API and data integration, eval design, production operations, customer discovery, domain modeling, and clear communication under ambiguous requirements.

### Entry paths

Senior software engineer with customer-facing delivery experience, solutions architect who still writes production code, implementation engineer moving into end-to-end ownership, technical consultant with strong product and AI depth.

---

## 22. AI Security Engineer

**Evidence label**: Role family. Cisco, Apple, GuidePoint Security, Marvell, Prologis, Société Générale, and other employers use the exact title or a seniority-qualified variant in current official postings.

### What they do

Protect AI applications, models, data paths, agents, and supporting platforms against misuse and attack. AI Security Engineers combine application, cloud, identity, data, and adversarial-ML security rather than treating prompt injection as the whole problem.

[Apple's AI Security Engineer, Red Team](https://jobs.apple.com/en-us/search?team=sicurezza-e-privacy-SFTWR-SEC) focuses on deep technical reviews. [Marvell's AI Security Engineer](https://marvell.wd1.myworkdayjobs.com/en-US/MarvellCareers/job/AI-Security-Engineer_2603452) owns enterprise controls, runtime protection, identity, telemetry, and remediation. [Société Générale's Lead AI Security Engineer](https://careers.societegenerale.com/en/job-offers/lead-ai-security-engineer-aps-26000H78-en) combines AI red teaming with secure software engineering.

### Responsibilities

- Threat-model model APIs, RAG, agents, tools, data flows, identities, and third-party components
- Test prompt injection, data exfiltration, poisoning, insecure tool use, privilege escalation, and model or supply-chain abuse
- Build preventive and detective controls for inputs, outputs, runtime actions, data access, and credentials
- Integrate AI findings into AppSec, cloud security, IAM, detection, incident response, and vulnerability-management workflows
- Validate mitigations with repeatable tests and retain evidence for risk owners

### Distinction from adjacent roles

| Role | Primary question |
|------|------------------|
| **AI Security Engineer** | How can an attacker, compromised component, or unsafe integration violate a security property? |
| **AI Safety Engineer** | Which model or system behaviors create unacceptable harm or misuse risk? |
| **AI Governance Engineer** | How are policies, approvals, inventories, evidence, and regulatory controls encoded and operated? |

### Entry paths

Application security, cloud security, security architecture, adversarial ML, IAM, or platform security with hands-on AI application knowledge.

---

## 23. AI Governance Engineer

**Evidence label**: Role family, but less standardized than AI Security Engineer. Current postings at State Street, Deeploy, and Dalio Family Office use the exact title or a combined analyst/engineer variant.

### What they do

Turn AI policy, risk, and regulatory requirements into operational tooling and evidence. This is an engineering role when it builds catalogs, lineage, approval gates, policy checks, audit trails, and self-service controls. A governance analyst or policy lead may own interpretation and oversight without building those systems.

[Deeploy](https://jobs.ashbyhq.com/deeploy/9b78c07e-9c45-4581-8969-719896f590d9/) uses the title for customer implementation, while [State Street](https://statestreet.wd1.myworkdayjobs.com/en-US/Global/job/AI-Governance-Engineer--VP_R-794568) places it closer to enterprise architecture. The common boundary is control implementation, not one reporting line.

### Responsibilities

- Build and operate AI inventories, ownership records, risk classifications, and approval workflows
- Translate policy and regulatory obligations into technical requirements and automated checks
- Capture model, dataset, prompt, evaluation, deployment, and human-approval lineage
- Provide reusable controls and evidence for engineering, risk, legal, compliance, and audit stakeholders
- Monitor control coverage and exceptions instead of treating a policy document as proof of implementation

### Distinction from compliance and security

Governance Engineering encodes and operates controls. Legal, compliance, risk, and policy specialists interpret obligations and decide acceptable risk. AI Security Engineering tests and enforces technical security properties. One person may cover several boundaries in a small organization, but the accountabilities should remain explicit.

### Entry paths

Governance, risk, and compliance engineer; responsible-AI specialist with software skills; data-governance engineer; platform engineer in a regulated environment; or security engineer focused on control automation.

---

## 24. Career Decision Matrix

Choose the ownership boundary first, then compare titles. In a small AI-augmented team, a credible profile combines one deep specialty with adjacent product, verification, and agent-supervision skills.

| Current strength | Closest role family | Evidence to build |
|------------------|---------------------|-------------------|
| Product or backend engineering | AI Engineer or Applied AI Engineer | A shipped workflow with evals, observability, failure analysis, and cost data |
| Model training and experimentation | ML Engineer or LLM Engineer | Reproducible experiments, model comparisons, and deployment constraints |
| Cloud, SRE, or internal platforms | AI Platform Engineer or MLOps Engineer | A reusable deployment path with identity, tracing, rollback, and cost controls |
| Application or cloud security | AI Security Engineer | An AI threat model, adversarial tests, mitigations, and retest evidence |
| GRC, data governance, or control automation | AI Governance Engineer | A working inventory, approval gate, lineage path, or policy-as-code control |
| Statistics, QA, or experiment design | AI Evaluation Engineer | A versioned dataset, validated graders, regression report, and release gate |
| Customer-facing technical delivery | Forward-Deployed Engineer | Production integration, adoption result, handoff, and reusable field feedback |
| Product strategy and user research | AI Product Manager | Acceptance criteria for variable behavior and explicit quality, cost, latency, and fallback decisions |
| IAM or platform security | AI Security or AI Platform Engineer with agent-identity depth | Delegated authorization, session attribution, least privilege, and revocation design |
| Technical writing or requirements analysis | Product, QA, or Applied AI role with specification depth | A versioned specification linked to tests and implementation evidence |

### Portfolio proof

1. Build a real workflow against a model API or open model.
2. Define the task, failure modes, and acceptance criteria before polishing the demo.
3. Add a versioned evaluation set and report false positives, false negatives, and uncovered cases.
4. Instrument latency, cost, errors, tool actions, and fallback behavior.
5. Document one incident or failed approach and the evidence that justified the correction.

These artifacts demonstrate production judgment. They do not substitute for domain, research, security, or regulatory depth where the role requires it.

---

## 25. Compensation Evidence

The earlier version of this page published broad entry, mid, and senior ranges assembled from secondary salary sites and adjacent-role estimates. That method could not support title-level comparisons, especially for new roles with inconsistent scope. This revision removes those estimates.

Current employer disclosures can establish a range for one role, level, location, and date. They are not market benchmarks:

| Posting observed in August 2026 | Published base range | Evidence boundary |
|---------------------------------|----------------------|-------------------|
| [OpenAI Applied AI Engineer, Enterprise, US](https://openai.com/careers/applied-ai-engineer-enterprise-san-francisco/) | $197K to $278K, equity separate | Customer-facing enterprise scope at one employer |
| [OpenAI Forward-Deployed Engineer, San Francisco](https://openai.com/careers/forward-deployed-engineer-%28fde%29-sf-san-francisco/) | $162K to $280K, equity separate | One employer, one location, broad level range |
| [OpenAI Backend Software Engineer (Evals), San Francisco and Seattle](https://openai.com/careers/backend-software-engineer-%28evals%29-san-francisco/) | $266K to $445K, equity separate | Product-domain eval infrastructure, not every evaluation role |
| [Cisco AI Security Engineer, US locations](https://cisco.wd5.myworkdayjobs.com/en-US/Cisco_Careers/job/AI-Security-Engineer_2017667) | $150.3K to $195.2K | One posting with employer-specific research scope |
| [Marvell AI Security Engineer, Santa Clara or Austin](https://marvell.wd1.myworkdayjobs.com/en-US/MarvellCareers/job/AI-Security-Engineer_2603452) | $131.54K to $197K | One enterprise cyber-engineering role |
| [BlackRock Senior AI Platform Engineer, Budapest](https://careers.blackrock.com/job/budapest/senior-ai-platform-engineer-vice-president-director/45831/99445872944) | HUF 13.4M to 20.1M | Hungary, VP or Director level, employer-specific band |

For negotiation, compare live postings with the same country, city or remote policy, level, employer type, and compensation components. Do not convert one US lab range into a global role average.

---

## 26. Capabilities and Title Qualifiers

The report used for this update was right to challenge title inflation. It was too aggressive in recommending deletion: a weak standalone title does not make the capability obsolete.

| Term | Classification in this guide | Where the work usually sits |
|------|------------------------------|------------------------------|
| Prompt Engineer | Capability | AI, applied AI, product, evaluation, or domain role |
| Context Engineer | Specialization | AI, applied AI, platform, developer productivity, or data role |
| Harness Engineer | Capability | Platform, staff engineering, developer productivity, or architecture |
| AI Orchestration Engineer | Specialization | Applied AI, agent, integration, automation, or platform engineering |
| Spec Engineer | Capability | Product engineering, requirements, QA, technical writing, or domain ownership |
| Agent Identity Architect | Capability | AI security, IAM, platform security, or AI platform engineering |
| Founding AI Engineer | Title qualifier | Early-stage AI or product engineering with broad ownership |
| AI-native engineer | Proficiency profile | Engineer who can supervise agents and own a wider delivery path |
| Vibe coder | Practice label | AI-assisted implementation; not a defensible career family |

Use these terms to describe depth or search for adjacent postings. Do not design a team with one mandatory seat per term.

---

## 27. Evidence Snapshot

The following primary employer pages were live or indexed as current during the August 31, 2026 review. A live vacancy proves title usage at that employer on that date. It does not prove market share or future persistence.

| Role family | Cross-employer evidence sampled | Review conclusion |
|-------------|---------------------------------|-------------------|
| Applied AI Engineer | [OpenAI](https://openai.com/careers/applied-ai-engineer-enterprise-san-francisco/), [Cohere](https://jobs.ashbyhq.com/cohere/5e488a01-f015-48e8-8d25-a41cf19ab45a), [Cognition](https://jobs.ashbyhq.com/cognition/9dc5bcf6-469d-426d-a5ca-46062f4fa33b), [Console](https://jobs.ashbyhq.com/console/7d8114fa-4cbd-4c23-a6ba-5154b31c1d80) | Confirmed family; customer boundary varies |
| AI Platform Engineer | [BlackRock](https://careers.blackrock.com/job/budapest/senior-ai-platform-engineer-vice-president-director/45831/99445872944), [Realtor.com](https://job-boards.greenhouse.io/rdccareers/jobs/7808378003?gh_jid=7808378003), [Absa](https://absa.wd3.myworkdayjobs.com/en-GB/ABSAcareersite/job/Senior-AI-Platform-Engineer--Cloud----KE_R-15989910), [Alcon](https://alcon.wd5.myworkdayjobs.com/en-US/careers_alcon/job/Senior-AI-Platform-Engineer_R-2026-47897) | Confirmed family; absorbs part of MLOps, security, eval, and agent operations |
| AI Security Engineer | [Apple](https://jobs.apple.com/en-us/search?team=sicurezza-e-privacy-SFTWR-SEC), [Marvell](https://marvell.wd1.myworkdayjobs.com/en-US/MarvellCareers/job/AI-Security-Engineer_2603452), [Société Générale](https://careers.societegenerale.com/en/job-offers/lead-ai-security-engineer-aps-26000H78-en), [GuidePoint Security](https://job-boards.greenhouse.io/guidepointsecurity/jobs/6030474004?gh_jid=6030474004) | Confirmed technical security family |
| AI Governance Engineer | [State Street](https://statestreet.wd1.myworkdayjobs.com/en-US/Global/job/AI-Governance-Engineer--VP_R-794568), [Deeploy](https://jobs.ashbyhq.com/deeploy/9b78c07e-9c45-4581-8969-719896f590d9/), [Dalio Family Office](https://job-boards.greenhouse.io/marinomanagementllc/jobs/6133372004) | Confirmed family; scope ranges from internal tooling to customer implementation and architecture |
| AI Evaluation Engineer | [Anthropic careers](https://www.anthropic.com/careers/jobs), [OpenAI Backend Software Engineer (Evals)](https://openai.com/careers/backend-software-engineer-%28evals%29-san-francisco/), [Ellipsis Health](https://jobs.ashbyhq.com/ellipsis-health/60fb0284-8ba7-48a6-b66b-9bf4beb7b133) | Confirmed work family; no canonical title |
| Forward-Deployed Engineer | [OpenAI](https://openai.com/careers/forward-deployed-engineer-%28fde%29-sf-san-francisco/), [Anthropic](https://www.anthropic.com/careers/jobs), [ServiceNow team description](https://careers.servicenow.com/teams/ai-engineering-product/) | Confirmed customer-deployment family |

The Perplexity report supplied for this revision also cited aggregators, search snippets, social posts, and company-specific observations. Those sources helped find candidates but did not determine the final classification when primary employer evidence was available.

---

## 28. Job Listings

This page does not maintain a vacancy feed. Career pages change too quickly for a static list to stay current. Use the employer links in the evidence snapshot, then verify that the posting is still open and that its ownership boundary matches the profile described here.

---

## See Also

- [Learning to Code with AI](./learning-with-ai.md): skill development for developers using AI
- [AI Ecosystem: Tools & Integrations](../ecosystem/ai-ecosystem.md): which tools each role uses
- [Methodologies](../core/methodologies.md): TDD, SDD, BDD workflows relevant to AI engineers
- [Architecture](../core/architecture.md): how Claude Code works, relevant for AI agent engineers
- [Security Hardening](../security/security-hardening.md): critical reading for AI Safety engineers and Platform engineers
