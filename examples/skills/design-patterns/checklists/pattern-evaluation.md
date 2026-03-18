---
title: "Design Pattern Quality Evaluation Checklist"
description: "Systematic scoring criteria for evaluating design pattern implementation quality"
tags: [cheatsheet, design-patterns, code-review]
---

# Design Pattern Quality Evaluation Checklist

Systematic criteria for evaluating the quality of design pattern implementations.

## Evaluation Criteria

Each criterion is scored **0-10**, where:
- **9-10**: Exemplary, reference-quality implementation
- **7-8**: Good, minor improvements possible
- **5-6**: Acceptable, notable issues to address
- **3-4**: Problematic, significant refactoring needed
- **0-2**: Incorrect or severely flawed

**Overall Score** = Average of all criteria scores

---

## 1. Correctness (0-10)

**Question**: Does the implementation correctly follow the canonical pattern structure?

### Scoring Guidelines

| Score | Description |
|-------|-------------|
| 9-10  | Perfect adherence to pattern structure, all roles present and correctly implemented |
| 7-8   | Minor deviations that don't compromise pattern intent |
| 5-6   | Some structural issues but pattern is recognizable and functional |
| 3-4   | Significant structural problems, pattern only partially implemented |
| 0-2   | Incorrect implementation, doesn't match pattern at all |

### Checklist

**Singleton**:
- [ ] Private constructor
- [ ] Static getInstance() method
- [ ] Private static instance field
- [ ] Thread-safe (if relevant)
- [ ] Returns same instance every time

**Observer**:
- [ ] Subject interface with attach/detach/notify
- [ ] Observer interface with update method
- [ ] Subject maintains list of observers
- [ ] Notify calls update on all observers
- [ ] Observers can be added/removed dynamically

**Strategy**:
- [ ] Strategy interface defining algorithm
- [ ] Context holds strategy reference
- [ ] Context delegates to strategy
- [ ] Strategies are interchangeable
- [ ] Client can set strategy at runtime

**Factory Method**:
- [ ] Factory method returns interface/abstract class
- [ ] Subclasses override factory method
- [ ] Client code depends on interface, not concrete classes
- [ ] Creation logic is encapsulated

**Decorator**:
- [ ] Decorator implements same interface as wrapped object
- [ ] Decorator holds reference to wrapped object
- [ ] Decorator delegates to wrapped object
- [ ] Can stack multiple decorators
- [ ] Maintains interface contract

### Common Mistakes (Deductions)

- **-2**: Missing key component (e.g., Singleton without private constructor)
- **-3**: Incorrect delegation (e.g., Decorator not calling wrapped object)
- **-4**: Breaking pattern invariants (e.g., Singleton returning different instances)

---

## 2. Testability (0-10)

**Question**: How easy is it to write unit tests for this implementation?

### Scoring Guidelines

| Score | Description |
|-------|-------------|
| 9-10  | Easily mockable, injectable dependencies, no global state |
| 7-8   | Testable with minor setup, some coupling exists |
| 5-6   | Requires significant test setup, moderate coupling |
| 3-4   | Hard to test, tight coupling, global state |
| 0-2   | Nearly impossible to test, static dependencies, no injection points |

### Checklist

- [ ] Dependencies are injected (not created internally)
- [ ] Interfaces are used (can be mocked)
- [ ] No hard-coded dependencies
- [ ] No global state access (or minimal)
- [ ] Test isolation is possible (tests don't affect each other)
- [ ] No static methods that can't be mocked
- [ ] Side effects are minimized or controllable

### Red Flags (Deductions)

- **-2**: Using `getInstance()` instead of dependency injection
- **-2**: Hard-coded concrete class instantiation
- **-3**: Accessing global state (window, global, process.env in business logic)
- **-3**: Static methods with side effects
- **-4**: No way to inject test doubles

### Examples

**Bad Testability (Score: 2/10)**:
```typescript
class PaymentService {
  processPayment(amount: number) {
    // Hard to test: creates dependency internally
    const gateway = PaymentGateway.getInstance();
    // Hard to test: accesses global config
    const apiKey = process.env.PAYMENT_API_KEY;
    return gateway.charge(amount, apiKey);
  }
}
```

**Good Testability (Score: 9/10)**:
```typescript
class PaymentService {
  constructor(
    private gateway: IPaymentGateway,
    private config: Config
  ) {}

  processPayment(amount: number) {
    const apiKey = this.config.getPaymentApiKey();
    return this.gateway.charge(amount, apiKey);
  }
}

// Easy to test with mocks
const mockGateway = { charge: jest.fn() };
const mockConfig = { getPaymentApiKey: () => 'test-key' };
const service = new PaymentService(mockGateway, mockConfig);
```

---

## 3. Single Responsibility Principle (0-10)

**Question**: Does the component have one, clearly defined responsibility?

### Scoring Guidelines

| Score | Description |
|-------|-------------|
| 9-10  | Single, focused responsibility; class has one reason to change |
| 7-8   | Mostly focused, minor secondary concerns |
| 5-6   | Multiple related responsibilities |
| 3-4   | Several unrelated responsibilities |
| 0-2   | God class with many responsibilities |

### Checklist

- [ ] Class/module has one clear purpose
- [ ] All methods relate to the primary responsibility
- [ ] Changing one requirement doesn't necessitate changing this class
- [ ] Class name clearly reflects its responsibility
- [ ] No "and" in class name or description (e.g., "UserManagerAndLogger" is bad)

### Red Flags (Deductions)

- **-2**: Class handles 2 distinct concerns
- **-3**: Class handles 3+ concerns
- **-4**: God class (>20 methods, >300 lines)
- **-1**: Methods unrelated to primary responsibility

### Examples

**Poor SRP (Score: 3/10)**:
```typescript
class UserService {
  createUser(data: UserData) { /* ... */ }
  validateEmail(email: string) { /* ... */ }
  sendWelcomeEmail(user: User) { /* ... */ }
  logUserActivity(activity: string) { /* ... */ }
  generateReport(userId: string) { /* ... */ }
  // Too many responsibilities: creation, validation, email, logging, reporting
}
```

**Good SRP (Score: 9/10)**:
```typescript
class UserService {
  constructor(
    private validator: UserValidator,
    private emailService: EmailService,
    private logger: Logger
  ) {}

  createUser(data: UserData): User {
    // Focuses only on user creation orchestration
    this.validator.validate(data);
    const user = new User(data);
    this.emailService.sendWelcomeEmail(user);
    this.logger.logActivity('user_created', user.id);
    return user;
  }
}
```

---

## 4. Open/Closed Principle (0-10)

**Question**: Can the component be extended without modifying its source code?

### Scoring Guidelines

| Score | Description |
|-------|-------------|
| 9-10  | Fully extensible via inheritance or composition, no modification needed |
| 7-8   | Mostly extensible, minor modifications might be needed |
| 5-6   | Some extension points exist but limited |
| 3-4   | Hard to extend, requires modification in multiple places |
| 0-2   | Closed for extension, must modify source code |

### Checklist

- [ ] Uses interfaces or abstract classes
- [ ] New behavior can be added via new classes, not modifications
- [ ] Configuration or strategy pattern for varying behavior
- [ ] No switch statements on types (if adding new type requires modification)
- [ ] Dependency inversion (depends on abstractions)

### Red Flags (Deductions)

- **-2**: Switch on type (adding new type requires modification)
- **-3**: No interfaces (concrete dependencies everywhere)
- **-3**: Hard-coded behavior (no extension points)
- **-4**: Modifying existing methods is the only way to add features

### Examples

**Closed for Extension (Score: 2/10)**:
```typescript
class PaymentProcessor {
  process(type: string, amount: number) {
    switch (type) {
      case 'credit': return this.processCreditCard(amount);
      case 'paypal': return this.processPaypal(amount);
      // Adding crypto payment requires modifying this class
    }
  }
}
```

**Open for Extension (Score: 9/10)**:
```typescript
interface PaymentStrategy {
  process(amount: number): Promise<Receipt>;
}

class PaymentProcessor {
  constructor(private strategies: Map<string, PaymentStrategy>) {}

  process(type: string, amount: number) {
    const strategy = this.strategies.get(type);
    if (!strategy) throw new Error(`Unknown payment type: ${type}`);
    return strategy.process(amount);
  }
}

// Add new payment method without modifying PaymentProcessor
class CryptoPaymentStrategy implements PaymentStrategy {
  process(amount: number) { /* ... */ }
}
```

---

## 5. Documentation (0-10)

**Question**: Is the implementation well-documented with clear intent and usage?

### Scoring Guidelines

| Score | Description |
|-------|-------------|
| 9-10  | Comprehensive documentation: intent, usage, examples, edge cases |
| 7-8   | Good documentation, covers main use cases |
| 5-6   | Basic documentation, minimal but present |
| 3-4   | Sparse documentation, unclear intent |
| 0-2   | No documentation or misleading documentation |

### Checklist

- [ ] Class/interface has JSDoc/TSDoc comment explaining purpose
- [ ] Pattern intent is documented ("This is a Singleton because...")
- [ ] Public methods have documentation
- [ ] Complex logic has inline comments
- [ ] Usage examples are provided (in README or comments)
- [ ] Invariants and constraints are documented
- [ ] Naming is self-documenting (clear, descriptive names)

### Red Flags (Deductions)

- **-2**: No class-level documentation
- **-2**: Public API methods undocumented
- **-3**: Cryptic naming (x, foo, temp, data)
- **-1**: Complex logic without explanation

### Examples

**Poor Documentation (Score: 2/10)**:
```typescript
class S {
  private static i: S;
  private constructor() {}
  static get() {
    if (!S.i) S.i = new S();
    return S.i;
  }
  do(x: any) { /* ... */ }
}
```

**Good Documentation (Score: 9/10)**:
```typescript
/**
 * Configuration service implemented as a Singleton to ensure
 * all components share the same configuration state.
 *
 * Use `ConfigService.getInstance()` to access the singleton instance.
 *
 * @example
 * const config = ConfigService.getInstance();
 * const apiUrl = config.get('API_URL');
 */
class ConfigService {
  private static instance: ConfigService;

  /**
   * Private constructor prevents direct instantiation.
   * Use `getInstance()` instead.
   */
  private constructor() {
    // Load configuration from environment
  }

  /**
   * Returns the singleton instance of ConfigService.
   * Creates the instance on first call (lazy initialization).
   *
   * @returns The singleton ConfigService instance
   */
  public static getInstance(): ConfigService {
    if (!ConfigService.instance) {
      ConfigService.instance = new ConfigService();
    }
    return ConfigService.instance;
  }

  /**
   * Retrieves a configuration value by key.
   *
   * @param key - Configuration key
   * @returns Configuration value or undefined if not found
   */
  public get(key: string): string | undefined {
    return process.env[key];
  }
}
```

---

## Pattern-Specific Evaluation

### Singleton Specific

**Additional Checklist**:
- [ ] Lazy initialization (if appropriate)
- [ ] Thread-safety considered (less critical in JS)
- [ ] Subclassing is prevented or controlled
- [ ] No public constructor
- [ ] Reset mechanism for tests (or DI alternative mentioned)

**Deductions**:
- **-3**: Public constructor (defeats purpose)
- **-2**: Multiple getInstance() methods returning different instances
- **-2**: No consideration of test isolation

### Observer Specific

**Additional Checklist**:
- [ ] Observers can unsubscribe
- [ ] No memory leaks (observers are properly removed)
- [ ] Notification order is deterministic (if it matters)
- [ ] Observers don't depend on notification order
- [ ] Subject doesn't know concrete observer types

**Deductions**:
- **-3**: No unsubscribe mechanism (memory leak risk)
- **-2**: Subject depends on concrete observer types
- **-2**: Notification order matters but isn't guaranteed

### Strategy Specific

**Additional Checklist**:
- [ ] Strategies implement common interface
- [ ] Context doesn't depend on concrete strategies
- [ ] Strategies are interchangeable
- [ ] Strategy can be set at runtime
- [ ] Strategies don't share state (unless explicitly designed to)

**Deductions**:
- **-3**: Context depends on concrete strategies
- **-2**: Strategies are not truly interchangeable
- **-2**: No way to change strategy at runtime

---

## Overall Assessment Formula

```
Overall Score = (
  Correctness × 0.30 +
  Testability × 0.25 +
  Single Responsibility × 0.20 +
  Open/Closed × 0.15 +
  Documentation × 0.10
) / 5
```

**Weighted** because correctness is most important, followed by testability.

---

## Interpretation Guide

| Overall Score | Interpretation | Action |
|--------------|----------------|--------|
| 9.0 - 10.0   | Excellent | Reference-quality, minimal changes needed |
| 7.0 - 8.9    | Good | Minor improvements, production-ready |
| 5.0 - 6.9    | Acceptable | Notable issues, refactoring recommended |
| 3.0 - 4.9    | Poor | Significant problems, refactoring required |
| 0.0 - 2.9    | Critical | Fundamentally flawed, redesign needed |

---

## Example Evaluation Report

### Pattern: Singleton
**File**: `src/services/config-singleton.ts`
**Lines**: 5-34

#### Scores

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Correctness | 8/10 | Implements singleton correctly, minor: no thread-safety (not critical in JS) |
| Testability | 4/10 | Hard to mock, no reset mechanism, global state makes tests interdependent |
| Single Responsibility | 9/10 | Focuses solely on configuration management |
| Open/Closed | 7/10 | Can add new config keys, but config sources are hard-coded |
| Documentation | 6/10 | Has JSDoc but missing rationale for singleton choice |

**Overall Score**: **6.8/10** (Acceptable)

#### Issues Identified

1. **High Priority**: Add `resetInstance()` method for test isolation
   - Current: Tests must run in specific order
   - Fix: Add `public static resetInstance()` guarded by environment check

2. **Medium Priority**: Document singleton rationale
   - Current: Unclear why global state is necessary
   - Fix: Add JSDoc explaining choice (e.g., "Singleton ensures consistent config across all services")

3. **Low Priority**: Consider dependency injection alternative
   - Current: Hard to test, tight coupling
   - Recommendation: Evaluate using DI container or React Context

#### Recommendations

```typescript
// Add test-friendly reset
public static resetInstance(): void {
  if (process.env.NODE_ENV === 'test') {
    ConfigService.instance = null!;
  }
}

// Better yet: refactor to DI
class ConfigService {
  constructor(private envVars: EnvVars) {}
}

// Inject in DI container or provider
const config = new ConfigService(process.env);
```

---

## Usage in Skill

When the design-patterns skill runs in **Evaluation Mode**, it:

1. Identifies which pattern is implemented
2. Applies relevant checklist items
3. Scores each criterion (0-10)
4. Calculates weighted overall score
5. Generates detailed report with:
   - Scores table
   - Issues found (priority-ranked)
   - Specific recommendations with code examples
   - Stack-native alternatives if applicable

---

## References

- *Clean Code* by Robert C. Martin (SOLID principles)
- *Refactoring: Improving the Design of Existing Code* by Martin Fowler
- *Design Patterns: Elements of Reusable Object-Oriented Software* (Gang of Four)
