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

**PDF stack**: Quarto → bundled Typst → PDF. Template: `whitepapers/_extensions/whitepaper/`. Bold Guy palette (warm beige + burnt orange).

**EPUB stack**: Quarto → Pandoc → EPUB3. CSS: `whitepapers/epub-styles.css`. Cover: `_extensions/whitepaper/assets/claude-code-ai-logo.jpg`.

**Available skill**: `/pdf-generator` for contextual help (YAML template, stack, troubleshooting).

**Whitepaper format**: use `--to whitepaper-typst` to select the project template. Recap cards and cheatsheets use their own formats.

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

**Sources**: `whitepapers/recap-cards/fr/*.qmd` (FR), `whitepapers/recap-cards/en/*.qmd` (EN).

**58 cards per language** in the Technical, Methodology, and Design series.

## Complete bilingual publication build

Run from the cloned repository root:

```bash
# Inventory only: 146 PDFs and 28 EPUB companions
python3 scripts/render-publications.py --list

# Build both languages; resume only when all recorded input/output hashes match
python3 scripts/render-publications.py --resume

# Check every output, source hash, one-page card, EPUB and PDF page boundary
python3 scripts/validate-publications.py

# Full guides only, using the same templates as the public downloads
python3 scripts/render-publications.py --collections guides

# A single language or collection
python3 scripts/render-publications.py --lang en --collections whitepapers cards
```

The complete catalog contains two full guides, 26 whitepapers, 116 recap cards,
and two daily cheatsheets. EPUB companions are generated for the guides and
whitepapers. Outputs, render logs, and `manifest.json` go to
`dist/publications/`, which is ignored by Git. The manifest records source and
output hashes; a successful render does not establish semantic accuracy.

Requirements: Python 3, Quarto 1.10.18 with bundled Typst, and the Inter and
JetBrains Mono fonts. The extensions select native Typst syntax highlighting
(`syntax-highlighting: idiomatic`) to preserve code lines with the custom raw-text
styles. Quarto 1.9 changed the default highlighter; see its
[Typst documentation](https://quarto.org/docs/output-formats/typst.html). `pdfinfo`, when installed, also checks readability and
records page counts. The build runs independent sources concurrently, while
PDF and EPUB rendering of one source remains sequential.

The full-guide preprocessor removes the manual English or French table of
contents and internal anchor links before rendering. Quarto supplies the PDF
table of contents. Cross-references to internal Markdown anchors are plain text
in these exports.

`scripts/generate-guide-exports.sh` remains a legacy English Pandoc export.
Use `scripts/render-publications.py` for the styled public editions and CI.

## French translation freshness

`guide/ultimate-guide.fr.md` is maintained against the recorded English source.
The bilingual build refuses to render a stale French full guide. Before marking
a refresh complete, review the complete English delta, restore any missing
sections, preserve executable examples, and review the French prose. Structural
counts alone are insufficient.

```bash
# Only after the translation review and source commit are complete
python3 scripts/check-translations.py --update-local --record-french-refresh
python3 scripts/check-translations.py --check --require-current-maintained
python3 scripts/render-publications.py --collections guides --lang fr
```

The September 2026 refresh uses Codex workers. The existing
`scripts/translate-guide.py` is a separate legacy Anthropic API tool and is not
invoked by the build. Its presence does not select the model used by Codex.

Full-guide wrappers are `whitepapers/guide-export.qmd` and
`whitepapers/guide-export-fr.qmd`. Preprocessed Markdown is generated and ignored.
See [translation maintenance](translations.md) for the evidence registry.

## Typst Templates — 3 Copies, Always Sync

`whitepapers/fr/_extensions/whitepaper/typst-template.typ` (used for FR rendering)
`whitepapers/en/_extensions/whitepaper/typst-template.typ` (used for EN rendering)
`whitepapers/_extensions/whitepaper/typst-template.typ` (fallback/reference)

**Quarto uses the `_extensions/` closest to the .qmd**: patching the root copy has no effect on fr/ or en/.

## PDF Deployment Checklist — 3 Files to Update

When pushing updated PDFs to the landing/portfolio, **3 files must always be updated together**. Missing any one of them causes old files to be served.

| File | Repo | Role |
|------|------|------|
| `florian-portfolio/public/guides/` | portfolio | Physical PDF files (copy with new versioned filename) |
| `landing/src/data/whitepapers-data.ts` | landing | Direct download buttons (`const V`, `hashedFileFr/En`) |
| `florian-portfolio/api/guides.mjs` | portfolio | **Email links**: `GUIDE_MANIFEST` stable-ID → versioned filename |

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
