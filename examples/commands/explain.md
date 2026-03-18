---
name: explain
description: "Explain code, concepts, or system behavior with adjustable depth levels"
---

# Code Explainer

Explain code, concepts, or system behavior with adjustable depth levels.

## Purpose

Get clear explanations of:
- How specific code works
- Why certain patterns are used
- What a system/module does
- Architectural decisions and trade-offs

## Instructions

### Step 1: Determine Scope

Identify what needs explanation:
- **File**: Entire file structure and purpose
- **Function/Method**: Specific implementation details
- **Concept**: Architectural pattern or design decision
- **Flow**: How data/control moves through the system

### Step 2: Assess Complexity

```
Simple (1-2 min read)     → Quick summary, key points only
Standard (3-5 min read)   → Purpose, how it works, key decisions
Deep (10+ min read)       → Full breakdown, alternatives, trade-offs
```

### Step 3: Gather Context

```bash
# For file explanations
head -50 "$FILE"  # See imports and structure

# For function explanations
grep -A 30 "function $NAME\|def $NAME\|fn $NAME" "$FILE"

# For module explanations
ls -la "$DIR"
cat "$DIR/index.ts" 2>/dev/null || cat "$DIR/__init__.py" 2>/dev/null
```

### Step 4: Structure the Explanation

## Output Format

---

### 📖 Explanation: [Target]

**Scope**: [file/function/concept/flow]
**Depth**: [simple/standard/deep]

### What It Does

[1-3 sentences describing the purpose]

### How It Works

[Step-by-step breakdown appropriate to depth level]

### Key Decisions

| Decision | Why | Alternative |
|----------|-----|-------------|
| [choice made] | [reasoning] | [what else could work] |

### Example Usage

```typescript
// How to use this correctly
```

### Related Code

- `path/to/related.ts` - [relationship]
- `path/to/dependency.ts` - [relationship]

### 💡 Learning Notes (if --learn flag)

[Additional context for understanding the broader pattern]

---

## Depth Levels

### Simple (`/explain --simple`)

```markdown
**validateUser()** checks if the user object has required fields
(email, password) and returns a boolean. Uses regex for email format.
```

### Standard (`/explain` - default)

```markdown
**validateUser(user: User): ValidationResult**

**Purpose**: Validates user input before database operations.

**Flow**:
1. Check required fields exist (email, password)
2. Validate email format with regex
3. Check password meets requirements (8+ chars, special char)
4. Return { valid: boolean, errors: string[] }

**Used by**: signup(), updateProfile()
```

### Deep (`/explain --deep`)

```markdown
[All of standard, plus:]

**Design Decisions**:
- Returns ValidationResult instead of throwing to allow batch validation
- Regex chosen over library for zero dependencies
- Password rules configurable via config.ts

**Trade-offs**:
- Pro: Fast, no dependencies
- Con: Regex email validation isn't RFC-compliant

**Alternatives Considered**:
- Zod schema: More powerful but adds 50KB
- Class-validator: Better for decorators but OOP-heavy
```

## Usage Examples

**Explain a file:**
```
/explain src/auth/middleware.ts
```

**Explain a function:**
```
/explain the handleWebhook function in payments.ts
```

**Explain a concept:**
```
/explain how our event sourcing works
```

**Explain with specific depth:**
```
/explain --deep the authentication flow
/explain --simple what useCallback does
```

**Explain for learning:**
```
/explain --learn the repository pattern used here
```

## Tips

1. **Be specific**: "Explain line 45-60" > "Explain this file"
2. **State your level**: "I'm new to TypeScript" helps calibrate
3. **Ask follow-ups**: "Why not use X instead?" deepens understanding
4. **Request analogies**: "Explain like I'm familiar with Python but not TS"

$ARGUMENTS
