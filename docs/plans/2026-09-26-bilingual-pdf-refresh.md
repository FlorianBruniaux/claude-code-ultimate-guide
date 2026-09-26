# Bilingual PDF refresh

Status: in progress. Owner: Codex coordinator. Starting baseline: published guide 3.43.0 and the September 24 command/model audit. The refresh also corrects source-backed defects discovered in the canonical English guide; French must include those corrections before its final source hash is recorded. Uncommitted work in the primary checkout is excluded from this publication baseline.

## Deliverables

| Collection | English | French | Total PDFs |
|------------|---------|--------|------------|
| Full guide | 1 | 1 | 2 |
| Numbered whitepapers | 13 | 13 | 26 |
| Recap cards | 58 | 58 | 116 |
| Daily cheatsheet | 1 | 1 | 2 |
| Total | 73 | 73 | 146 |

EPUB companions for the full guides and whitepapers must use the same reviewed source. The September 24 refresh already rebuilt 22 affected PDFs; the broader collection still requires review. A successful render alone does not establish translation freshness.

## Ownership

| Owner | Files and responsibility |
|-------|--------------------------|
| English Codex worker | `whitepapers/en/*.qmd`, `whitepapers/recap-cards/en/*.qmd`: audit active guidance, preserve historical evidence, update affected sources |
| French Codex worker | `guide/ultimate-guide.fr.md` and French recap cards: compare the recorded English baseline with the frozen current source, translate additions, reconcile previous targeted corrections |
| French print worker | `whitepapers/fr/*.qmd` and `whitepapers/fr/fiches/*.qmd`: complete source review and parity with the English corrections |
| Coordinator | Shared templates, export scripts, translation registry, validation, changelogs, and deployment |

Workers must preserve other edits and use separate intermediate output directories. Only the coordinator changes shared metadata or publishes. Translation uses Codex; the legacy Anthropic translation script is not part of this execution.

## Execution checklist

- [x] Inspect the current checkout and isolate work from unrelated edits.
- [x] Load the export and translation workflows.
- [x] Recover public numbered QMD sources and the French full-guide wrapper that were missing from version control.
- [x] Start the English and French Codex workers.
- [x] Review and track every public source needed by a clean checkout.
- [x] Complete French full-guide catch-up and restore historical omissions.
- [x] Complete English derivative review.
- [x] Reconcile French derivatives with the same technical baseline.
- [x] Validate translation coverage, unchanged code/identifiers, figures, links, and navigation.
- [ ] Refresh source provenance from real commits after semantic review.
- [x] Make the full-guide build support both languages and reject a stale French edition.
- [ ] Generate 146 PDFs and the corresponding full-guide/whitepaper EPUBs with a manifest of source and output hashes.
- [ ] Check page counts, text extraction, language metadata, missing glyphs, wide tables, code blocks, and representative rendered pages. Every recap card must remain one page.
- [ ] Rebuild series ZIPs, synchronize download manifests and displayed page counts.
- [ ] Run the guide, MCP, landing, public-path, and download integrity checks.
- [ ] Commit and push the scoped changes, then verify deployment and live artifact hashes.

## Findings during execution

- The previous French baseline contained missing sections, untranslated passages, and broken code fences. The refresh restores these in addition to translating recent English changes.
- Fourteen top-level public inputs and nine included French sheets were absent from Git. They are recovered and included in the clean-checkout inventory.
- Quarto's changed default syntax highlighter conflicted with the custom templates. Native Typst highlighting restores code-block line breaks.
- The first English guide and recap-card renders succeeded. Final artifacts must be rebuilt after all content corrections.

## Acceptance gates

The French full guide stays `stale` until its semantic catch-up is complete. Structural parity, a version change, or an artifact hash is insufficient. Changes in one language must not alter code, dates, amounts, sources, or evidence limits silently.

The publication inventory must contain 146 distinct PDF outputs without name collisions. All input files must be available from a clean checkout. Derived downloads must resolve to those exact reviewed outputs. The portfolio download map, landing buttons, and series archives must change together. Keep existing public artifact URLs available.

The final report must list changed files, commits, checks, source baseline, remaining limitations, and live publication results. Do not treat a pushed commit as evidence that deployment succeeded.

## References

- [Export workflow](../workflows/whitepaper-build.md)
- [Translation provenance and freshness](../workflows/translations.md)
- [September command/model audit](../audits/2026-09-24-commands-models.md)
