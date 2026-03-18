---
title: "Structural Design Patterns"
description: "Reference for Adapter, Decorator, Facade, Proxy and other composition patterns"
tags: [reference, design-patterns, architecture]
---

# Structural Design Patterns

Patterns that deal with object composition and relationships between entities, providing ways to assemble objects and classes into larger structures.

## Adapter

### Definition
Converts the interface of a class into another interface clients expect, allowing incompatible interfaces to work together.

### When to Use
- [x] Want to use an existing class with an incompatible interface
- [x] Need to integrate third-party libraries with different interfaces
- [x] Want to create a reusable class that cooperates with unrelated classes
- [x] Legacy code must work with new systems

### TypeScript Signature
```typescript
// Target interface (what client expects)
interface Target {
  request(): string;
}

// Adaptee (existing incompatible class)
class Adaptee {
  specificRequest(): string {
    return '.eetpadA eht fo roivaheb laicepS';
  }
}

// Adapter (makes Adaptee compatible with Target)
class Adapter implements Target {
  private adaptee: Adaptee;

  constructor(adaptee: Adaptee) {
    this.adaptee = adaptee;
  }

  public request(): string {
    const result = this.adaptee.specificRequest().split('').reverse().join('');
    return `Adapter: ${result}`;
  }
}

// Client code
function clientCode(target: Target) {
  console.log(target.request());
}

// Usage
const adaptee = new Adaptee();
const adapter = new Adapter(adaptee);
clientCode(adapter);
```

### Real-World Example: Third-Party Library Integration
```typescript
// Third-party library (can't modify)
class XMLDataProvider {
  getXMLData(): string {
    return '<data><item>1</item></data>';
  }
}

// Your application expects JSON
interface JSONDataProvider {
  getJSONData(): object;
}

// Adapter
class XMLToJSONAdapter implements JSONDataProvider {
  constructor(private xmlProvider: XMLDataProvider) {}

  getJSONData(): object {
    const xml = this.xmlProvider.getXMLData();
    // Convert XML to JSON (simplified)
    return { data: { item: '1' } };
  }
}

// Usage
const xmlProvider = new XMLDataProvider();
const adapter = new XMLToJSONAdapter(xmlProvider);
const data = adapter.getJSONData();
```

### Detection Markers
- Class implements target interface
- Holds reference to adaptee
- Delegates to adaptee with interface conversion
- Names like `*Adapter`, `*Wrapper`

### Code Smells It Fixes
- **Incompatible interfaces**: Makes legacy or third-party code compatible
- **Interface proliferation**: Single adapter vs modifying multiple client calls

### Common Mistakes
- **Two-way adapters**: Bidirectional conversion is complex; create two adapters
- **Adapter chains**: Multiple adapters in sequence indicate design issues
- **Overusing for new code**: Design compatible interfaces from the start

---

## Bridge

### Definition
Decouples an abstraction from its implementation so the two can vary independently.

### When to Use
- [x] Want to avoid permanent binding between abstraction and implementation
- [x] Both abstractions and implementations should be extensible by subclassing
- [x] Changes in implementation shouldn't affect clients
- [x] Want to share implementation among multiple objects (Flyweight-like)

### TypeScript Signature
```typescript
// Implementation interface
interface Implementation {
  operationImpl(): string;
}

// Concrete implementations
class ConcreteImplementationA implements Implementation {
  operationImpl(): string {
    return 'ConcreteImplementationA';
  }
}

class ConcreteImplementationB implements Implementation {
  operationImpl(): string {
    return 'ConcreteImplementationB';
  }
}

// Abstraction
class Abstraction {
  constructor(protected implementation: Implementation) {}

  public operation(): string {
    return `Abstraction: ${this.implementation.operationImpl()}`;
  }
}

// Refined abstraction
class ExtendedAbstraction extends Abstraction {
  public operation(): string {
    return `ExtendedAbstraction: ${this.implementation.operationImpl()}`;
  }
}

// Usage
const implA = new ConcreteImplementationA();
const abstraction1 = new Abstraction(implA);
console.log(abstraction1.operation());

const implB = new ConcreteImplementationB();
const abstraction2 = new ExtendedAbstraction(implB);
console.log(abstraction2.operation());
```

### Real-World Example: UI Components with Multiple Renderers
```typescript
// Implementation: Renderers
interface Renderer {
  renderCircle(radius: number): string;
  renderSquare(side: number): string;
}

class VectorRenderer implements Renderer {
  renderCircle(radius: number): string {
    return `Drawing circle (vector) with radius ${radius}`;
  }
  renderSquare(side: number): string {
    return `Drawing square (vector) with side ${side}`;
  }
}

class RasterRenderer implements Renderer {
  renderCircle(radius: number): string {
    return `Drawing circle (pixels) with radius ${radius}`;
  }
  renderSquare(side: number): string {
    return `Drawing square (pixels) with side ${side}`;
  }
}

// Abstraction: Shapes
abstract class Shape {
  constructor(protected renderer: Renderer) {}
  abstract draw(): string;
}

class Circle extends Shape {
  constructor(renderer: Renderer, private radius: number) {
    super(renderer);
  }
  draw(): string {
    return this.renderer.renderCircle(this.radius);
  }
}

class Square extends Shape {
  constructor(renderer: Renderer, private side: number) {
    super(renderer);
  }
  draw(): string {
    return this.renderer.renderSquare(this.side);
  }
}

// Usage: Can mix any shape with any renderer
const vectorCircle = new Circle(new VectorRenderer(), 5);
const rasterSquare = new Square(new RasterRenderer(), 10);
```

### Detection Markers
- Abstraction holds reference to implementation interface
- Constructor injects implementation
- Two parallel hierarchies (abstraction and implementation)

### Common Mistakes
- **Confusion with Adapter**: Bridge is design-time; Adapter is runtime fix
- **Over-engineering simple scenarios**: Use only when both hierarchies need to vary

---

## Composite

### Definition
Composes objects into tree structures to represent part-whole hierarchies, letting clients treat individual objects and compositions uniformly.

### When to Use
- [x] Want to represent part-whole hierarchies of objects
- [x] Want clients to ignore difference between compositions and individual objects
- [x] Tree structures are natural for the domain (file systems, UI components, org charts)

### TypeScript Signature
```typescript
// Component interface
interface Component {
  operation(): string;
  add?(component: Component): void;
  remove?(component: Component): void;
  getChild?(index: number): Component;
}

// Leaf (no children)
class Leaf implements Component {
  constructor(private name: string) {}

  operation(): string {
    return this.name;
  }
}

// Composite (has children)
class Composite implements Component {
  private children: Component[] = [];

  constructor(private name: string) {}

  add(component: Component): void {
    this.children.push(component);
  }

  remove(component: Component): void {
    const index = this.children.indexOf(component);
    if (index !== -1) {
      this.children.splice(index, 1);
    }
  }

  getChild(index: number): Component {
    return this.children[index];
  }

  operation(): string {
    const results = this.children.map(child => child.operation());
    return `${this.name}(${results.join(', ')})`;
  }
}

// Usage
const tree = new Composite('root');
const branch1 = new Composite('branch1');
branch1.add(new Leaf('leaf1'));
branch1.add(new Leaf('leaf2'));

const branch2 = new Composite('branch2');
branch2.add(new Leaf('leaf3'));

tree.add(branch1);
tree.add(branch2);
tree.add(new Leaf('leaf4'));

console.log(tree.operation());
// Output: root(branch1(leaf1, leaf2), branch2(leaf3), leaf4)
```

### Real-World Example: File System
```typescript
interface FileSystemComponent {
  getName(): string;
  getSize(): number;
  print(indent: string): void;
}

class File implements FileSystemComponent {
  constructor(private name: string, private size: number) {}

  getName(): string {
    return this.name;
  }

  getSize(): number {
    return this.size;
  }

  print(indent: string): void {
    console.log(`${indent}📄 ${this.name} (${this.size} bytes)`);
  }
}

class Directory implements FileSystemComponent {
  private children: FileSystemComponent[] = [];

  constructor(private name: string) {}

  add(component: FileSystemComponent): void {
    this.children.push(component);
  }

  getName(): string {
    return this.name;
  }

  getSize(): number {
    return this.children.reduce((sum, child) => sum + child.getSize(), 0);
  }

  print(indent: string): void {
    console.log(`${indent}📁 ${this.name} (${this.getSize()} bytes)`);
    this.children.forEach(child => child.print(indent + '  '));
  }
}

// Usage
const root = new Directory('root');
const home = new Directory('home');
home.add(new File('photo.jpg', 2048));
home.add(new File('document.pdf', 4096));

const work = new Directory('work');
work.add(new File('report.docx', 8192));

root.add(home);
root.add(work);
root.print('');
```

### Detection Markers
- Tree structure with uniform interface
- Collection of children components
- `add()`, `remove()`, `getChild()` methods
- Recursive operation calls

### Code Smells It Fixes
- **Type checking for composition vs leaf**: Uniform interface eliminates `instanceof` checks
- **Different handling for parts vs wholes**: Clients treat both uniformly

### Common Mistakes
- **Violating uniformity**: Leaf and Composite should have same interface
- **Incorrect child management**: Not handling removal properly
- **Deep recursion**: Can cause stack overflow on very deep trees

---

## Decorator

### Definition
Attaches additional responsibilities to an object dynamically, providing a flexible alternative to subclassing for extending functionality.

### When to Use
- [x] Need to add responsibilities to objects dynamically and transparently
- [x] Responsibilities can be withdrawn
- [x] Extension by subclassing is impractical (many possible combinations)
- [x] Want to add features incrementally

### TypeScript Signature
```typescript
// Component interface
interface Component {
  operation(): string;
}

// Concrete component
class ConcreteComponent implements Component {
  operation(): string {
    return 'ConcreteComponent';
  }
}

// Base decorator
abstract class Decorator implements Component {
  constructor(protected component: Component) {}

  operation(): string {
    return this.component.operation();
  }
}

// Concrete decorators
class DecoratorA extends Decorator {
  operation(): string {
    return `DecoratorA(${super.operation()})`;
  }
}

class DecoratorB extends Decorator {
  operation(): string {
    return `DecoratorB(${super.operation()})`;
  }
}

// Usage: Stack decorators
const simple = new ConcreteComponent();
const decorated1 = new DecoratorA(simple);
const decorated2 = new DecoratorB(decorated1);
console.log(decorated2.operation());
// Output: DecoratorB(DecoratorA(ConcreteComponent))
```

### Stack-Native Alternatives

**React - Higher-Order Components**:
```typescript
// HOC decorator
function withAuth<P extends object>(
  Component: React.ComponentType<P>
): React.ComponentType<P> {
  return (props: P) => {
    const { user } = useAuth();
    if (!user) return <Redirect to="/login" />;
    return <Component {...props} />;
  };
}

// Usage: Stack decorators
const AuthenticatedProfile = withAuth(Profile);
const AuthenticatedAdminProfile = withLogging(withAuth(Profile));
```

**NestJS - Interceptors**:
```typescript
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    console.log('Before...');
    return next.handle().pipe(
      tap(() => console.log('After...'))
    );
  }
}

// Apply decorator
@UseInterceptors(LoggingInterceptor)
@Controller('users')
export class UsersController {}
```

### Detection Markers
- Implements same interface as wrapped object
- Holds reference to wrapped object
- Delegates to wrapped, adding behavior
- Can be stacked

### Code Smells It Fixes
- **Class explosion**: Avoid creating subclass for every feature combination
- **Rigid feature addition**: Add/remove features dynamically

### Common Mistakes
- **Order dependency**: DecoratorA(DecoratorB(x)) ≠ DecoratorB(DecoratorA(x))
- **Decorator explosion**: Too many small decorators can be hard to manage
- **Breaking interface**: Decorator must maintain interface contract

---

## Facade

### Definition
Provides a unified interface to a set of interfaces in a subsystem, making the subsystem easier to use.

### When to Use
- [x] Want to provide a simple interface to a complex subsystem
- [x] Many dependencies exist between clients and implementation classes
- [x] Want to layer subsystems
- [x] Need to decouple subsystem from clients

### TypeScript Signature
```typescript
// Complex subsystem classes
class SubsystemA {
  operationA(): string {
    return 'SubsystemA';
  }
}

class SubsystemB {
  operationB(): string {
    return 'SubsystemB';
  }
}

class SubsystemC {
  operationC(): string {
    return 'SubsystemC';
  }
}

// Facade
class Facade {
  private subsystemA: SubsystemA;
  private subsystemB: SubsystemB;
  private subsystemC: SubsystemC;

  constructor() {
    this.subsystemA = new SubsystemA();
    this.subsystemB = new SubsystemB();
    this.subsystemC = new SubsystemC();
  }

  // Simplified interface
  public simpleOperation(): string {
    const resultA = this.subsystemA.operationA();
    const resultB = this.subsystemB.operationB();
    const resultC = this.subsystemC.operationC();
    return `Facade coordinates: ${resultA}, ${resultB}, ${resultC}`;
  }
}

// Client code
const facade = new Facade();
console.log(facade.simpleOperation());
// Instead of:
// const a = new SubsystemA(); const b = new SubsystemB(); const c = new SubsystemC();
// a.operationA(); b.operationB(); c.operationC();
```

### Real-World Example: Payment Processing
```typescript
// Complex subsystems
class PaymentValidator {
  validate(amount: number, card: string): boolean {
    // Complex validation logic
    return amount > 0 && card.length === 16;
  }
}

class PaymentGateway {
  charge(amount: number, card: string): string {
    return `Charged $${amount} to ${card}`;
  }
}

class NotificationService {
  sendReceipt(email: string, transactionId: string): void {
    console.log(`Receipt sent to ${email}: ${transactionId}`);
  }
}

class TransactionLogger {
  log(transaction: string): void {
    console.log(`Logged: ${transaction}`);
  }
}

// Facade
class PaymentFacade {
  private validator = new PaymentValidator();
  private gateway = new PaymentGateway();
  private notifications = new NotificationService();
  private logger = new TransactionLogger();

  processPayment(amount: number, card: string, email: string): boolean {
    // Simplified interface for complex process
    if (!this.validator.validate(amount, card)) {
      return false;
    }

    const result = this.gateway.charge(amount, card);
    this.logger.log(result);
    this.notifications.sendReceipt(email, result);
    return true;
  }
}

// Client code (simple!)
const payment = new PaymentFacade();
payment.processPayment(100, '1234567890123456', 'user@example.com');
```

### Detection Markers
- Class with multiple subsystem dependencies
- Simple public methods coordinating subsystems
- Named `*Facade`, `*API`, `*Service`

### Code Smells It Fixes
- **Complex subsystem usage**: Clients don't need to know subsystem details
- **Tight coupling**: Clients depend on facade, not many classes

### Common Mistakes
- **God Facade**: Facade does too much; should coordinate, not contain logic
- **Leaky abstraction**: Exposing subsystem details defeats the purpose

---

## Flyweight

### Definition
Uses sharing to support large numbers of fine-grained objects efficiently by storing shared state externally.

### When to Use
- [x] Application uses large number of objects
- [x] Storage cost is high due to object quantity
- [x] Most object state can be made extrinsic (externalized)
- [x] Many groups of objects may be replaced by relatively few shared objects

### TypeScript Signature
```typescript
// Flyweight
class Flyweight {
  constructor(private sharedState: string) {}

  operation(uniqueState: string): void {
    console.log(`Flyweight: Shared (${this.sharedState}) and unique (${uniqueState}) state.`);
  }
}

// Flyweight factory
class FlyweightFactory {
  private flyweights: Map<string, Flyweight> = new Map();

  constructor(initialFlyweights: string[][]) {
    for (const state of initialFlyweights) {
      this.flyweights.set(this.getKey(state), new Flyweight(state.join('_')));
    }
  }

  private getKey(state: string[]): string {
    return state.join('_');
  }

  getFlyweight(sharedState: string[]): Flyweight {
    const key = this.getKey(sharedState);

    if (!this.flyweights.has(key)) {
      console.log('Creating new flyweight');
      this.flyweights.set(key, new Flyweight(key));
    } else {
      console.log('Reusing existing flyweight');
    }

    return this.flyweights.get(key)!;
  }

  listFlyweights(): void {
    console.log(`FlyweightFactory: ${this.flyweights.size} flyweights:`);
    for (const key of this.flyweights.keys()) {
      console.log(key);
    }
  }
}

// Usage
const factory = new FlyweightFactory([
  ['Chevrolet', 'Camaro2018', 'pink'],
  ['Mercedes Benz', 'C300', 'black'],
]);

const flyweight1 = factory.getFlyweight(['Chevrolet', 'Camaro2018', 'pink']);
flyweight1.operation('license-123');

const flyweight2 = factory.getFlyweight(['Chevrolet', 'Camaro2018', 'pink']);
flyweight2.operation('license-456'); // Reuses same flyweight
```

### Real-World Example: Text Editor Characters
```typescript
// Flyweight: Character formatting (shared)
class CharacterFormat {
  constructor(
    public font: string,
    public size: number,
    public color: string
  ) {}
}

// Flyweight factory
class FormatFactory {
  private formats = new Map<string, CharacterFormat>();

  getFormat(font: string, size: number, color: string): CharacterFormat {
    const key = `${font}_${size}_${color}`;
    if (!this.formats.has(key)) {
      this.formats.set(key, new CharacterFormat(font, size, color));
    }
    return this.formats.get(key)!;
  }
}

// Character with extrinsic state
class Character {
  constructor(
    private char: string,
    private format: CharacterFormat // Shared flyweight
  ) {}

  render(position: number): string {
    return `'${this.char}' at ${position} (${this.format.font}, ${this.format.size}px, ${this.format.color})`;
  }
}

// Document
const formatFactory = new FormatFactory();
const arial12Black = formatFactory.getFormat('Arial', 12, 'black');
const arial12Red = formatFactory.getFormat('Arial', 12, 'red');

// 10,000 characters, but only 2 format objects
const characters: Character[] = [];
for (let i = 0; i < 10000; i++) {
  const format = i % 2 === 0 ? arial12Black : arial12Red;
  characters.push(new Character('A', format));
}
```

### Detection Markers
- Factory managing pool of shared objects
- Intrinsic (shared) vs extrinsic (unique) state separation
- Map/cache of flyweights

### Common Mistakes
- **Premature optimization**: Only use if memory is actually a problem
- **Incorrect state separation**: Mixing intrinsic and extrinsic state

---

## Proxy

### Definition
Provides a surrogate or placeholder for another object to control access to it.

### When to Use
- [x] Lazy initialization (virtual proxy): Create expensive object only when needed
- [x] Access control (protection proxy): Control access to original object
- [x] Local representative of remote object (remote proxy)
- [x] Logging, caching, or monitoring access

### TypeScript Signature
```typescript
// Subject interface
interface Subject {
  request(): void;
}

// Real subject
class RealSubject implements Subject {
  request(): void {
    console.log('RealSubject: Handling request');
  }
}

// Proxy
class Proxy implements Subject {
  private realSubject: RealSubject | null = null;

  request(): void {
    // Access control
    if (this.checkAccess()) {
      // Lazy initialization
      if (!this.realSubject) {
        this.realSubject = new RealSubject();
      }

      // Logging
      this.logAccess();

      // Delegate to real subject
      this.realSubject.request();
    }
  }

  private checkAccess(): boolean {
    console.log('Proxy: Checking access');
    return true;
  }

  private logAccess(): void {
    console.log('Proxy: Logging access time');
  }
}

// Usage
const proxy = new Proxy();
proxy.request();
// Output:
// Proxy: Checking access
// Proxy: Logging access time
// RealSubject: Handling request
```

### Modern JavaScript Proxy
```typescript
const target = {
  message: 'Hello',
  getValue() {
    return this.message;
  }
};

const handler = {
  get(target: any, prop: string) {
    console.log(`Accessing property: ${prop}`);
    return target[prop];
  },
  set(target: any, prop: string, value: any) {
    console.log(`Setting property: ${prop} = ${value}`);
    target[prop] = value;
    return true;
  }
};

const proxy = new Proxy(target, handler);
console.log(proxy.message); // Logs: Accessing property: message
proxy.message = 'World';     // Logs: Setting property: message = World
```

### Detection Markers
- Implements same interface as real subject
- Holds reference to real subject
- Controls access (checks, logging, caching)
- Lazy initialization of real subject

### Common Mistakes
- **Proxy chains**: Multiple proxies wrapping each other
- **Performance overhead**: Every access goes through proxy
- **Confusion with Decorator**: Proxy controls access; Decorator adds behavior

---

## Summary Table

| Pattern | Complexity | Use Frequency | Main Benefit |
|---------|------------|---------------|--------------|
| Adapter | Low | High | Interface compatibility |
| Bridge | High | Low | Decouple abstraction from implementation |
| Composite | Medium | High | Uniform tree structure handling |
| Decorator | Medium | High | Dynamic responsibility addition |
| Facade | Low | Very High | Simplified subsystem interface |
| Flyweight | High | Low | Memory optimization |
| Proxy | Medium | Medium | Controlled access |

## Best Practices

1. **Adapter vs Bridge**: Adapter fixes incompatibility; Bridge designs flexibility
2. **Decorator vs Proxy**: Decorator adds features; Proxy controls access
3. **Facade simplicity**: Should coordinate, not contain business logic
4. **Composite uniformity**: Leaf and Composite must share interface
5. **Use native Proxy**: JavaScript `Proxy` object for dynamic property access

## References

- *Design Patterns: Elements of Reusable Object-Oriented Software* (Gang of Four)
- [MDN: Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy)
- [Refactoring Guru: Structural Patterns](https://refactoring.guru/design-patterns/structural-patterns)
