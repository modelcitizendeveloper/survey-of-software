# S2 Comprehensive Discovery - Approach

## Goal

Deep analysis of text diff libraries with:
- Detailed feature comparison matrices
- Performance benchmarks (speed, memory)
- Accuracy testing (minimal edit distance vs readability)
- Integration pattern analysis
- Edge case handling (unicode, large files, binary data)

## Evaluation Framework

### 1. Feature Completeness Matrix

**Line-based diff libraries** (difflib, diff-match-patch, GitPython):
- Algorithms supported (Myers, patience, histogram)
- Output formats (unified, context, HTML)
- Patch generation/application
- Three-way merge support
- Incremental/streaming diff
- Character vs word vs line granularity
- Semantic cleanup (merge trivial edits)

**Semantic diff libraries** (tree-sitter):
- Language support (via grammars)
- Parse tree construction
- Query language for pattern matching
- Incremental parsing
- Error recovery (incomplete code)
- Integration with diff tools

**Object diff libraries** (DeepDiff):
- Data types supported (dict, list, set, custom classes)
- Type change detection
- Ignore rules (paths, regex, types)
- Delta generation/application
- JSON serialization
- Custom comparison operators

**Format-specific** (jsondiff, xmldiff):
- Format understanding (JSON Patch RFC, XML XUpdate)
- Tree structure awareness
- Attribute handling
- Namespace support
- Normalization (whitespace, order)

**Parsing/metrics** (unidiff, python-Levenshtein):
- Input format support
- Metadata extraction
- Edit operations enumeration
- Distance metrics (Levenshtein, Jaro-Winkler, Hamming)

### 2. Performance Benchmarks

**Test datasets**:
- Small (1KB): Individual functions, short files
- Medium (10KB): Typical Python module
- Large (100KB): Large source file
- Very large (1MB+): Concatenated logs, documentation

**Diff scenarios**:
- Minor edit: Change 1 line in 100
- Major edit: Change 50% of lines
- Insert/delete: Add or remove blocks
- Move: Reorder functions/classes
- Whitespace: Formatting changes only
- Rename: Identifier changes (semantic diff)

**Metrics**:
- Diff generation time (ms)
- Patch application time (ms)
- Memory usage (MB)
- Output size (bytes)
- Quality: edit distance vs human readability

**Comparison**:
- difflib vs diff-match-patch (Python vs optimized)
- Myers vs patience (Git via GitPython)
- Line diff vs semantic diff (traditional vs tree-sitter)
- Pure Python vs C extensions (difflib vs python-Levenshtein)

### 3. Accuracy Testing

**Minimal edit distance** vs **human readability**:
```python
# Example: Sorting imports
before = "import b\nimport a"
after = "import a\nimport b"

# Myers: delete 2 lines, add 2 lines (D=4)
# Patience: recognize move, show reordering (D=2)
# Which is more "accurate"?
```

**Test cases**:
- Moved blocks: Functions reordered
- Refactorings: Rename, extract method
- Whitespace changes: Indentation, formatting
- Comment changes: Added/removed/modified
- Import sorting: Alphabetized imports
- Code folding: Extract variable, inline function

**Metrics**:
- Edit distance (optimal?)
- Human annotation: "Is this diff helpful?" (1-5 scale)
- False positives: Noise (irrelevant changes shown)
- False negatives: Signal (relevant changes hidden)

### 4. Edge Case Analysis

**Unicode**:
- Non-ASCII characters (Chinese, emoji)
- Combining characters (é vs e + ´)
- Bidirectional text (Arabic, Hebrew)
- Zero-width characters
- Normalization (NFC vs NFD)

**Large files**:
- Does it complete in reasonable time?
- Memory usage scaling
- Incremental/streaming support
- Deadline-based execution (timeout)

**Binary data**:
- Does it detect binary? Graceful failure?
- Mixed text/binary files
- Line endings (CRLF vs LF vs CR)
- Null bytes, control characters

**Pathological inputs**:
- Completely different files (D ≈ N)
- One-character-per-line files
- Very long lines (>10k chars)
- Deeply nested structures (for object diff)
- Circular references (for object diff)

**Merge conflicts**:
- Conflicting edits to same line
- Nearby edits (context overlap)
- Moved code with edits
- Three-way merge base selection

### 5. Integration Patterns

How libraries work together:

```python
# Pattern 1: Git diff → unidiff parser → analysis
GitPython.git.diff() → unidiff.PatchSet() → analyze()

# Pattern 2: Generate with difflib → parse with unidiff
difflib.unified_diff() → unidiff.PatchSet() → filter()

# Pattern 3: Diff objects → serialize with DeepDiff
DeepDiff(obj1, obj2) → Delta() → JSON export

# Pattern 4: Parse with tree-sitter → custom tree diff
tree_sitter.parse() → custom_tree_diff() → semantic changes

# Pattern 5: Fuzzy match → precise diff
python_Levenshtein.get_close_matches() → difflib.unified_diff()
```

**Questions**:
- Can unidiff parse all diff-match-patch output? (No - different format)
- Can DeepDiff diff file contents as strings? (Yes, but specialized tools better)
- Can tree-sitter diff work with partial parses? (Yes, error recovery)
- Best pipeline for code review? (GitPython patience → unidiff → semantic layer)

### 6. API Usability Analysis

**Criteria**:
- Learning curve: Time to first working code
- Documentation: Examples, edge cases, API reference
- Error messages: Helpful vs cryptic
- Type hints: Static typing support
- Consistency: Similar operations have similar APIs
- Discoverability: Can you find what you need?

**Comparison**:
- difflib: Verbose but explicit
- diff-match-patch: Lots of options, steeper curve
- GitPython: Mirrors git CLI (familiar if you know git)
- DeepDiff: Intuitive for Python developers
- tree-sitter: Complex (parsing library, not just diff)

## Deliverables

1. **Feature Comparison Matrix**: Comprehensive capability table
2. **Performance Benchmarks**: Speed/memory on realistic datasets
3. **Accuracy Report**: Edit distance vs readability trade-offs
4. **Edge Case Catalog**: Pass/fail for each library
5. **Integration Guide**: Best practices for combining libraries
6. **API Usability Analysis**: Learning curve, documentation quality

## Benchmark Methodology

### Performance Testing
```python
import time
import psutil
import difflib

def benchmark_diff(text1, text2, library_fn):
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024 / 1024  # MB

    start = time.perf_counter()
    diff_result = library_fn(text1, text2)
    elapsed = (time.perf_counter() - start) * 1000  # ms

    mem_after = process.memory_info().rss / 1024 / 1024
    mem_delta = mem_after - mem_before

    return {
        'time_ms': elapsed,
        'memory_mb': mem_delta,
        'output_size': len(str(diff_result))
    }

# Test difflib
result = benchmark_diff(
    text1_lines, text2_lines,
    lambda a, b: list(difflib.unified_diff(a, b))
)
```

### Accuracy Testing
```python
# Human-annotated test cases
test_cases = [
    {
        'before': "def foo():\n    return 1",
        'after': "def bar():\n    return 1",
        'type': 'rename',
        'expected_quality': 'high',  # Should show as rename
    },
    {
        'before': "import b\nimport a",
        'after': "import a\nimport b",
        'type': 'reorder',
        'expected_quality': 'high',  # Should show as move
    },
]

for test in test_cases:
    diff = generate_diff(test['before'], test['after'])
    # Human evaluation: does diff match expected_quality?
```

## Test Datasets

### Real-World Sources
- **Python stdlib**: Changes between Python versions
- **Linux kernel**: C code with massive diffs
- **React source**: JavaScript with refactorings
- **Documentation**: Markdown, prose edits
- **Configuration**: JSON, YAML, XML changes

### Synthetic Tests
- **Minimal pairs**: Differ in one aspect only
- **Pathological**: Worst-case for algorithms
- **Graduated complexity**: 10 lines → 100 → 1000 → 10000
- **Graduated change**: 1% → 10% → 50% → 100% different

## Success Criteria

**S2 is complete when we have**:
1. Feature matrix comparing all 9 libraries
2. Benchmark results on 4 file sizes × 5 edit scenarios
3. Accuracy evaluation on 20+ annotated test cases
4. Edge case catalog with pass/fail ratings
5. Integration patterns with code examples
6. API usability scoring

## Next Steps

1. Create detailed feature comparison matrix
2. Set up benchmark harness with real datasets
3. Run performance tests (speed, memory)
4. Evaluate accuracy (edit distance vs readability)
5. Test edge cases (unicode, large files, binary)
6. Document integration patterns
7. Synthesize findings and update recommendations
