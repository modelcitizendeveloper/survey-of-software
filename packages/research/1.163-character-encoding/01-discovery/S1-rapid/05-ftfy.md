# ftfy - Fixes Text For You

## Overview

**Purpose**: Repair mojibake (garbled text from encoding errors)
**PyPI**: `ftfy` - https://pypi.org/project/ftfy/
**GitHub**: https://github.com/rspeer/python-ftfy
**Type**: Pure Python
**Maintenance**: Active (2015-present)

## What Problem Does It Solve?

**Mojibake**: Text that's been decoded with the wrong encoding, then re-encoded, possibly multiple times.

**Common scenarios**:
- Decoded Big5 as UTF-8: `中文` → `ä¸­æ–‡`
- Double UTF-8 encoding: `"Hello"` → `â€œHelloâ€`
- Windows-1252 in UTF-8 pipeline: `café` → `cafÃ©`
- Latin-1 misinterpretation: `你好` → `ä½ å¥½`

ftfy analyzes the garbled text and tries to reverse the encoding mistakes.

## Basic Usage

```python
import ftfy

# Simple repair
garbled = "ä¸­æ–‡"  # 中文 decoded as UTF-8 when it was Big5
fixed = ftfy.fix_text(garbled)
print(fixed)  # 中文

# Explain what was fixed
result = ftfy.fix_and_explain(garbled)
print(result.fixed)  # 中文
print(result.fixes)  # Shows steps taken
```

## Real-World Examples

### Double UTF-8 Encoding

```python
# Common in web scraping
garbled = "â€œHelloâ€"
fixed = ftfy.fix_text(garbled)
print(fixed)  # "Hello"
```

### CJK Mojibake

```python
# Big5 decoded as UTF-8
garbled = "ä¸­æ–‡æª"æ¡ˆ"
fixed = ftfy.fix_text(garbled)
print(fixed)  # 中文檔案

# GB2312 in Latin-1 pipeline
garbled = "Ä¿Â¼Â¼Â¯"
fixed = ftfy.fix_text(garbled)  # Attempts repair
```

### HTML Entities

```python
# Incorrectly escaped HTML
garbled = "&lt;hello&gt;"
fixed = ftfy.fix_text(garbled)
print(fixed)  # <hello>

# Numeric entities
garbled = "&#20013;&#25991;"
fixed = ftfy.fix_text(garbled)
print(fixed)  # 中文
```

## Advanced: Explain Fixes

```python
from ftfy import fix_and_explain

garbled = "ä¸­æ–‡"
result = fix_and_explain(garbled)

print(f"Original: {garbled}")
print(f"Fixed: {result.fixed}")
print(f"Fixes applied: {result.fixes}")
# Fixes applied: ['unescape_html', 'decode_inconsistent_utf8']
```

## Configuration

```python
import ftfy

# Don't fix HTML entities
fixed = ftfy.fix_text(garbled, unescape_html=False)

# Don't normalize Unicode
fixed = ftfy.fix_text(garbled, normalization=None)

# Preserve case
fixed = ftfy.fix_text(garbled, fix_latin_ligatures=False)
```

## What It Can Fix

- **Encoding mixups**: UTF-8 decoded as Latin-1, Big5 as UTF-8, etc.
- **Double encoding**: Multiple rounds of UTF-8 encoding
- **HTML entities**: Incorrectly escaped `&lt;`, `&#20013;`, etc.
- **Unicode normalization**: NFC/NFD inconsistencies
- **Control characters**: Removes invisible characters
- **Latin ligatures**: `ﬁ` → `fi`

## What It Cannot Fix

- **Lost information**: If bytes were actually corrupted/truncated
- **Unknown original encoding**: Needs to guess the encoding chain
- **Complex encoding chains**: >3 layers of mistakes
- **Semantic errors**: Wrong characters that happen to be valid

## Strengths

- **Automatic**: Just call `fix_text()`, it tries everything
- **Explains**: Shows what fixes were applied
- **Conservative**: Won't "fix" things that aren't broken
- **CJK aware**: Handles common CJK mojibake patterns
- **Pure Python**: No C dependencies

## Limitations

- **Not magic**: Can't fix everything, especially complex chains
- **Heuristic-based**: May misidentify some patterns
- **Performance**: Tries many possibilities, slower on large text
- **False positives**: Rare cases where "fix" makes it worse

## When to Use

- **Text is already garbled**: You see mojibake characters
- **Unknown encoding history**: Don't know the mistake chain
- **User-submitted content**: Database with mixed-up encodings
- **Legacy data migration**: Old systems with encoding issues
- **Web scraping**: Sites with broken charset declarations

## When to Look Elsewhere

- **Known encoding**: Use stdlib `codecs` to transcode correctly
- **Detection needed**: Use `chardet`/`charset-normalizer` first
- **Prevention**: Fix the source of encoding errors
- **Binary data**: ftfy is for text only

## Real-World Workflow

```python
import ftfy
from charset_normalizer import from_bytes

def rescue_garbled_file(filepath):
    """Try to rescue a file with encoding issues"""
    # First, try detection
    with open(filepath, 'rb') as f:
        raw_data = f.read()

    result = from_bytes(raw_data)
    if result.best():
        text = str(result.best())
    else:
        # Detection failed, try as UTF-8
        text = raw_data.decode('utf-8', errors='replace')

    # Now repair mojibake
    fixed = ftfy.fix_text(text)
    return fixed
```

## Maintenance Status

- ✅ **Active**: Regular updates (2024-2025)
- 📦 **PyPI**: `pip install ftfy`
- 🐍 **Python version**: 3.8+
- ⭐ **GitHub stars**: ~3.7k
- 📥 **Downloads**: Very popular (millions/month)
- 🧪 **Testing**: Extensive test suite with real-world examples

## Quick Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| CJK Coverage | ⭐⭐⭐⭐ | Handles common CJK mojibake |
| Performance | ⭐⭐⭐ | Moderate, tries many fixes |
| Accuracy | ⭐⭐⭐⭐ | Good for common cases |
| Ease of Use | ⭐⭐⭐⭐⭐ | Single function call |
| Maintenance | ⭐⭐⭐⭐⭐ | Active, well-maintained |

## Verdict

**Essential repair tool**. If you have garbled text and don't know the encoding history, ftfy is your best bet. It won't fix everything, but it handles common mojibake patterns well. Use *after* detection fails or when you know text is already garbled.

**Complements**: charset-normalizer (detection) + ftfy (repair) is a powerful combo
**Not a substitute**: Prevention (correct encoding handling) is better than repair
