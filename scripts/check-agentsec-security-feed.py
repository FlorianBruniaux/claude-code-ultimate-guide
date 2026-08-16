#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEED_RELATIVE = Path("machine-readable/agentsec-security-feed.v1.json")
DATABASE_RELATIVE = Path("examples/commands/resources/threat-db.yaml")
REQUIRED_KEYS = {
    "schema_version",
    "content_license",
    "agentsec",
    "database",
    "landing_metrics",
    "intelligence",
    "detectors",
    "input_digests",
}
VERSION_PATTERN = re.compile(r'^version:\s*["\']?([^"\'\s#]+)', re.MULTILINE)


class FeedCheckError(Exception):
    pass


def _read(path: Path, label: str) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise FeedCheckError(f"cannot read {label}: {path}") from exc


def _mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        raise FeedCheckError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _load_feed(path: Path) -> tuple[dict[str, object], bytes]:
    raw = _read(path, "guide feed")
    try:
        loaded = cast(object, json.loads(raw))
    except json.JSONDecodeError as exc:
        raise FeedCheckError("guide feed is not valid JSON") from exc
    feed = _mapping(loaded, "guide feed")
    missing = sorted(REQUIRED_KEYS - set(feed))
    if missing:
        raise FeedCheckError(f"missing required feed keys: {', '.join(missing)}")
    if feed.get("schema_version") != "1":
        raise FeedCheckError("unsupported feed schema version")
    if feed.get("content_license") != "CC-BY-SA-4.0":
        raise FeedCheckError("unexpected feed content license")
    _mapping(feed.get("agentsec"), "feed agentsec")
    _mapping(feed.get("database"), "feed database")
    _mapping(feed.get("landing_metrics"), "feed landing metrics")
    intelligence = _mapping(feed.get("intelligence"), "feed intelligence")
    if not isinstance(intelligence.get("events"), list) or not isinstance(
        intelligence.get("sources"), list
    ):
        raise FeedCheckError("feed intelligence events and sources must be arrays")
    if not isinstance(feed.get("detectors"), list):
        raise FeedCheckError("feed detectors must be an array")
    _mapping(feed.get("input_digests"), "feed input digests")
    return feed, raw


def _database_version(path: Path) -> str:
    try:
        content = _read(path, "guide threat database").decode("utf-8")
    except UnicodeError as exc:
        raise FeedCheckError("guide threat database is not UTF-8") from exc
    match = VERSION_PATTERN.search(content)
    if match is None:
        raise FeedCheckError("guide threat database has no top-level version")
    return match.group(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check the AgentSec feed mirror in the guide.")
    parser.add_argument("--guide-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--feed", type=Path)
    parser.add_argument("--threat-database", type=Path)
    parser.add_argument("--agentsec-feed", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    feed_path = arguments.feed or arguments.guide_root / FEED_RELATIVE
    database_path = arguments.threat_database or arguments.guide_root / DATABASE_RELATIVE
    try:
        feed, feed_raw = _load_feed(feed_path)
        feed_database = _mapping(feed["database"], "feed database")
        feed_version = feed_database.get("version")
        guide_version = _database_version(database_path)
        if feed_version != guide_version:
            raise FeedCheckError(
                "threat database version differs: "
                f"guide={guide_version} agentsec={feed_version}"
            )
        if arguments.agentsec_feed is not None:
            canonical = _read(arguments.agentsec_feed, "AgentSec canonical feed")
            if canonical != feed_raw:
                raise FeedCheckError("guide mirror differs from AgentSec canonical feed")
    except FeedCheckError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    digest = hashlib.sha256(feed_raw).hexdigest()
    print(f"AgentSec feed compatible database={guide_version} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
