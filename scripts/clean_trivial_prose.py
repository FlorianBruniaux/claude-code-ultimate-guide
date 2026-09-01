#!/usr/bin/env python3
"""Apply conservative, deterministic prose cleanup to Markdown files."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


EM_DASH = "—"
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#\s+)([^`\n]+?) — ([^`\n]+?)(\r?\n)?$")
RHETORICAL_HEADING_RE = re.compile(
    r"^### The learning curve is real(?: —|:) here's how to manage it(\r?\n)?$"
)
WP_TITLE_RE = re.compile(r"\b(WP\d{2}) — ")
LINK_LABEL_RE = re.compile(r"\[([^\]`\n]+?) — ([^\]`\n]+?)\]\(")
BOLD_LABEL_RE = re.compile(r"(\*\*[^*\n]+\*\*) — ")
LINK_DESCRIPTION_RE = re.compile(r"(\]\([^)\n]+\)) — ")
WHITEPAPERS_LIST_RE = re.compile(r"^(\s*[-*+]\s+Whitepapers) — ")
TABLE_PLACEHOLDER_RE = re.compile(r"(?<=\|)\s*—\s*(?=\|)")
QUOTED_EM_DASH_RE = re.compile(
    r'"[^"\n]* — [^"\n]*"|“[^”\n]* — [^”\n]*”|«[^»\n]* — [^»\n]*»'
)


@dataclass(frozen=True)
class TransformResult:
    text: str
    replacements: int
    remaining: list[tuple[int, str]]


def _replace_heading(line: str) -> tuple[str, int]:
    separator_index = line.find(" — ")
    before_separator = line[:separator_index]
    if (
        before_separator.count('"') % 2 == 1
        or before_separator.count("“") > before_separator.count("”")
        or before_separator.count("«") > before_separator.count("»")
    ):
        return line, 0

    match = HEADING_RE.match(line)
    if not match:
        return line, 0
    prefix, left, right, newline = match.groups()
    return f"{prefix}{left}: {right}{newline or ''}", 1


def _replace_safe_separators(line: str) -> tuple[str, int]:
    if QUOTED_EM_DASH_RE.search(line):
        return line, 0

    replacements = 0

    line, count = RHETORICAL_HEADING_RE.subn(
        lambda match: f"### Managing the learning curve{match.group(1) or ''}",
        line,
    )
    replacements += count

    line, count = _replace_heading(line)
    replacements += count

    for pattern, replacement in (
        (WP_TITLE_RE, r"\1: "),
        (LINK_LABEL_RE, r"[\1: \2]("),
        (BOLD_LABEL_RE, r"\1: "),
        (LINK_DESCRIPTION_RE, r"\1: "),
        (WHITEPAPERS_LIST_RE, r"\1: "),
    ):
        line, count = pattern.subn(replacement, line)
        replacements += count

    if replacements:
        line = re.sub(r"(?<![ \t])[ \t](\r?\n)$", r"\1", line)

    return line, replacements


def transform_markdown(text: str) -> TransformResult:
    output: list[str] = []
    remaining: list[tuple[int, str]] = []
    replacements = 0
    fence_character: str | None = None
    fence_length = 0

    for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length:
                fence_character = None
                fence_length = 0
            output.append(line)
            continue

        if fence_character is not None:
            output.append(line)
            continue

        if line.lstrip().startswith(">"):
            transformed = line
            count = 0
        else:
            transformed, count = _replace_safe_separators(line)

        output.append(transformed)
        replacements += count
        prose_candidate = TABLE_PLACEHOLDER_RE.sub("", transformed)
        if EM_DASH in prose_candidate:
            remaining.append((line_number, transformed.rstrip("\r\n")))

    return TransformResult("".join(output), replacements, remaining)


def _plural(count: int, singular: str, plural: str | None = None) -> str:
    return singular if count == 1 else plural or f"{singular}s"


def process_files(paths: Iterable[Path], write: bool, verbose: bool = False) -> tuple[int, int]:
    total_replacements = 0
    total_remaining = 0

    for path in paths:
        source = path.read_text(encoding="utf-8")
        result = transform_markdown(source)
        total_replacements += result.replacements
        total_remaining += len(result.remaining)
        if verbose:
            for line_number, (before, after) in enumerate(
                zip(source.splitlines(), result.text.splitlines()), start=1
            ):
                if before != after:
                    print(f"{path}:{line_number}: {before} => {after}")
        if write and result.text != source:
            path.write_text(result.text, encoding="utf-8")

    return total_replacements, total_remaining


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report safe changes without writing")
    mode.add_argument("--write", action="store_true", help="apply safe changes in place")
    parser.add_argument("--verbose", action="store_true", help="print every changed line")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    replacements, remaining = process_files(
        args.paths, write=args.write, verbose=args.verbose
    )
    availability = "applied" if args.write else "available"
    print(
        f"{replacements} safe {_plural(replacements, 'replacement')} {availability}; "
        f"{remaining} ambiguous {_plural(remaining, 'line')} "
        f"{_plural(remaining, 'remains', 'remain')}"
    )
    return 1 if args.check and replacements else 0


if __name__ == "__main__":
    raise SystemExit(main())
