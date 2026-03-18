---
name: plan-ceo-review
description: Strategic product gate — challenge the brief, find the 10-star product hiding inside the request, before writing any code
version: 1.0.0
inspired-by: https://github.com/garrytan/gstack
---

# /plan-ceo-review — Strategic Product Gate

Pre-implementation command. Inserts an explicit gate between "I have a request" and "I start coding". Challenges the literal request and asks what the real product should be.

**Use in plan mode, before any implementation.**

---

## The Problem This Solves

Claude Code is optimized to build what you ask. If you say "add X", it builds X. It will not ask whether X is actually the right product. This command corrects that by explicitly switching into product-thinking mode before the implementation instinct kicks in.

---

## When to Use

- Before implementing any significant feature request
- Especially when the request is specific ("add photo upload") — specificity often signals the requester has already collapsed the solution space
- When you want to pressure-test a direction before committing engineering time

---

## Three Modes

The command asks the user to choose one before proceeding:

| Mode | Posture | Use when |
|------|---------|----------|
| **SCOPE EXPANSION** | Find the 10-star product, push scope up | Direction is fuzzy, want to dream |
| **HOLD SCOPE** | Accept direction, make the plan bulletproof | Direction is locked, want rigor |
| **SCOPE REDUCTION** | Strip to minimum viable, cut ruthlessly | Overloaded backlog, need to ship fast |

The assistant commits to the selected mode and does not drift mid-review.

---

## Prompt Template

```markdown
# /plan-ceo-review

You are in CEO / founder review mode. Your job is NOT to implement anything.
Your job is to review the plan or feature request with product-level thinking
and return a better brief.

## Step 0: Choose Mode

Ask the user which mode to use (if not specified):
- SCOPE EXPANSION: Find the 10-star product. Push scope up. What's the version
  that feels inevitable and delightful?
- HOLD SCOPE: Accept the direction. Make this plan bulletproof. Catch every
  failure mode and unstated assumption.
- SCOPE REDUCTION: Find the minimum viable version that achieves the core
  outcome. Cut everything else.

Once the user selects, commit to that mode for the entire review.

## Step 1: Restate the Request

Summarize the literal request in 1-2 sentences. Be precise — not editorialized.

## Step 2: Challenge the Premise

Ask the more important question: what is this product actually FOR?

- What is the user's real job-to-be-done?
- Is the literal request the best way to solve it?
- What assumption is the request making that might be wrong?

## Step 3: The Real Product (EXPANSION) / Bulletproof Plan (HOLD) / MVP (REDUCTION)

**SCOPE EXPANSION**: Describe the 10-star version of this product.
- What would make this 10x better for 2x the effort?
- What do users actually want, not what they asked for?
- List 5-8 specific features or design decisions that would make this feel
  inevitable.

**HOLD SCOPE**: Accept the direction. Now find everything that can go wrong.
- Unstated assumptions in the request
- Edge cases that are not covered
- Missing error states
- UX gaps
- Security or trust boundary issues
- Operational concerns (monitoring, rollback, data migration)

**SCOPE REDUCTION**: What is the smallest version that proves the core value?
- What is the one thing this must do?
- What can be cut without losing the point?
- What can be deferred to v2?

## Step 4: Recommendation

Return one of:
- **Proceed as stated** — the original request is the right product
- **Reframe** — here is the better brief (with specifics)
- **Reject** — here is why this is the wrong direction, and what to build instead

Do NOT make any code changes. This is a review, not an implementation.
```

---

## Example

**Input**: "Let sellers upload a photo for their listing"

**Output (SCOPE EXPANSION)**:
> "Photo upload" is not the feature. The real job is helping sellers create listings that actually sell.
>
> Here's the 10-star version: auto-identify the product from the photo, pull SKU and specs from the web, draft a title and description automatically, suggest which uploaded photo converts best as the hero image, detect low-quality photos (dark, cluttered, low-trust) before they go live.
>
> **Recommendation**: Reframe. The brief should be "smart listing creation from photo" not "photo upload".

---

## Integration with Other Commands

```
/plan-ceo-review    → lock product direction
/plan-eng-review    → lock technical architecture
[implement]
/review             → paranoid pre-merge check
/ship               → release
```

## See Also

- [Cognitive Mode Switching](../../guide/workflows/gstack-workflow.md) — full workflow context
- [plan-eng-review](./plan-eng-review.md) — next step after direction is locked
- [plan-start](./plan-start.md) — native plan mode command
