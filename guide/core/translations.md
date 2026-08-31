---
title: "Translations and Language Status"
description: "Canonical, maintained, and community translations of the Claude Code Ultimate Guide, with explicit version and coverage status"
tags: [translations, languages, french, chinese, ukrainian, community]
---

# Translations and Language Status

The English guide is the canonical edition. The French edition is maintained in this repository. Chinese and Ukrainian editions are independent community projects that credit this guide and manage their own release schedules.

**Status checked:** 2026-08-31. The machine-readable source is [`machine-readable/translations.json`](../../machine-readable/translations.json).

| Language | Edition | Version | Last full sync | Current state | Entry point |
|---|---|---:|---:|---|---|
| English | Canonical | 3.43.0 | 2026-08-30 | Current | [Read the English guide](../ultimate-guide.md) |
| Français | Maintained here | 3.41.1 | 2026-07-09 | Behind canonical | [Lire le guide français](../ultimate-guide.fr.md) |
| 简体中文 | Community, unofficial | 3.41.0 | 2026-05-23 | Behind canonical, 23 of 26 priority groups reported complete | [JAYcodr/claude-code-ultimate-guide-zh](https://github.com/JAYcodr/claude-code-ultimate-guide-zh) |
| Українська | Community, unofficial | 3.40.0 | 2026-05-19 | Behind canonical | [gerasimsergey/claude-code-ultimate-guide-ua](https://github.com/gerasimsergey/claude-code-ultimate-guide-ua) |

## Chinese community edition

The [Simplified Chinese repository maintained by JAYcodr](https://github.com/JAYcodr/claude-code-ultimate-guide-zh) is the most complete Chinese adaptation found during the 2026-08-31 review. It credits the original guide, records its upstream baseline, provides an upstream synchronization script, and publishes a translation status file.

The project reports 23 of 26 priority groups complete. The quiz, resource evaluations, and machine-readable references are not translated in that snapshot. Its version 3.41.0 predates the canonical 3.43.0 edition. This guide links to the project as a useful community resource, not as an official or synchronized edition.

## What is not synchronized yet

The maintained French guide is complete for the English 3.41.1 baseline. It does not yet include English changes introduced after that baseline, including the latest pricing, version-control, tool-search, repository-harness, cross-session messaging, and safe event-delegation additions.

The Chinese and Ukrainian repositories also predate 3.43.0. Their maintainers control their content, update cadence, licensing decisions, and publication process. A matching version number remains a weak signal until the maintainer records the upstream commit or source checksum used for the translation.

## Publication coverage

The full guide and the smaller publications follow different schedules:

| Publication | Languages | Parity rule |
|---|---|---|
| Full guide | English, French | Version, source checksum, and last full refresh are recorded |
| Public whitepapers 00 to 12 | French, English | Every public numeric prefix must exist in both languages and record the same guide baseline |
| Recap cards | French, English | Every source card must exist in both languages and pair metadata must match |
| Community adaptations | Chinese, Ukrainian | Remote version, last observed sync, coverage, and repository commit are recorded |

Publication parity does not imply freshness. A French and English whitepaper pair may be internally consistent while both files intentionally record an older guide baseline. The `wp-version` field belongs to each language edition and may differ when one edition receives a language-specific correction.

## Maintainer workflow

Run the translation check before publishing:

```bash
python3 scripts/check-translations.py --check
```

Use the strict gate before publishing a new maintained French full-guide export:

```bash
python3 scripts/check-translations.py --check --require-current-maintained
```

The default check accepts a declared stale translation and reports it clearly. It fails on an incorrect version, source checksum, language pair, missing paired publication, or status that contradicts the recorded evidence.

For the complete update procedure, see [`docs/workflows/translations.md`](../../docs/workflows/translations.md).

## Contributing a translation

Open an issue or pull request with the language, repository URL, maintainer, license, source version or commit, last synchronization date, and a short coverage statement. Community editions remain independently maintained unless the repository owners agree on a shared release process.

The canonical guide uses [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). A translation must preserve attribution and comply with that license.
