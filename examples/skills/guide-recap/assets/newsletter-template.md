# Newsletter Template

Target: ~500 words. Structured sections with depth.

## FR Template

```markdown
# {title_fr}

{intro_paragraph_fr}

## Ce qui a change

{highlights_section_fr}

## En detail

{detail_section_fr}

## A retenir

{takeaway_fr}

---

[Guide complet]({landing_url}) | [GitHub]({github_url})
```

## EN Template

```markdown
# {title_en}

{intro_paragraph_en}

## What changed

{highlights_section_en}

## In detail

{detail_section_en}

## Key takeaway

{takeaway_en}

---

[Full guide]({landing_url}) | [GitHub]({github_url})
```

## Field Rules

### title (max 80 chars)

Version or week framing, descriptive.

```
FR: "Guide v3.20.5 : Reference visuelle enrichie"
EN: "Guide v3.20.5: Enhanced Visual Reference"

FR: "Semaine du 27 janvier : 4 releases, 9 patterns avances"
EN: "Week of January 27: 4 releases, 9 advanced patterns"
```

### intro_paragraph (2-3 sentences, max 150 words)

What happened and why it matters. No hype.

```
FR: "La version 3.20.5 du Claude Code Ultimate Guide ajoute 4 nouveaux
diagrammes ASCII a la reference visuelle. Le guide contient maintenant
20 diagrammes couvrant TDD, securite et workflows d'apprentissage."

EN: "Version 3.20.5 of the Claude Code Ultimate Guide adds 4 new ASCII
diagrams to the visual reference. The guide now contains 20 diagrams
covering TDD, security, and learning workflows."
```

### highlights_section (bullet list, 3-5 items)

Top scored entries, transformed. Each bullet: 1-2 sentences max.

```
FR:
- **Cycle TDD Red-Green-Refactor** : Diagramme du flux iteratif test-code-refactor
- **Protocole UVAL** : Visualisation du framework Comprendre-Verifier-Appliquer-Apprendre
- **Defense securite 3 couches** : Prevention, detection, reponse avec guide d'adoption
- **Timeline d'exposition de secrets** : Actions d'urgence par fenetre temporelle (15min/1h/24h)

EN:
- **TDD Red-Green-Refactor Cycle**: Diagram of the iterative test-code-refactor flow
- **UVAL Protocol Flow**: Visualization of the Understand-Verify-Apply-Learn framework
- **Security 3-Layer Defense**: Prevention, detection, response with adoption guide
- **Secret Exposure Timeline**: Emergency actions by time window (15min/1h/24h)
```

### detail_section (1-2 paragraphs, max 200 words)

Expand on the most interesting highlight. Provide context, explain what the user gains.
Credit sources if applicable.

### takeaway (1-2 sentences)

Single actionable insight or summary.

```
FR: "Si vous apprenez mieux en visuel, les 20 diagrammes du guide couvrent
maintenant les workflows les plus frequents, de TDD a la gestion d'incidents."

EN: "If you're a visual learner, the guide's 20 diagrams now cover the most
common workflows, from TDD to incident management."
```

## Constraints

- Total: 400-600 words
- Emoji budget: 2-3 (section headers only)
- No hype words
- FR: vouvoiement
- EN: American English
- Both links (landing + GitHub) in footer
- Credit all named sources
