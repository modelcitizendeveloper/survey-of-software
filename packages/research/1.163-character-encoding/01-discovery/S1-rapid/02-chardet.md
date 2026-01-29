# chardet - Character Encoding Detection

## Overview

**Purpose**: Automatic character encoding detection using statistical analysis
**PyPI**: `chardet` - https://pypi.org/project/chardet/
**GitHub**: https://github.com/chardet/chardet
**Type**: Pure Python port of Mozilla's Universal Charset Detector
**Maintenance**: Stable but slow development (original algorithm from 2000s)

## CJK Support

**Detectable encodings**:
- Big5 (Traditional Chinese)
- GB2312/GBK (Simplified Chinese)
- EUC-TW, EUC-KR, EUC-JP (East Asian)
- Shift-JIS, ISO-2022-JP (Japanese)
- Various Unicode encodings (UTF-8, UTF-16, UTF-32)

**Detection method**: Statistical analysis of byte patterns
- Measures frequency of character sequences
- Uses language-specific models
- Returns confidence score (0-1)

## Basic Usage

```python
import chardet

# Detect encoding of bytes
with open('unknown.txt', 'rb') as f:
    raw_data = f.read()

result = chardet.detect(raw_data)
print(result)
# {'encoding': 'GB2312', 'confidence': 0.99, 'language': 'Chinese'}

# Decode with detected encoding
text = raw_data.decode(result['encoding'])
```

## Incremental Detection

```python
from chardet.universaldetector import UniversalDetector

detector = UniversalDetector()
with open('large_file.txt', 'rb') as f:
    for line in f:
        detector.feed(line)
        if detector.done:
            break
detector.close()

print(detector.result)
# {'encoding': 'big5', 'confidence': 0.95}
```

## Real-World Example

```python
def safe_read_file(filepath):
    """Read file with unknown encoding"""
    with open(filepath, 'rb') as f:
        raw_data = f.read()

    detection = chardet.detect(raw_data)
    encoding = detection['encoding']
    confidence = detection['confidence']

    if confidence < 0.7:
        print(f"Warning: Low confidence ({confidence}) for {encoding}")

    return raw_data.decode(encoding, errors='replace')
```

## Strengths

- **Language support**: Covers major East Asian encodings
- **Confidence scores**: Tells you how sure it is
- **Incremental API**: Can detect from streaming data
- **Industry standard**: Mozilla algorithm, battle-tested
- **Language hints**: Can detect language as well as encoding

## Limitations

- **Performance**: Pure Python, slow on large files (100KB+ takes seconds)
- **Accuracy**: 80-95% depending on text length and content
- **Short text**: Needs 50+ bytes for reliable detection
- **Similar encodings**: Confuses Big5/GB2312/GBK (overlapping byte ranges)
- **UTF-8 bias**: May over-detect UTF-8 in ambiguous cases
- **Maintenance**: Minimal updates since 2019

## When to Use

- **Unknown encoding**: Files from users, scraped content, legacy systems
- **Moderate file sizes**: <1MB files where speed isn't critical
- **Need confidence**: Want to know how certain the detection is
- **Pure Python**: Can't use C extensions

## When to Look Elsewhere

- **Performance**: Large files → use `cchardet` (C version)
- **Better accuracy**: Modern algorithm → use `charset-normalizer`
- **Known encoding**: Use stdlib `codecs` directly
- **Already garbled**: Detection won't help → use `ftfy` to repair

## Maintenance Status

- ⚠️ **Maintenance mode**: Last significant update 2019
- 📦 **PyPI**: `pip install chardet`
- 🐍 **Python version**: 3.6+
- ⭐ **GitHub stars**: ~2k
- 📥 **Downloads**: Very popular (millions/month as dependency)

## Quick Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| CJK Coverage | ⭐⭐⭐⭐ | Good East Asian support |
| Performance | ⭐⭐ | Pure Python, slow |
| Accuracy | ⭐⭐⭐ | 80-95%, struggles with short text |
| Ease of Use | ⭐⭐⭐⭐⭐ | Simple API |
| Maintenance | ⭐⭐ | Stable but minimal updates |

## Verdict

**Historical standard, now superseded**. Chardet was the go-to library for a decade, but it's showing age. For new projects, consider `charset-normalizer` (better accuracy) or `cchardet` (better performance). Still useful as a dependency-free option if you need pure Python.

**Migration path**: Drop-in replacement with `charset-normalizer` or `cchardet` (same API).
