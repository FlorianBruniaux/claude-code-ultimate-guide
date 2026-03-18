---
title: "Design-to-Code Workflow with Figma MCP"
description: "Automated design system implementation using Figma MCP Server for 1:1 design-code parity"
tags: [workflow, mcp, integration]
---

# Design-to-Code Workflow with Figma MCP

> **Confidence**: Tier 2 — Based on documented production case studies (Parallel HQ, builder.io), MCP server specifications, and community workflows.

Automated design system implementation using Figma MCP Server enables Product Designers to hand off production-ready specifications to Claude Code, which implements components maintaining 1:1 design-code parity.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [Documented Impact](#documented-impact)
3. [Architecture Overview](#architecture-overview)
4. [3-Tier Token Hierarchy](#3-tier-token-hierarchy)
5. [Prerequisites](#prerequisites)
6. [Core Workflows](#core-workflows)
7. [Code Connect Setup](#code-connect-setup)
8. [Example Prompts](#example-prompts)
9. [Team Adoption Patterns](#team-adoption-patterns)
10. [Anti-Patterns](#anti-patterns)
11. [Implementation Roadmap](#implementation-roadmap)
12. [Resources](#resources)

---

## TL;DR

```
Designer (Figma Make) → Export (Figma Design) → Claude (Figma MCP) → Production Code

Key insight: Design system = source of truth
Claude consumes tokens/components directly from Figma
Implementation maintains design parity automatically
```

---

## Documented Impact

Based on production case studies from January 2026:

| Metric | Improvement | Source |
|--------|-------------|--------|
| Design inconsistencies | 62% reduction | Parallel HQ study |
| Workflow efficiency | 78% improvement | builder.io case study |
| Engineering time saved | 75 days (6 months) | Parallel HQ production data |
| Time-to-market | 56% reduction | Multi-org composite |
| Design technical debt | 82% reduction | Post-implementation audit |

**Typical workflow timing**:
- Single frame → Production component: 2-3 minutes
- Design system drift audit: 3 weeks → 3 minutes
- Token update propagation: Manual hours → Automated seconds

*Sources: builder.io/blog/claude-code-figma-mcp-server, parallelhq.com/blog/automating-design-systems-with-ai, composio.dev/blog/how-to-use-figma-mcp-with-claude-code*

---

## Architecture Overview

### Full Stack

```
[Figma Design File]
    ↓ (Variables & Styles)
[Tokens Studio Plugin] (optional but recommended)
    ↓ (JSON export)
[GitHub Repository]
    ↓ (CI/CD)
[Style Dictionary]
    ↓ (Transform)
[CSS Custom Properties / Tailwind Config]
    ↓ (Consumed by)
[Component Library]
    ↑ (Reads via)
[Claude Code + Figma MCP]
```

### MCP Integration Point

Claude Code accesses Figma through the Figma MCP Server:

```
Claude Code
    ↓ (uses)
Figma MCP Server (mcp-server-figma)
    ↓ (authenticates via)
Figma Personal Access Token
    ↓ (reads)
Figma File (Dev Mode data)
```

**What Claude can access**:
- File structure and frames
- Color/text/effect styles
- Component properties
- Variables (tokens)
- Dev Mode annotations
- Code Connect snippets (if configured)

**What Claude cannot access**:
- Private files without token permissions
- Edit capabilities (read-only)
- Real-time collaboration data
- Version history (only current state)

---

## 3-Tier Token Hierarchy

Modern design systems use a hierarchical token structure. Claude Code understands this hierarchy when consuming Figma data.

| Tier | Definition | Figma Implementation | Code Output |
|------|------------|----------------------|-------------|
| **Base** | Primitive values | Figma Variables (e.g., `blue-600: #0066CC`, `spacing-2: 8px`) | CSS custom properties (`--blue-600`, `--spacing-2`) |
| **Composite** | Combined primitives | Component fills referencing variables | Tailwind config or CSS classes |
| **Semantic** | Contextual meaning | Contextual variable aliases (e.g., `color-interactive-primary` → `blue-600`) | Component props or theme tokens |

### Example Hierarchy

```
Base:
  --color-blue-600: #0066CC
  --spacing-2: 8px
  --radius-md: 4px

Composite:
  --button-padding: var(--spacing-2) var(--spacing-4)
  --button-border-radius: var(--radius-md)

Semantic:
  --interactive-primary: var(--color-blue-600)
  --interactive-primary-hover: var(--color-blue-700)
```

**Claude Code behavior**: When given a Figma component, Claude:
1. Extracts referenced variables (base tier)
2. Identifies composite patterns (spacing, sizing)
3. Applies semantic naming from your token conventions
4. Generates code matching this hierarchy

---

## Prerequisites

### For Designers

| Requirement | Details |
|-------------|---------|
| **Figma License** | Dev Mode seat (enables variable inspection, code snippets) |
| **Organized Variables** | Use Figma Variables or Tokens Studio plugin for token management |
| **Component Structure** | Auto Layout, named layers, consistent naming conventions |
| **Frame Naming** | Descriptive frame names (Claude uses these for component names) |

### For Developers

| Requirement | Details |
|-------------|---------|
| **Claude Code** | Version 1.5.0+ (MCP support) |
| **Figma MCP Server** | `npm install -g @modelcontextprotocol/server-figma` |
| **Personal Access Token** | Generated from Figma account settings → Tokens |
| **MCP Configuration** | Token configured in Claude Code settings |

### MCP Configuration

Add to your Claude Code MCP settings (`.claude/mcp.json` or settings UI):

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-figma"],
      "env": {
        "FIGMA_PERSONAL_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

**Security note**: Use environment variables for production:
```json
{
  "env": {
    "FIGMA_PERSONAL_ACCESS_TOKEN": "${FIGMA_TOKEN}"
  }
}
```

Then export in your shell: `export FIGMA_TOKEN="figd_..."`

---

## Core Workflows

### Workflow A: Single Frame → Production Component

**Timing**: 2-3 minutes per component

**Steps**:

1. **Designer**: Create component in Figma with proper variables/styles
2. **Designer**: Share Figma file URL with dev/Claude
3. **Developer**: Prompt Claude Code:

```
Read the "Button/Primary" component from Figma file:
https://www.figma.com/design/FILE_KEY

Implement as a React component with TypeScript.
Use Tailwind for styling, mapping Figma variables to our design tokens.
Ensure responsive behavior matches Figma's Auto Layout constraints.
```

4. **Claude**:
   - Fetches component via Figma MCP
   - Extracts styles, dimensions, spacing
   - Maps variables to code tokens
   - Generates component with props matching Figma variants

5. **Verification**: `npm run dev` → Visual comparison against Figma

**Example output**:
```tsx
// components/Button/Primary.tsx
interface ButtonProps {
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: React.ReactNode;
}

export function PrimaryButton({ size = 'md', disabled, children }: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-md font-medium transition-colors',
        'bg-interactive-primary text-white',
        'hover:bg-interactive-primary-hover',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        {
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        }
      )}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
```

---

### Workflow B: Design System Drift Audit

**Timing**: 3 weeks manual review → 3 minutes automated

**Problem**: Over time, code diverges from design system (magic numbers, hardcoded colors, inconsistent spacing).

**Solution**: Claude audits codebase against Figma source of truth.

**Prompt**:
```
Audit src/components for design system compliance.
Compare against our Figma design system:
https://www.figma.com/design/FILE_KEY

Report:
1. Hardcoded colors not using design tokens
2. Magic number spacing values
3. Components not matching Figma structure
4. Missing responsive patterns

Then propose fixes with token replacements.
```

**Claude output**:
```markdown
## Design System Audit Results

### Issues Found (23 total)

#### Hardcoded Colors (8 instances)
- `src/components/Card.tsx:45` → `#0066CC` should be `var(--interactive-primary)`
- `src/components/Header.tsx:12` → `#F3F4F6` should be `var(--surface-secondary)`
...

#### Magic Numbers (11 instances)
- `src/components/Modal.tsx:23` → `padding: 16px 24px` should be `var(--spacing-4) var(--spacing-6)`
...

#### Structural Mismatches (4 instances)
- `src/components/Button.tsx` → Missing `icon-left` variant present in Figma
...
```

---

### Workflow C: Token Automation Pipeline

**Goal**: Figma variable changes automatically propagate to code.

**Architecture**:

```
Figma Variables
    ↓ (Tokens Studio export or Figma API)
GitHub Repository (tokens.json)
    ↓ (GitHub Actions CI/CD)
Style Dictionary Transform
    ↓ (generates)
CSS / Tailwind / Platform-specific tokens
    ↓ (commit & deploy)
Production
```

**Setup** (one-time):

1. **Tokens Studio Plugin**: Connect to GitHub repo
2. **Style Dictionary Config**: Define transform rules
3. **GitHub Actions**: Auto-run on token updates
4. **Claude Role**: Review and validate generated tokens

**Developer Prompt** (after CI runs):
```
Review the token update from commit abc1234.
Check if any components need updates to consume new tokens.
Generate migration guide if breaking changes exist.
```

**Claude output**:
```markdown
## Token Update Review (v2.3.0 → v2.4.0)

### Changes
- Added: `--spacing-7`, `--spacing-8` (requested by design)
- Changed: `--interactive-secondary` hue shift 5° (brand refresh)
- Deprecated: `--legacy-blue` (remove by Q3)

### Impact Analysis
- 12 components reference `--interactive-secondary` → Auto-updated via token reference
- 3 components use deprecated `--legacy-blue` → Migration needed

### Migration Required
1. `src/components/LegacyButton.tsx:34` → Replace `--legacy-blue` with `--interactive-primary`
2. `src/components/OldCard.tsx:67` → Replace with new token
3. `src/utils/theme.ts:12` → Update theme export

### Migration Script
[Claude generates codemod or find/replace script]
```

---

### Workflow D: Visual Iteration Loop (Figma + Playwright)

**Goal**: Automated visual regression testing against Figma designs.

**MCP Stack**: Figma MCP + Playwright MCP

**Setup**:
```
Claude Code accesses:
- Figma (design source of truth)
- Playwright (automated browser testing)
```

**Prompt**:
```
Take a screenshot of our Button component in all variants.
Compare against Figma frames from:
https://www.figma.com/design/FILE_KEY → "Button Tests" page

Report any visual differences (color, spacing, typography).
```

**Workflow**:
1. Claude reads Figma frames (expected state)
2. Claude uses Playwright to screenshot live components (actual state)
3. Claude compares (pixel diff or visual inspection)
4. Reports discrepancies with fix suggestions

**Example output**:
```markdown
## Visual Regression Report

### ✅ Matching (5/7)
- Button/Primary/Default
- Button/Primary/Hover
- Button/Secondary/Default
...

### ❌ Mismatches (2/7)

#### Button/Primary/Disabled
- **Issue**: Text opacity 0.4 in code, 0.5 in Figma
- **Fix**: Update `disabled:opacity-50` → `disabled:opacity-40`
- **File**: `src/components/Button.tsx:23`

#### Button/Large
- **Issue**: Padding 12px in code, 16px in Figma
- **Fix**: Update `py-3` → `py-4` (16px)
- **File**: `src/components/Button.tsx:18`
```

---

## Code Connect Setup

**Code Connect** is Figma's no-code tool for linking design components to code snippets. This enhances Claude's ability to generate correct code.

### What It Does

- Designers annotate Figma components with code examples
- Claude reads these annotations via MCP
- Generated code matches team conventions automatically

### Setup (for Designers)

1. In Figma Dev Mode → Select component → Code Connect panel
2. Add code snippet showing how component is used:

```tsx
// Example Code Connect annotation in Figma
<Button variant="primary" size="lg">
  Click me
</Button>
```

3. Claude sees this when asked to implement, uses team's exact patterns

### Benefits

| Without Code Connect | With Code Connect |
|---------------------|-------------------|
| Claude generates generic code | Claude uses team conventions |
| Prop naming inconsistent | Props match Figma variants exactly |
| Requires manual correction | Production-ready first pass |

**Reference**: Read more at parallelhq.com/blog (Code Connect UI article)

---

## Alternative: Pencil (IDE-Native Canvas)

**Overview**: [Pencil](https://pencil.dev) brings infinite design canvas directly into Claude Code/Cursor/VSCode, eliminating external tool switching and enabling design-as-code workflows.

### Architecture

**Core Innovation**: Unlike Figma (cloud-based) or Excalidraw (standalone), Pencil embeds the design canvas directly in your IDE where Claude and your code live.

```
Traditional Workflow:
Figma (design) → Export → Claude Code → Implementation → Manual sync

Pencil Workflow:
IDE Canvas (design + AI agents + code) → Git commit → Continuous alignment
```

**Key Features**:
- **WebGL Canvas**: Infinite, performant, fully editable
- **AI Multiplayer Agents**: Parallel agents process design collaboratively
- **Git-Native**: `.pen` files (JSON format) version-controlled alongside code
- **MCP Bi-Directional**: Full read+write access (not just read like Figma MCP)
- **Figma Import**: Copy-paste directly from Figma preserving vectors and styles

### Pencil vs. Figma MCP

| Aspect | Pencil | Figma MCP |
|--------|--------|-----------|
| **Location** | IDE-native (Cursor/VSCode/Claude Code) | External cloud |
| **Format** | `.pen` JSON (open) | Proprietary binary |
| **Versioning** | Git-native (branch/merge/history) | Figma cloud versions |
| **AI Agents** | Multiplayer parallel | Single-threaded via MCP |
| **Collaboration** | Code-first (developers + designers) | Design-first (designers + devs) |
| **MCP Access** | Bi-directional (read+write) | Read-only |
| **Workflow** | Design → Commit → Code in same env | Design → Export → Handoff → Code |
| **Best For** | Engineer-designers, code-centric teams | Traditional design-dev separation |
| **Maturity** | Emerging (launched Jan 2026) | Mature (2024+) |
| **Pricing** | Currently free, TBD future | Freemium (free tier available) |

### When to Use Pencil

✅ **Good Fit**:
- Team uses Cursor or VSCode + Claude Code as primary environment
- Engineer-designers comfortable with terminal/IDE workflows
- Projects requiring tight design-code alignment (design-as-code paradigm)
- Desire for git-native design versioning (branch protection, rollback, etc.)
- Want to leverage parallel AI agents for design automation

⚠️ **Consider Carefully**:
- Traditional design team (non-technical) → Figma may be better
- Need enterprise SLA/support → Pencil still maturing
- Complex design system with 50+ components → Figma ecosystem more mature
- Team not using Cursor/VSCode → Limited compatibility

### Setup

1. **Install Pencil extension**:
   - Visit [pencil.dev](https://pencil.dev)
   - Follow installation for Cursor/VSCode/Claude Code
   - Create account (currently free)

2. **Create first canvas**:
   ```bash
   # Open IDE, launch Pencil extension
   # Create new .pen file in your repo
   # Design on infinite canvas
   ```

3. **Git workflow**:
   ```bash
   git add design/homepage.pen
   git commit -m "feat(design): add homepage hero section"
   git push
   ```

4. **Claude integration**:
   - Claude can read .pen files via MCP
   - Prompt: "Implement the Button component from design/components.pen"
   - Claude extracts design specs and generates code

### Example Prompt

```
Read the "Hero Section" from design/homepage.pen.

Implement as React component with:
- Responsive behavior matching canvas breakpoints
- Animations from design (fade-in, slide-up)
- Copy exactly as specified in canvas
- Use Tailwind for styling

Ensure pixel-perfect match with design specs.
```

### Founder & Backing

**Tom Krcha** (CEO, Pencil):
- Co-founder Adobe XD (2014-2018), 10 years at Adobe
- Prior exits: Alter Avatars (acquired by Google), Around (acquired by Miro)
- 14+ years development experience

**Funding**: a16z Speedrun (~$1M) + KAYA VC

**Traction**: 1M+ views on launch, thousands of signups including Microsoft, Shopify, Uber executives.

### Maturity Note

**⚠️ Status**: Launched January 2026 (very recent). Strong early signals but documentation and ecosystem still maturing.

**Recommendations**:
- **Production projects**: Pilot with 1-2 non-critical features first
- **New projects**: Safe to adopt for teams on Cursor/Claude Code
- **Traditional workflows**: Stick with Figma MCP until Pencil matures (3-6 months)

**Monitor**: Pricing announcement, public GitHub repo, mature documentation expected Q2 2026.

---

## Example Prompts

### Component Implementation
```
Implement the "Card/Product" component from our Figma design system:
[Figma URL]

Requirements:
- Use our existing design tokens from tailwind.config.ts
- Include hover states matching Figma interactions
- Implement all variants (default, featured, compact)
- Add TypeScript types for all props
```

### Design System Expansion
```
Our design team added a new "Badge" component to Figma:
[Figma URL → Badge frame]

Generate:
1. React component with all variants
2. Storybook stories
3. Unit tests for prop combinations
4. Update design system docs
```

### Token Validation
```
Compare the color tokens in our Tailwind config against
Figma variables from: [Figma URL]

Report any mismatches and generate update script.
```

### Responsive Implementation
```
Implement the "Hero" section from Figma with exact responsive behavior:
[Figma URL → Hero/Responsive frame]

Figma has 3 breakpoints configured. Match these precisely.
```

### Accessibility Audit
```
Review the "Modal" component implementation against Figma specs:
[Figma URL]

Check:
- Focus management matches Figma's interaction flow
- Color contrast meets WCAG AA (Figma has contrast checker)
- Keyboard navigation (Figma annotations specify tab order)
```

### Design QA Before Handoff
```
Review the "Checkout Flow" frames for implementation readiness:
[Figma URL → Checkout Flow page]

Check:
- All interactive states defined (hover, focus, disabled, error)
- Variables used consistently (no magic values)
- Auto Layout constraints are implementable
- Missing anything needed for production code?
```

### Multi-Component Atomic Implementation
```
Implement the atomic design system components in order:

1. Atoms: [Figma URL → Atoms page]
   - Button, Input, Label, Badge

2. Molecules: [Figma URL → Molecules page]
   - FormField (Label + Input + Error)
   - SearchBar (Input + Button)

3. Organisms: [Figma URL → Organisms page]
   - LoginForm (using molecules)

Ensure each level only imports from lower levels.
```

---

## Team Adoption Patterns

### For Product Designers

**New workflow**:
1. Design in Figma with proper variable structure
2. Use Figma Make for rapid prototyping
3. Export to Figma Design with Dev Mode enabled
4. Share file URL + specific frames with dev team
5. Claude consumes design → Generates implementation
6. Designer reviews code output visually (not reading code)

**Key insight**: Designers don't need to learn code. They review implementation by visual comparison against Figma.

### For Developers

**New workflow**:
1. Receive Figma URL from designer
2. Prompt Claude to implement from Figma source
3. Review generated code for architecture fit
4. Run visual comparison (Playwright or manual)
5. Commit production-ready component

**Time saved**: Skip manual pixel-perfect implementation. Focus on logic, not layout matching.

### For Product Managers

**New capability**: Request design implementation estimates based on Figma frames.

**Prompt for PMs**:
```
Review the "Dashboard Redesign" Figma file:
[Figma URL]

Estimate implementation complexity:
- How many new components needed?
- Which existing components can be reused?
- Any technical blockers?

Provide rough timeline for dev implementation.
```

Claude output:
```markdown
## Implementation Analysis

### Scope
- 12 frames total
- 4 new components (DataTable, MetricCard, FilterPanel, DateRangePicker)
- 8 existing components reused

### Complexity Assessment
- **Low**: MetricCard (similar to existing Card, 1-2h)
- **Medium**: FilterPanel (multi-select logic, 4-6h)
- **High**: DataTable (sorting, pagination, virtualization, 2-3 days)
- **High**: DateRangePicker (third-party library integration, 1-2 days)

### Technical Considerations
- DataTable needs backend API for server-side pagination
- DateRangePicker: evaluate date-fns vs dayjs vs native
- FilterPanel state management (local vs global)

### Estimated Timeline
- Development: 5-7 days
- Code review + QA: 2 days
- Total: 1.5-2 weeks
```

---

## Anti-Patterns

| ❌ Anti-Pattern | Why It Fails | ✅ Correct Approach |
|----------------|-------------|-------------------|
| **Manual design transcription** | Error-prone, time-consuming, drift inevitable | Let Claude read Figma directly via MCP |
| **Screenshots as specs** | No token data, no interactivity, ambiguous | Share Figma URLs, let Claude access structured data |
| **Hardcoded values** | Breaks when design system updates | Use design tokens from Figma variables |
| **Designer codes** | Inefficient use of designer skills | Designer designs → Claude codes → Dev reviews |
| **Developer guesses spacing** | Inconsistent with design system | Claude extracts exact values from Figma |
| **No Code Connect annotations** | Generic code output | Annotate once → Claude uses team conventions |
| **Skipping visual comparison** | Implementation drift | Always verify against Figma source |
| **Token naming mismatch** | Figma variables ≠ code tokens | Establish naming convention, use Style Dictionary |
| **Missing responsive specs** | Developer guesses breakpoints | Figma has responsive frames → Claude reads exact specs |
| **Single-tier tokens** | Inflexible, hard to theme | Use 3-tier hierarchy (base/composite/semantic) |

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**Goal**: Basic Figma → Claude → Code pipeline

- [ ] Install Figma MCP Server
- [ ] Configure personal access token
- [ ] Test connection: Claude reads public Figma file
- [ ] Create project CLAUDE.md with design system conventions
- [ ] Implement 3-5 simple components (Button, Input, Badge)
- [ ] Establish visual QA process (manual comparison)

**Success criteria**:
- Claude generates component from Figma URL
- Output matches design visually
- Dev team understands workflow

---

### Phase 2: Scaling (Week 3-4)

**Goal**: Full design system implementation + automation

- [ ] Implement 20+ components from Figma library
- [ ] Set up token automation (Tokens Studio + Style Dictionary)
- [ ] Create component testing suite (Storybook + visual regression)
- [ ] Train designers on variable hygiene
- [ ] Document team conventions in CLAUDE.md
- [ ] Run first design system drift audit

**Success criteria**:
- 80%+ of UI components auto-generated
- Token updates propagate automatically
- Designers confident in handoff process

---

### Phase 3: Orchestration (Week 5+)

**Goal**: Multi-MCP workflows + continuous sync

- [ ] Integrate Playwright MCP for automated visual testing
- [ ] Set up CI/CD for design-code parity checks
- [ ] Create Figma → GitHub → Production pipeline
- [ ] Implement design system governance (linting, audits)
- [ ] Enable non-devs to trigger Claude implementations (tickets, Slack)
- [ ] Measure metrics (TTM, inconsistency rate, dev time saved)

**Success criteria**:
- Design updates → Production in <1 day
- Zero manual design transcription
- Measurable team velocity increase

---

## Resources

### Official Documentation

- **Figma MCP Server**: [@modelcontextprotocol/server-figma](https://github.com/modelcontextprotocol/servers/tree/main/src/figma) (GitHub)
- **Figma Developer Docs**: [figma.com/developers](https://www.figma.com/developers)
- **Style Dictionary**: [amzn.github.io/style-dictionary](https://amzn.github.io/style-dictionary/)
- **Tokens Studio Plugin**: [tokens.studio](https://tokens.studio/)

### Case Studies & Tutorials

- **builder.io**: "Claude Code + Figma MCP Server: AI Design-to-Code Workflow" (January 2026)
  - [builder.io/blog/claude-code-figma-mcp-server](https://www.builder.io/blog/claude-code-figma-mcp-server)
  - Production metrics, workflow examples

- **Vladimir Siedykh**: "Multi-MCP Orchestration with Claude Code"
  - [vladimirsiedykh.com/blog/claude-code-mcp-workflow](https://vladimirsiedykh.com/)
  - Figma + Playwright + Linear integration

- **Parallel HQ**: "Automating Design Systems with AI"
  - [parallelhq.com/blog/automating-design-systems-with-ai](https://parallelhq.com/)
  - 75 days saved, Code Connect UI guide

- **Composio**: "How to Use Figma MCP with Claude Code"
  - [composio.dev/blog/how-to-use-figma-mcp-with-claude-code](https://composio.dev/)
  - Token hierarchy patterns, setup guide

### Community Resources

- **Figma Community**: Search "Design System Tokens" for starter templates
- **MCP Registry**: [mcp.run](https://mcp.run/) → Figma server examples
- **Discord**: Anthropic Discord → #mcp-servers channel

### Related Workflows

- [Working with Images](../ultimate-guide.md#24-working-with-images) — Claude Code image analysis
- [ASCII Art & Wireframing](../ultimate-guide.md#wireframing-tools) — Low-fidelity design iteration
- [Playwright MCP](../ultimate-guide.md#playwright-mcp) — Visual regression testing

---

## See Also

- [../ultimate-guide.md#figma-mcp](../ultimate-guide.md) — Main guide Figma MCP section
- [examples/claude-md/product-designer.md](../../examples/claude-md/product-designer.md) — Product Designer CLAUDE.md template
- [../cheatsheet.md](../cheatsheet.md) — Quick reference
