#!/usr/bin/env python3
"""Render deterministic regions in the Agent Harness Landscape page."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MARKERS = (
    "category-summary",
    "strict-runtime-map",
    "adjacent-control-planes",
    "project-catalog",
)

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
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog = load_json(args.catalog)
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
