#!/usr/bin/env python3
"""
Regression tests for scripts/resync-reference-yaml.py.

Each test covers a trap the tooling has already fallen into once, and each one is
written so it DISCRIMINATES: alongside asserting that the shipped implementation
is right, it runs the known-bad implementation against the same input and asserts
that the bad one is wrong. A test that cannot fail proves nothing, which is the
whole reason this backlog survived for months: the only check in place asked
whether a referenced line existed inside a 26,554-line document, and that question
cannot answer false.

  python3 scripts/test-resync-reference-yaml.py

Exit code 0 = all pass, 1 = at least one failure.
"""
import importlib.util
import re
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "scripts" / "resync-reference-yaml.py"

_spec = importlib.util.spec_from_file_location("resync", TOOL)
resync = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(resync)

failures = []
passes = 0


def check(name, cond, detail=""):
    global passes
    if cond:
        passes += 1
        print(f"  PASS  {name}")
    else:
        failures.append(name)
        print(f"  FAIL  {name}  {detail}")


# ---------------------------------------------------------------------------
# Trap 1 — counter corruption
#
# The first version of the repair tool would have rewritten
# resource_evaluations_count: 167 and ui_ux_pro_max_stars: 33700 with line
# numbers, because a bare integer carries no type information. Corrupting a
# counter is silent and propagates; it must be impossible.
# ---------------------------------------------------------------------------
print("\nTrap 1 — counter-valued integers must never be treated as line numbers")

GUIDE_LEN = 26554  # representative; the real value comes from the file at runtime

COUNTERS = [
    ("resource_evaluations_count", 167),
    ("ui_ux_pro_max_stars", 33700),
    ("quiz_questions", 473),
    ("templates_total", 268),
    ("guide_version", 3410),
]
for key, val in COUNTERS:
    protected, why = resync.is_count_value(key, val, GUIDE_LEN)
    check(f"protected: {key} = {val}", protected, f"(reason={why!r})")

# The bounds check must stand on its own, with no help from the name. A value
# past the end of the file cannot be a line number whatever the key is called.
protected, why = resync.is_count_value("some_unremarkable_name", 99999, GUIDE_LEN)
check("bounds check alone protects an out-of-range value", protected, f"(reason={why!r})")

# Discrimination: a guard with no suffix list and no bounds check lets both through.
def guard_without_any_check(key, value, max_lines):
    return False, ""


leaks = [k for k, v in COUNTERS if not guard_without_any_check(k, v, GUIDE_LEN)[0]]
check("unguarded implementation leaks every counter (test discriminates)",
      len(leaks) == len(COUNTERS), f"(leaked {len(leaks)}/{len(COUNTERS)})")


# ---------------------------------------------------------------------------
# Trap 2 — the guard being too broad
#
# The first guard matched substrings anywhere in the key. "count" caught nothing
# extra, but "limit" swallowed tasks_api_limitations, "budget" swallowed
# subscription_token_budgets, "ratio" swallowed subscription_opus_ratio and
# "sizing" swallowed claudemd_sizing. Those are genuine line references that then
# silently stopped being repaired. Protecting a real reference is a quieter
# failure than corrupting a counter, but it is still a failure.
# ---------------------------------------------------------------------------
print("\nTrap 2 — the counter guard must not swallow genuine line references")

REAL_REFS = [
    ("memory_files", 5300),
    ("cost_optimization", 2624),
    ("ui_ux_pro_max_guide", 12000),
    ("claudemd_sizing", 5553),
    ("tasks_api_limitations", 4826),
    ("subscription_token_budgets", 2633),
    ("subscription_opus_ratio", 2633),
    ("todowrite_migration_flag", 4920),
]
for key, val in REAL_REFS:
    protected, why = resync.is_count_value(key, val, GUIDE_LEN)
    check(f"not protected: {key} = {val}", not protected, f"(wrongly protected: {why!r})")

# Discrimination: the old substring guard wrongly protects several of these.
OLD_SUBSTRINGS = ["count", "score", "stars", "year", "limit", "budget",
                  "savings", "total", "ratio", "sizing"]


def old_substring_guard(key):
    return any(s in key for s in OLD_SUBSTRINGS)


swallowed = [k for k, _ in REAL_REFS if old_substring_guard(k)]
check("old substring guard swallows real refs (test discriminates)",
      len(swallowed) >= 4, f"(swallowed {swallowed})")


# ---------------------------------------------------------------------------
# Trap 3 — fence tracking
#
# A naive `startswith("```") -> flip` desynchronises on any file with an odd
# fence count. enterprise-governance.md has 51 fence lines: the toggle got stuck
# inside a block, dropped every heading after it, and reported 9 valid anchors as
# broken. CommonMark requires the closing fence to use the same character, be at
# least as long as the opener, and carry nothing after it.
# ---------------------------------------------------------------------------
print("\nTrap 3 — fence tracking must follow CommonMark, not a naive toggle")

# A 4-backtick block whose body contains a single unmatched 3-backtick opener.
# The fence count is odd, so a naive toggle ends up inverted and swallows
# everything after it. CommonMark closes the block correctly at the 4-backtick
# line, because a 3-backtick run is shorter than the opener and carries an info
# string, so it cannot be the closer.
FIXTURE = """# Title

````markdown
```bash
echo "an unmatched opener, quoted as an example"
# This heading is inside a fence and must be ignored
````

## Real Heading A

```python
print("hi")
```

## Real Heading B

~~~
a tilde fence closed by a longer tilde run
~~~~

## Real Heading C
"""


def naive_headings(path):
    """The implementation that shipped first, kept here as the control."""
    out, inside = [], False
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        if line.lstrip().startswith("```"):
            inside = not inside
            continue
        if inside:
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            out.append((n, len(m.group(1)), m.group(2).strip()))
    return out


with tempfile.TemporaryDirectory() as td:
    f = Path(td) / "fixture.md"
    f.write_text(FIXTURE, encoding="utf-8")

    got = [h[2] for h in resync.headings(f)]
    expected = ["Title", "Real Heading A", "Real Heading B", "Real Heading C"]
    check("CommonMark extractor finds every real heading", got == expected, f"(got {got})")
    check("CommonMark extractor ignores the heading inside the fence",
          "This heading is inside a fence and must be ignored" not in got)

    naive = [h[2] for h in naive_headings(f)]
    check("naive toggle loses headings on this fixture (test discriminates)",
          naive != expected, f"(naive got {naive})")

# The same rule, exercised against the file that actually broke it. The failure
# is two-sided and the second half is the one that got missed originally: the
# desynchronised toggle both DROPS real sections (it is stuck inside a fence) and
# INVENTS headings out of shell comments and the markdown examples embedded in
# code blocks (it is stuck outside one). Counting headings alone hides this,
# because the invented ones outnumber the dropped ones.
gov = REPO_ROOT / "guide" / "security" / "enterprise-governance.md"
if gov.exists():
    n_fences = sum(1 for l in open(gov, encoding="utf-8", errors="ignore")
                   if l.lstrip().startswith("```"))
    real = {(h[0], h[2]) for h in resync.headings(gov)}
    naive_real = {(h[0], h[2]) for h in naive_headings(gov)}
    dropped = real - naive_real
    invented = naive_real - real
    check(f"enterprise-governance.md has an odd fence count ({n_fences})",
          n_fences % 2 == 1, f"(got {n_fences})")
    check("naive toggle drops real sections there (test discriminates)",
          len(dropped) >= 15, f"(dropped {len(dropped)})")
    check("naive toggle invents headings from fenced content (test discriminates)",
          len(invented) >= 40, f"(invented {len(invented)})")
    check("the dropped set contains real numbered sections",
          any(t.startswith("5. ") or t.startswith("6. ") for _, t in dropped),
          f"(dropped sample {sorted(dropped)[:3]})")
    check("CommonMark extractor invents nothing from fenced shell comments",
          not any(t.startswith("Create .claude") or t.startswith("Usage:")
                  for _, t in real))
else:
    print("  SKIP  enterprise-governance.md not present")


# ---------------------------------------------------------------------------
# Trap 4 — the URL / prose false positive
#
# `"([^"]+):(\d+)"` also matches URLs and prose. "http://localhost:37777" parsed
# as a file named `http://localhost` at line 37777, and a sentence ending in
# "... see guide/core/foo.md:2215" parsed as a file named after the whole
# sentence. Both surfaced as FILE MISSING and inflated the broken count.
# ---------------------------------------------------------------------------
print("\nTrap 4 — URLs and prose must not parse as positional references")

YAML_SAMPLE = '''deep_dive:
  claude_mem_dashboard: "http://localhost:37777"
  docs_link: "https://code.claude.com/docs/en/skills"
  prose_note: "Context budget is documented in detail, see guide/core/foo.md:2215"
  real_ref: "guide/core/architecture.md:310"
  real_anchor: "guide/core/architecture.md#2-the-tool-arsenal"
  a_count: 167
'''
parsed = resync.parse_refs(YAML_SAMPLE)
keys = {p["key"] for p in parsed}
check("localhost URL is not parsed as a reference", "claude_mem_dashboard" not in keys)
check("https URL is not parsed as a reference", "docs_link" not in keys)
check("prose sentence is not parsed as a reference", "prose_note" not in keys)
check("a genuine path:line reference is still parsed", "real_ref" in keys)
check("a genuine path#anchor reference is still parsed", "real_anchor" in keys)

# Discrimination: the permissive pattern picks up the URL and the prose.
loose = re.compile(r'^(\s*)(\S+):\s*"([^"]+):(\d+)"')
loose_hits = {m.group(2).rstrip(":") for m in
              (loose.match(l) for l in YAML_SAMPLE.split("\n")) if m}
check("permissive pattern matches URL and prose (test discriminates)",
      {"claude_mem_dashboard", "prose_note"} <= loose_hits, f"(loose hits {loose_hits})")


# ---------------------------------------------------------------------------
# Trap 5 — the hardcoded file whitelist
#
# The header index was built for a hardcoded list of 14 files. Every reference
# into a file outside that list scored against an empty index and was reported
# UNKNOWN, which made 29 tractable references look undecidable. rpi.md was the
# clearest case: its "Phase 1: Research" / "Phase 2: Plan" / "Phase 3: Implement"
# headings are real and unambiguous, but the file was not on the list.
# ---------------------------------------------------------------------------
print("\nTrap 5 — the header index must cover any referenced file, not a whitelist")

rpi = "guide/workflows/rpi.md"
if (REPO_ROOT / rpi).exists():
    titles = [h[2] for h in resync.get_headings(rpi)]
    for want in ("Phase 1: Research", "Phase 2: Plan", "Phase 3: Implement"):
        check(f"{rpi} indexes {want!r}", want in titles)
else:
    print(f"  SKIP  {rpi} not present")


# ---------------------------------------------------------------------------
# Guard behaviour: --check must be able to fail
# ---------------------------------------------------------------------------
print("\nGate — --check must exit non-zero when the backlog exceeds the ceiling")
import subprocess

r = subprocess.run([sys.executable, str(TOOL), "--check", "--max-broken", "-1"],
                   capture_output=True, text=True, cwd=REPO_ROOT)
check("--check --max-broken -1 exits non-zero", r.returncode != 0,
      f"(exit={r.returncode})")

r = subprocess.run([sys.executable, str(TOOL), "--check", "--max-broken", "100000"],
                   capture_output=True, text=True, cwd=REPO_ROOT)
check("--check --max-broken 100000 exits zero", r.returncode == 0,
      f"(exit={r.returncode})")


print(f"\n{passes} passed, {len(failures)} failed")
if failures:
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
sys.exit(0)
