# S2-Comprehensive: Recommendation

## Two-Tier Approach

Based on comprehensive analysis, recommend splitting the solution:

### Tier 1: Character Decomposition
**Tool:** makemeahanzi + CJKVI-IDS hybrid

**Rationale:**
- makemeahanzi provides rich data for common characters (9K+)
  - IDS decomposition
  - Etymology information
  - Stroke order SVG data
  - JSON format (modern, easy to parse)
- CJKVI-IDS fills gaps for comprehensive CJK coverage
- Both are data sources, not libraries - gives full control
- No Python 2 legacy issues
- Active maintenance

**Implementation:**
1. Primary: Parse makemeahanzi JSON for covered characters
2. Fallback: Parse CJKVI-IDS for remaining CJK characters
3. Build custom API layer for application needs

### Tier 2: Word Segmentation
**Tool:** HanLP

**Rationale:**
- Production-ready Python 3 library
- Comprehensive NLP pipeline
- Active development
- pip installable
- Handles word boundary identification

**Caveat:** HanLP provides segmentation, not morpheme decomposition.

## The Morpheme Decomposition Gap

**Critical finding:** No library found that decomposes Chinese compounds into morphemes.

**Example of gap:**
- Character decomposition: 电 = IDS ⿻日乚 (components)
- Word segmentation: "我用电脑" → ["我", "用", "电脑"]
- **Missing:** "电脑" → "电" + "脑" (morpheme analysis)

**Options:**
1. **Redefine requirements:** Focus on character decomposition + word segmentation
2. **Custom implementation:** Build morpheme analyzer using:
   - Word segmentation from HanLP
   - Character decomposition from makemeahanzi
   - Linguistic rules for identifying productive compounds
3. **Accept limitation:** Most compounds are lexicalized (treated as single words)

## Recommended Stack

```
Application Layer
    ↓
Word Segmentation: HanLP
    ↓
Character Decomposition: makemeahanzi + CJKVI-IDS
    ↓
Data Layer: JSON + IDS text files
```

## Why Not cjklib?

**cjklib is functionally superior for character analysis, but:**
- Python 2 codebase
- Python 3 requires fork + manual setup
- Not pip installable for Python 3
- Uncertain maintenance

**Alternative:** Extract cjklib's algorithms and port to modern Python, using makemeahanzi/CJKVI-IDS as data sources. This gets the best of both:
- Proven algorithms (cjklib)
- Modern data formats (makemeahanzi)
- Clean Python 3 code
- Full control over implementation

## Production Deployment

**Low-risk path:**
1. Start with makemeahanzi data (9K characters covers most use cases)
2. Parse JSON in Python 3
3. Build simple API: `decompose(char) → components`
4. Add CJKVI-IDS for complete coverage as needed
5. Use HanLP for word segmentation

**Higher-effort, more capable path:**
1. Port cjklib algorithms to Python 3
2. Use makemeahanzi + CJKVI-IDS as data
3. Build comprehensive character analysis library
4. Integrate with HanLP for word processing

## Next Steps for S3: Need-Driven

Must clarify actual use cases:
- What is "compound word analysis" supposed to do?
- Are we analyzing character structure or word structure?
- What's the end goal: teaching, search, analysis?

Different use cases may lead to different recommendations.

---

Sources:
- [makemeahanzi GitHub](https://github.com/skishore/makemeahanzi)
- [CJKVI-IDS GitHub](https://github.com/cjkvi/cjkvi-ids)
- [HanLP GitHub](https://github.com/hankcs/HanLP)
- [cjklib3 Fork](https://github.com/free-utils-python/cjklib3)
