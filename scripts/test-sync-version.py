#!/usr/bin/env python3
"""Exercise version sync without rewriting historical references or headings."""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("sync-version.sh")


class VersionSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        shutil.copyfile(SCRIPT, self.root / "scripts/sync-version.sh")
        # Translation provenance has its own integration suite; isolate this
        # fixture from Git history so failures concern version metadata only.
        (self.root / "scripts/check-translations.py").write_text("", encoding="utf-8")
        (self.root / "VERSION").write_text("3.44.0\n", encoding="utf-8")
        files = {
            "README.md": "Guide-v3.44.0-brightgreen\n*Version 3.44.0 | Updated daily*\nHistorical release 3.30.0\n",
            "guide/cheatsheet.md": "**Version**: 3.44.0 | **Last Updated**: Oct 6, 2026\n*Last updated: Oct 6, 2026 | Version 3.44.0*\nExample 3.30.0\n",
            "guide/ultimate-guide.md": "**Version**: 3.44.0\n### 3.5.3 Version control & backup\n**Last updated**: Oct 6, 2026 | **Version**: 3.44.0\n",
            "machine-readable/reference.yaml": 'version: "3.44.0"\n  aligned_with_guide: "3.44.0"\n  note: "Introduced in v3.30.0"\n',
        }
        for name, contents in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")

    def run_sync(self):
        return subprocess.run(
            ["bash", str(self.root / "scripts/sync-version.sh"), "--check"],
            capture_output=True, text=True,
        )

    def test_historical_versions_and_section_numbers_do_not_fail_check(self):
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_old_version_field_fails_even_when_current_version_appears_elsewhere(self):
        path = self.root / "guide/ultimate-guide.md"
        path.write_text("**Version**: 3.43.0\nExample refers to v3.44.0\n", encoding="utf-8")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("3.43.0", result.stdout)


if __name__ == "__main__":
    unittest.main()
