#!/usr/bin/env python3
"""
Generate CATALOG.md from template metadata.

Scans all templates in examples/ for frontmatter metadata and generates
a comprehensive catalog organized by category, complexity, and time.

Usage:
    python3 scripts/generate-template-catalog.py
    python3 scripts/generate-template-catalog.py --validate
"""

import os
import re
import sys
import json
import yaml
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

# Template categories
CATEGORIES = {
    'agents': ('examples/agents', 'Agent'),
    'commands': ('examples/commands', 'Skill'),  # legacy stubs — redirect to examples/skills/
    'skills': ('examples/skills', 'Skill'),
    'hooks': ('examples/hooks', 'Hook'),
    'workflows': ('examples/workflows', 'Workflow'),
    'scripts': ('examples/scripts', 'Script'),
}

# Complexity levels
COMPLEXITY_LEVELS = ['beginner', 'intermediate', 'advanced']

# Time estimates
TIME_ESTIMATES = ['5 min', '15 min', '30 min', '1 hour', '2 hours', '4+ hours', 'varies']

# Default metadata
DEFAULT_METADATA = {
    'complexity': 'intermediate',
    'time': '30 min',
    'domain': 'general',
    'prerequisites': [],
    'status': 'stable',
}


def extract_frontmatter(filepath: Path) -> Tuple[Optional[Dict], str]:
    """Extract YAML frontmatter from a markdown or shell file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return None, content[:200]

    # Look for YAML frontmatter (---)
    if content.startswith('---'):
        try:
            end_marker = content.find('---', 3)
            if end_marker != -1:
                frontmatter_str = content[3:end_marker].strip()
                metadata = yaml.safe_load(frontmatter_str)
                return metadata or {}, content[end_marker+3:].strip()
        except yaml.YAMLError:
            pass

    # Fallback: look for <!-- metadata --> HTML comments
    match = re.search(r'<!--\s*(.+?)\s*-->', content, re.DOTALL)
    if match:
        try:
            metadata = json.loads(match.group(1))
            return metadata, content
        except json.JSONDecodeError:
            pass

    return {}, content


def extract_description(filepath: Path, content: str) -> str:
    """Extract description from file content."""
    # Try to get from frontmatter
    metadata, _ = extract_frontmatter(filepath)
    if metadata and 'description' in metadata:
        return metadata['description']

    # Fallback: first non-heading line
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('-'):
            return line[:100]

    return 'No description'


def scan_templates() -> Dict[str, List[Dict]]:
    """Scan all templates and extract metadata."""
    templates = defaultdict(list)

    for category, (path, label) in CATEGORIES.items():
        if not os.path.exists(path):
            continue

        # Find all relevant files
        extensions = {'.md'} if category != 'hooks' else {'.sh', '.ps1'}

        for filepath in Path(path).rglob('*'):
            if filepath.is_file() and filepath.suffix in extensions:
                metadata, content = extract_frontmatter(filepath)

                # Build template info
                template_info = {
                    'name': metadata.get('name', filepath.stem),
                    # CATALOG.md lives inside examples/, so links must be relative
                    # to that directory rather than to the repository root.
                    'file': str(filepath.relative_to('examples')),
                    'description': metadata.get('description', extract_description(filepath, content)),
                    'complexity': metadata.get('complexity', DEFAULT_METADATA['complexity']),
                    'time': metadata.get('time', DEFAULT_METADATA['time']),
                    'domain': metadata.get('domain', DEFAULT_METADATA['domain']),
                    'prerequisites': metadata.get('prerequisites', []),
                    'status': metadata.get('status', DEFAULT_METADATA['status']),
                    'keywords': metadata.get('keywords', []),
                }

                templates[category].append(template_info)

    # Sort by name within each category
    for category in templates:
        templates[category].sort(key=lambda x: x['name'].lower())

    return templates


def generate_catalog(templates: Dict[str, List[Dict]]) -> str:
    """Generate markdown catalog from templates."""
    output = []
    output.append('# Template Catalog\n')
    output.append('Auto-generated template index with complexity, time, and domain filters.\n')
    output.append('**Last updated**: [auto-generated]\n')
    output.append('---\n')

    # Summary statistics
    total = sum(len(v) for v in templates.values())
    output.append(f'**Total Templates**: {total}\n')
    for category, items in templates.items():
        output.append(f'- **{category.title()}**: {len(items)}')
    output.append('')

    # Quick filter sections
    output.append('## Filter by Complexity\n')
    for level in COMPLEXITY_LEVELS:
        count = sum(1 for items in templates.values() for t in items if t['complexity'] == level)
        output.append(f'- **{level.title()}**: {count} templates')
    output.append('')

    output.append('## Filter by Time\n')
    for time_est in TIME_ESTIMATES:
        count = sum(1 for items in templates.values() for t in items if t['time'] == time_est)
        if count > 0:
            output.append(f'- **{time_est}**: {count} templates')
    output.append('')

    # Category sections
    output.append('---\n')
    output.append('## By Category\n')

    for category, items in templates.items():
        if not items:
            continue

        output.append(f'### {CATEGORIES[category][1]}s ({len(items)})\n')

        for template in items:
            # Build the entry
            entry = f'**[{template["name"]}]({template["file"]})** '
            entry += f'*{template["complexity"]}* • {template["time"]}'
            if template['domain'] != 'general':
                entry += f' • {template["domain"]}'
            if template['status'] != 'stable':
                entry += f' • ⚠️ {template["status"]}'
            output.append(f'- {entry}')

            if template['description']:
                description = str(template['description']).replace(' \u2014 ', ': ')
                output.append(f'  {description}')

            if template['prerequisites']:
                prereqs = ', '.join(template['prerequisites'])
                output.append(f'  *Prerequisites*: {prereqs}')

            output.append('')

        output.append('')

    # Domain-based index
    output.append('---\n')
    output.append('## By Domain\n')

    domains = defaultdict(list)
    for items in templates.values():
        for template in items:
            domain = template.get('domain', 'general')
            domains[domain].append(template)

    for domain in sorted(domains.keys()):
        templates_in_domain = sorted(domains[domain], key=lambda x: x['name'])
        output.append(f'### {domain.title()} ({len(templates_in_domain)})\n')

        for template in templates_in_domain:
            output.append(f'- **{template["name"]}** ({template["complexity"]}, {template["time"]})')

        output.append('')

    # Beginner-friendly section
    output.append('---\n')
    output.append('## For Beginners\n')
    output.append('Templates recommended for first-time users:\n')

    beginner_templates = [
        t for items in templates.values() for t in items
        if t['complexity'] == 'beginner'
    ]

    if beginner_templates:
        for template in sorted(beginner_templates, key=lambda x: x['name']):
            output.append(f'- **{template["name"]}** ({template["time"]})')
            output.append(f'  {template["description"]}')
    else:
        output.append('No templates explicitly marked as beginner-friendly yet.')

    output.append('')

    # Metadata reference
    output.append('---\n')
    output.append('## Metadata Reference\n')
    output.append('Templates can include the following metadata in YAML frontmatter:\n')
    output.append('```yaml\n')
    output.append('name: template-name\n')
    output.append('description: What this template does\n')
    output.append('complexity: beginner|intermediate|advanced\n')
    output.append('time: 5 min|15 min|30 min|1 hour|2 hours|4+ hours|varies\n')
    output.append('domain: security|testing|deployment|general|...\n')
    output.append('prerequisites: [skill1, skill2]\n')
    output.append('status: stable|experimental|deprecated\n')
    output.append('keywords: [tag1, tag2]\n')
    output.append('```\n')

    return '\n'.join(output)


def validate_metadata(templates: Dict[str, List[Dict]]) -> List[str]:
    """Validate template metadata."""
    issues = []

    for category, items in templates.items():
        for template in items:
            # Check complexity
            if template['complexity'] not in COMPLEXITY_LEVELS:
                issues.append(
                    f"{template['file']}: Invalid complexity '{template['complexity']}'. "
                    f"Must be one of: {', '.join(COMPLEXITY_LEVELS)}"
                )

            # Check time
            if template['time'] not in TIME_ESTIMATES:
                issues.append(
                    f"{template['file']}: Invalid time '{template['time']}'. "
                    f"Use one of: {', '.join(TIME_ESTIMATES)}"
                )

            # Check description length
            if len(template['description']) < 5:
                issues.append(
                    f"{template['file']}: Description too short. Provide meaningful description."
                )

    return issues


def main():
    # Scan templates
    print('📦 Scanning templates...', file=sys.stderr)
    templates = scan_templates()

    if not templates:
        print('❌ No templates found', file=sys.stderr)
        return 1

    print(f'✅ Found {sum(len(v) for v in templates.values())} templates', file=sys.stderr)

    # Validate if requested
    if '--validate' in sys.argv:
        print('\n🔍 Validating metadata...', file=sys.stderr)
        issues = validate_metadata(templates)
        if issues:
            print(f'⚠️  Found {len(issues)} validation issues:', file=sys.stderr)
            for issue in issues:
                print(f'  - {issue}', file=sys.stderr)
        else:
            print('✅ All metadata valid', file=sys.stderr)

    # Generate catalog
    catalog = generate_catalog(templates)

    # Output
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        output_file = sys.argv[idx + 1]
        with open(output_file, 'w') as f:
            f.write(catalog)
        print(f'✅ Catalog written to {output_file}', file=sys.stderr)
    else:
        print(catalog)

    return 0


if __name__ == '__main__':
    sys.exit(main())
