#!/usr/bin/env python3
"""Regression tests for the generated Agent Harness Landscape regions."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/build-agent-harness-page.py"
CATALOG_PATH = ROOT / "machine-readable/agent-harnesses.json"
PAGE_PATH = ROOT / "guide/ecosystem/agent-harness-landscape.md"


def load_builder():
    spec = importlib.util.spec_from_file_location("agent_harness_page", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load page builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bind_catalog_checksum(catalog: dict) -> dict:
    catalog["_meta"].pop("dataset_sha256", None)
    payload = json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    catalog["_meta"]["dataset_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    return catalog


class AgentHarnessPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = load_builder()
        cls.catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        cls.page = PAGE_PATH.read_text(encoding="utf-8")

    def test_generated_markers_occur_once(self):
        for marker in (
            "category-summary",
            "strict-runtime-map",
            "adjacent-control-planes",
            "project-catalog",
        ):
            self.assertEqual(1, self.page.count(f"BEGIN GENERATED: {marker}"))
            self.assertEqual(1, self.page.count(f"END GENERATED: {marker}"))

    def test_rendered_counts_match_canonical_sets(self):
        self.assertEqual(12, self.builder.render_category_summary(self.catalog).count("\n| ["))
        self.assertEqual(42, self.builder.count_table_records(self.builder.render_strict_runtime_map(self.catalog)))
        self.assertEqual(15, self.builder.count_table_records(self.builder.render_adjacent_control_planes(self.catalog)))
        directory = self.builder.render_project_catalog(self.catalog)
        self.assertEqual(12, directory.count("<details>"))
        self.assertEqual(160, self.builder.count_upstream_project_links(directory))
        self.assertIn("Guide supplements (32)", directory)

    def test_every_runtime_and_control_plane_cell_has_external_project_link(self):
        for fragment in (
            self.builder.render_strict_runtime_map(self.catalog),
            self.builder.render_adjacent_control_planes(self.catalog),
        ):
            rows = [line for line in fragment.splitlines() if line.startswith("| ")][1:]
            self.assertTrue(rows)
            for row in rows:
                first_cell = row.split("|", 2)[1]
                self.assertRegex(first_cell, r"\[[^]]+\]\(https://[^)]+\)")
                self.assertNotRegex(first_cell, r"\]\((?:\.\.?/|/guide/)")

    def test_all_192_directory_rows_link_to_external_projects(self):
        directory = self.builder.render_project_catalog(self.catalog)
        rows = [line for line in directory.splitlines() if line.startswith("| [")]
        self.assertEqual(192, len(rows))
        for row in rows:
            first_cell = row.split("|", 2)[1]
            self.assertRegex(first_cell, r"\[[^]]+\]\(https://[^)]+\)")

    def test_stars_render_only_with_repository_and_capture_date(self):
        records = self.builder.project_index(self.catalog)
        for mapping in self.catalog["sets"]["strict_runtime_map"]:
            record = records[mapping["project_ref"]]
            cell = self.builder.render_project_cell(record)
            if "★" in cell:
                self.assertIsNotNone(record["repository_url"])
                self.assertIsNotNone(record["stars_captured_at"])
                self.assertIsInstance(record["stars"], int)

    def test_page_builder_can_apply_an_optional_github_sidecar(self):
        """Break caught: the renderer cannot consume verified volatile observations."""
        catalog = bind_catalog_checksum({
            "_meta": {},
            "sets": {
                "upstream_snapshot": {"projects": [{
                    "repository_url": "https://github.com/owner/repo",
                    "stars": 1,
                    "stars_captured_at": "2026-08-20",
                    "archived": "unknown",
                }]},
                "guide_supplement": [],
            },
        })
        sidecar = {
            "schema_version": "1.0.0",
            "catalog_sha256": catalog["_meta"]["dataset_sha256"],
            "captured_at": "2026-08-29T12:00:00Z",
            "repositories": [{
                "repository_url": "https://github.com/owner/repo",
                "resolved_full_name": "owner/repo",
                "stargazers_count": 42,
                "archived": True,
                "language": "Python",
                "license_spdx": "MIT",
                "pushed_at": "2026-08-28T12:00:00Z",
                "default_branch": "main",
                "captured_at": "2026-08-29T12:00:00Z",
            }],
        }
        merged = self.builder.apply_github_sidecar(catalog, sidecar)
        record = merged["sets"]["upstream_snapshot"]["projects"][0]
        self.assertEqual(42, record["stars"])
        self.assertEqual("2026-08-29", record["stars_captured_at"])
        self.assertTrue(record["archived"])
        self.assertEqual(1, catalog["sets"]["upstream_snapshot"]["projects"][0]["stars"])

    def test_page_builder_rejects_a_stale_catalog_checksum(self):
        catalog = bind_catalog_checksum({
            "_meta": {},
            "sets": {"upstream_snapshot": {"projects": []}, "guide_supplement": []},
        })
        catalog["sets"]["upstream_snapshot"]["projects"].append({"name": "tampered"})

        with self.assertRaisesRegex(ValueError, "catalog checksum is invalid"):
            self.builder.apply_github_sidecar(catalog, {})

    def test_page_builder_rejects_incomplete_or_invalid_sidecars(self):
        catalog = bind_catalog_checksum({
            "_meta": {},
            "sets": {
                "upstream_snapshot": {"projects": [{"repository_url": "https://github.com/owner/repo"}]},
                "guide_supplement": [],
            },
        })
        valid = {
            "schema_version": "1.0.0",
            "catalog_sha256": catalog["_meta"]["dataset_sha256"],
            "captured_at": "2026-08-29T12:00:00Z",
            "repositories": [{
                "repository_url": "https://github.com/owner/repo",
                "resolved_full_name": "owner/repo",
                "stargazers_count": 42,
                "archived": False,
                "language": None,
                "license_spdx": None,
                "pushed_at": None,
                "default_branch": "main",
                "captured_at": "2026-08-29T12:00:00Z",
            }],
        }
        hostile = []
        for mutate in (
            lambda value: value.update(schema_version="2.0.0"),
            lambda value: value["repositories"][0].update(stargazers_count=-1),
            lambda value: value["repositories"][0].pop("default_branch"),
            lambda value: value["repositories"][0].update(captured_at="not-a-date"),
        ):
            candidate = json.loads(json.dumps(valid))
            mutate(candidate)
            hostile.append(candidate)

        for candidate in hostile:
            with self.subTest(candidate=candidate):
                with self.assertRaises(ValueError):
                    self.builder.apply_github_sidecar(catalog, candidate)

        for invalid_timestamp in ("2026-08-29Z", "2026-08-29 12:00:00Z", "2026-08-29T12:00:00+00:00"):
            candidate = json.loads(json.dumps(valid))
            candidate["captured_at"] = invalid_timestamp
            candidate["repositories"][0]["captured_at"] = invalid_timestamp
            with self.subTest(invalid_timestamp=invalid_timestamp):
                with self.assertRaisesRegex(ValueError, "RFC 3339 UTC timestamp"):
                    self.builder.apply_github_sidecar(catalog, candidate)

    def test_generated_summaries_are_plain_short_sentences(self):
        sample = {
            "summary": (
                "A **runtime** with `tools` and a long marketing clause that should not leak into the "
                "reader-facing table. A second sentence must not be rendered."
            )
        }
        rendered = self.builder.concise_summary(sample)
        self.assertEqual(
            "A runtime with tools and a long marketing clause that should not leak into the reader-facing table.",
            rendered,
        )
        self.assertLessEqual(len(rendered), 180)
        self.assertNotIn("**", rendered)
        self.assertNotIn("`", rendered)

    def test_generated_summaries_normalize_em_dash(self):
        self.assertEqual(
            "Runtime: provider-neutral and local.",
            self.builder.concise_summary({"summary": "Runtime—provider-neutral and local."}),
        )

    def test_unknown_table_values_render_as_accessible_question_marks(self):
        marker = '<abbr title="Not established from the pinned sources">?</abbr>'
        self.assertEqual(marker, self.builder.humanize(None))
        self.assertEqual(marker, self.builder.humanize(""))
        self.assertEqual(marker, self.builder.humanize("unknown"))
        self.assertEqual("N/A", self.builder.humanize("not_applicable"))

        for fragment in (
            self.builder.render_strict_runtime_map(self.catalog),
            self.builder.render_adjacent_control_planes(self.catalog),
            self.builder.render_project_catalog(self.catalog),
        ):
            self.assertNotIn("Unknown", fragment)

    def test_strict_runtime_map_explains_compact_markers(self):
        rendered = self.builder.render_strict_runtime_map(self.catalog)
        self.assertIn("**Legend:**", rendered)
        self.assertIn("not established from the pinned sources", rendered)
        self.assertIn("N/A = does not apply", rendered)

    def test_guide_profile_anchors_exist(self):
        profile_page = (ROOT / "guide/ecosystem/agentic-tools.md").read_text(encoding="utf-8")
        anchors = set()
        for heading in re.findall(r"^#{1,6}\s+(.+)$", profile_page, re.MULTILINE):
            slug = heading.casefold()
            slug = re.sub(r"[`*_]", "", slug)
            slug = re.sub(r"[^\w\s-]", "", slug)
            slug = re.sub(r"[\s-]+", "-", slug).strip("-")
            anchors.add(slug)
        for target in self.builder.GUIDE_PROFILES.values():
            anchor = target.split("#", 1)[1]
            self.assertIn(anchor, anchors, target)

    def test_second_build_is_byte_stable(self):
        first = self.builder.build_page(self.page, self.catalog)
        second = self.builder.build_page(first, self.catalog)
        self.assertEqual(first, second)

    def test_page_keeps_source_criticism_and_trial_protocol(self):
        built = self.builder.build_page(self.page, self.catalog)
        for required in (
            "160 Projects Does Not Mean 160 Runtime Harnesses",
            "86 deep-dive profiles",
            "8 to 12 representative tasks",
            "accepted-task cost",
            "claude-code-guide://agent-harnesses",
        ):
            self.assertIn(required, built)
        self.assertNotIn("the catalog contains 160 runtime harnesses", built.casefold())


if __name__ == "__main__":
    unittest.main(verbosity=2)
