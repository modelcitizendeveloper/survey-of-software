# Character Encoding Libraries (CJK Focus)

## What Problem Does This Solve?

Character encoding is the bridge between bytes (how computers store text) and characters (what humans read). When working with text data, especially multilingual content or legacy systems, you need libraries that can:

1. **Detect encoding** - Identify which encoding a file or byte stream uses
2. **Convert between encodings** - Transform text from one encoding to another
3. **Handle CJK characters** - Work with Chinese, Japanese, and Korean text that uses complex character sets
4. **Debug mojibake** - Fix garbled text that results from encoding mismatches
5. **Preserve fidelity** - Ensure round-trip conversions don't lose information

## Why This Matters for Python Developers

### The Unicode Sandwich Model

Modern Python 3 uses UTF-8/Unicode internally, but you still encounter encoding issues when:
- Reading files from legacy systems (Big5, GB2312, Shift-JIS)
- Processing web scraping data with unknown encodings
- Importing CSV/text files from international sources
- Working with databases that use non-UTF8 collations
- Handling email attachments or user uploads

**Pattern**: Decode bytes → work with Unicode strings → encode back to bytes

### Real-World Scenarios

**Legacy System Integration**
```python
# Taiwan banking system exports Big5 CSV files
# Mainland China API returns GB2312 JSON
# Japanese vendor sends Shift-JIS XML
# Your Python 3 app expects UTF-8
```

**Data Quality Issues**
```python
# User uploads file, claims it's UTF-8, actually Big5
# Scraper downloads HTML, meta tag says GB2312, body is GBK
# Database returns mojibake because connection encoding != table encoding
```

**Variant Character Handling**
```python
# Traditional Chinese "台" (Taiwan) vs Simplified "台" (Mainland)
# Same semantic meaning, different codepoints, different visual forms
# Need to convert for search/matching but preserve original for display
```

## CJK Character Encoding Landscape

### Big5 (Traditional Chinese - Taiwan/Hong Kong)

**What it is**: Legacy encoding for Traditional Chinese characters
**Coverage**: ~13,000 characters (basic Big5), extended versions add more
**Problem**: Multiple incompatible extensions (Big5-HKSCS, Big5-2003, Big5-UAO)
**Use case**: Processing data from Taiwan government systems, Hong Kong financial institutions

**Python challenge**:
```python
# Python's "big5" codec != Windows Code Page 950
# Hong Kong Supplementary Character Set (HKSCS) needs separate handling
# Round-trip Big5 → Unicode → Big5 may produce different bytes
```

### GB2312/GBK/GB18030 (Simplified Chinese - Mainland China)

**What they are**: Progressive Chinese government standards
- **GB2312** (1980): ~7,000 characters, very limited
- **GBK** (1995): ~21,000 characters, backward compatible with GB2312
- **GB18030** (2005): Variable-width encoding, mandatory for Chinese software, full Unicode coverage

**Python challenge**:
```python
# Many systems say "GB2312" but actually use GBK
# GB18030 is variable-width (1, 2, or 4 bytes per character)
# Detection libraries often misidentify GB18030 as GBK
```

### Unicode CJK Blocks

**Why not just use UTF-8 for everything?**
You should! But you still need to understand CJK blocks for:
- **Han Unification**: Unicode merged Chinese/Japanese/Korean variants (controversial)
- **Variant selectors**: Same codepoint, different glyphs (語 in Japanese vs Chinese font)
- **Extension blocks**: CJK Extension A-G add rare/historical characters
- **Compatibility characters**: Duplicated for round-trip legacy conversions

**Python challenge**:
```python
# U+8A9E (語) renders differently in Japanese vs Chinese fonts
# Search/match needs to handle variants
# Font fallback chain affects display
# Extension G characters need recent Python/Unicode versions
```

## Common Pain Points

### Mojibake (文字化け - "character corruption")

**What causes it**:
1. Decode with wrong encoding: `bytes.decode('utf-8')` on Big5 data
2. Encode with wrong encoding: `text.encode('latin-1')` on Chinese text
3. Double encoding: Decode UTF-8, encode UTF-8 again, decode UTF-8 (nested encoding hell)
4. Wrong database collation: Store UTF-8 bytes in latin1 column

**Example**:
```
Original (Big5): 中文
Wrong decode as UTF-8: ä¸­æ–‡
Wrong encode then decode: â€œHello"
Double-encoded: Ã¤Â¸Â­Ã¦â€"â€¡
```

### Round-Trip Conversion Loss

**Problem**: Encoding A → Unicode → Encoding A may not be reversible

**Why**:
- Unicode has multiple ways to represent some characters (NFC vs NFD normalization)
- Legacy encodings have vendor-specific extensions
- Private Use Area (PUA) characters have no standard Unicode mapping
- Some characters genuinely don't exist in the target encoding

**Example**:
```python
# Hong Kong character in Big5-HKSCS
original_bytes = b'\x87\x40'  # 㐀 (CJK Extension A)
text = original_bytes.decode('big5hkscs')
roundtrip = text.encode('big5')  # Encoding error! Not in basic Big5
```

### Encoding Detection Challenges

**The problem**: No 100% reliable way to detect encoding from raw bytes

**Why**:
- Many encodings are valid interpretations of the same bytes
- GB2312/GBK/Big5 byte ranges overlap
- Short text samples don't have enough statistical signal
- Files may contain mixed encodings (email with multiple MIME parts)

**Libraries try to help**:
- `chardet`: Statistical analysis (slow, probabilistic)
- `charset-normalizer`: Improved chardet algorithm
- `cchardet`: Fast C implementation of chardet
- Manual heuristics: BOM detection, HTML meta tags, statistical patterns

## What We're Evaluating

Python libraries for:
1. **Encoding detection**: Identify unknown encodings in files/streams
2. **Transcoding**: Convert between encodings reliably
3. **CJK variant handling**: Convert traditional↔simplified, handle Unicode variants
4. **Mojibake repair**: Detect and fix double-encoding issues
5. **Legacy codec support**: Big5 variants, GB18030, Shift-JIS, EUC-KR

**Key evaluation criteria**:
- **Accuracy**: Correct detection rate, lossless conversion
- **Performance**: Speed on large files, memory efficiency
- **CJK coverage**: Support for Big5-HKSCS, GB18030, variant selectors
- **Debugging tools**: Help identify encoding issues, suggest fixes
- **API ergonomics**: Easy to use correctly, hard to use wrong

## Out of Scope

- **Font rendering**: How glyphs are drawn (that's font/rendering engine territory)
- **Input methods**: How users type CJK characters (OS/IME responsibility)
- **OCR**: Extracting text from images (different problem domain)
- **Translation**: Converting between languages (NLP/MT territory)

We're focused on encoding/decoding, not semantics or display.

## References

- [Python Unicode HOWTO](https://docs.python.org/3/howto/unicode.html)
- [Joel on Software: The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)
- [GB18030 Standard](https://en.wikipedia.org/wiki/GB_18030)
- [Big5 and variants](https://en.wikipedia.org/wiki/Big5)
- [Unicode Han Unification](https://en.wikipedia.org/wiki/Han_unification)
