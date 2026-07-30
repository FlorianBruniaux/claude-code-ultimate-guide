#!/usr/bin/env python3
"""
Audit, repair and migrate the positional references in machine-readable/reference.yaml.

This is the single tool for the job. It replaces the earlier pair
(`resync-reference-yaml.py` + `fix-reference-refs.py`), which overlapped on
key-name-to-heading matching while neither was a superset of the other: resync
validated the content actually present at the stored line and understood both
`"path:N"` strings and bare integers but had no notion of anchors; fix-reference-refs
migrated to anchors, guarded counter-valued integers and applied CommonMark fence
rules but never looked at what sat at the stored line. Both behaviours are kept here.

Three reference shapes exist in reference.yaml:

  A) anchor   key: "guide/foo/bar.md#some-heading"   drift-proof, preferred
  B) line     key: "guide/foo/bar.md:123"            consumed by the landing (line stripped)
  C) bare int key: 19597                             ultimate-guide.md line, LLM-only

Usage:
  python3 scripts/resync-reference-yaml.py              # full report -> claudedocs/resync-report.md
  python3 scripts/resync-reference-yaml.py --apply      # apply confident fixes to reference.yaml
  python3 scripts/resync-reference-yaml.py --check [--max-broken N]   # CI gate

Regression tests for the three traps this tool has already fallen into once
(counter corruption, over-broad counter guard, fence desynchronisation) live in
scripts/test-resync-reference-yaml.py and run in CI.
"""

import argparse
import difflib
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
YAML_FILE = REPO_ROOT / "machine-readable" / "reference.yaml"
REPORT_FILE = REPO_ROOT / "claudedocs" / "resync-report.md"

# Bare integers are resolved against the main guide.
MAIN_GUIDE = "guide/ultimate-guide.md"

# Only repo-relative paths under one of these roots are references. Without this
# restriction the `"([^"]+):(\d+)"` pattern also matches URLs and prose:
# "http://localhost:37777" parsed as a file named `http://localhost` at line 37777,
# and a sentence ending in "... see guide/core/foo.md:2215" parsed as a file named
# after the whole sentence. Both surfaced as FILE MISSING and inflated the count.
PATH_ROOTS = ("guide", "examples", "docs", "machine-readable", "whitepapers",
              "scripts", "mcp-server", "quiz", "tools")
PATH_ROOT_RE = "|".join(PATH_ROOTS)

# ---------------------------------------------------------------------------
# Trap 1 + 2: counter-valued integers
#
# Bare integers in reference.yaml are NOT all line numbers. Some are quantities:
# resource_evaluations_count: 167, ui_ux_pro_max_stars: 33700. Rewriting one of
# those with a line number is silent data corruption.
#
# The guard matches on SUFFIX only and the list stays short. An earlier version
# matched substrings anywhere in the key and swallowed memory_files,
# cost_optimization, ui_ux_pro_max_guide and three others, which are genuine line
# refs that then silently stopped being repaired. Protecting a real reference
# leaves it visibly unrepaired; corrupting a counter is silent and propagates.
# So the guard is narrow, and an independent bounds check catches the rest: a
# value past the end of the target file cannot be a line number whatever the key
# is called.
# ---------------------------------------------------------------------------
COUNT_SUFFIX = re.compile(
    r'_(count|counts|total|totals|num|nb|stars|pct|percent|questions|'
    r'categories|version|year)$')


def is_count_value(key: str, value: int, max_lines: int) -> tuple[bool, str]:
    """Return (protected, reason). Either guard alone is enough to protect."""
    if COUNT_SUFFIX.search(key):
        return True, "count suffix"
    if value > max_lines:
        return True, f"> {max_lines} lines in target file"
    return False, ""


# ---------------------------------------------------------------------------
# Trap 3: fence tracking
# ---------------------------------------------------------------------------
def headings(path: Path) -> list[tuple[int, int, str]]:
    """
    Return [(line_no, level, text)] for every ATX heading outside a code fence.

    CommonMark fence semantics, not a naive toggle. `startswith("```") -> flip`
    desynchronises on any file with an odd fence count (a 4-backtick block
    containing 3-backtick examples closes nothing). enterprise-governance.md has
    51 fence lines: the toggle got stuck inside a block, dropped every heading
    after it, and reported 9 perfectly valid anchors as broken. A closing fence
    must use the same character, be at least as long as the opener, and carry
    nothing but whitespace after it.
    """
    out = []
    fence_char, fence_len = None, 0
    try:
        fh = open(path, encoding="utf-8", errors="ignore")
    except (FileNotFoundError, IsADirectoryError):
        return out
    with fh:
        for n, raw in enumerate(fh, 1):
            s = raw.lstrip()
            m = re.match(r'^([`~]{3,})(.*)$', s)
            if m:
                marker, rest = m.group(1), m.group(2).strip()
                if fence_char is None:
                    fence_char, fence_len = marker[0], len(marker)
                    continue
                if marker[0] == fence_char and len(marker) >= fence_len and not rest:
                    fence_char, fence_len = None, 0
                    continue
            if fence_char is not None:
                continue
            m = re.match(r'^(#{1,6})\s+(.*)$', raw)
            if m:
                out.append((n, len(m.group(1)), m.group(2).strip()))
    return out


def _strip_non_slug_chars(text: str) -> str:
    """Keep what github-slugger's generated regex keeps: letters, digits,
    underscore, hyphen, whitespace, and Unicode combining marks (category M*).

    Python's `\\w` does not include category Mn (nonspacing mark), so a plain
    `[^\\w\\s\\-]` strip drops a variation selector (U+FE0F) that rides on a
    preceding emoji, e.g. the U+FE0F in "⚠️". github-slugger's regex keeps it.
    Measured against 4,835 real headings via the actual `github-slugger` npm
    package (the same one @astrojs/markdown-remark uses to stamp heading ids):
    without this, 7 headings using variation-selector emoji, a pattern this
    guide reuses often ("⚠️ ..."), produced a slug matching nothing rendered.
    """
    return ''.join(
        c for c in text
        if c.isalnum() or c in (' ', '-', '_') or unicodedata.category(c).startswith('M')
    )


def slugify(heading_text: str) -> str:
    """GitHub-style slug, honouring an explicit {#custom-id}.

    Must match github-slugger exactly, since that is what actually stamps `id`
    on rendered headings (both GitHub's own render and the landing's Starlight
    pipeline, via @astrojs/markdown-remark -> github-slugger). No `.strip()`:
    github-slugger does not trim leading/trailing hyphens left behind by a
    stripped leading emoji or symbol. A heading starting with an emoji (common
    in this guide: "🔄 LLM Day-to-Day...", "⚠️ Migration Risks...") produces a
    leading hyphen in the real id. Stripping it here produced a slug that
    matched nothing rendered anywhere: 16 anchors were dead in production
    while validate-reference-yaml.py reported them all valid, because the
    validator recomputed the same wrong slug to check against.
    """
    ex = re.search(r'\{#([^}]+)\}', heading_text)
    if ex:
        return ex.group(1)
    h = re.sub(r'`', '', heading_text)
    h = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', h)
    return _strip_non_slug_chars(h.lower()).replace(' ', '-')


def slugs(path: Path) -> set[str]:
    out = set()
    for _, _, h in headings(path):
        ex = re.search(r'\{#([^}]+)\}', h)
        if ex:
            out.add(ex.group(1))
            h = re.sub(r'\{#[^}]+\}', '', h).strip()
        out.add(slugify(h))
    return out


# ---------------------------------------------------------------------------
# Caches
# ---------------------------------------------------------------------------
_headings_cache: dict[str, list[tuple[int, int, str]]] = {}
_slugs_cache: dict[str, set[str]] = {}
_len_cache: dict[str, int] = {}


def get_headings(rel_path: str) -> list[tuple[int, int, str]]:
    """
    Header index for any referenced file, built on demand.

    The previous version indexed a hardcoded whitelist of 14 files. Every
    reference into a file outside that list was scored against an empty index and
    reported UNKNOWN, which made 29 tractable references look like undecidable
    ones. There is no reason for the list: the set of files to index is exactly
    the set of files referenced.
    """
    if rel_path not in _headings_cache:
        _headings_cache[rel_path] = headings(REPO_ROOT / rel_path)
    return _headings_cache[rel_path]


def get_slugs(rel_path: str) -> set[str]:
    if rel_path not in _slugs_cache:
        _slugs_cache[rel_path] = slugs(REPO_ROOT / rel_path)
    return _slugs_cache[rel_path]


def anchor_line(rel_path: str, slug: str, hint_line: int | None = None) -> int | None:
    """Line of the heading whose slug is `slug`, or None if absent/ambiguous.

    Ambiguity has to be None, not the first hit: GitHub suffixes a repeated slug
    `-1`, `-2`, so a duplicated slug does not identify a section and an anchor
    built from it would silently resolve to the wrong one. `hint_line` is the
    escape hatch for a reference that was manually verified against a heading
    with a duplicated slug (e.g. "Best Practices", used 4 times in this guide):
    if the slug is ambiguous but `hint_line` is exactly one of the candidates,
    that specific reference is still resolvable, because the human already did
    the disambiguation the slug alone cannot do. It still cannot be auto-repaired
    if it drifts to a line outside the candidate set later (which of several
    "Best Practices" a stale reference now means cannot be re-derived), so a
    drift past the candidate set correctly reports as unresolved rather than
    silently landing on the wrong one of the duplicates.
    """
    hits = [n for n, _, t in get_headings(rel_path) if slugify(t) == slug]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1 and hint_line in hits:
        return hint_line
    return None


def file_length(rel_path: str) -> int:
    if rel_path not in _len_cache:
        p = REPO_ROOT / rel_path
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                _len_cache[rel_path] = sum(1 for _ in f)
        except (FileNotFoundError, IsADirectoryError):
            _len_cache[rel_path] = 0
    return _len_cache[rel_path]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
NOISE = {"the", "a", "an", "and", "or", "of", "in", "to", "for",
         "is", "at", "by", "on", "it", "its", "from", "with",
         "guide", "section", "line", "ref", "reference", "api",
         "mode", "modes", "type", "types", "table", "example",
         "examples", "list", "advanced", "basic", "overview", "vs"}

STOP = {"guide", "section", "ref", "line", "the", "and", "for", "with", "md",
        "file", "doc", "docs", "link", "url", "path"}


def key_to_keywords(key: str) -> list[str]:
    words = re.split(r"[_\-]", key.lower())
    return [w for w in words if w not in NOISE and len(w) > 2]


def score_header(keywords: list[str], header_text: str) -> float:
    """Classification scorer (inherited from resync). Drives status only."""
    hl = header_text.lower()
    s = 0.0
    for kw in keywords:
        if kw in hl:
            s += 1
        elif len(kw) > 4 and any(kw in w for w in hl.split()):
            s += 0.5
    return s


def find_best_header(key: str, hs: list[tuple[int, int, str]]) -> tuple[int | None, float, str]:
    """Classification match. Returns (line, confidence, heading_text)."""
    keywords = key_to_keywords(key)
    if not keywords:
        return None, 0.0, ""
    best_score, best_line, best_text, second = 0.0, None, "", 0.0
    for line_num, _, text in hs:
        s = score_header(keywords, text)
        if s > best_score:
            second = best_score
            best_score, best_line, best_text = s, line_num, text
        elif s > second:
            second = s
    if best_score == 0:
        return None, 0.0, ""
    if best_score >= 2 and (second == 0 or best_score / max(second, 0.1) >= 2):
        conf = min(1.0, best_score / max(len(keywords), 1))
    else:
        conf = 0.4 * (best_score / max(len(keywords), 1))
    return best_line, conf, best_text


def toks(s: str) -> list[str]:
    s = re.sub(r'[^\w\s]', ' ', s.lower())
    return [t for t in re.split(r'[\s_]+', s) if len(t) > 2 and t not in STOP]


def overlap_score(key: str, heading_text: str) -> float:
    """Apply-gate scorer: normalised token overlap with fuzzy matching."""
    kt, ht = toks(key), toks(heading_text)
    if not kt or not ht:
        return 0.0
    hits = 0.0
    for t in kt:
        best = 0.0
        for h in ht:
            if t == h:
                best = 1.0
            elif len(t) > 3 and (t in h or h in t):
                best = max(best, 0.8)
            else:
                r = difflib.SequenceMatcher(None, t, h).ratio()
                if r > 0.86:
                    best = max(best, r * 0.7)
        hits += best
    return hits / len(kt)


MIN_CONF = 0.60
MIN_MARGIN = 0.15


def best_overlap_match(rel_path: str, key: str, cur_line: int):
    """Return (line, slug, conf, margin, text) for the apply gate, or None."""
    hs = get_headings(rel_path)
    if not hs:
        return None
    scored = sorted(((overlap_score(key, h[2]), h) for h in hs), key=lambda x: -x[0])
    top_s, top_h = scored[0]
    runner = scored[1][0] if len(scored) > 1 else 0.0
    ties = [h for s, h in scored if abs(s - top_s) < 1e-9]
    if len(ties) > 1:
        ties.sort(key=lambda h: abs(h[0] - cur_line))
        top_h = ties[0]
        runner = top_s  # ambiguous by definition, margin collapses to 0
    return (top_h[0], slugify(top_h[2]), top_s, top_s - runner, top_h[2])


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
RE_ANCHOR = re.compile(
    rf'^(\s*)([a-z0-9_]+):\s*"((?:{PATH_ROOT_RE})/[^"#\s]+)#([^"\s]+)"(.*)$')
RE_LINE = re.compile(
    rf'^(\s*)([a-z0-9_]+):\s*"((?:{PATH_ROOT_RE})/[^"#\s]+):(\d+)"(.*)$')
RE_BARE = re.compile(r'^(\s*)([a-z0-9_]+):\s*(\d{3,5})\s*(#.*)?$')

# A bare integer may declare which heading it means, as `# anchor: some-slug`
# anywhere in its trailing comment. That turns a guess into a fact: the stored
# line is correct if and only if it equals the line of the heading with that slug.
#
# This exists because the token-overlap heuristic below cannot confirm a correct
# reference whose key name shares no words with its heading. `cicd` pointing at
# "9.3 CI/CD Integration" is right, and the heuristic scores it zero because the
# heading spells it "CI/CD". Weakening the heuristic to accommodate that would be
# guessing at scale in the other direction. Declaring the anchor is not a guess,
# it is the author saying which section they meant, and it is then machine-checked
# on every run and auto-repairable when lines shift above it.
RE_ANCHOR_HINT = re.compile(r'#\s*anchor:\s*([A-Za-z0-9._\-]+)')


def parse_refs(yaml_content: str) -> list[dict]:
    refs = []
    for i, line in enumerate(yaml_content.split("\n"), 1):
        m = RE_ANCHOR.match(line)
        if m:
            refs.append({"key": m.group(2), "file": m.group(3), "anchor": m.group(4),
                         "old_line": None, "yaml_line": i, "type": "anchor_ref",
                         "indent": m.group(1), "tail": m.group(5)})
            continue
        m = RE_LINE.match(line)
        if m:
            refs.append({"key": m.group(2), "file": m.group(3), "anchor": None,
                         "old_line": int(m.group(4)), "yaml_line": i, "type": "string_ref",
                         "indent": m.group(1), "tail": m.group(5)})
            continue
        m = RE_BARE.match(line)
        if m:
            n = int(m.group(3))
            if n <= 100:
                continue
            tail = m.group(4) or ""
            hint = RE_ANCHOR_HINT.search(tail)
            refs.append({"key": m.group(2), "file": MAIN_GUIDE,
                         "anchor": hint.group(1) if hint else None,
                         "old_line": n, "yaml_line": i, "type": "bare_int",
                         "indent": m.group(1), "tail": tail})
    return refs


def line_content(rel_path: str, line_num: int) -> str:
    p = REPO_ROOT / rel_path
    try:
        with open(p, encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except (FileNotFoundError, IsADirectoryError):
        return "(file not found)"
    if 1 <= line_num <= len(lines):
        return lines[line_num - 1].rstrip()
    return f"(line {line_num} out of range, file has {len(lines)} lines)"


def is_sensible_content(key: str, content: str) -> bool:
    """Does the text at the stored position plausibly belong to this key?"""
    if not content or content.startswith("("):
        return False
    keywords = key_to_keywords(key)
    if not keywords:
        return True
    cl = content.lower()
    matches = sum(1 for kw in keywords if kw in cl)
    return matches >= max(1, len(keywords) // 2)


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------
def classify(ref: dict) -> dict:
    """Attach status, suggested target and confidence to a reference."""
    key, rel_path = ref["key"], ref["file"]
    abs_path = REPO_ROOT / rel_path

    if ref["type"] == "anchor_ref":
        if not abs_path.exists():
            return {**ref, "status": "FILE_MISSING", "confidence": 0.0,
                    "current_content": "(file not found)", "new_line": None,
                    "suggested_header": ""}
        ok = ref["anchor"] in get_slugs(rel_path)
        return {**ref, "status": "OK" if ok else "ANCHOR_DEAD", "confidence": 1.0 if ok else 0.0,
                "current_content": f"#{ref['anchor']}", "new_line": None,
                "suggested_header": ""}

    if ref["type"] == "bare_int":
        protected, why = is_count_value(key, ref["old_line"], file_length(MAIN_GUIDE))
        if protected:
            return {**ref, "status": "PROTECTED", "confidence": 0.0,
                    "current_content": f"(quantity: {why})", "new_line": None,
                    "suggested_header": ""}
        if ref["anchor"]:
            # Declared anchor: a hard check, no heuristics involved.
            target = anchor_line(MAIN_GUIDE, ref["anchor"], hint_line=ref["old_line"])
            if target is None:
                return {**ref, "status": "ANCHOR_DEAD", "confidence": 0.0,
                        "current_content": f"(declared anchor #{ref['anchor']} "
                                           f"matches no heading)",
                        "new_line": None, "suggested_header": ""}
            if target == ref["old_line"]:
                return {**ref, "status": "OK", "confidence": 1.0,
                        "current_content": line_content(MAIN_GUIDE, ref["old_line"]),
                        "new_line": None, "suggested_header": ""}
            return {**ref, "status": "LINE_DRIFTED", "confidence": 1.0,
                    "current_content": line_content(MAIN_GUIDE, ref["old_line"]),
                    "new_line": target,
                    "suggested_header": f"#{ref['anchor']}"}

    if not abs_path.exists():
        return {**ref, "status": "FILE_MISSING", "confidence": 0.0,
                "current_content": "(file not found)", "new_line": None,
                "suggested_header": ""}

    content = line_content(rel_path, ref["old_line"])
    if is_sensible_content(key, content):
        return {**ref, "status": "OK", "confidence": 1.0, "current_content": content,
                "new_line": None, "suggested_header": ""}

    new_line, conf, header_text = find_best_header(key, get_headings(rel_path))
    if conf >= 0.7:
        status = "HIGH"
    elif conf >= 0.4:
        status = "MEDIUM"
    elif new_line:
        status = "LOW"
    else:
        status = "UNKNOWN"
    return {**ref, "status": status, "confidence": conf, "current_content": content,
            "new_line": new_line, "suggested_header": header_text}


BROKEN_STATUSES = {"HIGH", "MEDIUM", "LOW", "UNKNOWN", "FILE_MISSING",
                   "ANCHOR_DEAD", "LINE_DRIFTED"}


# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------
def plan_fixes(entries: list[dict]) -> list[dict]:
    """
    Decide what to rewrite, using the stricter overlap scorer with a margin.

    string_ref -> anchor migration is preferred over line repair: anchors survive
    insertions above them, line numbers do not. bare ints are repaired in place
    and never converted, because the landing turns every deep_dive string starting
    with `guide/` into a Cmd+K entry and ~90 new entries pointing into a 26K-line
    file is a UX change to another repo, not an index fix.
    """
    plan = []
    for e in entries:
        if e["status"] not in BROKEN_STATUSES or e["type"] == "anchor_ref":
            continue
        if e["status"] == "LINE_DRIFTED":
            # Declared anchor, line moved. Deterministic repair, no confidence gate.
            plan.append({**e, "action": "repair",
                         "old_raw": str(e["old_line"]), "new_raw": str(e["new_line"]),
                         "apply_conf": 1.0, "heading": e["suggested_header"],
                         "heading_line": e["new_line"]})
            continue
        bm = best_overlap_match(e["file"], e["key"], e["old_line"])
        if not bm:
            continue
        hl, slug, conf, margin, text = bm
        if conf < MIN_CONF or margin < MIN_MARGIN:
            continue
        if e["type"] == "string_ref":
            plan.append({**e, "action": "migrate",
                         "old_raw": f'"{e["file"]}:{e["old_line"]}"',
                         "new_raw": f'"{e["file"]}#{slug}"',
                         "apply_conf": conf, "heading": text, "heading_line": hl})
        elif hl != e["old_line"]:
            plan.append({**e, "action": "repair",
                         "old_raw": str(e["old_line"]), "new_raw": str(hl),
                         "apply_conf": conf, "heading": text, "heading_line": hl})
    return plan


def apply_plan(yaml_content: str, plan: list[dict]) -> tuple[str, int]:
    lines = yaml_content.split("\n")
    applied = 0
    for p in plan:
        idx = p["yaml_line"] - 1
        if 0 <= idx < len(lines) and p["old_raw"] in lines[idx]:
            lines[idx] = lines[idx].replace(p["old_raw"], p["new_raw"], 1)
            applied += 1
    return "\n".join(lines), applied


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def parse_args():
    ap = argparse.ArgumentParser(
        description="Audit, repair and migrate positional refs in reference.yaml")
    ap.add_argument("--apply", action="store_true",
                    help="rewrite reference.yaml with the confident fixes")
    ap.add_argument("--check", action="store_true",
                    help="CI gate: compact summary, no files written, exit code is the gate")
    ap.add_argument("--max-broken", type=int, default=0,
                    help="max allowed broken references in --check mode (default 0)")
    return ap.parse_args()


def main():
    args = parse_args()
    quiet = args.check

    yaml_content = YAML_FILE.read_text(encoding="utf-8")
    refs = parse_refs(yaml_content)
    entries = [classify(r) for r in refs]

    stats = {}
    for e in entries:
        stats[e["status"]] = stats.get(e["status"], 0) + 1
    broken = sum(v for k, v in stats.items() if k in BROKEN_STATUSES)

    def g(k):
        return stats.get(k, 0)

    if args.check:
        print(f"Total references: {len(refs)}")
        print(f"  anchors        {sum(1 for e in entries if e['type'] == 'anchor_ref')}")
        print(f"  path:line      {sum(1 for e in entries if e['type'] == 'string_ref')}")
        print(f"  bare ints      {sum(1 for e in entries if e['type'] == 'bare_int')}")
        print(f"OK:            {g('OK')}")
        print(f"PROTECTED:     {g('PROTECTED')}  (quantities, never rewritten)")
        print(f"HIGH:          {g('HIGH')}")
        print(f"MEDIUM:        {g('MEDIUM')}")
        print(f"LOW:           {g('LOW')}")
        print(f"UNKNOWN:       {g('UNKNOWN')}")
        print(f"ANCHOR DEAD:   {g('ANCHOR_DEAD')}")
        print(f"LINE DRIFTED:  {g('LINE_DRIFTED')}  (declared anchor, --apply repairs)")
        print(f"FILE MISSING:  {g('FILE_MISSING')}")
        print(f"Broken total:  {broken} (max allowed: {args.max_broken})")
        if broken > args.max_broken:
            print(f"FAIL: {broken} broken references exceeds --max-broken {args.max_broken}")
            sys.exit(1)
        print("PASS")
        sys.exit(0)

    plan = plan_fixes(entries)

    print(f"Total references: {len(refs)}")
    for k in ("OK", "PROTECTED", "HIGH", "MEDIUM", "LOW", "UNKNOWN",
              "ANCHOR_DEAD", "LINE_DRIFTED", "FILE_MISSING"):
        print(f"  {k:<13} {g(k)}")
    print(f"Broken total:     {broken}")
    print(f"Applicable fixes: {len(plan)} "
          f"({sum(1 for p in plan if p['action'] == 'migrate')} migrate, "
          f"{sum(1 for p in plan if p['action'] == 'repair')} repair)")

    for p in plan[:40]:
        print(f"  L{p['yaml_line']:<5} {p['action']:<8} {p['key'][:38]:<38} "
              f"{p['old_raw']} -> {p['new_raw']}  conf={p['apply_conf']:.2f}")
    if len(plan) > 40:
        print(f"  ... and {len(plan) - 40} more")

    # Report
    rows = [
        "# Re-sync Report: machine-readable/reference.yaml",
        f"Generated: {date.today().isoformat()}",
        f"Total references scanned: {len(refs)}",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "|--------|-------|",
    ]
    for k in ("OK", "PROTECTED", "HIGH", "MEDIUM", "LOW", "UNKNOWN",
              "ANCHOR_DEAD", "LINE_DRIFTED", "FILE_MISSING"):
        rows.append(f"| {k} | {g(k)} |")
    rows += [f"| **Broken total** | **{broken}** |", "",
             f"Applicable without guessing: **{len(plan)}**", ""]

    needs = [e for e in entries if e["status"] in BROKEN_STATUSES]
    if needs:
        rows += ["## Entries Needing Correction", ""]
        for e in sorted(needs, key=lambda x: (x["file"], x["key"])):
            rows.append(f"### {e['key']} ({e['status']}, conf={e['confidence']:.2f})")
            rows.append(f"- **File**: `{e['file']}`")
            rows.append(f"- **Stored**: {e['old_line'] if e['old_line'] else '#' + (e['anchor'] or '')}")
            rows.append(f"- **Content there**: `{e['current_content'][:110]}`")
            if e["new_line"]:
                rows.append(f"- **Nearest heading match**: line {e['new_line']} "
                            f"`{e['suggested_header'][:90]}`")
            else:
                rows.append("- **Nearest heading match**: none (manual search needed)")
            rows.append("")

    REPORT_FILE.parent.mkdir(exist_ok=True)
    REPORT_FILE.write_text("\n".join(rows), encoding="utf-8")
    print(f"\nReport saved to {REPORT_FILE}")

    if args.apply and plan:
        new_content, applied = apply_plan(yaml_content, plan)
        YAML_FILE.write_text(new_content, encoding="utf-8")
        print(f"Applied {applied}/{len(plan)} fixes to {YAML_FILE}")
    elif args.apply:
        print("Nothing to apply.")
    else:
        print("DRY RUN (pass --apply to write)")


if __name__ == "__main__":
    main()
