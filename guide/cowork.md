---
title: "Claude Cowork: Agentic Desktop for Knowledge Work"
description: "Summary of Claude's agentic desktop feature for non-technical knowledge workers"
tags: [guide, agents, workflows]
---

# Claude Cowork: Agentic Desktop for Knowledge Work

> **📦 Complete documentation migrated to dedicated repository**
> This file is a summary. For full documentation, see:
> **https://github.com/FlorianBruniaux/claude-cowork-guide**

---

## Quick Overview

**Cowork** is Claude's agentic desktop feature that extends autonomous AI capabilities to non-technical users through the Claude Desktop app. Instead of terminal commands, Cowork accesses local folders and files directly.

### Key Facts

| Aspect | Details |
|--------|---------|
| **Status** | Research preview (January 2026) |
| **Access** | Pro ($20/mo) or Max ($100-200/mo) subscription, macOS only |
| **Focus** | File manipulation, document generation, organization |
| **Difference from Code** | No code execution—files only |

---

## Three Claude Tools: Which One for You?

Three tools, one subscription ($20/mo Pro). They're complementary, not competing.

| | Claude AI | Claude Code | Cowork |
|---|-----------|-------------|--------|
| **Interface** | Web / Mobile | Terminal (CLI) | Desktop app |
| **Tagline** | You write, think, search | You code at scale | You automate without code |
| **Definition** | Generalist conversational assistant | Autonomous agent for full codebases | Agentic file workflows for non-devs |
| **Primary use cases** | Writing, brainstorming, research | Debugging, refactoring, testing | File organization, PDF extraction, cross-app workflows |
| **Executes code** | No | Yes | No |
| **File system access** | Upload only | Full | Folder sandbox |
| **Setup required** | None | npm install -g @anthropic-ai/claude-code | macOS app install |
| **Maturity** | Production | Production | Research preview |
| **Ideal profile** | Writer · Consultant · Student | Developer · Engineer · Tech Lead | Ops · Assistant · SMB non-tech |
| **Main tradeoff** | No system access | Token costs on heavy projects | macOS only, limited config |

→ [Full Cowork vs Code comparison](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/reference/comparison.md)

### Decision guide

- **Writing a doc or doing research?** → Claude AI
- **Coding: refactoring, debugging, tests?** → Claude Code (you're in the right place)
- **Organizing files, extracting PDFs, no code?** → Cowork

---

## Use Cases

- **File Organization** — Messy folders → organized structure
- **Expense Tracking** — Receipts → Excel reports
- **Report Synthesis** — Multiple docs → unified report
- **Meeting Prep** — Research → briefing documents

→ [Detailed Workflows](https://github.com/FlorianBruniaux/claude-cowork-guide/tree/main/workflows)

---

## Security Summary

No official security documentation exists yet. Essential practices:

1. **Dedicated workspace** — Never grant access to Documents/Desktop
2. **Review plans** — Check every action before approval
3. **No credentials** — Keep sensitive data out of workspace
4. **Backup first** — Before destructive operations

→ [Complete Security Guide](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/03-security.md)

---

## Documentation

| Resource | Description |
|----------|-------------|
| **[Complete Documentation](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/README.md)** | Full Cowork guide hub |
| **[Getting Started](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/01-getting-started.md)** | Setup and first workflow |
| **[Capabilities](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/02-capabilities.md)** | What Cowork can/cannot do |
| **[Prompt Library](https://github.com/FlorianBruniaux/claude-cowork-guide/tree/main/prompts)** | 50+ ready-to-use prompts |
| **[Cheatsheet](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/reference/cheatsheet.md)** | 1-page quick reference |
| **[FAQ](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/reference/faq.md)** | Common questions |

---

*Back to [AI Ecosystem Guide](./ai-ecosystem.md) | [Ultimate Guide](./ultimate-guide.md) | [Main README](../README.md)*
