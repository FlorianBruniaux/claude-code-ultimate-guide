---
title: "Memory Stack Integration: Real-World Multi-Day Workflow"
description: "5-day sprint example combining claude-mem, Serena, grepai and rg for auth refactoring"
tags: [workflow, memory, integration]
---

# Memory Stack Integration: Real-World Multi-Day Workflow

**Scenario**: Refactoring authentication system from session-based to JWT across a 5-day sprint

**Tools Used**: claude-mem (auto capture) + Serena (manual decisions) + grepai (discovery) + rg (exact search)

**Project**: E-commerce API (Node.js/TypeScript, 50k lines, 200+ files)

---

## Day 1: Discovery & Planning

### Morning: Initial Exploration

**User**: "Let's explore the current authentication system"

**Claude** (with no claude-mem yet):
```bash
# Manual discovery
rg "authenticate|session" --type ts | head -20
# 47 matches across 12 files
```

**Problem**: Too many files, no context on architecture decisions.

---

### After Installing claude-mem

```bash
# Install claude-mem
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
# Restart Claude Code
```

**User**: "Explore authentication architecture"

**Claude** (now with auto-capture):
```bash
# 1. SEMANTIC DISCOVERY (grepai)
grepai search "authentication and session management"
# → Finds:
#   - src/auth/auth.service.ts (main service)
#   - src/middleware/session.middleware.ts (session handling)
#   - src/controllers/user.controller.ts (endpoints)
#   - config/session.config.ts (session config)

# 2. STRUCTURAL OVERVIEW (Serena)
serena get_symbols_overview --file src/auth/auth.service.ts
# → AuthService class:
#   - login(email, password)
#   - logout(sessionId)
#   - validateSession(sessionId)
#   - createSession(userId)

# 3. CALL GRAPH (grepai)
grepai trace callers "createSession"
# → Called by:
#   - UserController.login() (47 times)
#   - AdminController.authenticate() (12 times)
#   - OAuthController.callback() (8 times)

# 4. EXACT SEARCH (rg)
rg "express-session" --type ts
# → Found in:
#   - package.json (dependency)
#   - session.middleware.ts (import)
#   - app.ts (config)
```

**claude-mem** automatically captures:
- 4 files read (auth.service.ts, session.middleware.ts, user.controller.ts, session.config.ts)
- 67 tool calls (reads, searches, traces)
- Key finding: "Current system uses express-session, stored in Redis"

---

### Afternoon: Architectural Decision

**User**: "Should we use JWT or stick with sessions?"

**Discussion**:
- JWT: Stateless, scalable, no Redis dependency
- Sessions: Server-side control, easy revocation
- **Decision**: JWT for API, keep sessions for web dashboard

**Record Decision (Serena)**:
```bash
serena write_memory "auth_architecture" "$(cat <<'EOF'
Decision: Migrate API to JWT, keep sessions for web dashboard.

Rationale:
- API clients (mobile, SPA) benefit from stateless JWT
- Web dashboard needs session revocation (admin logout)
- Hybrid approach: /api/* uses JWT, /admin/* uses sessions

Library choice: jose (vs jsonwebtoken)
- Lighter (40% fewer dependencies)
- Better TypeScript support
- Active maintenance (last update: 2 weeks ago)

Next steps:
1. Install jose
2. Create JwtService
3. Update UserController to use JWT for /api/* routes
4. Keep SessionMiddleware for /admin/* routes
EOF
)"
```

**claude-mem** automatically captures:
- Decision discussion (compressed summary)
- Serena write_memory call
- Rationale for JWT + jose library

---

### End of Day 1

**Claude** auto-generates session summary:
```
Session Summary (Day 1):
- Explored authentication system (4 key files identified)
- Current: express-session + Redis
- Decision: Migrate to JWT for API, keep sessions for admin
- Library: jose (lighter, better TS support)
- Next: Install jose, create JwtService
```

**claude-mem dashboard** (`http://localhost:37777`):
- Timeline: 67 observations
- Key files: auth.service.ts, session.middleware.ts
- Decision recorded: auth_architecture

---

## Day 2: Implementation Start

### Morning: Session Resume

**Claude** (auto-injected context):
```
📋 Previous Session (Day 1):
- Explored auth system (4 files: auth.service.ts, session.middleware.ts, user.controller.ts, session.config.ts)
- Decision: JWT for API, sessions for admin
- Library: jose (40% lighter than jsonwebtoken)
- Next steps: Install jose, create JwtService
```

**User**: "Let's implement JWT service"

**Claude** (already has context, no re-reading):
```bash
# Install jose
npm install jose

# Create JWT service
```

**Implementation**:
```typescript
// src/auth/jwt.service.ts
import * as jose from 'jose';

export class JwtService {
  private secret: Uint8Array;

  constructor(secretKey: string) {
    this.secret = new TextEncoder().encode(secretKey);
  }

  async generateToken(userId: string, email: string): Promise<string> {
    const jwt = await new jose.SignJWT({ userId, email })
      .setProtectedHeader({ alg: 'HS256' })
      .setIssuedAt()
      .setExpirationTime('24h')
      .sign(this.secret);

    return jwt;
  }

  async verifyToken(token: string): Promise<{ userId: string; email: string }> {
    const { payload } = await jose.jwtVerify(token, this.secret);
    return payload as { userId: string; email: string };
  }
}
```

**claude-mem** automatically captures:
- npm install jose
- JwtService implementation
- Method signatures (generateToken, verifyToken)

---

### Afternoon: Decision Checkpoint

**User**: "Should we add refresh tokens now or later?"

**Discussion**:
- Refresh tokens = better security (short access tokens)
- BUT: More complexity, need database storage
- **Decision**: Add in Phase 2 (after basic JWT works)

**Record Decision (Serena)**:
```bash
serena write_memory "jwt_refresh_tokens" "$(cat <<'EOF'
Decision: Defer refresh tokens to Phase 2

Rationale:
- Phase 1: Basic JWT (access tokens only, 24h expiry)
- Phase 2: Add refresh tokens (1 week expiry, stored in DB)

Why defer:
- Validate JWT flow works first
- Avoid premature complexity
- Need to design refresh token storage schema

Reminder for Phase 2:
- Refresh tokens in separate table (id, userId, token, expiresAt)
- Rotation on refresh (invalidate old, issue new)
- Endpoint: POST /api/auth/refresh
EOF
)"
```

**claude-mem** automatically captures:
- Refresh token discussion
- Decision to defer
- Phase 2 reminder

---

### End of Day 2

**Claude** auto-generates session summary:
```
Session Summary (Day 2):
- Installed jose library
- Implemented JwtService (generateToken, verifyToken)
- Decision: Defer refresh tokens to Phase 2
- Next: Update UserController to use JwtService
```

**Memory Stack Status**:

| Layer | Content | Tool |
|-------|---------|------|
| **Session capture** | Day 1-2 observations (134 total) | claude-mem |
| **Manual decisions** | 2 memories (auth_architecture, jwt_refresh_tokens) | Serena |
| **Code discovery** | 4 files indexed, call graph mapped | grepai |

---

## Day 3: Integration

### Morning: Session Resume

**Claude** (auto-injected context):
```
📋 Previous Sessions (Day 1-2):
- Day 1: Explored auth, decided JWT for API
- Day 2: Implemented JwtService, deferred refresh tokens to Phase 2
- Files modified: jwt.service.ts
- Next: Update UserController to use JwtService
```

**User**: "Update login endpoint to return JWT"

**Claude** (already knows the context):
```bash
# 1. FIND DEPENDENCIES (grepai)
grepai trace callers "login"
# → UserController.login() called by 47 routes

# 2. READ CURRENT IMPLEMENTATION (rg + Read)
rg "async login" src/controllers/user.controller.ts -A 10
```

**Current Implementation**:
```typescript
// src/controllers/user.controller.ts (before)
async login(req: Request, res: Response) {
  const { email, password } = req.body;
  const user = await this.authService.authenticate(email, password);

  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // OLD: Create session
  const sessionId = await this.authService.createSession(user.id);
  req.session.userId = user.id;

  return res.json({ success: true, sessionId });
}
```

**Update to JWT**:
```typescript
// src/controllers/user.controller.ts (after)
import { JwtService } from '../auth/jwt.service';

async login(req: Request, res: Response) {
  const { email, password } = req.body;
  const user = await this.authService.authenticate(email, password);

  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // NEW: Generate JWT
  const token = await this.jwtService.generateToken(user.id, user.email);

  return res.json({ success: true, token });
}
```

**claude-mem** automatically captures:
- UserController modification
- Removed: createSession call, session storage
- Added: JWT generation

---

### Afternoon: Middleware Update

**User**: "Create JWT authentication middleware"

**Implementation**:
```typescript
// src/middleware/jwt.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { JwtService } from '../auth/jwt.service';

export function jwtAuthMiddleware(jwtService: JwtService) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Missing or invalid token' });
    }

    const token = authHeader.slice(7); // Remove "Bearer "

    try {
      const payload = await jwtService.verifyToken(token);
      req.user = payload; // Attach user to request
      next();
    } catch (error) {
      return res.status(401).json({ error: 'Invalid or expired token' });
    }
  };
}
```

**Apply to API routes**:
```typescript
// src/app.ts
import { jwtAuthMiddleware } from './middleware/jwt.middleware';

// Apply JWT middleware to /api/* routes
app.use('/api/*', jwtAuthMiddleware(jwtService));

// Keep session middleware for /admin/* routes
app.use('/admin/*', sessionMiddleware);
```

**claude-mem** automatically captures:
- New middleware: jwt.middleware.ts
- Route split: /api/* (JWT) vs /admin/* (sessions)
- Backward compatibility maintained

---

### End of Day 3

**User**: "Record the migration status"

**Serena Memory Update**:
```bash
serena write_memory "jwt_migration_status" "$(cat <<'EOF'
JWT Migration Status (Day 3):

✅ Completed:
- JwtService implemented (jose library)
- UserController.login() updated to return JWT
- jwtAuthMiddleware created and applied to /api/* routes
- Admin routes still use sessions (/admin/*)

📝 Files Modified:
- src/auth/jwt.service.ts (new)
- src/middleware/jwt.middleware.ts (new)
- src/controllers/user.controller.ts (updated)
- src/app.ts (route split)

🧪 Next Steps (Day 4):
1. Write tests for JwtService
2. Test login flow end-to-end
3. Update API clients to use JWT (frontend, mobile)
4. Monitor logs for any session-related errors

⚠️ Rollback Plan:
- Keep session code intact (not deleted)
- Can revert by changing app.ts route config
- Database unchanged (no schema migration needed)
EOF
)"
```

**claude-mem dashboard** shows:
- 3 days of history
- 217 observations total
- 3 Serena memories (arch, refresh_tokens, migration_status)
- 8 files modified

---

## Day 4: Testing & Validation

### Morning: Session Resume

**Claude** (auto-injected context):
```
📋 Previous Sessions (Day 1-3):
- Day 1: Explored auth, decided JWT
- Day 2: Implemented JwtService
- Day 3: Updated login endpoint, created JWT middleware
- Status: /api/* uses JWT, /admin/* uses sessions
- Next: Write tests, validate end-to-end
```

**User**: "Write tests for JwtService"

**Claude** (knows implementation from Day 2):
```typescript
// src/auth/__tests__/jwt.service.test.ts
import { JwtService } from '../jwt.service';

describe('JwtService', () => {
  let jwtService: JwtService;

  beforeEach(() => {
    jwtService = new JwtService('test-secret-key-32-chars-long!!');
  });

  describe('generateToken', () => {
    it('should generate valid JWT token', async () => {
      const token = await jwtService.generateToken('user-123', 'test@example.com');

      expect(token).toBeDefined();
      expect(typeof token).toBe('string');
      expect(token.split('.')).toHaveLength(3); // JWT format: header.payload.signature
    });

    it('should include userId and email in payload', async () => {
      const token = await jwtService.generateToken('user-456', 'user@example.com');
      const payload = await jwtService.verifyToken(token);

      expect(payload.userId).toBe('user-456');
      expect(payload.email).toBe('user@example.com');
    });

    it('should set 24h expiration', async () => {
      const token = await jwtService.generateToken('user-789', 'exp@example.com');
      const payload = await jwtService.verifyToken(token);

      // JWT exp is in seconds, not milliseconds
      const now = Math.floor(Date.now() / 1000);
      const expectedExp = now + (24 * 60 * 60); // 24 hours

      expect(payload.exp).toBeGreaterThan(now);
      expect(payload.exp).toBeLessThanOrEqual(expectedExp + 10); // 10s tolerance
    });
  });

  describe('verifyToken', () => {
    it('should verify valid token', async () => {
      const token = await jwtService.generateToken('user-abc', 'valid@example.com');
      const payload = await jwtService.verifyToken(token);

      expect(payload).toEqual({
        userId: 'user-abc',
        email: 'valid@example.com',
        iat: expect.any(Number),
        exp: expect.any(Number)
      });
    });

    it('should throw on invalid token', async () => {
      await expect(jwtService.verifyToken('invalid.token.here'))
        .rejects.toThrow();
    });

    it('should throw on expired token', async () => {
      // Create token with -1h expiration (already expired)
      const jwtService2 = new JwtService('test-secret');
      const expiredToken = await jwtService2.generateToken('user-old', 'old@example.com');

      // Wait 2 seconds (simulate expiration)
      await new Promise(resolve => setTimeout(resolve, 2000));

      await expect(jwtService2.verifyToken(expiredToken))
        .rejects.toThrow('expired');
    });

    it('should throw on token with wrong secret', async () => {
      const token = await jwtService.generateToken('user-123', 'test@example.com');

      // Try to verify with different secret
      const jwtService2 = new JwtService('different-secret-key-here!!!!');
      await expect(jwtService2.verifyToken(token))
        .rejects.toThrow();
    });
  });
});
```

**Run Tests**:
```bash
npm test jwt.service.test.ts

# Output:
# JwtService
#   generateToken
#     ✓ should generate valid JWT token (45ms)
#     ✓ should include userId and email in payload (32ms)
#     ✓ should set 24h expiration (28ms)
#   verifyToken
#     ✓ should verify valid token (21ms)
#     ✓ should throw on invalid token (15ms)
#     ✓ should throw on expired token (2018ms)
#     ✓ should throw on token with wrong secret (19ms)
#
# Tests: 7 passed, 7 total
```

**claude-mem** automatically captures:
- Test file created (jwt.service.test.ts)
- 7 test cases (all passing)
- Edge cases tested (invalid, expired, wrong secret)

---

### Afternoon: End-to-End Test

**User**: "Test the full login flow"

**Manual E2E Test**:
```bash
# 1. Login (get JWT)
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Response:
# {
#   "success": true,
#   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJ1c2VyLTEyMyIsImVtYWlsIjoidGVzdEBleGFtcGxlLmNvbSIsImlhdCI6MTcwNzU4MjAwMCwiZXhwIjoxNzA3NjY4NDAwfQ.xYz..."
# }

# 2. Access protected API endpoint
curl -X GET http://localhost:3000/api/profile \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Response:
# {
#   "userId": "user-123",
#   "email": "test@example.com",
#   "profile": { ... }
# }

# 3. Test without token (should fail)
curl -X GET http://localhost:3000/api/profile

# Response:
# { "error": "Missing or invalid token" }

# 4. Test admin route (should still use sessions)
curl -X GET http://localhost:3000/admin/dashboard \
  -H "Cookie: connect.sid=s%3A..."

# Response:
# { "dashboard": "admin data" }
```

**✅ All tests pass!**

**Record Validation (Serena)**:
```bash
serena write_memory "jwt_validation_results" "$(cat <<'EOF'
JWT Validation Results (Day 4):

✅ Unit Tests: 7/7 passed
- Token generation works
- Token verification works
- Expiration handling correct
- Error cases handled (invalid, expired, wrong secret)

✅ E2E Tests: 4/4 passed
- Login returns JWT
- Protected routes accept JWT
- Unauthorized requests rejected
- Admin routes still use sessions (backward compatibility)

📊 Performance:
- Token generation: ~30ms
- Token verification: ~20ms
- No Redis dependency (stateless)

⚠️ Observations:
- Frontend needs update to store JWT (localStorage)
- Mobile app needs update to send Authorization header
- Consider token refresh after 24h (Phase 2)

✅ Ready for deployment
EOF
)"
```

---

### End of Day 4

**Memory Search Demo**:

```bash
# User searches session history
"Search my memory for JWT decisions"
```

**claude-mem returns**:
```
🔍 Found 3 relevant sessions:

Session 1 (Day 1):
- Decision: JWT for API, sessions for admin
- Library: jose (40% lighter)

Session 2 (Day 2):
- Implemented JwtService
- Deferred refresh tokens to Phase 2

Session 4 (Day 4):
- All tests passing (7/7 unit, 4/4 E2E)
- Ready for deployment
```

**Memory Stack Final Status**:

| Layer | Content | Tool |
|-------|---------|------|
| **Session capture** | 4 days, 312 observations | claude-mem |
| **Manual decisions** | 4 memories (arch, refresh, migration, validation) | Serena |
| **Code discovery** | 8 files modified, call graph updated | grepai |

---

## Day 5: Deployment

### Morning: Pre-Deployment Check

**User**: "What did we accomplish this week?"

**Claude** (query claude-mem):
```
"Show summary of JWT migration project"
```

**claude-mem comprehensive summary**:
```
📋 JWT Migration Project Summary (5 days):

Day 1: Discovery & Planning
- Explored auth system (4 key files)
- Decision: JWT for API, sessions for admin
- Library: jose (40% lighter, better TS)

Day 2: Implementation
- Installed jose
- Created JwtService (generateToken, verifyToken)
- Deferred refresh tokens to Phase 2

Day 3: Integration
- Updated UserController.login()
- Created jwtAuthMiddleware
- Applied to /api/*, kept sessions for /admin/*

Day 4: Testing
- Unit tests: 7/7 passed
- E2E tests: 4/4 passed
- Validation complete

📊 Impact:
- Files modified: 8
- Tool calls: 312
- Dependencies removed: express-session, connect-redis
- Dependencies added: jose
- Performance: Stateless (no Redis lookups)

✅ Ready for deployment
```

**Serena Memories Available**:
```bash
serena list_memories

# Output:
# 1. auth_architecture (Day 1)
# 2. jwt_refresh_tokens (Day 2)
# 3. jwt_migration_status (Day 3)
# 4. jwt_validation_results (Day 4)
```

---

### Afternoon: Deployment & Handoff

**User**: "Deploy to staging"

```bash
# Deploy to staging
git checkout -b feature/jwt-migration
git add .
git commit -m "feat: migrate API authentication to JWT

- Replace express-session with JWT (jose library)
- Apply JWT to /api/* routes
- Keep sessions for /admin/* routes
- Add comprehensive tests (7 unit, 4 E2E)
- All tests passing

Breaking changes: None (backward compatible)
Migration: None required (no DB changes)
Rollback: Change app.ts route config"

git push origin feature/jwt-migration

# Create PR
gh pr create --title "Migrate API to JWT authentication" \
  --body "$(serena read_memory jwt_migration_status)"
```

**Handoff Document** (auto-generated from memories):
```bash
# Generate handoff doc from Serena memories
serena read_memory auth_architecture > docs/jwt-migration.md
serena read_memory jwt_migration_status >> docs/jwt-migration.md
serena read_memory jwt_validation_results >> docs/jwt-migration.md
```

**Result**: Complete documentation of architectural decisions, implementation details, and validation results.

---

## 🎯 Key Takeaways

### Memory Stack in Action

**Without Memory Stack**:
- Re-read files every day (~200 files × 5 days = 1000 reads)
- Lose context between sessions
- Forget architectural decisions
- Manual documentation of decisions

**With Memory Stack (claude-mem + Serena + grepai)**:
- Auto-injected context every morning (0 re-reads)
- Preserved architectural decisions (4 Serena memories)
- Call graph maintained (grepai traces)
- Comprehensive session history (312 observations)
- **Result**: 5-day project completed with full context retention

---

### Token Efficiency

| Metric | Without | With Memory Stack | Savings |
|--------|---------|-------------------|---------|
| **File reads** | 1000 | 150 (85% reduction) | 850 reads |
| **Input tokens** | ~500k | ~75k (85% reduction) | 425k tokens |
| **Context loss** | Every session | Never | 100% retention |
| **Decision recall** | Manual notes | 4 Serena memories | Instant |

**Progressive Disclosure Impact**:
- Day 5 summary query: 3 layers (search → timeline → details)
- Without: Load all 312 observations (~50k tokens)
- With: Load summary → 5 sessions → 1 detail (~5k tokens)
- **Savings**: 90% tokens

---

### Practical Insights

**When to Use Each Tool**:

1. **claude-mem** (automatic):
   - Session start/end (auto)
   - "What did we do yesterday?"
   - "Show me the full project history"

2. **Serena** (manual, high-value):
   - Architectural decisions
   - Library choices
   - Migration status
   - Rollback plans

3. **grepai** (semantic discovery):
   - "Find authentication code"
   - "Who calls this function?"
   - "Show dependency graph"

4. **rg** (exact search):
   - "Find import statements"
   - "Show all TODOs"
   - "Grep for specific pattern"

---

### Cost Analysis

**5-Day Project**:

| Tool | Cost | Notes |
|------|------|-------|
| **claude-mem** | $4.68 | 312 observations × $0.15/100 |
| **Serena** | Free | Local storage |
| **grepai** | Free | Local Ollama |
| **Total** | **$4.68** | For 5 days of perfect memory |

**ROI**: 850 fewer file reads × ~500 tokens/read = 425k tokens saved = $4.25 (at $0.01/1k tokens)

**Net cost**: $0.43 for complete memory across 5 days

---

## 🔗 Resources

**Memory Stack Tools**:
- [claude-mem GitHub](https://github.com/thedotmack/claude-mem)
- [Serena GitHub](https://github.com/oraios/serena)
- [grepai GitHub](https://github.com/yoanbernabeu/grepai)

**Guide Sections**:
- Section 8.2.3: Serena (Symbol Memory)
- Section 8.2.4: grepai (Semantic Search)
- Section 8.2.5: claude-mem (Automatic Session Memory)
- Memory Tools Decision Matrix: guide/ultimate-guide.md:8630

---

**Workflow Created**: 2026-02-10
**Guide Version**: 3.24.0
**Author**: Florian BRUNIAUX + Claude (Anthropic)
