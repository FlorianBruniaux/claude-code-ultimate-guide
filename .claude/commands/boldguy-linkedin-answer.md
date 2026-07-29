---
name: boldguy-linkedin-answer
description: Draft a LinkedIn comment on a post, referencing the guide's relevant section, in Flow style with AI markers removed
argument-hint: "<linkedin-post-url>"
---

# Bold Guy LinkedIn Answer

Draft a LinkedIn comment responding to a post, referencing the Claude Code Ultimate Guide's relevant sections, written in Florian "Flow" Bruniaux's voice with zero AI markers.

## Usage

```
/boldguy-linkedin-answer https://www.linkedin.com/posts/...
```

## Step 1: Read the LinkedIn Post

1. Parse `$ARGUMENTS` for the LinkedIn URL. If missing, ask: "Quel post LinkedIn ?"
2. Fetch the post content via WebFetch
3. Extract: author name, main argument, key points, tone

## Step 2: Identify Relevant Guide Sections

Search the guide for content that connects to the post's topic:

1. Search `guide/ultimate-guide.md` and other `guide/*.md` files for keywords from the post
2. Search `machine-readable/reference.yaml` for matching sections
3. Check if a dedicated landing page exists (e.g., `/learning`, `/quiz`)
4. Prioritize sections where the guide adds unique value (protocols, tools, data, methodology)

**Output of this step**: A list of 2-4 relevant elements to reference (section name, key concept, landing URL if applicable).

## Step 3: Draft the Comment

Write a LinkedIn comment following these rules:

### Language Rule (CRITICAL)
- **Match the post's language**: if the post is in English, write the comment in English; if in French, write in French.
- Never mix languages in the same comment.

### Voice Rules (Florian's voice, NOT a team)
- Always "I've" / "I" — never "we've" / "we" (Florian works alone on the guide)
- Posture: "I share what I learn" — never "I teach you"
- Practitioner, not guru
- In French: "j'ai" / "je" — never "on a" / "nous avons"

### Platform Rules (LinkedIn Comment)
- **First name** direct with the post author (tutoiement in French, first name in English)
- Conversational, like a hallway discussion
- **Max 1200 characters** (hard limit)
- Zero hashtags
- Zero emojis (or 1 max if really warranted)
- Link only if direct value-add (guide section, landing page)

### Content Structure
```
[Validate/acknowledge the author's point — 1 sentence]

[Connect to guide content — what I've documented, what the data says]

[1-2 concrete elements: protocol, metric, tool, methodology]

[Closing: link to relevant guide/landing section OR conversational question]
```

### What to Include
- Concrete guide elements: protocols (UVAL, etc.), tools (`--learn`, etc.), methodologies
- Real data if available (academic studies cited in the guide, measured metrics)
- The right landing/guide URL for the reader to go deeper

### Linking Strategy

**Guide reader** (`cc.bruniaux.com/guide/`): use for ALL guide section links. The guide is split into numbered pages matching the original chapter structure.

URL format: `cc.bruniaux.com/guide/ultimate-guide/[NN-slug]/` with optional anchor `#NN-section-name`

**Page map** (file → URL):
| Chapter | URL |
|---------|-----|
| 0 Introduction | `cc.bruniaux.com/guide/ultimate-guide/00-introduction/` |
| 1 Quick Start | `cc.bruniaux.com/guide/ultimate-guide/01-quick-start/` |
| 2 Core Workflow | `cc.bruniaux.com/guide/ultimate-guide/02-core-workflow/` |
| 3 Memory Files | `cc.bruniaux.com/guide/ultimate-guide/03-memory-files/` |
| 4 Agents | `cc.bruniaux.com/guide/ultimate-guide/04-agents/` |
| 5 Skills | `cc.bruniaux.com/guide/ultimate-guide/05-skills/` |
| 6 Commands | `cc.bruniaux.com/guide/ultimate-guide/06-commands/` |
| 7 Hooks | `cc.bruniaux.com/guide/ultimate-guide/07-hooks/` |
| 8 MCP | `cc.bruniaux.com/guide/ultimate-guide/08-mcp/` |
| 9 Advanced Patterns | `cc.bruniaux.com/guide/ultimate-guide/09-advanced-patterns/` |
| 10 Reference | `cc.bruniaux.com/guide/ultimate-guide/10-reference/` |
| 11 AI Ecosystem | `cc.bruniaux.com/guide/ultimate-guide/11-ai-ecosystem/` |
| 12 Appendices | `cc.bruniaux.com/guide/ultimate-guide/12-appendices/` |

**Key section anchors** (most referenced in comments):
| Section | Full URL |
|---------|---------|
| 1.1 Installation | `cc.bruniaux.com/guide/ultimate-guide/01-quick-start/#11-installation` |
| 2.2 Context Management | `cc.bruniaux.com/guide/ultimate-guide/02-core-workflow/#22-context-management` |
| 2.3 Plan Mode | `cc.bruniaux.com/guide/ultimate-guide/02-core-workflow/#23-plan-mode` |
| 3.1 Memory Files (CLAUDE.md) | `cc.bruniaux.com/guide/ultimate-guide/03-memory-files/#31-memory-files-claudemd` |
| 4.1 What Are Agents | `cc.bruniaux.com/guide/ultimate-guide/04-agents/#41-what-are-agents` |
| 5.1 Understanding Skills | `cc.bruniaux.com/guide/ultimate-guide/05-skills/#51-understanding-skills` |
| 7.1 The Event System (Hooks) | `cc.bruniaux.com/guide/ultimate-guide/07-hooks/#71-the-event-system` |

Anchors follow Starlight/Astro rules: lowercase, spaces → hyphens, dots/parens removed.
Example: `## 3.1 Memory Files (CLAUDE.md)` → `#31-memory-files-claudemd`

**Landing site** (`cc.bruniaux.com`): use only for non-guide pages
- `cc.bruniaux.com` — main landing
- `cc.bruniaux.com/examples` — template browser
- `cc.bruniaux.com/quiz` — interactive quiz

**Rule**: Always prefer `cc.bruniaux.com/guide/ultimate-guide/[NN-slug]/` with the exact anchor over any GitHub link. Never use the GitHub blob URL.

### What to Avoid
- Listing features like a product page
- Marketing language (see vocabulary-rules.md)
- Engagement bait, FOMO, mystery box
- Inventing metrics or durations not documented in the guide
- Over-selling the guide

## Step 4: Anti-AI Pass

Run the /boldguy-adapt skill on the draft to remove AI markers.

Specifically verify:

### Checklist (every item must pass)
- [ ] Zero em dash (`—`) — use comma, parenthesis, or restructure
- [ ] No staccato (3+ sentences under 5 words in a row)
- [ ] "C'est pas X. C'est Y." pattern max 1 time, with comma not period
- [ ] Varied sentence lengths within each paragraph
- [ ] No overly symmetric/perfect closing punchline
- [ ] Paragraphs link ideas (not 1 idea = 1 isolated paragraph)
- [ ] No bold bullet parallelism (e.g., 4x "Un **X** qui...")
- [ ] No `→` arrows in lists (conversational, not slide deck)

### Rhythm Check
The comment should read like a cafe conversation between practitioners:
- Mix short and long sentences in the same paragraph
- Ideas flow into each other, not stacked in isolation
- Closing is natural (question or simple statement), not a slogan

## Step 5: Character Count & Final Validation

1. Count characters (must be <= 1200)
2. If over limit: cut the least essential element, merge sentences, tighten phrasing
3. If significantly under (~800): good, don't pad it

### Final Checklist
- [ ] "je" everywhere (never "on" for the guide work)
- [ ] <= 1200 characters
- [ ] Tutoiement with author
- [ ] Anti-AI checklist passed
- [ ] At least 1 concrete guide reference (protocol, tool, data)
- [ ] Max 1 link (guide or landing)
- [ ] No marketing language
- [ ] Reads like a human practitioner, not a pitch

## Step 6: Output

Present to the user:

```
### Commentaire LinkedIn (~[N] caractères)

[The comment text, ready to paste]

---

### Sections du guide référencées
- [Section 1]: [brief description]
- [Section 2]: [brief description]

### Anti-AI check
[List of markers checked — all passed or flagged for manual review]
```

## Error Handling

- **No URL provided** → Ask for it
- **Post not accessible** → Ask user to paste the post content
- **No relevant guide section** → Draft a comment based on general expertise, flag that no specific guide section was referenced
- **Over 1200 chars after tightening** → Present both a full version and a trimmed version, let user choose
