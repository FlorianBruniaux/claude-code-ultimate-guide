# Claude Code Releases Tracking

This repo maintains a condensed history of official Claude Code releases.

## Files

| File | Role |
|------|------|
| `machine-readable/claude-code-releases.yaml` | Local source of truth for the condensed release history and `latest` value |
| `guide/core/claude-code-releases.md` | Human-readable version (Markdown) |
| `mcp-server/content/claude-code-releases.yaml` | Byte-identical release registry bundled with the MCP package |
| `llms.txt`, `machine-readable/llms.txt`, `mcp-server/content/llms.txt` | Byte-identical discovery indexes that announce the tracked `latest` version |
| `scripts/update-cc-releases.sh` | Script for checking new versions |

Anthropic's official Claude Code changelog is the upstream source. The local YAML is a reviewed condensation, so local consistency does not prove that upstream tracking is current or complete.

## Check for New Versions

```bash
./scripts/update-cc-releases.sh
```

The script:
1. Fetches the official CHANGELOG from GitHub
2. Compares against our tracked version
3. Displays new releases to condense

## Update Workflow

1. **Verify**: `./scripts/update-cc-releases.sh`
2. **Update YAML**: Add new entry in `claude-code-releases.yaml`
   - Update `latest` and `updated`
   - Add entry in `releases` (condensed: 2-4 highlights max)
   - Add to `breaking_summary` if applicable
   - Add to `milestones` if major feature
3. **Update Markdown**: Update `claude-code-releases.md` consistently
4. **Update mirrors**: Copy the reviewed YAML to `mcp-server/content/claude-code-releases.yaml`
5. **Update discovery version**: Change the version sentence in all three `llms.txt` mirrors to the YAML `latest` value
6. **Validate local coupling**:

   ```bash
   python3 scripts/validate-reference-yaml.py --ci
   (cd mcp-server && node --test --test-name-pattern='canonical MCP guide is complete' test/render-product-docs.test.mjs)
   ```

7. **Landing sync**: `./scripts/check-landing-sync.sh`
8. **Commit**: `docs: update Claude Code releases (vX.Y.Z)`

The MCP test first requires the three `llms.txt` files to be byte-identical, then parses `machine-readable/claude-code-releases.yaml` and compares its `latest` value with the version announced in `llms.txt`. `npm run release:check` executes this test in the `index-integrity` CI workflow. The check proves repository and package consistency. It does not fetch Anthropic's changelog or prove release-summary completeness.

## YAML Entry Format

```yaml
- version: "2.1.13"
  date: "2026-01-20"
  highlights:
    - "Main feature"
    - "Other notable feature"
  breaking:
    - "Description of breaking change (if applicable)"
```
