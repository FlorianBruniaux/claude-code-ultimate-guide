#!/usr/bin/env python3
"""
Structural validation of machine-readable/reference.yaml.

Checks YAML parseability, anchor resolution against real headings, path
existence, line-reference bounds, how far each bare integer sits from its
nearest heading, and section_maps validity.

  python3 scripts/validate-reference-yaml.py         # full report
  python3 scripts/validate-reference-yaml.py --ci    # exit 1 on any hard failure

Hard failures are: unparseable YAML, an anchor with no matching heading, a path
that does not exist, a line reference past the end of its file, or a section_maps
entry that does not resolve. Bare integers landing far from a heading are
reported but do not fail the build; that backlog is gated by
scripts/resync-reference-yaml.py instead.
"""
import os, re, sys, glob, yaml

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REF = 'machine-readable/reference.yaml'
CI = '--ci' in sys.argv
failures = 0

print("=== integrity ===")
n_new = sum(1 for _ in open(REF, encoding='utf-8'))
print(f"{REF}: {n_new} lines")

for f in ['machine-readable/reference.yaml', 'machine-readable/cowork-reference.yaml',
          'machine-readable/claude-code-releases.yaml']:
    try:
        d = yaml.safe_load(open(f, encoding='utf-8'))
        print(f"YAML OK   {f}  ({len(d)} top-level keys)")
    except Exception as e:
        print(f"YAML FAIL {f}: {e}")
        failures += 1


def headings(path):
    """
    CommonMark fence rules, not a naive toggle.

    A naive `startswith('```') -> flip` desynchronises on any file with an odd
    fence count (nested markdown examples, 4-backtick blocks containing 3-backtick
    ones). enterprise-governance.md has 51 such lines: the toggle got stuck inside
    a fence and silently dropped every heading after it, reporting 9 perfectly
    valid anchors as broken. Closing fences must match the opening char and be at
    least as long, with nothing but whitespace after them.
    """
    out = []
    fence_char, fence_len = None, 0
    for n, l in enumerate(open(path, encoding='utf-8', errors='ignore'), 1):
        s = l.lstrip()
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
        m = re.match(r'^(#{1,6})\s+(.*)$', l)
        if m:
            out.append((n, len(m.group(1)), m.group(2).strip()))
    return out


def slugs(path):
    s = set()
    for _, _, h in headings(path):
        ex = re.search(r'\{#([^}]+)\}', h)
        if ex:
            s.add(ex.group(1))
            h = re.sub(r'\{#[^}]+\}', '', h).strip()
        h = re.sub(r'`', '', h)
        h = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', h)
        s.add(re.sub(r'[^\w\s\-]', '', h.lower(), flags=re.UNICODE).strip().replace(' ', '-'))
    return s


print("\n=== anchors / paths / line refs ===")
cache, bad_a, n_a, dead, n_l, oob = {}, [], 0, [], 0, []
for i, line in enumerate(open(REF, encoding='utf-8'), 1):
    for m in re.finditer(r'"((?:guide|examples|docs)/[^"#\s]*?\.md)#([^"\s]+)"', line):
        p, a = m.groups()
        if not os.path.exists(p):
            continue
        cache.setdefault(p, slugs(p))
        n_a += 1
        if a not in cache[p]:
            bad_a.append((i, p, a))
    for m in re.finditer(r'"((?:guide|examples|machine-readable|docs|whitepapers|scripts|mcp-server)/[^"#\s]*?)(?:#[^"\s]*)?(?::(\d+))?(?:\s[^"]*)?"', line):
        p, n = m.group(1).rstrip('/'), m.group(2)
        if not (os.path.exists(p) or '*' in p):
            dead.append((i, p))
        elif n:
            n_l += 1
            t = sum(1 for _ in open(p, encoding='utf-8', errors='ignore'))
            if int(n) > t:
                oob.append((i, p, n, t))

failures += len(bad_a) + len(dead) + len(oob)
print(f"anchors  : {n_a - len(bad_a)}/{n_a} resolve")
for b in bad_a:
    print(f"   BAD  L{b[0]} {b[1]}#{b[2]}")
print(f"paths    : {len(dead)} dead")
for d in dead:
    print(f"   DEAD L{d[0]} {d[1]}")
print(f"line refs: {n_l - len(oob)}/{n_l} in bounds")
for o in oob:
    print(f"   OOB  L{o[0]} {o[1]}:{o[2]} > {o[3]}")

print("\n=== declared anchors on bare integers ===")
# A bare integer may name the heading it means as `# anchor: some-slug`. That
# turns an unverifiable position into a hard check, so the anchor itself has to
# be real: it must match exactly one heading. A slug that matches two is not a
# reference, because GitHub suffixes the repeat `-1` and the anchor would resolve
# to whichever one came first.
ug = 'guide/ultimate-guide.md'
_ug_heads = headings(ug)
n_decl, bad_decl = 0, []
for i, line in enumerate(open(REF, encoding='utf-8'), 1):
    m = re.match(r'^\s*([a-z0-9_]+):\s*(\d{3,5})\s*#.*?anchor:\s*([A-Za-z0-9._\-]+)', line)
    if not m:
        continue
    key, stored, slug = m.group(1), int(m.group(2)), m.group(3)
    n_decl += 1
    hits = [n for n, _, t in _ug_heads
            if re.sub(r'[^\w\s\-]', '',
                      re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1',
                             re.sub(r'`', '', t)).lower(),
                      flags=re.UNICODE).strip().replace(' ', '-') == slug]
    if len(hits) == 0:
        bad_decl.append((i, key, slug, 'matches no heading'))
    elif len(hits) > 1:
        bad_decl.append((i, key, slug, f'ambiguous, matches {len(hits)} headings'))
    elif hits[0] != stored:
        bad_decl.append((i, key, slug, f'stored {stored}, heading is at {hits[0]}'))
print(f"declared: {n_decl - len(bad_decl)}/{n_decl} resolve and match their line")
for b in bad_decl:
    print(f"   BAD  L{b[0]} {b[1]} -> #{b[2]}: {b[3]}")
failures += len(bad_decl)

print("\n=== bare-int refs vs nearest heading (post-repair spot check) ===")
ug = 'guide/ultimate-guide.md'
hs = headings(ug)
tot = sum(1 for _ in open(ug, encoding='utf-8'))
exact, near, far, cnt = 0, 0, [], 0
COUNT_SUFFIX = re.compile(r'_(count|counts|total|totals|num|nb|stars|pct|percent|questions|categories|version|year)$')
for i, line in enumerate(open(REF, encoding='utf-8'), 1):
    m = re.match(r'^\s*([a-z0-9_]+):\s*(\d{3,5})\s*(#.*)?$', line)
    if not m:
        continue
    key, n = m.group(1), int(m.group(2))
    if COUNT_SUFFIX.search(key) or n > tot:
        cnt += 1
        continue
    above = [h for h in hs if h[0] <= n]
    if not above:
        continue
    d = n - above[-1][0]
    if d == 0:
        exact += 1
    elif d <= 40:
        near += 1
    else:
        far.append((i, key, n, d, above[-1][2]))
print(f"land exactly on a heading : {exact}")
print(f"within 40 lines of one    : {near}")
print(f"further than 40 lines     : {len(far)}")
print(f"protected counts skipped  : {cnt}")
for f in far[:25]:
    print(f"   L{f[0]:<5} {f[1][:36]:<36} :{f[2]:<6} +{f[3]:<5} {f[4][:46]}")
if len(far) > 25:
    print(f"   ... and {len(far)-25} more")

print("\n=== section_maps block ===")
d = yaml.safe_load(open(REF, encoding='utf-8'))
sm = d.get('section_maps')
if not sm:
    print("absent (run gen-section-maps.py --apply)")
else:
    tot_a = sum(len(v) for v in sm.values())
    bad = 0
    for p, anchors in sm.items():
        if not os.path.exists(p):
            print(f"   DEAD FILE {p}")
            bad += 1
            continue
        s = slugs(p)
        for a in anchors:
            if a not in s:
                print(f"   BAD {p}#{a}")
                bad += 1
    print(f"{len(sm)} files, {tot_a} anchors, {bad} invalid")
    failures += bad

if CI:
    print(f"\n=== CI verdict: {failures} hard failure(s) ===")
    sys.exit(1 if failures else 0)
