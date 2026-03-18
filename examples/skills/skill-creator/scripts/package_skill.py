#!/usr/bin/env python3
"""
Package a Claude Code skill into a distributable zip file.

Usage:
    python3 package_skill.py <path/to/skill-folder> [output-directory]

Example:
    python3 package_skill.py ~/.claude/skills/my-skill ./dist
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path


def validate_skill(skill_path: Path) -> tuple[bool, list[str]]:
    """Validate skill structure and return (is_valid, errors)."""
    errors = []

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        errors.append("Missing required file: SKILL.md")
    else:
        # Check SKILL.md has frontmatter
        content = skill_md.read_text()
        if not content.startswith('---'):
            errors.append("SKILL.md missing YAML frontmatter (must start with ---)")
        elif content.count('---') < 2:
            errors.append("SKILL.md frontmatter not properly closed (needs second ---)")
        else:
            # Check required frontmatter fields
            frontmatter_end = content.index('---', 3)
            frontmatter = content[3:frontmatter_end]
            if 'name:' not in frontmatter:
                errors.append("SKILL.md frontmatter missing 'name' field")
            if 'description:' not in frontmatter:
                errors.append("SKILL.md frontmatter missing 'description' field")

    return len(errors) == 0, errors


def package_skill(skill_path: str, output_dir: str = '.') -> bool:
    """Package skill folder into a zip file."""

    skill_dir = Path(skill_path).expanduser().resolve()
    output_path = Path(output_dir).expanduser().resolve()

    # Validate skill folder exists
    if not skill_dir.exists():
        print(f"Skill folder not found: {skill_dir}")
        return False

    if not skill_dir.is_dir():
        print(f"Not a directory: {skill_dir}")
        return False

    # Validate skill structure
    print(f"Validating skill: {skill_dir.name}")
    is_valid, errors = validate_skill(skill_dir)

    if not is_valid:
        print("Validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("   Validation passed")

    # Create output directory if needed
    output_path.mkdir(parents=True, exist_ok=True)

    # Create zip file
    zip_name = f"{skill_dir.name}.zip"
    zip_path = output_path / zip_name

    try:
        print(f"Packaging skill...")

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in skill_dir.rglob('*'):
                if file_path.is_file():
                    # Skip common ignored files
                    if file_path.name.startswith('.'):
                        continue
                    if file_path.name == '__pycache__':
                        continue
                    if file_path.suffix == '.pyc':
                        continue

                    arcname = file_path.relative_to(skill_dir.parent)
                    zipf.write(file_path, arcname)
                    print(f"   Added: {arcname}")

        print(f"\nSkill packaged successfully!")
        print(f"Output: {zip_path}")
        print(f"Size: {zip_path.stat().st_size / 1024:.1f} KB")

        return True

    except Exception as e:
        print(f"Error packaging skill: {e}")
        if zip_path.exists():
            zip_path.unlink()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Package a Claude Code skill into a zip file'
    )

    parser.add_argument(
        'skill_path',
        help='Path to the skill folder'
    )

    parser.add_argument(
        'output_dir',
        nargs='?',
        default='.',
        help='Output directory for the zip file (default: current directory)'
    )

    args = parser.parse_args()

    success = package_skill(args.skill_path, args.output_dir)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()