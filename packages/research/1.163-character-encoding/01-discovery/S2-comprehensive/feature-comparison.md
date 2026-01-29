# Feature Comparison Matrix

## Detection Libraries

| Feature | charset-normalizer | cchardet | chardet | uchardet |
|---------|-------------------|----------|---------|----------|
| **Implementation** | Pure Python | C extension | Pure Python | C binding |
| **Algorithm** | Coherence analysis | Mozilla UCD | Mozilla UCD | Mozilla UCD |
| **Speed (10MB file)** | ~3s | ~0.1s | ~5s | ~0.1s |
| **Accuracy (typical)** | 95%+ | 85-90% | 85-90% | 85-90% |
| **Incremental detection** | ✅ | ❌ | ✅ | ✅ |
| **Confidence scoring** | ✅ (0-1) | ✅ (0-1) | ✅ (0-1) | ✅ (0-1) |
| **Multiple hypotheses** | ✅ (ranked list) | ❌ (single) | ❌ (single) | ❌ (single) |
| **Language detection** | ✅ | ❌ | ✅ | ❌ |
| **Explanation/debugging** | ✅ (shows reasoning) | ❌ | ❌ | ❌ |
| **Unicode normalization** | ✅ (NFC/NFD aware) | ❌ | ❌ | ❌ |
| **API compatibility** | chardet-compatible | chardet-compatible | Original | Different |
| **Dependencies** | Pure Python | C compiler | Pure Python | C library |
| **Wheels available** | ✅ | ✅ | N/A | ⚠️ (limited) |
| **Maintenance (2024-25)** | ✅ Active | ⚠️ Sporadic | ⚠️ Maintenance | ⚠️ Stable |
| **PyPI downloads/month** | 100M+ | 10M+ | 50M+ | <1M |

### CJK Encoding Support

| Encoding | charset-normalizer | cchardet | chardet | uchardet |
|----------|-------------------|----------|---------|----------|
| UTF-8 | ✅ | ✅ | ✅ | ✅ |
| UTF-16/32 | ✅ | ✅ | ✅ | ✅ |
| Big5 | ✅ | ✅ | ✅ | ✅ |
| Big5-HKSCS | ⚠️ (as Big5) | ⚠️ (as Big5) | ⚠️ (as Big5) | ⚠️ (as Big5) |
| GB2312 | ✅ | ✅ | ✅ | ✅ |
| GBK | ✅ | ✅ | ✅ | ✅ |
| GB18030 | ⚠️ (as GBK) | ⚠️ (as GBK) | ⚠️ (as GBK) | ⚠️ (as GBK) |
| EUC-TW | ✅ | ✅ | ✅ | ✅ |
| EUC-JP | ✅ | ✅ | ✅ | ✅ |
| EUC-KR | ✅ | ✅ | ✅ | ✅ |
| Shift-JIS | ✅ | ✅ | ✅ | ✅ |
| ISO-2022-JP | ✅ | ✅ | ✅ | ✅ |

**Notes**:
- Big5-HKSCS: All libraries detect as "Big5", missing Hong Kong extensions
- GB18030: Detected as "GBK" or "GB2312" (similar byte ranges)
- Ambiguity: GB2312 vs GBK vs Big5 have overlapping byte sequences

### Detection Accuracy by Text Length

| Text Length | charset-normalizer | cchardet/chardet | Notes |
|-------------|-------------------|-----------------|-------|
| <50 bytes | 60-70% | 50-60% | Insufficient statistical signal |
| 50-500 bytes | 80-90% | 70-80% | Minimal but workable |
| 500-5000 bytes | 95%+ | 85-90% | Good statistical sample |
| >5000 bytes | 98%+ | 90-95% | Strong statistical signal |

## Transcoding (Python codecs)

| Feature | Python 3.7+ | Notes |
|---------|-------------|-------|
| **CJK Encodings** | ||
| Big5 | ✅ `big5` | Basic Big5 |
| Big5-HKSCS | ✅ `big5hkscs` | Hong Kong extensions |
| GB2312 | ✅ `gb2312` | Basic Simplified Chinese |
| GBK | ✅ `gbk` | Extended Simplified |
| GB18030 | ✅ `gb18030` | Full Unicode coverage |
| Shift-JIS | ✅ `shift_jis` | Japanese |
| EUC-JP | ✅ `euc_jp` | Japanese |
| EUC-KR | ✅ `euc_kr` | Korean |
| ISO-2022-JP | ✅ `iso2022_jp` | Japanese email |
| **Error Handling** | ||
| Strict mode | ✅ | Raise on invalid bytes |
| Ignore mode | ✅ | Skip invalid bytes |
| Replace mode | ✅ | Use � for invalid |
| Backslashreplace | ✅ | Use \\xNN escape |
| **Streaming** | ||
| Incremental encoder | ✅ | `codecs.getencoder()` |
| Incremental decoder | ✅ | `codecs.getdecoder()` |
| File I/O | ✅ | `codecs.open()` |
| **Performance** | Very fast (C implementation) ||

### Python codecs Edge Cases

| Scenario | Behavior | Notes |
|----------|----------|-------|
| Invalid Big5 sequence | UnicodeDecodeError | Unless errors='replace' |
| GB18030 4-byte char | ✅ Handled | Proper variable-width support |
| Big5-HKSCS char in `big5` | ⚠️ May fail | Use `big5hkscs` codec |
| GBK char in `gb2312` | ⚠️ May fail | GB2312 is subset of GBK |
| Round-trip UTF-8→Big5→UTF-8 | ⚠️ May lose chars | Big5 can't represent all Unicode |

## Repair Library (ftfy)

| Feature | ftfy | Notes |
|---------|------|-------|
| **Mojibake Patterns** | ||
| Double UTF-8 encoding | ✅ | "â€œHello" → "Hello" |
| UTF-8 as Latin-1 | ✅ | "cafÃ©" → "café" |
| Big5 as UTF-8 | ✅ | "ä¸­æ–‡" → "中文" |
| Win-1252 in UTF-8 | ✅ | Smart quotes, em dashes |
| GB2312 in Latin-1 | ⚠️ (partial) | Some patterns |
| Triple encoding | ⚠️ (limited) | Complex chains hard |
| **Other Fixes** | ||
| HTML entities | ✅ | `&lt;` → `<`, `&#20013;` → 中 |
| Unicode normalization | ✅ | NFC/NFD handling |
| Control characters | ✅ | Removes invisible chars |
| Latin ligatures | ✅ | `ﬁ` → `fi` |
| **Configuration** | ||
| Unescape HTML | ✅ (toggle) | Can disable |
| Normalization | ✅ (NFC/NFKC/None) | Configurable |
| Fix Latin ligatures | ✅ (toggle) | Can disable |
| **False Positives** | ||
| "Fix" good text | ⚠️ (rare) | Conservative heuristics |
| **Performance** | ||
| Speed | Moderate | Tries multiple patterns |
| Memory | Low | Processes incrementally |

### ftfy Repair Success Rates (Estimated)

| Mojibake Pattern | Success Rate | Notes |
|------------------|--------------|-------|
| Double UTF-8 | 95%+ | Well-handled |
| UTF-8 as Latin-1 | 90%+ | Common pattern |
| Big5 as UTF-8 | 85%+ | CJK-aware |
| Win-1252 smart quotes | 98%+ | Very common |
| Triple encoding | 60-70% | Hit or miss |
| Complex chains | 40-50% | Often can't reverse |

## Chinese Variant Conversion

| Feature | OpenCC | zhconv |
|---------|--------|--------|
| **Implementation** | Pure Python | Pure Python |
| **Conversion Type** | Phrase-aware | Character-level |
| **Dictionaries** | Large (100K+ entries) | Small (10K entries) |
| **Context Analysis** | ✅ | ❌ |
| **Regional Variants** | ||
| Traditional (generic) | ✅ `t` | ✅ `zh-hant` |
| Simplified (generic) | ✅ `s` | ✅ `zh-hans` |
| Taiwan Traditional | ✅ `tw` | ✅ `zh-tw` |
| Hong Kong Traditional | ✅ `hk` | ✅ `zh-hk` |
| Mainland Simplified | ✅ `cn` | ✅ `zh-cn` |
| Singapore Simplified | ❌ | ✅ `zh-sg` |
| **Vocabulary Conversion** | ||
| Regional terms | ✅ (計算機→電腦) | ❌ |
| Idiom localization | ✅ (公車→公交車) | ❌ |
| **Accuracy** | ||
| Simple text | 95%+ | 90%+ |
| Ambiguous characters | 90%+ (context helps) | 70-80% (guesses) |
| Technical terms | 85%+ | 75%+ |
| **Performance** | ||
| Speed (10KB text) | ~50ms | ~10ms |
| Memory | ~50MB (dictionaries) | ~5MB |
| **Reversibility** | ||
| Round-trip loss | Moderate (one-to-many) | Moderate |
| **Maintenance** | ✅ Active (2024) | ✅ Active (2024) |

### Conversion Accuracy Examples

| Original | OpenCC Output | zhconv Output | Correct |
|----------|---------------|---------------|---------|
| 理发 (haircut, S) | 理髮 | 理髮 | Both ✅ (lucky) |
| 发展 (develop, S) | 發展 | 髮展 | OpenCC ✅, zhconv ❌ |
| 计算机 (computer, S) | 電腦 (TW vocab) | 計算機 (literal) | OpenCC ✅ (regional) |
| 软件 (software, S) | 軟體 (TW vocab) | 軟件 (literal) | OpenCC ✅ (regional) |
| 信息 (information, S) | 資訊 (TW vocab) | 信息 (literal) | OpenCC ✅ (regional) |

**Key difference**: OpenCC uses phrase dictionaries to choose correct character based on context and regional vocabulary. zhconv does simple character mapping.

## Summary: Best Tool for Each Job

| Task | Best Choice | Alternative |
|------|-------------|-------------|
| **Detection (accuracy)** | charset-normalizer | - |
| **Detection (speed)** | cchardet | - |
| **Detection (pure Python)** | charset-normalizer | chardet |
| **Transcoding** | Python codecs | - |
| **Mojibake repair** | ftfy | - |
| **CJK conversion (quality)** | OpenCC | - |
| **CJK conversion (speed)** | zhconv | - |
| **Legacy Python** | chardet | - |

## Integration Patterns

### Pattern 1: Unknown Encoding → UTF-8
```python
from charset_normalizer import from_bytes

with open('unknown.txt', 'rb') as f:
    raw = f.read()

result = from_bytes(raw)
text = str(result.best())  # Now in UTF-8
```

### Pattern 2: Garbled Text Repair
```python
import ftfy

garbled = load_from_database()  # Already decoded wrong
fixed = ftfy.fix_text(garbled)
```

### Pattern 3: Big5 → UTF-8 → Simplified
```python
# Step 1: Transcode
with open('big5_file.txt', 'rb') as f:
    big5_bytes = f.read()
text = big5_bytes.decode('big5')  # Traditional Chinese, UTF-8

# Step 2: Convert variant
import opencc
converter = opencc.OpenCC('t2s')  # Traditional → Simplified
simplified = converter.convert(text)
```

### Pattern 4: Full Rescue Pipeline
```python
from charset_normalizer import from_bytes
import ftfy
import opencc

# Unknown encoding, possibly garbled, need Simplified Chinese
with open('mystery.txt', 'rb') as f:
    raw = f.read()

# Step 1: Detect and decode
result = from_bytes(raw)
text = str(result.best())

# Step 2: Repair mojibake
fixed = ftfy.fix_text(text)

# Step 3: Convert to Simplified
converter = opencc.OpenCC('t2s')
simplified = converter.convert(fixed)
```

## Performance vs Accuracy Trade-offs

| Priority | Detection | Repair | CJK Conversion |
|----------|-----------|--------|----------------|
| **Best Accuracy** | charset-normalizer | ftfy | OpenCC |
| **Best Speed** | cchardet | ftfy (only option) | zhconv |
| **Balanced** | charset-normalizer | ftfy | OpenCC (fast enough) |
| **Pure Python** | charset-normalizer | ftfy | Both are pure Python |
| **Minimal Dependencies** | chardet | ftfy | zhconv |

## Recommendation Matrix

| Use Case | Detection | Transcode | Repair | Convert |
|----------|-----------|-----------|--------|---------|
| **Web scraping** | charset-normalizer | codecs | ftfy | - |
| **User uploads** | charset-normalizer | codecs | ftfy | - |
| **Taiwan content** | charset-normalizer | codecs | ftfy | OpenCC (s2tw) |
| **Mainland content** | charset-normalizer | codecs | ftfy | - |
| **Bilingual site** | charset-normalizer | codecs | - | OpenCC |
| **Legacy migration** | cchardet (speed) | codecs | ftfy | - |
| **Search indexing** | cchardet | codecs | - | zhconv (normalize) |
| **Professional content** | charset-normalizer | codecs | ftfy | OpenCC |
