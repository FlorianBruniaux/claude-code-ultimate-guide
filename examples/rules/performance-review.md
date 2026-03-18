---
description: "Performance review criteria for plan and code reviews"
---

# Performance Review Criteria

When reviewing performance, evaluate these dimensions:

## Database Access
- Are there N+1 query patterns (loop with individual queries)?
- Are queries using appropriate indexes?
- Is data fetched at the right granularity (not over-fetching)?
- Are bulk operations used where possible?

## Memory
- Are large datasets streamed rather than loaded entirely in memory?
- Are there potential memory leaks (event listeners, unclosed connections)?
- Is object allocation minimized in hot paths?

## Caching
- What data is expensive to compute and stable enough to cache?
- Are cache invalidation strategies defined?
- Is caching applied at the right layer (application, database, CDN)?

## Complexity
- Are there O(n^2) or worse algorithms that could be optimized?
- Are hot paths identified and optimized?
- Is unnecessary work being done (redundant computations, unused data transforms)?
- Are expensive operations deferred or lazy-loaded where possible?
