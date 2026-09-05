#!/usr/bin/env python3
"""Create review-only feature proposals from untrusted README snapshots."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path, PurePosixPath
from typing import Any

from lib.agent_harnesses import (
    COMMIT_RE,
    EVIDENCE_STATUSES,
    LOOP_STATUSES,
    _is_github_repository,
    write_json,
)

FEATURE_NAMES = (
    "sandboxing",
    "memory",
    "lifecycle_hooks",
    "prompt_optimization",
    "build_vs_buy",
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def needs_extraction(manifest_entry: dict[str, Any], proposal: dict[str, Any] | None) -> bool:
    if not proposal:
        return True
    return manifest_entry.get("source_commit") != proposal.get("source_commit")


def validate_proposal(proposal: Any, readme_line_count: int) -> list[str]:
    if not isinstance(proposal, dict):
        return ["proposal must be an object"]
    errors: list[str] = []
    meta = proposal.get("_meta")
    source = meta.get("source") if isinstance(meta, dict) else None
    if not isinstance(source, dict):
        errors.append("proposal source binding is required")
    else:
        if not _is_github_repository(source.get("repository_url")):
            errors.append("repository_url must be a canonical GitHub HTTPS URL")
        readme_path = source.get("readme_path")
        if (
            not isinstance(readme_path, str)
            or not readme_path
            or readme_path.startswith("/")
            or "\\" in readme_path
            or ".." in PurePosixPath(readme_path).parts
        ):
            errors.append("readme_path must be repository-relative")
        if not isinstance(source.get("readme_sha256"), str) or not SHA256_RE.match(
            source["readme_sha256"]
        ):
            errors.append("readme_sha256 must be 64 lowercase hexadecimal characters")
    source_commit = proposal.get("source_commit")
    if not isinstance(source_commit, str) or not COMMIT_RE.match(source_commit):
        errors.append("source_commit must be 40 hexadecimal characters")
    if proposal.get("owns_loop") not in LOOP_STATUSES:
        errors.append("owns_loop is invalid")
    owns_loop_evidence = proposal.get("owns_loop_evidence")
    if not isinstance(owns_loop_evidence, list):
        errors.append("owns_loop_evidence must be an array")
        owns_loop_evidence = []
    if proposal.get("owns_loop") in {"confirmed", "claimed", "no"} and not owns_loop_evidence:
        errors.append("owns_loop status requires evidence")
    for item in owns_loop_evidence:
        if not isinstance(item, dict):
            errors.append("owns_loop evidence must be an object")
            continue
        start = item.get("start_line")
        end = item.get("end_line")
        if (
            not isinstance(start, int)
            or not isinstance(end, int)
            or start < 1
            or end < start
            or end > readme_line_count
        ):
            errors.append("owns_loop evidence line range is outside source")
    features = proposal.get("features")
    if not isinstance(features, dict):
        errors.append("features must be an object")
        return errors
    for name, feature in features.items():
        if not isinstance(feature, dict):
            errors.append(f"feature {name} must be an object")
            continue
        if feature.get("status") not in EVIDENCE_STATUSES:
            errors.append(f"feature {name} status is invalid")
        evidence = feature.get("evidence", [])
        if not isinstance(evidence, list):
            errors.append(f"feature {name} evidence must be an array")
            continue
        if feature.get("status") in {"confirmed", "claimed"} and not evidence:
            errors.append(f"feature {name} status requires evidence")
        if feature.get("status") in {"unknown", "not_applicable"} and evidence:
            errors.append(f"feature {name} status cannot carry evidence")
        for item in evidence:
            if not isinstance(item, dict):
                errors.append(f"feature {name} evidence must be an object")
                continue
            start = item.get("start_line")
            end = item.get("end_line")
            if (
                not isinstance(start, int)
                or not isinstance(end, int)
                or start < 1
                or end < start
                or end > readme_line_count
            ):
                errors.append("evidence line range is outside source")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", type=Path, required=True)
    parser.add_argument("--repository-url", required=True)
    parser.add_argument("--readme-path", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-readme-bytes", type=int, default=120_000)
    return parser.parse_args()


def read_bounded_readme(path: Path, max_bytes: int) -> tuple[str, int, int, bool, str]:
    if max_bytes < 1:
        raise ValueError("max_readme_bytes must be positive")
    source_bytes = path.stat().st_size
    with path.open("rb") as handle:
        raw = handle.read(max_bytes + 1)
    truncated = source_bytes > max_bytes or len(raw) > max_bytes
    raw = raw[:max_bytes]
    digest = hashlib.sha256(raw).hexdigest()
    return raw.decode("utf-8", errors="replace"), source_bytes, len(raw), truncated, digest


def generate_deterministic_proposal(
    readme: str,
    repository_url: str,
    readme_path: str,
    readme_sha256: str,
    source_commit: str,
    source_bytes: int,
    read_bytes: int,
    truncated: bool,
) -> dict[str, Any]:
    del readme  # Untrusted text is deliberately not interpreted or copied to output.
    return {
        "_meta": {
            "extractor": "deterministic-unknown-v1",
            "source_bytes": source_bytes,
            "read_bytes": read_bytes,
            "readme_truncated": truncated,
            "publication_status": "review_required",
            "source": {
                "repository_url": repository_url,
                "readme_path": readme_path,
                "readme_sha256": readme_sha256,
            },
        },
        "source_commit": source_commit,
        "owns_loop": "unknown",
        "owns_loop_evidence": [],
        "features": {
            name: {"value": "unknown", "status": "unknown", "evidence": []}
            for name in FEATURE_NAMES
        },
    }


def main() -> int:
    args = parse_args()
    if not COMMIT_RE.match(args.source_commit):
        raise SystemExit("source_commit must be 40 hexadecimal characters")
    readme, source_bytes, read_bytes, truncated, readme_sha256 = read_bounded_readme(
        args.readme, args.max_readme_bytes
    )
    proposal = generate_deterministic_proposal(
        readme,
        repository_url=args.repository_url,
        readme_path=args.readme_path,
        readme_sha256=readme_sha256,
        source_commit=args.source_commit,
        source_bytes=source_bytes,
        read_bytes=read_bytes,
        truncated=truncated,
    )
    errors = validate_proposal(proposal, len(readme.splitlines()))
    if errors:
        raise SystemExit("invalid proposal:\n- " + "\n- ".join(errors))
    write_json(args.output, proposal)
    print("proposal_written=true")
    print("publication_status=review_required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
