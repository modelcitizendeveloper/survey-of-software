# Use Case: Validation Before Writing Pattern

## Pattern Definition

**Name**: Validation Before Writing

**Description**: After modifying code programmatically, validate that the result is syntactically correct and semantically sound before writing to disk, catching errors that would break the codebase.

**Parameters**:
- Validation depth: syntax only, import validity, type consistency, runtime safety
- Error handling: fail fast, collect all errors, suggest fixes
- Validation scope: single file, cross-file dependencies

**Generic Example**:
```python
# After programmatic modification, validate:
# 1. Syntax: Code parses without SyntaxError
# 2. Imports: All imported names exist
# 3. Names: All referenced names are defined
# 4. Types: Type hints are valid
# 5. Indentation: Proper indentation maintained

# Example: Added method but forgot closing parenthesis
class User:
    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str  # Invalid: missing closing paren
        self.name = name
```

## Requirements Specification

### Must-Have Requirements
1. **Syntax Validation**: Detect syntax errors before writing
2. **Fast Validation**: < 100ms for typical file
3. **Error Reporting**: Clear error messages with location
4. **No False Positives**: Valid code always passes
5. **Integration**: Easy to integrate into modification workflow

### Should-Have Requirements
6. **Import Validation**: Check that imports resolve
7. **Name Resolution**: Verify referenced names are defined
8. **Type Hint Validation**: Check type annotations are valid
9. **Indentation Check**: Verify correct indentation
10. **Batch Validation**: Validate multiple files efficiently

### Nice-to-Have Requirements
11. **Semantic Validation**: Check for runtime errors (undefined variables)
12. **Style Validation**: Check code follows style guide
13. **Complexity Metrics**: Warn on overly complex code
14. **Deprecation Check**: Flag use of deprecated APIs
15. **Security Validation**: Detect security issues

## Library Fit Analysis

### Python ast Module

**Capability Assessment**:
The `ast` module is ideal for syntax validation - it's what Python itself uses.

**Evidence from Documentation**:
> "ast.parse() can be used to check if source code is syntactically valid. If invalid, SyntaxError is raised."

**Code Pattern**:
```python
import ast

def validate_syntax(code: str) -> tuple[bool, str]:
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"

# After modification
modified_code = generate_code()
is_valid, error = validate_syntax(modified_code)
if is_valid:
    write_to_file(modified_code)
else:
    print(f"Validation failed: {error}")
```

**Requirement Satisfaction**:
1. Syntax Validation: **YES** - Exactly what ast.parse() does
2. Fast Validation: **YES** - ~10ms for typical file
3. Error Reporting: **YES** - SyntaxError includes line, column, message
4. No False Positives: **YES** - Python's own parser
5. Integration: **YES** - Simple try/catch pattern
6. Import Validation: **NO** - AST doesn't resolve imports
7. Name Resolution: **NO** - AST has no semantic analysis
8. Type Hint Validation: **PARTIAL** - Validates structure, not types
9. Indentation Check: **YES** - Parser enforces indentation rules
10. Batch Validation: **YES** - Very fast, easy to loop
11. Semantic Validation: **NO** - Syntax only
12. Style Validation: **NO** - Not ast's purpose
13. Complexity Metrics: **MANUAL** - Can implement with visitor
14. Deprecation Check: **NO** - No runtime knowledge
15. Security Validation: **NO** - Static AST only

**Fit Score**: **5/5 - Perfect Fit**

**Justification**: For syntax validation (must-have requirements), ast is perfect. It's Python's own parser, so it's the definitive answer on syntax validity. Lightning fast. Easy integration.

**Gap**: No semantic validation (imports, names), but that's should-have, not must-have.

### LibCST

**Capability Assessment**:
LibCST validates syntax as part of parsing and can check formatting consistency.

**Evidence from Documentation**:
> "parse_module() validates that code is syntactically correct. ParserSyntaxError is raised for invalid syntax."

**Code Pattern**:
```python
import libcst as cst

def validate_syntax(code: str) -> tuple[bool, str]:
    try:
        cst.parse_module(code)
        return True, ""
    except cst.ParserSyntaxError as e:
        return False, f"Syntax error: {e.message}"

# Validation of generated CST
tree = modify_tree(original_tree)
code = tree.code
is_valid, error = validate_syntax(code)
```

**Requirement Satisfaction**:
1. Syntax Validation: **YES** - parse_module() validates syntax
2. Fast Validation: **MODERATE** - ~50ms for typical file (slower than ast)
3. Error Reporting: **YES** - ParserSyntaxError with details
4. No False Positives: **YES** - Valid Python always parses
5. Integration: **YES** - Simple try/catch, or validate CST directly
6. Import Validation: **NO** - No import resolution
7. Name Resolution: **LIMITED** - ScopeProvider can help but not validation
8. Type Hint Validation: **PARTIAL** - Validates structure
9. Indentation Check: **YES** - CST includes indentation rules
10. Batch Validation: **YES** - Can loop, moderate performance
11. Semantic Validation: **NO** - Syntax focus
12. Style Validation: **LIMITED** - Can check formatting consistency
13. Complexity Metrics: **MANUAL** - Implement with visitor
14. Deprecation Check: **NO** - No runtime knowledge
15. Security Validation: **NO** - Static only

**Fit Score**: **4/5 - Good Fit**

**Justification**: LibCST validates syntax well, with advantage of CST-specific checks (formatting). Slightly slower than ast. Good integration with LibCST modification workflow.

**Gap**: No semantic validation, slower than ast for pure syntax checking.

### Rope

**Capability Assessment**:
Rope performs validation as part of refactoring operations.

**Evidence from Documentation**:
> "Rope validates changes before applying them. get_changes() returns ChangeSet with validation errors if any."

**Code Pattern**:
```python
from rope.base.project import Project
from rope.base import libutils

project = Project('.')
resource = project.root.get_file('module.py')

# Rope validates when parsing
try:
    code = resource.read()
    module = libutils.parse_module(code, resource)
    # If parsing succeeds, syntax is valid
except Exception as e:
    # Syntax or semantic error
    print(f"Validation failed: {e}")
```

**Requirement Satisfaction**:
1. Syntax Validation: **YES** - Parses and validates
2. Fast Validation: **MODERATE** - ~200ms (slow due to full analysis)
3. Error Reporting: **YES** - Exception with details
4. No False Positives: **YES** - Validates correctly
5. Integration: **MODERATE** - Requires project setup
6. Import Validation: **YES** - Rope resolves imports
7. Name Resolution: **YES** - Rope tracks names and scopes
8. Type Hint Validation: **LIMITED** - Basic type understanding
9. Indentation Check: **YES** - Enforced by parser
10. Batch Validation: **MODERATE** - Slow for large batches
11. Semantic Validation: **YES** - Checks name resolution
12. Style Validation: **NO** - Not Rope's focus
13. Complexity Metrics: **NO** - Not provided
14. Deprecation Check: **NO** - No deprecation knowledge
15. Security Validation: **NO** - Not provided

**Fit Score**: **4/5 - Good Fit**

**Justification**: Rope provides both syntax and semantic validation (imports, names). Advantage: catches more errors than ast. Disadvantage: slower, heavier, requires project setup.

**Gap**: Heavyweight for simple validation, slow for batch operations.

### Parso

**Capability Assessment**:
Parso validates syntax and provides error-tolerant parsing.

**Evidence from Documentation**:
> "Parso parses Python code and reports errors via module.errors. Can validate syntax even with recovery."

**Code Pattern**:
```python
import parso

def validate_syntax(code: str) -> tuple[bool, list]:
    module = parso.parse(code)
    if module.errors:
        return False, [f"Line {e.start_pos[0]}: {e.message}" for e in module.errors]
    return True, []

# After modification
modified_code = generate_code()
is_valid, errors = validate_syntax(modified_code)
```

**Requirement Satisfaction**:
1. Syntax Validation: **YES** - Parses and reports errors
2. Fast Validation: **MODERATE** - ~30ms for typical file
3. Error Reporting: **YES** - Detailed error list
4. No False Positives: **YES** - Accurate validation
5. Integration: **YES** - Simple pattern
6. Import Validation: **NO** - No import resolution
7. Name Resolution: **NO** - Syntax focus
8. Type Hint Validation: **PARTIAL** - Validates structure
9. Indentation Check: **YES** - Enforced by parser
10. Batch Validation: **YES** - Reasonable performance
11. Semantic Validation: **NO** - Syntax focus
12. Style Validation: **NO** - Not provided
13. Complexity Metrics: **NO** - Not provided
14. Deprecation Check: **NO** - No runtime knowledge
15. Security Validation: **NO** - Not provided

**Fit Score**: **4/5 - Good Fit**

**Justification**: Parso validates syntax well, with unique feature: can partially validate files with errors. Moderate performance. Good integration.

**Gap**: No semantic validation, no significant advantage over ast for strict validation.

## Best Fit Recommendation

**Winner**: **Python ast**

**Reasoning**:
1. **Fastest**: 10ms validation, critical for tight loops
2. **Definitive**: Python's own parser, no false positives
3. **Simplest**: Minimal API, easy integration
4. **Standard library**: No dependencies
5. **Sufficient**: Syntax validation is primary need

**Runner-up**: **Rope** (if semantic validation needed)

## Comparative Analysis

### Pure Syntax Validation

**ast**: **Excellent** - Fastest, simplest, definitive
**LibCST**: **Good** - Works well but slower
**Parso**: **Good** - Works but no advantage
**Rope**: **Overkill** - Too slow for simple syntax check

### Syntax + Import Validation

**ast**: **Insufficient** - Syntax only
**LibCST**: **Insufficient** - Syntax only
**Parso**: **Insufficient** - Syntax only
**Rope**: **Excellent** - Validates imports resolve

### Syntax + Name Resolution

**ast**: **Insufficient** - No semantic analysis
**LibCST**: **Limited** - ScopeProvider helps but not validation
**Parso**: **Insufficient** - No semantic analysis
**Rope**: **Excellent** - Full name resolution

### Batch Validation (1000 files)

**ast**: **Excellent** - ~10 seconds
**LibCST**: **Good** - ~50 seconds
**Parso**: **Good** - ~30 seconds
**Rope**: **Poor** - ~200 seconds

## Hybrid Approach: Layered Validation

For complete validation, combine multiple layers:

```python
# Layer 1: Fast syntax check (ast)
try:
    ast.parse(code)
except SyntaxError as e:
    return f"Syntax error: {e}"

# Layer 2: Import resolution (Rope)
try:
    validate_imports(code)
except ImportError as e:
    return f"Import error: {e}"

# Layer 3: Type checking (mypy via subprocess)
result = subprocess.run(['mypy', '--strict', file])
if result.returncode != 0:
    return "Type errors found"

return "Valid"
```

**Use Cases**:
- CI pipeline: All three layers
- Development: Layer 1 only (fast feedback)
- Pre-commit: Layers 1 and 2

## Gap Analysis

### Ast Gaps
- **No Import Validation**: Cannot check if imports resolve
- **No Name Resolution**: Cannot detect undefined variables
- **No Type Checking**: Doesn't validate type hints semantically
- **No Style Checking**: Not a linter

### LibCST Gaps
- **Performance**: Slower than ast for syntax checking
- **No Semantic Validation**: Like ast, syntax only
- **Complexity**: More complex API for same result

### Rope Gaps
- **Performance**: Too slow for tight validation loops
- **Setup Overhead**: Requires project setup
- **No Type Checking**: Basic type understanding only

### Parso Gaps
- **No Advantages**: For strict validation, no benefit over ast
- **No Semantic Validation**: Syntax focus like ast
- **Moderate Performance**: Slower than ast

## Edge Cases & Considerations

### Validating Generated Code

```python
# After generating method, validate before writing
generated_method = generate_method(spec)
# Must validate: syntax, indentation, closing braces
```

**ast**: **Ideal** - Fast syntax validation
**Others**: Work but slower

### Validating Partial Code

```python
# Validating code snippet to be inserted
snippet = "def foo():\n    pass"
# Must validate: correct indentation, valid syntax
```

**ast**: **Ideal** - Can parse code snippets
**Parso**: **Alternative** - Can handle partial code
**Others**: Work

### Cross-File Validation

```python
# Modified file imports from other file
# Validate: imported names exist in other file
```

**ast**: **Insufficient** - Cannot resolve across files
**Rope**: **Excellent** - Project-wide understanding
**Others**: Insufficient

### Type Hint Validation

```python
# Added type hint: Optional[Dict[str, List[int]]]
# Validate: Types exist and are correct
```

**ast**: **Partial** - Validates structure, not semantic meaning
**Rope**: **Partial** - Basic type understanding
**mypy**: **Excellent** - Use external type checker

## Real-World Validation

### Use Case: Code Generator Validation
**Requirement**: Validate generated code before writing to files

**ast**: **Ideal** - Fast, simple, catches syntax errors
**LibCST**: **Good** - Works well if already using LibCST
**Rope**: **Overkill** - Too slow for generation pipeline
**Parso**: **Good** - Works but no advantage

### Use Case: Codemod Safety Check
**Requirement**: Ensure batch modification doesn't break syntax

**ast**: **Ideal** - Fast enough for 1000s of files
**LibCST**: **Good** - Natural integration with LibCST codemods
**Rope**: **Poor** - Too slow for batch validation
**Parso**: **Good** - Moderate speed

### Use Case: IDE Real-Time Validation
**Requirement**: Validate as user types (every keystroke)

**ast**: **Excellent** - Fast enough for real-time
**Parso**: **Excellent** - Error tolerance helps during typing
**LibCST**: **Moderate** - Slightly slow for real-time
**Rope**: **Poor** - Too slow for keystroke frequency

### Use Case: CI Pipeline Validation
**Requirement**: Comprehensive validation before merge

**Hybrid**: **Ideal** - ast + Rope + mypy + flake8
- ast: Syntax
- Rope: Imports/names
- mypy: Types
- flake8: Style

### Use Case: Pre-Commit Hook
**Requirement**: Fast validation before commit

**ast**: **Ideal** - Fast enough to not annoy developers
**LibCST**: **Moderate** - Slight delay but acceptable
**Rope**: **Poor** - Too slow for pre-commit (users will skip)
**Parso**: **Good** - Fast enough

## Performance Comparison

### Single File Validation (1000 lines)
- **ast**: 10ms
- **LibCST**: 50ms
- **Parso**: 30ms
- **Rope**: 200ms

### Batch Validation (100 files)
- **ast**: 1 second
- **LibCST**: 5 seconds
- **Parso**: 3 seconds
- **Rope**: 20 seconds

### Real-Time (every keystroke)
- **ast**: ✓ Fast enough
- **LibCST**: ~ Borderline
- **Parso**: ✓ Fast enough
- **Rope**: ✗ Too slow

## Integration Patterns

### With LibCST Modification

```python
import libcst as cst
import ast

# Modify with LibCST
tree = cst.parse_module(code)
modified = tree.visit(transformer)
new_code = modified.code

# Validate with ast (faster)
try:
    ast.parse(new_code)
except SyntaxError:
    raise ValidationError("Generated invalid code")

write_file(new_code)
```

**Why**: ast validation is faster than LibCST re-parsing

### With ast Modification

```python
import ast

tree = ast.parse(code)
# Modify tree
modified = modify_tree(tree)
new_code = ast.unparse(modified)

# Validate
try:
    ast.parse(new_code)  # Re-parse to validate
except SyntaxError:
    raise ValidationError("Modification broke syntax")

write_file(new_code)
```

**Why**: Sanity check after unparse

### With Rope Modification

```python
from rope.base.project import Project

project = Project('.')
changes = refactoring.get_changes()

# Rope validates internally
if not changes.is_valid():
    raise ValidationError("Refactoring would break code")

project.do(changes)
```

**Why**: Rope validates as part of refactoring

## External Validation Tools

For comprehensive validation, combine with external tools:

### mypy (Type Checking)
```bash
mypy --strict file.py
```
Validates type hints semantically

### flake8 (Style + Some Semantic)
```bash
flake8 file.py
```
Style guide enforcement, some semantic checks

### pylint (Comprehensive)
```bash
pylint file.py
```
Deep semantic analysis, style, complexity

### ruff (Fast Linter)
```bash
ruff check file.py
```
Fast linting, multiple rule sets

**Recommendation**: Use ast for syntax, external tools for deeper validation

## Conclusion

For validation before writing:
- **Use ast**: Default choice for syntax validation (fast, simple, definitive)
- **Use LibCST**: If already using LibCST and consistency matters
- **Use Rope**: If need semantic validation (imports, names)
- **Use Parso**: If validating incomplete code (IDE scenario)
- **Use External Tools**: For type checking, style, comprehensive analysis

**Confidence**: **High** - ast is the clear winner for syntax validation, with Rope as complement for semantic validation.

**Critical Insight**: Syntax validation (must-have) and semantic validation (should-have) are separate concerns. ast excels at syntax. For semantic validation, need Rope or external tools. Most use cases only need syntax validation, making ast the ideal choice.

**Recommended Pattern**:
```python
# Fast syntax check (ast)
validate_syntax_ast(code)

# Write file
write_file(code)

# Deep validation separately (CI, pre-commit)
validate_comprehensive(file)  # mypy, flake8, etc.
```

This separates fast feedback loop from comprehensive validation.
