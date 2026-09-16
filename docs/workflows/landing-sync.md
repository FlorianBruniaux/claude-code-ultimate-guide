# Landing Site Synchronization

Workflow for keeping `cc.bruniaux.com` in sync with the guide after significant changes.

**Landing repo**: [claude-code-ultimate-guide-landing](https://github.com/FlorianBruniaux/claude-code-ultimate-guide-landing). Commands assume sibling guide and landing checkouts.

## Elements to Sync

| Element | Source (guide) | Destination (landing) |
|---------|----------------|----------------------|
| Version | `VERSION` | index.html footer + FAQ |
| Templates count | Count `examples/` files | Badges, title, meta tags |
| Guide lines | `wc -l guide/ultimate-guide.md` | Badges |
| Golden Rules | README.md | index.html section |
| FAQ | README.md | index.html FAQ |

## Sync Triggers

After these modifications, **remember** to update the landing:

1. **Version bump** → Update `VERSION` here, then landing
2. **Templates added/removed** → Recalculate count, update landing
3. **Golden Rules or FAQ modified** → Propagate to landing
4. **Significant guide change** (>100 lines)

## Landing rebuild dispatch credential

`.github/workflows/trigger-landing-deploy.yml` calls the landing repo's API to run
`deploy.yml` whenever `guide/`, `machine-readable/` or `examples/` changes on `main`.
It authenticates with the `LANDING_DEPLOY_TOKEN` secret. This is the only
cross-repository credential the guide holds.

**Never record the token value here, in a commit, or in a run log.** The workflow reads
it from an environment variable and prints neither the value nor its length; GitHub's
secret masking is a backstop, not the control.

| | |
|---|---|
| Secret name | `LANDING_DEPLOY_TOKEN` |
| Stored in | This repo, Settings → Secrets and variables → Actions |
| Owned by | The account with write access to `FlorianBruniaux/claude-code-ultimate-guide-landing` |
| Grants | Dispatching `deploy.yml` on the landing repo, nothing else |
| Rotate at | https://github.com/settings/personal-access-tokens |

### Required scope

Issue a **fine-grained** personal access token, not a classic one. A classic token with
`repo` grants far more than dispatching a workflow.

- Resource owner: `FlorianBruniaux`
- Repository access: **only** `claude-code-ultimate-guide-landing`
- Repository permissions: **Actions: Read and write**. Nothing else is needed.

The job itself declares `permissions: {}`, so the run's own `GITHUB_TOKEN` gets no scopes
on this repository. The only authority in play is the token's, on the landing repo.

### Rotating

1. Issue a replacement token with the scope above, and set an expiry you will act on.
2. Update `LANDING_DEPLOY_TOKEN` in this repo's Actions secrets.
3. Re-verify without waiting for a guide push: Actions → **Trigger landing site rebuild**
   → **Run workflow**. The workflow accepts `workflow_dispatch` for exactly this.
4. Confirm the run logs `Dispatched deploy.yml` and that a corresponding run appears at
   `claude-code-ultimate-guide-landing/actions/workflows/deploy.yml`.
5. Revoke the old token.

### Reading a failure

The workflow distinguishes the failure modes rather than surfacing a bare 401 — an absent
secret and an expired one otherwise look identical, since an empty token sends an
unauthenticated request.

| Symptom | Meaning | Action |
|---|---|---|
| `LANDING_DEPLOY_TOKEN is not set` | Secret missing or emptied | Add it (step 2 above) |
| `HTTP 401 Bad credentials` | Token expired or revoked | Rotate |
| `HTTP 403 Forbidden` | Token lacks Actions: write, or owner lost repo access | Re-scope |
| `HTTP 404` | Workflow absent, or repo outside the token's scope | Check the scope first; a fine-grained token reports out-of-scope repos as 404, not 403 |

Any other status is rethrown unchanged: it is an API problem, not a credential one.

**A failure here does not block the landing deploy.** Pushing directly to the landing repo
still deploys it. What breaks is only the guide-to-landing automatic rebuild, so the site
keeps serving the previous guide content until someone notices — which is why the job is
set to fail loudly rather than pass quietly.

## Guide Reader Rebuild (every release)

The landing exposes guide content at `cc.bruniaux.com/guide/`. Content is generated from this repo at build time — **never committed in the landing**.

```bash
# From the landing repo, before each push to main:
cd ../claude-code-ultimate-guide-landing
node scripts/prepare-guide-content.mjs && pnpm build
```

**When to do this**: at every release (`/release patch|minor|major`) so the site reflects the latest guide version.

## Verification Command

```bash
./scripts/check-landing-sync.sh
```

**What the script checks (4 verifications):**

| Check | Source | Comparison |
|-------|--------|-----------|
| Version | `VERSION` | index.html (footer + FAQ) |
| Templates | `find examples/` | index.html + examples.html |
| Quiz questions | `questions.json` | index.html + quiz.html |
| Guide lines | `wc -l ultimate-guide.md` | index.html (tolerance ±500) |

**Expected output (if synced):**
```
=== Landing Site Sync Check ===

1. Version
   Guide:   3.8.1
   Landing: 3.8.1
   OK
...
=== Summary ===
All synced!
```

If mismatch: exit code = number of issues found. Check `landing/CLAUDE.md` for exact line numbers to modify.

## Search Index (Cmd+K)

The landing's Cmd+K search palette includes guide entries generated from `machine-readable/reference.yaml` (the `deep_dive` section).

```bash
# From the landing repo, after any reference.yaml change:
cd ../claude-code-ultimate-guide-landing
pnpm build:search
```

The script (`scripts/build-guide-index.mjs`) regenerates `src/data/guide-search-entries.ts`. How it handles anchors: for guide files served locally at `/guide/<slug>/`, the anchor is stripped and the search result links to the top of the page. For everything else, the entry links to GitHub with the anchor kept, so a stale anchor there means a dead link in prod.

**When to rebuild**: after adding, removing, or renaming `deep_dive` keys in `reference.yaml`. Anchor-only changes on locally served guide files don't alter the generated URLs, but keeping the YAML accurate matters anyway since it's the LLM-facing index.

File: `src/components/global/AnnouncementBanner.astro` (landing repo)

**Update workflow**:
1. Edit banner text in the component
2. Bump `BANNER_ID` (e.g., `banner-guide-2026-04`) to reset dismissed state for all visitors
3. `pnpm build` + commit + push

**When to update**: major new page, important section added, guide milestone, visible new feature.

## RSS Feed

The landing exposes a unified RSS feed at `/rss.xml`.

**Two merged sources** (sorted by date, 50 entries max):
1. CC releases: auto from `src/data/releases.ts`
2. Guide entries: **manual** in `src/data/rss-entries.ts`

**Available types**: `guide_release | new_page | new_cheatcard | new_whitepaper | new_section`

**When to add a manual entry**:
- New page added to the site (`new_page`)
- New card series (`new_cheatcard`)
- New whitepaper available (`new_whitepaper`)
- Major new section in the guide (`new_section`)

## Sitemap

File: `src/pages/sitemap/index.astro` (landing repo)

**Rule**: add each new page to the sitemap. Sections are in the `sections` array in the Astro frontmatter.
