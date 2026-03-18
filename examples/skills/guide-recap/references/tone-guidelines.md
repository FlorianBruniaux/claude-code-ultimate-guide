# Tone Guidelines

Rules for social content generated from CHANGELOG entries. Central principle: **engagement through value, not hype**.

## DO / DON'T Checklist

### DO

- Use concrete numbers from the CHANGELOG (`227 -> 257`, `+522 lines`, `4 new diagrams`)
- State what the user can do now (`Test your knowledge`, `New visual guide for...`)
- Ask genuine questions (`Visual learner?`, `How do you review PRs?`)
- Credit named sources (`Based on Pat Cullen's workflow`, `From Addy Osmani's research`)
- Use precise action verbs (`added`, `integrated`, `documented`, `evaluated`)
- Reference specific patterns by name (`Permutation Frameworks`, `Split-Role Agents`)

### DON'T

- Use hype words: `game-changer`, `revolutionary`, `incredible`, `amazing`, `must-have`
- Use FOMO: `You're missing out`, `Don't fall behind`, `Everyone is using this`
- Use fake urgency: `Act now`, `Limited time`, `Before it's too late`
- Use clickbait hooks: `This ONE trick`, `You won't believe`, `Hidden feature`
- Invent metrics: `10x faster`, `saves hours`, `boosts productivity by 300%`
- Use more than 3-4 emojis per LinkedIn post, 2 per tweet
- Over-promise: `The only guide you'll ever need`, `Complete mastery`

## Language Rules

### French (FR)

| Format | Register | Example |
|--------|----------|---------|
| LinkedIn | Vouvoiement | `Vous utilisez Claude Code au quotidien ?` |
| Newsletter | Vouvoiement | `Vous trouverez dans cette version...` |
| Twitter/X | Tutoiement | `Tu connais les Permutation Frameworks ?` |
| Slack | Tutoiement | `Nouvelle version dispo, check ca` |

### English (EN)

- Direct address (`you`) in all formats
- American English spelling (`optimize`, `analyze`, not `optimise`, `analyse`)
- No British idioms or spellings

## Emoji Budget

| Format | Max Emojis | Placement |
|--------|-----------|-----------|
| LinkedIn | 3-4 | Hook line (0-1), bullets (1 each, max 3), CTA (0-1) |
| Twitter | 2 | Hook (1), key point (1) |
| Newsletter | 2-3 | Section headers only |
| Slack | 4-6 | Status markers, emphasis |

Allowed emojis: `+`, `->`, technical symbols preferred over decorative ones.
Avoid: fire, rocket, explosion, 100, mind-blown (marketing cliches).

## CTA Rules

| Format | CTA Style | Link Target |
|--------|-----------|-------------|
| LinkedIn | Soft question or value statement | Landing site URL |
| Twitter | Short action or link | GitHub repo |
| Newsletter | Explicit link with context | Landing site URL |
| Slack | Direct link | GitHub repo |

No `Click here`, `Check this out`, `Link in bio` patterns.

## Quality Checklist (Pre-Output)

Before outputting any social content, verify:

1. [ ] Every number comes from the actual CHANGELOG entry
2. [ ] No hype words (grep against DON'T list)
3. [ ] Emoji count within budget
4. [ ] FR register matches format (vous/tu)
5. [ ] EN uses American spelling
6. [ ] CTA links to correct target
7. [ ] Named sources credited when used
8. [ ] No invented metrics or percentages
