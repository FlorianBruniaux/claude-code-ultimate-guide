#!/usr/bin/env python3
"""Collect the pinned Best of Agent Harnesses source snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Any

from lib.agent_harnesses import (
    MAX_UPSTREAM_BYTES,
    PINNED_UPSTREAM_COMMIT,
    PINNED_UPSTREAM_SHA256,
    write_json,
)


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


def read_limited_stream(stream: Any, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while total <= max_bytes:
        remaining = max_bytes + 1 - total
        chunk = stream.read(min(64 * 1024, remaining))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
    if total > max_bytes:
        raise ValueError(f"upstream response exceeds {max_bytes} bytes")
    return b"".join(chunks)


def fetch_snapshot(
    commit: str, timeout: int = 60, max_bytes: int = MAX_UPSTREAM_BYTES
) -> tuple[dict[str, Any], bytes]:
    if commit != PINNED_UPSTREAM_COMMIT:
        raise ValueError(f"initial collector only accepts pinned commit {PINNED_UPSTREAM_COMMIT}")
    request = urllib.request.Request(
        RAW_URL.format(commit=commit),
        headers={"Accept": "application/json", "User-Agent": "claude-code-ultimate-guide"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        declared_size = response.headers.get("Content-Length")
        if declared_size is not None and int(declared_size) > max_bytes:
            raise ValueError(f"upstream response exceeds {max_bytes} bytes")
        raw = read_limited_stream(response, max_bytes=max_bytes)
    if hashlib.sha256(raw).hexdigest() != PINNED_UPSTREAM_SHA256:
        raise ValueError("source snapshot SHA-256 mismatch")
    source = json.loads(raw.decode("utf-8"))
    errors = validate_upstream_snapshot(source)
    if errors:
        raise ValueError("invalid upstream snapshot:\n- " + "\n- ".join(errors))
    return source, raw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream-commit", default=PINNED_UPSTREAM_COMMIT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--max-bytes", type=int, default=MAX_UPSTREAM_BYTES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source, raw = fetch_snapshot(
        args.upstream_commit,
        timeout=args.timeout_seconds,
        max_bytes=args.max_bytes,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_bytes(raw)
    temporary.replace(args.output)
    manifest_path = args.output.with_name(args.output.stem + ".manifest.json")
    write_json(
        manifest_path,
        {
            "repository": source["meta"]["url"],
            "commit": args.upstream_commit,
            "sha256": PINNED_UPSTREAM_SHA256,
            "license": source["meta"]["license"],
            "project_count": len(source["projects"]),
            "category_count": len(source["categories"]),
        },
    )
    print(f"upstream_projects={len(source['projects'])}")
    print(f"upstream_categories={len(source['categories'])}")
    print(f"upstream_commit={args.upstream_commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
