---
name: generate-tests
description: Generate comprehensive tests for specified code
argument-hint: "<file_or_module> [--framework jest|vitest|pytest]"
effort: medium
when_to_use: "Use when adding test coverage for a function, module, or feature."
disable-model-invocation: true
---

# Generate tests

Generate comprehensive tests for specified code.

## Instructions

1. Read the target file(s)
2. Identify testable units (functions, classes, methods)
3. Generate tests following project conventions
4. Ensure high coverage of edge cases

## Test generation process

### 1. Analyze target
- Identify public interfaces
- Understand dependencies
- Note edge cases and boundaries

### 2. Detect test framework
Check for:
- `jest.config.js` → Jest
- `vitest.config.ts` → Vitest
- `pytest.ini` → pytest
- `mocha` in package.json → Mocha

### 3. Generate tests
Follow the detected framework conventions.

## Test categories

### Happy path
Normal expected behavior with valid input.

### Edge cases
- Empty inputs
- Null/undefined values
- Boundary values (0, -1, MAX_INT)
- Single item vs multiple items

### Error cases
- Invalid input types
- Missing required parameters
- Network/IO failures
- Timeout scenarios

### Integration points
- Database interactions
- External API calls
- File system operations

## Output format

```typescript
describe('[ComponentName]', () => {
  describe('[methodName]', () => {
    // Happy path
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      // Act
      // Assert
    });

    // Edge cases
    it('should handle empty input', () => {});
    it('should handle null values', () => {});

    // Error cases
    it('should throw when [invalid condition]', () => {});
  });
});
```

## Conventions

- One assertion per test (when practical)
- Descriptive test names
- AAA pattern (Arrange-Act-Assert)
- No test interdependence
- Mock external dependencies

## Usage

```
/generate-tests src/utils/calculator.ts
/generate-tests src/services/
```

$ARGUMENTS
