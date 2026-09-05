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
- the maintained French version, artifact hash, and recorded English source baseline;
- required registry fields, unique languages, source commit ancestry, and pinned Git lag;
- the declared unofficial status, attribution evidence, and coverage boundary of each community translation;
- the 6 declared whitepaper source pairs and the known French-only prefix `03`;
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

For every remote review:

1. Confirm the repository URL, maintainer, default branch, HEAD, license, and declared version.
2. Find the exact English source commit from a manifest or Git ancestry. If none is demonstrable, store a null source commit and null numeric lag instead of estimating.
3. Verify attribution in the README, license, repository description, or translation notice.
4. Record maintainer-reported coverage and a separate filesystem observation.
5. Recompute guide-only and repository-wide commit lag against `measured_at_commit`.
6. Update `last_checked_at` only after every recorded remote fact is checked.

Do not execute scripts from a community repository during an audit. Inspect source files and Git objects only.

## Paired publications

Public whitepaper sources pair by their two-digit prefix, not by translated filename. The public landing catalog contains 13 paired releases, while this repository contains 6 paired `.qmd` source prefixes and one declared French-only source. Missing source files are not counted as synchronized. Client-specific French documents without a numbered public prefix stay outside this parity gate.

Recap cards pair by source filename. PDF presence is an export concern; the translation gate compares the `.qmd` sources and their front matter.

Publication parity does not prove freshness against the full guide. Whitepapers and recap cards are topic adaptations or summaries, so their full-guide lag remains `UNKNOWN` until a dedicated content audit records a source baseline.

## Official locale gate

French is the current priority. Do not begin an official Chinese or other full-guide edition until:

- French passes `--require-current-maintained`;
- a human review covers navigation, examples, links, terminology, and untranslated residue;
- a named maintainer accepts ongoing ownership;
- the update cadence and source-commit manifest are documented;
- the landing can host stable equivalent pages.

An independently maintained translation remains a community edition even when its quality is high.

## Landing, sitemap, canonical, and `hreflang`

After changing `guide/core/translations.md`, build the landing against a clean guide worktree:

```bash
GUIDE_REPO_PATH=/absolute/path/to/clean/guide-worktree pnpm build
pnpm test
```

Verify the built output:

- `/guide/translations/` exists;
- its canonical URL points to itself;
- the XML sitemap contains the local route exactly once;
- normal links expose English, French, and all registered community adaptations;
- community repository URLs are absent from the local XML sitemap;
- no `hreflang` is emitted for a locale without equivalent pages and reciprocal annotations.

Fetch the deployed page and sitemap after deployment. A local build, pushed branch, or in-progress workflow is not deployment evidence.

## Mentions page boundary

Translation attribution belongs on the language-status page and in the registry. If the separate portfolio Mentions page lists translations, verify it independently and preserve the official versus community label. A guide or landing commit does not prove that the portfolio deployment is live.
