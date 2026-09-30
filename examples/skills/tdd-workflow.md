---
name: tdd-workflow
description: Test-Driven Development workflow and best practices
effort: low
---

# TDD workflow skill

## The TDD cycle

```
RED → GREEN → REFACTOR
 ↑__________________|
```

### 1. RED: Write a failing test
- Write the smallest test that fails
- Test should fail for the right reason
- Ensure the test actually runs

### 2. GREEN: Make it Pass
- Write minimal code to pass the test
- Don't optimize yet
- It's okay if the code is ugly

### 3. REFACTOR: Clean up
- Improve code structure
- Remove duplication
- Keep tests passing

## TDD best practices

### Test naming convention
```
should_[expected behavior]_when_[condition]
```

Examples:
- `should_return_empty_array_when_no_items`
- `should_throw_error_when_invalid_input`
- `should_calculate_total_when_items_present`

### Test structure (AAA)
```typescript
it('should calculate discount when coupon applied', () => {
  // Arrange - Set up test data
  const cart = new Cart();
  cart.addItem({ price: 100 });
  const coupon = new Coupon('10OFF', 10);

  // Act - Execute the behavior
  cart.applyCoupon(coupon);

  // Assert - Verify the result
  expect(cart.total).toBe(90);
});
```

### Test isolation
- Each test should be independent
- No shared state between tests
- Use `beforeEach` for common setup
- Clean up in `afterEach`

## TDD workflow example

### Feature: Add item to cart

**Step 1: RED**
```typescript
describe('Cart', () => {
  it('should add item to cart', () => {
    const cart = new Cart();
    cart.addItem({ id: 1, name: 'Book', price: 29.99 });
    expect(cart.items).toHaveLength(1);
  });
});
```
Run test → FAILS (Cart doesn't exist)

**Step 2: GREEN**
```typescript
class Cart {
  items = [];

  addItem(item) {
    this.items.push(item);
  }
}
```
Run test → PASSES

**Step 3: REFACTOR**
```typescript
class Cart {
  private _items: CartItem[] = [];

  get items(): ReadonlyArray<CartItem> {
    return this._items;
  }

  addItem(item: CartItem): void {
    this._items.push(item);
  }
}
```
Run test → Still PASSES

### Next iteration: Calculate total
Repeat the cycle for each new behavior.

## When to use TDD

### Good for TDD
- Business logic
- Complex algorithms
- API endpoints
- State management
- Utility functions

### Less suitable
- UI layout (visual testing better)
- Database migrations
- External integrations (use integration tests)
- Exploratory/prototype code

## Common TDD mistakes

1. **Writing too much test** - Start with smallest failing test
2. **Writing too much code** - Only enough to pass
3. **Skipping refactor** - Technical debt accumulates
4. **Testing implementation** - Test behavior, not internals
5. **Ignoring failing tests** - Fix or delete, never skip

## Test doubles

| Type | Purpose | Example |
|------|---------|---------|
| Stub | Return fixed data | `jest.fn().mockReturnValue(42)` |
| Mock | Verify interactions | `expect(mock).toHaveBeenCalled()` |
| Spy | Track calls | `jest.spyOn(obj, 'method')` |
| Fake | Simplified implementation | In-memory database |
