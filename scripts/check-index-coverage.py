#!/usr/bin/env python3
"""Check that every guide file is reachable from the machine-readable index.

`validate-reference-yaml.py` answers "do the references in reference.yaml still
resolve?". This script answers the opposite question, the one that has actually
bitten this repo: "did anything get added to guide/ that reference.yaml never
learned about?" A page nobody indexed is invisible to the MCP server, to the
landing's Cmd+K palette, and to any LLM reading the index instead of the repo.

Modes:
  --check                 exit 1 if any tracked guide file is unindexed
  --check --max-missing N ratchet, exit 1 only above N (must only go down)
  --staged                restrict to files staged for commit (hook use)
  --quiet                 print only the verdict line

Exit codes: 0 clean or within ratchet, 1 over budget, 2 usage or IO error.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INDEX = REPO / "machine-readable" / "reference.yaml"
GUIDE = REPO / "guide"

# Files that exist for humans browsing the tree, not as indexable content.
EXEMPT_NAMES = {"README.md"}
EXEMPT_SUFFIXES = (".fr.md",)  # translations follow their English source


def tracked_guide_files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "guide/**/*.md", "guide/*.md"],
        cwd=REPO, capture_output=True, text=True, check=False,
    ).stdout
    files = []
    for line in out.splitlines():
        p = REPO / line.strip()
        if not line.strip() or p.name in EXEMPT_NAMES:
            continue
        if any(line.endswith(s) for s in EXEMPT_SUFFIXES):
            continue
        files.append(p)
    return sorted(set(files))


def staged_guide_files() -> list[Path]:
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "--", "guide/"],
        cwd=REPO, capture_output=True, text=True, check=False,
    ).stdout
    files = []
    for line in out.splitlines():
        line = line.strip()
        if not line.endswith(".md") or Path(line).name in EXEMPT_NAMES:
            continue
        if any(line.endswith(s) for s in EXEMPT_SUFFIXES):
            continue
        files.append(REPO / line)
    return sorted(set(files))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--max-missing", type=int, default=0)
    args = ap.parse_args()

    if not INDEX.exists():
        print(f"error: {INDEX} not found", file=sys.stderr)
        return 2

    # Substring match against the raw text rather than a YAML parse: an entry is
    # "covered" if its path appears anywhere, whatever key or nesting holds it.
    index_text = INDEX.read_text(encoding="utf-8")

    files = staged_guide_files() if args.staged else tracked_guide_files()
    missing = [f for f in files if f.relative_to(REPO).as_posix() not in index_text]

    if not args.quiet:
        for f in missing:
            print(f"  unindexed  {f.relative_to(REPO).as_posix()}")

    scope = "staged" if args.staged else "tracked"
    print(
        f"index coverage: {len(files) - len(missing)}/{len(files)} {scope} guide files "
        f"referenced in machine-readable/reference.yaml"
    )

    if not args.check:
        return 0
    if len(missing) > args.max_missing:
        print(
            f"FAIL: {len(missing)} unindexed (budget {args.max_missing}). "
            f"Add a deep_dive entry per file, then rebuild the landing search index "
            f"with `pnpm build:search`.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
