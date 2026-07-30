# Template Catalog

Auto-generated template index with complexity, time, and domain filters.

**Last updated**: [auto-generated]

---

**Total Templates**: 181

- **Agents**: 23
- **Commands**: 52
- **Skills**: 64
- **Hooks**: 37
- **Workflows**: 3
- **Scripts**: 2

## Filter by Complexity

- **Beginner**: 0 templates
- **Intermediate**: 181 templates
- **Advanced**: 0 templates

## Filter by Time

- **30 min**: 181 templates

---

## By Category

### Agents (23)

- **[adr-writer](agents/adr-writer.md)** *intermediate* • 30 min
  Architecture Decision Record generator agent — read-only. Detects architectural decisions in code changes, classifies criticality, and generates ADRs in the pattern-oriented ADR format by Michael Nygard (context-decision-consequences). Never modifies code. Use after significant changes or when a decision needs documenting.

- **[analytics-agent](agents/analytics-with-eval/analytics-agent.md)** *intermediate* • 30 min
  SQL query generator with built-in evaluation and safety checks

- **[anomaly-detector](agents/cyber-defense/anomaly-detector.md)** *intermediate* • 30 min
  Detect statistical anomalies and attack patterns from structured security events. Second stage of the cyber defense pipeline — reads cyber-defense-events.json and produces anomalies.

- **[architecture-reviewer](agents/architecture-reviewer.md)** *intermediate* • 30 min
  Architecture and design review agent — read-only. Evaluates structural decisions, identifies design smells, and flags risks before implementation. Never modifies code. Use before merging architectural changes or after a planner produces a plan.

- **[code-reviewer](agents/code-reviewer.md)** *intermediate* • 30 min
  Use for thorough code review with quality, security, and performance checks

- **[devops-sre](agents/devops-sre.md)** *intermediate* • 30 min
  Infrastructure troubleshooting using the FIRE framework (First Response, Investigate, Remediate, Evaluate)

- **[implementer](agents/implementer.md)** *intermediate* • 30 min
  Mechanical execution agent for bounded, well-defined tasks. Scope and approach must be explicit in the task prompt. Use after a planner has produced a plan. For complex logic or design decisions, use Sonnet instead.

- **[integration-reviewer](agents/integration-reviewer.md)** *intermediate* • 30 min
  Runtime integration validator — read-only. Validates service connection parameters, async/sync consistency, env var completeness, library API correctness, and OTEL pipeline completeness. Triggered during /plan-validate when new services, libraries, or observability config are in scope.

- **[log-ingestor](agents/cyber-defense/log-ingestor.md)** *intermediate* • 30 min
  Parse raw logs into structured security events. First stage of the cyber defense pipeline — reads log files and extracts typed events (errors, warnings, auth failures, anomalies).

- **[loop-monitor](agents/loop-monitor.md)** *intermediate* • 30 min
  Autonomous loop monitor — detects stalls, token runaway, and infinite loops in long-running unattended Claude sessions. Use alongside a watchdog process when running autonomous pipelines.

- **[output-evaluator](agents/output-evaluator.md)** *intermediate* • 30 min
  Evaluate Claude Code outputs for quality before commit/action (LLM-as-a-Judge pattern)

- **[plan-challenger](agents/plan-challenger.md)** *intermediate* • 30 min
  Adversarial plan review agent — read-only. Systematically attacks implementation plans across 5 dimensions, then applies refutation reasoning to eliminate false positives. Never modifies code. Use before committing to any significant implementation plan.

- **[planner](agents/planner.md)** *intermediate* • 30 min
  Strategic planning agent — read-only exploration before implementation. Use to decompose tasks, analyze codebases, and produce a detailed plan. Never modifies files.

- **[planning-coordinator](agents/planning-coordinator.md)** *intermediate* • 30 min
  Synthesis agent for dynamic research teams — read-only. Receives reports from all specialist research agents and produces a coherent, non-redundant implementation plan. Spawned automatically when 2+ agents are selected in /plan-start Phase 4.

- **[README](agents/cyber-defense/README.md)** *intermediate* • 30 min
  A 4-agent pipeline that detects security threats in log files. Built natively with Claude Code Agent

- **[README](agents/analytics-with-eval/README.md)** *intermediate* • 30 min
  Production-ready analytics agent with automated metrics collection and safety validation

- **[refactoring-specialist](agents/refactoring-specialist.md)** *intermediate* • 30 min
  Use for clean code refactoring following SOLID principles and best practices

- **[report-template](agents/analytics-with-eval/eval/report-template.md)** *intermediate* • 30 min
  Monthly evaluation template for scoring analytics agent performance and accuracy

- **[risk-classifier](agents/cyber-defense/risk-classifier.md)** *intermediate* • 30 min
  Classify overall risk level from detected anomalies. Third stage of the cyber defense pipeline — reads cyber-defense-anomalies.json and assigns CRITICAL/HIGH/MEDIUM/LOW with justification.

- **[security-auditor](agents/security-auditor.md)** *intermediate* • 30 min
  Use for security vulnerability detection and OWASP compliance checks

- **[security-patcher](agents/security-patcher.md)** *intermediate* • 30 min
  Apply security patches from security-auditor findings. Requires audit report as input. Always proposes patches for human review — never applies without approval.

- **[test-writer](agents/test-writer.md)** *intermediate* • 30 min
  Use for generating comprehensive tests following TDD/BDD principles

- **[threat-reporter](agents/cyber-defense/threat-reporter.md)** *intermediate* • 30 min
  Generate a human-readable security incident report. Final stage of the cyber defense pipeline — reads all three JSON files and produces a Markdown report for security teams.


### Commands (52)

- **[audit-agents-skills](commands/audit-agents-skills.md)** *intermediate* • 30 min
  Audit quality of agents, skills, and commands in a Claude Code project

- **[audit-codebase](commands/audit-codebase.md)** *intermediate* • 30 min
  Codebase health audit scoring 7 categories with progression plan

- **[autoresearch](commands/autoresearch.md)** *intermediate* • 30 min
  Autonomous improvement loop — scan codebase metrics, scaffold experiment files, run agent-driven iterations until metric improves

- **[canary](commands/canary.md)** *intermediate* • 30 min
  Post-deploy monitoring — watch production after a deploy and alert on regressions

- **[catchup](commands/catchup.md)** *intermediate* • 30 min
  Restore context after /clear by summarizing recent work and project state

- **[check-cache-bugs](commands/check-cache-bugs.md)** *intermediate* • 30 min
  Audit Claude Code setup for cache bugs (CC#40524) — sentinel, --resume/--continue, attribution header + ArkNill B3/B4/B5

- **[ci:all](commands/ci/all.md)** *intermediate* • 30 min
  Full CI pipeline: run local tests, type check, push branch, and return the pipeline URL. The only command you need before opening a PR.

- **[ci:pipeline](commands/ci/pipeline.md)** *intermediate* • 30 min
  Push current branch and return the pipeline tracking URL (GitLab or GitHub Actions)

- **[ci:status](commands/ci/status.md)** *intermediate* • 30 min
  Show current pipeline status for the active branch — GitLab CI or GitHub Actions

- **[ci:tests](commands/ci/tests.md)** *intermediate* • 30 min
  Run the test suite for the current repo — auto-detects Python (pytest/uv), Node (vitest/pnpm), or Rust (cargo test)

- **[commit](commands/commit.md)** *intermediate* • 30 min
  Generate a conventional commit message for staged changes

- **[create-handoff](commands/handoff/create-handoff.md)** *intermediate* • 30 min
  Generate a structured handoff document from the current session. Captures scope, relevant files with line numbers, key discoveries, work completed, current status, next steps, and code snippets. Use before ending a session or handing work to another agent.

- **[diagnose](commands/diagnose.md)** *intermediate* • 30 min
  Interactive troubleshooting assistant for Claude Code issues

- **[explain](commands/explain.md)** *intermediate* • 30 min
  Explain code, concepts, or system behavior with adjustable depth levels

- **[generate-tests](commands/generate-tests.md)** *intermediate* • 30 min
  Generate comprehensive tests for specified code

- **[git-worktree](commands/git-worktree.md)** *intermediate* • 30 min
  Create isolated git worktrees for feature development without switching branches

- **[git-worktree-clean](commands/git-worktree-clean.md)** *intermediate* • 30 min
  Clean up stale git worktrees with merged branch detection and disk usage report

- **[git-worktree-remove](commands/git-worktree-remove.md)** *intermediate* • 30 min
  Safely remove a git worktree with branch cleanup and safety checks

- **[git-worktree-status](commands/git-worktree-status.md)** *intermediate* • 30 min
  Check status of background verification tasks running in a git worktree

- **[investigate](commands/investigate.md)** *intermediate* • 30 min
  Systematic root-cause debugging — find the cause before writing any fix

- **[land-and-deploy](commands/land-and-deploy.md)** *intermediate* • 30 min
  Merge PR, wait for CI, verify deploy, run canary — the complete landing pipeline

- **[learn-alternatives](commands/learn/alternatives.md)** *intermediate* • 30 min
  Compare different approaches to solve the same problem

- **[learn-quiz](commands/learn/quiz.md)** *intermediate* • 30 min
  Test understanding of recently written or accepted code

- **[learn-teach](commands/learn/teach.md)** *intermediate* • 30 min
  Step-by-step explanation of a concept with progressive depth

- **[methodology-advisor](commands/methodology-advisor.md)** *intermediate* • 30 min
  Analyzes your codebase and asks 3 targeted questions to recommend the right AI-assisted development methodology stack

- **[optimize](commands/optimize.md)** *intermediate* • 30 min
  Analyze and suggest performance improvements for code, queries, or systems

- **[plan-ceo-review](commands/plan-ceo-review.md)** *intermediate* • 30 min
  Strategic product gate — challenge the brief, find the 10-star product hiding inside the request, before writing any code

- **[plan-eng-review](commands/plan-eng-review.md)** *intermediate* • 30 min
  Engineering architecture gate — lock architecture, diagrams, edge cases, and test matrix before writing implementation code

- **[plan-execute](commands/plan-execute.md)** *intermediate* • 30 min
  Execute a validated plan: worktree isolation, TDD scaffolding, level-based parallel agents, quality gate with smoke test, PR creation and merge. Handles everything through to merged PR.

- **[plan-start](commands/plan-start.md)** *intermediate* • 30 min
  5-phase planning command: PRD analysis, design review, technical decisions, dynamic research team, metrics. Produces a complete implementation plan + ADRs before any code is written.

- **[plan-validate](commands/plan-validate.md)** *intermediate* • 30 min
  2-layer plan validation: instant structural checks + trigger-based specialist agents. Auto-fixes issues using ADRs and first principles. Every issue must be resolved before execution.

- **[pr](commands/pr.md)** *intermediate* • 30 min
  Analyze changes, detect scope issues, and create a well-structured PR

- **[qa](commands/qa.md)** *intermediate* • 30 min
  Systematic QA testing of a web application — diff-aware, tiered, with fix-and-verify loop

- **[README](commands/ci/README.md)** *intermediate* • 30 min
  Slash commands for CI/CD workflows. Auto-detect stack (Python/Node/Rust) and support both GitLab CI 

- **[recipe-template](commands/recipe-template.md)** *intermediate* • 30 min
  Template for commands that implement a structured recipe: validate preconditions, then execute numbered steps. Fork this and replace the placeholder content. The 'Context Validation Checkpoints' section is the key pattern — it forces Claude to verify preconditions before starting.

- **[refactor](commands/refactor.md)** *intermediate* • 30 min
  Analyze code for SOLID violations and suggest targeted improvements

- **[release-notes](commands/release-notes.md)** *intermediate* • 30 min
  Generate release notes in multiple formats from git commits

- **[resume-handoff](commands/handoff/resume-handoff.md)** *intermediate* • 30 min
  Load a handoff document and resume work from where a previous session left off. Parses scope, file references, completed work, and next steps, then confirms understanding before proceeding.

- **[review-plan](commands/review-plan.md)** *intermediate* • 30 min
  Structured plan review across 4 axes before writing any code (inspired by Garry Tan's workflow)

- **[review-pr](commands/review-pr.md)** *intermediate* • 30 min
  Perform a comprehensive code review of a pull request

- **[routines-discover](commands/routines-discover.md)** *intermediate* • 30 min
  Analyzes the current project to surface high-value Routines use cases across the three trigger types (schedule, API, GitHub events). Usage: /routines-discover

- **[sandbox-status](commands/sandbox-status.md)** *intermediate* • 30 min
  Display native sandbox status, configuration, and recent violations

- **[sandbox-unblock](skills/sandbox-unblock/SKILL.md)** *intermediate* • 30 min
  Eight-check diagnostic protocol to run before reporting a sandbox blocker, plus a report template and escalation path. Cuts the false-positive rate that makes blocker reports expensive to act on.

- **[scaffold](commands/scaffold.md)** *intermediate* • 30 min
  Interactive coach that asks 4-5 questions to determine whether you need an agent, command, skill, hook, or rule — then generates a ready-to-use template. Usage: /scaffold (no arguments — starts the coaching session)

- **[security](commands/security.md)** *intermediate* • 30 min
  Rapid security assessment focused on OWASP Top 10 vulnerabilities

- **[security-audit](commands/security-audit.md)** *intermediate* • 30 min
  Comprehensive security audit with scored posture assessment

- **[security-check](commands/security-check.md)** *intermediate* • 30 min
  Quick configuration security check against known threats database

- **[session-save](commands/session-save.md)** *intermediate* • 30 min
  Save the current session state — decisions, modified files, current status, and next steps — to a handoff file for later resume.

- **[ship](commands/ship.md)** *intermediate* • 30 min
  Comprehensive pre-deployment verification to ensure release readiness

- **[sonarqube](commands/sonarqube.md)** *intermediate* • 30 min
  Analyze SonarCloud quality issues for a specific PR

- **[update-handoff](commands/handoff/update-handoff.md)** *intermediate* • 30 min
  Update an existing handoff document with current session progress. Applies section-specific merge rules: append-only for Work Done (never deletes history), replace for Status and Next Steps, merge for Files and Discoveries. Falls back to creating a new handoff if no source file is found.

- **[update-threat-db](commands/update-threat-db.md)** *intermediate* • 30 min
  Research and update the AI agent security threat intelligence database

- **[validate-changes](commands/validate-changes.md)** *intermediate* • 30 min
  Evaluate staged changes using LLM-as-a-Judge before committing


### Skills (64)

- **[ast-grep-patterns](skills/ast-grep-patterns.md)** *intermediate* • 30 min
  Skill teaching Claude when and how to use ast-grep for structural code searches

- **[audit-agents-skills](skills/audit-agents-skills/SKILL.md)** *intermediate* • 30 min
  Audit Claude Code agents, skills, and commands for quality and production readiness. Use when evaluating skill quality, checking production readiness scores, or comparing agents against best-practice templates.

- **[before-after](skills/voice-refine/examples/before-after.md)** *intermediate* • 30 min
  Real-world examples of verbose voice input transformed into structured prompts

- **[behavioral](skills/design-patterns/reference/behavioral.md)** *intermediate* • 30 min
  Reference for Observer, Strategy, Command, Chain of Responsibility and other behavior patterns

- **[ccboard](skills/ccboard/SKILL.md)** *intermediate* • 30 min
  Launch and navigate the ccboard TUI/Web dashboard for Claude Code. Use when monitoring token usage, tracking costs, browsing sessions, or checking MCP server status across projects.

- **[ccboard-install](skills/ccboard/commands/install.md)** *intermediate* • 30 min
  Install or update ccboard

- **[ccboard-web](skills/ccboard/commands/web.md)** *intermediate* • 30 min
  Launch ccboard web interface

- **[changelog-parsing-rules](skills/guide-recap/references/changelog-parsing-rules.md)** *intermediate* • 30 min
  How to extract and categorize entries from `CHANGELOG.md` for social content generation.

- **[changelog-template](skills/release-notes-generator/assets/changelog-template.md)** *intermediate* • 30 min
  Use this template for generating CHANGELOG.md entries.

- **[commit-categories](skills/release-notes-generator/references/commit-categories.md)** *intermediate* • 30 min
  This document defines how to categorize commits based on Conventional Commits format.

- **[content-transformation](skills/guide-recap/references/content-transformation.md)** *intermediate* • 30 min
  Maps technical CHANGELOG language to user-facing social value. Apply tone-guidelines.md rules to all

- **[costs](skills/ccboard/commands/costs.md)** *intermediate* • 30 min
  Open ccboard costs analysis tab

- **[creational](skills/design-patterns/reference/creational.md)** *intermediate* • 30 min
  Reference for Singleton, Factory, Builder, Prototype and other object creation patterns

- **[cyber-defense-team](skills/cyber-defense-team/SKILL.md)** *intermediate* • 30 min
  Orchestrate a 4-agent cyber defense pipeline to analyze log files for threats. Use when investigating security logs, detecting anomalies in access patterns, classifying breach severity, or generating incident reports from nginx/auth/syslog files.

- **[dashboard](skills/ccboard/commands/dashboard.md)** *intermediate* • 30 min
  Launch ccboard TUI dashboard

- **[design-patterns](skills/design-patterns/SKILL.md)** *intermediate* • 30 min
  Detect, suggest, and evaluate GoF design patterns in TypeScript/JavaScript codebases. Use when refactoring code, applying singleton/factory/observer/strategy patterns, reviewing pattern quality, or finding stack-native alternatives for React, Angular, NestJS, and Vue.

- **[eval-rules](skills/eval-rules/SKILL.md)** *intermediate* • 30 min
  Audit .claude/rules/ files for structural correctness, glob validity, and real-world usefulness. Resolves each paths: pattern against actual project files, then asks the user whether each rule is still relevant and useful. Can update rules in-place based on answers. Use when setting up rules for the first time, debugging rules that fire too often or never, or doing a periodic rules hygiene pass.

- **[eval-skills](skills/eval-skills/SKILL.md)** *intermediate* • 30 min
  Audit all skills in the current project for frontmatter completeness, effort level appropriateness, allowed-tools scoping, and content quality. Produces a scored report with effort-level recommendations for each skill. Use when onboarding to a new project, reviewing skill quality before shipping, or adding effort fields to an existing skill library.

- **[feedback-draft](skills/talk-pipeline/stage-4-position/templates/feedback-draft.md)** *intermediate* • 30 min
  Usage: Send to 1-2 trusted peers BEFORE submitting the CFP or finalizing the script.

- **[git-ai-archaeology](skills/git-ai-archaeology/SKILL.md)** *intermediate* • 30 min
  Analyze AI config evolution in a git repo — first commits per path, monthly distribution, major PRs, maturity phases

- **[guide-recap](skills/guide-recap/SKILL.md)** *intermediate* • 30 min
  Transform CHANGELOG entries into social content (LinkedIn, Twitter/X, Newsletter, Slack) in FR + EN. Use after releases or weekly to generate release notes, announcements, social media posts, or recap summaries from guide updates.

- **[issue-comment](skills/issue-triage/templates/issue-comment.md)** *intermediate* • 30 min
  Use these templates to generate GitHub issue comments during `/issue-triage` Phase 3. Comments are p

- **[issue-triage](skills/issue-triage/SKILL.md)** *intermediate* • 30 min
  3-phase issue backlog management with audit, deep analysis, and validated triage actions. Use when triaging GitHub issues, sorting bug reports, cleaning up stale tickets, or detecting duplicate issues. Args: 'all' to analyze all, issue numbers to focus (e.g. '42 57'), 'en'/'fr' for language, no arg = audit only.

- **[kimi-prompt-template](skills/talk-pipeline/stage-5-script/templates/kimi-prompt-template.md)** *intermediate* • 30 min
  > Copy-paste this entire prompt into Kimi.com to generate the presentation.

- **[landing-page-generator](skills/landing-page-generator/SKILL.md)** *intermediate* • 30 min
  Generate complete, deploy-ready landing pages from any repository. Use when creating a homepage for an open-source project, building a project website, converting a README into a marketing page, or standardizing landing pages across multiple repos.

- **[landing-pattern](skills/landing-page-generator/references/landing-pattern.md)** *intermediate* • 30 min
  Documentation of the established landing page pattern used in `claude-code-ultimate-guide-landing` a

- **[linkedin-template](skills/guide-recap/assets/linkedin-template.md)** *intermediate* • 30 min
  Target: ~1300 characters. Structure: hook + context + bullets + CTA + hashtags.

- **[mcp-integration-reference](skills/mcp-integration-reference/SKILL.md)** *intermediate* • 30 min
  Template for skills that integrate with an MCP server. Demonstrates the reference file pattern: Claude reads a domain-specific MCP cheatsheet before making any tool calls, reducing query failures caused by server-specific gotchas. Fork this skill and replace the Sentry example with your target MCP.

- **[mcp-status](skills/ccboard/commands/mcp-status.md)** *intermediate* • 30 min
  Open ccboard MCP servers tab

- **[newsletter-template](skills/guide-recap/assets/newsletter-template.md)** *intermediate* • 30 min
  Target: ~500 words. Structured sections with depth.

- **[pattern-evaluation](skills/design-patterns/checklists/pattern-evaluation.md)** *intermediate* • 30 min
  Systematic scoring criteria for evaluating design pattern implementation quality

- **[pdf-generator](skills/pdf-generator.md)** *intermediate* • 30 min
  Generate professional PDFs using Quarto/Typst stack with modern design template

- **[pr-triage](skills/pr-triage/SKILL.md)** *intermediate* • 30 min
  4-phase PR backlog management with audit, deep code review, validated comments, and optional worktree setup. Use when triaging pull requests, catching up on pending code reviews, or managing a backlog of open PRs. Args: 'all' to review all, PR numbers to focus (e.g. '42 57'), 'en'/'fr' for language, no arg = audit only.

- **[README](skills/ccboard/README.md)** *intermediate* • 30 min
  > Comprehensive TUI/Web dashboard for monitoring and managing Claude Code

- **[README](skills/talk-pipeline/README.md)** *intermediate* • 30 min
  6-stage skill pipeline that transforms raw material (article, transcript, notes) into a complete con

- **[README](skills/release-notes-generator/references/README.md)** *intermediate* • 30 min
  This directory contains documentation that will be loaded contextually during skill execution.

- **[README](skills/release-notes-generator/scripts/README.md)** *intermediate* • 30 min
  This directory contains executable scripts for deterministic, repeatable tasks.

- **[README](skills/release-notes-generator/assets/README.md)** *intermediate* • 30 min
  This directory contains templates, images, and boilerplate code.

- **[release-notes-generator](skills/release-notes-generator/SKILL.md)** *intermediate* • 30 min
  Generate release notes in 3 formats (CHANGELOG.md, PR body, Slack announcement) from git commits. Automatically categorizes changes and converts technical language to user-friendly messaging. Use for releases, changelogs, version notes, what's new summaries, or ship announcements.

- **[review-comment](skills/pr-triage/templates/review-comment.md)** *intermediate* • 30 min
  Use this template to generate GitHub PR review comments. Fill in each section based on the code-revi

- **[rtk-optimizer](skills/rtk-optimizer/SKILL.md)** *intermediate* • 30 min
  Wrap high-verbosity shell commands with RTK to reduce token consumption. Use when running git log, git diff, cargo test, pytest, or other verbose CLI output that wastes context window tokens.

- **[security-checklist](skills/security-checklist.md)** *intermediate* • 30 min
  Comprehensive security checklist for web applications

- **[sentry-mcp](skills/mcp-integration-reference/references/sentry-mcp.md)** *intermediate* • 30 min
  Reference file for the Sentry MCP server. Read this before making any Sentry MCP calls. It contains 

- **[sessions](skills/ccboard/commands/sessions.md)** *intermediate* • 30 min
  Browse Claude Code sessions history

- **[skill-creator](skills/skill-creator/SKILL.md)** *intermediate* • 30 min
  Scaffold a new Claude Code skill with SKILL.md, frontmatter, and bundled resources. Use when creating a custom skill, standardizing skill structure across a team, or packaging a skill for distribution.

- **[slack-template](skills/guide-recap/assets/slack-template.md)** *intermediate* • 30 min
  Compact, scannable, emoji-rich. Ready to paste.

- **[slack-template](skills/release-notes-generator/assets/slack-template.md)** *intermediate* • 30 min
  Use this template for generating product-focused Slack messages.

- **[smart-explore](skills/smart-explore.md)** *intermediate* • 30 min
  Progressive code exploration using tree-sitter AST — structure first, drill second. Reduces code reading from 10-15k tokens per file to 200-500 tokens.

- **[structural](skills/design-patterns/reference/structural.md)** *intermediate* • 30 min
  Reference for Adapter, Decorator, Facade, Proxy and other composition patterns

- **[talk-pipeline](skills/talk-pipeline/orchestrator/SKILL.md)** *intermediate* • 30 min
  Orchestrates the complete talk preparation pipeline from raw material to revision sheets, running 6 stages in sequence with human-in-the-loop checkpoints for REX or Concept mode talks. Use when starting a new talk pipeline, resuming a pipeline from a specific stage, or running the full end-to-end preparation workflow.

- **[talk-stage1-extract](skills/talk-pipeline/stage-1-extract/SKILL.md)** *intermediate* • 30 min
  Extracts and structures source material (articles, transcripts, notes) into a talk summary with narrative arc, themes, metrics, and gaps. Auto-detects REX vs Concept type. Use when starting a new talk from any source material or auditing existing material before committing to a talk.

- **[talk-stage2-research](skills/talk-pipeline/stage-2-research/SKILL.md)** *intermediate* • 30 min
  Performs git archaeology, changelog analysis, and builds a verified factual timeline by cross-referencing git history with source material. REX mode only — skipped automatically in Concept mode. Use when building a REX talk and you need verified commit metrics, release timelines, and contributor data from a git repository.

- **[talk-stage3-concepts](skills/talk-pipeline/stage-3-concepts/SKILL.md)** *intermediate* • 30 min
  Builds a numbered, categorized concept catalogue from the talk summary and timeline, scoring each concept HIGH / MEDIUM / LOW for talk potential with optional repo enrichment. Use when you need a structured inventory of concepts before choosing a talk angle, or when assessing which ideas have the strongest presentation potential.

- **[talk-stage4-position](skills/talk-pipeline/stage-4-position/SKILL.md)** *intermediate* • 30 min
  Generates 3-4 strategic talk angles with strength/weakness analysis, title options, CFP descriptions, and a peer feedback draft, then enforces a mandatory CHECKPOINT for user confirmation before scripting. Use when deciding how to frame a talk, preparing a CFP submission, or choosing between multiple narrative angles.

- **[talk-stage5-script](skills/talk-pipeline/stage-5-script/SKILL.md)** *intermediate* • 30 min
  Produces a complete 5-act pitch with speaker notes, a slide-by-slide specification, and a ready-to-paste Kimi prompt for AI slide generation. Requires validated angle and title from Stage 4. Use when you have a confirmed talk angle and need the full script, slide spec, and AI-generated presentation prompt.

- **[talk-stage6-revision](skills/talk-pipeline/stage-6-revision/SKILL.md)** *intermediate* • 30 min
  Produces revision sheets with quick navigation by act, a master concept-to-URL table, Q&A cheat-sheet with 6-10 anticipated questions, glossary, and external resources list. Use when preparing for a talk with Q&A, creating shareable reference material for attendees, or building a safety-net glossary for live delivery.

- **[tdd-workflow](skills/tdd-workflow.md)** *intermediate* • 30 min
  Test-Driven Development workflow and best practices

- **[tech-to-product-mappings](skills/release-notes-generator/references/tech-to-product-mappings.md)** *intermediate* • 30 min
  This document defines how to transform technical commit messages into user-friendly product language

- **[token-audit](skills/token-audit/skill.md)** *intermediate* • 30 min
  Audit Claude Code configuration to measure fixed-context token overhead and produce a prioritized action plan

- **[tone-guidelines](skills/guide-recap/references/tone-guidelines.md)** *intermediate* • 30 min
  Rules for social content generated from CHANGELOG entries. Central principle: **engagement through v

- **[twitter-template](skills/guide-recap/assets/twitter-template.md)** *intermediate* • 30 min
  Two modes: single tweet (280 chars) or thread (2-3 tweets).

- **[version-output](skills/guide-recap/examples/version-output.md)** *intermediate* • 30 min
  Input: `/guide-recap v3.20.5`

- **[voice-refine](skills/voice-refine/SKILL.md)** *intermediate* • 30 min
  Transform verbose voice input into structured, token-efficient Claude prompts. Use when cleaning up voice memos, dictation output, or speech-to-text transcriptions that contain filler words, repetitions, and unstructured thoughts.

- **[week-output](skills/guide-recap/examples/week-output.md)** *intermediate* • 30 min
  Input: `/guide-recap week 2026-01-27`


### Hooks (37)

- **[auto-checkpoint](hooks/bash/auto-checkpoint.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[auto-format](hooks/bash/auto-format.sh)** *intermediate* • 30 min
  INPUT=$(cat)

- **[auto-format](hooks/powershell/auto-format.ps1)** *intermediate* • 30 min
  $inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json

- **[auto-rename-session](hooks/bash/auto-rename-session.sh)** *intermediate* • 30 min
  set -uo pipefail

- **[claudemd-scanner](hooks/bash/claudemd-scanner.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[dangerous-actions-blocker](hooks/bash/dangerous-actions-blocker.sh)** *intermediate* • 30 min
  set -e

- **[file-guard](hooks/bash/file-guard.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[governance-enforcement-hook](hooks/bash/governance-enforcement-hook.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[identity-reinjection](hooks/bash/identity-reinjection.sh)** *intermediate* • 30 min
  set -uo pipefail

- **[learning-capture](hooks/bash/learning-capture.sh)** *intermediate* • 30 min
  set -e

- **[mcp-config-integrity](hooks/bash/mcp-config-integrity.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[notification](hooks/bash/notification.sh)** *intermediate* • 30 min
  set -e

- **[output-secrets-scanner](hooks/bash/output-secrets-scanner.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[output-validator](hooks/bash/output-validator.sh)** *intermediate* • 30 min
  set -e

- **[permission-request](hooks/bash/permission-request.sh)** *intermediate* • 30 min
  INPUT=$(cat)

- **[pre-commit-evaluator](hooks/bash/pre-commit-evaluator.sh)** *intermediate* • 30 min
  set -e

- **[pre-commit-secrets](hooks/bash/pre-commit-secrets.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[privacy-warning](hooks/bash/privacy-warning.sh)** *intermediate* • 30 min
  if [[ -n "$PRIVACY_WARNING_SHOWN" ]]; then

- **[prompt-injection-detector](hooks/bash/prompt-injection-detector.sh)** *intermediate* • 30 min
  set -e

- **[repo-integrity-scanner](hooks/bash/repo-integrity-scanner.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[rtk-auto-wrapper](hooks/bash/rtk-auto-wrapper.sh)** *intermediate* • 30 min
  if ! command -v rtk &> /dev/null; then

- **[rtk-baseline](hooks/bash/rtk-baseline.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[sandbox-validation](hooks/bash/sandbox-validation.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[security-check](hooks/bash/security-check.sh)** *intermediate* • 30 min
  INPUT=$(cat)

- **[security-check](hooks/powershell/security-check.ps1)** *intermediate* • 30 min
  $inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json

- **[security-gate](hooks/bash/security-gate.sh)** *intermediate* • 30 min
  set -e

- **[session-logger](hooks/bash/session-logger.sh)** *intermediate* • 30 min
  set -e

- **[session-summary](hooks/bash/session-summary.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[session-summary-config](hooks/bash/session-summary-config.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[setup-init](hooks/bash/setup-init.sh)** *intermediate* • 30 min
  INPUT=$(cat)

- **[smart-suggest](hooks/bash/smart-suggest.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[subagent-stop](hooks/bash/subagent-stop.sh)** *intermediate* • 30 min
  INPUT=$(cat)

- **[test-on-change](hooks/bash/test-on-change.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[tts-selective](hooks/bash/tts-selective.sh)** *intermediate* • 30 min
  set -e

- **[typecheck-on-save](hooks/bash/typecheck-on-save.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[unicode-injection-scanner](hooks/bash/unicode-injection-scanner.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[velocity-governor](hooks/bash/velocity-governor.sh)** *intermediate* • 30 min
  set -euo pipefail


### Workflows (3)

- **[database-branch-setup](workflows/database-branch-setup.md)** *intermediate* • 30 min
  Guide for isolated feature development using database branches with Neon or PlanetScale

- **[memory-stack-integration](workflows/memory-stack-integration.md)** *intermediate* • 30 min
  5-day sprint example combining claude-mem, Serena, grepai and rg for auth refactoring

- **[remotion-quickstart](workflows/remotion-quickstart.md)** *intermediate* • 30 min
  15-minute quickstart to create programmatic videos with Remotion and Claude Code


### Scripts (2)

- **[ai-usage-charter-template](scripts/ai-usage-charter-template.md)** *intermediate* • 30 min
  > **Template** — Copy to `docs/ai-usage-charter.md` in your organization's docs repo.

- **[README](scripts/README.md)** *intermediate* • 30 min
  Utility scripts for Claude Code power users: audits, health checks, and session management


---

## By Domain

### General (181)

- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **adr-writer** (intermediate, 30 min)
- **ai-usage-charter-template** (intermediate, 30 min)
- **analytics-agent** (intermediate, 30 min)
- **anomaly-detector** (intermediate, 30 min)
- **architecture-reviewer** (intermediate, 30 min)
- **ast-grep-patterns** (intermediate, 30 min)
- **audit-agents-skills** (intermediate, 30 min)
- **audit-agents-skills** (intermediate, 30 min)
- **audit-codebase** (intermediate, 30 min)
- **auto-checkpoint** (intermediate, 30 min)
- **auto-format** (intermediate, 30 min)
- **auto-format** (intermediate, 30 min)
- **auto-rename-session** (intermediate, 30 min)
- **autoresearch** (intermediate, 30 min)
- **before-after** (intermediate, 30 min)
- **behavioral** (intermediate, 30 min)
- **canary** (intermediate, 30 min)
- **catchup** (intermediate, 30 min)
- **ccboard** (intermediate, 30 min)
- **ccboard-install** (intermediate, 30 min)
- **ccboard-web** (intermediate, 30 min)
- **changelog-parsing-rules** (intermediate, 30 min)
- **changelog-template** (intermediate, 30 min)
- **check-cache-bugs** (intermediate, 30 min)
- **ci:all** (intermediate, 30 min)
- **ci:pipeline** (intermediate, 30 min)
- **ci:status** (intermediate, 30 min)
- **ci:tests** (intermediate, 30 min)
- **claudemd-scanner** (intermediate, 30 min)
- **code-reviewer** (intermediate, 30 min)
- **commit** (intermediate, 30 min)
- **commit-categories** (intermediate, 30 min)
- **content-transformation** (intermediate, 30 min)
- **costs** (intermediate, 30 min)
- **create-handoff** (intermediate, 30 min)
- **creational** (intermediate, 30 min)
- **cyber-defense-team** (intermediate, 30 min)
- **dangerous-actions-blocker** (intermediate, 30 min)
- **dashboard** (intermediate, 30 min)
- **database-branch-setup** (intermediate, 30 min)
- **design-patterns** (intermediate, 30 min)
- **devops-sre** (intermediate, 30 min)
- **diagnose** (intermediate, 30 min)
- **eval-rules** (intermediate, 30 min)
- **eval-skills** (intermediate, 30 min)
- **explain** (intermediate, 30 min)
- **feedback-draft** (intermediate, 30 min)
- **file-guard** (intermediate, 30 min)
- **generate-tests** (intermediate, 30 min)
- **git-ai-archaeology** (intermediate, 30 min)
- **git-worktree** (intermediate, 30 min)
- **git-worktree-clean** (intermediate, 30 min)
- **git-worktree-remove** (intermediate, 30 min)
- **git-worktree-status** (intermediate, 30 min)
- **governance-enforcement-hook** (intermediate, 30 min)
- **guide-recap** (intermediate, 30 min)
- **identity-reinjection** (intermediate, 30 min)
- **implementer** (intermediate, 30 min)
- **integration-reviewer** (intermediate, 30 min)
- **investigate** (intermediate, 30 min)
- **issue-comment** (intermediate, 30 min)
- **issue-triage** (intermediate, 30 min)
- **kimi-prompt-template** (intermediate, 30 min)
- **land-and-deploy** (intermediate, 30 min)
- **landing-page-generator** (intermediate, 30 min)
- **landing-pattern** (intermediate, 30 min)
- **learn-alternatives** (intermediate, 30 min)
- **learn-quiz** (intermediate, 30 min)
- **learn-teach** (intermediate, 30 min)
- **learning-capture** (intermediate, 30 min)
- **linkedin-template** (intermediate, 30 min)
- **log-ingestor** (intermediate, 30 min)
- **loop-monitor** (intermediate, 30 min)
- **mcp-config-integrity** (intermediate, 30 min)
- **mcp-integration-reference** (intermediate, 30 min)
- **mcp-status** (intermediate, 30 min)
- **memory-stack-integration** (intermediate, 30 min)
- **methodology-advisor** (intermediate, 30 min)
- **newsletter-template** (intermediate, 30 min)
- **notification** (intermediate, 30 min)
- **optimize** (intermediate, 30 min)
- **output-evaluator** (intermediate, 30 min)
- **output-secrets-scanner** (intermediate, 30 min)
- **output-validator** (intermediate, 30 min)
- **pattern-evaluation** (intermediate, 30 min)
- **pdf-generator** (intermediate, 30 min)
- **permission-request** (intermediate, 30 min)
- **plan-ceo-review** (intermediate, 30 min)
- **plan-challenger** (intermediate, 30 min)
- **plan-eng-review** (intermediate, 30 min)
- **plan-execute** (intermediate, 30 min)
- **plan-start** (intermediate, 30 min)
- **plan-validate** (intermediate, 30 min)
- **planner** (intermediate, 30 min)
- **planning-coordinator** (intermediate, 30 min)
- **pr** (intermediate, 30 min)
- **pr-triage** (intermediate, 30 min)
- **pre-commit-evaluator** (intermediate, 30 min)
- **pre-commit-secrets** (intermediate, 30 min)
- **privacy-warning** (intermediate, 30 min)
- **prompt-injection-detector** (intermediate, 30 min)
- **qa** (intermediate, 30 min)
- **recipe-template** (intermediate, 30 min)
- **refactor** (intermediate, 30 min)
- **refactoring-specialist** (intermediate, 30 min)
- **release-notes** (intermediate, 30 min)
- **release-notes-generator** (intermediate, 30 min)
- **remotion-quickstart** (intermediate, 30 min)
- **repo-integrity-scanner** (intermediate, 30 min)
- **report-template** (intermediate, 30 min)
- **resume-handoff** (intermediate, 30 min)
- **review-comment** (intermediate, 30 min)
- **review-plan** (intermediate, 30 min)
- **review-pr** (intermediate, 30 min)
- **risk-classifier** (intermediate, 30 min)
- **routines-discover** (intermediate, 30 min)
- **rtk-auto-wrapper** (intermediate, 30 min)
- **rtk-baseline** (intermediate, 30 min)
- **rtk-optimizer** (intermediate, 30 min)
- **sandbox-status** (intermediate, 30 min)
- **sandbox-unblock** (intermediate, 30 min)
- **sandbox-validation** (intermediate, 30 min)
- **scaffold** (intermediate, 30 min)
- **security** (intermediate, 30 min)
- **security-audit** (intermediate, 30 min)
- **security-auditor** (intermediate, 30 min)
- **security-check** (intermediate, 30 min)
- **security-check** (intermediate, 30 min)
- **security-check** (intermediate, 30 min)
- **security-checklist** (intermediate, 30 min)
- **security-gate** (intermediate, 30 min)
- **security-patcher** (intermediate, 30 min)
- **sentry-mcp** (intermediate, 30 min)
- **session-logger** (intermediate, 30 min)
- **session-save** (intermediate, 30 min)
- **session-summary** (intermediate, 30 min)
- **session-summary-config** (intermediate, 30 min)
- **sessions** (intermediate, 30 min)
- **setup-init** (intermediate, 30 min)
- **ship** (intermediate, 30 min)
- **skill-creator** (intermediate, 30 min)
- **slack-template** (intermediate, 30 min)
- **slack-template** (intermediate, 30 min)
- **smart-explore** (intermediate, 30 min)
- **smart-suggest** (intermediate, 30 min)
- **sonarqube** (intermediate, 30 min)
- **structural** (intermediate, 30 min)
- **subagent-stop** (intermediate, 30 min)
- **talk-pipeline** (intermediate, 30 min)
- **talk-stage1-extract** (intermediate, 30 min)
- **talk-stage2-research** (intermediate, 30 min)
- **talk-stage3-concepts** (intermediate, 30 min)
- **talk-stage4-position** (intermediate, 30 min)
- **talk-stage5-script** (intermediate, 30 min)
- **talk-stage6-revision** (intermediate, 30 min)
- **tdd-workflow** (intermediate, 30 min)
- **tech-to-product-mappings** (intermediate, 30 min)
- **test-on-change** (intermediate, 30 min)
- **test-writer** (intermediate, 30 min)
- **threat-reporter** (intermediate, 30 min)
- **token-audit** (intermediate, 30 min)
- **tone-guidelines** (intermediate, 30 min)
- **tts-selective** (intermediate, 30 min)
- **twitter-template** (intermediate, 30 min)
- **typecheck-on-save** (intermediate, 30 min)
- **unicode-injection-scanner** (intermediate, 30 min)
- **update-handoff** (intermediate, 30 min)
- **update-threat-db** (intermediate, 30 min)
- **validate-changes** (intermediate, 30 min)
- **velocity-governor** (intermediate, 30 min)
- **version-output** (intermediate, 30 min)
- **voice-refine** (intermediate, 30 min)
- **week-output** (intermediate, 30 min)

---

## For Beginners

Templates recommended for first-time users:

No templates explicitly marked as beginner-friendly yet.

---

## Metadata Reference

Templates can include the following metadata in YAML frontmatter:

```yaml

name: template-name

description: What this template does

complexity: beginner|intermediate|advanced

time: 5 min|15 min|30 min|1 hour|2 hours|4+ hours|varies

domain: security|testing|deployment|general|...

prerequisites: [skill1, skill2]

status: stable|experimental|deprecated

keywords: [tag1, tag2]

```
