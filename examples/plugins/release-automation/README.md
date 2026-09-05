# Release Automation Plugin

Semantic versioning, changelog generation, and release management.

## Install

```bash
bash install.sh
```

## Components

- **/release command**: Semantic version bumping and tagging
- **/changelog command**: Generate release notes from commits
- **release-notes-generator skill**: Automated release documentation
- **version-sync hook**: Keep version consistent across files

## Quick Start

```bash
# Bump version and create release
/release patch      # v1.0.0 → v1.0.1
/release minor      # v1.0.1 → v1.1.0
/release major      # v1.1.0 → v2.0.0

# Generate changelog
/changelog 10       # Last 10 releases

# The hook auto-syncs VERSION across docs
```

## Features

✓ Semantic versioning
✓ Automated changelog
✓ Git tagging
✓ Release notes
✓ Version consistency

---

See `guide/workflows/releases-tracking.md` for version management.
