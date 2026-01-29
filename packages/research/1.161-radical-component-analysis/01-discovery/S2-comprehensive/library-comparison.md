# S2 Comprehensive: Library & Data Source Deep-Dive

**Status**: Discovery research (no code execution)
**Created**: 2026-01-28
**Purpose**: Deep technical analysis of libraries, data sources, and formats for character decomposition

---

## Python Library Landscape

### 1. cjklib (Comprehensive but Inactive)

**Repository**: [cburgmer/cjklib on GitHub](https://github.com/cburgmer/cjklib)
**PyPI**: [cjklib](https://pypi.org/project/cjklib/)
**Latest Version**: 0.3.2
**Maintenance Status**: ❌ **INACTIVE** ([Snyk analysis](https://snyk.io/advisor/python/cjklib))

**Maintenance Indicators**:
- No releases to PyPI in past 12+ months
- Past year: 0 issues, 0 pull requests, 0 issue authors, 0 PR authors
- Classified as discontinued or receiving minimal attention
- Weekly downloads: ~70 (limited popularity)
- **Python 3 Support**: NO - major blocker for modern projects

**Technical Capabilities**:

1. **IDS (Ideographic Description Sequences)**:
   - Hierarchical character decomposition stored in database
   - Binary operators (⿰ for left-right: 好 → ⿰女子)
   - Trinary operators (⿲ for three components: 辨 → ⿲⾟刂⾟)
   - Handles non-distinct partitioning, unencoded components, multi-level hierarchies

2. **Kangxi Radicals**:
   - Character-to-radical mapping via Unihan integration
   - Radical-to-character lookup (find all chars with specific radical)
   - Variant handling: Unicode radical forms (⾔), variants (⻈), equivalent chars (言/讠)

3. **Database Architecture**:
   - Uses DatabaseConnector supporting multiple DB systems
   - Default: SQLite (`cjklib.db`)
   - Configuration via `cjklib.conf`
   - Core data storage: IDS sequences with Unicode operators

4. **API Methods** (from [documentation](https://cjklib.readthedocs.io/en/0.3.2/library/cjklib.characterlookup.html)):
   - `getReadingForCharacter()` - pronunciation lookups
   - `getCharactersForReading()` - reverse lookup by pronunciation
   - `getDefaultGlyph()` - locale-specific glyph mappings
   - `getAvailableCharacterDomains()` - supported character sets

**Assessment**:
- ✅ Most comprehensive feature set
- ❌ Inactive development
- ❌ No Python 3 support
- ⚠️ Risk: Unmaintained dependencies, compatibility issues

**Potential**: Fork exists as [cjklib3](https://github.com/free-utils-python/cjklib3) (Python 3 port) - needs verification of maintenance status

---

### 2. hanzipy (Learner-Focused)

**Repository**: [Synkied/hanzipy on GitHub](https://github.com/Synkied/hanzipy)
**PyPI**: hanzipy 1.0.4
**Maintenance Status**: ⚠️ **UNCLEAR** (no recent activity visible in 2025 search results)

**Purpose**: Chinese character NLP framework for language learners

**Features**:
- Character decomposition into radicals/components
- Learning-focused API design
- Framework for character exploration

**Assessment**:
- ✅ Learner-friendly design
- ⚠️ Limited documentation on advanced features
- ⚠️ Unclear maintenance trajectory
- ⚠️ Smaller community than cjklib

**Use Case Fit**: Better for educational tools than computational linguistics research

---

### 3. pypinyin / python-pinyin (Active, Production-Ready)

**Repository**: [mozillazg/python-pinyin](https://github.com/mozillazg/python-pinyin/blob/master/README_en.rst)
**PyPI**: [pypinyin](https://pypi.org/project/pypinyin/)
**Latest Release**: July 20, 2025
**Python Support**: 2.7, 3.5 through 3.13
**Maintenance Status**: ✅ **ACTIVELY MAINTAINED**

**Primary Focus**: Pinyin/Zhuyin/Cyrillic conversion
- Heteronym support (characters with multiple readings)
- Recommended for PRC-style simplified characters
- Most commonly used Python package for modern Chinese

**Assessment for Radical Decomposition**:
- ❌ Not focused on structural decomposition
- ✅ Excellent for pronunciation/reading features
- ✅ Strong maintenance and community

**Recommendation**: Use for pronunciation features, combine with IDS data source for decomposition

---

### 4. Other Alternatives

**dragonmapper** ([PyPI](https://pypi.org/project/dragonmapper/)):
- Conversion between characters/Pinyin/Zhuyin/IPA
- Traditional vs. Simplified identification
- Not focused on structural decomposition

**hanzitools** ([jcklie/hanzitools on GitHub](https://github.com/jcklie/hanzitools)):
- Heisig entry lookups
- CEDICT translation integration
- Recommends pypinyin for Pinyin conversion
- Limited decomposition features

---

## Data Source Deep-Dive

### 1. CJKVI-IDS (Primary Recommendation)

**Repository**: [cjkvi/cjkvi-ids on GitHub](https://github.com/cjkvi/cjkvi-ids)
**Last Release**: February 20, 2018 (v18.02.20)
**Commits**: 158 (ongoing development)
**License**: GPLv2 (most files), some unrestricted

**Data Files** (10 total):

| File | Purpose | License |
|------|---------|---------|
| `ids.txt` | Main IDS data (from CHISE project) | GPLv2 |
| `ids-cdp.txt` | With Academia Sinica CDP PUA chars | GPLv2 |
| `ids-ext-cdef.txt` | Extended IDS (Ext-C/D/E/F) | ❗ No GPL restriction |
| `ids-analysis.txt` | Analysis data | GPLv2 |
| `hanyo-ids.txt` | Hanyo-specific IDS | GPLv2 |
| `waseikanji-ids.txt` | Japanese Waseikanji | GPLv2 |
| `ws2015-ids.txt` | 2015 worksheet | GPLv2 |
| `ws2015-ids-cdp.txt` | 2015 worksheet with CDP | GPLv2 |
| `ucs-strokes.txt` | Stroke count info | GPLv2 |

**Format**: Plain text, tab-delimited
- Column 1: Unicode codepoint (U+XXXX)
- Column 2: Character
- Column 3: IDS sequence using U+2FF0..U+2FFB operators

**Example**:
```
U+5730	地	⿰土也
U+82B1	花	⿱艹化
```

**Coverage**: CJK Unified Ideographs (URO + Extensions)

**Programmatic Usage**:
- Text-based format → easy parsing with Python
- Companion tool: [kawabata/ids](https://github.com/kawabata/ids) for IDS normalization
- Font requirement: HanaMin/HanaMin AFDKO for full character display

**Assessment**:
- ✅ Most comprehensive open IDS database
- ✅ Easy to parse (plain text)
- ✅ Actively developed (158 commits)
- ✅ Covers extended character sets
- ⚠️ Last release 2018 (but ongoing commits)
- ⚠️ GPLv2 licensing for most files

**Comparison to Alternatives**:
- **BabelStone IDS**: UTF-8 plain text, all CJK Unified Ideographs
- **cjklib embedded IDS**: Database format, requires library installation
- **makemeahanzi**: JSON format, includes etymology types

---

### 2. Unihan Database (Official Unicode Standard)

**Specification**: [UAX #38](https://www.unicode.org/reports/tr38/)
**Lookup Interface**: [Unihan Database Lookup](https://www.unicode.org/charts/unihan.html)
**Development**: [unicode-org/unihan-database on GitHub](https://github.com/unicode-org/unihan-database)

**Relevant Fields for Radical/Component Analysis**:

| Field | Description | Example |
|-------|-------------|---------|
| `kRSUnicode` | Radical-stroke count (Unicode) | 32.3 (Radical 土 + 3 strokes) |
| `kRSAdobe_Japan1_6` | Radical-stroke (Adobe-Japan1-6) | Variant system |
| `kRSKangXi` | Kangxi Dictionary radical-stroke | Traditional reference |
| `kTotalStrokes` | Total stroke count | 6 (for 地) |
| `kCangjie` | Cangjie input code | Stroke-based decomposition |
| `kPhonetic` | Phonetic component index | For phonetic compounds |
| `kSemanticVariant` | Semantic variants | Related characters |

**Format**: Tab-delimited text files
- `Unihan_RadicalStrokeCounts.txt`
- `Unihan_Readings.txt`
- `Unihan_Variants.txt`

**Assessment**:
- ✅ Official Unicode standard (authoritative)
- ✅ Regularly updated by consortium
- ✅ Comprehensive coverage of all encoded CJK chars
- ✅ Well-documented specification
- ⚠️ Radical-based (not full structural decomposition)
- ⚠️ Requires parsing multiple files for full data

**Use Case**: Combine with CJKVI-IDS for comprehensive solution:
- Unihan → Radical, stroke count, phonetic info
- CJKVI-IDS → Full structural decomposition

---

### 3. makemeahanzi (Open-Source Character Data)

**Repository**: [skishore/makemeahanzi on GitHub](https://github.com/skishore/makemeahanzi)
**Website**: [Make Me a Hanzi](https://www.skishore.me/makemeahanzi/)
**Format**: JSON data files
**License**: Open-source, free to use
**Data Sources**: Derived from Unihan and cjklib

**JSON Structure** (from website):
```json
{
  "character": "花",
  "etymology": {
    "type": "pictophonetic",
    "hint": "plants",
    "phonetic": "化",
    "semantic": "艹"
  },
  "strokes": [...],
  "medians": [...]
}
```

**Etymology Types**:
- `ideographic`: Meaning-based composition
- `pictographic`: Picture representation
- `pictophonetic`: Phonetic-semantic compound (形聲字)

**Phonetic-Semantic Fields** (when type = "pictophonetic"):
- `hint`: Semantic category hint
- `phonetic`: Phonetic component (string, may be null)
- `semantic`: Semantic radical (string, may be null)

**Assessment**:
- ✅ JSON format (easy integration)
- ✅ Includes etymology type classification
- ✅ Phonetic-semantic decomposition
- ✅ Open-source, permissive license
- ⚠️ Derived data (not primary source)
- ⚠️ Limited to common characters (not full Unicode coverage)

**Best Use**: Educational tools, mnemonic generation, character learning apps

---

### 4. Hsiao & Shillcock Phonetic Compound Database

**Publication**: [Analysis of a Chinese Phonetic Compound Database (2006)](https://link.springer.com/article/10.1007/s10936-006-9022-y)
**Journal**: Journal of Psycholinguistic Research

**Content**:
- Most frequent phonetic compounds
- Decomposition into semantic/phonetic radicals (etymologically accurate)
- Further decomposition into Cangjie stroke patterns
- Pronunciation data included
- Character frequency information

**Format**: Academic dataset (not open GitHub repo)
**Access**: May require contacting authors or institutional access

**Assessment**:
- ✅ Academically rigorous
- ✅ Etymologically accurate decompositions
- ✅ Includes frequency data (useful for learning progression)
- ❌ Limited availability (not easily downloadable)
- ❌ Focused on frequent characters only
- ⚠️ Published 2006 (may need updates for newer Unicode)

**Use Case**: Research reference for validating other data sources

---

## Data Quality Comparison

### IDS Coverage Comparison

| Source | Coverage | Format | Maintenance | License |
|--------|----------|--------|-------------|---------|
| CJKVI-IDS | Full URO + Ext | Plain text | Active commits | GPLv2 |
| BabelStone IDS | All CJK Unified | Plain text | Unknown | Unknown |
| cjklib embedded | URO + common | SQLite | Inactive | BSD-like |
| makemeahanzi | Common chars | JSON | Active | Open |

**Recommendation**: CJKVI-IDS for comprehensive coverage, makemeahanzi for educational/learner focus

---

### Radical System Comparison

| System | Radicals | Source | Use Case |
|--------|----------|--------|----------|
| Kangxi (康熙) | 214 | Traditional standard | Unicode Unihan, dictionaries |
| Simplified | 189 | PRC standard | Mainland China education |
| Unicode Radical | 214 + variants | Unicode Standard | Digital text processing |

**Key Insight**: Multiple valid radical systems exist. Unihan uses Kangxi as baseline with variants.

---

### Phonetic-Semantic Decomposition Sources

| Source | Phonetic Info | Semantic Info | Coverage | Format |
|--------|---------------|---------------|----------|--------|
| makemeahanzi | ✅ Component | ✅ Component | Common | JSON |
| Unihan kPhonetic | ✅ Index only | ❌ Limited | Full | Text |
| Hsiao & Shillcock | ✅ Full | ✅ Full | Frequent | Academic |
| CJKVI-IDS | ❌ No | ❌ No | Full | Text |

**Gap Identified**: No comprehensive open database combining:
1. Full Unicode coverage (CJKVI-IDS level)
2. Phonetic-semantic component classification (makemeahanzi level)
3. Etymology type annotation (ideographic/pictographic/pictophonetic)

**Workaround**: Combine multiple sources programmatically

---

## Integration Strategy

### Recommended Data Stack

**Layer 1: Structural Decomposition**
- **Primary**: CJKVI-IDS (`ids.txt`) for full structural decomposition
- **Fallback**: Parse Unihan for characters not in CJKVI-IDS

**Layer 2: Radical Information**
- **Primary**: Unihan `kRSUnicode` for Kangxi radical + stroke count
- **Enhancement**: Unihan `kRSKangXi` for traditional dictionary reference

**Layer 3: Phonetic-Semantic Classification**
- **Primary**: makemeahanzi for common characters (JSON)
- **Research**: Hsiao & Shillcock for validation/academic reference

**Layer 4: Pronunciation & Readings**
- **Primary**: pypinyin for modern Mandarin pinyin
- **Enhancement**: Unihan readings for historical/variant pronunciations

---

### Library Selection by Use Case

**Use Case: Educational Tool / Language Learning App**
- Data: makemeahanzi (etymology, mnemonics) + pypinyin (pronunciation)
- Library: Custom parser (JSON + pypinyin library)
- Rationale: JSON format easy, mnemonic focus, active maintenance

**Use Case: Computational Linguistics Research**
- Data: CJKVI-IDS (full coverage) + Unihan (radicals/metadata)
- Library: Custom parser or cjklib3 fork (if verified maintained)
- Rationale: Comprehensive data, research flexibility

**Use Case: Dictionary/Reference Application**
- Data: Unihan (comprehensive) + CJKVI-IDS (structure) + pypinyin (pronunciation)
- Library: Custom integration layer
- Rationale: Multiple data sources needed, no single library sufficient

**Use Case: Quick Prototype**
- Data: makemeahanzi JSON
- Library: Standard Python JSON parsing
- Rationale: Fastest time-to-value, single file

---

## Technical Debt & Risk Assessment

### cjklib (Inactive)
- **Risk**: No Python 3 support, abandoned project
- **Mitigation**: Fork to cjklib3 OR extract database and write custom parser
- **Effort**: High (forking), Medium (custom parser)

### CJKVI-IDS (2018 release)
- **Risk**: Stale release despite active commits
- **Mitigation**: Use latest GitHub main branch, not release tag
- **Effort**: Low (just change download source)

### Multiple Data Source Dependencies
- **Risk**: Conflicting decompositions, synchronization issues
- **Mitigation**: Document source precedence rules, version pinning
- **Effort**: Medium (governance + tooling)

### License Compliance
- **Risk**: GPLv2 for CJKVI-IDS main file
- **Mitigation**: Use `ids-ext-cdef.txt` (no GPL) OR comply with GPLv2
- **Effort**: Low (file selection) or Medium (GPL compliance)

---

## Next Steps

**For S3 (Need-Driven Patterns)**:
- Map generic use cases to data source combinations
- Identify gaps in current data sources
- Prototype parsing strategies (pseudo-code level, no implementation)

**For S4 (Strategic Analysis)**:
- Unicode Consortium roadmap for Unihan updates
- Python ecosystem trend analysis (active vs. dormant projects)
- Traditional vs. Simplified handling strategies
- CJK variant forms (Japan/Korea/Vietnam) decomposition differences

---

**Sources**:
- [cburgmer/cjklib GitHub](https://github.com/cburgmer/cjklib)
- [cjklib PyPI](https://pypi.org/project/cjklib/)
- [Snyk: cjklib Health Analysis](https://snyk.io/advisor/python/cjklib)
- [cjklib Documentation](https://cjklib.readthedocs.io/en/0.3.2/library/cjklib.characterlookup.html)
- [pypinyin PyPI](https://pypi.org/project/pypinyin/)
- [python-pinyin README](https://github.com/mozillazg/python-pinyin/blob/master/README_en.rst)
- [CJKVI-IDS GitHub](https://github.com/cjkvi/cjkvi-ids)
- [Unihan Database (UAX #38)](https://www.unicode.org/reports/tr38/)
- [makemeahanzi GitHub](https://github.com/skishore/makemeahanzi)
- [Hsiao & Shillcock (2006) Paper](https://link.springer.com/article/10.1007/s10936-006-9022-y)
