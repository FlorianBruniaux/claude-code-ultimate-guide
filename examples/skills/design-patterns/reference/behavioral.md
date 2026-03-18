---
title: "Behavioral Design Patterns"
description: "Reference for Observer, Strategy, Command, Chain of Responsibility and other behavior patterns"
tags: [reference, design-patterns, architecture]
---

# Behavioral Design Patterns

Patterns concerned with algorithms and the assignment of responsibilities between objects, focusing on communication patterns.

## Chain of Responsibility

### Definition
Passes requests along a chain of handlers, where each handler decides either to process the request or pass it to the next handler.

### When to Use
- [x] More than one object may handle a request, and handler isn't known a priori
- [x] Want to issue request without specifying receiver explicitly
- [x] Set of handlers can be specified dynamically
- [x] Processing order matters

### TypeScript Signature
```typescript
interface Handler {
  setNext(handler: Handler): Handler;
  handle(request: string): string | null;
}

abstract class AbstractHandler implements Handler {
  private nextHandler: Handler | null = null;

  setNext(handler: Handler): Handler {
    this.nextHandler = handler;
    return handler; // Allows chaining: h1.setNext(h2).setNext(h3)
  }

  handle(request: string): string | null {
    if (this.nextHandler) {
      return this.nextHandler.handle(request);
    }
    return null;
  }
}

class ConcreteHandlerA extends AbstractHandler {
  handle(request: string): string | null {
    if (request === 'A') {
      return `HandlerA processed ${request}`;
    }
    return super.handle(request);
  }
}

class ConcreteHandlerB extends AbstractHandler {
  handle(request: string): string | null {
    if (request === 'B') {
      return `HandlerB processed ${request}`;
    }
    return super.handle(request);
  }
}

// Usage
const handlerA = new ConcreteHandlerA();
const handlerB = new ConcreteHandlerB();
handlerA.setNext(handlerB);

console.log(handlerA.handle('B')); // HandlerB processed B
```

### Stack-Native Alternatives

**Express Middleware**:
```typescript
app.use(authMiddleware);
app.use(loggingMiddleware);
app.use(errorMiddleware);
```

**NestJS Guards/Interceptors**:
```typescript
@UseGuards(AuthGuard, RolesGuard)
@UseInterceptors(LoggingInterceptor)
```

### Code Smells It Fixes
- **Tight coupling to request handler**: Client doesn't know which handler processes request
- **Complex conditional logic**: Each handler has simple logic

---

## Command

### Definition
Encapsulates a request as an object, letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

### When to Use
- [x] Parameterize objects with operations
- [x] Queue, specify, and execute requests at different times
- [x] Support undo/redo operations
- [x] Log changes for system crash recovery

### TypeScript Signature
```typescript
// Command interface
interface Command {
  execute(): void;
  undo?(): void;
}

// Receiver
class Light {
  turnOn(): void {
    console.log('Light is on');
  }
  turnOff(): void {
    console.log('Light is off');
  }
}

// Concrete commands
class TurnOnCommand implements Command {
  constructor(private light: Light) {}

  execute(): void {
    this.light.turnOn();
  }

  undo(): void {
    this.light.turnOff();
  }
}

class TurnOffCommand implements Command {
  constructor(private light: Light) {}

  execute(): void {
    this.light.turnOff();
  }

  undo(): void {
    this.light.turnOn();
  }
}

// Invoker
class RemoteControl {
  private history: Command[] = [];

  execute(command: Command): void {
    command.execute();
    this.history.push(command);
  }

  undo(): void {
    const command = this.history.pop();
    if (command?.undo) {
      command.undo();
    }
  }
}

// Usage
const light = new Light();
const remote = new RemoteControl();

remote.execute(new TurnOnCommand(light));  // Light is on
remote.execute(new TurnOffCommand(light)); // Light is off
remote.undo();                             // Light is on
```

### Stack-Native: Redux Actions
```typescript
const incrementAction = { type: 'INCREMENT', payload: 1 };
dispatch(incrementAction); // Command pattern
```

---

## Iterator

### Definition
Provides a way to access elements of a collection sequentially without exposing its underlying representation.

### When to Use
- [x] Need to access collection's contents without exposing internal structure
- [x] Support multiple traversals of collections
- [x] Provide uniform interface for traversing different structures

### TypeScript Signature
```typescript
// Iterator interface
interface Iterator<T> {
  next(): { value: T; done: boolean };
  hasNext(): boolean;
}

// Iterable collection
interface Iterable<T> {
  createIterator(): Iterator<T>;
}

// Concrete iterator
class ArrayIterator<T> implements Iterator<T> {
  private position = 0;

  constructor(private collection: T[]) {}

  next(): { value: T; done: boolean } {
    if (this.position < this.collection.length) {
      return { value: this.collection[this.position++], done: false };
    }
    return { value: null as any, done: true };
  }

  hasNext(): boolean {
    return this.position < this.collection.length;
  }
}

// Collection
class NumberCollection implements Iterable<number> {
  constructor(private items: number[]) {}

  createIterator(): Iterator<number> {
    return new ArrayIterator(this.items);
  }
}
```

### JavaScript Native Support
```typescript
// Symbol.iterator
const collection = {
  items: [1, 2, 3],
  [Symbol.iterator]() {
    let index = 0;
    const items = this.items;
    return {
      next() {
        return index < items.length
          ? { value: items[index++], done: false }
          : { done: true, value: undefined };
      }
    };
  }
};

for (const item of collection) {
  console.log(item); // 1, 2, 3
}

// Generator (simpler)
function* numberGenerator() {
  yield 1;
  yield 2;
  yield 3;
}

for (const num of numberGenerator()) {
  console.log(num);
}
```

---

## Mediator

### Definition
Defines an object that encapsulates how a set of objects interact, promoting loose coupling by keeping objects from referring to each other explicitly.

### When to Use
- [x] Set of objects communicate in complex ways
- [x] Reusing object is difficult because it refers to many others
- [x] Behavior distributed between classes should be customizable without subclassing

### TypeScript Signature
```typescript
// Mediator interface
interface Mediator {
  notify(sender: object, event: string): void;
}

// Concrete mediator
class ConcreteMediator implements Mediator {
  private component1: Component1;
  private component2: Component2;

  constructor(c1: Component1, c2: Component2) {
    this.component1 = c1;
    this.component1.setMediator(this);
    this.component2 = c2;
    this.component2.setMediator(this);
  }

  notify(sender: object, event: string): void {
    if (event === 'A') {
      console.log('Mediator reacts to A and triggers:');
      this.component2.doC();
    }
    if (event === 'D') {
      console.log('Mediator reacts to D and triggers:');
      this.component1.doB();
    }
  }
}

// Base component
class BaseComponent {
  protected mediator: Mediator | null = null;

  setMediator(mediator: Mediator): void {
    this.mediator = mediator;
  }
}

// Concrete components
class Component1 extends BaseComponent {
  doA(): void {
    console.log('Component 1 does A');
    this.mediator?.notify(this, 'A');
  }

  doB(): void {
    console.log('Component 1 does B');
  }
}

class Component2 extends BaseComponent {
  doC(): void {
    console.log('Component 2 does C');
  }

  doD(): void {
    console.log('Component 2 does D');
    this.mediator?.notify(this, 'D');
  }
}

// Usage
const c1 = new Component1();
const c2 = new Component2();
const mediator = new ConcreteMediator(c1, c2);

c1.doA();
// Output:
// Component 1 does A
// Mediator reacts to A and triggers:
// Component 2 does C
```

### Stack-Native: React Context
```typescript
const ChatContext = createContext<ChatMediator>(null!);

// Mediator as context
function ChatRoom({ children }: Props) {
  const sendMessage = (from: string, to: string, msg: string) => {
    // Mediator logic
  };

  return (
    <ChatContext.Provider value={{ sendMessage }}>
      {children}
    </ChatContext.Provider>
  );
}
```

### Code Smells It Fixes
- **Complex web of interactions**: Centralized in mediator
- **God object with many responsibilities**: Mediator focuses on coordination only

---

## Memento

### Definition
Captures and externalizes an object's internal state without violating encapsulation, so the object can be restored to this state later.

### When to Use
- [x] Need to save/restore object snapshots (undo/redo)
- [x] Direct interface to state would expose implementation
- [x] Want to preserve encapsulation boundaries

### TypeScript Signature
```typescript
// Memento
class Memento {
  constructor(private state: string, private date: Date) {}

  getState(): string {
    return this.state;
  }

  getDate(): Date {
    return this.date;
  }
}

// Originator
class Editor {
  private content: string = '';

  type(text: string): void {
    this.content += text;
  }

  getContent(): string {
    return this.content;
  }

  save(): Memento {
    return new Memento(this.content, new Date());
  }

  restore(memento: Memento): void {
    this.content = memento.getState();
  }
}

// Caretaker
class History {
  private mementos: Memento[] = [];

  push(memento: Memento): void {
    this.mementos.push(memento);
  }

  pop(): Memento | undefined {
    return this.mementos.pop();
  }
}

// Usage
const editor = new Editor();
const history = new History();

editor.type('Hello ');
history.push(editor.save());

editor.type('World');
history.push(editor.save());

editor.type('!!!');
console.log(editor.getContent()); // Hello World!!!

editor.restore(history.pop()!);
console.log(editor.getContent()); // Hello World
```

### Code Smells It Fixes
- **Exposing internal state for undo**: Memento encapsulates state
- **Complex undo logic**: History manages snapshots

---

## Observer

### Definition
Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified automatically.

### When to Use
- [x] Change to one object requires changing others (unknown number)
- [x] Object should notify others without knowing who they are
- [x] Event-driven architectures
- [x] Reactive programming

### TypeScript Signature
```typescript
// Observer interface
interface Observer {
  update(subject: Subject): void;
}

// Subject
interface Subject {
  attach(observer: Observer): void;
  detach(observer: Observer): void;
  notify(): void;
}

// Concrete subject
class ConcreteSubject implements Subject {
  private observers: Observer[] = [];
  private state: number = 0;

  attach(observer: Observer): void {
    if (!this.observers.includes(observer)) {
      this.observers.push(observer);
    }
  }

  detach(observer: Observer): void {
    const index = this.observers.indexOf(observer);
    if (index !== -1) {
      this.observers.splice(index, 1);
    }
  }

  notify(): void {
    for (const observer of this.observers) {
      observer.update(this);
    }
  }

  setState(state: number): void {
    this.state = state;
    this.notify();
  }

  getState(): number {
    return this.state;
  }
}

// Concrete observers
class ConcreteObserverA implements Observer {
  update(subject: ConcreteSubject): void {
    console.log(`ObserverA: State is now ${subject.getState()}`);
  }
}

class ConcreteObserverB implements Observer {
  update(subject: ConcreteSubject): void {
    console.log(`ObserverB: State is now ${subject.getState()}`);
  }
}

// Usage
const subject = new ConcreteSubject();
const observerA = new ConcreteObserverA();
const observerB = new ConcreteObserverB();

subject.attach(observerA);
subject.attach(observerB);

subject.setState(5);
// Output:
// ObserverA: State is now 5
// ObserverB: State is now 5
```

### Stack-Native Alternatives

**React**:
```typescript
const [value, setValue] = useState(0);
useEffect(() => {
  // Auto-notified on value change
}, [value]);
```

**RxJS**:
```typescript
const subject = new BehaviorSubject(0);
subject.subscribe(value => console.log(value));
subject.next(5); // Notifies subscribers
```

**Angular**:
```typescript
private data$ = new BehaviorSubject<Data>(initial);
getData() { return this.data$.asObservable(); }
```

### Code Smells It Fixes
- **Scattered notification logic**: Centralized in subject
- **Tight coupling**: Observers don't know about each other

### Common Mistakes
- **Memory leaks**: Forgetting to unsubscribe/detach
- **Notification storms**: Too many updates triggering cascades
- **Order dependency**: Observers should be independent

---

## State

### Definition
Allows an object to alter its behavior when its internal state changes, appearing to change its class.

### When to Use
- [x] Object behavior depends on its state
- [x] Operations have large conditional statements that depend on state
- [x] State transitions are well-defined

### TypeScript Signature
```typescript
// State interface
interface State {
  handle(context: Context): void;
}

// Context
class Context {
  private state: State;

  constructor(initialState: State) {
    this.state = initialState;
  }

  setState(state: State): void {
    console.log(`Context: Transitioning to ${state.constructor.name}`);
    this.state = state;
  }

  request(): void {
    this.state.handle(this);
  }
}

// Concrete states
class ConcreteStateA implements State {
  handle(context: Context): void {
    console.log('StateA handles request');
    context.setState(new ConcreteStateB());
  }
}

class ConcreteStateB implements State {
  handle(context: Context): void {
    console.log('StateB handles request');
    context.setState(new ConcreteStateA());
  }
}

// Usage
const context = new Context(new ConcreteStateA());
context.request(); // StateA handles request, transitions to StateB
context.request(); // StateB handles request, transitions to StateA
```

### Real-World: Document States
```typescript
interface DocumentState {
  publish(doc: Document): void;
  review(doc: Document): void;
}

class Draft implements DocumentState {
  publish(doc: Document): void {
    console.log('Cannot publish draft directly');
  }
  review(doc: Document): void {
    console.log('Sending for review');
    doc.setState(new InReview());
  }
}

class InReview implements DocumentState {
  publish(doc: Document): void {
    console.log('Publishing document');
    doc.setState(new Published());
  }
  review(doc: Document): void {
    console.log('Already in review');
  }
}

class Published implements DocumentState {
  publish(doc: Document): void {
    console.log('Already published');
  }
  review(doc: Document): void {
    console.log('Cannot review published document');
  }
}

class Document {
  private state: DocumentState = new Draft();

  setState(state: DocumentState): void {
    this.state = state;
  }

  publish(): void {
    this.state.publish(this);
  }

  review(): void {
    this.state.review(this);
  }
}
```

### Stack-Native: React useReducer
```typescript
const reducer = (state: State, action: Action) => {
  switch (action.type) {
    case 'DRAFT': return { status: 'draft' };
    case 'REVIEW': return { status: 'review' };
    case 'PUBLISHED': return { status: 'published' };
  }
};

const [state, dispatch] = useReducer(reducer, { status: 'draft' });
```

### Code Smells It Fixes
- **Complex conditionals on state**: Each state is a separate class
- **Scattered state-dependent behavior**: Localized in state classes

---

## Strategy

### Definition
Defines a family of algorithms, encapsulates each one, and makes them interchangeable, letting the algorithm vary independently from clients.

### When to Use
- [x] Many related classes differ only in behavior
- [x] Need different variants of an algorithm
- [x] Algorithm uses data clients shouldn't know about
- [x] Class has multiple conditional statements for selecting behavior

### TypeScript Signature
```typescript
// Strategy interface
interface Strategy {
  execute(a: number, b: number): number;
}

// Concrete strategies
class AddStrategy implements Strategy {
  execute(a: number, b: number): number {
    return a + b;
  }
}

class MultiplyStrategy implements Strategy {
  execute(a: number, b: number): number {
    return a * b;
  }
}

// Context
class Calculator {
  constructor(private strategy: Strategy) {}

  setStrategy(strategy: Strategy): void {
    this.strategy = strategy;
  }

  calculate(a: number, b: number): number {
    return this.strategy.execute(a, b);
  }
}

// Usage
const calculator = new Calculator(new AddStrategy());
console.log(calculator.calculate(5, 3)); // 8

calculator.setStrategy(new MultiplyStrategy());
console.log(calculator.calculate(5, 3)); // 15
```

### Stack-Native: React Hooks
```typescript
// Strategies as hooks
const useCreditPayment = () => ({ process: async (amount) => { /* ... */ } });
const usePaypalPayment = () => ({ process: async (amount) => { /* ... */ } });

const usePaymentStrategy = (type: PaymentType) => {
  const strategies = {
    credit: useCreditPayment(),
    paypal: usePaypalPayment(),
  };
  return strategies[type];
};

// Usage in component
const PaymentForm = ({ type }: Props) => {
  const strategy = usePaymentStrategy(type);
  const handlePay = () => strategy.process(amount);
};
```

### Code Smells It Fixes
- **Switch on type**: `switch (type) { case 'A': ... case 'B': ... }`
  → Replace with strategy selection
- **Hardcoded algorithms**: Strategies are interchangeable

### Common Mistakes
- **Strategy explosion**: Too many small strategies
- **Client awareness**: Client shouldn't know strategy details

---

## Template Method

### Definition
Defines the skeleton of an algorithm in a method, deferring some steps to subclasses, letting subclasses redefine certain steps without changing structure.

### When to Use
- [x] Implement invariant parts of algorithm once, leave varying parts to subclasses
- [x] Common behavior among subclasses should be factored and localized
- [x] Control subclass extensions (hook operations)

### TypeScript Signature
```typescript
abstract class AbstractClass {
  // Template method
  templateMethod(): void {
    this.baseOperation1();
    this.requiredOperation1();
    this.baseOperation2();
    this.hook();
    this.requiredOperation2();
  }

  // Implemented operations
  baseOperation1(): void {
    console.log('AbstractClass: base operation 1');
  }

  baseOperation2(): void {
    console.log('AbstractClass: base operation 2');
  }

  // Must be implemented by subclasses
  abstract requiredOperation1(): void;
  abstract requiredOperation2(): void;

  // Hook (optional override)
  hook(): void {
    // Default empty implementation
  }
}

class ConcreteClassA extends AbstractClass {
  requiredOperation1(): void {
    console.log('ConcreteClassA: operation 1');
  }

  requiredOperation2(): void {
    console.log('ConcreteClassA: operation 2');
  }

  hook(): void {
    console.log('ConcreteClassA: hook override');
  }
}

class ConcreteClassB extends AbstractClass {
  requiredOperation1(): void {
    console.log('ConcreteClassB: operation 1');
  }

  requiredOperation2(): void {
    console.log('ConcreteClassB: operation 2');
  }
}

// Usage
const classA = new ConcreteClassA();
classA.templateMethod();
```

### Code Smells It Fixes
- **Duplicated algorithm structure**: Template defines common steps
- **Inconsistent step order**: Template enforces order

---

## Visitor

### Definition
Represents an operation to be performed on elements of an object structure, letting you define new operations without changing classes of elements.

### When to Use
- [x] Object structure contains many classes with differing interfaces
- [x] Many distinct operations need to be performed on objects
- [x] Object structure rarely changes but operations on it often do

### TypeScript Signature
```typescript
// Element interface
interface Element {
  accept(visitor: Visitor): void;
}

// Concrete elements
class ConcreteElementA implements Element {
  accept(visitor: Visitor): void {
    visitor.visitConcreteElementA(this);
  }

  operationA(): string {
    return 'A';
  }
}

class ConcreteElementB implements Element {
  accept(visitor: Visitor): void {
    visitor.visitConcreteElementB(this);
  }

  operationB(): string {
    return 'B';
  }
}

// Visitor interface
interface Visitor {
  visitConcreteElementA(element: ConcreteElementA): void;
  visitConcreteElementB(element: ConcreteElementB): void;
}

// Concrete visitor
class ConcreteVisitor implements Visitor {
  visitConcreteElementA(element: ConcreteElementA): void {
    console.log(`Visiting A: ${element.operationA()}`);
  }

  visitConcreteElementB(element: ConcreteElementB): void {
    console.log(`Visiting B: ${element.operationB()}`);
  }
}

// Usage
const elements: Element[] = [
  new ConcreteElementA(),
  new ConcreteElementB(),
];

const visitor = new ConcreteVisitor();
for (const element of elements) {
  element.accept(visitor);
}
```

### Code Smells It Fixes
- **Adding new operations requires modifying elements**: Visitor externalizes operations
- **Operations scattered across classes**: Visitor groups related operations

### Common Mistakes
- **Adding new element types**: Requires modifying all visitors (rigid)
- **Breaking encapsulation**: Visitor may need access to internals

---

## Interpreter

### Definition
Defines a representation for a grammar along with an interpreter that uses the representation to interpret sentences in the language.

### When to Use
- [x] Grammar is simple (for complex grammars, use parser generators)
- [x] Efficiency is not critical
- [x] Building a simple domain-specific language (DSL)

### TypeScript Signature
```typescript
// Context
class Context {
  constructor(public input: string) {}
}

// Abstract expression
interface Expression {
  interpret(context: Context): number;
}

// Terminal expression
class NumberExpression implements Expression {
  constructor(private value: number) {}

  interpret(context: Context): number {
    return this.value;
  }
}

// Non-terminal expressions
class AddExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Context): number {
    return this.left.interpret(context) + this.right.interpret(context);
  }
}

class MultiplyExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Context): number {
    return this.left.interpret(context) * this.right.interpret(context);
  }
}

// Usage: (5 + 3) * 2
const context = new Context('(5 + 3) * 2');
const expression = new MultiplyExpression(
  new AddExpression(
    new NumberExpression(5),
    new NumberExpression(3)
  ),
  new NumberExpression(2)
);

console.log(expression.interpret(context)); // 16
```

### Code Smells It Fixes
- **Complex parsing logic**: Grammar rules are explicit classes
- **Hardcoded language interpretation**: Extensible grammar

---

## Summary Table

| Pattern | Complexity | Use Frequency | Main Benefit |
|---------|------------|---------------|--------------|
| Chain of Responsibility | Medium | Medium | Decouple sender from receiver |
| Command | Medium | Medium | Parameterize, queue, undo operations |
| Iterator | Low | High | Sequential access without exposure |
| Mediator | Medium | Medium | Reduce coupling between objects |
| Memento | Medium | Low | Save/restore state |
| Observer | Low | Very High | One-to-many notifications |
| State | Medium | Medium | State-dependent behavior |
| Strategy | Low | High | Interchangeable algorithms |
| Template Method | Medium | Medium | Algorithm skeleton with variants |
| Visitor | High | Low | Operations on object structure |
| Interpreter | High | Very Low | Simple DSL interpretation |

## Best Practices

1. **Observer**: Always unsubscribe to prevent memory leaks
2. **Strategy vs State**: Strategy changes behavior externally; State changes internally
3. **Use framework patterns**: React hooks, RxJS, Redux provide these patterns
4. **Command for undo**: Store history of command objects
5. **Chain of Responsibility**: Keep handlers simple, ensure request is handled

## References

- *Design Patterns: Elements of Reusable Object-Oriented Software* (Gang of Four)
- [Refactoring Guru: Behavioral Patterns](https://refactoring.guru/design-patterns/behavioral-patterns)
- [RxJS Documentation](https://rxjs.dev/)
