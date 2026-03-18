---
title: "Database Branch Setup with Worktrees"
description: "Guide for isolated feature development using database branches with Neon or PlanetScale"
tags: [workflow, git, devops]
---

# Database Branch Setup with Worktrees

Complete guide for isolated feature development with database branches.

**Source**: Inspired by [Neon database branching](https://neon.tech/docs/guides/branching) and [PlanetScale branching workflows](https://planetscale.com/docs/concepts/branching).

---

## TL;DR (90% Use Case)

**Using Neon:**
```bash
/git-worktree feature/auth
cd .worktrees/feature-auth
neonctl branches create --name feature-auth --parent main
# Copy DATABASE_URL from output to .env
pnpm prisma migrate dev
```

Done. Skip to [workflow examples](#workflow-examples).

---

## Provider Setup

### Neon (Recommended)

**Install CLI:**
```bash
npm install -g neonctl
neonctl auth
```

**Create branch:**
```bash
neonctl branches create --name <branch-name> --parent main
```

**Get connection string:**
```bash
neonctl connection-string --branch <branch-name>
```

**Update .env in worktree:**
```bash
echo "DATABASE_URL=<connection-string>" > .worktrees/<branch>/.env
```

**Delete when done:**
```bash
neonctl branches delete <branch-name>
```

**Strengths:**
- Instant branch creation (~1s)
- True copy-on-write (efficient storage)
- Branch resets without data loss
- Excellent CLI

**Limitations:**
- Connection pooling configuration needed

---

### PlanetScale

**Install CLI:**
```bash
brew install pscale
pscale auth login
```

**Create branch:**
```bash
pscale branch create <database-name> <branch-name>
```

**Connect (spawns local proxy):**
```bash
pscale connect <database-name> <branch-name> --port 3309
```

**Update .env to use localhost:3309:**
```bash
echo "DATABASE_URL=mysql://root@127.0.0.1:3309/<database-name>" > .worktrees/<branch>/.env
```

**Delete when done:**
```bash
pscale branch delete <database-name> <branch-name>
```

**Strengths:**
- Git-like workflow for schema
- Built-in schema diff
- Safe deploy requests

**Limitations:**
- Different connection string per branch
- Requires `pscale connect` for local dev

---

### Local Postgres (Schema-based)

For projects without cloud DB:

**Create schema:**
```bash
psql $DATABASE_URL -c "CREATE SCHEMA <schema-name>;"
```

**Update .env to use schema:**
```bash
DATABASE_URL="postgresql://user:pass@localhost:5432/db?schema=<schema-name>"
```

**Run migrations in schema:**
```bash
npx prisma migrate deploy
```

**Cleanup:**
```bash
psql $DATABASE_URL -c "DROP SCHEMA <schema-name> CASCADE;"
```

**Strengths:**
- Free
- Full control

**Limitations:**
- Manual setup
- No automatic copy-on-write

---

## When to Use Database Branches

### Decision Tree

```
Does feature touch database schema?
├─ No → Use shared database, skip branch creation
└─ Yes → Create database branch
    ├─ Using Neon/PlanetScale? → Use native branching
    ├─ Using local Postgres? → Create dedicated schema
    └─ Other provider? → Consider Docker or shared DB with caution
```

### Scenario Table

| Scenario | Use DB Branch? | Rationale |
|----------|---------------|-----------|
| Adding database migrations | ✅ Yes | Isolate schema changes |
| Refactoring data model | ✅ Yes | Safe to experiment |
| Performance testing | ✅ Yes | Dedicated resources |
| Bug fix (no schema change) | ❌ No | Shared DB is fine |
| Feature with schema changes | ✅ Yes | Avoid conflicts |
| Hotfix (urgent) | ❌ No | Speed over isolation |

---

## Workflow Examples

### Example 1: Schema Migration Feature

```bash
# 1. Create worktree + DB branch
/git-worktree feature/add-user-roles
cd .worktrees/feature-add-user-roles

# 2. Create Neon branch
neonctl branches create --name feature-add-user-roles --parent main

# 3. Update .env with new DATABASE_URL
# (Copy from neonctl output)

# 4. Create migration in steps
npx prisma migrate dev --name step1_add_role_column
npx prisma migrate dev --name step2_migrate_existing_users
npx prisma migrate dev --name step3_add_constraints

# 5. Test entire migration sequence
pnpm prisma migrate reset --skip-seed
pnpm prisma migrate deploy
pnpm test

# 6. If successful, merge PR
# 7. Apply to main DB after deploy
```

---

### Example 2: Data Model Experimentation

```bash
# Try different schemas without commitment
/git-worktree experiment/normalize-addresses
cd .worktrees/experiment-normalize-addresses

# Create DB branch
neonctl branches create --name experiment-normalize-addresses --parent main

# Completely remodel data
# Test with real-ish data
# Compare performance

# If better → merge
# If worse → delete branch (no cleanup needed)
```

---

### Example 3: Parallel Feature Development

```bash
# Terminal 1
/git-worktree feature/payments
cd .worktrees/feature-payments
neonctl branches create --name feature-payments --parent main
# DATABASE_URL → feature-payments branch

# Terminal 2
/git-worktree feature/subscriptions
cd .worktrees/feature-subscriptions
neonctl branches create --name feature-subscriptions --parent main
# DATABASE_URL → feature-subscriptions branch

# Both can modify schema independently
# No conflicts until merge
```

---

## Checklist

### Before starting work in worktree with DB changes:
- [ ] `.worktreeinclude` contains `.env`
- [ ] Database branch created (if provider supports it)
- [ ] `.env` in worktree updated with new `DATABASE_URL`
- [ ] Connection tested (`npx prisma db execute --stdin <<< "SELECT 1;"`)
- [ ] Migrations applied (`npx prisma migrate dev`)

### After PR merge:
- [ ] Git worktree removed
- [ ] Database branch deleted
- [ ] No orphaned connections

---

## Troubleshooting

### Issue: "Database not found" in worktree
**Fix:** Check `.env` was copied, verify `.worktreeinclude` setup

### Issue: Migrations affect main database
**Fix:** Verify `DATABASE_URL` points to branch, not main

### Issue: Can't create Neon branch - "not authenticated"
**Fix:** Run `neonctl auth` to log in

### Issue: PlanetScale branch exists but can't connect
**Fix:** Use `pscale connect` proxy, don't connect directly

### Issue: "Branch already exists"
```bash
# List existing branches
neonctl branches list

# Delete if stale
neonctl branches delete <branch-name> --force
```

### Issue: Migration failed
```bash
# Reset DB branch to clean state
neonctl branches reset <branch-name> --parent main

# Re-apply migrations
npx prisma migrate deploy
```

---

## Security Notes

⚠️ **Remember:**
- Database branches are NOT in `.gitignore` by default
- Add `.env` to `.worktreeinclude` so credentials are copied
- Never commit `DATABASE_URL` with real credentials
- Use different credentials per environment

✅ **Best Practice:**
```bash
# .worktreeinclude
.env
.env.local
.env.development

# Each worktree gets copy of credentials
# But each points to different DB branch
```

---

## Advanced Patterns

### Pattern: Progressive Schema Migration

```bash
# 1. Create worktree + DB branch
/git-worktree migration/split-user-table
cd .worktrees/migration-split-user-table

# 2. Create migration in steps
npx prisma migrate dev --name step1_add_new_columns
npx prisma migrate dev --name step2_migrate_data
npx prisma migrate dev --name step3_drop_old_columns

# 3. Test entire migration sequence
pnpm prisma migrate reset --skip-seed
pnpm prisma migrate deploy

# 4. If successful, merge PR
# 5. Apply to main DB after deploy
```

### Pattern: Performance Benchmarking

```bash
# Create worktree with isolated DB
/git-worktree perf/optimize-queries
cd .worktrees/perf-optimize-queries

# DB branch lets you:
# - Add indexes without affecting dev
# - Run load tests safely
# - Compare before/after metrics

# Merge proven optimizations only
```

---

**Related guides:**
- [Git Worktree Command Reference](../commands/git-worktree.md)
- [Neon Branching Docs](https://neon.tech/docs/guides/branching)
- [PlanetScale Branching](https://planetscale.com/docs/concepts/branching)