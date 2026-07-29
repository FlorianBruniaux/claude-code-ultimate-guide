#!/usr/bin/env python3
"""
Repair + migrate reference.yaml positional references.

Two ref shapes exist:
  A) string form   key: "guide/foo/bar.md:123"   -> consumed by the landing (line + anchor stripped)
  B) bare int form key: 19597                    -> ultimate-guide.md line, LLM-only, landing ignores it

Strategy:
  A) migrate to "guide/foo/bar.md#anchor" when a confident heading match exists,
     otherwise repair the line number if it drifted, otherwise leave untouched.
  B) repair the line number when a confident heading match exists; never convert
     (converting would inject ~200 new entries into the landing search palette).

Confidence = normalized token overlap between the YAML key name and the heading text,
with a required margin over the runner-up so ambiguous cases are left alone.
"""
import os, re, sys, difflib

os.chdir('/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide')
REF = 'machine-readable/reference.yaml'
APPLY = '--apply' in sys.argv

STOP = {'guide', 'section', 'ref', 'line', 'the', 'and', 'for', 'with', 'md',
        'file', 'doc', 'docs', 'link', 'url', 'path'}

# Bare integers in reference.yaml are NOT all line numbers. A few are quantities
# (resource_evaluations_count: 120, ui_ux_pro_max_stars: 33700). Rewriting one of
# those with a line number is silent data corruption.
#
# Match on SUFFIX only, and keep the list tight. A substring match is too greedy:
# it swallowed memory_files, cost_optimization and ui_ux_pro_max_guide, which are
# all genuine line refs that then silently stopped being repaired. Protecting a
# real ref is a quieter failure than corrupting a count, so the guard must be
# narrow and paired with the out-of-bounds check below.
COUNT_SUFFIX = re.compile(
    r'_(count|counts|total|totals|num|nb|stars|pct|percent|questions|'
    r'categories|version|year)$')


def is_count_key(key, value, max_lines):
    if COUNT_SUFFIX.search(key):
        return True
    # a value past the end of the target file cannot be a line number
    return value > max_lines


def headings(path):
    """
    CommonMark fence rules. A naive `startswith('```') -> flip` desynchronises on
    any file with an odd fence count and then silently drops every heading after
    it, which makes best_match pick from an incomplete set. enterprise-governance.md
    (51 fence lines) lost 9 real sections that way.
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


def slugify(h):
    ex = re.search(r'\{#([^}]+)\}', h)
    if ex:
        return ex.group(1)
    h = re.sub(r'`', '', h)
    h = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', h)
    return re.sub(r'[^\w\s\-]', '', h.lower(), flags=re.UNICODE).strip().replace(' ', '-')


def toks(s):
    s = re.sub(r'[^\w\s]', ' ', s.lower())
    return [t for t in re.split(r'[\s_]+', s) if len(t) > 2 and t not in STOP]


def score(key, heading_text):
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


hcache = {}


def get_headings(p):
    if p not in hcache:
        hcache[p] = headings(p)
    return hcache[p]


def best_match(path, key, cur_line):
    """Return (line, slug, conf, margin, text) for the best heading matching `key`."""
    hs = get_headings(path)
    if not hs:
        return None
    scored = sorted(((score(key, h[2]), h) for h in hs), key=lambda x: -x[0])
    top_s, top_h = scored[0]
    runner = scored[1][0] if len(scored) > 1 else 0.0
    # tie-break identical scores by proximity to the current line
    ties = [h for s, h in scored if abs(s - top_s) < 1e-9]
    if len(ties) > 1:
        ties.sort(key=lambda h: abs(h[0] - cur_line))
        top_h = ties[0]
        runner = top_s  # ambiguous by definition
    return (top_h[0], slugify(top_h[2]), top_s, top_s - runner, top_h[2])


MIN_CONF = 0.60
MIN_MARGIN = 0.15

lines = open(REF, encoding='utf-8').read().split('\n')
mig, rep, skip, amb, prot = [], [], [], [], []

for i, line in enumerate(lines):
    # form A: key: "path:NNN"  (allow trailing comment)
    ma = re.match(r'^(\s*)([a-z0-9_]+):\s*"((?:guide|examples|docs|whitepapers|scripts)/[^"#\s]+):(\d+)"(.*)$', line)
    # form B: key: NNN
    mb = re.match(r'^(\s*)([a-z0-9_]+):\s*(\d{3,5})\s*(#.*)?$', line)

    if ma:
        ind, key, path, n, tail = ma.group(1), ma.group(2), ma.group(3), int(ma.group(4)), ma.group(5)
        if not os.path.exists(path):
            skip.append((i + 1, key, path, n, 'file missing'))
            continue
        bm = best_match(path, key, n)
        if not bm:
            skip.append((i + 1, key, path, n, 'no headings'))
            continue
        hl, slug, conf, margin, text = bm
        if conf >= MIN_CONF and margin >= MIN_MARGIN:
            lines[i] = f'{ind}{key}: "{path}#{slug}"{tail}'
            mig.append((i + 1, key, f'{path}:{n}', f'{path}#{slug}', round(conf, 2), n, hl, text))
        else:
            amb.append((i + 1, key, path, n, round(conf, 2), round(margin, 2), text))

    elif mb:
        ind, key, n, tail = mb.group(1), mb.group(2), int(mb.group(3)), (mb.group(4) or '')
        path = 'guide/ultimate-guide.md'
        ug_lines = sum(1 for _ in open(path, encoding='utf-8', errors='ignore'))
        if is_count_key(key, n, ug_lines):
            why = 'count suffix' if COUNT_SUFFIX.search(key) else f'>{ug_lines} lines'
            prot.append((i + 1, key, n, why))
            continue
        bm = best_match(path, key, n)
        if not bm:
            continue
        hl, slug, conf, margin, text = bm
        if conf >= MIN_CONF and margin >= MIN_MARGIN:
            if hl != n:
                sep = '  ' if tail else ''
                lines[i] = f'{ind}{key}: {hl}{sep}{tail}'
                rep.append((i + 1, key, n, hl, round(conf, 2), text))
        else:
            amb.append((i + 1, key, path, n, round(conf, 2), round(margin, 2), text))

print(f"MIGRATED to anchors : {len(mig)}")
print(f"REPAIRED line nums  : {len(rep)}")
print(f"AMBIGUOUS (left)    : {len(amb)}")
print(f"PROTECTED (counts)  : {len(prot)}")
print(f"SKIPPED             : {len(skip)}")

print("\n--- protected: integer keys that are quantities, never rewritten ---")
for p in prot:
    print(f"  L{p[0]:<5} {p[1][:44]:<44} = {p[2]:<8} ({p[3]})")

print("\n--- migrations (path:N -> path#anchor) ---")
for m in mig:
    drift = m[6] - m[5]
    d = f"  [drift {drift:+d} lines]" if abs(drift) > 30 else ""
    print(f"  L{m[0]:<5} {m[1][:40]:<40} {m[2].split('/')[-1]:<34} -> #{m[3].split('#')[1][:44]:<44} conf={m[4]}{d}")

print("\n--- repaired ultimate-guide.md line numbers ---")
for r in rep:
    print(f"  L{r[0]:<5} {r[1][:40]:<40} {r[2]} -> {r[3]}  ({r[3]-r[2]:+d})  conf={r[4]}  {r[5][:50]}")

print("\n--- ambiguous, left untouched (ALL) ---")
for a in amb:
    print(f"  L{a[0]:<5} {a[1][:38]:<38} {a[2].split('/')[-1]}:{a[3]:<6} conf={a[4]} margin={a[5]}  near={a[6][:44]}")

if APPLY:
    open(REF, 'w', encoding='utf-8').write('\n'.join(lines))
    print("\nAPPLIED to " + REF)
else:
    print("\nDRY RUN (pass --apply to write)")
