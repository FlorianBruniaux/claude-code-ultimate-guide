# Bilingual publication refresh

Review date: September 26, 2026. Guide version: 3.43.0.

## Scope

The catalog contains 146 PDFs: two full guides, 26 numbered whitepapers,
116 recap cards and two daily cheatsheets. The guides and whitepapers also
have 28 EPUB companions. Six archives group the recap cards by language
and series.

Public sources now include all 13 whitepapers and 58 cards in each language.
Fourteen top-level QMD inputs and nine included French sheets were recovered
from previously ignored files so a clean checkout can build the catalog.

## Full-guide review

The French refresh compared its recorded English 3.41.1 baseline with the
current canonical guide and reconciled 372 source-delta spans. It restored
missing sections, examples and historical code-fence boundaries, then
incorporated the canonical factual corrections made during the print audit.

The review covered current commands, provider-specific model aliases,
context and pricing, effort persistence, memory paths, skill invocation,
permissions, hooks, task coordination and data boundaries. Historical
model-specific observations remain dated rather than relabeled as current
measurements.

Both guides expose 1,133 Markdown headings. Their numbered sections align,
and local fragment links resolve after correcting stale section references
and adding explicit anchors to the French guide. These structural checks
support the translation review; they do not establish semantic equivalence
on their own.

The [translation registry](../../machine-readable/translations.json) binds
the French artifact to the committed canonical source. It records the
review separately from source-hash validation. The work was performed with
Codex and does not constitute a human editorial sign-off. Unchanged
historical claims were not all independently re-verified.

## Print corrections

The source audit checks every catalog QMD and the included French sheets.
Corrections address obsolete command names, invalid configuration examples,
current model behavior, and unsupported security or privacy guarantees.
In particular, hook warnings must not be described as preventive blocks,
session forks must not be presented as filesystem isolation, and local
instruction files must not be confused with policy enforcement.

Primary references include the official [hook schema](https://code.claude.com/docs/en/hooks),
[permissions](https://code.claude.com/docs/en/permissions),
[memory documentation](https://code.claude.com/docs/en/memory),
[model configuration](https://code.claude.com/docs/en/model-config) and
[API pricing](https://platform.claude.com/docs/en/about-claude/pricing).

## Build and verification

The renderer records source dependencies, template and font hashes,
Quarto/Typst versions, output hashes and page counts. A resumed build only
reuses an output when its evidence still matches. French full-guide builds
first require the maintained-translation freshness gate.

Native Typst syntax highlighting replaces the incompatible default
highlighter that collapsed code-block line breaks. Markdown reader settings
preserve lists that immediately follow a paragraph. The guide preprocessor
handles French contents headings and nested fenced examples.

Validation checks the complete inventory, file integrity, source freshness,
one-page recap cards, extractable PDF text, text outside page boundaries,
EPUB language metadata and archive structure. Geometry checks cannot detect
all overlapping content or poor spacing; representative page images also
require visual review.

Publication status and final validation results are still being recorded.
See the [execution plan](../plans/2026-09-26-bilingual-pdf-refresh.md) for the
remaining gates. A source commit or successful local render is not proof
that a public download has been updated.
