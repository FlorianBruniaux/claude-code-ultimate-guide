#!/usr/bin/env python3
"""
generate-examples-data.py — regenerate landing/src/data/examples-data.ts from examples/.

Reads every template file in examples/, extracts descriptions from frontmatter,
and emits a TypeScript file matching the ExamplesData interface. Preserves
existing favorite: true flags and curated descriptions from the current file.

Usage:
    python3 scripts/generate-examples-data.py              # emit to stdout
    python3 scripts/generate-examples-data.py --write       # overwrite examples-data.ts
    python3 scripts/generate-examples-data.py --check       # exit 1 if file would change
    python3 scripts/generate-examples-data.py --diff        # print unified diff

Paths (configurable at top of file):
    EXAMPLES_DIR  — guide repo examples/
    OUTPUT_FILE   — landing src/data/examples-data.ts
"""

import os
import re
import sys
import json
import difflib
import yaml
from pathlib import Path
from datetime import date
from typing import Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
LANDING_ROOT = REPO_ROOT.parent / "claude-code-ultimate-guide-landing"
OUTPUT_FILE = LANDING_ROOT / "src" / "data" / "examples-data.ts"

# ---------------------------------------------------------------------------
# Category configuration — order and display metadata
# ---------------------------------------------------------------------------
CATEGORIES = [
    {
        "key": "agents",
        "icon": "🤖",
        "description": "Custom AI personas for specialized tasks. Place in .claude/agents/ or ~/.claude/agents/",
        "path": "agents",
        "extensions": {".md"},
        "exclude_names": {"README.md", "index.md"},
        "mode": "flat_md",
    },
    {
        "key": "skills",
        "icon": "📚",
        "description": "Reusable knowledge modules. Place in .claude/skills/ or ~/.claude/skills/",
        "path": "skills",
        "extensions": {".md"},
        "exclude_names": {"README.md", "index.md"},
        "mode": "skills",
    },
    {
        "key": "commands",
        "icon": "⚡",
        "label": "User-Invocable Skills",
        "description": "Custom slash commands (user-invocable skills). Place in .claude/skills/ with disable-model-invocation: true",
        "path": "commands",
        "extensions": {".md", ".yaml", ".yml", ".json"},
        "exclude_names": {"README.md", "index.md"},
        "mode": "flat_md",
    },
    {
        "key": "hooks-bash",
        "icon": "🔒",
        "label": "Hooks (Bash)",
        "description": "Event-driven automation scripts for macOS/Linux. Place in .claude/hooks/",
        "path": "hooks/bash",
        "extensions": {".sh"},
        "exclude_names": set(),
        "mode": "flat_md",
    },
    {
        "key": "hooks-powershell",
        "icon": "🪟",
        "label": "Hooks (PowerShell)",
        "description": "Event-driven automation scripts for Windows",
        "path": "hooks/powershell",
        "extensions": {".ps1"},
        "exclude_names": set(),
        "mode": "flat_md",
    },
    {
        "key": "config",
        "icon": "⚙️",
        "description": "Configuration file templates. Place in .claude/ or ~/.claude/",
        "path": "config",
        "extensions": {".json", ".md", ".yaml", ".yml"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "memory",
        "icon": "🧠",
        "description": "CLAUDE.md memory file templates for persistent context",
        "path": "memory",
        "extensions": {".md"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "claude-md",
        "icon": "📄",
        "label": "CLAUDE.md Configs",
        "description": "Ready-to-use CLAUDE.md configuration profiles. Add to ~/.claude/CLAUDE.md or project CLAUDE.md",
        "path": "claude-md",
        "extensions": {".md"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "rules",
        "icon": "📋",
        "label": "Rules",
        "description": "Behavioral rules auto-loaded by Claude for common review patterns. Place in .claude/rules/",
        "path": "rules",
        "extensions": {".md"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "scripts",
        "icon": "🛠️",
        "description": "Utility scripts for setup, diagnostics, and monitoring",
        "path": "scripts",
        "extensions": {".sh", ".ps1", ".py", ".ts", ".md", ".yaml", ".yml", ".json"},
        "exclude_names": {"README.md", "index.md"},
        "mode": "flat_md",
    },
    {
        "key": "team-config",
        "icon": "👥",
        "label": "Team Config",
        "description": "Templates for scaling Claude Code across teams. Place in .claude/",
        "path": "team-config",
        "extensions": {".md", ".yaml", ".ts"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "templates",
        "icon": "📝",
        "label": "Templates",
        "description": "Session and workflow templates for context continuity",
        "path": "templates",
        "extensions": {".md", ".json"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "github-actions",
        "icon": "🚀",
        "label": "GitHub Actions",
        "description": "CI/CD workflows for GitHub Actions automation",
        "path": "github-actions",
        "extensions": {".yml", ".yaml", ".md"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "workflows",
        "icon": "📋",
        "description": "Advanced development workflow guides",
        "path": "workflows",
        "extensions": {".md", ".json"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "plugins",
        "icon": "🧩",
        "description": "Community plugins extending Claude Code capabilities",
        "path": "plugins",
        "extensions": {".md", ".json"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "integrations",
        "icon": "🔌",
        "label": "Integrations",
        "description": "Community integrations and MCP server extensions for Claude Code",
        "path": "integrations",
        "extensions": {".md"},
        "exclude_names": set(),
        "mode": "flat_md",
    },
    {
        "key": "mcp-configs",
        "icon": "🔧",
        "label": "MCP Configs",
        "description": "MCP server configuration files",
        "path": "mcp-configs",
        "extensions": {".json"},
        "exclude_names": set(),
        "mode": "flat_md",
    },
    {
        "key": "modes",
        "icon": "🎭",
        "description": "Behavioral modes for Claude (SuperClaude framework). Place in ~/.claude/",
        "path": "modes",
        "extensions": {".md"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "context-engineering",
        "icon": "🧬",
        "label": "Context Engineering",
        "description": "Templates for structuring Claude's context: code maps, budgets, eval questions, CI drift checks",
        "path": "context-engineering",
        "extensions": {".md", ".yaml", ".yml", ".sh", ".ts"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "styles",
        "icon": "🎨",
        "label": "Styles",
        "description": "Custom style templates for consistent AI output tone and formatting",
        "path": "styles",
        "extensions": {".md"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
    {
        "key": "semantic-anchors",
        "icon": "🔗",
        "label": "Semantic Anchors",
        "description": "Precise vocabulary for better LLM outputs",
        "path": "semantic-anchors",
        "extensions": {".md"},
        "exclude_names": {"README.md"},
        "mode": "flat_md",
    },
]

# Skill collections (multi-file directories) listed as a single pointer entry.
# Format: { relative_path_from_skills_dir: description }
SKILL_COLLECTIONS = {
    "git-ai-archaeology": "Analyze AI config evolution in a git repo: first commits, monthly distribution, maturity phases",
    "design-patterns": "Detect and analyze GoF design patterns",
    "voice-refine": "Writing voice refinement with before/after examples",
    "rtk-optimizer": "RTK token optimization analysis",
    "audit-agents-skills": "Quality audit for agents, skills, and commands",
    "skill-creator": "Create new skills with proper structure and best practices",
    "landing-page-generator": "Generate deploy-ready landing pages from any repository",
    "ccboard": "TUI/Web dashboard for Claude Code session monitoring",
    "guide-recap": "Transform CHANGELOG entries into social content",
    "release-notes-generator": "Generate release notes in 3 formats from git commits",
    "pr-triage": "4-phase PR backlog management with worktree setup",
    "issue-triage": "3-phase issue backlog management",
    "cyber-defense-team": "Multi-agent cyber defense team orchestration",
    "talk-pipeline": "6-stage pipeline: raw material to slides via Kimi",
    "token-audit": "Measure fixed-context token overhead, classify rules by usage frequency, audit hook cost",
    "eval-skills": "Audit all skills for frontmatter completeness and effort-level inference",
    "eval-rules": "Audit .claude/rules/: resolves glob patterns against real files, interactive usefulness review",
    "mcp-integration-reference": "MCP integration reference with Sentry patterns and multi-tool query examples",
    "plan-pipeline": "Complete planning pipeline: product direction to architecture to implementation plan, validation, and execution",
}

# Favorites (path values that should get favorite: true)
FAVORITES = {
    "skills/security-checklist.md",
    "skills/pdf-generator.md",
    "skills/smart-explore.md",
    "skills/eval-rules/SKILL.md",
    "skills/pr-triage/",
    "skills/guide-recap/",
    "skills/eval-agents/SKILL.md",
    "skills/eval-hooks/SKILL.md",
    "skills/commit/SKILL.md",
    "skills/ship/SKILL.md",
    "skills/pr/SKILL.md",
    "skills/ci-all/SKILL.md",
    "skills/land-and-deploy/SKILL.md",
    "skills/handoff-create/SKILL.md",
    "skills/investigate/SKILL.md",
    "skills/scaffold/SKILL.md",
    "agents/code-reviewer.md",
    "agents/planner.md",
    "agents/architecture-reviewer.md",
    "commands/commit.md",
    "commands/pr.md",
    "commands/release-notes.md",
    "commands/git-worktree.md",
    "commands/security-check.md",
    "commands/check-cache-bugs.md",
    "commands/plan-start.md",
    "commands/plan-validate.md",
    "commands/plan-execute.md",
    "commands/autoresearch.md",
    "commands/investigate.md",
    "commands/land-and-deploy.md",
    "commands/scaffold.md",
    "commands/ci/all.md",
    "hooks/bash/dangerous-actions-blocker.sh",
    "hooks/bash/prompt-injection-detector.sh",
    "hooks/bash/auto-rename-session.sh",
    "hooks/bash/smart-suggest.sh",
    "hooks/bash/session-summary.sh",
    "config/sandbox-native.json",
    "claude-md/session-naming.md",
    "rules/first-principles.md",
    "scripts/cc-sessions.py",
    "scripts/smart-suggest-roi.py",
    "github-actions/claude-code-review.yml",
    "context-engineering/skeleton-template.md",
    "semantic-anchors/anchor-catalog.md",
    "modes/MODE_Learning.md",
    "plugins/security-suite/",
}


def extract_frontmatter(filepath: Path):
    """Extract YAML frontmatter and body from a file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return {}, ""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            try:
                fm = yaml.safe_load(content[3:end].strip()) or {}
                return fm, content[end + 3:].strip()
            except yaml.YAMLError:
                pass
    return {}, content


def extract_description(filepath: Path) -> str:
    """Extract a short description from frontmatter or first meaningful line."""
    fm, body = extract_frontmatter(filepath)
    if fm.get("description"):
        return str(fm["description"])[:120]
    # Fallback: first non-heading, non-empty line
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("-") and not line.startswith(">"):
            return line[:120]
    return filepath.stem.replace("-", " ").capitalize()


def scan_skills(skills_dir: Path) -> list[dict]:
    """Scan examples/skills/ and return one entry per skill (folder pointer or standalone .md)."""
    entries = []
    if not skills_dir.exists():
        return entries

    # Collection pointers (multi-file skills)
    for name, desc in SKILL_COLLECTIONS.items():
        skill_path = skills_dir / name
        if not skill_path.exists():
            continue
        # Prefer SKILL.md path if exists, else folder pointer
        skill_md = skill_path / "SKILL.md"
        skill_md_lower = skill_path / "skill.md"
        if skill_md.exists():
            path_val = f"skills/{name}/SKILL.md"
        elif skill_md_lower.exists():
            path_val = f"skills/{name}/"
        else:
            path_val = f"skills/{name}/"
        entries.append({
            "name": f"{name}/",
            "path": path_val,
            "description": desc,
        })

    # Standalone .md skills at the top level of skills/
    collection_names = set(SKILL_COLLECTIONS.keys())
    for f in sorted(skills_dir.iterdir()):
        if f.is_file() and f.suffix == ".md" and f.name not in {"README.md", "index.md"}:
            desc = extract_description(f)
            entries.append({
                "name": f.name,
                "path": f"skills/{f.name}",
                "description": desc,
            })

    # Single-file skills (folder with single SKILL.md, not a multi-file collection)
    for d in sorted(skills_dir.iterdir()):
        if not d.is_dir() or d.name in collection_names:
            continue
        skill_md = d / "SKILL.md"
        skill_md_lower = d / "skill.md"
        actual_md = skill_md if skill_md.exists() else (skill_md_lower if skill_md_lower.exists() else None)
        if actual_md:
            desc = extract_description(actual_md)
            entries.append({
                "name": f"{d.name}/",
                "path": f"skills/{d.name}/{actual_md.name}",
                "description": desc,
            })

    return entries


def scan_category(cat: dict) -> list[dict]:
    """Scan a category directory and return ExampleFile entries."""
    base = EXAMPLES_DIR / cat["path"]
    if not base.exists():
        return []
    entries = []
    exts = cat["extensions"]
    excludes = cat["exclude_names"]

    for f in sorted(base.rglob("*")):
        if not f.is_file():
            continue
        if f.name in excludes:
            continue
        if f.suffix not in exts:
            continue
        rel = f.relative_to(EXAMPLES_DIR)
        path_str = str(rel).replace("\\", "/")
        desc = extract_description(f)
        entries.append({
            "name": f.name if str(rel.parent) == cat["path"] else str(rel.relative_to(cat["path"])),
            "path": path_str,
            "description": desc,
        })
    return entries


def ts_string(s: str) -> str:
    """Escape a string for TypeScript."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def entry_to_ts(e: dict, indent: int = 12) -> str:
    pad = " " * indent
    name = ts_string(e["name"])
    path = ts_string(e["path"])
    desc = ts_string(e["description"])
    fav = ", favorite: true" if e.get("favorite") else ""
    return f'{pad}{{ name: "{name}", path: "{path}", description: "{desc}"{fav} }}'


def build_ts(categories_data: list[dict]) -> str:
    today = date.today().isoformat()
    total = sum(len(c["entries"]) for c in categories_data)
    lines = [
        "/**",
        " * Examples data - Shared across all pages for global search",
        f" * Source of truth for indexed templates ({total} total — auto-generated {today})",
        f" * Last synced: {today}",
        " * Note: collection-internal support files (yamls, assets) use folder-pointer entries",
        " * Generated by: scripts/generate-examples-data.py",
        " */",
        "",
        "export interface ExampleFile {",
        "  readonly name: string;",
        "  readonly path: string;",
        "  readonly description: string;",
        "  readonly favorite?: boolean;",
        "}",
        "",
        "export interface ExampleCategory {",
        "  readonly icon: string;",
        "  readonly label?: string;",
        "  readonly description: string;",
        "  readonly files: readonly ExampleFile[];",
        "}",
        "",
        "export type ExamplesData = Record<string, ExampleCategory>;",
        "",
        "export const EXAMPLES = {",
    ]

    for i, cat in enumerate(categories_data):
        key = cat["key"]
        icon_escaped = cat["icon"].encode("unicode_escape").decode("ascii")
        # Use proper unicode escape for emoji
        icon_ts = _emoji_to_ts(cat["icon"])
        label_line = f'\n        label: "{ts_string(cat["label"])}",\n' if cat.get("label") else "\n"
        desc = ts_string(cat["description"])
        entries = cat["entries"]
        is_last_cat = i == len(categories_data) - 1

        # Keys with a hyphen ("hooks-bash", "claude-md"...) are not valid bare
        # JS identifiers, so they must be quoted or esbuild fails the landing build.
        key_ts = key if key.isidentifier() else f'"{key}"'
        lines.append(f'    {key_ts}: {{')
        lines.append(f'        icon: "{icon_ts}",')
        if cat.get("label"):
            lines.append(f'        label: "{ts_string(cat["label"])}",')
        lines.append(f'        description: "{desc}",')
        lines.append(f'        files: [')
        for j, entry in enumerate(entries):
            comma = "," if j < len(entries) - 1 else ""
            lines.append(entry_to_ts(entry) + comma)
        lines.append(f'        ]')
        cat_comma = "," if not is_last_cat else ""
        lines.append(f'    }}{cat_comma}')

    lines.append("} as const satisfies ExamplesData;")
    lines.append("")
    return "\n".join(lines)


def _emoji_to_ts(emoji: str) -> str:
    """Convert emoji to TypeScript unicode escape or raw string."""
    # For code points > 0xFFFF use \\u{XXXXXX} syntax
    result = []
    for ch in emoji:
        cp = ord(ch)
        if cp > 0xFFFF:
            result.append(f"\\u{{{cp:X}}}")
        elif cp > 0x7E:
            result.append(f"\\u{cp:04X}")
        else:
            result.append(ch)
    return "".join(result)


def load_existing_favorites_and_descriptions(existing_path: Path) -> dict:
    """Parse current examples-data.ts to extract path -> {favorite, description} mapping."""
    data = {}
    if not existing_path.exists():
        return data
    content = existing_path.read_text(encoding="utf-8")
    # Match entries like: { name: "...", path: "...", description: "...", favorite: true }
    pattern = re.compile(
        r'\{ name: "(?P<name>[^"]*)", path: "(?P<path>[^"]*)", description: "(?P<desc>[^"]*)"(?P<fav>, favorite: true)? \}'
    )
    for m in pattern.finditer(content):
        data[m.group("path")] = {
            "description": m.group("desc"),
            "favorite": bool(m.group("fav")),
        }
    return data


def main():
    existing = load_existing_favorites_and_descriptions(OUTPUT_FILE)
    categories_data = []

    for cat_cfg in CATEGORIES:
        if cat_cfg["mode"] == "skills":
            raw_entries = scan_skills(EXAMPLES_DIR / cat_cfg["path"])
        else:
            raw_entries = scan_category(cat_cfg)

        entries = []
        for e in raw_entries:
            path = e["path"]
            # Preserve curated description and favorite from existing file
            if path in existing:
                e["description"] = existing[path]["description"]
                if existing[path]["favorite"]:
                    e["favorite"] = True
            # Apply FAVORITES set
            if path in FAVORITES:
                e["favorite"] = True
            entries.append(e)

        categories_data.append({
            "key": cat_cfg["key"],
            "icon": cat_cfg["icon"],
            "label": cat_cfg.get("label"),
            "description": cat_cfg["description"],
            "entries": entries,
        })

    output = build_ts(categories_data)

    mode = "--check" if "--check" in sys.argv else ("--write" if "--write" in sys.argv else ("--diff" if "--diff" in sys.argv else "print"))

    if mode == "print":
        print(output)
    elif mode == "--write":
        OUTPUT_FILE.write_text(output, encoding="utf-8")
        total = sum(len(c["entries"]) for c in categories_data)
        print(f"Written: {OUTPUT_FILE} ({total} indexed entries)", file=sys.stderr)
    elif mode == "--check":
        if OUTPUT_FILE.exists():
            current = OUTPUT_FILE.read_text(encoding="utf-8")
            if current == output:
                print("OK: examples-data.ts is up to date", file=sys.stderr)
                sys.exit(0)
            else:
                lines_a = current.splitlines()
                lines_b = output.splitlines()
                diff = list(difflib.unified_diff(lines_a, lines_b, fromfile="current", tofile="generated", lineterm=""))
                print(f"DRIFT: {len([l for l in diff if l.startswith(('+', '-')) and not l.startswith(('+++', '---'))])} line(s) differ", file=sys.stderr)
                sys.exit(1)
        elif not LANDING_ROOT.exists():
            # The landing repo is a sibling checkout, absent in CI where only this
            # repo is cloned. Sync cannot be judged against a repo we do not have,
            # so skip rather than fail: a permanently red gate teaches people to
            # ignore it. Drift is still caught locally and by the landing's own CI.
            print(f"SKIP: landing repo not present at {LANDING_ROOT}", file=sys.stderr)
            sys.exit(0)
        else:
            print("MISSING: examples-data.ts does not exist", file=sys.stderr)
            sys.exit(1)
    elif mode == "--diff":
        if OUTPUT_FILE.exists():
            current = OUTPUT_FILE.read_text(encoding="utf-8")
            diff = difflib.unified_diff(
                current.splitlines(keepends=True),
                output.splitlines(keepends=True),
                fromfile="current",
                tofile="generated",
            )
            sys.stdout.writelines(diff)
        else:
            print(output)


if __name__ == "__main__":
    main()
