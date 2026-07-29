# Whitepaper & Guide Export Build Reference

Commands and stack details for generating PDFs, EPUBs, and recap cards from source `.qmd` files.

## Whitepaper Generation (PDF + EPUB)

```bash
# --- PDF (default format: whitepaper-typst → Typst → PDF) ---

# Single file
cd whitepapers/fr && quarto render 00-introduction-serie.qmd

# All FR whitepapers
cd whitepapers/fr && quarto render *.qmd

# All EN whitepapers
cd whitepapers/en && quarto render *.qmd

# Preview with hot-reload
cd whitepapers/fr && quarto preview 00-introduction-serie.qmd

# Batch with error summary (loop)
cd whitepapers/fr && for f in *.qmd; do echo "→ $f" && quarto render "$f" 2>&1 | grep -E "(Output created|ERROR)"; done

# --- EPUB (format: epub → Pandoc → EPUB3) ---

# Single file
cd whitepapers/fr && quarto render 00-introduction-serie.qmd --to epub

# All EPUBs (FR + EN) → epub-output/{fr,en}/
cd whitepapers && ./render-epub.sh all
cd whitepapers && ./render-epub.sh fr   # French only
cd whitepapers && ./render-epub.sh en   # English only
```

**PDF stack**: Quarto → Typst 0.13 → PDF. Template: `whitepapers/_extensions/whitepaper/`. Bold Guy palette (warm beige + burnt orange).

**EPUB stack**: Quarto → Pandoc → EPUB3. CSS: `whitepapers/epub-styles.css`. Cover: `_extensions/whitepaper/assets/claude-code-ai-logo.jpg`.

**Available skill**: `/pdf-generator` for contextual help (YAML template, stack, troubleshooting).

**Critical**: Always use `--to whitepaper-typst`, never `--to pdf`. See `MEMORY.md` for details.

## Recap Cards (Thematic Memo Sheets)

Printable A4 1-page sheets, midway between cheatsheet and whitepapers.

```bash
# Single card
cd whitepapers/recap-cards/fr && quarto render 01-commandes-essentielles.qmd --to recap-card-typst

# All FR cards (via script)
cd whitepapers/recap-cards && ./render-recap-cards.sh fr

# All cards (FR + EN)
cd whitepapers/recap-cards && ./render-recap-cards.sh all
```

**Stack**: `recap-card` extension (`whitepapers/_extensions/recap-card/`). Format `recap-card-typst`. Same Bold Guy palette.

**Sources**: `whitepapers/recap-cards/fr/*.qmd` (FR), `whitepapers/recap-cards/en/*.qmd` (EN coming).

**25 cards planned** — 5 Phase 1-2 prototypes delivered: 01, 03, 04, 06, 25.

## Guide Export (EPUB + PDF, full ~25K lines)

Generates `guide/ultimate-guide.md` as EPUB and/or PDF. Output goes to `dist/`.

```bash
# Generate both EPUB and PDF (default)
./scripts/generate-guide-exports.sh

# EPUB only
./scripts/generate-guide-exports.sh --epub

# PDF only
./scripts/generate-guide-exports.sh --pdf

# Custom output directory
./scripts/generate-guide-exports.sh -o /tmp/exports

# Verbose
./scripts/generate-guide-exports.sh -v
```

**Stack**: pandoc → EPUB3 (488K) and pandoc + Typst → PDF (2.9 MB).

**Dependency**: `brew install pandoc` (macOS). Typst is auto-detected from Quarto's bundled binary if not installed standalone.

**PDF note**: Internal anchor links are stripped before PDF rendering (Typst label compatibility). The PDF is purely sequential — no clickable cross-refs, but fully readable with TOC.

**Note**: Different from whitepaper EPUBs — this generates the full guide, not individual focused documents. `dist/` is gitignored.

## French Guide Translation + Export

`guide/ultimate-guide.fr.md` is a French translation of the full guide, generated via the Anthropic API.

```bash
# 1. Translate (or re-translate after updates)
#    Resumes from .translation-cache/ if interrupted
python3 scripts/translate-guide.py

# 2. Preprocess for Quarto (strips links, escapes @citations, fixes lists)
python3 scripts/preprocess-guide.py \
  --input guide/ultimate-guide.fr.md \
  --output whitepapers/guide-content-fr.md

# 3. Render PDF (Bold Guy template, ~3.7 MB)
cd whitepapers && quarto render guide-export-fr.qmd --to whitepaper-typst

# 4. Render EPUB (optional)
cd whitepapers && quarto render guide-export-fr.qmd --to epub
```

**Key files**:
- `scripts/translate-guide.py` (chunked translation, claude-sonnet-5, retry x3; cost per run not reverified since the model bump, was ~$3/run on claude-sonnet-4-6)
- `whitepapers/guide-export-fr.qmd` — QMD wrapper (lang: fr)
- `whitepapers/guide-content-fr.md` — preprocessed content (gitignored, generated)

**Known issue**: `strip_inline_toc` in preprocess-guide.py looks for EN headings — won't strip the FR TOC section, minor visual artifact only.

## Typst Templates — 3 Copies, Always Sync

`whitepapers/fr/_extensions/whitepaper/typst-template.typ` (used for FR rendering)
`whitepapers/en/_extensions/whitepaper/typst-template.typ` (used for EN rendering)
`whitepapers/_extensions/whitepaper/typst-template.typ` (fallback/reference)

**Quarto uses the `_extensions/` closest to the .qmd** — patching the root copy has no effect on fr/ or en/.

## PDF Deployment Checklist — 3 Files to Update

When pushing updated PDFs to the landing/portfolio, **3 files must always be updated together**. Missing any one of them causes old files to be served.

| File | Repo | Role |
|------|------|------|
| `florian-portfolio/public/guides/` | portfolio | Physical PDF files (copy with new versioned filename) |
| `landing/src/data/whitepapers-data.ts` | landing | Direct download buttons (`const V`, `hashedFileFr/En`) |
| `florian-portfolio/api/guides.mjs` | portfolio | **Email links** — `GUIDE_MANIFEST` stable-ID → versioned filename |

**`guides.mjs` is the one that's easy to forget.** It controls what URL is sent by email when a user subscribes. Old links in emails redirect through `/api/guides?id=...`, so updating this file retroactively fixes all past email recipients too.

```bash
# Verify all 3 are in sync after an update:
grep "const V" landing/src/data/whitepapers-data.ts          # should show new version
grep "08-agent-teams.en" florian-portfolio/api/guides.mjs    # should show new version
ls florian-portfolio/public/guides/ | grep "v3.40.0" | wc -l # should show 18+ files
```

## Ebook Versioning

Each ebook has its own version, independent from the guide version.

**Two frontmatter fields**:
- `version: "3.30.0"` → guide version (synced via `./scripts/sync-version.sh`)
- `wp-version: "1.0.0"` → ebook version (bump manually)

**Update workflow**:
1. Bump `wp-version` in the `.qmd` frontmatter
2. Add an entry to `whitepapers/CHANGELOG.md`
3. Rebuild: `cd whitepapers/fr && quarto render XX.qmd --to whitepaper-typst`

**Semver convention**: MAJOR = structural rewrite, MINOR = new sections/angles, PATCH = minor fixes.
