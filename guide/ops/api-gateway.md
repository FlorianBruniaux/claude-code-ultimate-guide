---
title: "API Gateway for Enterprise Claude Code"
description: "Centralize cost control, progressive spend policy, terminal budgets, model allowlists, and usage tracking across teams using Claude apps gateway or another Anthropic-compatible proxy"
tags: [enterprise, cost, observability, ops, guide]
---

# API Gateway for Enterprise Claude Code

> **Audience**: Platform engineers and DevOps teams deploying Claude Code across an organization.
>
> **Scope**: Setting up a proxy layer between Claude Code clients and a model upstream to centralize cost control, budget enforcement, and usage visibility. For individual session cost estimation, see [observability.md](./observability.md). For MCP governance, see [enterprise-governance.md §3](../security/enterprise-governance.md#3-mcp-governance-workflow).

---

## TL;DR: third-party gateway examples

The table and setup below describe the LiteLLM and Portkey examples in this page. They do not describe Claude apps gateway.

| Problem | Third-party gateway example |
|---------|-----------------|
| No per-team cost breakdown | Virtual keys with team metadata, aggregated in dashboards |
| Developers can call any model | Model allowlists per key (unapproved calls return 403) |
| Runaway costs from unattended agents | Terminal budget cap per key, monthly reset, returns 429 when hit |
| Interactive developer spend spikes | Gateway telemetry can feed warnings, approvals, and model downshifts; a budget field alone does not implement that policy |
| No common API telemetry | Routed requests attributed by key alias, team, model, and tokens; payload logging depends on configuration |

**The third-party approach**: Set `ANTHROPIC_API_URL` on each developer machine to point to a compatible gateway instead of `api.anthropic.com`. The examples below forward requests, add configured logging and budget enforcement, and issue virtual keys so the provider key need not be present on developer machines.

---

## Current first-party surface: Claude apps gateway

[Claude apps gateway](https://code.claude.com/docs/en/claude-apps-gateway) is Anthropic's self-hosted gateway. It ships in the `claude` binary and runs with `claude gateway --config gateway.yaml`. It sits between Claude Code clients and an upstream. Its ordered configuration can route and fail over across the five documented upstream provider options: Anthropic API, Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, and Microsoft Foundry.

Use it when the organization needs a self-hosted, Claude Code-specific gateway with corporate SSO, per-identity-group model access, managed-settings delivery, and OpenTelemetry Protocol telemetry. The gateway retains the upstream credential in organization infrastructure. Developers authenticate through the corporate identity provider and receive short-lived bearer tokens instead of provider credentials.

### Deployment boundary

The official quickstart requires Claude Code v2.1.195 or later on the gateway host and developer machines, an OIDC identity provider, PostgreSQL, an upstream credential, and a private-network gateway address. The private-address requirement is a security control because a trusted gateway can deliver settings that run commands on developer machines. Put it behind an internal load balancer or VPN; do not expose it as a public endpoint.

The documented sign-in flow is interactive browser SSO. It has no service-token flow for unattended CI, so a CI system without a developer to approve the device flow must authenticate directly to its provider instead. A developer-signed-in machine can use the existing gateway session for `claude -p` and Agent SDK runs, subject to gateway policy.

### What the gateway controls, and what it does not

| Surface | Documented behavior |
|---|---|
| Identity and upstream credentials | The gateway authenticates developers with the IdP, issues short-lived bearer tokens (one hour by default), and uses the organization's provider credential upstream. |
| Model and client policy | IdP groups map to model allowlists and managed settings. A request for a non-granted model returns `400`. Locked managed settings cannot be overridden locally. |
| Telemetry | The gateway forwards OTLP metrics with token counts, model, identity, and latency. It does not log or store prompt or completion content. Logs and traces are per-destination opt-ins and can include commands and file paths. |
| Anthropic data plane | The gateway's data plane sends nothing to Anthropic unless the Anthropic API is configured as an upstream. |
| Other client traffic | Version checks and downloads can still go directly from Claude Code to Anthropic and require separate egress policy or documented nonessential-traffic controls. |

![User subscriptions bypass gateway budgets and attribution while CI, shared agents, scheduled workflows, and internal services pass through centralized keys, quotas, model allowlists, fallback, and observability](../images/gateway-visibility-boundary.webp)

The gateway does not make a desktop application, local filesystem, or plugin automatically safe. [Computer Use](../core/computer-use.md) has a separate desktop trust boundary, and [plugin distribution](../ecosystem/plugin-distribution.md) has a separate extension supply-chain boundary.

### Verify before rollout

The official quickstart defines three initial checks: fetch the OAuth discovery document, request device authorization, then complete browser sign-in. These check boot, database access, and identity-provider redirection in sequence. A successful gateway boot is not proof that the upstream inference path works, because some cloud credentials resolve only on the first request. Run a permitted test request through the intended upstream and examine the first failing layer if it fails.

Confirm the gateway's TLS certificate fingerprint during first connection, publish the full expected SHA-256 fingerprint for developers, and plan certificate rotations. Test a denied-model request, a managed-setting restriction, IdP deprovisioning, telemetry destination, and fail-closed startup for a gateway-signed-in session before declaring gateway policy enforced. Enforce provider egress separately if gateway-only routing is required.

For general gateway architecture and external gateway constraints, read [Anthropic's gateway overview](https://code.claude.com/docs/en/gateways). The remainder of this page covers third-party gateway examples and is not an Anthropic product specification.

---

## Third-party implementation examples

The remaining LiteLLM and Portkey material is third-party implementation guidance. Its virtual keys, `403` model rejection, `429` budget behavior, and request/response logging are not claims about Claude apps gateway.

## 1. Why a Gateway Layer

Claude Code can call Anthropic or another supported provider directly with the credential and endpoint configured by the organization. Without a proxy layer:

- Team and project attribution depends on provider reporting and how the organization separates keys
- Model restrictions depend on the upstream provider's controls
- Budget enforcement depends on upstream controls or an external policy layer
- There is no common request telemetry across providers

A gateway sits between configured Claude Code instances and their upstream providers. It issues virtual keys to developers (scoped to a team or project), keeps provider credentials server-side, and enforces policies on requests routed through it. Subscription-authenticated traffic and clients using direct provider credentials remain outside that control plane.

---

## 2. LiteLLM Gateway

[LiteLLM](https://github.com/BerriAI/litellm) is an open-source Python LLM proxy. It supports Anthropic, issues virtual keys, can enforce configured budgets, and exposes metrics for external dashboards.

### 2.1 Installation

```bash
pip install 'litellm[proxy]'

# Docker is recommended for production
docker pull ghcr.io/berriai/litellm:main-latest
```

### 2.2 Configuration

Create `litellm_config.yaml` to route to Anthropic:

```yaml
model_list:
  - model_name: claude-haiku-4-5
    litellm_params:
      model: anthropic/claude-haiku-4-5-20251001
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: claude-sonnet-5
    litellm_params:
      model: anthropic/claude-sonnet-5
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: claude-opus-4-8
    litellm_params:
      model: anthropic/claude-opus-4-8
      api_key: os.environ/ANTHROPIC_API_KEY

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL  # PostgreSQL required for persistent keys

litellm_settings:
  drop_params: true  # Ignore unknown params silently
```

Start the proxy:

```bash
litellm --config litellm_config.yaml --port 4000
```

### 2.3 Connecting Claude Code

Set these two environment variables on each developer machine (distribute via your secrets manager, dotfile repo, or onboarding script):

```bash
# Point Claude Code to your LiteLLM instance
# Note the /anthropic path suffix, required for Anthropic Messages API format
export ANTHROPIC_API_URL=http://your-litellm-host:4000/anthropic

# Developer uses a virtual key, not the real Anthropic key
export ANTHROPIC_API_KEY=sk-litellm-team-backend-abc123
```

Claude Code does not require any other change. It reads `ANTHROPIC_API_URL` and uses it transparently. The `/anthropic` path suffix is required: LiteLLM exposes the Anthropic Messages API format at `/anthropic/v1/messages`, separate from its OpenAI-compatible endpoint at `/v1/chat/completions`.

---

## 3. Virtual Keys and Team Budgets

Create virtual keys through the LiteLLM management API. Each key maps to a team or project and carries an optional monthly budget cap.

```bash
# Backend team: Sonnet + Haiku only, $50/month budget
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "key_alias": "team-backend",
    "team_id": "team-backend",
    "max_budget": 50,
    "budget_duration": "monthly",
    "models": ["claude-haiku-4-5", "claude-sonnet-5"],
    "metadata": {"team": "backend", "project": "api-v2"}
  }'

# Leads: all models, $300/month
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "key_alias": "lead-full-access",
    "team_id": "leads",
    "max_budget": 300,
    "budget_duration": "monthly",
    "models": ["claude-haiku-4-5", "claude-sonnet-5", "claude-opus-5"]
  }'
```

When a budget is hit, Claude Code receives a `429 BudgetExceededError`. The key automatically resets at the start of the next budget cycle.

```bash
# Check current spend for a key
curl http://localhost:4000/key/info?key=sk-litellm-team-backend-abc123 \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"
```

### 3.1 Progressive spend policy for interactive users

The LiteLLM example above demonstrates a terminal cap. It does not demonstrate progressive warnings, approval gates, or a quality-safe model downshift. Build those as an explicit policy layer, or verify that the selected gateway implements each stage on the intended client and traffic path.

| Threshold stage | Required behavior | Evidence to retain |
|---|---|---|
| **Visibility** | Show current spend, spend rate, model, and remaining headroom without interrupting work | User, team, model, timestamp, routed traffic scope |
| **Self-clearing warning** | Ask the developer to acknowledge an unusual spend rate | Threshold, acknowledgement, session or task identifier |
| **Approval gate** | Require a budget owner to approve further premium-model spend | Approver, approved amount or duration, reason, expiry |
| **Downshift** | Move future work to a lower-cost approved model only for task classes that passed the same quality gate | Previous and new model-harness pair, routing reason, cache effect, accepted outcome |
| **Suspension** | Return a clear terminal error with reset or escalation instructions | Denial reason, reset time, owner, recovery path |

Keep a hard terminal budget for unattended agents, CI, scheduled jobs, and services. No person is present to interpret a warning, and a silent downshift can change behavior inside an automated workflow. For interactive development, the stages above can prevent accidental spend before suspension. Databricks reports this progressive pattern from its own deployment and conversations with other companies; the report is informal and does not establish that higher spend means higher productivity. Source: [Databricks, "Managing AI Coding Costs at Scale"](https://www.databricks.com/blog/managing-ai-coding-costs-scale), 2026-08-07.

A gateway can only apply these controls to traffic it sees. Subscription-authenticated clients and direct provider credentials remain outside this policy. Reconcile gateway events with workforce-plan controls and provider invoices before calling the organization-wide spend policy complete.

---

## 4. Model Allowlists

Calls to models not in a key's `models` list return a `403 ModelNotAllowedError` before the request reaches Anthropic. This enforces your model approval policy at the network layer regardless of what a developer puts in their Claude Code config.

A three-tier structure that matches most org needs:

| Tier | Models allowed | Monthly budget | For |
|------|---------------|---------------|-----|
| Developer default | Haiku, Sonnet | $30 | All engineers |
| Project elevated | Haiku, Sonnet | $100 | Active sprint work |
| Lead/Architect | All models | $300 | Tech leads, architects |

A model allowlist is not a provider allowlist. An aggregator can expose the same model through several infrastructure providers, each with a different contract and processing path. Back Market reported allowing only a small internally reviewed subset of the providers available through OpenRouter. The transcript does not establish the exact count, and the speaker did not present the statement as legal advice. Review and approve each provider separately. Source: [Nicolas Martignole at 38:17](https://www.youtube.com/watch?v=DRtd8S_3E-w&t=2297s), published 2026-07-22. See [Subscription Strategy](./subscription-strategy.md#6-workforce-plans-and-production-api-traffic-solve-different-problems) for the workforce and API identity split.

---

## 5. Usage Dashboards

LiteLLM exposes Prometheus metrics at `/metrics`. Add a scrape config in Prometheus:

```yaml
scrape_configs:
  - job_name: litellm
    static_configs:
      - targets: ['litellm-host:4000']
    metrics_path: /metrics
```

Key metrics for Grafana panels:

```
# Total requests by team and model
litellm_requests_total{model, team_id, key_alias}

# Cost by team (USD)
litellm_spend_total{model, team_id}

# Token counts split by input/output/cache
litellm_tokens_total{token_type, model, team_id}

# Error rate by type (budget exceeded, model not allowed, upstream timeout)
litellm_failed_requests_total{model, error_type}
```

For a progressive spend policy, also record the configured threshold stage, warning acknowledgements, approval decisions, downshifts, suspensions, and the task outcome after each intervention. Raw spend and token counters cannot show whether a downshift increased retries, review time, or rejected work.

LiteLLM also ships a basic UI at `/ui` (enable with `LITELLM_UI_USERNAME` and `LITELLM_UI_PASSWORD` env vars) for quick cost breakdown views without needing a full Grafana setup.

Practitioner accounts show what this attribution can reveal, within the traffic the gateway observes. Shopify reports attributing enterprise API costs by team and person through an internal proxy. Ramp reports tracing costs by team and product. Back Market says its BigQuery telemetry exposed Anthropic API spend from clients such as Cursor alongside an existing license cost. These accounts publish neither the underlying spend data nor implementation cost or cost per accepted task. Sources: [Shopify at 22:22](https://www.youtube.com/watch?v=u-3IILWQPRM&t=1342s), published 2025-07-02; [Ramp at 24:53](https://www.youtube.com/watch?v=NMs8C2_3M0w&t=1493s), published 2026-03-09; and [Back Market at 45:09](https://www.youtube.com/watch?v=kSrEZ57thMg&t=2709s), published 2026-04-03.

---

## 6. OpenTelemetry Integration

LiteLLM supports native OTel export, which integrates with the observability stack covered in [observability.md §10](./observability.md):

```yaml
litellm_settings:
  otel_endpoint: http://otel-collector:4317
  otel_headers:
    Authorization: Bearer ${OTEL_BEARER_TOKEN}
```

Each request generates a span with attributes including `litellm.model`, `litellm.team_id`, `litellm.key_alias`, `litellm.total_tokens`, and `litellm.spend`. These flow into your existing traces alongside application-level spans.

---

## 7. Production Deployment

Run LiteLLM behind a TLS-terminating reverse proxy (nginx or Caddy). A minimal Docker Compose setup:

```yaml
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    ports:
      - "4000:4000"
    environment:
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      LITELLM_MASTER_KEY: ${LITELLM_MASTER_KEY}
      DATABASE_URL: postgresql://user:pass@db:5432/litellm
    volumes:
      - ./litellm_config.yaml:/app/config.yaml
    command: ["--config", "/app/config.yaml", "--port", "4000"]
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: litellm
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

PostgreSQL is required for persistent key management and usage history. Without it, virtual keys and budget state reset on container restart.

For high availability, run two LiteLLM instances behind a load balancer. Both share the same PostgreSQL database for consistent key state.

---

## 8. Portkey as a Managed Alternative

[Portkey](https://portkey.ai) offers the same gateway capabilities as a hosted service, with no infrastructure to manage. Free tier covers small teams (up to 10K requests/month).

```bash
export ANTHROPIC_API_URL=https://api.portkey.ai/anthropic
export ANTHROPIC_API_KEY=your-real-anthropic-key
export PORTKEY_API_KEY=your-portkey-api-key
```

Portkey also supports `x-portkey-virtual-key` headers for routing, logging, and fallback configs. The trade-off: your request metadata leaves your infrastructure and goes to Portkey's servers. Review their data processing terms if you have compliance requirements.

---

## 9. What the Gateway Does Not Cover

The gateway controls requests routed through it. It does not address:

- Subscription-authenticated Claude usage sent directly to Anthropic
- API traffic from clients that retain direct provider credentials or bypass the gateway endpoint
- What files Claude Code reads on the developer's machine (use `permissions.deny` in `settings.json`)
- Which MCP servers are active locally (see [enterprise-governance.md §3](../security/enterprise-governance.md#3-mcp-governance-workflow))
- Code quality of AI output (use PR review gates)
- Whether a warning, approval, or model downshift preserves accepted-task quality
- Session-level audit trails showing which files were modified (see [ai-traceability.md](./ai-traceability.md#pr-audit-trail))

If gateway-only API routing is a policy requirement, remove direct provider credentials from developer machines and enforce provider egress separately. Reconcile gateway telemetry with workforce-plan and provider invoices; a gateway dashboard alone is not a complete organization-wide spend ledger.

---

## See Also

- [observability.md](./observability.md) for individual session logging and cost estimation without a proxy
- [enterprise-governance.md](../security/enterprise-governance.md) for MCP governance and guardrail tiers
- [ai-traceability.md](./ai-traceability.md) for AI attribution in commits and PR audit trails
- [Computer Use in Claude Code](../core/computer-use.md) for desktop control and its local permission boundary
- [Plugin Distribution and Recommendation Hints](../ecosystem/plugin-distribution.md) for marketplace and CLI recommendation controls
- [Databricks cost-management resource evaluation](../../docs/resource-evaluations/databricks-managing-ai-coding-costs-scale.md) for the evidence boundary behind progressive spend controls and routing claims
- [Claude apps gateway](https://code.claude.com/docs/en/claude-apps-gateway) for Anthropic's current gateway reference
- [LiteLLM proxy documentation](https://docs.litellm.ai/docs/proxy/quick_start)
- [Portkey documentation](https://docs.portkey.ai)
