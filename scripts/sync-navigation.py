#!/usr/bin/env python3
"""Validate intent navigation and keep the README excerpt synchronized."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "machine-readable" / "navigation.json"
DEFAULT_README = ROOT / "README.md"
BEGIN_MARKER = "<!-- BEGIN GENERATED INTENT NAVIGATION -->"
END_MARKER = "<!-- END GENERATED INTENT NAVIGATION -->"
EXPECTED_GROUPS = ["start", "build", "scale", "resources", "updates"]


def github_slug(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value.strip().lower())
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"\s+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if not match:
            continue
        base = github_slug(match.group(1))
        occurrence = counts.get(base, 0)
        counts[base] = occurrence + 1
        anchors.add(base if occurrence == 0 else f"{base}-{occurrence}")
    return anchors


def load_and_validate() -> dict:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []

    group_ids = [group.get("id") for group in data.get("groups", [])]
    if group_ids != EXPECTED_GROUPS:
        errors.append(f"group order must be {EXPECTED_GROUPS}, got {group_ids}")

    item_ids: set[str] = set()
    site_paths: set[str] = set()
    for group in data.get("groups", []):
        if not group.get("items"):
            errors.append(f"group {group.get('id')} has no items")
        for item in group.get("items", []):
            item_id = item.get("id", "")
            site_path = item.get("site_path", "")
            source_path = item.get("source_path")
            source_anchor = item.get("source_anchor")

            if item_id in item_ids:
                errors.append(f"duplicate item id: {item_id}")
            item_ids.add(item_id)

            if not site_path.startswith("/"):
                errors.append(f"site path must start with /: {site_path}")
            if site_path in site_paths:
                errors.append(f"duplicate site path: {site_path}")
            site_paths.add(site_path)

            if source_path is None:
                if source_anchor:
                    errors.append(f"{item_id} has an anchor without a source path")
                continue

            source = (ROOT / source_path).resolve()
            try:
                source.relative_to(ROOT)
            except ValueError:
                errors.append(f"source escapes repository root: {source_path}")
                continue
            if not source.exists():
                errors.append(f"source does not exist: {source_path}")
                continue
            if source_anchor:
                anchor = source_anchor.removeprefix("#")
                if anchor not in markdown_anchors(source):
                    errors.append(f"source anchor does not exist: {source_path}{source_anchor}")

    if errors:
        raise ValueError("\n".join(errors))
    return data


def render_readme_table(data: dict) -> str:
    base = data["site_base_url"].rstrip("/")
    rows = ["| Intent | Browse online |", "|---|---|"]
    for group in data["groups"]:
        links = []
        for item in group["items"]:
            href = f"{base}{item['site_path']}"
            links.append(f"[{item['title']}]({href})")
        rows.append(f"| **{group['title']}** | {' · '.join(links)} |")
    return "\n".join(rows)


def synchronized_readme(content: str, rendered: str) -> str:
    if content.count(BEGIN_MARKER) != 1 or content.count(END_MARKER) != 1:
        raise ValueError("README must contain one generated navigation marker pair")
    before, remainder = content.split(BEGIN_MARKER, 1)
    _, after = remainder.split(END_MARKER, 1)
    return f"{before}{BEGIN_MARKER}\n{rendered}\n{END_MARKER}{after}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--readme", type=Path, default=DEFAULT_README)
    parser.add_argument("--write", action="store_true", help="Update the generated README block")
    args = parser.parse_args()

    readme = args.readme.resolve()
    try:
        data = load_and_validate()
        rendered = render_readme_table(data)
        current = readme.read_text(encoding="utf-8")
        expected = synchronized_readme(current, rendered)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"navigation validation failed: {exc}", file=sys.stderr)
        return 1

    if current != expected:
        if not args.write:
            print(f"{readme.relative_to(ROOT)} navigation is out of sync", file=sys.stderr)
            print("run: python3 scripts/sync-navigation.py --write", file=sys.stderr)
            return 1
        readme.write_text(expected, encoding="utf-8")
        print(f"updated {readme.relative_to(ROOT)}")
    else:
        print(f"navigation valid; {readme.relative_to(ROOT)} is synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
