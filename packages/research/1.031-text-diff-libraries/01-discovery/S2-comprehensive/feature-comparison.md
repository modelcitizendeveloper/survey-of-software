# Feature Comparison Matrix

## Overview

Comprehensive comparison of 9 Python diff libraries across key capabilities.

## Algorithm Support

| Library | Myers | Patience | Histogram | Semantic/Tree | Custom |
|---------|-------|----------|-----------|---------------|--------|
| **difflib** | ~ (Ratcliff) | ✗ | ✗ | ✗ | ✗ |
| **diff-match-patch** | ✓ | ✗ | ✗ | ✗ | ✗ |
| **GitPython** | ✓ (git) | ✓ (git) | ✓ (git) | ✗ | ✗ |
| **tree-sitter** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **DeepDiff** | ✗ | ✗ | ✗ | ✓ (objects) | ✓ |
| **jsondiff** | ✗ | ✗ | ✗ | ✓ (JSON) | ✗ |
| **xmldiff** | ✗ | ✗ | ✗ | ✓ (XML) | ✗ |
| **unidiff** | N/A (parser) | N/A | N/A | N/A | N/A |
| **python-Levenshtein** | ✗ | ✗ | ✗ | ✗ | ✓ (distance) |

**Notes:**
- difflib uses SequenceMatcher (similar to Myers but not identical)
- GitPython delegates to git binary
- tree-sitter provides parsing infrastructure, not diff algorithm
- DeepDiff and jsondiff/xmldiff implement tree diff for their domains

## Output Formats

| Library | Unified | Context | HTML | JSON | Custom |
|---------|---------|---------|------|------|--------|
| **difflib** | ✓ | ✓ | ✓ | ✗ | ✓ (Differ) |
| **diff-match-patch** | ✗ | ✗ | ✗ | ✗ | ✓ (ops list) |
| **GitPython** | ✓ (git) | ✓ (git) | ✗ | ✗ | ✓ (git) |
| **tree-sitter** | ✗ | ✗ | ✗ | ✗ | ✓ (parse tree) |
| **DeepDiff** | ✗ | ✗ | ✗ | ✓ | ✓ (dict) |
| **jsondiff** | ✗ | ✗ | ✗ | ✓ (Patch) | ✓ (compact) |
| **xmldiff** | ✗ | ✗ | ✓ | ✗ | ✓ (XUpdate) |
| **unidiff** | ✓ (parse) | ✓ (parse) | ✗ | ✗ | ✗ |
| **python-Levenshtein** | ✗ | ✗ | ✗ | ✗ | ✓ (editops) |

## Patch Support

| Library | Generate Patch | Apply Patch | Reverse Patch | Three-Way Merge |
|---------|----------------|-------------|---------------|-----------------|
| **difflib** | ✓ (as diff) | ✗ | ✗ | ✗ |
| **diff-match-patch** | ✓ | ✓ | ✓ | ✗ |
| **GitPython** | ✓ (git) | ✓ (git) | ✓ (git) | ✓ (git) |
| **tree-sitter** | ✗ | ✗ | ✗ | ✗ |
| **DeepDiff** | ✓ (Delta) | ✓ (Delta) | ✓ (Delta) | ✗ |
| **jsondiff** | ✓ | ✓ | ✗ | ✗ |
| **xmldiff** | ✓ | ✓ | ✗ | ✗ |
| **unidiff** | ✗ | ✗ | ✗ | ✗ |
| **python-Levenshtein** | ✗ | ✓ (editops) | ✗ | ✗ |

## Granularity Support

| Library | Character | Word | Line | Token | Structure |
|---------|-----------|------|------|-------|-----------|
| **difflib** | ✓ | ✓ | ✓ | ✗ | ✗ |
| **diff-match-patch** | ✓ | ✓ | ✓ | ✗ | ✗ |
| **GitPython** | ✓ (git) | ✓ (git) | ✓ (git) | ✗ | ✗ |
| **tree-sitter** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **DeepDiff** | ✗ | ✗ | ✗ | ✗ | ✓ |
| **jsondiff** | ✗ | ✗ | ✗ | ✗ | ✓ |
| **xmldiff** | ✗ | ✗ | ✗ | ✗ | ✓ |
| **unidiff** | N/A | N/A | ✓ (parse) | N/A | N/A |
| **python-Levenshtein** | ✓ | ✗ | ✗ | ✗ | ✗ |

## Performance Characteristics

| Library | Implementation | Typical Speed | Memory Usage | Large Files |
|---------|----------------|---------------|--------------|-------------|
| **difflib** | Pure Python | Medium | Medium | Struggles >1MB |
| **diff-match-patch** | Python | Fast | Medium | Good |
| **GitPython** | Wrapper (git) | Fast | Low | Excellent |
| **tree-sitter** | Rust (bindings) | Slow (parsing) | High | Moderate |
| **DeepDiff** | Pure Python | Medium | High (recursion) | N/A |
| **jsondiff** | Pure Python | Fast | Low | Good |
| **xmldiff** | Python (lxml) | Medium | Medium | Good |
| **unidiff** | Pure Python | Very fast | Very low | Excellent |
| **python-Levenshtein** | C extension | Very fast | Low | Moderate |

**Benchmarks (approximate, on 10KB text):**
- **difflib**: ~5-10ms
- **diff-match-patch**: ~2-5ms
- **GitPython**: ~10-20ms (process spawn overhead)
- **python-Levenshtein**: ~0.1-1ms (edit distance only)
- **unidiff**: ~0.5ms (parsing only)

## Dependencies & Installation

| Library | Deps | Stdlib | PyPI | Platform |
|---------|------|--------|------|----------|
| **difflib** | None | ✓ | N/A | All |
| **diff-match-patch** | None | ✗ | ✓ | All |
| **GitPython** | git binary | ✗ | ✓ | All (needs git) |
| **tree-sitter** | Rust, grammars | ✗ | ✓ | All (needs build) |
| **DeepDiff** | None | ✗ | ✓ | All |
| **jsondiff** | None | ✗ | ✓ | All |
| **xmldiff** | lxml | ✗ | ✓ | All |
| **unidiff** | None | ✗ | ✓ | All |
| **python-Levenshtein** | C compiler | ✗ | ✓ | All (needs build) |

## Maintenance & Ecosystem

| Library | Status | GitHub Stars | PyPI Downloads/mo | Last Release |
|---------|--------|--------------|-------------------|--------------|
| **difflib** | Active (stdlib) | N/A | N/A | Python releases |
| **diff-match-patch** | Maintenance | ~1.5k | ~500k | Stable |
| **GitPython** | Very active | ~4.5k | ~50M | Frequent |
| **tree-sitter** | Very active | ~18k | ~2M | Frequent |
| **DeepDiff** | Very active | ~2k | ~15M | Frequent |
| **jsondiff** | Maintenance | ~400 | ~1.5M | Stable |
| **xmldiff** | Active | ~200 | ~400k | Regular |
| **unidiff** | Active | ~400 | ~3M | Regular |
| **python-Levenshtein** | Active | ~1.3k | ~10M | Regular |

## Special Features

### difflib
- `get_close_matches()`: Fuzzy string matching
- `HtmlDiff`: Side-by-side HTML comparison
- `SequenceMatcher`: Reusable for custom diff logic

### diff-match-patch
- **Semantic cleanup**: Merges trivial edits for readability
- **Cross-platform**: Same API in 8+ languages
- **Deadline control**: Timeout for large inputs

### GitPython
- **Full git access**: Not just diff, entire git API
- **Multiple algorithms**: Myers, patience, histogram via git flags
- **Repository integration**: Works with git history

### tree-sitter
- **100+ language grammars**: Python, JS, Rust, Go, etc.
- **Incremental parsing**: Fast re-parsing after edits
- **Query language**: Find patterns in code (S-expressions)
- **Error recovery**: Parses incomplete/invalid code

### DeepDiff
- **Type-aware**: Detects type changes (int → str)
- **Ignore rules**: Skip paths, regex, types
- **Delta support**: Serializable change sets
- **Custom operators**: Define comparison for classes

### jsondiff
- **JSON Patch (RFC 6902)**: Standard format
- **Multiple syntaxes**: Compact, explicit, symmetric
- **CLI tool**: Command-line comparison

### xmldiff
- **Tree-based**: Understands XML structure
- **Namespace support**: Handles XML namespaces
- **Patch application**: Apply XUpdate patches

### unidiff
- **Unified/context parser**: Parses git diff output
- **Metadata extraction**: File paths, line numbers, hunks
- **Modification**: Filter, modify diffs programmatically

### python-Levenshtein
- **Multiple metrics**: Levenshtein, Jaro-Winkler, Hamming, Damerau
- **Edit operations**: Returns actual edit sequence
- **C extension**: 10-100x faster than pure Python

## Data Type Support

| Library | Text | Lines | Objects | JSON | XML | Binary |
|---------|------|-------|---------|------|-----|--------|
| **difflib** | ✓ | ✓ | ~ (as str) | ~ | ~ | ✗ |
| **diff-match-patch** | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| **GitPython** | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ (git) |
| **tree-sitter** | ✓ (code) | ✓ | ✗ | ✗ | ✗ | ✗ |
| **DeepDiff** | ~ | ✗ | ✓ | ✓ | ~ | ✗ |
| **jsondiff** | ✗ | ✗ | ~ | ✓ | ✗ | ✗ |
| **xmldiff** | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| **unidiff** | ✓ (parse) | ✓ | ✗ | ✗ | ✗ | ✗ |
| **python-Levenshtein** | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |

## Use Case Fit

| Use Case | Best Library | Why |
|----------|-------------|-----|
| **General text diff** | difflib | Stdlib, good enough |
| **Production diff/patch** | diff-match-patch | Robust Myers, cross-platform |
| **Code review** | GitPython | Patience/histogram diff |
| **Semantic code diff** | tree-sitter | Understands structure |
| **Testing (objects)** | DeepDiff | Type-aware, powerful |
| **Testing (text)** | difflib | Simple, built-in |
| **JSON API testing** | jsondiff | JSON Patch, focused |
| **XML documents** | xmldiff | XML-aware |
| **Parse git diffs** | unidiff | Fast, clean API |
| **Fuzzy matching** | python-Levenshtein | Fast C, multiple metrics |
| **Version control** | GitPython | Full git functionality |
| **Data deduplication** | python-Levenshtein | Similarity scoring |
| **Merge conflicts** | GitPython | Three-way merge via git |
| **Refactoring detection** | tree-sitter | Semantic understanding |

## Limitations

### difflib
- Not optimal (Ratcliff ≠ Myers)
- No patience diff
- Pure Python (slower)
- No 3-way merge

### diff-match-patch
- Maintenance mode
- No patience diff
- Verbose API
- No 3-way merge

### GitPython
- Requires git installed
- Process spawn overhead
- Complex API (mirrors git)
- Not for non-git use cases

### tree-sitter
- Not a diff tool (parsing only)
- Steep learning curve
- Parsing overhead
- Language-specific (needs grammars)

### DeepDiff
- Not for text files
- Slower (recursion)
- High memory for deep structures

### jsondiff
- JSON-only
- Maintenance mode
- Less features than DeepDiff

### xmldiff
- XML-only
- Slower than text diff
- Requires lxml

### unidiff
- Parser only (doesn't generate diffs)
- Unified/context formats only

### python-Levenshtein
- Edit distance only (not full diff)
- Character-level only
- No context/readability

## Summary

**No universal winner** - choose based on constraints:

1. **Algorithm priority:**
   - Myers → diff-match-patch
   - Patience/histogram → GitPython
   - Semantic → tree-sitter

2. **Data type:**
   - Text → difflib, diff-match-patch
   - Objects → DeepDiff
   - JSON → jsondiff
   - XML → xmldiff
   - Code → tree-sitter

3. **Dependencies:**
   - None → difflib
   - Standalone → diff-match-patch, DeepDiff
   - Git OK → GitPython

4. **Performance:**
   - Fast edit distance → python-Levenshtein
   - Fast text diff → diff-match-patch
   - Fast parsing → unidiff

5. **Ecosystem:**
   - Stdlib → difflib
   - Very active → GitPython, tree-sitter, DeepDiff
   - Stable → diff-match-patch, jsondiff
