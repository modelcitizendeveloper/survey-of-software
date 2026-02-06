# Head-to-Head Comparison: pyate vs KeyBERT

## Quick Decision Matrix

| Criterion | pyate | KeyBERT | Winner |
|-----------|-------|---------|--------|
| **Terminology extraction** | ✓ Purpose-built | ✗ Keywords, not terms | **pyate** |
| **Keyword extraction** | ✗ Not designed for it | ✓ Semantic keywords | **KeyBERT** |
| **Multilingual (general)** | ~70 languages (via spaCy) | 50-100+ languages | **KeyBERT** |
| **CJK support (Chinese/Japanese/Korean)** | ❌ No corpora | ✅ Works out-of-box | **KeyBERT** |
| **Speed** | Fast (stats) | Slow (BERT) | **pyate** |
| **Memory footprint** | Low (~100MB spaCy model) | High (80MB-1.1GB BERT) | **pyate** |
| **Multi-word terms** | ✓ Designed for this | ~ May split into chars (CJK) | **pyate** |
| **Semantic understanding** | ✗ Statistical only | ✓ BERT embeddings | **KeyBERT** |
| **No training required** | ✓ (but needs corpora) | ✓ Pre-trained models | **Tie** |
| **Installation simplicity** | Moderate (spaCy + model) | Easy (pip + auto-download) | **KeyBERT** |

## Fundamental Difference: Terminology vs Keywords

### Terminology Extraction (pyate)
**Goal**: Find **domain-specific technical terms** (multi-word expressions, low ambiguity, conceptual importance)

**Example Input**: "Machine learning models use gradient descent for optimization."

**pyate Output**:
- "machine learning models" (technical term)
- "gradient descent" (technical term)
- "optimization" (domain-specific concept)

**Characteristics**:
- Multi-word terms preferred ("natural language processing" > "language")
- Domain-specificity (contrasts technical vs general corpus via Weirdness algorithm)
- Low ambiguity (terms have specific technical meaning)

### Keyword Extraction (KeyBERT)
**Goal**: Find **semantically important words/phrases** (document-level semantic relevance)

**Example Input**: "Machine learning models use gradient descent for optimization."

**KeyBERT Output**:
- "machine learning" (semantically central to document)
- "gradient descent" (semantically central to document)
- "optimization" (important concept)

**Characteristics**:
- Semantic similarity to document meaning
- May include general words if semantically important ("important discovery", "key finding")
- Single or multi-word based on semantic coherence

Per [Wikipedia](https://en.wikipedia.org/wiki/Terminology_extraction) and [Sketch Engine](https://www.sketchengine.eu/guide/keywords-and-term-extraction/):
> Terminologists focus on finding **terms specific to a particular technical domain**, while information retrieval focuses on **indexing terms capable of distinguishing among documents**.

## Algorithm Comparison

### pyate (Statistical + Linguistic)

**Algorithms**:
1. **C-Value**: Multi-word term recognition (nested term handling)
2. **Combo Basic**: Weighted frequency + containment + length (highest precision)
3. **Weirdness**: Technical corpus vs general corpus contrast
4. **Basic**: Frequency with POS filtering
5. **Term Extractor**: Hybrid approach

**Process**:
1. spaCy POS tagging → identify noun phrases
2. Apply statistical algorithm (frequency, containment, corpus contrast)
3. Rank candidates by termhood score
4. Return top-k terms

**Benchmark**: Astrakhantsev 2016 shows Combo Basic has highest precision for terminology extraction.

### KeyBERT (Transformer-Based)

**Algorithm**:
1. BERT embedding for full document (768-dim vector)
2. BERT embedding for each n-gram candidate
3. Cosine similarity between document and candidates
4. Return top-k by similarity

**Process**:
- Purely semantic (no POS tagging, no frequency counting)
- Finds candidates **semantically similar to document meaning**
- No contrast with general corpus (single-document operation)

## Dependency Comparison

### pyate

**Required**:
- spaCy (100MB-500MB language models)
- numpy, pandas
- pyahocorasick
- General domain corpus (for Weirdness, Term Extractor)

**Total Install**: ~150MB-600MB (depending on spaCy model)

**Languages**: Depends on spaCy model + corpus availability
- ✅ English, Italian (pre-built)
- ⚠️ ~70 languages (spaCy models exist, but no pyate corpora)
- ❌ CJK (spaCy models exist, but no general corpora for pyate algorithms)

### KeyBERT

**Required**:
- sentence-transformers (or alternative backend)
- BERT model (80MB-1.1GB depending on model)

**Total Install**: ~100MB-1.2GB (depending on model choice)

**Languages**: Depends on BERT model
- ✅ English (`all-MiniLM-L6-v2`): 80MB
- ✅ Multilingual 50+ languages (`paraphrase-multilingual-MiniLM-L12-v2`): 420MB
- ✅ 109 languages including CJK (`LaBSE`): 470MB

## Performance: Speed & Resource Usage

| Metric | pyate | KeyBERT |
|--------|-------|---------|
| **Inference Time** (1000 words) | ~0.1-0.2s | ~1-2s |
| **Relative Speed** | 10x faster | Baseline |
| **Memory Usage** | 200MB-600MB | 500MB-1.5GB |
| **GPU Acceleration** | ✗ Not applicable | ✓ Available (optional) |

**Bottleneck**:
- **pyate**: spaCy POS tagging (fast, CPU-efficient)
- **KeyBERT**: BERT inference (slow, GPU benefits)

**Optimization**:
- **pyate**: Use smaller spaCy models (`sm` instead of `lg`)
- **KeyBERT**: Use ONNX backend (1.3-1.5x faster), smaller models (`MiniLM` vs `mpnet`)

## Use Case Fit

### Translation Workflows

**Terminology Management**:
→ **pyate** (builds glossaries of technical terms for translators)

**Content Tagging**:
→ **KeyBERT** (identifies topics/themes for routing to translators)

**Multilingual Term Extraction**:
→ **KeyBERT** (if CJK or low-resource languages)
→ **pyate** (if English/Italian and need precise terminology)

### Technical Writing

**Glossary Generation**:
→ **pyate** (extracts technical terms for documentation glossaries)

**Index Creation**:
→ **KeyBERT** (finds semantically important keywords for document index)

**Domain-Specific NLP**:
→ **pyate** (legal, medical, engineering terminology extraction)

### CJK Language Projects

**Chinese/Japanese/Korean**:
→ **KeyBERT** (only viable option - pyate lacks CJK corpora)

**Chinese-Specific**:
→ `chinese_keybert` fork (better word segmentation via CKIP)

## Integration Recommendations

### Already Using spaCy?
→ **pyate** (natural fit, add to pipeline)

### Already Using sentence-transformers/BERT?
→ **KeyBERT** (natural fit, same infrastructure)

### Starting Fresh?
- **For terminology**: pyate (if English/Italian) or KeyBERT (if CJK)
- **For keywords**: KeyBERT
- **For speed**: pyate
- **For multilingual**: KeyBERT

## When to Use Both

**Complementary Use Case**: Run both and combine results
- **pyate** → Technical terms (high precision, domain-specific)
- **KeyBERT** → Semantic keywords (broader context)
- **Union**: Comprehensive term + keyword coverage

**Example**: Technical documentation might need both:
- Glossary (pyate) + Index (KeyBERT)
- Translation terms (pyate) + Content tags (KeyBERT)

## Bottom Line

**Choose pyate if**:
- ✅ You need **pure terminology extraction** (technical terms, glossaries)
- ✅ Language is English or Italian (pre-built support)
- ✅ Speed and resource efficiency matter
- ✅ Multi-word technical terms are critical
- ✅ You have or can build general domain corpora for your language

**Choose KeyBERT if**:
- ✅ You need **semantic keyword extraction** (topics, themes, content tags)
- ✅ Language is CJK (Chinese, Japanese, Korean) or low-resource
- ✅ Multilingual support (50-100+ languages) is required
- ✅ Semantic understanding (meaning-based) is more important than term specificity
- ✅ You don't have general domain corpora available

**Choose both if**:
- ✅ You need comprehensive coverage (technical terms + semantic keywords)
- ✅ Resource constraints are not an issue
- ✅ Use cases include both glossary generation and content tagging
