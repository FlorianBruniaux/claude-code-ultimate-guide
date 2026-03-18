# Claude Code — For Product Managers & Product Designers

> You don't need to become a developer to get value from Claude Code. But understanding what it does — and what it can do for you directly — changes how you work with your team and what you can ship yourself.

---

## Two distinct use cases

**1. You work alongside developers who use Claude Code**
Understanding the tool helps you write better specs, unblock faster, and have more grounded conversations about effort and trade-offs.

**2. You want to use it yourself**
"Vibe coding" is real. PMs are increasingly prototyping features, writing scripts, and generating data analyses without a developer. Claude Code makes this accessible if you're willing to learn the basics.

---

## If you work with developers who use Claude Code

### What changes for your workflow

**Specs become context** — Your PRD, acceptance criteria, and edge cases can live in a `CLAUDE.md` file at the root of a feature branch. The developer's Claude Code instance reads it automatically. Better specs = less back-and-forth.

**You can review AI-assisted work** — When a developer says "Claude wrote most of this," you can ask Claude Code to explain what was generated, why, and what the trade-offs are. No code reading required.

**Velocity expectations shift** — Boilerplate, tests, documentation, migrations: these take a fraction of the time with Claude Code. If your sprint estimates still reflect pre-AI effort, they're wrong.

### The one thing worth reading

WP05 — Deploying with a Team *(whitepaper, coming soon)* — specifically the adoption phases section. Understanding the Champion → Pilot → Team rollout pattern helps you plan feature releases that depend on the team being productive with AI tooling.

---

## If you want to use Claude Code yourself

### What you can do without coding experience

- **Prototype a feature** — describe what you want, Claude Code generates a working demo
- **Query your data** — write SQL or Python scripts by describing what you need in plain language
- **Automate repetitive tasks** — Excel → CSV → formatted report, without asking a developer
- **Generate test cases** — paste an acceptance criteria, get a test suite
- **Understand existing code** — "What does this function do?" works better than Stack Overflow for your codebase

### What you actually need to get started

1. Install Claude Code (5 min) → [Guide Ch.1.1](../guide/ultimate-guide.md#11-installation)
2. Learn the one prompt formula → [Guide Ch.2.8 — Structured Prompting](../guide/ultimate-guide.md#28-structured-prompting-with-xml-tags)
3. Understand how to give it context → [Guide Ch.3.1 — CLAUDE.md](../guide/ultimate-guide.md#31-memory-files-claudemd)

That's it for the first week.

### The learning curve is real — here's how to manage it

WP09 — Learning with AI (UVAL Protocol) *(whitepaper, coming soon)* was written specifically for this. The UVAL framework (Understand / Verify / Apply / Learn) is a structured approach to building real competency rather than copy-pasting outputs you don't understand.

Key insight: **comprehension debt** is the risk. Using Claude Code to ship features you don't understand creates fragility. The protocol helps you stay in control.

---

## What's NOT for you in this guide

This guide is primarily for developers. Most of chapters 4-9 (Agents, Skills, Hooks, MCP, Advanced Patterns) will be irrelevant to you unless you're going deep.

For general Claude productivity (writing, research, analysis, meeting prep):
→ **[Claude Cowork Guide](https://github.com/FlorianBruniaux/claude-cowork-guide)** — designed specifically for non-developers

---

## Recommended reading (30 min)

| Document | Time | If you're... |
|----------|------|-------------|
| WP09 — Learning with AI *(coming soon)* | 30 min | Considering using CC yourself |
| [Guide Ch.1.1-1.3](../guide/ultimate-guide.md#11-installation) | 20 min | Ready to install and try |
| WP05 — Team Deployment *(coming soon)* | 25 min | Working with a dev team that uses CC |

---

## Quick links

- [Claude Cowork Guide](https://github.com/FlorianBruniaux/claude-cowork-guide) — for non-dev Claude usage
- WP09 — Learning with AI *(coming soon)*
- [Guide Ch.1 — Quick Start](../guide/ultimate-guide.md#1-quick-start-day-1)
- [Cheatsheet](../guide/cheatsheet.md) — daily reference once you're started

← [Back to main README](../README.md)
