# S2 Comprehensive Discovery - Approach

## Goal

Deep analysis of character encoding libraries with:
- Detailed feature comparison matrices
- Performance benchmarks on real-world data
- Accuracy testing on edge cases
- Integration pattern analysis
- Error handling robustness

## Evaluation Framework

### 1. Feature Completeness Matrix

**Detection libraries** (charset-normalizer, cchardet, chardet):
- Supported encodings (CJK specific)
- Incremental/streaming support
- Confidence scoring
- Language detection
- Multi-encoding hypothesis
- Explanation/debugging info

**Transcoding** (Python codecs):
- Encoding coverage
- Error handling modes
- Streaming support
- Memory efficiency

**Repair** (ftfy):
- Mojibake patterns detected
- HTML entity handling
- Unicode normalization
- Configurability
- False positive rate

**CJK conversion** (OpenCC, zhconv):
- Traditional↔Simplified coverage
- Regional variants (TW, HK, CN)
- Vocabulary conversion
- Phrase vs character-level
- Reversibility

### 2. Performance Benchmarks

**Test datasets**:
- Small (1KB): Detection may be unreliable
- Medium (10KB): Typical text file
- Large (1MB): Log file, book
- Very large (10MB+): Database dump

**Encodings to test**:
- UTF-8 (baseline)
- Big5 (Traditional Chinese)
- GB2312 (Simplified Chinese, basic)
- GBK (Simplified Chinese, extended)
- GB18030 (Simplified Chinese, full Unicode)
- Mixed/ambiguous (could be multiple encodings)

**Metrics**:
- Detection time (ms)
- Memory usage (MB)
- Accuracy (% correct on labeled dataset)
- Confidence calibration (does 0.95 confidence mean 95% correct?)

### 3. Accuracy Testing

**Edge cases**:
- Short text (<50 bytes): Insufficient statistical signal
- Binary with text snippets: Should reject, not misdetect
- Mixed encodings: Different parts use different encodings
- Rare characters: Extension B-G, private use area
- Ambiguous byte sequences: Valid in multiple encodings

**CJK-specific edge cases**:
- Big5-HKSCS characters: Hong Kong supplementary set
- GB18030 mandatory characters: 4-byte sequences
- Variant selectors: Unicode Ideographic Variation Sequences
- Compatibility characters: Duplicate codepoints for roundtrip

**Mojibake patterns**:
- Double UTF-8 encoding
- Big5 decoded as UTF-8
- GB2312 in Latin-1 pipeline
- Windows-1252 smart quotes in UTF-8
- Nested encoding (3+ layers)

### 4. Integration Patterns

How libraries work together:
```python
# Pattern 1: Detection → Transcode
charset-normalizer → Python codecs

# Pattern 2: Detection → Repair → Transcode
charset-normalizer → ftfy → Python codecs

# Pattern 3: Transcode → Convert variants
Python codecs → OpenCC

# Pattern 4: Full pipeline
charset-normalizer → ftfy → Python codecs → OpenCC
```

**Questions**:
- Does detection work on mojibake? (No - detect first, repair later)
- Can ftfy fix double-encoded CJK? (Sometimes)
- Does OpenCC handle mojibake? (No - repair first)
- Order of operations for best results?

### 5. Error Handling & Robustness

**Failure modes**:
- Detection returns None (no confident match)
- Decode errors (invalid byte sequences)
- Round-trip loss (encoding doesn't support all Unicode)
- Repair makes things worse (false positive)
- Conversion ambiguity (one-to-many mappings)

**Recovery strategies**:
- Fallback encodings (try UTF-8, then Latin-1)
- Error handlers (strict, ignore, replace, backslashreplace)
- Manual override (let user choose encoding)
- Multiple hypotheses (show top 3 guesses)

## Deliverables

1. **Feature Comparison Matrix**: Comprehensive table of capabilities
2. **Performance Benchmarks**: Speed and memory on real datasets
3. **Accuracy Report**: Detection success rate by encoding
4. **Edge Case Analysis**: How libraries handle tricky scenarios
5. **Integration Guide**: Best practices for combining libraries
6. **Error Handling Patterns**: Robust code templates

## Test Datasets

### Real-World Sources
- **Taiwan news sites**: Big5 encoded articles
- **Mainland forums**: GBK/GB18030 content
- **Wikipedia dumps**: Mixed UTF-8 with occasional mojibake
- **User submissions**: Files with claimed encoding ≠ actual
- **Legacy databases**: Migrated data with encoding issues

### Synthetic Tests
- **Minimal pairs**: Texts that differ only in ambiguous bytes
- **Binary edge**: Non-text data with valid encoding sequences
- **Truncation**: Cut off mid-character to test error handling
- **Concatenation**: Multiple encodings in one file

## Methodology

### Detection Accuracy
```python
# Labeled dataset with known encodings
test_cases = [
    ("中文", "utf-8"),
    (b'\xa4\xa4\xa4\xe5', "big5"),  # 中文 in Big5
    (b'\xd6\xd0\xce\xc4', "gb2312"),  # 中文 in GB2312
]

for data, expected in test_cases:
    detected = library.detect(data)
    correct = (detected['encoding'].lower() == expected.lower())
    accuracy_scores.append(correct)
```

### Performance Benchmarking
```python
import time
import psutil

def benchmark(library, data):
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024 / 1024  # MB

    start = time.time()
    result = library.detect(data)
    elapsed = time.time() - start

    mem_after = process.memory_info().rss / 1024 / 1024
    mem_used = mem_after - mem_before

    return {
        'time_ms': elapsed * 1000,
        'memory_mb': mem_used,
        'result': result
    }
```

### Mojibake Repair Testing
```python
# Known mojibake patterns
mojibake_tests = [
    ("ä¸­æ–‡", "中文", "Big5 as UTF-8"),
    ("â€œHello", "\"Hello", "Win-1252 smart quotes"),
    ("cafÃ©", "café", "Latin-1 é in UTF-8"),
]

for garbled, expected, pattern in mojibake_tests:
    fixed = ftfy.fix_text(garbled)
    success = (fixed == expected)
    results[pattern] = success
```

## Success Criteria

**S2 is complete when we have**:
1. Feature matrix comparing all 8 libraries
2. Benchmark results on 5+ file sizes × 5+ encodings
3. Accuracy percentages on labeled test set (100+ examples)
4. Edge case catalog with pass/fail for each library
5. Integration patterns with code examples
6. Error handling guide with recovery strategies

## Next Steps

1. Create feature comparison matrix
2. Set up benchmark harness
3. Build labeled test dataset
4. Run accuracy tests
5. Document integration patterns
6. Synthesize findings into recommendations
