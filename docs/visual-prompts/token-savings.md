# Token savings visual prompts

These prompts illustrate the claimed-versus-measured comparison of token-saving tools and the breakdown of tool tokens by call type. Every visible string comes from the primary sources read on 2026-09-30 (JetBrains AI blog, Stet.sh, Dasein Code-Compression Bench, vendor READMEs, Marmelab Atomic CRM Builder). Generate one image per prompt with Gemini 3 Pro Image, review every rendered label and number against the source strings before publication, and convert the selected source to WebP at its native size (Gemini returned 1376 x 768; the images were not upscaled).

## Selection record

| Published asset | Attempt | Status |
|---|---|---|
| `token-savings-claimed-vs-measured.webp` | 2 | Attempt 1 rejected: each tag line was rendered twice per row (once under each value). Attempt 2 selected after a brief fix (one tag line per row): all four rows, eight values, four tags, four unit markers, footer and source line match the source strings; no extra text. The source line wraps onto two lines at "Code-" and "Compression" but the string is intact |
| `token-savings-tool-token-share.webp` | 1 | Selected on first attempt: headline, three segment labels, two callouts, note and source line match; segment widths measured at about 90%, 6.7% and 3.4% of the bar, visibly proportional to 90.6, 6.4 and 3.0 |

## Shared art direction

Use a warm cream graph-paper background (`#f5f1e8`), a subtle grid (`#d4cfb8`), precise dark ink lines (`#1a1a1a`), and restrained orange (`#d97706`), green (`#16a34a`), and yellow (`#fbbf24`) accents. Reserve red for warnings. Do not use photos, 3D, mascots, decorative doodles, company logos, page numbers, or an extra pretitle. All visible text is English. Do not use em dashes. Requested aspect 16:9.

## 1. Claimed versus measured

Output: `guide/images/token-savings-claimed-vs-measured.webp`

Alt text: Four token-saving tools compared on vendor claim versus independent measurement: Caveman claims 65% fewer output tokens and measured 8.5%, RTK claims 60-90% fewer shell-output tokens and measured +7.6% cost per task, Ponytail claims about 20% cheaper and measured +20% then -2%, Headroom claims 73-92% fewer tokens on specific content and measured +44% total cost.

```text
Create a clean editorial data infographic for a technical documentation guide, landscape 16:9 at 1600x900. Warm cream graph-paper background (#f5f1e8) with a subtle grid (#d4cfb8), precise dark ink lines (#1a1a1a), restrained orange (#d97706), green (#16a34a) and yellow (#fbbf24) accents, red only for the warning marker. No photos, no 3D, no mascots, no decorative doodles, no company logos, no page number, and no pretitle. All visible text must be exactly the English strings listed below, spelled correctly, each appearing exactly once. Do not use em dashes. Do not add any other words, numbers, or labels.

Headline at top left, large bold sans-serif: "CLAIMED VS MEASURED"

Below the headline, a table of four horizontal rows, each row a flat card with a thin ink border. Each row has three zones from left to right: a narrow tool name zone, a "claimed" zone with an orange left edge, and a "measured" zone with a dark ink left edge. Above the two value zones, shown once only as column captions in small monospace capitals: "CLAIMED" over the left value zone and "MEASURED" over the right value zone. Each row carries exactly ONE small monospace tag line, placed once at the bottom of the row card, spanning the row under the two value zones; it is never repeated inside both zones. At the far right of each row, a small rounded pill marker.

Row 1. Tool name in bold: "Caveman". Claimed value: "65% fewer output tokens". Measured value: "8.5% fewer output tokens". Tag line: "JetBrains, 82 paired tasks, forced activation". Pill marker: "same unit".
Row 2. Tool name in bold: "RTK". Claimed value: "60-90% fewer tokens in shell output". Measured value: "+7.6% cost per task (low effort)". Tag line: "JetBrains, 86 SkillsBench tasks". Pill marker: "different unit".
Row 3. Tool name in bold: "Ponytail". Claimed value: "~20% cheaper". Measured value: "+20% then -2% cost over two runs". Tag line: "Stet, 10 tasks, 2 runs". Pill marker: "same unit".
Row 4. Tool name in bold: "Headroom". Claimed value: "73-92% fewer tokens on specific content". Measured value: "+44% total cost". Tag line: "Dasein, 100 SWE-bench tasks, sponsor-run". Pill marker: "different unit".

Pill markers reading "same unit" are green outlined; pill markers reading "different unit" are yellow filled.

Bottom strip across the full width with a small red warning marker and the text in regular weight: "A shell-output or content-type saving is not a total-cost saving."

Footer at bottom right in small monospace, with a clear margin so no character touches the canvas edge: "Sources: JetBrains AI blog, Stet.sh, Dasein Code-Compression Bench, vendor READMEs. Read 2026-09-30."
```

## 2. Where tool tokens come from

Output: `guide/images/token-savings-tool-token-share.webp`

Alt text: A single stacked bar of tool tokens in an Atomic CRM Builder baseline: Read 90.6% at 958 tokens per call, Bash 6.4% at 77 tokens per call, Edit, Write and other 3.0%, so a shell-output filter only touches the Bash slice.

```text
Create a clean editorial data infographic for a technical documentation guide, landscape 16:9 at 1600x900. Warm cream graph-paper background (#f5f1e8) with a subtle grid (#d4cfb8), precise dark ink lines (#1a1a1a), restrained orange (#d97706), green (#16a34a) and yellow (#fbbf24) accents, red only for the warning marker. No photos, no 3D, no mascots, no decorative doodles, no company logos, no page number, and no pretitle. All visible text must be exactly the English strings listed below, spelled correctly, each appearing exactly once. Do not use em dashes. Do not add any other words, numbers, axis ticks, or labels.

Headline at top left, large bold sans-serif: "WHERE TOOL TOKENS COME FROM"

Center of the canvas: a single very wide horizontal 100% stacked bar, spanning almost the full canvas width, with a thin ink outline, tall enough to hold labels inside or directly above. Three segments, widths strictly proportional to their values: the first segment takes 90.6% of the bar width (orange), the second takes 6.4% (green), the third takes 3.0% (yellow). The first segment is therefore much wider than the other two combined. Each segment is labeled with exactly one label: the orange segment "Read 90.6%", the green segment "Bash 6.4%", the yellow segment "Edit, Write, other 3.0%". Because the green and yellow segments are narrow, place their labels just above or below them with a thin leader line.

Under the bar, two callout cards side by side, flat with thin ink borders. Left card, under the orange part: "Read: 958 tokens per call". Right card, under the green part: "Bash: 77 tokens per call".

Below the callouts, a wide strip with a small red warning marker and the text in regular weight: "A shell-output filter only touches the Bash slice."

Footer at bottom right in small monospace: "Marmelab, Atomic CRM Builder, 9 baseline instances, August 2026."
```
