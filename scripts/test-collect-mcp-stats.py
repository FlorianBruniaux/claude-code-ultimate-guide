#!/usr/bin/env python3
"""Offline contract tests for the public MCP statistics snapshot."""

from __future__ import annotations

import importlib.util
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "collect-mcp-stats.py"
FIXTURES = ROOT / "scripts" / "fixtures"
WORKFLOW = ROOT / ".github" / "workflows" / "collect-mcp-stats.yml"


def load_collector():
    if not SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location("collect_mcp_stats", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CollectorContractTests(unittest.TestCase):
    def test_executable_collector_exists(self):
        """Break caught: removing the collector makes refresh impossible."""
        self.assertTrue(SCRIPT.exists(), "collect-mcp-stats.py must exist")

    def setUp(self):
        self.collector = load_collector()
        if self.collector is None and self._testMethodName != "test_executable_collector_exists":
            self.skipTest("collector not implemented yet")

    def test_distribution_includes_zero_and_flags_only_the_large_outlier(self):
        """Break caught: dropping zero days or weakening MAD hides skew."""
        values = [0, 1, 2, 3, 4, 5, 6, 30]
        self.assertEqual(3.5, self.collector.median(values))
        self.assertEqual(2.0, self.collector.median_absolute_deviation(values))
        self.assertEqual([7], self.collector.detect_anomalies(values))

    def test_zero_mad_flags_values_different_from_the_median(self):
        """Break caught: dividing by zero loses anomalies in flat series."""
        self.assertEqual([0, 4], self.collector.detect_anomalies([0, 1, 1, 1, 9]))

    def test_empty_distributions_fail_closed(self):
        """Break caught: empty upstream data silently becomes a statistic."""
        with self.assertRaisesRegex(ValueError, "at least one daily value"):
            self.collector.median([])

    def test_periods_end_on_the_last_complete_utc_day(self):
        """Break caught: including the current partial day changes totals."""
        periods = self.collector.periods_for_snapshot(
            "2026-02-01T08:15:30Z", "2026-01-10T12:00:00.000Z"
        )
        self.assertEqual(
            {
                "year_to_date": ("2026-01-01", "2026-01-31"),
                "since_launch": ("2026-01-10", "2026-01-31"),
                "last_30_days": ("2026-01-02", "2026-01-31"),
                "last_7_days": ("2026-01-25", "2026-01-31"),
            },
            periods,
        )

    def test_fixture_snapshot_reconciles_totals_and_statistics(self):
        """Break caught: aggregate values drift from the checked daily series."""
        candidate = self.collector.collect_from_fixture_dir(FIXTURES)
        downloads = candidate["downloads"]
        self.assertEqual(
            {"start": "2026-01-01", "end": "2026-01-31", "count": 168},
            downloads["year_to_date"],
        )
        self.assertEqual(
            {"start": "2026-01-10", "end": "2026-01-31", "count": 136},
            downloads["since_launch"],
        )
        self.assertEqual(
            {"start": "2026-01-02", "end": "2026-01-31", "count": 168},
            downloads["last_30_days"],
        )
        self.assertEqual(
            {"start": "2026-01-25", "end": "2026-01-31", "count": 75},
            downloads["last_7_days"],
        )
        self.assertEqual(4.5, downloads["daily_median"])
        self.assertEqual(5.6, downloads["daily_mean"])
        self.assertEqual(40, downloads["daily_max"])
        self.assertEqual(2.5, downloads["daily_mad"])
        self.assertEqual(["2026-01-31"], downloads["anomaly_dates"])
        self.assertEqual(31, len(downloads["daily"]))
        self.assertEqual(0, downloads["daily"][0]["downloads"])
        self.assertFalse(downloads["daily"][0]["anomaly"])
        self.assertTrue(downloads["daily"][-1]["anomaly"])

    def test_snapshot_records_npm_time_and_registry_status_without_user_claims(self):
        """Break caught: public metadata is detached from its evidence boundary."""
        candidate = self.collector.collect_from_fixture_dir(FIXTURES)
        self.assertEqual("1.2.10", candidate["public_version"])
        self.assertEqual("2026-01-10T12:00:00.000Z", candidate["package_created_at"])
        self.assertEqual("2026-01-20T09:30:00.000Z", candidate["version_published_at"])
        self.assertEqual(
            {"name": "io.github.FlorianBruniaux/claude-code-guide", "published": False},
            candidate["registries"]["official_mcp"],
        )
        self.assertEqual(
            ["users", "active installations", "sessions", "executions"],
            candidate["methodology"]["not_equivalent_to"],
        )

    def test_schema_validation_rejects_missing_raw_series(self):
        """Break caught: CI accepts an aggregate snapshot with no auditable evidence."""
        candidate = self.collector.collect_from_fixture_dir(FIXTURES)
        self.assertEqual([], self.collector.validate_snapshot(candidate))
        broken = copy.deepcopy(candidate)
        del broken["downloads"]["daily"]
        self.assertIn("downloads.daily must be a non-empty array", self.collector.validate_snapshot(broken))

    def test_rejects_missing_duplicate_and_negative_daily_values(self):
        """Break caught: malformed daily evidence is accepted as complete."""
        valid = {
            "start": "2026-01-01",
            "end": "2026-01-03",
            "package": "claude-code-ultimate-guide-mcp",
            "downloads": [
                {"day": "2026-01-01", "downloads": 0},
                {"day": "2026-01-02", "downloads": 1},
                {"day": "2026-01-03", "downloads": 2},
            ],
        }
        for mutation, message in (
            ({**valid, "downloads": valid["downloads"][:2]}, "missing daily dates"),
            ({**valid, "downloads": [valid["downloads"][0]] * 3}, "duplicate daily date"),
            ({**valid, "downloads": [{"day": "2026-01-01", "downloads": -1}, *valid["downloads"][1:]]}, "non-negative integer"),
        ):
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                self.collector.validate_daily_range(mutation, "2026-01-01", "2026-01-03")

    def test_rejects_total_mismatch_non_utc_time_and_missing_version_time(self):
        """Break caught: contradictory or undated upstream metadata is published."""
        payload = json.loads((FIXTURES / "mcp-npm-range.json").read_text())
        point = {
            "start": payload["start"],
            "end": payload["end"],
            "package": payload["package"],
            "downloads": 999,
        }
        with self.assertRaisesRegex(ValueError, "total endpoint differs"):
            self.collector.reconcile_total(payload, point)

        with self.assertRaisesRegex(ValueError, "UTC timestamp"):
            self.collector.validate_snapshot_at("2026-02-01T00:00:00+01:00")

        metadata = json.loads((FIXTURES / "mcp-npm-metadata.json").read_text())
        del metadata["time"][metadata["dist-tags"]["latest"]]
        with self.assertRaisesRegex(ValueError, "absent from npm time metadata"):
            self.collector.validate_npm_metadata(metadata)

    def test_check_prints_candidate_without_writing_and_write_is_no_diff(self):
        """Break caught: validation mutates output or stable inputs churn bytes."""
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "mcp-stats.json"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--fixture-dir", str(FIXTURES), "--check", "--output", str(output)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse(output.exists())
            self.assertEqual(1, json.loads(result.stdout)["schema_version"])

            command = [sys.executable, str(SCRIPT), "--fixture-dir", str(FIXTURES), "--output", str(output)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(0, first.returncode, first.stderr)
            first_bytes = output.read_bytes()
            first_mtime = output.stat().st_mtime_ns
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertEqual(first_bytes, output.read_bytes())
            self.assertEqual(first_mtime, output.stat().st_mtime_ns)
            self.assertFalse(output.with_suffix(".json.tmp").exists())

    def test_changelog_renderer_updates_only_its_unreleased_marker(self):
        """Break caught: a scheduled refresh rewrites historical changelog prose."""
        candidate = self.collector.collect_from_fixture_dir(FIXTURES)
        source = (
            "# Changelog\n\n## [Unreleased]\n\n"
            "<!-- mcp-product:start -->\nproduct line\n<!-- mcp-product:end -->\n\n"
            "## [1.0.0]\n\nhistorical\n"
        )
        rendered = self.collector.render_changelog(source, candidate)
        self.assertIn("npm 1.2.10", rendered)
        self.assertIn("2026-01-10 through 2026-01-31: 136 downloads", rendered)
        self.assertIn("2026-01-02 through 2026-01-31: 168 downloads", rendered)
        self.assertIn("2026-01-25 through 2026-01-31: 75 downloads", rendered)
        self.assertIn("## [1.0.0]\n\nhistorical", rendered)
        self.assertNotIn('"daily"', rendered)
        self.assertEqual(rendered, self.collector.render_changelog(rendered, candidate))
        with self.assertRaisesRegex(ValueError, "exactly one mcp-product marker pair"):
            self.collector.render_changelog("## [Unreleased]\n", candidate)

    def test_daily_workflow_is_pinned_credential_free_and_path_scoped(self):
        """Break caught: automation gains broad credentials or commits unrelated files."""
        self.assertTrue(WORKFLOW.exists(), "collect-mcp-stats.yml must exist")
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(
            "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6",
            source,
        )
        self.assertIn("contents: write", source)
        self.assertNotIn("id-token: write", source)
        self.assertNotIn("GOOGLE_ACCESS_TOKEN", source)
        self.assertIn("python3 scripts/test-collect-mcp-stats.py", source)
        self.assertIn("python3 scripts/collect-mcp-stats.py --changelog CHANGELOG.md", source)
        self.assertIn("git add -- machine-readable/mcp-stats.json CHANGELOG.md", source)
        self.assertIn('git commit -m "chore(mcp): refresh public npm statistics"', source)
        self.assertNotIn("git add .", source)

        index_workflow = (ROOT / ".github" / "workflows" / "index-integrity.yml").read_text()
        self.assertIn("python3 scripts/test-collect-mcp-stats.py", index_workflow)
        self.assertIn(
            "python3 scripts/collect-mcp-stats.py --validate-file machine-readable/mcp-stats.json",
            index_workflow,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
