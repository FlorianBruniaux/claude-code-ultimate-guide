# Context Engineering Templates

Context engineering is the practice of deliberately designing what information Claude receives at session start — treating your `CLAUDE.md` and supporting files as a production system, not a one-time setup. These templates give you everything to build, measure, and maintain that system.

## Files

| File | Description |
|------|-------------|
| `profile-template.yaml` | Developer profile for per-person context assembly |
| `skeleton-template.md` | Annotated `CLAUDE.md` skeleton with section-by-section guidance |
| `assembler.ts` | TypeScript script to build `CLAUDE.md` from profile + modules |
| `eval-questions.yaml` | 20 self-evaluation questions to audit your `CLAUDE.md` |
| `canary-check.sh` | Behavioral regression test script (structural validation) |
| `ci-drift-check.yml` | GitHub Actions workflow for weekly context drift detection |
| `context-budget-calculator.sh` | Measures always-on token cost of your context configuration |
| `rules/knowledge-feeding.md` | Rule template for proactive context updates after sessions |
| `rules/update-loop-retro.md` | Session retrospective template to capture learnings |

## Quick Start

**New project — get a working `CLAUDE.md` in 3 steps:**

```bash
# 1. Copy the skeleton and fill in your project details
cp examples/context-engineering/skeleton-template.md CLAUDE.md

# 2. Check your context budget (keep it under 10K tokens)
bash examples/context-engineering/context-budget-calculator.sh .

# 3. Run canary checks to validate structure
bash examples/context-engineering/canary-check.sh .
```

**Existing project — audit and improve:**

```bash
# Run the structural check
bash examples/context-engineering/canary-check.sh .

# Then use eval-questions.yaml to score your CLAUDE.md manually
# Target: 16+ / 20
```

**Team setup — per-developer profiles:**

```bash
# Install dependencies for the assembler
npm install js-yaml @types/js-yaml ts-node typescript

# Copy the profile template and customize
cp examples/context-engineering/profile-template.yaml .claude/profiles/yourname.yaml
# Edit .claude/profiles/yourname.yaml with your stack and preferences

# Assemble your CLAUDE.md
ts-node examples/context-engineering/assembler.ts \
  --profile .claude/profiles/yourname.yaml \
  --modules .claude/modules \
  --output CLAUDE.md
```

**Ongoing maintenance:**

```bash
# Weekly: run canary checks
bash examples/context-engineering/canary-check.sh .

# After sessions: use the retro template
# See rules/update-loop-retro.md

# Add the CI workflow for automated drift detection
cp examples/context-engineering/ci-drift-check.yml .github/workflows/context-drift.yml
```

## Guide Section

Full methodology and principles: `guide/core/context-engineering.md`

The templates here are the operational layer — the guide explains the reasoning behind each design decision.
