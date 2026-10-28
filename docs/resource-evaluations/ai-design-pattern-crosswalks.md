# AI design pattern crosswalks (classic patterns to agent patterns)

**Reviewed**: 2026-10-27. **Overall score**: 3/5. Selective use: cite the best crosswalks as sources for a page that pairs classic software patterns with Claude Code harness features, and label every Claude Code pairing that no source states as the guide's own reading.

## Method and evidence limits

- Each source was opened at its origin (page fetched, repository cloned, or arXiv page read), unless the table says otherwise.
- Two arXiv entries were verified only through a search snippet. Their score is provisional.
- No opened source maps GoF or EIP patterns to Claude Code hooks, subagents, skills or MCP. Rows such as "Observer to hooks" are therefore a synthesis, backed only where two or more independent crosswalks agree.
- Leak-derived repositories on this topic were excluded and are not cited.
- Star counts were not re-checked and are not used for scoring.

## Per-source scores

| Source | Score | What it gives | Limit | Reuse |
|---|---|---|---|---|
| [Pattern Evolution (Jia Huang, kage-ai)](https://kage-ai.com/research/pattern-evolution/) | 3/5 | 25 distributed-system patterns, all written, each with an agent counterpart (Saga, Retry, Timeout, Circuit Breaker, Bulkhead, Idempotency, Outbox, Sidecar) | Only 4 of 23 GoF cards are written (Singleton, Factory Method, Observer, Strategy); 19 are pending. Cards come from the site data; the page text does not mention Claude Code | Cite only; copyright notice, no reuse terms |
| [Classical SE Patterns as Agent Design Analogues (agentpatterns.ai)](https://agentpatterns.ai/patterns/agent-design/classical-se-patterns-agent-analogues/) | 3/5 | 10 GoF-style mappings; reviewed 2026-06-12 | No author; labeled "emerging" by the site; Facade to CLAUDE.md is single-source | Cite only; no license stated |
| [Patrones GoF en agentes IA (aicodingpatterns.com)](https://aicodingpatterns.com/patterns/patrones-gof-patrones-agenticos-mapeo-completo/) | 4/5 | 23 mappings (14 GoF, 3 PoEAA, 3 EIP, 3 resilience), published 2026-05-11; widest overlap with the other crosswalks | Spanish text; no license stated | Cite only |
| [roanbrasil/agents-integration-patterns](https://github.com/roanbrasil/agents-integration-patterns) | 4/5 | A real EIP-to-agent table (Message Router, Scatter-Gather, Pipes and Filters, Process Manager, Dead Letter Channel and others), a FAILURE-MAP that maps the 14 MAST failure modes to patterns, and a FORCES file with 14 named forces | The README lists Circuit Breaker in its EIP table although it is not an EIP-book pattern. The MAST-to-pattern mapping is the repository author's judgment, not the MAST paper's. 34 pattern files claimed; not re-counted | CC BY 4.0, adaptable with attribution |
| [jlldavies/go4-llm-design-patterns](https://github.com/jlldavies/go4-llm-design-patterns) | 2/5 | 94 patterns in full GoF format, useful as vocabulary (Bounded Execution, Tool Budget, Checkpointing, Agent Isolation) | Not a crosswalk: one classic alias only (Bounded Execution, also known as Circuit Breaker) | MIT |
| [huangjia2019/agent-design-patterns](https://github.com/huangjia2019/agent-design-patterns) | 2/5 | 27 core patterns in a 7 by 6 matrix (the repository description says 28; the README counts 27), runnable Python, a list of agent features per pattern | Not a GoF crosswalk: classic names appear only as lineage notes. Its source-level citations for Claude Code are not reused here | MIT |
| [arXiv 2601.19752](https://arxiv.org/abs/2601.19752), Dao et al., Agentic Design Patterns: A System-Theoretic Framework | 3/5 (provisional) | 12 patterns with explicit GoF links, such as the controller as Observer and tool use as Proxy or Adapter | Checked through a search snippet only; the paper body was not read | Cite |
| [arXiv 2605.13850](https://arxiv.org/abs/2605.13850), Huang and Zhou, A Two-Dimensional Framework for AI Agent Design Patterns | 3/5 | 7 cognitive functions by 6 execution topologies, 28 named patterns; a second axis for organizing the page | Not a classic crosswalk; the 28 count differs from the 27 in the companion repository | Cite |
| [arXiv 2605.20173](https://arxiv.org/abs/2605.20173), Srinivasan, selecting and composing runtime architecture patterns | 3/5 | 6 runtime patterns including scatter-gather plus saga, supervisor plus gate and human in the loop; backs the Saga row | Methodology paper; no Claude Code anchoring | Cite |
| [arXiv 2609.00006](https://arxiv.org/abs/2609.00006), Barbaste et al., Harness Engineering | 3/5 (provisional) | Source-code study of 11 coding agent systems including Claude Code; 29 design patterns and 13 observations per the abstract | Only the abstract was verified. The pattern list was not read, and a search snippet that places hooks under a policy-as-code pattern is unconfirmed. Read the paper before citing any pattern | Cite after reading |

## Where the crosswalks agree

At least two independent sources back each row. These are the candidate rows for the guide:

| Classic pattern | Agent analogue | Sources |
|---|---|---|
| Observer | Hooks around tool calls | agentpatterns.ai, aicodingpatterns.com |
| Chain of Responsibility | Hook and permission pipelines | agentpatterns.ai, AHEP |
| Memento | Checkpoints and rewind | agentpatterns.ai, AHEP |
| Composite, Mediator | Orchestrator and subagents | agentpatterns.ai, aicodingpatterns.com |
| Factory | Subagent spawning | agentpatterns.ai, aicodingpatterns.com |
| Strategy | Routing and model selection | agentpatterns.ai, aicodingpatterns.com |
| Circuit Breaker | Turn and loop limits | agentpatterns.ai, aicodingpatterns.com |
| Saga | Compensating actions | agentpatterns.ai, aicodingpatterns.com, arXiv 2605.20173 |
| Adapter | Tool and MCP adapters | aicodingpatterns.com, arXiv 2601.19752 |

Facade to CLAUDE.md rests on one source and stays a proposal. Observer to hooks and the other Claude Code anchors are the guide's reading of those mappings, because none of the opened sources states them for Claude Code.

## Where they disagree

The disagreements are worth showing as such:

- Decorator: guardrails in one source, context-injection middleware in another.
- Template Method: the system prompt in one source, a fixed agent-loop skeleton in another.
- Chain of Responsibility: a hook pipeline in one source, chained agents in another.
- Singleton: a tool registry in one source, a pattern of its own in AHEP.

## Decision

Use the crosswalks as citable sources and do not copy any card. Build the guide's table from the consensus rows above, mark single-source and own-reading rows as such, and add the Claude Code anchoring from official documentation. Use the roanbrasil EIP table and the kage-ai distributed-pattern cards as the strongest sources for the EIP and resilience rows. Treat the go4 and huangjia2019 repositories as vocabulary and as feature lists, not as crosswalks.

Read the Barbaste et al. paper before citing any of its patterns, and the body of arXiv 2601.19752 before relying on its GoF links. The overall score of 3/5 reflects a topic that is useful but young: most sources are dated 2026 and none has been tested against Claude Code behavior. This evaluation does not establish that any pairing is correct, only that sources propose it.
