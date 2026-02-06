# S1 Rapid: Radical & Component Analysis Ecosystem Scan

**Status**: Discovery research (no code execution)
**Created**: 2026-01-28
**Purpose**: Quick ecosystem scan for Chinese character radical decomposition and component analysis

---

## Overview

Chinese character decomposition involves breaking down characters (汉字/漢字) into their constituent parts: radicals (部首), components, and stroke sequences. This is essential for:

- **Etymology**: Understanding character origins and historical development
- **Mnemonic generation**: Creating memory aids for language learners
- **Character learning progression**: Building curriculum from simple to complex components
- **Computational linguistics**: Enabling character-aware NLP applications

---

## Key Standards & Data Sources

### 1. Unihan Database (Unicode Consortium)

**Source**: [Unicode Han Database (UAX #38)](https://www.unicode.org/reports/tr38/)

The official Unicode Han Database provides comprehensive data for all unified CJK ideographs:

- **Radical-Stroke Data**: Based on 214 Kangxi radicals system (18th century)
  - Format: `kRSUnicode` and `kRSAdobe_Japan1_6` fields
  - Structure: radical number + residual stroke count
  - Example: Character 地 = Radical 土 (32) + 3 residual strokes

- **Interactive Access**: [Unihan Database Lookup](https://www.unicode.org/charts/unihan.html)
- **Radical Index**: [Unihan Radical-Stroke Index](http://www.unicode.org/charts/unihanrsindex.html)
- **Development**: [GitHub repository](https://github.com/unicode-org/unihan-database) for expert review

**Key Fields**:
- `kRSUnicode`: Radical-stroke count
- `kCangjie`: Cangjie input method codes
- `kPhonetic`: Phonetic component information
- `kSemanticVariant`: Semantic variant mappings

### 2. IDS (Ideographic Description Sequences)

**Source**: [Unicode Standard Chapter 18](https://en.wikipedia.org/wiki/Ideographic_Description_Characters_(Unicode_block))

IDS provides a standardized way to represent character composition using Unicode operators (U+2FF0..U+2FFB):

- **Purpose**: Describe characters in featural terms by arrangement of components
- **Operators**: 12 special characters (⿰, ⿱, ⿲, etc.) for spatial arrangement
  - ⿰ (U+2FF0): Left-to-right composition
  - ⿱ (U+2FF1): Top-to-bottom composition
  - ⿲ (U+2FF2): Left-middle-right composition
  - etc.

**Examples**:
- 地 → ⿰土也 (left-right: 土 + 也)
- 花 → ⿱艹化 (top-bottom: 艹 + 化)

**Technical Constraints**:
- Maximum sequence length: 16 Unicode code points
- Useful for describing unencoded characters or characters missing from fonts

**Main IDS Database**: [CJKVI-IDS on GitHub](https://github.com/cjkvi/cjkvi-ids) - Comprehensive IDS data for CJK Unified Ideographs

### 3. Phonetic-Semantic Compounds (形聲字)

**Concept**: 80% of Chinese characters are phonetic-semantic compounds combining:
- **Semantic radical (義符)**: Indicates meaning category
- **Phonetic component (聲符)**: Provides pronunciation hint

**Key Resources**:
- [Hacking Chinese: Phonetic Components Guide](https://www.hackingchinese.com/phonetic-components-part-1-the-key-to-80-of-all-chinese-characters/)
- [Wikipedia: Chinese character internal structures](https://en.wikipedia.org/wiki/Chinese_character_internal_structures)

**Research Databases**:
- **Hsiao & Shillcock (2006)**: Chinese lexical database with phonetic compound decomposition into semantic/phonetic radicals
  - Published in [Journal of Psycholinguistic Research](https://link.springer.com/article/10.1007/s10936-006-9022-y)
  - Includes Cangjie stroke pattern decomposition
  - Contains pronunciation and frequency data

---

## Python Libraries & Tools

### 1. **cjklib** (Most Comprehensive)

**PyPI**: [cjklib](https://pypi.org/project/cjklib/)
**Docs**: [cjklib.characterlookup](https://cjklib.readthedocs.io/en/0.3.2/library/cjklib.characterlookup.html)

**Capabilities**:
- Character decomposition using IDS (Ideographic Description Sequences)
- Radical lookups (Kangxi radical system)
- Stroke decomposition
- Variant character information
- Pronunciation data (Pinyin, Wade-Giles, Cantonese, etc.)
- Glyph component analysis

**Database Storage**: IDS stored in SQLite database with Unicode IDS operators

**Maintenance Status**: Last release 0.3.2 (check PyPI for latest)

### 2. **hanzipy**

**GitHub**: [Synkied/hanzipy](https://github.com/Synkied/hanzipy)

**Purpose**: Chinese character NLP framework for language learners

**Features**:
- Character decomposition into radicals/components
- Learning-focused API
- Framework for character exploration

**Target Audience**: Language learners and educational applications

### 3. **makemeahanzi** (Data Only)

**GitHub**: [skishore/makemeahanzi](https://github.com/skishore/makemeahanzi)
**Web**: [Make Me a Hanzi](https://www.skishore.me/makemeahanzi/)

**Format**: JSON data files, not a Python library

**Data Sources**: Derived from Unihan and cjklib

**Content**:
- Character etymology (type: ideographic/pictographic/pictophonetic)
- Phonetic/semantic component breakdowns
- Stroke order data
- Open-source, free to use

### 4. **cjk-decomp** (Decomposition Data)

**GitHub**: [amake/cjk-decomp](https://github.com/amake/cjk-decomp)

**Scope**: Decomposition data for 75,000+ CJK ideographs
- 36 stroke types
- 115 radicals
- 20,924 unified characters
- Extension sets (Ext-A, Ext-B, etc.)

**Format**: Data files (not a Python library, but can be parsed)

---

## Web-Based Resources

### Reference & Etymology

1. **[Zhongwen.com](https://zhongwen.com/)**: Character genealogies (zipu) showing interconnections between 4000+ characters based on Shuowen Jiezi
2. **[Arch Chinese Radicals](https://www.archchinese.com/arch_chinese_radicals.html)**: Interactive radical reference
3. **[Dong Chinese Wiki](https://www.dong-chinese.com/wiki)**: Character wiki with etymological information
4. **[Multi-function Chinese Character Database (漢語多功能字庫)](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/)**: University of Hong Kong free online dictionary with character origins

### Technical References

1. **[BabelStone IDS Database](https://www.babelstone.co.uk/CJK/IDS.HTML)**: UTF-8 encoded plain text IDS for all CJK Unified Ideographs
2. **[CJKVI GitHub Organization](https://github.com/cjkvi)**: Multiple databases (IDS, variants, etc.)

---

## Quick Assessment

### Strengths

✅ **Unicode Standard Foundation**: Unihan is official, comprehensive, regularly maintained
✅ **IDS Standardization**: Structural decomposition with standardized operators
✅ **Multiple Python Options**: From comprehensive (cjklib) to learner-focused (hanzipy)
✅ **Open Data Available**: makemeahanzi, cjk-decomp, CJKVI-IDS all freely accessible
✅ **Rich Academic Research**: Hsiao & Shillcock database, phonetic compound research

### Gaps & Considerations

⚠️ **Library Maintenance**: Need to verify current maintenance status of cjklib, hanzipy
⚠️ **Data Quality**: Different sources may have conflicting decompositions (historical vs. modern)
⚠️ **Traditional vs. Simplified**: Need to handle both character sets
⚠️ **Variant Forms**: Regional variants (China, Taiwan, Hong Kong, Japan, Korea) complicate decomposition

---

## Next Steps for S2-S4

**S2 Comprehensive**:
- Deep dive into cjklib API and database schema
- Compare IDS coverage across CJKVI-IDS vs. BabelStone vs. cjklib
- Analyze phonetic-semantic compound databases (Hsiao & Shillcock data)
- Review academic literature on character decomposition approaches

**S3 Need-Driven**:
- Generic use cases: etymology lookup, mnemonic generation, learning progression
- Pattern: "Given character X, find all components"
- Pattern: "Given radical Y, find all characters containing it"
- Pattern: "Find phonetic series (characters sharing phonetic component)"

**S4 Strategic**:
- Unicode Consortium maintenance trajectory
- Python library ecosystem health
- Integration with modern NLP pipelines (transformers, embeddings)
- Traditional vs. simplified character handling strategies

---

**Sources**:
- [UAX #38: Unicode Han Database](https://www.unicode.org/reports/tr38/)
- [Unihan Database Lookup](https://www.unicode.org/charts/unihan.html)
- [Ideographic Description Characters (Wikipedia)](https://en.wikipedia.org/wiki/Ideographic_Description_Characters_(Unicode_block))
- [CJKVI-IDS GitHub](https://github.com/cjkvi/cjkvi-ids)
- [cjklib PyPI](https://pypi.org/project/cjklib/)
- [Hacking Chinese: Phonetic Components](https://www.hackingchinese.com/phonetic-components-part-1-the-key-to-80-of-all-chinese-characters/)
- [Analysis of a Chinese Phonetic Compound Database](https://link.springer.com/article/10.1007/s10936-006-9022-y)
- [Make Me a Hanzi](https://www.skishore.me/makemeahanzi/)
