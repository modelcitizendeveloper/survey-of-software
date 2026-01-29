# dragonmapper

## Basic Information
- **Package Name**: dragonmapper
- **Repository**: tsroten/dragonmapper
- **Latest Version**: 0.2.6
- **License**: MIT
- **PyPI**: https://pypi.org/project/dragonmapper/
- **GitHub**: https://github.com/tsroten/dragonmapper
- **Documentation**: https://dragonmapper.readthedocs.io/

## What It Does
Provides identification and conversion functions for Chinese text processing across multiple transcription systems.

## Key Features
- **Multi-system support**: Pinyin (accented and numbered), Zhuyin (Bopomofo), IPA
- **Bidirectional conversion**: Convert between any of the supported systems
- **Text identification**: Can identify whether a string is Traditional/Simplified Chinese, Pinyin, Zhuyin, or IPA
- **Two main modules**:
  - `dragonmapper.hanzi`: Chinese characters → romanization
  - `dragonmapper.transcriptions`: Conversion between romanization systems

## Zhuyin Support
**YES** - Full bidirectional support

Example:
```python
pinyin_to_zhuyin('Wǒ shì yīgè měiguórén.')
# Returns: 'ㄨㄛˇ ㄕˋ ㄧ ㄍㄜˋ ㄇㄟˇ ㄍㄨㄛˊ ㄖㄣˊ.'
```

## First Impression
More focused on transcription system conversion than character-to-Pinyin conversion. The ability to convert between Pinyin and Zhuyin (both directions) is a distinguishing feature. The identification capability is unique among the three libraries.

## Quick Assessment
- ✅ Pinyin conversion: Yes (via hanzi module)
- ✅ Zhuyin conversion: Yes (bidirectional!)
- ✅ Pinyin ↔ Zhuyin: Direct conversion without going through hanzi
- ❓ Heteronym handling: Not mentioned in initial research
- ✅ Text identification: Unique feature
- ❓ Maintenance status: Version 0.2.6 (needs verification of recency)

## Potential Use Cases
- Applications needing to switch between transcription systems
- Text processing pipelines that work with mixed romanization formats
- Tools that need to identify which transcription system is in use

## Sources
- [dragonmapper PyPI](https://pypi.org/project/dragonmapper/)
- [GitHub repository](https://github.com/tsroten/dragonmapper)
- [Official documentation](https://dragonmapper.readthedocs.io/)
