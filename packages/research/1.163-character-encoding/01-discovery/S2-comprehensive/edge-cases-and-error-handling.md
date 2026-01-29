# Edge Cases and Error Handling

## Detection Edge Cases

### Short Text (<50 bytes)

**Problem**: Insufficient statistical signal for reliable detection

```python
# 10-byte Chinese text
short_text = "中文测试".encode('gbk')  # 8 bytes

# Detection unreliable
chardet.detect(short_text)
# May return: GB2312, GBK, Big5, or even random encoding with low confidence
```

**Mitigation strategies**:
1. Use longer sample (read more of file)
2. Check confidence score
3. Fall back to user override or common default (UTF-8)
4. Use file extension/metadata hints

### Binary Files with Text Snippets

**Problem**: Executable with embedded strings looks like valid encoding

```python
# Binary file with some ASCII strings
binary_data = b'\x00\x00\x7fELF\x00\x00Hello World\x00\x00'

chardet.detect(binary_data)
# May return: ASCII with high confidence (WRONG - it's binary!)
```

**Mitigation**:
```python
def is_likely_binary(data, sample_size=8192):
    """Heuristic: check for null bytes and non-text bytes"""
    sample = data[:sample_size]
    null_count = sample.count(b'\x00')
    if null_count > len(sample) * 0.05:  # >5% null bytes
        return True

    non_text = sum(1 for b in sample if b < 32 and b not in (9, 10, 13))
    if non_text > len(sample) * 0.3:  # >30% control chars
        return True

    return False
```

### Mixed Encodings in One File

**Problem**: Different sections use different encodings (e.g., email with attachments)

**Example**: HTML page with UTF-8 meta tag but Latin-1 body

```html
<!DOCTYPE html>
<meta charset="utf-8">
<!-- Body is actually Latin-1 -->
<body>café</body>  <!-- Stored as Latin-1 bytes -->
```

**Detection will fail** - tries to find single encoding for entire file.

**Mitigation**:
- Split file into parts (MIME multipart, HTML sections)
- Detect encoding per part
- For HTML: Check meta tag, then verify with detection

### Ambiguous Byte Sequences

**Problem**: Some byte sequences are valid in multiple encodings

| Bytes | Big5 | GBK | UTF-8 |
|-------|------|-----|-------|
| `0xB1 0xE2` | 憭 | 被 | Invalid |
| `0xC4 0xE3` | 囜 | 你 | Invalid |

**Detection chooses based on statistics**, but short text can guess wrong.

**Mitigation**:
- Increase sample size
- Use charset-normalizer (multiple hypotheses)
- Ask user if confidence < 80%

## Encoding Edge Cases

### GB18030 Mandatory Characters

**Problem**: Chinese government requires GB18030 for characters outside GBK range

```python
# Character only in GB18030 (not in GBK)
text = "\U0001f600"  # 😀 emoji

# GBK encoding fails
text.encode('gbk')
# UnicodeEncodeError: 'gbk' codec can't encode character

# GB18030 handles it
text.encode('gb18030')
# b'\x94\x39\xd3\x38' (4-byte sequence)
```

**Mitigation**: Use GB18030 instead of GBK for Mainland Chinese content.

### Big5 vs Big5-HKSCS

**Problem**: Hong Kong characters missing from standard Big5

```python
# Hong Kong Supplementary Character Set character
text = "㗎"  # Cantonese particle

# Standard Big5 may fail
text.encode('big5')
# May work or fail depending on Python version

# Big5-HKSCS handles it
text.encode('big5hkscs')
# Works reliably
```

**Mitigation**: Use `big5hkscs` for Hong Kong content, even if detected as `big5`.

### Round-Trip Conversion Loss

**Problem**: Not all Unicode characters can round-trip through legacy encodings

```python
# Character not in Big5
text = "𠮷" # U+20BB7 (CJK Extension B)

# Encoding fails or replaces
text.encode('big5', errors='replace')
# b'?' (lost character)

# Round-trip fails
restored = b'?'.decode('big5')
assert restored == text  # FAILS
```

**Mitigation**:
1. Check if encoding supports character before converting
2. Use errors='xmlcharrefreplace' to preserve as `&#...;`
3. Keep UTF-8 as canonical, only convert when necessary

### Variant Selectors and CJK Compatibility

**Problem**: Unicode has multiple ways to represent "same" character

```python
# Same logical character, different codepoints
nfc = "語"  # U+8A9E (composed)
nfd = "語"  # U+8A9E U+3099 (decomposed) - actually this is wrong example

# Better example: Compatibility vs unified
compat = "﨑"  # U+FA11 (compatibility ideograph)
unified = "崎"  # U+5D0E (unified ideograph)

# Visually identical, different codepoints
assert compat == unified  # FALSE
```

**Mitigation**: Use Unicode normalization (NFC/NFKC) before comparison.

## Repair Edge Cases

### False Positives

**Problem**: ftfy "fixes" text that wasn't broken

```python
import ftfy

# Text with intentional special characters
text = "Use the ﬁ ligature for ﬁnish"

# ftfy expands ligature
fixed = ftfy.fix_text(text)
print(fixed)  # "Use the fi ligature for finish"

# May not be desired!
```

**Mitigation**: Only use ftfy when you know text is garbled.

### Unrecoverable Mojibake

**Problem**: Information is genuinely lost

```python
# Double-encoded then truncated
original = "中文"  # 2 characters
utf8_bytes = original.encode('utf-8')  # b'\xe4\xb8\xad\xe6\x96\x87'
double = utf8_bytes.decode('latin-1')  # ä¸­æ–‡
truncated = double[:3]  # ä¸­ (missing second character)

# ftfy cannot recover truncated data
ftfy.fix_text(truncated)  # Best effort, but second char is gone
```

**Mitigation**: Prevention is better than repair. Validate encodings at boundaries.

### Nested Encoding (3+ Layers)

**Problem**: Multiple rounds of wrong encoding/decoding

```python
# UTF-8 → decode as Latin-1 → encode as UTF-8 → decode as Latin-1
original = "café"
layer1 = original.encode('utf-8').decode('latin-1')  # cafÃ©
layer2 = layer1.encode('utf-8').decode('latin-1')    # cafÃÂ©
layer3 = layer2.encode('utf-8').decode('latin-1')    # cafÃÂÂ©

# ftfy struggles with 3+ layers
ftfy.fix_text(layer3)  # Partial fix at best
```

**Mitigation**: Fix at source. If text is already 3+ layers garbled, may be unrecoverable.

## CJK Conversion Edge Cases

### One-to-Many Ambiguity

**Problem**: One Simplified character maps to multiple Traditional characters

```python
# 发 (Simplified) could be:
# - 髮 (hair)
# - 發 (develop, emit)

text_s = "理发店"  # Haircut shop

# Without context, conversion may be wrong
zhconv.convert(text_s, 'zh-hant')
# May produce: 理髮店 ✅ or 理發店 ❌

# OpenCC uses phrase dictionary to choose correctly
opencc_converter = opencc.OpenCC('s2t')
opencc_converter.convert(text_s)
# 理髮店 ✅ (understands 理发 = haircut phrase)
```

**Mitigation**: Use OpenCC for context-aware conversion, not character-by-character mapping.

### Regional Vocabulary Mismatch

**Problem**: Same concept, different words in different regions

```python
# "Software" in Simplified Chinese
mainland = "软件"

# Taiwan Traditional uses different word
taiwan_correct = "軟體"  # Preferred in Taiwan
taiwan_literal = "軟件"  # Literal conversion

# Simple conversion gives literal
zhconv.convert(mainland, 'zh-tw')  # 軟件 (technically correct but not idiomatic)

# OpenCC uses vocabulary conversion
opencc_converter = opencc.OpenCC('s2tw')
opencc_converter.convert(mainland)  # 軟體 ✅ (idiomatic)
```

**Mitigation**: Use OpenCC with region-specific profiles (s2tw, s2hk) not generic (s2t).

### Irreversible Conversion

**Problem**: Round-trip Traditional → Simplified → Traditional loses information

```python
# Two traditional characters both become 发 in Simplified
trad1 = "頭髮"  # Hair
trad2 = "發展"  # Development

# Both convert to same Simplified character
zhconv.convert(trad1, 'zh-hans')  # 头发
zhconv.convert(trad2, 'zh-hans')  # 发展

# Converting back loses context
zhconv.convert("头发", 'zh-hant')  # Could be 頭髮 or 頭發
zhconv.convert("发展", 'zh-hant')  # Could be 發展 or 髮展
```

**Mitigation**: Keep original encoding as canonical, only convert for display/search.

## Error Handling Patterns

### Pattern 1: Detect with Fallback

```python
from charset_normalizer import from_bytes

def safe_detect(data, fallback='utf-8'):
    """Detect encoding with fallback to UTF-8"""
    result = from_bytes(data)
    best = result.best()

    if best is None:
        return fallback

    if best.encoding_confidence < 0.7:
        # Low confidence, use fallback
        return fallback

    return best.encoding
```

### Pattern 2: Try Multiple Encodings

```python
def decode_with_fallback(data, encodings=['utf-8', 'gbk', 'big5', 'latin-1']):
    """Try encodings in order until one works"""
    for encoding in encodings:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue

    # Last resort: decode with replacement
    return data.decode('utf-8', errors='replace')
```

### Pattern 3: Validate Before Converting

```python
def safe_traditional_to_simplified(text):
    """Convert Traditional to Simplified with error handling"""
    try:
        # Normalize first (handle NFD/NFC)
        import unicodedata
        normalized = unicodedata.normalize('NFC', text)

        # Convert
        converter = opencc.OpenCC('t2s')
        result = converter.convert(normalized)

        # Verify output is valid
        if len(result) == 0 and len(text) > 0:
            # Conversion failed, return original
            return text

        return result
    except Exception as e:
        # Fallback: return original
        return text
```

### Pattern 4: Partial Repair

```python
def conservative_repair(text):
    """Repair mojibake only if confident"""
    import ftfy

    # Try repair
    fixed = ftfy.fix_text(text)

    # Heuristic: if "repair" changed >50% of characters, it's probably wrong
    import difflib
    ratio = difflib.SequenceMatcher(None, text, fixed).ratio()

    if ratio < 0.5:
        # Too many changes, probably not mojibake
        return text

    return fixed
```

### Pattern 5: User Override

```python
def detect_with_override(data, user_encoding=None):
    """Allow user to override detection"""
    if user_encoding:
        try:
            return data.decode(user_encoding)
        except UnicodeDecodeError:
            # User was wrong, fall back to detection
            pass

    # Auto-detect
    result = charset_normalizer.from_bytes(data)
    return str(result.best())
```

## Testing Recommendations

### Build a Test Suite

```python
# Collect real-world failures
test_cases = [
    {
        'name': 'Big5 Taiwan news',
        'file': 'test_data/big5_news.txt',
        'expected_encoding': 'big5',
        'expected_lang': 'Chinese',
    },
    {
        'name': 'GBK with GB18030 chars',
        'file': 'test_data/gb18030_chars.txt',
        'expected_encoding': 'gb18030',
        'notes': 'Contains 4-byte sequences',
    },
    {
        'name': 'Double UTF-8 mojibake',
        'file': 'test_data/double_utf8.txt',
        'garbled': True,
        'expected_repair': 'original_text.txt',
    },
]
```

### Monitor False Positives

```python
# Track when ftfy changes text it shouldn't
def audit_repairs(input_dir, output_dir):
    """Log all ftfy changes for human review"""
    for file in input_dir.glob('*.txt'):
        original = file.read_text()
        fixed = ftfy.fix_text(original)

        if original != fixed:
            # Log change for review
            diff_file = output_dir / f"{file.stem}.diff"
            diff_file.write_text(f"BEFORE:\n{original}\n\nAFTER:\n{fixed}")
```

### Regression Testing

```python
# Keep problematic files in test suite
# Re-test after library updates

def test_big5_hkscs_detection():
    """Ensure Big5-HKSCS characters are handled"""
    with open('test_data/hkscs_chars.txt', 'rb') as f:
        data = f.read()

    result = charset_normalizer.from_bytes(data)
    assert result.best().encoding in ['big5', 'big5hkscs']
```

## Common Gotchas

1. **Assuming UTF-8**: Always detect, never assume
2. **Ignoring confidence**: Low confidence means uncertain, handle gracefully
3. **Converting without normalizing**: NFC/NFD matters for comparison
4. **Repairing good text**: Only use ftfy on known-garbled text
5. **Character-level CJK conversion**: Use phrase-aware (OpenCC) for quality
6. **Forgetting error handlers**: Always use `errors='replace'` or similar
7. **Not testing round-trip**: Encode → decode → encode may not preserve
8. **Mixing encoding with variant conversion**: Big5→GB2312 is NOT Traditional→Simplified

## Summary: Robust Code Checklist

- [ ] Detect encoding (don't assume UTF-8)
- [ ] Check confidence score (warn if <80%)
- [ ] Handle detection failure (fallback encoding)
- [ ] Use appropriate error handler (`replace` vs `strict`)
- [ ] Validate output (check for � replacement chars)
- [ ] Only repair if text is known to be garbled
- [ ] Use OpenCC for CJK conversion (not simple mapping)
- [ ] Normalize Unicode before comparison (NFC)
- [ ] Test with real-world data (not just ASCII)
- [ ] Log failures for debugging
