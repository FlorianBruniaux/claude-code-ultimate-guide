#!/usr/bin/env python3
"""
Generate audit report from agent reviews.

Collects agent review outputs and compiles them into a comprehensive report.

Input: claudedocs/audit-reviews/*.txt (agent outputs)
Output: claudedocs/audit-report.md

Usage:
    python3 scripts/generate-audit-report.py
"""

import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


BASE_DIR = Path(__file__).parent.parent
REVIEWS_DIR = BASE_DIR / "claudedocs" / "audit-reviews"
OUTPUT_REPORT = BASE_DIR / "claudedocs" / "audit-report.md"


def parse_review_file(filepath: Path) -> Dict:
    """
    Parse agent review output.

    Expected format:
        PASS: Q01-001
        ISSUE: Q01-002 - [critical] CORRECT_ANSWER - Description
        ISSUE: Q01-003 - [warning] AMBIGUITY - Description
    """
    content = filepath.read_text()
    results = {
        'pass': [],
        'issues': []
    }

    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue

        if line.startswith('PASS:'):
            q_id = line.replace('PASS:', '').strip()
            results['pass'].append(q_id)

        elif line.startswith('ISSUE:'):
            # Parse: ISSUE: Q01-002 - [critical] CORRECT_ANSWER - Description
            match = re.match(r'ISSUE:\s+(Q\d+-\d+)\s+-\s+\[(\w+)\]\s+(\w+)\s+-\s+(.+)', line)
            if match:
                q_id, severity, issue_type, description = match.groups()
                results['issues'].append({
                    'q_id': q_id,
                    'severity': severity,
                    'type': issue_type,
                    'description': description
                })

    return results


def generate_report(all_reviews: List[Dict]) -> str:
    """Generate comprehensive audit report."""
    lines = []

    # Header
    lines.append("# Quiz Question Audit Report")
    lines.append("")
    lines.append(f"**Generated**: 2026-02-04")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Aggregate statistics
    total_pass = sum(len(r['pass']) for r in all_reviews)
    total_issues = sum(len(r['issues']) for r in all_reviews)
    total_questions = total_pass + total_issues

    critical_count = sum(1 for r in all_reviews for i in r['issues'] if i['severity'] == 'critical')
    warning_count = sum(1 for r in all_reviews for i in r['issues'] if i['severity'] == 'warning')
    info_count = sum(1 for r in all_reviews for i in r['issues'] if i['severity'] == 'info')

    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"**Total Questions Reviewed**: {total_questions}")
    lines.append(f"**Pass**: {total_pass} ({total_pass/total_questions*100:.1f}%)")
    lines.append(f"**Issues Found**: {total_issues} ({total_issues/total_questions*100:.1f}%)")
    lines.append("")
    lines.append("### Issue Breakdown")
    lines.append("")
    lines.append(f"- **Critical**: {critical_count} (wrong answer, major factual error)")
    lines.append(f"- **Warning**: {warning_count} (ambiguous, outdated, misleading)")
    lines.append(f"- **Info**: {info_count} (minor wording, trivial)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Critical issues
    lines.append("## Critical Issues (Immediate Fix Required)")
    lines.append("")
    critical_issues = [i for r in all_reviews for i in r['issues'] if i['severity'] == 'critical']

    if critical_issues:
        for issue in sorted(critical_issues, key=lambda x: x['q_id']):
            lines.append(f"### {issue['q_id']}")
            lines.append("")
            lines.append(f"**Type**: {issue['type']}")
            lines.append(f"**Issue**: {issue['description']}")
            lines.append("")
    else:
        lines.append("*No critical issues found.*")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Warnings
    lines.append("## Warnings (Review & Consider Fixing)")
    lines.append("")
    warning_issues = [i for r in all_reviews for i in r['issues'] if i['severity'] == 'warning']

    if warning_issues:
        # Group by type
        by_type = defaultdict(list)
        for issue in warning_issues:
            by_type[issue['type']].append(issue)

        for issue_type, issues in sorted(by_type.items()):
            lines.append(f"### {issue_type} ({len(issues)} questions)")
            lines.append("")
            for issue in sorted(issues, key=lambda x: x['q_id']):
                lines.append(f"- **{issue['q_id']}**: {issue['description']}")
            lines.append("")
    else:
        lines.append("*No warnings found.*")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Info
    lines.append("## Info (Minor Issues)")
    lines.append("")
    info_issues = [i for r in all_reviews for i in r['issues'] if i['severity'] == 'info']

    if info_issues:
        for issue in sorted(info_issues, key=lambda x: x['q_id']):
            lines.append(f"- **{issue['q_id']}** ({issue['type']}): {issue['description']}")
        lines.append("")
    else:
        lines.append("*No info issues found.*")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Health by category
    lines.append("## Health by Category")
    lines.append("")
    lines.append("| Category | Pass | Issues | Pass Rate |")
    lines.append("|----------|------|--------|-----------|")

    # Extract category from Q01-001 format
    by_category = defaultdict(lambda: {'pass': 0, 'issues': 0})
    for review in all_reviews:
        for q_id in review['pass']:
            cat = q_id.split('-')[0]
            by_category[cat]['pass'] += 1
        for issue in review['issues']:
            cat = issue['q_id'].split('-')[0]
            by_category[cat]['issues'] += 1

    for cat in sorted(by_category.keys()):
        stats = by_category[cat]
        total = stats['pass'] + stats['issues']
        pass_rate = stats['pass'] / total * 100 if total > 0 else 0
        lines.append(f"| Category {cat} | {stats['pass']} | {stats['issues']} | {pass_rate:.1f}% |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Next steps
    lines.append("## Recommended Actions")
    lines.append("")
    lines.append("1. **Fix Critical Issues** (Priority 1)")
    lines.append("   - Review each critical issue")
    lines.append("   - Fix question/answer or update explanation")
    lines.append("   - Rebuild: `python3 scripts/build-questions.py`")
    lines.append("")
    lines.append("2. **Review Warnings** (Priority 2)")
    lines.append("   - Evaluate ambiguities and outdated info")
    lines.append("   - Decide: fix, clarify, or accept")
    lines.append("")
    lines.append("3. **Consider Info Issues** (Priority 3)")
    lines.append("   - Minor improvements for quality")
    lines.append("")

    return '\n'.join(lines)


def main():
    """Main entry point."""
    print("═══════════════════════════════════════════════════════════════")
    print("Quiz Question Audit Report Generation")
    print("═══════════════════════════════════════════════════════════════")
    print()

    if not REVIEWS_DIR.exists():
        print(f"Error: Reviews directory not found: {REVIEWS_DIR}", file=sys.stderr)
        print("Place agent review outputs in claudedocs/audit-reviews/*.txt", file=sys.stderr)
        return 1

    # Find review files
    review_files = sorted(REVIEWS_DIR.glob('*.txt'))
    if not review_files:
        print(f"Error: No review files found in {REVIEWS_DIR}", file=sys.stderr)
        return 1

    print(f"Found {len(review_files)} review files")
    print()

    # Parse all reviews
    all_reviews = []
    for filepath in review_files:
        print(f"Parsing {filepath.name}...")
        review = parse_review_file(filepath)
        all_reviews.append(review)
        print(f"  Pass: {len(review['pass'])}, Issues: {len(review['issues'])}")

    print()

    # Generate report
    report = generate_report(all_reviews)

    # Write output
    OUTPUT_REPORT.write_text(report)

    print("═══════════════════════════════════════════════════════════════")
    print(f"✓ Report generated: {OUTPUT_REPORT}")
    print("═══════════════════════════════════════════════════════════════")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
