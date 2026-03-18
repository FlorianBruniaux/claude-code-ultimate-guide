---
title: "Claude Code Examples"
description: "Annotated templates teaching why patterns work, with trade-offs and alternatives"
tags: [template, reference, workflows, architecture]
---

# Claude Code Examples

Annotated templates that teach you **why** patterns work, not just how to configure them. Each template includes comments explaining trade-offs, alternatives, and when to deviate.

> **[Browse Interactive Catalog](./index.html)** — View, copy, and download all templates with syntax highlighting

## Structure

| Folder | Description | Count |
|--------|-------------|-------|
| [`agents/`](./agents/) | Custom AI personas for specialized tasks | 14 + 2 collections |
| [`commands/`](./commands/) | Slash commands (workflow automation) | 31 |
| [`hooks/`](./hooks/) | Event-driven security & automation scripts | 34 |
| [`skills/`](./skills/) | Reusable knowledge modules — [9 on SkillHub](https://skills.palebluedot.live/owner/FlorianBruniaux) | 17 |
| [`claude-md/`](./claude-md/) | CLAUDE.md configuration profiles | 7 |
| [`config/`](./config/) | Settings, MCP, git templates | 8 |
| [`memory/`](./memory/) | CLAUDE.md memory file templates | 2 |
| [`rules/`](./rules/) | Behavioral rules for common review patterns | 5 |
| [`scripts/`](./scripts/) | Diagnostic & utility scripts | 16 |
| [`team-config/`](./team-config/) | Team onboarding templates | 3 |
| [`templates/`](./templates/) | Session and workflow templates | 1 |
| [`github-actions/`](./github-actions/) | CI/CD workflows | 4 |
| [`workflows/`](./workflows/) | Advanced development workflows | 3 |
| [`plugins/`](./plugins/) | Community plugins (SE-CoVe, claude-mem) | 2 |
| [`integrations/`](./integrations/) | External tool integrations (Agent Vibes TTS) | 1 |
| [`mcp-configs/`](./mcp-configs/) | MCP server configurations | 1 |
| [`modes/`](./modes/) | Behavioral modes (SuperClaude) | 1 |
| [`semantic-anchors/`](./semantic-anchors/) | Precise vocabulary for better LLM outputs | 1 |
| [`multi-provider/`](./multi-provider/) | Multi-provider bridge → [dedicated repo](https://github.com/FlorianBruniaux/cc-copilot-bridge) | — |

## Quick Start

1. Copy the template you need
2. Customize for your project
3. Place in the correct location (see paths below)

## File Locations

| Type | Project Location | Global Location |
|------|------------------|-----------------|
| Agents | `.claude/agents/` | `~/.claude/agents/` |
| Skills | `.claude/skills/` | `~/.claude/skills/` |
| Commands | `.claude/commands/` | `~/.claude/commands/` |
| Hooks | `.claude/hooks/` | `~/.claude/hooks/` |
| Config | `.claude/` | `~/.claude/` |
| Memory | `./CLAUDE.md` or `.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| Modes | — | `~/.claude/MODE_*.md` |

> **Windows**: Replace `~/.claude/` with `%USERPROFILE%\.claude\`

## Templates Index

### Agents (16)

| File | Purpose | Model |
|------|---------|-------|
| [code-reviewer.md](./agents/code-reviewer.md) | Thorough code review | Sonnet |
| [test-writer.md](./agents/test-writer.md) | TDD/BDD test generation | Sonnet |
| [security-auditor.md](./agents/security-auditor.md) | Security vulnerability detection | Sonnet |
| [refactoring-specialist.md](./agents/refactoring-specialist.md) | Clean code refactoring | Sonnet |
| [output-evaluator.md](./agents/output-evaluator.md) | LLM-as-a-Judge quality gate | Haiku |
| [devops-sre.md](./agents/devops-sre.md) | Infrastructure troubleshooting with FIRE framework | Sonnet |
| [planner.md](./agents/planner.md) | Strategic planning — read-only, before implementation | Opus |
| [implementer.md](./agents/implementer.md) | Mechanical execution — bounded scope | Haiku |
| [architecture-reviewer.md](./agents/architecture-reviewer.md) | Architecture & design review — read-only | Opus |
| [adr-writer.md](./agents/adr-writer.md) | Architecture Decision Record generator — read-only | Opus |
| [integration-reviewer.md](./agents/integration-reviewer.md) | Runtime integration validator — read-only | Sonnet |
| [plan-challenger.md](./agents/plan-challenger.md) | Adversarial plan review across 5 dimensions — read-only | Sonnet |
| [planning-coordinator.md](./agents/planning-coordinator.md) | Synthesis agent for dynamic research teams — read-only | Sonnet |
| [security-patcher.md](./agents/security-patcher.md) | Apply security patches from audit findings — proposes for review | Sonnet |
| [analytics-with-eval/](./agents/analytics-with-eval/) | Collection: analytics agent + evaluation hooks | — |
| [cyber-defense/](./agents/cyber-defense/) | Collection: anomaly detector, log ingestor, risk classifier, threat reporter | — |

### Skills (17) — [9 on SkillHub](https://skills.palebluedot.live/owner/FlorianBruniaux)

| File | Purpose |
|------|---------|
| [design-patterns/](./skills/design-patterns/) | Detect and analyze GoF design patterns with stack-aware suggestions |
| [tdd-workflow.md](./skills/tdd-workflow.md) | Test-Driven Development process |
| [security-checklist.md](./skills/security-checklist.md) | OWASP Top 10 security checks |
| [pdf-generator.md](./skills/pdf-generator.md) | Professional PDF generation (Quarto/Typst) |
| [voice-refine/](./skills/voice-refine/) | Writing voice refinement with before/after examples |
| [ast-grep-patterns.md](./skills/ast-grep-patterns.md) | AST-based code search patterns |
| [rtk-optimizer/](./skills/rtk-optimizer/) | RTK token optimization analysis |
| [audit-agents-skills/](./skills/audit-agents-skills/) | Quality audit for agents, skills, and commands |
| [skill-creator/](./skills/skill-creator/) | Create new skills with proper structure and best practices |
| [landing-page-generator/](./skills/landing-page-generator/) | Generate deploy-ready landing pages from any repository |
| [ccboard/](./skills/ccboard/) | Comprehensive TUI/Web dashboard for Claude Code monitoring |
| [guide-recap/](./skills/guide-recap/) | Transform CHANGELOG entries into social content (LinkedIn, Twitter/X, Slack) |
| [release-notes-generator/](./skills/release-notes-generator/) | Generate release notes in 3 formats from git commits |
| [pr-triage/](./skills/pr-triage/) | 4-phase PR backlog management (audit, deep review, validated comments, worktree setup) |
| [issue-triage/](./skills/issue-triage/) | 3-phase issue backlog management (audit, deep analysis, validated actions) |
| [cyber-defense-team/](./skills/cyber-defense-team/) | Multi-agent cyber defense team orchestration |
| [talk-pipeline/](./skills/talk-pipeline/) | 6-stage pipeline: raw material to slides via Kimi |

### Commands (31)

| File | Trigger | Purpose |
|------|---------|---------|
| [commit.md](./commands/commit.md) | `/commit` | Conventional commit messages |
| [pr.md](./commands/pr.md) | `/pr` | Create well-structured PRs with scope analysis |
| [review-pr.md](./commands/review-pr.md) | `/review-pr` | PR review workflow |
| [release-notes.md](./commands/release-notes.md) | `/release-notes` | Generate release notes in 3 formats |
| [sonarqube.md](./commands/sonarqube.md) | `/sonarqube` | Analyze SonarCloud quality issues for PRs |
| [generate-tests.md](./commands/generate-tests.md) | `/generate-tests` | Test generation |
| [git-worktree.md](./commands/git-worktree.md) | `/git-worktree` | Isolated git worktree setup |
| [git-worktree-status.md](./commands/git-worktree-status.md) | `/git-worktree-status` | Check worktree background verification tasks |
| [git-worktree-remove.md](./commands/git-worktree-remove.md) | `/git-worktree-remove` | Safe worktree removal with merge checks |
| [git-worktree-clean.md](./commands/git-worktree-clean.md) | `/git-worktree-clean` | Batch cleanup of stale worktrees |
| [diagnose.md](./commands/diagnose.md) | `/diagnose` | Interactive troubleshooting assistant (FR/EN) |
| [validate-changes.md](./commands/validate-changes.md) | `/validate-changes` | LLM-as-a-Judge pre-commit validation |
| [catchup.md](./commands/catchup.md) | `/catchup` | Restore context after /clear |
| [security.md](./commands/security.md) | `/security` | Quick OWASP security audit |
| [security-check.md](./commands/security-check.md) | `/security-check` | Config scan vs known threats (~30s) |
| [security-audit.md](./commands/security-audit.md) | `/security-audit` | Full 6-phase audit with score /100 |
| [update-threat-db.md](./commands/update-threat-db.md) | `/update-threat-db` | Research & update threat intelligence |
| [audit-agents-skills.md](./commands/audit-agents-skills.md) | `/audit-agents-skills` | Quality audit for .claude/ config |
| [sandbox-status.md](./commands/sandbox-status.md) | `/sandbox-status` | Sandbox isolation status check |
| [refactor.md](./commands/refactor.md) | `/refactor` | SOLID-based code improvements |
| [explain.md](./commands/explain.md) | `/explain` | Code explanations (3 depth levels) |
| [optimize.md](./commands/optimize.md) | `/optimize` | Performance analysis and roadmap |
| [ship.md](./commands/ship.md) | `/ship` | Pre-deploy checklist |
| [learn/quiz.md](./commands/learn/quiz.md) | `/learn:quiz` | Self-testing for learning concepts |
| [learn/teach.md](./commands/learn/teach.md) | `/learn:teach` | Step-by-step concept explanations |
| [learn/alternatives.md](./commands/learn/alternatives.md) | `/learn:alternatives` | Compare different approaches |
| [audit-codebase.md](./commands/audit-codebase.md) | `/audit-codebase` | Codebase health audit scoring 7 categories |
| [plan-start.md](./commands/plan-start.md) | `/plan-start` | 5-phase planning: PRD analysis, design review, technical decisions, research team, metrics |
| [plan-execute.md](./commands/plan-execute.md) | `/plan-execute` | Execute validated plan: worktree isolation, TDD scaffolding, parallel agents, PR creation |
| [plan-validate.md](./commands/plan-validate.md) | `/plan-validate` | 2-layer plan validation: structural checks + specialist agents, auto-fix issues |
| [review-plan.md](./commands/review-plan.md) | `/review-plan` | Structured plan review across 4 axes before writing code |

### Hooks (34)

Security-first: 12 security hooks, 8 productivity hooks, 5 automation hooks, 5 monitoring hooks.

**Security Hooks** (13 bash):

| File | Event | Purpose |
|------|-------|---------|
| [dangerous-actions-blocker.sh](./hooks/bash/dangerous-actions-blocker.sh) | PreToolUse | Block `rm -rf`, force-push, production ops |
| [prompt-injection-detector.sh](./hooks/bash/prompt-injection-detector.sh) | PreToolUse | Detect injection patterns in prompts |
| [unicode-injection-scanner.sh](./hooks/bash/unicode-injection-scanner.sh) | PreToolUse | Detect zero-width, RTL override, ANSI escape |
| [repo-integrity-scanner.sh](./hooks/bash/repo-integrity-scanner.sh) | PreToolUse | Scan README/package.json for hidden injection |
| [security-check.sh](./hooks/bash/security-check.sh) | PreToolUse | Block secrets in commands |
| [sandbox-validation.sh](./hooks/bash/sandbox-validation.sh) | PreToolUse | Validate sandbox isolation |
| [file-guard.sh](./hooks/bash/file-guard.sh) | PreToolUse | Protect sensitive files from modification |
| [permission-request.sh](./hooks/bash/permission-request.sh) | PreToolUse | Explicit permission flow for risky ops |
| [mcp-config-integrity.sh](./hooks/bash/mcp-config-integrity.sh) | SessionStart | Verify MCP config hash (CVE protection) |
| [claudemd-scanner.sh](./hooks/bash/claudemd-scanner.sh) | SessionStart | Detect CLAUDE.md injection attacks |
| [output-secrets-scanner.sh](./hooks/bash/output-secrets-scanner.sh) | PostToolUse | Prevent API keys/tokens in Claude responses |
| [pre-commit-secrets.sh](./hooks/bash/pre-commit-secrets.sh) | Git hook | Block secrets from entering commits |
| [security-gate.sh](./hooks/bash/security-gate.sh) | PreToolUse | Detect vulnerable code patterns before writing to source files |

**Productivity Hooks** (10):

| File | Event | Purpose |
|------|-------|---------|
| [auto-format.sh](./hooks/bash/auto-format.sh) | PostToolUse | Auto-format after edits (Prettier, Black, go fmt) |
| [auto-checkpoint.sh](./hooks/bash/auto-checkpoint.sh) | PostToolUse | Auto-checkpoint work at intervals |
| [typecheck-on-save.sh](./hooks/bash/typecheck-on-save.sh) | PostToolUse | Run TypeScript checks on save |
| [test-on-change.sh](./hooks/bash/test-on-change.sh) | PostToolUse | Run tests on file changes |
| [rtk-auto-wrapper.sh](./hooks/bash/rtk-auto-wrapper.sh) | PreToolUse | Auto-wrap commands with RTK for token savings |
| [rtk-baseline.sh](./hooks/bash/rtk-baseline.sh) | SessionStart | Save RTK baseline for session savings tracking |
| [setup-init.sh](./hooks/bash/setup-init.sh) | SessionStart | Initialize session environment |
| [subagent-stop.sh](./hooks/bash/subagent-stop.sh) | Stop | Clean up sub-agent resources |
| [auto-rename-session.sh](./hooks/bash/auto-rename-session.sh) | SessionEnd | AI-powered session title generation (Haiku) |
| [velocity-governor.sh](./hooks/bash/velocity-governor.sh) | PreToolUse | Rate-limit tool calls to avoid API throttling |

**Monitoring Hooks** (6):

| File | Event | Purpose |
|------|-------|---------|
| [output-validator.sh](./hooks/bash/output-validator.sh) | PostToolUse | Heuristic output validation |
| [session-logger.sh](./hooks/bash/session-logger.sh) | PostToolUse | Log operations for monitoring |
| [session-summary.sh](./hooks/bash/session-summary.sh) | SessionEnd | Display session stats (duration, tools, cost, RTK savings) |
| [session-summary-config.sh](./hooks/bash/session-summary-config.sh) | CLI tool | Configure session-summary sections and display |
| [learning-capture.sh](./hooks/bash/learning-capture.sh) | Stop | Prompt for daily learning capture |
| [privacy-warning.sh](./hooks/bash/privacy-warning.sh) | PostToolUse | Warn on potential privacy leaks |

**Notification & TTS** (3):

| File | Event | Purpose |
|------|-------|---------|
| [notification.sh](./hooks/bash/notification.sh) | Notification | Contextual macOS sound alerts |
| [tts-selective.sh](./hooks/bash/tts-selective.sh) | PostToolUse | Text-to-speech for selected outputs |
| [pre-commit-evaluator.sh](./hooks/bash/pre-commit-evaluator.sh) | Git hook | LLM-as-a-Judge pre-commit |

**PowerShell** (2):

| File | Event | Purpose |
|------|-------|---------|
| [security-check.ps1](./hooks/powershell/security-check.ps1) | PreToolUse | Block secrets in commands |
| [auto-format.ps1](./hooks/powershell/auto-format.ps1) | PostToolUse | Auto-format after edits |

> **See [hooks/README.md](./hooks/README.md) for full documentation, configuration examples, and security hardening patterns**

### Config (8)

| File | Purpose |
|------|---------|
| [settings.json](./config/settings.json) | Hooks configuration |
| [mcp.json](./config/mcp.json) | MCP servers setup |
| [.gitignore-claude](./config/.gitignore-claude) | Git ignore patterns |
| [CONTRIBUTING-ai-disclosure.md](./config/CONTRIBUTING-ai-disclosure.md) | AI disclosure template for CONTRIBUTING.md |
| [PULL_REQUEST_TEMPLATE-ai.md](./config/PULL_REQUEST_TEMPLATE-ai.md) | PR template with AI attribution |
| [sandbox-native.json](./config/sandbox-native.json) | Native Claude Code sandbox configuration |
| [settings-personalization.json](./config/settings-personalization.json) | UI personalization: spinner verbs, custom tips carousel |
| [settings.local.json.example](./config/settings.local.json.example) | Local overrides example (gitignored) |

### Memory (2)

| File | Purpose |
|------|---------|
| [CLAUDE.md.project-template](./memory/CLAUDE.md.project-template) | Team project memory |
| [CLAUDE.md.personal-template](./memory/CLAUDE.md.personal-template) | Personal global memory |

### CLAUDE.md Configurations (7)

| File | Purpose |
|------|---------|
| [learning-mode.md](./claude-md/learning-mode.md) | Learning-focused development configuration |
| [devops-sre.md](./claude-md/devops-sre.md) | DevOps/SRE project configuration |
| [product-designer.md](./claude-md/product-designer.md) | Product designer workflow configuration |
| [tts-enabled.md](./claude-md/tts-enabled.md) | Text-to-speech enabled configuration |
| [rtk-optimized.md](./claude-md/rtk-optimized.md) | RTK token-optimized configuration |
| [session-naming.md](./claude-md/session-naming.md) | Auto-rename sessions with descriptive titles for parallel work |
| [design-reference-file.md](./claude-md/design-reference-file.md) | Brand-book and UI kit context for consistent UI generation |

> **See [guide/learning-with-ai.md](../guide/learning-with-ai.md) for learning mode documentation**
> **See [guide/devops-sre.md](../guide/devops-sre.md) for DevOps/SRE guide**

### Scripts (16)

| File | Purpose | Output |
|------|---------|--------|
| [audit-scan.sh](./scripts/audit-scan.sh) | Fast setup audit scanner | JSON / Human |
| [check-claude.sh](./scripts/check-claude.sh) | Health check diagnostics (macOS/Linux) | Human |
| [check-claude.ps1](./scripts/check-claude.ps1) | Health check diagnostics (Windows) | Human |
| [clean-reinstall-claude.sh](./scripts/clean-reinstall-claude.sh) | Clean reinstall procedure (macOS/Linux) | Human |
| [clean-reinstall-claude.ps1](./scripts/clean-reinstall-claude.ps1) | Clean reinstall procedure (Windows) | Human |
| [session-stats.sh](./scripts/session-stats.sh) | Analyze session logs & costs | JSON / Human |
| [session-search.sh](./scripts/session-search.sh) | Fast session search & resume | Human |
| [cc-sessions.py](./scripts/cc-sessions.py) | Advanced session search with incremental indexing | Human |
| [fresh-context-loop.sh](./scripts/fresh-context-loop.sh) | Auto-restart sessions at context limits | Human |
| [bridge.py](./scripts/bridge.py) | Plan bridging between sessions | JSON |
| [bridge-plan-schema.json](./scripts/bridge-plan-schema.json) | JSON Schema for bridge plan v1 format | — |
| [migrate-arguments-syntax.sh](./scripts/migrate-arguments-syntax.sh) | Migrate v1 → v2 argument syntax (bash) | Human |
| [migrate-arguments-syntax.ps1](./scripts/migrate-arguments-syntax.ps1) | Migrate v1 → v2 argument syntax (PowerShell) | Human |
| [rtk-benchmark.sh](./scripts/rtk-benchmark.sh) | Benchmark RTK token savings | Human |
| [sync-claude-config.sh](./scripts/sync-claude-config.sh) | Sync Claude config across machines | Human |
| [sonnetplan.sh](./scripts/sonnetplan.sh) | Alias to run Claude with Sonnet instead of Opus (cost optimization) | Human |

> **See [scripts/README.md](./scripts/README.md) for detailed usage**

### Rules (5)

| File | Purpose |
|------|---------|
| [architecture-review.md](./rules/architecture-review.md) | Rules for architecture review sessions |
| [code-quality-review.md](./rules/code-quality-review.md) | Rules for code quality review sessions |
| [first-principles.md](./rules/first-principles.md) | First-principles reasoning rules |
| [performance-review.md](./rules/performance-review.md) | Rules for performance review sessions |
| [test-review.md](./rules/test-review.md) | Rules for test review sessions |

### Team Config (3)

| File | Purpose |
|------|---------|
| [claude-skeleton.md](./team-config/claude-skeleton.md) | Minimal CLAUDE.md skeleton for new team members |
| [profile-template.yaml](./team-config/profile-template.yaml) | Profile assembly template for multi-tool teams |
| [sync-script.ts](./team-config/sync-script.ts) | Sync Claude config across team machines |

### Templates (1)

| File | Purpose |
|------|---------|
| [session-handoff-lorenz.md](./templates/session-handoff-lorenz.md) | Session handoff template for context continuity |

### GitHub Actions (4)

| File | Trigger | Purpose |
|------|---------|---------|
| [claude-code-review.yml](./github-actions/claude-code-review.yml) ⭐ | PR open/sync + `/claude-review` comment | Prompt-based review (externalized prompt + anti-hallucination protocol) |
| [claude-pr-auto-review.yml](./github-actions/claude-pr-auto-review.yml) | PR open/update | Auto code review with inline comments |
| [claude-security-review.yml](./github-actions/claude-security-review.yml) | PR open/update | Security-focused scan (OWASP) |
| [claude-issue-triage.yml](./github-actions/claude-issue-triage.yml) | Issue opened | Auto-triage with labels and severity |

> **See [github-actions/README.md](./github-actions/README.md) for setup instructions and customization**

### Workflows (3)

| File | Purpose |
|------|---------|
| [database-branch-setup.md](./workflows/database-branch-setup.md) | Isolated feature dev with database branches (Neon/PlanetScale) |
| [memory-stack-integration.md](./workflows/memory-stack-integration.md) | Multi-day workflow with memory tools (claude-mem + Serena + grepai) |
| [remotion-quickstart.md](./workflows/remotion-quickstart.md) | Video generation workflow with Remotion |

### Plugins (2)

| File | Purpose |
|------|---------|
| [se-cove.md](./plugins/se-cove.md) | Chain-of-Verification for independent code review (Meta AI, ACL 2024) |
| [claude-mem.md](./plugins/claude-mem.md) | Persistent memory management plugin |

### Integrations (1)

| Tool | Purpose |
|------|---------|
| [Agent Vibes TTS](./integrations/agent-vibes/) | Text-to-speech narration for Claude Code responses |

> **See [agent-vibes/README.md](./integrations/agent-vibes/README.md) for installation and voice catalog**

### MCP Configs (1)

| File | Purpose |
|------|---------|
| [figma.json](./mcp-configs/figma.json) | Figma MCP server configuration |

### Modes (1)

| File | Purpose | Activation |
|------|---------|------------|
| [MODE_Learning.md](./modes/MODE_Learning.md) | Just-in-time explanations | `--learn` flag |

> **See [modes/README.md](./modes/README.md) for installation and SuperClaude framework reference**

### Semantic Anchors (1)

| File | Purpose |
|------|---------|
| [anchor-catalog.md](./semantic-anchors/anchor-catalog.md) | Comprehensive catalog of precise technical terms for prompting |

> **See [Section 2.7](../guide/ultimate-guide.md#27-semantic-anchors) in the guide for how to use semantic anchors**

### Multi-Provider Bridge

| Tool | Purpose |
|------|---------|
| [cc-copilot-bridge](./multi-provider/) | Bridge GitHub Copilot to Claude Code CLI for flat-rate access |

> Moved to dedicated repository: [github.com/FlorianBruniaux/cc-copilot-bridge](https://github.com/FlorianBruniaux/cc-copilot-bridge)

---

*See the [main guide](../guide/ultimate-guide.md) for detailed explanations, or the [architecture guide](../guide/architecture.md) for how Claude Code works internally.*
