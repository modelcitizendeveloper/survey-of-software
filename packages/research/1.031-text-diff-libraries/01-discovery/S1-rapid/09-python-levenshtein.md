# python-Levenshtein

## Overview
**Package:** `python-Levenshtein`
**Algorithm:** Levenshtein distance, Damerau-Levenshtein, Hamming
**Status:** Active
**Author:** Max Bachmann (fork of original by Matthias C. Bachmann)
**First Released:** 2004 (original), 2021 (modern fork)
**Language:** C extension for performance

## Description
A fast C implementation of string similarity metrics, including Levenshtein distance (edit distance). While not a full diff library, it provides the mathematical foundation for diff algorithms - computing the **minimum edit distance** between strings.

**Key features:**
- **Levenshtein distance**: Minimum insertions/deletions/substitutions
- **Damerau-Levenshtein**: Adds transpositions (swaps)
- **Hamming distance**: For equal-length strings
- **Similarity ratios**: Normalized distance scores
- **Jaro-Winkler**: Fuzzy string matching
- **Fast**: C extension, 10-100x faster than pure Python

## Use Cases
- **Fuzzy matching**: Find similar strings (spell check, search)
- **Data deduplication**: Identify near-duplicate records
- **DNA/protein sequences**: Bioinformatics alignment
- **Quality metrics**: Measure diff quality (distance)
- **Autocorrect**: Suggest corrections for typos
- **Testing**: Measure how "close" output is to expected

## Installation
```bash
pip install python-Levenshtein
```

Or modern fork:
```bash
pip install levenshtein
```

## Basic Usage

### Edit distance
```python
import Levenshtein

s1 = "kitten"
s2 = "sitting"

distance = Levenshtein.distance(s1, s2)
print(f"Edit distance: {distance}")  # 3
# Operations: k→s, e→i, insert g
```

### Similarity ratio
```python
import Levenshtein

s1 = "hello"
s2 = "hallo"

ratio = Levenshtein.ratio(s1, s2)
print(f"Similarity: {ratio:.2%}")  # 80.00%
```

### Find best match
```python
import Levenshtein

query = "appel"
candidates = ["apple", "application", "apply", "banana"]

# Find closest match
best = min(candidates, key=lambda x: Levenshtein.distance(query, x))
print(f"Best match: {best}")  # apple
```

### Jaro-Winkler similarity
```python
import Levenshtein

s1 = "MARTHA"
s2 = "MARHTA"

# Jaro distance
jaro = Levenshtein.jaro(s1, s2)
print(f"Jaro: {jaro:.2f}")  # 0.94

# Jaro-Winkler (emphasizes prefix similarity)
jaro_winkler = Levenshtein.jaro_winkler(s1, s2)
print(f"Jaro-Winkler: {jaro_winkler:.2f}")  # 0.96
```

### Hamming distance
```python
import Levenshtein

s1 = "1011101"
s2 = "1001001"

hamming = Levenshtein.hamming(s1, s2)
print(f"Hamming distance: {hamming}")  # 2
```

### Edit operations (editops)
```python
import Levenshtein

s1 = "kitten"
s2 = "sitting"

ops = Levenshtein.editops(s1, s2)
print(ops)
# [('replace', 0, 0), ('replace', 4, 4), ('insert', 6, 6)]
```

### Apply operations
```python
import Levenshtein

s1 = "kitten"
s2 = "sitting"

ops = Levenshtein.editops(s1, s2)
result = Levenshtein.apply_edit(ops, s1, s2)
print(result)  # sitting
```

## Algorithms

### Levenshtein Distance
Minimum number of single-character edits:
- **Insert**: Add a character
- **Delete**: Remove a character
- **Substitute**: Replace a character

**Complexity:** O(n * m) where n, m are string lengths

### Damerau-Levenshtein Distance
Adds **transposition** (swap adjacent characters):
- All Levenshtein operations
- **Transpose**: Swap two adjacent characters

Useful for typos: "teh" → "the" is 1 transposition vs 2 substitutions.

### Hamming Distance
Number of positions where characters differ (strings must be equal length).

**Use case:** Error detection in fixed-length codes (binary, DNA).

### Jaro-Winkler
Fuzzy string matching that emphasizes common prefixes.

**Use case:** Name matching, record linkage.

## Pros
- **Fast**: C extension, optimized algorithms
- **Multiple metrics**: Levenshtein, Jaro-Winkler, Hamming
- **Battle-tested**: Decades of use in production
- **Edit operations**: Returns actual edit sequence
- **Standard algorithms**: Well-known, documented
- **Active fork**: Modern version with maintenance

## Cons
- **Single-character edits only**: Can't detect moved blocks
- **No semantic understanding**: Character-level only
- **Not a full diff tool**: Doesn't generate human-readable diffs
- **Limited to strings**: Can't diff complex structures

## When to Use
- **Fuzzy matching**: Spell check, autocorrect, search
- **Data cleaning**: Find duplicates, normalize names
- **Quality metrics**: Measure diff/patch quality
- **Bioinformatics**: DNA/protein sequence alignment
- **Testing**: Quantify how "wrong" output is
- **Autocomplete**: Rank suggestions by similarity

## When NOT to Use
- **Human-readable diffs**: Use `difflib` or `diff-match-patch`
- **Semantic understanding**: Use tree-sitter or AST diff
- **Multi-line text**: Edit distance explodes for large texts
- **Complex structures**: Use DeepDiff or jsondiff

## Integration with Diff Libraries
```python
import difflib
import Levenshtein

# Use difflib for diff generation
diff = difflib.unified_diff(lines1, lines2)

# Use Levenshtein to measure quality
for line in diff:
    if line.startswith('-') and not line.startswith('---'):
        old_line = line[1:]
        # Find corresponding + line, compute distance
        # (conceptual - full implementation more complex)
```

## Popularity
- **GitHub stars:** ~1.3k
- **PyPI downloads:** ~10M/month (original), ~15M/month (Levenshtein fork)
- **Status:** Very active (modern fork)

## Real-World Usage
- **Spell checkers**: Google, Microsoft Word
- **Search engines**: "Did you mean?" suggestions
- **Data deduplication**: Customer record matching
- **Bioinformatics**: BLAST, sequence alignment
- **NLP**: Text similarity, clustering

## Related Libraries
- **fuzzywuzzy**: Higher-level fuzzy string matching (uses Levenshtein)
- **rapidfuzz**: Even faster fuzzy matching (Rust)
- **difflib**: Full diff library (slower but more features)

## Comparison with difflib

| Feature | python-Levenshtein | difflib |
|---------|-------------------|---------|
| **Edit distance** | ✓ (exact) | ~ (ratio) |
| **Performance** | Very fast (C) | Medium (Python) |
| **Diff generation** | ✗ | ✓ |
| **Edit operations** | ✓ | ✓ |
| **Multi-line text** | Limited | ✓ |

**Use together:**
- Levenshtein for similarity scoring
- difflib for human-readable diffs

## Verdict
**Best for:** Fast edit distance calculations for fuzzy matching, spell check, data deduplication, and quality metrics. Essential for any application needing string similarity.

**Skip if:** You need full diff generation with context (use `difflib`), or semantic understanding (use tree-sitter).

**Pro tip:** Combine with `difflib` for best results - use Levenshtein to find similar items, then difflib to show how they differ.
