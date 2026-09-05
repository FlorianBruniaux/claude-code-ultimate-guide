#!/usr/bin/env python3
"""Render deterministic regions in the Agent Harness Landscape page."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


MARKERS = (
    "category-summary",
    "strict-runtime-map",
    "adjacent-control-planes",
    "project-catalog",
)
RFC3339_UTC_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")

CATEGORY_GUIDANCE = {
    "coding-agent-products": ("Turnkey coding agents", "Usually", "Runtime"),
    "coding-harness-configs": ("Configuration packs and agent SDKs", "Sometimes", "Repository / construction"),
    "evaluation": ("Benchmarks and evaluation harnesses", "No", "Evaluation"),
    "frameworks": ("Libraries for building an agent loop", "Sometimes", "Construction"),
    "libraries-sdks": ("Reusable agent building blocks", "No", "Construction"),
    "memory": ("Persistent state and retrieval", "No", "Memory"),
    "multi-agent": ("Coordination across agents or runtimes", "Sometimes", "Orchestrator"),
    "observability": ("Tracing, quality, and operations", "No", "Observability"),
    "personal-agent-runtimes": ("Ready-to-run personal agents", "Usually", "Runtime"),
    "plugins-mcp-cli": ("Tools connected to an existing runtime", "No", "Extension"),
    "progressive-disclosure": ("Context and prompt-loading strategies", "Sometimes", "Repository / context"),
    "research-task": ("Domain-specific agents and research systems", "Sometimes", "Runtime / task-specific"),
}

GUIDE_PROFILES = {
    "aider": "./agentic-tools.md#13-aider",
    "codex": "./agentic-tools.md#11-codex-cli-openai",
    "crush": "./agentic-tools.md#17-crush-charm",
    "deepseek-harness": "./agentic-tools.md#18-deepseek-harness-dsh",
    "gemini-cli": "./agentic-tools.md#16-gemini-cli-google",
    "goose": "./agentic-tools.md#14-goose-aaifblock",
    "openhands": "./agentic-tools.md#24-openhands-all-hands-ai",
    "opencode": "./agentic-tools.md#15-opencode-anomaly-formerly-sst",
    "swe-agent": "./agentic-tools.md#22-swe-agent-princeton",
}

UNKNOWN_MARKER = '<abbr title="Not established from the pinned sources">?</abbr>'
GITHUB_SIDECAR_FIELDS = {
    "repository_url", "resolved_full_name", "stargazers_count", "archived", "language",
    "license_spdx", "pushed_at", "default_branch", "captured_at", "etag",
}
GITHUB_SIDECAR_REQUIRED_FIELDS = GITHUB_SIDECAR_FIELDS - {"etag"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("catalog must be a JSON object")
    return value


def markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def humanize(value: Any) -> str:
    if value is None or value == "":
        return UNKNOWN_MARKER
    text = str(value)
    if text.casefold() == "unknown":
        return UNKNOWN_MARKER
    if text == "not_applicable":
        return "N/A"
    return text.replace("_", " ").strip().capitalize()


def concise_summary(record: dict[str, Any], limit: int = 180) -> str:
    """Return one plain-text sentence for dense comparison tables."""
    if not record.get("summary"):
        return UNKNOWN_MARKER
    raw = str(record["summary"])
    plain = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", raw)
    plain = plain.replace("**", "").replace("__", "").replace("`", "")
    plain = plain.replace("—", ": ").replace("–", "-")
    plain = re.sub(r"\s+", " ", plain).strip()
    sentence = re.split(r"(?<=[.!?])\s+", plain, maxsplit=1)[0]
    if len(sentence) <= limit:
        return sentence
    clipped = sentence[: limit - 3].rsplit(" ", 1)[0].rstrip(" ,;:")
    return clipped + "..."


def project_index(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    sets = catalog["sets"]
    records = list(sets["upstream_snapshot"]["projects"]) + list(sets["guide_supplement"])
    return {record["id"]: record for record in records}


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


def validate_utc_timestamp(value: Any, label: str) -> str:
    if not isinstance(value, str) or not RFC3339_UTC_PATTERN.fullmatch(value):
        raise ValueError(f"{label} must be an RFC 3339 UTC timestamp")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{label} must be an RFC 3339 UTC timestamp") from error
    return value


def canonical_github_repository_url(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("GitHub sidecar repository_url must be a string")
    parsed = urlparse(value)
    parts = [part for part in parsed.path.split("/") if part]
    if (
        parsed.scheme != "https" or parsed.netloc.lower() != "github.com" or parsed.username
        or parsed.password or parsed.params or parsed.query or parsed.fragment or len(parts) != 2
    ):
        raise ValueError("GitHub sidecar repository_url must be canonical")
    canonical = f"https://github.com/{parts[0]}/{parts[1]}"
    if value != canonical:
        raise ValueError("GitHub sidecar repository_url must be canonical")
    return canonical


def apply_github_sidecar(catalog: dict[str, Any], sidecar: dict[str, Any]) -> dict[str, Any]:
    """Overlay checksum-bound GitHub stars and archive state without mutating the catalog."""
    checksum = verified_catalog_checksum(catalog)
    if set(sidecar) != {"schema_version", "catalog_sha256", "captured_at", "repositories"}:
        raise ValueError("GitHub sidecar top-level fields are invalid")
    if sidecar.get("schema_version") != "1.0.0":
        raise ValueError("GitHub sidecar schema_version is invalid")
    if sidecar.get("catalog_sha256") != checksum:
        raise ValueError("GitHub sidecar checksum does not match catalog")
    sidecar_captured_at = validate_utc_timestamp(sidecar.get("captured_at"), "GitHub sidecar captured_at")
    repositories = sidecar.get("repositories")
    if not isinstance(repositories, list):
        raise ValueError("GitHub sidecar repositories must be an array")
    sidecar_by_url: dict[str, dict[str, Any]] = {}
    for repository in repositories:
        if not isinstance(repository, dict):
            raise ValueError("GitHub sidecar repository must be an object")
        if set(repository) - GITHUB_SIDECAR_FIELDS or not GITHUB_SIDECAR_REQUIRED_FIELDS.issubset(repository):
            raise ValueError("GitHub sidecar repository fields are invalid")
        url = canonical_github_repository_url(repository.get("repository_url"))
        if url in sidecar_by_url:
            raise ValueError("GitHub sidecar repository URLs must be unique strings")
        expected_full_name = "/".join(urlparse(url).path.split("/")[1:])
        resolved_full_name = repository.get("resolved_full_name")
        if not isinstance(resolved_full_name, str) or resolved_full_name.casefold() != expected_full_name.casefold():
            raise ValueError("GitHub sidecar resolved_full_name differs from repository_url")
        stars = repository.get("stargazers_count")
        if not isinstance(stars, int) or isinstance(stars, bool) or stars < 0:
            raise ValueError("GitHub sidecar stargazers_count must be a non-negative integer")
        if not isinstance(repository.get("archived"), bool):
            raise ValueError("GitHub sidecar archived must be boolean")
        for nullable_field in ("language", "license_spdx"):
            value = repository.get(nullable_field)
            if value is not None and not isinstance(value, str):
                raise ValueError(f"GitHub sidecar {nullable_field} must be a string or null")
        pushed_at = repository.get("pushed_at")
        if pushed_at is not None:
            validate_utc_timestamp(pushed_at, "GitHub sidecar pushed_at")
        if not isinstance(repository.get("default_branch"), str) or not repository["default_branch"]:
            raise ValueError("GitHub sidecar default_branch must be a non-empty string")
        captured_at = validate_utc_timestamp(repository.get("captured_at"), "GitHub sidecar repository captured_at")
        if captured_at != sidecar_captured_at:
            raise ValueError("GitHub sidecar repository captured_at differs from sidecar captured_at")
        if "etag" in repository and (not isinstance(repository["etag"], str) or not repository["etag"]):
            raise ValueError("GitHub sidecar etag must be a non-empty string")
        sidecar_by_url[url] = repository
    merged = copy.deepcopy(catalog)
    records = (
        merged["sets"]["upstream_snapshot"]["projects"]
        + merged["sets"]["guide_supplement"]
    )
    catalog_urls = {record["repository_url"] for record in records if record.get("repository_url")}
    if set(sidecar_by_url) != catalog_urls:
        raise ValueError("GitHub sidecar repository URLs do not match catalog")
    if repositories != sorted(repositories, key=lambda item: item["repository_url"].casefold()):
        raise ValueError("GitHub sidecar repositories are not deterministically sorted")
    for record in records:
        repository = sidecar_by_url.get(record.get("repository_url"))
        if repository is None:
            continue
        record["stars"] = repository["stargazers_count"]
        record["stars_captured_at"] = repository["captured_at"][:10]
        record["archived"] = repository["archived"]
    return merged


def render_project_cell(record: dict[str, Any]) -> str:
    suffix = " (Archived)" if record.get("archived") is True else ""
    cell = f"[{markdown_escape(record['name'])}]({record['project_url']}){suffix}"
    stars = record.get("stars")
    captured = record.get("stars_captured_at")
    repository = record.get("repository_url")
    if isinstance(stars, int) and repository and captured:
        cell += f"<br><small>★ {stars:,} · {captured}</small>"
    return cell


def render_category_summary(catalog: dict[str, Any]) -> str:
    lines = [
        "| Category | Projects | What it contributes | Owns an agent loop? | Guide layer |",
        "|---|---:|---|---|---|",
    ]
    for category in catalog["sets"]["upstream_snapshot"]["categories"]:
        contribution, loop, layer = CATEGORY_GUIDANCE[category["id"]]
        lines.append(
            f"| [{markdown_escape(category['title'])}](#{category['id']}) | {category['count']} | "
            f"{contribution} | {loop} | {layer} |"
        )
    return "\n".join(lines)


def _render_profile(mapping_id: str) -> str:
    profile = GUIDE_PROFILES.get(mapping_id)
    return f" [Guide profile]({profile})" if profile else ""


def render_strict_runtime_map(catalog: dict[str, Any]) -> str:
    records = project_index(catalog)
    lines = [
        f"**Snapshot:** {catalog['_meta']['generated_at'][:10]}. "
        "GitHub stars are captured on the date shown in each project cell.",
        "",
        f"**Legend:** {UNKNOWN_MARKER} = not established from the pinned sources; "
        "N/A = does not apply.",
        "",
        "| Harness | Interface | Provider strategy | Loop evidence | Licence | Role |",
        "|---|---|---|---|---|---|",
    ]
    for mapping in catalog["sets"]["strict_runtime_map"]:
        record = records[mapping["project_ref"]]
        interfaces = ", ".join(humanize(item) for item in record.get("interfaces", [])) or UNKNOWN_MARKER
        role = markdown_escape(concise_summary(record)) + _render_profile(mapping["id"])
        lines.append(
            f"| {render_project_cell(record)} | {interfaces} | {humanize(record['provider_strategy'])} | "
            f"{humanize(mapping['evidence_status'])} | "
            f"{markdown_escape(humanize(record['license_signal']))} | {role} |"
        )
    return "\n".join(lines)


def render_adjacent_control_planes(catalog: dict[str, Any]) -> str:
    records = project_index(catalog)
    lines = [
        "| Control plane | Role | Loop ownership | Licence |",
        "|---|---|---|---|",
    ]
    for mapping in catalog["sets"]["adjacent_control_planes"]:
        record = records[mapping["project_ref"]]
        lines.append(
            f"| {render_project_cell(record)} | {markdown_escape(concise_summary(record))} | "
            f"{humanize(mapping['owns_loop'])}; evidence {humanize(mapping['evidence_status']).casefold()} | "
            f"{markdown_escape(humanize(record['license_signal']))} |"
        )
    return "\n".join(lines)


def _capabilities(record: dict[str, Any]) -> str:
    confirmed = [
        name.replace("_", " ")
        for name, feature in record.get("features", {}).items()
        if feature.get("status") in {"confirmed", "claimed"}
    ]
    values = confirmed + list(record.get("tags", []))
    unique: list[str] = []
    for value in values:
        label = humanize(value)
        if label not in unique:
            unique.append(label)
        if len(unique) == 4:
            break
    return ", ".join(unique) if unique else UNKNOWN_MARKER


def _directory_table(records: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Project | Role | Main capabilities | Adoption | Autonomy / Recovery | Licence |",
        "|---|---|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            f"| {render_project_cell(record)} | {markdown_escape(concise_summary(record))} | "
            f"{_capabilities(record)} | {humanize(record['adoption_surface'])} | "
            f"{humanize(record['autonomy'])} / {humanize(record['recovery'])} | "
            f"{markdown_escape(humanize(record['license_signal']))} |"
        )
    return lines


def render_project_catalog(catalog: dict[str, Any]) -> str:
    upstream = catalog["sets"]["upstream_snapshot"]
    by_category: dict[str, list[dict[str, Any]]] = {category["id"]: [] for category in upstream["categories"]}
    for record in upstream["projects"]:
        by_category[record["category"]].append(record)

    lines = ["<!-- BEGIN UPSTREAM PROJECT DIRECTORY -->"]
    for category in upstream["categories"]:
        records = sorted(by_category[category["id"]], key=lambda item: item["name"].casefold())
        lines.extend(
            [
                f'<details><summary id="{category["id"]}"><strong>{markdown_escape(category["title"])} '
                f'({len(records)})</strong></summary>',
                "",
                *_directory_table(records),
                "",
                "</details>",
                "",
            ]
        )
    lines.append("<!-- END UPSTREAM PROJECT DIRECTORY -->")

    supplements = sorted(catalog["sets"]["guide_supplement"], key=lambda item: item["name"].casefold())
    lines.extend(
        [
            "",
            f"### Guide supplements ({len(supplements)})",
            "",
            "These official products and researched candidates are absent from the pinned upstream snapshot. "
            "Their inclusion does not change the upstream 160-project count.",
            "",
            *_directory_table(supplements),
        ]
    )
    return "\n".join(lines).rstrip()


def replace_generated_section(text: str, marker: str, replacement: str) -> str:
    begin = f"<!-- BEGIN GENERATED: {marker} -->"
    end = f"<!-- END GENERATED: {marker} -->"
    if text.count(begin) != 1 or text.count(end) != 1:
        raise ValueError(f"generated marker {marker!r} must occur exactly once")
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.DOTALL)
    return pattern.sub(f"{begin}\n{replacement.rstrip()}\n{end}", text)


def build_page(text: str, catalog: dict[str, Any]) -> str:
    rendered = {
        "category-summary": render_category_summary(catalog),
        "strict-runtime-map": render_strict_runtime_map(catalog),
        "adjacent-control-planes": render_adjacent_control_planes(catalog),
        "project-catalog": render_project_catalog(catalog),
    }
    for marker in MARKERS:
        text = replace_generated_section(text, marker, rendered[marker])
    return text.rstrip() + "\n"


def count_table_records(fragment: str) -> int:
    return max(0, sum(line.startswith("| ") for line in fragment.splitlines()) - 1)


def count_upstream_project_links(fragment: str) -> int:
    match = re.search(
        r"<!-- BEGIN UPSTREAM PROJECT DIRECTORY -->(.*?)<!-- END UPSTREAM PROJECT DIRECTORY -->",
        fragment,
        re.DOTALL,
    )
    if not match:
        return 0
    return sum(
        1
        for line in match.group(1).splitlines()
        if line.startswith("| [") and "](https://" in line.split("|", 2)[1]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--page", type=Path, required=True)
    parser.add_argument("--github-sidecar", type=Path)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog = load_json(args.catalog)
    if args.github_sidecar is not None:
        catalog = apply_github_sidecar(catalog, load_json(args.github_sidecar))
    current = args.page.read_text(encoding="utf-8")
    rendered = build_page(current, catalog)
    if args.check:
        if rendered != current:
            print("generated Agent Harness Landscape regions are stale", file=sys.stderr)
            return 1
        print("generated Agent Harness Landscape regions are current")
        return 0
    args.page.write_text(rendered, encoding="utf-8")
    print(f"updated {args.page}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
