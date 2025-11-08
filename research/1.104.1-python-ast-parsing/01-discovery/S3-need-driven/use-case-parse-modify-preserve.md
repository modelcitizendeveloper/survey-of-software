# Use Case: Parse-Modify-Preserve Pattern

## Pattern Definition

**Name**: Parse-Modify-Preserve

**Description**: Parse a Python source file into a manipulable structure, make targeted modifications to specific code elements, then write back to file while preserving original formatting, comments, and style.

**Parameters**:
- File size: 100-5000 lines
- Modification type: Insert new element, update existing element, delete element
- Preservation scope: Comments (inline, block, docstrings), whitespace, formatting style

**Generic Example**:
```python
# Input file with specific formatting style
class UserService:
    """Handles user operations."""

    def get_user(self, id: int) -> User:  # Primary lookup
        return self.db.query(User).get(id)

    # Modification: Insert new method after get_user
    # Requirement: Preserve comments, indentation, blank lines
```

## Requirements Specification

### Must-Have Requirements
1. **Format Preservation**: Original indentation, spacing, line breaks maintained
2. **Comment Preservation**: All comments (inline, block, docstrings) retained in correct positions
3. **Surgical Modification**: Change only target elements, leave rest untouched
4. **Syntax Correctness**: Modified output is valid Python
5. **Round-Trip Fidelity**: Parse → write (no modification) produces identical output

### Should-Have Requirements
6. **Style Preservation**: Maintain coding style (quote types, trailing commas, etc.)
7. **Import Preservation**: Keep import order and formatting
8. **Type Hint Preservation**: Maintain type annotations exactly
9. **Decorator Preservation**: Keep decorator formatting and arguments

### Nice-to-Have Requirements
10. **Diff Minimization**: Changes produce minimal diff (only modified lines)
11. **Performance**: Handle 5000-line files in < 1 second
12. **Error Recovery**: Graceful handling of minor syntax irregularities

## Library Fit Analysis

### LibCST

**Capability Assessment**:
LibCST is explicitly designed for this exact pattern. From documentation:

> "LibCST parses Python source code as a Concrete Syntax Tree (CST) that keeps all formatting details. When you modify a tree and convert it back to code, all original formatting is preserved unless you explicitly changed it."

**Evidence from Documentation**:
- Tutorial: "Preserve Comments and Formatting" shows round-trip preservation
- Example: Inserting method into class preserves all surrounding formatting
- API: `parse_module()` returns CST that maintains all tokens including whitespace

**Requirement Satisfaction**:
1. Format Preservation: **YES** - Core design goal, maintains all whitespace nodes
2. Comment Preservation: **YES** - Comments stored as part of CST
3. Surgical Modification: **YES** - `deep_replace()` and visitor pattern for targeted changes
4. Syntax Correctness: **YES** - Can validate via `parse_module()` before writing
5. Round-Trip Fidelity: **YES** - Documented guarantee: `code == parse(code).code`
6. Style Preservation: **YES** - Maintains quote types, trailing commas, etc.
7. Import Preservation: **YES** - Imports are CST nodes with full formatting
8. Type Hint Preservation: **YES** - Type annotations preserved exactly
9. Decorator Preservation: **YES** - Decorators are CST nodes with formatting
10. Diff Minimization: **YES** - Only modified nodes change
11. Performance: **YES** - Documented as "production-ready for large codebases"
12. Error Recovery: **NO** - Requires syntactically valid Python

**Fit Score**: **5/5 - Perfect Fit**

**Justification**: LibCST was explicitly designed for this pattern. All must-have and should-have requirements satisfied with documented, tested capabilities.

### Python ast Module

**Capability Assessment**:
The standard library `ast` module parses to Abstract Syntax Tree, which intentionally discards formatting information.

**Evidence from Documentation**:
> "The ast module helps Python applications to process trees of the Python abstract syntax grammar. The abstract syntax itself might change with each Python release."

**Requirement Satisfaction**:
1. Format Preservation: **NO** - AST discards all formatting information
2. Comment Preservation: **NO** - AST discards all comments
3. Surgical Modification: **PARTIAL** - Can modify tree but no preservation
4. Syntax Correctness: **YES** - Can validate structure
5. Round-Trip Fidelity: **NO** - `ast.unparse()` generates new formatting
6. Style Preservation: **NO** - Style is lost in AST
7. Import Preservation: **NO** - Import formatting lost
8. Type Hint Preservation: **PARTIAL** - Structure preserved, formatting lost
9. Decorator Preservation: **PARTIAL** - Structure preserved, formatting lost
10. Diff Minimization: **NO** - Entire file reformatted
11. Performance: **YES** - Very fast parsing
12. Error Recovery: **NO** - Requires valid Python

**Fit Score**: **1/5 - No Fit**

**Justification**: Fails critical must-have requirements (1, 2, 5). While `ast` can parse and modify code, it fundamentally cannot preserve formatting, making it unsuitable for this pattern.

### Rope

**Capability Assessment**:
Rope is a refactoring library that operates on source code text with AST understanding.

**Evidence from Documentation**:
> "Rope is a python refactoring library. It provides functionality for rename, extract method, inline, and other refactorings."

**Requirement Satisfaction**:
1. Format Preservation: **YES** - Rope performs text-based modifications
2. Comment Preservation: **YES** - Comments in untouched code preserved
3. Surgical Modification: **YES** - Refactoring operations are surgical
4. Syntax Correctness: **YES** - Validates before applying changes
5. Round-Trip Fidelity: **PARTIAL** - Some refactorings may adjust formatting
6. Style Preservation: **PARTIAL** - Depends on refactoring type
7. Import Preservation: **YES** - Import refactorings preserve or improve imports
8. Type Hint Preservation: **YES** - Type hints preserved
9. Decorator Preservation: **YES** - Decorators preserved
10. Diff Minimization: **PARTIAL** - Tries to minimize but may adjust
11. Performance: **MODERATE** - Slower than LibCST due to analysis overhead
12. Error Recovery: **LIMITED** - Some tolerance but not guaranteed

**Fit Score**: **3/5 - Adequate Fit**

**Justification**: Rope can satisfy this pattern but is designed for higher-level refactorings, not generic parse-modify-preserve. Works but not optimized for this use case. Less control than LibCST for custom modifications.

### Parso

**Capability Assessment**:
Parso is an error-tolerant parser that maintains formatting information.

**Evidence from Documentation**:
> "Parso is a Python parser that supports error recovery and round-trip parsing to preserve formatting."

**Requirement Satisfaction**:
1. Format Preservation: **YES** - Maintains all formatting in parse tree
2. Comment Preservation: **YES** - Comments preserved in tree
3. Surgical Modification: **LIMITED** - API less developed for modifications
4. Syntax Correctness: **YES** - Can validate syntax
5. Round-Trip Fidelity: **YES** - Designed for round-trip parsing
6. Style Preservation: **YES** - Maintains style information
7. Import Preservation: **YES** - Imports preserved
8. Type Hint Preservation: **YES** - Type annotations preserved
9. Decorator Preservation: **YES** - Decorators preserved
10. Diff Minimization: **YES** - Only changed nodes differ
11. Performance: **MODERATE** - Slower than ast, comparable to LibCST
12. Error Recovery: **YES** - Error-tolerant parsing

**Fit Score**: **4/5 - Good Fit**

**Justification**: Parso has the right foundation (format preservation, round-trip fidelity) but its modification API is less mature than LibCST. Can satisfy requirements but with more manual work.

## Best Fit Recommendation

**Winner**: **LibCST**

**Reasoning**:
1. **Purpose-built**: Explicitly designed for parse-modify-preserve pattern
2. **Complete API**: Rich modification APIs (visitors, matchers, transformers)
3. **Documentation**: Extensive examples of this exact use case
4. **Production-ready**: Used by large projects (Instagram, Dropbox) for codemod operations
5. **Zero gaps**: Satisfies all must-have and should-have requirements

**Runner-up**: **Parso** (for error tolerance needs)

## Gap Analysis

### LibCST Gaps
- **Error Tolerance**: Cannot parse files with syntax errors
- **Learning Curve**: CST API more complex than AST
- **Python Version**: Must match parser version to target version

### Ast Gaps (Critical)
- **Formatting Loss**: Fundamental dealbreaker for this pattern
- **Comment Loss**: Cannot preserve comments
- **No Round-Trip**: Cannot produce original code

### Rope Gaps
- **Modification Flexibility**: Limited to predefined refactorings
- **Custom Operations**: Hard to implement non-standard modifications
- **API Complexity**: Project-based API heavyweight for simple modifications

### Parso Gaps
- **Modification API**: Less developed than LibCST
- **Documentation**: Fewer examples of modification patterns
- **Community**: Smaller ecosystem than LibCST

## Edge Cases & Considerations

### Multi-Line String Modifications
**Challenge**: Preserving multi-line string formatting when modifying nearby code

**LibCST**: Handles correctly - multi-line strings are CST nodes
**Ast**: Loses original formatting
**Rope**: Preserves if not in modification scope

### Complex Decorator Chains
**Challenge**: Preserving decorator ordering and arguments

**LibCST**: Full preservation with exact formatting
**Ast**: Structure preserved, formatting lost
**Rope**: Preserved unless decorator is modification target

### Inline Comments on Modified Lines
**Challenge**: Keeping inline comments when changing the line

**LibCST**: Preserved if using node replacement (not text replacement)
**Ast**: Comments lost entirely
**Rope**: Generally preserved

## Real-World Validation

### Use Case: Codemod Tool
**Requirement**: Modify 1000+ files to update deprecated API usage

**LibCST**: **Ideal** - Designed for this (Instagram uses for codemods)
**Ast**: **Unsuitable** - Would reformat entire codebase
**Rope**: **Possible** - If refactoring matches Rope's operations

### Use Case: Auto-Generated Method Insertion
**Requirement**: Add boilerplate methods to classes

**LibCST**: **Ideal** - Precise control over insertion point and formatting
**Ast**: **Unsuitable** - Loses original formatting
**Parso**: **Good** - Can work with manual tree manipulation

## Conclusion

For the Parse-Modify-Preserve pattern, **LibCST is the clear winner** with a perfect fit score. It's the only library explicitly designed for this use case with complete requirement satisfaction and no critical gaps.

**Use ast**: Never for this pattern (formatting loss is fatal)
**Use LibCST**: Default choice for this pattern
**Use Parso**: Only if error tolerance is critical and you can build modification logic
**Use Rope**: Only if modification matches Rope's refactoring operations
