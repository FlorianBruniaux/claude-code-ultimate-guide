#!/usr/bin/env python3
"""Build and validate the canonical machine-readable agent-harness dataset."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lib.agent_harnesses import (
    build_catalog,
    load_json,
    load_pinned_snapshot,
    serialize_catalog,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path)
    parser.add_argument("--overrides", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = args.source_manifest or args.source.with_name(
        args.source.stem + ".manifest.json"
    )
    try:
        source = load_pinned_snapshot(args.source, manifest)
        catalog = build_catalog(source, load_json(args.overrides))
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    rendered = serialize_catalog(catalog)
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            print("generated output is stale", file=sys.stderr)
            return 1
        print("agent-harness dataset is current")
        return 0
    write_json(args.output, catalog)
    print(f"upstream_projects={catalog['stats']['upstream_project_count']}")
    print(f"strict_runtimes={catalog['stats']['strict_runtime_count']}")
    print(f"adjacent_control_planes={catalog['stats']['adjacent_control_plane_count']}")
    print(f"dataset_sha256={catalog['_meta']['dataset_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
