# xpinyin

## Basic Information
- **Package Name**: xpinyin
- **Repository**: lxneng/xpinyin
- **Latest Version**: 0.7.7
- **License**: MIT
- **PyPI**: https://pypi.org/project/xpinyin/
- **GitHub**: https://github.com/lxneng/xpinyin

## What It Does
Translates Chinese hanzi to Pinyin romanization with a focus on simplicity and flexibility.

## Key Features
- **Tone formats**: Both tone marks (shàng-hǎi) and tone numbers (shang4-hai3)
- **Customizable separators**: Default hyphen, but can be changed or removed
- **Initial extraction**: Can extract initial consonants separately
- **Polyphone handling**: `get_pinyins()` method for multiple readings (added in v0.7.0)
- **Python version support**: >=3.6 for latest version, 0.5.7 for older Python

## Zhuyin Support
**NO** - Only Pinyin romanization, no Zhuyin (Bopomofo) output

## First Impression
Simpler, more straightforward API than pypinyin. Good for basic Pinyin needs but lacks the comprehensive style options and Zhuyin support. The polyphone support is a positive feature but not as sophisticated as pypinyin's context-aware heteronym handling.

## Quick Assessment
- ✅ Pinyin conversion: Full support
- ❌ Zhuyin conversion: No support
- ✅ Tone formats: Multiple options (marks and numbers)
- ✅ Polyphone handling: Yes (get_pinyins)
- ✅ API simplicity: Appears simplest of the three
- ❓ Context awareness: Not mentioned (likely less sophisticated than pypinyin)

## Verdict for This Research
**Not suitable** for the scope of this research since it lacks Zhuyin support. Included for completeness but will not be carried forward to S2-comprehensive analysis.

## Potential Use Cases (Pinyin-only)
- Simple Pinyin conversion tools
- Applications that only need basic romanization
- Projects where Zhuyin is not required

## Sources
- [xpinyin PyPI](https://pypi.org/project/xpinyin/)
- [GitHub repository](https://github.com/lxneng/xpinyin)
- [Libraries.io listing](https://libraries.io/pypi/xpinyin)
