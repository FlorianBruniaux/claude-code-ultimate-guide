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
# Trap 2b — slugify must match the real renderer, not itself
#
# validate-reference-yaml.py used to carry its own copy of slugify() and check
# anchors against it. That copy had the same bug as this one: a trailing
# `.strip()` before the space->hyphen replace, which github-slugger does not
# do. The validator was checking the data against its own mistake, so 16
# anchors were dead in production (both on GitHub and on the landing, which
# stamps heading ids via @astrojs/markdown-remark -> the same github-slugger
# package) while validate-reference-yaml.py reported every one of them fine.
#
# These pairs are pinned from the ACTUAL `github-slugger@2.0.0` npm package
# (resolved from ../claude-code-ultimate-guide-landing/node_modules), not
# reasoned out. Do not "fix" a failing pair here by editing the expected
# value: verify against the real package first, the whole reason this bug
# existed is that a self-referential check produced a value nobody checked
# against reality.
# ---------------------------------------------------------------------------
print("\nTrap 2b — slugify must match github-slugger, verified against the real package")

GITHUB_SLUGGER_GROUND_TRUTH = [
    ("2. Architecture Deep-Dive", "2-architecture-deep-dive"),
    ("3. Setup & Configuration", "3-setup--configuration"),
    ("6. Limitations & Gotchas", "6-limitations--gotchas"),
    ("9.11 Common Pitfalls & Best Practices", "911-common-pitfalls--best-practices"),
    ("isError: false + Empty Content vs isError: true",
     "iserror-false--empty-content-vs-iserror-true"),
    ("2. Excessive Token Consumption (Jan 2026 - Present)",
     "2-excessive-token-consumption-jan-2026---present"),
    ("🔄 LLM Day-to-Day Performance Variance", "-llm-day-to-day-performance-variance"),
    ("❌ Myth: \"Claude Code is 100x faster than other AI coding tools\"",
     "-myth-claude-code-is-100x-faster-than-other-ai-coding-tools"),
    ("⚠️ Migration Risks & Caveats", "️-migration-risks--caveats"),
    ("⚠️ AGENTS.md Support Status", "️-agentsmd-support-status"),
]
for text, want in GITHUB_SLUGGER_GROUND_TRUTH:
    got = resync.slugify(text)
    check(f"slugify matches github-slugger: {text[:44]!r}", got == want,
          f"(got {got!r}, want {want!r})")

# Discrimination: the old double-strip implementation fails the emoji-prefixed cases.


def old_slugify_with_strip(h):
    h = re.sub(r'`', '', h)
    h = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', h)
    return re.sub(r'[^\w\s\-]', '', h.lower(), flags=re.UNICODE).strip().replace(' ', '-')


emoji_cases = [(t, w) for t, w in GITHUB_SLUGGER_GROUND_TRUTH if t[0] in "🔄❌⚠️"]
old_wrong = [t for t, w in emoji_cases if old_slugify_with_strip(t) != w]
check("the old .strip()'d implementation gets emoji-prefixed headings wrong "
      "(test discriminates)", len(old_wrong) == len(emoji_cases),
      f"(old impl got {len(old_wrong)}/{len(emoji_cases)} wrong)")


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
# Declared anchors on bare integers
#
# The token-overlap heuristic cannot confirm a correct reference whose key name
# shares no words with its heading: `cicd` pointing at "9.3 CI/CD Integration" is
# right and scores zero, because the heading spells it "CI/CD". Declaring the
# anchor in the trailing comment replaces the heuristic with a hard check.
# ---------------------------------------------------------------------------
print("\nDeclared anchors — a bare integer may name the heading it means")

SAMPLE = '''deep_dive:
  plain_int: 4826
  declared: 15027  # anchor: 93-cicd-integration
  declared_with_note: 6442  # anchor: memory-loading-comparison | some note
'''
by_key = {p["key"]: p for p in resync.parse_refs(SAMPLE)}
check("a bare integer without a comment declares no anchor",
      by_key["plain_int"]["anchor"] is None)
check("`# anchor: slug` is parsed off a bare integer",
      by_key["declared"]["anchor"] == "93-cicd-integration",
      f"(got {by_key['declared']['anchor']!r})")
check("the anchor is parsed even when other notes follow it",
      by_key["declared_with_note"]["anchor"] == "memory-loading-comparison",
      f"(got {by_key['declared_with_note']['anchor']!r})")

# anchor_line must refuse an ambiguous slug rather than return the first hit.
# GitHub suffixes a repeated slug `-1`, so a duplicated slug identifies nothing.
with tempfile.TemporaryDirectory() as td:
    root_backup = resync.REPO_ROOT
    d = Path(td)
    (d / "dup.md").write_text("# A\n\n## Best Practices\n\ntext\n\n## Best Practices\n",
                              encoding="utf-8")
    (d / "uniq.md").write_text("# A\n\n## Only Once\n", encoding="utf-8")
    resync.REPO_ROOT = d
    resync._headings_cache.clear()
    check("anchor_line resolves a unique slug",
          resync.anchor_line("uniq.md", "only-once") == 3,
          f"(got {resync.anchor_line('uniq.md', 'only-once')})")
    check("anchor_line refuses a duplicated slug instead of picking the first",
          resync.anchor_line("dup.md", "best-practices") is None,
          f"(got {resync.anchor_line('dup.md', 'best-practices')})")
    check("anchor_line returns None for a slug that matches nothing",
          resync.anchor_line("uniq.md", "does-not-exist") is None)

    # hint_line is the escape hatch: a reference manually verified against one
    # specific occurrence of a duplicated heading stays resolvable, because a
    # human already did the disambiguation the slug alone cannot do. 3 real
    # references hit exactly this ("Best Practices" is duplicated 4x in the
    # guide) and were stuck reporting LOW forever under the plain heuristic
    # even though their content was hand-verified correct.
    check("hint_line resolves an ambiguous slug when it matches one candidate",
          resync.anchor_line("dup.md", "best-practices", hint_line=3) == 3,
          f"(got {resync.anchor_line('dup.md', 'best-practices', hint_line=3)})")
    check("hint_line resolves the OTHER candidate too, not just the first",
          resync.anchor_line("dup.md", "best-practices", hint_line=7) == 7,
          f"(got {resync.anchor_line('dup.md', 'best-practices', hint_line=7)})")
    check("hint_line outside the candidate set still refuses (drift is still caught)",
          resync.anchor_line("dup.md", "best-practices", hint_line=99) is None,
          f"(got {resync.anchor_line('dup.md', 'best-practices', hint_line=99)})")
    resync.REPO_ROOT = root_backup
    resync._headings_cache.clear()

# Every declared anchor in the live file must resolve AND match its stored line.
live = resync.YAML_FILE.read_text(encoding="utf-8")
declared = [r for r in resync.parse_refs(live)
            if r["type"] == "bare_int" and r["anchor"]]
check("the live reference.yaml declares at least one anchor", len(declared) > 0,
      f"(found {len(declared)})")
mismatched = []
for ref in declared:
    target = resync.anchor_line(resync.MAIN_GUIDE, ref["anchor"], hint_line=ref["old_line"])
    if target != ref["old_line"]:
        mismatched.append((ref["key"], ref["anchor"], ref["old_line"], target))
check("every declared anchor resolves to exactly its stored line",
      not mismatched, f"(mismatched {mismatched})")


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
