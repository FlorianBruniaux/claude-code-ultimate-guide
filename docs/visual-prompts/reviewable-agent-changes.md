# Reviewable agent changes visual prompts

These prompts illustrate [Reviewable agent changes](../../guide/workflows/reviewable-agent-changes.md): the five fields an agent note records per hunk, and where a note can live with what survives a rewrite. Every visible string comes from that page and from the tests behind it (git 2.56.0 and git-ai 1.7.7, November 8, 2026). Generate one image per prompt with Gemini 3 Pro Image, check every rendered label against the strings below before publication, and convert the selected output to WebP at its native size.

## Selection record

| Published asset | Attempt | Status |
|---|---|---|
| `agent-note-storage.webp` | 1 | Selected on the first attempt, the pilot: title, subtitle, three column headers, four row labels, twelve cells, bottom strip and footer match the strings; green and grey edges on the expected cells; no extra text. Gemini returned JPEG data at 1376 x 768 under a `.png` name; converted to WebP at native size, not upscaled |
| `agent-note-fields.webp` | 2 | Attempt 1 rejected: the icon of card 2 carried the extra word "Why?", and two cards had green top rules instead of ink. Attempt 2 (same prompt, defect judged stochastic) has every string correct and no extra text, but cards 2 to 5 had orange, green and yellow top rules instead of ink. That was fixed locally rather than with a third paid call: the saturated pixels of the rule rows only (rows 227 to 238, right of the first card) were blended toward ink; no text pixel is in those rows. Native 1376 x 768 JPEG data, converted to WebP, not upscaled |

## Shared art direction

Use a warm cream graph-paper background (`#f5f1e8`), a subtle grid (`#d4cfb8`), precise dark ink lines (`#1a1a1a`), and restrained orange (`#d97706`), green (`#16a34a`), and yellow (`#fbbf24`) accents, with grey (`#9ca3af`) for parts that were read but not run. Do not use photos, 3D, mascots, decorative doodles, company logos, page numbers, or an extra pretitle. All visible text is English. Do not use em dashes. Requested aspect 16:9.

## 1. Where an agent note lives

Output: `guide/images/agent-note-storage.webp`

Alt text: Three places an agent note can live compared on four rows. Git notes in refs/notes/rationale are not visible in the merge request unless a tool posts them, follow amend and rebase with notes.rewriteRef (tested) and are lost on a squash merge for plain notes (tested). A file committed with the code shows as a changed file, moves with the content and is kept in a squash with line ranges that may drift. A forge comment is visible in the merge request, is marked outdated on a new head, and its fate in a squash depends on the forge and was not checked.

```text
Create ONE clean editorial data infographic for a technical documentation guide, landscape 16:9 at 1600x900. Warm cream graph-paper background (#f5f1e8) with a subtle grid (#d4cfb8), precise dark ink lines (#1a1a1a), restrained orange (#d97706), green (#16a34a) and yellow (#fbbf24) accents, grey (#9ca3af) for cells read but not run. No photos, no 3D, no mascots, no decorative doodles, no company logos, no page number, no pretitle. Do not use em dashes.

Layout: a comparison table with three aligned columns and four labelled rows, read left to right then top to bottom.

Title at top left, large bold sans-serif: "Where an agent note lives, and what survives a rewrite"
Subtitle under the title, regular weight: "Green: tested. Grey: read from source, not run."

Three column headers in bold, each in a flat card with a thin ink border:
Column 1: "Git notes"
Column 2: "File committed with the code"
Column 3: "Forge comment"

Four row labels in small monospace capitals in a narrow left column:
Row 1: "STORED IN"
Row 2: "VISIBLE IN THE MERGE REQUEST"
Row 3: "AMEND AND REBASE"
Row 4: "SQUASH MERGE"

Cells, each a flat card with a thin ink border:
Row 1, column 1: "refs/notes/rationale" in monospace. Row 1, column 2: "SARIF or JSON beside the code". Row 1, column 3: "Merge request discussion".
Row 2, column 1: "No, unless a tool posts it". Row 2, column 2: "As a changed file". Row 2, column 3: "Yes".
Row 3, column 1: "Kept with notes.rewriteRef", with a green left edge. Row 3, column 2: "Moves with the content", with a grey left edge. Row 3, column 3: "Marked outdated on a new head", with a grey left edge.
Row 4, column 1: "Lost for plain notes", with a green left edge. Row 4, column 2: "Kept, line ranges may drift", with a grey left edge. Row 4, column 3: "Depends on the forge", with a grey left edge.
Rows 1 and 2 have no coloured edge.

Bottom strip across the full width, with a small yellow marker, regular weight: "A forge merge button rewrites history on the server: not tested."

Footer at bottom right in small monospace, with a clear margin from the canvas edge: "git 2.56.0 and git-ai 1.7.7, November 8, 2026"

Colour names, layout words and the words row, column, cell and edge are instructions, never visible text. Text inventory: exactly the strings in double quotes above, each appearing exactly once, spelled exactly as written; nothing else, no extra labels, numbers, icons with text, or legend.
```

## 2. Five things an agent note records

Output: `guide/images/agent-note-fields.webp`

Alt text: Five equal cards for the fields of an agent note per hunk: intent, what the change is for; rejected alternative, the option not taken and why; risk, what this could break and for whom; evidence, what the reviewer can rerun; open question, what the agent could not decide. Each card has an example from the template. Unknown is a valid answer except for intent; a note is a claim to check, not evidence.

```text
Create ONE clean editorial data infographic for a technical documentation guide, landscape 16:9 at 1600x900. Warm cream graph-paper background (#f5f1e8) with a subtle grid (#d4cfb8), precise dark ink lines (#1a1a1a), restrained orange (#d97706), green (#16a34a) and yellow (#fbbf24) accents. No photos, no 3D, no mascots, no decorative doodles, no company logos, no page number, no pretitle. Do not use em dashes.

Layout: five equal cards side by side in one row, read left to right. Each card is flat with a thin ink border and has, from top to bottom: a simple line icon, a bold name, a one-line definition, and at the lower edge a small monospace example chip with a thin ink outline. The first card has an orange top rule; the other four have a thin ink top rule.

Title at top left, large bold sans-serif: "Five things an agent note records for each hunk"
Subtitle under the title, regular weight: "This guide's proposal. Unknown is a valid answer, except for intent."

Card 1: name "Intent", definition "What the change is for", example chip "Sum prices, not item objects".
Card 2: name "Rejected alternative", definition "The option not taken, and why", example chip "Give Item an __add__ method".
Card 3: name "Risk", definition "What this could break, for whom", example chip "Items without a price raise AttributeError".
Card 4: name "Evidence", definition "What the reviewer can rerun", example chip "test_cart.py::test_total_uses_price".
Card 5: name "Open question", definition "What the agent could not decide", example chip "unknown".

Closing sentence centred below the cards, regular weight: "A note is a claim to check, not evidence."

Footer at bottom right in small monospace, with a clear margin from the canvas edge: "Template: examples/skills/agent-rationale"

Colour names and layout words are instructions, never visible text. Icons carry no text. Text inventory: exactly the strings in double quotes above, each appearing exactly once, spelled exactly as written; nothing else.
```
