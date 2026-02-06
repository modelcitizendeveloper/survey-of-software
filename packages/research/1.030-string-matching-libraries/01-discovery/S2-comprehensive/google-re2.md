# google-re2 (pyre2) - Technical Analysis

## Algorithm Foundation

**Engine Type:** Deterministic Finite Automaton (DFA) engine

**Key Innovation:** Compiles regex to DFA, guaranteeing linear time

## How It Differs from Backtracking Engines

| Aspect | RE2 (DFA) | re/regex (Backtracking) |
|--------|-----------|-------------------------|
| Algorithm | Build DFA, scan once | Try paths, backtrack on fail |
| Time complexity | O(n) guaranteed | O(2^n) worst case |
| Features | Limited (no backrefs) | Full PCRE features |
| Memory | O(m) or more | O(m) stack depth |
| Security | DoS-resistant | Vulnerable to regex DoS |

## Complexity Analysis

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Compile regex | O(m²) | O(m) to O(2^m) |
| Match | O(n) | O(1) to O(m) |
| Total | O(m² + n) | DFA size varies |

*Worst case DFA can be exponential in pattern size, but typically manageable*

## Performance Characteristics

### When RE2 is Faster:
- Complex patterns with alternations
- Patterns vulnerable to backtracking explosions
- Large input texts

### When RE2 is Slower:
- Simple patterns (`re` has less overhead)
- Very short texts (DFA compilation cost dominates)

**Key Quote from pyre2 docs:**
> "For very simple substitutions, I've found that occasionally python's regular re module is actually slightly faster. However, when the re module gets slow, it gets really slow, while this module buzzes along."

## API Design

### Minimal Examples

**Drop-in replacement (mostly):**
```python
import re2

# Standard operations
re2.search(r'\d{3}-\d{4}', "Call 555-1234")  # → Match object
re2.findall(r'\w+', "Hello world")  # → ['Hello', 'world']
```

**UTF-8 optimization:**
```python
# Best performance with bytes
pattern = re2.compile(b'\\d+')
pattern.search(b"Age: 42")  # → Fastest path
```

**Fallback to re:**
```python
import re2
re2.set_fallback_notification(re2.FALLBACK_WARNING)

# Features not supported in RE2 fall back to re module
# Can change fallback from 're' to 'regex' module
```

## Feature Limitations

### NOT Supported (vs re/regex):
❌ Backreferences (`\1`, `\2`, etc.)
❌ Lookahead/lookbehind assertions
❌ Conditional patterns
❌ Some Unicode properties
❌ Recursion

### Supported:
✅ Character classes
✅ Alternation (`|`)
✅ Quantifiers (`*`, `+`, `?`, `{m,n}`)
✅ Groups (capturing and non-capturing)
✅ Anchors (`^`, `$`, `\b`)

## Architecture

- **Core**: C++ (Google's RE2 library)
- **Python Wrapper**: Multiple implementations (facebook/pyre2, axiak/pyre2, etc.)
- **Platforms**: Linux, macOS, Windows
- **License**: BSD-3-Clause

## Strengths

1. **Linear-time guarantee**: O(n) regardless of pattern complexity
2. **DoS-resistant**: Safe for untrusted regex patterns
3. **Predictable**: Worst-case = best-case asymptotically
4. **Google pedigree**: Proven at massive scale
5. **Thread-safe**: Can be used concurrently

## Limitations

1. **Feature restrictions**: No backreferences or lookaround
2. **DFA compilation cost**: Upfront cost for complex patterns
3. **Memory**: DFA can be large for some patterns
4. **Multiple Python wrappers**: Ecosystem fragmentation (confusing)

## When to Choose google-re2

✅ **Use when:**
- Processing untrusted user input (security critical)
- Need guaranteed O(n) performance
- Predictable latency required at scale
- Regex DoS attacks are a concern

❌ **Skip when:**
- Need backreferences or lookaround
- Simple patterns (re overhead lower)
- Can validate/limit regex complexity
- Features matter more than security

## Use Case Example

**Content moderation at scale:**
```python
# User-submitted regex patterns for content filtering
# RE2 prevents malicious patterns from causing DoS
import re2

user_pattern = re2.compile(user_input, re2.UNICODE)
# Safe: O(n) guaranteed, no regex bomb possible
```

## References

- [GitHub - google/re2](https://github.com/google/re2)
- [pyre2 Documentation](https://sarnold.github.io/pyre2/README.html)
- [GitHub - facebook/pyre2](https://github.com/facebook/pyre2/)
