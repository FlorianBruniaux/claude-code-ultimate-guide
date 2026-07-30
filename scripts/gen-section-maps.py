#!/usr/bin/env python3
"""
Point 3: generate a `section_maps:` top-level block listing every H2 anchor
per thematic guide file.

Why a separate top-level block and not more deep_dive keys:
  build-guide-index.mjs iterates deep_dive and turns every string starting with
  guide/ into a Cmd+K palette entry. Adding ~600 section keys there would bloat
  the palette and reference.yaml alike. A top-level block of anchor *lists*
  (not paths) is invisible to that script, so LLMs get full section coverage
  with zero landing impact.
"""
import glob, importlib.util, os, sys

os.chdir('/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide')
REF = 'machine-readable/reference.yaml'
APPLY = '--apply' in sys.argv

# headings()/slugify() used to be copy-pasted into this file, validate-reference-yaml.py,
# and resync-reference-yaml.py: three independent implementations that had to agree by
# accident. They didn't. All three had `.strip()` before the space->hyphen replace, which
# github-slugger does not do, so a heading starting with a stripped emoji ("🔄 LLM Day-to-Day...")
# produced a slug with no leading hyphen while the real rendered id has one. 16 anchors were
# dead on both GitHub and the landing while every one of the three copies agreed the slug was
# fine, because they were all checking against each other's mistake, not against reality.
# Importing the single implementation makes that class of bug structurally impossible.
_spec = importlib.util.spec_from_file_location("resync", "scripts/resync-reference-yaml.py")
_resync = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_resync)
headings = _resync.headings  # accepts str or Path, both work with open()
slugify = _resync.slugify

SKIP_HEADINGS = {'table of contents', 'see also', 'resources', 'related resources',
                 'related sections', 'references', 'sources', 'quick jump', 'quick nav'}


files = sorted(p for p in glob.glob('guide/**/*.md', recursive=True)
               if not p.endswith('.fr.md') and not p.endswith('README.md')
               and p != 'guide/ultimate-guide.md')

block = []
block.append('# ════════════════════════════════════════════════════════════════')
block.append('# SECTION MAPS - every H2 anchor per thematic guide file')
block.append('# Purpose: let an LLM see what is inside a file before reading it, and')
block.append('#          build a valid deep link without guessing the slug.')
block.append('# Not consumed by the landing search index (build-guide-index.mjs only')
block.append('# reads deep_dive string values), so this costs nothing in the Cmd+K palette.')
block.append('# Regenerate with: python3 scripts/gen-section-maps.py --apply')
block.append('# ════════════════════════════════════════════════════════════════')
block.append('section_maps:')

total_anchors = 0
dupes = []
for p in files:
    hs = [h for h in headings(p) if h[1] == 2 and h[2].lower() not in SKIP_HEADINGS]
    if not hs:
        continue
    slugs, seen = [], set()
    for h in hs:
        s = slugify(h[2])
        if not s:
            continue
        if s in seen:
            dupes.append((p, s))
            continue
        seen.add(s)
        slugs.append(s)
    if not slugs:
        continue
    total_anchors += len(slugs)
    block.append(f'  "{p}":')
    for s in slugs:
        block.append(f'    - "{s}"')

print(f"{len(files)} guide files scanned")
print(f"{total_anchors} H2 anchors mapped")
if dupes:
    print(f"{len(dupes)} duplicate slugs skipped (ambiguous, GitHub would suffix -1):")
    for d in dupes[:15]:
        print(f"   {d[0]} -> #{d[1]}")

new_block = '\n'.join(block) + '\n'

src = open(REF, encoding='utf-8').read()
marker = '\n# ════════════════════════════════════════════════════════════════\n# SECTION MAPS'
if marker in src:
    head = src.split(marker)[0].rstrip('\n')
    # section_maps is appended last, so everything after it is regenerated
    out = head + '\n\n' + new_block
else:
    out = src.rstrip('\n') + '\n\n' + new_block

if APPLY:
    open(REF, 'w', encoding='utf-8').write(out)
    print(f"\nAPPLIED: section_maps block written to {REF}")
else:
    print("\nDRY RUN (pass --apply to write)")
    print("\npreview (first 30 lines):")
    for l in block[:30]:
        print("  " + l)
