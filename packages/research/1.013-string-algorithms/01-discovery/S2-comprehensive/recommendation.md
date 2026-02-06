# S2: Comprehensive Discovery - Recommendations

## Algorithm Selection Framework

### For Pattern Matching

**Single pattern, short text (< 1KB)**: Use built-in string search
- Most languages optimize this case (e.g., SIMD in libc's strstr)
- Boyer-Moore overhead not worth it

**Single pattern, large text**: Boyer-Moore variant
- Best average case performance
- Built-in methods often use this

**Multiple patterns (< 100)**: Rabin-Karp or simple loop
- Rabin-Karp good for moderate pattern counts
- Loop with built-in search often sufficient

**Multiple patterns (100+)**: Aho-Corasick
- O(n + m + z) regardless of pattern count
- Essential for content filtering, log analysis

**Fuzzy matching**:
- **Levenshtein**: For accuracy, spell checking
- **Bitap/fuse.js**: For interactive search, short patterns
- **Jaro-Winkler**: For name matching specifically

**Regex with untrusted input**: RE2/Rust regex/Go regexp
- Linear time guarantee
- DoS-resistant
- Worth the feature trade-offs for security

**Regex with trusted input**: PCRE/language built-ins
- Full feature set (backreferences, lookahead)
- Better expressiveness
- Monitor for performance issues

### For Parsing

**Simple structured data**: Regex or string split
- CSV, simple logs, key=value formats
- Fast and adequate

**Nested structures**: PEG or parser combinators
- JSON-like, s-expressions, configuration DSLs
- Modern, composable, good error messages

**Programming languages**: ANTLR or hand-written recursive descent
- Complex grammars require parser generator power
- Or hand-written for ultimate control

**High performance**: Hand-optimized parser with SIMD
- Protocol parsing, high-throughput systems
- Worth the implementation cost only at scale

### For Unicode

**Simple text processing**: Language built-ins
- Python str, Rust String, Go string usually sufficient
- Modern languages handle UTF-8 well

**Case-insensitive comparison**: Unicode case folding
- Use `unicodedata.normalize()` + `.casefold()` (Python)
- Or ICU collation with strength

**Locale-aware operations**: ICU
- Sorting, case conversion, date/number formatting
- Only library with comprehensive locale support

**Grapheme iteration**: Specialized libraries
- `unicode-segmentation` (Rust)
- `graphemer` (JavaScript)
- `grapheme` (Python)

**Full internationalization**: ICU
- If you need collation, transliteration, boundary analysis
- Accept the size cost for correctness

## Performance vs Safety Trade-offs

### When to Prioritize Safety

**User input processing**: Always
- Use DoS-resistant regex (RE2-based)
- Validate UTF-8 strictly
- Sanitize before use (HTML escaping, SQL parameterization)

**Parsing untrusted data**: Always
- Bounds-check all operations
- Use safe languages (Rust, Go) or safe libraries (C++)
- Limit resource consumption (memory, time)

**High-security contexts**: Always
- Avoid custom crypto/encoding
- Use vetted libraries
- Audit for injection vulnerabilities

### When to Optimize for Performance

**Inner loops of hot paths**: After profiling
- SIMD string operations
- Skip UTF-8 validation on trusted data
- Use byte-level operations where safe

**Large-scale batch processing**: If cost-justified
- Custom parsers with zero-copy
- Parallel processing
- Specialized data structures (suffix arrays)

**High-throughput systems**: With monitoring
- Accept complexity for critical paths
- Maintain escape hatches (rate limiting, timeouts)
- Extensive testing and fuzzing

## Architecture Recommendations

### String Handling Strategy

1. **Choose encoding early**: UTF-8 for most applications
2. **Validate at boundaries**: Check encoding on input, trust internally
3. **Normalize once**: Apply NFC normalization on input
4. **Use appropriate abstractions**: String views for zero-copy, builders for construction

### Library Selection

1. **Start with built-ins**: Most languages provide adequate basics
2. **Add specialized libraries as needed**:
   - Fuzzy matching → thefuzz/fuse.js
   - Multi-pattern → aho-corasick
   - Parsing → PEG/parser combinator
   - I18n → ICU (if truly needed)
3. **Avoid redundancy**: Don't include multiple regex engines
4. **Consider bundle size**: Especially for web/mobile

### Testing Strategy

1. **Unit test with Unicode**: Include emoji, CJK, RTL text in test data
2. **Fuzz string operations**: Use fuzzing to find edge cases
3. **Benchmark hot paths**: Profile before optimizing
4. **Security audit**: Check for injection vulnerabilities

## Common Anti-patterns to Avoid

### 1. Rolling Your Own
- ❌ Custom regex engine
- ❌ Custom UTF-8 decoder
- ❌ Homebrew fuzzy matching

→ Use battle-tested libraries

### 2. Ignoring Unicode
- ❌ Treating strings as byte arrays
- ❌ Length checks on bytes instead of graphemes
- ❌ Assuming ASCII

→ Use Unicode-aware operations

### 3. Naive Regex
- ❌ Parsing HTML with regex
- ❌ No timeouts on backtracking engines
- ❌ User-controlled patterns without validation

→ Use appropriate parsing tools, safe regex engines

### 4. String Building
- ❌ Repeated concatenation in loops
- ❌ No pre-allocation when size known

→ Use string builders, join operations

### 5. Security Oversights
- ❌ String concatenation for SQL/shell commands
- ❌ No escaping in templates
- ❌ Trusting client-side validation

→ Parameterized queries, auto-escaping templates, server-side validation

## Decision Matrix

| Requirement | Primary Concern | Recommended Choice |
|-------------|----------------|-------------------|
| Single pattern search | Performance | Language built-in |
| Multi-pattern (many) | Throughput | Aho-Corasick |
| Fuzzy search | Accuracy | Levenshtein-based |
| Regex (trusted) | Features | PCRE/built-in |
| Regex (untrusted) | Security | RE2-based |
| Simple parsing | Simplicity | Regex/split |
| Complex parsing | Maintainability | PEG/parser combinator |
| Language parsing | Power | ANTLR/hand-written |
| Unicode (basic) | Compatibility | Built-in |
| Unicode (i18n) | Correctness | ICU |
| High performance | Speed | SIMD, custom parser |

## S2 Conclusion

String algorithms offer a wide range of trade-offs between performance, safety, features, and complexity. The key to good engineering is:

1. **Understand your requirements**: Performance? Security? Features?
2. **Profile before optimizing**: Measure actual bottlenecks
3. **Choose appropriate tools**: Don't over-engineer or under-protect
4. **Test thoroughly**: Especially with Unicode edge cases
5. **Maintain security awareness**: Validate, sanitize, escape

**Next**: S3 will explore need-driven scenarios and specific use case recommendations.
