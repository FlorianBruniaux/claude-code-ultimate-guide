---
name: self-assessment
version: 1.0.0
description: Interactive skill assessment with personalized learning path generation
trigger: /self-assessment
invocation: manual

profiles:
  - name: junior
    label: "Beginner"
    min_score: 0
    max_score: 6
  - name: intermediate
    label: "Intermediate"
    min_score: 7
    max_score: 13
  - name: advanced
    label: "Advanced"
    min_score: 14
    max_score: 20

topics:
  - id: 01
    name: "Quick Start"
    guide_section: "guide/ultimate-guide.md#1-quick-start-day-1"
    importance: "critical"
    depends_on: []
    
  - id: 02
    name: "Core Concepts"
    guide_section: "guide/ultimate-guide.md#2-core-concepts"
    importance: "critical"
    depends_on: [01]
    
  - id: 03
    name: "Memory & Settings"
    guide_section: "guide/ultimate-guide.md#3-memory--settings"
    importance: "high"
    depends_on: [02]
    
  - id: 04
    name: "Agents"
    guide_section: "guide/ultimate-guide.md#4-agents"
    importance: "high"
    depends_on: [02, 03]
    
  - id: 05
    name: "Skills"
    guide_section: "guide/ultimate-guide.md#5-skills"
    importance: "high"
    depends_on: [02, 03]
    
  - id: 06
    name: "Commands"
    guide_section: "guide/ultimate-guide.md#6-commands-user-invocable-skills"
    importance: "medium"
    depends_on: [02]
    
  - id: 07
    name: "Hooks"
    guide_section: "guide/ultimate-guide.md#7-hooks"
    importance: "medium"
    depends_on: [02, 03]
    
  - id: 08
    name: "MCP Servers"
    guide_section: "guide/ultimate-guide.md#8-mcp-servers"
    importance: "medium"
    depends_on: [02]
    
  - id: 09
    name: "Advanced Patterns"
    guide_section: "guide/ultimate-guide.md#9-advanced-patterns"
    importance: "low"
    depends_on: [04, 05, 06, 07, 08]
    
  - id: 10
    name: "Security & Production"
    guide_section: "guide/security/"
    importance: "critical"
    depends_on: [02, 03]

modes:
  - id: quick
    name: "Quick Assessment"
    duration: "5 minutes"
    questions_per_topic: 1
    total_questions: 10
    description: "Rapid assessment across core topics. Get a skill level + identify 2-3 immediate gaps."
    
  - id: comprehensive
    name: "Comprehensive Assessment"
    duration: "20 minutes"
    questions_per_topic: 2
    total_questions: 20
    description: "Deep dive into each topic. Get per-topic scores + detailed learning path + practice projects."
---

# Codex Self-Assessment

**Master your Codex skills with a personalized learning journey.**

This interactive assessment identifies your current expertise level and generates a custom learning path tailored to your gaps and goals.

---

## How It Works

### Step 1: Choose Your Mode

**Quick Mode** (5 min)
- 10 questions across 10 topics
- Best for: Quick skill check, understanding your general level
- Output: Overall profile (Beginner/Intermediate/Advanced) + top 2-3 gaps

**Comprehensive Mode** (20 min)
- 20 questions (2 per topic)
- Best for: Detailed mastery assessment, planning team training
- Output: Per-topic scores + detailed learning path + 3 practice projects

### Step 2: Answer Questions

Questions cover:
- Practical usage (how to do things)
- Decision-making (when to use what)
- Architecture patterns (why things work)
- Production best practices (security, performance, scaling)

Each question has:
- 4 options (A-D)
- Immediate feedback on correct answer
- Link to relevant guide section

### Step 3: Get Your Profile

**Quick Mode Output:**
```
╔═══════════════════════════════════════════════╗
║ Your Profile: Intermediate Developer          ║
╠═══════════════════════════════════════════════╣
║ Overall Score: 14/20                          ║
║ Level: Intermediate (strong)                  ║
╠═══════════════════════════════════════════════╣
║ Immediate Gaps:                               ║
║  • MCP Servers (5/5 topics weak)              ║
║  • Advanced Patterns (4/5 weak)               ║
║  • Hooks (3/5 partially weak)                 ║
║                                               ║
║ → Recommended learning time: 4-6 hours        ║
╚═══════════════════════════════════════════════╝
```

**Comprehensive Mode Output:**
```
╔═══════════════════════════════════════════════════════════════╗
║ Detailed Mastery Profile                                      ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║ 01 Quick Start          ████░░░░░░  8/10  Proficient         ║
║ 02 Core Concepts        ██████░░░░  6/10  Proficient         ║
║ 03 Memory & Settings    ██████░░░░  6/10  Proficient         ║
║ 04 Agents              ████░░░░░░  4/10  Basic               ║
║ 05 Skills              ████░░░░░░  4/10  Basic               ║
║ 06 Commands            ██████░░░░  6/10  Proficient          ║
║ 07 Hooks               ██░░░░░░░░  2/10  None                ║
║ 08 MCP Servers         ██░░░░░░░░  2/10  None                ║
║ 09 Advanced Patterns   ░░░░░░░░░░  0/10  None                ║
║ 10 Security            ███░░░░░░░  3/10  Basic               ║
║                                                               ║
║ OVERALL: Intermediate (14/100 points)                         ║
╚═══════════════════════════════════════════════════════════════╝
```

### Step 4: Get Your Learning Path

Based on your scores, you get:

**Prioritized learning sequence** (respects dependencies):
1. Topics ordered by weakness + importance
2. Prerequisites shown (you can't skip foundations)
3. Time estimates for each topic (sums only what you need)
4. Templates and examples linked to each topic

**Example path for Intermediate developer:**
```
Phase 1: Hooks Fundamentals (2 hours)
  → Read: guide/ultimate-guide.md#7-hooks
  → Try: examples/hooks/event-driven-formatting.sh
  → Quiz: /lesson-quiz 07-hooks

Phase 2: MCP Integration (3 hours)
  → Read: guide/ultimate-guide.md#8-mcp-servers
  → Try: examples/mcp-configs/github-integration.json
  → Quiz: /lesson-quiz 08-mcp-servers

Phase 3: Advanced Patterns (4 hours)
  → Read: guide/ultimate-guide.md#9-advanced-patterns
  → Practice: 3 real-world projects (see below)
  → Quiz: /lesson-quiz 09-advanced-patterns
```

**3 Practice Projects**
Based on your profile, you get targeted exercises:
- Project 1: Combine 2-3 topics you're weak in
- Project 2: Real-world workflow integration
- Project 3: Team/production scenario

---

## Getting Started

### Quick Assessment
```
/self-assessment quick
```

### Full Assessment
```
/self-assessment comprehensive
```

### Options
```
/self-assessment quick --verbose      # Show explanations
/self-assessment comprehensive --save  # Save results to file
```

---

## What You Learn

This assessment is designed to identify:

### Fundamental Gaps
- Core interaction loops you haven't tried
- Essential features you've overlooked
- Mental model misconceptions

### Decision-Making Blind Spots
- When to use agents vs skills vs commands
- Which hook event to use for which problem
- MCP server selection for your needs

### Production Readiness
- Security best practices
- Performance optimization patterns
- Scaling multi-agent systems
- Team configuration and governance

---

## After Your Assessment

### Immediate Actions
1. **See your profile** — Understand your current mastery level
2. **Identify gaps** — Know exactly what to learn next
3. **Get a learning path** — Personalized, dependency-aware sequence
4. **Practice** — 3 targeted projects matching your level

### Recommended Follow-up Skills
- `/lesson-quiz [topic]` — Quiz yourself on specific topics
- `/audit-agents-skills` — Audit your own config quality
- `/Codex-md` — Manage your AGENTS.md configuration

### Integration with Learning Path

After assessment, the `/lesson-quiz` skill provides per-module verification:
- Answer 5 questions per module
- Get instant feedback on weak areas
- Unlock next module when ready

---

## Scoring & Profiles

### Junior Developer (0-6 points)
- Just installed Codex
- Know basic commands and workflows
- Haven't touched memory/agents/hooks yet
- **Next step:** Core Concepts + Memory module

### Intermediate Developer (7-13 points)
- Using Codex daily
- Comfortable with AGENTS.md and basic agents
- Exploring skills and commands
- Some hook usage, no MCP servers
- **Next step:** Deep MCP + Advanced Patterns

### Advanced Developer (14-20 points)
- Master multi-agent orchestration
- Production-grade security and scaling
- Custom skills and complex hooks
- MCP server expertise
- **Next step:** Team training, enterprise patterns

---

## Tips for Better Results

1. **Answer honestly** — Don't guess, skip unknown questions
2. **Review explanations** — Each question has a guide link
3. **Revisit before level-up** — Retake assessment after learning new topics
4. **Share results** — Use your profile to coordinate with your team

---

## Need Help?

- **Questions about the assessment?** → Check `/help self-assessment`
- **Want to discuss results?** → See `guide/roles/learning-with-ai.md`
- **Found an error?** → Report it on GitHub Issues

---

**Ready to master Codex?** Start with `/self-assessment quick` now.
