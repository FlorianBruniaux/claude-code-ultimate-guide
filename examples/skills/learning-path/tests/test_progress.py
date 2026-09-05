"""Behaviour tests for the local learning-path progress engine."""

from __future__ import annotations

import contextlib
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import io
import json
from datetime import date
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest import mock


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

    def test_concurrent_profile_creation_allows_exactly_one_winner(self) -> None:
        worker_count = 16
        start = threading.Barrier(worker_count)

        def create_profile(index: int) -> str:
            start.wait()
            try:
                return progress.create_profile(self.root, self.path, "Beginner")["track"]
            except progress.ProgressError:
                return "rejected"

        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            results = list(executor.map(create_profile, range(worker_count)))

        self.assertEqual(results.count("Beginner"), 1)
        self.assertEqual(results.count("rejected"), worker_count - 1)
        self.assertEqual(progress.load_state(self.root, self.path)["track"], "Beginner")

    def test_atomic_save_leaves_complete_json_without_a_temporary_file(self) -> None:
        state = progress.new_state("Practitioner")
        progress.save_state(self.root, state, self.path)

        state_file = self.root / ".claude" / "learning" / "claude-code-guide-progress.json"
        self.assertEqual(json.loads(state_file.read_text(encoding="utf-8")), state)
        self.assertEqual(list(state_file.parent.glob("*.tmp")), [])

    def test_atomic_save_keeps_existing_bytes_when_replace_fails(self) -> None:
        original = progress.new_state("Beginner")
        progress.save_state(self.root, original, self.path)
        state_file = self.root / ".claude" / "learning" / "claude-code-guide-progress.json"
        original_bytes = state_file.read_bytes()

        with mock.patch.object(progress.os, "replace", side_effect=OSError("injected failure")):
            with self.assertRaisesRegex(progress.ProgressError, "Could not save"):
                progress.save_state(self.root, progress.new_state("Production"), self.path)

        self.assertEqual(state_file.read_bytes(), original_bytes)
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

        schedule = progress.review_schedule(state, self.path, "module-01")
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
            progress.load_state(self.root, self.path)

    def test_rejects_invalid_state_schema_against_the_path(self) -> None:
        state_file = self.root / ".claude" / "learning" / "claude-code-guide-progress.json"
        state_file.parent.mkdir(parents=True)
        cases = {
            "boolean version": {"version": True, "track": "Beginner", "modules": {}},
            "unknown track": {"version": 1, "track": "Unknown", "modules": {}},
            "unknown module": {
                "version": 1,
                "track": "Beginner",
                "modules": {"module-99": {"completed_on": "2026-08-31", "evidence": "note"}},
            },
            "module outside track": {
                "version": 1,
                "track": "Beginner",
                "modules": {"module-04": {"completed_on": "2026-08-31", "evidence": "note"}},
            },
        }

        for name, state in cases.items():
            with self.subTest(name=name):
                state_file.write_text(json.dumps(state), encoding="utf-8")
                with self.assertRaisesRegex(progress.ProgressError, "corrupt"):
                    progress.load_state(self.root, self.path)

    def test_state_commands_reject_corrupt_state_before_execution(self) -> None:
        state_file = self.root / ".claude" / "learning" / "claude-code-guide-progress.json"
        state_file.parent.mkdir(parents=True)
        corrupt = {
            "version": 1,
            "track": "Beginner",
            "modules": {"module-99": {"completed_on": "2026-08-31", "evidence": "note"}},
        }
        commands = (
            ["status"],
            ["next"],
            ["due"],
            ["complete", "module-01", "--evidence", "new note"],
        )

        for command in commands:
            with self.subTest(command=command):
                state_file.write_text(json.dumps(corrupt), encoding="utf-8")
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(progress.main(["--root", str(self.root)] + command), 2)


if __name__ == "__main__":
    unittest.main()
