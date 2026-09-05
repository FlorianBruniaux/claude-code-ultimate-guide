#!/usr/bin/env python3
"""Collect the monthly public MCP product dashboard."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from calendar import monthrange
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "claude-code-ultimate-guide-mcp"
LANDING_PAGE_URL = "https://cc.bruniaux.com/mcp/"
PORTFOLIO_PAGE_URL = "https://florian.bruniaux.com/blog/articles/claude-code-guide-mcp/"
PORTFOLIO_PAGE_PATH = "/blog/articles/claude-code-guide-mcp/"
DEFAULT_OUTPUT = ROOT / "machine-readable" / "mcp-dashboard.json"
NPM_DOWNLOADS_URL = "https://api.npmjs.org/downloads"
UTC_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


def validate_utc_timestamp(value: str) -> datetime:
    if not isinstance(value, str) or not UTC_TIMESTAMP.fullmatch(value):
        raise ValueError("timestamp must be exact UTC and end in Z")
    parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    if parsed.utcoffset() != timedelta(0):
        raise ValueError("timestamp must be exact UTC and end in Z")
    return parsed


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def last_completed_month(snapshot_at: str) -> Tuple[str, str]:
    current = validate_utc_timestamp(snapshot_at).date()
    first_current = date(current.year, current.month, 1)
    end = first_current - timedelta(days=1)
    start = date(end.year, end.month, 1)
    return start.isoformat(), end.isoformat()


def gsc_query(start: str, end: str, page_url: str) -> Dict[str, Any]:
    return {
        "startDate": start,
        "endDate": end,
        "dimensions": ["page"],
        "dimensionFilterGroups": [
            {
                "groupType": "and",
                "filters": [
                    {"dimension": "page", "operator": "equals", "expression": page_url}
                ],
            }
        ],
        "rowLimit": 1,
        "dataState": "final",
    }


def ga4_query(start: str, end: str, page_path: str) -> Dict[str, Any]:
    return {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": "pagePath"}],
        "metrics": [
            {"name": "sessions"},
            {"name": "engagedSessions"},
            {"name": "screenPageViews"},
        ],
        "dimensionFilter": {
            "filter": {
                "fieldName": "pagePath",
                "stringFilter": {"matchType": "EXACT", "value": page_path},
            }
        },
        "limit": "1",
    }


def npm_definitions() -> Dict[str, str]:
    return {"downloads": "npm package downloads during the completed calendar month"}


def gsc_definitions() -> Dict[str, str]:
    return {
        "clicks": "Google Search clicks for the exact page URL",
        "impressions": "Google Search impressions for the exact page URL",
        "ctr": "clicks divided by impressions as reported by Google Search Console",
        "average_position": "average topmost result position as reported by Google Search Console",
    }


def ga4_definitions() -> Dict[str, str]:
    return {
        "sessions": "GA4 sessions containing the exact page path",
        "engaged_sessions": "GA4 engaged sessions containing the exact page path",
        "views": "GA4 screenPageViews for the exact page path",
    }


def available_source(
    retrieved_at: str,
    scope: Mapping[str, Any],
    definitions: Mapping[str, str],
    values: Mapping[str, Any],
) -> Dict[str, Any]:
    validate_utc_timestamp(retrieved_at)
    return {
        "status": "available",
        "retrieved_at": retrieved_at,
        "scope": dict(scope),
        "definitions": dict(definitions),
        "values": dict(values),
        "reason": None,
    }


def unavailable_source(
    retrieved_at: str,
    scope: Mapping[str, Any],
    definitions: Mapping[str, str],
    reason: str,
) -> Dict[str, Any]:
    validate_utc_timestamp(retrieved_at)
    if not reason:
        raise ValueError("unavailable source requires a reason")
    return {
        "status": "unavailable",
        "retrieved_at": retrieved_at,
        "scope": dict(scope),
        "definitions": dict(definitions),
        "values": None,
        "reason": reason,
    }


def validate_npm(payload: Any, start: str, end: str) -> Dict[str, int]:
    if not isinstance(payload, dict) or payload.get("package") != PACKAGE:
        raise ValueError(f"npm dashboard source must describe {PACKAGE}")
    if payload.get("start") != start or payload.get("end") != end:
        raise ValueError("npm dashboard source period differs from the completed month")
    count = payload.get("downloads")
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise ValueError("npm dashboard downloads must be a non-negative integer")
    return {"downloads": count}


def parse_gsc(payload: Any, page_url: str) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("GSC response must be an object")
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        raise ValueError("GSC rows must be an array")
    if not rows:
        return {"clicks": 0, "impressions": 0, "ctr": 0.0, "average_position": None}
    if len(rows) != 1 or not isinstance(rows[0], dict) or rows[0].get("keys") != [page_url]:
        raise ValueError("GSC response must contain only the exact requested page")
    row = rows[0]
    values = {
        "clicks": row.get("clicks"),
        "impressions": row.get("impressions"),
        "ctr": row.get("ctr"),
        "average_position": row.get("position"),
    }
    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"GSC {name} must be a non-negative number")
    if values["ctr"] > 1:
        raise ValueError("GSC ctr must be between zero and one")
    return values


def parse_ga4(payload: Any, page_path: str) -> Dict[str, int]:
    if not isinstance(payload, dict):
        raise ValueError("GA4 response must be an object")
    dimensions = payload.get("dimensionHeaders")
    metrics = payload.get("metricHeaders")
    if dimensions != [{"name": "pagePath"}]:
        raise ValueError("GA4 response must contain only pagePath")
    expected_metrics = ["sessions", "engagedSessions", "screenPageViews"]
    if not isinstance(metrics, list) or [item.get("name") for item in metrics if isinstance(item, dict)] != expected_metrics:
        raise ValueError("GA4 response metric headers differ from the aggregate contract")
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        raise ValueError("GA4 rows must be an array")
    if not rows:
        return {"sessions": 0, "engaged_sessions": 0, "views": 0}
    if len(rows) != 1 or not isinstance(rows[0], dict):
        raise ValueError("GA4 response must contain at most the exact requested page")
    row = rows[0]
    if row.get("dimensionValues") != [{"value": page_path}]:
        raise ValueError("GA4 response must contain only the exact requested page path")
    raw_values = row.get("metricValues")
    if not isinstance(raw_values, list) or len(raw_values) != 3:
        raise ValueError("GA4 response must contain three aggregate metric values")
    parsed: List[int] = []
    for item in raw_values:
        try:
            value = int(item["value"])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("GA4 aggregate metrics must be integers") from error
        if value < 0:
            raise ValueError("GA4 aggregate metrics must be non-negative")
        parsed.append(value)
    return {"sessions": parsed[0], "engaged_sessions": parsed[1], "views": parsed[2]}


def scopes(environment: Mapping[str, str]) -> Dict[str, Dict[str, Any]]:
    return {
        "npm": {"package": PACKAGE},
        "gsc_landing": {
            "property": environment.get("MCP_GSC_LANDING_SITE_URL"),
            "page_url": LANDING_PAGE_URL,
        },
        "gsc_portfolio": {
            "property": environment.get("MCP_GSC_PORTFOLIO_SITE_URL"),
            "page_url": PORTFOLIO_PAGE_URL,
        },
        "ga4_portfolio": {
            "property": environment.get("MCP_GA4_PORTFOLIO_PROPERTY_ID"),
            "page_path": PORTFOLIO_PAGE_PATH,
        },
    }


def build_unavailable_dashboard(
    npm_payload: Any,
    snapshot_at: str,
    environment: Mapping[str, str],
) -> Dict[str, Any]:
    start, end = last_completed_month(snapshot_at)
    source_scopes = scopes(environment)
    sources = {
        "npm": available_source(
            snapshot_at,
            source_scopes["npm"],
            npm_definitions(),
            validate_npm(npm_payload, start, end),
        ),
        "gsc_landing": unavailable_source(
            snapshot_at,
            source_scopes["gsc_landing"],
            gsc_definitions(),
            "Google access token or MCP_GSC_LANDING_SITE_URL is not configured",
        ),
        "gsc_portfolio": unavailable_source(
            snapshot_at,
            source_scopes["gsc_portfolio"],
            gsc_definitions(),
            "Google access token or MCP_GSC_PORTFOLIO_SITE_URL is not configured",
        ),
        "ga4_portfolio": unavailable_source(
            snapshot_at,
            source_scopes["ga4_portfolio"],
            ga4_definitions(),
            "Google access token or MCP_GA4_PORTFOLIO_PROPERTY_ID is not configured",
        ),
    }
    return finalize_dashboard(snapshot_at, start, end, sources)


def finalize_dashboard(
    snapshot_at: str,
    start: str,
    end: str,
    sources: Mapping[str, Any],
) -> Dict[str, Any]:
    candidate = {
        "schema_version": 1,
        "snapshot_at": snapshot_at,
        "period": {"start": start, "end": end, "timezone": "UTC"},
        "sources": dict(sources),
        "methodology": {
            "publication_boundary": "aggregate page and package metrics only",
            "missing_source": "unavailable with a reason, never inferred as zero",
            "npm_not_equivalent_to": ["users", "active installations", "sessions", "executions"],
        },
    }
    errors = validate_dashboard(candidate)
    if errors:
        raise ValueError("invalid MCP dashboard:\n- " + "\n- ".join(errors))
    return candidate


def build_available_dashboard(
    npm_payload: Any,
    gsc_landing_payload: Any,
    gsc_portfolio_payload: Any,
    ga4_portfolio_payload: Any,
    snapshot_at: str,
    environment: Mapping[str, str],
) -> Dict[str, Any]:
    start, end = last_completed_month(snapshot_at)
    source_scopes = scopes(environment)
    sources = {
        "npm": available_source(snapshot_at, source_scopes["npm"], npm_definitions(), validate_npm(npm_payload, start, end)),
        "gsc_landing": available_source(snapshot_at, source_scopes["gsc_landing"], gsc_definitions(), parse_gsc(gsc_landing_payload, LANDING_PAGE_URL)),
        "gsc_portfolio": available_source(snapshot_at, source_scopes["gsc_portfolio"], gsc_definitions(), parse_gsc(gsc_portfolio_payload, PORTFOLIO_PAGE_URL)),
        "ga4_portfolio": available_source(snapshot_at, source_scopes["ga4_portfolio"], ga4_definitions(), parse_ga4(ga4_portfolio_payload, PORTFOLIO_PAGE_PATH)),
    }
    return finalize_dashboard(snapshot_at, start, end, sources)


def validate_dashboard(candidate: Any) -> List[str]:
    errors: List[str] = []
    if not isinstance(candidate, dict):
        return ["dashboard must be an object"]
    if candidate.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    try:
        validate_utc_timestamp(candidate.get("snapshot_at"))
    except (TypeError, ValueError) as error:
        errors.append(str(error))
    period = candidate.get("period")
    if not isinstance(period, dict) or period.get("timezone") != "UTC":
        errors.append("period must contain UTC start and end dates")
    else:
        try:
            start = date.fromisoformat(period["start"])
            end = date.fromisoformat(period["end"])
            if start.day != 1 or start.year != end.year or start.month != end.month:
                errors.append("period must be one completed calendar month")
            elif end.day != monthrange(end.year, end.month)[1]:
                errors.append("period must end on the calendar month boundary")
        except (KeyError, TypeError, ValueError):
            errors.append("period must contain valid start and end dates")
    sources = candidate.get("sources")
    expected = ["npm", "gsc_landing", "gsc_portfolio", "ga4_portfolio"]
    if not isinstance(sources, dict) or list(sources) != expected:
        return [*errors, "sources must contain npm, gsc_landing, gsc_portfolio and ga4_portfolio in order"]
    expected_metrics = {
        "npm": {"downloads"},
        "gsc_landing": {"clicks", "impressions", "ctr", "average_position"},
        "gsc_portfolio": {"clicks", "impressions", "ctr", "average_position"},
        "ga4_portfolio": {"sessions", "engaged_sessions", "views"},
    }
    for name in expected:
        source = sources[name]
        if not isinstance(source, dict):
            errors.append(f"sources.{name} must be an object")
            continue
        status = source.get("status")
        if status not in ("available", "unavailable"):
            errors.append(f"sources.{name}.status must be available or unavailable")
        try:
            validate_utc_timestamp(source.get("retrieved_at"))
        except (TypeError, ValueError):
            errors.append(f"sources.{name}.retrieved_at must be exact UTC")
        if not isinstance(source.get("scope"), dict) or not isinstance(source.get("definitions"), dict):
            errors.append(f"sources.{name} must contain scope and definitions")
        values = source.get("values")
        if status == "available":
            if not isinstance(values, dict) or set(values) != expected_metrics[name]:
                errors.append(f"sources.{name}.values has the wrong aggregate metrics")
            else:
                for metric_name, value in values.items():
                    if name.startswith("gsc_") and metric_name == "average_position" and value is None:
                        continue
                    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                        errors.append(f"sources.{name}.values must be non-negative numbers, except an unknown GSC average_position")
                        break
            if source.get("reason") is not None:
                errors.append(f"sources.{name}.reason must be null when available")
        else:
            if values is not None:
                errors.append(f"sources.{name}.values must be null when unavailable")
            if not isinstance(source.get("reason"), str) or not source["reason"]:
                errors.append(f"sources.{name}.reason is required when unavailable")
    return errors


def read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def collect_from_fixture_dir(fixture_dir: Path) -> Dict[str, Any]:
    fixture_dir = Path(fixture_dir)
    config = read_json(fixture_dir / "mcp-dashboard-config.json")
    environment = {
        "MCP_GSC_LANDING_SITE_URL": config["gsc_landing_site_url"],
        "MCP_GSC_PORTFOLIO_SITE_URL": config["gsc_portfolio_site_url"],
        "MCP_GA4_PORTFOLIO_PROPERTY_ID": config["ga4_portfolio_property_id"],
    }
    return build_available_dashboard(
        read_json(fixture_dir / "mcp-dashboard-npm.json"),
        read_json(fixture_dir / "mcp-gsc-landing.json"),
        read_json(fixture_dir / "mcp-gsc-portfolio.json"),
        read_json(fixture_dir / "mcp-ga4-portfolio.json"),
        config["snapshot_at"],
        environment,
    )


def request_json(url: str, timeout: int = 30) -> Any:
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "claude-code-ultimate-guide-mcp-dashboard/1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read(8 * 1024 * 1024 + 1)
    if len(raw) > 8 * 1024 * 1024:
        raise ValueError("upstream response exceeds 8 MiB")
    return json.loads(raw.decode("utf-8"))


def google_json(url: str, body: Mapping[str, Any], token: str, timeout: int = 30) -> Any:
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "claude-code-ultimate-guide-mcp-dashboard/1",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read(8 * 1024 * 1024 + 1)
    if len(raw) > 8 * 1024 * 1024:
        raise ValueError("Google response exceeds 8 MiB")
    return json.loads(raw.decode("utf-8"))


def unavailable_reason(label: str, error: BaseException) -> str:
    if isinstance(error, urllib.error.HTTPError):
        return f"{label} request failed with HTTP {error.code}"
    return f"{label} request failed; access or upstream availability was not confirmed"


def collect_live(snapshot_at: str, environment: Mapping[str, str], timeout: int = 30) -> Dict[str, Any]:
    start, end = last_completed_month(snapshot_at)
    package = urllib.parse.quote(PACKAGE, safe="@")
    npm_payload = request_json(f"{NPM_DOWNLOADS_URL}/point/{start}:{end}/{package}", timeout)
    source_scopes = scopes(environment)
    sources: Dict[str, Any] = {
        "npm": available_source(snapshot_at, source_scopes["npm"], npm_definitions(), validate_npm(npm_payload, start, end))
    }
    token = environment.get("GOOGLE_ACCESS_TOKEN")
    google_specs = [
        ("gsc_landing", "MCP_GSC_LANDING_SITE_URL", "Google Search Console", gsc_definitions()),
        ("gsc_portfolio", "MCP_GSC_PORTFOLIO_SITE_URL", "Google Search Console", gsc_definitions()),
        ("ga4_portfolio", "MCP_GA4_PORTFOLIO_PROPERTY_ID", "Google Analytics Data API", ga4_definitions()),
    ]
    for name, property_key, label, definitions in google_specs:
        property_value = environment.get(property_key)
        if not token or not property_value:
            sources[name] = unavailable_source(
                snapshot_at,
                source_scopes[name],
                definitions,
                f"GOOGLE_ACCESS_TOKEN or {property_key} is not configured",
            )
            continue
        try:
            if name.startswith("gsc_"):
                page_url = source_scopes[name]["page_url"]
                encoded_property = urllib.parse.quote(property_value, safe="")
                payload = google_json(
                    f"https://searchconsole.googleapis.com/webmasters/v3/sites/{encoded_property}/searchAnalytics/query",
                    gsc_query(start, end, page_url),
                    token,
                    timeout,
                )
                values = parse_gsc(payload, page_url)
            else:
                encoded_property = urllib.parse.quote(property_value, safe="")
                payload = google_json(
                    f"https://analyticsdata.googleapis.com/v1beta/properties/{encoded_property}:runReport",
                    ga4_query(start, end, PORTFOLIO_PAGE_PATH),
                    token,
                    timeout,
                )
                values = parse_ga4(payload, PORTFOLIO_PAGE_PATH)
            sources[name] = available_source(snapshot_at, source_scopes[name], definitions, values)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            sources[name] = unavailable_source(snapshot_at, source_scopes[name], definitions, unavailable_reason(label, error))
    return finalize_dashboard(snapshot_at, start, end, sources)


def serialize(candidate: Mapping[str, Any]) -> str:
    return json.dumps(candidate, ensure_ascii=False, indent=2) + "\n"


def stabilize_retrieval_times(candidate: Dict[str, Any], output: Path) -> Dict[str, Any]:
    if not output.exists():
        return candidate
    try:
        previous = read_json(output)
    except (OSError, json.JSONDecodeError):
        return candidate
    unchanged = True
    for name, source in candidate["sources"].items():
        previous_source = previous.get("sources", {}).get(name)
        if not isinstance(previous_source, dict):
            unchanged = False
            continue
        current_semantic = copy.deepcopy(source)
        previous_semantic = copy.deepcopy(previous_source)
        current_semantic.pop("retrieved_at", None)
        previous_semantic.pop("retrieved_at", None)
        if current_semantic == previous_semantic and isinstance(previous_source.get("retrieved_at"), str):
            source["retrieved_at"] = previous_source["retrieved_at"]
        else:
            unchanged = False
    if unchanged and previous.get("period") == candidate.get("period") and isinstance(previous.get("snapshot_at"), str):
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
    parser.add_argument("--fixture-npm", type=Path)
    parser.add_argument("--snapshot-at")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--validate-file", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    if args.validate_file:
        errors = validate_dashboard(read_json(args.validate_file))
        if errors:
            raise ValueError("invalid MCP dashboard:\n- " + "\n- ".join(errors))
        print(f"mcp_dashboard_valid={args.validate_file}")
        return 0
    if args.fixture_dir:
        candidate = collect_from_fixture_dir(args.fixture_dir)
    elif args.fixture_npm:
        if not args.snapshot_at:
            raise ValueError("--fixture-npm requires --snapshot-at")
        candidate = build_unavailable_dashboard(read_json(args.fixture_npm), args.snapshot_at, os.environ)
    else:
        candidate = collect_live(args.snapshot_at or utc_now(), os.environ, args.timeout_seconds)
    candidate = stabilize_retrieval_times(candidate, args.output)
    content = serialize(candidate)
    if args.check:
        sys.stdout.write(content)
        return 0
    changed = atomic_write_if_changed(args.output, content)
    print(f"mcp_dashboard_changed={str(changed).lower()}")
    print(f"mcp_dashboard_output={args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"collect-mcp-dashboard.py: {error}", file=sys.stderr)
        raise SystemExit(1)
