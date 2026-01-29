# charset-normalizer - Modern Encoding Detection

## Overview

**Purpose**: Character encoding detection with improved accuracy and Unicode normalization
**PyPI**: `charset-normalizer` - https://pypi.org/project/charset-normalizer/
**GitHub**: https://github.com/Ousret/charset-normalizer
**Type**: Pure Python with optional C acceleration
**Maintenance**: Active development (2019-present)

## Key Improvements Over chardet

1. **Better accuracy**: 95%+ detection rate (vs 80-95% for chardet)
2. **Unicode normalization**: Handles NFD/NFC/NFKD/NFKC variants
3. **Modern algorithm**: Uses coherence analysis, not just frequency tables
4. **Multiple candidates**: Returns ranked list of possible encodings
5. **Explanations**: Shows why each encoding was chosen

## CJK Support

**Detectable encodings**:
- All encodings that chardet supports
- Better disambiguation of Big5 vs GBK vs GB2312
- UTF-8 variants with different normalizations
- Handles mixed encodings better

**Coherence checking**:
- Analyzes whether decoded text makes linguistic sense
- Detects when characters form valid CJK words
- Reduces false positives on binary data

## Basic Usage

```python
from charset_normalizer import from_bytes, from_path

# Detect from bytes
with open('unknown.txt', 'rb') as f:
    raw_data = f.read()

results = from_bytes(raw_data)
best_guess = results.best()

print(f"Encoding: {best_guess.encoding}")
print(f"Confidence: {best_guess.encoding_confidence}")
print(f"Text: {best_guess.output()}")
```

## Advanced: Multiple Candidates

```python
from charset_normalizer import from_bytes

with open('ambiguous.txt', 'rb') as f:
    raw_data = f.read()

results = from_bytes(raw_data)

# Iterate over all candidates
for match in results:
    print(f"{match.encoding}: {match.encoding_confidence:.2%}")
    print(f"  First 100 chars: {str(match)[:100]}")
    print()

# Output:
# utf-8: 98.50%
#   First 100 chars: 这是UTF-8编码的文本...
# gb2312: 45.20%
#   First 100 chars: è¿™æ˜¯UTF-8ç¼...
```

## File Path Convenience

```python
from charset_normalizer import from_path

results = from_path('data.txt')
best = results.best()

if best is None:
    print("Could not detect encoding")
else:
    # Already decoded text
    text = str(best)
```

## Strengths

- **Higher accuracy**: Outperforms chardet on benchmarks
- **Explainable**: Shows reasoning for detection
- **Multiple candidates**: Lets you choose if top guess is wrong
- **Unicode aware**: Handles normalization forms
- **Drop-in replacement**: Compatible with chardet API
- **Active maintenance**: Regular updates, bug fixes

## Limitations

- **Performance**: Slower than chardet (more thorough analysis)
- **Memory**: Uses more RAM for coherence analysis
- **Overkill for simple cases**: If you know it's UTF-8 vs Big5, stdlib is faster
- **Not a C extension**: Slower than `cchardet` on very large files

## When to Use

- **Accuracy critical**: Financial data, medical records, legal documents
- **Ambiguous encodings**: Files that might be Big5 or GBK
- **Need explanations**: Want to understand why encoding was chosen
- **Modern codebase**: Can afford slightly slower but more accurate detection

## When to Look Elsewhere

- **Performance critical**: Large files → use `cchardet`
- **Known encoding**: Use stdlib `codecs`
- **Already garbled**: Use `ftfy` to repair mojibake

## Real-World Example

```python
from charset_normalizer import from_bytes
import sys

def robust_file_reader(filepath):
    """Read file with encoding detection and fallback"""
    with open(filepath, 'rb') as f:
        raw_data = f.read()

    results = from_bytes(raw_data)
    best = results.best()

    if best is None:
        print("Could not detect encoding", file=sys.stderr)
        return None

    if best.encoding_confidence < 0.8:
        print(f"Low confidence ({best.encoding_confidence:.2%})", file=sys.stderr)
        print(f"Alternatives:", file=sys.stderr)
        for match in results:
            print(f"  {match.encoding}: {match.encoding_confidence:.2%}", file=sys.stderr)

    return str(best)
```

## Maintenance Status

- ✅ **Active**: Regular releases in 2024-2025
- 📦 **PyPI**: `pip install charset-normalizer`
- 🐍 **Python version**: 3.7+
- ⭐ **GitHub stars**: ~2.5k
- 📥 **Downloads**: Very popular (as urllib3 dependency)
- 🏆 **Used by**: requests, urllib3 (replacing chardet)

## Quick Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| CJK Coverage | ⭐⭐⭐⭐⭐ | Excellent East Asian support |
| Performance | ⭐⭐⭐ | Moderate, slower than cchardet |
| Accuracy | ⭐⭐⭐⭐⭐ | Best-in-class detection |
| Ease of Use | ⭐⭐⭐⭐⭐ | Simple and powerful API |
| Maintenance | ⭐⭐⭐⭐⭐ | Very active |

## Verdict

**Modern default choice**. If you're starting a new project that needs encoding detection, use this. Better accuracy than chardet, actively maintained, used by major projects like `requests`. Only choose `cchardet` if performance on large files is critical.

**Replaces**: chardet (directly), auto-detection in file readers
