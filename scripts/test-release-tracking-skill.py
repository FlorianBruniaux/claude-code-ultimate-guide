#!/usr/bin/env python3
"""Check that release tracking has one workflow and two matching projections."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sync_release", ROOT / "scripts/sync-release-tracking-skill.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for host in (".claude", ".agents"):
            relative = Path(host) / "skills/source-command-update-infos-release"
            shutil.copytree(ROOT / relative, self.root / relative)

    def test_check_detects_drift_without_writing(self):
        target = self.root / ".agents/skills/source-command-update-infos-release/SKILL.md"
        target.write_text("Concurrent content")
        self.assertEqual(len(sync.synchronize(self.root)), 1)
        self.assertEqual(target.read_text(), "Concurrent content")

    def test_explicit_write_restores_both_resources(self):
        target = self.root / ".agents/skills/source-command-update-infos-release"
        shutil.rmtree(target)
        self.assertEqual(len(sync.synchronize(self.root)), 2)
        self.assertEqual(sync.synchronize(self.root, write=True), [])
        self.assertEqual(sync.synchronize(self.root), [])

    def test_invalid_corpus_refused_before_write(self):
        source = self.root / ".claude/skills/source-command-update-infos-release/evals/scenarios.json"
        source.write_text(json.dumps({"skill": "different", "positive": [], "negative": []}))
        target = self.root / ".agents/skills/source-command-update-infos-release/SKILL.md"
        target.write_text("Preserve existing projection")
        with self.assertRaises(ValueError):
            sync.synchronize(self.root, write=True)
        self.assertEqual(target.read_text(), "Preserve existing projection")

    def test_installed_project_contract_is_canonical(self):
        self.assertEqual(sync.synchronize(ROOT), [])
        wrapper = (ROOT / ".claude/skills/source-command-update-infos-release/SKILL.md").read_text()
        self.assertIn("`.claude/commands/update-infos-release.md`", wrapper)
        self.assertNotIn("git reset --hard", wrapper)
        self.assertNotIn("Codex-releases.yaml", wrapper)
        command = (ROOT / ".claude/commands/update-infos-release.md").read_text()
        section = command.split("### 4.5.", 1)[1].split("### 4.7.", 1)[0]
        self.assertIn("do not add a second manual Claude Code release item", section)
        self.assertIn("including a release of the guide itself", section)
        self.assertNotIn("#vX.Y.Z", section)


if __name__ == "__main__":
    unittest.main()
