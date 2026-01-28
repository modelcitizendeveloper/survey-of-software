# HanziConv (Hanzi Converter)

**Repository:** https://github.com/berniey/hanziconv
**PyPI Package:** https://pypi.org/project/hanziconv/
**GitHub Stars:** 189
**Primary Language:** Python (100% pure Python)
**Contributors:** 2
**Last Release:** v0.3.2
**License:** Apache 2.0

## Quick Assessment

- **Popularity:** ⭐⭐ Low-Medium (189 stars, modest PyPI downloads)
- **Maintenance:** ⚠️ Unclear (no recent activity visible)
- **Documentation:** ✅ Fair (basic README, simple API examples)
- **Language Support:** Python only (no bindings needed)

## Pros

✅ **Pure Python** - Zero native dependencies, works everywhere Python runs
✅ **Simple API** - Straightforward conversion functions, minimal configuration
✅ **Easy Installation** - `pip install hanziconv` just works, no C++ compiler needed
✅ **Lightweight** - Small package size, fast installation
✅ **CLI Tool Included** - Command-line utility `hanzi-convert` for shell scripts
✅ **Character Database** - Based on CUHK Multi-function Chinese Character Database

## Cons

❌ **Limited Maintenance** - Only 2 contributors, unclear if actively maintained
❌ **Character-Level Only** - No phrase-level conversion (less accurate for idioms)
❌ **Basic Regional Support** - Doesn't handle Taiwan/HK/Mainland vocabulary differences
❌ **Performance** - Pure Python is slower than C++ alternatives for large texts
❌ **No Advanced Features** - Missing variant selectors, proper noun detection
❌ **Small Community** - Low star count suggests limited production usage

## Quick Take

**Good for prototypes and simple use cases.** If you need to quickly add Traditional ↔ Simplified conversion to a Python project and don't want to deal with native dependencies, HanziConv gets the job done.

**Limitation:** This is character-level conversion, not phrase-level. That means:
- "头发" (hair) → might incorrectly convert 发
- Idioms may convert wrong
- Regional vocabulary differences ignored

For production applications handling significant Chinese text, the lack of phrase-level conversion is a deal-breaker.

**Use HanziConv if:**
- You need pure Python (no C++ dependencies allowed)
- Your conversion needs are simple (character-level is good enough)
- You're building a prototype or internal tool
- You want minimal installation friction

**Skip HanziConv if:**
- Accuracy matters (idioms, regional variants, proper nouns)
- You're processing large volumes of text (performance will suffer)
- You need active maintenance and community support

## Installation

```bash
pip install hanziconv
```

## Python Usage Example

```python
from hanziconv import HanziConv

# Simplified to Traditional
traditional = HanziConv.toTraditional("中国")
print(traditional)  # 中國

# Traditional to Simplified
simplified = HanziConv.toSimplified("中國")
print(simplified)  # 中国
```

## Command-Line Usage

```bash
# Convert file
hanzi-convert -i input.txt -o output.txt -m s2t

# Pipe usage
echo "中国" | hanzi-convert -m s2t
```

## S1 Verdict: FALLBACK OPTION

**Confidence:** Medium (70%)

HanziConv serves a niche: pure-Python environments where native dependencies are prohibited. It's a reasonable choice for:
- AWS Lambda with Python runtime (no build tools)
- Educational projects (students without C++ compilers)
- Quick scripts where accuracy isn't critical

However, for production applications, the lack of phrase-level conversion and unclear maintenance status make it a risky choice. OpenCC is significantly better if you can install it.

**Ranking:** #2 out of 3 (behind OpenCC, ahead of inactive zhconv)

---

**Sources:**
- [GitHub - berniey/hanziconv](https://github.com/berniey/hanziconv)
- [PyPI - hanziconv](https://pypi.org/project/hanziconv/)
- [Libraries.io - hanziconv](https://libraries.io/pypi/hanziconv)
