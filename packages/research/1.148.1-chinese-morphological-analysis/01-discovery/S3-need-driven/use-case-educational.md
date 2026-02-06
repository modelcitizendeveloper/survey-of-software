# Use Case: Educational & Learning Tools

## Goal

Help learners understand Chinese characters through component analysis and etymology, making character acquisition more systematic and memorable.

## User Stories

1. **Student learning character 認 (recognize):**
   - Wants to know: What are the components?
   - System shows: ⿰言刃 (words + blade)
   - Etymology: "recognizing" = distinguishing with words as sharp as a blade

2. **Teacher creating flashcards:**
   - Needs: Systematic grouping by radicals/components
   - System provides: Characters sharing components (e.g., all with 氵water radical)
   - Use for: Progressive learning sequences

3. **Self-study app developer:**
   - Requirement: Show character decomposition in mobile app
   - Data needs: IDS, stroke order, semantic hints
   - Performance: Fast lookup, offline capability

## Required Capabilities

### Character-Level
- ✅ IDS decomposition (show structure)
- ✅ Radical identification (search by radical)
- ✅ Etymology data (learning mnemonics)
- ✅ Stroke order (writing practice)
- ⚠️ Semantic/phonetic classification (which component carries meaning vs. sound)

### Word-Level
- Optional: Word segmentation for context
- Not needed: Complex morphological tagging

## Library Fit Analysis

### makemeahanzi
**Excellent fit (9/10):**
- ✅ Rich etymology data with type (ideographic, pictophonetic, etc.)
- ✅ Semantic and phonetic hints explicitly marked
- ✅ SVG stroke data for animations
- ✅ IDS decomposition
- ✅ JSON format (easy integration with web/mobile)
- ⚠️ Coverage: 9,000+ characters (sufficient for learners, not comprehensive)

**Sample data:**
```json
{
  "character": "認",
  "decomposition": "⿰言刃",
  "etymology": {
    "type": "pictophonetic",
    "phonetic": "刃",
    "semantic": "言"
  }
}
```

### cjklib/cjklib3
**Good fit (7/10):**
- ✅ Comprehensive character coverage
- ✅ IDS decomposition
- ✅ Radical lookups
- ❌ Limited etymology data
- ⚠️ Python 3 via fork (deployment complexity)
- ❌ No stroke order SVG

### CJKVI-IDS
**Moderate fit (5/10):**
- ✅ Complete CJK coverage
- ✅ IDS decomposition
- ❌ No etymology
- ❌ No stroke order
- ❌ No semantic/phonetic distinction
- ⚠️ Raw IDS text (requires parser)

### HanLP/Stanza/LTP
**Poor fit (2/10):**
- ❌ No character decomposition
- ✅ Word segmentation (useful for context)
- Not designed for educational character analysis

## Recommended Solution

**Primary: makemeahanzi**

### Implementation:
1. Download makemeahanzi JSON files
2. Parse into SQLite or key-value store
3. Build API:
   ```python
   def get_character_info(char):
       return {
           'decomposition': '⿰言刃',
           'components': ['言', '刃'],
           'etymology': {...},
           'strokes': [svg_paths...]
       }
   ```
4. For characters not in makemeahanzi, fall back to CJKVI-IDS (IDS only, no etymology)

### Why this works:
- 9K characters cover HSK 1-6 + common characters (sufficient for learners)
- Rich etymology enables mnemonic generation
- Stroke order supports writing practice
- JSON format = easy web/mobile integration
- No heavy NLP dependencies

### What's missing:
- Component genealogy (how components evolved)
- Cross-references to related characters
- Difficulty ratings
- **Solution:** Build on top of makemeahanzi data

## Alternative Approach: Custom Dataset

If makemeahanzi is insufficient, consider:
1. Start with makemeahanzi core data
2. Enhance with linguistic annotations
3. Add pedagogy-specific fields:
   - Frequency rank
   - HSK level
   - Related characters
   - Common mnemonics
4. Curate for learner needs

## Example Integration: Flashcard App

```
User sees: 認

App displays:
┌─────────────────────────────┐
│ 認 (rèn) - recognize        │
├─────────────────────────────┤
│ Components:                  │
│ 言 (words) + 刃 (blade)      │
│                              │
│ Etymology: Pictophonetic     │
│ Phonetic: 刃 (rèn)          │
│ Semantic: 言 (words)        │
│                              │
│ Mnemonic: Using sharp words  │
│ to distinguish/recognize     │
└─────────────────────────────┘

[Show stroke order animation]
```

Data source: makemeahanzi JSON + custom mnemonic database

---

**Verdict:** makemeahanzi is ideal for educational use cases. Combine with custom learning scaffolding for complete solution.
