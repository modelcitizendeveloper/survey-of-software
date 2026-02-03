# String Parsing and Manipulation - Deep Dive

## Parsing Approaches

### Recursive Descent Parsers
- **Method**: Hand-written parser following grammar structure
- **Complexity**: O(n) for LL(k) grammars
- **Pros**: Easy to understand, debuggable, good error messages
- **Cons**: Left recursion requires elimination, manual implementation
- **Use case**: Small DSLs, configuration parsers, JSON alternatives

### Parser Generators (LALR/LR)
- **Examples**: Yacc, Bison, ANTLR (v3 and earlier)
- **Method**: Bottom-up parsing with lookahead
- **Complexity**: O(n) for LR(k) grammars
- **Pros**: Handles more grammars than LL, shift-reduce power
- **Cons**: Complex error recovery, harder to debug generated code
- **Use case**: Programming language compilers, complex grammars

### PEG (Parsing Expression Grammars)
- **Examples**: PEG.js, pest (Rust), pyparsing
- **Method**: Packrat parsing with memoization
- **Complexity**: O(n) with memoization, exponential without
- **Pros**: Ordered choice (no ambiguity), easy composition, intuitive
- **Cons**: Left recursion challenging, backtracking can hide errors
- **Use case**: Modern DSLs, data extraction, markup languages

### Parser Combinators
- **Examples**: Parsec (Haskell), nom (Rust), combine (Rust)
- **Method**: Build parsers by combining smaller parsers
- **Pros**: Highly composable, embedded in host language, type-safe
- **Cons**: Performance varies, can be cryptic for beginners
- **Use case**: Functional programming contexts, protocol parsing

### Regex-based Parsing
- **Method**: Extract data using regular expressions
- **Limitation**: Cannot parse nested structures (HTML, JSON)
- **Pros**: Fast for simple patterns, widely available
- **Cons**: Unmaintainable for complex grammars, limited expressiveness
- **Use case**: Log parsing, simple data extraction, validation

## String Manipulation Patterns

### Immutable vs Mutable Strings

**Immutable (Python str, Java String, Go string)**
- **Pattern**: Create new string on each modification
- **Cost**: O(n) per modification due to copying
- **Benefit**: Thread-safe, easier reasoning, prevents aliasing bugs
- **Anti-pattern**: Repeated concatenation in loops

**Mutable (C++ std::string, Rust String, Java StringBuilder)**
- **Pattern**: In-place modification with capacity management
- **Cost**: O(1) amortized append with pre-allocation
- **Benefit**: Efficient for building large strings
- **Caution**: Not thread-safe, mutation requires care

### String Building Strategies

**Naive concatenation (anti-pattern)**
```python
result = ""
for item in items:
    result += item  # O(n²) total!
```

**Builder pattern**
```python
result = "".join(items)  # O(n) total
```

**Pre-allocated buffer**
```rust
let mut s = String::with_capacity(estimated_size);
s.push_str("...");  // Minimal reallocations
```

### Unicode Normalization

**Forms**:
- **NFD**: Canonical decomposition (é → e + ́)
- **NFC**: Canonical composition (e + ́ → é)
- **NFKD**: Compatibility decomposition (ﬁ → f + i)
- **NFKC**: Compatibility composition

**Use cases**:
- **NFC**: Default for most applications (composed, compact)
- **NFD**: Case-insensitive comparison, sorting
- **NFKC**: Search, form input normalization
- **NFKD**: Indexing, ASCII folding

### String Interning

**Technique**: Store only one copy of each distinct string value
**Benefit**: O(1) equality comparison, reduced memory
**Cost**: Interning overhead, unbounded intern table growth
**Use case**: Compilers (identifiers), configuration keys, enum-like strings

### Zero-Copy String Operations

**String Views (C++17 string_view, Rust &str)**
- **Pattern**: Reference into existing string without copying
- **Benefit**: O(1) substring, split, trim operations
- **Caution**: Lifetime management, dangling references possible

**Rope Data Structure**
- **Pattern**: Tree of string fragments for large texts
- **Benefit**: O(log n) insert/delete, efficient concatenation
- **Use case**: Text editors, document processing

## Security Considerations

### Injection Vulnerabilities

**SQL Injection**
- **Anti-pattern**: String concatenation for queries
- **Solution**: Parameterized queries, ORMs

**Command Injection**
- **Anti-pattern**: Shell=true with user input
- **Solution**: Argument arrays, safe_execute wrappers

**XSS (Cross-Site Scripting)**
- **Anti-pattern**: Unescaped user content in HTML
- **Solution**: Auto-escaping templates, sanitization libraries

### ReDoS (Regular Expression Denial of Service)

**Vulnerable pattern**: Nested quantifiers with overlapping alternatives
```regex
(a+)+b    # Exponential on "aaaaaa..." without 'b'
(a|a)*b
(a|ab)*c
```

**Mitigation**:
- Use linear-time regex engines (RE2, Rust regex, Go regexp)
- Set timeouts on backtracking engines
- Validate regex patterns before deployment

### Buffer Overflows (C/C++)

**Unsafe**:
```c
strcpy(dest, src);        // No bounds checking
sprintf(buf, fmt, ...);   // Fixed buffer
```

**Safe**:
```c
strlcpy(dest, src, sizeof(dest));  // BSD
snprintf(buf, sizeof(buf), fmt, ...);  // C99
```

## Performance Optimization Techniques

### Small String Optimization (SSO)
- **Technique**: Store short strings inline in string object
- **Threshold**: Usually 15-23 bytes depending on implementation
- **Benefit**: Avoid heap allocation for small strings (common case)
- **Implementation**: C++ std::string, Rust String (in some cases)

### SIMD String Operations
- **Operations**: Search, compare, validate UTF-8
- **Speedup**: 2-8x for bulk operations
- **Examples**: memchr (libc), simdutf, Rust's std::string SIMD paths

### Compile-Time String Processing
- **Technique**: Regex compilation, template expansion at compile time
- **Benefit**: Zero runtime overhead for static patterns
- **Examples**: Rust `regex!` macro, C++20 constexpr

### Memory Layout
- **Cache locality**: Keep string data contiguous
- **Alignment**: Align string operations to word boundaries
- **Prefetching**: Hint upcoming string data to cache

## Recommendations by Use Case

| Use Case | Recommended Approach | Rationale |
|----------|---------------------|-----------|
| Log parsing | Regex or custom parser | Simple structure, speed matters |
| Config files | PEG or recursive descent | Clear syntax, good error messages |
| Programming language | ANTLR or parser combinator | Complex grammar, tooling support |
| Data extraction | Regex (simple) or PEG (nested) | Match complexity to tool |
| High-throughput | SIMD, zero-copy, interning | Every cycle counts |
| User input | Auto-escaping, sanitization | Security critical |
| Large documents | Rope data structure | Efficient editing operations |
