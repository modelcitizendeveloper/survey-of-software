# zhconv - Lightweight Chinese Conversion

## Overview

**Purpose**: Traditional ↔ Simplified Chinese conversion (lightweight alternative to OpenCC)
**PyPI**: `zhconv` - https://pypi.org/project/zhconv/
**GitHub**: https://github.com/gumblex/zhconv
**Type**: Pure Python
**Maintenance**: Active (2014-present)

## Key Difference from OpenCC

**zhconv is simpler and lighter**:
- Smaller dictionary (faster, less memory)
- Character-based conversion (not phrase-based like OpenCC)
- Single-pass conversion (OpenCC uses multi-pass)
- No regional vocabulary differences (just character mapping)

**Trade-off**: Less accurate for complex text, but faster and easier to embed.

## Basic Usage

```python
import zhconv

# Simplified to Traditional
simplified = "软件开发"
traditional = zhconv.convert(simplified, 'zh-hant')
print(traditional)  # 軟件開發

# Traditional to Simplified
traditional = "軟件開發"
simplified = zhconv.convert(traditional, 'zh-hans')
print(simplified)  # 软件开发
```

## Locale Variants

```python
import zhconv

text = "软件"

# Generic Traditional
print(zhconv.convert(text, 'zh-hant'))  # 軟件

# Taiwan variant
print(zhconv.convert(text, 'zh-tw'))  # 軟體

# Hong Kong variant
print(zhconv.convert(text, 'zh-hk'))  # 軟件

# Mainland Simplified
print(zhconv.convert(text, 'zh-cn'))  # 软件
```

## Strengths

- **Lightweight**: Small library, minimal dependencies
- **Fast**: Character-based mapping is quick
- **Simple API**: One function for all conversions
- **Locale support**: zh-cn, zh-tw, zh-hk, zh-sg, zh-hans, zh-hant
- **Pure Python**: No compilation needed

## Limitations

- **Less accurate**: No phrase context (e.g., 发 could be 髮 or 發)
- **No vocabulary conversion**: Doesn't change terms like 计算机→電腦
- **Simple mapping**: Can't handle ambiguous conversions well
- **Smaller dictionary**: Missing some rare characters

## When to Use

- **Simple conversion**: Just need character-level Traditional↔Simplified
- **Embedded systems**: Need lightweight library
- **Performance**: Faster than OpenCC for large batches
- **Good enough**: Accuracy isn't critical

## When to Use OpenCC Instead

- **Phrase context**: Need "發展" (develop) vs "頭髮" (hair)
- **Regional vocabulary**: 计算机→電腦 (computer), 信息→資訊 (information)
- **High accuracy**: Professional content, public-facing text
- **Complex documents**: Literary or technical text

## Comparison Example

```python
import zhconv
import opencc

text = "理发"  # "haircut" in Simplified

# zhconv (character-based)
result_zhconv = zhconv.convert(text, 'zh-hant')
print(result_zhconv)  # 理髮 (correct by luck)

# OpenCC (phrase-aware)
converter = opencc.OpenCC('s2t')
result_opencc = converter.convert(text)
print(result_opencc)  # 理髮 (correct by context)

# Ambiguous case
text2 = "发展"  # "develop" in Simplified

result_zhconv = zhconv.convert(text2, 'zh-hant')
print(result_zhconv)  # 髮展 (WRONG - used 髮 for hair)

result_opencc = converter.convert(text2)
print(result_opencc)  # 發展 (CORRECT - used 發 for develop)
```

## Real-World Use Case

```python
import zhconv

def quick_traditional_preview(simplified_text):
    """Quick Traditional preview for UI, not publication"""
    return zhconv.convert(simplified_text, 'zh-tw')

def search_normalization(text):
    """Convert all variants to Simplified for search indexing"""
    return zhconv.convert(text, 'zh-cn')
```

## Maintenance Status

- ✅ **Active**: Regular updates (2024)
- 📦 **PyPI**: `pip install zhconv`
- 🐍 **Python version**: 3.5+
- ⭐ **GitHub stars**: ~400
- 📥 **Downloads**: Moderate (thousands/month)

## Quick Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| CJK Coverage | ⭐⭐⭐ | Good for simple conversions |
| Performance | ⭐⭐⭐⭐⭐ | Fast, lightweight |
| Accuracy | ⭐⭐ | Character-based, misses context |
| Ease of Use | ⭐⭐⭐⭐⭐ | Very simple API |
| Maintenance | ⭐⭐⭐⭐ | Active |

## Verdict

**Fast and lightweight, but limited**. Use zhconv if you need quick Traditional↔Simplified conversion and accuracy isn't critical (search normalization, quick previews). For production content, professional documents, or user-facing text, use OpenCC instead.

**Best for**: Search indexing, internal tools, embedded systems
**Not for**: Publication, professional content, ambiguous text
**Complements**: Can use zhconv for bulk processing, then OpenCC for final polish
