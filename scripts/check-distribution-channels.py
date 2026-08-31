#!/usr/bin/env python3
"""Validate the guide distribution registry without third-party packages."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "machine-readable" / "distribution-channels.yaml"
ALLOWED_STATUSES = {"planned", "ready", "submitted", "published", "blocked"}
ALLOWED_ASSET_STATUSES = {"planned", "ready", "published", "blocked", "stale"}
PLACEMENT_STATUS_BY_STATUS = {
    "planned": "planned",
    "ready": "ready",
    "submitted": "submitted",
    "published": "verified",
    "blocked": "blocked",
}
COHERENT_ASSET_STATUSES = {
    "planned": {"planned", "ready", "published"},
    "ready": {"ready", "published"},
    "submitted": {"ready", "published"},
    "published": {"published"},
    "blocked": {"planned", "ready", "published", "blocked", "stale"},
}
OUTCOME_FIELDS = {"impressions", "visits", "clones", "stars"}
UTM_FIELDS = {"utm_source", "utm_medium", "utm_campaign"}


def _date_or_none(value: object, label: str, errors: list[str]) -> date | None:
    if value is None:
        return None
    if not isinstance(value, str):
        errors.append(f"{label}: expected an ISO date or null")
        return None
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label}: invalid ISO date {value!r}")
        return None
    if parsed > date.today():
        errors.append(f"{label}: date cannot be in the future")
    return parsed


def _https_url(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{label}: expected an HTTPS URL")
        return
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        errors.append(f"{label}: expected an HTTPS URL, found {value!r}")


def validate_registry(registry: dict[str, Any], repo_root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []
    if registry.get("schema_version") != 1:
        errors.append("schema_version: expected 1")
    updated_at = _date_or_none(registry.get("updated_at"), "updated_at", errors)
    if registry.get("measurement_window_days") != 30:
        errors.append("measurement_window_days: expected 30")
    campaign = registry.get("campaign")
    if not isinstance(campaign, str) or not campaign.strip():
        errors.append("campaign: expected a non-empty string")

    channels = registry.get("channels")
    if not isinstance(channels, list) or not channels:
        errors.append("channels: expected a non-empty list")
        return errors

    seen: set[str] = set()
    for index, channel in enumerate(channels):
        label = f"channels[{index}]"
        if not isinstance(channel, dict):
            errors.append(f"{label}: expected an object")
            continue

        channel_id = channel.get("id")
        if not isinstance(channel_id, str) or not channel_id.strip():
            errors.append(f"{label}.id: expected a non-empty string")
        elif channel_id in seen:
            errors.append(f"{label}.id: duplicate {channel_id!r}")
        else:
            seen.add(channel_id)

        for field in ("channel", "locale", "owner", "asset"):
            value = channel.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}.{field}: expected a non-empty string")

        asset = channel.get("asset")
        asset_status = channel.get("asset_status")
        if (
            isinstance(asset, str)
            and asset_status in {"ready", "published"}
            and not urlparse(asset).scheme
            and not (repo_root / asset).is_file()
        ):
            errors.append(f"{label}.asset: ready local asset does not exist: {asset!r}")

        status = channel.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{label}.status: unsupported value {status!r}")
        if asset_status not in ALLOWED_ASSET_STATUSES:
            errors.append(f"{label}.asset_status: unsupported value {asset_status!r}")
        elif status in COHERENT_ASSET_STATUSES and asset_status not in COHERENT_ASSET_STATUSES[status]:
            allowed = ", ".join(sorted(COHERENT_ASSET_STATUSES[status]))
            errors.append(
                f"{label}.asset_status: {asset_status!r} is inconsistent with status "
                f"{status!r}; expected one of {allowed}"
            )

        placement_status = channel.get("placement_status")
        expected_placement = PLACEMENT_STATUS_BY_STATUS.get(status)
        if placement_status != expected_placement:
            errors.append(
                f"{label}.placement_status: expected {expected_placement!r} for status {status!r}"
            )

        _https_url(channel.get("canonical_url"), f"{label}.canonical_url", errors)
        tagged_url = channel.get("tagged_url")
        _https_url(tagged_url, f"{label}.tagged_url", errors)
        if isinstance(tagged_url, str):
            parameters = parse_qs(urlparse(tagged_url).query)
            missing = sorted(UTM_FIELDS - set(parameters))
            if missing:
                errors.append(f"{label}.tagged_url: missing {', '.join(missing)}")
            if campaign and parameters.get("utm_campaign") != [campaign]:
                errors.append(f"{label}.tagged_url: campaign does not match registry campaign")

        published_at = _date_or_none(channel.get("published_at"), f"{label}.published_at", errors)
        observed_at = _date_or_none(channel.get("observed_at"), f"{label}.observed_at", errors)
        submission_date = _date_or_none(channel.get("submission_date"), f"{label}.submission_date", errors)
        measurement_started_at = _date_or_none(
            channel.get("measurement_started_at"),
            f"{label}.measurement_started_at",
            errors,
        )
        placement_verified_at = _date_or_none(
            channel.get("placement_verified_at"),
            f"{label}.placement_verified_at",
            errors,
        )
        if status == "submitted" and not channel.get("submission_date"):
            errors.append(f"{label}.submission_date: required for submitted")
        if status == "published":
            if not channel.get("placement_evidence_url"):
                errors.append(f"{label}.placement_evidence_url: required for published")
            else:
                _https_url(
                    channel.get("placement_evidence_url"),
                    f"{label}.placement_evidence_url",
                    errors,
                )
            if not channel.get("placement_verified_at"):
                errors.append(f"{label}.placement_verified_at: required for published")
            if not channel.get("observed_at"):
                errors.append(f"{label}.observed_at: required for published")
            if not channel.get("measurement_started_at"):
                errors.append(f"{label}.measurement_started_at: required for published")
        elif channel.get("placement_evidence_url") or channel.get("placement_verified_at"):
            errors.append(f"{label}.placement_evidence: only valid for published status")

        if status in {"planned", "ready", "blocked"} and channel.get("submission_date"):
            errors.append(f"{label}.submission_date: must be null before submission")
        if status in {"planned", "ready", "submitted", "blocked"} and channel.get("measurement_started_at"):
            errors.append(f"{label}.measurement_started_at: requires published status")
        if status == "blocked" and not channel.get("blocker"):
            errors.append(f"{label}.blocker: required for blocked")

        if updated_at:
            for field_name, parsed in (
                ("published_at", published_at),
                ("observed_at", observed_at),
                ("submission_date", submission_date),
                ("measurement_started_at", measurement_started_at),
                ("placement_verified_at", placement_verified_at),
            ):
                if parsed and parsed > updated_at:
                    errors.append(f"{label}.{field_name}: cannot be after updated_at")
        if published_at and observed_at and published_at > observed_at:
            errors.append(f"{label}: published_at must be on or before observed_at")
        if observed_at and measurement_started_at and observed_at > measurement_started_at:
            errors.append(f"{label}: observed_at must be on or before measurement_started_at")
        if observed_at and placement_verified_at and observed_at > placement_verified_at:
            errors.append(f"{label}: observed_at must be on or before placement_verified_at")
        if placement_verified_at and measurement_started_at and placement_verified_at > measurement_started_at:
            errors.append(f"{label}: placement_verified_at must be on or before measurement_started_at")
        if submission_date and measurement_started_at and submission_date > measurement_started_at:
            errors.append(f"{label}: submission_date must be on or before measurement_started_at")

        outcome = channel.get("outcome")
        if not isinstance(outcome, dict) or set(outcome) != OUTCOME_FIELDS:
            errors.append(f"{label}.outcome: expected exactly {sorted(OUTCOME_FIELDS)}")
        else:
            for metric, value in outcome.items():
                if value is not None and (isinstance(value, bool) or not isinstance(value, int) or value < 0):
                    errors.append(f"{label}.outcome.{metric}: expected a non-negative integer or null")
                if value is not None and not channel.get("measurement_started_at"):
                    errors.append(
                        f"{label}.outcome.{metric}: measurement_started_at is required for a recorded value"
                    )

        production_brief = channel.get("production_brief")
        if production_brief is not None:
            if not isinstance(production_brief, str) or not production_brief.strip():
                errors.append(f"{label}.production_brief: expected a non-empty local path")
            elif not (repo_root / production_brief).is_file():
                errors.append(f"{label}.production_brief: local file does not exist: {production_brief!r}")
            if channel.get("production_brief_status") != "ready":
                errors.append(f"{label}.production_brief_status: expected 'ready'")

    return errors


def load_registry(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read JSON-compatible YAML registry: {error}") from error
    if not isinstance(value, dict):
        raise ValueError("Registry root must be an object")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args(argv)
    try:
        registry = load_registry(args.registry)
    except ValueError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    errors = validate_registry(registry)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(registry['channels'])} distribution channels are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
