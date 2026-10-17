#!/usr/bin/env python3
"""Synchronize the release-tracking skill from its Claude source to Codex."""
import argparse
import json
from pathlib import Path

FILES = ("SKILL.md", "evals/scenarios.json")

def synchronize(root, write=False):
    source = root / ".claude/skills/source-command-update-infos-release"
    target = root / ".agents/skills/source-command-update-infos-release"
    corpus = json.loads((source / FILES[1]).read_text())
    if corpus.get("skill") != "source-command-update-infos-release" or len(corpus.get("positive", [])) < 8 or len(corpus.get("negative", [])) < 2:
        raise ValueError("Invalid release-tracking routing corpus")
    drift = []
    for relative in FILES:
        expected = (source / relative).read_bytes()
        destination = target / relative
        if write:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(expected)
        if not destination.is_file() or destination.read_bytes() != expected:
            drift.append(str(destination.relative_to(root)))
    return drift

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--write", action="store_true")
    args = parser.parse_args()
    drift = synchronize(Path(__file__).resolve().parents[1], args.write)
    print("Projection differs: " + ", ".join(drift) if drift else "Claude/Codex release-tracking skill and routing scenarios match.")
    return int(bool(drift))

if __name__ == "__main__":
    raise SystemExit(main())
