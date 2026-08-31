#!/usr/bin/env python3
"""Regression checks for check-media-mentions.py."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError as exc:  # pragma: no cover - environment guard
    raise SystemExit(
        "PyYAML is required. Run this test with the repository's Python environment "
        "or install the 'pyyaml' package."
    ) from exc


SCRIPT = Path(__file__).with_name("check-media-mentions.py")
SPEC = importlib.util.spec_from_file_location("check_media_mentions", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def mention(identifier: str, url: str) -> dict:
    return {
        "id": identifier,
        "platform": "article",
        "url": url,
        "title": "Example",
        "author": "Example",
        "date": None,
        "angle": "Explicit project reference.",
        "reach": "unknown",
        "status": "active",
        "notes": None,
        "first_seen": "2026-08-31",
    }


class MentionValidationTest(unittest.TestCase):
    def write_yaml(self, root: Path, name: str, data: dict) -> Path:
        path = root / name
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def test_accepts_separate_confirmed_and_review_urls(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = self.write_yaml(
                root,
                "mentions.yaml",
                {"meta": {"total_mentions": 1}, "mentions": [mention("001", "https://example.com/post/")]},
            )
            queue = self.write_yaml(
                root,
                "queue.yaml",
                {"pending": [{"id": "P001", "url": "https://example.org/mirror"}], "rejected": []},
            )
            self.assertEqual(MODULE.validate(catalog, queue), [])

    def test_rejects_canonical_url_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = self.write_yaml(
                root,
                "mentions.yaml",
                {"meta": {"total_mentions": 1}, "mentions": [mention("001", "https://EXAMPLE.com/post/?utm_source=test")]},
            )
            queue = self.write_yaml(
                root,
                "queue.yaml",
                {"pending": [{"id": "P001", "url": "https://example.com/post"}], "rejected": []},
            )
            errors = MODULE.validate(catalog, queue)
            self.assertTrue(any("both confirmed and queued" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
