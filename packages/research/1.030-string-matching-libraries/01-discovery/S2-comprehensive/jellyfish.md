# Jellyfish - Technical Analysis

## Algorithm Foundation

**Core Technology:** Python with C extensions for performance-critical code

### Supported Algorithms

**Phonetic Encoding:**
- **Soundex**: Classic phonetic algorithm (US census bureau)
- **Metaphone**: Improved phonetic encoding
- **NYSIIS**: New York State Identification and Intelligence System
- **Match Rating**: Phonetic comparison codex

**String Distance:**
- **Levenshtein**: Edit distance (insertion, deletion, substitution)
- **Damerau-Levenshtein**: Edit distance with transpositions
- **Jaro distance**: Measures character matches and transpositions
- **Jaro-Winkler**: Jaro with prefix bonus for better performance

## Complexity Analysis

| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Levenshtein | O(nm) | O(nm) |
| Jaro-Winkler | O(nm) | O(1) |
| Soundex | O(n) | O(1) |
| Metaphone | O(n) | O(1) |

## Performance Benchmarks

From 2025 comparative study:
- **Strength**: Excellent for short strings (names, words)
- **Weakness**: Struggles with long text inputs
- **Speed**: Slower than RapidFuzz for edit distance
- **Memory**: Higher usage with long strings

## API Design

### Minimal Examples

**Phonetic encoding:**
```python
import jellyfish

jellyfish.soundex("Smith")  # → "S530"
jellyfish.soundex("Smyth")  # → "S530"  # Same encoding!

jellyfish.metaphone("Catherine")  # → "K0RN"
jellyfish.metaphone("Katherine")  # → "K0RN"  # Same encoding!
```

**String distance:**
```python
jellyfish.levenshtein_distance("kitten", "sitting")  # → 3
jellyfish.jaro_winkler_similarity("MARTHA", "MARHTA")  # → 0.961
```

## Feature Matrix

| Feature | Supported | Notes |
|---------|-----------|-------|
| Phonetic encoding | ✅ | Unique strength |
| Edit distances | ✅ | Slower than RapidFuzz |
| Token-based | ❌ | Not available |
| Multi-pattern | ❌ | Single comparisons only |

## Strengths

1. **Unique phonetic algorithms**: Only library with Soundex, Metaphone, NYSIIS
2. **Name matching**: Excellent for finding similar names despite spelling differences
3. **Simple API**: Easy to use, straightforward function calls

## Limitations

1. **Performance**: Slower than RapidFuzz for edit distance operations
2. **Long text**: Performance degrades with string length
3. **Limited scope**: Smaller algorithm selection than RapidFuzz

## When to Choose Jellyfish

✅ **Use when:**
- Matching names or words (phonetic similarity critical)
- Need Soundex or Metaphone algorithms specifically
- User search where pronunciation matters

❌ **Skip when:**
- Pure edit distance needed (→ RapidFuzz - faster)
- Large-scale fuzzy matching (→ RapidFuzz - more efficient)
- Token-based matching required (→ RapidFuzz)

## References

- [GitHub - jamesturk/jellyfish](https://github.com/jamesturk/jellyfish)
- [Comparative Analysis (2025)](https://ijeedu.com/index.php/ijeedu/article/view/188)
