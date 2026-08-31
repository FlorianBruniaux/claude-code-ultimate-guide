#!/usr/bin/env python3
"""Unit tests for check-translations.py."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("check-translations.py")
SPEC = importlib.util.spec_from_file_location("check_translations", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def write_qmd(path: Path, language: str, version: str = "3.43.0", publication_version: str = "1.0.0") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f'lang: "{language}"\n'
        f'version: "{version}"\n'
        f'wp-version: "{publication_version}"\n'
        f'guide-version: "{version}"\n'
        "---\n\n# Test\n",
        encoding="utf-8",
    )


class TranslationStatusTests(unittest.TestCase):
    def test_extracts_markdown_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "guide.md"
            path.write_text("# Guide\n\n**Version**: 3.43.0\n", encoding="utf-8")
            self.assertEqual(MODULE.extract_guide_version(path), "3.43.0")

    def test_maintained_translation_requires_matching_source_hash(self) -> None:
        self.assertEqual(
            MODULE.expected_sync_state(
                "3.43.0",
                "3.43.0",
                canonical_sha256="abc",
                translated_from_sha256="def",
                maintained=True,
            ),
            "stale",
        )
        self.assertEqual(
            MODULE.expected_sync_state(
                "3.43.0",
                "3.43.0",
                canonical_sha256="abc",
                translated_from_sha256="abc",
                maintained=True,
            ),
            "current",
        )

    def test_publication_pairs_accept_translated_filenames_by_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_qmd(root / "whitepapers/fr/00-introduction.qmd", "fr")
            write_qmd(root / "whitepapers/en/00-introduction-en.qmd", "en")
            write_qmd(root / "cards/fr/c01-card.qmd", "fr")
            write_qmd(root / "cards/en/c01-card.qmd", "en")
            registry = {
                "paired_publications": {
                    "whitepapers": {
                        "roots": {"fr": "whitepapers/fr", "en": "whitepapers/en"},
                        "public_prefixes": ["00"],
                    },
                    "recap_cards": {
                        "roots": {"fr": "cards/fr", "en": "cards/en"},
                    },
                }
            }
            errors, stats = MODULE.validate_publication_pairs(registry, root)
            self.assertEqual(errors, [])
            self.assertEqual(
                stats,
                {"whitepapers": 1, "whitepaper_revision_differences": 0, "recap_cards": 1},
            )

    def test_publication_pairs_report_missing_recap_translation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_qmd(root / "whitepapers/fr/00-introduction.qmd", "fr")
            write_qmd(root / "whitepapers/en/00-introduction.qmd", "en")
            write_qmd(root / "cards/fr/c01-card.qmd", "fr")
            (root / "cards/en").mkdir(parents=True)
            registry = {
                "paired_publications": {
                    "whitepapers": {
                        "roots": {"fr": "whitepapers/fr", "en": "whitepapers/en"},
                        "public_prefixes": ["00"],
                    },
                    "recap_cards": {
                        "roots": {"fr": "cards/fr", "en": "cards/en"},
                    },
                }
            }
            errors, _ = MODULE.validate_publication_pairs(registry, root)
            self.assertTrue(any("Recap cards en: missing c01-card.qmd" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
