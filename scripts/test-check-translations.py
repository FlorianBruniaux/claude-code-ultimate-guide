#!/usr/bin/env python3
"""Unit tests for check-translations.py."""

from __future__ import annotations

import importlib.util
import copy
import json
import subprocess
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

    def test_git_lag_counts_guide_and_repository_commits_separately(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._git(root, "init")
            self._git(root, "config", "user.email", "tests@example.invalid")
            self._git(root, "config", "user.name", "Translation Tests")
            guide = root / "guide.md"
            guide.write_text("baseline\n", encoding="utf-8")
            self._git(root, "add", "guide.md")
            self._git(root, "commit", "-m", "baseline")
            source = self._git(root, "rev-parse", "HEAD")
            (root / "other.txt").write_text("other\n", encoding="utf-8")
            self._git(root, "add", "other.txt")
            self._git(root, "commit", "-m", "other")
            guide.write_text("baseline\nchanged\n", encoding="utf-8")
            self._git(root, "add", "guide.md")
            self._git(root, "commit", "-m", "guide")

            self.assertEqual(
                {"canonical_guide_commits": 1, "canonical_repo_commits": 2},
                MODULE.compute_git_lag(root, source, "guide.md"),
            )

    def test_checked_in_registry_passes_evidence_validation(self) -> None:
        root = Path(__file__).resolve().parents[1]
        registry = json.loads(
            (root / "machine-readable/translations.json").read_text(encoding="utf-8")
        )

        self.assertEqual([], MODULE.validate_evidence_registry(registry, root))
        chinese = next(item for item in registry["translations"] if item["language"] == "zh-CN")
        self.assertEqual(
            "7b43b9c10b241f8e196e27651e3fea6079a48d26",
            chinese["translated_from"]["commit"],
        )
        self.assertIn("es-419", {item["language"] for item in registry["translations"]})

    def test_community_translation_cannot_be_project_official(self) -> None:
        root = Path(__file__).resolve().parents[1]
        registry = json.loads(
            (root / "machine-readable/translations.json").read_text(encoding="utf-8")
        )
        modified = copy.deepcopy(registry)
        chinese = next(item for item in modified["translations"] if item["language"] == "zh-CN")
        chinese["status"] = "official"

        errors = MODULE.validate_evidence_registry(modified, root)

        self.assertTrue(any("must remain unofficial" in error for error in errors), errors)

    def test_unknown_source_requires_unknown_numeric_lag(self) -> None:
        root = Path(__file__).resolve().parents[1]
        registry = json.loads(
            (root / "machine-readable/translations.json").read_text(encoding="utf-8")
        )
        modified = copy.deepcopy(registry)
        ukrainian = next(item for item in modified["translations"] if item["language"] == "uk")
        ukrainian["known_lag"]["canonical_repo_commits"] = 1

        errors = MODULE.validate_evidence_registry(modified, root)

        self.assertTrue(any("unknown numeric lag" in error for error in errors), errors)

    @staticmethod
    def _git(root: Path, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()


if __name__ == "__main__":
    unittest.main()
