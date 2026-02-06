# KeyBERT: Deep Technical Analysis

## Algorithm Implementation

### Core Approach:
1. **Document Embedding**: Extract BERT embedding for entire document (semantic representation)
2. **Candidate Embeddings**: Extract BERT embeddings for n-gram candidates (words/phrases)
3. **Cosine Similarity**: Calculate similarity between document and each candidate
4. **Top-K Selection**: Return candidates most similar to document (highest cosine similarity)

**Key Insight**: Unlike statistical methods (frequency, co-occurrence), KeyBERT finds terms **semantically similar to the document's meaning**, not just statistically prominent.

## Embedding Backends

### Primary: sentence-transformers (Recommended)

**Models Available**:

| Model | Languages | Use Case | Size |
|-------|-----------|----------|------|
| `all-MiniLM-L6-v2` | English | Fast, good quality | 80MB |
| `paraphrase-multilingual-MiniLM-L12-v2` | 50+ languages | **Multilingual default** | 420MB |
| `paraphrase-multilingual-mpnet-base-v2` | 50+ languages | Higher quality | 1.1GB |
| `distiluse-base-multilingual-cased-v1` | 15 languages (incl. Chinese, Korean) | Lightweight multilingual | 480MB |
| `LaBSE` | **109 languages** | Maximum language coverage | 470MB |

**Performance**: Per [MDPI study](https://www.mdpi.com/2504-2289/9/3/67), `mpnet` achieved mean similarity score **0.71 ± 0.04** on STS 2017 dataset, but with higher computational demands.

### Alternative Backends:
- **Flair**: Contextual embeddings (slower, higher quality)
- **Gensim**: Word2Vec, Doc2Vec (lightweight, no transformers)
- **spaCy**: spaCy vectors (if already using spaCy)
- **USE**: Universal Sentence Encoder (Google)

## Multilingual Support

### General Multilingual:
✅ **Excellent** - Works with 50-100+ languages via multilingual BERT models

### CJK-Specific Handling:

**Tokenization** ([Google BERT docs](https://github.com/google-research/bert/blob/master/multilingual.md)):
- **Chinese**: Character-tokenized (spaces added around every CJK Unicode character before WordPiece)
- **Japanese Kanji**: Character-tokenized (same as Chinese)
- **Korean Hanja**: Character-tokenized (Chinese-origin characters)
- **Katakana/Hiragana**: Whitespace + WordPiece (normal tokenization)
- **Hangul Korean**: Whitespace + WordPiece (normal tokenization)

**Implication**: Multilingual BERT handles CJK natively, but character-level tokenization may affect term quality for Chinese.

### Chinese-Specific Implementation:

[chinese_keybert](https://github.com/JacksonCakes/chinese_keybert) exists as a specialized fork:
- Uses CKIP library for Chinese word segmentation and POS tagging
- Leverages sentence-transformers for embeddings
- **Better for Chinese** than generic multilingual BERT (proper word boundaries)

**Recommendation for CJK**: Use `paraphrase-multilingual-MiniLM-L12-v2` or language-specific BERT models (e.g., `bert-base-chinese`).

## Performance Characteristics

### Strengths:
- **Semantic understanding**: Finds keywords by meaning, not just frequency
- **Multilingual**: 50-100+ languages out-of-box
- **No training required**: Pre-trained BERT models work immediately
- **Simple API**: "pip install + 3 lines of code" design goal
- **Flexible backends**: sentence-transformers, Flair, spaCy, Gensim

### Weaknesses:
- **Compute-intensive**: BERT inference is slower than statistical methods
- **Memory footprint**: Models are 80MB-1.1GB (vs <10MB for statistical tools)
- **Keywords ≠ Terminology**: Extracts semantically important words, not necessarily technical terms
- **Character-level CJK**: Chinese/Japanese may get character-level tokens, not proper words

### Speed Comparison:

| Method | Relative Speed | Notes |
|--------|---------------|-------|
| RAKE/YAKE | 10x faster | Pure statistics |
| pyate | 5x faster | spaCy POS + stats |
| KeyBERT | Baseline (1x) | BERT inference |

**Optimization**: Use ONNX backend (1.3-1.5x speedup) or OpenVINO (Intel hardware optimization).

## Integration Patterns

### Basic Usage:
```python
from keybert import KeyBERT

kw_model = KeyBERT()
keywords = kw_model.extract_keywords(
    "Your document text here...",
    keyphrase_ngram_range=(1, 3),
    top_n=10
)
```

### Custom Embedding Model:
```python
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# Multilingual model for CJK support
st_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
kw_model = KeyBERT(model=st_model)
```

### Chinese-Specific:
```python
# Use chinese_keybert fork for better Chinese support
from chinese_keybert import ChineseKeyBERT

kw_model = ChineseKeyBERT()
keywords = kw_model.extract_keywords("中文文本...")
```

## Use Case Fit

**Best For**:
- ✅ **Semantic keyword extraction** (meaning-based, not just frequency)
- ✅ **Multilingual content** (50-100+ languages including CJK)
- ✅ **Content tagging/classification** (finding topics, themes)
- ✅ **Document similarity** (embeddings enable clustering)
- ✅ **Low-resource languages** (multilingual BERT covers many languages)

**NOT Best For**:
- ❌ **Pure terminology extraction** (extracts keywords, not technical terms)
- ❌ **Speed-critical applications** (BERT inference is slow)
- ❌ **Resource-constrained environments** (large models, high memory)
- ❌ **Multi-word technical terms** (may split into characters for CJK)

## Terminology vs Keywords: Key Difference

**Example Document**: "Machine learning uses neural networks for classification tasks."

**KeyBERT Output** (semantic keywords):
- "machine learning" (semantically central)
- "neural networks" (semantically central)
- "classification" (important concept)

**Terminology Extraction Output** (technical terms):
- "machine learning"
- "neural networks"
- "classification tasks"

**Difference**: KeyBERT finds **semantically important words**. Terminology extraction finds **domain-specific technical terms**. Overlap exists, but goals differ.

Per [Wikipedia](https://en.wikipedia.org/wiki/Terminology_extraction) and [Sketch Engine](https://www.sketchengine.eu/guide/keywords-and-term-extraction/):
- **Terminology**: Domain-specific, low-ambiguity, multi-word expressions
- **Keywords**: Distinguish documents, may be general words with high semantic importance

## Maintenance and Community

- **Status**: ✅ Active (2023+ releases)
- **GitHub**: 3.5K+ stars, very active
- **Documentation**: Excellent (comprehensive guides, FAQ)
- **Community**: Large user base, active discussions

## Key Citations

1. **Multilingual BERT** (Google Research): 110K shared vocabulary, 102 languages, character-tokenization for CJK.
   - [GitHub Multilingual BERT Docs](https://github.com/google-research/bert/blob/master/multilingual.md)

2. **Sentence-Transformers Models**: Performance benchmarks on STS 2017 dataset.
   - [Pretrained Models Documentation](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)

3. **KeyBERT FAQ**: Guidance on model selection and use cases.
   - [KeyBERT FAQ](https://maartengr.github.io/KeyBERT/faq.html)

## Bottom Line

KeyBERT is the **strongest choice for semantic keyword extraction** across 50-100+ languages including CJK. Excellent multilingual support via BERT, but extracts **keywords** (semantic importance) not **terminology** (technical terms). For pure terminology extraction, pyate is better (if language is supported). For CJK semantic keywords, KeyBERT works out-of-box with multilingual models, though chinese_keybert fork provides better Chinese word segmentation.
