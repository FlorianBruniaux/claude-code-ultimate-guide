---
title: "Dual-Instance Planning Workflow"
description: "Use two Claude instances with distinct roles for planning and implementation"
tags: [workflow, architecture, design-patterns]
---

# Dual-Instance Planning Workflow

> **Confidence**: Tier 2 — Based on practitioner experience (Jon Williams, Feb 2026). Pattern validated through personal transition Cursor → Claude Code over 6 months.

Use two Claude instances with distinct roles: one for planning and review (Claude Zero), one for implementation (Claude One). Separation of concerns improves plan quality and reduces implementation errors.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [When to Use This Pattern](#when-to-use-this-pattern)
3. [Setup](#setup)
4. [Complete Workflow](#complete-workflow)
5. [Plan Template](#plan-template)
6. [Cost Analysis](#cost-analysis)
7. [Tips and Troubleshooting](#tips-and-troubleshooting)
8. [See Also](#see-also)

---

## TL;DR

```
1. Launch Claude Zero (planner): explores, writes plans, reviews
2. Launch Claude One (implementer): reads plans, codes, commits
3. Human gatekeeper: approve plans before implementation
4. Plans directory: Review/ → Active/ → Completed/
5. Cost: ~$100-200/month (vs $500-1K for Boris horizontal pattern)
```

**Best for**: Solo devs, spec-heavy work, quality > speed, budget <$300/month

---

## When to Use This Pattern

### ✅ Use When

- **Complex specifications**: Requirements need clarification through interview-style questions
- **Quality-critical features**: Security, payments, data migrations
- **Learning phase**: New codebase, unfamiliar patterns
- **Product designers coding**: Non-dev background, need planning rigor
- **Budget constraints**: $100-200/month (vs $500-1K for parallel multi-instance)
- **Spec-heavy workflows**: Detailed requirements, many edge cases

### ❌ Don't Use When

- **Simple changes**: Typo fixes, trivial refactors (use single instance)
- **Exploratory coding**: Problem space unknown (planning overhead not justified)
- **Tight deadlines**: Speed > quality (accept correction loops)
- **High-volume parallel features**: Use Boris pattern (Section 9.17) instead
- **Very limited budget**: <$100/month (use Sonnet, single instance)

### Comparison to Other Patterns

| Pattern | Scaling Axis | Cost/Month | Best For |
|---------|--------------|------------|----------|
| **Single instance** | None | $50-100 | Most developers, general use |
| **Dual-instance (Jon)** | Vertical (plan ↔ implement) | $100-200 | Spec-heavy, quality focus |
| **Multi-instance (Boris)** | Horizontal (5-15 parallel) | $500-1,000 | Teams, high-volume shipping |

---

## Setup

### Step 1: Create Directory Structure

```bash
cd ~/projects/your-project
mkdir -p .claude/plans/{Review,Active,Completed}
```

**Directory roles**:
- `Review/` — Plans awaiting human approval
- `Active/` — Approved plans under implementation
- `Completed/` — Archived plans (learning resource)

**Add to .gitignore**:
```bash
# .gitignore
.claude/plans/Review/
.claude/plans/Active/
# Optional: commit Completed/ for team learning
```

### Step 2: Launch Claude Zero (Planner)

**Terminal 1**:
```bash
cd ~/projects/your-project
claude
```

**First message** (role enforcement):
```
You are Claude Zero (Planner).

Your role:
- Explore codebase using Plan Mode (Shift+Tab twice)
- Interview user about requirements
- Write detailed plans to .claude/plans/Review/
- Review implementations after Claude One completes them
- NEVER edit code directly
- NEVER commit changes

Start by acknowledging this role.
```

Claude Zero confirms: "Understood. I am Claude Zero (Planner). I will explore, plan, and review, but never touch code."

### Step 3: Launch Claude One (Implementer)

**Terminal 2** (new session):
```bash
cd ~/projects/your-project
claude
```

**First message** (role enforcement):
```
You are Claude One (Implementer).

Your role:
- Read approved plans from .claude/plans/Active/
- Implement exactly as specified
- Commit changes after each logical step
- Report completion back to user
- NEVER create plans
- NEVER skip approval steps

Start by acknowledging this role.
```

Claude One confirms: "Understood. I am Claude One (Implementer). I execute approved plans only."

---

## Complete Workflow

### Phase 1: Planning (Claude Zero)

#### Step 1.1: Initiate Planning

**You** (to Claude Zero):
```
# Enter Plan Mode (Shift+Tab twice), then:

Implement JWT authentication for the API:
- Access tokens (15min expiry)
- Refresh tokens (7 day expiry)
- Middleware to protect routes
- Logout capability (revoke refresh tokens)
```

#### Step 1.2: Claude Zero Explores

Claude Zero (in Plan Mode):
- Reads existing auth code
- Searches for auth patterns in codebase
- Identifies dependencies (libraries, env vars)

#### Step 1.3: Claude Zero Interviews You

Claude Zero asks clarifying questions:
```
Before I draft the plan, I need to clarify:

1. Should we support multiple concurrent sessions per user?
   (e.g., user logged in on phone + laptop simultaneously)

2. Where should refresh tokens be stored?
   - Database table
   - Redis
   - Other

3. Which routes should be protected?
   - All /api/* routes?
   - Specific routes only?

4. Do you want rate limiting on login attempts?

5. Success criteria for "done"?
   - Tests passing?
   - Postman collection?
   - Documentation updated?
```

**You answer**, Claude Zero refines understanding.

#### Step 1.4: Claude Zero Writes Plan

Claude Zero creates `.claude/plans/Review/auth-jwt.md`:

```markdown
# Plan: JWT Authentication

**Created**: 2026-02-04
**Author**: Claude Zero
**Estimated effort**: 3-4 hours
**Risk level**: Medium (security-critical)

## Summary
Implement JWT-based authentication with access/refresh token pattern.
Support multiple concurrent sessions per user.
Refresh tokens stored in database with revocation capability.

## Requirements Clarified
- Multiple sessions per user: YES
- Refresh token storage: Database (new table)
- Protected routes: All /api/* except /api/auth/*
- Rate limiting: YES (5 attempts per 15min)
- Success criteria: Tests pass + Postman collection

## Files to Create

### 1. src/auth/jwt.ts (~120 lines)
**Purpose**: JWT utility functions

**Exports**:
- `generateAccessToken(userId: string): string`
  - Payload: { userId, type: 'access' }
  - Expiry: 15 minutes
  - Sign with JWT_SECRET

- `generateRefreshToken(userId: string): string`
  - Payload: { userId, type: 'refresh', jti: uuid() }
  - Expiry: 7 days
  - Sign with JWT_REFRESH_SECRET
  - jti = unique token ID for revocation

- `verifyAccessToken(token: string): { userId: string } | null`
  - Verify signature
  - Check expiry
  - Return payload or null

- `verifyRefreshToken(token: string): { userId: string, jti: string } | null`
  - Verify signature
  - Check expiry
  - Check not revoked (database lookup)
  - Return payload or null

**Dependencies**: jsonwebtoken, uuid

### 2. src/middleware/auth.ts (~60 lines)
**Purpose**: Authentication middleware

**Exports**:
- `requireAuth(req, res, next)`
  - Extract token from Authorization header (Bearer format)
  - Verify using verifyAccessToken()
  - Attach userId to req.userId
  - 401 if invalid/missing

**Dependencies**: jwt.ts

### 3. src/db/migrations/YYYYMMDD_create_refresh_tokens.ts (~40 lines)
**Purpose**: Database table for refresh tokens

**Schema**:
```sql
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  jti UUID NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP NOT NULL,
  revoked_at TIMESTAMP
);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_jti ON refresh_tokens(jti);
```

## Files to Modify

### 1. src/routes/api.ts
**Location**: Line 23 (after imports)
**Change**: Add requireAuth middleware to all routes except /auth/*

**Before**:
```typescript
router.get('/profile', profileController);
router.post('/posts', createPostController);
```

**After**:
```typescript
import { requireAuth } from '../middleware/auth';
router.get('/profile', requireAuth, profileController);
router.post('/posts', requireAuth, createPostController);
```

### 2. src/routes/auth.ts
**Location**: Create new file OR add to existing auth routes
**Changes**:
- POST /auth/login → return { accessToken, refreshToken }
- POST /auth/refresh → exchange refresh token for new access token
- POST /auth/logout → revoke refresh token

### 3. src/config/env.ts
**Location**: Line 15 (after existing secrets)
**Add**:
```typescript
JWT_SECRET: process.env.JWT_SECRET || '',
JWT_REFRESH_SECRET: process.env.JWT_REFRESH_SECRET || '',
```

### 4. .env.example
**Add**:
```
JWT_SECRET=your-secret-here-min-32-chars
JWT_REFRESH_SECRET=your-refresh-secret-here-min-32-chars
```

## Implementation Steps (Sequential)

1. **Install dependencies**
   ```bash
   npm install jsonwebtoken uuid
   npm install --save-dev @types/jsonwebtoken @types/uuid
   ```

2. **Create JWT utilities** (jwt.ts)
   - Implement all 4 functions
   - Add error handling (try/catch on verify)

3. **Run database migration** (refresh_tokens table)
   - Test migration up/down

4. **Create auth middleware** (auth.ts)
   - Implement requireAuth
   - Test with mock token

5. **Create/update auth routes** (auth.ts routes)
   - POST /auth/login
   - POST /auth/refresh
   - POST /auth/logout

6. **Protect existing routes** (api.ts)
   - Apply requireAuth to all /api/* routes

7. **Add JWT secrets to .env**
   - Generate secure random strings (64 chars)

8. **Write tests**
   - Unit tests for jwt.ts functions
   - Integration tests for auth flow
   - Test token expiry
   - Test revocation

9. **Create Postman collection**
   - Login → get tokens
   - Access protected route with access token
   - Refresh access token
   - Logout → revoke refresh token
   - Verify revoked token rejected

## Success Criteria

- [ ] POST /auth/login returns accessToken + refreshToken
- [ ] Protected routes return 401 without valid access token
- [ ] Protected routes return 200 with valid access token
- [ ] POST /auth/refresh exchanges refresh token for new access token
- [ ] POST /auth/logout revokes refresh token
- [ ] Revoked refresh tokens are rejected on /auth/refresh
- [ ] Expired access tokens are rejected
- [ ] Multiple sessions per user work (different refresh tokens)
- [ ] All tests pass (npm test)
- [ ] Postman collection works end-to-end

## Security Checklist

- [ ] JWT secrets are in .env (never committed)
- [ ] JWT secrets are ≥32 characters
- [ ] Refresh tokens stored in database (not just JWT)
- [ ] Refresh tokens have unique jti for revocation
- [ ] Access tokens have short expiry (15min)
- [ ] Authorization header validated (Bearer format)
- [ ] Token verification errors are caught (no crashes)

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| JWT secrets leaked | High | .env in .gitignore, never log secrets |
| Token expiry too long | Medium | 15min access, 7 day refresh (short enough) |
| No rate limiting on login | Medium | Add rate limiting (5 attempts/15min) |
| Refresh token table grows indefinitely | Low | Add cleanup job (delete expired tokens) |

## Questions for Implementer (Claude One)

If you encounter these scenarios during implementation:

1. **Existing user login flow**: Integrate with existing login logic, don't replace entire auth system
2. **Database ORM**: Use existing ORM (Prisma/TypeORM/Knex) for refresh_tokens table
3. **Error messages**: Return generic "Invalid token" (don't leak whether token is expired vs invalid signature)

## Estimated Effort Breakdown

- JWT utilities: 45 min
- Database migration: 15 min
- Middleware: 30 min
- Auth routes: 60 min
- Protect existing routes: 15 min
- Tests: 90 min
- Postman collection: 15 min

**Total**: ~4 hours

---

**Plan approved?** → Move to `.claude/plans/Active/auth-jwt.md`
```

### Phase 2: Human Review

**You review** `.claude/plans/Review/auth-jwt.md`:

**Checklist**:
- [ ] All requirements covered?
- [ ] Approach makes sense for this codebase?
- [ ] Security considerations addressed?
- [ ] Estimated effort realistic?
- [ ] Success criteria clear and testable?
- [ ] Files to create/modify are correct paths?

**If approved**:
```bash
mv .claude/plans/Review/auth-jwt.md .claude/plans/Active/
```

**If changes needed**, ask Claude Zero to revise:
```
(to Claude Zero): Update the plan:
- Change refresh token expiry to 30 days instead of 7
- Add password reset flow to scope
```

### Phase 3: Implementation (Claude One)

**You** (to Claude One):
```
Implement .claude/plans/Active/auth-jwt.md

Follow the plan exactly. Commit after each logical step.
Report back when complete.
```

Claude One:
1. Reads plan file
2. Installs dependencies
3. Creates jwt.ts
4. Creates database migration
5. Runs migration
6. Creates auth middleware
7. Updates routes
8. Adds env vars
9. Writes tests
10. Creates Postman collection

**Claude One commits** after each step:
```
feat: add JWT utility functions
feat: create refresh_tokens table migration
feat: add auth middleware
feat: protect API routes with JWT auth
test: add JWT auth flow tests
```

### Phase 4: Verification (Claude Zero)

**You** (to Claude Zero):
```
Review the JWT implementation Claude One just completed.
Check against the plan in .claude/plans/Active/auth-jwt.md.
```

Claude Zero reviews:
- Code structure matches plan?
- All success criteria met?
- Security checklist completed?
- Tests passing?
- Any code smells or issues?

**Claude Zero report**:
```
✅ Review complete: auth-jwt.md

Code Quality: 9/10
- All files created as planned
- Success criteria met (9/9)
- Security checklist complete
- Tests pass (15/15)

Minor suggestions:
1. Consider adding refresh token rotation (security best practice)
2. Add JSDoc comments to jwt.ts functions
3. Consider extracting magic numbers (15min, 7 days) to config

Critical issues: None

Ready to archive plan to Completed/.
```

### Phase 5: Archive

**If approved**:
```bash
mv .claude/plans/Active/auth-jwt.md .claude/plans/Completed/
```

**Plan is now archived** for future reference and team learning.

---

## Plan Template

Save this template to `.claude/plan-template.md` for consistent plan structure:

```markdown
# Plan: [Feature Name]

**Created**: [Date]
**Author**: Claude Zero
**Estimated effort**: [Hours]
**Risk level**: Low | Medium | High

## Summary
[2-3 sentence overview of what this plan accomplishes]

## Requirements Clarified
[List of requirements confirmed through interview]
- Requirement 1: [Answer]
- Requirement 2: [Answer]

## Files to Create

### 1. [File path] (~[Lines] lines)
**Purpose**: [What this file does]

**Exports**:
- `functionName(params): returnType`
  - [What it does]
  - [Key implementation details]

**Dependencies**: [Libraries, other files]

## Files to Modify

### 1. [File path]
**Location**: Line [N] ([Context: after what, before what])
**Change**: [What to change]

**Before**:
```[language]
[Existing code snippet]
```

**After**:
```[language]
[Modified code snippet]
```

## Implementation Steps (Sequential)

1. **[Step name]**
   - [Substep]
   - [Substep]

2. **[Step name]**
   - [Substep]

## Success Criteria

- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

## Security Checklist (if applicable)

- [ ] [Security item 1]
- [ ] [Security item 2]

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [High/Med/Low] | [How to prevent/handle] |

## Questions for Implementer (Claude One)

If you encounter these scenarios during implementation:
1. [Scenario]: [Guidance]

## Estimated Effort Breakdown

- [Task 1]: [Time]
- [Task 2]: [Time]

**Total**: [Hours]

---

**Plan approved?** → Move to `.claude/plans/Active/[filename].md`
```

---

## Cost Analysis

### Dual-Instance vs Single Instance with Corrections

| Scenario | Single Instance | Dual Instance | Savings |
|----------|----------------|---------------|---------|
| **Simple feature** (login form) | 1 session × $5 = **$5** | 2 sessions × $3 = $6 | +$1 (single wins) |
| **Medium feature** (auth system) | 1 session × $15 + 2 corrections × $10 = **$35** | 2 sessions × $12 = $24 | **$11 saved** |
| **Complex feature** (ambiguous spec) | 1 session × $20 + 3 corrections × $15 = **$65** | 2 sessions × $18 = $36 | **$29 saved** |

**Breakeven point**: Features requiring ≥2 correction loops → dual-instance is cheaper.

### Monthly Budget Estimates

**Assumptions**:
- 20 working days/month
- 2 features per day (mix of simple + complex)
- Opus 4.5 pricing (~$15/1M input, $75/1M output)

| Profile | Features/Month | Single Instance | Dual Instance | Savings |
|---------|----------------|----------------|---------------|---------|
| **Light user** | 20 simple | $100 | $120 | -$20 (single wins) |
| **Moderate user** | 30 mixed (60% medium, 40% simple) | $650 | $480 | **$170 saved** |
| **Heavy user** | 40 complex | $2,000 | $1,200 | **$800 saved** |

**Recommendation**:
- Simple features only → Single instance
- Medium/complex features → Dual instance saves money and time

---

## Tips and Troubleshooting

### Role Enforcement

**Problem**: Claude Zero starts editing code.

**Solution**: Remind in every request:
```
(to Claude Zero): Remember: you are Claude Zero (Planner only).
Do not edit code. Write plan to .claude/plans/Review/
```

**Prevention**: Use CLAUDE.md to enforce roles:

```markdown
# .claude/CLAUDE.md

## If you are Claude Zero (Planner):
- Use Plan Mode (Shift+Tab twice) for all exploration
- Save all plans to .claude/plans/Review/[feature].md
- NEVER edit code
- NEVER commit changes
- Review implementations after Claude One completes them

## If you are Claude One (Implementer):
- Read plans from .claude/plans/Active/
- Implement exactly as specified
- Commit after each logical step
- NEVER create plans
```

### Context Pollution

**Problem**: Claude One's context is polluted with planning discussions.

**Solution**: Use separate terminal sessions (separate contexts):
- Terminal 1 = Claude Zero (planning context)
- Terminal 2 = Claude One (implementation context)

**Never share context** between Claude Zero and Claude One.

### Plan Drift

**Problem**: Claude One deviates from plan during implementation.

**Solution**: Include this in plan:
```markdown
## Implementation Rules for Claude One

- Follow plan steps sequentially (don't skip or reorder)
- If you encounter blockers, STOP and report (don't improvise)
- Commit after each step (granular history)
- If unclear, ask user (don't guess)
```

### Overhead Management

**Problem**: Moving files between directories is manual overhead.

**Solution**: Create bash aliases:

```bash
# Add to ~/.bashrc or ~/.zshrc

# Move plan to Active (approve)
approve-plan() {
    mv ".claude/plans/Review/$1.md" ".claude/plans/Active/"
    echo "✅ Approved: $1.md → Active/"
}

# Move plan to Completed (archive)
complete-plan() {
    mv ".claude/plans/Active/$1.md" ".claude/plans/Completed/"
    echo "✅ Completed: $1.md → Archived"
}

# List plans by status
plans() {
    echo "📋 Review:"
    ls -1 .claude/plans/Review/ 2>/dev/null || echo "  (empty)"
    echo ""
    echo "🔄 Active:"
    ls -1 .claude/plans/Active/ 2>/dev/null || echo "  (empty)"
    echo ""
    echo "✅ Completed:"
    ls -1 .claude/plans/Completed/ 2>/dev/null | tail -5 || echo "  (empty)"
}
```

**Usage**:
```bash
plans                     # List all plans
approve-plan auth-jwt     # Approve plan
complete-plan auth-jwt    # Archive completed plan
```

---

## See Also

- **Main guide**: [Section 9.17.1](../ultimate-guide.md#alternative-pattern-dual-instance-planning-vertical-separation) — Overview and comparison
- **Plan Mode**: [plan-driven.md](plan-driven.md) — Foundation for planning workflows
- **Multi-Instance (Boris)**: [Section 9.17](../ultimate-guide.md#917-scaling-patterns-multi-instance-workflows) — Horizontal scaling alternative
- **Cost optimization**: [Section 8.10](../ultimate-guide.md#810-cost-optimization) — Budget management

**External resources**:
- [Jon Williams LinkedIn post](https://www.linkedin.com/posts/thatjonwilliams_ive-been-using-cursor-for-six-months-now-activity-7424481861802033153-k8bu) — Original pattern description (Feb 3, 2026)
- [10 Tips from Claude Code Team](https://paddo.dev/blog/claude-code-team-tips/) — Team workflows including plan-first approach
