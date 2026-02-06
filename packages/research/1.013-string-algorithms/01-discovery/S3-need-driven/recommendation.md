# S3: Need-Driven Discovery - Recommendations

## Key Insights from Use Cases

### 1. Don't Roll Your Own for Complex Problems

**Anti-pattern**: Custom regex for email validation, custom CSV parser, homebrew fuzzy matching

**Better approach**: Use specialized libraries that handle edge cases
- Email: `email-validator`, `validator.js`
- CSV: `csv` module/crate, `pandas`
- Fuzzy matching: `fuse.js`, `thefuzz`, `rapidfuzz`

**Why**: These problems have more edge cases than apparent. Battle-tested libraries save debugging time.

### 2. Security Must Be Built In, Not Added

**Critical patterns**:
- Auto-escaping templates (Jinja2, React, Askama)
- Parameterized queries (SQLAlchemy, diesel, prepared statements)
- Timeouts on regex (especially with user input)
- Input validation at boundaries

**Never trust**:
- User input (validate and sanitize)
- Client-side validation alone (always verify server-side)
- String concatenation for security contexts (SQL, shell, HTML)

### 3. Choose Tools Based on Scale

| Scale | Approach | Example |
|-------|----------|---------|
| Small (< 1K items) | Simple algorithms | Built-in string search, linear scan |
| Medium (1K-100K) | Standard libraries | fuse.js, basic indexing |
| Large (100K-1M) | Optimized libraries | Aho-Corasick, suffix arrays |
| Very large (> 1M) | Specialized systems | Elasticsearch, database indexes |

**Don't over-engineer**: Simple solutions work until they don't. Profile before optimizing.

### 4. Streaming Beats Loading for Large Data

**Problem**: 10GB log file, CSV with millions of rows, continuous data stream

**Solution**: Process line-by-line or in chunks
```python
# Bad: data = file.read()  # OOM on large files
# Good: for line in file: process(line)
```

**Benefits**:
- Constant memory usage
- Can start processing immediately
- Handles files larger than RAM

### 5. Terminal vs Non-Terminal Contexts

**Considerations**:
- Colors: Use in terminal, strip in pipes/files
- Progress bars: Show in terminal, omit in logs
- Interactive prompts: Detect TTY before showing
- Line buffering: Different behavior in pipes

**Detection**:
```python
import sys
is_terminal = sys.stdout.isatty()
```

### 6. Unicode is Default, Not Optional

**Wrong assumption**: "My users only speak English"

**Reality**: Usernames, addresses, product names are international

**Best practices**:
- Use UTF-8 everywhere
- Normalize on input (NFC)
- Test with emoji, CJK, RTL text
- Use grapheme-aware operations for display

## Decision Tree by Use Case

### String Search/Matching

```
Do you control the pattern?
├─ Yes: Is it a single simple pattern?
│  ├─ Yes → Built-in string search
│  └─ No: Many patterns? (> 10)
│     ├─ Yes → Aho-Corasick
│     └─ No → Loop with built-in search
└─ No (user-controlled)
   ├─ Simple glob? → minimatch/globset
   ├─ Regex needed?
   │  ├─ Trusted input → Built-in regex
   │  └─ Untrusted input → RE2-based (Rust regex, Go regexp)
   └─ Fuzzy matching? → fuse.js/thefuzz
```

### Parsing

```
What structure?
├─ Key=value, simple → String split or regex
├─ CSV → csv module/crate
├─ JSON/YAML/TOML → Standard parser + validation
├─ Nested custom format
│  ├─ Simple grammar → PEG (pest, PEG.js)
│  └─ Complex grammar → ANTLR or hand-written
└─ HTML/XML → DOM parser (never regex!)
```

### Validation

```
What input?
├─ Email → email-validator library
├─ Phone → phonenumbers library
├─ URL → urlparse + scheme check
├─ Password strength → zxcvbn
├─ Custom format
│  ├─ Simple → Regex with clear pattern
│  └─ Complex → Parser + semantic validation
└─ Sanitization needed?
   ├─ HTML → Auto-escaping template or bleach
   ├─ SQL → Parameterized queries
   └─ Shell → Avoid shell=True, use arg list
```

## Library Selection Criteria by Context

### Web Applications
**Priority**: Security, Unicode, XSS prevention

**Recommended**:
- Templates: Jinja2 (Python), React (JS), Askama (Rust)
- Validation: email-validator, phonenumbers
- Search: Elasticsearch (large scale), fuse.js (client-side)
- Slugs: python-slugify, slugify (JS)

### CLI Tools
**Priority**: Performance, streaming, terminal UX

**Recommended**:
- Glob: globset (Rust), pathlib (Python)
- CSV: csv crate (Rust), csv module (Python)
- Colors: colored (Rust), rich (Python)
- Progress: indicatif (Rust), tqdm (Python)

### Data Processing
**Priority**: Throughput, memory efficiency, correctness

**Recommended**:
- CSV: polars, csv crate for speed
- JSON: serde_json (Rust), orjson (Python)
- Regex: regex crate (Rust), re (Python)
- Streaming: Iterator-based processing

### Compilers/Parsers
**Priority**: Correctness, error messages, maintainability

**Recommended**:
- Grammar: ANTLR (complex), pest (simple PEG), parser combinators
- Lexing: Hand-written, logos (Rust), PLY (Python)
- Error recovery: Resilient parsing, error productions

## Common Integration Patterns

### 1. Validation + Normalization Pipeline
```python
def process_user_input(raw_input):
    # 1. Decode and validate encoding
    text = raw_input.decode('utf-8')

    # 2. Normalize Unicode
    text = unicodedata.normalize('NFC', text)

    # 3. Trim whitespace
    text = text.strip()

    # 4. Validate format
    if not is_valid(text):
        raise ValueError("Invalid format")

    # 5. Sanitize for context
    return escape_html(text)  # Or other context-specific escaping
```

### 2. Streaming with Error Recovery
```python
def process_large_file(path):
    errors = []

    with open(path, encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                result = parse_line(line)
                yield result
            except ValueError as e:
                errors.append((line_num, str(e)))
                if len(errors) > 100:
                    raise TooManyErrors(errors)
```

### 3. Caching Compiled Patterns
```python
import functools

@functools.lru_cache(maxsize=128)
def get_regex(pattern):
    return re.compile(pattern)

# Reuses compiled regex across calls
for text in texts:
    if get_regex(r'\d+').search(text):
        process(text)
```

## Pitfall Checklist

Before deploying string-processing code, verify:

**Security**:
- [ ] User input validated at boundaries
- [ ] Templates auto-escape by default
- [ ] No string concatenation for SQL/shell/HTML
- [ ] Regex has timeouts or uses linear-time engine
- [ ] Unicode normalized before security checks

**Correctness**:
- [ ] Handles empty strings
- [ ] Handles very long strings (> 1MB)
- [ ] Tested with Unicode (emoji, CJK, RTL)
- [ ] Error handling for malformed input
- [ ] Streaming for large files

**Performance**:
- [ ] Compiled/cached patterns where reused
- [ ] Appropriate algorithm for scale
- [ ] Not loading large files entirely into memory
- [ ] Profiled if performance-critical

**Usability**:
- [ ] Clear error messages (which field, why invalid)
- [ ] Preserves user input on errors (don't lose their work)
- [ ] Appropriate UI feedback (validation, progress)
- [ ] Accessible (screen readers, keyboard navigation)

## S3 Conclusion

String processing requirements are driven by context: web apps need security, CLI tools need streaming, compilers need correctness. The "best" solution depends on:

1. **Scale**: Simple algorithms often sufficient until proven otherwise
2. **Trust**: Untrusted input requires defensive measures
3. **Performance**: Profile before optimizing, know your bottlenecks
4. **Maintainability**: Use libraries for complex problems

**Core principle**: Match tool sophistication to problem complexity. A regex might be over-engineering for simple validation, but under-engineering for a parser.

**Next**: S4 will explore strategic implications and architectural patterns for string processing at scale.
