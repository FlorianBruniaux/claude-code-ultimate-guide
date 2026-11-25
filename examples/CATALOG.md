# Template Catalog

Auto-generated template index with complexity, time, and domain filters.

**Last updated**: [auto-generated]

---

**Total Templates**: 195

- **Agents**: 23
- **Skills**: 124
- **Hooks**: 40
- **Workflows**: 6
- **Scripts**: 2

## Filter by Complexity

- **Beginner**: 0 templates
- **Intermediate**: 195 templates
- **Advanced**: 0 templates

## Filter by Time

- **15 min**: 1 templates
- **30 min**: 192 templates
- **varies**: 2 templates

---

## By category

### Agents (23)

- **[adr-writer](agents/adr-writer.md)** *intermediate* • 30 min
  Architecture Decision Record generator agent: read-only. Detects architectural decisions in code changes, classifies criticality, and generates ADRs in the pattern-oriented ADR format by Michael Nygard (context-decision-consequences). Never modifies code. Use after significant changes or when a decision needs documenting.

- **[analytics-agent](agents/analytics-with-eval/analytics-agent.md)** *intermediate* • 30 min
  SQL query generator with built-in evaluation and safety checks

- **[anomaly-detector](agents/cyber-defense/anomaly-detector.md)** *intermediate* • 30 min
  Detect statistical anomalies and attack patterns from structured security events. Second stage of the cyber defense pipeline: reads cyber-defense-events.json and produces anomalies.

- **[architecture-reviewer](agents/architecture-reviewer.md)** *intermediate* • 30 min
  Architecture and design review agent: read-only. Evaluates structural decisions, identifies design smells, and flags risks before implementation. Never modifies code. Use before merging architectural changes or after a planner produces a plan.

- **[code-reviewer](agents/code-reviewer.md)** *intermediate* • 30 min
  Use proactively after code changes for a thorough review of quality, security, and performance. Read-only: reports findings with severity and does not edit files.

- **[devops-sre](agents/devops-sre.md)** *intermediate* • 30 min
  Infrastructure troubleshooting using the FIRE framework (First Response, Investigate, Remediate, Evaluate)

- **[implementer](agents/implementer.md)** *intermediate* • 30 min
  Mechanical execution agent for bounded, well-defined tasks. Scope and approach must be explicit in the task prompt. Use after a planner has produced a plan. For complex logic or design decisions, use Sonnet instead.

- **[integration-reviewer](agents/integration-reviewer.md)** *intermediate* • 30 min
  Runtime integration validator: read-only. Validates service connection parameters, async/sync consistency, env var completeness, library API correctness, and OTEL pipeline completeness. Triggered during /plan-pipeline-validate when new services, libraries, or observability config are in scope.

- **[log-ingestor](agents/cyber-defense/log-ingestor.md)** *intermediate* • 30 min
  Parse raw logs into structured security events. First stage of the cyber defense pipeline: reads log files and extracts typed events (errors, warnings, auth failures, anomalies).

- **[loop-monitor](agents/loop-monitor.md)** *intermediate* • 30 min
  Autonomous loop monitor: detects stalls, token runaway, and infinite loops in long-running unattended Claude sessions. Use alongside a watchdog process when running autonomous pipelines.

- **[output-evaluator](agents/output-evaluator.md)** *intermediate* • 30 min
  Evaluate Claude Code outputs for quality before commit/action (LLM-as-a-Judge pattern)

- **[plan-challenger](agents/plan-challenger.md)** *intermediate* • 30 min
  Adversarial plan review agent: read-only. Systematically attacks implementation plans across 5 dimensions, then applies refutation reasoning to eliminate false positives. Never modifies code. Use before committing to any significant implementation plan.

- **[planner](agents/planner.md)** *intermediate* • 30 min
  Strategic planning agent: read-only exploration before implementation. Use to decompose tasks, analyze codebases, and produce a detailed plan. Never modifies files.

- **[planning-coordinator](agents/planning-coordinator.md)** *intermediate* • 30 min
  Synthesis agent for dynamic research teams: read-only. Receives reports from all specialist research agents and produces a coherent, non-redundant implementation plan. Spawned automatically when 2+ agents are selected in /plan-pipeline-start Phase 4.

- **[README](agents/cyber-defense/README.md)** *intermediate* • 30 min
  A 4-agent pipeline that detects security threats in log files. Built natively with Claude Code Agent

- **[README](agents/analytics-with-eval/README.md)** *intermediate* • 30 min
  Production-ready analytics agent with automated metrics collection and safety validation

- **[refactoring-specialist](agents/refactoring-specialist.md)** *intermediate* • 30 min
  Use for clean code refactoring following SOLID principles and best practices

- **[report-template](agents/analytics-with-eval/eval/report-template.md)** *intermediate* • 30 min
  Monthly evaluation template for scoring analytics agent performance and accuracy

- **[risk-classifier](agents/cyber-defense/risk-classifier.md)** *intermediate* • 30 min
  Classify overall risk level from detected anomalies. Third stage of the cyber defense pipeline: reads cyber-defense-anomalies.json and assigns CRITICAL/HIGH/MEDIUM/LOW with justification.

- **[security-auditor](agents/security-auditor.md)** *intermediate* • 30 min
  Use for security vulnerability detection and OWASP compliance checks

- **[security-patcher](agents/security-patcher.md)** *intermediate* • 30 min
  Apply security patches from security-auditor findings. Requires audit report as input. Always proposes patches for human review: never applies without approval.

- **[test-writer](agents/test-writer.md)** *intermediate* • 30 min
  Use for generating comprehensive tests following TDD/BDD principles

- **[threat-reporter](agents/cyber-defense/threat-reporter.md)** *intermediate* • 30 min
  Generate a human-readable security incident report. Final stage of the cyber defense pipeline: reads all three JSON files and produces a Markdown report for security teams.


### Skills (124)

- **[agent-rationale](skills/agent-rationale/SKILL.md)** *intermediate* • 30 min
  Record why each hunk of an agent-written commit looks the way it does (intent, rejected alternative, risk, evidence, open question) in git notes under refs/notes/rationale, anchored by hunk hash, so a reviewer can read it beside the diff and see when a note went stale. Use after committing agent-written code that a human will review. Not for commit messages, PR descriptions or AI attribution metrics.

- **[ast-grep-patterns](skills/ast-grep-patterns/SKILL.md)** *intermediate* • 30 min
  Structural code search and refactoring with ast-grep: choose it over Grep, then write tested pattern and YAML rule recipes. Use when renaming calls or changing an API signature across a large codebase, migrating a framework, or finding code by shape (async functions without try/catch, empty catch blocks, long parameter lists). Not for plain text searches, which Grep handles faster.

- **[audit-agents-skills](skills/audit-agents-skills/SKILL.md)** *intermediate* • 30 min
  Audit Claude Code agents, skills, and commands for quality and production readiness. Use when evaluating skill quality, checking production readiness scores, or comparing agents against best-practice templates.

- **[audit-codebase](skills/audit-codebase/SKILL.md)** *intermediate* • 30 min
  Codebase health audit scoring 7 categories with progression plan

- **[autoresearch](skills/autoresearch/SKILL.md)** *intermediate* • 30 min
  Autonomous improvement loop: scan codebase metrics, scaffold experiment files, run agent-driven iterations until metric improves

- **[before-after](skills/voice-refine/examples/before-after.md)** *intermediate* • 30 min
  Real-world examples of verbose voice input transformed into structured prompts

- **[behavioral](skills/design-patterns/reference/behavioral.md)** *intermediate* • 30 min
  Reference for Observer, Strategy, Command, Chain of Responsibility and other behavior patterns

- **[best-of-n](skills/best-of-n/SKILL.md)** *intermediate* • 30 min
  Generate bounded independent candidates, score them against a frozen rubric, and verify the selected result with a proof log.

- **[canary](skills/canary/SKILL.md)** *intermediate* • 30 min
  Post-deploy monitoring: watch production after a deploy and alert on regressions

- **[catchup](skills/catchup/SKILL.md)** *intermediate* • 30 min
  Restore context after /clear by summarizing recent commits, uncommitted changes, TODO markers and project state. Read-only.

- **[ccboard](skills/ccboard/SKILL.md)** *intermediate* • 30 min
  Read Claude Code usage data with the ccboard CLI: token and cost stats, recent or searchable sessions, usage reports, skill invocation counts, and the TUI or web dashboard. Use when asked about token usage, spend, session history, which skills actually ran, or how to launch ccboard. Not for editing Claude Code settings.

- **[changelog-parsing-rules](skills/guide-recap/references/changelog-parsing-rules.md)** *intermediate* • 30 min
  How to extract and categorize entries from `CHANGELOG.md` for social content generation.

- **[changelog-template](skills/release-notes-generator/assets/changelog-template.md)** *intermediate* • 30 min
  Use this template for generating CHANGELOG.md entries.

- **[check-cache-bugs](skills/check-cache-bugs/SKILL.md)** *intermediate* • 30 min
  Audit Claude Code setup for cache bugs (CC#40524): sentinel, --resume/--continue, attribution header + ArkNill B3/B4/B5

- **[ci-all](skills/ci-all/SKILL.md)** *intermediate* • 30 min
  Run the local test suite and type check, push the current branch, and return the pipeline URL. Use before opening a PR.

- **[ci-pipeline](skills/ci-pipeline/SKILL.md)** *intermediate* • 30 min
  Push current branch and return the pipeline tracking URL (GitLab or GitHub Actions)

- **[ci-status](skills/ci-status/SKILL.md)** *intermediate* • 30 min
  Show the CI pipeline status for the active branch (GitLab CI or GitHub Actions), or for a given MR or PR number. Use when asked whether CI passed, is running, or failed.

- **[ci-tests](skills/ci-tests/SKILL.md)** *intermediate* • 30 min
  Run the test suite for the current repo, auto-detecting Python (pytest/uv), Node (vitest/pnpm), or Rust (cargo test)

- **[commit](skills/commit/SKILL.md)** *intermediate* • 30 min
  Generate a conventional commit message for staged changes

- **[commit-categories](skills/release-notes-generator/references/commit-categories.md)** *intermediate* • 30 min
  This document defines how to categorize commits based on Conventional Commits format.

- **[content-transformation](skills/guide-recap/references/content-transformation.md)** *intermediate* • 30 min
  Maps technical CHANGELOG language to user-facing social value. Apply tone-guidelines.md rules to all

- **[costs](skills/ccboard/commands/costs.md)** *intermediate* • 30 min
  Show Claude Code token usage and cost figures from ccboard

- **[creational](skills/design-patterns/reference/creational.md)** *intermediate* • 30 min
  Reference for Singleton, Factory, Builder, Prototype and other object creation patterns

- **[cyber-defense-team](skills/cyber-defense-team/SKILL.md)** *intermediate* • 30 min
  Orchestrate a 4-agent cyber defense pipeline to analyze log files for threats. Use when investigating security logs, detecting anomalies in access patterns, classifying breach severity, or generating incident reports from nginx/auth/syslog files.

- **[dashboard](skills/ccboard/commands/dashboard.md)** *intermediate* • 30 min
  Launch the ccboard TUI dashboard for Claude Code usage

- **[design-patterns](skills/design-patterns/SKILL.md)** *intermediate* • 30 min
  Detect, suggest, and evaluate GoF design patterns in TypeScript/JavaScript codebases. Use when refactoring code, applying singleton/factory/observer/strategy patterns, reviewing pattern quality, or finding stack-native alternatives for React, Angular, NestJS, and Vue.

- **[diagnose](skills/diagnose/SKILL.md)** *intermediate* • 30 min
  Interactive troubleshooting assistant for Claude Code issues

- **[eval-agents](skills/eval-agents/SKILL.md)** *intermediate* • 30 min
  Audit custom subagent definitions for Claude Code (.claude/agents/*.md) and Codex (.codex/agents/*.toml): loadability against the native schema, description overlap, model tier, tool scope, and headless-safe instructions. Use when onboarding to a project with agents, after adding or importing agents, or when the parent agent delegates to the wrong agent.

- **[eval-hooks](skills/eval-hooks/SKILL.md)** *intermediate* • 30 min
  Audit Claude Code and Codex hooks for validity, safety, and correctness across settings.json, hooks.json, config.toml, plugin, and skill or agent frontmatter hooks. Resolves each command, checks event names, handler types, matchers, exit-code and JSON decision strategy, and timeouts against each host's documented rules, then reviews hooks one by one. Use when setting up hooks, debugging a hook that never fires, never blocks, or hangs the agent, or doing a periodic hooks hygiene pass. Not for writing a new hook from scratch.

- **[eval-rules](skills/eval-rules/SKILL.md)** *intermediate* • 30 min
  Audit Claude Code instruction rules in .claude/rules/ and ~/.claude/rules/: frontmatter, paths glob validity against real files, symlink load status, and day-to-day usefulness, then update rules with the user. Use for first-time rules setup, rules that apply too often or never, or periodic rules hygiene. Not for Codex .rules command-approval files.

- **[eval-skills](skills/eval-skills/SKILL.md)** *intermediate* • 30 min
  Audit a project or library of skills for metadata, trigger boundaries, workflow completion criteria, local resource closure, instruction economy, tool scope, effort, and routing evidence. Use before shipping skills, after importing a skill collection, or when a skill triggers too often or not at all.

- **[explain](skills/explain/SKILL.md)** *intermediate* • 30 min
  Explain code, concepts, or system behavior with adjustable depth levels

- **[feedback-draft](skills/talk-stage4-position/templates/feedback-draft.md)** *intermediate* • 30 min
  Usage: Send to 1-2 trusted peers BEFORE submitting the CFP or finalizing the script.

- **[generate-tests](skills/generate-tests/SKILL.md)** *intermediate* • 30 min
  Generate tests for given code in the project's own test framework, covering happy path, edge cases and error cases. Use when adding test coverage for a function, module, or feature.

- **[git-ai-archaeology](skills/git-ai-archaeology/SKILL.md)** *intermediate* • 30 min
  Git-history archaeology of a repository's AI coding harness (Copilot, Claude Code, Codex, Cursor, MCP, skills, agents, hooks). Use to date when each AI config appeared, trace how it spread, churned or was abandoned across modules, measure AI-assisted commits over time, or derive maturity phases. Not for auditing the current config or generic git stats.

- **[git-worktree](skills/git-worktree/SKILL.md)** *intermediate* • 30 min
  Create isolated git worktrees for feature development without switching branches

- **[git-worktree-clean](skills/git-worktree-clean/SKILL.md)** *intermediate* • 30 min
  Clean up stale git worktrees with merged branch detection and disk usage report

- **[git-worktree-remove](skills/git-worktree-remove/SKILL.md)** *intermediate* • 30 min
  Safely remove a git worktree with branch cleanup and safety checks

- **[git-worktree-status](skills/git-worktree-status/SKILL.md)** *intermediate* • 30 min
  Report the type check, test and build results that /git-worktree started in the background for the current worktree, read from .worktree-logs/. Use when asked whether a worktree's checks passed or are still running.

- **[guide-recap](skills/guide-recap/SKILL.md)** *intermediate* • 30 min
  Transform CHANGELOG entries into social content (LinkedIn, Twitter/X, Newsletter, Slack) in FR + EN. Use after releases or weekly to generate release notes, announcements, social media posts, or recap summaries from guide updates.

- **[handoff-create](skills/handoff-create/SKILL.md)** *intermediate* • 30 min
  Generate a structured handoff document from the current session. Captures scope, relevant files with line numbers, key discoveries, work completed, current status, next steps, and code snippets. Use before ending a session or handing work to another agent.

- **[handoff-resume](skills/handoff-resume/SKILL.md)** *intermediate* • 30 min
  Load a handoff document and resume work from where a previous session left off. Parses scope, file references, completed work, and next steps, then checks live state and existing authorization before proceeding.

- **[handoff-update](skills/handoff-update/SKILL.md)** *intermediate* • 30 min
  Update an existing handoff document with current session progress. Applies section-specific merge rules: append-only for Work Done (never deletes history), replace for Status and Next Steps, merge for Files and Discoveries. Falls back to creating a new handoff if no source file is found.

- **[install](skills/ccboard/commands/install.md)** *intermediate* • 30 min
  Install or update ccboard

- **[investigate](skills/investigate/SKILL.md)** *intermediate* • 30 min
  Systematic root-cause debugging: find and confirm the cause before writing any fix. Use when a bug, test failure, or unexpected behavior needs a verified root cause and a regression test.

- **[issue-comment](skills/issue-triage/templates/issue-comment.md)** *intermediate* • 30 min
  Use these templates to generate GitHub issue comments during `/issue-triage` Phase 3. Comments are p

- **[issue-triage](skills/issue-triage/SKILL.md)** *intermediate* • 30 min
  Triage a GitHub issue backlog in 3 phases: audit, deep analysis, and validated comment, label, or close actions. Use when triaging GitHub issues, sorting bug reports, cleaning up stale tickets, or detecting duplicate issues. Not for pull requests (use pr-triage).

- **[kimi-prompt-template](skills/talk-stage5-script/templates/kimi-prompt-template.md)** *intermediate* • 30 min
  > Copy-paste this entire prompt into Kimi.com to generate the presentation.

- **[land-and-deploy](skills/land-and-deploy/SKILL.md)** *intermediate* • 30 min
  Merge the current PR after a readiness gate, wait for CI and the deploy, then run a production health check. Use after /ship has created the PR and the user wants it landed.

- **[landing-page-generator](skills/landing-page-generator/SKILL.md)** *intermediate* • 30 min
  Generate complete, deploy-ready landing pages from any repository. Use when creating a homepage for an open-source project, building a project website, converting a README into a marketing page, or standardizing landing pages across multiple repos.

- **[landing-pattern](skills/landing-page-generator/references/landing-pattern.md)** *intermediate* • 30 min
  Documentation of the established landing page pattern used in `claude-code-ultimate-guide-landing` a

- **[learn-alternatives](skills/learn-alternatives/SKILL.md)** *intermediate* • 30 min
  Compare 3-5 alternative approaches to the same problem with trade-offs and a recommendation. Use when the user asks for alternatives, options, or how else something could be done.

- **[learn-quiz](skills/learn-quiz/SKILL.md)** *intermediate* • 30 min
  Quiz the user on recently written or accepted code, one question at a time with explained feedback. Use when the user asks to be quizzed or wants to check they understand code Claude just produced.

- **[learn-teach](skills/learn-teach/SKILL.md)** *intermediate* • 30 min
  Teach a programming concept step by step: definition, minimal example, practical example, common mistakes, next topics. Use when the user asks to learn or understand a concept.

- **[learning-path](skills/learning-path/SKILL.md)** *intermediate* • 30 min
  Run the local Claude Code learning path: pick a track, record evidence for each completed module, and schedule evidence-based reviews. Use when the user wants to follow the guide's learning path, see the next module, check progress, or list due reviews. Not for the quick skill diagnostic (use self-assessment).

- **[linkedin-template](skills/guide-recap/assets/linkedin-template.md)** *intermediate* • 30 min
  Target: ~1300 characters. Structure: hook + context + bullets + CTA + hashtags.

- **[mcp-integration-reference](skills/mcp-integration-reference/SKILL.md)** *intermediate* • 30 min
  Template for skills that wrap an MCP server, with a working Sentry error report as the example. Use when building a skill around an MCP server, or when asked for a Sentry error report grouped by root cause. Claude reads a domain-specific MCP cheatsheet before any tool call, which avoids server-specific query failures. Fork it and replace the Sentry example with your target MCP.

- **[mcp-status](skills/ccboard/commands/mcp-status.md)** *intermediate* • 30 min
  Open the MCP servers tab of the ccboard TUI

- **[methodology-advisor](skills/methodology-advisor/SKILL.md)** *intermediate* • 30 min
  Analyze the codebase, ask 3 targeted questions, and recommend one AI-assisted development methodology stack (TDD, spec-driven, BDD, eval-driven, and others). Use when the user asks which methodology, workflow, or process to adopt with Claude Code for a project.

- **[newsletter-template](skills/guide-recap/assets/newsletter-template.md)** *intermediate* • 30 min
  Target: ~500 words. Structured sections with depth.

- **[optimize](skills/optimize/SKILL.md)** *intermediate* • 30 min
  Analyze and suggest performance improvements for code, queries, or systems

- **[pattern-evaluation](skills/design-patterns/checklists/pattern-evaluation.md)** *intermediate* • 30 min
  Systematic scoring criteria for evaluating design pattern implementation quality

- **[pdf-generator](skills/pdf-generator/SKILL.md)** *intermediate* • 30 min
  Generate professional PDFs from Markdown with the Quarto and Typst stack: project setup, templates, rendering, and troubleshooting. Use when the user wants a styled PDF or EPUB from .qmd or Markdown sources, or when a Quarto/Typst render fails.

- **[plan-pipeline](skills/plan-pipeline/SKILL.md)** *intermediate* • 30 min
  Coordinate the plan-to-merged-PR pipeline: product direction (ceo-review), architecture (eng-review), implementation plan (start), validation (validate), execution (execute). Use when planning and shipping a non-trivial feature end to end, or to resume the pipeline from a given stage. Not for small changes (use plan mode).

- **[plan-pipeline-ceo-review](skills/plan-pipeline-ceo-review/SKILL.md)** *intermediate* • 30 min
  Strategic product gate: challenge the brief and find the 10-star product hiding in the request before any code is written. Use before implementing a significant feature when the product direction is not locked.

- **[plan-pipeline-eng-review](skills/plan-pipeline-eng-review/SKILL.md)** *intermediate* • 30 min
  Engineering architecture gate: lock architecture, diagrams, edge cases, and the test matrix before implementation code. Use after product direction is locked, for features with async parts, external dependencies, or multi-step flows.

- **[plan-pipeline-execute](skills/plan-pipeline-execute/SKILL.md)** *intermediate* • 30 min
  Execute a validated plan: worktree isolation, TDD scaffolding, level-based parallel agents, quality gate with smoke test, PR creation and merge. Use only after /plan-pipeline-validate has resolved all issues.

- **[plan-pipeline-start](skills/plan-pipeline-start/SKILL.md)** *intermediate* • 30 min
  5-phase planning: PRD analysis, design review, technical decisions, dynamic research team, metrics. Produces a complete implementation plan and ADRs before any code is written. Use for any non-trivial feature.

- **[plan-pipeline-validate](skills/plan-pipeline-validate/SKILL.md)** *intermediate* • 30 min
  2-layer plan validation: instant structural checks plus trigger-based specialist agents. Auto-fixes issues using ADRs and first principles; every issue must be resolved before execution. Use after /plan-pipeline-start and before /plan-pipeline-execute.

- **[pr](skills/pr/SKILL.md)** *intermediate* • 30 min
  Analyze changes, detect scope issues, and create a well-structured PR

- **[pr-triage](skills/pr-triage/SKILL.md)** *intermediate* • 30 min
  Triage a pull request backlog in 4 phases: audit, deep code review, validated comments, and optional local worktrees. Use when triaging pull requests, catching up on pending code reviews, or managing a backlog of open PRs. Not for a single PR (use review-pr) or issues (use issue-triage).

- **[qa](skills/qa/SKILL.md)** *intermediate* • 30 min
  Systematic QA testing of a web application: diff-aware scope, three tiers, and an atomic fix-and-verify loop. Use before opening a PR or cutting a release.

- **[reading-grid](skills/git-ai-archaeology/references/reading-grid.md)** *intermediate* • 30 min
  Each indicator comes from `{slug}-harness.json`. The thresholds are reading aids, not verdicts: a ca

- **[README](skills/learning-path/README.md)** *intermediate* • 30 min
  This dependency-free prototype turns the existing [seven-module learning path](../../../guide/learni

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

- **[recipe-template](skills/recipe-template/SKILL.md)** *intermediate* • 30 min
  Template for skills that implement a structured recipe: validate preconditions, then execute numbered steps. Fork this and replace the placeholder content. The 'Context Validation Checkpoints' section is the key pattern, forcing Claude to verify preconditions before starting.

- **[refactor](skills/refactor/SKILL.md)** *intermediate* • 30 min
  Analyze code for SOLID violations and suggest targeted improvements

- **[release-notes](skills/release-notes/SKILL.md)** *intermediate* • 30 min
  Generate release notes in multiple formats from git commits

- **[release-notes-generator](skills/release-notes-generator/SKILL.md)** *intermediate* • 30 min
  Generate release notes in 3 formats (CHANGELOG.md, PR body, Slack announcement) from git commits. Automatically categorizes changes and converts technical language to user-friendly messaging. Use for releases, changelogs, version notes, what's new summaries, or ship announcements.

- **[review-comment](skills/pr-triage/templates/review-comment.md)** *intermediate* • 30 min
  Use this template to generate GitHub PR review comments. Fill in each section based on the code-revi

- **[review-plan](skills/review-plan/SKILL.md)** *intermediate* • 30 min
  Structured plan review across 4 axes before writing any code (inspired by Garry Tan's workflow)

- **[review-pr](skills/review-pr/SKILL.md)** *intermediate* • 30 min
  Review a GitHub pull request by number or URL with a structured checklist (quality, correctness, security, tests, docs) and an optional multi-agent pass. Use when asked to review a PR before merge.

- **[routines-discover](skills/routines-discover/SKILL.md)** *intermediate* • 30 min
  Analyzes the current project to surface high-value Routines use cases across the three trigger types (schedule, API, GitHub events). Usage: /routines-discover

- **[rtk-optimizer](skills/rtk-optimizer/SKILL.md)** *intermediate* • 30 min
  Wrap high-verbosity shell commands with RTK to reduce token consumption. Use when running git log, git diff, cargo test, pytest, or other verbose CLI output that wastes context window tokens.

- **[sandbox-status](skills/sandbox-status/SKILL.md)** *intermediate* • 30 min
  Display native sandbox status, configuration, and recent violations

- **[sandbox-unblock](skills/sandbox-unblock/SKILL.md)** *intermediate* • 30 min
  Diagnostic protocol to run before reporting a sandbox blocker or asking for a configuration change. Eleven checks that eliminate false positives, then a report template the person holding the settings can act on. On one measured day, six of eight reported blockers turned out to be false, all from the same handful of method errors.


- **[scaffold](skills/scaffold/SKILL.md)** *intermediate* • 30 min
  Interactive coach that asks 4-5 questions to decide whether a use case needs an agent, a skill, a hook, or a rule, then generates a ready-to-use template. Start it with /scaffold (no arguments); it runs only on request.

- **[security](skills/security/SKILL.md)** *intermediate* • 30 min
  Rapid heuristic security scan of the current codebase for OWASP Top 10 patterns (secrets, injection, XSS, dependencies, auth). Use for a quick pass on application code; for configuration and posture scoring use security-audit.

- **[security-audit](skills/security-audit/SKILL.md)** *intermediate* • 30 min
  Comprehensive security audit with scored posture assessment

- **[security-check](skills/security-check/SKILL.md)** *intermediate* • 30 min
  Quick configuration security check against known threats database

- **[security-checklist](skills/security-checklist/SKILL.md)** *intermediate* • 30 min
  Reference security checklist and code patterns for web applications (authentication, authorization, input validation, headers, secrets, logging). Use when writing or reviewing web app code that handles auth, user input, sessions, or deployment hardening. Not for scanning a codebase: use the security skill.

- **[sentry-mcp](skills/mcp-integration-reference/references/sentry-mcp.md)** *intermediate* • 30 min
  Reference file for the Sentry MCP server. Read this before making any Sentry MCP calls. It contains 

- **[session-save](skills/session-save/SKILL.md)** *intermediate* • 30 min
  Save the current session state (decisions, modified files, current status, and next steps) to a handoff file for later resume.

- **[sessions](skills/ccboard/commands/sessions.md)** *intermediate* • 30 min
  List or search recent Claude Code sessions with ccboard

- **[ship](skills/ship/SKILL.md)** *intermediate* • 30 min
  Comprehensive pre-deployment verification to ensure release readiness

- **[skill-creator](skills/skill-creator/SKILL.md)** *intermediate* • 30 min
  Scaffold a new Claude Code skill with SKILL.md, frontmatter, and bundled resources. Use when creating a custom skill, standardizing skill structure across a team, or packaging a skill for distribution.

- **[slack-template](skills/guide-recap/assets/slack-template.md)** *intermediate* • 30 min
  Compact, scannable, emoji-rich. Ready to paste.

- **[slack-template](skills/release-notes-generator/assets/slack-template.md)** *intermediate* • 30 min
  Use this template for generating product-focused Slack messages.

- **[smart-explore](skills/smart-explore/SKILL.md)** *intermediate* • 30 min
  Progressive code exploration, structure first and drill second, using grep patterns, a tree-sitter signature script, or an MCP server. Use when understanding an unfamiliar module or finding where to add a feature without reading whole files. Not for reading one known function. Illustrative estimate: 10-15k tokens per file down to 200-500.

- **[sonarqube](skills/sonarqube/SKILL.md)** *intermediate* • 30 min
  Analyze SonarCloud quality issues for a specific pull request and produce a report with metrics, top violators, and an action plan. Read-only; makes no code changes.

- **[structural](skills/design-patterns/reference/structural.md)** *intermediate* • 30 min
  Reference for Adapter, Decorator, Facade, Proxy and other composition patterns

- **[talk-pipeline](skills/talk-pipeline/SKILL.md)** *intermediate* • 30 min
  Orchestrates the complete talk preparation pipeline from raw material to revision sheets, running 6 stages in sequence with human-in-the-loop checkpoints for REX or Concept mode talks. Use when starting a new talk pipeline, resuming a pipeline from a specific stage, or running the full end-to-end preparation workflow.

- **[talk-stage1-extract](skills/talk-stage1-extract/SKILL.md)** *intermediate* • 30 min
  Extracts and structures source material (articles, transcripts, notes) into a talk summary with narrative arc, themes, metrics, and gaps. Auto-detects REX vs Concept type. Use when starting a new talk from any source material or auditing existing material before committing to a talk.

- **[talk-stage2-research](skills/talk-stage2-research/SKILL.md)** *intermediate* • 30 min
  Performs git archaeology, changelog analysis, and builds a verified factual timeline by cross-referencing git history with source material. REX mode only (skipped automatically in Concept mode). Use when building a REX talk and you need verified commit metrics, release timelines, and contributor data from a git repository.

- **[talk-stage3-concepts](skills/talk-stage3-concepts/SKILL.md)** *intermediate* • 30 min
  Builds a numbered, categorized concept catalogue from the talk summary and timeline, scoring each concept HIGH / MEDIUM / LOW for talk potential with optional repo enrichment. Use when you need a structured inventory of concepts before choosing a talk angle, or when assessing which ideas have the strongest presentation potential.

- **[talk-stage4-position](skills/talk-stage4-position/SKILL.md)** *intermediate* • 30 min
  Generates 3-4 strategic talk angles with strength/weakness analysis, title options, CFP descriptions, and a peer feedback draft, then enforces a mandatory CHECKPOINT for user confirmation before scripting. Use when deciding how to frame a talk, preparing a CFP submission, or choosing between multiple narrative angles.

- **[talk-stage5-script](skills/talk-stage5-script/SKILL.md)** *intermediate* • 30 min
  Produces a complete 5-act pitch with speaker notes, a slide-by-slide specification, and a ready-to-paste Kimi prompt for AI slide generation. Requires validated angle and title from Stage 4. Use when you have a confirmed talk angle and need the full script, slide spec, and AI-generated presentation prompt.

- **[talk-stage6-revision](skills/talk-stage6-revision/SKILL.md)** *intermediate* • 30 min
  Produces revision sheets with quick navigation by act, a master concept-to-URL table, Q&A cheat-sheet with 6-10 anticipated questions, glossary, and external resources list. Use when preparing for a talk with Q&A, creating shareable reference material for attendees, or building a safety-net glossary for live delivery.

- **[tdd-workflow](skills/tdd-workflow/SKILL.md)** *intermediate* • 30 min
  Red-green-refactor workflow with test naming, Arrange-Act-Assert structure and isolation rules. Use when writing a feature or bug fix test-first, or when the user asks for TDD.

- **[tech-to-product-mappings](skills/release-notes-generator/references/tech-to-product-mappings.md)** *intermediate* • 30 min
  This document defines how to transform technical commit messages into user-friendly product language

- **[token-audit](skills/token-audit/SKILL.md)** *intermediate* • 30 min
  Audit Claude Code configuration to measure fixed-context token overhead and produce a prioritized action plan. Use when hitting rate limits, experiencing early context compression, or after adding significant config files. Not for per-skill cost: use /skill-doctor.

- **[tone-guidelines](skills/guide-recap/references/tone-guidelines.md)** *intermediate* • 30 min
  Rules for social content generated from CHANGELOG entries. Central principle: **engagement through v

- **[twitter-template](skills/guide-recap/assets/twitter-template.md)** *intermediate* • 30 min
  Two modes: single tweet (280 chars) or thread (2-3 tweets).

- **[update-threat-db](skills/update-threat-db/SKILL.md)** *intermediate* • 30 min
  Refresh the guide's threat intelligence by delegating research and updates to AgentSec Triage, then validate the guide and landing mirrors. Use when asked to update the threat database, pull new coding-agent or MCP security advisories, or sync the security feed. Not for scanning a repository (use security-check or security-audit) or tracking Claude Code releases.

- **[validate-changes](skills/validate-changes/SKILL.md)** *intermediate* • 30 min
  Evaluate staged changes with the output-evaluator agent (LLM-as-a-Judge) and return an APPROVE, NEEDS_REVIEW, or REJECT verdict before committing. Use before committing significant or security-sensitive changes.

- **[version-output](skills/guide-recap/examples/version-output.md)** *intermediate* • 30 min
  Input: `/guide-recap v3.20.5`

- **[voice-refine](skills/voice-refine/SKILL.md)** *intermediate* • 30 min
  Transform verbose voice input into structured, token-efficient Claude prompts. Use when cleaning up voice memos, dictation output, or speech-to-text transcriptions that contain filler words, repetitions, and unstructured thoughts.

- **[web](skills/ccboard/commands/web.md)** *intermediate* • 30 min
  Launch the ccboard web interface

- **[week-output](skills/guide-recap/examples/week-output.md)** *intermediate* • 30 min
  Input: `/guide-recap week 2026-01-27`

- **[worktree-setup](skills/pr-triage/references/worktree-setup.md)** *intermediate* • 30 min
  Loaded on demand by `pr-triage` when the user asks for local worktrees. Heading levels below keep th


### Hooks (40)

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
  set -euo pipefail

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
  cat > /dev/null  # consume stdin

- **[prompt-injection-detector](hooks/bash/prompt-injection-detector.sh)** *intermediate* • 30 min
  set -e

- **[repo-integrity-scanner](hooks/bash/repo-integrity-scanner.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[rtk-auto-wrapper](hooks/bash/rtk-auto-wrapper.sh)** *intermediate* • 30 min
  INPUT=$(cat)

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

- **[test-hooks](hooks/bash/test-hooks.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[test-on-change](hooks/bash/test-on-change.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[test-private-key-detection](hooks/bash/test-private-key-detection.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[tts-selective](hooks/bash/tts-selective.sh)** *intermediate* • 30 min
  set -e

- **[typecheck-on-save](hooks/bash/typecheck-on-save.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[unicode-injection-scanner](hooks/bash/unicode-injection-scanner.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[velocity-governor](hooks/bash/velocity-governor.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[verification-gate](hooks/bash/verification-gate.sh)** *intermediate* • 30 min
  set -euo pipefail


### Workflows (6)

- **[bounded-loop-contract](workflows/bounded-loop-contract.md)** *intermediate* • 15 min • architecture
  Reference contract for a bounded agent loop with a separate verifier interface, evidence, and escalation
  *Prerequisites*: Python 3.10+

- **[database-branch-setup](workflows/database-branch-setup.md)** *intermediate* • 30 min
  Guide for isolated feature development using database branches with Neon or PlanetScale

- **[lean-harness-experiment](workflows/lean-harness-experiment.md)** *intermediate* • varies • testing • ⚠️ experimental
  Test one repository harness countermeasure against a known failure and its operating cost

- **[memory-stack-integration](workflows/memory-stack-integration.md)** *intermediate* • 30 min
  5-day sprint example combining claude-mem, Serena, grepai and rg for auth refactoring

- **[remotion-quickstart](workflows/remotion-quickstart.md)** *intermediate* • 30 min
  15-minute quickstart to create programmatic videos with Remotion and Claude Code

- **[review-admission](workflows/review-admission.md)** *intermediate* • varies • testing • ⚠️ experimental
  Define shared review capacity, pause and resume rules, and a tabletop exercise


### Scripts (2)

- **[ai-usage-charter-template](scripts/ai-usage-charter-template.md)** *intermediate* • 30 min
  > **Template**: Copy to `docs/ai-usage-charter.md` in your organization's docs repo.

- **[README](scripts/README.md)** *intermediate* • 30 min
  Utility scripts for Claude Code power users: audits, health checks, and session management


---

## By domain

### Architecture (1)

- **bounded-loop-contract** (intermediate, 15 min)

### General (192)

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
- **agent-rationale** (intermediate, 30 min)
- **ai-usage-charter-template** (intermediate, 30 min)
- **analytics-agent** (intermediate, 30 min)
- **anomaly-detector** (intermediate, 30 min)
- **architecture-reviewer** (intermediate, 30 min)
- **ast-grep-patterns** (intermediate, 30 min)
- **audit-agents-skills** (intermediate, 30 min)
- **audit-codebase** (intermediate, 30 min)
- **auto-checkpoint** (intermediate, 30 min)
- **auto-format** (intermediate, 30 min)
- **auto-format** (intermediate, 30 min)
- **auto-rename-session** (intermediate, 30 min)
- **autoresearch** (intermediate, 30 min)
- **before-after** (intermediate, 30 min)
- **behavioral** (intermediate, 30 min)
- **best-of-n** (intermediate, 30 min)
- **canary** (intermediate, 30 min)
- **catchup** (intermediate, 30 min)
- **ccboard** (intermediate, 30 min)
- **changelog-parsing-rules** (intermediate, 30 min)
- **changelog-template** (intermediate, 30 min)
- **check-cache-bugs** (intermediate, 30 min)
- **ci-all** (intermediate, 30 min)
- **ci-pipeline** (intermediate, 30 min)
- **ci-status** (intermediate, 30 min)
- **ci-tests** (intermediate, 30 min)
- **claudemd-scanner** (intermediate, 30 min)
- **code-reviewer** (intermediate, 30 min)
- **commit** (intermediate, 30 min)
- **commit-categories** (intermediate, 30 min)
- **content-transformation** (intermediate, 30 min)
- **costs** (intermediate, 30 min)
- **creational** (intermediate, 30 min)
- **cyber-defense-team** (intermediate, 30 min)
- **dangerous-actions-blocker** (intermediate, 30 min)
- **dashboard** (intermediate, 30 min)
- **database-branch-setup** (intermediate, 30 min)
- **design-patterns** (intermediate, 30 min)
- **devops-sre** (intermediate, 30 min)
- **diagnose** (intermediate, 30 min)
- **eval-agents** (intermediate, 30 min)
- **eval-hooks** (intermediate, 30 min)
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
- **handoff-create** (intermediate, 30 min)
- **handoff-resume** (intermediate, 30 min)
- **handoff-update** (intermediate, 30 min)
- **identity-reinjection** (intermediate, 30 min)
- **implementer** (intermediate, 30 min)
- **install** (intermediate, 30 min)
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
- **learning-path** (intermediate, 30 min)
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
- **plan-challenger** (intermediate, 30 min)
- **plan-pipeline** (intermediate, 30 min)
- **plan-pipeline-ceo-review** (intermediate, 30 min)
- **plan-pipeline-eng-review** (intermediate, 30 min)
- **plan-pipeline-execute** (intermediate, 30 min)
- **plan-pipeline-start** (intermediate, 30 min)
- **plan-pipeline-validate** (intermediate, 30 min)
- **planner** (intermediate, 30 min)
- **planning-coordinator** (intermediate, 30 min)
- **pr** (intermediate, 30 min)
- **pr-triage** (intermediate, 30 min)
- **pre-commit-evaluator** (intermediate, 30 min)
- **pre-commit-secrets** (intermediate, 30 min)
- **privacy-warning** (intermediate, 30 min)
- **prompt-injection-detector** (intermediate, 30 min)
- **qa** (intermediate, 30 min)
- **reading-grid** (intermediate, 30 min)
- **recipe-template** (intermediate, 30 min)
- **refactor** (intermediate, 30 min)
- **refactoring-specialist** (intermediate, 30 min)
- **release-notes** (intermediate, 30 min)
- **release-notes-generator** (intermediate, 30 min)
- **remotion-quickstart** (intermediate, 30 min)
- **repo-integrity-scanner** (intermediate, 30 min)
- **report-template** (intermediate, 30 min)
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
- **test-hooks** (intermediate, 30 min)
- **test-on-change** (intermediate, 30 min)
- **test-private-key-detection** (intermediate, 30 min)
- **test-writer** (intermediate, 30 min)
- **threat-reporter** (intermediate, 30 min)
- **token-audit** (intermediate, 30 min)
- **tone-guidelines** (intermediate, 30 min)
- **tts-selective** (intermediate, 30 min)
- **twitter-template** (intermediate, 30 min)
- **typecheck-on-save** (intermediate, 30 min)
- **unicode-injection-scanner** (intermediate, 30 min)
- **update-threat-db** (intermediate, 30 min)
- **validate-changes** (intermediate, 30 min)
- **velocity-governor** (intermediate, 30 min)
- **verification-gate** (intermediate, 30 min)
- **version-output** (intermediate, 30 min)
- **voice-refine** (intermediate, 30 min)
- **web** (intermediate, 30 min)
- **week-output** (intermediate, 30 min)
- **worktree-setup** (intermediate, 30 min)

### Testing (2)

- **lean-harness-experiment** (intermediate, varies)
- **review-admission** (intermediate, varies)

---

## For beginners

Templates recommended for first-time users:

No templates explicitly marked as beginner-friendly yet.

---

## Metadata reference

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
