# difflib (Python Standard Library)

## Overview
**Package:** `difflib` (built-in, no installation needed)
**Algorithm:** SequenceMatcher (Myers-like, based on Ratcliff-Obershelp)
**Status:** Active (maintained as part of Python stdlib)
**First Released:** Python 2.1 (2001)

## Description
The standard library module for computing differences between sequences. It provides classes and functions for comparing sequences (strings, lists, files) and generating diffs in various formats.

**Key features:**
- **SequenceMatcher**: Computes similarity ratio and matching blocks between sequences
- **Differ**: Produces human-readable line-by-line diffs
- **unified_diff / context_diff**: Generates standard diff formats (like Unix `diff`)
- **HtmlDiff**: Generates side-by-side HTML comparison tables
- **get_close_matches**: Fuzzy string matching based on similarity

## Algorithm
Uses a modified version of the **Ratcliff-Obershelp pattern recognition algorithm**, which recursively finds the longest contiguous matching subsequence. This is similar in spirit to Myers but optimized for human readability over mathematical optimality.

**Complexity:** O(n²) in worst case, but fast for typical inputs with many matches.

## Installation
```python
import difflib  # No installation needed
```

## Basic Usage

### Line-by-line diff
```python
import difflib

text1 = """Line 1
Line 2
Line 3
""".splitlines(keepends=True)

text2 = """Line 1
Line 2 modified
Line 3
Line 4
""".splitlines(keepends=True)

# Unified diff (like git diff)
diff = difflib.unified_diff(text1, text2, fromfile='original', tofile='modified')
print(''.join(diff))
```

Output:
```diff
--- original
+++ modified
@@ -1,3 +1,4 @@
 Line 1
-Line 2
+Line 2 modified
 Line 3
+Line 4
```

### Similarity ratio
```python
import difflib

s1 = "Hello, world!"
s2 = "Hello, world?"

ratio = difflib.SequenceMatcher(None, s1, s2).ratio()
print(f"Similarity: {ratio:.2%}")  # Similarity: 92.31%
```

### HTML side-by-side diff
```python
import difflib

text1_lines = ['Line 1\n', 'Line 2\n', 'Line 3\n']
text2_lines = ['Line 1\n', 'Line 2 modified\n', 'Line 3\n', 'Line 4\n']

html_diff = difflib.HtmlDiff().make_file(text1_lines, text2_lines)
# Returns full HTML page with side-by-side comparison
```

## Pros
- **Standard library**: No dependencies, always available
- **Multiple output formats**: unified, context, HTML, custom
- **Well-documented**: Extensive docs and examples
- **Proven**: 20+ years of use in production
- **Fuzzy matching**: `get_close_matches()` for similarity search

## Cons
- **Not optimal**: Doesn't implement Myers algorithm exactly (not minimal edit distance)
- **No patience diff**: Can't handle moved blocks well
- **No semantic awareness**: Line-based only, no AST/structure understanding
- **Performance**: Slower than optimized C implementations (pure Python)
- **No 3-way merge**: Can't resolve merge conflicts

## When to Use
- **Comparing text files**: Version control, file diff utilities
- **Testing**: Assert expected vs actual output with readable diffs
- **Similarity scoring**: Find closest match from a set of candidates
- **HTML reports**: Generate visual diff reports for non-technical users
- **Prototyping**: Quick diff functionality without external dependencies

## When NOT to Use
- **Large files**: Slower than C-based alternatives (consider `diff-match-patch`)
- **Code refactoring**: No semantic understanding (consider tree-sitter)
- **Merge conflicts**: No 3-way merge support (consider git libraries)
- **Performance-critical**: Pure Python is slower than native code

## Alternatives
- **diff-match-patch**: Faster, more algorithms (Google's library)
- **tree-sitter**: Semantic/structural diff for code
- **DeepDiff**: Python object diffing (nested dicts, lists)

## Popularity
- **Usage:** Extremely high (shipped with every Python installation)
- **GitHub stars:** N/A (part of CPython)
- **PyPI downloads:** N/A (stdlib)
- **Stack Overflow:** 1000+ questions tagged `python-difflib`

## Verdict
**Best for:** General-purpose text diffing when you need "good enough" results with zero dependencies. The go-to choice for simple diff needs in Python projects.

**Skip if:** You need Myers/patience diff, 3-way merge, or high performance on large files.
