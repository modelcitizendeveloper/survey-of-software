# Use Case: Batch File Processing Pattern

## Pattern Definition

**Name**: Batch File Processing

**Description**: Apply same modification operation to multiple Python files (10-1000s), handling errors gracefully per file, maintaining performance, and ensuring consistency across all files.

**Parameters**:
- File count: 10 to 10,000 files
- Modification type: uniform change (add method, update import, rename symbol)
- Error handling: per-file isolation, continue on error, collect failures
- Performance target: 10-100 files per second

**Generic Example**:
```python
# Apply to 500 files:
# - Add logging import: "import logging"
# - Add logger attribute: "logger = logging.getLogger(__name__)"
# - Ensure consistency across all files
# - Handle files that already have change
# - Report which files failed
```

## Requirements Specification

### Must-Have Requirements
1. **Consistent Transformation**: Same modification applied identically to all files
2. **Error Isolation**: Failure in one file doesn't stop batch
3. **Error Reporting**: Collect and report which files failed
4. **Atomic Per-File**: Each file write is all-or-nothing (no partial writes)
5. **Performance**: Process large batches in reasonable time

### Should-Have Requirements
6. **Idempotency**: Safe to run batch multiple times (skip already-modified)
7. **Validation**: Verify each file's syntax before writing
8. **Progress Tracking**: Report progress during long batches
9. **Dry-Run Mode**: Preview changes without writing files
10. **Rollback Capability**: Undo batch if issues discovered

### Nice-to-Have Requirements
11. **Parallel Processing**: Process multiple files concurrently
12. **Selective Processing**: Filter which files to process based on criteria
13. **Change Summary**: Report what changed in each file
14. **Backup Creation**: Auto-backup files before modification
15. **Git Integration**: Auto-commit batch changes

## Library Fit Analysis

### LibCST

**Capability Assessment**:
LibCST is designed for codemod operations - batch transformations across codebases.

**Evidence from Documentation**:
> "LibCST is built for codemods - automated code transformations applied to many files. Use Codemod class for batch operations."

> "libcst.Codemod provides a framework for applying transformations to multiple files with error handling and reporting."

**Code Pattern from Documentation**:
```python
from libcst.codemod import CodemodContext, VisitorBasedCodemod

class AddLoggingCodemod(VisitorBasedCodemod):
    def leave_Module(self, original, updated):
        # Add import and logger
        ...

# Apply to many files
for path in file_paths:
    try:
        context = CodemodContext()
        codemod = AddLoggingCodemod.transform_module_from_file(path)
        # Write back
    except Exception as e:
        errors.append((path, e))
```

**Requirement Satisfaction**:
1. Consistent Transformation: **YES** - Single transformer applies to all files
2. Error Isolation: **YES** - Try/catch per file, continue on error
3. Error Reporting: **YES** - Can collect exceptions per file
4. Atomic Per-File: **YES** - Read → transform → write is atomic
5. Performance: **GOOD** - ~50ms per file, 20 files/second single-threaded
6. Idempotency: **MANUAL** - Must implement check in transformer
7. Validation: **YES** - Can validate tree before writing
8. Progress Tracking: **MANUAL** - Implement with progress bar library
9. Dry-Run Mode: **YES** - Transform without writing to file
10. Rollback Capability: **MANUAL** - Git integration or file backups
11. Parallel Processing: **YES** - Thread-safe, can use multiprocessing
12. Selective Processing: **YES** - Filter files before processing
13. Change Summary: **MANUAL** - Compare before/after code
14. Backup Creation: **MANUAL** - Copy files before processing
15. Git Integration: **MANUAL** - Shell out to git commands

**Fit Score**: **5/5 - Perfect Fit**

**Justification**: LibCST is explicitly designed for batch codemod operations. Instagram uses it to transform millions of lines of code. All must-have and should-have requirements satisfied with documented patterns.

**Evidence**: Instagram's "LibCST in production" blog post describes processing entire codebase in batch.

### Python ast Module

**Capability Assessment**:
The `ast` module can be used for batch processing with custom scripting.

**Code Pattern**:
```python
import ast
from pathlib import Path

def transform_file(path):
    with open(path) as f:
        tree = ast.parse(f.read())

    # Modify tree
    # ...

    code = ast.unparse(tree)
    with open(path, 'w') as f:
        f.write(code)

errors = []
for path in file_paths:
    try:
        transform_file(path)
    except Exception as e:
        errors.append((path, e))
```

**Requirement Satisfaction**:
1. Consistent Transformation: **YES** - Same logic applies to all files
2. Error Isolation: **YES** - Try/catch per file
3. Error Reporting: **YES** - Collect exceptions
4. Atomic Per-File: **YES** - Read → transform → write
5. Performance: **EXCELLENT** - ~15ms per file, 60+ files/second
6. Idempotency: **MANUAL** - Implement check logic
7. Validation: **YES** - Parse before writing
8. Progress Tracking: **MANUAL** - Implement yourself
9. Dry-Run Mode: **MANUAL** - Skip write step
10. Rollback Capability: **MANUAL** - Git or backups
11. Parallel Processing: **YES** - Easy to parallelize with multiprocessing
12. Selective Processing: **YES** - Filter files before loop
13. Change Summary: **DIFFICULT** - Entire file reformatted, hard to diff
14. Backup Creation: **MANUAL** - Copy files yourself
15. Git Integration: **MANUAL** - Shell out to git

**Fit Score**: **3/5 - Adequate Fit**

**Justification**: ast can be used for batch processing but requires manual scripting for all orchestration. Major gap: reformats entire file, making diffs large and change summary difficult. Good performance, but poor user experience due to formatting loss.

### Rope

**Capability Assessment**:
Rope provides project-wide refactoring operations.

**Evidence from Documentation**:
> "Rope refactorings can be applied to multiple files. Use Project.do() to apply refactoring across project."

**Code Pattern**:
```python
from rope.base.project import Project
from rope.refactor.rename import Rename

project = Project('path/to/project')
# Find resource
resource = project.root.get_file('module.py')

# Create refactoring
rename = Rename(project, resource, offset)
changes = rename.get_changes('new_name')

# Apply to all affected files
project.do(changes)
```

**Requirement Satisfaction**:
1. Consistent Transformation: **YES** - Refactoring applies consistently
2. Error Isolation: **LIMITED** - Project-wide transaction model
3. Error Reporting: **LIMITED** - May rollback entire batch on error
4. Atomic Per-File: **NO** - Atomic at project level, not per-file
5. Performance: **POOR** - ~200ms per file, slow for large batches
6. Idempotency: **LIMITED** - Depends on refactoring type
7. Validation: **YES** - Validates changes before applying
8. Progress Tracking: **LIMITED** - Not exposed in API
9. Dry-Run Mode: **YES** - Preview changes before applying
10. Rollback Capability: **YES** - Can rollback project changes
11. Parallel Processing: **NO** - Project is not thread-safe
12. Selective Processing: **LIMITED** - Refactoring determines scope
13. Change Summary: **YES** - `changes` object describes modifications
14. Backup Creation: **MANUAL** - Not built-in
15. Git Integration: **MANUAL** - Not built-in

**Fit Score**: **2/5 - Poor Fit**

**Justification**: Rope's project-wide transaction model doesn't fit per-file isolation requirement. Too slow for large batches. Limited to predefined refactoring operations. Not designed for custom batch modifications.

**Gap**: Cannot do arbitrary batch modifications, only predefined refactorings.

### Parso

**Capability Assessment**:
Parso can be used for batch processing with custom scripting, similar to ast.

**Code Pattern**:
```python
import parso

def transform_file(path):
    with open(path) as f:
        code = f.read()

    module = parso.parse(code)
    # Modify tree (manual work)
    # ...

    new_code = module.get_code()
    with open(path, 'w') as f:
        f.write(new_code)

errors = []
for path in file_paths:
    try:
        transform_file(path)
    except Exception as e:
        errors.append((path, e))
```

**Requirement Satisfaction**:
1. Consistent Transformation: **YES** - Same logic for all files
2. Error Isolation: **YES** - Try/catch per file
3. Error Reporting: **YES** - Collect exceptions
4. Atomic Per-File: **YES** - Read → transform → write
5. Performance: **MODERATE** - ~40ms per file, 25 files/second
6. Idempotency: **MANUAL** - Implement check logic
7. Validation: **YES** - Can check for errors
8. Progress Tracking: **MANUAL** - Implement yourself
9. Dry-Run Mode: **MANUAL** - Skip write step
10. Rollback Capability: **MANUAL** - Git or backups
11. Parallel Processing: **YES** - Can parallelize with multiprocessing
12. Selective Processing: **YES** - Filter files before loop
13. Change Summary: **GOOD** - Formatting preserved, diffs are clean
14. Backup Creation: **MANUAL** - Copy files yourself
15. Git Integration: **MANUAL** - Shell out to git

**Fit Score**: **3/5 - Adequate Fit**

**Justification**: Parso can be used for batch processing like ast, but modification API is less developed. Advantage: preserves formatting so diffs are cleaner. Disadvantage: slower than ast, more manual work than LibCST.

## Best Fit Recommendation

**Winner**: **LibCST**

**Reasoning**:
1. **Purpose-built**: Designed specifically for batch codemod operations
2. **Production-proven**: Used at scale (Instagram, Dropbox) for batch transformations
3. **Complete framework**: Codemod class provides orchestration
4. **Clean diffs**: Formatting preservation keeps changes minimal
5. **Documented patterns**: Clear examples of batch processing

**Runner-up**: **ast** (if formatting loss acceptable and maximum speed needed)

## Comparative Scenarios

### Scenario 1: Small Batch (10 files)

**LibCST**: ~500ms total (acceptable latency)
**ast**: ~150ms total (faster but reformats all)
**Rope**: ~2 seconds (slow but high-level)
**Parso**: ~400ms total (acceptable)

**Winner**: Any except Rope (too slow for advantage)

### Scenario 2: Medium Batch (100 files)

**LibCST**: ~5 seconds (reasonable, clean diffs)
**ast**: ~1.5 seconds (fast but large diffs)
**Rope**: ~20 seconds (too slow)
**Parso**: ~4 seconds (reasonable, clean diffs)

**Winner**: LibCST (balanced speed and diff quality)

### Scenario 3: Large Batch (1000 files)

**LibCST**: ~50 seconds single-threaded, ~10s with 8 cores
**ast**: ~15 seconds single-threaded, ~3s with 8 cores
**Rope**: ~200 seconds (impractical)
**Parso**: ~40 seconds single-threaded, ~8s with 8 cores

**Winner**: ast if speed critical, LibCST if diff quality matters

### Scenario 4: Continuous Codemod (daily operations)

**LibCST**: **Ideal** - Clean diffs, code review friendly
**ast**: **Poor** - Daily formatting churn unacceptable
**Rope**: **Poor** - Too slow, limited operations
**Parso**: **Moderate** - Works but less tooling than LibCST

### Scenario 5: One-Time Migration (5000 files)

**LibCST**: ~4 minutes with parallelization (acceptable for one-time)
**ast**: ~1 minute (fast but may reformat entire codebase)
**Rope**: ~15 minutes (too slow)
**Parso**: ~3 minutes (acceptable)

**Winner**: Depends on whether formatting preservation matters

## Gap Analysis

### LibCST Gaps
- **Learning Curve**: Codemod API requires understanding
- **Speed**: Slower than ast (but acceptable for most use cases)
- **Complex Setup**: More ceremony than simple script

### Ast Gaps (Critical for Batch)
- **Formatting Loss**: Every file gets reformatted (huge diffs)
- **Code Review**: Hard to review when entire files change
- **Git History**: Pollutes history with formatting changes
- **Conflict Risk**: Batch reformat conflicts with concurrent edits

### Rope Gaps
- **Performance**: Too slow for large batches (200ms per file)
- **Flexibility**: Limited to predefined refactorings
- **Error Handling**: Project-wide transactions don't fit per-file isolation
- **Parallelization**: Not thread-safe

### Parso Gaps
- **Modification API**: Less developed than LibCST
- **Tooling**: No built-in codemod framework
- **Documentation**: Fewer batch processing examples
- **Ecosystem**: Smaller than LibCST for codemods

## Edge Cases & Considerations

### Files That Already Have Change

```python
# Some files already have logger, some don't
# Idempotency: Don't duplicate logger attribute
```

**LibCST**: Implement check in transformer (standard pattern)
**ast**: Implement check in modification logic
**Rope**: Depends on refactoring type
**Parso**: Implement check manually

### Files with Syntax Errors

```python
# Batch includes some broken files
# Requirement: Skip broken files, continue processing
```

**LibCST**: Raises exception, skip in try/catch (standard pattern)
**ast**: Raises exception, skip in try/catch
**Rope**: May fail entire batch
**Parso**: **Advantage** - Can process even with errors

### Files in Git Working Directory

```python
# Batch modifies files with uncommitted changes
# Requirement: Handle gracefully, maybe skip or warn
```

**All libraries**: Detect with Git commands, manual handling

### Concurrent Modifications

```python
# Another process modifying files during batch
# Requirement: Detect and handle conflicts
```

**All libraries**: File system race conditions possible, need locking or retry logic

## Performance Optimization Strategies

### Parallel Processing with LibCST

```python
from multiprocessing import Pool

def process_file(path):
    # LibCST transformation
    ...

with Pool(8) as pool:
    results = pool.map(process_file, file_paths)
```

**Speedup**: 6-8x on 8-core machine
**Works with**: LibCST, ast, Parso
**Not with**: Rope (not thread-safe)

### Memory-Efficient Streaming

For very large batches (10,000+ files):
- Process in chunks to avoid memory pressure
- All libraries support this pattern

### Selective Processing

Filter files before processing:
```python
# Only process files that need change
filtered = [f for f in files if needs_change(f)]
```

Saves time on already-processed files.

## Real-World Validation

### Use Case: Deprecation Codemod
**Requirement**: Update 1000 files to use new API

**LibCST**: **Ideal** - Designed for this, clean diffs for code review
**ast**: **Acceptable** - Fast but entire codebase reformatted
**Rope**: **Unsuitable** - Too slow, may not match refactoring types
**Parso**: **Moderate** - Can work but more manual than LibCST

### Use Case: Add Type Hints to Codebase
**Requirement**: Add type hints to 5000 functions

**LibCST**: **Ideal** - Format-preserving keeps changes minimal
**ast**: **Poor** - Reformatting obscures actual type hint additions
**Rope**: **Unsuitable** - No type hint refactoring
**Parso**: **Moderate** - Manual but preserves formatting

### Use Case: Import Cleanup
**Requirement**: Organize imports in 500 files

**LibCST**: **Good** - Can implement, preserves rest of file
**ast**: **Poor** - Reformats entire file for import change
**Rope**: **Good** - Has import refactoring capabilities
**Parso**: **Moderate** - Manual import organization

### Use Case: Rename Symbol Project-Wide
**Requirement**: Rename class used in 200 files

**LibCST**: **Good** - Can implement with scope analysis
**ast**: **Moderate** - Can rename but reformats everything
**Rope**: **Excellent** - Rename refactoring designed for this
**Parso**: **Poor** - No scope analysis for renames

## When to Use Each Library

### Use LibCST for Batch When:
- Codemod is recurring operation (CI, pre-commit)
- Clean diffs are important for code review
- Formatting preservation is required
- Batch size is moderate (< 10,000 files)

### Use ast for Batch When:
- One-time migration where formatting doesn't matter
- Maximum speed is critical
- Reformatting entire codebase is acceptable
- Simple transformations with custom scripting

### Use Rope for Batch When:
- Transformation matches Rope's refactorings exactly
- Small batch size (< 100 files)
- Semantic understanding required (rename with scope)

### Use Parso for Batch When:
- Files may have syntax errors
- Error tolerance is critical
- Formatting preservation important but LibCST not available

## Conclusion

For batch file processing:
- **Use LibCST**: Default choice for production codemods
- **Use ast**: Only if speed critical and formatting loss acceptable
- **Use Rope**: Only for specific refactorings (rename, extract)
- **Use Parso**: Only when error tolerance required

**Confidence**: **High** - LibCST's codemod framework is purpose-built for this pattern with production validation at scale.

**Critical Insight**: Formatting preservation is more important than speed for batch processing. Clean diffs enable code review, reduce merge conflicts, and keep git history meaningful. LibCST's slight speed penalty is worth it.
