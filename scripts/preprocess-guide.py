#!/usr/bin/env python3
"""
Pre-process guide/ultimate-guide.md for Quarto/Typst rendering.

Transformations applied:
1. Strip YAML frontmatter (--- block at top)
2. Convert internal anchor links [text](#anchor) → text
   (Typst raises "label does not exist" errors on these)
3. Escape @word patterns outside code blocks
   (pandoc parses them as citations → Typst #cite() calls → "no bibliography" error)

Output: whitepapers/guide-content.md (gitignored)
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
_DEFAULT_INPUT  = REPO_ROOT / "guide" / "ultimate-guide.md"
_DEFAULT_OUTPUT = REPO_ROOT / "whitepapers" / "guide-content.md"


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter block (--- ... ---)."""
    if not content.startswith("---"):
        return content
    end = content.find("\n---", 3)
    if end == -1:
        return content
    return content[end + 4:].lstrip("\n")


def strip_internal_links(content: str) -> str:
    """Convert [text](#anchor) → text (internal anchor links only)."""
    return re.sub(r'\[([^\]]+)\]\(#[^)]+\)', r'\1', content)


def strip_inline_toc(content: str) -> str:
    """
    Remove the inline markdown Table of Contents section from the guide.

    The guide contains a '## Table of Contents' section (~115 lines) with
    internal anchor links listing all chapters and sections. In PDF export:
    - All anchor links are already stripped (non-functional)
    - The Quarto-generated outline() TOC replaces it at the document start
    - It renders as 4 pages of unstyled nested bullet lists

    We keep the heading as a brief note instead of deleting it entirely,
    so the section numbering flow in the PDF remains coherent.
    """
    for title, note in (
        ("Table of Contents", "See the Table of Contents at the beginning of this document."),
        ("Table des matières", "Consultez la table des matières au début de ce document."),
    ):
        heading = re.search(r"^## " + re.escape(title) + r"\s*$", content, re.MULTILINE)
        if heading is None:
            continue
        end = re.search(r"^## 1\.1 Installation\s*$", content[heading.end():], re.MULTILINE)
        if end is None:
            return content
        replacement = f"## {title}\n\n_{note}_\n\n"
        return content[:heading.start()] + replacement + content[heading.end() + end.start():]
    return content


def escape_citation_patterns(content: str) -> str:
    """
    Escape @word patterns outside code fences/inline code so pandoc
    doesn't convert them to Typst #cite() calls.

    Safe: emails (user@domain.com), scoped packages (@scope/pkg),
          anything inside backticks or code fences.
    Escaped: @Word, @layer, @Injectable, etc. in regular text.
    """
    lines = content.split("\n")
    result = []
    in_fence = False
    fence_marker = ""

    for line in lines:
        # Track code fence state
        stripped = line.lstrip()
        if not in_fence:
            opening = re.match(r"(`{3,}|~{3,})", stripped)
            if opening:
                in_fence = True
                fence_marker = opening.group(1)
                result.append(line)
                continue
        else:
            if re.fullmatch(re.escape(fence_marker[0]) + "{" + str(len(fence_marker)) + r",}\s*", stripped):
                in_fence = False
                result.append(line)
                continue

        if in_fence:
            result.append(line)
            continue

        # Outside code fence: escape @word patterns that look like pandoc citations
        # Citation pattern: @[A-Za-z][A-Za-z0-9_:.#$%&-+?<>~/]*
        # Skip: email (preceded by \w), scoped npm (@scope/), inline backticks handled separately
        def escape_at(m):
            full = m.group(0)
            # Keep if inside inline backtick (handled by split below)
            return "\\@" + m.group(1)

        # Process line parts: split on inline code to avoid touching `@word` in backticks
        parts = re.split(r'(`[^`]*`)', line)
        new_parts = []
        for i, part in enumerate(parts):
            if i % 2 == 1:
                # Inside inline code — leave untouched
                new_parts.append(part)
            else:
                # Outside inline code — escape citation-like @word
                # Match @Word not preceded by \w (email) and not followed by / (scoped pkg)
                part = re.sub(
                    r'(?<![/\w@])@([A-Za-z][A-Za-z0-9_-]*)(?!/)',
                    lambda m: '\\@' + m.group(1),
                    part
                )
                new_parts.append(part)
        result.append("".join(new_parts))

    return "\n".join(result)


def ensure_blank_before_lists(content: str) -> str:
    """
    Insert a blank line before list items that immediately follow a
    non-blank, non-list line (no separator after ':').

    Without this, pandoc's markdown reader merges the preceding paragraph
    and the list items into a single Para block, rendering them inline as
    "text: - item1 - item2" instead of a proper bullet list.

    CommonMark allows lists to interrupt paragraphs, but pandoc's default
    markdown reader requires a blank line before the first list item.
    """
    LIST_PREFIXES = ("- ", "* ", "+ ")

    def is_list_line(s: str) -> bool:
        stripped = s.lstrip()
        if any(stripped.startswith(p) for p in LIST_PREFIXES):
            return True
        # Ordered list: "1. " or "1) "
        if stripped and stripped[0].isdigit():
            rest = stripped.lstrip("0123456789")
            if rest.startswith(". ") or rest.startswith(") "):
                return True
        return False

    lines = content.split("\n")
    result = []
    fence_marker = ""

    for i, line in enumerate(lines):
        stripped = line.lstrip()

        # Track code fences
        opening = re.match(r"(`{3,}|~{3,})", stripped)
        if not fence_marker and opening:
            fence_marker = opening.group(1)
            result.append(line)
            continue
        if fence_marker:
            if re.fullmatch(re.escape(fence_marker[0]) + "{" + str(len(fence_marker)) + r",}\s*", stripped):
                fence_marker = ""
            result.append(line)
            continue

        # Inject blank line before list start when preceding line is not blank/list
        if is_list_line(line) and i > 0:
            prev = lines[i - 1]
            prev_stripped = prev.strip()
            if prev_stripped and not is_list_line(prev):
                result.append("")  # blank line separator

        result.append(line)

    return "\n".join(result)


def process(content: str) -> str:
    content = strip_frontmatter(content)
    content = strip_inline_toc(content)
    content = strip_internal_links(content)
    content = escape_citation_patterns(content)
    content = ensure_blank_before_lists(content)
    return content


def main():
    parser = argparse.ArgumentParser(description="Pre-process a guide markdown file for Quarto/Typst rendering.")
    parser.add_argument("--input",  type=Path, default=_DEFAULT_INPUT,  help="Source markdown file")
    parser.add_argument("--output", type=Path, default=_DEFAULT_OUTPUT, help="Output markdown file")
    args = parser.parse_args()

    INPUT  = args.input
    OUTPUT = args.output

    if not INPUT.exists():
        print(f"Error: {INPUT} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {INPUT}...")
    content = INPUT.read_text(encoding="utf-8")
    original_lines = content.count("\n")

    result = process(content)
    processed_lines = result.count("\n")

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(result, encoding="utf-8")

    links_stripped = len(re.findall(r'\[([^\]]+)\]\(#[^)]+\)', content))
    at_escaped = result.count("\\@")
    blank_lines_added = processed_lines - original_lines + 6  # 6 = frontmatter removed

    print(f"Written {OUTPUT}")
    print(f"Lines: {original_lines} → {processed_lines}")
    print(f"Internal links stripped: {links_stripped}")
    print(f"@citations escaped: {at_escaped}")
    print(f"Blank lines injected before lists: {blank_lines_added}")


if __name__ == "__main__":
    main()
