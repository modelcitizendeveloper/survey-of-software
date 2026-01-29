# Stroke Order Data Sources: Comprehensive Catalog

**Research ID**: research-k6iy
**Date**: 2026-01-29
**Pass**: S2 (Comprehensive Coverage)
**Purpose**: Complete catalog of SVG stroke order data, stroke count databases, and animated dictionary resources for CJK characters

---

## 1. SVG Stroke Order Data Sources

### 1.1 Make Me a Hanzi (Chinese Characters)

**Repository**: [skishore/makemeahanzi](https://github.com/skishore/makemeahanzi)
**Website**: [makemeahanzi](https://www.skishore.me/makemeahanzi/)
**Coverage**: 9,000+ most common simplified and traditional Chinese characters
**License**: Multiple (see repository for details)

**Key Features**:
- Stroke-order vector graphics for all characters
- Dictionary data (definitions, pinyin)
- Graphical data (stroke decomposition)
- Experimental animated SVGs (svgs.tar.gz)
- SVGs named by Unicode codepoint

**Data Format**:
- `dictionary.txt` - character definitions, pronunciations
- `graphics.txt` - stroke order and decomposition data
- `svgs.tar.gz` - pre-rendered animated SVG files

**Use Cases**:
- Foundation for building stroke order animation systems
- Reference for stroke decomposition algorithms
- Educational apps requiring accurate stroke order

---

### 1.2 KanjiVG (Japanese Kanji)

**Repository**: [KanjiVG/kanjivg](https://github.com/KanjiVG/kanjivg)
**Website**: [kanjivg.tagaini.net](https://kanjivg.tagaini.net/)
**Coverage**: Japanese kanji characters
**License**: Creative Commons Attribution-Share Alike 3.0

**Key Features**:
- SVG file for each character with stroke shape and direction
- Stroke order information
- Component metadata (radicals, stroke types)
- Variant forms included
- Widely adopted (used by Duolingo, many dictionary sites)

**Distribution**:
- Zip file with all non-variant SVG files
- Individual files in repository
- Vector graphics suitable for scaling

**Notable Users**:
- Duolingo (language learning platform)
- Multiple Japanese dictionary websites
- Educational apps for kanji learning

---

### 1.3 HanziVG (Chinese Hanzi)

**Repository**: [Connum/hanzivg](https://github.com/Connum/hanzivg)
**Goal**: Become for Chinese what KanjiVG is for Japanese
**Coverage**: Traditional and Simplified Chinese characters

**Key Features**:
- SVG stroke order files with metadata
- Radical information
- Character component decomposition
- Modeled after KanjiVG structure

**Status**: Active development, growing coverage

---

### 1.4 animCJK (Multi-Language)

**Repository**: [parsimonhi/animCJK](https://github.com/parsimonhi/animCJK)
**Coverage**: Chinese, Japanese (Kanji + Kana), Korean (Hanja)
**Total Characters**: 7,672+ in Chinese simplified folder

**Key Features**:
- Animated stroke order using SVG
- Free and open-source
- Multi-language support (CJK)
- Organized by language:
  - `svgsZhHans/` - Simplified Chinese (7,000 common + uncommon)
  - Traditional Chinese variants
  - Japanese Kanji and Kana
  - Korean Hanja
  - Basic strokes and components

**Use Cases**:
- Universal CJK character applications
- Cross-language learning platforms
- Comparative stroke order analysis

---

### 1.5 Hanzi Writer (JavaScript Library + Data)

**Repository**: [chanind/hanzi-writer](https://github.com/chanind/hanzi-writer)
**Website**: [hanziwriter.org](https://hanziwriter.org/)
**Data Explorer**: [chanind.github.io/hanzi-writer-data](https://chanind.github.io/hanzi-writer-data/)
**Type**: JavaScript library with accompanying SVG data

**Key Features**:
- Free and open-source library for stroke order animations
- Based on Make Me a Hanzi data
- HTML5 + SVG rendering
- Stroke order practice quizzes
- Embeddable in web applications
- Character data in separate repository

**Technical Stack**:
- JavaScript/TypeScript
- SVG rendering
- No backend required

**Use Cases**:
- Web-based character writing practice
- Interactive quizzes
- Browser-based learning applications

---

## 2. Online Animated Dictionaries

### 2.1 strokeorder.info

**URL**: [strokeorder.info](http://www.strokeorder.info/)
**Format**: Animated GIFs
**Coverage**: 4,000+ characters

**Features**:
- Pre-rendered animated GIFs
- Instant playback (no JavaScript required)
- Easy to embed in static sites

---

### 2.2 strokeorder.com

**URL**: [strokeorder.com](https://www.strokeorder.com/)

**Features**:
- Type-to-animate interface
- Automatic playback on character entry
- Interactive stroke order display

---

### 2.3 Chinese Character Web API

**URL**: [ccdb.hemiola.com](http://ccdb.hemiola.com/)
**Type**: RESTful API
**Data Source**: Unihan Database (MySQL + PHP)

**Key Features**:
- 20,902 characters (CJK Unified Ideographs range)
- Stroke count information
- Radical lookup (kRSKangXi field)
- Programmatic access

**Use Cases**:
- Backend for dictionary apps
- Automated stroke count lookup
- Character metadata retrieval

---

## 3. Stroke Count Databases

### 3.1 Chinese Character Stroke Count Resources

**GitHub Repository**: [caiguanhao/ChineseStrokes](https://github.com/caiguanhao/ChineseStrokes)
**Coverage**: 81,000+ Chinese characters
**Purpose**: Sort characters by stroke count

**Key Features**:
- Comprehensive stroke count data
- Suitable for dictionary lookup systems
- Enables stroke-based search

**Use Cases**:
- Implement radical/stroke lookup in dictionaries
- Sort characters by complexity
- Character learning progression systems

---

### 3.2 Unihan Database (kTotalStrokes)

**Source**: Unicode Consortium
**Coverage**: 101,996 CJK unified ideographs (as of Unicode 17.0)
**Field**: `kTotalStrokes`

**Note**: Some errors exist in the data. Cross-reference recommended.

**Access Methods**:
- Direct download from Unicode.org
- Via libraries (cjklib, Python)
- Through APIs (CCDB)

---

### 3.3 cjklib (Python Library)

**PyPI**: [cjklib](https://pypi.org/project/cjklib/)
**Documentation**: [cjklib.readthedocs.io](https://cjklib.readthedocs.io/en/0.3.2/library/cjklib.characterlookup.html)

**Key Features**:
- Language routines for Han characters (Chinese, Japanese, Korean, Vietnamese)
- Character pronunciations
- Radical information
- Glyph component analysis
- Stroke decomposition
- Variant information
- Locale-aware stroke counts (simplified vs. traditional)

**Important**: Stroke counts can vary by locale (traditional vs. simplified Chinese)

**Use Cases**:
- Building Python-based dictionary tools
- Linguistic analysis
- Character decomposition systems

---

### 3.4 KRADFILE/RADKFILE (Kanji Radical Decomposition)

**Maintainer**: Electronic Dictionary Research and Development Group (EDRDG)
**Website**: [edrdg.org/krad/kradinf.html](https://www.edrdg.org/krad/kradinf.html)
**License**: EDRDG License
**Coverage**: 6,355+ kanji (JIS X 0208-1997) + 5,801 (JIS X 0212)

**Key Features**:
- Kanji decomposition into visual elements/radicals
- Enables radical-based lookup
- KRADFILE: Kanji → Radicals mapping
- RADKFILE: Radicals → Kanji mapping (inverted, used by lookup software)

**Historical Context**:
- Initial work by Michael Raine (1994/1995)
- Revised by Jim Breen (1995)
- Extended by Jim Rose (2007)

**Use Cases**:
- Implement radical-based kanji search
- Component-based learning systems
- Dictionary lookup by visual elements

---

## 4. Reference Data

### 4.1 Frequency and Stroke Count Tables

**Resource**: [technology.chtsai.org/charfreq](https://technology.chtsai.org/charfreq/)

**Available Data**:
- Characters sorted by frequency
- Stroke counts for common characters
- Statistical analysis

---

### 4.2 Wiktionary Appendix

**Resource**: [Wiktionary - Chinese total strokes](https://en.wiktionary.org/wiki/Appendix:Chinese_total_strokes)

**Features**:
- Community-maintained stroke count data
- Free to use
- Multiple character variants

---

## References

### Primary Sources
- [Make Me a Hanzi](https://github.com/skishore/makemeahanzi) - Chinese stroke order SVG data
- [KanjiVG](https://github.com/KanjiVG/kanjivg) - Japanese kanji stroke order
- [HanziVG](https://github.com/Connum/hanzivg) - Chinese hanzi stroke order
- [animCJK](https://github.com/parsimonhi/animCJK) - Multi-language CJK animations
- [Hanzi Writer](https://hanziwriter.org/) - JavaScript library and data

### APIs and Libraries
- [Chinese Character Web API](http://ccdb.hemiola.com/) - Unihan-based API
- [cjklib](https://pypi.org/project/cjklib/) - Python library for CJK processing
- [ChineseStrokes](https://github.com/caiguanhao/ChineseStrokes) - Stroke count database

### Reference Databases
- [KRADFILE/RADKFILE](https://www.edrdg.org/krad/kradinf.html) - Kanji radical decomposition
- [Frequency and Stroke Counts](https://technology.chtsai.org/charfreq/) - Statistical data
- [Wiktionary - Chinese total strokes](https://en.wiktionary.org/wiki/Appendix:Chinese_total_strokes) - Community data

### Online Tools
- [strokeorder.info](http://www.strokeorder.info/) - Animated GIF dictionary
- [strokeorder.com](https://www.strokeorder.com/) - Interactive stroke order
- [Hanzi Writer Data Explorer](https://chanind.github.io/hanzi-writer-data/) - Browse character data

---

**Document Status**: Complete
**Last Updated**: 2026-01-29
