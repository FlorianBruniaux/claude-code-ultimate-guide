"""Deterministic normalization and validation for the agent-harness catalog."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


PINNED_UPSTREAM_COMMIT = "ece314654d2c23fe7bd69fc6ef7088f093207e49"
PINNED_UPSTREAM_SHA256 = "4c02e547e11b056aa4d7e519305b7f4ca4f02550c27018d70757a59d26ace65f"
UPSTREAM_PROJECT_COUNT = 160
UPSTREAM_CATEGORY_COUNT = 12
MAX_UPSTREAM_BYTES = 2_000_000
EVIDENCE_STATUSES = {"confirmed", "claimed", "unknown", "not_applicable"}
LOOP_STATUSES = {"confirmed", "claimed", "unknown", "no"}
AUTONOMY_VALUES = {
    "step_gated",
    "checkpoint_gated",
    "bounded",
    "headless",
    "unknown",
    "not_applicable",
}
RECOVERY_VALUES = {"none", "retry", "resumable", "durable", "unknown", "not_applicable"}
INTERFACE_VALUES = {"chat", "cli", "desktop", "ide", "tui", "web"}
INTERFACE_TAG_MAP = {
    "browser": "web",
    "cli": "cli",
    "ide": "ide",
    "tui": "tui",
}
PINNED_GITHUB_RE = re.compile(r"^https://github\.com/[^/]+/[^/]+/(?:blob|commit)/[0-9a-fA-F]{40}(?:/|$)")
PINNED_RAW_GITHUB_RE = re.compile(
    r"^https://raw\.githubusercontent\.com/[^/]+/[^/]+/[0-9a-fA-F]{40}/"
)
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def load_pinned_snapshot(
    path: Path, manifest_path: Path, max_bytes: int = MAX_UPSTREAM_BYTES
) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    expected_manifest_fields = {
        "repository",
        "commit",
        "sha256",
        "license",
        "project_count",
        "category_count",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("upstream source manifest fields are invalid")
    if manifest.get("commit") != PINNED_UPSTREAM_COMMIT:
        raise ValueError("declared upstream commit is invalid")
    if manifest.get("sha256") != PINNED_UPSTREAM_SHA256:
        raise ValueError("declared upstream SHA-256 is invalid")
    if manifest.get("license") != "CC-BY-SA-4.0":
        raise ValueError("declared upstream license is invalid")
    if manifest.get("project_count") != UPSTREAM_PROJECT_COUNT:
        raise ValueError("declared upstream project count is invalid")
    if manifest.get("category_count") != UPSTREAM_CATEGORY_COUNT:
        raise ValueError("declared upstream category count is invalid")
    source_size = path.stat().st_size
    if source_size > max_bytes:
        raise ValueError(f"source snapshot exceeds {max_bytes} bytes")
    with path.open("rb") as handle:
        raw = handle.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise ValueError(f"source snapshot exceeds {max_bytes} bytes")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PINNED_UPSTREAM_SHA256:
        raise ValueError("source snapshot SHA-256 mismatch")
    try:
        source = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("source snapshot is not valid UTF-8 JSON") from error
    if not isinstance(source, dict):
        raise ValueError("source snapshot must contain a JSON object")
    if source.get("meta", {}).get("url") != manifest.get("repository"):
        raise ValueError("source repository does not match its declaration")
    return source


def serialize_catalog(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(serialize_catalog(data), encoding="utf-8")
    temporary.replace(path)


def _is_https(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username


def _is_github_repository(value: Any) -> bool:
    if not _is_https(value):
        return False
    parsed = urlparse(value)
    return parsed.netloc.lower() == "github.com" and len([part for part in parsed.path.split("/") if part]) == 2


def _validate_evidence(evidence: Any) -> list[str]:
    if not isinstance(evidence, dict):
        return ["evidence entry must be an object"]
    errors: list[str] = []
    if evidence.get("status") not in EVIDENCE_STATUSES:
        errors.append("evidence status is invalid")
    url = evidence.get("url")
    if not _is_https(url):
        errors.append("evidence URL must be absolute HTTPS")
    elif urlparse(url).netloc.lower() in {"github.com", "www.github.com"}:
        if not PINNED_GITHUB_RE.match(url):
            errors.append("GitHub evidence URL must pin a 40-character commit")
    elif urlparse(url).netloc.lower() == "raw.githubusercontent.com":
        if not PINNED_RAW_GITHUB_RE.match(url):
            errors.append("GitHub evidence URL must pin a 40-character commit")
    checked_at = evidence.get("checked_at")
    if not isinstance(checked_at, str) or not DATE_RE.match(checked_at):
        errors.append("evidence checked_at must be YYYY-MM-DD")
    return errors


def validate_feature(feature: Any) -> list[str]:
    if not isinstance(feature, dict):
        return ["feature must be an object"]
    errors: list[str] = []
    allowed = {"value", "status", "evidence"}
    extra = sorted(set(feature) - allowed)
    if extra:
        errors.append(f"feature has unknown fields: {', '.join(extra)}")
    status = feature.get("status")
    if status not in EVIDENCE_STATUSES:
        errors.append("feature status is invalid")
    evidence = feature.get("evidence")
    if not isinstance(evidence, list):
        errors.append("feature evidence must be an array")
        evidence = []
    if status in {"confirmed", "claimed"} and not evidence:
        errors.append("feature status requires evidence")
    if status in {"unknown", "not_applicable"} and evidence:
        errors.append("unknown or not_applicable feature cannot carry evidence")
    for item in evidence:
        errors.extend(_validate_evidence(item))
    return errors


def validate_record(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ["project record must be an object"]
    errors: list[str] = []
    required = {
        "id",
        "name",
        "project_url",
        "repository_url",
        "homepage_url",
        "category",
        "summary",
        "owns_loop",
        "stars",
        "stars_captured_at",
        "license_signal",
        "archived",
        "language",
        "interfaces",
        "provider_strategy",
        "tags",
        "adoption_surface",
        "autonomy",
        "recovery",
        "features",
        "freshness",
        "provenance",
    }
    missing = sorted(required - set(record))
    if missing:
        errors.append(f"missing project fields: {', '.join(missing)}")
    extra = sorted(set(record) - required)
    if extra:
        errors.append(f"project has unknown fields: {', '.join(extra)}")
    if not _is_https(record.get("project_url")):
        errors.append("project_url must be absolute HTTPS")
    repository_url = record.get("repository_url")
    if repository_url is not None and not _is_github_repository(repository_url):
        errors.append("repository_url must be a canonical GitHub HTTPS URL or null")
    homepage_url = record.get("homepage_url")
    if homepage_url is not None and not _is_https(homepage_url):
        errors.append("homepage_url must be absolute HTTPS or null")
    stars = record.get("stars")
    captured = record.get("stars_captured_at")
    if stars is not None and (not isinstance(stars, int) or isinstance(stars, bool) or stars < 0):
        errors.append("stars must be a non-negative integer or null")
    if stars is not None and repository_url is None:
        errors.append("stars require repository_url")
    if stars is not None and not captured:
        errors.append("stars require stars_captured_at")
    if repository_url is None and stars is not None:
        errors.append("non-GitHub project stars must be null")
    if captured is not None and (not isinstance(captured, str) or not DATE_RE.match(captured)):
        errors.append("stars_captured_at must be YYYY-MM-DD or null")
    if record.get("owns_loop") not in LOOP_STATUSES:
        errors.append("owns_loop status is invalid")
    if record.get("autonomy") not in AUTONOMY_VALUES:
        errors.append("autonomy status is invalid")
    if record.get("recovery") not in RECOVERY_VALUES:
        errors.append("recovery status is invalid")
    interfaces = record.get("interfaces")
    if not isinstance(interfaces, list):
        errors.append("interfaces must be an array")
    else:
        unsupported = sorted(
            (str(value) for value in interfaces if not isinstance(value, str) or value not in INTERFACE_VALUES),
            key=str.casefold,
        )
        if unsupported:
            errors.append(f"interfaces contain unsupported values: {', '.join(unsupported)}")
        if not unsupported and interfaces != sorted(set(interfaces)):
            errors.append("interfaces must be unique and deterministically sorted")
    if record.get("archived") not in {True, False, "unknown"}:
        errors.append("archived must be true, false, or unknown")
    features = record.get("features")
    if not isinstance(features, dict):
        errors.append("features must be an object")
    else:
        for name, feature in features.items():
            errors.extend(f"feature {name}: {error}" for error in validate_feature(feature))
    freshness = record.get("freshness")
    if not isinstance(freshness, dict):
        errors.append("freshness must be an object")
    else:
        source_commit = freshness.get("source_commit")
        if repository_url is not None and not COMMIT_RE.match(str(source_commit or "")):
            errors.append("freshness source_commit must be 40 hexadecimal characters for GitHub projects")
        if repository_url is None and source_commit is not None and not COMMIT_RE.match(str(source_commit)):
            errors.append("freshness source_commit must be null or 40 hexadecimal characters")
        if not DATE_RE.match(str(freshness.get("checked_at", ""))):
            errors.append("freshness checked_at must be YYYY-MM-DD")
    provenance = record.get("provenance")
    if not isinstance(provenance, list) or not provenance:
        errors.append("project provenance is required")
    else:
        for item in provenance:
            errors.extend(_validate_evidence(item))
    return errors


def _validate_map_record(record: Any, known_refs: set[str], label: str) -> list[str]:
    if not isinstance(record, dict):
        return [f"{label} entry must be an object"]
    errors: list[str] = []
    required = {"id", "project_ref", "source_set", "owns_loop", "evidence_status", "evidence"}
    if set(record) != required:
        errors.append(f"{label} entry fields are invalid")
    if record.get("project_ref") not in known_refs:
        errors.append(f"{label} references unknown project {record.get('project_ref')}")
    if record.get("owns_loop") not in LOOP_STATUSES:
        errors.append(f"{label} owns_loop status is invalid")
    if record.get("evidence_status") not in EVIDENCE_STATUSES:
        errors.append(f"{label} evidence status is invalid")
    if record.get("evidence_status") not in {"confirmed", "claimed"}:
        errors.append(f"{label} requires evidence_status confirmed or claimed")
    evidence = record.get("evidence")
    if not isinstance(evidence, list):
        errors.append(f"{label} evidence must be an array")
        evidence = []
    if record.get("evidence_status") in {"confirmed", "claimed"} and not evidence:
        errors.append(f"{label} evidence is required")
    evidence_status = record.get("evidence_status")
    for item in evidence:
        errors.extend(f"{label}: {error}" for error in _validate_evidence(item))
        if isinstance(item, dict) and item.get("status") != evidence_status:
            errors.append(f"{label} evidence status must match evidence_status")
    return errors


def validate_catalog(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["catalog must be an object"]
    errors: list[str] = []
    expected_sets = {
        "upstream_snapshot",
        "guide_supplement",
        "strict_runtime_map",
        "adjacent_control_planes",
    }
    sets = data.get("sets")
    if not isinstance(sets, dict) or set(sets) != expected_sets:
        return ["catalog must contain exactly the four canonical sets"]
    upstream = sets["upstream_snapshot"]
    if not isinstance(upstream, dict):
        return ["upstream_snapshot must be an object"]
    projects = upstream.get("projects", [])
    categories = upstream.get("categories", [])
    if len(projects) != UPSTREAM_PROJECT_COUNT:
        errors.append("upstream_snapshot must contain exactly 160 projects")
    if len(categories) != UPSTREAM_CATEGORY_COUNT:
        errors.append("upstream_snapshot must contain exactly 12 categories")
    if upstream.get("commit") != PINNED_UPSTREAM_COMMIT:
        errors.append("upstream_snapshot commit is invalid")
    if upstream.get("license") != "CC-BY-SA-4.0":
        errors.append("upstream_snapshot license is missing or invalid")
    ids = [record.get("id") for record in projects if isinstance(record, dict)]
    folded_ids = [identifier.casefold() for identifier in ids if isinstance(identifier, str)]
    duplicates = sorted(identifier for identifier in set(folded_ids) if folded_ids.count(identifier) > 1)
    errors.extend(f"duplicate project id: {identifier}" for identifier in duplicates)
    category_ids = [category.get("id") for category in categories if isinstance(category, dict)]
    if len(category_ids) != len(set(category_ids)):
        errors.append("duplicate category id")
    category_counts: dict[str, int] = {identifier: 0 for identifier in category_ids}
    for index, record in enumerate(projects):
        errors.extend(f"upstream project {index}: {error}" for error in validate_record(record))
        category = record.get("category") if isinstance(record, dict) else None
        if category not in category_counts:
            errors.append(f"upstream project {index}: unknown category")
        else:
            category_counts[category] += 1
    for category in categories:
        if isinstance(category, dict) and category.get("count") != category_counts.get(category.get("id")):
            errors.append(f"category count mismatch: {category.get('id')}")
    supplements = sets["guide_supplement"]
    if not isinstance(supplements, list):
        errors.append("guide_supplement must be an array")
        supplements = []
    if len(supplements) != 32:
        errors.append("guide_supplement must contain exactly 32 projects")
    supplement_ids = [record.get("id") for record in supplements if isinstance(record, dict)]
    folded_supplement_ids = [
        identifier.casefold() for identifier in supplement_ids if isinstance(identifier, str)
    ]
    if len(folded_supplement_ids) != len(set(folded_supplement_ids)):
        errors.append("duplicate guide_supplement project id")
    cross_ids = folded_ids + folded_supplement_ids
    if len(cross_ids) != len(set(cross_ids)):
        errors.append("duplicate project id across canonical sets")
    for index, record in enumerate(supplements):
        errors.extend(f"guide supplement {index}: {error}" for error in validate_record(record))
    known_refs = set(ids) | set(supplement_ids)
    projects_by_id = {
        record["id"]: record
        for record in [*projects, *supplements]
        if isinstance(record, dict) and isinstance(record.get("id"), str)
    }
    map_project_refs: dict[str, set[str]] = {}
    for label in ("strict_runtime_map", "adjacent_control_planes"):
        records = sets[label]
        if not isinstance(records, list):
            errors.append(f"{label} must be an array")
            continue
        expected_count = 42 if label == "strict_runtime_map" else 15
        if len(records) != expected_count:
            errors.append(f"{label} must contain exactly {expected_count} entries")
        map_ids = [record.get("id") for record in records if isinstance(record, dict)]
        if len(map_ids) != len(set(map_ids)):
            errors.append(f"duplicate {label} id")
        references = [
            record.get("project_ref", "").casefold()
            for record in records
            if isinstance(record, dict) and isinstance(record.get("project_ref"), str)
        ]
        if len(references) != len(set(references)):
            errors.append(f"duplicate project_ref within {label}")
        map_project_refs[label] = set(references)
        for record in records:
            errors.extend(_validate_map_record(record, known_refs, label))
            if isinstance(record, dict):
                reference = record.get("project_ref")
                declared_set = record.get("source_set")
                if reference in set(ids) and declared_set != "upstream_snapshot":
                    errors.append(f"{label} source_set does not match upstream project {reference}")
                if reference in set(supplement_ids) and declared_set != "guide_supplement":
                    errors.append(f"{label} source_set does not match guide supplement {reference}")
                if label == "strict_runtime_map":
                    referenced_project = projects_by_id.get(reference)
                    if referenced_project is not None and not referenced_project.get("interfaces"):
                        errors.append("strict_runtime_map requires at least one project interface")
                    if record.get("owns_loop") == "no":
                        errors.append("strict_runtime_map cannot contain owns_loop=no")
                    elif record.get("owns_loop") not in {"confirmed", "claimed"}:
                        errors.append(
                            "strict_runtime_map requires owns_loop confirmed or claimed"
                        )
                    if (
                        record.get("owns_loop") == "confirmed"
                        and record.get("evidence_status") != "confirmed"
                    ):
                        errors.append(
                            "strict_runtime_map owns_loop=confirmed requires "
                            "evidence_status=confirmed"
                        )
                if label == "adjacent_control_planes" and record.get("owns_loop") != "no":
                    errors.append("adjacent_control_planes requires owns_loop=no")
    if map_project_refs.get("strict_runtime_map", set()) & map_project_refs.get(
        "adjacent_control_planes", set()
    ):
        errors.append("project_ref appears in multiple maps")
    stats = data.get("stats")
    if not isinstance(stats, dict):
        errors.append("catalog stats are required")
    else:
        expected_stats = {
            "upstream_project_count": len(projects),
            "upstream_category_count": len(categories),
            "guide_supplement_count": len(supplements),
            "strict_runtime_count": len(sets["strict_runtime_map"]),
            "adjacent_control_plane_count": len(sets["adjacent_control_planes"]),
        }
        for key, value in expected_stats.items():
            if stats.get(key) != value:
                errors.append(f"stats mismatch: {key}")
    meta = data.get("_meta")
    if not isinstance(meta, dict) or not meta.get("provenance") or not meta.get("license"):
        errors.append("catalog license and provenance are required")
    if isinstance(meta, dict):
        checksum = meta.get("dataset_sha256")
        without_checksum = json.loads(json.dumps(data))
        without_checksum.get("_meta", {}).pop("dataset_sha256", None)
        expected = hashlib.sha256(serialize_catalog(without_checksum).encode()).hexdigest()
        if checksum != expected:
            errors.append("catalog checksum is invalid")
    return errors


def build_evidence_url(
    repo_url: str, commit: str, path: str, start: int, end: int
) -> str:
    if not _is_github_repository(repo_url):
        raise ValueError("repo_url must be a canonical GitHub repository URL")
    if not COMMIT_RE.match(commit):
        raise ValueError("commit must contain 40 hexadecimal characters")
    if path.startswith("/") or ".." in Path(path).parts:
        raise ValueError("path must be repository-relative")
    if start < 1 or end < start:
        raise ValueError("invalid line range")
    return f"{repo_url}/blob/{commit}/{path}#L{start}-L{end}"


def _upstream_evidence(status: str = "claimed") -> dict[str, str]:
    return {
        "source_type": "upstream_catalog",
        "status": status,
        "url": (
            "https://github.com/RyanAlberts/best-of-Agent-Harnesses/"
            f"blob/{PINNED_UPSTREAM_COMMIT}/harnesses.json"
        ),
        "checked_at": "2026-08-23",
    }


def _normalize_tier(value: str) -> str:
    return value.replace(" ", "_").replace("-", "_")


def _normalize_runtime_value(value: str) -> str:
    if value == "n/a":
        return "not_applicable"
    return value.replace("-", "_")


def _normalize_license(value: str) -> str:
    if value == "open-source":
        return "open_source"
    if value == "unknown":
        return "unknown"
    return value


def _normalize_features(project: dict[str, Any]) -> dict[str, Any]:
    deep_dive = project.get("deep_dive")
    if not isinstance(deep_dive, dict):
        return {}
    features: dict[str, Any] = {}
    for source_name, target_name in (
        ("tooling_sandboxing", "sandboxing"),
        ("context_memory", "memory"),
        ("lifecycle_hooks", "lifecycle_hooks"),
        ("prompt_optimization", "prompt_optimization"),
        ("build_vs_buy", "build_vs_buy"),
    ):
        source = deep_dive.get(source_name)
        if not isinstance(source, dict):
            continue
        value = source.get("rating", source.get("label", "unknown"))
        features[target_name] = {
            "value": value,
            "status": "claimed",
            "evidence": [_upstream_evidence()],
        }
    return features


def _normalize_override_project(project: dict[str, Any]) -> dict[str, Any]:
    evidence_status = project["evidence_status"]
    evidence = {
        "source_type": project.get("source_type", "official_documentation"),
        "status": evidence_status,
        "url": project["evidence_url"],
        "checked_at": project["checked_at"],
    }
    return {
        "id": project["id"],
        "name": project["name"],
        "project_url": project["project_url"],
        "repository_url": project.get("repository_url"),
        "homepage_url": project.get("homepage_url"),
        "category": project["category"],
        "summary": project["summary"],
        "owns_loop": project["owns_loop"],
        "stars": project.get("stars"),
        "stars_captured_at": project.get("stars_captured_at"),
        "license_signal": project["license_signal"],
        "archived": project["archived"],
        "language": project["language"],
        "interfaces": sorted(set(project.get("interfaces", []))),
        "provider_strategy": project.get("provider_strategy", "unknown"),
        "tags": sorted(set(project.get("tags", []))),
        "adoption_surface": project.get("adoption_surface", "unknown"),
        "autonomy": project.get("autonomy", "unknown"),
        "recovery": project.get("recovery", "unknown"),
        "features": {},
        "freshness": {
            "source_commit": project.get("source_commit"),
            "checked_at": project["checked_at"],
        },
        "provenance": [evidence],
    }


def _normalize_map_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": entry["id"],
        "project_ref": entry["project_ref"],
        "source_set": entry["source_set"],
        "owns_loop": entry["owns_loop"],
        "evidence_status": entry["evidence_status"],
        "evidence": [{
            "source_type": entry.get("source_type", "official_documentation"),
            "status": entry["evidence_status"],
            "url": entry["evidence_url"],
            "checked_at": entry["checked_at"],
        }],
    }


def _normalize_upstream_project(project: dict[str, Any], captured_at: str) -> dict[str, Any]:
    tags = sorted(set(project.get("tags", [])))
    return {
        "id": project["github_id"],
        "name": project["name"],
        "project_url": project["url"],
        "repository_url": project["url"],
        "homepage_url": None,
        "category": project["category"],
        "summary": project["description"],
        "owns_loop": "unknown",
        "stars": project["stars"],
        "stars_captured_at": captured_at,
        "license_signal": _normalize_license(project["license_signal"]),
        "archived": "unknown",
        "language": "unknown",
        "interfaces": sorted({INTERFACE_TAG_MAP[tag] for tag in tags if tag in INTERFACE_TAG_MAP}),
        "provider_strategy": "unknown",
        "tags": tags,
        "adoption_surface": _normalize_tier(project["tier"]),
        "autonomy": _normalize_runtime_value(project["autonomy"]),
        "recovery": _normalize_runtime_value(project["recovery"]),
        "features": _normalize_features(project),
        "freshness": {
            "source_commit": PINNED_UPSTREAM_COMMIT,
            "checked_at": captured_at,
        },
        "provenance": [_upstream_evidence()],
    }


def _apply_upstream_project_override(
    record: dict[str, Any], override: dict[str, Any]
) -> dict[str, Any]:
    allowed = {"id", "interfaces", "source_commit", "source_type", "evidence_url", "checked_at"}
    extra = sorted(set(override) - allowed)
    if extra:
        raise ValueError(f"upstream project override has unknown fields: {', '.join(extra)}")
    if override.get("id") != record["id"]:
        raise ValueError("upstream project override id mismatch")
    interfaces = override.get("interfaces")
    if not isinstance(interfaces, list) or not interfaces:
        raise ValueError("upstream project override interfaces must be a non-empty array")
    record["interfaces"] = sorted(set(interfaces))
    record["freshness"] = {
        "source_commit": override["source_commit"],
        "checked_at": override["checked_at"],
    }
    record["provenance"].append({
        "source_type": override.get("source_type", "readme"),
        "status": "confirmed",
        "url": override["evidence_url"],
        "checked_at": override["checked_at"],
    })
    return record


def build_catalog(source: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    meta = source.get("meta", {})
    projects = source.get("projects", [])
    categories = source.get("categories", [])
    if meta.get("project_count") != UPSTREAM_PROJECT_COUNT or len(projects) != UPSTREAM_PROJECT_COUNT:
        raise ValueError("upstream snapshot must contain exactly 160 projects")
    if len(categories) != UPSTREAM_CATEGORY_COUNT:
        raise ValueError("upstream snapshot must contain exactly 12 categories")
    if meta.get("license") != "CC-BY-SA-4.0":
        raise ValueError("upstream snapshot license is missing or invalid")
    captured_at = meta.get("stars_captured")
    if not isinstance(captured_at, str) or not DATE_RE.match(captured_at):
        raise ValueError("upstream stars_captured date is missing or invalid")
    normalized_projects = sorted(
        (_normalize_upstream_project(project, captured_at) for project in projects),
        key=lambda project: project["id"].casefold(),
    )
    upstream_overrides = overrides.get("upstream_project_overrides", [])
    if not isinstance(upstream_overrides, list):
        raise ValueError("upstream_project_overrides must be an array")
    overrides_by_id = {item["id"]: item for item in upstream_overrides}
    if len(overrides_by_id) != len(upstream_overrides):
        raise ValueError("upstream_project_overrides ids must be unique")
    known_upstream_ids = {project["id"] for project in normalized_projects}
    unknown_override_ids = sorted(set(overrides_by_id) - known_upstream_ids)
    if unknown_override_ids:
        raise ValueError(
            "upstream_project_overrides reference unknown projects: "
            + ", ".join(unknown_override_ids)
        )
    normalized_projects = [
        _apply_upstream_project_override(project, overrides_by_id[project["id"]])
        if project["id"] in overrides_by_id
        else project
        for project in normalized_projects
    ]
    counts: dict[str, int] = {}
    for project in normalized_projects:
        counts[project["category"]] = counts.get(project["category"], 0) + 1
    normalized_categories = sorted(
        (
            {
                "id": category["id"],
                "title": category["title"],
                "summary": category["subtitle"],
                "count": counts.get(category["id"], 0),
            }
            for category in categories
        ),
        key=lambda category: category["id"],
    )
    pinned_stats = {
        "open_source_count": (
            sum(project["license_signal"] == "open_source" for project in normalized_projects),
            118,
        ),
        "deep_dive_count": (sum(bool(project["features"]) for project in normalized_projects), 86),
        "headless_count": (sum(project["autonomy"] == "headless" for project in normalized_projects), 46),
        "durable_count": (sum(project["recovery"] == "durable" for project in normalized_projects), 8),
        "autonomy_not_applicable_count": (
            sum(project["autonomy"] == "not_applicable" for project in normalized_projects),
            65,
        ),
        "recovery_not_applicable_count": (
            sum(project["recovery"] == "not_applicable" for project in normalized_projects),
            64,
        ),
    }
    for name, (actual, expected) in pinned_stats.items():
        if actual != expected:
            raise ValueError(f"{name} drifted from {expected} to {actual}")
    supplement_defaults = overrides.get("guide_supplement_defaults", {})
    supplements = sorted(
        (
            _normalize_override_project({**supplement_defaults, **item})
            for item in overrides.get("guide_supplement", [])
        ),
        key=lambda item: item["id"].casefold(),
    )
    map_defaults = overrides.get("map_defaults", {})
    strict = sorted(
        (_normalize_map_entry({**map_defaults, **item}) for item in overrides.get("strict_runtime_map", [])),
        key=lambda item: item["id"].casefold(),
    )
    adjacent = sorted(
        (
            _normalize_map_entry({**map_defaults, **item})
            for item in overrides.get("adjacent_control_planes", [])
        ),
        key=lambda item: item["id"].casefold(),
    )
    catalog: dict[str, Any] = {
        "_meta": {
            "schema_version": "1.0.0",
            "generated_at": overrides.get("generated_at", "2026-08-28T00:00:00Z"),
            "license": "CC-BY-SA-4.0 for upstream-derived records; project metadata retains its source terms",
            "provenance": {
                "upstream_repository": "https://github.com/RyanAlberts/best-of-Agent-Harnesses",
                "upstream_commit": PINNED_UPSTREAM_COMMIT,
                "upstream_snapshot_date": captured_at,
                "methodology": "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/docs/superpowers/specs/2026-08-27-agent-harness-landscape-enrichment-design.md",
            },
        },
        "stats": {
            "upstream_project_count": len(normalized_projects),
            "upstream_category_count": len(normalized_categories),
            "guide_supplement_count": len(supplements),
            "strict_runtime_count": len(strict),
            "adjacent_control_plane_count": len(adjacent),
            **{name: actual for name, (actual, _expected) in pinned_stats.items()},
        },
        "sets": {
            "upstream_snapshot": {
                "repository": "https://github.com/RyanAlberts/best-of-Agent-Harnesses",
                "commit": PINNED_UPSTREAM_COMMIT,
                "snapshot_date": captured_at,
                "license": "CC-BY-SA-4.0",
                "categories": normalized_categories,
                "projects": normalized_projects,
            },
            "guide_supplement": supplements,
            "strict_runtime_map": strict,
            "adjacent_control_planes": adjacent,
        },
    }
    checksum_source = json.loads(json.dumps(catalog))
    catalog["_meta"]["dataset_sha256"] = hashlib.sha256(
        serialize_catalog(checksum_source).encode()
    ).hexdigest()
    errors = validate_catalog(catalog)
    if errors:
        raise ValueError("catalog validation failed:\n- " + "\n- ".join(errors))
    return catalog
