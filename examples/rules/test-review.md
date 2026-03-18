---
description: "Test review criteria for plan and code reviews"
---

# Test Review Criteria

When reviewing tests, evaluate these dimensions:

## Coverage Gaps
- Are there untested public functions or API endpoints?
- Is there unit, integration, AND e2e coverage where appropriate?
- Are critical paths (auth, payments, data mutations) fully tested?

## Test Quality
- Do assertions test behavior, not implementation details?
- Are test descriptions clear about what they verify?
- Do tests fail for the right reasons (not brittle/flaky)?
- Is each test independent (no shared mutable state)?

## Edge Cases
- Are boundary values tested (empty, null, max, negative)?
- Are error paths tested (network failures, invalid input, timeouts)?
- Are race conditions and concurrent access scenarios covered?

## Failure Modes
- What happens when external services are unavailable?
- Are retry and fallback mechanisms tested?
- Do tests verify graceful degradation?
- Are error messages and status codes correct for each failure?
