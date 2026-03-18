---
description: "Architecture review criteria for plan and code reviews"
---

# Architecture Review Criteria

When reviewing architecture (plans or code), evaluate these dimensions:

## System Design
- Are component boundaries clear and well-defined?
- Does each component have a single, well-understood responsibility?
- Are interfaces between components minimal and well-documented?

## Dependencies
- Is the dependency graph acyclic and manageable?
- Are there circular dependencies that need breaking?
- Are external dependencies justified and up-to-date?

## Data Flow
- Is data ownership clear (which component is source of truth)?
- Are there potential bottlenecks in the data pipeline?
- Is data transformation happening at the right layer?

## Scaling
- What are the single points of failure?
- Where will the system break under 10x load?
- Are stateless and stateful components properly separated?

## Security
- Are authentication and authorization properly layered?
- Is data access controlled at the right boundaries?
- Are API boundaries validated (input sanitization, rate limiting)?
- Are secrets properly managed (no hardcoded values)?
