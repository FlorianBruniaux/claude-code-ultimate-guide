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

The maintained English and French full guides were reviewed on **2026-09-26** at version **3.43.0**. The French refresh reconciled source changes since 3.41.1 and repaired older omissions and code fences. Its recorded source hash matches the committed English guide. This was a Codex review, not a human editorial sign-off; see the [review record](../../docs/audits/2026-09-26-bilingual-publications.md).

| Edition | Version | Maintenance and coverage |
|---------|---------|--------------------------|
| English | 3.43.0 | Canonical full guide, maintained by Florian Bruniaux |
| French | 3.43.0 | Project-maintained full guide; current against its recorded English source |
| Simplified Chinese | 3.41.0 | Independent adaptation by JAYcodr; partial and behind its recorded source |
| Ukrainian | 3.40.0 | Independent adaptation by gerasimsergey; partial, exact source commit unknown |
| Latin American Spanish | 3.32.2 | Independent adaptation by Richardls; partial and behind its recorded source |

The community repositories were last inspected on **2026-08-31**. Their current remote state has not been rechecked in this publication refresh. The [registry](../../machine-readable/translations.json) retains each maintainer, source commit or `UNKNOWN`, coverage observations, verification date and measured lag. A later English change invalidates maintained translation freshness until it is reviewed and recorded.

Character counts from the community audit are language indicators, not semantic coverage scores. A file can contain translated words while retaining English passages, and code-only files need not contain target-language characters.

All 13 English/French whitepaper source pairs and 58 recap-card pairs are now present in the repository, together with both daily cheatsheets and the French full-guide export wrapper. The print review covers commands, configuration, models, security and privacy across these adaptations. They summarize topics and are not line-equivalent translations of the full guide. Build completion and public download verification are recorded separately in the publication audit.

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

The release build runs this strict gate before rendering the French full guide. A new English source change must be reviewed in French before the gate can pass again.

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
