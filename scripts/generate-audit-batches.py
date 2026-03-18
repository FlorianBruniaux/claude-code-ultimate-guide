#!/usr/bin/env python3
"""
Generate audit batches for quiz question review.

Splits 256 questions into category-based batches for agent review.
Each batch includes: question, options, correct answer, explanation, and guide context.

Output: claudedocs/audit-batches/*.md (16 files)

Usage:
    python3 scripts/generate-audit-batches.py
"""

import json
from pathlib import Path
from typing import Dict, List


BASE_DIR = Path(__file__).parent.parent
AUDIT_CONTEXT = BASE_DIR / "claudedocs" / "audit-context.json"
BATCH_TEMPLATE = BASE_DIR / "claudedocs" / "audit-batch-template.md"
OUTPUT_DIR = BASE_DIR / "claudedocs" / "audit-batches"

# Category names (from _categories.yaml in landing repo)
CATEGORIES = {
    1: "Quick Start",
    2: "Core Concepts",
    3: "Best Practices",
    4: "Configuration",
    5: "Context Management",
    6: "Tools & Features",
    7: "Workflows",
    8: "MCP Ecosystem",
    9: "Advanced Patterns",
    10: "Reference",
    11: "Learning with AI",
    12: "Methodologies",
    13: "Security",
    14: "Philosophy",
    15: "Ecosystem"
}

# Priority order for review
PRIORITY_ORDER = [
    1,   # Quick Start
    2,   # Core Concepts
    13,  # Security
    10,  # Reference
    8,   # MCP Ecosystem
    9,   # Advanced Patterns
    3,   # Best Practices
    5,   # Context Management
    6,   # Tools & Features
    7,   # Workflows
    11,  # Learning with AI
    12,  # Methodologies
    4,   # Configuration
    14,  # Philosophy
    15   # Ecosystem
]


def format_question_for_review(q: Dict) -> str:
    """Format a single question for human review."""
    lines = []
    lines.append(f"### Question {q['id']}")
    lines.append("")
    lines.append(f"**Difficulty**: {q['difficulty']}")
    lines.append(f"**Profiles**: {', '.join(q['profiles'])}")
    lines.append("")
    lines.append("**Question:**")
    lines.append(q['question'])
    lines.append("")
    lines.append("**Options:**")
    for key in ['a', 'b', 'c', 'd']:
        marker = "✓" if key == q['correct'] else " "
        lines.append(f"  {key}. {q['options'][key]} {marker}")
    lines.append("")
    lines.append(f"**Correct Answer**: {q['correct']}")
    lines.append("")
    lines.append("**Explanation:**")
    lines.append(q['explanation'])
    lines.append("")

    # Guide context
    if q.get('guide_context'):
        lines.append("**Guide Context:**")
        lines.append(f"*Source: {q.get('guide_source_file', 'N/A')} (line {q.get('guide_line_number', 'N/A')})*")
        lines.append(f"*Resolution: {q.get('resolution_strategy')} (confidence: {q.get('resolution_confidence', 0)}%)*")
        lines.append("```")
        # Truncate context if too long (max 100 lines)
        context_lines = q['guide_context'].split('\n')
        if len(context_lines) > 100:
            lines.extend(context_lines[:100])
            lines.append(f"... (truncated {len(context_lines) - 100} lines)")
        else:
            lines.extend(context_lines)
        lines.append("```")
    else:
        lines.append("**Guide Context:** ⚠️ UNRESOLVED")
        if 'doc_reference' in q:
            lines.append(f"*Intended reference: {q['doc_reference']}*")

    lines.append("")
    lines.append("---")
    lines.append("")
    return '\n'.join(lines)


def generate_batch(category_id: int, questions: List[Dict], template: str) -> str:
    """Generate a batch file for a category."""
    category_name = CATEGORIES[category_id]

    # Format questions
    questions_text = []
    for q in questions:
        questions_text.append(format_question_for_review(q))

    # Fill template
    batch_content = template.replace('{questions}', '\n'.join(questions_text))

    # Add header
    header = f"""# Audit Batch: Category {category_id:02d} - {category_name}

**Questions**: {len(questions)}
**Priority**: {PRIORITY_ORDER.index(category_id) + 1}/{len(PRIORITY_ORDER)}

---

"""
    return header + batch_content


def main():
    """Main entry point."""
    print("═══════════════════════════════════════════════════════════════")
    print("Quiz Question Audit Batch Generation")
    print("═══════════════════════════════════════════════════════════════")
    print()

    # Load audit context
    if not AUDIT_CONTEXT.exists():
        print(f"Error: audit-context.json not found. Run extract-audit-context.py first.", file=sys.stderr)
        return 1

    data = json.loads(AUDIT_CONTEXT.read_text())
    questions = data['questions']

    print(f"Loaded {len(questions)} questions")

    # Load template
    if not BATCH_TEMPLATE.exists():
        print(f"Error: batch template not found: {BATCH_TEMPLATE}", file=sys.stderr)
        return 1

    template = BATCH_TEMPLATE.read_text()

    # Group by category
    by_category = {}
    for q in questions:
        cat_id = q['category_id']
        if cat_id not in by_category:
            by_category[cat_id] = []
        by_category[cat_id].append(q)

    print(f"Categories: {len(by_category)}")
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate batches
    for cat_id in PRIORITY_ORDER:
        if cat_id not in by_category:
            continue

        cat_questions = by_category[cat_id]
        batch_content = generate_batch(cat_id, cat_questions, template)

        # Handle advanced-patterns (split into 2 batches if >20 questions)
        if cat_id == 9 and len(cat_questions) > 20:
            # Split into 2 batches
            mid = len(cat_questions) // 2
            batch1 = cat_questions[:mid]
            batch2 = cat_questions[mid:]

            batch1_content = generate_batch(cat_id, batch1, template)
            batch2_content = generate_batch(cat_id, batch2, template)

            output_file1 = OUTPUT_DIR / f"{cat_id:02d}-{CATEGORIES[cat_id].lower().replace(' ', '-')}-part1.md"
            output_file2 = OUTPUT_DIR / f"{cat_id:02d}-{CATEGORIES[cat_id].lower().replace(' ', '-')}-part2.md"

            # Add part indicators
            batch1_content = batch1_content.replace(
                f"# Audit Batch: Category {cat_id:02d}",
                f"# Audit Batch: Category {cat_id:02d} - Part 1/2"
            )
            batch2_content = batch2_content.replace(
                f"# Audit Batch: Category {cat_id:02d}",
                f"# Audit Batch: Category {cat_id:02d} - Part 2/2"
            )

            output_file1.write_text(batch1_content)
            output_file2.write_text(batch2_content)

            print(f"✓ Generated {output_file1.name} ({len(batch1)} questions)")
            print(f"✓ Generated {output_file2.name} ({len(batch2)} questions)")
        else:
            output_file = OUTPUT_DIR / f"{cat_id:02d}-{CATEGORIES[cat_id].lower().replace(' ', '-')}.md"
            output_file.write_text(batch_content)
            print(f"✓ Generated {output_file.name} ({len(cat_questions)} questions)")

    print()
    print("═══════════════════════════════════════════════════════════════")
    print(f"✓ Batches generated in: {OUTPUT_DIR}")
    print(f"  Total files: {len(list(OUTPUT_DIR.glob('*.md')))}")
    print()
    print("Review order (priority):")
    for idx, cat_id in enumerate(PRIORITY_ORDER, 1):
        if cat_id in by_category:
            count = len(by_category[cat_id])
            print(f"  {idx:2d}. Category {cat_id:02d} - {CATEGORIES[cat_id]} ({count} questions)")
    print("═══════════════════════════════════════════════════════════════")


if __name__ == '__main__':
    import sys
    sys.exit(main() or 0)
