# regex (Enhanced Regex) - Technical Analysis

## Algorithm Foundation

**Engine Type:** Backtracking regex engine with enhancements

**Key Difference from `re`:** More features, better Unicode, optional optimizations

## Supported Features

### Beyond Standard `re`:
- **Named lists**: Reusable character class definitions
- **Set operations**: Union, intersection, difference in character classes
- **Possessive quantifiers**: Prevent backtracking for performance
- **Atomic groups**: Similar to possessive quantifiers
- **Variable-length lookbehind**: Not in standard `re`
- **Recursive patterns**: Limited support
- **Better Unicode**: Full Unicode 17.0.0 categories and scripts

## Complexity Analysis

| Operation | Worst Case | Typical Case |
|-----------|------------|--------------|
| Simple match | O(n) | O(n) |
| Backtracking | O(2^n) | O(n) or O(nm) |
| Character class | O(n) | O(n) |

*Backtracking worst-case can be mitigated with possessive quantifiers*

## Performance Characteristics

### Speed Comparison with `re`:
- **Simple patterns**: Similar or slightly slower
- **Complex patterns**: Can be faster (better optimizations)
- **Unicode operations**: Significantly faster (better implementation)

### GIL Behavior:
- **Key advantage**: Releases GIL during matching
- **Benefit**: Other Python threads can run concurrently
- **Use case**: Multi-threaded text processing

## API Design

### Minimal Examples

**Drop-in replacement:**
```python
import regex

# Works like re module
regex.search(r'\d+', "Price: $42")  # → Match object

# Enhanced features
regex.search(r'\p{Script=Han}+', "你好world")  # → Matches Chinese chars
```

**Named lists:**
```python
# Define reusable patterns
pattern = regex.compile(r'(?V1)(?<vowel>[aeiou])')
pattern.findall("hello world")  # → ['e', 'o', 'o']
```

**Set operations:**
```python
# Character class operations
regex.findall(r'[a-z&&[^aeiou]]', "hello")  # → consonants only
```

## Feature Matrix

| Feature | `regex` | `re` | Notes |
|---------|---------|------|-------|
| Named groups | ✅ | ✅ | Same |
| Lookbehind (variable) | ✅ | ❌ | regex only |
| Possessive quantifiers | ✅ | ❌ | `++`, `*+`, `?+` |
| Set operations | ✅ | ❌ | `&&`, `--` |
| Unicode 17.0.0 | ✅ | ⚠️ | Older in `re` |
| GIL release | ✅ | ❌ | Concurrency benefit |

## Architecture

- **Language**: Python (with C extensions for performance)
- **Python Support**: 3.8+
- **Platforms**: Cross-platform (Linux, macOS, Windows)
- **License**: Apache 2.0

## Strengths

1. **Drop-in replacement**: Backwards compatible with `re`
2. **More powerful**: Advanced features for complex patterns
3. **Better Unicode**: Modern Unicode support
4. **Concurrency**: GIL release enables multi-threading

## Limitations

1. **Extra dependency**: Not in stdlib (must install)
2. **Backtracking risks**: Still vulnerable to catastrophic backtracking
3. **Learning curve**: Advanced features require documentation study
4. **Performance variance**: Sometimes slower than `re` for simple cases

## When to Choose regex

✅ **Use when:**
- Need features beyond standard `re` (set ops, var-length lookbehind)
- Unicode 17.0.0 support required
- Multi-threaded regex processing
- `re` limitations frustrating you

❌ **Skip when:**
- Standard `re` works fine
- Security/DoS concerns (→ google-re2)
- Can't add dependencies (→ use stdlib `re`)
- Need guaranteed linear time (→ google-re2)

## References

- [regex · PyPI](https://pypi.org/project/regex/)
- [GitHub - mrabarnett/mrab-regex](https://github.com/mrabarnett/mrab-regex)
- [PyPI Download Stats](https://pypistats.org/packages/regex)
