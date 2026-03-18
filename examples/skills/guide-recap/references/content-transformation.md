# Content Transformation

Maps technical CHANGELOG language to user-facing social value. Apply tone-guidelines.md rules to all outputs.

## Transformation Principle

```
Technical fact (CHANGELOG) -> User benefit (social post)
```

Never invent benefits. Every transformation must trace back to a concrete CHANGELOG line.

## Mapping Table

### New Content

| Technical (CHANGELOG) | Social (User Value) |
|---|---|
| `N new ASCII diagrams (X -> Y total)` | `Visual learner? N new diagrams for [topics]` |
| `N New Quiz Questions (X -> Y total)` | `Test your Claude Code knowledge: N new questions covering [top categories]` |
| `New [guide-name].md (N lines)` | `New guide: [topic in plain language]` |
| `New section: [Section Name] (~N lines)` | `[What you can now learn/do]: [plain description]` |
| `New workflow: [name]` | `Step-by-step: how to [action] with Claude Code` |
| `Enhanced [command/agent] (+N lines)` | `[Command] now supports [new capability]` |
| `N new entries in reference.yaml` | Skip (internal indexing, no user value) |

### Research & Sources

| Technical (CHANGELOG) | Social (User Value) |
|---|---|
| `Score: 5/5 - [Source]` | `Critical finding from [Author]: [key insight]` |
| `Score: 4/5 - [Source]` | `From [Author]'s research: [practical takeaway]` |
| `Score: 3/5 - [Source]` | `[Author] confirms: [relevant finding]` |
| `Source: [URL] ([Author], [Date])` | `Based on [Author]'s work` |
| `Competitive Analysis: N Gaps from [source]` | `N advanced patterns identified: [top 2-3 names]` |
| `Resource evaluation: [file]` | Skip (internal process, not user-facing) |
| `Fact-checked: N/N claims verified` | Can mention as credibility signal: `All N claims verified` |

### Growth Metrics

| Technical (CHANGELOG) | Social (User Value) |
|---|---|
| `Guide line count: X -> Y (+N lines)` | `+N lines of documentation added this [week/version]` |
| `X -> Y total [items]` | `Now Y [items] (was X)` |
| `+N lines: X -> Y` | `[Feature] expanded with N lines of [content type]` |

### Fixes & Changes

| Technical (CHANGELOG) | Social (User Value) |
|---|---|
| `Fixed [technical issue]` | `Corrected: [what users see fixed]` |
| `[File]: Updated [field] (X -> Y)` | Skip unless user-visible change |
| `Landing synced` | Skip (infrastructure) |
| `Badge updated` | Skip (infrastructure) |

### Maintenance (Usually Skip)

| Technical (CHANGELOG) | Social Value |
|---|---|
| `README.md: Added [X] to table` | Skip |
| `Updated counts in [files]` | Skip |
| `Sync: [description]` | Skip |
| `reference.yaml: +N entries` | Skip |
| `CLAUDE.md: [update]` | Skip |

## Pattern Recognition

### Numbers to Highlight

When an entry contains numeric changes, extract and format:

```
"30 New Quiz Questions (227 -> 257)"
-> number: 30
-> growth: "227 -> 257"
-> highlight: "30 new questions" or "now 257 questions"

"4 new ASCII diagrams (16 -> 20 total)"
-> number: 4
-> growth: "16 -> 20"
-> highlight: "4 new diagrams" or "now 20 diagrams"

"+522 lines"
-> number: 522
-> highlight: "+522 lines of new content"
```

### Named Sources to Credit

Extract author names and give proper attribution:

```
"Pat Cullen's Final Review Gist" -> "From Pat Cullen's production workflow"
"Addy Osmani's 80% Problem"     -> "Based on Addy Osmani's research"
"Shen & Tamkin RCT"             -> "From Shen & Tamkin's study (Anthropic)"
"claudelog.com (InventorBlack)"  -> "Identified via claudelog.com community"
"Jude Gao (Vercel)"             -> "From Vercel's benchmarks (Jude Gao)"
```

### Topic Clustering

When multiple entries share a theme, cluster them:

```
Entries about code review:
- "Multi-Agent PR Review"
- "Enhanced /review-pr command"
- "Enhanced code-reviewer agent"
-> Cluster: "Code review overhaul: multi-agent workflow, anti-hallucination rules, severity classification"

Entries about security:
- "Docker sandbox isolation"
- "Security 3-Layer Defense diagram"
- "Secret Exposure Timeline diagram"
-> Cluster: "Security focus: sandbox isolation, defense layers, incident response timeline"
```

## Version vs Week Framing

### Single Version

```
FR: "Claude Code Ultimate Guide v3.20.5"
EN: "Claude Code Ultimate Guide v3.20.5"
```

### Week (Multiple Versions)

```
FR: "Cette semaine dans le guide (N releases)"
EN: "This week in the guide (N releases)"
```

### Week (Single Version)

```
FR: "Cette semaine : guide v3.20.5"
EN: "This week: guide v3.20.5"
```
