# Use Case: Etymology & Character Origin Research

## Goal

Study the historical development, original meanings, and structural evolution of Chinese characters for linguistic research or educational content creation.

## User Stories

1. **Linguist researching pictophonetic characters:**
   - Query: Which characters use 工 as phonetic component?
   - System: Returns 江 (river), 紅 (red), 功 (achievement), etc.
   - Analysis: Common phonetic 'gong' sound

2. **Content creator making etymology videos:**
   - Need: Visual evolution of character forms
   - System provides: Oracle bone → bronze → seal → modern
   - Plus: Semantic/phonetic classification

3. **Dictionary editor adding etymology notes:**
   - Input: Character 信
   - System returns: Pictophonetic (人 person + 言 words)
   - Context: "信" = person standing by their words = trust

4. **Historical text researcher:**
   - Analyzing archaic character forms
   - Needs variant mappings (ancient → modern)
   - Tracks character evolution through dynasties

## Required Capabilities

### Etymology-Specific
- ✅ Character origin classification (pictographic, ideographic, pictophonetic, etc.)
- ✅ Semantic/phonetic component identification
- ✅ Historical forms (oracle bone, bronze, seal script)
- ✅ Etymology explanations (why this structure?)
- Optional: Cross-reference to variants

### Structure Analysis
- ✅ IDS decomposition (see construction)
- ✅ Component relationships (semantic vs. phonetic)
- Optional: Component genealogy (how components evolved)

## Library Fit Analysis

### makemeahanzi
**Excellent fit (9/10):**
- ✅ **Etymology field explicitly included**
- ✅ Classification: pictographic, ideographic, pictophonetic
- ✅ Semantic and phonetic components marked
- ✅ IDS decomposition
- ⚠️ Coverage: 9,000+ characters (common ones well-covered)
- ❌ No historical forms (oracle bone, bronze, seal)

**Etymology data structure:**
```json
{
  "character": "江",
  "decomposition": "⿰氵工",
  "etymology": {
    "type": "pictophonetic",
    "phonetic": "工",
    "semantic": "氵",
    "hint": "river; water (氵) + phonetic gong (工)"
  },
  "pinyin": ["jiāng"]
}
```

**Strengths:**
- Direct etymology classification
- Phonetic/semantic explicitly distinguished
- Hint field provides explanation
- Easy to build etymology database

### cjklib/cjklib3
**Moderate fit (6/10):**
- ✅ IDS decomposition (structure visible)
- ✅ Radical identification
- ⚠️ Limited etymology information
- ❌ No semantic/phonetic classification
- ❌ No historical forms
- ✅ Comprehensive character coverage

**Use case:** Structural analysis, but requires external etymology data

### CJKVI-IDS
**Poor fit (3/10):**
- ✅ IDS structure
- ❌ No etymology information
- ❌ No component classification
- ❌ No historical forms
- Use case: Structural data only, need external etymology source

### Specialized Etymology Resources (Not Libraries)

#### Zhongwen.com
- Online etymology dictionary
- Not programmatic access
- Rich explanations

#### Chinese Etymology by Richard Sears
- Historical character forms database
- Shows evolution: oracle bone → modern
- Not easily parsable API

#### Wiktionary Chinese Etymology
- Community-contributed
- Variable quality
- Can be scraped but maintenance burden

## Recommended Solution

### For Etymology Research: makemeahanzi + External Sources

**Architecture:**
```
Primary: makemeahanzi (9K characters with etymology)
    ↓
Fallback: Manual curation for specialized characters
    ↓
Enhancement: Scrape Sears database for historical forms
    ↓
Output: Comprehensive etymology database
```

**Implementation:**

1. **Base layer:** makemeahanzi JSON
   - Parse etymology field
   - Index by type (pictographic, ideographic, pictophonetic)
   - Build phonetic component index
   - Build semantic component index

2. **Enhancement layer:** Add historical forms
   - Scrape Richard Sears database
   - Map ancient forms to modern characters
   - Store evolution sequences

3. **Query API:**
   ```python
   def get_etymology(char):
       base = makemeahanzi_db.get(char)
       historical = sears_db.get(char)

       return {
           'modern': char,
           'type': base['etymology']['type'],
           'semantic': base['etymology']['semantic'],
           'phonetic': base['etymology']['phonetic'],
           'hint': base['etymology']['hint'],
           'historical_forms': historical['forms'],
           'evolution': historical['timeline']
       }
   ```

## Use Case Examples

### Research Query: Find All Pictophonetic Characters with Phonetic '马'

```python
results = [
    char for char, data in etymology_db.items()
    if data['etymology']['type'] == 'pictophonetic'
    and '马' in data['etymology']['phonetic']
]
# → ['吗', '妈', '码', '玛', etc.]
# All pronounced 'ma'
```

### Educational Content: Explain Character 好

```python
info = get_etymology('好')

# Output:
{
  'modern': '好',
  'structure': '⿰女子',
  'type': 'ideographic',
  'meaning': 'woman + child = good (mother with child)',
  'components': {
    '女': 'woman (semantic)',
    '子': 'child (semantic)'
  }
}
```

### Linguistic Research: Analyze Phonetic Components

```python
# Find all characters using same phonetic
phonetic_family = find_by_phonetic_component('工')

# Analysis:
# 工 (gōng) - work
# 江 (jiāng) - river [older pronunciation gōng]
# 紅 (hóng) - red
# 功 (gōng) - achievement
# Common phonetic base indicating ancient sound
```

## Gaps & Workarounds

### Gap 1: Historical Forms Not in makemeahanzi

**Workaround:**
- Scrape Richard Sears etymology database
- Map to makemeahanzi characters
- Store separately, join on character key

**Effort:** ~3-5 days scraping + integration

### Gap 2: Only 9K Characters Covered

**Workaround:**
- Most research focuses on common characters (covered)
- For rare characters: Manual annotation
- Or: Use CJKVI-IDS for structure, manual etymology

### Gap 3: No Component Evolution Tracking

**Workaround:**
- Requires linguistic research
- Not available in any library
- Build manually for specific research questions

## Alternative Approach: Build Comprehensive Etymology DB

If makemeahanzi is insufficient:

1. **Foundation:** makemeahanzi (9K with etymology)
2. **Historical forms:** Scrape Sears database
3. **Extended coverage:** Manual annotation for specialized characters
4. **Component evolution:** Linguistic research + manual entry
5. **Cross-references:** Link related characters

**Effort:** Significant (~weeks/months)
**Benefit:** Research-grade etymology resource

## Production Considerations

### For Educational Content
- makemeahanzi sufficient for most cases
- Focus on common 3,000-5,000 characters
- Supplement with curated explanations

### For Linguistic Research
- Start with makemeahanzi
- Enhance with historical data (Sears)
- Accept manual work for specialized queries
- Build custom database over time

### For Dictionary/Reference
- makemeahanzi + manual curation
- Quality control on etymology explanations
- Peer review by linguists
- Continuous refinement

---

**Verdict:** makemeahanzi provides best programmatic access to etymology data for common characters. For comprehensive research, combine with historical databases (Sears) and expect manual curation for specialized needs.
