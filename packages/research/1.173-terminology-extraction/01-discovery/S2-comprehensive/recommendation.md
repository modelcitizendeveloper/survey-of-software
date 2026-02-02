# S2 Comprehensive: Technical Recommendations

## Executive Summary

Deep analysis reveals **fundamentally different tools for different goals**:
- **pyate**: Pure terminology extraction (technical terms, domain-specific)
- **KeyBERT**: Semantic keyword extraction (meaning-based, content-level)

**CJK Impact**: Research label `cjk` is **critical decision factor**. pyate has no CJK support (missing corpora), making KeyBERT the only viable option for Chinese, Japanese, Korean.

## Main Findings

### 1. Terminology vs Keywords: Different Goals

**Critical Insight**: These libraries solve **different problems**.

| Aspect | Terminology Extraction (pyate) | Keyword Extraction (KeyBERT) |
|--------|-------------------------------|------------------------------|
| **Goal** | Domain-specific technical terms | Semantically important words |
| **Target** | Multi-word expressions, low ambiguity | Document-level semantic relevance |
| **Use Case** | Glossaries, translation memory | Content tagging, indexing |
| **Example Output** | "natural language processing", "gradient descent optimization" | "language", "processing", "gradient descent" |

**Evidence**: Per [Wikipedia](https://en.wikipedia.org/wiki/Terminology_extraction), terminologists focus on **terms specific to a technical domain** (organized knowledge), while information retrieval focuses on **indexing terms** (document retrieval).

**Implication**: Choice depends on use case, not just "which is better."

### 2. pyate Strengths & Weaknesses

**Strengths**:
- ✅ **Highest precision for terminology** (Astrakhantsev 2016: combo_basic most precise)
- ✅ **Multiple algorithms** (C-Value, Combo Basic, Weirdness, Basic, Term Extractor)
- ✅ **Multi-word term focus** (designed for phrases like "machine learning model")
- ✅ **Domain-specificity** (Weirdness contrasts technical vs general corpus)
- ✅ **Fast** (10x faster than KeyBERT, statistical algorithms)

**Weaknesses**:
- ❌ **NO CJK support** (missing general corpora for Chinese, Japanese, Korean)
- ❌ **Limited languages** (only English, Italian pre-built)
- ❌ **Requires corpora** (Weirdness and Term Extractor need reference corpora)
- ❌ **spaCy dependency** (100MB-500MB language models)

**Verdict**: **Best for English/Italian terminology extraction**. Not viable for CJK.

### 3. KeyBERT Strengths & Weaknesses

**Strengths**:
- ✅ **Excellent CJK support** (50-109 languages via multilingual BERT)
- ✅ **Semantic understanding** (meaning-based, not just frequency)
- ✅ **Simple API** ("pip install + 3 lines of code")
- ✅ **No corpora required** (pre-trained BERT works immediately)
- ✅ **Multilingual** (single model for many languages)

**Weaknesses**:
- ❌ **Keywords, not terminology** (different goal - semantic importance vs technical terms)
- ❌ **Character-level CJK** (Chinese tokenized as characters, may miss word boundaries)
- ❌ **Slow** (BERT inference 10x slower than pyate)
- ❌ **Large models** (80MB-1.1GB vs pyate's statistical approach)

**Verdict**: **Best for CJK keyword extraction**. Use chinese_keybert fork for better Chinese quality.

### 4. CJK Support: Decisive Factor

**Requirement**: Research label `cjk` indicates Chinese, Japanese, Korean support needed.

**Analysis**:
- **pyate**: ❌ No CJK corpora → **Cannot be recommended**
- **KeyBERT**: ✅ Works out-of-box → **Only viable option**

**CJK-Specific Challenges**:
- Multilingual BERT tokenizes Chinese **character-level** (not word-level)
- May extract "语言" (language) and "处理" (processing) separately, missing "自然语言处理" (natural language processing)
- **Solution**: chinese_keybert fork (CKIP word segmentation) for Chinese-only use cases

**Recommendation**: KeyBERT with `paraphrase-multilingual-MiniLM-L12-v2` for multi-CJK, chinese_keybert for Chinese-only.

### 5. Algorithm Comparison

**pyate Algorithms** (ranked by precision per Astrakhantsev 2016):
1. **Combo Basic** (highest precision): Weighted frequency + containment + length
2. **C-Value** (close second): Multi-word term recognition, nested terms
3. **Basic** (baseline): Frequency with POS filtering

**KeyBERT Algorithm**:
- BERT document embedding → candidate embeddings → cosine similarity → top-k

**Benchmark**: Combo Basic beats Basic and C-Value. PU-ATR and KeyConceptRel have higher precision but are not implemented (and PU-ATR is much slower).

**Implication**: pyate's combo_basic is **state-of-practice** (not state-of-art, but best available in pip-installable libraries).

### 6. Performance Trade-offs

| Metric | pyate | KeyBERT | Ratio |
|--------|-------|---------|-------|
| **Speed** (1000 words) | ~0.1-0.2s | ~1-2s | 10x faster |
| **Memory** | 200-600MB | 500-1500MB | 2-3x lighter |
| **Model Size** | 100-500MB (spaCy) | 80-1100MB (BERT) | Similar |

**Optimization**:
- pyate: Use `sm` spaCy models (smallest)
- KeyBERT: Use ONNX backend (1.3-1.5x faster), `MiniLM` models (80MB)

**Verdict**: pyate is faster and lighter, but KeyBERT is acceptable for most use cases.

## Recommendations by Use Case

### Translation Workflows

**Glossary Creation** (technical term extraction):
- **English/Italian**: pyate with combo_basic
- **CJK**: KeyBERT with multilingual model (fallback: manual review)

**Content Tagging** (routing to translators):
- **All languages**: KeyBERT (semantic keywords for topic identification)

**Chinese-English Translation**:
- **chinese_keybert** for Chinese terms
- **pyate** for English terms
- **Challenge**: Character-level Chinese tokenization may miss multi-character terms

### Technical Writing

**Glossary Generation**:
- **English/Italian**: pyate (purpose-built for terminology)
- **CJK**: KeyBERT (only option, but review character-level output)

**Index Creation**:
- **All languages**: KeyBERT (semantic keywords for index)

**Domain-Specific NLP** (medical, legal, engineering):
- **English/Italian**: pyate (domain terminology extraction via Weirdness)
- **CJK**: KeyBERT + manual filtering (BERT may extract keywords, not domain terms)

### Multilingual Projects (CJK + English)

**Single Model for All**:
- **KeyBERT** with `paraphrase-multilingual-MiniLM-L12-v2` (50+ languages)
- Consistent approach across languages
- Trade-off: Character-level CJK, keywords (not terms)

**Per-Language Optimization**:
- **English**: pyate (terminology)
- **Chinese**: chinese_keybert (better word segmentation)
- **Japanese/Korean**: KeyBERT with multilingual model
- Trade-off: Inconsistent approaches, but higher quality

## S2 Decision Tree

```
Do you need CJK (Chinese, Japanese, Korean) support?
├─ YES → KeyBERT (only viable option)
│         ├─ Chinese-only → chinese_keybert (better word segmentation)
│         ├─ Multi-CJK → KeyBERT + paraphrase-multilingual-MiniLM-L12-v2
│         └─ Note: Character-level tokenization, keywords not terms
│
└─ NO (English, Italian, or other spaCy-supported languages)
    │
    ├─ Do you need TERMINOLOGY extraction (technical terms, glossaries)?
    │  ├─ YES → pyate with combo_basic
    │  │         ├─ Multi-word terms: Use C-Value
    │  │         ├─ Domain-specific: Use Weirdness (requires general corpus)
    │  │         └─ General: Use Combo Basic (highest precision)
    │  │
    │  └─ NO → Go to keyword extraction
    │
    └─ Do you need KEYWORD extraction (semantic importance, content tags)?
        ├─ YES → KeyBERT
        │         ├─ English: all-MiniLM-L6-v2 (80MB, fast)
        │         ├─ Multilingual: paraphrase-multilingual-MiniLM-L12-v2 (420MB)
        │         └─ High quality: paraphrase-multilingual-mpnet-base-v2 (1.1GB)
        │
        └─ BOTH? → Run both, combine results
                    ├─ pyate → Technical terms
                    ├─ KeyBERT → Semantic keywords
                    └─ Union → Comprehensive coverage
```

## S2 Top Recommendations

### 1. For CJK Use Cases (per research label):
**KeyBERT with multilingual model**
- **Model**: `paraphrase-multilingual-MiniLM-L12-v2` (420MB, 50+ languages)
- **Rationale**: Only pip-installable library with CJK support
- **Trade-off**: Keywords (not terminology), character-level Chinese
- **Mitigation**: Use chinese_keybert for Chinese-only, manual review for technical terms

### 2. For English/Italian Terminology Extraction:
**pyate with combo_basic algorithm**
- **Rationale**: Highest precision (Astrakhantsev 2016), purpose-built for terminology
- **Use cases**: Glossaries, translation memory, domain-specific NLP
- **Trade-off**: No CJK, requires spaCy dependency

### 3. For Hybrid Multilingual (CJK + English):
**KeyBERT (CJK) + pyate (English)**
- **Rationale**: Best-of-both (KeyBERT for CJK, pyate for English terminology)
- **Trade-off**: Two libraries, inconsistent approaches
- **Value**: Maximizes quality per language

## Next Steps (S3: Need-Driven)

**Recommended focus for S3**:
1. **Real-world use cases**: Translation workflows, technical writing, domain-specific NLP
2. **CJK quality assessment**: How well does KeyBERT handle Chinese/Japanese/Korean in practice?
3. **Integration patterns**: spaCy pipelines (pyate) vs sentence-transformers (KeyBERT)
4. **TCO analysis**: Installation, dependencies, resource requirements
5. **Community feedback**: What do users report about CJK quality?

**Key questions for S3**:
- Can chinese_keybert quality justify additional dependency?
- What is acceptable precision for CJK technical term extraction?
- Should users run both libraries and combine results?
- Are there workflow patterns that maximize value (e.g., KeyBERT extraction → human validation)?
