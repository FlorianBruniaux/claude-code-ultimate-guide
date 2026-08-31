---
title: "Translations and Language Governance"
description: "Verified inventory, freshness status, attribution, and maintenance rules for official and community language editions"
tags: [translations, localization, governance, community]
---

# Translations and Language Governance

English is the canonical language of the Claude Code Ultimate Guide. The French full guide is the only project-maintained translation. Chinese, Ukrainian, and Latin American Spanish repositories listed here are independent community adaptations. They are not official project editions and they are not maintained by Anthropic.

The machine-readable source of truth is [`machine-readable/translations.json`](../../machine-readable/translations.json). Its offline validator checks recorded versions, source hashes, source commits, Git lag, and paired publication metadata:

```bash
python3 scripts/check-translations.py --check
```

That command validates the evidence in the registry. It does not review translation quality or refresh remote repositories.

## Read an Edition

- [English canonical guide](../ultimate-guide.md)
- [French project-maintained guide](../ultimate-guide.fr.md)
- [Simplified Chinese community adaptation](https://github.com/JAYcodr/claude-code-ultimate-guide-zh)
- [Ukrainian community adaptation](https://github.com/gerasimsergey/claude-code-ultimate-guide-ua)
- [Latin American Spanish community adaptation](https://github.com/Richardls/claude-code-ultimate-guide-es)

## Verified Inventory

Snapshot date: **2026-08-31**. Lag is measured from the recorded English source commit to canonical snapshot `fb3c671cc742ce21959ebab48d3829df64250ed7`. A guide commit changed `guide/ultimate-guide.md`; repository commits include every path. Pinning the measurement commit keeps the evidence reproducible after unrelated repository commits. Any later change to the canonical guide still invalidates its recorded commit and hash.

| Language | Maintainer | Status | Version | Recorded English source | Coverage evidence | Known lag |
|---|---|---|---:|---|---|---|
| English (`en`) | Florian Bruniaux | Project canonical | 3.43.0 | `7a9f55dd39db2e075274114c3be115fe04dbfdb0` | Complete canonical full guide | Current |
| French (`fr`) | Florian Bruniaux | Project-maintained translation | 3.41.1 | `d05a95c6c58cc1bcdb4b5db9aa76ad5a119baec6` | Full guide at the recorded source; semantic review not automated | **Stale: 17 guide commits, 193 repository commits** |
| Simplified Chinese (`zh-CN`) | [JAYcodr](https://github.com/JAYcodr/claude-code-ultimate-guide-zh) | Unofficial community adaptation | 3.41.0 | `7b43b9c10b241f8e196e27651e3fea6079a48d26` | Maintainer reports 23 of 26 priority groups; audit found Han characters in 154 of 520 Markdown files | **Stale: 31 guide commits, 257 repository commits** |
| Ukrainian (`uk`) | [gerasimsergey](https://github.com/gerasimsergey/claude-code-ultimate-guide-ua) | Unofficial community adaptation | 3.40.0 | `UNKNOWN` | 92 Ukrainian sidecars among 559 Markdown files; 110 files contain Cyrillic | **Exact commit lag UNKNOWN** |
| Latin American Spanish (`es-419`) | [Richardls](https://github.com/Richardls/claude-code-ultimate-guide-es) | Unofficial community adaptation | 3.32.2 | `11dadc28156112cb17cf2935244b3f9d6ccf01ee` | 330 of 335 Markdown files contain Spanish diacritics; the translation commit reports about 360 files | **Stale: 115 guide commits, 525 repository commits** |

The file counts are target-script indicators, not semantic coverage scores. A file can contain a target-language character while retaining untranslated passages. Conversely, code-only files can be correctly adapted without target-language prose.

The public landing catalog lists 13 French and English whitepaper pairs and 58 French and English recap-card pairs. This repository contains only 6 paired whitepaper `.qmd` sources plus one French-only source with prefix `03`; the remaining public whitepaper source files are not present here. All 58 recap-card source pairs are present. These publications are topic adaptations and summaries, not line-equivalent translations of the full guide. Their content freshness against the canonical guide is `UNKNOWN` until a dedicated content audit records a source baseline.

## Chinese Attribution and Source Correction

The Chinese repository's README explicitly identifies the work as a Chinese translation, credits Florian Bruniaux, links the original repository, and keeps the CC BY-SA 4.0 license. Its attribution is therefore present.

Its `TRANSLATION_STATUS` file labels `dbeb30c` as the upstream commit. Git history shows that `dbeb30c` is the community repository's first Chinese README translation commit. The parent, `7b43b9c10b241f8e196e27651e3fea6079a48d26`, is the matching English source baseline. The registry records the parent and preserves this evidence note so the incorrect label is not repeated as fact.

Attribution and freshness are separate questions. Correct attribution does not make an edition official or current.

## Official Translation Priority

The next translation investment is French maintenance, not an official Chinese edition. Before another official locale starts, the French full guide must meet both gates:

1. The recorded source version and SHA-256 must match the English canonical guide.
2. A documented review must cover navigation, examples, links, terminology, and visible untranslated sections.

Run the strict gate when planning a release or a new official locale:

```bash
python3 scripts/check-translations.py --check --require-current-maintained
```

This strict command currently fails because French is behind English. That failure is expected evidence, not a broken validator.

## Official and Community Labels

Within this registry, `official` means maintained by this guide project. It never means official Anthropic documentation. A community adaptation remains `community` unless its maintainer, review process, source baseline, release workflow, and ongoing ownership are explicitly transferred and accepted.

Community links must display the target language, independent maintainer, unofficial status, last verification date, version, source commit or `UNKNOWN`, coverage boundary, and known lag.

## Language Navigation and SEO

Readers can use normal links between this page, the English canonical guide, the maintained French file, and community repositories. The site does not publish `hreflang` for community adaptations because they are cross-domain, not demonstrably page-equivalent, not synchronized, and do not provide verified reciprocal annotations.

Every locally hosted page keeps a self-referencing canonical URL. Add `hreflang` only when equivalent indexable pages exist, reciprocal links are verified, and the locale pair has coordinated maintenance. Do not use `x-default` as a substitute for that proof.

The landing XML sitemap should contain the local translation-status page after deployment. Community repository URLs do not belong in the local sitemap.

## Evidence Boundary

The public-repository discovery pass searched GitHub repository names and README attribution, then inspected the repositories found. It identified the three community adaptations above. Private, renamed, unindexed, and non-GitHub translations remain outside the measured scope.

The last verification date is not a synchronization claim. Remote repository heads and coverage observations can change after the snapshot. Follow the refresh workflow in [`docs/workflows/translations.md`](../../docs/workflows/translations.md) before updating them.
