#!/usr/bin/env python3
"""Collect the public npm and MCP Registry statistics snapshot."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from statistics import median as statistics_median
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "claude-code-ultimate-guide-mcp"
REGISTRY_NAME = "io.github.FlorianBruniaux/claude-code-guide"
DEFAULT_OUTPUT = ROOT / "machine-readable" / "mcp-stats.json"
NPM_REGISTRY_URL = f"https://registry.npmjs.org/{PACKAGE}"
NPM_DOWNLOADS_URL = "https://api.npmjs.org/downloads"
MCP_REGISTRY_URL = "https://registry.modelcontextprotocol.io/v0/servers"
UTC_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
PRODUCT_CHANGELOG_START = "<!-- mcp-product:start -->"
PRODUCT_CHANGELOG_END = "<!-- mcp-product:end -->"
STATS_CHANGELOG_START = "<!-- mcp-stats:start -->"
STATS_CHANGELOG_END = "<!-- mcp-stats:end -->"


def median(values: List[int]) -> float:
    if not values:
        raise ValueError("at least one daily value is required")
    return float(statistics_median(values))


def median_absolute_deviation(values: List[int]) -> float:
    center = median(values)
    return median([abs(value - center) for value in values])


def detect_anomalies(values: List[int], threshold: float = 6.0) -> List[int]:
    center = median(values)
    mad = median_absolute_deviation(values)
    if mad == 0:
        return [index for index, value in enumerate(values) if value != center]
    return [
        index
        for index, value in enumerate(values)
        if abs(value - center) / mad > threshold
    ]


def validate_snapshot_at(value: str) -> datetime:
    if not isinstance(value, str) or not UTC_TIMESTAMP.fullmatch(value):
        raise ValueError("snapshot_at must be an exact UTC timestamp ending in Z")
    parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    if parsed.utcoffset() != timedelta(0):
        raise ValueError("snapshot_at must be an exact UTC timestamp ending in Z")
    return parsed


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def date_range(start: str, end: str) -> List[str]:
    first = date.fromisoformat(start)
    last = date.fromisoformat(end)
    if first > last:
        raise ValueError(f"invalid period: {start} is after {end}")
    days: List[str] = []
    current = first
    while current <= last:
        days.append(current.isoformat())
        current += timedelta(days=1)
    return days


def periods_for_snapshot(snapshot_at: str, package_created_at: str) -> Dict[str, Tuple[str, str]]:
    snapshot = validate_snapshot_at(snapshot_at)
    created = validate_snapshot_at(package_created_at)
    last_complete = snapshot.date() - timedelta(days=1)
    if created.date() > last_complete:
        raise ValueError("package creation date is after the last complete UTC day")
    return {
        "year_to_date": (date(last_complete.year, 1, 1).isoformat(), last_complete.isoformat()),
        "since_launch": (created.date().isoformat(), last_complete.isoformat()),
        "last_30_days": ((last_complete - timedelta(days=29)).isoformat(), last_complete.isoformat()),
        "last_7_days": ((last_complete - timedelta(days=6)).isoformat(), last_complete.isoformat()),
    }


def validate_npm_metadata(payload: Any) -> Tuple[str, str, str]:
    if not isinstance(payload, dict) or payload.get("name") != PACKAGE:
        raise ValueError(f"npm metadata must describe {PACKAGE}")
    tags = payload.get("dist-tags")
    times = payload.get("time")
    if not isinstance(tags, dict) or not isinstance(tags.get("latest"), str):
        raise ValueError("npm metadata is missing dist-tags.latest")
    if not isinstance(times, dict) or not isinstance(times.get("created"), str):
        raise ValueError("npm metadata is missing package creation time")
    version = tags["latest"]
    if not isinstance(times.get(version), str):
        raise ValueError(f"public version {version} is absent from npm time metadata")
    validate_snapshot_at(times["created"])
    validate_snapshot_at(times[version])
    return version, times["created"], times[version]


def validate_daily_range(payload: Any, expected_start: str, expected_end: str) -> List[Dict[str, Any]]:
    if not isinstance(payload, dict):
        raise ValueError("npm daily range must be an object")
    if payload.get("package") != PACKAGE:
        raise ValueError(f"npm daily range must describe {PACKAGE}")
    if payload.get("start") != expected_start or payload.get("end") != expected_end:
        raise ValueError(
            f"npm daily range boundaries differ: expected {expected_start} through {expected_end}, "
            f"received {payload.get('start')} through {payload.get('end')}"
        )
    records = payload.get("downloads")
    if not isinstance(records, list):
        raise ValueError("npm daily range downloads must be an array")
    observed: List[str] = []
    normalized: List[Dict[str, Any]] = []
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("day"), str):
            raise ValueError("each npm daily record must contain an ISO date")
        day = record["day"]
        try:
            date.fromisoformat(day)
        except ValueError as error:
            raise ValueError(f"invalid npm daily date: {day}") from error
        count = record.get("downloads")
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ValueError("npm daily downloads must be a non-negative integer")
        observed.append(day)
        normalized.append({"day": day, "downloads": count})
    if len(observed) != len(set(observed)):
        raise ValueError("duplicate daily date in npm range")
    expected = date_range(expected_start, expected_end)
    if observed != expected:
        missing = sorted(set(expected) - set(observed))
        extra = sorted(set(observed) - set(expected))
        raise ValueError(f"missing daily dates or unexpected dates: missing={missing}, extra={extra}")
    return normalized


def reconcile_total(daily_payload: Mapping[str, Any], point_payload: Any) -> Dict[str, Any]:
    if not isinstance(point_payload, dict):
        raise ValueError("npm total endpoint must return an object")
    if point_payload.get("package") != PACKAGE:
        raise ValueError(f"npm total endpoint must describe {PACKAGE}")
    if point_payload.get("start") != daily_payload.get("start") or point_payload.get("end") != daily_payload.get("end"):
        raise ValueError("npm total endpoint period differs from the daily series")
    total = point_payload.get("downloads")
    if isinstance(total, bool) or not isinstance(total, int) or total < 0:
        raise ValueError("npm total downloads must be a non-negative integer")
    daily_total = sum(record["downloads"] for record in daily_payload["downloads"])
    if total != daily_total:
        raise ValueError(f"npm total endpoint differs from daily series: {total} != {daily_total}")
    return {"start": point_payload["start"], "end": point_payload["end"], "count": total}


def slice_daily(records: Iterable[Mapping[str, Any]], start: str, end: str) -> Dict[str, Any]:
    selected = [dict(record) for record in records if start <= str(record["day"]) <= end]
    return {"start": start, "end": end, "package": PACKAGE, "downloads": selected}


def registry_contains(payload: Any, registry_name: str = REGISTRY_NAME) -> bool:
    if not isinstance(payload, dict):
        raise ValueError("official MCP Registry response must be an object")
    servers = payload.get("servers")
    if not isinstance(servers, list):
        raise ValueError("official MCP Registry response is missing servers")
    for entry in servers:
        if not isinstance(entry, dict):
            continue
        candidates = [entry, entry.get("server"), entry.get("_meta")]
        for candidate in candidates:
            if isinstance(candidate, dict) and candidate.get("name") == registry_name:
                return True
    return False


def validate_snapshot(candidate: Any) -> List[str]:
    errors: List[str] = []
    if not isinstance(candidate, dict):
        return ["snapshot must be an object"]
    if candidate.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if candidate.get("package") != PACKAGE:
        errors.append(f"package must be {PACKAGE}")
    try:
        validate_snapshot_at(candidate.get("snapshot_at"))
    except (TypeError, ValueError) as error:
        errors.append(str(error))
    for field in ("public_version", "package_created_at", "version_published_at"):
        if not isinstance(candidate.get(field), str) or not candidate[field]:
            errors.append(f"{field} must be a non-empty string")
    for field in ("package_created_at", "version_published_at"):
        if isinstance(candidate.get(field), str):
            try:
                validate_snapshot_at(candidate[field])
            except ValueError:
                errors.append(f"{field} must be an exact UTC timestamp ending in Z")

    downloads = candidate.get("downloads")
    if not isinstance(downloads, dict):
        return [*errors, "downloads must be an object"]
    for name in ("year_to_date", "since_launch", "last_30_days", "last_7_days"):
        period = downloads.get(name)
        if not isinstance(period, dict):
            errors.append(f"downloads.{name} must be an object")
            continue
        try:
            expected_days = date_range(period.get("start"), period.get("end"))
        except (TypeError, ValueError):
            errors.append(f"downloads.{name} must contain valid start and end dates")
            continue
        count = period.get("count")
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            errors.append(f"downloads.{name}.count must be a non-negative integer")
        if name == "last_30_days" and len(expected_days) != 30:
            errors.append("downloads.last_30_days must contain exactly 30 dates")
        if name == "last_7_days" and len(expected_days) != 7:
            errors.append("downloads.last_7_days must contain exactly 7 dates")
    daily = downloads.get("daily")
    if not isinstance(daily, list) or not daily:
        errors.append("downloads.daily must be a non-empty array")
    else:
        days: List[str] = []
        total = 0
        for record in daily:
            if not isinstance(record, dict):
                errors.append("downloads.daily entries must be objects")
                continue
            day = record.get("day")
            count = record.get("downloads")
            anomaly = record.get("anomaly")
            if not isinstance(day, str):
                errors.append("downloads.daily day must be an ISO date")
            else:
                days.append(day)
            if isinstance(count, bool) or not isinstance(count, int) or count < 0:
                errors.append("downloads.daily downloads must be a non-negative integer")
            else:
                total += count
            if not isinstance(anomaly, bool):
                errors.append("downloads.daily anomaly must be boolean")
        if len(days) != len(set(days)):
            errors.append("downloads.daily contains duplicate dates")
        ytd = downloads.get("year_to_date")
        if isinstance(ytd, dict):
            try:
                expected = date_range(ytd.get("start"), ytd.get("end"))
                if days != expected:
                    errors.append("downloads.daily must cover year_to_date without gaps")
            except (TypeError, ValueError):
                pass
            if isinstance(ytd.get("count"), int) and total != ytd["count"]:
                errors.append("downloads.daily sum must equal year_to_date count")
        anomaly_dates = downloads.get("anomaly_dates")
        if not isinstance(anomaly_dates, list):
            errors.append("downloads.anomaly_dates must be an array")
        else:
            flagged = [record.get("day") for record in daily if record.get("anomaly") is True]
            if flagged != anomaly_dates:
                errors.append("downloads anomaly flags must match anomaly_dates")
    if downloads.get("distribution_period") != "last_30_days":
        errors.append("downloads.distribution_period must be last_30_days")
    for field in ("daily_median", "daily_mean", "daily_max", "daily_mad"):
        value = downloads.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            errors.append(f"downloads.{field} must be a non-negative number")
    official = candidate.get("registries", {}).get("official_mcp") if isinstance(candidate.get("registries"), dict) else None
    if not isinstance(official, dict) or official.get("name") != REGISTRY_NAME or not isinstance(official.get("published"), bool):
        errors.append("registries.official_mcp must record the exact name and boolean status")
    exclusions = candidate.get("methodology", {}).get("not_equivalent_to") if isinstance(candidate.get("methodology"), dict) else None
    expected_exclusions = ["users", "active installations", "sessions", "executions"]
    if exclusions != expected_exclusions:
        errors.append("methodology.not_equivalent_to must preserve all four exclusions")
    return errors


def build_snapshot(
    metadata: Any,
    year_to_date_payload: Any,
    since_launch_payload: Any,
    totals: Mapping[str, Any],
    registry_payload: Any,
    snapshot_at: str,
) -> Dict[str, Any]:
    version, created_at, published_at = validate_npm_metadata(metadata)
    periods = periods_for_snapshot(snapshot_at, created_at)
    year_to_date = validate_daily_range(year_to_date_payload, *periods["year_to_date"])
    since_launch = validate_daily_range(since_launch_payload, *periods["since_launch"])
    derived = {
        "year_to_date": {**year_to_date_payload, "downloads": year_to_date},
        "since_launch": {**since_launch_payload, "downloads": since_launch},
        "last_30_days": slice_daily(year_to_date, *periods["last_30_days"]),
        "last_7_days": slice_daily(year_to_date, *periods["last_7_days"]),
    }
    reconciled: Dict[str, Dict[str, Any]] = {}
    for name in periods:
        point = totals.get(name)
        reconciled[name] = reconcile_total(derived[name], point)

    distribution = derived["last_30_days"]["downloads"]
    values = [record["downloads"] for record in distribution]
    anomaly_indices = detect_anomalies(values)
    anomaly_dates = [distribution[index]["day"] for index in anomaly_indices]
    anomaly_date_set = set(anomaly_dates)
    daily = [
        {"day": record["day"], "downloads": record["downloads"], "anomaly": record["day"] in anomaly_date_set}
        for record in year_to_date
    ]
    candidate = {
        "schema_version": 1,
        "snapshot_at": snapshot_at,
        "package": PACKAGE,
        "public_version": version,
        "package_created_at": created_at,
        "version_published_at": published_at,
        "downloads": {
            **reconciled,
            "distribution_period": "last_30_days",
            "daily_median": median(values),
            "daily_mean": round(sum(values) / len(values), 1),
            "daily_max": max(values),
            "daily_mad": median_absolute_deviation(values),
            "anomaly_threshold_mad": 6.0,
            "anomaly_dates": anomaly_dates,
            "daily_period": "year_to_date",
            "daily": daily,
        },
        "registries": {
            "official_mcp": {"name": REGISTRY_NAME, "published": registry_contains(registry_payload)}
        },
        "methodology": {
            "unit": "npm package downloads",
            "daily_distribution": "last 30 complete UTC days, including zero-download days",
            "anomaly_rule": "absolute deviation from the median greater than 6 MAD; when MAD is zero, any value different from the median",
            "not_equivalent_to": ["users", "active installations", "sessions", "executions"],
        },
    }
    errors = validate_snapshot(candidate)
    if errors:
        raise ValueError("invalid MCP statistics snapshot:\n- " + "\n- ".join(errors))
    return candidate


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_from_fixture_dir(fixture_dir: Path, snapshot_at: Optional[str] = None) -> Dict[str, Any]:
    fixture_dir = Path(fixture_dir)
    fixture_config = read_json(fixture_dir / "mcp-stats-fixture.json")
    return build_snapshot(
        read_json(fixture_dir / "mcp-npm-metadata.json"),
        read_json(fixture_dir / "mcp-npm-range.json"),
        read_json(fixture_dir / "mcp-npm-since-launch-range.json"),
        read_json(fixture_dir / "mcp-npm-totals.json"),
        read_json(fixture_dir / "mcp-registry-empty.json"),
        snapshot_at or fixture_config["snapshot_at"],
    )


def fetch_json(url: str, timeout: int = 30) -> Any:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "claude-code-ultimate-guide-mcp-stats/1"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read(16 * 1024 * 1024 + 1)
    if len(raw) > 16 * 1024 * 1024:
        raise ValueError("upstream JSON response exceeds 16 MiB")
    return json.loads(raw.decode("utf-8"))


def period_url(kind: str, start: str, end: str) -> str:
    package = urllib.parse.quote(PACKAGE, safe="@")
    return f"{NPM_DOWNLOADS_URL}/{kind}/{start}:{end}/{package}"


def collect_live(snapshot_at: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    captured_at = snapshot_at or utc_now()
    metadata = fetch_json(NPM_REGISTRY_URL, timeout)
    _, created_at, _ = validate_npm_metadata(metadata)
    periods = periods_for_snapshot(captured_at, created_at)
    year_to_date = fetch_json(period_url("range", *periods["year_to_date"]), timeout)
    since_launch = fetch_json(period_url("range", *periods["since_launch"]), timeout)
    totals = {
        name: fetch_json(period_url("point", *period), timeout)
        for name, period in periods.items()
    }
    registry_query = urllib.parse.urlencode({"search": REGISTRY_NAME, "limit": 100})
    registry = fetch_json(f"{MCP_REGISTRY_URL}?{registry_query}", timeout)
    return build_snapshot(metadata, year_to_date, since_launch, totals, registry, captured_at)


def serialize(candidate: Mapping[str, Any]) -> str:
    return json.dumps(candidate, ensure_ascii=False, indent=2) + "\n"


def render_changelog_line(candidate: Mapping[str, Any]) -> str:
    downloads = candidate["downloads"]
    since_launch = downloads["since_launch"]
    year_to_date = downloads["year_to_date"]
    last_30 = downloads["last_30_days"]
    last_7 = downloads["last_7_days"]
    registry = (
        "published"
        if candidate["registries"]["official_mcp"]["published"]
        else "not returned by the official MCP Registry"
    )
    return (
        f"- **MCP public statistics snapshot** (`machine-readable/mcp-stats.json`): "
        f"snapshot `{candidate['snapshot_at']}` for npm {candidate['public_version']}; "
        f"since launch {since_launch['start']} through {since_launch['end']}: {since_launch['count']:,} downloads; "
        f"year to date {year_to_date['start']} through {year_to_date['end']}: {year_to_date['count']:,} downloads; "
        f"trailing 30 complete UTC days {last_30['start']} through {last_30['end']}: {last_30['count']:,} downloads; "
        f"trailing 7 complete UTC days {last_7['start']} through {last_7['end']}: {last_7['count']:,} downloads. "
        f"The package is {registry}. Download counts are not users, active installations, sessions, or executions."
    )


def render_changelog(source: str, candidate: Mapping[str, Any]) -> str:
    if source.count(PRODUCT_CHANGELOG_START) != 1 or source.count(PRODUCT_CHANGELOG_END) != 1:
        raise ValueError("CHANGELOG.md must contain exactly one mcp-product marker pair")
    product_start = source.index(PRODUCT_CHANGELOG_START)
    product_end = source.index(PRODUCT_CHANGELOG_END)
    if product_start >= product_end:
        raise ValueError("mcp-product changelog markers must be ordered")
    stats_start_count = source.count(STATS_CHANGELOG_START)
    stats_end_count = source.count(STATS_CHANGELOG_END)
    line = render_changelog_line(candidate)
    if stats_start_count == 0 and stats_end_count == 0:
        insertion = f"{STATS_CHANGELOG_START}\n{line}\n{STATS_CHANGELOG_END}\n"
        return f"{source[:product_end]}{insertion}{source[product_end:]}"
    if stats_start_count != 1 or stats_end_count != 1:
        raise ValueError("CHANGELOG.md must contain exactly one mcp-stats marker pair")
    stats_start = source.index(STATS_CHANGELOG_START)
    stats_end = source.index(STATS_CHANGELOG_END)
    if not product_start < stats_start < stats_end < product_end:
        raise ValueError("mcp-stats markers must stay inside the mcp-product block")
    content_start = stats_start + len(STATS_CHANGELOG_START)
    return f"{source[:content_start]}\n{line}\n{source[stats_end:]}"


def stabilize_snapshot(candidate: Dict[str, Any], output: Path) -> Dict[str, Any]:
    if not output.exists():
        return candidate
    try:
        previous = read_json(output)
    except (OSError, json.JSONDecodeError):
        return candidate
    previous_without_time = copy.deepcopy(previous)
    candidate_without_time = copy.deepcopy(candidate)
    previous_without_time.pop("snapshot_at", None)
    candidate_without_time.pop("snapshot_at", None)
    if previous_without_time == candidate_without_time and isinstance(previous.get("snapshot_at"), str):
        candidate["snapshot_at"] = previous["snapshot_at"]
    return candidate


def atomic_write_if_changed(path: Path, content: str) -> bool:
    encoded = content.encode("utf-8")
    if path.exists() and path.read_bytes() == encoded:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("wb") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    return True


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture-dir", type=Path)
    parser.add_argument("--snapshot-at")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--changelog", type=Path)
    parser.add_argument("--validate-file", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    if args.validate_file:
        errors = validate_snapshot(read_json(args.validate_file))
        if errors:
            raise ValueError("invalid MCP statistics snapshot:\n- " + "\n- ".join(errors))
        print(f"mcp_stats_valid={args.validate_file}")
        return 0
    candidate = (
        collect_from_fixture_dir(args.fixture_dir, args.snapshot_at)
        if args.fixture_dir
        else collect_live(args.snapshot_at, args.timeout_seconds)
    )
    candidate = stabilize_snapshot(candidate, args.output)
    content = serialize(candidate)
    if args.check:
        sys.stdout.write(content)
        return 0
    changelog_content: Optional[str] = None
    if args.changelog:
        changelog_content = render_changelog(args.changelog.read_text(encoding="utf-8"), candidate)
    changed = atomic_write_if_changed(args.output, content)
    changelog_changed = False
    if args.changelog and changelog_content is not None:
        changelog_changed = atomic_write_if_changed(args.changelog, changelog_content)
    print(f"mcp_stats_changed={str(changed).lower()}")
    if args.changelog:
        print(f"mcp_stats_changelog_changed={str(changelog_changed).lower()}")
    print(f"mcp_stats_output={args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"collect-mcp-stats.py: {error}", file=sys.stderr)
        raise SystemExit(1)
