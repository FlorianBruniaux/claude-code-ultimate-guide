#!/usr/bin/env python3
"""Validate the AI design patterns dataset and render its generated guide blocks.

The dataset in machine-readable/ai-design-patterns.json is the single source for
the crosswalk tables of guide/core/ai-design-patterns.md, the landing page, and
the MCP resource. This script checks referential integrity, rewrites the blocks
between the GENERATED markers of the guide page, and mirrors the dataset into
mcp-server/content/. With --check it writes nothing and exits 1 on any drift.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "machine-readable/ai-design-patterns.json"
MIRROR_PATH = ROOT / "mcp-server/content/ai-design-patterns.json"
PAGE_PATH = ROOT / "guide/core/ai-design-patterns.md"

CONSENSUS_LABELS = {
    "consensus": "Consensus",
    "single-source": "Single source",
    "divergent": "Divergent",
}
PROVENANCE_LABELS = {
    "third-party": "Named by a source",
    "own-synthesis": "Our mapping",
}
RELATED_KINDS = {
    "guide": "guide",
    "template": "template",
    "project": "author's project",
    "article": "author's article",
}
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
EM_DASH = "—"


def slugify(text: str) -> str:
    """GitHub-style heading slug, as used by the guide reader and the landing."""
    slug = text.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    return re.sub(r"\s", "-", slug)


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    source_ids = [s["id"] for s in data["sources"]]
    known_sources = set(source_ids)
    sources_by_id = {s["id"]: s for s in data["sources"]}
    family_ids = {f["id"] for f in data["families"]}
    category_ids = {c["id"] for c in data["anti_pattern_categories"]}
    pattern_ids: list[str] = []

    if len(known_sources) != len(source_ids):
        errors.append("duplicate source id")
    if data.get("last_updated", "") < data["last_verified"]:
        errors.append("last_updated must be on or after last_verified")

    def check_refs(owner: str, refs: list[str]) -> None:
        if not refs:
            errors.append(f"{owner}: no source")
        for ref in refs:
            if ref not in known_sources:
                errors.append(f"{owner}: unknown source {ref!r}")

    def check_media(owner: str, row: dict) -> None:
        infographic = row.get("infographic")
        if infographic:
            expected = f"guide/images/ai-design-patterns/patterns/{row['id']}.webp"
            if infographic["file"] != expected:
                errors.append(f"{owner}: infographic must be {expected}")
            elif not (ROOT / infographic["file"]).is_file():
                errors.append(f"{owner}: missing infographic {infographic['file']}")
        for video in row.get("videos", []):
            source = sources_by_id.get(video["source"])
            if source is None or source["kind"] != "video":
                errors.append(f"{owner}: video {video['source']!r} is not a video source")

    def check_related(owner: str, row: dict) -> None:
        for item in row.get("related", []):
            kind = item.get("kind")
            if kind not in RELATED_KINDS:
                errors.append(f"{owner}: unknown related kind {kind!r}")
            elif kind in ("guide", "template"):
                path, _, anchor = item.get("path", "").partition("#")
                target = ROOT / path
                if not path or not target.is_file():
                    errors.append(f"{owner}: related path not found {item.get('path')!r}")
                elif anchor and anchor not in heading_slugs(target):
                    errors.append(f"{owner}: related anchor not found {item['path']!r}")
            elif not item.get("url", "").startswith("https://"):
                errors.append(f"{owner}: related {kind} needs an https url")
            image = item.get("image")
            if image and not (ROOT / image["file"]).is_file():
                errors.append(f"{owner}: missing related image {image['file']}")

    def check_mechanisms(owner: str, mechanisms: list[dict]) -> None:
        if not mechanisms:
            errors.append(f"{owner}: no Claude Code mechanism")
        for mechanism in mechanisms:
            if not mechanism["doc"].startswith("https://code.claude.com/docs/"):
                errors.append(f"{owner}: mechanism doc is not official: {mechanism['doc']}")

    for row in data["crosswalk"]:
        owner = f"crosswalk {row['id']}"
        pattern_ids.append(row["id"])
        if row["id"] != slugify(row["classic"]):
            errors.append(f"{owner}: id must equal the heading slug {slugify(row['classic'])!r}")
        if row["family"] not in family_ids:
            errors.append(f"{owner}: unknown family {row['family']!r}")
        if row["consensus"] not in CONSENSUS_LABELS:
            errors.append(f"{owner}: unknown consensus {row['consensus']!r}")
        if row["provenance"] not in PROVENANCE_LABELS:
            errors.append(f"{owner}: unknown provenance {row['provenance']!r}")
        check_mechanisms(owner, row["claude_code"])
        check_refs(owner, row["sources"])
        check_media(owner, row)
        check_related(owner, row)
        analogue_sources = []
        for analogue in row["agent_analogue"]:
            check_refs(owner, analogue["sources"])
            analogue_sources.extend(analogue["sources"])
            for ref in analogue["sources"]:
                if ref not in row["sources"]:
                    errors.append(f"{owner}: analogue source {ref!r} missing from row sources")
        distinct = set(analogue_sources)
        if row["consensus"] == "divergent":
            if len(row["agent_analogue"]) < 2:
                errors.append(f"{owner}: divergent row needs 2+ analogues")
            firsts = {tuple(a["sources"]) for a in row["agent_analogue"]}
            if len(firsts) < 2:
                errors.append(f"{owner}: divergent analogues need distinct sources")
        first = set(row["agent_analogue"][0]["sources"])
        if row["consensus"] == "consensus" and len(first) < 2:
            errors.append(f"{owner}: consensus row needs 2+ sources on its main analogue")
        if row["consensus"] == "single-source" and len(distinct) != 1:
            errors.append(f"{owner}: single-source row must cite exactly one analogue source")

    for row in data["native"]:
        owner = f"native {row['id']}"
        pattern_ids.append(row["id"])
        if row["id"] != slugify(row["name"]):
            errors.append(f"{owner}: id must equal the heading slug {slugify(row['name'])!r}")
        check_mechanisms(owner, row["claude_code"])
        check_refs(owner, row["sources"])
        check_media(owner, row)
        check_related(owner, row)

    known_patterns = set(pattern_ids)
    if len(known_patterns) != len(pattern_ids):
        errors.append("duplicate pattern id across crosswalk and native")

    for row in data["anti_patterns"]:
        owner = f"anti-pattern {row['id']}"
        if row["id"] != slugify(row["name"]):
            errors.append(f"{owner}: id must equal the heading slug {slugify(row['name'])!r}")
        if row["category"] not in category_ids:
            errors.append(f"{owner}: unknown category {row['category']!r}")
        for ref in row["patterns"]:
            if ref not in known_patterns:
                errors.append(f"{owner}: unknown pattern {ref!r}")
        check_refs(owner, row["sources"])

    for item in data.get("further_reading", []):
        check_refs(f"further reading {item['source']}", [item["source"]])
        for ref in item["patterns"]:
            if ref not in known_patterns:
                errors.append(f"further reading {item['source']}: unknown pattern {ref!r}")

    for ref in [c["source"] for c in data["anti_pattern_categories"] if c["source"]]:
        if ref not in known_sources:
            errors.append(f"anti-pattern category: unknown source {ref!r}")

    for item in iter_strings(data):
        if EM_DASH in item:
            errors.append(f"em dash in {item[:60]!r}")

    for value in source_ids + pattern_ids:
        if not ID_RE.match(value):
            errors.append(f"id {value!r} is not kebab-case")
    return errors


def heading_slugs(path: Path) -> set[str]:
    slugs: set[str] = set()
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
        heading = None if in_fence else re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            slugs.add(slugify(heading.group(1)))
    return slugs


def iter_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)


def cell(text: str) -> str:
    return text.replace("|", "\\|")


class Renderer:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.sources = {s["id"]: s for s in data["sources"]}
        self.families = {f["id"]: f["label"] for f in data["families"]}
        self.categories = {c["id"]: c["label"] for c in data["anti_pattern_categories"]}
        self.titles = {r["id"]: r["classic"] for r in data["crosswalk"]}
        self.titles.update({r["id"]: r["name"] for r in data["native"]})

    def label(self, ref: str) -> str:
        source = self.sources[ref]
        return f"{source['author']}: {source['title']}" if source["kind"] == "official" else source["author"]

    def cite(self, refs: list[str]) -> str:
        return ", ".join(f"[{self.label(r)}]({self.sources[r]['url']})" for r in refs)

    def mechanisms(self, mechanisms: list[dict]) -> str:
        return "; ".join(f"[{m['name']}]({m['doc']})" for m in mechanisms)

    def infographic(self, row: dict) -> list[str]:
        if "infographic" not in row:
            return []
        image = row["infographic"]
        return [f"![{image['alt']}](../{image['file'].removeprefix('guide/')})", ""]

    def related(self, row: dict) -> list[str]:
        links = []
        for item in row.get("related", []):
            if "path" in item:
                path, _, anchor = item["path"].partition("#")
                href = os.path.relpath(ROOT / path, PAGE_PATH.parent) + (f"#{anchor}" if anchor else "")
            else:
                href = item["url"]
            links.append(f"[{item['title']}]({href}) ({RELATED_KINDS[item['kind']]})")
        return [f"- **Go further:** {'; '.join(links)}"] if links else []

    def related_images(self, row: dict) -> list[str]:
        lines = []
        for item in row.get("related", []):
            if "image" in item:
                image = item["image"]
                lines += ["", f"![{image['alt']}](../{image['file'].removeprefix('guide/')})"]
        return lines

    def videos(self, row: dict) -> list[str]:
        lines = []
        for video in row.get("videos", []):
            source = self.sources[video["source"]]
            minutes, seconds = divmod(video["t"], 60)
            lines.append(
                f"- **Watch:** {source['author']}, [{source['title']}]({source['url']}&t={video['t']}s) "
                f"at {minutes}:{seconds:02d}: {video['point']}"
            )
        return lines

    def crosswalk_table(self) -> str:
        lines = [
            "| Classic pattern | Family | Agent analogue | In Claude Code | Evidence | Mapping |",
            "|---|---|---|---|---|---|",
        ]
        for row in self.data["crosswalk"]:
            analogue = " / ".join(a["label"] for a in row["agent_analogue"])
            mechanisms = "; ".join(m["name"] for m in row["claude_code"])
            lines.append(
                f"| [{row['classic']}](#{row['id']}) | {self.families[row['family']]} | {cell(analogue)} "
                f"| {cell(mechanisms)} | {CONSENSUS_LABELS[row['consensus']]} | {PROVENANCE_LABELS[row['provenance']]} |"
            )
        return "\n".join(lines)

    def pattern_cards(self) -> str:
        blocks = []
        for family_id, family_label in self.families.items():
            rows = [r for r in self.data["crosswalk"] if r["family"] == family_id]
            if not rows:
                continue
            for row in rows:
                analogues = "\n".join(
                    f"  - {a['label']} ({self.cite(a['sources'])})" for a in row["agent_analogue"]
                )
                if len(row["agent_analogue"]) == 1:
                    first = row["agent_analogue"][0]
                    analogue_block = f"- **Agent side:** {first['label']} ({self.cite(first['sources'])})"
                elif row["consensus"] == "divergent":
                    analogue_block = f"- **Agent side, sources disagree:**\n{analogues}"
                else:
                    analogue_block = f"- **Agent side, main reading first:**\n{analogues}"
                blocks.append(
                    "\n".join(
                        [
                            f"### {row['classic']}",
                            "",
                            f"`{family_label}` `{CONSENSUS_LABELS[row['consensus']]}` `{PROVENANCE_LABELS[row['provenance']]}`",
                            "",
                            *self.infographic(row),
                            f"- **Classic intent:** {row['classic_intent']}",
                            analogue_block,
                            f"- **In Claude Code:** {self.mechanisms(row['claude_code'])}",
                            f"- **Failure mode:** {row['failure_mode']}",
                            f"- **How to verify:** {row['verify']}",
                            *self.related(row),
                            *self.videos(row),
                            *self.related_images(row),
                        ]
                    )
                )
        return "\n\n".join(blocks)

    def native_cards(self) -> str:
        blocks = []
        for row in self.data["native"]:
            blocks.append(
                "\n".join(
                    [
                        f"### {row['name']}",
                        "",
                        *self.infographic(row),
                        row["summary"],
                        "",
                        f"- **What is new:** {row['why_new']}",
                        f"- **In Claude Code:** {self.mechanisms(row['claude_code'])}",
                        f"- **Sources:** {self.cite(row['sources'])}",
                        *self.related(row),
                        *self.videos(row),
                        *self.related_images(row),
                    ]
                )
            )
        return "\n\n".join(blocks)

    def anti_patterns_table(self) -> str:
        lines = [
            "| Anti-pattern | Symptom | Fix | Category | Related patterns |",
            "|---|---|---|---|---|",
        ]
        for row in self.data["anti_patterns"]:
            related = ", ".join(f"[{self.titles[p]}](#{p})" for p in row["patterns"])
            lines.append(
                f"| **{row['name']}** | {cell(row['symptom'])} | {cell(row['fix'])} "
                f"| {self.categories[row['category']]} | {related} |"
            )
        return "\n".join(lines)

    def further_reading(self) -> str:
        lines = []
        for item in self.data.get("further_reading", []):
            source = self.sources[item["source"]]
            related = ", ".join(f"[{self.titles[p]}](#{p})" for p in item["patterns"])
            lines.append(f"- {source['author']}, [{source['title']}]({source['url']}): {item['note']} Related: {related}.")
        return "\n".join(lines)

    def sources_list(self) -> str:
        groups = [
            ("Crosswalks and catalogs", {"crosswalk", "catalog"}),
            ("Papers", {"paper"}),
            ("Vendor guidance and articles", {"vendor", "article"}),
            ("Talks", {"video"}),
            ("Classic references", {"classic"}),
            ("Claude Code documentation", {"official"}),
        ]
        out = []
        for title, kinds in groups:
            items = [s for s in self.data["sources"] if s["kind"] in kinds]
            if not items:
                continue
            out.append(f"**{title}**")
            out.append("")
            out.extend(f"- {s['author']}, [{s['title']}]({s['url']})" for s in items)
            out.append("")
        return "\n".join(out).rstrip()

    def blocks(self) -> dict[str, str]:
        return {
            "crosswalk-table": self.crosswalk_table(),
            "pattern-cards": self.pattern_cards(),
            "native-cards": self.native_cards(),
            "anti-patterns-table": self.anti_patterns_table(),
            "further-reading": self.further_reading(),
            "sources": self.sources_list(),
        }


def replace_blocks(page: str, blocks: dict[str, str]) -> str:
    for marker, body in blocks.items():
        begin = f"<!-- BEGIN GENERATED: {marker} -->"
        end = f"<!-- END GENERATED: {marker} -->"
        pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
        if not pattern.search(page):
            raise SystemExit(f"marker {marker!r} not found in {PAGE_PATH.relative_to(ROOT)}")
        page = pattern.sub(lambda _: f"{begin}\n\n{body}\n\n{end}", page)
    return page


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail on drift instead of writing")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw = DATASET_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    page = PAGE_PATH.read_text(encoding="utf-8")
    rendered = replace_blocks(page, Renderer(data).blocks())
    mirror = MIRROR_PATH.read_text(encoding="utf-8") if MIRROR_PATH.exists() else None

    if args.check:
        drift = []
        if rendered != page:
            drift.append(str(PAGE_PATH.relative_to(ROOT)))
        if mirror != raw:
            drift.append(str(MIRROR_PATH.relative_to(ROOT)))
        if drift:
            print("out of date, run scripts/build-ai-design-patterns.py: " + ", ".join(drift), file=sys.stderr)
            return 1
        print(f"ai-design-patterns: {len(data['crosswalk'])} crosswalk rows, {len(data['native'])} native, {len(data['anti_patterns'])} anti-patterns, up to date")
        return 0

    PAGE_PATH.write_text(rendered, encoding="utf-8")
    MIRROR_PATH.write_text(raw, encoding="utf-8")
    print(f"wrote {PAGE_PATH.relative_to(ROOT)} and {MIRROR_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
