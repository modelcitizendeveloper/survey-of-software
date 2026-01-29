# uchardet - Universal Charset Detection

## Overview

**Purpose**: Character encoding detection (C library binding)
**PyPI**: `uchardet` - https://pypi.org/project/uchardet/
**Upstream**: https://www.freedesktop.org/wiki/Software/uchardet/
**Type**: Python binding to Mozilla's uchardet C library
**Maintenance**: Stable but minimal updates

## Relationship to Other Libraries

**The family tree**:
1. **universalchardet** (original Mozilla C++ code)
2. **uchardet** (C library maintained by freedesktop.org)
3. **chardet** (pure Python port)
4. **cchardet** (Python binding to uchardet)
5. **This library** (also binds to uchardet)

**uchardet vs cchardet**: Both bind to the same C library (uchardet), slightly different Python APIs.

## CJK Support

Same as chardet/cchardet (Mozilla algorithm):
- Big5, GB2312, GBK, GB18030
- EUC-TW, EUC-KR, EUC-JP
- Shift-JIS, ISO-2022-JP
- UTF-8, UTF-16, UTF-32

## Basic Usage

```python
import uchardet

# Detect encoding
with open('unknown.txt', 'rb') as f:
    data = f.read()

encoding = uchardet.detect(data)
print(encoding)
# {'encoding': 'GB2312', 'confidence': 0.99}

# Decode
text = data.decode(encoding['encoding'])
```

## Incremental Detection

```python
import uchardet

detector = uchardet.Detector()

with open('large_file.txt', 'rb') as f:
    for line in f:
        detector.feed(line)
        if detector.done:
            break

result = detector.result
print(result)  # {'encoding': 'big5', 'confidence': 0.95}
```

## uchardet vs cchardet

**Both use the same C library** (freedesktop.org uchardet), but:

**uchardet package**:
- Direct binding to system uchardet library
- Or bundles uchardet if not found
- API: `uchardet.detect(data)` returns dict

**cchardet package**:
- Always bundles uchardet (no system dependency)
- API: `cchardet.detect(data)` returns dict (compatible with chardet)

**In practice**: cchardet is more popular because:
- Drop-in chardet replacement
- More downloads/usage
- Bundled library (no system deps)

## Strengths

- **Performance**: C implementation, fast
- **System integration**: Can use system uchardet library
- **Same algorithm**: Mozilla detector, proven
- **Low-level access**: Can tweak detection parameters

## Limitations

- **Less popular**: cchardet has more users/support
- **API differences**: Not a drop-in chardet replacement
- **Platform quirks**: System library version may vary
- **Same accuracy**: 80-95% (doesn't improve on algorithm)

## When to Use

- **System uchardet available**: Want to use OS package
- **Low-level control**: Need to tweak detection
- **Already using uchardet**: System has it installed

## When to Use Alternatives

- **Drop-in chardet**: Use cchardet instead
- **Better accuracy**: Use charset-normalizer
- **Pure Python**: Use chardet
- **Standard API**: cchardet is more common

## Comparison

| Feature | chardet | cchardet | uchardet | charset-normalizer |
|---------|---------|----------|----------|-------------------|
| Speed | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Accuracy | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Pure Python | ✅ | ❌ | ❌ | ✅ |
| Drop-in API | N/A | ✅ | ❌ | ✅ |
| Popularity | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |

## Real-World Example

```python
import uchardet

def detect_and_decode(filepath):
    """Detect encoding and decode file"""
    with open(filepath, 'rb') as f:
        data = f.read()

    result = uchardet.detect(data)

    if result['confidence'] < 0.7:
        print(f"Warning: Low confidence {result['confidence']}")

    return data.decode(result['encoding'], errors='replace')
```

## Maintenance Status

- ⚠️ **Stable**: Minimal updates (reflects upstream uchardet)
- 📦 **PyPI**: `pip install uchardet`
- 🐍 **Python version**: 3.6+
- ⭐ **GitHub stars**: ~130 (Python binding)
- 📥 **Downloads**: Moderate (lower than cchardet)

## Quick Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| CJK Coverage | ⭐⭐⭐⭐ | Same as chardet/cchardet |
| Performance | ⭐⭐⭐⭐⭐ | Fast C implementation |
| Accuracy | ⭐⭐⭐ | Mozilla algorithm (80-95%) |
| Ease of Use | ⭐⭐⭐ | Different API from chardet |
| Maintenance | ⭐⭐⭐ | Stable, tracks upstream |

## Verdict

**Works but less popular than cchardet**. Both uchardet and cchardet bind to the same C library (freedesktop.org uchardet), but cchardet has:
- More users
- Drop-in chardet compatibility
- More PyPI downloads

Unless you specifically need system uchardet library integration, use **cchardet** instead for the same performance with better ecosystem support.

**Recommendation**: Skip this, use cchardet or charset-normalizer
