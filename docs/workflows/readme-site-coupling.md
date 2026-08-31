# README and Website Navigation Contract

The website owns human browsing and discovery. The guide repository owns Markdown sources, reusable files, machine-readable indexes, and contribution history. `machine-readable/navigation.json` connects those surfaces.

## Ownership

| Surface | Responsibility | Canonical location |
|---|---|---|
| Human navigation | Intent routes, search, rendered pages, downloads | `https://cc.bruniaux.com/` |
| Guide content | Long-form Markdown and examples | `guide/`, `examples/`, `docs/` |
| Curated intent model | `Start`, `Build`, `Scale`, `Resources`, `Updates` | `machine-readable/navigation.json` |
| Repository summary | Short project entry point and source access | `README.md` |
| Guide history | Repository changes | `CHANGELOG.md` and `/changelog/` |
| Claude Code history | Product versions and operational impact | `machine-readable/claude-code-releases.yaml` and `/releases/` |

The README should not duplicate the website sitemap. It exposes a generated intent excerpt, a short repository-specific quick start, and source links for contributors or offline readers.

## Existing README coverage

This table records where the large sections of the previous README belong. `Remove` means the block duplicated another destination or relied on an unsupported claim. It does not authorize deleting a unique source page.

| Previous README section | Decision | Destination or retained source |
|---|---|---|
| Badges and downloads | Condense | Website CTA, `/downloads/`, repository version and license |
| StarMapper | Remove from main flow | `/projects/` or a single footer link if retained |
| Languages and translations | Keep a short summary | `/guide/translations/` and `guide/core/translations.md` |
| Choose Your Path | Replace | Generated `Start`, `Build`, and `Scale` navigation |
| What You'll Learn | Merge | README introduction and `/guide/` |
| Guide comparison and ASCII matrix | Replace | `/compare/`, `/ecosystem/`, and the complementary-resource table |
| Quick Start | Keep a bounded repository version | `/guide/ultimate-guide/01-quick-start/` and `guide/ultimate-guide.md` |
| MCP Server | Keep | `/mcp/` and `mcp-server/README.md` |
| Repository Structure | Keep a compact map | README repository map and directory indexes |
| What Makes This Guide Unique | Merge | `/guide/` topic groups and evidence-bearing source pages |
| Learning Paths | Move discovery to website | `/learning/`, `/roles/`, and role-specific pages |
| Rate Limits and Cost Savings | Move | `/projects/`, `/guide/subscription-strategy/`, and the relevant project repository |
| Golden Rules | Link to canonical guidance | `/cheatsheet/`, security pages, and the full guide |
| For AI Assistants | Keep | `machine-readable/` and `/mcp/` |
| Whitepapers | Move discovery to website | `/whitepapers/` and `/downloads/` |
| Recap Cards | Move discovery to website | `/cheatsheets/` and `whitepapers/recap-cards/` |
| Ecosystem | Replace | `/ecosystem/`, `/compare/`, and source evaluations |
| Security inventory | Move discovery to website | `/security/` and `guide/security/` |
| About and related projects | Condense | `/projects/`, portfolio, and a short maintainer section |
| What's Inside | Replace | `/guide/`, `/sitemap/`, and directory indexes |
| Star History | Remove | Repository hosting already exposes star history |
| Contributing | Keep | `CONTRIBUTING.md` |
| License and Support | Keep | Repository license and public update routes |
| Further Reading | Move | `/resources/`, `/ecosystem/`, and resource evaluations |

## Change workflow

1. Edit `machine-readable/navigation.json` in the guide repository.
2. Run `python3 scripts/sync-navigation.py --write`.
3. Review the generated README block and the source-path validation result.
4. Build the landing with the guide repository available as its sibling or through `GUIDE_REPO_PATH`.
5. Verify `/sitemap/`, `/guide/`, the header navigation, search, and the public route targeted by each changed entry.
6. Keep landing-only routes in the shared manifest with `source_path: null`.

## Acceptance gates

- The five intent groups remain ordered as `Start`, `Build`, `Scale`, `Resources`, and `Updates`.
- Item identifiers and public routes are unique.
- Every non-null `source_path` exists inside the guide repository.
- Every declared source anchor resolves to a Markdown heading.
- The marked README block matches the manifest byte for byte after rendering.
- The landing copy matches the guide manifest before Astro builds.
- Public reading links target `cc.bruniaux.com`; repository links identify source or downloadable files.
- Counts are generated at the consuming surface or omitted.
