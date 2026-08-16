from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER = PROJECT_ROOT / "scripts" / "check-agentsec-security-feed.py"


def feed(version: str = "2.26.0") -> dict[str, object]:
    return {
        "schema_version": "1",
        "content_license": "CC-BY-SA-4.0",
        "agentsec": {"version": "0.1.0a0"},
        "database": {"version": version, "updated": "2026-08-06"},
        "landing_metrics": {},
        "intelligence": {"events": [], "sources": []},
        "detectors": [],
        "input_digests": {},
    }


def run(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--guide-root", str(root), *arguments],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def write_fixture(root: Path, payload: object, database_version: str = "2.26.0") -> Path:
    mirror = root / "machine-readable" / "agentsec-security-feed.v1.json"
    database = root / "examples" / "commands" / "resources" / "threat-db.yaml"
    mirror.parent.mkdir(parents=True)
    database.parent.mkdir(parents=True)
    mirror.write_text(json.dumps(payload) + "\n", encoding="utf-8")
    database.write_text(
        f'version: "{database_version}"\nupdated: "2026-08-06"\n',
        encoding="utf-8",
    )
    return mirror


def test_checker_accepts_compatible_guide_mirror() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write_fixture(root, feed())

        completed = run(root)

        assert completed.returncode == 0, completed.stderr


def test_checker_rejects_stale_database_version() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write_fixture(root, feed("2.25.0"))

        completed = run(root)

        assert completed.returncode == 1
        assert "threat database version differs" in completed.stderr


def test_checker_rejects_malformed_feed() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write_fixture(root, {"schema_version": "1"})

        completed = run(root)

        assert completed.returncode == 1
        assert "missing required feed keys" in completed.stderr


def test_checker_rejects_byte_drift_from_agentsec() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        mirror = write_fixture(root, feed())
        canonical = root / "canonical.json"
        canonical.write_bytes(mirror.read_bytes() + b" ")

        completed = run(root, "--agentsec-feed", str(canonical))

        assert completed.returncode == 1
        assert "guide mirror differs from AgentSec" in completed.stderr


if __name__ == "__main__":
    tests = (
        test_checker_accepts_compatible_guide_mirror,
        test_checker_rejects_stale_database_version,
        test_checker_rejects_malformed_feed,
        test_checker_rejects_byte_drift_from_agentsec,
    )
    for test in tests:
        test()
    print(f"{len(tests)} AgentSec feed checks passed")
