# Radical & Component Analysis: Research Explainer

**Research ID**: 1.161
**Category**: Chinese Language Processing / Character Decomposition
**Completed**: 2026-01-28
**Discovery Phase**: S1-S4 Complete

---

## What Is This?

Character decomposition is the process of breaking down Chinese characters (汉字/漢字) into their constituent parts: radicals (部首), components, and structural relationships. This research surveys data sources, tools, and patterns for implementing character decomposition systems.

**Key Use Cases**:
- **Etymology**: Understand character origins and historical development
- **Mnemonic generation**: Create memory aids for language learners
- **Character learning progression**: Build curricula from simple to complex
- **Computational linguistics**: Enable character-aware NLP applications

---

## What We Researched

### S1: Quick Ecosystem Scan ([ecosystem-scan.md](01-discovery/S1-rapid/ecosystem-scan.md))

**Data Standards**:
- **Unihan Database**: Official Unicode consortium database with radical-stroke data, variants, pronunciations
- **IDS (Ideographic Description Sequences)**: Standardized structural representation using operators (⿰, ⿱, etc.)
- **Phonetic-Semantic Compounds (形聲字)**: 80% of characters combine semantic radical + phonetic component

**Python Libraries**:
- **cjklib**: Comprehensive but inactive (no Python 3 support)
- **hanzipy**: Learner-focused, unclear maintenance
- **pypinyin**: Active, production-ready (pronunciation focus)
- **makemeahanzi**: Open-source character data (JSON format)

**Open Data Sources**:
- **CJKVI-IDS**: 158 commits, comprehensive IDS database (plain text)
- **cjk-decomp**: 75,000+ character decomposition data
- **Hsiao & Shillcock Database**: Academic phonetic compound research

---

### S2: Deep Technical Dive ([library-comparison.md](01-discovery/S2-comprehensive/library-comparison.md))

**Library Status**:
- ❌ **cjklib**: Abandoned (0 PRs/issues in past year, no Python 3)
- ✅ **pypinyin**: Actively maintained (July 2025 release, Python 3.5-3.13)
- ⚠️ **hanzipy**: Maintenance unclear
- ✅ **CJKVI-IDS**: Active commits (158 total), stale releases (2018)

**Data Format Comparison**:
```
CJKVI-IDS:    U+5730  地  ⿰土也   (plain text, tab-delimited)
Unihan:       kRSUnicode: 32.3      (radical 土 + 3 strokes)
makemeahanzi: {"character": "地", "etymology": {...}}  (JSON)
```

**Integration Strategy**:
- **Layer 1**: CJKVI-IDS for structural decomposition
- **Layer 2**: Unihan for radical/stroke metadata
- **Layer 3**: makemeahanzi for phonetic-semantic classification
- **Layer 4**: pypinyin for pronunciation

**Critical Insight**: No single comprehensive library exists. Hybrid data-source approach recommended.

---

### S3: Generic Use Cases ([use-case-patterns.md](01-discovery/S3-need-driven/use-case-patterns.md))

**10 Key Patterns Identified**:

1. **Character Decomposition Lookup**: 花 → ⿱艹化 (structure)
2. **Radical-Based Search**: Find all chars with radical 土
3. **Phonetic Series Identification**: 青 → 清情請晴... (pronunciation families)
4. **Etymology Tree Generation**: Recursive component hierarchy
5. **Mnemonic Component Extraction**: 好 = 女+子 → "woman + child = good"
6. **Learning Progression Sequencing**: Simple components before complex compounds
7. **Character Similarity Analysis**: Structural/radical/phonetic overlap
8. **Component Reusability Analysis**: Identify high-value components (口, 氵, etc.)
9. **Traditional ↔ Simplified Mapping**: 國 ↔ 国 (variant handling)
10. **Stroke Order Alignment**: Component order vs. writing sequence

**Data Gap Identified**: No comprehensive open database combining:
- Full Unicode coverage (CJKVI-IDS level)
- Phonetic-semantic classification (makemeahanzi level)
- Etymology type annotation (ideographic/pictographic/pictophonetic)

**Workaround**: Combine multiple data sources programmatically

---

### S4: Strategic Viability ([viability-analysis.md](01-discovery/S4-strategic/viability-analysis.md))

**Unicode Roadmap**:
- ✅ Stable: Unihan database regularly updated (annual Unicode releases)
- ✅ Mature: IDS operators stable since 1999 (no breaking changes)
- ✅ Ongoing: CJK extensions (Ext-I in Unicode 17.0, 2026)

**Python Ecosystem Health**:
- ❌ cjklib: Abandoned (technical debt if used)
- ✅ pypinyin: Active (recommended for pronunciation)
- ⚠️ CJKVI-IDS: Active commits but stale releases (monitor closely)

**Recommended Architecture**:
- **Bet on**: Open data sources (Unihan, CJKVI-IDS), stable standards
- **Avoid**: Unmaintained libraries (cjklib), proprietary datasets
- **Hedge with**: Modular design, data versioning, automated testing

**10-Year Outlook**:
- Stable: Unicode, Unihan, IDS operators
- Uncertain: Python library consolidation, CJK NLP evolution
- Emerging: LLM-powered mnemonics, adaptive learning curricula

---

## Key Findings

### 1. Data Sources Are More Reliable Than Libraries

| Aspect | Libraries | Open Data |
|--------|-----------|-----------|
| Maintenance | Fragile (cjklib abandoned) | Stable (Unicode consortium) |
| Format | APIs can break | Plain text (future-proof) |
| Control | Dependency on maintainers | Full parsing control |
| Risk | High (abandonment) | Low (can fork) |

**Recommendation**: **Data-first approach** - parse CJKVI-IDS and Unihan directly, avoid unmaintained libraries.

---

### 2. Hybrid Data Stack Required

No single source provides everything:

```
Use Case: Educational App
├─ Structure: CJKVI-IDS (⿰土也)
├─ Radicals: Unihan (kRSUnicode = 32.3)
├─ Etymology: makemeahanzi (type: pictophonetic)
└─ Pronunciation: pypinyin (dì, de)

Use Case: Comprehensive Dictionary
├─ Structure: CJKVI-IDS (full Unicode)
├─ Metadata: Unihan (variants, readings, strokes)
├─ Phonetic: makemeahanzi (common chars) + custom for rare chars
└─ Pronunciation: pypinyin + Unihan kMandarin
```

---

### 3. Traditional vs. Simplified Requires Dual Storage

**Challenge**: Same Unicode codepoint, different glyphs
- 骨 (bone): PRC vs. Taiwan vs. Japan variants
- Decomposition differs: 國 (⿴囗或) vs. 国 (⿴囗玉)

**Solution**:
- Store IDS for both traditional and simplified forms
- Use Unihan `kSimplifiedVariant` / `kTraditionalVariant` for mapping
- Locale preference determines which decomposition to show

---

### 4. 80% of Characters Are Phonetic-Semantic Compounds

**Structure**: Semantic radical + Phonetic component

**Example**: 清 (clear, qīng)
- Semantic: 氵 (water) → meaning category
- Phonetic: 青 (qīng) → pronunciation hint

**Implication**:
- Mnemonic generation: "Clear water (氵) sounds like 青"
- Learning progression: Teach phonetic families together (清情請晴)
- Etymology tools: Must classify phonetic vs. semantic components

**Data Source**: makemeahanzi for common chars, Hsiao & Shillcock for research

---

### 5. Regional Variants Complicate Decomposition

**Unicode Han Unification**: One codepoint for "same" character across regions
- Benefit: Interoperability
- Challenge: Visual/structural differences not captured

**Handling Strategy**:
1. Default to Unicode standard (Unihan)
2. Store multiple IDS per character (regional variants)
3. Locale-aware decomposition (user's region preference)
4. Document variant policy (e.g., "prefer simplified for PRC learners")

---

## Data Source Recommendations

### For Structural Decomposition
✅ **Primary**: [CJKVI-IDS](https://github.com/cjkvi/cjkvi-ids) `ids.txt`
- Coverage: Full URO + Extensions
- Format: Plain text (easy parsing)
- License: ids-ext-cdef.txt is GPL-exempt

### For Radical & Metadata
✅ **Primary**: [Unihan Database](https://www.unicode.org/charts/unihan.html)
- Authority: Official Unicode consortium
- Fields: kRSUnicode, kTotalStrokes, kSemanticVariant, etc.
- Maintenance: Regular updates

### For Phonetic-Semantic Classification
✅ **Common Chars**: [makemeahanzi](https://github.com/skishore/makemeahanzi)
- Format: JSON (easy integration)
- Fields: etymology.type, etymology.phonetic, etymology.semantic
- License: Open-source

✅ **Research Reference**: Hsiao & Shillcock (2006) Database
- Academic rigor
- Cangjie stroke decomposition
- Limited availability (contact authors)

### For Pronunciation
✅ **Primary**: [pypinyin](https://pypi.org/project/pypinyin/)
- Actively maintained (July 2025)
- Python 3.5-3.13 support
- Heteronym support

---

## Library Recommendations

| Use Case | Recommended Approach | Why |
|----------|---------------------|-----|
| Quick Prototype | Parse makemeahanzi JSON | Fastest, single file, common chars |
| Educational App | makemeahanzi + pypinyin | Etymology + pronunciation, learner-focused |
| Comprehensive Dictionary | CJKVI-IDS + Unihan + pypinyin | Full coverage, authoritative |
| Research Project | All sources + validation | Cross-reference, data quality assurance |

**Libraries to AVOID**:
- ❌ cjklib: No Python 3 support, abandoned
- ❌ cjklib3 fork: Maintenance unverified (as of 2026-01-28)

---

## Implementation Guidance

### Parsing CJKVI-IDS (Plain Text)

**Format**: Tab-delimited
```
U+5730	地	⿰土也
```

**Python Pseudo-Code** (concept, not implementation):
```python
def parse_ids_line(line):
    parts = line.strip().split('\t')
    return {
        'unicode': parts[0],        # U+5730
        'character': parts[1],      # 地
        'ids': parts[2],            # ⿰土也
        'components': extract_components(parts[2])  # [土, 也]
    }
```

### Parsing Unihan (Tab-Delimited)

**Format**: `U+XXXX<tab>kField<tab>Value`
```
U+5730	kRSUnicode	32.3
U+5730	kTotalStrokes	6
```

**Python Pseudo-Code**:
```python
def parse_unihan_file(file_path):
    char_data = defaultdict(dict)
    for line in file:
        if line.startswith('#'): continue
        codepoint, field, value = line.strip().split('\t')
        char_data[codepoint][field] = value
    return char_data
```

### Parsing makemeahanzi (JSON)

**Format**: JSON objects, one per line
```json
{"character": "地", "etymology": {"type": "pictophonetic", "phonetic": "也", "semantic": "土"}}
```

**Python Pseudo-Code**:
```python
import json

def parse_makemeahanzi(file_path):
    characters = {}
    with open(file_path) as f:
        for line in f:
            data = json.loads(line)
            characters[data['character']] = data
    return characters
```

---

## Next Steps

### If Building Educational Tool
1. Download [makemeahanzi dictionary.txt](https://github.com/skishore/makemeahanzi)
2. Install pypinyin: `pip install pypinyin`
3. Parse JSON for etymology, use pypinyin for pronunciation
4. Implement Pattern 5 (Mnemonic Extraction) from S3

### If Building Comprehensive Dictionary
1. Clone [CJKVI-IDS](https://github.com/cjkvi/cjkvi-ids) (use `ids.txt`)
2. Download [Unihan Database](https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip)
3. Write parsers for both formats (see pseudo-code above)
4. Implement Pattern 1 (Character Decomposition Lookup) from S3
5. Cross-validate data sources (check for conflicts)

### If Doing Research
1. Obtain Hsiao & Shillcock (2006) database (academic access)
2. Combine all sources: CJKVI-IDS + Unihan + makemeahanzi
3. Build validation pipeline (data quality metrics)
4. Implement Pattern 7 (Similarity Analysis) and Pattern 8 (Reusability) from S3

---

## Critical Warnings

### ❌ Do NOT Use cjklib
- No Python 3 support
- Abandoned (no updates in years)
- Fork (cjklib3) maintenance unclear
- Use direct data parsing instead

### ⚠️ Handle Regional Variants
- Same Unicode codepoint ≠ same visual form
- Store multiple IDS per character
- Document locale handling policy

### ⚠️ License Compliance
- CJKVI-IDS `ids.txt`: GPLv2
- CJKVI-IDS `ids-ext-cdef.txt`: No GPL restriction
- Choose file based on license requirements

### ⚠️ Data Version Pinning
- CJKVI-IDS: Use git commit SHA (not release tag)
- Unihan: Track Unicode version number
- makemeahanzi: Use GitHub release tag
- Reproducibility requires version tracking

---

## Maintenance Strategy

### Quarterly Tasks
- [ ] Check CJKVI-IDS for new commits (git log)
- [ ] Monitor Unicode announcements (new CJK extensions)
- [ ] Verify pypinyin still actively maintained (PyPI releases)
- [ ] Test data parsers against latest versions

### Annual Tasks
- [ ] Update Unihan database (new Unicode release)
- [ ] Re-download CJKVI-IDS (latest commit)
- [ ] Review makemeahanzi for updates
- [ ] Audit data conflicts (cross-source validation)

### As-Needed
- [ ] Contribute fixes to CJKVI-IDS if errors found
- [ ] Fork CJKVI-IDS if maintenance lapses
- [ ] Publish derived datasets (community contribution)

---

## Further Reading

**Discovery Documents**:
- [S1: Ecosystem Scan](01-discovery/S1-rapid/ecosystem-scan.md) - Overview of standards and tools
- [S2: Library Comparison](01-discovery/S2-comprehensive/library-comparison.md) - Technical deep-dive
- [S3: Use Case Patterns](01-discovery/S3-need-driven/use-case-patterns.md) - 10 generic patterns
- [S4: Viability Analysis](01-discovery/S4-strategic/viability-analysis.md) - Long-term strategy

**External Resources**:
- [Unicode Unihan Database (UAX #38)](https://www.unicode.org/reports/tr38/) - Official spec
- [CJKVI-IDS GitHub](https://github.com/cjkvi/cjkvi-ids) - Comprehensive IDS data
- [makemeahanzi](https://github.com/skishore/makemeahanzi) - Open-source character data
- [Hacking Chinese: Phonetic Components](https://www.hackingchinese.com/phonetic-components-part-1-the-key-to-80-of-all-chinese-characters/) - Learner guide
- [Hsiao & Shillcock (2006)](https://link.springer.com/article/10.1007/s10936-006-9022-y) - Academic research

---

**Research Completed**: 2026-01-28
**Status**: Discovery phase complete (S1-S4)
**Next**: Implementation phase (02-implementations/) if needed
