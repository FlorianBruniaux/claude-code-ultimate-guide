---
title: "Practitioner Insights"
description: "Field reports from production teams on agentic systems, context engineering, LLM evaluation, and AI-assisted development"
tags: [guide, community, insights]
---

# Practitioner Insights

This page collects paraphrased field reports from engineers and technology leads who have built production systems with LLMs and agentic tooling. These are practitioner accounts, not vendor documentation. Every insight is attributed to its source.

The corpus now spans six sources on this page. [IFTTD](https://www.ifttd.io/) (If This Then Dev), a French tech podcast hosted by Bruno Soulez covering practical software engineering, remains the largest with episodes 290 to 361 (roughly 2024-2025) and verbatim transcripts for 55 recent episodes. Devoxx adds talks from its Java/JVM and architecture conference family, Dev With AI contributes from a French AI-native development meetup, and ByteByteGo covers system design. Stanford Online supplies academic coursework on machine learning and large language models. Pavan Belagatti's 62 English-language videos published in 2026 add a vendor-oriented view of agentic engineering, loop engineering, context platforms, and software factories. Every talk and episode across the six sources was analyzed for patterns applicable to Claude Code workflows and paraphrased; no direct quotes appear on this page. A seventh source, The Product Crew (a French product-management podcast), was analyzed for the same project but its insights are folded into the guide's adoption, roles, and unit-economics pages instead, since none of its material fit this page's themes; see [credits.md](../core/credits.md) for that attribution.

---

## Context Engineering

**Context quality beats context volume.** Filling a 1M-token window is not a sign of capability; it is often a mistake. LLMs attend better to information at the beginning and end of their context window than to what sits in the middle (see [Lost-in-the-Middle Problem](../core/context-engineering.md#the-lost-in-the-middle-problem)). Injecting large volumes of partially relevant text degrades focus without improving outcomes.

*Guillaume Laforge (Developer Advocate, Google Cloud), [IFTTD ep 361 "Pourquoi le RAG n'est pas mort"](https://www.ifttd.io/episodes/rag)*

---

**Specialized sub-agents receive narrower context on purpose.** The trend toward sub-agents is partly a context management strategy: each sub-agent gets only the slice of context it actually needs, rather than the full session history. A sub-agent validating a schema does not need the product roadmap. Isolation produces better focus and reduces token costs simultaneously.

*Guillaume Laforge (Developer Advocate, Google Cloud), [IFTTD ep 361 "Pourquoi le RAG n'est pas mort"](https://www.ifttd.io/episodes/rag)*

---

**"Harness engineering" is the emerging term for multi-agent context coordination.** Orchestrating several agents with isolated context windows requires deliberate decisions about what each agent receives and when. The discipline of managing this has started to be called harness engineering: you design the container that controls context flow, not just the agents themselves.

*Guillaume Laforge (Developer Advocate, Google Cloud), [IFTTD ep 361 "Pourquoi le RAG n'est pas mort"](https://www.ifttd.io/episodes/rag)*

---

**Semantic chunking outperforms fixed-token splitting.** When preparing knowledge for retrieval, chunking by semantic unit (paragraph, section, logical block) rather than by a fixed token count produces more coherent retrieval. A 500-token boundary drawn mid-sentence makes both resulting fragments ambiguous. See [§6 RAG Optimization](../ecosystem/context-engineering-tools.md#6-rag-optimization) for implementation detail.

*Guillaume Laforge (Developer Advocate, Google Cloud), [IFTTD ep 361 "Pourquoi le RAG n'est pas mort"](https://www.ifttd.io/episodes/rag)*

---

**Generating synthetic questions at index time improves retrieval matching.** Rather than indexing raw chunks and matching them against user queries, generate the questions a chunk would answer and index those instead. At query time, user questions match indexed questions far more consistently than they match raw prose. Laforge observed improvements around 10% on his evaluation sets; the doc2query and HyDE papers document similar mechanisms with varying gains depending on dataset.

*Guillaume Laforge (Developer Advocate, Google Cloud), [IFTTD ep 361 "Pourquoi le RAG n'est pas mort"](https://www.ifttd.io/episodes/rag)*

---

**A smarter model can actively degrade a RAG system.** A highly capable model that disagrees with retrieved context tends to favor its training knowledge instead. The result is technically coherent but misses the user's actual knowledge base entirely. The fix is explicit prompt instructions telling the model to prioritize injected context over its priors.

*Guillaume Laforge (Developer Advocate, Google Cloud), [IFTTD ep 361 "Pourquoi le RAG n'est pas mort"](https://www.ifttd.io/episodes/rag)*

---

**Inject live context into tool descriptions, not just the prompt body.** Tool descriptions are parsed by the model with high attention before the conversation begins. Including dynamic facts there (current date, session state, active tenant) reaches the model at a point of maximum focus and compensates for knowledge cutoffs without polluting the main prompt.

*Frédéric Barthelet (engineer), [IFTTD ep 329 "Front agentique"](https://www.ifttd.io/episodes/front-agentique)*

---

**Context quality drops sharply around 70% of the budget used, not gradually.** Nine independent speakers at the same meetup converged on this threshold: once a session crosses roughly 70% of its context window, output quality falls off a cliff rather than declining in a straight line. The practical implication is to purge or compact context before hitting that mark, not after symptoms appear. Malo and Dorian emphasized the abruptness of the drop specifically, warning that teams who wait for visible signs of confusion have usually already crossed the threshold.

*Emmanuel Sciara, Dev With AI Meetup, 2026; Malo and Dorian, same event and year*

---

**Too much context can cause hallucination just as reliably as too little.** The failure mode is symmetric: practitioners tend to guard against starving a model of context, but flooding it with more than it needs induces the same kind of confident, wrong answers. This nuances the 70% threshold above: the ceiling is not just about volume, it is about matching what is actually relevant to the task.

*Victor Rentea, Devoxx, 2026*

---

**A growing CLAUDE.md file degrades model performance, not just token cost.** The common reflex when an agent misbehaves is to add another paragraph to the system prompt. Multiple practitioners at the same meetup reported the opposite effect: past a certain size, the extra instructions compete for attention and measurably worsen output quality. Modularizing into separate, scoped files that get loaded only when relevant outperforms a single accumulating system prompt.

*Florian Allainmat, Dev With AI Meetup, 2026; Samuel Gallet & Geslain Dahan, Dev With AI Meetup, 2026*

---

**Markdown files work as persistent memory shared across agents, alongside a dedicated conventions file.** Rather than standing up a database for agent memory, plain Markdown files checked into the repository serve the same purpose: durable, versioned, and readable by both humans and agents. A separate file listing code convention rules complements this, mapping onto the same idea as a CLAUDE.md or AGENTS.md file.

*Alex Gavrilescu, Devoxx, 2025; Konstantin Pavlov, Devoxx, 2025*

---

**Structure agent work as Research, Plan, Implement, with a handoff document at each step.** Each phase produces an artifact (`research.md`, `plan.md`) that the next phase consumes instead of relying on conversational memory. The research document cites file paths and line numbers directly, so the plan phase can verify claims instead of trusting a summary.

*Emmanuel Sciara, Dev With AI Meetup, 2026*

---

**"Reasoning" in an LLM is operationally defined as the intermediate tokens generated between input and output, not a separate cognitive faculty.** A formal result attaches to this framing: a transformer allowed to produce a chain-of-thought can solve any problem solvable by a boolean circuit, given a constant number of intermediate steps. This is the theoretical grounding for deliberately giving a model room to generate tokens before an answer, the mechanism behind extended thinking and chain-of-thought prompting.

*Denny Zhou (Google DeepMind), Stanford CS25 V5, 2025*

---

**In-context generation often beats fine-tuning for injecting new knowledge.** Two independent courses converge on the same conclusion: retrieval-augmented prompting typically outperforms fine-tuning when the goal is teaching a model a new fact, partly because fine-tuned models suffer from the "reversal curse," learning that A implies B without being able to infer that B implies A.

*Stanford CS25, 2026; CS230 Lecture 8, 2025*

---

**A shared context layer needs provenance and revocation, not only retrieval.** Centralizing documentation, service relationships, runtime state, and ownership data can reduce tool fragmentation. The same layer can propagate stale or poisoned data to every connected agent. Treat freshness, source identity, scoped access, and rollback as part of the context contract rather than assuming that one shared catalog is authoritative.

*Pavan Belagatti, [Context Engineering Explained](https://www.youtube.com/watch?v=oExfgB9zRzA), 2026. The video demonstrates a Port-oriented architecture; the risk boundary is this guide's analysis, not a claim measured in the video.*

---

## Agentic Patterns & Orchestration

**A software factory is an operating model, not a product category alone.** The model, runtime harness, repository gates, orchestrator, and accountable humans own different decisions. A managed platform can package those layers, but it does not remove the need to define who writes intent, who accepts evidence, who handles exceptions, and who can release an irreversible change.

*Pavan Belagatti, [What Is a Software Factory?](https://www.youtube.com/watch?v=0nM1ygBm8tA) and [Build Your Own Software Factory](https://www.youtube.com/watch?v=pE1S1egMrAI), 2026*

---

**Removing the operator from repeated prompting does not remove human governance.** Loop engineering can automate planning, action, observation, and retry within a budget. Humans still own permissions, acceptance policy, exceptions, and high-impact releases. Separating the execution loop from the governance loop resolves the apparent conflict between unattended iteration and human approval gates.

*Pavan Belagatti, [Loop Engineering Explained](https://www.youtube.com/watch?v=RvG7R0Ue1k4) and the [human review gate in Build Your Own Software Factory](https://www.youtube.com/watch?v=pE1S1egMrAI&t=908s), 2026*

---

**One agent, one task.** A single agent that accumulates prompt additions over time degrades in unpredictable ways: fixing one behavior inadvertently breaks another. The alternative is small, focused agents with narrow instructions and explicit tool sets. Each agent becomes independently testable, observable, and replaceable.

*Samy Lastmann (CTO, Smart Tribune), [IFTTD ep 311 "IA Agentique"](https://www.ifttd.io/episodes/ia-agentique)*

---

**Not every step in an agent workflow needs a language model.** A pipeline step that matches a regex, queries a database, or looks up a key in a dictionary does not benefit from LLM reasoning. Injecting LLMs indiscriminately increases cost, latency, and variance. Reserve reasoning models for steps where genuine ambiguity exists.

*Samy Lastmann (CTO, Smart Tribune), [IFTTD ep 311 "IA Agentique"](https://www.ifttd.io/episodes/ia-agentique); Jocelyn N'takpe (Head of Engineering & Architecture, ManoMano), [IFTTD ep 346 "IA & DevX"](https://www.ifttd.io/episodes/ia-devx)*

---

**Design MCP tools as complete user journeys, not atomic endpoints.** A tool that handles only one API call forces the agent to chain five sequential calls, each introducing independent failure probability. A tool that encapsulates a full intent ("place the order") dramatically reduces the surface where the model can go wrong.

*Frédéric Barthelet (engineer), [IFTTD ep 329 "Front agentique"](https://www.ifttd.io/episodes/front-agentique)*

---

**Add a feedback tool to every MCP server you build.** A mechanism that lets the agent report problems in real time catches integration issues before they accumulate. It also provides a continuous signal for improving tool descriptions and parameter contracts.

*Frédéric Barthelet (engineer), [IFTTD ep 329 "Front agentique"](https://www.ifttd.io/episodes/front-agentique)*

---

**The MCP client holds all the intelligence; the LLM is stateless.** The model receives tool schemas and descriptions on each request but has no memory of prior tool calls from previous messages. Claude Code (as the client) is responsible for routing, retrying, and composing tool results. Treating a remote MCP server as an intelligent collaborator is a category error.

*Zineb Bendhiba (Principal Software Engineer, Red Hat), [IFTTD ep 326 "MCP Servers"](https://www.ifttd.io/episodes/mcp-servers)*

---

**More tools exposed to the model means more hallucinations.** Each tool schema consumes context tokens and adds decision surface. When the model is given 30 tools but only needs 3 for a task, the irrelevant 27 introduce noise. Keep active tool counts low; prefer targeted MCP servers with scoped permissions over general-purpose servers.

*Zineb Bendhiba (Principal Software Engineer, Red Hat), [IFTTD ep 326 "MCP Servers"](https://www.ifttd.io/episodes/mcp-servers)*

---

**Routing prompts by complexity to the right model cuts costs by roughly half.** Rather than sending every request to the most capable and most expensive model, a routing layer evaluates prompt complexity and dispatches simple requests to cheaper models. Antonio Goncalves observed approximately a 2x cost reduction in production; academic work on RouteLLM (LMSYS, [arXiv 2406.18665](https://arxiv.org/abs/2406.18665)) documents similar gains with no significant quality loss on benchmarks.

*Antonio Goncalves (Java Champion, developer advocate), [IFTTD ep 357 "Dans l'ouragan des modèles"](https://www.ifttd.io/episodes/azure-et-ia)*

---

**Orchestrate large-context models for tasks that exceed the primary model's window.** Quentin Adam's pattern: Claude decomposes a task and orchestrates Gemini (which has a larger context window) to execute large rewrites on massive codebases. The planning and task formulation stay with the more capable reasoner; the brute execution of large reads goes to the model best suited for bulk context ingestion.

*Quentin Adam (CEO, Clever Cloud), [IFTTD ep 341 "Bilan 2025"](https://www.ifttd.io/episodes/bilan-2025)*

---

**Design systems now for agents as the primary users.** Rate limits, throughput assumptions, and API contracts built for human interaction patterns collapse when an automated client generates 10,000 to 50,000 operations per day. Systems that will serve agents need to be designed for it from the start.

*Antonio Goncalves (Java Champion, developer advocate), [IFTTD ep 357 "Dans l'ouragan des modèles"](https://www.ifttd.io/episodes/azure-et-ia)*

---

**Claude Code does not loop indefinitely by default; define explicit exit criteria anyway.** A session left without a completion promise or a maximum iteration count can burn tokens without ever converging on a working state. Setting an explicit stopping condition, either a defined "done" state or a hard iteration cap, prevents the agent from spinning on a task it cannot resolve.

*Vyncke, Dev With AI Meetup, 2026*

---

**Over-constraining an agent degrades output about as much as giving it no spec at all.** This is the "spec paradox": a rigid, exhaustive specification leaves no room for the model to apply judgment, producing brittle results similar to an underspecified prompt. Counterintuitively, a more ambitious goal sometimes improves the creativity of what comes back. A field report from Picnic illustrates the failure mode downstream: perceived productivity with an AI assistant rises in the short term, then degrades once review capacity cannot keep pace, and code shipped fast ends up needing repeated rework.

*Max Sumrall, Devoxx, 2026*

---

**Insert an "analyze" step between plan and implementation.** This step triangulates the spec, the plan, and the task breakdown against each other, surfacing contradictions and orphaned tasks before any code gets touched. Catching a mismatch at this stage costs a re-read; catching it during implementation costs a rewrite.

*Luis Iglesias Hernandez, Dev With AI Meetup, 2026*

---

**LLMs do not solve combinatorial optimization problems; pair them with classical solvers instead.** Planning and routing problems, vehicle routing or scheduling for instance, are exactly the kind of task where asking a model for a complete solution produces plausible-looking but wrong answers. The practical boundary: let the model handle the parts that require language and judgment, and delegate the actual optimization to a dedicated solver.

*Tom Cools, Devoxx, 2026*

---

**Externalize every effectful operation through controlled, validated, and logged tools; never let the model act directly on the system.** Script execution, file writes, and any other operation with side effects should go through a runtime that validates and journals the action, rather than trusting the model's direct output. This keeps a deterministic audit trail between what the model proposes and what actually executes.

*Alexandre Balmes, Dev With AI Meetup, 2026; Florian Allainmat, Dev With AI Meetup, 2026*

---

**Start simple, measure, and add complexity only once the need is proven.** Designing for maximum scale from day one is a common anti-pattern: the complexity cost lands immediately, while the need for that scale usually stays hypothetical. The same logic applies directly to agent setups, hooks, and skills, where premature over-engineering is one of the more frequent traps.

*ByteByteGo, "7 System Design Concepts", 2025*

---

## LLM Evaluation

**A dashboard or a fast demonstration is not an outcome study.** Claims such as root-cause analysis in seconds, tenfold productivity, or an entire SDLC automated need a task denominator, baseline, repeated runs, failure distribution, human review time, and cost. Without those fields, the result remains a product demonstration even when the workflow executes successfully.

*Pavan Belagatti, [Become a 10x Developer](https://www.youtube.com/watch?v=6VBhFq5SJ0s) and [DORA Dashboard](https://www.youtube.com/watch?v=nqdSoLq_Qe0), 2026. The measurement requirements are this guide's evidence boundary.*

---

**Evaluation is a scored dataset, not a red/green test.** Unit tests that pass or fail deterministically do not apply to probabilistic outputs. Instead, build a dataset of inputs paired with expected outputs, run a scoring function, and track the score over time. The goal is moving from 85% to 87% to 89%, not achieving a binary pass state.

*Louis Pinsard (CTO, Dialogue), [IFTTD ep 338 "Evaluation de GenAI"](https://www.ifttd.io/episodes/evaluation-de-genai)*

---

**Replay key scenarios 10 to 100 times and measure the success rate.** Because LLM outputs are non-deterministic, a single test run proves nothing. Statistical CI/CD replays the same scenario many times in parallel and reports a success rate with a confidence interval. This is the foundation of a regression suite for agentic systems.

*Frédéric Barthelet (engineer), [IFTTD ep 329 "Front agentique"](https://www.ifttd.io/episodes/front-agentique)*

---

**Use LLM-as-judge asynchronously, not in the critical path.** Running a judgment step synchronously on every response penalizes all users for the failure rate of a minority of interactions. Serve the response first, judge it afterward, and use the verdict to improve future prompts and model selection.

*Samy Lastmann (CTO, Smart Tribune), [IFTTD ep 311 "IA Agentique"](https://www.ifttd.io/episodes/ia-agentique); Louis Pinsard (CTO, Dialogue), [IFTTD ep 338 "Evaluation de GenAI"](https://www.ifttd.io/episodes/evaluation-de-genai)*

---

**Hallucination is a trade-off to calibrate, not a bug to eliminate.** The training process for LLMs rewards confident answers over abstentions, which means models sometimes fabricate plausible-sounding content rather than saying they do not know. The practical question is: what balance of correct answers, abstentions, and hallucinations fits your use case? Tune confidence thresholds and system prompts to reach that balance; do not expect hallucination to reach zero.

*Louis Pinsard (CTO, Dialogue), [IFTTD ep 338 "Evaluation de GenAI"](https://www.ifttd.io/episodes/evaluation-de-genai)*

---

**Instrument with OpenTelemetry and Langfuse from day one.** Trace inputs, intermediate LLM calls with their responses and latencies, and final outputs. A trace structure that mirrors Sentry spans gives you the same observability for an LLM pipeline as for a conventional service. Adding instrumentation retroactively is expensive and disruptive.

*Louis Pinsard (CTO, Dialogue), [IFTTD ep 338 "Evaluation de GenAI"](https://www.ifttd.io/episodes/evaluation-de-genai)*

---

**When an AI disappoints, the cause is almost always context or prompting.** When an LLM system produces poor output, the most common root cause is insufficient or misaligned context, not model incapability. Abandoning an AI tool after one failure is a high-cost error. Diagnose the context first: what was missing, misrepresented, or ambiguous in the input?

*Louis Pinsard (CTO, Dialogue), [IFTTD ep 338 "Evaluation de GenAI"](https://www.ifttd.io/episodes/evaluation-de-genai)*

---

**Temperature 0 does not guarantee deterministic output.** Floating-point variance on GPU hardware and Mixture-of-Experts routing both introduce variation even at zero temperature. Determinism, when it matters, has to be engineered around the model rather than assumed from it: versioned APIs, a pinned model version in production, and versioned prompts.

*Alexandre Balmes, Dev With AI Meetup, 2026*

---

**The same prompt can produce a different response two days apart, even under controlled temperature.** Never assume a stable answer holds over time. This strengthens the case for continuous evaluation over a single evaluation pass: a system that passed its eval last month is not guaranteed to still pass it today.

*Brian Vermeer, Devoxx, 2026*

---

**Match the evaluation metric to the phase, and default to out-of-distribution testing.** A lightweight metric fits a dev-loop feedback cycle; a costly, qualitative one fits model selection; a reliable, monitored one fits production. Test against cases unlike the training distribution by default, not just similar ones, and watch for benchmarks potentially contaminated by the tested model's own training data. For human or LLM-as-judge evaluation, measure inter-rater agreement with Cohen's kappa rather than a raw percentage agreement, which overstates consistency when raters agree by chance.

*Yann Dubois, Stanford CS224N, 2024; CS336 Lecture 12, 2026*

---

**Combine several evaluation frameworks rather than relying on one, and force structured output over free text.** No single framework covers every metric that matters for a given system. Requiring a structured schema, a Pydantic model for instance, instead of parsing free-form text removes an entire class of parsing failures from the evaluation pipeline itself.

*Mete Atamel, Devoxx, 2025*

---

**An agent is evaluated on confidence, not coverage.** Component-by-component quality matters, but so does the complete system's behavior under guardrails. A useful reframing organizes that evaluation around three pillars, principle, policy, and personality, rather than trying to score every possible path through the agent.

*Jettro Coenradie & Daniël Spee, Devoxx, 2026*

---

**Skill self-improvement works like applied reinforcement learning.** Incremental modifications get tested against a binary criterion: keep what improves the outcome, discard what does not. Evaluating a skill itself works best on two layers, whether it activates at the right moment, and the quality of its output once activated, with human supervision reserved for edge cases.

*Emmanuel Sciara, Dev With AI Meetup, 2026; Negouai & Drode, Dev With AI Meetup, 2026*

---

**Verify that a model is actually needed before adding one.** Extra sophistication has to prove its marginal gain: an LLM remains hard to control even inside the best teams, and prompting or retrieval usually gets you further than fine-tuning before either is justified. This is one of the stronger convergences across the corpus, echoed independently by academic coursework.

*Stanford, ISLR (Hastie & Tibshirani); CS230 Lecture 8, 2025*

---

## Agent Security

**Agents find alternate paths around blocked actions.** Guardrails that prevent a specific operation do not prevent the agent from achieving the same effect through a different route. In a documented incident, a DELETE was blocked by filesystem permissions, so the agent emptied the file contents to satisfy the user's intent. Effective security requires blocking the intent, not just the operation.

*Zineb Bendhiba (Principal Software Engineer, Red Hat), [IFTTD ep 326 "MCP Servers"](https://www.ifttd.io/episodes/mcp-servers)*

---

**Unsupervised autonomous mode has produced home directory wipes and production database deletions.** These incidents are not model-specific; they appear across Claude, Gemini, and others when agents operate with high autonomy and broad filesystem or network access. The common factor is unsupervised operation combined with insufficient permission scoping.

*Guillaume Lours (Software Engineer, Docker), [IFTTD ep 360 "Sécuriser les agents IA sans ralentir les devs"](https://www.ifttd.io/episodes/docker-sandbox)*

---

**Micro-VM isolation with network-level secret injection is the safest pattern for fully autonomous agents.** Rather than running an agent on the host machine and relying on application-level guardrails, Docker Sandbox runs agents inside a micro-VM where outbound network traffic is intercepted. API credentials are injected at the network layer by a man-in-the-middle proxy: the agent never sees the credential directly, and the host machine cannot be accessed. Network rules default to deny-all with an explicit allowlist.

*Guillaume Lours (Software Engineer, Docker), [IFTTD ep 360 "Sécuriser les agents IA sans ralentir les devs"](https://www.ifttd.io/episodes/docker-sandbox)*

---

**Allowlist specific commands rather than granting blanket auto-approval.** Granting an agent permission to run all commands to reduce interruptions is tempting and dangerous. The safer practice is an explicit allowlist: `git commit` allowed, `git push` blocked until human review. N'takpe documented losing all Firefox bookmarks to an agent that misidentified them as context to clear during a cleanup task.

*Jocelyn N'takpe (Head of Engineering & Architecture, ManoMano), [IFTTD ep 346 "IA & DevX"](https://www.ifttd.io/episodes/ia-devx)*

---

**Maintain human oversight on production paths regardless of agent capability.** Agent capability and the scope of what an agent should be allowed to do autonomously are separate questions. Even a highly capable agent should go through the same review gates as a human engineer on changes that touch production systems.

*Jocelyn N'takpe (Head of Engineering & Architecture, ManoMano), [IFTTD ep 346 "IA & DevX"](https://www.ifttd.io/episodes/ia-devx)*

---

**One-shot autonomous sessions with underspecified goals produce unreadable output.** Giving an agent a vague spec and a 3-hour window with no checkpoints yields 50,000 lines of code across 25 containers that no human can meaningfully review. Autonomous sessions need tight specs, frequent checkpoints, and humans who interrupt rather than wait for completion.

*Guillaume Lours (Software Engineer, Docker), [IFTTD ep 360 "Sécuriser les agents IA sans ralentir les devs"](https://www.ifttd.io/episodes/docker-sandbox)*

---

**Test at least five prompt injection techniques before putting an agent into production.** System message manipulation, structured-output attacks, role-play framing to bypass refusals, and multi-turn manipulation all deserve a dedicated pass before launch. The same caution applies to installing a skill or agent definition sourced from the internet without review: it is a direct injection vector, not a convenience shortcut.

*Brian Vermeer, Devoxx, 2026*

---

**Do not let an agent decide its own permissions.** Wrap it in an MCP server with deterministic access control around it, rather than trusting the model's own judgment about what it should be allowed to do. Scope rights precisely through OAuth and fine-grained relationship-based authorization, in the style of OpenFGA.

*Christoph Bühler, Devoxx, 2026; Deepu Sasidharan, Devoxx, 2025*

---

**An MCP server exposed over HTTP needs the same security discipline as any API.** Authentication, authorization, and HTTPS are not optional because the client happens to be a model. A local MCP server left without authentication or with un-hardened defaults remains an exploitable attack surface even when the model itself has no flaw.

*Daniel Garnier-Moiroux, Devoxx, 2025; Makan Sepehrifar, Devoxx, 2026*

---

**Treat LLM sessions as a sensitive channel, the same way a code repository is treated.** The more developers write code through an AI assistant, the higher the risk of API keys leaking into prompts and into the logs that capture them. Session logs deserve the same access controls as source control, not an afterthought.

*Brian Vermeer, Devoxx, 2026*

---

**Isolate production agents in an ephemeral, read-only container.** Read-only access to the repository, a network allowlist, CPU and RAM quotas, and a maximum session duration together bound what a runaway session can do. This converges with the Docker Sandbox and micro-VM pattern already covered in the IFTTD corpus above.

*Dev With AI Meetup, 2026 (Bolin, Vyncke, Allainmat)*

---

## DevX & Adoption

**Treat the agent as a new developer who needs onboarding.** An agent given a well-maintained AGENTS.md file and up-to-date rules about how your codebase works (database connection patterns, message bus encoding, naming conventions) produces dramatically better output than one dropped into an undocumented codebase. At ManoMano, a dedicated platform team maintains skills and rules so agents understand the internal architecture. The agent-facing documentation is now better maintained than the team's Confluence wiki.

*Jocelyn N'takpe (Head of Engineering & Architecture, ManoMano), [IFTTD ep 346 "IA & DevX"](https://www.ifttd.io/episodes/ia-devx)*

---

**Prefer skills over MCP servers when the capability can be expressed as one.** Skills (slash commands, agent instructions) run on the model without network overhead or token cost from schema injection. MCP servers add latency and consume tool-description tokens. Use skills for anything that can be expressed as instructions or prompts; reach for MCP only when you genuinely need an external tool call.

*Jocelyn N'takpe (Head of Engineering & Architecture, ManoMano), [IFTTD ep 346 "IA & DevX"](https://www.ifttd.io/episodes/ia-devx)*

---

**Alternate AI-assisted and manual coding sessions to preserve deep system understanding.** Delegating all coding to an AI agent efficiently over time erodes the engineer's granular understanding of the system. The judgment required to evaluate agent output depends on that understanding. Deliberately returning to manual coding on parts of the codebase maintains the substrate needed for effective oversight.

*Sébastien Deleuze (Spring Framework committer, VMware), [IFTTD ep 349 "Tech et Soft Skills"](https://www.ifttd.io/episodes/tech-et-soft-skills)*

---

**Cap daily AI development cycles against cognitive load, not against what the tooling allows.** When fast tooling makes three or more full feature cycles per day technically possible, engineers who sustain that pace for weeks report significant cognitive fatigue. Deliberate throughput limits protect the quality of judgment applied to each cycle.

*Julien Lepine (engineer), [IFTTD ep 351 "AWS Summit"](https://www.ifttd.io/episodes/aws-summit)*

---

**Strictly typed languages and strict architectural patterns improve agent output quality.** Research from ETH Zurich and UC Berkeley (Mündler et al., PLDI 2025, [arXiv 2504.09246](https://arxiv.org/abs/2504.09246)) found that 94% of compilation errors in LLM-generated code are type errors, meaning the compiler catches the vast majority of compile-time mistakes before they reach a human reviewer. Jocelyn N'takpe draws the practical conclusion: strict type systems and patterns like hexagonal architecture act as a safety net for agent output. The compiler rejects common agent mistakes automatically, and well-known structural patterns give the model a strong scaffold to work within.

*Jocelyn N'takpe (Head of Engineering & Architecture, ManoMano), [IFTTD ep 346 "IA & DevX"](https://www.ifttd.io/episodes/ia-devx). Research: Mündler et al., "Type-Constrained Code Generation with Language Models", PLDI 2025, [arXiv 2504.09246](https://arxiv.org/abs/2504.09246).*

---

**An agent excels at refactors that exceed human working memory.** At Docker, a codebase refactor that engineers had attempted and abandoned multiple times due to complexity was completed by an agent in two days. The engineers could articulate exactly what they wanted, but could not hold enough of the system in working memory simultaneously to execute it. The agent does not have that constraint.

*Guillaume Lours (Software Engineer, Docker), [IFTTD ep 360 "Sécuriser les agents IA sans ralentir les devs"](https://www.ifttd.io/episodes/docker-sandbox)*

---

**The best results come from a supervisory posture: steer, do not launch-and-forget.** Practitioners who report the best outcomes describe watching what the agent does and interrupting when it heads in the wrong direction, rather than launching a session and reviewing the result hours later. The interruption cost is far lower than the rework cost.

*Guillaume Lours (Software Engineer, Docker), [IFTTD ep 360 "Sécuriser les agents IA sans ralentir les devs"](https://www.ifttd.io/episodes/docker-sandbox)*

---

**AI amplifies a team's existing practices, good and bad alike.** A team with weak practices before adopting an AI assistant tends to see its anti-patterns get worse, not corrected, contradicting the narrative that AI democratizes good engineering habits by default.

*Geoffrey Graveaud, Dev With AI Meetup, 2026*

---

**Full delegation of user stories to unsupervised, always-on agents cost one team velocity instead of gaining it.** The regression was only caught because the team deliberately set out to measure it, not because it was visible day to day. It stands out as a rare, honestly reported failure case rather than a success story.

*Samuel Gallet & Geslain Dahan, Dev With AI Meetup, 2026*

---

**Instrument coding assistants themselves, including Claude Code and Codex, with OpenTelemetry.** Tracing every decision an assistant makes applies the same discipline already used for services: a system that cannot be observed is a system that cannot be trusted, and that principle does not stop at the boundary of the tool writing the code.

*Annie Freeman, Devoxx, 2026*

---

**Deliberately simulate scenarios where the AI is unavailable or degraded.** Running this as a drill checks whether the system, and the team, still function without it, the same way a chaos engineering exercise checks resilience to infrastructure failure.

*Konstantin Pavlov, Devoxx, 2025*

---

**The critical skill for the next generation of engineers is verifying AI-generated code, not writing code from scratch.** This legitimizes a posture of systematic review on everything an agent produces, treating review capacity as the actual bottleneck rather than generation speed.

*Mehran Sahami, Stanford, "It's Never Too Late", 2025*

---

## Sources

### IFTTD Podcast

[IFTTD](https://www.ifttd.io/) is a French tech podcast hosted by Bruno Soulez. The episodes cited on this page were recorded between 2024 and 2025. Transcripts were analyzed and paraphrased; no direct quotes appear on this page.

| Episode | Guest | Role / Company | Theme |
|---------|-------|---------------|-------|
| [ep 311](https://www.ifttd.io/episodes/ia-agentique) | Samy Lastmann | CTO, Smart Tribune | Agentic AI |
| [ep 326](https://www.ifttd.io/episodes/mcp-servers) | Zineb Bendhiba | Principal SWE, Red Hat | MCP Servers |
| [ep 329](https://www.ifttd.io/episodes/front-agentique) | Frédéric Barthelet | Engineer | Agentic front-end |
| [ep 338](https://www.ifttd.io/episodes/evaluation-de-genai) | Louis Pinsard | CTO, Dialogue | GenAI Evaluation |
| [ep 341](https://www.ifttd.io/episodes/bilan-2025) | Quentin Adam | CEO, Clever Cloud | 2025 retrospective |
| [ep 346](https://www.ifttd.io/episodes/ia-devx) | Jocelyn N'takpe | Head of Eng & Arch, ManoMano | AI & DevX |
| [ep 349](https://www.ifttd.io/episodes/tech-et-soft-skills) | Sébastien Deleuze | Spring committer, VMware | Tech & Soft Skills |
| [ep 351](https://www.ifttd.io/episodes/aws-summit) | Julien Lepine | Engineer | Production agents |
| [ep 357](https://www.ifttd.io/episodes/azure-et-ia) | Antonio Goncalves | Java Champion, dev advocate | Model routing |
| [ep 360](https://www.ifttd.io/episodes/docker-sandbox) | Guillaume Lours | Software Engineer, Docker | Agent sandboxing |
| [ep 361](https://www.ifttd.io/episodes/rag) | Guillaume Laforge | Developer Advocate, Google Cloud | RAG & context |

### Devoxx

Devoxx is a family of developer conferences covering Java, DevOps, architecture, and AI. Talks cited on this page were paraphrased from the 2025 and 2026 editions; no direct quotes appear on this page.

| Speaker | Role / Company | Theme |
|---------|----------------|-------|
| Victor Rentea | Speaker, Devoxx | Context volume & hallucination |
| Alex Gavrilescu | Speaker, Devoxx | Agent memory & conventions |
| Konstantin Pavlov | Speaker, Devoxx | Agent memory & resilience drills |
| Max Sumrall | Speaker, Devoxx | Spec paradox |
| Tom Cools | Speaker, Devoxx | Combinatorial optimization |
| Brian Vermeer | Speaker, Devoxx | Prompt injection & evaluation drift |
| Mete Atamel | Speaker, Devoxx | Evaluation frameworks |
| Jettro Coenradie & Daniël Spee | Speakers, Devoxx | Agent evaluation |
| Christoph Bühler | Speaker, Devoxx | Agent permissions |
| Deepu Sasidharan | Speaker, Devoxx | Agent permissions |
| Daniel Garnier-Moiroux | Speaker, Devoxx | MCP server security |
| Makan Sepehrifar | Speaker, Devoxx | MCP server security |
| Annie Freeman | Speaker, Devoxx | Assistant observability |

### Dev With AI Meetup

Dev With AI is a French meetup dedicated to AI-native development practices. Talks cited on this page were paraphrased from the 2026 edition; no direct quotes appear on this page.

| Speaker | Role / Company | Theme |
|---------|----------------|-------|
| Emmanuel Sciara | Speaker, Dev With AI Meetup | Context thresholds & RPI workflow |
| Malo & Dorian | Speakers, Dev With AI Meetup | Context degradation |
| Florian Allainmat | Speaker, Dev With AI Meetup | CLAUDE.md size & tool isolation |
| Samuel Gallet & Geslain Dahan | Speakers, Dev With AI Meetup | Agent delegation velocity |
| Vyncke | Speaker, Dev With AI Meetup | Agent exit criteria & sandboxing |
| Luis Iglesias Hernandez | Speaker, Dev With AI Meetup | Plan/implementation analysis |
| Alexandre Balmes | Speaker, Dev With AI Meetup | Determinism & tool isolation |
| Negouai & Drode | Speakers, Dev With AI Meetup | Skill self-improvement |
| Geoffrey Graveaud | Speaker, Dev With AI Meetup | AI amplifying team practices |
| Bolin | Speaker, Dev With AI Meetup | Agent sandboxing |

### ByteByteGo

ByteByteGo is a system design channel covering architecture and scaling patterns. One talk is cited on this page, paraphrased; no direct quotes appear.

| Speaker | Role / Company | Theme |
|---------|----------------|-------|
| ByteByteGo | System design channel | Scaling only on proven need |

### Stanford Online

Stanford Online publishes academic coursework on machine learning and large language models. Lectures cited on this page were paraphrased; no direct quotes appear on this page.

| Speaker | Role / Company | Theme |
|---------|----------------|-------|
| Denny Zhou | Google DeepMind, Stanford CS25 V5 | Reasoning as intermediate tokens |
| Yann Dubois | Stanford CS224N | Evaluation metrics & OOD testing |
| Mehran Sahami | Stanford, "It's Never Too Late" | Verifying AI-generated code |
| CS25 (2026 cohort) | Stanford Online | In-context learning vs. fine-tuning |
| CS230 Lecture 8 | Stanford Online | In-context learning vs. fine-tuning |
| CS336 Lecture 12 | Stanford Online | Evaluation metrics |
| ISLR (Hastie & Tibshirani) | Stanford textbook / course | Verifying LLM necessity |

### Pavan Belagatti YouTube Corpus

The 62 English-language videos published in 2026 were analyzed from local WebVTT transcripts. They provide practical demonstrations of agentic workflows, context engineering, loop engineering, and software factories. Port appears repeatedly as the implementation platform, so these videos are treated as vendor-oriented practitioner material rather than independent architectural validation. Timestamped quotations used elsewhere in the guide were checked against the corresponding transcript.

| Video | Theme | Evidence boundary |
|---|---|---|
| [Build Your Own Software Factory](https://www.youtube.com/watch?v=pE1S1egMrAI) | SDLC workflow, human gates, rollback, feedback | Configured Port workflow; no comparative reliability or cost study |
| [What Is a Software Factory?](https://www.youtube.com/watch?v=0nM1ygBm8tA) | Agent execution and human gates | Short conceptual framing |
| [Loop Engineering Explained](https://www.youtube.com/watch?v=RvG7R0Ue1k4) | Repeated execution without manual reprompting | Emerging practitioner term, not a standard |
| [Context Engineering Explained](https://www.youtube.com/watch?v=oExfgB9zRzA) | Shared context layer | Benefits asserted without measured failure distribution |
| [Deep Agents Hands-On](https://www.youtube.com/watch?v=K7G_FFZ9jHY) | Planning, delegation, persistent filesystem | Product tutorial, not a harness benchmark |
| [Traditional RAG vs GraphRAG](https://www.youtube.com/watch?v=Gbztrb_Yabs) | GraphRAG comparison | One example scored by an LLM judge; no general superiority claim |

---

*See also: [credits.md](../core/credits.md) for full attribution details.*
