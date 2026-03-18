#!/usr/bin/env python3
"""
Initialize a new Claude Code skill with proper directory structure.

Usage:
    python3 init_skill.py <skill-name> --path <output-directory>

Example:
    python3 init_skill.py release-notes-generator --path ~/.claude/skills/
"""

import argparse
import os
import sys
from pathlib import Path


SKILL_MD_TEMPLATE = '''---
name: {skill_name}
description: [One-line description of what this skill does and when to use it]
---

# {skill_title}

[Brief introduction explaining the skill's purpose]

## When to Use This Skill

- [Trigger condition 1]
- [Trigger condition 2]
- [Trigger condition 3]

## What This Skill Does

1. **[Step 1]**: [Description]
2. **[Step 2]**: [Description]
3. **[Step 3]**: [Description]

## How to Use

### Basic Usage

```
[Example prompt that triggers this skill]
```

### With Options

```
[Advanced usage example with parameters]
```

## Example

**User**: "[Example user prompt]"

**Output**:
```markdown
[Example output from the skill]
```

## Tips

- [Best practice 1]
- [Best practice 2]
- [Best practice 3]

## Related Use Cases

- [Related task 1]
- [Related task 2]
'''

SCRIPTS_README = '''# Scripts

This directory contains executable scripts for deterministic, repeatable tasks.

## Guidelines

- Scripts should be self-contained and well-documented
- Include usage examples in script headers
- Handle errors gracefully with clear messages
- Use appropriate exit codes (0 for success, 1 for failure)

## Files

Add your scripts here. Examples:
- `generate.py` - Main generation script
- `validate.py` - Validation utilities
- `transform.py` - Data transformation helpers
'''

REFERENCES_README = '''# References

This directory contains documentation that will be loaded contextually during skill execution.

## Guidelines

- Keep files focused and well-organized
- Use markdown format for readability
- Include concrete examples where possible
- Update when domain knowledge changes

## Files

Add your reference documents here. Examples:
- `api-docs.md` - API documentation
- `style-guide.md` - Formatting guidelines
- `domain-knowledge.md` - Domain-specific information
'''

ASSETS_README = '''# Assets

This directory contains templates, images, and boilerplate code.

**Note**: Assets are NOT automatically loaded into context. They must be explicitly referenced.

## Guidelines

- Use descriptive filenames
- Include usage instructions in file headers
- Keep templates minimal and customizable

## Files

Add your assets here. Examples:
- `template.md` - Output template
- `boilerplate.ts` - Code boilerplate
- `config.json` - Configuration template
'''


def validate_skill_name(name: str) -> bool:
    """Validate skill name follows kebab-case convention."""
    if not name:
        return False
    if not all(c.isalnum() or c == '-' for c in name):
        return False
    if name.startswith('-') or name.endswith('-'):
        return False
    if '--' in name:
        return False
    return True


def skill_name_to_title(name: str) -> str:
    """Convert kebab-case skill name to Title Case."""
    return ' '.join(word.capitalize() for word in name.split('-'))


def create_skill(skill_name: str, output_path: str) -> bool:
    """Create a new skill with proper directory structure."""

    if not validate_skill_name(skill_name):
        print(f"Invalid skill name: '{skill_name}'")
        print("   Use kebab-case (e.g., 'my-skill-name')")
        return False

    output_dir = Path(output_path).expanduser().resolve()
    skill_dir = output_dir / skill_name

    if skill_dir.exists():
        print(f"Skill already exists: {skill_dir}")
        return False

    try:
        print(f"Creating skill: {skill_name}")

        skill_dir.mkdir(parents=True, exist_ok=True)
        print(f"   Created {skill_dir}")

        for subdir in ['scripts', 'references', 'assets']:
            (skill_dir / subdir).mkdir(exist_ok=True)
            print(f"   Created {subdir}/")

        skill_title = skill_name_to_title(skill_name)
        skill_md_content = SKILL_MD_TEMPLATE.format(
            skill_name=skill_name,
            skill_title=skill_title
        )
        (skill_dir / 'SKILL.md').write_text(skill_md_content)
        print("   Created SKILL.md")

        (skill_dir / 'scripts' / 'README.md').write_text(SCRIPTS_README)
        (skill_dir / 'references' / 'README.md').write_text(REFERENCES_README)
        (skill_dir / 'assets' / 'README.md').write_text(ASSETS_README)
        print("   Created README files")

        print(f"\nSkill '{skill_name}' created successfully!")
        print(f"\nLocation: {skill_dir}")
        print("\nNext steps:")
        print("   1. Edit SKILL.md with your skill's instructions")
        print("   2. Add scripts to scripts/ for automation")
        print("   3. Add reference docs to references/")
        print("   4. Add templates to assets/")
        print(f"   5. Test with: skill: \"{skill_name}\"")

        return True

    except Exception as e:
        print(f"Error creating skill: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Initialize a new Claude Code skill'
    )

    parser.add_argument(
        'skill_name',
        help='Name of the skill (kebab-case, e.g., "my-skill-name")'
    )

    parser.add_argument(
        '--path',
        required=True,
        help='Output directory where skill folder will be created'
    )

    args = parser.parse_args()

    success = create_skill(args.skill_name, args.path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()