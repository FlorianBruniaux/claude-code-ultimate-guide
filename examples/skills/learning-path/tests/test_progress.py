"""Behaviour tests for the local learning-path progress engine."""

from __future__ import annotations

import importlib.util
import json
from datetime import date
from pathlib import Path
import sys
import tempfile
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "progress.py"
SPEC = importlib.util.spec_from_file_location("learning_progress", SCRIPT)
assert SPEC and SPEC.loader
progress = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = progress
SPEC.loader.exec_module(progress)


class ProgressTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.path = progress.load_path(SKILL_ROOT / "assets" / "path.yaml")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_creates_a_new_beginner_profile_outside_the_skill(self) -> None:
        state = progress.create_profile(self.root, self.path, "Beginner")

        state_file = self.root / ".claude" / "learning" / "claude-code-guide-progress.json"
        self.assertEqual(state["track"], "Beginner")
        self.assertTrue(state_file.is_file())
        self.assertEqual(json.loads(state_file.read_text(encoding="utf-8"))["modules"], {})

    def test_atomic_save_leaves_complete_json_without_a_temporary_file(self) -> None:
        state = progress.new_state("Practitioner")
        progress.save_state(self.root, state)

        state_file = self.root / ".claude" / "learning" / "claude-code-guide-progress.json"
        self.assertEqual(json.loads(state_file.read_text(encoding="utf-8")), state)
        self.assertEqual(list(state_file.parent.glob("*.tmp")), [])

    def test_rejects_completion_when_a_prerequisite_is_incomplete(self) -> None:
        state = progress.new_state("Production")

        with self.assertRaisesRegex(progress.ProgressError, "requires module-01"):
            progress.complete_module(state, self.path, "module-02", "I ran the core loop exercise")

    def test_rejects_completion_without_a_non_empty_evidence_note(self) -> None:
        state = progress.new_state("Beginner")

        with self.assertRaisesRegex(progress.ProgressError, "evidence note"):
            progress.complete_module(state, self.path, "module-01", "   ")

    def test_next_module_selects_the_first_available_module_for_the_track(self) -> None:
        state = progress.new_state("Practitioner")
        progress.complete_module(state, self.path, "module-01", "Installed Claude Code and ran /help")

        self.assertEqual(progress.next_module(state, self.path)["id"], "module-02")

    def test_review_schedule_uses_the_required_intervals(self) -> None:
        state = progress.new_state("Beginner")
        progress.complete_module(
            state,
            self.path,
            "module-01",
            "Installed Claude Code and recorded the version",
            completed_on=date(2026, 8, 31),
        )

        schedule = progress.review_schedule(state, "module-01")
        self.assertEqual(
            [(entry["interval_days"], entry["due_on"]) for entry in schedule],
            [
                (1, "2026-09-01"),
                (3, "2026-09-03"),
                (7, "2026-09-07"),
                (14, "2026-09-14"),
                (30, "2026-09-30"),
                (60, "2026-10-30"),
                (90, "2026-11-29"),
            ],
        )

    def test_corrupt_state_fails_closed(self) -> None:
        state_file = self.root / ".claude" / "learning" / "claude-code-guide-progress.json"
        state_file.parent.mkdir(parents=True)
        state_file.write_text("not json", encoding="utf-8")

        with self.assertRaisesRegex(progress.ProgressError, "corrupt"):
            progress.load_state(self.root)


if __name__ == "__main__":
    unittest.main()
