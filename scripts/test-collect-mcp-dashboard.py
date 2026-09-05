#!/usr/bin/env python3
"""Offline contract tests for the monthly MCP public dashboard."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "collect-mcp-dashboard.py"
FIXTURES = ROOT / "scripts" / "fixtures"
WORKFLOW = ROOT / ".github" / "workflows" / "collect-mcp-dashboard.yml"
INDEX_WORKFLOW = ROOT / ".github" / "workflows" / "index-integrity.yml"


def load_collector():
    if not SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location("collect_mcp_dashboard", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DashboardContractTests(unittest.TestCase):
    def test_executable_collector_exists(self):
        """Break caught: removing the dashboard collector makes refresh impossible."""
        self.assertTrue(SCRIPT.exists(), "collect-mcp-dashboard.py must exist")

    def setUp(self):
        self.collector = load_collector()
        if self.collector is None and self._testMethodName != "test_executable_collector_exists":
            self.skipTest("collector not implemented yet")

    def test_default_period_is_the_last_completed_calendar_month(self):
        """Break caught: a partial current month is presented as complete."""
        self.assertEqual(
            ("2026-07-01", "2026-07-31"),
            self.collector.last_completed_month("2026-08-31T12:30:00Z"),
        )
        self.assertEqual(
            ("2025-12-01", "2025-12-31"),
            self.collector.last_completed_month("2026-01-02T00:00:00Z"),
        )

    def test_fixture_dashboard_has_four_available_scoped_sources(self):
        """Break caught: a source loses its period, scope, definitions, or values."""
        dashboard = self.collector.collect_from_fixture_dir(FIXTURES)
        self.assertEqual(
            {"start": "2026-07-01", "end": "2026-07-31", "timezone": "UTC"},
            dashboard["period"],
        )
        self.assertEqual(
            ["npm", "gsc_landing", "gsc_portfolio", "ga4_portfolio"],
            list(dashboard["sources"]),
        )
        self.assertEqual({"downloads": 3210}, dashboard["sources"]["npm"]["values"])
        self.assertEqual(
            {"clicks": 12, "impressions": 480, "ctr": 0.025, "average_position": 8.75},
            dashboard["sources"]["gsc_landing"]["values"],
        )
        self.assertEqual(
            {"sessions": 42, "engaged_sessions": 31, "views": 58},
            dashboard["sources"]["ga4_portfolio"]["values"],
        )
        for source in dashboard["sources"].values():
            self.assertEqual("available", source["status"])
            self.assertRegex(source["retrieved_at"], r"Z$")
            self.assertIsInstance(source["scope"], dict)
            self.assertIsInstance(source["definitions"], dict)
            self.assertIsNone(source["reason"])

    def test_missing_google_configuration_is_unavailable_not_zero(self):
        """Break caught: missing Google access is misreported as zero traffic."""
        dashboard = self.collector.build_unavailable_dashboard(
            npm_payload={"start": "2026-07-01", "end": "2026-07-31", "package": "claude-code-ultimate-guide-mcp", "downloads": 3210},
            snapshot_at="2026-08-31T12:30:00Z",
            environment={},
        )
        self.assertEqual("available", dashboard["sources"]["npm"]["status"])
        for name in ("gsc_landing", "gsc_portfolio", "ga4_portfolio"):
            source = dashboard["sources"][name]
            self.assertEqual("unavailable", source["status"])
            self.assertIsNone(source["values"])
            self.assertIsInstance(source["reason"], str)
            self.assertNotEqual("", source["reason"])
        serialized = json.dumps(dashboard)
        self.assertNotIn("GOOGLE_ACCESS_TOKEN\":", serialized)

    def test_google_queries_are_page_exact_and_publish_only_aggregate_metrics(self):
        """Break caught: a broad query exposes unrelated pages or dimensions."""
        gsc = self.collector.gsc_query(
            "2026-07-01", "2026-07-31", "https://cc.bruniaux.com/mcp/"
        )
        self.assertEqual(["page"], gsc["dimensions"])
        self.assertEqual(
            {"dimension": "page", "operator": "equals", "expression": "https://cc.bruniaux.com/mcp/"},
            gsc["dimensionFilterGroups"][0]["filters"][0],
        )
        self.assertEqual(1, gsc["rowLimit"])

        ga4 = self.collector.ga4_query(
            "2026-07-01", "2026-07-31", "/blog/articles/claude-code-guide-mcp/"
        )
        self.assertEqual([{"name": "pagePath"}], ga4["dimensions"])
        self.assertEqual(
            [{"name": "sessions"}, {"name": "engagedSessions"}, {"name": "screenPageViews"}],
            ga4["metrics"],
        )
        self.assertEqual(
            {"fieldName": "pagePath", "stringFilter": {"matchType": "EXACT", "value": "/blog/articles/claude-code-guide-mcp/"}},
            ga4["dimensionFilter"]["filter"],
        )
        forbidden = ("user", "demographic", "device", "country", "city", "identifier")
        lowered = json.dumps(ga4).lower()
        self.assertFalse(any(word in lowered for word in forbidden))

    def test_empty_gsc_result_keeps_position_unknown(self):
        """Break caught: no impressions are published as a measured position of zero."""
        values = self.collector.parse_gsc(
            {"rows": []}, "https://cc.bruniaux.com/mcp/"
        )
        self.assertEqual(0, values["clicks"])
        self.assertEqual(0, values["impressions"])
        self.assertEqual(0.0, values["ctr"])
        self.assertIsNone(values["average_position"])

    def test_fixture_cli_check_is_read_only_and_unavailable_mode_is_explicit(self):
        """Break caught: check mode writes or absent credentials erase source status."""
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "mcp-dashboard.json"
            check = subprocess.run(
                [sys.executable, str(SCRIPT), "--fixture-dir", str(FIXTURES), "--check", "--output", str(output)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, check.returncode, check.stderr)
            self.assertFalse(output.exists())
            self.assertEqual("available", json.loads(check.stdout)["sources"]["gsc_landing"]["status"])

            environment = {key: value for key, value in os.environ.items() if not key.startswith("MCP_G") and key != "GOOGLE_ACCESS_TOKEN"}
            unavailable = subprocess.run(
                [sys.executable, str(SCRIPT), "--fixture-npm", str(FIXTURES / "mcp-dashboard-npm.json"), "--snapshot-at", "2026-08-31T12:30:00Z", "--check", "--output", str(output)],
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertEqual(0, unavailable.returncode, unavailable.stderr)
            payload = json.loads(unavailable.stdout)
            self.assertIsNone(payload["sources"]["gsc_landing"]["values"])
            self.assertEqual("unavailable", payload["sources"]["ga4_portfolio"]["status"])

    def test_monthly_workflow_separates_public_and_oidc_paths(self):
        """Break caught: missing Google configuration either blocks npm or grants needless OIDC."""
        self.assertTrue(WORKFLOW.exists(), "collect-mcp-dashboard.yml must exist")
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("d23441a48e516b6c34aea4fa41551a30e30af803", source)
        self.assertIn("c200f3691d83b41bf9bbd8638997a462592937ed", source)
        self.assertIn("collect-public-only:", source)
        self.assertIn("collect-with-google:", source)
        public_job = source.split("collect-public-only:", 1)[1].split("collect-with-google:", 1)[0]
        google_job = source.split("collect-with-google:", 1)[1]
        self.assertNotIn("id-token: write", public_job)
        self.assertIn("id-token: write", google_job)
        self.assertIn("token_format: access_token", google_job)
        self.assertIn("GOOGLE_ACCESS_TOKEN: ${{ steps.google-auth.outputs.access_token }}", google_job)
        self.assertIn("python3 scripts/test-collect-mcp-dashboard.py", source)
        self.assertIn("machine-readable/mcp-dashboard.json", source)
        self.assertNotIn("client_secret", source.lower())

        index_source = INDEX_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("scripts/test-collect-mcp-dashboard.py", index_source)
        self.assertIn(
            "scripts/collect-mcp-dashboard.py --validate-file machine-readable/mcp-dashboard.json",
            index_source,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
