# Use Case: Search & Information Retrieval

## Goal

Enable search and retrieval of Chinese text based on character structure, components, and morphological properties.

## User Stories

1. **Dictionary user searching by radical:**
   - "Show me all characters with 氵 water radical"
   - System returns: 江, 河, 湖, 海, 洋, 汉, etc.
   - Sorted by stroke count or frequency

2. **Unicode researcher finding similar glyphs:**
   - "Find characters structurally similar to 好"
   - System finds: All ⿰ left-right compositions
   - Filter by specific components

3. **Translation tool handling variants:**
   - Input: Traditional 學 or Simplified 学
   - System recognizes as variants
   - Returns unified results

4. **Digital library indexing text:**
   - Index historical documents by characters
   - Handle variant forms
   - Enable component-based search

## Required Capabilities

### Character-Level
- ✅ Component extraction (index by radicals/components)
- ✅ IDS parsing (structural similarity)
- ✅ Variant mapping (traditional/simplified/regional)
- ✅ Radical classification (standard lookup tables)
- ⚠️ Fuzzy matching (partial component match)

### Word-Level
- ✅ Word segmentation (identify searchable units)
- Optional: Morphological normalization

## Library Fit Analysis

### cjklib/cjklib3
**Excellent fit (9/10):**
- ✅ `getCharactersForComponents()` - exact match search
- ✅ `getRadicalForms()` - handle radical variants
- ✅ `getCharacterVariants()` - traditional/simplified mapping
- ✅ Comprehensive CJK coverage
- ✅ SQLite backend (efficient lookup)
- ⚠️ Python 3 via fork

**Key APIs for search:**
```python
from cjklib import characterlookup
cjk = characterlookup.CharacterLookup('T')  # Traditional

# Find by component
chars = cjk.getCharactersForComponents(['氵'])

# Get variants
variants = cjk.getCharacterVariants('學')  # → ['学', ...]

# Radical-based search
radical_chars = cjk.getCharactersForRadical('水')
```

### CJKVI-IDS
**Good fit (7/10):**
- ✅ Complete IDS data (structural search)
- ✅ Can build component index
- ⚠️ Requires custom search implementation
- ❌ No built-in variant mapping
- ❌ No radical classification tables

**Use case:**
- Parse IDS for all characters
- Build inverted index: component → [characters]
- Implement fuzzy structure matching

### makemeahanzi
**Moderate fit (6/10):**
- ✅ IDS decomposition
- ⚠️ Limited coverage (9K chars)
- ❌ No variant tables
- ❌ No radical classification
- ✅ Easy to index (JSON)

**Best for:** Simple component search in constrained character set

### HanLP
**Moderate fit for word-level (6/10):**
- ✅ Word segmentation (identify search terms)
- ✅ Can index at word level
- ❌ No character structure search
- Use case: "Find documents containing '学习'" (word search, not component search)

## Recommended Solution

### For Character Search: cjklib/cjklib3

**Architecture:**
```
User Query → cjklib API → SQLite DB → Results
```

**Implementation:**
1. Use cjklib3 fork for Python 3
2. Build search index on startup
3. Implement query patterns:
   - By radical: `cjk.getCharactersForRadical()`
   - By component: `cjk.getCharactersForComponents()`
   - By structure: Parse IDS, filter by pattern
   - Variants: `cjk.getCharacterVariants()`

**Advantages:**
- Proven search algorithms
- Comprehensive data
- SQL backend = efficient queries
- Handles complex cases (variant forms, radical positioning)

### For Document Search: HanLP + cjklib

**Hybrid approach:**
1. **Preprocessing:** HanLP segments documents into words
2. **Indexing:**
   - Word-level index (standard search)
   - Character-level index (cjklib for component search)
3. **Query:**
   - Regular search: Use word index
   - Component search: Use character index

**Example:**
```
Document: "我喜欢学习汉字"
Word index: ["我", "喜欢", "学习", "汉字"]
Character index: {
  '子': ['字'],
  '宀': ['字'],
  '氵': ['汉'],
  // etc.
}

Query "characters with 氵" → returns positions of: 汉
```

## Production Considerations

### Performance
- **cjklib SQLite:** Fast lookups for single-character queries
- **Inverted index:** Fast component search
- **Caching:** Cache common queries (radical lists)

### Scalability
- **Character search:** O(1) with proper indexing
- **Document search:** O(n) with inverted index
- **Structure matching:** O(n) requires full scan, optimize with filters

### Deployment
- **Option A:** Use cjklib3 fork (accept Python 3 complexity)
- **Option B:** Port cjklib algorithms to modern Python, use CJKVI-IDS data
- **Option C:** Use cjklib Python 2 via subprocess (isolation)

## Alternative: Build Custom Search

If cjklib complexity is prohibitive:

1. **Data:** CJKVI-IDS (all CJK characters with IDS)
2. **Preprocessing:**
   - Parse IDS into component trees
   - Build inverted index: component → characters
   - Create radical mapping table
3. **Query engine:**
   - Component search: O(1) lookup in index
   - Structure search: Filter by IDS pattern
   - Fuzzy match: Levenshtein distance on IDS strings

**Effort:** ~1-2 weeks development
**Advantage:** Full control, modern Python 3, no legacy dependencies

---

**Verdict:** For production character search, cjklib provides comprehensive functionality despite Python 2 legacy. For new projects, consider building custom search on CJKVI-IDS data with modern Python.
