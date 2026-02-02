# pyate: Deep Technical Analysis

## Algorithm Implementation

### Available Algorithms (5 total):

1. **Basic**: Frequency-based with POS filtering
2. **Combo Basic**: Extension of Basic (highest precision per Astrakhantsev 2016)
3. **C-Value**: Multi-word term recognition (Frantzi et al. 1998)
4. **Weirdness**: Contrasts technical vs general corpus
5. **Term Extractor**: Hybrid approach

### Combo Basic (Recommended)

**Formula**: Weighted average of:
- Number of times term `t` contains another candidate
- Number of times another term contains `t`
- Length of `t` in characters × log(frequency of `t`)

**Performance**: Per [Astrakhantsev 2016](https://link.springer.com/article/10.1007/s13740-017-0082-4), `combo_basic` is **most precise** of the five algorithms implemented in pyate. Basic and C-Value are "not too far behind."

**Comparison to State-of-Art**: PU-ATR and KeyConceptRel have higher precision than combo_basic but:
- Not implemented in pyate
- PU-ATR takes significantly more time (uses machine learning)

## Dependencies

**Required**:
- spaCy (POS tagging)
- numpy, pandas (data processing)
- pyahocorasick (pattern matching)

**Language Models**: Requires spaCy language model (e.g., `en_core_web_sm` for English)

## Multilingual Support

### Current Status:
- **Supported** (as of v0.4.2): English, Italian
- **Requires**: Language-specific spaCy model + general domain corpus

### Language Switching:
```python
from pyate import combo_basic
combo_basic.set_language("zh", "zh_core_web_sm")  # Chinese example
```

### CJK Language Support:

**spaCy Models Available**:
- ✓ Chinese (`zh_core_web_sm`, `zh_core_web_md`, `zh_core_web_lg`)
- ✓ Japanese (`ja_core_news_sm`, `ja_core_news_md`, `ja_core_news_lg`)
- ✓ Korean (rule-based tokenizer available)

**pyate Status for CJK**:
❌ **No native CJK support** - Per [GitHub Issue #13](https://github.com/kevinlu1248/pyate/issues/13), pyate lacks **general domain corpora** for Chinese, Japanese, Korean. While spaCy can tokenize/POS-tag CJK text, pyate's algorithms (especially Weirdness and Term Extractor) require reference corpora that don't exist yet.

**Implication**: pyate can technically run on CJK text if you provide your own general corpus, but no out-of-box CJK support.

## Performance Characteristics

### Strengths:
- **High precision** for terminology (vs keywords): Targets multi-word technical terms
- **Multiple algorithms**: Can choose based on use case (C-Value for nested terms, Combo Basic for precision)
- **Domain-specific**: Weirdness algorithm contrasts technical vs general language
- **Benchmark-proven**: Astrakhantsev 2016 validates performance

### Weaknesses:
- **Requires corpora**: Weirdness and Term Extractor need reference corpora (not available for all languages)
- **spaCy dependency**: Heavier stack, requires language models (100MB-500MB)
- **Limited CJK**: No pre-built support for Chinese, Japanese, Korean

### Speed:
- Fast (statistical algorithms, not ML inference)
- Slower than YAKE/RAKE (due to spaCy POS tagging)
- Much faster than KeyBERT (no transformer inference)

## Integration Patterns

### spaCy Pipeline Integration:
```python
import spacy
from pyate import combo_basic

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("combo_basic")
doc = nlp("Your technical document here...")
terms = doc._.terms  # Extracted terminology
```

### Standalone Usage:
```python
from pyate import combo_basic

text = "Natural language processing and machine learning..."
terms = combo_basic(text).sort_values(ascending=False).head(10)
```

## Use Case Fit

**Best For**:
- ✅ Technical terminology extraction (not general keywords)
- ✅ Translation memory creation
- ✅ Glossary generation for technical writing
- ✅ Domain-specific NLP (medical, legal, engineering)
- ✅ Multi-word term recognition (e.g., "natural language processing")

**NOT Best For**:
- ❌ CJK languages (no pre-built corpora)
- ❌ General keyword extraction (use YAKE or KeyBERT)
- ❌ Semantic understanding (use KeyBERT)
- ❌ Low-resource languages (requires spaCy model + corpus)

## Maintenance and Community

- **Status**: ✅ Active (spaCy v3 support, releases in 2023)
- **GitHub**: 320+ stars, regular updates
- **Documentation**: Good (docs site + demo app)
- **Community**: Listed in spaCy Universe (official ecosystem)

## Key Citations

1. **Astrakhantsev, N. (2016)**. "ATR4S: toolkit with state-of-the-art automatic terms recognition methods in Scala." Language Resources and Evaluation, 52(3), 853-872.
   - Benchmark showing combo_basic has highest precision

2. **Frantzi, K.T., Ananiadou, S., Tsujii, J. (1998)**. "The C-value/NC-value Method of Automatic Recognition for Multi-word Terms."
   - Original C-Value algorithm for multi-word term extraction

## Bottom Line

pyate is the **strongest choice for pure terminology extraction** in supported languages (English, Italian). Implements proven algorithms (Combo Basic, C-Value) with benchmark-validated precision. **CJK support is blocked** by lack of general domain corpora, making it unsuitable for Chinese, Japanese, Korean unless you provide your own reference corpus.
