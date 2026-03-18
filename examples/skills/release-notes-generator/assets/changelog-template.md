# CHANGELOG Section Template

Use this template for generating CHANGELOG.md entries.

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Objective
[1-2 sentence summary of this release]

### New Features

#### [Feature Name] (#PR_NUMBER)
- **Description** : [Clear functional description]
- **Spec link** : [Link to spec if available]
- **Impacted components** : `component-a`, `service-b`, etc.
- **Impact** : [Who is affected: End-users / Admins / All]

### Bug Fixes

#### [Module/Component] (#PR_NUMBER)
- **Issue** : [Bug description]
- **Cause** : [Root cause identified]
- **Fix** : [Fix description]
- **[Error tracker]** : PROJECT-XX (if applicable)

### Technical Improvements

#### Performance
- [Optimization description with measurable impact if possible]

#### UI/UX
- [Interface improvement description]

#### Architecture
- [Significant refactoring description]

### Security
- **[CVE-XXXX-XXXXX]** : [Description and impact]

### Database Migrations

#### Deployment Process

**Step 1: Apply migrations**
```bash
[migration-command]
```

**Step 2: Data migration scripts** (if applicable)
```bash
[data-migration-command]
```

**Post-migration verification**
```sql
-- Verification queries
SELECT COUNT(*) FROM [table];
```

### Breaking Changes

**None** or:

- **[Component/API]** : Breaking change description
  - **Migration required** : How to migrate
  - **Impact** : Who is affected

### Deprecations

**None** or:

- **[Feature X]** : Deprecated in this version
  - **Reason** : Why
  - **Alternative** : What to use instead
  - **Planned removal** : Version X.Y.Z

### Tests
- [X] unit tests for [feature]
- [X] integration tests for [module]

### Statistics
- **PRs** : #XX, #YY, #ZZ
- **Files impacted** : XX+
- **New tables** : [list if applicable]
- **Migrations** : X migrations
- **Breaking changes** : 0

### Links
- PR: https://github.com/{owner}/{repo}/pull/XXX
- Included PRs : #XX, #YY, #ZZ
- [Error tracker] issues : PROJECT-XX
```
