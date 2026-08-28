#!/usr/bin/env python3
"""Collect the pinned Best of Agent Harnesses source snapshot."""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path
from typing import Any

from lib.agent_harnesses import PINNED_UPSTREAM_COMMIT, write_json


RAW_URL = "https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/{commit}/harnesses.json"


def validate_upstream_snapshot(source: Any) -> list[str]:
    if not isinstance(source, dict):
        return ["upstream snapshot must be an object"]
    errors: list[str] = []
    projects = source.get("projects")
    categories = source.get("categories")
    meta = source.get("meta")
    if not isinstance(meta, dict):
        return ["upstream snapshot metadata is missing"]
    if meta.get("project_count") != 160 or not isinstance(projects, list) or len(projects) != 160:
        errors.append("upstream snapshot must contain exactly 160 projects")
    if not isinstance(categories, list) or len(categories) != 12:
        errors.append("upstream snapshot must contain exactly 12 categories")
    if not meta.get("license"):
        errors.append("upstream snapshot license is missing")
    elif meta.get("license") != "CC-BY-SA-4.0":
        errors.append("upstream snapshot license must be CC-BY-SA-4.0")
    if isinstance(projects, list):
        ids = [project.get("github_id") for project in projects if isinstance(project, dict)]
        if len(ids) != len(set(ids)):
            errors.append("upstream snapshot contains duplicate project ids")
    return errors


def fetch_snapshot(commit: str, timeout: int = 60) -> dict[str, Any]:
    if commit != PINNED_UPSTREAM_COMMIT:
        raise ValueError(f"initial collector only accepts pinned commit {PINNED_UPSTREAM_COMMIT}")
    request = urllib.request.Request(
        RAW_URL.format(commit=commit),
        headers={"Accept": "application/json", "User-Agent": "claude-code-ultimate-guide"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        source = json.loads(response.read().decode("utf-8"))
    errors = validate_upstream_snapshot(source)
    if errors:
        raise ValueError("invalid upstream snapshot:\n- " + "\n- ".join(errors))
    return source


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream-commit", default=PINNED_UPSTREAM_COMMIT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = fetch_snapshot(args.upstream_commit, timeout=args.timeout_seconds)
    write_json(args.output, source)
    print(f"upstream_projects={len(source['projects'])}")
    print(f"upstream_categories={len(source['categories'])}")
    print(f"upstream_commit={args.upstream_commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
