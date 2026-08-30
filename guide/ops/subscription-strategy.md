---
title: "Subscription Strategy at Team Scale"
description: "A decision framework for choosing between per-seat subscriptions, Enterprise API billing, a capped API gateway, and self-hosted inference once an engineering org grows past a handful of developers"
tags: [ops, cost, enterprise, guide]
---

# Subscription Strategy at Team Scale

> **Audience**: Engineering leaders and platform teams sizing an AI coding tool budget for an organization, not an individual subscription choice.
>
> **Scope**: Which billing model fits which org size and workload shape. Anthropic paused the announced June 2026 interactive/programmatic billing split on June 15, so the historical announcement is not a current budgeting rule; see [Anthropic's current Agent SDK plan guidance](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan). For gateway implementation, see [api-gateway.md](./api-gateway.md). For the economics of self-hosting instead of any subscription, see [Local vs Cloud Inference](../ecosystem/local-vs-cloud-inference.md#sizing-self-hosted-inference-for-a-team). For per-task cost modeling, see [ai-unit-economics.md](./ai-unit-economics.md).

---

## TL;DR

| Org shape | Start here |
|---|---|
| 2 to 150 intended Claude users, mostly terminal/IDE usage | Claude Team, standard and premium seats mixed |
| More than 150 intended Claude users | Enterprise, or a multi-workspace design confirmed with Anthropic sales |
| Shared production automation through `claude -p`, Agent SDK, or CI | Claude Platform API keys behind a capped gateway; subscription-authenticated programmatic usage still draws from plan limits while Anthropic's announced split remains paused |
| Anthropic API spend already unpredictable across many keys | API gateway (LiteLLM or Portkey) for the API traffic routed through it |
| Considering self-hosted open-weight models | Model it as a separate business case, not a line in this decision. See the sizing math linked above before quoting a number |

---

## 1. Authentication and billing source matter more than interaction mode

The planned split between interactive subscription usage and a separate programmatic credit did not take effect. Anthropic's June 15 update says that subscription-authenticated Agent SDK, `claude -p`, and third-party app usage still draw from the same subscription limits as interactive Claude usage. The previously announced monthly programmatic credit is unavailable until Anthropic publishes a replacement plan. Source: [Anthropic, Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan), verified 2026-08-30.

Current budgeting therefore starts with the credential and plan, not whether a request is interactive:

- **Team subscription authentication** includes usage subject to rolling five-hour and weekly limits. All activity across Claude and Claude Code draws from the same pool. Paid plans can enable usage credits to continue at standard API rates after included limits are reached. Source: [Claude pricing FAQ](https://claude.com/pricing), verified 2026-08-30.
- **Claude Platform API keys** use prepaid credits or an invoicing arrangement and are billed at API rates. This is the billing source to place behind a gateway for shared production automation. Source: [Anthropic API billing guidance](https://support.claude.com/en/articles/8977456-how-do-i-pay-for-my-claude-api-usage), verified 2026-08-30.
- **Usage-based Enterprise** charges a fixed seat fee for access and bills usage separately by token consumption. The current Enterprise seat does not include usage. Source: [Anthropic Enterprise billing guidance](https://support.claude.com/en/articles/11526368-how-am-i-billed-for-my-enterprise-plan), verified 2026-08-30.

Do not compare a Team seat, an Enterprise seat, and a Platform API key as if each buys the same unit. Team buys included capacity with plan limits; Enterprise buys governed access plus metered usage; a Platform key buys metered API traffic without a Claude seat.

---

## 2. Claude Team: the per-seat default, and its hard ceiling

Claude Team costs $20/seat/month (standard, billed annually; $25 billed monthly) or $100/seat/month (premium, billed annually; $125 billed monthly), mixable within one organization. It includes Claude Code, Claude Cowork, Claude Design, Claude Science, central billing, SSO, and admin controls. Source: [claude.com/pricing](https://claude.com/pricing), verified 2026-08-30.

**The ceiling applies to intended Claude users, not total company headcount: one Team workspace supports 2 to 150 seats.** A 350-person company can stay within Team's published scope if no more than 150 people need seats. If more than 150 people need access, Anthropic's pricing page positions Enterprise for large businesses but does not document multiple Team workspaces as one administratively unified organization. Treat a multi-workspace split as an arrangement to confirm with Anthropic sales, not as a documented extension of one Team workspace. Source: [claude.com/pricing](https://claude.com/pricing), verified 2026-08-30.

Subscription-authenticated automation currently consumes the same plan limits as interactive work. Anthropic's preserved guidance says shared production automation should use Claude Platform with an API key for predictable pay-as-you-go billing. Put that API traffic behind a tested gateway cap rather than letting unattended jobs exhaust developers' shared plan capacity. Source: [Anthropic Agent SDK plan guidance](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan), verified 2026-08-30.

---

## 3. Claude Enterprise: usage-priced, seat fee included

Enterprise starts at $20/seat plus usage billed at API rates, available either self-serve or sales-assisted for custom terms. It adds role-based access with granular permissions, SCIM, audit logs, compliance APIs, custom data retention, network-level controls, IP allowlisting, and a HIPAA-ready option. Source: [claude.com/pricing](https://claude.com/pricing), verified 2026-08-30.

Anthropic's Claude Code cost guide reports an average of about $13 per developer per active day and $150 to $250 per developer per month across API-priced enterprise deployments, with costs below $30 per active day for 90% of users. Anthropic also says that model choice, codebase size, multiple concurrent instances, and automation make per-developer cost vary widely, and recommends a pilot before rollout. Use those figures as a vendor benchmark, not as a forecast for a specific organization. Source: [Anthropic, Manage costs effectively](https://code.claude.com/docs/en/costs), verified 2026-08-30.

Observed usage telemetry adds a distribution that a per-developer average hides. TraceLab released a 2026 trace of 4,265 Claude Code and Codex sessions from 43 developers, collected from September 2025 through June 2026 across 23 models. At the providers' published API list prices, the paper estimates a median session cost of $0.61, an average of $9.70, and a P99 of $178. Prefix-cache reads account for 59.5% of that estimated cost, while output tokens account for 11.2%. These are reconstructed price equivalents from one research group's usage, not invoices or production serving costs, and the trace does not measure whether a task was accepted. Use the result to instrument complete workflows and cache behavior, not to extrapolate a 43-developer sample directly to an organization of 300 engineers. Source: [Zhu et al., TraceLab](https://arxiv.org/pdf/2606.30560), PDF pp. 4 and 6, Tables 1, 5, and 6.

Production telemetry also rules out converting seats directly into concurrent inference calls. A one-week GitHub Copilot Agent trace covered 13.5 million sessions from 3.2 million users and found that 87% of LLM calls were agent-initiated. LLM execution remained mostly serial within a turn, with median concurrency of 1.15 and P90 of 1.4 among turns with overlap, while failure-heavy turns used 36 median LLM calls versus 9 for read-heavy deep loops. This is client-side telemetry with anonymized models and no server cost, coding-task quality, GPU, or acceptance signal, so it informs pilot instrumentation rather than a budget forecast. Source: [Liu et al., Agentic Coding in the Wild](https://arxiv.org/pdf/2608.00101), PDF pp. 1, 3, 5-6, Tables 1, 3, and 5 and Figure 7.

A Back Market practitioner account supplies a larger organizational denominator, but not audited billing data. Within a stated scope of 280 people, Nicolas Martignole reported 210 to 220 active users and defined an active user as someone who spent at least $1 in the month. He reported a three-month average of $191 per active developer and said one January user spent about $3,000. The talk provides neither a median nor a full distribution, and two oral summaries conflict on January's total. Preserve the denominator, inactive population, median, upper percentiles, and outcome measure before using any fleet average. Source: [Nicolas Martignole, "Claude Code en entreprise", 49:05](https://www.youtube.com/watch?v=kSrEZ57thMg&t=2945s), [50:04](https://www.youtube.com/watch?v=kSrEZ57thMg&t=3004s), and [50:48](https://www.youtube.com/watch?v=kSrEZ57thMg&t=3048s), published 2026-04-03.

The same account describes a staged billing policy rather than one plan for every developer. Back Market began with metered API access to avoid paying for inactive subscriptions and to collect usage telemetry, then recommended moving sustained daily users to a fixed-price plan after observing their spend. The speaker's claimed API-to-Max price equivalence was introduced as an estimate and showed no calculation. Use measured crossover points from the organization's own billing data, and apply the contract and governance checks in Section 6 before treating a personal Max plan as an enterprise option. Source: [initial API decision at 06:37](https://www.youtube.com/watch?v=kSrEZ57thMg&t=397s) and [heavy-user recommendation at 44:00](https://www.youtube.com/watch?v=kSrEZ57thMg&t=2640s).

A 2026 preprint analyzing eight frontier models on SWE-bench Verified found that agentic coding runs consumed 1,000 times more tokens than code reasoning and code chat in its experimental comparison. Repeated runs on the same task varied by up to 30 times in total tokens, and higher token use did not imply higher accuracy. The study also found only weak-to-moderate correlation between agents' predicted and actual token use, peaking at 0.39. This is benchmark evidence, not production telemetry, and the authors identify their eight-model sample as a limitation. It still explains why one average per developer or a model's own estimate cannot set a safe cap. Source: [Bai et al., How Do AI Agents Spend Your Money?](https://arxiv.org/pdf/2604.22750), PDF pp. 1-6 and 10-12.

Task specification is a second measurable cost variable. A preprint released on August 26, 2026 ran 2,700 Kimi K3 coding-agent trials across five SWE-bench Verified tasks, 12 specification variants, three thinking-effort levels, and 15 repeats. Reducing a full specification to a bare user story increased token spend by 29.7% in its pooled estimate, with a 90% credible interval from 5.1% to 58.7%. A single $0.11 probe reduced the median error of its cross-configuration cost predictor from 161% to 36%. The authors explicitly limit generalization because the experiment covers one model and five tasks. Treat this as a pilot design, not a universal saving: sample specification variants and effort levels, then price the observed distribution. Source: [Smékal, Can your AI agent be cheaper?](https://arxiv.org/pdf/2608.25399), PDF pp. 3-5, 7-10, and Appendix C p. 16.

Four controls keep usage-priced billing bounded:

- **Native Enterprise caps**, configured per organization or user before rollout. Anthropic lists user and organizational spend controls as an Enterprise feature. Source: [claude.com/pricing](https://claude.com/pricing), verified 2026-08-30.
- **A budget cap per team or key for Platform API traffic**, enforced by a gateway. LiteLLM's `max_budget` defaults to `null`, so a deployed proxy is not a cap until the operator configures the budget and verifies the rejection path. Source: [LiteLLM budget documentation](https://docs.litellm.ai/docs/proxy/users). See [api-gateway.md](./api-gateway.md).
- **Model routing**, sending routine API calls to a cheaper model and reserving the expensive one for tasks that need it. RouteLLM evaluates this pattern on MT-Bench; its measured result is workload-specific, not a guaranteed saving for coding agents. Source: [Ong et al., RouteLLM](https://arxiv.org/abs/2406.18665). See [ai-unit-economics.md](./ai-unit-economics.md) for the repository's task-level cost model.
- **Workflow and iteration budgets**, limiting candidate count, review loops, and retries against a task-success objective. The OSDI 2026 Murakkab evaluation found an order-of-magnitude spread in completion tokens and roughly a twofold pass@1 range across configurations of its LiveCodeBench coding workflow. Its review phase helped some model-task combinations and harmed others. The paper's separate multi-workflow experiment reported a cost reduction factor of up to 4.3 relative to its LangGraph baseline while maintaining its defined SLOs, but it approximated agent arrivals from a 24-hour Azure LLM trace rather than observing production coding-agent traffic. The result supports profiling workflow configurations, not applying 4.3 as a budget forecast. Source: [Chaudhry et al., Murakkab](https://www.usenix.org/system/files/osdi26-chaudhry.pdf), OSDI 2026 proceedings pp. 567-568 and 575-577, Sections 4.1, 4.3, and 4.4.

Agentless provides a separate reason to cap candidate generation. Its FSE 2025 evaluation used a fixed localization, repair, and validation workflow with GPT-4o on 300 SWE-bench Lite issues. It resolved 96 issues, or 32%, at an average reported inference cost of $0.70 per issue, and its repair result plateaued around 40 candidate patches. This is one benchmark with 2024 API pricing, not a production cost study; the reported cost excludes test infrastructure and human review. Use it to test a candidate ceiling and selection policy before funding more retries. Source: [Xia et al., Demystifying LLM-Based Software Engineering Agents](https://lingming.cs.illinois.edu/publications/fse2025.pdf), DOI [10.1145/3715754](https://doi.org/10.1145/3715754), PDF pp. 10-15, Table 1 and Figure 6.

---

## 4. API gateway: a control plane for routed API traffic

A gateway (LiteLLM or Portkey) sits between clients and provider APIs. For traffic routed through it, LiteLLM can issue virtual keys, restrict models, track spend, and reject requests after a configured budget is exceeded. Its documentation shows a 429 response for an exceeded user budget, while key budgets default to disabled until `max_budget` is set. Source: [LiteLLM budget documentation](https://docs.litellm.ai/docs/proxy/users), verified 2026-08-30. Full setup in [api-gateway.md](./api-gateway.md).

The boundary is traffic routing. A gateway cannot meter subscription-authenticated requests that go directly to Anthropic and still draw from Team plan limits. Enterprise already provides native user and organizational spend controls. Add a gateway when the organization needs one policy layer for Platform API keys, multiple providers, or automation; do not deploy it solely because Enterprise is assumed to lack spend controls. Sources: [Anthropic's current subscription guidance](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan), [Claude pricing](https://claude.com/pricing), and [LiteLLM budget documentation](https://docs.litellm.ai/docs/proxy/users), verified 2026-08-30.

Practitioner reports show what attribution adds beyond a global cap. Shopify's internal LLM proxy routes users through enterprise APIs and attributes API cost by team and person. Ramp described an internal provider layer that traces cost by team and product while comparing model performance against spend. Back Market separately exported Claude Code API usage to BigQuery and used client metadata to detect Anthropic calls from tools whose licenses were already being paid. These accounts provide no exported dashboards or quantified savings, and token volume remains an adoption signal until it is joined to accepted outcomes. For routed API traffic, record team, person or service, product, environment, workflow, model version, and outcome identifiers so the organization can detect duplicate spend and calculate cost per accepted result. Sources: [Farhan Thawar, Shopify, 22:22](https://www.youtube.com/watch?v=u-3IILWQPRM&t=1342s), [Ramp, 24:53](https://www.youtube.com/watch?v=NMs8C2_3M0w&t=1493s), and [Nicolas Martignole, Back Market, 45:09](https://www.youtube.com/watch?v=kSrEZ57thMg&t=2709s).

---

## 5. Multi-vendor by design, not by accident

An organization can run Claude and a second provider side by side, either through separate first-party tools or a multi-provider harness such as opencode. A gateway can centralize API keys and budgets across routed traffic, but it does not make provider contracts, retention policies, or model behavior interchangeable. Treat provider choice, harness choice, and billing control as three separate decisions. Sources: [LiteLLM budget documentation](https://docs.litellm.ai/docs/proxy/users) and [opencode provider documentation](https://opencode.ai/docs/providers/), verified 2026-08-30.

An aggregator contract does not approve every downstream provider. In a Back Market account, the organization evaluated and allowed only a small subset of OpenRouter's available providers. The transcript does not preserve the approved count reliably, and the speaker explicitly did not offer legal advice. Treat provider allowlisting, data location, retention, security review, and incident ownership as controls outside the routing API. Source: [Nicolas Martignole, "Claude Max ou API", 38:17](https://www.youtube.com/watch?v=DRtd8S_3E-w&t=2297s), published 2026-07-22.

If evaluating a third harness for this purpose, check its subscription model against Section 1, not just its headline price. [opencode](../ecosystem/agentic-tools.md#15-opencode-anomaly-formerly-sst)'s Go plan is a concrete case that fails the team-scale provisioning test: $10/month with usage caps of $12 per 5 hours, $30 per week, and $60 per month, and only one member per workspace can subscribe. Its current catalog also includes Grok 4.6 and GPT 5.6 Luna alongside DeepSeek, Qwen, GLM, and Kimi models, so Go is no longer accurately summarized as an open-weight-only plan. Source: [opencode.ai/docs/go](https://opencode.ai/docs/go/), verified 2026-08-30.

---

## 6. Personal Pro/Max plans: not an organization control plane

A personal Claude Pro or Max subscription is priced below organization plans, which can make individual reimbursement look like a shortcut. It does not give the employer the same contractual or administrative position as an organization plan:

- **No organization control plane.** Anthropic lists central billing, SSO, and connector administration on Team and Enterprise, not on individual plans. A reimbursed personal account does not become an employer-managed seat. Source: [claude.com/pricing](https://claude.com/pricing), verified 2026-08-30.
- **Terms depend on region and capacity.** The current Consumer Terms served for EEA and Swiss residents define a consumer as acting mainly outside their trade or profession and prohibit using the services for commercial or business purposes. Other regions may have different applicable terms. Resolve the applicable contract with legal rather than generalizing from one regional page. Source: [Anthropic Consumer Terms of Service](https://www.anthropic.com/legal/consumer-terms), effective 2025-10-08 and verified 2026-08-30.

Retention does not have one 30-day default across these products. For consumer accounts, turning off model improvement prevents future chats from being used for training, but saved chats remain in the product until the user deletes them; deletion from backend storage then occurs within 30 days, subject to safety and legal exceptions. Anthropic does not train on Team, Enterprise, or API inputs and outputs by default. API inputs and outputs are deleted from the backend within 30 days by default, while saved commercial-product chats are retained to provide conversation history. Enterprise can set a custom product retention period, with a 30-day minimum; if no custom period is set, the current guidance says product data is retained indefinitely. Sources: [consumer retention](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data), [commercial retention](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data), [commercial model-training policy](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training), and [Enterprise custom retention](https://privacy.claude.com/en/articles/10440198-configure-custom-data-retention-controls-for-enterprise-plans), verified 2026-08-30.

---

## 7. Self-hosted open-weight models: a separate business case, not a line item here

Every option above is a subscription or API billing choice. Self-hosting is a different kind of decision: a capital or dedicated-rental commitment sized to concurrent throughput, not a per-seat price. It deserves its own spike, not a bullet point in a plan-comparison table, because the two questions ("what plan do we buy" and "should we run our own inference") have almost no shared inputs.

The worked example in [Local vs Cloud Inference](../ecosystem/local-vs-cloud-inference.md#sizing-self-hosted-inference-for-a-team) is one 671B-class, 4-bit model on an 8xH100 node. Its source estimates about $10 per 1M output tokens at full utilization, $5,000 to $15,000/month of loaded operations time, and roughly 50 to 100 requests in flight to keep that specific batch full. Those figures are scenario inputs, not a portable threshold for every model or serving engine. Source: [Developers Digest, Self-Hosting Open-Weights Models](https://www.developersdigest.tech/blog/self-hosting-open-weights-models-break-even-math).

The same June analysis compared $10 self-hosted output against DeepSeek V4 Pro at $0.87 per 1M output tokens and correctly reported a gap above 11 times for that snapshot. DeepSeek's current primary pricing is $1.98 off-peak and $3.96 peak per 1M V4 Pro output tokens. Holding the self-host estimate fixed, the comparison is now about 5.1 times off-peak or 2.5 times peak, before redundancy or additional operations cost. Sources: [DeepSeek Models and Pricing](https://api-docs.deepseek.com/quick_start/pricing/) and the [June break-even analysis](https://www.developersdigest.tech/blog/self-hosting-open-weights-models-break-even-math), verified 2026-08-30.

General-purpose coding-agent demand is also too variable to infer GPU utilization from seat count. The 2026 coding-agent preprint found up to 30 times token variation across repeated runs of the same benchmark task. Capture a representative arrival trace, prompt and output lengths, cache behavior, parallel calls per task, and latency targets before comparing GPU-hour prices with API or seat prices. Source: [Bai et al., How Do AI Agents Spend Your Money?](https://arxiv.org/pdf/2604.22750), PDF pp. 1-6 and 10-12.
