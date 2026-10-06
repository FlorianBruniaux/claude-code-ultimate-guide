# Bilingual publication refresh: October 6, 2026

## Source review

Edition: 3.44.1. The canonical source is the English full guide. The French refresh reconciles every semantic delta since its recorded English source `279192a4cda799018afa06a1ff0884a61f81302c`, plus the pricing and paused-billing corrections made for this edition. The baseline diff contains 31 semantic hunks and 314 case-only hunks. Existing translated semantic-anchor and billing-pause sections were compared and retained. This is a Codex delta reconciliation, not a new human review of every historical paragraph.

All 26 numbered EN/FR e-book sources passed complete Quarto and frontmatter inspection; their contemporary passages received targeted review against the relevant canonical guide sections. A final pass also read the introductions, summaries and conclusions of all 26 e-books, reconciling illustrative examples and study-sample limits with their corrected body sections. All 116 recap cards and two daily cheatsheets were read and compared with their canonical references. Their edition metadata is 3.44.1. Independent e-book revisions retain legitimate FR/EN differences and follow patch or minor increments according to the change. Of the 118 card/cheatsheet sources, 31 needed substantive corrections and 87 only edition metadata.

Corrections cover current model names and executable IDs, context and billing boundaries, hook inputs, unsupported productivity and security promises, token-output estimates versus whole-task costs, verification-capacity admission, FinOps and agent recovery controls. Historical studies remain dated and attributed. RTK references disclose the author's contribution; these recommendations are not independent product evaluations.

The four standard Anthropic model API rates were checked directly on October 6 against the [official pricing table](https://platform.claude.com/docs/en/about-claude/pricing). This rate check does not revalidate every provider alias, plan allowance, security policy or historical research result. The old pricing anchor remains available. The batch-processing paragraph no longer treats the paused programmatic credit as active.

## Export and deployment acceptance

Eleven French recap fragments embedded in the e-books were also reviewed and corrected at their included source. Typst formatting now uses content blocks, and unsupported J-curve and universal productivity claims were bounded. The whitepaper templates preserve physical page numbers after the unnumbered cover and keep callout titles with their following content. Both formatting fixes passed targeted PDF behavior checks.

The complete catalog comprises 146 PDF files and 28 EPUB files. `scripts/render-publications.py` records the committed source, source hashes, tool and font versions, and output hashes. `scripts/validate-publications.py` checks all 174 outputs for integrity, source freshness, PDF page boundaries, one-page recap cards, EPUB language and spine validity. Automated geometry checks do not establish visual or semantic quality. A separate visual pass must inspect representative dense pages and card contact sheets before deployment.

Public download synchronization covers the publication registry, landing page metadata and EPUBs, portfolio PDF files, six recap-card ZIPs, and the stable email download manifest. Previous versioned files are retained. The English landing cards are regenerated from the reviewed EN QMD sources while preserving reviewed web-only RTK disclosures.

## Evidence limits

This refresh does not independently reproduce benchmark studies, execute every code example, certify legal or security statements, or establish search-engine indexation or traffic gains. The translation registry records the exact committed English source only after that source is committed. Publication hashes and dates reflect the actual render, rather than the website build date.
