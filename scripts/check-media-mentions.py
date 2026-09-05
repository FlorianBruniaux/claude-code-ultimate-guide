#!/usr/bin/env python3
"""Validate the confirmed mentions catalog and its review queue."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

try:
    import yaml
except ModuleNotFoundError as exc:  # pragma: no cover - environment guard
    raise SystemExit(
        "PyYAML is required. Run this script with the repository's Python environment "
        "or install the 'pyyaml' package."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "docs/media-mentions/mentions.yaml"
DEFAULT_QUEUE = ROOT / "docs/media-mentions/review-queue.yaml"
ALLOWED_PLATFORMS = {
    "article",
    "reddit",
    "linkedin-own",
    "linkedin-other",
    "twitter",
    "directory",
    "instagram",
    "podcast",
    "forum",
    "video",
    "translation",
}
TRACKING_QUERY_PREFIXES = ("utm_",)
TRACKING_QUERY_KEYS = {"fbclid", "gclid"}


def canonical_url(raw: str) -> str:
    parts = urlsplit(raw.strip())
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in TRACKING_QUERY_KEYS
        and not key.lower().startswith(TRACKING_QUERY_PREFIXES)
    ]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), "")
    )


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def validate(catalog_path: Path, queue_path: Path) -> list[str]:
    errors: list[str] = []
    catalog = load_yaml(catalog_path)
    queue = load_yaml(queue_path)
    mentions = catalog.get("mentions") or []

    if catalog.get("meta", {}).get("total_mentions") != len(mentions):
        errors.append(
            "meta.total_mentions does not match the number of confirmed mentions"
        )

    expected_ids = [f"{index:03d}" for index in range(1, len(mentions) + 1)]
    actual_ids = [str(item.get("id", "")) for item in mentions]
    if actual_ids != expected_ids:
        errors.append("confirmed mention IDs must be unique, sequential, and zero-padded")

    confirmed_urls: list[str] = []
    required = {
        "id",
        "platform",
        "url",
        "title",
        "author",
        "date",
        "angle",
        "reach",
        "status",
        "notes",
        "first_seen",
    }
    for item in mentions:
        mention_id = item.get("id", "unknown")
        missing = sorted(required - set(item))
        if missing:
            errors.append(f"mention {mention_id}: missing fields {', '.join(missing)}")
        platform = item.get("platform")
        if platform not in ALLOWED_PLATFORMS:
            errors.append(f"mention {mention_id}: unsupported platform {platform!r}")
        url = item.get("url")
        if not isinstance(url, str) or not url.startswith(("https://", "http://")):
            errors.append(f"mention {mention_id}: invalid URL")
        else:
            confirmed_urls.append(canonical_url(url))

    duplicates = sorted(
        url for url, count in Counter(confirmed_urls).items() if count > 1
    )
    if duplicates:
        errors.append(f"duplicate confirmed URLs: {', '.join(duplicates)}")

    queue_urls: list[str] = []
    for section in ("pending", "rejected"):
        for item in queue.get(section) or []:
            url = item.get("url")
            if not isinstance(url, str) or not url.startswith(("https://", "http://")):
                errors.append(f"review queue {item.get('id', 'unknown')}: invalid URL")
                continue
            queue_urls.append(canonical_url(url))

    queue_duplicates = sorted(
        url for url, count in Counter(queue_urls).items() if count > 1
    )
    if queue_duplicates:
        errors.append(f"duplicate review-queue URLs: {', '.join(queue_duplicates)}")

    overlap = sorted(set(confirmed_urls) & set(queue_urls))
    if overlap:
        errors.append(f"URLs cannot be both confirmed and queued: {', '.join(overlap)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    args = parser.parse_args()

    try:
        errors = validate(args.catalog, args.queue)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"media mentions validation failed: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    catalog = load_yaml(args.catalog)
    queue = load_yaml(args.queue)
    print(
        "media mentions valid: "
        f"{len(catalog.get('mentions') or [])} confirmed, "
        f"{len(queue.get('pending') or [])} pending, "
        f"{len(queue.get('rejected') or [])} rejected"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
