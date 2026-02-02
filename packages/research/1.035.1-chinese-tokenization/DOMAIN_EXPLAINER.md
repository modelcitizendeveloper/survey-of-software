# Chinese Tokenization for NLP: Domain Explainer

## What is Chinese Tokenization?

**Chinese tokenization** is the process of breaking Chinese text into meaningful units (tokens) for natural language processing. Unlike English, Chinese has no spaces between words, making tokenization a non-trivial preprocessing step.

### The Core Problem

**English**: "I love Beijing" → Spaces naturally indicate word boundaries
**Chinese**: "我爱北京" → No spaces; algorithms must determine boundaries

This creates a fundamental challenge: **Where do words begin and end?**

## Why Tokenization Matters

Tokenization is the **foundation** of all NLP tasks. Wrong tokenization cascades through:
- Machine translation (wrong alignments)
- Named entity recognition (broken entities)
- Text classification (lost semantic units)
- Search (query-document mismatches)

Research shows tokenization choice can affect machine translation by 7-8 BLEU points and impact other tasks significantly.

## Core Concepts

### 1. Granularity Levels

**Character-level**: Each Chinese character is a token
```
"我爱北京" → ["我", "爱", "北", "京"]
```
- Pros: No segmentation errors, zero OOV
- Cons: Longer sequences, lost semantic units

**Word-level**: Segment into linguistic words first
```
"我爱北京" → ["我", "爱", "北京"]
```
- Pros: Shorter sequences, semantic preservation
- Cons: Segmentation errors, OOV problem, requires dictionary

**Subword-level**: Data-driven token boundaries
```
"我爱北京" → ["我", "爱", "北京"] (learned from corpus)
```
- Pros: Balance between character and word, handles OOV
- Cons: Requires training, may not match linguistic intuition

### 2. Key Algorithms

**BPE (Byte-Pair Encoding)**:
- Merges frequent character pairs iteratively
- Used in GPT models
- **Problem for Chinese**: Byte-level BPE inflates Chinese text 2-3x

**WordPiece**:
- Similar to BPE but uses likelihood maximization
- Used in BERT
- BERT-base-chinese uses character-level (no subword merging)

**SentencePiece (Unigram)**:
- Language-independent, no pre-tokenization needed
- **Gold standard for Chinese**: Explicit CJK support
- Used in T5, XLNet, mT5

### 3. The Segmentation Ambiguity Problem

Chinese word boundaries are inherently ambiguous:

**Example**: "结婚的和尚未结婚的"

**Segmentation A**: 结婚 / 的 / 和尚 / 未 / 结婚 / 的
- Translation: "The married monk has not married"

**Segmentation B**: 结婚 / 的 / 和 / 尚未 / 结婚 / 的
- Translation: "Those who are married and those not yet married"

Same text, completely different meanings based on segmentation.

## Practical Approaches

### Modern Neural Approach (Dominant in 2025)

**Character-level with transformers** (BERT approach):
- Feed raw characters into model
- Let attention mechanism learn word-level composition
- **Result**: No explicit segmentation, no error propagation

**Why it works**:
- Multi-head attention learns character combinations
- Deep layers build hierarchical representations
- Bidirectional context resolves ambiguities

**Example**: bert-base-chinese
- 21,128 character vocabulary
- State-of-the-art on many Chinese NLP tasks
- Character-level tokenization but word-level understanding

### Traditional Segmentation Tools

**Jieba** (结巴):
- Most popular Python library (34.7K stars)
- Dictionary + HMM hybrid
- Fast (400 KB/s) but lower accuracy (F1 ~85%)
- Best for: Prototyping, keyword extraction

**PKUSEG** (北大分词):
- Neural network (BiLSTM-CRF)
- Domain-specific models (news, web, medicine)
- Highest accuracy (F1 ~96%) among traditional tools
- Best for: Domain-specific production systems

**LAC** (Baidu):
- Neural network (BiGRU-CRF)
- Best speed + accuracy combo (800 QPS, F1 > 0.91)
- Joint segmentation + POS + NER
- Best for: Production Chinese-only systems

**spaCy**:
- Multilingual NLP framework
- Uses pkuseg backend for Chinese (F1 ~94.6%)
- Best for: Multilingual pipelines

**HuggingFace Tokenizers**:
- Access to pre-trained transformer tokenizers
- Qwen, ChatGLM: Chinese-optimized
- Best for: Building transformer models

## Trade-Offs

### Accuracy vs Speed vs Simplicity Triangle

You can pick two:

| Tool/Approach | Accuracy | Speed | Simplicity |
|--------------|----------|-------|------------|
| Jieba | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| PKUSEG | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| LAC | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| BERT | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

### Token Efficiency Comparison

**Example**: "我喜欢学习中文" (I like learning Chinese)

| Method | Tokens | Efficiency |
|--------|--------|-----------|
| Character-level | 7 | 100% |
| SentencePiece (Chinese-optimized) | 4-5 | ~140-175% |
| Byte-level BPE (GPT-4) | 14-18 | ~40-50% |

**Key insight**: Byte-level BPE (used in GPT-4) inflates Chinese text significantly, causing 2-3x cost in API usage.

## Impact on Downstream Tasks

### Machine Translation
- **Best**: Subword (BPE/SentencePiece)
- **Impact**: 7-8 BLEU point difference between good and poor tokenization
- **Reason**: Word alignment and OOV handling critical

### Named Entity Recognition
- **Best**: Character-level with BIO tagging
- **Reason**: Avoids segmentation errors that break entity boundaries
- **Alternative**: Lattice LSTM (char + word) for highest accuracy

### Text Classification
- **Best**: Pre-trained models (BERT) - tokenization already chosen
- **Impact**: Less sensitive than MT/NER with large training data
- **Consideration**: Sequence length limits for long documents

### Information Retrieval
- **Best**: Search-optimized segmentation (Jieba search mode) or character n-grams
- **Reason**: High recall (match substrings) more important than precision
- **Pitfall**: Query-document tokenization must match

### Language Modeling
- **Best**: SentencePiece or character-level
- **Metric trap**: Cannot compare perplexity across different tokenizations without normalization
- **Solution**: Use bits-per-character (BPC) instead

## Common Pitfalls

1. **Using English tokenizers on Chinese**: Catastrophic failure
2. **Byte-level BPE for Chinese-heavy workloads**: 2-3x token inflation
3. **Not setting character_coverage=0.9995**: Poor rare character handling
4. **Comparing perplexity across tokenizations**: Not directly comparable
5. **Mixing pre-training and fine-tuning tokenizations**: Vocabulary mismatch
6. **Ignoring OOV rate**: Word-level models fail on out-of-domain text
7. **Over-relying on dictionaries**: Fails on neologisms and slang
8. **Not handling preprocessing**: Crashes on emoji, URLs, mixed text

## Best Practices (2025)

### Default Recommendations

**For most use cases**: bert-base-chinese (character-level)
- Battle-tested, widely supported, good accuracy
- No segmentation errors, zero OOV

**For production accuracy**: LAC or PKUSEG
- Highest accuracy among traditional tools
- Domain models available (PKUSEG)
- Fast enough for production (LAC: 800 QPS)

**For multilingual**: SentencePiece Unigram
- Language-independent, works across all languages
- Proven in T5, XLNet, mT5
- Train on balanced corpus (50% Chinese + 50% English for bilingual)

**For building from scratch**: SentencePiece with proper configuration
```python
import sentencepiece as spm

spm.SentencePieceTrainer.train(
    input='chinese_corpus.txt',
    vocab_size=32000,
    character_coverage=0.9995,  # Critical for Chinese
    split_by_whitespace=False,  # Critical for Chinese
    model_type='unigram'
)
```

### Quick Decision Tree

```
Need to tokenize Chinese?
├─ Prototyping? → Use Jieba
├─ Production (accuracy critical)?
│  ├─ Chinese-only? → Use LAC or PKUSEG
│  └─ Multilingual? → Use SentencePiece or Qwen
├─ Building transformer model?
│  ├─ Chinese-only? → Use bert-base-chinese
│  └─ Multilingual? → Use mT5 or custom SentencePiece
└─ Search/IR? → Use Jieba search mode or character n-grams
```

## Advanced Topics

### Hybrid Approaches

**Lattice LSTM**: Uses character sequence + all dictionary word matches
- Best accuracy but complex architecture
- Handles ambiguity by considering multiple segmentations

**Multi-task Learning**: Train segmentation + POS + NER jointly
- Shared representations improve all tasks
- One model, multiple outputs

**Sub-character Tokenization**: Decompose characters into radicals/strokes
- 25% shorter sequences than character-level
- Captures semantic relationships via radicals
- Emerging research area (2023+)

### Whole-Word Masking for BERT

**Standard masking**: Random characters
```
Original: 我爱北京天安门
Masked:   我爱[MASK]京天安门
```

**Whole-word masking**: Entire words
```
Segmented: 我 / 爱 / 北京 / 天安门
Masked:    我爱[MASK][MASK]天安门
```

**Why better**: Forces model to learn word-level semantics, not just character prediction

**Popular models**: Chinese-BERT-wwm, Chinese-RoBERTa-wwm, MacBERT

## Future Trends (2025-2026)

1. **Character-level is winning**: Transformers eliminate need for explicit segmentation
2. **Subword is standard for multilingual**: SentencePiece dominates multilingual models
3. **Sub-character emerging**: Radical/stroke-based tokenization showing promise
4. **Task-adaptive tokenization**: Future models may learn tokenization jointly with task
5. **Mega tokenization**: Research showing benefits of very large tokens

## Key Metrics

**Segmentation Accuracy**: F1 score on benchmark datasets (PKU, MSR, CTB)
- Jieba: 81-89%
- PKUSEG: ~96%
- LAC: ~91%
- BERT: ~96-97%

**Speed**: Characters processed per second
- Jieba: 400 KB/s
- PKUSEG: 130 KB/s
- LAC: 800 QPS (queries per second)
- BERT: ~20 KB/s (very slow)

**Token Efficiency**: Tokens per character
- Character-level: 1.0
- Word-level: 0.3-0.5
- SentencePiece (Chinese-optimized): ~0.7-1.0
- Byte-level BPE (GPT-4): 2.0-3.0 (inefficient)

## Resources

### Essential Reading
- [BERT for Chinese](https://github.com/google-research/bert) - Character-level approach
- [SentencePiece](https://github.com/google/sentencepiece) - Language-independent tokenization
- [Chinese Word Segmentation Research](https://github.com/fxsjy/jieba) - Most popular tool

### Benchmarks
- **CLUE** (Chinese Language Understanding Evaluation): Standard benchmark suite
- **SIGHAN Bakeoff**: Traditional word segmentation benchmarks (PKU, MSR, CTB)

### Pre-trained Models
- **bert-base-chinese**: Character-level, general-purpose
- **Qwen**: Chinese-optimized, efficient tokenization
- **ChatGLM**: Bilingual (Chinese-English)

## Terminology

**CWS**: Chinese Word Segmentation - traditional task of finding word boundaries
**OOV**: Out-of-vocabulary - words not in the tokenizer's vocabulary
**BIO tagging**: Begin-Inside-Outside labels for sequence labeling (used in NER)
**BMES tagging**: Begin-Middle-End-Single labels for segmentation
**Perplexity**: Language model metric (lower is better, but not comparable across tokenizations)
**BPC**: Bits-per-character - normalized perplexity metric

## Summary

Chinese tokenization is a critical preprocessing step with cascading effects through all NLP tasks. Modern approaches (2025) favor:

1. **Character-level with transformers** for most tasks (eliminates segmentation errors)
2. **SentencePiece** for custom/multilingual models (language-independent, proven)
3. **Domain-specific segmenters** (PKUSEG, LAC) when accuracy is critical

The field has shifted from viewing tokenization as a standalone problem to integrating it into end-to-end neural models, but understanding the trade-offs remains essential for building robust Chinese NLP systems.

## Sources

This domain explainer synthesizes research from:
- Academic papers (TACL, ACL, EMNLP)
- Production systems (Baidu LAC, Google BERT)
- Industry benchmarks (CLUE, SIGHAN)
- Recent developments (2023-2025)

For detailed citations, see individual discovery documents in the S1-S4 directories.
