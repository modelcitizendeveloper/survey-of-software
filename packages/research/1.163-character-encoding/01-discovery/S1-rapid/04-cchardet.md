# cchardet - Fast Encoding Detection

## Overview

**Purpose**: High-performance character encoding detection (C extension)
**PyPI**: `cchardet` - https://pypi.org/project/cchardet/
**GitHub**: https://github.com/PyYoshi/cChardet
**Type**: C extension wrapping uchardet (Mozilla's C++ library)
**Maintenance**: Sporadic updates, mostly stable

## Key Advantage

**Speed**: 10-100x faster than `chardet` on large files
- chardet: ~2MB/sec (pure Python)
- cchardet: ~50MB/sec (C extension)

Same detection algorithm as chardet (Mozilla Universal Charset Detector), but implemented in C.

## CJK Support

**Same as chardet**:
- Big5, GB2312, GBK, GB18030
- EUC-TW, EUC-KR, EUC-JP
- Shift-JIS, ISO-2022-JP
- UTF-8, UTF-16, UTF-32

**Detection quality**: Identical to chardet (same algorithm)

## Basic Usage

```python
import cchardet

# Detect encoding
with open('large_file.txt', 'rb') as f:
    raw_data = f.read()

result = cchardet.detect(raw_data)
print(result)
# {'encoding': 'GB2312', 'confidence': 0.99}

# Decode
text = raw_data.decode(result['encoding'])
```

## Drop-in Replacement for chardet

```python
# Works with existing chardet code
try:
    import cchardet as chardet  # Use fast version if available
except ImportError:
    import chardet  # Fallback to pure Python

result = chardet.detect(data)
```

## Performance Comparison

```python
import time
import chardet
import cchardet

# 10MB test file
with open('big_data.txt', 'rb') as f:
    data = f.read()

# chardet
start = time.time()
result1 = chardet.detect(data)
print(f"chardet: {time.time() - start:.2f}s")  # ~5 seconds

# cchardet
start = time.time()
result2 = cchardet.detect(data)
print(f"cchardet: {time.time() - start:.2f}s")  # ~0.1 seconds

# Same result
assert result1['encoding'] == result2['encoding']
```

## Strengths

- **Performance**: 10-100x faster than chardet
- **Same algorithm**: Proven Mozilla detector
- **Drop-in replacement**: Compatible API
- **Low memory**: C implementation is memory-efficient
- **Batch processing**: Ideal for processing thousands of files

## Limitations

- **C extension**: Requires compilation (no pure Python fallback)
- **Platform support**: May not work on exotic platforms
- **Same accuracy as chardet**: Not improved, just faster (80-95%)
- **Maintenance**: Less active than charset-normalizer
- **No coherence checking**: Doesn't have charset-normalizer's improvements

## When to Use

- **Large files**: Multi-MB files, hundreds of KB
- **Batch processing**: Processing many files
- **Performance critical**: Encoding detection in hot path
- **Known to work**: Files similar to chardet training set

## When to Look Elsewhere

- **Need accuracy**: charset-normalizer has better detection
- **Small files**: Speed difference negligible on <100KB
- **Pure Python required**: Can't compile C extensions
- **Already garbled**: Use `ftfy` to repair mojibake

## Installation Considerations

```bash
# May need build tools
pip install cchardet

# On some systems:
# apt-get install python3-dev build-essential
# yum install python3-devel gcc-c++
```

**Wheels available**: Most common platforms have pre-built wheels on PyPI (Linux, macOS, Windows)

## Real-World Example

```python
import cchardet
from pathlib import Path
import sys

def batch_convert_to_utf8(input_dir, output_dir):
    """Convert directory of mixed-encoding files to UTF-8"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    for filepath in input_path.glob('**/*.txt'):
        with open(filepath, 'rb') as f:
            raw_data = f.read()

        # Fast detection
        result = cchardet.detect(raw_data)
        if result['confidence'] < 0.7:
            print(f"Skipping {filepath}: low confidence", file=sys.stderr)
            continue

        # Convert to UTF-8
        text = raw_data.decode(result['encoding'], errors='replace')
        out_file = output_path / filepath.name
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"{filepath.name}: {result['encoding']} → UTF-8")
```

## Maintenance Status

- ⚠️ **Sporadic**: Updates every 6-12 months
- 📦 **PyPI**: `pip install cchardet`
- 🐍 **Python version**: 3.6+
- ⭐ **GitHub stars**: ~680
- 📥 **Downloads**: Popular (hundreds of thousands/month)
- 🏗️ **Build**: Requires C++ compiler (but wheels available)

## Quick Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| CJK Coverage | ⭐⭐⭐⭐ | Same as chardet |
| Performance | ⭐⭐⭐⭐⭐ | 10-100x faster than chardet |
| Accuracy | ⭐⭐⭐ | Same as chardet (80-95%) |
| Ease of Use | ⭐⭐⭐⭐ | Drop-in replacement |
| Maintenance | ⭐⭐⭐ | Stable but infrequent updates |

## Verdict

**Speed champion**. If you're processing large files or batches and chardet is too slow, cchardet is the obvious choice. Same algorithm, same API, 10-100x faster. But if accuracy matters more than speed, consider charset-normalizer instead.

**Best for**: Batch ETL pipelines, web crawlers, large file processing
**Trade-off**: Speed vs accuracy (charset-normalizer is more accurate but slower)
