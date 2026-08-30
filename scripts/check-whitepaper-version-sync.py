#!/usr/bin/env python3
"""Check source and rendered version metadata for selected publications."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict


ROOT = Path(__file__).resolve().parents[1]


def read_frontmatter(path: Path) -> Dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"missing YAML frontmatter: {path}")

    values: Dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = re.match(r'^([a-zA-Z0-9_-]+):\s*["\']?([^"\']+?)["\']?\s*$', line)
        if field:
            values[field.group(1)] = field.group(2).strip()
    return values


def pdf_text(path: Path) -> str:
    completed = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-pdfs",
        action="store_true",
        help="Fail when a selected generated PDF is absent.",
    )
    args = parser.parse_args()

    failures = []
    guide_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    bridges = [
        ROOT / "whitepapers/_extensions/whitepaper/typst-show.typ",
        ROOT / "whitepapers/fr/_extensions/whitepaper/typst-show.typ",
        ROOT / "whitepapers/en/_extensions/whitepaper/typst-show.typ",
    ]
    for bridge in bridges:
        content = bridge.read_text(encoding="utf-8")
        if "$if(wp-version)$" not in content or 'wp-version: "$wp-version$"' not in content:
            failures.append(f"missing wp-version bridge: {bridge}")

    publications = [
        ("whitepapers/fr/12-agent-engineering.qmd", "whitepapers/fr/12-agent-engineering.pdf"),
        ("whitepapers/en/12-agent-engineering.qmd", "whitepapers/en/12-agent-engineering.pdf"),
        ("whitepapers/fr/cheatsheet.qmd", "whitepapers/fr/cheatsheet.pdf"),
        ("whitepapers/en/cheatsheet.qmd", "whitepapers/en/cheatsheet.pdf"),
    ]

    can_read_pdf = shutil.which("pdftotext") is not None
    if args.require_pdfs and not can_read_pdf:
        failures.append("pdftotext is required when --require-pdfs is set")

    for qmd_relative, pdf_relative in publications:
        qmd = ROOT / qmd_relative
        pdf = ROOT / pdf_relative
        metadata = read_frontmatter(qmd)
        version = metadata.get("version")
        wp_version = metadata.get("wp-version")
        if version != guide_version:
            failures.append(f"{qmd_relative}: version {version!r} != {guide_version!r}")
        if not wp_version:
            failures.append(f"{qmd_relative}: missing wp-version")
            continue
        if pdf.exists() and can_read_pdf:
            expected = f"v{wp_version} · Guide v{version}"
            if expected not in pdf_text(pdf):
                failures.append(f"{pdf_relative}: missing {expected!r}")
        elif args.require_pdfs:
            failures.append(f"missing generated PDF: {pdf_relative}")

    recap_cards = [
        ("whitepapers/recap-cards/fr/c14-agent-harness-map.qmd", "whitepapers/recap-cards/fr/c14-agent-harness-map.pdf"),
        ("whitepapers/recap-cards/en/c14-agent-harness-map.qmd", "whitepapers/recap-cards/en/c14-agent-harness-map.pdf"),
    ]
    for qmd_relative, pdf_relative in recap_cards:
        qmd = ROOT / qmd_relative
        pdf = ROOT / pdf_relative
        metadata = read_frontmatter(qmd)
        version = metadata.get("version")
        declared_guide_version = metadata.get("guide-version")
        if version != guide_version or declared_guide_version != guide_version:
            failures.append(
                f"{qmd_relative}: version fields must both equal {guide_version!r}"
            )
        if pdf.exists() and can_read_pdf:
            if f"v{guide_version} ·" not in pdf_text(pdf):
                failures.append(f"{pdf_relative}: missing guide version footer")
        elif args.require_pdfs:
            failures.append(f"missing generated PDF: {pdf_relative}")

    for relative in ("whitepapers/fr/cheatsheet.qmd", "whitepapers/en/cheatsheet.qmd"):
        content = (ROOT / relative).read_text(encoding="utf-8")
        if f"Version {guide_version} |" not in content:
            failures.append(f"{relative}: stale body version")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    print("PASS: publication version metadata is synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
