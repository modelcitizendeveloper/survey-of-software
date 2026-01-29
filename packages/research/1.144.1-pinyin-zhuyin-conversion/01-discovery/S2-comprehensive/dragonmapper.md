# dragonmapper - Comprehensive Analysis

## Package Information
- **PyPI**: dragonmapper
- **Repository**: tsroten/dragonmapper
- **Latest Version**: 0.2.6
- **License**: MIT
- **Documentation**: https://dragonmapper.readthedocs.io/
- **Focus**: Multi-system transcription identification and conversion

## Installation
```bash
pip install dragonmapper
```

## Core Architecture

### Two Main Modules

**1. dragonmapper.hanzi** - Character processing
- Identifies character types (Traditional/Simplified)
- Converts Chinese characters to transcription systems
- Loads CC-CEDICT and Unihan data into memory

**2. dragonmapper.transcriptions** - Transcription conversion
- Identifies which transcription system is in use
- Converts between Pinyin, Zhuyin, and IPA
- **Does NOT require Chinese character input** - works with romanizations directly

### Data Sources
- **CC-CEDICT**: Open-source Chinese-English dictionary
- **Unihan Database**: Unicode Han character database

## Transcription Systems Supported
1. **Pinyin** (accented and numbered variants)
2. **Zhuyin** (Bopomofo)
3. **IPA** (International Phonetic Alphabet)

## API Patterns

### Character Identification (hanzi module)

```python
from dragonmapper import hanzi

# Identify character types
hanzi.identify('繁體字')  # Returns: Traditional
hanzi.identify('简体字')  # Returns: Simplified
hanzi.identify('繁简字')  # Returns: Mixed

# Boolean checks
hanzi.is_traditional('繁體字')  # True
hanzi.is_simplified('简体字')   # True
hanzi.has_chinese('Hello 你好')  # True
```

### Character to Transcription (hanzi module)

```python
# To Pinyin (with tone marks)
hanzi.to_pinyin('你好')  # 'nǐhǎo'

# To Pinyin (numbered tones)
hanzi.to_pinyin('你好', accented=False)  # 'ni3hao3'

# To Zhuyin
hanzi.to_zhuyin('你好')  # 'ㄋㄧˇ ㄏㄠˇ'

# To IPA
hanzi.to_ipa('你好')  # IPA representation
```

### Transcription Identification (transcriptions module)

```python
from dragonmapper import transcriptions

# Identify transcription system
transcriptions.identify('nǐhǎo')      # Returns: Pinyin
transcriptions.identify('ㄋㄧˇ ㄏㄠˇ')  # Returns: Zhuyin
transcriptions.identify('[ni xau]')   # Returns: IPA

# Boolean validation
transcriptions.is_pinyin('nǐhǎo')     # True
transcriptions.is_zhuyin('ㄋㄧˇ')      # True
transcriptions.is_ipa('[ni]')        # True
```

### Transcription Conversion (transcriptions module)

**Pinyin ↔ Zhuyin** (Bidirectional):
```python
# Pinyin to Zhuyin
transcriptions.pinyin_to_zhuyin('Wǒ shì yīgè měiguórén.')
# Returns: 'ㄨㄛˇ ㄕˋ ㄧ ㄍㄜˋ ㄇㄟˇ ㄍㄨㄛˊ ㄖㄣˊ.'

# Single syllable
transcriptions.pinyin_syllable_to_zhuyin('nǐ')  # 'ㄋㄧˇ'

# Zhuyin to Pinyin
transcriptions.zhuyin_to_pinyin('ㄋㄧˇ ㄏㄠˇ')  # 'nǐ hǎo'

# Single syllable
transcriptions.zhuyin_syllable_to_pinyin('ㄋㄧˇ')  # 'nǐ'
```

**Pinyin Variant Conversion**:
```python
# Numbered to accented
transcriptions.numbered_syllable_to_accented('ni3')  # 'nǐ'

# Accented to numbered
transcriptions.accented_syllable_to_numbered('nǐ')   # 'ni3'
```

**IPA Conversions**:
- Bidirectional with Pinyin: `pinyin_to_ipa()`, `ipa_to_pinyin()`
- Bidirectional with Zhuyin: `zhuyin_to_ipa()`, `ipa_to_zhuyin()`

## Unique Capabilities

### 1. Direct Transcription Conversion
**Key differentiator**: Can convert between transcription systems WITHOUT going through Chinese characters.

```python
# Convert Pinyin to Zhuyin directly
transcriptions.pinyin_to_zhuyin('zhōngwén')  # 'ㄓㄨㄥ ㄨㄣˊ'
```

This is useful for:
- Processing text that's already romanized
- Converting between input methods
- Working with mixed-source data

### 2. Transcription System Detection
**Unique feature**: Automatically identify which system is in use.

```python
text = user_input()
system = transcriptions.identify(text)

if system == 'Pinyin':
    process_pinyin(text)
elif system == 'Zhuyin':
    process_zhuyin(text)
```

### 3. Character Type Identification
Distinguish Traditional vs Simplified Chinese programmatically.

## Edge Cases & Behavior

### Tone Mark Placement (Pinyin)
Follows standard Pinyin rules:
1. Priority: 'a' > 'e' > 'o'
2. If none of above, uses final vowel

### Zhuyin Spacing
- `to_zhuyin()` adds spaces between syllables automatically
- Single syllable functions preserve spacing control

### Validation vs Conversion
- `is_*()` functions validate individual syllables
- Conversion functions process full text with spacing

## Dependencies
- Requires CC-CEDICT and Unihan data (bundled with package)
- Data loaded into memory on first use

## Maintenance Status
- **Version**: 0.2.6 (stable)
- **Activity**: Less frequent updates than pypinyin
- **Maturity**: Feature-complete for stated scope
- **Forks**: Some community forks (e.g., TTWNO/dragonmapper)

## Strengths
✅ Bidirectional Pinyin ↔ Zhuyin conversion
✅ Works with romanizations directly (no Chinese text needed)
✅ Transcription system identification
✅ Character type identification (Traditional/Simplified)
✅ IPA support (unique among the three libraries)
✅ Clean, focused API
✅ Multiple transcription systems in one library

## Limitations
⚠️ No context-aware heteronym handling (simpler than pypinyin)
⚠️ Less frequent updates/maintenance
⚠️ No style variants (just one format per system)
⚠️ Memory overhead from loading dictionaries
⚠️ No CLI tool

## Ideal Use Cases
- Applications working with multiple transcription systems
- Tools that need to detect/identify romanization formats
- Systems that process existing romanized text (not raw Chinese)
- IME (Input Method Editor) backends
- Cross-system conversion utilities
- Educational tools teaching different romanization systems
- Data cleaning pipelines with mixed romanization formats

## Comparison to pypinyin

| Feature | pypinyin | dragonmapper |
|---------|----------|--------------|
| Pinyin styles | 13+ variants | 2 variants (accented, numbered) |
| Zhuyin support | Yes (via Style.BOPOMOFO) | Yes (primary feature) |
| Pinyin ↔ Zhuyin | Indirect (via characters) | Direct conversion |
| Heteronym handling | Context-aware | Dictionary-based only |
| System identification | No | Yes |
| IPA support | No | Yes |
| CLI tool | Yes | No |

## When to Choose dragonmapper Over pypinyin
1. You need direct Pinyin ↔ Zhuyin conversion without Chinese text
2. You're building an IME or input conversion tool
3. You need to identify which transcription system is in use
4. You need IPA support
5. You prefer a focused, stable API over extensive options
