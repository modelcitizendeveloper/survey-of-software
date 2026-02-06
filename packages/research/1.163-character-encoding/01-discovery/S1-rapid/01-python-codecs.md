# Python Codecs (Standard Library)

## Overview

**Purpose**: Built-in encoding/decoding for 100+ character encodings
**Type**: Standard library module (no installation needed)
**Maintenance**: Part of Python core, continuously maintained

## CJK Support

**Encodings supported**:
- `big5` - Traditional Chinese (Taiwan)
- `big5hkscs` - Hong Kong variant with Supplementary Character Set
- `gb2312` - Simplified Chinese (basic)
- `gbk` - Simplified Chinese (extended)
- `gb18030` - Simplified Chinese (full Unicode coverage, mandatory in China)
- `shift_jis`, `euc_jp`, `iso2022_jp` - Japanese
- `euc_kr`, `johab` - Korean

**Key features**:
- Direct `bytes.decode(encoding)` and `str.encode(encoding)` API
- Error handling modes: `strict`, `ignore`, `replace`, `backslashreplace`
- `codecs.open()` for file I/O with automatic encoding
- Incremental codecs for streaming data

## Basic Usage

```python
# Decoding bytes to string
big5_bytes = b'\xa4\xa4\xa4\xe5'  # "中文" in Big5
text = big5_bytes.decode('big5')
print(text)  # 中文

# Encoding string to bytes
text = "简体中文"
gb_bytes = text.encode('gb2312')
gb18030_bytes = text.encode('gb18030')

# Error handling
malformed = b'\xff\xfe'
safe_text = malformed.decode('big5', errors='replace')  # Uses � for invalid bytes

# File I/O with encoding
import codecs
with codecs.open('data.txt', 'r', encoding='big5') as f:
    content = f.read()
```

## Transcoding Example

```python
# Big5 file → UTF-8 file
with open('input.txt', 'rb') as f_in:
    big5_bytes = f_in.read()

text = big5_bytes.decode('big5')
utf8_bytes = text.encode('utf-8')

with open('output.txt', 'wb') as f_out:
    f_out.write(utf8_bytes)
```

## Strengths

- **Zero dependencies**: Built into Python, always available
- **Wide encoding coverage**: 100+ encodings including obscure ones
- **Well documented**: Part of Python standard library docs
- **Stable API**: Won't break between Python versions
- **Performance**: C implementation for most codecs

## Limitations

- **No encoding detection**: Must know encoding beforehand
- **No mojibake repair**: Can't fix double-encoded text
- **No variant conversion**: Can't convert Traditional↔Simplified Chinese
- **Limited error recovery**: Strict/ignore/replace are blunt tools
- **Big5 quirks**: `big5` codec has known issues with some characters, `big5hkscs` is better but still incomplete

## When to Use

- **Known encoding**: You have metadata (HTML charset, file header, API docs)
- **Transcoding**: Convert between encodings reliably
- **Standard encodings**: Big5, GBK, GB18030, Shift-JIS are well supported
- **No dependencies**: Can't add external libraries

## When to Look Elsewhere

- **Unknown encoding**: Need detection → use `chardet`/`charset-normalizer`
- **Mojibake repair**: Text already garbled → use `ftfy`
- **Traditional↔Simplified**: Need semantic conversion → use `OpenCC`/`zhconv`
- **Variant handling**: Need CJK unification → specialized libraries

## Maintenance Status

- ✅ **Active**: Part of Python core, continuously maintained
- 📦 **Availability**: Built-in, no PyPI package needed
- 🐍 **Python version**: All versions (3.7+)

## Quick Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| CJK Coverage | ⭐⭐⭐⭐ | Good support for common encodings |
| Performance | ⭐⭐⭐⭐⭐ | C implementation, very fast |
| Ease of Use | ⭐⭐⭐⭐⭐ | Simple, Pythonic API |
| Detection | ⭐ | No encoding detection |
| Repair | ⭐ | No mojibake repair |

## Verdict

**Must-have foundation**. Every Python developer uses these codecs, but they solve only half the problem (transcoding with known encodings). Combine with detection libraries (`chardet`/`charset-normalizer`) for unknown encodings and repair libraries (`ftfy`) for mojibake.
