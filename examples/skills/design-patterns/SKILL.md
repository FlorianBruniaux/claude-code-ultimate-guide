---
name: design-patterns
description: "Detect, suggest, and evaluate GoF design patterns in TypeScript/JavaScript codebases. Use when refactoring code, applying singleton/factory/observer/strategy patterns, reviewing pattern quality, or finding stack-native alternatives for React, Angular, NestJS, and Vue."
allowed-tools: Read Grep Glob mcp__grepai__grepai_search
context: fork
agent: specialist
effort: high
---

# Design patterns analyzer skill

**Purpose**: Detect, suggest, and evaluate Gang of Four (GoF) design patterns in TypeScript/JavaScript codebases with stack-aware adaptations.

## Core capabilities

1. **Stack Detection**: Identify primary framework/library (React, Angular, NestJS, Vue, Express, RxJS, Redux, ORMs)
2. **Pattern Detection**: Find existing implementations of 23 GoF patterns
3. **Smart Suggestions**: Recommend patterns to fix code smells, using stack-native idioms when available
4. **Quality Evaluation**: Assess pattern implementation quality against best practices

## Operating modes

### Mode 1: Detection

**Trigger**: User requests pattern detection or analysis
**Output**: JSON report of patterns found with confidence scores and stack context

**Workflow**:
```
1. Stack Detection (package.json, tsconfig.json, framework files)
2. Pattern Search (Glob for candidates -> Grep for signatures -> Read for validation)
3. Classification (native to stack vs custom implementations)
4. Confidence Scoring (0.0-1.0 based on detection rules)
5. JSON Report Generation
```

**Example invocation**:
```
/design-patterns detect src/
/design-patterns analyze --format=json
```

### Mode 2: Suggestion

**Trigger**: User requests pattern suggestions or refactoring advice
**Output**: Markdown report with prioritized suggestions and stack-adapted examples

**Workflow**:
```
1. Code Smell Detection (switch statements, long parameter lists, global state, etc.)
2. Pattern Matching (map smell -> applicable patterns)
3. Stack Adaptation (prefer native framework patterns over custom implementations)
4. Priority Ranking (impact x feasibility)
5. Markdown Report with Code Examples
```

**Example invocation**:
```
/design-patterns suggest src/payment/
/design-patterns refactor --focus=creational
```

### Mode 3: Evaluation

**Trigger**: User requests pattern quality assessment
**Output**: JSON report with scores per evaluation criterion

**Workflow**:
```
1. Pattern Identification (which pattern is implemented)
2. Criteria Assessment (correctness, testability, SOLID compliance, documentation)
3. Issue Detection (common mistakes, anti-patterns)
4. Scoring (0-10 per criterion)
5. JSON Report with Recommendations
```

**Example invocation**:
```
/design-patterns evaluate src/services/singleton.ts
/design-patterns quality --pattern=observer
```

## Methodology

### Phase 1: Stack detection

**Sources** (in priority order):
1. `package.json` -> Check dependencies and devDependencies
2. Framework-specific files -> `angular.json`, `next.config.*`, `nest-cli.json`, `vite.config.*`
3. `tsconfig.json` -> Check compilerOptions, paths, lib
4. File extensions -> `*.jsx`, `*.tsx`, `*.vue` presence

**Detection Rules** (from `signatures/stack-patterns.yaml`):
- React: `react` in deps + `*.jsx/*.tsx` files
- Angular: `@angular/core` + `angular.json`
- NestJS: `@nestjs/core` + `nest-cli.json`
- Vue: `vue` v3+ + `*.vue` files
- Express: `express` in deps + `app.use` patterns
- RxJS: `rxjs` in deps + Observable usage
- Redux/Zustand: `redux`/`zustand` in deps + store patterns
- Prisma/TypeORM: `prisma`/`typeorm` in deps + schema files

**Output**:
```json
{
  "stack_detected": {
    "primary": "react",
    "version": "18.2.0",
    "secondary": ["typescript", "zustand", "prisma"],
    "detection_sources": ["package.json", "tsconfig.json", "37 *.tsx files"],
    "confidence": 0.95
  }
}
```

### Phase 2: Pattern detection

**Search Strategy**:
1. **Glob Phase**: Find candidate files by naming convention
   - `*Singleton*.ts`, `*Factory*.ts`, `*Strategy*.ts`, `*Observer*.ts`, etc.
   - `*Manager*.ts`, `*Builder*.ts`, `*Adapter*.ts`, `*Proxy*.ts`, etc.

2. **Grep Phase**: Search for pattern signatures (from `signatures/detection-rules.yaml`)
   - Primary signals: `private constructor`, `static getInstance()`, `subscribe()`, `createXxx()`, etc.
   - Secondary signals: Interface naming, delegation patterns, method signatures

3. **Read Phase**: Validate pattern structure
   - Parse class/interface definitions
   - Verify relationships (inheritance, composition, delegation)
   - Check for complete pattern implementation vs partial usage

**Confidence Scoring**:
- 0.9-1.0: All primary + secondary signals present, structure matches exactly
- 0.7-0.89: All primary signals + some secondary, minor deviations
- 0.5-0.69: Primary signals present, missing secondary validation
- 0.3-0.49: Naming convention matches, weak structural evidence
- 0.0-0.29: Insufficient evidence, likely false positive

**Classification**:
- `native`: Pattern implemented using stack-native features (React Context, Angular Services, NestJS Guards, etc.)
- `custom`: Manual TypeScript implementation
- `library`: Third-party library providing pattern (RxJS Subject, Redux Store, etc.)

### Phase 3: Code smell detection

**Target Smells** (from `signatures/code-smells.yaml`):
1. **Switch on Type** -> Strategy/Factory pattern
2. **Long Parameter List (>4)** -> Builder pattern
3. **Global State Access** -> Singleton (or preferably DI)
4. **Duplicated Conditionals on State** -> State pattern
5. **Scattered Notification Logic** -> Observer pattern
6. **Complex Object Creation** -> Factory/Abstract Factory
7. **Tight Coupling to Concrete Classes** -> Adapter/Bridge
8. **Repetitive Interface Conversions** -> Adapter pattern
9. **Deep Nesting for Feature Addition** -> Decorator pattern
10. **Large Class with Many Responsibilities** -> Facade pattern

**Detection Heuristics**:
- Grep for `switch (.*type)`, `switch (.*kind)`, `switch (.*mode)`
- Count function parameters: `function \w+\([^)]{60,}\)` (approximation for >4 params)
- Search for global access: `window\.`, `global\.`, `process\.env\.\w+` (not in config files)
- Find state conditionals: `if.*state.*===.*&&.*if.*state.*===`
- Find notification patterns: `forEach.*notify`, `map.*\.emit\(`

### Phase 4: Stack-Aware suggestions

**Adaptation Logic** (from `signatures/stack-patterns.yaml`):

```
IF pattern_detected == "custom" AND stack_has_native_equivalent:
  SUGGEST: "Use stack-native pattern instead"
  PROVIDE: Side-by-side comparison (current vs recommended)

ELSE IF code_smell_detected AND pattern_missing:
  IF stack_provides_pattern:
    SUGGEST: Stack-native implementation with examples
  ELSE:
    SUGGEST: Custom TypeScript implementation with best practices

ELSE IF pattern_implemented_incorrectly:
  PROVIDE: Refactoring steps to fix anti-patterns
```

**Example Adaptations**:

| Pattern | Stack | Native Alternative | Recommendation |
|---------|-------|-------------------|----------------|
| Singleton | React | Context API + Provider | Use `createContext()` instead of `getInstance()` |
| Observer | Angular | RxJS Subject/BehaviorSubject | Use built-in Observables, not custom implementation |
| Decorator | NestJS | @Injectable() decorators + Interceptors | Use framework interceptors |
| Strategy | Vue 3 | Composition API composables | Use `ref()` + composables instead of classes |
| Chain of Responsibility | Express | Middleware (`app.use()`) | Use Express middleware chain |
| Command | Redux | Action creators + reducers | Use Redux actions, not custom command objects |

### Phase 5: Quality evaluation

**Criteria** (from `checklists/pattern-evaluation.md`):
1. **Correctness (0-10)**: Does it match the canonical pattern structure?
2. **Testability (0-10)**: Can dependencies be mocked/stubbed easily?
3. **Single Responsibility (0-10)**: Does it do one thing only?
4. **Open/Closed Principle (0-10)**: Extensible without modification?
5. **Documentation (0-10)**: Clear intent, descriptive naming?

**Scoring Guidelines**:
- 9-10: Exemplary, reference-quality implementation
- 7-8: Good, minor improvements possible
- 5-6: Acceptable, notable issues to address
- 3-4: Problematic, significant refactoring needed
- 0-2: Incorrect or severely flawed

**Issue Detection**:
- Hard-coded dependencies (Singleton with new inside getInstance)
- God classes (too many responsibilities)
- Leaky abstractions (exposing internal structure)
- Missing error handling
- Poor naming (Strategy1, Strategy2 instead of descriptive names)

## Output formats

### Detection mode (JSON)

```json
{
  "metadata": {
    "scan_date": "2026-01-21T10:30:00Z",
    "scope": "src/",
    "files_scanned": 147,
    "execution_time_ms": 2341
  },
  "stack_detected": {
    "primary": "react",
    "version": "18.2.0",
    "secondary": ["typescript", "zustand", "prisma"],
    "detection_sources": ["package.json", "tsconfig.json", "37 *.tsx files"],
    "confidence": 0.95
  },
  "patterns_found": {
    "singleton": [
      {
        "file": "src/lib/api-client.ts",
        "lines": "5-28",
        "confidence": 0.85,
        "type": "custom",
        "signals": ["private constructor", "static getInstance", "private static instance"],
        "note": "Consider using React Context instead for better testability"
      }
    ],
    "observer": [
      {
        "file": "src/hooks/useAuth.ts",
        "lines": "12-45",
        "confidence": 0.92,
        "type": "native",
        "implementation": "React useState + useEffect",
        "note": "Correctly using React's built-in observer pattern"
      }
    ],
    "factory": [
      {
        "file": "src/services/notification-factory.ts",
        "lines": "8-67",
        "confidence": 0.78,
        "type": "custom",
        "signals": ["createNotification method", "type discrimination", "returns interface"]
      }
    ]
  },
  "summary": {
    "total_patterns": 7,
    "native_to_stack": 4,
    "custom_implementations": 3,
    "by_category": {
      "creational": 2,
      "structural": 3,
      "behavioral": 2
    },
    "by_confidence": {
      "high": 5,
      "medium": 2,
      "low": 0
    }
  },
  "recommendations": [
    "Consider replacing custom Singleton (api-client.ts) with React Context for better DI",
    "Review Factory pattern (notification-factory.ts) - could be simplified with strategy pattern"
  ]
}
```

### Suggestion mode (markdown)

```markdown
# Design Pattern Suggestions

**Scope**: `src/payment/`
**Stack**: React 18 + TypeScript + Stripe
**Date**: 2026-01-21

---

## High Priority

### 1. Strategy Pattern: `src/payment/processor.ts:45-89`

**Code Smell**: Switch statement on payment type (4 cases, 78 lines)

**Current Implementation** (lines 52-87):
```typescript
switch (paymentType) {
  case 'credit':
    // 20 lines of credit card logic
    break;
  case 'paypal':
    // 15 lines of PayPal logic
    break;
  case 'crypto':
    // 18 lines of crypto logic
    break;
  case 'bank':
    // 12 lines of bank transfer logic
    break;
}
```

**Recommended (React-adapted Strategy)**:
```typescript
// Define strategy interface
interface PaymentStrategy {
  process: (amount: number) => Promise<PaymentResult>;
}

// Custom hooks as strategies
const useCreditPayment = (): PaymentStrategy => ({
  process: async (amount) => { /* credit logic */ }
});

const usePaypalPayment = (): PaymentStrategy => ({
  process: async (amount) => { /* PayPal logic */ }
});

// Strategy selection hook
const usePaymentStrategy = (type: PaymentType): PaymentStrategy => {
  const strategies = {
    credit: useCreditPayment(),
    paypal: usePaypalPayment(),
    crypto: useCryptoPayment(),
    bank: useBankPayment(),
  };
  return strategies[type];
};

// Usage in component
const PaymentForm = ({ type }: Props) => {
  const strategy = usePaymentStrategy(type);
  const handlePay = () => strategy.process(amount);
  // ...
};
```

**Impact**:
- **Complexity**: Reduces cyclomatic complexity from 12 to 2
- **Extensibility**: New payment methods = new hook, no modification to existing code
- **Testability**: Each strategy hook can be tested in isolation
- **Effort**: ~2 hours (extract logic into hooks, add tests)

---

## Medium Priority

### 2. Observer Pattern: `src/cart/CartManager.ts:23-156`

**Code Smell**: Manual notification logic scattered across 8 methods

**Current**: Manual loops calling update functions
**Recommended**: Use Zustand store (already in dependencies)

```typescript
// Instead of custom observer:
import create from 'zustand';

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  // Zustand automatically notifies subscribers
}

export const useCartStore = create<CartStore>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({ items: state.items.filter(i => i.id !== id) })),
}));

// Components auto-subscribe:
const CartDisplay = () => {
  const items = useCartStore((state) => state.items);
  // Re-renders automatically on cart changes
};
```

**Impact**:
- **LOC**: Reduces from 156 to ~25 lines
- **Stack-native**: Uses existing Zustand dependency
- **Testability**: Zustand stores are easily tested
- **Effort**: ~1.5 hours

---

## Summary

- **Total suggestions**: 4
- **High priority**: 2 (Strategy, Observer)
- **Medium priority**: 2 (Builder, Facade)
- **Estimated total effort**: ~6 hours
- **Primary benefits**: Reduced complexity, improved testability, stack-native idioms
```

### Evaluation mode (JSON)

```json
{
  "file": "src/services/config-singleton.ts",
  "pattern": "singleton",
  "lines": "5-34",
  "scores": {
    "correctness": 8,
    "testability": 4,
    "single_responsibility": 9,
    "open_closed": 7,
    "documentation": 6,
    "overall": 6.8
  },
  "details": {
    "correctness": {
      "score": 8,
      "rationale": "Implements singleton structure correctly with private constructor and static getInstance",
      "issues": ["Missing thread-safety consideration (not critical in JS single-threaded context)"]
    },
    "testability": {
      "score": 4,
      "rationale": "Hard to mock or reset instance in tests",
      "issues": [
        "No reset method for test isolation",
        "Static instance makes dependency injection impossible",
        "Tests must run in specific order or share state"
      ],
      "suggestions": [
        "Add resetInstance() method for tests (with appropriate guards)",
        "Consider using dependency injection instead"
      ]
    },
    "single_responsibility": {
      "score": 9,
      "rationale": "Focuses solely on configuration management",
      "issues": []
    },
    "open_closed": {
      "score": 7,
      "rationale": "Configuration can be extended but requires modification for new sources",
      "suggestions": ["Consider strategy pattern for configuration sources"]
    },
    "documentation": {
      "score": 6,
      "rationale": "Has JSDoc but missing rationale for singleton choice",
      "suggestions": ["Document why singleton is chosen over DI", "Add usage examples"]
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "suggestion": "Add test-friendly reset mechanism or refactor to use DI",
      "rationale": "Current implementation makes testing difficult"
    },
    {
      "priority": "medium",
      "suggestion": "Document singleton rationale in JSDoc",
      "rationale": "Team members should understand why global state is necessary here"
    }
  ]
}
```

## Constraints & guidelines

### Read-only analysis
- **No modifications**: This skill only analyzes and suggests, never modifies code
- **No file creation**: Does not generate refactored code files
- **User decision**: All suggestions require explicit user approval before implementation

### Language focus
- **Primary**: TypeScript (`.ts`, `.tsx`)
- **Secondary**: JavaScript (`.js`, `.jsx`)
- **Exclusions**: Other languages (Python, Java, C#) not supported

### Pattern coverage
- **Creational (5)**: Singleton, Factory Method, Abstract Factory, Builder, Prototype
- **Structural (7)**: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
- **Behavioral (11)**: Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor, Interpreter

### Performance considerations
- **Large codebases (>500 files)**: Use `--scope` to limit scan to specific directories
- **Parallel search**: Grep searches run independently for each pattern
- **Caching**: Stack detection results cached per session to avoid redundant package.json reads

## Usage examples

### Basic detection
```bash
# Detect all patterns in src/
/design-patterns detect src/

# Detect only creational patterns
/design-patterns detect src/ --category=creational

# Focus on specific pattern
/design-patterns detect src/ --pattern=singleton
```

### Targeted suggestions
```bash
# Get suggestions for payment module
/design-patterns suggest src/payment/

# Focus on specific smell
/design-patterns suggest src/ --smell=switch-on-type

# High priority only
/design-patterns suggest src/ --priority=high
```

### Quality evaluation
```bash
# Evaluate specific file
/design-patterns evaluate src/services/api-client.ts

# Evaluate all singletons
/design-patterns evaluate src/ --pattern=singleton

# Full quality report
/design-patterns evaluate src/ --detailed
```

## Integration with other skills

This skill can be inherited by:
- `refactoring-specialist.md`: Provides pattern knowledge for refactoring
- `code-reviewer.md`: Adds pattern detection to review process
- `architecture-advisor.md`: Informs architectural decisions with pattern usage

## Reference files

- `reference/patterns-index.yaml`: Machine-readable index of 23 patterns with metadata
- `reference/creational.md`: Creational patterns documentation
- `reference/structural.md`: Structural patterns documentation
- `reference/behavioral.md`: Behavioral patterns documentation
- `signatures/detection-rules.yaml`: Regex patterns and heuristics for detection
- `signatures/code-smells.yaml`: Mapping from code smells to applicable patterns
- `signatures/stack-patterns.yaml`: Stack detection rules and native pattern equivalents
- `checklists/pattern-evaluation.md`: Quality evaluation criteria and scoring guidelines

## Version

**Skill Version**: 1.0.0
**Pattern Coverage**: 23 GoF patterns
**Supported Stacks**: 8 (React, Angular, NestJS, Vue, Express, RxJS, Redux/Zustand, ORMs)
**Last Updated**: 2026-01-21
