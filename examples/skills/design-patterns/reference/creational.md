---
title: "Creational Design Patterns"
description: "Reference for Singleton, Factory, Builder, Prototype and other object creation patterns"
tags: [reference, design-patterns, architecture]
---

# Creational Design Patterns

Patterns that deal with object creation mechanisms, trying to create objects in a manner suitable to the situation.

## Singleton

### Definition
Ensures a class has only one instance and provides a global point of access to it.

### When to Use
- [x] Exactly one instance of a class is needed (configuration, logging, database connection)
- [x] Controlled access to a single object is required
- [x] The instance should be extensible by subclassing

**Warning**: Often overused. Consider dependency injection or context-based alternatives first.

### TypeScript Signature
```typescript
class Singleton {
  private static instance: Singleton;
  private constructor() {
    // Private constructor prevents instantiation
  }

  public static getInstance(): Singleton {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton();
    }
    return Singleton.instance;
  }

  public someMethod(): void {
    // Business logic
  }
}

// Usage
const instance = Singleton.getInstance();
```

### Stack-Native Alternatives

**React**:
```typescript
// Instead of Singleton, use Context
const ConfigContext = createContext<Config>(defaultConfig);

export const ConfigProvider = ({ children }: Props) => {
  const [config] = useState(() => loadConfig());
  return <ConfigContext.Provider value={config}>{children}</ConfigContext.Provider>;
};
```

**Angular**:
```typescript
// Injectable service (singleton by default)
@Injectable({ providedIn: 'root' })
export class ConfigService {
  // Automatically singleton via DI
}
```

**NestJS**:
```typescript
@Injectable() // Default scope is SINGLETON
export class AppService {}
```

### Detection Markers
- `private constructor`
- `static getInstance()` method
- `private static instance` field
- Lazy initialization check: `if (!instance)`

### Code Smells It Fixes
- **Global state access**: Provides controlled access instead of scattered global variables
- **Multiple instances of shared resource**: Ensures single database connection, config object, etc.

### Common Mistakes
- **Hard to test**: Static methods and global state make unit testing difficult
  - *Solution*: Use dependency injection instead, or provide `resetInstance()` for tests
- **Thread-safety issues**: (Less relevant in JavaScript's single-threaded model, but important for Node.js workers)
- **Hidden dependencies**: Classes using `getInstance()` have hidden coupling
- **Violates Single Responsibility**: Often manages both instance creation and business logic

### Evaluation Criteria
- **Testability**: 3/10 (hard to mock, global state)
- **Thread-safety**: 7/10 (less critical in JS)
- **Extensibility**: 5/10 (subclassing is complex)

---

## Factory Method

### Definition
Defines an interface for creating an object, but lets subclasses decide which class to instantiate.

### When to Use
- [x] Class cannot anticipate the type of objects it needs to create
- [x] Class wants its subclasses to specify the objects it creates
- [x] Centralize object creation logic to avoid duplication
- [x] Need to decouple object creation from usage

### TypeScript Signature
```typescript
// Product interface
interface Product {
  operation(): string;
}

// Concrete products
class ConcreteProductA implements Product {
  operation(): string {
    return 'Product A';
  }
}

class ConcreteProductB implements Product {
  operation(): string {
    return 'Product B';
  }
}

// Creator (Factory)
abstract class Creator {
  // Factory method
  abstract createProduct(): Product;

  // Business logic using the product
  someOperation(): string {
    const product = this.createProduct();
    return `Creator: ${product.operation()}`;
  }
}

// Concrete creators
class CreatorA extends Creator {
  createProduct(): Product {
    return new ConcreteProductA();
  }
}

class CreatorB extends Creator {
  createProduct(): Product {
    return new ConcreteProductB();
  }
}

// Usage
const creator: Creator = new CreatorA();
console.log(creator.someOperation());
```

### Modern TypeScript Alternative
```typescript
// Simpler approach without inheritance
type ProductType = 'A' | 'B';

function createProduct(type: ProductType): Product {
  switch (type) {
    case 'A': return new ConcreteProductA();
    case 'B': return new ConcreteProductB();
  }
}
```

### Detection Markers
- Method named `create*()` returning interface/abstract class
- `abstract createProduct()` in base class
- Subclasses override factory method
- `switch` or `if-else` on type/kind parameter

### Code Smells It Fixes
- **Tight coupling to concrete classes**: Client code depends on interface, not implementation
- **Duplication of instantiation logic**: Centralized in factory method
- **Switch statements scattered**: Consolidated in one place

### Common Mistakes
- **Simple Factory confusion**: Factory Method uses inheritance; Simple Factory uses composition
- **Too many parameters**: Should create objects with default configuration
- **Forgetting to make factory method abstract**: Defeats the purpose of subclass specialization

### Evaluation Criteria
- **Testability**: 8/10 (easy to mock products)
- **Flexibility**: 9/10 (new products don't modify existing code)
- **Complexity**: 6/10 (adds inheritance hierarchy)

---

## Abstract Factory

### Definition
Provides an interface for creating families of related or dependent objects without specifying their concrete classes.

### When to Use
- [x] System should be independent of how its products are created
- [x] System should be configured with one of multiple families of products
- [x] Family of related product objects must be used together
- [x] You want to provide a library of products and reveal only interfaces

### TypeScript Signature
```typescript
// Abstract products
interface AbstractProductA {
  usefulFunctionA(): string;
}

interface AbstractProductB {
  usefulFunctionB(): string;
  anotherFunctionB(collaborator: AbstractProductA): string;
}

// Concrete products - Family 1
class ConcreteProductA1 implements AbstractProductA {
  usefulFunctionA(): string {
    return 'Product A1';
  }
}

class ConcreteProductB1 implements AbstractProductB {
  usefulFunctionB(): string {
    return 'Product B1';
  }

  anotherFunctionB(collaborator: AbstractProductA): string {
    return `B1 collaborating with ${collaborator.usefulFunctionA()}`;
  }
}

// Concrete products - Family 2
class ConcreteProductA2 implements AbstractProductA {
  usefulFunctionA(): string {
    return 'Product A2';
  }
}

class ConcreteProductB2 implements AbstractProductB {
  usefulFunctionB(): string {
    return 'Product B2';
  }

  anotherFunctionB(collaborator: AbstractProductA): string {
    return `B2 collaborating with ${collaborator.usefulFunctionA()}`;
  }
}

// Abstract factory
interface AbstractFactory {
  createProductA(): AbstractProductA;
  createProductB(): AbstractProductB;
}

// Concrete factories
class ConcreteFactory1 implements AbstractFactory {
  createProductA(): AbstractProductA {
    return new ConcreteProductA1();
  }

  createProductB(): AbstractProductB {
    return new ConcreteProductB1();
  }
}

class ConcreteFactory2 implements AbstractFactory {
  createProductA(): AbstractProductA {
    return new ConcreteProductA2();
  }

  createProductB(): AbstractProductB {
    return new ConcreteProductB2();
  }
}

// Client code
function clientCode(factory: AbstractFactory) {
  const productA = factory.createProductA();
  const productB = factory.createProductB();

  console.log(productB.anotherFunctionB(productA));
}

// Usage
clientCode(new ConcreteFactory1());
clientCode(new ConcreteFactory2());
```

### Detection Markers
- Multiple `create*()` methods in factory interface
- Families of related products (e.g., Button + Checkbox for Windows/Mac)
- Factory implementations return different product families
- Interface with 2+ factory methods

### Code Smells It Fixes
- **Inconsistent product families**: Ensures compatible products are created together (Windows Button + Windows Checkbox, not mixed)
- **Scattered creation logic**: Centralizes creation of related objects

### Common Mistakes
- **Over-engineering**: Often too complex for simple scenarios; Factory Method may suffice
- **Rigid product families**: Adding new product types requires changing all factories
- **Confusion with Factory Method**: Abstract Factory creates families; Factory Method creates one product type

### Evaluation Criteria
- **Testability**: 8/10 (factories are easily mocked)
- **Consistency**: 10/10 (guarantees compatible products)
- **Complexity**: 4/10 (high complexity, many classes)

---

## Builder

### Definition
Separates the construction of a complex object from its representation, allowing step-by-step construction.

### When to Use
- [x] Object has many optional parameters (>4)
- [x] Construction process should allow different representations
- [x] Need to construct complex objects step-by-step
- [x] Want to avoid "telescoping constructor" anti-pattern

### TypeScript Signature
```typescript
// Product
class House {
  public walls: string = '';
  public doors: number = 0;
  public windows: number = 0;
  public roof: string = '';
  public garage: boolean = false;
  public pool: boolean = false;

  public describe(): string {
    return `House with ${this.walls} walls, ${this.doors} doors, ${this.windows} windows, ${this.roof} roof, garage: ${this.garage}, pool: ${this.pool}`;
  }
}

// Builder
class HouseBuilder {
  private house: House;

  constructor() {
    this.house = new House();
  }

  public setWalls(walls: string): this {
    this.house.walls = walls;
    return this;
  }

  public setDoors(doors: number): this {
    this.house.doors = doors;
    return this;
  }

  public setWindows(windows: number): this {
    this.house.windows = windows;
    return this;
  }

  public setRoof(roof: string): this {
    this.house.roof = roof;
    return this;
  }

  public addGarage(): this {
    this.house.garage = true;
    return this;
  }

  public addPool(): this {
    this.house.pool = true;
    return this;
  }

  public build(): House {
    const result = this.house;
    this.house = new House(); // Reset for next build
    return result;
  }
}

// Usage
const house = new HouseBuilder()
  .setWalls('brick')
  .setDoors(2)
  .setWindows(6)
  .setRoof('tile')
  .addGarage()
  .build();
```

### Modern TypeScript Alternative (Type-Safe Builder)
```typescript
// Progressive type safety: each step unlocks the next
type HouseBuilderState<
  TWalls extends boolean = false,
  TRoof extends boolean = false
> = {
  setWalls: TWalls extends true ? never : (walls: string) => HouseBuilderState<true, TRoof>;
  setRoof: TRoof extends true ? never : (roof: string) => HouseBuilderState<TWalls, true>;
  build: TWalls extends true ? (TRoof extends true ? () => House : never) : never;
};
```

### Detection Markers
- Method chaining (returns `this` or builder type)
- `build()` method returning final product
- `with*()` or `set*()` methods
- Optional fields being set incrementally

### Code Smells It Fixes
- **Telescoping constructor**: Constructor with many parameters
  ```typescript
  // Bad
  new House(walls, doors, windows, roof, garage, pool, garden, basement, ...);

  // Good with Builder
  new HouseBuilder().setWalls('brick').setRoof('tile').build();
  ```
- **Unclear parameter order**: Named methods make intent clear
- **Optional parameters complexity**: Builder handles optional features elegantly

### Common Mistakes
- **Mutable builder**: Reusing builder can lead to unexpected state
  - *Solution*: Reset internal state after `build()`
- **Incomplete builder**: Not validating required fields in `build()`
  - *Solution*: Use TypeScript types to enforce required steps
- **Too simple for the pattern**: If <4 parameters, constructor or object literal may be simpler

### Evaluation Criteria
- **Testability**: 9/10 (easy to create test fixtures)
- **Readability**: 10/10 (fluent interface is self-documenting)
- **Complexity**: 7/10 (adds builder class)

---

## Prototype

### Definition
Creates new objects by copying an existing object (prototype) rather than creating from scratch.

### When to Use
- [x] Object creation is expensive (complex initialization, database queries)
- [x] Need to avoid subclassing just to change initialization
- [x] System should be independent of how products are created
- [x] Classes to instantiate are specified at runtime

### TypeScript Signature
```typescript
// Prototype interface
interface Prototype {
  clone(): Prototype;
}

// Concrete prototype
class ConcretePrototype implements Prototype {
  public field: number;
  public complexObject: { data: string };

  constructor(field: number, complexObject: { data: string }) {
    this.field = field;
    this.complexObject = complexObject;
  }

  // Shallow clone
  public clone(): ConcretePrototype {
    return Object.create(this);
  }

  // Deep clone
  public deepClone(): ConcretePrototype {
    return new ConcretePrototype(
      this.field,
      { data: this.complexObject.data } // Clone nested objects
    );
  }
}

// Usage
const original = new ConcretePrototype(42, { data: 'important' });
const shallowCopy = original.clone();
const deepCopy = original.deepClone();

// Shallow copy shares nested objects
shallowCopy.complexObject.data = 'modified';
console.log(original.complexObject.data); // 'modified' (!)

// Deep copy is independent
deepCopy.field = 99;
console.log(original.field); // 42 (unchanged)
```

### Modern JavaScript Alternatives
```typescript
// Spread operator (shallow)
const copy1 = { ...original };

// Object.assign (shallow)
const copy2 = Object.assign({}, original);

// structuredClone (deep, modern browsers/Node 17+)
const copy3 = structuredClone(original);

// JSON (deep, but limited: no functions, undefined, etc.)
const copy4 = JSON.parse(JSON.stringify(original));
```

### Detection Markers
- `clone()` method
- `Object.create()`
- `structuredClone()`
- `JSON.parse(JSON.stringify())` pattern
- Spread operator `{ ...obj }`

### Code Smells It Fixes
- **Expensive initialization**: Clone instead of re-initializing
- **Complex object graphs**: Cloning preserves relationships
- **Runtime type specification**: Clone prototype instead of hardcoding types

### Common Mistakes
- **Shallow vs Deep clone confusion**: Shallow clone shares nested objects
  ```typescript
  // Dangerous if nested objects are modified
  const shallow = { ...original };
  ```
- **Circular references**: `JSON.stringify` fails on circular references
  - *Solution*: Use `structuredClone()` or custom clone logic
- **Cloning methods/functions**: Some approaches lose methods
  ```typescript
  JSON.parse(JSON.stringify(obj)); // Loses all methods!
  ```
- **Not cloning private state**: Ensure all necessary state is copied

### Evaluation Criteria
- **Performance**: 9/10 (faster than re-initialization)
- **Simplicity**: 7/10 (shallow vs deep cloning is tricky)
- **Reliability**: 6/10 (easy to get wrong with nested objects)

---

## Summary Table

| Pattern | Complexity | Use Frequency | Main Benefit |
|---------|------------|---------------|--------------|
| Singleton | Low | High | Global access control |
| Factory Method | Medium | High | Decouples creation from usage |
| Abstract Factory | High | Medium | Consistent product families |
| Builder | Medium | High | Fluent construction of complex objects |
| Prototype | Low | Low | Efficient cloning |

## Best Practices

1. **Prefer composition over inheritance**: Factory and Builder often better than Singleton
2. **Use stack-native alternatives**: React Context > Singleton, DI > getInstance()
3. **TypeScript leverage**: Use generics and type constraints for type-safe builders
4. **Test-friendly design**: Avoid Singleton; use dependency injection
5. **Simplicity first**: Don't use Abstract Factory when Factory Method suffices

## References

- *Design Patterns: Elements of Reusable Object-Oriented Software* (Gang of Four)
- *Effective TypeScript* by Dan Vanderkam
- [Refactoring Guru: Creational Patterns](https://refactoring.guru/design-patterns/creational-patterns)
