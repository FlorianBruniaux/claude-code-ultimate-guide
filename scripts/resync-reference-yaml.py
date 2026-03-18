#!/usr/bin/env python3
"""
Re-sync line numbers in machine-readable/reference.yaml

Strategy:
  1. Build header index for each guide file (all lines starting with #)
  2. For each reference.yaml entry with a line number, read what's at that line
  3. If content doesn't look right, search by key-name keywords in headers
  4. Output a patch file with proposed fixes + confidence scores

Usage:
  python3 scripts/resync-reference-yaml.py [--apply]

  Without --apply: prints report to stdout + saves claudedocs/resync-report.md
  With --apply:    applies HIGH CONFIDENCE fixes directly to reference.yaml
"""

import re
import sys
import os
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
YAML_FILE = REPO_ROOT / "machine-readable" / "reference.yaml"
REPORT_FILE = REPO_ROOT / "claudedocs" / "resync-report.md"

# Files that reference.yaml points to (with bare integers → ultimate-guide.md)
GUIDE_FILES = {
    "guide/ultimate-guide.md": None,
    "guide/architecture.md": None,
    "guide/workflows/iterative-refinement.md": None,
    "guide/observability.md": None,
    "guide/learning-with-ai.md": None,
    "guide/ai-ecosystem.md": None,
    "guide/ai-traceability.md": None,
    "guide/sandbox-isolation.md": None,
    "guide/sandbox-native.md": None,
    "guide/known-issues.md": None,
    "guide/third-party-tools.md": None,
    "guide/adoption-approaches.md": None,
    "examples/commands/review-pr.md": None,
    "examples/agents/code-reviewer.md": None,
}


def build_header_index(filepath: Path) -> list[tuple[int, str]]:
    """Return list of (line_num, header_text) for all # headers."""
    headers = []
    try:
        with open(filepath, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                stripped = line.rstrip()
                if stripped.startswith("#"):
                    headers.append((i, stripped))
    except FileNotFoundError:
        pass
    return headers


def get_line_content(filepath: Path, line_num: int, context: int = 2) -> str:
    """Return content around a given line number."""
    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
        start = max(0, line_num - 1 - context)
        end = min(len(lines), line_num + context)
        result = []
        for i in range(start, end):
            marker = ">>>" if i == line_num - 1 else "   "
            result.append(f"{marker} {i+1}: {lines[i].rstrip()}")
        return "\n".join(result)
    except FileNotFoundError:
        return "(file not found)"


def key_to_keywords(key: str) -> list[str]:
    """Convert snake_case key to search keywords, filtering noise words."""
    noise = {"the", "a", "an", "and", "or", "of", "in", "to", "for",
             "is", "at", "by", "on", "it", "its", "from", "with",
             "guide", "section", "line", "ref", "reference", "api",
             "mode", "modes", "type", "types", "table", "example",
             "examples", "list", "advanced", "basic", "overview", "vs"}
    words = re.split(r"[_\-]", key.lower())
    return [w for w in words if w not in noise and len(w) > 2]


def score_header(keywords: list[str], header_text: str) -> int:
    """Score a header based on keyword matches (higher = better)."""
    header_lower = header_text.lower()
    score = 0
    for kw in keywords:
        if kw in header_lower:
            score += 1
        # Partial match bonus
        elif len(kw) > 4 and any(kw in w for w in header_lower.split()):
            score += 0.5
    return score


def find_best_header(key: str, headers: list[tuple[int, str]],
                     old_line: int) -> tuple[int | None, float, str]:
    """Find best matching header. Returns (new_line, confidence, header_text)."""
    keywords = key_to_keywords(key)
    if not keywords:
        return None, 0.0, ""

    best_score = 0
    best_line = None
    best_text = ""
    second_best = 0

    for line_num, header_text in headers:
        score = score_header(keywords, header_text)
        if score > best_score:
            second_best = best_score
            best_score = score
            best_line = line_num
            best_text = header_text
        elif score > second_best:
            second_best = score

    if best_score == 0:
        return None, 0.0, ""

    # Confidence: high if best is clearly better than second best
    if best_score >= 2 and (second_best == 0 or best_score / max(second_best, 0.1) >= 2):
        confidence = min(1.0, best_score / max(len(keywords), 1))
    else:
        confidence = 0.4 * (best_score / max(len(keywords), 1))

    return best_line, confidence, best_text


def parse_yaml_line_refs(yaml_content: str) -> list[dict]:
    """
    Parse reference.yaml and extract all line number references.
    Returns list of {key, file, old_line, yaml_line, raw_value}
    """
    results = []
    in_main_guide_section = False
    lines = yaml_content.split("\n")

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            # Track if we're in the main guide section (bare integers = ultimate-guide.md)
            if "# Main guide (guide/ultimate-guide.md)" in stripped:
                in_main_guide_section = True
            elif stripped.startswith("#") and in_main_guide_section:
                # New major section — stop treating bare ints as ultimate-guide.md
                # But keep it true since the pattern continues after comments
                pass
            continue

        # Pattern 1: key: "filepath:NNNN"  or  key: "filepath:NNNN"  # comment
        m = re.match(r'^(\s*)(\S+):\s*"([^"]+):(\d+)"', line)
        if m:
            key = m.group(2).rstrip(":")
            filepath = m.group(3)
            line_num = int(m.group(4))
            results.append({
                "key": key,
                "file": filepath,
                "old_line": line_num,
                "yaml_line": i,
                "raw_value": f'"{filepath}:{line_num}"',
                "type": "string_ref",
            })
            continue

        # Pattern 2: key: NNNN  (bare integer, implies ultimate-guide.md if in that section)
        m = re.match(r'^(\s*)(\S+):\s*(\d{3,5})\s*(?:#.*)?$', line)
        if m:
            key = m.group(2).rstrip(":")
            line_num = int(m.group(3))
            # Heuristic: if line_num > 100 and key looks like a content reference
            # (not a count, score, year etc.)
            if line_num > 100 and not any(x in key for x in
                    ["count", "score", "stars", "year", "limit", "budget",
                     "savings", "total", "ratio", "budget", "sizing"]):
                results.append({
                    "key": key,
                    "file": "guide/ultimate-guide.md",
                    "old_line": line_num,
                    "yaml_line": i,
                    "raw_value": str(line_num),
                    "type": "bare_int",
                })

    return results


def validate_line(filepath: Path, line_num: int) -> str:
    """Return the content at a given line (or error)."""
    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
        if 1 <= line_num <= len(lines):
            return lines[line_num - 1].rstrip()
        return f"(line {line_num} out of range, file has {len(lines)} lines)"
    except FileNotFoundError:
        return "(file not found)"


def is_sensible_content(key: str, content: str) -> bool:
    """Quick check if content at old line is plausibly related to the key."""
    if not content or content.startswith("("):
        return False
    keywords = key_to_keywords(key)
    if not keywords:
        return True
    content_lower = content.lower()
    matches = sum(1 for kw in keywords if kw in content_lower)
    return matches >= max(1, len(keywords) // 2)


def main():
    apply_fixes = "--apply" in sys.argv

    print("Reading reference.yaml...")
    with open(YAML_FILE, encoding="utf-8") as f:
        yaml_content = f.read()

    print("Building header indexes...")
    header_indexes = {}
    for rel_path in GUIDE_FILES:
        abs_path = REPO_ROOT / rel_path
        idx = build_header_index(abs_path)
        header_indexes[rel_path] = idx
        if idx:
            print(f"  {rel_path}: {len(idx)} headers")
        else:
            print(f"  {rel_path}: NOT FOUND or no headers")

    print("\nParsing YAML references...")
    refs = parse_yaml_line_refs(yaml_content)
    print(f"Found {len(refs)} line number references")

    report_lines = [
        "# Re-sync Report: machine-readable/reference.yaml",
        f"Generated: 2026-02-25",
        f"Total references scanned: {len(refs)}",
        "",
    ]

    corrections = []  # (yaml_line, old_value, new_value, key)
    stats = {"ok": 0, "high": 0, "medium": 0, "low": 0, "unknown": 0, "file_missing": 0}

    ok_entries = []
    needs_fix = []

    for ref in refs:
        key = ref["key"]
        rel_path = ref["file"]
        old_line = ref["old_line"]
        abs_path = REPO_ROOT / rel_path

        current_content = validate_line(abs_path, old_line)
        headers = header_indexes.get(rel_path, [])

        if not headers and not abs_path.exists():
            stats["file_missing"] += 1
            needs_fix.append({**ref, "status": "FILE_MISSING", "new_line": None,
                              "confidence": 0, "current_content": current_content,
                              "suggested_header": ""})
            continue

        sensible = is_sensible_content(key, current_content)

        if sensible:
            stats["ok"] += 1
            ok_entries.append({**ref, "current_content": current_content})
        else:
            new_line, confidence, header_text = find_best_header(key, headers, old_line)

            if confidence >= 0.7:
                level = "HIGH"
                stats["high"] += 1
            elif confidence >= 0.4:
                level = "MEDIUM"
                stats["medium"] += 1
            elif new_line:
                level = "LOW"
                stats["low"] += 1
            else:
                level = "UNKNOWN"
                stats["unknown"] += 1

            needs_fix.append({
                **ref,
                "status": level,
                "new_line": new_line,
                "confidence": confidence,
                "current_content": current_content,
                "suggested_header": header_text,
            })

            if new_line and level in ("HIGH", "MEDIUM"):
                if ref["type"] == "string_ref":
                    old_val = f'"{rel_path}:{old_line}"'
                    new_val = f'"{rel_path}:{new_line}"'
                else:
                    old_val = str(old_line)
                    new_val = str(new_line)
                corrections.append((ref["yaml_line"], old_val, new_val, key))

    # Build report
    report_lines += [
        "## Summary",
        "",
        f"| Status | Count |",
        f"|--------|-------|",
        f"| OK (content matches) | {stats['ok']} |",
        f"| HIGH confidence fix | {stats['high']} |",
        f"| MEDIUM confidence fix | {stats['medium']} |",
        f"| LOW confidence (manual review) | {stats['low']} |",
        f"| UNKNOWN (no match found) | {stats['unknown']} |",
        f"| FILE MISSING | {stats['file_missing']} |",
        f"| **Total** | **{len(refs)}** |",
        "",
        f"Auto-fixable (HIGH + MEDIUM): **{stats['high'] + stats['medium']}**",
        "",
    ]

    if needs_fix:
        report_lines += ["## Entries Needing Correction", ""]
        for entry in sorted(needs_fix, key=lambda x: (-x["confidence"], x["key"])):
            status = entry["status"]
            emoji = {"HIGH": "✅", "MEDIUM": "⚠️", "LOW": "🔶", "UNKNOWN": "❓", "FILE_MISSING": "🚫"}.get(status, "")
            report_lines.append(f"### {emoji} {entry['key']} ({status}, conf={entry['confidence']:.2f})")
            report_lines.append(f"- **File**: `{entry['file']}`")
            report_lines.append(f"- **Old line**: {entry['old_line']}")
            report_lines.append(f"- **Content at old line**: `{entry['current_content'][:100]}`")
            if entry["new_line"]:
                report_lines.append(f"- **Suggested line**: {entry['new_line']}")
                report_lines.append(f"- **Header found**: `{entry['suggested_header']}`")
            else:
                report_lines.append(f"- **Suggested line**: (not found — manual search needed)")
            report_lines.append("")

    report_lines += ["## OK Entries (sample)", ""]
    for entry in ok_entries[:20]:
        report_lines.append(f"- `{entry['key']}`: line {entry['old_line']} → `{entry['current_content'][:80]}`")

    report_content = "\n".join(report_lines)

    # Write report
    REPORT_FILE.parent.mkdir(exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"\nReport saved to {REPORT_FILE}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"OK:            {stats['ok']}")
    print(f"HIGH fix:      {stats['high']}")
    print(f"MEDIUM fix:    {stats['medium']}")
    print(f"LOW fix:       {stats['low']}")
    print(f"UNKNOWN:       {stats['unknown']}")
    print(f"FILE MISSING:  {stats['file_missing']}")
    print(f"Auto-fixable:  {stats['high'] + stats['medium']}")
    print(f"{'='*60}")

    if corrections:
        print(f"\n{'='*60}")
        print("PROPOSED CORRECTIONS (HIGH + MEDIUM confidence):")
        print(f"{'='*60}")
        for yaml_line, old_val, new_val, key in corrections[:30]:
            print(f"  Line {yaml_line:4d} | {key}")
            print(f"           {old_val} → {new_val}")
        if len(corrections) > 30:
            print(f"  ... and {len(corrections) - 30} more (see report)")

    if apply_fixes and corrections:
        print(f"\nApplying {len(corrections)} fixes to reference.yaml...")
        content = yaml_content
        applied = 0
        for yaml_line_num, old_val, new_val, key in corrections:
            # Find the exact occurrence of old_val near the yaml_line_num
            # Use line-by-line replacement to be precise
            lines = content.split("\n")
            target_idx = yaml_line_num - 1
            if target_idx < len(lines) and old_val in lines[target_idx]:
                lines[target_idx] = lines[target_idx].replace(old_val, new_val, 1)
                applied += 1
            else:
                # Try ±2 lines
                for delta in [-1, 1, -2, 2]:
                    idx = target_idx + delta
                    if 0 <= idx < len(lines) and old_val in lines[idx]:
                        lines[idx] = lines[idx].replace(old_val, new_val, 1)
                        applied += 1
                        break
            content = "\n".join(lines)

        with open(YAML_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Applied {applied}/{len(corrections)} fixes.")
        print(f"Run without --apply to verify remaining issues.")
    elif not apply_fixes and corrections:
        print(f"\nRun with --apply to apply HIGH+MEDIUM confidence fixes automatically.")
        print(f"LOW and UNKNOWN confidence fixes require manual review (see report).")


if __name__ == "__main__":
    main()
