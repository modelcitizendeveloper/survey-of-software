# Unicode and Internationalization - Deep Dive

## Unicode Fundamentals

### Encoding Schemes
- **UTF-8**: Variable length (1-4 bytes), ASCII-compatible, web standard
- **UTF-16**: Variable length (2 or 4 bytes), Windows/Java native
- **UTF-32**: Fixed 4 bytes, simple indexing, memory-intensive

### Key Concepts

**Code Point**: Numeric value assigned to character (U+0041 = 'A')
**Code Unit**: Basic unit of encoding (byte in UTF-8, 16-bit in UTF-16)
**Grapheme Cluster**: User-perceived character (e.g., 'é' can be one or two code points)

### The Complexity

```
String: "🏳️‍🌈"  (Rainbow flag)
Code points: 4 (flag + VS + ZWJ + rainbow)
UTF-8 bytes: 14
UTF-16 units: 5
Grapheme clusters: 1
String length: Depends on what you count!
```

## Common Unicode Pitfalls

### 1. String Length Ambiguity

**Byte length**: Size in memory (UTF-8 variable)
```python
len("café".encode('utf-8'))  # 5 bytes
```

**Code point count**: Number of Unicode characters
```python
len("café")  # 4 code points
```

**Grapheme count**: User-visible characters
```python
# Requires ICU or grapheme library
grapheme_length("👨‍👩‍👧")  # 1 grapheme, 5 code points
```

### 2. Case Conversion

**Problem**: Not all languages have simple uppercase/lowercase
- Turkish: 'i' → 'İ' (dotted capital I)
- German: 'ß' → 'SS' (sharp s expands)
- Greek: Σ vs σ vs ς (different forms)

**Solution**: Locale-aware case folding
```python
import icu
icu.UnicodeString("İstanbul").toLower("tr_TR")  # turkish locale
```

### 3. String Comparison and Collation

**Problem**: Lexicographic order differs by language
- Swedish: 'ö' sorts after 'z'
- German: 'ö' treated as 'o' variant
- Thai: Tone marks don't affect primary sort

**Solution**: Use collation libraries (ICU, std::locale)

### 4. Normalization Forms

**Problem**: Same visual character, different encodings
```
"café" can be:
  Option 1: c + a + f + é     (NFC, 4 code points)
  Option 2: c + a + f + e + ́  (NFD, 5 code points)
```

**Solution**: Normalize before comparison
```python
unicodedata.normalize('NFC', text) == unicodedata.normalize('NFC', other)
```

### 5. Text Boundaries

**Grapheme boundaries**: Where characters start/end
**Word boundaries**: Space, punctuation, but language-dependent
**Sentence boundaries**: Complex rules (e.g., "Dr. Smith" doesn't end sentence)

**Problem**: Naive splitting breaks composed characters
```rust
"नमस्ते".chars().take(3)  // May split combining marks!
```

**Solution**: Use boundary analysis (ICU, unicode-segmentation crate)

## Internationalization Best Practices

### 1. Encoding

**Always declare encoding**
```html
<meta charset="UTF-8">
```

**Use UTF-8 everywhere**
- File storage
- Database columns
- HTTP headers
- API responses

### 2. String Handling

**Index by code point, not byte**
```javascript
// BAD: May slice mid-character
text.substring(0, 10)

// GOOD: Use grapheme-aware library
[...text].slice(0, 10).join('')
```

**Be careful with reverse**
```python
# BAD: Breaks combining marks
text[::-1]

# GOOD: Reverse grapheme clusters
''.join(reversed(list(grapheme.graphemes(text))))
```

### 3. Display Width

**Problem**: Not all characters have same display width
```
"Hello" = 5 columns
"こんにちは" = 10 columns (full-width)
"🏳️‍🌈" = 2 columns (wide emoji)
```

**Solution**: Use wcwidth library for terminal display, or Unicode East Asian Width property

### 4. Validation

**Check encoding validity**
```rust
std::str::from_utf8(bytes)?  // Returns error on invalid UTF-8
```

**Reject problematic characters**
- Control characters (C0, C1)
- Private use area (unless intended)
- Surrogate pairs (invalid in UTF-8)

### 5. Sanitization

**Remove invisible characters**
- Zero-width spaces (U+200B)
- Bidirectional overrides (U+202E, U+202D)
- Combining marks without base

**Normalize Unicode**
- Apply NFC normalization
- Remove variation selectors if not needed
- Fold compatibility characters (NFKC)

## Library Recommendations

### Comprehensive Solutions

**ICU (International Components for Unicode)**
- **Coverage**: Collation, normalization, boundary analysis, transliteration, calendar
- **Languages**: C/C++, Java (ICU4J), Python (PyICU)
- **Size**: Large (~30MB), but comprehensive
- **Use case**: Full internationalization needs

**libunistring (GNU)**
- **Coverage**: Basic Unicode operations for C
- **Size**: Smaller than ICU
- **Use case**: C projects needing Unicode basics

### Language-Specific

**Python**
- `unicodedata`: Built-in normalization, categories
- `PyICU`: Full ICU binding
- `regex`: Unicode-aware regex with categories
- `grapheme`: Grapheme cluster handling

**Rust**
- `unicode-segmentation`: Grapheme/word/sentence boundaries
- `unicode-normalization`: NFC/NFD/NFKC/NFKD
- `unicode-width`: Display width calculation

**JavaScript**
- `Intl`: Built-in collation, date/number formatting
- `graphemer`: Grapheme splitting
- `punycode`: IDN encoding/decoding

**Go**
- `golang.org/x/text/unicode/norm`: Normalization
- `golang.org/x/text/collate`: Collation
- `golang.org/x/text/width`: Display width

## Performance Considerations

### UTF-8 Benefits
- **Space-efficient** for ASCII-heavy text
- **Cache-friendly** due to compactness
- **Self-synchronizing**: Can find character boundaries without scanning from start
- **Backward compatible** with ASCII

### UTF-8 Costs
- **Variable length**: Cannot index in O(1)
- **Validation overhead**: Must check well-formedness
- **Worst case**: 4 bytes per character (emoji, rare CJK)

### Optimization Techniques

**Skip validation on trusted data**
```rust
// SAFE if bytes known valid UTF-8
unsafe { std::str::from_utf8_unchecked(bytes) }
```

**Use byte operations when possible**
```rust
// Searching ASCII in UTF-8 safe at byte level
text.as_bytes().iter().position(|&b| b == b' ')
```

**Cache length calculations**
```python
# Count once, reuse
grapheme_len = grapheme.length(text)
```

**Consider UTF-32 for heavy random access**
- If frequently indexing by grapheme
- If character length queries dominate
- Trade memory for speed

## Security Implications

### Homograph Attacks
**Problem**: Visually similar characters from different scripts
```
paypal.com (ASCII)
pаypal.com (Cyrillic 'а')
```

**Mitigation**: Restrict to single script, use IDN policies

### Normalization Attacks
**Problem**: Normalization changes meaning
```
File: "/../etc/passwd" (blocked)
After NFC: "/../etc/passwd" (still blocked)
After NFKC: "/../etc/passwd" (may bypass naive check)
```

**Mitigation**: Normalize before security checks, validate after normalization

### Overlong Encoding
**Problem**: Invalid UTF-8 sequences bypass filters
```
'/' can be encoded as 0xC0 0xAF (overlong, invalid)
```

**Mitigation**: Strict UTF-8 validation, reject overlong sequences

## Testing Recommendations

**Test data**:
- ASCII edge cases: empty, very long, all printable
- Latin with diacritics: café, naïve, Zürich
- CJK: 中文, 日本語, 한국어
- Emoji and symbols: 👨‍👩‍👧, 🏳️‍🌈, ⚠️
- RTL text: العربية, עברית
- Combining marks: q̃, 각
- Zero-width and invisibles
- Malformed UTF-8 sequences

**Test scenarios**:
- Round-trip encode/decode
- Case conversion
- Normalization preservation
- Boundary detection
- Length calculations
- Comparison and sorting
