# compound-engineering (Every.to) - Resource Evaluation

**Evaluated**: 2026-03-04
**Source**: https://github.com/EveryInc/every-marketplace (plugin compound-engineering)
**Article**: https://every.to/p/the-compound-engineering-philosophy (Kieran Klaassen, Every.to)
**Type**: Claude Code Plugin (agents + commands + skills) + Engineering Philosophy
**License**: MIT
**Status**: Active — prod-tested at Every.to on Cora (their flagship AI product)

---

## Executive Summary

**Final Score**: **4/5 (HIGH VALUE)**

Compound Engineering is a production-tested engineering philosophy from Every.to, implemented as a full Claude Code plugin: 29 specialized review agents, 22 workflow commands, 20 domain skills. The philosophy formalizes a Plan → Work → Review → Compound loop with explicit 50/50 allocation between feature work and system improvement. Several patterns are absent from the guide and portable without installing the plugin: Named Perspective Agents (DHH, Kent Beck as opinion shortcuts), Swarm Mode (ad-hoc parallel reviewers), Skill Quality Gates (explicit checklist beyond frontmatter), and the Brainstorm-before-planning workflow. The multi-tool AI converter (Claude → GPT-4 → Gemini syntax) is innovative but out of scope for this guide.

---

## Resource Overview

### Plugin Structure

| Component | Count | Examples |
|-----------|-------|---------|
| Agents | 29 | DHH reviewer, Kent Beck reviewer, swarm orchestrator |
| Commands | 22 | /workflows:plan, /workflows:work, /workflows:review, /workflows:compound |
| Skills | 20 | security, performance, architecture, accessibility |
| Directory structure | 4 | docs/brainstorms/, docs/plans/, docs/solutions/, todos/ |

### Core Concepts

- **Plan → Work → Review → Compound loop**: 40% plan, 10% implement, 40% review, 10% compound
- **50/50 rule**: Half time building features, half improving the system
- **Named Perspective Agents**: Agents named after known engineers (DHH, Kent Beck) as compact opinion shortcuts
- **Swarm Mode**: On-demand parallel specialist review, no predefined team structure
- **Brainstorm-before-planning**: Check existing brainstorms before creating a plan, avoid re-solving solved problems
- **Docs-as-memory**: Structured directory hierarchy replaces ad-hoc CLAUDE.md sprawl

### Production Context

Compound Engineering runs in production at Every.to on Cora, their AI-native note-taking and knowledge product. Kieran Klaassen is a founding engineer. The patterns described come from a live codebase, not a theoretical framework.

---

## Evaluation

### Score: 4/5 (HIGH VALUE)

**Justification**:

1. **Credible source**: Every.to is a serious AI-native company. Kieran Klaassen is a practitioner, not a blogger. The plugin is open-source and contains real agents with real prompts, not marketing copy.

2. **Portable patterns**: Named Perspective Agents, Swarm Mode, Skill Quality Gates, and the Brainstorm-before-planning workflow all work with any Claude Code setup. Zero dependency on the plugin itself.

3. **Real implementation**: 29 agents means 29 actual system prompts you can read and learn from. Most Claude Code content describes patterns without showing real implementations. This one shows the code.

4. **Novel patterns**: Named Perspective Agents and Swarm Mode are not documented anywhere in the current guide. Both are immediately applicable and distinct from existing patterns (scope-focused agents, agent teams).

5. **Philosophy depth**: The 50/50 allocation rule and the adoption ladder (stages 0-5) are concrete decision tools, not vague recommendations.

**Why not 5/5**:

- No quantified metrics — no "X% improvement" in shipping velocity, review catch rate, or defect rate. All claims are qualitative.
- Named Perspective Agents are opinion-based — whether a DHH agent reliably encodes "fat models, thin controllers" depends on Claude's training, which varies by version.
- Several agents are short (<20 lines) and may not be more effective than a well-crafted inline prompt.
- The multi-tool AI converter is the most novel feature but is completely out of scope for this guide.

### Caveats

- **Named personas risk drift**: DHH's opinions evolve. A static "DHH agent" may become outdated or diverge from his current thinking as Claude's training data shifts.
- **Swarm vs Teams**: Swarm Mode (ad-hoc) and Agent Teams (persistent, coordinated) solve different problems. Conflating them is a common confusion point.
- **Plugin install not required**: Installing the plugin adds 29 agents + 22 commands to every project, which may be excessive. The patterns work without it.

---

## Portable Patterns

### 1. Named Perspective Agents

Instead of generic "reviewer" agents, name agents after engineers whose views you want represented:

```markdown
---
name: dhh-reviewer
description: Review code from DHH's perspective (Rails conventions, fat models, thin controllers, pragmatic REST)
---
```

The name serves as a compressed prompt — it bundles a recognizable set of opinions into a single token rather than spelling them out. Works for: DHH (Rails, REST), Kent Beck (TDD, simplicity), Martin Fowler (refactoring, patterns).

**Constraint**: Only works for engineers whose views Claude has been trained on and whose opinions map to a distinct, stable style.

### 2. Swarm Mode

On-demand parallel review across multiple specialists, without predefined coordination:

```bash
/slfg                      # Start swarm
/workflows:review --swarm  # Launch all relevant reviewers in parallel
```

Unlike Agent Teams (which have a persistent lead + member structure), swarm is stateless: each reviewer gets the PR/diff independently, reports findings, and the human synthesizes. Best for: final review before merge, unfamiliar codebase areas, thoroughness over coordination.

### 3. Skill Quality Gates

Beyond frontmatter validation, Compound Engineering defines explicit content quality criteria for skills:

- Frontmatter must include name, description, allowed-tools
- "When to Apply" section is required (not optional)
- Methodology must be structured (steps, not paragraphs)
- No TODOs or placeholder language
- allowed-tools scoped to minimum necessary
- Output format must be documented
- No AskUserQuestion in cross-platform skills

### 4. Brainstorm-before-planning Workflow

Before creating a plan, check if a brainstorm already exists:

```
docs/brainstorms/    <- Thinking documents (problem exploration)
docs/plans/          <- Active implementation plans
docs/solutions/      <- Solved problems with context
todos/               <- Task tracking
```

Agent instruction: "Before creating a plan for X, check docs/brainstorms/ for existing thinking on this topic."

---

## Gap Analysis

### Current Guide Coverage (Before Integration)

| Pattern | Coverage |
|---------|---------|
| Compound Engineering philosophy | Partial (added in recent release, loop + plugin) |
| Named Perspective Agents | Not documented |
| Swarm Mode | Not documented |
| Skill Quality Gates (content criteria) | Not documented (frontmatter validation only) |
| Brainstorm-before-planning workflow | Not documented |
| Docs directory hierarchy (brainstorms/plans/) | Partial (solutions/ mentioned, not the full hierarchy) |

### Post-Integration Target

- Named Perspective Agents: subsection after Pat Cullen Multi-Agent Code Review example
- Swarm vs Sequential: comparison table after Agent Teams decision tree
- Skill Quality Gates: checklist after "Validating Skills" section
- Compound Engineering expansion: brainstorm workflow + docs hierarchy added to existing CE section

---

## Integration Details

### Placement

| Insert | Section | After |
|--------|---------|-------|
| 1A Named Perspective | 3.x Multi-Agent | Pat Cullen example (~l.6406) |
| 1B Swarm vs Sequential | 9.20 Agent Teams | Decision tree (~l.19643) |
| 1C Skill Quality Gates | 5.2 Skills | Validating Skills (~l.6720) |
| 1D CE Expansion | 3.x CE Philosophy | Plugin paragraph (~l.4455) |

### reference.yaml keys to add

```yaml
named_perspective_agents: "guide/ultimate-guide.md:XXXX"
swarm_mode: "guide/ultimate-guide.md:XXXX"
skill_quality_gates: "guide/ultimate-guide.md:XXXX"
compound_engineering_brainstorm: "guide/ultimate-guide.md:XXXX"
compound_engineering_source: "https://every.to/p/the-compound-engineering-philosophy"
compound_engineering_score: "4/5 HIGH VALUE - 2026-03-04"
```

---

## Sources

| Source | Type | Date |
|--------|------|------|
| [every.to compound-engineering article](https://every.to/p/the-compound-engineering-philosophy) | Primary — authored by Kieran Klaassen | 2026 |
| [EveryInc/every-marketplace](https://github.com/EveryInc/every-marketplace) | Plugin source (agents, commands, skills) | 2026-03-04 |
| Every.to Cora product | Production context | Ongoing |

---

**End of Evaluation**
