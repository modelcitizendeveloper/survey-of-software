# Translation Workflow Use Case

## Typical Translation Terminology Workflow

**Without Automated Extraction**:
1. Translator receives source document
2. Manually identifies technical terms while translating
3. Adds terms to glossary as encountered
4. **Time**: 2-4 hours per 10,000-word document for terminology work

**With Automated Extraction**:
1. Run terminology extraction on source document
2. Review extracted terms (validate, filter false positives)
3. Add validated terms to glossary
4. **Time**: 30-60 minutes per 10,000-word document

**Time Savings**: 60-80% reduction in terminology preparation time

Source: [Nimdzi](https://www.nimdzi.com/term-extraction/)

## CAT Tool Integration

### Current State:
- **Most CAT tools** (SDL Trados, MemoQ, Smartcat) have **built-in term extraction**
- Python libraries (pyate, KeyBERT) require **manual export/import workflow**
- **Translator preference**: Integrated tools within CAT environment

Per [LinguaGreca survey](https://linguagreca.com/blog/2018/03/nine-terminology-extraction-tools-are-they-useful-for-translators/):
> Translators prefer to have terminology extraction integrated in their CAT tool, rather than using separate tools.

### Integration Pattern:
```
Source Document → Python Extract → CSV/TBX → Import to CAT Tool → Human Review → Glossary
```

**Trade-off**: Python libraries offer better algorithms but require extra steps. CAT built-in tools are convenient but less sophisticated.

## Bilingual Terminology Extraction

**Need**: Extract source term + target translation pairs from aligned text (translation memories)

**Challenge**: pyate and KeyBERT are **monolingual** (extract from single language)

**Workflow for Bilingual**:
1. Extract terms from source language (EN: pyate or KeyBERT)
2. Extract terms from target language (CJK: KeyBERT only viable option)
3. **Manual alignment**: Match source terms to target translations
4. Alternative: Use bilingual extraction tools (SynchroTerm, XTM)

**Time Savings** (per XTM): Automated bilingual extraction saves **80% of glossary creation time**

## pyate in Translation

### Strengths:
- ✅ High precision for technical terms (Combo Basic algorithm)
- ✅ Multi-word term focus (translations often need phrases, not single words)
- ✅ Domain-specific (Weirdness algorithm useful for specialized translations)

### Weaknesses:
- ❌ English/Italian only (no CJK support)
- ❌ Monolingual (no automatic source-target pairing)
- ❌ Requires export to CAT tool (not integrated)

### Best For:
- English → X translations (extract English source terms)
- Technical domain translations (medical, legal, engineering)
- Initial glossary creation (one-time extraction)

## KeyBERT in Translation

### Strengths:
- ✅ Multilingual (50-109 languages) including CJK
- ✅ Works for low-resource languages (no corpora needed)
- ✅ Simple API (easy to integrate into custom workflows)

### Weaknesses:
- ❌ Keywords, not terminology (may extract non-technical words)
- ❌ Character-level CJK (may miss proper Chinese word boundaries)
- ❌ Requires filtering (more false positives than pyate)

### Best For:
- CJK language pairs (Chinese, Japanese, Korean)
- Multilingual projects (single tool for many languages)
- Content tagging (route documents to domain-specific translators)

## Real-World Translator Feedback

**Positive**: Per [translator testimonial](https://www.veriloquium.com/keybert/):
> "My translation and localization life is much easier today thanks to this tool [KeyBERT]... a valuable tool for any translator or linguist."

**Caveat**: KeyBERT extracts keywords, not terms. Translators should **filter and validate** output.

## Recommended Workflow

### For English/Italian → X Translation:
1. **Extract** source terms: pyate with combo_basic
2. **Review** extracted terms (precision ~70-80%, some filtering needed)
3. **Export** to CSV/TBX format
4. **Import** to CAT tool glossary
5. **Translate** terms in context (CAT tool termbase feature)
6. **Maintain** glossary (add missed terms during translation)

**Effort**: ~30-60 min for 10,000-word document (vs 2-4 hours manual)

### For CJK → X or X → CJK Translation:
1. **Extract** source terms: KeyBERT with multilingual model
2. **Filter** false positives (keywords vs terminology)
3. **Validate** CJK terms (check word boundaries, technical accuracy)
4. **Export** to CAT tool
5. **Human-in-loop** review (CJK extraction ~60-70% precision, needs validation)

**Effort**: ~60-90 min for 10,000-word document (CJK requires more validation)

### For Bilingual Terminology:
1. **Option A**: Use CAT tool built-in (SynchroTerm, XTM) if available
2. **Option B**: Extract monolingual (pyate/KeyBERT) + manual alignment
3. **Recommended**: Option A for speed, Option B for algorithm quality

## Integration with CAT Tools

### Export Formats:
- **CSV**: Simple, universal (all CAT tools support)
- **TBX** (TermBase eXchange): Standard for terminology (SDL Trados, MemoQ)
- **Excel**: Bilingual glossaries (source | target | domain | notes)

### Sample CSV Export (pyate/KeyBERT → CAT):
```python
import pandas as pd
from pyate import combo_basic

text = "Your source document..."
terms = combo_basic(text).sort_values(ascending=False).head(100)

# Export to CSV for CAT tool import
df = pd.DataFrame({
    'Source Term': terms.index,
    'Termhood Score': terms.values,
    'Target Term': '',  # Fill manually or via MT
    'Domain': 'Technical',
    'Notes': ''
})
df.to_csv('glossary_for_cat.csv', index=False)
```

## Value Proposition

**When Automated Extraction Justifies Effort**:
- ✅ Large documents (>5,000 words) with technical terminology
- ✅ Recurring projects (same domain, build glossary once, reuse)
- ✅ Multiple translators (shared glossary ensures consistency)
- ✅ Tight deadlines (60-80% time savings on term prep)

**When Manual Curation is Better**:
- ❌ Small documents (<1,000 words) - extraction overhead > manual effort
- ❌ General content (few technical terms to extract)
- ❌ One-off projects (no glossary reuse value)
- ❌ High precision required (extraction ~70-80% precision, manual ~95%+)

## Bottom Line for Translators

**pyate**: Best for **English/Italian technical translations**. High precision, multi-word terms, domain-specific. Export to CAT tool via CSV/TBX.

**KeyBERT**: Best for **CJK language pairs**. Only viable automated option for Chinese/Japanese/Korean. Requires validation (keywords vs terminology, character-level output).

**Recommendation**: Use automated extraction for **initial glossary creation** (60-80% time savings), then **human review and maintenance** (precision improvement from 70-80% to 95%+). Automation handles volume, humans ensure quality.
