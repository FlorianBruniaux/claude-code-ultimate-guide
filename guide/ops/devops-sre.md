---
title: "DevOps & SRE with Claude Code"
description: "FIRE framework for infrastructure diagnosis and DevOps workflows with Claude Code"
tags: [devops, guide, ci-cd, workflows]
---

# DevOps & SRE with Claude Code

**Reading time**: 30 minutes
**Skill level**: Intermediate (assumes DevOps basics)
**Prerequisites**: Claude Code basics ([Sections 1-2](./ultimate-guide.md#1-getting-started) of main guide)

---

> **The FIRE Framework**: A systematic approach to infrastructure diagnosis with Claude Code.
>
> **F**irst Response → **I**nvestigate → **R**emediate → **E**valuate

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Pattern: Infrastructure Diagnosis](#pattern-infrastructure-diagnosis)
3. [Pattern: Incident Response](#pattern-incident-response)
4. [Pattern: Infrastructure as Code](#pattern-infrastructure-as-code)
5. [Guardrails & Adoption](#guardrails--adoption)
6. [Quick Reference](#quick-reference)

---

# Quick Start

**Goal**: Get productive with Claude Code for DevOps in 5 minutes.

## Quick Self-Check

| Situation | Jump To |
|-----------|---------|
| I'm in an active incident NOW | [Emergency: K8s Troubleshooting](#kubernetes-troubleshooting) |
| First time using Claude for DevOps | [Tutorial: First Diagnosis](#your-first-infrastructure-diagnosis) |
| Want to automate my runbooks | [Pattern: Incident Response](#pattern-incident-response) |
| Evaluating for my team | [Guardrails & Adoption](#guardrails--adoption) |
| Need ready-to-use prompts | [Quick Reference](#quick-reference) |

## The FIRE Framework

Every infrastructure diagnosis with Claude follows this pattern:

```
F - First Response   → Give Claude the symptom + context
I - Investigate      → Claude analyzes logs, metrics, config
R - Remediate        → Claude proposes fix (with human approval)
E - Evaluate         → Postmortem, documentation, prevention
```

### Why FIRE?

| Phase | Human Role | Claude Role |
|-------|------------|-------------|
| **F**irst Response | Describe symptom, provide context | Triage, prioritize checks |
| **I**nvestigate | Run commands, paste output | Analyze, correlate, hypothesize |
| **R**emediate | **Approve or reject** | Propose fix, explain impact |
| **E**valuate | Review, share knowledge | Generate postmortem, docs |

**Critical**: Claude proposes, you approve. This is especially important for:
- Destructive operations (delete, scale down, restart)
- Production environments
- Security-sensitive changes

## Your First Infrastructure Diagnosis

### Example: Pod CrashLoopBackOff

```bash
# Step 1: FIRST RESPONSE - Give context
claude "I have a pod in CrashLoopBackOff in the payment-service namespace.
Environment: production
Cluster: gke-prod-us-east1
Started: 10 minutes ago
What are the first 3 things I should check?"

# Step 2: INVESTIGATE - Run suggested commands and share output
kubectl describe pod payment-api-7d4b8c6f5-x2j9k -n payment-service
# Copy output and paste to Claude

# Step 3: REMEDIATE - Claude proposes, you approve
claude "Based on this describe output, what's the fix?
CONSTRAINT: Show me the exact command but don't execute anything."

# Step 4: EVALUATE - Document the incident
claude "Create a brief incident note for our wiki:
- What happened
- Root cause
- Fix applied
- Prevention recommendation"
```

### What Claude Returns (First Response Example)

```markdown
## CrashLoopBackOff Triage (Priority Order)

1. **Check exit code and last logs**
   ```bash
   kubectl logs payment-api-7d4b8c6f5-x2j9k -n payment-service --previous
   ```
   Most common: OOM (exit 137), config errors (exit 1), dependency failures

2. **Check pod events and resource limits**
   ```bash
   kubectl describe pod payment-api-7d4b8c6f5-x2j9k -n payment-service
   ```
   Look for: OOMKilled, ImagePullBackOff, liveness probe failures

3. **Check recent deployment changes**
   ```bash
   kubectl rollout history deployment/payment-api -n payment-service
   ```
   If recent: consider rollback while investigating
```

---

# Pattern: Infrastructure Diagnosis

**Goal**: Systematic troubleshooting for common infrastructure issues.

## Kubernetes Troubleshooting

### K8s MCP Server Setup

For persistent K8s context, install the K8s MCP server:

```json
// ~/.claude.json (or .mcp.json)
{
  "mcpServers": {
    "kubernetes": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-kubernetes"]
    }
  }
}
```

**Benefits**: Claude can query cluster state directly, reducing copy-paste cycles.

**Without MCP**: You'll pipe kubectl output to Claude manually (still effective).

### Prompts by Symptom

Copy-paste these prompts, replacing `<bracketed>` values.

#### CrashLoopBackOff

```bash
kubectl describe pod <pod> -n <ns> | claude "Analyze this CrashLoopBackOff:
1. What's the exit code and what does it mean?
2. Check the last 5 restarts pattern (timing, consistent or escalating?)
3. Suggest 3 most likely root causes based on the events
4. Give me the exact commands to investigate each hypothesis"
```

**Common Causes Claude Will Identify**:
- Exit 137: OOMKilled (memory limit hit)
- Exit 1: Application error (bad config, missing dependency)
- Exit 143: SIGTERM (graceful shutdown timeout)

#### OOMKilled

```bash
kubectl top pods -n <ns> && kubectl describe pod <pod> -n <ns> | claude "This pod was OOMKilled:
1. Compare requests vs limits vs actual usage
2. Is this a memory leak or under-provisioning?
3. If leak: what patterns in the container suggest investigation paths?
4. If under-provisioned: suggest optimal resource settings based on this data"
```

**Follow-up for Memory Leaks**:
```bash
claude "The pod has been restarting every 2 hours with OOMKilled.
Memory grows linearly from 200Mi to 512Mi limit before crash.
Language: Node.js 18
What are the top 3 things to check for memory leaks in this stack?"
```

#### ImagePullBackOff

```bash
kubectl describe pod <pod> -n <ns> | claude "ImagePullBackOff diagnosis:
1. Is this an auth issue, network issue, or wrong image name?
2. What's the exact error message telling us?
3. Give me commands to verify the image exists and credentials work"
```

#### Pending Pod (Not Scheduling)

```bash
kubectl describe pod <pod> -n <ns> && kubectl describe nodes | claude "Pod stuck in Pending:
1. Is this resource constraints, node selectors, or affinity rules?
2. Which nodes were considered and why rejected?
3. What's the quickest fix vs proper solution?"
```

#### Service Not Reachable

```bash
kubectl get svc,endpoints -n <ns> && kubectl describe svc <svc> -n <ns> | claude "Service not reachable:
1. Are there healthy endpoints?
2. Is the selector matching pods correctly?
3. Is it a network policy blocking traffic?
Give me diagnostic commands for each possibility"
```

### Case Study: Production Outage Root Cause

**Situation**: E-commerce platform, 3 AM page, checkout service returning 503s.

**FIRE in Action**:

```bash
# F - First Response
claude "INCIDENT: checkout-service returning 503s, started 10 min ago.
Impact: 100% of checkout attempts failing.
Environment: AWS EKS production, us-east-1.
Recent changes: deployment 2 hours ago (new feature flag logic).
What's the fastest diagnostic path?"

# I - Investigate (Claude suggested checking pods first)
kubectl get pods -n checkout -l app=checkout-service
# Output: 3/5 pods in CrashLoopBackOff

kubectl logs checkout-service-xxx --previous | tail -50 | claude "Analyze crash logs"
# Claude identifies: panic: nil pointer dereference in feature flag code

# R - Remediate
claude "Root cause identified: nil pointer in feature flag logic from recent deploy.
Options:
A) Rollback to previous version
B) Hotfix the nil check
Which is faster and safer at 3 AM?"
# Claude recommends: Rollback (faster, proven state, fix properly tomorrow)

kubectl rollout undo deployment/checkout-service -n checkout
# Service restored in 2 minutes

# E - Evaluate (next day)
claude "Create postmortem from this incident:
Timeline: 3:02 AM alert, 3:15 AM root cause found, 3:17 AM rollback, 3:19 AM resolved
Root cause: Feature flag nil pointer from commit abc123
Impact: 15 minutes checkout downtime
Format: Blameless, focused on prevention"
```

**Outcome**: 15-minute MTTR, clear postmortem, prevention action items identified.

## Log Analysis & Correlation

### Multi-Service Log Correlation

```bash
# Collect logs from related services
kubectl logs -l app=api-gateway -n ingress --since=10m > gateway.log
kubectl logs -l app=auth-service -n auth --since=10m > auth.log
kubectl logs -l app=payment-service -n payment --since=10m > payment.log

# Analyze correlation
cat gateway.log auth.log payment.log | claude "Correlate these logs:
1. Find the request flow for failed transactions
2. Identify where the failure originates
3. Are there patterns in timing or specific endpoints?
4. Create a timeline of events"
```

### Log Pattern Detection

```bash
# Find anomalies in error patterns
grep -E "ERROR|WARN|Exception" app.log | claude "Analyze error patterns:
1. Cluster similar errors (group by type, not timestamp)
2. What's the most frequent vs most severe?
3. Which errors are correlated (same root cause)?
4. Prioritize investigation order"
```

### Prometheus/Grafana Query Help

```bash
claude "I need a PromQL query to:
- Show p99 latency for the payment-service
- Group by endpoint
- Alert if > 500ms for 5 minutes
Include the alert rule YAML too"
```

## What Claude CAN'T Do (Limitations)

Understanding limitations prevents frustration and unsafe reliance.

| Limitation | Impact | Workaround |
|------------|--------|------------|
| **No real-time cluster state** | Can't see current pod status | Use K8s MCP or paste kubectl output |
| **No direct API access** | Can't call AWS/GCP APIs | Use MCP servers or share CLI output |
| **Context window limits** | ~100K tokens max | Focus on relevant logs, not full dumps |
| **No persistent memory** | Forgets between sessions | Use CLAUDE.md for project context |
| **Hallucination risk** | May suggest invalid flags | Always verify commands before running |
| **No real-time metrics** | Can't see current graphs | Screenshot Grafana or paste metric values |
| **No secrets access** | Can't read vault/secrets | Good! Never share secrets with any LLM |

### When NOT to Use Claude

- **Time-critical decisions under 30 seconds**: Your muscle memory is faster
- **Highly confidential incidents**: Data breach investigation (legal implications)
- **Simple, obvious fixes**: If you know the answer, just do it
- **Compliance-restricted environments**: Check if AI tools are allowed
- **AI-specific security incidents**: Prompt injection detected, MCP compromised, agent exfiltrating data → See [Security Hardening — Response](../security/security-hardening.md#part-3-response-when-things-go-wrong) for dedicated procedures (kill switch architecture, containment levels, incident timelines)

### When Claude Excels

- **Complex root cause analysis**: Multiple interacting systems
- **Documentation generation**: Postmortems, runbooks, procedures
- **Learning new tools**: Unfamiliar cloud services, new k8s features
- **Second opinion**: Validating your hypothesis
- **Bulk operations**: Generating configs for multiple environments

---

# Pattern: Incident Response

**Goal**: Structured workflows for incident management.

## Solo Incident Workflow

**Reality**: At 3 AM, you're alone. This workflow is designed for one person.

### FIRE in Action: Solo Incident

#### F - First Response (30 seconds)

```bash
claude "INCIDENT: [symptom - be specific]
Context: [service], [environment], [time started]
Recent changes: [deploys, infra changes, traffic spikes]
Current impact: [% users affected, revenue impact if known]
What are the 3 most critical things to check first?"
```

**Example**:
```bash
claude "INCIDENT: API returning 500 errors on /checkout endpoint
Context: checkout-service, production-us-east-1, started 5 min ago
Recent changes: deployed v2.3.4 at 2:45 AM, added new payment provider
Current impact: ~30% of checkout requests failing
What are the 3 most critical things to check first?"
```

#### I - Investigate (2-5 minutes)

Run Claude's suggested commands, share output:

```bash
# Claude suggested checking pod health first
kubectl get pods -n checkout | claude "Quick assessment of this pod list"

# Then checking recent logs
kubectl logs -l app=checkout --since=5m | head -100 | claude "Analyze for error patterns"

# Then checking the deployment diff
kubectl rollout history deployment/checkout-service -n checkout | claude "What changed in the last deployment?"
```

**Pro tip**: Keep a terminal for running commands, another for Claude conversation.

#### R - Remediate (with approval)

```bash
claude "Based on investigation:
- Root cause: [your understanding]
- Evidence: [key findings]

Propose remediation options:
1. Quick mitigation (restore service)
2. Proper fix (address root cause)

CONSTRAINT: I need to approve before any action. Show exact commands."
```

**Approval Gate Example**:
```
Claude: "Recommended: Rollback to v2.3.3
Command: kubectl rollout undo deployment/checkout-service -n checkout
Risk: Low - previous version was stable for 2 weeks
Alternative: Scale down the new payment provider feature flag

Which approach do you want to take?"

You: "Proceed with rollback"
```

#### E - Evaluate (post-incident, not during)

```bash
claude "Create incident postmortem:

Timeline:
- 2:45 AM: Deployed v2.3.4
- 3:00 AM: First alerts fired
- 3:05 AM: Incident declared
- 3:12 AM: Root cause identified (nil pointer in new payment provider code)
- 3:15 AM: Rollback initiated
- 3:17 AM: Service restored

Format: Blameless, focus on systems not people
Include: Action items with owners"
```

## Communication During Incidents

### Stakeholder Update Generator

```bash
claude "Generate incident update for stakeholders:

Incident: Checkout service degradation
Current status: Mitigated, monitoring
Impact: 15 minutes of 30% checkout failures
ETA to full resolution: 2 hours (proper fix in next deploy)

Audience: Non-technical executives
Tone: Professional, reassuring, factual
Length: 3 sentences max"
```

**Output Example**:
> We experienced a 15-minute disruption to our checkout service affecting approximately 30% of transactions, which has now been resolved. The issue was caused by a software bug in a recent update and was quickly rolled back. We'll deploy a permanent fix during our next scheduled maintenance window with no expected customer impact.

### Incident Bridge Prompt

For real-time incident channels:

```bash
claude "I'm managing an incident bridge. Help me:
1. Maintain a running timeline of events
2. Suggest next investigation steps when we hit dead ends
3. Draft comms updates every 15 minutes
4. Flag when I should escalate

Current status: [paste latest update]
What should I communicate to the bridge now?"
```

## Multi-Agent Pattern: Post-Incident Analysis

**When to use multi-agent**: Not during active incidents. Use for comprehensive analysis afterward.

```bash
# Agent 1: Timeline Reconstruction
claude "You are an incident timeline analyst.
From these logs and Slack messages, reconstruct a precise timeline:
[paste logs and comms]
Output: Timestamped events, who did what when"

# Agent 2: Root Cause Analysis
claude "You are a root cause analyst.
Given this timeline and system architecture, perform 5-whys analysis:
[paste timeline from Agent 1]
Output: Root cause chain, contributing factors"

# Agent 3: Prevention Recommendations
claude "You are an SRE process improvement specialist.
Given this root cause analysis:
[paste RCA from Agent 2]
Output: Prioritized prevention measures, effort estimates, ownership suggestions"
```

### Case Study: OpsWorker.ai MTTR Reduction

**Context**: SRE team managing 200+ microservices, 5 on-call engineers.

**Before Claude**:
- Average MTTR: 45 minutes
- Postmortems: Often delayed or skipped
- Knowledge silos: Each engineer knew different services

**Claude Integration**:
1. FIRE framework adopted for all incidents
2. Claude generates initial postmortem draft within 1 hour
3. Runbooks augmented with Claude-assisted troubleshooting

**After 3 Months**:
- Average MTTR: 18 minutes (60% reduction)
- Postmortem completion: 95% within 24 hours
- Knowledge sharing: Claude-generated runbooks accessible to all

**Key Insight**: Biggest gains weren't speed—they were consistency and documentation.

---

# Pattern: Infrastructure as Code

**Goal**: Leverage Claude for Terraform, Ansible, and GitOps workflows.

## Terraform with Claude

### Reference: Anton Babenko's Terraform Skill

The most comprehensive Terraform skill for Claude Code:

**Repository**: [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill)
**Author**: Anton Babenko (creator of terraform-aws-modules, 1B+ downloads)

```bash
# Install
cd ~/.claude/skills/
git clone https://github.com/antonbabenko/terraform-skill.git terraform
```

**What it provides**:
- Best practices for module structure
- AWS, GCP, Azure patterns
- State management guidance
- CI/CD integration patterns

### Common Terraform Prompts

#### Plan Review

```bash
terraform plan -out=plan.txt && cat plan.txt | claude "Review this Terraform plan:
1. Any dangerous changes? (data loss, downtime)
2. Are the changes what we expect?
3. Any missing changes we should add?
4. Cost implications if visible"
```

#### Module Generation

```bash
claude "Generate a Terraform module for:
- AWS ECS Fargate service
- With ALB and target group
- Auto-scaling based on CPU
- Secrets from SSM Parameter Store

Follow these conventions:
- Use for_each over count
- All resources tagged with var.tags
- Output the service URL and ARN"
```

#### State Surgery Helper

```bash
claude "I need to move a resource to a different state file:
Current state: terraform-prod/terraform.tfstate
Resource: aws_s3_bucket.logs
Target state: terraform-shared/terraform.tfstate

What's the safest procedure? Include rollback steps."
```

### Drift Detection Workflow

```bash
# Detect drift
terraform plan -detailed-exitcode 2>&1 | tee drift.txt

# Analyze with Claude
cat drift.txt | claude "Analyze this Terraform drift:
1. What changed outside of Terraform?
2. Is this drift expected (manual change) or concerning?
3. Should we import the changes or revert to Terraform state?
4. What's the safest remediation path?"
```

## Ansible with Claude

### Playbook Review

```bash
cat playbook.yml | claude "Review this Ansible playbook:
1. Idempotency issues?
2. Security concerns?
3. Error handling gaps?
4. Performance optimizations?"
```

### Role Generation

```bash
claude "Generate an Ansible role for:
- Installing and configuring Nginx
- SSL certificates via Let's Encrypt (certbot)
- Hardened configuration (disable server tokens, etc.)
- Log rotation

Follow best practices:
- Use handlers for service restarts
- Variables in defaults/main.yml
- Include molecule tests structure"
```

## GitOps with Claude

### ArgoCD Application Review

```bash
cat application.yaml | claude "Review this ArgoCD Application:
1. Sync policy appropriate for the environment?
2. Resource health checks defined?
3. Any sync wave ordering issues?
4. Namespace and project permissions correct?"
```

### Helm Values Generation

```bash
claude "Generate Helm values for deploying [application] to:
- Environment: staging
- Resources: Limited (cost-conscious)
- Replicas: 2
- Ingress: Internal only
- Secrets: From external-secrets operator

Base chart: [chart name]
Include comments explaining each value"
```

## Security Review Automation

### Infrastructure Security Scan

```bash
# Run tfsec or checkov, analyze results
tfsec . --format=json | claude "Analyze these security findings:
1. Prioritize by severity and exploitability
2. Which are false positives in our context?
3. For real issues: what's the fix?
4. Which can we ignore with a documented reason?"
```

### IAM Policy Review

```bash
cat iam-policy.json | claude "Review this IAM policy:
1. Does it follow least privilege?
2. Any overly permissive actions? (*, admin, etc.)
3. Resource constraints appropriate?
4. Suggest a more restrictive version that still works"
```

---

# Guardrails & Adoption

**Goal**: Implement Claude Code safely and get team buy-in.

## Cost Awareness

### Claude Code Costs

| Model | Input (1M tokens) | Output (1M tokens) |
|-------|-------------------|-------------------|
| Sonnet 4 | $3 | $15 |
| Opus 4 | $15 | $75 |

**Typical DevOps session**: 20K-50K tokens = $0.10-$0.50

**Cost control strategies**:
1. Use Sonnet for routine tasks (default)
2. Reserve Opus for complex multi-system analysis
3. Use `/compact` to reduce context when conversation gets long
4. Avoid pasting entire log files; grep relevant sections first

### Infrastructure Costs from Claude Suggestions

**Beware**: Claude doesn't see your cloud bill. Always ask:

```bash
claude "Before I apply these changes, estimate:
1. Monthly cost impact (compute, storage, network)
2. Any resources that could scale unbounded?
3. Cost optimization alternatives?"
```

## Security Boundaries

### Never Share with Claude

| Data Type | Why Not | Alternative |
|-----------|---------|-------------|
| API keys, tokens | Could be cached/logged | Use placeholders: `<API_KEY>` |
| Production secrets | Security risk | Describe the secret type, not value |
| Customer PII | Privacy/compliance | Use anonymized examples |
| Proprietary algorithms | IP protection | Describe behavior, not code |
| Incident details with PII | Legal liability | Sanitize before sharing |

### Safe Prompting Template

```bash
claude "Debug this authentication issue:
- Service: auth-service
- Error: 401 Unauthorized for valid tokens
- Environment: staging (not production)
- Token format: JWT with claims [user_id, org_id, exp]
- NOTE: I've redacted all actual token values

Here's the sanitized log:
[paste log with secrets replaced]"
```

### Approval Gates for Production

Always require human approval for:

```yaml
# Example: Production change checklist
approval_required:
  - kubectl delete
  - kubectl scale (down)
  - terraform destroy
  - DROP TABLE / DELETE FROM
  - rm -rf (outside tmp directories)
  - Any production database write
  - Any IAM policy change
  - Any security group modification
```

## Team Rollout Checklist

### Phase 1: Pilot (1-2 engineers, 2 weeks)

- [ ] Install Claude Code for pilot users
- [ ] Create team CLAUDE.md with common context
- [ ] Document first 5 successful use cases
- [ ] Identify one workflow to standardize
- [ ] Track time saved (before/after)

### Phase 2: Expand (Team, 4 weeks)

- [ ] Share pilot learnings in team meeting
- [ ] Create team-specific prompts library
- [ ] Establish security guidelines (what to share/not share)
- [ ] Set up shared skills/commands repository
- [ ] Define when to use Claude vs when not to

### Phase 3: Optimize (Ongoing)

- [ ] Monthly review of prompt library
- [ ] A/B test: Claude-assisted vs traditional for similar incidents
- [ ] Contribute back to community (awesome-lists, this guide)
- [ ] Track MTTR, postmortem completion, documentation quality

### Adoption Pitfalls to Avoid

| Pitfall | Why It Happens | Prevention |
|---------|---------------|------------|
| **Over-reliance** | Claude is so helpful | Mandate learning time, not just output |
| **Blind trust** | Commands usually work | Always review before running |
| **Context dumping** | Hope Claude figures it out | Provide focused context, not everything |
| **Skipping verification** | Time pressure | Build verification into workflow |
| **Shadow usage** | No team visibility | Share wins, normalize usage |

---

# Quick Reference

## FIRE Framework Summary

```
┌─────────────────────────────────────────────────────────────┐
│ F - FIRST RESPONSE                                          │
│   "INCIDENT: [symptom]. Context: [service, env, time].      │
│    Recent changes: [what]. Impact: [who affected].          │
│    What are the 3 most critical things to check?"           │
├─────────────────────────────────────────────────────────────┤
│ I - INVESTIGATE                                             │
│   Run Claude's suggested commands                           │
│   Share output: "[output] | claude 'Analyze this'"          │
│   Iterate until root cause identified                       │
├─────────────────────────────────────────────────────────────┤
│ R - REMEDIATE                                               │
│   "Based on [findings], propose remediation.                │
│    CONSTRAINT: I need to approve before any action."        │
│   APPROVE → Execute │ REJECT → More investigation           │
├─────────────────────────────────────────────────────────────┤
│ E - EVALUATE                                                │
│   "Create postmortem: Timeline, root cause, prevention.     │
│    Format: Blameless, action items with owners."            │
└─────────────────────────────────────────────────────────────┘
```

## Prompts by Symptom

### Kubernetes

| Symptom | Prompt |
|---------|--------|
| CrashLoopBackOff | `kubectl describe pod <pod> -n <ns> \| claude "Exit code meaning? 3 likely causes? Commands to investigate?"` |
| OOMKilled | `kubectl top pods && describe pod \| claude "Leak or under-provisioned? Optimal resources?"` |
| ImagePullBackOff | `kubectl describe pod \| claude "Auth, network, or wrong image? Verification commands?"` |
| Pending | `kubectl describe pod && describe nodes \| claude "Resource, selector, or affinity issue?"` |
| Service unreachable | `kubectl get svc,endpoints \| claude "Healthy endpoints? Selector matching? Network policy?"` |

### Cloud/Infrastructure

| Symptom | Prompt |
|---------|--------|
| High latency | `[metrics] \| claude "Bottleneck location? Is it compute, network, or dependency?"` |
| Disk full | `df -h && du -sh /* \| claude "What's consuming space? Safe to delete?"` |
| Connection refused | `netstat -tlnp \| claude "Service listening? Port correct? Firewall rules?"` |
| SSL cert expiry | `openssl s_client -connect host:443 \| claude "Days until expiry? Renewal steps?"` |
| DNS issues | `dig +trace domain \| claude "Where does resolution fail?"` |

### Terraform

| Task | Prompt |
|------|--------|
| Plan review | `terraform plan \| claude "Dangerous changes? Missing changes? Cost impact?"` |
| Drift analysis | `terraform plan -detailed-exitcode \| claude "What drifted? Expected? Remediation?"` |
| Module request | `claude "Generate Terraform module for [resource] with [requirements]"` |

## MCP Servers for DevOps

| Server | Purpose | Install |
|--------|---------|---------|
| Kubernetes | Direct cluster access | `npx -y @anthropic/mcp-kubernetes` |
| AWS | AWS API access | `npx -y @anthropic/mcp-aws` |
| GCP | GCP API access | `npx -y @anthropic/mcp-gcp` |
| Prometheus | Direct metrics queries | Community: search awesome-mcp-servers |
| Terraform | State/plan analysis | Community: search awesome-mcp-servers |

**Config location**: `~/.claude.json` (field `"mcpServers"`)

```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-kubernetes"]
    }
  }
}
```

## External Resources

### Awesome Lists

- **[awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)** (8.1k stars): Agent personas including SRE
- **[awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)** (4.6k stars): Skills including infra-related

### Official Resources

- **[terraform-skill](https://github.com/antonbabenko/terraform-skill)**: Production-grade Terraform skill by Anton Babenko
- **[Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)**: Official documentation

### Community

- **Anthropic Discord**: #claude-code channel
- **Reddit**: r/ClaudeAI
- **GitHub**: Open issues on awesome-lists for feature requests

---

## See Also

- **[Agent Template](../examples/agents/devops-sre.md)**: DevOps/SRE agent persona for Claude
- **[CLAUDE.md Template](../examples/claude-md/devops-sre.md)**: Project configuration for DevOps teams
- **[Security Hardening Guide](../security/security-hardening.md)**: Additional security practices
- **[Architecture Guide](../core/architecture.md)**: How Claude Code works internally

---

*Contributions welcome! If you have DevOps prompts that work well, consider adding them to the awesome-lists or submitting a PR to this guide.*
