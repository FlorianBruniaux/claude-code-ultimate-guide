---
name: skill-creator
description: Create new Claude Code skills with proper structure, YAML frontmatter, and bundled resources. Generates skill templates following best practices for modular, self-contained capability packages.
tags: [meta, skill, generator, claude-code]
---

# Skill Creator

This skill helps you create new Claude Code skills with proper structure and best practices.

## When to Use This Skill

- Creating a new custom skill for your project
- Standardizing skill structure across your team
- Generating skill templates with scripts, references, and assets
- Packaging skills for distribution

## Skill Structure

A Claude skill consists of:

```
skill-name/
├── SKILL.md          # Required: Main skill file with YAML frontmatter
├── scripts/          # Optional: Executable code for deterministic tasks
├── references/       # Optional: Documentation loaded contextually
└── assets/           # Optional: Templates, images, boilerplate (not loaded into context)
```

## SKILL.md Format

Every skill requires a `SKILL.md` file with:

```markdown
---
name: skill-name
description: One-line description of what the skill does and when to use it.
---

# Skill Name

Brief introduction explaining the skill's purpose.

## When to Use This Skill

- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

## What This Skill Does

1. **Step 1**: Description
2. **Step 2**: Description
3. **Step 3**: Description

## How to Use

### Basic Usage
[Examples of how to invoke the skill]

### With Options
[Advanced usage patterns]

## Example

**User**: "Example prompt"

**Output**:
[Example output]

## Tips

- Best practice 1
- Best practice 2

## Related Use Cases

- Related task 1
- Related task 2
```

## How to Use

### Create a New Skill

```
Create a new skill called "my-skill-name" in ~/.claude/skills/
```

### Create with Specific Purpose

```
Create a skill for generating release notes from git commits,
with templates for CHANGELOG.md and Slack announcements
```

### Initialize Skill Structure

Run the initialization script:

```bash
python3 ~/.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>
```

### Package Skill for Distribution

```bash
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

## Design Principles

### Progressive Disclosure

Context loads hierarchically to optimize token usage:
1. **Metadata** (~100 words): Always present via skill description
2. **SKILL.md** (<5k words): Loaded when skill is triggered
3. **Bundled resources**: Loaded as needed during execution

### Organizational Patterns

Choose the pattern that fits your skill:

| Pattern | Best For | Structure |
|---------|----------|-----------|
| **Workflow-Based** | Sequential procedures | Step-by-step instructions |
| **Task-Based** | Multiple operations | Collection of tasks |
| **Reference/Guidelines** | Standards, specs | Rules and examples |
| **Capabilities-Based** | Interrelated features | Feature descriptions |

### Naming Conventions

- Use `kebab-case` for skill names: `release-notes-generator`
- Use descriptive names that indicate purpose
- Keep names concise but meaningful

## Bundled Resources

### scripts/

Executable code for deterministic, repeatable tasks:
- `init_skill.py` - Initialize new skill structure
- `package_skill.py` - Package skill for distribution

### references/

Documentation loaded contextually:
- API documentation
- Style guides
- Domain knowledge

### assets/

Templates and resources (not auto-loaded):
- Output templates
- Boilerplate code
- Images and fonts

## Example: Creating a Release Notes Skill

**User**: "Create a skill for generating release notes with 3 output formats: CHANGELOG.md, PR body, and Slack message"

**Steps**:
1. Initialize structure: `init_skill.py release-notes-generator --path ~/.claude/skills/`
2. Add templates to `assets/`:
   - `changelog-template.md`
   - `pr-release-template.md`
   - `slack-template.md`
3. Add transformation rules to `references/`:
   - `tech-to-product-mappings.md`
4. Complete `SKILL.md` with usage instructions
5. Package: `package_skill.py ~/.claude/skills/release-notes-generator`

## Tips

- Keep SKILL.md under 5000 words for efficient context usage
- Use references/ for domain knowledge that doesn't change often
- Put templates in assets/ so they're not auto-loaded
- Test your skill with real use cases before packaging
- Include concrete examples in your SKILL.md

## Related Use Cases

- Creating project-specific automation skills
- Building team-shared development workflows
- Packaging reusable Claude capabilities
