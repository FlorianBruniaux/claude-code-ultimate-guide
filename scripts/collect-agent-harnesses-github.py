#!/usr/bin/env python3
"""Collect verified GitHub metadata for the Agent Harness catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse


GITHUB_API_VERSION = "2022-11-28"
SIDECAR_SCHEMA_VERSION = "1.0.0"
REPOSITORY_FIELDS = {
    "repository_url", "resolved_full_name", "stargazers_count", "archived", "language",
    "license_spdx", "pushed_at", "default_branch", "captured_at", "etag",
}
MAX_RESPONSE_BYTES = 1_000_000
MIN_RATE_LIMIT_REMAINING = 100
MAX_RETRY_DELAY_SECONDS = 30
MAX_REQUEST_ATTEMPTS = 3
TRANSIENT_HTTP_STATUSES = {429, 500, 502, 503, 504}
RFC3339_UTC_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


def serialize_sidecar(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def verified_catalog_checksum(catalog: dict[str, Any]) -> str:
    embedded = catalog.get("_meta", {}).get("dataset_sha256")
    if not isinstance(embedded, str) or len(embedded) != 64:
        raise ValueError("catalog dataset_sha256 is required")
    without_checksum = json.loads(json.dumps(catalog))
    without_checksum.get("_meta", {}).pop("dataset_sha256", None)
    payload = json.dumps(without_checksum, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    computed = hashlib.sha256(payload.encode()).hexdigest()
    if embedded != computed:
        raise ValueError("catalog checksum is invalid")
    return computed


def read_limited_stream(stream: Any, max_bytes: int = MAX_RESPONSE_BYTES) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = stream.read(min(64 * 1024, max_bytes + 1 - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > max_bytes:
            raise ValueError(f"GitHub API response exceeds {max_bytes} bytes")
    return b"".join(chunks)


def enforce_rate_limit(headers: dict[str, Any]) -> None:
    remaining = _header(headers, "X-RateLimit-Remaining")
    if remaining is None:
        return
    try:
        parsed = int(remaining)
    except (TypeError, ValueError) as error:
        raise ValueError("GitHub rate limit remaining header is invalid") from error
    if parsed < MIN_RATE_LIMIT_REMAINING:
        reset = _header(headers, "X-RateLimit-Reset")
        suffix = f"; reset={reset}" if reset is not None else ""
        raise ValueError(
            f"GitHub rate limit remaining {parsed} is below {MIN_RATE_LIMIT_REMAINING}{suffix}"
        )


def retry_delay_seconds(headers: dict[str, Any], attempt: int) -> int:
    retry_after = _header(headers, "Retry-After")
    try:
        parsed = int(retry_after)
    except (TypeError, ValueError):
        parsed = 2 ** attempt
    return max(1, min(parsed, MAX_RETRY_DELAY_SECONDS))


def canonical_repository_url(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("repository_url must be a string")
    parsed = urlparse(value)
    parts = [part for part in parsed.path.split("/") if part]
    if (
        parsed.scheme != "https" or parsed.netloc.lower() != "github.com" or parsed.username
        or parsed.password or parsed.params or parsed.query or parsed.fragment or len(parts) != 2
    ):
        raise ValueError("repository_url must be a canonical GitHub HTTPS URL")
    canonical = f"https://github.com/{parts[0]}/{parts[1]}"
    if value != canonical:
        raise ValueError("repository_url must be canonical without a trailing slash")
    return canonical


def catalog_repository_urls(catalog: dict[str, Any]) -> list[str]:
    try:
        sets = catalog["sets"]
        records = list(sets["upstream_snapshot"]["projects"]) + list(sets["guide_supplement"])
    except (KeyError, TypeError) as error:
        raise ValueError("catalog does not contain Agent Harness project sets") from error
    urls = [canonical_repository_url(record["repository_url"]) for record in records if record.get("repository_url")]
    if len({url.casefold() for url in urls}) != len(urls):
        raise ValueError("catalog contains a duplicate canonical GitHub repository")
    return sorted(urls, key=str.casefold)


def _validate_timestamp(value: Any, label: str) -> str:
    if not isinstance(value, str) or not RFC3339_UTC_PATTERN.fullmatch(value):
        raise ValueError(f"{label} must be an RFC 3339 UTC timestamp")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{label} must be an RFC 3339 UTC timestamp") from error
    return value


def _header(headers: dict[str, Any], name: str) -> Any:
    for key, value in headers.items():
        if key.casefold() == name.casefold():
            return value
    return None


def _expected_full_name(repository_url: str) -> str:
    return "/".join(urlparse(repository_url).path.split("/")[1:])


def _normalize_response(repository_url: str, payload: Any, headers: dict[str, Any], captured_at: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("GitHub API response must be a JSON object")
    expected_full_name = _expected_full_name(repository_url)
    full_name = payload.get("full_name")
    if not isinstance(full_name, str) or full_name.casefold() != expected_full_name.casefold():
        raise ValueError(f"GitHub resolved_full_name differs from catalog: {repository_url}")
    stars = payload.get("stargazers_count")
    if not isinstance(stars, int) or isinstance(stars, bool) or stars < 0:
        raise ValueError("GitHub stargazers_count must be a non-negative integer")
    if not isinstance(payload.get("archived"), bool):
        raise ValueError("GitHub archived must be boolean")
    language = payload.get("language")
    if language is not None and not isinstance(language, str):
        raise ValueError("GitHub language must be a string or null")
    license_data = payload.get("license")
    if license_data is not None and not isinstance(license_data, dict):
        raise ValueError("GitHub license must be an object or null")
    license_spdx = None if license_data is None else license_data.get("spdx_id")
    if license_spdx is not None and not isinstance(license_spdx, str):
        raise ValueError("GitHub license.spdx_id must be a string or null")
    pushed_at = payload.get("pushed_at")
    if pushed_at is not None:
        _validate_timestamp(pushed_at, "GitHub pushed_at")
    default_branch = payload.get("default_branch")
    if not isinstance(default_branch, str) or not default_branch:
        raise ValueError("GitHub default_branch must be a non-empty string")
    record: dict[str, Any] = {
        "repository_url": repository_url, "resolved_full_name": full_name,
        "stargazers_count": stars, "archived": payload["archived"], "language": language,
        "license_spdx": license_spdx, "pushed_at": pushed_at, "default_branch": default_branch,
        "captured_at": captured_at,
    }
    etag = _header(headers, "ETag")
    if etag is not None:
        if not isinstance(etag, str) or not etag:
            raise ValueError("GitHub ETag must be a non-empty string")
        record["etag"] = etag
    return record


def validate_sidecar(sidecar: Any, catalog_sha256: str, expected_urls: list[str]) -> list[str]:
    if not isinstance(sidecar, dict):
        return ["sidecar must be an object"]
    errors: list[str] = []
    if sidecar.get("schema_version") != SIDECAR_SCHEMA_VERSION:
        errors.append("sidecar schema_version is invalid")
    if sidecar.get("catalog_sha256") != catalog_sha256:
        errors.append("sidecar catalog checksum does not match catalog")
    try:
        _validate_timestamp(sidecar.get("captured_at"), "sidecar captured_at")
    except ValueError as error:
        errors.append(str(error))
    repositories = sidecar.get("repositories")
    if not isinstance(repositories, list):
        return errors + ["sidecar repositories must be an array"]
    if len(repositories) != len(expected_urls):
        errors.append("sidecar repository cardinality does not match catalog")
    records_by_url: dict[str, dict[str, Any]] = {}
    for record in repositories:
        if not isinstance(record, dict):
            errors.append("sidecar repository must be an object")
            continue
        if set(record) - REPOSITORY_FIELDS:
            errors.append("sidecar repository has unapproved fields")
        try:
            repository_url = canonical_repository_url(record.get("repository_url"))
            if repository_url in records_by_url:
                errors.append("sidecar contains duplicate repository_url")
            records_by_url[repository_url] = record
            normalized = _normalize_response(repository_url, {
                "full_name": record.get("resolved_full_name"), "stargazers_count": record.get("stargazers_count"),
                "archived": record.get("archived"), "language": record.get("language"),
                "license": {"spdx_id": record.get("license_spdx")} if record.get("license_spdx") is not None else None,
                "pushed_at": record.get("pushed_at"), "default_branch": record.get("default_branch"),
            }, {"ETag": record["etag"]} if "etag" in record else {}, record.get("captured_at"))
            if set(normalized) != set(record):
                errors.append("sidecar repository fields are incomplete")
        except ValueError as error:
            errors.append(str(error))
    if set(records_by_url) != set(expected_urls):
        errors.append("sidecar repository URLs do not match catalog")
    if repositories != sorted(repositories, key=lambda item: str(item.get("repository_url", "")).casefold()):
        errors.append("sidecar repositories are not deterministically sorted")
    return errors


def collect_metadata(
    catalog: dict[str, Any],
    transport: Callable[[str, dict[str, str]], tuple[int, dict[str, Any], Any]],
    captured_at: str,
    previous_sidecar: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Collect one complete, checksum-bound metadata sidecar through `transport`."""
    _validate_timestamp(captured_at, "captured_at")
    catalog_checksum = verified_catalog_checksum(catalog)
    urls = catalog_repository_urls(catalog)
    previous_by_url: dict[str, dict[str, Any]] = {}
    if previous_sidecar is not None:
        errors = validate_sidecar(previous_sidecar, catalog_checksum, urls)
        if errors:
            raise ValueError("previous sidecar is invalid:\n- " + "\n- ".join(errors))
        previous_by_url = {record["repository_url"]: record for record in previous_sidecar["repositories"]}
    repositories: list[dict[str, Any]] = []
    for repository_url in urls:
        expected_full_name = _expected_full_name(repository_url)
        headers = {
            "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": GITHUB_API_VERSION,
            "User-Agent": "claude-code-ultimate-guide-agent-harnesses",
        }
        cached = previous_by_url.get(repository_url)
        if cached and cached.get("etag"):
            headers["If-None-Match"] = cached["etag"]
        status, response_headers, payload = transport(f"https://api.github.com/repos/{expected_full_name}", headers)
        enforce_rate_limit(response_headers)
        if status == 304:
            if cached is None:
                raise ValueError(f"GitHub API returned 304 without cached metadata: {repository_url}")
            record = dict(cached)
            record["captured_at"] = captured_at
            repositories.append(record)
        elif status == 200:
            repositories.append(_normalize_response(repository_url, payload, response_headers, captured_at))
        else:
            raise ValueError(f"GitHub API returned HTTP {status}: {repository_url}")
    sidecar = {
        "schema_version": SIDECAR_SCHEMA_VERSION, "catalog_sha256": catalog_checksum,
        "captured_at": captured_at,
        "repositories": sorted(repositories, key=lambda item: item["repository_url"].casefold()),
    }
    errors = validate_sidecar(sidecar, catalog_checksum, urls)
    if errors:
        raise ValueError("generated sidecar is invalid:\n- " + "\n- ".join(errors))
    return sidecar


def write_sidecar(path: Path, sidecar: dict[str, Any]) -> None:
    """Atomically replace `path` only after a complete sidecar has been validated."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(serialize_sidecar(sidecar))
        handle.flush()
        os.fsync(handle.fileno())
    try:
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _network_transport(token: str) -> Callable[[str, dict[str, str]], tuple[int, dict[str, Any], Any]]:
    def request(url: str, headers: dict[str, str]) -> tuple[int, dict[str, Any], Any]:
        request_headers = {**headers, "Authorization": f"Bearer {token}"}
        for attempt in range(MAX_REQUEST_ATTEMPTS):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=request_headers), timeout=30) as response:
                    raw = read_limited_stream(response)
                    return response.status, dict(response.headers.items()), json.loads(raw.decode("utf-8"))
            except urllib.error.HTTPError as error:
                response_headers = dict(error.headers.items()) if error.headers else {}
                raw = read_limited_stream(error)
                try:
                    payload = json.loads(raw.decode("utf-8")) if raw else None
                except (UnicodeDecodeError, json.JSONDecodeError):
                    payload = None
                retryable = error.code in TRANSIENT_HTTP_STATUSES or (
                    error.code == 403 and _header(response_headers, "Retry-After") is not None
                )
                if retryable and attempt + 1 < MAX_REQUEST_ATTEMPTS:
                    time.sleep(retry_delay_seconds(response_headers, attempt))
                    continue
                return error.code, response_headers, payload
            except OSError as error:
                if attempt + 1 < MAX_REQUEST_ATTEMPTS:
                    time.sleep(2 ** attempt)
                    continue
                raise ValueError(f"GitHub API request failed after {MAX_REQUEST_ATTEMPTS} attempts: {error}") from error
        raise AssertionError("unreachable GitHub request loop")
    return request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--captured-at")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required; sidecar output was not changed")
    captured_at = args.captured_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        previous_path = args.previous or args.output
        previous = json.loads(previous_path.read_text(encoding="utf-8")) if previous_path.exists() else None
        sidecar = collect_metadata(catalog, _network_transport(token), captured_at, previous)
        write_sidecar(args.output, sidecar)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"GitHub metadata collection failed; sidecar output was not changed: {error}") from error
    print(f"published GitHub metadata for {len(sidecar['repositories'])} repositories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
