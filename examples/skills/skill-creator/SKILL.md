---
name: skill-creator
description: "Scaffold a new Claude Code skill with SKILL.md, frontmatter, and bundled resources. Use when creating a custom skill, standardizing skill structure across a team, or packaging a skill for distribution."
allowed-tools: Write Bash
effort: low
---

# Skill creator

Generate new Claude Code skills with correct directory structure, YAML frontmatter, and optional bundled resources.

## When to use

- Creating a new custom skill for a project
- Standardizing skill structure across a team
- Generating skill templates with scripts, references, and assets
- Packaging skills for distribution

## Skill directory structure

```
skill-name/
├── SKILL.md          # Required: Main skill file with YAML frontmatter
├── scripts/          # Optional: Executable code for deterministic tasks
├── references/       # Optional: Documentation loaded contextually
└── assets/           # Optional: Templates, images, boilerplate (not loaded into context)
```

## Workflow

### 1. Create the skill

```
Create a new skill called "my-skill-name" in ~/.claude/skills/
```

Or with a specific purpose:

```
Create a skill for generating release notes from git commits,
with templates for CHANGELOG.md and Slack announcements
```

Or via the initialization script:

```bash
python3 ~/.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>
```

### 2. Generated SKILL.md template

The created SKILL.md follows this structure:

```markdown
---
name: skill-name
description: "What the skill does. Use when [trigger conditions]."
---

# Skill Name

## When to Use
- Trigger condition 1
- Trigger condition 2

## What This Skill Does
1. **Step 1**: Description
2. **Step 2**: Description

## How to Use
[Usage examples]

## Example
**User**: "Example prompt"
**Output**: [Example output]
```

### 3. Validate the skill

After creation, verify:

1. **Frontmatter**: `name` is kebab-case, 1-64 chars; `description` is a quoted string with "Use when" clause
2. **Content**: Has "When to Use" section with trigger conditions and at least one usage example
3. **Structure**: SKILL.md is under 5000 words; references and assets are in correct subdirectories
4. **Test**: Invoke the skill with a real use case and confirm expected output

### 4. Package for distribution (optional)

```bash
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

## Organizational patterns

| Pattern | Best For | Structure |
|---------|----------|-----------|
| **Workflow-Based** | Sequential procedures | Step-by-step instructions |
| **Task-Based** | Multiple operations | Collection of tasks |
| **Reference/Guidelines** | Standards, specs | Rules and examples |
| **Capabilities-Based** | Interrelated features | Feature descriptions |

## Example: Creating a release notes skill

**User**: "Create a skill for generating release notes with 3 output formats"

**Steps**:
1. Initialize: `init_skill.py release-notes-generator --path ~/.claude/skills/`
2. Add templates to `assets/`: `changelog-template.md`, `pr-release-template.md`, `slack-template.md`
3. Add rules to `references/`: `tech-to-product-mappings.md`
4. Complete `SKILL.md` with usage instructions
5. Validate: check frontmatter, test with a real commit range
6. Package: `package_skill.py ~/.claude/skills/release-notes-generator`

## Tips

- Keep SKILL.md under 5000 words for efficient context usage
- Use `references/` for domain knowledge that doesn't change often
- Put templates in `assets/` so they're not auto-loaded into context
- Always include a "Use when" clause in the description frontmatter
- Test with real use cases before packaging
