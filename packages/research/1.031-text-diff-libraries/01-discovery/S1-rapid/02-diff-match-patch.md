# diff-match-patch (Google)

## Overview
**Package:** `diff-match-patch`
**Algorithm:** Myers diff + custom optimizations
**Status:** Maintenance mode (stable, infrequent updates)
**Author:** Google (Neil Fraser)
**First Released:** 2006
**Language:** Multi-language (Python, JavaScript, C++, Java, C#, Lua, Dart)

## Description
Google's robust library for synchronizing plain text across multiple platforms. It implements the Myers diff algorithm with optimizations for performance and quality. Originally designed for Google Wave (collaborative editing), now widely used in editors, version control, and synchronization tools.

**Key features:**
- **diff**: Compute differences between two texts
- **match**: Fuzzy string matching with location
- **patch**: Apply/unapply patches to text
- **Semantic cleanup**: Improves diff readability by merging trivial edits
- **Multi-level granularity**: Character-level, word-level, line-level
- **Optimized**: Deadline-based execution (stop after X seconds for large inputs)

## Algorithm
**Myers diff** with semantic cleanup post-processing:
1. Compute optimal diff using Myers algorithm
2. Apply **semantic cleanup** to merge trivial changes (e.g., "delete space, insert space" → "no change")
3. Optionally shift diff boundaries to word/line edges for readability

**Complexity:** O(ND) where N is length and D is edit distance (Myers). Worst case O(N²) but fast in practice.

## Installation
```bash
pip install diff-match-patch
```

## Basic Usage

### Character-level diff
```python
from diff_match_patch import diff_match_patch

dmp = diff_match_patch()
text1 = "Hello, world!"
text2 = "Hello, Python world!"

diffs = dmp.diff_main(text1, text2)
# Result: [(0, 'Hello, '), (1, 'Python '), (0, 'world!')]
# 0 = no change, 1 = insert, -1 = delete

# Human-readable output
for op, data in diffs:
    if op == -1:
        print(f"DELETE: {repr(data)}")
    elif op == 1:
        print(f"INSERT: {repr(data)}")
    else:
        print(f"EQUAL: {repr(data)}")
```

### Line-level diff
```python
from diff_match_patch import diff_match_patch

dmp = diff_match_patch()
text1 = "Line 1\nLine 2\nLine 3"
text2 = "Line 1\nLine 2 modified\nLine 3\nLine 4"

# Convert to line-based diff
lines_text1, lines_text2, line_array = dmp.diff_linesToChars(text1, text2)
diffs = dmp.diff_main(lines_text1, lines_text2, False)
dmp.diff_charsToLines(diffs, line_array)

for op, data in diffs:
    print(f"{'DELETE' if op == -1 else 'INSERT' if op == 1 else 'EQUAL'}: {repr(data)}")
```

### Patch generation and application
```python
from diff_match_patch import diff_match_patch

dmp = diff_match_patch()
text1 = "The quick brown fox"
text2 = "The slow brown fox"

# Create patch
diffs = dmp.diff_main(text1, text2)
patches = dmp.patch_make(text1, diffs)
patch_text = dmp.patch_toText(patches)

print("Patch:")
print(patch_text)

# Apply patch
text_patched, success_flags = dmp.patch_apply(patches, text1)
print(f"\nPatched text: {text_patched}")
print(f"All patches applied: {all(success_flags)}")
```

### Semantic cleanup
```python
from diff_match_patch import diff_match_patch

dmp = diff_match_patch()
text1 = "mouse"
text2 = "sofas"

# Without semantic cleanup
diffs = dmp.diff_main(text1, text2, checklines=False)
print("Raw diffs:", diffs)

# With semantic cleanup (improves readability)
dmp.diff_cleanupSemantic(diffs)
print("Cleaned diffs:", diffs)
```

## Pros
- **Myers algorithm**: Mathematically optimal edit distance
- **Semantic cleanup**: Improves diff readability automatically
- **Patch support**: Can apply diffs as patches to text
- **Performance**: Optimized C++ port available for speed
- **Multi-granularity**: Character, word, line-level diffs
- **Deadline control**: Prevents hanging on huge inputs
- **Cross-platform**: Same API in 8+ languages

## Cons
- **Maintenance mode**: Infrequent updates (still stable)
- **No patience diff**: Only Myers algorithm
- **No 3-way merge**: Can't resolve conflicts
- **No AST/semantic understanding**: Line-based only
- **API verbosity**: More boilerplate than modern libraries

## When to Use
- **Collaborative editing**: Real-time sync (Google Docs-style)
- **Version control**: Implement custom diff/patch system
- **Cross-platform sync**: Need same algorithm across languages
- **Patch files**: Generate and apply patches programmatically
- **Performance**: Need fast Myers diff with semantic cleanup

## When NOT to Use
- **Modern alternatives exist**: For simple use cases, `difflib` may suffice
- **Need patience diff**: Use git libraries or tree-sitter
- **Merge conflicts**: No 3-way merge support
- **Inactive maintenance**: If you need cutting-edge features

## Real-World Usage
- **Google Wave**: Original use case (collaborative editing)
- **Wikipedia**: Visual diff for article history
- **Etherpad**: Real-time collaborative editor
- **Various wikis and CMS**: Content versioning

## Popularity
- **GitHub stars:** ~1.5k (main repo, JavaScript version)
- **PyPI downloads:** ~500k/month
- **Status:** Stable and widely deployed, but not actively developed

## Alternatives
- **difflib**: Simpler, stdlib, no dependencies
- **python-Levenshtein**: Fast edit distance (C extension)
- **tree-sitter**: Semantic diff for code

## Verdict
**Best for:** Production-grade diff/patch operations with Myers algorithm. Ideal when you need cross-platform compatibility or collaborative editing features.

**Skip if:** You want patience diff, 3-way merge, or actively maintained cutting-edge features. For simple cases, `difflib` is easier.
