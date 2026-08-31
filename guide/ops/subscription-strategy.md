---
title: "Subscription Strategy at Team Scale"
description: "A control-led framework for choosing workforce coding plans, governed API access, and self-hosted inference, with a multi-provider exercise for regulated organizations"
tags: [ops, cost, enterprise, multi-provider, mistral, guide]
---

# Subscription Strategy at Team Scale

> **Audience**: Engineering leaders, platform teams, security teams, and procurement owners deciding how an organization should buy and govern AI coding tools.
>
> **Scope**: Anthropic Team and Enterprise are the detailed worked example. The decision exercise also covers Codex, GitHub Copilot, Gemini Code Assist, Cursor, Mistral Vibe, governed API traffic, and self-hosted inference. This page does not treat a product plan or provider nationality as proof of regulatory compliance. For gateway implementation, see [API Gateway for Claude Code at Scale](./api-gateway.md). For task-level cost measurement, see [AI Unit Economics](./ai-unit-economics.md).

---

## TL;DR

| Situation | Start here | Why |
|---|---|---|
| The service supports a critical or important function under DORA, at any team size | Classify the function and run the [control gate](#7-decision-and-pilot-gate) before comparing seat counts | DORA does not mandate an Anthropic plan, but one required Enterprise-only control is enough to rule out Team for the assessed workflow |
| 2 to 150 intended users, Team controls satisfy the risk assessment | Team, with standard and premium seats mixed | The seat includes usage subject to plan limits, SSO, central administration, Commercial Terms, and no training on inputs or outputs by default |
| More than 150 intended users, or a documented need for an Enterprise-only control | Enterprise | The $20 seat fee buys organization access and controls; every token is then billed at API rates |
| Shared CI jobs, services, Agent SDK workloads, or unattended agents | Claude Platform API behind a tested spend policy and terminal cap | A human seat is the wrong identity and budget boundary for a production service |
| Regulated organization with both workforce use and production automation | Team or Enterprise for people, Platform API for services | Identity governance and API traffic control are separate decisions |
| Several coding assistants or providers under consideration | Run the [300-engineer portfolio exercise](#exercise-choose-a-provider-portfolio-for-300-engineers) | Claude, Codex, Copilot, Gemini, Cursor, and Mistral use different seat, credit, overage, and control boundaries |
| Self-hosted inference under consideration | A separate capacity and operations business case | Seat prices do not include the hardware, reliability, security, and staffing boundaries needed for a valid comparison |

Team and Enterprise expose the same model families. Enterprise adds centralized control over the models, effort levels, roles, and budgets available to each population. Choose it when a named control owner requires one of those features, when intended users exceed Team's documented scope, or when metered usage without per-seat plan limits is required. Otherwise, Team is the stronger default. The Enterprise label alone proves neither model quality nor regulatory compliance.

![A 300-engineer organization split into managed interactive workforce subscriptions, governed service automation, and private inference, each with separate cost and acceptance measures](../images/subscription-provider-portfolio.webp)

---

## 1. The $20 Enterprise seat does not include usage

The two $20 prices buy different things:

- **Team Standard** costs $20 per seat per month when billed annually, or $25 when billed monthly. The seat includes Claude usage subject to rolling plan limits. Team Premium costs $100 per seat per month when billed annually, or $125 when billed monthly, and includes five times more usage than Standard.
- **Usage-based Enterprise** costs $20 per seat per month, billed annually, for access. It includes no token allowance. Claude, Claude Code, and Cowork usage is billed separately at standard API rates. Anthropic documents no per-seat usage limit on this plan, and administrators can set organization and user spend limits.

Sources: [Anthropic plan pricing](https://claude.com/pricing) and [What is the Enterprise plan?](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan), verified 2026-08-31.

Anthropic publishes a minimum of 20 seats for self-serve Enterprise and 50 seats for sales-assisted Enterprise. A smaller regulated team that needs an Enterprise-only control cannot infer a smaller purchase path from the public documentation. It must budget against the published minimum. If Sales proposes another arrangement, the purchasing file should record it before using a lower seat count in the business case.

The default comparison is therefore:

```text
Team monthly cost       = seat price + optional usage credits beyond plan limits
Enterprise monthly cost = $20 access fee + metered token usage
```

At list price, an active developer's Enterprise bill combines the $20 access fee with uncapped, metered consumption. A custom sales contract may change the commercial result, but the public $20 headline does not establish a volume discount.

---

## 2. Team covers the baseline; Enterprise adds specific controls

The statement "we need Enterprise for compliance" is too vague to approve a purchase. Team and Enterprise both operate under Anthropic's Commercial Terms. Anthropic says it does not train generative models on Team, Enterprise, or API inputs and outputs by default. Team also includes SSO, central billing, connector administration, and a standard 30-day retention period for Claude Code data.

Enterprise adds controls that can close specific audit, identity, retention, or network gaps:

| Control | Team | Usage-based Enterprise | Decision relevance |
|---|---|---|---|
| Commercial Terms and no model training by default | Yes | Yes | Baseline protection, not an Enterprise differentiator |
| Supplier certifications and assurance artifacts | Supplier-level artifacts, subject to report scope | Supplier-level artifacts, subject to report scope | SOC 2 Type I and II, ISO 27001:2022, and ISO/IEC 42001:2023 are procurement inputs, not plan differentiators; verify each artifact's product scope and audit period in the Trust Center |
| SSO and central administration | Yes | Yes | Team can satisfy a basic managed-access requirement |
| Provisioning | Invite, manual removal, or JIT | SCIM available | SCIM matters when offboarding must remove access and seats from the identity provider without a second manual action |
| Roles | Primary Owner, Owner, Admin, and User | Custom roles and groups in addition to standard roles | Required when duties, feature access, or population policies must be separated more finely than Team permits |
| Model access | Access to all available models; no documented organization policy by model | Organization and custom-role model allowlists, plus per-model effort caps for custom roles | The model families are shared; Enterprise makes the approved model and effort policy enforceable across covered products |
| Audit evidence | No audit-log export | Audit logs and Compliance API | Required when investigations, surveillance, or control testing need organization-level evidence |
| Claude Code retention | Standard 30-day retention | Standard 30-day retention, plus eligible ZDR | ZDR is an Enterprise difference for Claude Code, but it disables features that require stored prompts or responses |
| Product retention policy | No custom organization schedule | Custom retention, minimum 30 days | Relevant when the organization's records schedule must be enforced centrally |
| Network and access controls | No documented IP allowlisting or tenant restriction | Network-level access control and IP allowlisting | Relevant only if the target surfaces and traffic paths are covered |
| Spend controls | Plan limits; optional usage-credit limits at organization and individual level | Organization, group, and individual spend limits for metered usage | Anthropic's dedicated Enterprise documentation confirms group policy; Team's published usage-credit controls stop at organization and individual levels |
| Additional data arrangements | No documented Team option for CMEK, US-only inference, or HIPAA-ready configuration | These options are available to eligible Enterprise organizations, subject to product scope and contract | A named requirement must map to the exact option; availability is not proof that it is enabled or sufficient |

Sources: [Anthropic pricing](https://claude.com/pricing), [Team plan](https://support.claude.com/en/articles/9266767-what-is-the-team-plan), [roles and permissions](https://support.claude.com/en/articles/9267276-roles-and-permissions), [Anthropic certifications](https://support.claude.com/en/articles/10015870-what-certifications-has-anthropic-obtained), [Anthropic Trust Center](https://trust.anthropic.com/), [Team and seat-based Enterprise usage credits](https://support.claude.com/en/articles/12005970-manage-usage-credits-for-team-and-seat-based-enterprise-plans), [Enterprise groups and spend limits](https://support.claude.com/en/articles/13799932-manage-groups-and-group-spend-limits-on-enterprise-plans), [Enterprise model access](https://support.claude.com/en/articles/15694740-manage-model-access-for-your-organization), [JIT and SCIM provisioning](https://support.claude.com/en/articles/13133195-set-up-jit-or-scim-provisioning), [Claude Code data usage](https://code.claude.com/docs/en/data-usage), and [Claude Code zero data retention](https://code.claude.com/docs/en/zero-data-retention), verified 2026-08-31.

Anthropic's Team help page and pricing comparison use overlapping labels for role-based access and spend controls. The table above uses the dedicated control documentation to distinguish Team's fixed roles and organization or user usage-credit limits from Enterprise custom roles, groups, and group-level spend policies. Confirm the exact control in the product instead of treating the shared label as feature parity.

### Provider certifications are supplier evidence, not a plan control

Anthropic scopes SOC 2 Type I and II, ISO 27001:2022, and ISO/IEC 42001:2023 to its commercial products rather than presenting them as Enterprise-only features. A procurement team should request the current certificates, reports, bridge letters, scope statements, exceptions, and any other available restricted assurance material through the Trust Center. It should then map each artifact to the products, processing paths, subcontractors, and period under review.

For a bank, those artifacts are an input to supplier assurance rather than a substitute for it. The ECB's July 2025 cloud-outsourcing guide says supervised entities must not rely over time solely on third-party audit reports or provider certifications. The institution still needs its own risk assessment, contractual audit rights, monitoring, and independent review. Source: [ECB Guide on outsourcing cloud services](https://www.bankingsupervision.europa.eu/ecb/pub/pdf/ssm.supervisory_guides202507.en.pdf), sections 2.5.1 to 2.5.3, verified 2026-08-31.

Each control has its own coverage boundary. The Compliance API does not capture Claude Code on the web, Claude Platform API workloads, Amazon Bedrock, or Google Vertex AI. Source: [Compliance API coverage](https://support.claude.com/en/articles/13015708-access-the-compliance-api), verified 2026-08-31.

ZDR is not included in the standard Enterprise plan. Anthropic enables it separately for qualified organizations. It applies to Claude Code inference, not to Chat or Cowork, and disables Claude Code on the web and cloud sessions from Desktop. Source: [Claude Code ZDR scope](https://code.claude.com/docs/en/zero-data-retention), verified 2026-08-31.

Terminal clients keep plaintext session transcripts on developer machines for 30 days by default unless the organization changes `cleanupPeriodDays` and enforces the setting. Transcripts started or most recently continued in Desktop or Cowork are exempt from that local default. Test the exact surface, provider, session type, and retention mode before writing a control statement. Source: [Claude Code data usage](https://code.claude.com/docs/en/data-usage), verified 2026-08-31.

### Compliance API evidence has its own risk boundary

The Compliance API creates a sensitive evidence plane. Depending on its scopes, a Compliance Access Key can expose organization activity, chats, files, projects, and Claude Code or Cowork session transcripts. It can also delete chats, files, and projects on demand. Source: [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api), verified 2026-08-31.

Anthropic documents six-year retention for the Activity Feed, six years by default for local session transcripts unless a finite organization retention period is set, and six years for remote Cowork transcripts. Those server-side records are separate from the local 30-day transcript files described above. Restrict Compliance API keys and exports, review their access, and define the retention of SIEM indexes and compliance archives. Source: [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention), verified 2026-08-31.

Team and Enterprise share important compliance foundations, but they expose different control evidence. Approve Enterprise only when one of its additional controls closes a documented requirement.

---

## 3. A bank buys against a control gap, not a plan label

A bank should classify the use case before comparing subscriptions. A developer using Claude Code on public sample code does not create the same risk as an agent reading customer data, production logs, payment logic, or authentication secrets.

For EU financial entities, DORA has required a register of contractual arrangements with ICT third-party providers since 17 January 2025. The institution must classify the supported function and assess the arrangement before selecting a plan. For banks under ECB supervision, the July 2025 cloud-outsourcing guide sets out DORA-aligned supervisory expectations and good practices using a risk-based, proportionate approach. Sources: [EBA preparation for DORA registers](https://www.eba.europa.eu/activities/direct-supervision-and-oversight/digital-operational-resilience-act/preparation-dora-application) and [ECB Guide on outsourcing cloud services](https://www.bankingsupervision.europa.eu/ecb/pub/pdf/ssm.supervisory_guides202507.en.pdf), verified 2026-08-31.

Where the service supports a critical or important function, the review reaches beyond product features to data and processing locations, access and audit rights, subcontracting, incident handling, continuity, and exit.

The purchasing file should answer these questions before it names Team or Enterprise:

1. **Data boundary**: Which repositories, data classes, connectors, secrets, logs, and production environments are allowed or prohibited?
2. **Identity lifecycle**: Is SSO plus JIT sufficient, or must deprovisioning and group membership be driven through SCIM?
3. **Evidence**: Which events, prompts, responses, files, and administrative changes must be available to security, audit, legal, or a regulator? For how long?
4. **Retention**: Does the use case require standard 30-day Claude Code retention, a custom product schedule, or ZDR? What must still be deleted from developer machines?
5. **Third-party risk**: Do the contract and annexes cover subprocessors, processing locations, incident notification, access and audit rights, service continuity, and exit?
6. **Change control**: Which model versions, Claude Code versions, connectors, MCP servers, and hosted surfaces are approved? How are updates tested and rolled back?
7. **Financial control**: What visibility, warning, approval, model-downshift, and terminal thresholds apply per user, team, service, and organization? Which stages apply to interactive people, and which workloads must stop deterministically?

Approve Enterprise when a named requirement maps to an Enterprise-only feature and a product test proves that the feature covers the intended workflow. A certification badge, a generic reference to compliance, or a sales comparison table is not that proof.

### What Enterprise still does not solve

Buying Enterprise does not transfer regulatory accountability to Anthropic. DORA keeps the financial entity responsible for its obligations, requires a register of ICT contractual arrangements, and requires additional assessment and contractual provisions where an ICT service supports a critical or important function.

The plan does not by itself provide:

- DORA compliance or the institution's required risk classification, due diligence, register, monitoring, and control evidence;
- EU data residency: Anthropic's published first-party Platform controls currently offer `global` or `us` inference and a US-only workspace geography, not an EU option;
- a tested exit and migration plan, including accessible data return and an adequate transition period;
- contractual capacity, recovery objectives, continuity tests, incident assistance, or precise service levels suitable for the classified function;
- automatic approval of every model, connector, MCP server, hosted surface, subprocessor, or future product change.

Articles 28 to 30 of DORA make these separate obligations concrete: the institution remains responsible, must assess concentration and substitutability, and must contract for processing locations, data access and return, service levels, incident support, audit rights, continuity, and exit where applicable. Enterprise features can supply parts of the evidence. They cannot replace the bank's assessment, contract, or tested operating controls. Sources: [DORA, Articles 28 to 30](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2554) and [Anthropic data residency](https://platform.claude.com/docs/en/manage-claude/data-residency), verified 2026-08-31.

---

## 4. The $13-per-active-day figure is a benchmark with missing denominators

Anthropic reports an average of about $13 per developer per active day and $150 to $250 per developer per month across enterprise deployments, with costs below $30 per active day for 90% of users. Anthropic recommends a pilot because model choice, codebase size, parallel sessions, and automation change the result. Source: [Anthropic, Manage costs effectively](https://code.claude.com/docs/en/costs), verified 2026-08-31.

That benchmark does not disclose the observation period, model mix, share of inactive developers, task mix, acceptance rate, or distribution above the 90th percentile. The daily denominator includes active days, while the monthly figure may include inactive days or users. The two values cannot establish what a particular developer, team, or agentic workflow should cost. They also cannot support the claim that a low-spend developer is not doing agentic engineering.

Current model defaults make the missing model mix material. Claude Code now defaults to Opus 5 for usage-based Enterprise and Team Premium, while Team Standard defaults to Sonnet 5. An administrator can override the organization default. A historical or mixed-model average is not a forecast for an Opus-heavy deployment. Source: [Claude Code model configuration](https://code.claude.com/docs/en/model-config), verified 2026-08-31.

Independent evidence supports measuring a distribution rather than trusting an average. Bai et al. repeated agentic coding runs on the same SWE-bench Verified tasks and observed up to 30-fold variation in total tokens; higher token use did not imply higher accuracy. Their eight-model benchmark is not production billing data, but it shows why one run or one fleet average cannot set a safe budget. Source: [Bai et al., How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks](https://arxiv.org/pdf/2604.22750), PDF pp. 1-4.

A practitioner account from Back Market provides a denominator closer to a 300-engineer scope. Nicolas Martignole reported 210 to 220 active users among 280 people, with an active user defined as someone who spent at least $1 that month. He reported a three-month average of $191 per active developer and about $3,000 for the highest-spend user in January. The talk provides no median, percentiles, accepted-task count, or billing export, and its later recap gives a January total that conflicts with an earlier figure. Treat the numbers as an operating account, not as an auditable forecast. Sources: [active-user scope at 49:05](https://www.youtube.com/watch?v=kSrEZ57thMg&t=2945s), [January tail at 50:04](https://www.youtube.com/watch?v=kSrEZ57thMg&t=3004s), and [three-month average at 50:48](https://www.youtube.com/watch?v=kSrEZ57thMg&t=3048s), published 2026-04-03.

The same account describes a staged purchasing policy: start with API billing to observe usage and avoid idle subscriptions, then consider a fixed-price Max plan for daily users. The claimed equivalence between a $200 Max plan and $1,100 to $1,200 of API usage was introduced as an estimate and came with no calculation. Measure the crossover from the organization's own invoices and accepted outcomes. A personal Max account also remains outside the employer-managed Team and Enterprise control boundary described in [Boundaries](#8-boundaries). Sources: [initial API decision at 06:37](https://www.youtube.com/watch?v=kSrEZ57thMg&t=397s) and [daily-user recommendation at 44:00](https://www.youtube.com/watch?v=kSrEZ57thMg&t=2640s), published 2026-04-03.

For a pilot, report at least:

- intended seats, activated seats, active users, and active days;
- task class, model version, effort level, context size, cache behavior, and number of parallel agents;
- cost per session and per accepted task, with median and upper percentiles;
- first-pass acceptance, retries, human review time, regressions, and rollback rate;
- separate totals for interactive work and unattended automation.

Without those denominators, a monthly average is an invoice summary, not an engineering decision.

---

## 5. Optimize cost per accepted task, not cost per token

Cheaper tokens can produce a higher workflow cost. If Haiku or Sonnet needs repeated prompting, produces a wrong patch, or shifts work into human review, its lower token rate may not offset retries and rework. One successful Opus run can be cheaper than three failed runs on a smaller model.

Use the canonical unit from [AI Unit Economics](./ai-unit-economics.md#2-building-a-cost-per-accepted-task):

```text
cost per accepted task =
  (model spend + retry spend + human review cost + rework cost)
  / accepted tasks
```

When a trial produces no accepted task, the ratio is undefined. Report zero accepted tasks, total attempts, and total spend instead of hiding the failed trial behind a dollar-per-task number.

At current public API rates, Opus 5 costs $5 per million input tokens and $25 per million output tokens, Sonnet 5 costs $2 and $10, and Haiku 4.5 costs $1 and $5. The 2.5-fold Opus-to-Sonnet rate difference is meaningful only if both models clear the same quality gate. Source: [Claude model pricing](https://platform.claude.com/docs/en/about-claude/pricing), verified 2026-08-31.

Databricks calls the set of models with the best price for a required quality level the *efficiency frontier*. Use the term as an evaluation discipline, not as a public ranking. A candidate belongs on the organization's frontier only for the task classes, model-harness pair, acceptance gate, and review-cost boundary that were actually tested. Databricks reports more than 30% lower average task cost from its internal Smart Router while roughly matching the most expensive model's quality, but publishes no task sample, paired protocol, or confidence interval. Source: [Databricks, "Managing AI Coding Costs at Scale"](https://www.databricks.com/blog/managing-ai-coding-costs-scale), 2026-08-07.

Set routing rules from measured task outcomes:

- Start ambiguous, cross-system, security-sensitive, or high-rework tasks on the strongest approved model.
- Use a cheaper model for mechanical or well-specified work only after repeated trials show that it preserves the acceptance rate and does not increase review or retry cost.
- Compare models on the same tasks, with more than one run per task. Record the full workflow through tests and human acceptance, not the first generated patch.
- Route by validated task class. Do not assume that a model family or an automatic complexity classifier knows the organization's quality threshold.
- Prefer a task-level model-harness decision before work starts when the task can remain on one stable cache path. If routing occurs per request, measure cache creation, cache reads, cold starts, and mid-task behavior changes.
- Price escalation and delegation as separate attempts. A cheap controller that consults an expensive model can still be cheaper, but duplicated context and review belong in the accepted-task total.

A failed cheaper-model comparison is valid evidence for the tasks that were tested. It is not evidence that every task requires Opus. The fleet decision needs the same comparison across representative work, with failure and rework priced into the result.

Team already includes access to all available models. Enterprise adds centralized enforcement. Administrators can disable models organization-wide and, for custom roles, restrict model access and cap the maximum effort level per model across Chat, Cowork, and supported Claude Code surfaces.

Anthropic's published plan comparison lists a 200k context window for Team and 500k on Enterprise's default model. That is a plan capability difference, not access to a different model family, and it does not establish a higher accepted-task rate. Source: [Anthropic pricing](https://claude.com/pricing), verified 2026-08-31.

Those controls have limits. Haiku cannot be disabled. Claude Code CLI version 2.1.199 or later reflects model and effort restrictions in its picker; earlier clients can still display disabled choices, but Anthropic says requests using them are rejected. The setting does not yet apply to Claude in Chrome or Claude Security. Claude aliases such as `opus` and `sonnet` can also move to newer versions over time. Pin full model identifiers for controlled deployments, run a regression suite before changing the pin, canary the new version, and keep a rollback path. Sources: [Team plan](https://support.claude.com/en/articles/9266767-what-is-the-team-plan), [Enterprise model access](https://support.claude.com/en/articles/15694740-manage-model-access-for-your-organization), and [Claude Code model configuration](https://code.claude.com/docs/en/model-config), verified 2026-08-31.

---

## 6. Workforce plans and production API traffic solve different problems

Use Team or Enterprise seats for named people. Use Claude Platform API identities for CI jobs, shared agents, scheduled workloads, and services that need their own budget, rate limit, and lifecycle.

A gateway such as LiteLLM or Portkey can issue virtual keys, attach team or service metadata, restrict models, and reject routed API requests after a configured budget is exceeded. A terminal cap does not by itself provide spend warnings, approvals, or quality-safe model downshifts; those require a policy layer and tested client behavior. The gateway cannot see or cap subscription-authenticated traffic sent directly to Anthropic. Enterprise already provides native user and organization spend controls for its metered workforce usage. Add a gateway when the organization needs one policy layer for Platform API traffic, multiple providers, or service identities. See [API Gateway for Claude Code at Scale](./api-gateway.md#31-progressive-spend-policy-for-interactive-users).

Practitioner accounts support gateway attribution, not productivity measurement. Shopify reports attributing enterprise API costs by team and person through its internal proxy. Ramp reports tracing costs by team and product through a similar internal layer. Back Market says its BigQuery telemetry exposed Anthropic API calls from clients such as Cursor alongside an existing license cost. None of the three accounts publishes the underlying spend data, implementation cost, or cost per accepted task. Sources: [Shopify at 22:22](https://www.youtube.com/watch?v=u-3IILWQPRM&t=1342s), published 2025-07-02; [Ramp at 24:53](https://www.youtube.com/watch?v=NMs8C2_3M0w&t=1493s), published 2026-03-09; and [Back Market at 45:09](https://www.youtube.com/watch?v=kSrEZ57thMg&t=2709s), published 2026-04-03.

A gateway contract does not approve every routed provider. Back Market reported that its organization allowed only a small internally reviewed subset of the providers available through OpenRouter. The transcript does not establish the exact count, and the speaker explicitly did not present the statement as legal advice. Keep a provider allowlist and review each provider's contract, processing path, and controls before enabling it. Source: [Nicolas Martignole at 38:17](https://www.youtube.com/watch?v=DRtd8S_3E-w&t=2297s), published 2026-07-22.

A regulated deployment can separate workforce and service identities:

```text
Developers  -> Team or Enterprise organization -> Anthropic workforce controls
CI/services -> Internal gateway                -> Claude Platform API
```

Do not use a developer's seat credential as the production identity of an unattended service.

---

## 7. Decision and pilot gate

Apply the gates in this order: function and data criticality, required controls and contract terms, product-surface coverage, then user count and cost. A critical or important DORA classification does not automatically mandate Enterprise. It does remove headcount as a safe shortcut: if the assessed workflow requires SCIM, Compliance API evidence, custom retention, network restrictions, or another Enterprise-only control, that requirement decides the plan even for a small team.

Choose **Team** when all three conditions hold: the intended user count stays within 150, Team's SSO and administrative model meet the identity requirement, and the risk assessment does not require Enterprise-only evidence, retention, network, or role controls.

Choose **Enterprise** when the user count or a signed control requirement forces it, and after the pilot validates the relevant feature on every intended surface. Accept that the $20 seat is an access charge and forecast token usage separately.

Add **Claude Platform behind a gateway** when production automation needs service identities, terminal budgets, cross-provider routing, or centralized API attribution. For interactive API traffic, test progressive warnings, approvals, and downshifts before the terminal cap. This can coexist with either workforce plan.

Those choices are the Anthropic branch of the decision. They do not establish that one provider should serve every developer or workload.

### Exercise: choose a provider portfolio for 300 engineers

The exercise asks which purchasing and deployment path should serve each population, not which vendor wins one universal ranking. Freeze every price, allowance, control, model version, and contract assumption on the date of the exercise. Re-run the commercial snapshot before procurement because several providers have changed their billing unit or plan eligibility during 2026.

#### Step 1: record the public commercial starting point

The table below is a source map verified on 2026-08-31. It is not a quote and does not normalize unlike billing units into one artificial seat price.

| Candidate path | Public starting point | Boundary the pilot must verify |
|---|---|---|
| Claude Team or usage-based Enterprise with Claude Code | Sections [1](#1-the-20-enterprise-seat-does-not-include-usage) and [2](#2-team-covers-the-baseline-enterprise-adds-specific-controls) document included Team usage versus Enterprise access plus metered tokens | Intended-user scope, active-user tail, model and effort policy, covered surfaces, and accepted-task cost |
| ChatGPT Business or Enterprise with Codex | Business publicly lists $20/$25 Standard and $100/$125 Premium seats, includes Codex, and targets organizations of 2 to 200 employees; Enterprise is custom-priced | A 300-engineer organization needs an Enterprise quote or another documented path. New Codex-only PAYG seats stopped being available to new Business workspaces on 2026-06-24, although eligible existing workspaces can retain them |
| GitHub Copilot Business or Enterprise | Business lists $19 per granted user with 1,900 monthly AI credits; Enterprise lists $39 with 3,900. Credits pool at the billing entity and additional usage is $0.01 per credit | Model-dependent credit burn, user and cost-center budgets, agent traffic, Enterprise-plan prerequisites, and the acceptance rate behind the credits consumed |
| Gemini Code Assist Standard or Enterprise | Google publishes per-license hourly rates under monthly and 12-month commitments. Enterprise adds code customization and higher agent usage | Actual billed commitment, license assignment, Google Cloud integration value, repository customization, daily agent limits, and portability outside Google Cloud |
| Cursor Teams or Enterprise | Teams lists $40 Standard and $120 Premium active seats; Enterprise is custom. Third-party model use is billed at public API price plus Cursor's $0.25 per million token rate | Per-user versus pooled usage, on-demand spend, Auto routing, third-party model markup, SCIM and advanced controls, Background Agent cost, and exit from Cursor-specific workflow state |
| Mistral Vibe Team or Enterprise | Team lists $24.99 per user; Enterprise is custom. The organization plan spans Vibe, Studio, and API usage, with included usage consumed before optional PAYG | Vibe CLI, IDE, Web, and remote-agent coverage; organization and Workspace caps; SAML, audit, Admin API maturity, support, and private-deployment terms |
| Governed multi-provider API | Provider tokens plus gateway, telemetry, and operator cost | Service identities, provider allowlist, fallback behavior, budget rejection, payload-logging policy, and traffic that bypasses the gateway |
| Self-hosted open-weight inference | No seat-price equivalent | Task quality, concurrency, TTFT, output speed, queue depth, availability, loaded infrastructure cost, and operator time at the same acceptance and latency gates |

Sources: [OpenAI business pricing](https://openai.com/business/pricing/) and [Codex flexible-pricing eligibility](https://help.openai.com/en/articles/11487671-flexible-pricing-for-the-enterprise-and-team-plan); [GitHub Copilot plan choice](https://docs.github.com/en/copilot/tutorials/roll-out-at-scale/assign-licenses/choose-enterprise-plan) and [AI-credit billing](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-organizations-and-enterprises); [Gemini Code Assist pricing](https://cloud.google.com/products/gemini/pricing); [Cursor team pricing](https://prod.cursor.com/docs/account/teams/pricing); [Mistral pricing](https://mistral.ai/pricing/), [subscriptions](https://docs.mistral.ai/admin/billing-usage/subscriptions), and [usage limits](https://docs.mistral.ai/admin/billing-usage/usage-limits), all verified 2026-08-31.

Mistral needs three separate candidate rows in the working spreadsheet even though the summary table groups them: Vibe workforce seats, Devstral or Codestral through Mistral's API, and a private or self-hosted open-weight deployment. Mistral says data is hosted in the EU by default, but some features can temporarily transfer data outside the EU; Enterprise customers can disable some of those features at organization level. French headquarters and EU-default hosting are relevant procurement facts, not proof that every processing path remains in France or the EU. Sources: [Mistral data-location guidance](https://help.mistral.ai/en/articles/347629-where-do-you-store-my-data-or-my-organization-s-data) and [Enterprise Admin API preview](https://docs.mistral.ai/admin/admin-api/overview), verified 2026-08-31.

#### Step 2: segment people before assigning seats

Do not start with 300 identical licenses. Complete this table from identity and billing exports. The first three rows partition the intended workforce without double-counting people; service workloads remain separate because they need non-human identities.

| Population | Intended users | Activated users | Monthly active users | Active days per user | Candidate surfaces | Required controls |
|---|---:|---:|---:|---:|---|---|
| Daily interactive coding-agent users |  |  |  |  |  |  |
| Occasional coding-assistant users |  |  |  |  |  |  |
| Restricted or sovereignty-sensitive users |  |  |  |  |  |  |
| CI, scheduled agents, and shared services | n/a | n/a | n/a | n/a |  |  |

#### Step 3: run the same four-week pilot across candidates

Use representative repository tasks and the same executable acceptance gates. Repeat tasks because one agentic run does not estimate the distribution. Record model and harness version, task class, routing level, routing decision, input and output tokens or provider credits, cache creation and reads, cold starts, tool failures, retries, review time, accepted outcome, latency, and any provider or gateway fallback. Record every spend warning, approval, downshift, and suspension with its threshold and outcome. A seat that also includes chat or office features may create value outside coding, but record that value separately instead of attributing the whole seat to engineering tasks.

For self-hosted candidates, replay the measured arrival pattern rather than translating 300 engineers into 300 concurrent requests. Capture GPU utilization, queue depth, TTFT, time per output token, cache eviction, outages, deployment work, and operator hours. Use the detailed method in [Sizing Self-Hosted Inference for a Team](../ecosystem/local-vs-cloud-inference.md#sizing-self-hosted-inference-for-a-team).

#### Step 4: calculate comparable decision units

```text
workforce monthly cost = committed seats + metered overage + non-seat add-ons
service monthly cost   = provider usage + gateway + telemetry + operator cost
self-host monthly cost = amortized hardware or rental + energy + network
                         + storage + monitoring + availability + operator cost

cost per active developer = workforce monthly cost / monthly active developers
cost per accepted task    = (all model, infrastructure, review, and rework cost)
                            / accepted tasks
```

Also report intended, assigned, activated, and active seats; median and upper-percentile spend; unused included credits; warnings, approvals, downshifts, terminal rejections; and workflows with zero accepted tasks. Do not hide failed trials behind an undefined cost-per-accepted-task ratio.

#### Step 5: choose a portfolio, then test the boundaries

A valid result can assign different paths to different populations. For example, a managed workforce plan may cover interactive development, a gateway may own CI and shared agents, and a private Mistral or other open-weight deployment may cover a narrow sovereignty-sensitive workload. This is a hypothesis to test, not a recommended allocation.

Reject a candidate when a required control or task-quality gate fails, even if its list price is lower. Before approval, test offboarding, each configured spend-policy stage, terminal rejection, audit export, data location and subprocessors, model-version change, cache behavior under routing, provider fallback, direct-traffic bypass, and exit or data-export behavior. Compare self-hosting only after the local model meets the same accepted-task and latency objectives as the managed candidates.

Before rollout, the decision owner should approve one evidence pack containing:

1. a supplier-assurance pack with the scope, audit period, exceptions, and independent assessment of each SOC 2, ISO, or restricted report used in the decision;
2. a Team-versus-Enterprise control matrix with an owner and test result for every required control;
3. a representative model evaluation with accepted-task quality and total workflow cost;
4. a monthly forecast showing median and tail usage, not only an average per seat;
5. an offboarding test, an audit or Compliance API coverage test, and a retention test;
6. a spend-policy test for every metered traffic path, including the terminal rejection path and any warning, approval, or downshift stages;
7. the completed multi-provider exercise with dated source URLs, contract deviations, and the selected population for each path;
8. a DORA and third-party-risk record where the organization determines those obligations apply.

For the Anthropic branch, if Team passes that gate, the purchasing file contains no demonstrated Enterprise business case. If Team fails a required control and Enterprise passes the same test, record the Enterprise-only feature, its owner, and the test evidence. For the portfolio decision, record why each selected path wins for its assigned population and which measured failure or control gap rejected the alternatives.

---

## 8. Boundaries

A reimbursed Pro or Max account is not an employer-managed substitute for Team or Enterprise. It lacks the same organization control plane and may be governed by Consumer Terms rather than Commercial Terms. Resolve the applicable contract before using personal accounts for company work. Source: [Claude Code legal and compliance](https://code.claude.com/docs/en/legal-and-compliance).

Self-hosted inference is a separate capacity and operations decision. The exercise includes it as a candidate path, but does not place it beside a seat price. Compare it on measured task quality, concurrency, throughput, latency, availability, security, and loaded operations cost. See [Local vs Cloud Inference](../ecosystem/local-vs-cloud-inference.md#sizing-self-hosted-inference-for-a-team).

---

## 9. One-page decision summary

Use this table after completing the pilot, not as a substitute for it. The decision gate combines the main control, cost, and rejection test. It does not rank model quality.

| Path | Use it for | How you pay | Decision gate |
|---|---|---|---|
| Claude Team | Managed interactive Claude Code use | Seat with included usage and plan limits | Team controls and included usage pass the pilot; otherwise test Enterprise |
| Claude Enterprise | Larger or regulated Claude Code deployments | $20 access fee per seat plus metered usage, subject to contract | A named Team control gap is resolved and tail usage remains affordable |
| ChatGPT Business or Enterprise with Codex | Interactive Codex use governed through a ChatGPT workspace | Business seat tier or Enterprise contract | The 300-person commercial path, audit coverage, spend behavior, and offboarding are documented |
| GitHub Copilot Business or Enterprise | GitHub-centered IDE, chat, and agent workflows | Granted-user fee, pooled AI credits, then overage | Model-specific credit burn produces an acceptable cost per accepted task |
| Gemini Code Assist Standard or Enterprise | Teams already governed through Google Cloud | Monthly or annual license-hour commitment | Code customization, agent limits, data controls, and portability justify the commitment |
| Cursor Teams or Enterprise | Teams choosing an AI-native editor workflow | Active seats plus model usage or overage | Outcome gains cover model markup, background agents, migration, and exit cost |
| Mistral Vibe Team or Enterprise | Managed Vibe workflows and European-provider procurement paths | Team seat with included usage and optional PAYG, or Enterprise contract | Vibe passes the task pilot and actual processing locations meet the sovereignty requirement |
| Governed multi-provider API | CI, shared agents, services, and model routing | Provider tokens plus gateway, telemetry, and operator cost | Routing, progressive or terminal spend controls, attribution, fallback, cache behavior, and bypass controls work; direct subscriptions remain outside the gateway |
| Self-hosted open-weight inference, including Devstral | Stable, high-volume or privacy-sensitive workloads | Infrastructure, energy, monitoring, availability, and operator time | Quality and latency match the target; measured concurrency and loaded cost beat the API alternative |

For 300 engineers, the defensible output is usually a portfolio assignment by population rather than one universal winner: a managed workforce path for interactive use, governed API identities for automation, and self-hosted inference only for workloads that pass the separate quality, capacity, and operations case. Record this as a measured decision, not a default allocation.
