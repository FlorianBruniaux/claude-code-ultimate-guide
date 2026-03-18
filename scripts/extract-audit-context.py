#!/usr/bin/env python3
"""
Extract audit context for quiz questions.

Reads 256 quiz questions from landing repo, resolves their doc_reference anchors
to sections in the guide, and extracts relevant context (max 150 lines per question).

Output: claudedocs/audit-context.json

Strategies for resolving doc_reference.anchor (in order):
  A. Anchor matching: Convert anchor to markdown heading and search
  B. Section name matching: Fuzzy match on doc_reference.section
  C. reference.yaml fallback: Use line numbers from index
  D. UNRESOLVED: Flag if no match found

Usage:
    python3 scripts/extract-audit-context.py

Requirements:
    - pyyaml (pip install pyyaml)
    - thefuzz (pip install thefuzz)
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import yaml

try:
    from thefuzz import fuzz
except ImportError:
    print("Error: thefuzz not installed. Run: pip install thefuzz", file=sys.stderr)
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent.parent
LANDING_DIR = Path(__file__).parent.parent.parent / "claude-code-ultimate-guide-landing"
QUESTIONS_DIR = LANDING_DIR / "questions"
REFERENCE_YAML = BASE_DIR / "machine-readable" / "reference.yaml"
OUTPUT_JSON = BASE_DIR / "claudedocs" / "audit-context.json"

CONTEXT_LINES = 150  # Max lines of guide context per question

# Cache for loaded guide files
_GUIDE_CACHE = {}


# ═══════════════════════════════════════════════════════════════
# Parsing Utilities (reuse from build-questions.py)
# ═══════════════════════════════════════════════════════════════

def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """Parse YAML frontmatter and body from Markdown content."""
    lines = content.split('\n')

    if lines[0].strip() != '---':
        raise ValueError("File must start with YAML frontmatter (---)")

    closing_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == '---':
            closing_idx = idx
            break

    if closing_idx is None:
        raise ValueError("Invalid frontmatter structure (missing closing ---)")

    yaml_text = '\n'.join(lines[1:closing_idx])
    body_text = '\n'.join(lines[closing_idx + 1:])

    try:
        frontmatter = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML frontmatter: {e}")

    return frontmatter, body_text


def split_body(body: str) -> Tuple[str, str]:
    """Split body into question and explanation at first --- (outside code blocks)."""
    lines = body.split('\n')
    in_code_block = False
    separator_idx = None

    for idx, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        if not in_code_block and line.strip() == '---':
            separator_idx = idx
            break

    if separator_idx is None:
        raise ValueError("Body must contain --- separator between question and explanation")

    question = '\n'.join(lines[:separator_idx]).strip()
    explanation = '\n'.join(lines[separator_idx + 1:]).strip()

    return question, explanation


# ═══════════════════════════════════════════════════════════════
# Guide Context Resolution
# ═══════════════════════════════════════════════════════════════

def load_guide(guide_file: str = "guide/ultimate-guide.md") -> List[str]:
    """
    Load guide lines from specified file.

    Args:
        guide_file: Relative path from BASE_DIR (e.g., "guide/ultimate-guide.md")

    Returns:
        List of lines
    """
    if guide_file in _GUIDE_CACHE:
        return _GUIDE_CACHE[guide_file]

    guide_path = BASE_DIR / guide_file
    if not guide_path.exists():
        raise FileNotFoundError(f"Guide file not found: {guide_path}")

    lines = guide_path.read_text().split('\n')
    _GUIDE_CACHE[guide_file] = lines
    return lines


def load_reference_yaml() -> Dict:
    """Load reference.yaml for fallback line numbers."""
    if not REFERENCE_YAML.exists():
        return {}
    return yaml.safe_load(REFERENCE_YAML.read_text())


def anchor_to_heading(anchor: str) -> str:
    """
    Convert anchor like '#11-installation' to markdown heading 'Installation'
    or '## 1.1 Installation'.

    Handles various anchor formats:
    - '#11-installation' → 'installation' (lowercase for fuzzy match)
    - '#core-concepts' → 'core concepts'
    - '#32-common-tasks' → 'common tasks'
    """
    # Remove '#' and leading numbers (XX-), replace '-' with ' '
    clean = anchor.lstrip('#').lower()
    clean = re.sub(r'^\d+-', '', clean)  # Remove leading XX-
    clean = clean.replace('-', ' ')
    return clean.strip()


def find_heading_in_guide(guide_lines: List[str], target_heading: str) -> Optional[int]:
    """
    Find line number of heading in guide (fuzzy match, threshold 70).

    Uses partial matching strategy:
    - Checks if target is a substring (case-insensitive)
    - Falls back to fuzzy ratio with threshold 70

    Returns:
        Line number (0-indexed) or None if not found
    """
    best_score = 0
    best_line = None
    target_lower = target_heading.lower()

    for idx, line in enumerate(guide_lines):
        if line.startswith('#'):
            # Extract heading text (remove #, ##, etc.)
            heading_text = re.sub(r'^#+\s*', '', line).lower()
            # Remove leading numbers like '1.1', '3.2', etc.
            heading_text = re.sub(r'^\d+\.?\d*\s*', '', heading_text)

            # Strategy 1: Substring match (exact)
            if target_lower in heading_text or heading_text in target_lower:
                return idx

            # Strategy 2: Fuzzy match
            score = fuzz.ratio(target_lower, heading_text)
            if score > best_score:
                best_score = score
                best_line = idx

    # Lowered threshold to 70 to catch more variations
    if best_score >= 70:
        return best_line
    return None


def extract_section_context(guide_lines: List[str], start_line: int, max_lines: int = CONTEXT_LINES) -> str:
    """
    Extract context from guide starting at start_line.
    Stops at next heading of same/higher level or after max_lines.

    Args:
        guide_lines: Full guide lines
        start_line: Starting line number (0-indexed)
        max_lines: Maximum lines to extract

    Returns:
        Context text
    """
    if start_line >= len(guide_lines):
        return ""

    # Determine heading level of start line
    start_heading = guide_lines[start_line]
    start_level = len(re.match(r'^#+', start_heading).group()) if start_heading.startswith('#') else 0

    context_lines = []
    for offset in range(max_lines):
        line_idx = start_line + offset
        if line_idx >= len(guide_lines):
            break

        line = guide_lines[line_idx]

        # Stop at next heading of same/higher level (but not the start heading itself)
        if offset > 0 and line.startswith('#'):
            heading_level = len(re.match(r'^#+', line).group())
            if heading_level <= start_level:
                break

        context_lines.append(line)

    return '\n'.join(context_lines)


def resolve_doc_reference(doc_ref: Dict, reference_yaml: Dict) -> Dict:
    """
    Resolve doc_reference to guide context.

    Strategies (in order):
      A. Anchor matching: Convert anchor to heading and search
      B. Section name matching: Fuzzy match on section field
      C. reference.yaml fallback: Use line numbers
      D. UNRESOLVED: No match found

    Returns:
        {
            'strategy': 'anchor|section|reference_yaml|unresolved|file_not_found',
            'context': 'extracted guide text or empty',
            'line_number': int or None,
            'confidence': int (0-100),
            'source_file': str (actual file searched)
        }
    """
    result = {
        'strategy': 'unresolved',
        'context': '',
        'line_number': None,
        'confidence': 0,
        'source_file': doc_ref.get('file', 'guide/ultimate-guide.md')
    }

    # Load the correct guide file
    guide_file = doc_ref.get('file', 'guide/ultimate-guide.md')
    try:
        guide_lines = load_guide(guide_file)
    except FileNotFoundError:
        result['strategy'] = 'file_not_found'
        return result

    # Strategy A: Anchor matching
    if 'anchor' in doc_ref and doc_ref['anchor']:
        target_heading = anchor_to_heading(doc_ref['anchor'])
        line_num = find_heading_in_guide(guide_lines, target_heading)

        if line_num is not None:
            result['strategy'] = 'anchor'
            result['line_number'] = line_num
            result['context'] = extract_section_context(guide_lines, line_num)
            result['confidence'] = 95
            return result

    # Strategy B: Section name matching
    if 'section' in doc_ref and doc_ref['section']:
        target_section = doc_ref['section'].lower()
        line_num = find_heading_in_guide(guide_lines, target_section)

        if line_num is not None:
            result['strategy'] = 'section'
            result['line_number'] = line_num
            result['context'] = extract_section_context(guide_lines, line_num)
            result['confidence'] = 80
            return result

    # Strategy C: reference.yaml fallback
    # TODO: Implement if anchor/section strategies fail too often
    # For now, skip since reference.yaml has complex structure

    # Strategy D: UNRESOLVED
    return result


# ═══════════════════════════════════════════════════════════════
# Main Processing
# ═══════════════════════════════════════════════════════════════

def process_questions() -> List[Dict]:
    """Process all quiz questions and extract audit context."""
    if not QUESTIONS_DIR.exists():
        print(f"Error: Questions directory not found: {QUESTIONS_DIR}", file=sys.stderr)
        sys.exit(1)

    # Load reference
    print("Loading reference.yaml...")
    reference_yaml = load_reference_yaml()

    # Find all question files
    md_files = sorted(QUESTIONS_DIR.glob('*/*.md'))
    if not md_files:
        print(f"Error: No .md files found in {QUESTIONS_DIR}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(md_files)} question files")
    print()

    # Process each question
    results = []
    stats = {
        'total': len(md_files),
        'anchor': 0,
        'section': 0,
        'reference_yaml': 0,
        'unresolved': 0,
        'no_reference': 0,
        'file_not_found': 0
    }

    for idx, filepath in enumerate(md_files, 1):
        try:
            content = filepath.read_text()
            frontmatter, body = parse_frontmatter(content)
            question_text, explanation_text = split_body(body)

            q_id = frontmatter['id']
            category_id = frontmatter['category_id']

            # Build question object
            question_obj = {
                'id': q_id,
                'category_id': category_id,
                'difficulty': frontmatter['difficulty'],
                'profiles': frontmatter['profiles'],
                'question': question_text,
                'options': frontmatter['options'],
                'correct': frontmatter['correct'],
                'explanation': explanation_text,
                'source_file': str(filepath.relative_to(QUESTIONS_DIR.parent))
            }

            # Resolve doc_reference if present
            if 'doc_reference' in frontmatter:
                doc_ref = frontmatter['doc_reference']
                resolution = resolve_doc_reference(doc_ref, reference_yaml)

                question_obj['doc_reference'] = doc_ref
                question_obj['guide_context'] = resolution['context']
                question_obj['resolution_strategy'] = resolution['strategy']
                question_obj['resolution_confidence'] = resolution['confidence']
                question_obj['guide_line_number'] = resolution['line_number']
                question_obj['guide_source_file'] = resolution['source_file']

                stats[resolution['strategy']] += 1
            else:
                question_obj['guide_context'] = ''
                question_obj['resolution_strategy'] = 'no_reference'
                stats['no_reference'] += 1

            results.append(question_obj)

            # Progress indicator
            if idx % 25 == 0:
                print(f"Processed {idx}/{len(md_files)} questions...")

        except Exception as e:
            print(f"Error processing {filepath.name}: {e}", file=sys.stderr)
            continue

    print()
    print("═══════════════════════════════════════════════════════════════")
    print("Resolution Statistics")
    print("═══════════════════════════════════════════════════════════════")
    print(f"Total questions:        {stats['total']}")
    print(f"Anchor strategy:        {stats['anchor']} ({stats['anchor']/stats['total']*100:.1f}%)")
    print(f"Section strategy:       {stats['section']} ({stats['section']/stats['total']*100:.1f}%)")
    print(f"reference.yaml:         {stats['reference_yaml']} ({stats['reference_yaml']/stats['total']*100:.1f}%)")
    print(f"No doc_reference:       {stats['no_reference']} ({stats['no_reference']/stats['total']*100:.1f}%)")
    print(f"File not found:         {stats['file_not_found']} ({stats['file_not_found']/stats['total']*100:.1f}%)")
    print(f"UNRESOLVED:             {stats['unresolved']} ({stats['unresolved']/stats['total']*100:.1f}%)")
    print()

    resolved_count = stats['anchor'] + stats['section'] + stats['reference_yaml']
    resolution_rate = resolved_count / (stats['total'] - stats['no_reference']) * 100 if stats['total'] > stats['no_reference'] else 0
    print(f"Resolution rate (excl. no_reference): {resolution_rate:.1f}%")

    if resolution_rate < 95:
        print()
        print("⚠️  WARNING: Resolution rate < 95%. Consider improving strategies.")

    return results


def main():
    """Main entry point."""
    print("═══════════════════════════════════════════════════════════════")
    print("Quiz Question Audit Context Extraction")
    print("═══════════════════════════════════════════════════════════════")
    print()

    # Process questions
    questions_with_context = process_questions()

    # Ensure output directory exists
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    # Write output
    output_data = {
        'version': '1.0',
        'generated_at': '2026-02-04',
        'total_questions': len(questions_with_context),
        'questions': questions_with_context
    }

    OUTPUT_JSON.write_text(json.dumps(output_data, indent=2, ensure_ascii=False) + '\n')

    print()
    print("═══════════════════════════════════════════════════════════════")
    print(f"✓ Output written to: {OUTPUT_JSON}")
    print(f"  Total questions: {len(questions_with_context)}")
    print("═══════════════════════════════════════════════════════════════")


if __name__ == '__main__':
    main()
