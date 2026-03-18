---
title: "Product Designer CLAUDE.md Template"
description: "CLAUDE.md configuration for design-to-code workflows using Figma MCP"
tags: [claude-md, template, design-patterns, mcp]
---

# Product Designer CLAUDE.md Template

A CLAUDE.md configuration optimized for design-to-code workflows using Figma MCP.

## Usage

Copy this content to your project's `CLAUDE.md` file and customize the sections marked with `[brackets]`.

---

## Template

```markdown
# Product Designer Project Configuration

## Design System Source

### Figma Files
- Design System Library: [Figma file URL]
- Component Library: [Figma file URL]
- Current Project: [Figma file URL]

### Access
- Figma MCP configured: Yes/No
- Personal Access Token: [Configured in MCP settings - never share value]
- Dev Mode access: [Required for full variable inspection]

## Token Hierarchy

Our design tokens follow a 3-tier structure:

### Base Tokens (Primitives)
Figma Variables → CSS Custom Properties
- Colors: `--blue-600`, `--gray-100`, etc.
- Spacing: `--spacing-1` (4px), `--spacing-2` (8px), etc.
- Typography: `--font-size-sm`, `--font-weight-medium`, etc.
- Radii: `--radius-sm`, `--radius-md`, etc.

### Composite Tokens
Combined primitives used in components
- Button padding: `var(--spacing-2) var(--spacing-4)`
- Card shadow: `var(--shadow-md)`
- Input border: `var(--border-width-1) solid var(--border-default)`

### Semantic Tokens
Context-specific meaning
- `--interactive-primary`: Main action color
- `--surface-elevated`: Card/modal backgrounds
- `--text-secondary`: Descriptive text
- `--border-error`: Form validation

## Design Rules

### Colors
- Primary: [#HEX] → `var(--interactive-primary)`
- Secondary: [#HEX] → `var(--interactive-secondary)`
- Never use: Hardcoded hex values in components
- Always use: Design token variables

### Spacing
- Base unit: [4px/8px]
- Scale: [4, 8, 12, 16, 24, 32, 48, 64, 96]
- Never use: Magic numbers (e.g., `padding: 13px`)
- Always use: Token multiples (e.g., `var(--spacing-3)`)

### Typography
- Font family: [Inter/Roboto/System/Custom]
- Scale: [12, 14, 16, 18, 20, 24, 32, 48, 64]
- Line heights: [1.2, 1.5, 1.6] depending on text size
- Letter spacing: Follow Figma text styles exactly

### Responsive Breakpoints
Match Figma frame sizes:
- Mobile: [320-767px]
- Tablet: [768-1023px]
- Desktop: [1024px+]
- Max width: [1440px]

## Figma MCP Commands

When I share a Figma URL, you can use these MCP commands:

### Reading Design Files
```
figma_get_file(file_key: string)
→ Returns: File structure, pages, frames
```

### Extracting Styles
```
figma_get_styles(file_key: string)
→ Returns: Color styles, text styles, effect styles
```

### Fetching Components
```
figma_get_component(file_key: string, node_id: string)
→ Returns: Component properties, variants, design tokens
```

### Variables (Design Tokens)
```
figma_get_variables(file_key: string)
→ Returns: All Figma variables (primitives)
```

## Code Connect Mappings

We use Figma Code Connect to link designs to code. When implementing components, reference these mappings:

| Figma Component | Code Path | Notes |
|-----------------|-----------|-------|
| Button/Primary | `components/Button/Primary.tsx` | Uses `PrimaryButton` component |
| Input/Text | `components/Input/Text.tsx` | Supports error states |
| Card/Default | `components/Card/index.tsx` | Auto Layout → Flexbox |
| Modal/Standard | `components/Modal/Standard.tsx` | Focus trap + A11y |

[Add your mappings here]

## Implementation Constraints

### Technology Stack
- Framework: [React/Vue/Svelte/Angular]
- Styling: [Tailwind/CSS Modules/Styled Components/CSS-in-JS]
- TypeScript: [Required/Optional]
- Component library: [Building custom / Using MUI/Chakra/etc.]

### Patterns
- Component structure: [Atomic Design / Feature-based / Flat]
- State management: [useState / Context / Redux / Zustand]
- Props naming: [Match Figma variants exactly]

### Quality Requirements
- TypeScript types for all props
- Accessible by default (WCAG AA minimum)
- Responsive behavior matching Figma frames
- Hover/focus/disabled states from Figma

## Design Handoff Checklist

When you implement a component from Figma, verify:

### Design Match
- [ ] Colors match Figma exactly (use browser DevTools color picker)
- [ ] Spacing matches Figma measurements
- [ ] Typography (size, weight, line-height) matches
- [ ] Border radius matches
- [ ] Shadows/effects match

### Tokens
- [ ] No hardcoded colors (all use `var(--token-name)`)
- [ ] No magic number spacing
- [ ] Font sizes use design tokens
- [ ] All values traceable to design system

### Responsive
- [ ] Mobile breakpoint implemented
- [ ] Tablet breakpoint implemented
- [ ] Desktop layout matches
- [ ] No horizontal scroll on mobile

### Accessibility
- [ ] Keyboard navigation works
- [ ] Focus states visible
- [ ] ARIA labels present where needed
- [ ] Color contrast passes WCAG AA
- [ ] Screen reader tested (if interactive)

### States
- [ ] Default state implemented
- [ ] Hover state matches Figma
- [ ] Focus state matches Figma
- [ ] Disabled state matches Figma
- [ ] Error state (if applicable)
- [ ] Loading state (if applicable)

## Response Preferences

### For Component Implementation
1. Read Figma component via MCP
2. Extract all variants and properties
3. Map design tokens to code tokens
4. Generate TypeScript component with full types
5. Include Storybook story (if we use Storybook)
6. Verify against checklist above

### For Design System Audits
1. Compare codebase against Figma source of truth
2. Report hardcoded values (colors, spacing, etc.)
3. Flag inconsistencies (missing variants, wrong tokens)
4. Propose automated fixes

### For Token Updates
1. When design tokens change in Figma, notify about affected components
2. Generate migration script if breaking changes
3. Verify no hardcoded values will break

## Team Conventions

### Commit Messages
- Format: `feat(ui): add Button component from Figma`
- Reference Figma frame: `feat(ui): implement Modal (Figma frame: abc123)`

### PR Requirements
- [ ] Screenshot comparison (code vs Figma)
- [ ] All checklist items verified
- [ ] Responsive behavior tested
- [ ] Accessibility verified

### Component Documentation
Each component should document:
- Figma source (URL + frame ID)
- When last synced with design
- Any deviations from design (with rationale)
```

---

## Customization Guide

### For React + Tailwind Projects

Add to "Technology Stack":
```markdown
### Tailwind Configuration
- Config file: `tailwind.config.ts`
- Custom utilities: `src/styles/utilities.css`
- Design tokens mapped in: `theme.extend` object

### Component Pattern
```tsx
// components/Button/Primary.tsx
import { cn } from '@/lib/utils';

interface ButtonProps {
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: React.ReactNode;
}

export function PrimaryButton({ size = 'md', disabled, children }: ButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        'rounded-md font-medium transition-colors',
        // Semantic tokens
        'bg-interactive-primary text-white',
        'hover:bg-interactive-primary-hover',
        // States
        'disabled:opacity-50 disabled:cursor-not-allowed',
        // Size variants
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
```

### For Design System with Tokens Studio

Add section:
```markdown
## Token Automation

### Tokens Studio Setup
- Plugin connected to: [GitHub repo URL]
- Branch: `design-tokens`
- Sync frequency: [On save / Manual / CI/CD]

### Token Export Format
```json
{
  "color": {
    "blue": {
      "600": {
        "value": "#0066CC",
        "type": "color"
      }
    }
  },
  "spacing": {
    "2": {
      "value": "8px",
      "type": "spacing"
    }
  }
}
```

### Style Dictionary Transform
- Config: `style-dictionary.config.js`
- Output: `src/tokens/` directory
- Platforms: CSS, Tailwind, iOS, Android
```

### For Teams Using Storybook

Add to "Response Preferences":
```markdown
### For Storybook Stories
Generate stories with all variants:

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { PrimaryButton } from './Primary';

const meta: Meta<typeof PrimaryButton> = {
  title: 'Components/Button/Primary',
  component: PrimaryButton,
  parameters: {
    design: {
      type: 'figma',
      url: 'https://www.figma.com/file/[FILE_KEY]?node-id=[NODE_ID]',
    },
  },
};

export default meta;
type Story = StoryObj<typeof PrimaryButton>;

export const Default: Story = {
  args: {
    children: 'Click me',
    size: 'md',
  },
};

export const Small: Story = {
  args: {
    children: 'Small button',
    size: 'sm',
  },
};

// ... all variants from Figma
```
```

---

## Integration with Workflows

This CLAUDE.md pairs with the Design-to-Code workflow:

- Read: [Design-to-Code Workflow](../../guide/workflows/design-to-code.md)
- Understand: Figma Make → Claude MCP → Production pipeline
- Apply: Use this config to maintain design-code parity

---

## Example Prompts

### Implement Component from Figma
```
Implement the "Card/Product" component from our Figma design system:
[Figma URL]

Follow the design handoff checklist.
Use our token conventions from this CLAUDE.md.
Generate TypeScript component with all variants.
```

### Audit Design System Drift
```
Audit src/components against our Figma design system:
[Figma URL]

Report:
1. Hardcoded values not using tokens
2. Missing variants present in Figma
3. Inconsistent spacing/colors
4. Propose fixes
```

### Update Component After Design Change
```
The Button component was updated in Figma:
[Figma URL → Button frame]

Review changes, update code to match.
Ensure backward compatibility if possible.
Update Storybook stories if needed.
```

---

## See Also

- [Design-to-Code Workflow](../../guide/workflows/design-to-code.md) — Complete Figma MCP workflow guide
- [Figma MCP Section](../../guide/ultimate-guide.md#figma-mcp) — Technical details
- [Working with Images](../../guide/ultimate-guide.md#24-working-with-images) — Visual analysis basics
