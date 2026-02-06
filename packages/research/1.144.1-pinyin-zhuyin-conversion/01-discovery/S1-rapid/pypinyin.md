# pypinyin

## Basic Information
- **Package Name**: pypinyin
- **Repository**: mozillazg/python-pinyin
- **Latest Version**: 0.55.0
- **License**: MIT
- **PyPI**: https://pypi.org/project/pypinyin/
- **GitHub**: https://github.com/mozillazg/python-pinyin

## What It Does
Converts Chinese characters (hanzi) to Pinyin romanization with comprehensive support for multiple output styles.

## Key Features
- **Multiple Pinyin styles**: Tone marks, tone numbers, first letters, initials/finals separation
- **Zhuyin (Bopomofo) support**: `Style.BOPOMOFO` option
- **Polyphonic character handling**: Intelligently detects heteronyms and matches correct pronunciation based on context
- **Word-based context**: Analyzes word groups for more accurate pronunciation selection

## Zhuyin Support
**YES** - Direct support via `Style.BOPOMOFO`

Example:
```python
pinyin('中心', style=Style.BOPOMOFO)
# Returns: [['ㄓㄨㄥ'], ['ㄒㄧㄣ']]
```

## First Impression
Most feature-rich library of the three. Comprehensive style options make it flexible for various use cases. The heteronym detection suggests sophisticated linguistic processing.

## Quick Assessment
- ✅ Pinyin conversion: Full support
- ✅ Zhuyin conversion: Native support
- ✅ Active maintenance: Latest version from 2024+
- ✅ Heteronym handling: Yes
- ❓ API complexity: Appears moderate (multiple style options)

## Sources
- [pypinyin PyPI](https://pypi.org/project/pypinyin/)
- [python-pinyin README](https://github.com/mozillazg/python-pinyin/blob/master/README_en.rst)
- [x-cmd package info](https://www.x-cmd.com/pkg/pypinyin/)
