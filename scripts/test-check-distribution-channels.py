from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stderr


SCRIPT = Path(__file__).with_name("check-distribution-channels.py")
SPEC = importlib.util.spec_from_file_location("distribution_validator", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def valid_registry() -> dict[str, object]:
    return {
        "schema_version": 1,
        "updated_at": "2026-08-31",
        "measurement_window_days": 30,
        "campaign": "campaign-one",
        "channels": [
            {
                "id": "github-en",
                "channel": "github",
                "locale": "en",
                "owner": "Owner",
                "asset": "README.md",
                "asset_status": "published",
                "canonical_url": "https://example.com/guide",
                "tagged_url": "https://example.com/guide?utm_source=github&utm_medium=repo&utm_campaign=campaign-one",
                "status": "published",
                "placement_status": "verified",
                "published_at": "2026-08-30",
                "observed_at": "2026-08-31",
                "submission_date": None,
                "measurement_started_at": "2026-08-31",
                "placement_evidence_url": "https://example.com/placement",
                "placement_verified_at": "2026-08-31",
                "outcome": {"impressions": None, "visits": None, "clones": None, "stars": None},
            }
        ],
    }


class DistributionRegistryTests(unittest.TestCase):
    def test_valid_registry_passes(self) -> None:
        self.assertEqual(validator.validate_registry(valid_registry()), [])

    def test_duplicate_channel_id_fails(self) -> None:
        registry = valid_registry()
        registry["channels"].append(dict(registry["channels"][0]))
        errors = validator.validate_registry(registry)
        self.assertTrue(any("duplicate" in error for error in errors))

    def test_missing_attribution_fails(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["tagged_url"] = "https://example.com/guide"
        errors = validator.validate_registry(registry)
        self.assertTrue(any("missing" in error for error in errors))

    def test_wrong_measurement_window_fails(self) -> None:
        registry = valid_registry()
        registry["measurement_window_days"] = 14
        errors = validator.validate_registry(registry)
        self.assertIn("measurement_window_days: expected 30", errors)

    def test_invalid_metric_fails(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["outcome"]["stars"] = -1
        errors = validator.validate_registry(registry)
        self.assertTrue(any("outcome.stars" in error for error in errors))

    def test_ready_local_asset_must_exist(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["asset"] = "missing-file.md"
        registry["channels"][0]["asset_status"] = "ready"
        registry["channels"][0]["status"] = "ready"
        registry["channels"][0]["placement_status"] = "ready"
        registry["channels"][0]["published_at"] = None
        registry["channels"][0]["observed_at"] = None
        registry["channels"][0]["measurement_started_at"] = None
        registry["channels"][0]["placement_evidence_url"] = None
        registry["channels"][0]["placement_verified_at"] = None
        with tempfile.TemporaryDirectory() as directory:
            errors = validator.validate_registry(registry, Path(directory))
        self.assertTrue(any("ready local asset does not exist" in error for error in errors))

    def test_submitted_channel_requires_submission_date(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["status"] = "submitted"
        registry["channels"][0]["placement_status"] = "submitted"
        registry["channels"][0]["observed_at"] = None
        registry["channels"][0]["measurement_started_at"] = None
        registry["channels"][0]["placement_evidence_url"] = None
        registry["channels"][0]["placement_verified_at"] = None
        errors = validator.validate_registry(registry)
        self.assertTrue(any("submission_date: required" in error for error in errors))

    def test_status_and_asset_status_must_be_coherent(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["asset_status"] = "planned"
        errors = validator.validate_registry(registry)
        self.assertTrue(any("inconsistent with status" in error for error in errors))

    def test_published_channel_requires_placement_evidence(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["placement_evidence_url"] = None
        errors = validator.validate_registry(registry)
        self.assertTrue(any("placement_evidence_url: required" in error for error in errors))

    def test_future_date_fails(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["observed_at"] = "2099-01-01"
        errors = validator.validate_registry(registry)
        self.assertTrue(any("date cannot be in the future" in error for error in errors))

    def test_publication_must_precede_observation(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["published_at"] = "2026-08-31"
        registry["channels"][0]["observed_at"] = "2026-08-30"
        errors = validator.validate_registry(registry)
        self.assertTrue(any("published_at must be on or before observed_at" in error for error in errors))

    def test_observation_must_precede_placement_verification(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["observed_at"] = "2026-08-31"
        registry["channels"][0]["placement_verified_at"] = "2026-08-30"
        errors = validator.validate_registry(registry)
        self.assertTrue(any("observed_at must be on or before placement_verified_at" in error for error in errors))

    def test_placement_verification_must_precede_measurement(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["placement_verified_at"] = "2026-08-31"
        registry["channels"][0]["measurement_started_at"] = "2026-08-30"
        errors = validator.validate_registry(registry)
        self.assertTrue(any("placement_verified_at must be on or before measurement_started_at" in error for error in errors))

    def test_ready_asset_can_wait_on_blocked_placement(self) -> None:
        registry = valid_registry()
        channel = registry["channels"][0]
        channel["asset_status"] = "ready"
        channel["status"] = "blocked"
        channel["placement_status"] = "blocked"
        channel["blocker"] = "Publication approval is missing."
        channel["published_at"] = None
        channel["observed_at"] = None
        channel["measurement_started_at"] = None
        channel["placement_evidence_url"] = None
        channel["placement_verified_at"] = None
        self.assertEqual(validator.validate_registry(registry), [])

    def test_metric_requires_measurement_start(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["status"] = "planned"
        registry["channels"][0]["placement_status"] = "planned"
        registry["channels"][0]["measurement_started_at"] = None
        registry["channels"][0]["placement_evidence_url"] = None
        registry["channels"][0]["placement_verified_at"] = None
        registry["channels"][0]["outcome"]["visits"] = 1
        errors = validator.validate_registry(registry)
        self.assertTrue(any("measurement_started_at is required" in error for error in errors))

    def test_ready_production_brief_must_exist(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["production_brief"] = "missing-brief.md"
        registry["channels"][0]["production_brief_status"] = "ready"
        with tempfile.TemporaryDirectory() as directory:
            errors = validator.validate_registry(registry, Path(directory))
        self.assertTrue(any("production_brief: local file does not exist" in error for error in errors))

    def test_cli_rejects_invalid_file(self) -> None:
        registry = valid_registry()
        registry["channels"][0]["status"] = "unknown"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.yaml"
            path.write_text(json.dumps(registry), encoding="utf-8")
            with redirect_stderr(io.StringIO()):
                self.assertEqual(validator.main(["--registry", str(path)]), 1)


if __name__ == "__main__":
    unittest.main()
