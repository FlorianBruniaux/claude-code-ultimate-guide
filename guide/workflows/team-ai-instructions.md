---
title: "Team AI Instructions Management"
description: "Scale CLAUDE.md across a multi-developer team using Profile-Based Module Assembly"
tags: [workflow, team, claude-md, configuration]
---

# Team AI Instructions Management

Manage AI instructions (CLAUDE.md, .cursorrules) across a team without fragmentation.

**Pattern**: Profile-Based Module Assembly — shared modules + per-dev profiles + automated assembler.

**When to use**: Team 5+ developers, multiple AI tools (Claude Code + Cursor/Windsurf), mixed OS.
**Skip if**: Solo developer, homogeneous team (same tool, same OS), short project (<3 months).

---

## The Problem: N x M x P Fragmentation

When a team grows, AI instructions fragment fast:

| Factor | Values | Example |
|--------|--------|---------|
| **N developers** | 5-20 | Alice, Bob, Charlie... |
| **M tools** | 2-4 | Claude Code, Cursor, Windsurf, Copilot |
| **P operating systems** | 2-3 | macOS, Linux, WSL |

**Total variants**: N x M x P = 5 x 3 x 2 = **30 possible configurations**.

Without a system, what happens:

```
Week 1: Team agrees on shared CLAUDE.md
Week 3: Alice adds TypeScript strict rules locally
Week 5: Bob copies Alice's file, removes half the rules
Week 8: New hire Charlie gets Bob's outdated copy
Week 12: 5 developers, 5 different CLAUDE.md files, nobody knows what's canonical
```

**Root cause**: CLAUDE.md is treated as a monolithic file instead of a composed configuration.

---

## Architecture Overview

```
profiles/                    modules/
├── alice.yaml               ├── core-standards.md
├── bob.yaml                 ├── git-workflow.md
├── charlie.yaml             ├── typescript-rules.md
│                            ├── test-conventions.md
│                            ├── macos-paths.md
│                            ├── linux-paths.md
│                            ├── cursor-rules.md
│                            └── communication-verbose.md
│
├── skeleton/
│   └── claude-skeleton.md   ← Template with {{MODULE:name}} placeholders
│
└── sync-ai-instructions.ts  ← Reads profile → injects modules → writes output
        │
        ▼
output/
├── alice/CLAUDE.md          ← Generated (read-only)
├── bob/CLAUDE.md
└── charlie/CLAUDE.md
```

**Flow**: Profile (YAML) + Skeleton (template) + Modules (fragments) → Assembler → Generated CLAUDE.md

---

## Phase 1: Audit Your Current CLAUDE.md

**Goal**: Classify every line as universal, conditional, or personal.

```markdown
# Audit template

## Universal (all devs, all tools)
- Architecture: hexagonal
- Tests: must pass before PR
- Naming: kebab-case for files

## Conditional (depends on tool or OS)
- Cursor: use @filename syntax → module: cursor-rules
- macOS paths: /opt/homebrew → module: macos-paths
- Linux paths: /usr/local → module: linux-paths

## Personal (individual preference)
- Style: verbose explanations → profile preference
- Language: French comments → profile preference
```

**Command to measure**:
```bash
wc -l CLAUDE.md  # Total lines before modularization
# Tag each line with [U]niversal, [C]onditional, [P]ersonal
# Count by category to estimate module split
```

**Typical result**: 60% universal, 25% conditional, 15% personal.

---

## Phase 2: Extract Modules

**Goal**: One `.md` file per thematic group.

**Recommended structure**:

```
modules/
├── core-standards.md         # Architecture, naming, patterns (all devs)
├── git-workflow.md           # Git conventions (all devs)
├── typescript-rules.md       # TS strict config (if TypeScript)
├── test-conventions.md       # Testing patterns (all devs)
├── macos-paths.md            # macOS-specific paths (if macOS)
├── linux-paths.md            # Linux paths (if Linux)
├── cursor-rules.md           # Cursor-specific rules (if Cursor)
└── communication-verbose.md  # Verbose explanation style (if preferred)
```

**Module format** (each module is a standalone Markdown fragment):

```markdown
<!-- modules/typescript-rules.md -->
## TypeScript Rules

- Use strict mode: `"strict": true` in tsconfig
- Prefer `type` over `interface` for unions
- No `any` — use `unknown` + type guards
- Zod for runtime validation at boundaries
```

**Guidelines**:
- Keep modules self-contained (no cross-references between modules)
- 15-50 lines per module is the sweet spot
- Name modules for their domain, not their audience
- One module = one reason to change

---

## Phase 3: Create Developer Profiles

**Goal**: One YAML per developer, listing their modules.

```yaml
# profiles/alice.yaml
name: "Alice"
os: "macos"
tools:
  - claude-code
  - cursor
communication_style: "concise"
modules:
  core:
    - core-standards
    - git-workflow
    - typescript-rules
    - test-conventions
  conditional:
    - macos-paths          # auto-included when os: macos
    - cursor-rules         # auto-included when cursor in tools
preferences:
  language: "english"
```

**Profile rules**:
- `core` modules: included for every dev (team standards)
- `conditional` modules: included based on `os` and `tools` fields
- `preferences`: personal settings injected into skeleton variables

**Template for new team members**: See [profile-template.yaml](../../examples/team-config/profile-template.yaml)

---

## Phase 4: Write the Assembler Script

**Goal**: Script that reads profile, injects modules, outputs CLAUDE.md.

```typescript
// sync-ai-instructions.ts (simplified ~30 lines)
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { parse } from 'yaml';
import { join } from 'path';

const profile = parse(readFileSync(`profiles/${process.argv[2]}.yaml`, 'utf8'));
let skeleton = readFileSync('skeleton/claude-skeleton.md', 'utf8');

// Collect modules from profile
const modules = [...profile.modules.core, ...profile.modules.conditional];

// Replace each placeholder with module content
for (const mod of modules) {
  const content = readFileSync(`modules/${mod}.md`, 'utf8');
  skeleton = skeleton.replace(`{{MODULE:${mod}}}`, content);
}

// Remove unused placeholders
skeleton = skeleton.replace(/\{\{MODULE:\w+\}\}/g, '');

// Write output
const outDir = `output/${process.argv[2]}`;
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'CLAUDE.md'), skeleton);
console.log(`Generated ${outDir}/CLAUDE.md (${modules.length} modules)`);
```

**Run**:
```bash
npx ts-node sync-ai-instructions.ts alice   # Single dev
npx ts-node sync-ai-instructions.ts --all   # Generate all profiles
npx ts-node sync-ai-instructions.ts --check # Verify no drift
```

Full template: [sync-script.ts](../../examples/team-config/sync-script.ts)

---

## Phase 5: CI Drift Detection

**Goal**: Catch when output files are out of sync with profiles/modules.

```yaml
# .github/workflows/ai-instructions-check.yml
name: AI Instructions Drift Check
on:
  push:
    paths:
      - 'modules/**'
      - 'profiles/**'
      - 'skeleton/**'
  schedule:
    - cron: '0 9 * * 1-5'  # Weekdays at 9am

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx ts-node sync-ai-instructions.ts --check
      - name: Fail if drift detected
        run: |
          if git diff --quiet output/; then
            echo "No drift detected"
          else
            echo "::error::AI instructions are out of sync!"
            git diff output/
            exit 1
          fi
```

**What it detects**:
- A module was edited but the assembler wasn't re-run
- A profile was added but no output CLAUDE.md exists
- A dev manually edited their generated CLAUDE.md

**Policy**: Generated files are read-only. All changes go through profiles/modules, then re-run the assembler.

---

## Phase 6: Onboarding New Developers

**Goal**: New dev gets their CLAUDE.md in under 5 minutes.

```bash
# 1. Clone repo
git clone <repo>

# 2. Copy profile template
cp examples/team-config/profile-template.yaml profiles/dave.yaml
# Edit: name, os, tools, modules

# 3. Generate
npx ts-node sync-ai-instructions.ts dave

# 4. Install
cp output/dave/CLAUDE.md .claude/CLAUDE.md
```

**CLAUDE.md placement reminder**:
- Project-wide: `project/CLAUDE.md` (committed, for team conventions)
- Personal overrides: `.claude/CLAUDE.md` (gitignored, for individual preferences)

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Generated file too long | Too many modules included | Review profile: remove rarely-used modules |
| Module missing in output | Placeholder typo in skeleton | Check `{{MODULE:name}}` matches filename |
| CI drift alert | Output not regenerated after module edit | Run `sync-ai-instructions.ts` and commit |
| Dev A has rules Dev B doesn't | Expected — it's the point | Verify profile is correct for that dev |
| Stale output after merge | Merge didn't trigger regeneration | Run assembler post-merge (add git hook) |

---

## Scaling Thresholds

| Team size | Approach |
|-----------|----------|
| 1-2 devs | Shared CLAUDE.md + precedence rules ([Section 3.4](../ultimate-guide.md#34-precedence-rules)) |
| 3-5 devs, same tools | Optional: modules only, no profiles |
| 5+ devs or multi-tool | Profile-Based Module Assembly (this workflow) |
| 20+ devs | Consider a CLAUDE.md config server + PR-based module changes |

---

## Measured Results

From a production team (5 developers, 3 tools, 2 OS):

| Metric | Before | After |
|--------|--------|-------|
| Lines per CLAUDE.md | ~380 (monolithic) | ~185 (assembled) |
| Token reduction | — | 59% less context consumed |
| Modules extracted | 0 | 12 |
| Onboarding time | "copy someone's file" | 5 min (template + generate) |
| Drift incidents | Weekly | 0 (CI catches) |

---

## Related

- [Section 3.5 Team Configuration at Scale](../ultimate-guide.md#35-team-configuration-at-scale) — Concept overview and measured results
- [Section 3.4 Precedence Rules](../ultimate-guide.md#34-precedence-rules) — How Claude reads multiple CLAUDE.md files
- [profile-template.yaml](../../examples/team-config/profile-template.yaml) — Profile template
- [claude-skeleton.md](../../examples/team-config/claude-skeleton.md) — Skeleton template
- [sync-script.ts](../../examples/team-config/sync-script.ts) — Full assembler script
