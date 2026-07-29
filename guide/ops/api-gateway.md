---
title: "API Gateway for Enterprise Claude Code"
description: "Centralize cost control, budget enforcement, model allowlists, and usage tracking across teams using LiteLLM Gateway or Portkey as an Anthropic API proxy"
tags: [enterprise, cost, observability, ops, guide]
---

# API Gateway for Enterprise Claude Code

> **Audience**: Platform engineers and DevOps teams deploying Claude Code across an organization.
>
> **Scope**: Setting up a proxy layer between Claude Code clients and Anthropic's API to centralize cost control, budget enforcement, and usage visibility. For individual session cost estimation, see [observability.md](./observability.md). For MCP governance, see [enterprise-governance.md §3](../security/enterprise-governance.md#3-mcp-governance-workflow).

---

## TL;DR

| Problem | Gateway solution |
|---------|-----------------|
| No per-team cost breakdown | Virtual keys with team metadata, aggregated in dashboards |
| Developers can call any model | Model allowlists per key (unapproved calls return 403) |
| Runaway costs from agents | Budget cap per key, monthly reset, returns 429 when hit |
| No central audit log | Every request/response logged with key alias, team, tokens |

**The approach**: Set `ANTHROPIC_API_URL` on each developer machine to point to your gateway instead of `api.anthropic.com`. The gateway forwards requests to Anthropic, adds logging and budget enforcement, and issues virtual keys so your real Anthropic key never touches developer machines.

---

## 1. Why a Gateway Layer

Claude Code calls Anthropic's API directly using whatever key is in `ANTHROPIC_API_KEY`. Without a proxy layer:

- You have no per-team or per-project cost breakdown until the monthly invoice
- Any developer with a key can call any model, including the most expensive ones
- Budget limits depend entirely on each person's discipline
- There is no org-level audit log of what was built with AI assistance

A gateway sits between all Claude Code instances and Anthropic. It issues virtual keys to developers (scoped to a team or project), keeps the real Anthropic key server-side, and enforces policies on every request before forwarding.

---

## 2. LiteLLM Gateway

[LiteLLM](https://github.com/BerriAI/litellm) is the most widely used open-source LLM proxy for enterprise deployments. It supports Anthropic natively, issues virtual keys, enforces budgets, and exposes Prometheus metrics for Grafana dashboards.

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
# Note the /anthropic path suffix — required for Anthropic Messages API format
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

---

## 4. Model Allowlists

Calls to models not in a key's `models` list return a `403 ModelNotAllowedError` before the request reaches Anthropic. This enforces your model approval policy at the network layer regardless of what a developer puts in their Claude Code config.

A three-tier structure that matches most org needs:

| Tier | Models allowed | Monthly budget | For |
|------|---------------|---------------|-----|
| Developer default | Haiku, Sonnet | $30 | All engineers |
| Project elevated | Haiku, Sonnet | $100 | Active sprint work |
| Lead/Architect | All models | $300 | Tech leads, architects |

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

LiteLLM also ships a basic UI at `/ui` (enable with `LITELLM_UI_USERNAME` and `LITELLM_UI_PASSWORD` env vars) for quick cost breakdown views without needing a full Grafana setup.

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

The gateway controls what reaches Anthropic's API. It does not address:

- What files Claude Code reads on the developer's machine (use `permissions.deny` in `settings.json`)
- Which MCP servers are active locally (see [enterprise-governance.md §3](../security/enterprise-governance.md#3-mcp-governance-workflow))
- Code quality of AI output (use PR review gates)
- Session-level audit trails showing which files were modified (see [ai-traceability.md](./ai-traceability.md#pr-audit-trail))

---

## See Also

- [observability.md](./observability.md) for individual session logging and cost estimation without a proxy
- [enterprise-governance.md](../security/enterprise-governance.md) for MCP governance and guardrail tiers
- [ai-traceability.md](./ai-traceability.md) for AI attribution in commits and PR audit trails
- [LiteLLM proxy documentation](https://docs.litellm.ai/docs/proxy/quick_start)
- [Portkey documentation](https://docs.portkey.ai)
