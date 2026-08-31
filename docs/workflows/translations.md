# Translation Status Workflow

The repository separates three facts that are easy to confuse:

1. **File parity** checks whether both languages contain the expected publication files.
2. **Metadata parity** checks whether a paired French and English publication records the same guide baseline. A language-specific `wp-version` may differ and is reported separately.
3. **Translation freshness** checks which canonical source version and checksum produced a translated full guide.

The machine-readable registry is [`machine-readable/translations.json`](../../machine-readable/translations.json). The public status page is [`guide/core/translations.md`](../../guide/core/translations.md).

## Local check

```bash
python3 scripts/check-translations.py --check
```

This command verifies:

- the canonical English version and SHA-256 against `VERSION` and `guide/ultimate-guide.md`;
- the maintained French version and its recorded English source baseline;
- the declared status of each community translation;
- public whitepaper prefixes 00 to 12 in French and English;
- French and English recap-card source filenames;
- paired guide baseline and `lang` metadata, plus language-specific whitepaper revision differences.

A translation that is accurately marked `stale` does not fail the default gate. The command still prints the lag. Use the strict form before publishing a maintained translated full guide:

```bash
python3 scripts/check-translations.py --check --require-current-maintained
```

## After changing the English full guide

Refresh local facts without claiming that a translation was regenerated:

```bash
python3 scripts/check-translations.py --update-local
```

This updates the canonical version and checksum, reads the local French version, and recomputes its status. It does not alter `translated_from` or `last_full_refresh_at`.

## After regenerating the French full guide

`scripts/translate-guide.py` records its cache input checksum. It refuses to reuse chunks created from another source version or model. After a complete translation, it calls:

```bash
python3 scripts/check-translations.py --update-local --record-french-refresh
```

That command binds the French output to the current English version and checksum. Run the strict check before exporting PDF or EPUB.

## Community translation review

Do not infer synchronization from the repository modification date alone. Record the following fields after reviewing the remote project:

- reported version;
- upstream commit or source baseline when available;
- remote head commit;
- last observed upstream synchronization date;
- coverage statement;
- review date.

Update the corresponding object in `machine-readable/translations.json`. The repository CI validates the declared state but does not contact third-party repositories during a build.

## Paired publications

Public whitepapers pair by their two-digit prefix, not by translated filename. Client-specific French documents without a numbered public prefix stay outside this parity gate.

Recap cards pair by source filename. PDF presence is an export concern; the translation gate compares the `.qmd` sources and their front matter.
