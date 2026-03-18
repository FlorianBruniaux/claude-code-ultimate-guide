---
name: generate-tests
description: "Generate comprehensive tests for specified code"
---

# Generate Tests

Generate comprehensive tests for specified code.

## Instructions

1. Read the target file(s)
2. Identify testable units (functions, classes, methods)
3. Generate tests following project conventions
4. Ensure high coverage of edge cases

## Test Generation Process

### 1. Analyze Target
- Identify public interfaces
- Understand dependencies
- Note edge cases and boundaries

### 2. Detect Test Framework
Check for:
- `jest.config.js` → Jest
- `vitest.config.ts` → Vitest
- `pytest.ini` → pytest
- `mocha` in package.json → Mocha

### 3. Generate Tests
Follow the detected framework conventions.

## Test Categories

### Happy Path
Normal expected behavior with valid input.

### Edge Cases
- Empty inputs
- Null/undefined values
- Boundary values (0, -1, MAX_INT)
- Single item vs multiple items

### Error Cases
- Invalid input types
- Missing required parameters
- Network/IO failures
- Timeout scenarios

### Integration Points
- Database interactions
- External API calls
- File system operations

## Output Format

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
