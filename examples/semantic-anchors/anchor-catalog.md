---
title: "Semantic Anchors Catalog"
description: "Curated vocabulary of precise technical terms that improve Claude Code output quality"
tags: [reference, semantic-anchors, architecture]
---

# Semantic Anchors Catalog

> **Concept**: Alexandre Soyer
> **Source**: [github.com/LLM-Coding/Semantic-Anchors](https://github.com/LLM-Coding/Semantic-Anchors) (Apache-2.0)
> **Adapted for**: Claude Code workflows

## What Are Semantic Anchors?

LLMs are statistical pattern matchers. When you use **precise technical vocabulary**, you help Claude access the right patterns from its training data. Generic terms produce generic code; specific terms produce specific, well-structured code.

**Analogy**: Technical terms are GPS coordinates into Claude's knowledge base.

---

## Testing & Quality Assurance

### Test Methodologies

| Vague | Semantic Anchor | What It Activates |
|-------|-----------------|-------------------|
| "write tests" | "TDD London School (mockist)" | Outside-in, mock collaborators, focus on behavior |
| "write tests" | "TDD Chicago School (classicist)" | Bottom-up, real collaborators, state verification |
| "test edge cases" | "Property-Based Testing (QuickCheck)" | Generative testing, shrinking, invariant discovery |
| "thorough testing" | "Mutation Testing (Stryker/PIT)" | Kill mutants, measure test effectiveness |
| "behavior tests" | "BDD Gherkin syntax (Given/When/Then)" | Cucumber-style, living documentation |

### Test Quality

| Vague | Semantic Anchor | Effect |
|-------|-----------------|--------|
| "good test names" | "Roy Osherove naming: MethodName_Scenario_ExpectedBehavior" | Consistent, descriptive names |
| "isolated tests" | "Test Pyramid (Fowler): 70% unit, 20% integration, 10% E2E" | Proper test distribution |
| "fast tests" | "Sociable unit tests with test doubles at boundaries" | Speed with realistic behavior |
| "readable tests" | "Arrange-Act-Assert (AAA) pattern" | Clear test structure |
| "maintainable tests" | "Object Mother / Test Data Builder pattern" | Reusable test fixtures |

---

## Architecture & Design

### Architectural Patterns

| Vague | Semantic Anchor | When to Use |
|-------|-----------------|-------------|
| "clean architecture" | "Hexagonal Architecture (Ports & Adapters)" | Domain isolation, testability |
| "layered architecture" | "Onion Architecture (Palermo)" | Dependency toward center |
| "microservices" | "Domain-Driven Design bounded contexts" | Service boundaries |
| "event-driven" | "CQRS with Event Sourcing" | Read/write separation, audit trail |
| "scalable" | "Event-Driven Architecture with message broker" | Async processing, decoupling |

### Domain-Driven Design (Evans)

| Vague | Semantic Anchor | Purpose |
|-------|-----------------|---------|
| "business logic" | "DDD Aggregate pattern" | Transactional consistency |
| "data access" | "DDD Repository pattern" | Persistence abstraction |
| "object mapping" | "DDD Value Objects" | Immutable, equality by value |
| "complex objects" | "DDD Entity pattern" | Identity-based equality |
| "business rules" | "DDD Domain Services" | Stateless operations |
| "integration" | "DDD Anti-Corruption Layer (ACL)" | External system isolation |

### SOLID Principles

| Vague | Semantic Anchor | Specific Guidance |
|-------|-----------------|-------------------|
| "single purpose" | "SRP: one reason to change (Robert C. Martin)" | Cohesion focus |
| "extensible" | "OCP: open for extension, closed for modification" | Plugin architecture |
| "substitutable" | "LSP: subtypes must be substitutable" | Contract preservation |
| "minimal interfaces" | "ISP: clients shouldn't depend on unused methods" | Interface segregation |
| "decoupled" | "DIP: depend on abstractions, not concretions" | Inversion of control |

---

## Code Quality & Refactoring

### Refactoring Catalog (Fowler)

| Vague | Semantic Anchor | Trigger |
|-------|-----------------|---------|
| "extract logic" | "Extract Method refactoring" | Long methods |
| "remove conditionals" | "Replace Conditional with Polymorphism" | Complex if/switch |
| "simplify creation" | "Replace Constructor with Factory Method" | Complex instantiation |
| "remove duplication" | "Extract Class / Extract Superclass" | Similar classes |
| "improve naming" | "Rename Method/Variable (intention-revealing names)" | Unclear names |

### Code Smells (Fowler/Beck)

| Smell | Semantic Anchor | Solution |
|-------|-----------------|----------|
| "long method" | "Extract Method until comments become unnecessary" | Methods < 10 lines |
| "large class" | "Extract Class following SRP" | Single responsibility |
| "feature envy" | "Move Method to class that owns data" | Better cohesion |
| "primitive obsession" | "Replace Primitive with Value Object" | Type safety |
| "shotgun surgery" | "Move Field/Method to consolidate changes" | Centralize logic |

### Clean Code (Martin)

| Vague | Semantic Anchor | Application |
|-------|-----------------|-------------|
| "readable" | "Screaming Architecture: package structure reveals intent" | Folder naming |
| "clear names" | "Intention-revealing names (Clean Code Ch. 2)" | Self-documenting |
| "no comments" | "Code should be self-explanatory (comments lie)" | Refactor instead |
| "small functions" | "Functions should do one thing (max 20 lines)" | Single responsibility |
| "no side effects" | "Command-Query Separation (CQS)" | Predictable behavior |

---

## Error Handling

### Functional Patterns

| Vague | Semantic Anchor | Benefits |
|-------|-----------------|----------|
| "error handling" | "Railway Oriented Programming with Either<L,R>" | Composable errors |
| "null safety" | "Option/Maybe monad (never return null)" | Explicit absence |
| "error accumulation" | "Validation applicative functor" | Collect all errors |
| "async errors" | "Task/Future monad with error channel" | Async error flow |

### Exception Strategies

| Vague | Semantic Anchor | Use Case |
|-------|-----------------|----------|
| "handle errors" | "Checked exceptions at boundaries only" | External integration |
| "error recovery" | "Circuit Breaker pattern (Nygard)" | Fault tolerance |
| "graceful degradation" | "Bulkhead pattern" | Isolation |
| "retry logic" | "Exponential backoff with jitter" | Resilience |

---

## API Design

### REST Maturity

| Vague | Semantic Anchor | Level |
|-------|-----------------|-------|
| "REST API" | "REST Level 0: HTTP as tunnel" | Basic |
| "proper REST" | "REST Level 2: HTTP verbs + status codes" | Standard |
| "HATEOAS" | "REST Level 3: Hypermedia controls" | Full REST |
| "API versioning" | "URL path versioning (/v1/) or header versioning" | Evolution |

### API Quality

| Vague | Semantic Anchor | Application |
|-------|-----------------|-------------|
| "consistent API" | "JSON:API specification" | Response format |
| "documented API" | "OpenAPI 3.0 (Swagger)" | Spec-first design |
| "secure API" | "OAuth 2.0 + PKCE flow" | Authentication |
| "rate limiting" | "Token bucket algorithm" | Traffic control |

---

## Documentation

### Architecture Documentation

| Vague | Semantic Anchor | Output |
|-------|-----------------|--------|
| "document architecture" | "C4 Model (Context, Container, Component, Code)" | Diagrams |
| "architecture docs" | "arc42 template structure" | Comprehensive docs |
| "design decisions" | "ADR (Architecture Decision Records) - Nygard format" | Decision log |
| "system overview" | "4+1 View Model (Kruchten)" | Multiple perspectives |

### Code Documentation

| Vague | Semantic Anchor | Format |
|-------|-----------------|--------|
| "API docs" | "JSDoc / TSDoc with @example tags" | Generated docs |
| "README" | "README-driven development (Tom Preston-Werner)" | Project intro |
| "changelog" | "Keep a Changelog format (semver)" | Release notes |
| "contributing" | "CONTRIBUTING.md with PR template" | Contributor guide |

---

## Requirements & Specifications

### Requirements Syntax

| Vague | Semantic Anchor | Format |
|-------|-----------------|--------|
| "requirements" | "EARS syntax (Easy Approach to Requirements)" | Structured requirements |
| "user stories" | "Connextra format: As a [role] I want [goal] so that [benefit]" | User perspective |
| "acceptance criteria" | "BDD Gherkin: Given/When/Then" | Testable criteria |
| "use cases" | "Cockburn's use case template (brief/casual/fully dressed)" | Interaction flows |

### Discovery & Mapping

| Vague | Semantic Anchor | Technique |
|-------|-----------------|-----------|
| "understand users" | "User Story Mapping (Jeff Patton)" | Journey visualization |
| "prioritize features" | "MoSCoW method (Must/Should/Could/Won't)" | Priority triage |
| "user needs" | "Jobs-to-be-Done framework (Christensen)" | Outcome focus |
| "event modeling" | "Event Storming (Brandolini)" | Domain discovery |

---

## Security

### OWASP & Common Vulnerabilities

| Vague | Semantic Anchor | Protection |
|-------|-----------------|------------|
| "secure code" | "OWASP Top 10 mitigations" | Comprehensive checklist |
| "input validation" | "Allowlist validation + parameterized queries" | Injection prevention |
| "authentication" | "OWASP ASVS Level 2 requirements" | Auth standards |
| "secrets management" | "HashiCorp Vault or cloud KMS" | Secret storage |

### Security Patterns

| Vague | Semantic Anchor | Implementation |
|-------|-----------------|----------------|
| "secure by default" | "Principle of least privilege" | Minimal permissions |
| "defense in depth" | "Multiple security layers (network, app, data)" | Layered security |
| "secure communication" | "TLS 1.3 with certificate pinning" | Transport security |
| "audit logging" | "Immutable audit trail with tamper detection" | Compliance |

---

## Performance

### Optimization Patterns

| Vague | Semantic Anchor | Application |
|-------|-----------------|-------------|
| "caching" | "Cache-aside pattern with TTL" | Read performance |
| "batch processing" | "Bulk operations with chunking" | Write performance |
| "lazy loading" | "Virtual proxy pattern" | Resource optimization |
| "memoization" | "Function memoization with LRU eviction" | Computation caching |

### Scalability

| Vague | Semantic Anchor | Technique |
|-------|-----------------|-----------|
| "horizontal scaling" | "Stateless services + external state store" | Scale-out |
| "database scaling" | "Read replicas + write-through caching" | DB performance |
| "async processing" | "Message queue with competing consumers" | Throughput |
| "load balancing" | "Round-robin with health checks" | Distribution |

---

## Prompting Patterns

### Anti-Anchoring Techniques

LLMs can fixate on their first suggestion, narrowing your solution space. These patterns combat anchoring bias:

| Pattern | Prompt Template | Effect |
|---------|-----------------|--------|
| Fresh start | "Ignore any prior ideas. Generate 4 novel approaches to [X]" | Forces diversity |
| Reflection loop | "Generate 3 options, then critique each, then recommend" | Self-correction |
| Quantified comparison | "Rank by [metric1], [metric2], [metric3] with scores 1-10" | Objective trade-offs |
| Devil's advocate | "What are the strongest arguments against your recommendation?" | Surface hidden costs |
| Constraint flip | "Now solve with [opposite constraint]" | Expand solution space |

### Exploration Prompts

Use these when you need multiple approaches before committing:

| Goal | Semantic Anchor Prompt |
|------|------------------------|
| Architecture choice | "Compare [A], [B], [C] using C4 model criteria: context fit, container complexity, component count" |
| Performance trade-off | "Analyze time complexity (Big O), space complexity, and cache-friendliness for each approach" |
| Team fit | "Evaluate learning curve, debugging difficulty, and ecosystem maturity (1-10 scale)" |
| Risk assessment | "For each option: what's the worst-case failure mode and recovery cost?" |

### Iteration Prompts

For progressive refinement of scripts and automation:

| Stage | Prompt Pattern |
|-------|----------------|
| Initial | "Create a [language] script that [goal]. Include basic error handling." |
| Constrain | "Add: [specific constraint]. Remove: [unwanted behavior]." |
| Harden | "Add input validation, logging, and handle edge case: [specific case]." |
| Optimize | "Optimize for [metric]. Target: [specific threshold]." |
| Document | "Add usage examples and inline comments for non-obvious logic." |

---

## CLAUDE.md Template with Semantic Anchors

```markdown
# Project Architecture

## Principles (Semantic Anchors)

### Architecture
- **Pattern**: Hexagonal Architecture (Ports & Adapters)
- **Domain modeling**: Domain-Driven Design tactical patterns (Aggregates, Value Objects, Domain Events)
- **Documentation**: ADR (Architecture Decision Records) for significant decisions

### Code Quality
- **Design**: SOLID principles, especially SRP and DIP
- **Refactoring**: Apply Fowler's catalog - Extract Method, Replace Conditional with Polymorphism
- **Naming**: Intention-revealing names, Screaming Architecture for packages

### Testing
- **Methodology**: TDD London School - outside-in, mock collaborators
- **Structure**: Arrange-Act-Assert (AAA) pattern
- **Coverage**: Test Pyramid - 70% unit, 20% integration, 10% E2E

### Error Handling
- **Pattern**: Railway Oriented Programming with Result<T, E>
- **Never**: Return null, throw for control flow
- **Always**: Use Option/Maybe for optional values

### API Design
- **Style**: REST Level 2 with proper HTTP verbs and status codes
- **Documentation**: OpenAPI 3.0 spec-first
- **Security**: OAuth 2.0 + PKCE for authentication

### Requirements
- **Format**: EARS syntax for formal requirements
- **User stories**: Connextra format with acceptance criteria
- **Discovery**: Event Storming for domain exploration
```

---

## Quick Reference

### Before/After Examples

| Before (Vague) | After (Anchored) |
|----------------|------------------|
| "Make it clean" | "Apply SRP: each class has one reason to change" |
| "Add error handling" | "Use Railway Oriented Programming with Either monad" |
| "Write good tests" | "Follow TDD London School with mock collaborators" |
| "Document the API" | "Generate OpenAPI 3.0 spec from annotations" |
| "Make it secure" | "Mitigate OWASP Top 10, specifically A03:Injection" |
| "Refactor this" | "Apply Extract Method until comments are unnecessary" |
| "Scale this service" | "Implement CQRS with Event Sourcing for read/write separation" |

---

## Usage Tips

1. **Combine anchors**: "Apply Hexagonal Architecture with DDD tactical patterns and Railway Oriented error handling"

2. **Specify versions/authors**: "Following Kent Beck's TDD (2003)" is more specific than "TDD"

3. **Reference books**: "Clean Code Chapter 2 naming conventions" activates specific knowledge

4. **Name patterns explicitly**: "Strategy pattern" > "pluggable behavior"

5. **Use with XML tags**: Combine anchors with `<constraints>` and `<quality_criteria>` tags for maximum effect

---

> **Remember**: The goal is precision, not jargon. Use anchors that Claude has seen extensively in its training data. When in doubt, reference the authoritative source (book, paper, framework).
