# Feature Comparison: pypinyin vs dragonmapper

## Executive Summary

| Aspect | pypinyin | dragonmapper |
|--------|----------|--------------|
| **Primary Strength** | Comprehensive Pinyin styles & context awareness | Multi-system conversion & identification |
| **Best For** | Rich formatting needs, heteronym handling | IME tools, cross-system conversion |
| **API Complexity** | Moderate (many options) | Simple (focused scope) |
| **Maintenance** | Very active (2024+) | Stable/mature (v0.2.6) |

## Conversion Capabilities

### Pinyin Support

| Feature | pypinyin | dragonmapper |
|---------|----------|--------------|
| **Tone marks** | ✅ (default) | ✅ (default) |
| **Tone numbers (after)** | ✅ (TONE2: zho1ng) | ❌ |
| **Tone numbers (end)** | ✅ (TONE3: zhong1) | ✅ (ni3) |
| **No tones** | ✅ (NORMAL, lazy_pinyin) | ❌ |
| **First letter** | ✅ (FIRST_LETTER) | ❌ |
| **Initials only** | ✅ (INITIALS) | ❌ |
| **Finals only** | ✅ (FINALS variants) | ❌ |
| **Heteronym handling** | ✅ Context-aware | ⚠️ Dictionary-based only |
| **Custom pronunciations** | ✅ (load_phrases_dict) | ❌ |

**Winner**: pypinyin for Pinyin flexibility and sophistication

### Zhuyin (Bopomofo) Support

| Feature | pypinyin | dragonmapper |
|---------|----------|--------------|
| **Chinese → Zhuyin** | ✅ (Style.BOPOMOFO) | ✅ (to_zhuyin) |
| **Pinyin → Zhuyin** | ⚠️ Indirect (via characters) | ✅ Direct conversion |
| **Zhuyin → Pinyin** | ❌ | ✅ Direct conversion |
| **Tone marks** | ✅ | ✅ |
| **Syllable spacing** | Manual | Automatic |

**Winner**: dragonmapper for Pinyin ↔ Zhuyin bidirectional conversion

### Other Transcription Systems

| Feature | pypinyin | dragonmapper |
|---------|----------|--------------|
| **IPA** | ❌ | ✅ Full support |
| **Cyrillic** | ✅ | ❌ |

**Tie**: Each has unique additional systems

## Identification & Detection

| Feature | pypinyin | dragonmapper |
|---------|----------|--------------|
| **Detect transcription type** | ❌ | ✅ (identify) |
| **Validate Pinyin** | ❌ | ✅ (is_pinyin) |
| **Validate Zhuyin** | ❌ | ✅ (is_zhuyin) |
| **Identify character type** | ❌ | ✅ (Traditional/Simplified) |
| **Check for Chinese** | ❌ | ✅ (has_chinese) |

**Winner**: dragonmapper (unique capability)

## API Design

### pypinyin API
```python
# Style-based approach
from pypinyin import pinyin, lazy_pinyin, Style

pinyin('中心', style=Style.BOPOMOFO)
pinyin('中心', style=Style.TONE3, heteronym=True)
lazy_pinyin('中心')  # Convenience function
```

**Characteristics**:
- Style enum for consistency
- Separate functions for different use cases (pinyin vs lazy_pinyin)
- Many options, steeper learning curve
- Consistent pattern across all styles

### dragonmapper API
```python
# Module-based approach
from dragonmapper import hanzi, transcriptions

hanzi.to_zhuyin('中心')
transcriptions.pinyin_to_zhuyin('zhōngxīn')
transcriptions.identify('ㄓㄨㄥ')
```

**Characteristics**:
- Clear module separation (character vs transcription)
- Explicit function names
- Simpler API surface
- Intuitive for transcription conversion tasks

**Preference**: Depends on use case. pypinyin better for character conversion with many formats; dragonmapper better for transcription-to-transcription work.

## Performance & Resources

### Memory Usage

| Aspect | pypinyin | dragonmapper |
|--------|----------|--------------|
| **Base memory** | Moderate | Moderate |
| **Phrase database** | Large (for context) | N/A |
| **Optimization options** | ✅ (env vars) | ❌ |
| **Data loaded** | pinyin-data, phrase-pinyin-data | CC-CEDICT, Unihan |

**Winner**: pypinyin (configurable memory footprint)

### Processing Speed
*Note: No benchmarking data available in initial research. Both should be adequate for typical use cases.*

**Assumption**: pypinyin may be slower for heteronym-heavy text due to context analysis. dragonmapper likely faster for simple transcription conversion.

## Developer Experience

### Documentation

| Aspect | pypinyin | dragonmapper |
|--------|----------|--------------|
| **Official docs** | pypinyin.rtfd.io | dragonmapper.readthedocs.io |
| **Examples** | Extensive | Good |
| **API reference** | Complete | Complete |
| **Tutorials** | ✅ | ✅ |

**Tie**: Both well-documented

### CLI Tools

| Tool | pypinyin | dragonmapper |
|------|----------|--------------|
| **Command-line interface** | ✅ (`pypinyin`) | ❌ |

**Winner**: pypinyin

### Community & Ecosystem

| Aspect | pypinyin | dragonmapper |
|--------|----------|--------------|
| **GitHub stars** | Higher | Lower |
| **Recent commits** | Active (2024+) | Stable/mature |
| **Issue activity** | Active | Lower |
| **Cross-platform ports** | JS, Go, Rust, C++, C# | Python-only |
| **PyPI downloads** | Higher | Lower |

**Winner**: pypinyin (more active community)

## Edge Cases & Quirks

### pypinyin Quirks
- Neutral tone syllables lack indicators
- lazy_pinyin uses 'v' for 'ü' by default
- Strict vs non-strict mode for initials ('y', 'w')
- Requires phrase context for accurate heteronym disambiguation

### dragonmapper Quirks
- Loads dictionaries into memory on first use (startup delay)
- Automatic spacing in Zhuyin output (may or may not be desired)
- Limited to CC-CEDICT coverage (no custom pronunciations)
- Less sophisticated heteronym handling

## Licensing & Attribution

| Aspect | pypinyin | dragonmapper |
|--------|----------|--------------|
| **License** | MIT | MIT |
| **Attribution needed** | Check data sources | Check CC-CEDICT, Unihan |
| **Commercial use** | ✅ | ✅ |

**Tie**: Both MIT, commercially friendly

## Use Case Matrix

### When to Choose pypinyin
- ✅ Need multiple Pinyin output styles (tone variants, initials/finals)
- ✅ Working primarily with Chinese characters → romanization
- ✅ Context-aware heteronym handling is critical
- ✅ Building Chinese learning applications
- ✅ Need Cyrillic output
- ✅ Want a CLI tool
- ✅ Need to customize pronunciation dictionaries

### When to Choose dragonmapper
- ✅ Converting between existing romanizations (Pinyin ↔ Zhuyin)
- ✅ Building IME (Input Method Editor) tools
- ✅ Need to detect/identify transcription systems
- ✅ Working with IPA
- ✅ Need to distinguish Traditional vs Simplified programmatically
- ✅ Processing text that may already be romanized
- ✅ Prefer simpler, more focused API

### When to Use Both
Consider using both libraries together:
- pypinyin for character → Pinyin/Zhuyin
- dragonmapper for Pinyin ↔ Zhuyin conversion and system identification

This combines pypinyin's superior character conversion with dragonmapper's transcription flexibility.

## Verdict by Use Case Category

| Use Case | Recommendation | Rationale |
|----------|----------------|-----------|
| **General-purpose converter** | pypinyin | More styles, better heteronyms |
| **IME backend** | dragonmapper | Direct transcription conversion |
| **Language learning app** | pypinyin | Context awareness, multiple formats |
| **Data cleaning pipeline** | dragonmapper | System identification |
| **Search indexing** | pypinyin | Multiple output styles for matching |
| **Transcription converter** | dragonmapper | Core strength |
| **Mobile app (memory-constrained)** | pypinyin w/ optimization | Configurable memory |
| **Research/linguistics** | Both | Complementary capabilities |
