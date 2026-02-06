# OpenCC - Traditional/Simplified Chinese Conversion

## Overview

**Purpose**: Convert between Traditional and Simplified Chinese with variant handling
**PyPI**: `opencc-python-reimplemented` - https://pypi.org/project/opencc-python-reimplemented/
**Original**: OpenCC C++ library (https://github.com/BYVoid/OpenCC)
**Type**: Pure Python reimplementation
**Maintenance**: Active (2015-present)

## What Problem Does It Solve?

**Traditional ↔ Simplified conversion is NOT simple character substitution**:

1. **One-to-many mappings**: 髮/發 (traditional) both become 发 (simplified)
2. **Regional variants**: Taiwan uses 台灣, Mainland uses 台湾 (different character for 台)
3. **Vocabulary differences**: "software" is 軟體 (Taiwan) vs 软件 (Mainland)
4. **Idiom localization**: "bus" is 公車 (Taiwan) vs 公交车 (Mainland)

OpenCC handles these using dictionaries and context-aware conversion.

## Conversion Presets

**Built-in conversions**:
- `s2t` - Simplified to Traditional Chinese (OpenCC standard)
- `t2s` - Traditional to Simplified Chinese (OpenCC standard)
- `s2tw` - Simplified to Taiwan Traditional
- `tw2s` - Taiwan Traditional to Simplified
- `s2hk` - Simplified to Hong Kong Traditional
- `hk2s` - Hong Kong Traditional to Simplified
- `t2tw` - Traditional to Taiwan standard
- `tw2t` - Taiwan standard to Traditional

## Basic Usage

```python
import opencc

# Create converter
converter = opencc.OpenCC('s2t')  # Simplified to Traditional

# Convert text
simplified = "软件开发"
traditional = converter.convert(simplified)
print(traditional)  # 軟件開發

# Reverse
converter_back = opencc.OpenCC('t2s')
result = converter_back.convert(traditional)
print(result)  # 软件开发
```

## Regional Variants

```python
import opencc

text = "软件"  # "software" in Simplified

# To Traditional (generic)
conv_t = opencc.OpenCC('s2t')
print(conv_t.convert(text))  # 軟件

# To Taiwan variant
conv_tw = opencc.OpenCC('s2tw')
print(conv_tw.convert(text))  # 軟體 (Taiwan prefers 體 over 件)

# To Hong Kong variant
conv_hk = opencc.OpenCC('s2hk')
print(conv_hk.convert(text))  # 軟件 (HK uses 件)
```

## Vocabulary Conversion

```python
import opencc

# Taiwan vs Mainland vocabulary
text_mainland = "计算机软件"  # Mainland: "computer software"
conv = opencc.OpenCC('s2tw')
text_taiwan = conv.convert(text_mainland)
print(text_taiwan)  # 電腦軟體 (Taiwan uses different words)

# Taiwan to Mainland
text_tw = "資訊安全"  # Taiwan: "information security"
conv2 = opencc.OpenCC('tw2s')
text_cn = conv2.convert(text_tw)
print(text_cn)  # 信息安全 (Mainland uses 信息 not 資訊)
```

## Batch Processing

```python
import opencc

def convert_file(input_file, output_file, config='s2t'):
    """Convert entire file"""
    converter = opencc.OpenCC(config)

    with open(input_file, 'r', encoding='utf-8') as f_in:
        content = f_in.read()

    converted = converter.convert(content)

    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write(converted)
```

## Strengths

- **Context-aware**: Uses phrase dictionaries, not just character mapping
- **Regional variants**: Taiwan, Hong Kong, Mainland differences
- **Vocabulary conversion**: Handles regional terminology differences
- **Reversible**: Can convert back and forth (with some loss)
- **Well-tested**: Large dictionary, actively maintained
- **Pure Python**: Reimplemented version needs no C compiler

## Limitations

- **Not perfect**: One-to-many mappings can't be fully reversed
- **Context limited**: Doesn't understand full sentence semantics
- **Regional edge cases**: Some terms have no clear mapping
- **Performance**: Pure Python version slower than C++ original
- **Dictionary size**: Large memory footprint

## When to Use

- **Content localization**: Website for Taiwan vs Mainland audiences
- **Search normalization**: Match searches across variants
- **Document conversion**: Migrate content between regions
- **Data cleaning**: Standardize to one variant for processing

## When to Look Elsewhere

- **Just encoding**: Use stdlib `codecs` (Big5 ↔ GB2312 is NOT the same as Traditional ↔ Simplified)
- **Machine translation**: OpenCC is conversion, not translation
- **Encoding detection**: Use `chardet`/`charset-normalizer`
- **Already garbled**: Use `ftfy` to repair mojibake first

## C++ vs Python Version

**opencc-python-reimplemented** (Pure Python):
- ✅ No compilation needed
- ✅ Easy to install
- ⚠️ Slower (~10x than C++)
- ⚠️ Higher memory usage

**opencc (C++ binding)**:
- ✅ Fast
- ✅ Lower memory
- ⚠️ Requires compilation
- ⚠️ Platform-specific builds

## Real-World Example

```python
import opencc
from pathlib import Path

def localize_for_taiwan(content):
    """Convert Mainland Chinese content for Taiwan readers"""
    converter = opencc.OpenCC('s2tw')
    return converter.convert(content)

def process_bilingual_site(content_dir):
    """Generate Taiwan variant from Simplified originals"""
    converter = opencc.OpenCC('s2tw')

    for md_file in Path(content_dir).glob('**/*.md'):
        # Read Simplified Chinese content
        with open(md_file, 'r', encoding='utf-8') as f:
            simplified_content = f.read()

        # Convert to Taiwan Traditional
        traditional_content = converter.convert(simplified_content)

        # Write to parallel directory
        tw_file = md_file.parent / 'tw' / md_file.name
        tw_file.parent.mkdir(exist_ok=True)
        with open(tw_file, 'w', encoding='utf-8') as f:
            f.write(traditional_content)
```

## Maintenance Status

- ✅ **Active**: Regular updates (2024-2025)
- 📦 **PyPI**: `pip install opencc-python-reimplemented`
- 🐍 **Python version**: 3.6+
- ⭐ **GitHub stars**: ~1k (Python version), ~8k (C++ original)
- 📥 **Downloads**: Moderate (tens of thousands/month)

## Quick Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| CJK Coverage | ⭐⭐⭐⭐⭐ | Best-in-class Traditional↔Simplified |
| Performance | ⭐⭐⭐ | Pure Python is slower |
| Accuracy | ⭐⭐⭐⭐ | Context-aware, large dictionary |
| Ease of Use | ⭐⭐⭐⭐⭐ | Simple API |
| Maintenance | ⭐⭐⭐⭐ | Active development |

## Verdict

**Essential for Chinese content**. If you work with Chinese text and need to serve multiple regions (Taiwan, Hong Kong, Mainland), OpenCC is the standard tool. Not a replacement for encoding libraries (you still need proper UTF-8/Big5/GB handling), but solves the semantic conversion problem.

**Use case**: Content localization, not encoding conversion
**Complements**: charset-normalizer (detection) → stdlib codecs (transcode to UTF-8) → OpenCC (Traditional↔Simplified)
