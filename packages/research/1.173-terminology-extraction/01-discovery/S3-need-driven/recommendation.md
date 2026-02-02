# S3 Need-Driven: Practical Recommendations

## Executive Summary

Real-world analysis confirms S2 technical findings:
- **pyate**: High-value for English/Italian technical terminology (60-80% time savings in translation)
- **KeyBERT**: Only viable option for CJK, but requires validation (precision ~60-70% for technical terms)

**Key Insight**: Automated extraction is **time-saving** (prep work), not **replacement** (human review essential).

## Use Case Validation

### Translation Workflows: ✅ High Value

**Quantified Benefits**:
- **Time savings**: 60-80% reduction in terminology preparation (2-4 hours → 30-60 min per 10K words)
- **ROI**: Bilingual extraction (e.g., XTM) saves 80% of glossary creation time
- **Translator feedback**: "Translation life much easier" with KeyBERT

**Reality Check**:
- CAT tools prefer integrated features (Python libraries require export/import)
- Precision ~70-80% for pyate, ~60-70% for KeyBERT (CJK) → human validation required
- Works best for **initial glossary creation**, not real-time translation support

**Recommendation**: **Use for large projects** (>5,000 words), **recurring domains** (glossary reuse), **multiple translators** (consistency). Skip for small/one-off translations.

### Technical Writing: ✅ Moderate Value

**Benefits**:
- Glossary generation for documentation
- Terminology consistency checking
- Index creation (KeyBERT for semantic keywords)

**Challenges**:
- Requires integration into docs-as-code workflow (Sphinx, MkDocs)
- One-time use per documentation set (less recurring value than translation)
- Manual review still needed (domain experts validate terms)

**Recommendation**: **Use for documentation >10K words** with complex terminology. Integrate into CI/CD for automated glossary updates.

### Domain-Specific NLP: ✅ High Value (Foundation)

**Use Case**: Build domain-specific models (medical, legal, engineering NLP)

**Value**:
- Terminology extraction is **foundation** for domain ontologies
- Multi-word term recognition (pyate) critical for technical domains
- Fine-tuning embeddings on extracted terminology improves downstream tasks

**Recommendation**: pyate for **English domain modeling**, KeyBERT for **CJK/multilingual domains**.

## Integration Patterns: Validated

### spaCy Pipeline (pyate)

**Pattern**: Add pyate as pipeline component
```python
import spacy
from pyate import combo_basic

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("combo_basic")
doc = nlp("Technical document...")
terms = doc._.terms
```

**Value**: If already using spaCy, pyate is **natural extension**. No additional infrastructure.

**Trade-off**: Requires spaCy models (100MB-500MB). If not using spaCy, KeyBERT may be lighter.

### sentence-transformers Ecosystem (KeyBERT)

**Pattern**: Use pre-trained embeddings, integrate with semantic search stack
```python
from keybert import KeyBERT
kw_model = KeyBERT("paraphrase-multilingual-MiniLM-L12-v2")
keywords = kw_model.extract_keywords("Document...")
```

**Value**: If building semantic search / retrieval system, KeyBERT reuses **same BERT models**. Infrastructure overlap.

**Trade-off**: BERT models are large (80MB-1.1GB). Not worth loading just for term extraction.

### Standalone / Batch Processing

**Use Case**: Process large corpus (thousands of documents)

**Pattern**:
1. Load model once (pyate: spaCy, KeyBERT: BERT)
2. Batch process documents (minimize model loading overhead)
3. Export results to database / CSV
4. Human review interface (validate extracted terms)

**Performance**: Both libraries support batch processing efficiently.

## TCO Analysis: Practical Costs

### Installation Complexity

| Library | Install Steps | Download Size | Time to First Run |
|---------|--------------|---------------|-------------------|
| **pyate** | `pip install pyate` + download spaCy model | ~150MB-600MB | ~5-10 min |
| **KeyBERT** | `pip install keybert` (auto-downloads model) | ~100MB-1.2GB | ~2-5 min |

**Verdict**: KeyBERT slightly simpler (auto-download), but pyate is straightforward if using spaCy already.

### Resource Requirements

| Metric | pyate | KeyBERT | Notes |
|--------|-------|---------|-------|
| **CPU** | ~2-4 cores | ~4-8 cores (or GPU) | KeyBERT benefits from GPU |
| **Memory** | ~500MB-1GB | ~1-2GB | BERT models are larger |
| **Disk** | ~200MB-600MB | ~500MB-1.5GB | Model storage |

**Verdict**: pyate is lighter. KeyBERT manageable for server deployments, but heavy for edge/mobile.

### Maintenance Overhead

**pyate**:
- spaCy model updates (quarterly)
- Python dependency conflicts (rare, spaCy stable)
- **Effort**: ~1-2 hours/year

**KeyBERT**:
- sentence-transformers model updates (bi-annual)
- BERT model changes (new models, deprecations)
- **Effort**: ~2-4 hours/year

**Verdict**: Both low-maintenance. pyate slightly lower due to spaCy stability.

### Learning Curve

| Audience | pyate | KeyBERT | Notes |
|----------|-------|---------|-------|
| **Non-ML Engineer** | Moderate (need spaCy basics) | Easy (3 lines of code) | KeyBERT simpler API |
| **NLP Engineer** | Easy (familiar with spaCy) | Easy (familiar with BERT) | Both straightforward |
| **Translator/Writer** | Hard (Python required) | Moderate (simple script) | Both require coding skills |

**Verdict**: KeyBERT easier for beginners. pyate easier if already using spaCy.

## CJK Quality in Practice

### Chinese (中文)

**KeyBERT** (generic multilingual):
- **Tokenization**: Character-level ("自然语言处理" → ["自", "然", "语", "言", "处", "理"])
- **Quality**: ~60-70% precision for technical terms (may extract characters, not words)
- **Validation**: Manual review **essential** (check word boundaries, technical accuracy)

**chinese_keybert** (specialized fork):
- **Tokenization**: Word-level via CKIP ("自然语言处理" → single token)
- **Quality**: ~70-80% precision (better word segmentation)
- **Trade-off**: Chinese-only, additional dependency

**Recommendation**: If Chinese-only, use **chinese_keybert**. If multi-CJK, use **KeyBERT + manual validation**.

### Japanese (日本語)

**KeyBERT** (multilingual):
- **Tokenization**: Mixed (Kanji character-level, Kana syllabic)
- **Quality**: ~65-75% precision (handles multiple scripts reasonably)
- **Validation**: Review for proper term boundaries

**Alternative**: textacy + spaCy Japanese model (if KeyBERT insufficient)

**Recommendation**: **KeyBERT** is viable, but expect ~25-35% false positives requiring manual filtering.

### Korean (한국어)

**KeyBERT** (multilingual):
- **Tokenization**: Syllable-level (Hangul) + character-level (Hanja)
- **Quality**: ~65-75% precision
- **Validation**: Manual review for technical terms

**Recommendation**: **KeyBERT** only option. Plan for human-in-loop validation.

## Decision Framework: Practical

```
Do you need CJK (Chinese, Japanese, Korean) support?
├─ YES → KeyBERT (only option)
│         ├─ Chinese-only → chinese_keybert (better quality)
│         ├─ Multi-CJK → KeyBERT + multilingual model
│         └─ **CRITICAL**: Plan for 25-40% manual validation (character-level issues)
│
└─ NO (English, Italian, or wait for pyate language support)
    │
    ├─ Do you have existing spaCy infrastructure?
    │  ├─ YES → pyate (natural fit, reuse spaCy models)
    │  └─ NO → pyate still recommended for terminology (precision)
    │
    ├─ Document size:
    │  ├─ Large (>5,000 words) → Automated extraction justified (60-80% time savings)
    │  └─ Small (<1,000 words) → Manual may be faster (extraction overhead)
    │
    └─ Use case:
        ├─ Translation → pyate (technical terms for glossaries)
        ├─ Technical writing → pyate (glossaries, documentation)
        ├─ Content tagging → KeyBERT (semantic keywords)
        └─ Domain NLP → pyate (foundation for ontologies)
```

## S3 Top Recommendations

### 1. For CJK Translation/Technical Writing:
**KeyBERT with human validation workflow**
- **Extract**: KeyBERT with `paraphrase-multilingual-MiniLM-L12-v2`
- **Review**: Human validation (expect ~25-40% false positives for CJK)
- **Effort**: 60-90 min per 10K words (vs 2-4 hours manual)
- **Value**: Automation handles volume, humans ensure CJK quality

### 2. For English/Italian Translation:
**pyate for initial glossary + CAT tool integration**
- **Extract**: pyate with combo_basic
- **Export**: CSV/TBX format to CAT tool
- **Effort**: 30-60 min per 10K words (vs 2-4 hours manual)
- **Value**: 60-80% time savings, ~70-80% precision

### 3. For Multilingual Technical Writing:
**KeyBERT for CJK + pyate for English (hybrid)**
- **Extract**: Per-language (best algorithm for each)
- **Consolidate**: Merge glossaries
- **Value**: Maximum quality per language

### 4. For Domain-Specific NLP:
**pyate as foundation for English, KeyBERT for CJK/multilingual**
- **Extract**: Multi-word technical terms (critical for ontologies)
- **Use**: Fine-tune embeddings, train domain classifiers
- **Value**: Terminology extraction as NLP pipeline component

## Workflow Pattern: Human-in-Loop

**Validated Pattern** (works across use cases):
1. **Automated Extraction**: pyate (English) or KeyBERT (CJK) on source corpus
2. **Bulk Filtering**: Remove obvious false positives (frequency < threshold, single characters for CJK)
3. **Human Review**: Domain expert validates technical accuracy (~15-30 min per 100 terms)
4. **Glossary Export**: CSV/TBX to CAT tool or documentation system
5. **Maintenance**: Add missed terms manually (ongoing, as new documents processed)

**Value**: Automation handles **volume** (extract 1000s of candidates), humans ensure **quality** (validate technical accuracy, domain fit).

## Next Steps (S4: Strategic)

**Key questions for S4**:
1. **Long-term viability**: Which libraries will be maintained in 2027-2030?
2. **Technology evolution**: Will character-level CJK improve (new BERT tokenizers)?
3. **Integration trends**: Will CAT tools adopt Python libraries, or remain separate?
4. **Alternative approaches**: Should teams build custom extractors vs use libraries?
