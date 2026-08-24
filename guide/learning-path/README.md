# Claude Code Learning Path

**Master Claude Code in 8-11 hours. Go deep on what matters to you with optional deep dives.**

This is your structured entry point. Follow the modules in order, then jump into the full guide for depth.

---

## The 7-Module Path

| Module | Time | Focus | Complexity |
|--------|------|-------|------------|
| **[01-Installation & Setup](01-installation.md)** | 15 min | Get Claude Code running | ⭐ Beginner |
| **[02-Core Loop](02-core-loop.md)** | 45 min | How Claude Code actually works | ⭐ Beginner |
| **[03-Memory & Config](03-memory.md)** | 1 hour | CLAUDE.md and settings | ⭐⭐ Intermediate |
| **[04-Agents & Specialization](04-agents.md)** | 1.5 hours | Creating focused agents | ⭐⭐ Intermediate |
| **[05-Skills & Automation](05-skills.md)** | 1.5 hours | Reusable capabilities | ⭐⭐ Intermediate |
| **[06-Hooks & Events](06-hooks.md)** | 1 hour | Triggering automation | ⭐⭐ Intermediate |
| **[07-Advanced Patterns](07-advanced.md)** | 2-3 hours | Multi-agent orchestration | ⭐⭐⭐ Advanced |

**Total: 8-11 hours base learning** + optional deep dives.

---

## How to Use This Path

### Step 1: Assess Your Level

**Beginner** (day 1 of Claude Code):
- Take the quick path: 01 → 02 → 03 (2 hours)
- Then jump to full guide `Part 1: Quick Start`

**Intermediate** (using Claude Code 1-4 weeks):
- Take the full path: 01 → 07 (8-11 hours)
- Focus on modules 04, 05, 06, 07 for depth

**Advanced** (using Claude Code 1+ months):
- Skim 01-03, deep-dive 04-07
- Jump to guide Part 9: Advanced Patterns for orchestration

### Step 2: Choose Your Track

**Track A: Master the Fundamentals** (11 hours)
- Follow modules 01-07 in order
- Complete all exercises
- Take `/lesson-quiz [topic]` after each module
- Finish with `/self-assessment comprehensive`

**Track B: Skill-Focused Deep Dive** (4-6 hours)
- Module 01-02 (basics)
- Skip to Module 04, 05, or 06 based on your goal
- Go deep on that one module
- Link to advanced patterns as needed

**Track C: Team Adoption** (5-7 hours)
- Module 01-02 (teach fundamentals)
- Module 03 (team configuration)
- Modules 04-07 (team workflows)
- Run `/self-assessment` across team, identify gaps
- Create follow-up training plan from gaps

### Step 3: Learn & Validate

Each module includes:
- 📖 **Reading** (10-30 min): Concepts and mental models
- 🔨 **Hands-on practice** (20-45 min): Real examples from `examples/`
- 📝 **Validation**: `/lesson-quiz [topic]` to verify understanding

### Step 4: Go Deeper

After this path, you have options:

**Option A: Deep Reference**
→ Jump to relevant section in `guide/ultimate-guide.md`

**Option B: Master a Domain**
→ Read dedicated guides (e.g., `guide/security/`, `guide/ops/`)

**Option C: Build with Plugins**
→ Install a plugin bundle from `examples/plugins/`

**Option D: Self-Assess**
→ Run `/self-assessment comprehensive` to identify remaining gaps

---

## Module Details

### Module 01: Installation & Setup (15 min)
**Goal:** Get Claude Code running and confirm it works

- Install for your platform (macOS/Linux/Windows)
- Run your first command
- Understand the prompt → output loop
- **Exercise:** Complete the "First 5 Minutes" workflow

**Complexity:** ⭐ (Beginner)
**Read:** [01-installation.md](01-installation.md)
**Then:** Part 1: Quick Start in main guide

---

### Module 02: Core Loop (45 min)
**Goal:** Understand how Claude Code works at the system level

- The interaction loop (prompt → tool → decision → feedback)
- Context and sessions
- Plans and thinking modes
- **Exercise:** Use `/plan` to plan a real task, observe the flow

**Complexity:** ⭐ (Beginner)
**Read:** [02-core-loop.md](02-core-loop.md)
**Then:** Part 2: Core Concepts in main guide

---

### Module 03: Memory & Config (1 hour)
**Goal:** Configure Claude Code for your workflow

- CLAUDE.md structure and hierarchy
- Settings precedence (global → project → session)
- Environment variables
- **Exercise:** Create your first CLAUDE.md, customize settings

**Complexity:** ⭐⭐ (Intermediate)
**Read:** [03-memory.md](03-memory.md)
**Then:** Part 3: Memory & Settings in main guide

---

### Module 04: Agents & Specialization (1.5 hours)
**Goal:** Create focused agents for specific tasks

- When to use agents vs a single session
- Tool restriction and isolation
- Creating agents (AGENT.md format)
- **Exercise:** Build 2 agents (generalist + specialist), test them

**Complexity:** ⭐⭐ (Intermediate)
**Read:** [04-agents.md](04-agents.md)
**Then:** Part 4: Agents in main guide

---

### Module 05: Skills & Automation (1.5 hours)
**Goal:** Build reusable capabilities that trigger automatically

- Skill lifecycle and frontmatter
- Auto-invocation patterns
- Bundling scripts with skills
- **Exercise:** Create a skill that solves a repeated problem

**Complexity:** ⭐⭐ (Intermediate)
**Read:** [05-skills.md](05-skills.md)
**Then:** Part 5: Skills in main guide

---

### Module 06: Hooks & Events (1 hour)
**Goal:** Automate responses to system events

- Hook events and matching
- Pre-validation vs post-execution
- Writing safe hooks
- **Exercise:** Add 2 hooks (one pre, one post) to your config

**Complexity:** ⭐⭐ (Intermediate)
**Read:** [06-hooks.md](06-hooks.md)
**Then:** Part 7: Hooks in main guide

---

### Module 07: Advanced Patterns (2-3 hours)
**Goal:** Orchestrate multi-agent workflows

- Multi-agent teams and dependencies
- Orchestration patterns
- Error handling and recovery
- **Exercise:** Design a 3-agent workflow for a realistic scenario

**Complexity:** ⭐⭐⭐ (Advanced)
**Read:** [07-advanced.md](07-advanced.md)
**Then:** Part 9: Advanced Patterns in main guide

---

## After the Learning Path

### Assessment
Take `/self-assessment comprehensive` to:
- Measure where you stand
- Identify knowledge gaps
- Get a personalized next-step plan

### Specialization
Choose where to go next:

| Interest | Path |
|----------|------|
| **Security & Production** | → `guide/security/` (43KB) |
| **DevOps & Operations** | → `guide/ops/` (113KB) |
| **Architecture & Design** | → `guide/core/architecture.md` (77KB) |
| **Building with AI** | → `guide/roles/learning-with-ai.md` (53KB) |
| **Teams & Adoption** | → `guide/roles/adoption-approaches.md` (15KB) |

### Practice
Try one of the practice projects from `/self-assessment` results:
- Project 1: Your first automation workflow
- Project 2: Team configuration
- Project 3: Production-grade setup

---

## Time Estimates

**For different goals:**

- **Just getting started:** 2 hours (Modules 01-02 only)
- **Daily usage:** 6 hours (Modules 01-05)
- **Team adoption:** 8-11 hours (Modules 01-07)
- **Deep mastery:** 15-20 hours (Path + guide deep-dives)
- **Specialization:** 20-30+ hours (Path + domain expertise)

---

## What You'll Be Able to Do

After this learning path, you'll:

✓ Navigate Claude Code without the docs
✓ Create custom agents and skills for your workflow
✓ Configure team-level settings and governance
✓ Build multi-agent orchestration
✓ Automate repetitive tasks with hooks
✓ Know where to go for deeper expertise

---

## Common Questions

**Q: Can I skip modules?**
A: Yes, but 01-03 are prerequisites. If you know basics, start at 04.

**Q: How long does it really take?**
A: 8-11 hours for the full path. Budget extra time for exercises.

**Q: Do I need prior Claude Code experience?**
A: No, start at Module 01. If you've used it before, skim 01-02.

**Q: After this, what's the full guide?**
A: `guide/ultimate-guide.md` (25K lines) is your reference. This path gets you to the point where you can read it effectively.

---

## Ready? Start Here

**First time:** → [Module 01: Installation](01-installation.md)
**Already using Claude Code:** → Assess your level, jump to relevant module
**Team adoption:** → [Module 03: Memory & Config](03-memory.md)

---

**Or take the quick assessment:** `/self-assessment quick` (5 minutes)
