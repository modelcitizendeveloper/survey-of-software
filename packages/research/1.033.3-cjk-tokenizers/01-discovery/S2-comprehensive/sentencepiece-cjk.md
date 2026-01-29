# SentencePiece CJK Configuration

## Technical Overview

SentencePiece is a **language-independent tokenizer** that trains subword models directly from raw text without pre-tokenization.

**Key innovation for CJK:** No dependency on word boundaries.

## CJK-Specific Configuration

### Critical Parameters

```python
import sentencepiece as spm

spm.SentencePieceTrainer.train(
    input='corpus.txt',
    model_prefix='cjk_tokenizer',
    vocab_size=32000,
    character_coverage=0.9995,  # ← Critical for CJK
    split_by_whitespace=False,  # ← Critical for CJK
    model_type='unigram',       # or 'bpe'
    normalization_rule_name='nmt_nfkc'
)
```

### Parameter Explanation

**`character_coverage=0.9995`**
- For CJK: Use 0.9995 (99.95% coverage)
- For English: Use 1.0
- Why: CJK has large character inventories (20,000+ common characters)
- Rare characters fall back to byte encoding
- Balances vocabulary size vs coverage

**`split_by_whitespace=False`**
- Allows pieces to cross word boundaries
- Essential for Chinese/Japanese (no spaces between words)
- Enables optimal subword segmentation

**`model_type='unigram'` vs `'bpe'`**
- **Unigram:** Default, often better for CJK (probabilistic segmentation)
- **BPE:** Deterministic merging, works well too
- Both support CJK, unigram slight edge

## Training Strategy

### Corpus Requirements
- **Minimum:** 1M sentences for basic quality
- **Recommended:** 10M+ sentences for production
- **Language balance:** Match your target distribution
  - 50% Chinese → tokenizer optimizes for Chinese
  - 50% English → balanced bilingual tokenizer

### Vocabulary Size Trade-offs

| Vocab Size | CJK Coverage | Token Efficiency | Model Size |
|------------|--------------|------------------|------------|
| 8,000 | Poor | Low | Small |
| 16,000 | Acceptable | Medium | Medium |
| 32,000 | Good | High | Standard |
| 64,000 | Excellent | Very High | Large |

**For CJK-primary:** 32,000-64,000 recommended
**For multilingual:** 32,000 is standard (BERT, T5)

## Performance Characteristics

### Speed
- **Training:** Slow (hours for 10M sentences)
- **Inference:** Moderate (slower than tiktoken, faster than naive segmentation)
- **Not optimized for speed** - prioritizes quality

### Token Efficiency
**Superior for CJK when trained properly:**
- ~1.0-1.2 tokens per character (vs 2-3 for tiktoken)
- Achieves this by learning common character sequences
- Example: 你好 (hello) might be 1 token instead of 2

### Memory
- Model file: ~1-10MB depending on vocab size
- Runtime memory: Moderate (need to load model)

## Architectural Advantages for CJK

### 1. End-to-End Training
No pre-tokenization → learns optimal boundaries from data
- Chinese: Learns which characters commonly group
- Japanese: Learns kanji/hiragana/katakana patterns naturally

### 2. Probabilistic Segmentation (Unigram)
Multiple valid segmentations with probabilities
- Handles ambiguous cases better
- More robust to rare constructions

### 3. Reversibility
Perfect reconstruction of original text including whitespace
- Important for Chinese (space can be semantically meaningful)

### 4. Unicode Normalization
Built-in handling of Unicode variants (simplified/traditional Chinese)

## Real-World Adoption

**Models using SentencePiece for CJK:**
- **T5** (Google): Multilingual, 32k vocab
- **ALBERT**: Chinese/English, strong CJK performance
- **XLNet**: Chinese tasks
- **mT5**: 101 languages including CJK

**Why they chose SentencePiece:** Explicit design for languages without word boundaries.

## Limitations

1. **Training required** - Can't use pre-built (unlike tiktoken's cl100k_base)
2. **Slower inference** - More complex segmentation logic
3. **Corpus dependency** - Quality depends on training data quality
4. **Configuration complexity** - Many parameters to tune

## Best Practices for CJK

1. **Mix CJK and English in training** if building multilingual model
2. **Use character_coverage=0.9995** for Chinese/Japanese
3. **Increase vocab size** if CJK-primary (32k → 64k)
4. **Test on your specific domain** - vocabulary is corpus-dependent
5. **Monitor rare character handling** - ensure fallback works

## Verdict

**Best choice for CJK-optimized tokenization** when you control the training process. Explicit parameters for CJK, proven track record, but requires investment in training infrastructure and corpus curation.
