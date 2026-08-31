# Distributing the Claude Code Ultimate Guide

The guide already has strong reference depth. Distribution work should make a useful first result easier to find, finish, translate, and attribute. It should not turn the main guide into promotional copy.

## Boundary

This workflow prepares assets and records channels. Publication, marketplace submission, outreach, license changes, and messages sent in the author's name require separate authorization.

Use three connected sources of truth:

- [`machine-readable/distribution-channels.yaml`](../../machine-readable/distribution-channels.yaml) records the channel, locale, asset, owner, state, attributed URL, and 30-day outcome fields;
- [`machine-readable/translations.json`](../../machine-readable/translations.json) records translation ownership and freshness;
- [the translation workflow](translations.md) defines what `current`, `stale`, and community-maintained mean.

## One outcome per asset

Each distribution asset should promise a result that can be completed and verified.

| Asset | Reader outcome | Destination |
| --- | --- | --- |
| Repository README | Decide whether the guide fits the reader's goal | [Guide navigation](../../guide/README.md) |
| Landing page | Reach the right learning or reference entry point | [Learning path](../../guide/learning-path/README.md) |
| Release note | Understand what changed and who should care | [CHANGELOG](../../CHANGELOG.md) |
| EPUB | Read the versioned reference offline | [Export workflow](whitepaper-build.md) |
| Slide deck | Teach one bounded workflow | [Learning path slides](../distribution/claude-code-learning-path-slides.pptx) |
| Quick-win video | Complete one task and inspect its proof | [Quick-win video series](../distribution/quick-win-video-series.md) |
| Directory entry | Qualify the resource in one paragraph | [Comparative audit](../resource-evaluations/mltut-learning-resources-comparative-audit.md) |

## Channel record

Add a channel before producing its asset. Use a stable ID and keep the canonical destination separate from the attributed link.

```json
{
  "id": "youtube-fr",
  "channel": "youtube",
  "locale": "fr",
  "owner": "Florian Bruniaux",
  "asset": "planned: quick-win video series",
  "asset_status": "planned",
  "production_brief": "docs/distribution/quick-win-video-series.md",
  "production_brief_status": "ready",
  "canonical_url": "https://www.youtube.com/",
  "tagged_url": "https://cc.bruniaux.com/?utm_source=youtube&utm_medium=video&utm_campaign=ccug-learning-path-2026",
  "status": "planned",
  "placement_status": "planned",
  "published_at": null,
  "observed_at": null,
  "submission_date": null,
  "measurement_started_at": null,
  "placement_evidence_url": null,
  "placement_verified_at": null,
  "outcome": {
    "impressions": null,
    "visits": null,
    "clones": null,
    "stars": null
  }
}
```

The `.yaml` registry deliberately contains JSON-compatible YAML. The validator therefore uses only the Python standard library.

## Status model

`asset_status` describes production readiness. `status` and `placement_status` describe the campaign placement. A ready asset can therefore remain `blocked` while approval or a fluent reviewer is missing.

| Status | Meaning | Required next action |
| --- | --- | --- |
| `planned` | Outcome and destination are defined | Produce the asset |
| `ready` | Asset exists and passed its checks | Obtain publication approval |
| `submitted` | An external platform received it | Record the submission date |
| `published` | The campaign link is publicly placed and verified | Record the evidence URL, verification date, and 30-day window start |
| `blocked` | A named dependency is missing | Assign the owner or produce the prerequisite |

Do not change `blocked` to `ready` because the prose exists. A Chinese Bilibili asset, for example, also needs a current translation, a reviewer who reads the locale, a thumbnail, and publication authority.

## Translation gate

Before producing a localized asset:

1. run `python3 scripts/check-translations.py`;
2. inspect the language's recorded version and source hash;
3. name the community maintainer when the translation is not official;
4. link to the translation's canonical repository;
5. send no translated submission until a fluent reviewer validates the copy.

The guide's Chinese translation is community-maintained. The registry describes its observed coverage and freshness; it carries no official full-guide publication claim.

## Quick-win series

A useful first series contains four bounded episodes:

1. first verified fix in 15 minutes;
2. choose between a skill, subagent, and MCP server;
3. build and test one safe hook;
4. compare several candidate solutions and preserve the proof bundle.

Each episode links to one canonical page, uses the channel's attributed URL, and ends with an observable check. Timestamped transcript evidence can later be indexed through YT Insights, but a successful upload does not prove that the lesson taught the intended skill.

The production-ready briefs are in the [quick-win video series](../distribution/quick-win-video-series.md). The [learning path slides](../distribution/claude-code-learning-path-slides.pptx) provide a shared nine-slide narrative for talks, workshops, and video planning. Both assets remain unpublished until the channel owner approves the external action.

## Thirty-day measurement

Record the same four raw measures for every channel after `measurement_started_at`:

- impressions, when the platform exposes them;
- visits to the tagged destination;
- repository clones;
- stars.

Keep missing measures as `null`. Do not convert missing analytics into zero. Compare channels only over the same 30-day observation window and retain the publication date, observation date, measurement start, locale, asset, and campaign.

The dates answer different questions:

- `published_at`: when the asset itself became public, if known;
- `observed_at`: when the public asset was directly observed;
- `submission_date`: when the campaign placement was submitted;
- `placement_verified_at`: when the attributed campaign link was verified on the public channel;
- `measurement_started_at`: when the 30-day outcome window began.

An existing public asset may still have campaign status `planned`. Public existence does not prove that the attributed campaign link was placed.

Stars alone do not identify learning completion or guide quality. They measure one visible action after exposure.

## Validation

Run:

```bash
python3 scripts/check-distribution-channels.py
python3 -m unittest scripts/test-check-distribution-channels.py
```

The validator checks identifiers, HTTPS destinations, attribution parameters, campaign consistency, asset and placement state coherence, non-future date order, placement evidence, the 30-day window, and non-negative outcome measures. It does not visit external pages or prove that an evidence URL still contains the attributed link.

## Related reading

- [Learning-resource comparative audit](../resource-evaluations/mltut-learning-resources-comparative-audit.md)
- [Distribution assets](../distribution/README.md)
- [Translation maintenance](translations.md)
- [Structured learning path](../../guide/learning-path/README.md)
- [Learning with AI](../../guide/roles/learning-with-ai.md)
- [Talk production workflow](../../guide/workflows/talk-pipeline.md)
