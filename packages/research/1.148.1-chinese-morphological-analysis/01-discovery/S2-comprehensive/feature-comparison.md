# Feature Comparison Matrix

## Character-Level Analysis

| Feature | cjklib | cjklib3 | makemeahanzi | HanLP | Stanza | LTP |
|---------|--------|---------|--------------|-------|--------|-----|
| **Character Decomposition (IDS)** | ✅ Full | ✅ Full | ✅ Full | ❌ | ❌ | ❌ |
| **Radical Extraction** | ✅ Kangxi | ✅ Kangxi | ✅ | ❌ | ❌ | ❌ |
| **Stroke Information** | ✅ Derived | ✅ Derived | ✅ SVG | ❌ | ❌ | ❌ |
| **Etymology Data** | ⚠️ Limited | ⚠️ Limited | ✅ Rich | ❌ | ❌ | ❌ |
| **Component Trees** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |

## Word-Level Analysis

| Feature | cjklib | HanLP | Stanza | LTP | Jieba | pkuseg |
|---------|--------|-------|--------|-----|-------|--------|
| **Word Segmentation** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **POS Tagging** | ❌ | ✅ | ✅ | ✅ | ⚠️ Basic | ✅ |
| **Morphological Features (UD)** | ❌ | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| **Morpheme Decomposition** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Compound Analysis** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Technical Characteristics

| Aspect | cjklib | cjklib3 | makemeahanzi | HanLP | Stanza | LTP |
|--------|--------|---------|--------------|-------|--------|-----|
| **Python 3 Support** | ❌ | ✅ | N/A (data) | ✅ | ✅ | ✅ |
| **pip Installable** | ⚠️ Py2 | ❌ Fork | N/A | ✅ | ✅ | ✅ |
| **Active Maintenance** | ❌ | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| **Documentation Quality** | ✅ Good | ✅ Good | ✅ | ✅ | ✅ | ✅ |
| **Setup Complexity** | Medium | High | Low | Low | Low | Low |

## Data Sources

| Source | Format | Coverage | Character Decomposition | Etymology | Strokes |
|--------|--------|----------|------------------------|-----------|---------|
| **CJKVI-IDS** | IDS files | CJK Unified | ✅ | ❌ | ❌ |
| **makemeahanzi** | JSON | 9,000+ chars | ✅ | ✅ | ✅ SVG |
| **cjklib DB** | SQLite | Comprehensive | ✅ | ⚠️ | ✅ |
| **Unicode IDS** | Standard | All CJK | ✅ | ❌ | ❌ |

## Alternative Approaches

### Character Decomposition Options

1. **Use cjklib3 fork** (library approach)
   - Pro: Complete API, rich functionality
   - Con: Setup complexity, Python 3 via fork

2. **Use makemeahanzi data** (data-first approach)
   - Pro: JSON format, modern, rich etymology
   - Con: Need to build parser, 9K characters (not all CJK)

3. **Parse CJKVI-IDS directly** (minimal approach)
   - Pro: Complete CJK coverage, simple format
   - Con: Need IDS parser, no etymology, no stroke data

4. **Hybrid: makemeahanzi + CJKVI-IDS**
   - Pro: Best of both worlds
   - Con: Integration complexity

### Word Segmentation Options

| Tool | Strength | Use Case |
|------|----------|----------|
| **HanLP** | Multilingual pipeline | Production, comprehensive NLP |
| **Stanza** | UD framework, Stanford | Research, cross-lingual |
| **LTP** | Chinese-specific | Chinese-only production |
| **Jieba** | Lightweight, popular | Simple segmentation |
| **pkuseg** | Domain-specific models | Specialized domains |

## Key Findings

### No Morpheme Decomposition Tools Found

**Significant gap:** None of the libraries analyzed actually decompose Chinese compound words into morphemes.

**Example of what's missing:**
- Input: "电脑" (computer)
- What tools do: Identify as single word [电脑/NOUN]
- What's missing: Decompose to "电" (electricity) + "脑" (brain)

**Why this matters:**
- Might need custom implementation
- Or: redefine requirements to focus on word segmentation + character decomposition
- Morpheme decomposition may require linguistic rules, not library

### Two Separate Problem Domains

**Character Structure:**
- Tools: cjklib, makemeahanzi, IDS databases
- Well-supported with existing libraries/data
- Mature solutions available

**Word/Morpheme Analysis:**
- Tools: HanLP, Stanza, LTP, Jieba, pkuseg
- All do word segmentation
- None do morpheme decomposition of compounds
- May need custom solution or clarified requirements

---

Sources: See individual library assessments in this directory.
