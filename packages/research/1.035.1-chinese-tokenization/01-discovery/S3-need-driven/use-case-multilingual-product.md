# Use Case: Multilingual SaaS Product

## Who Needs This

**Persona**: Product engineer at SaaS company expanding to China

**Context**: Building document analysis tool (summarization, classification, search) supporting English, Chinese, Japanese, Korean. Single codebase, unified API. Target: Enterprise customers with multilingual content.

**Scale**: 100K+ documents per customer, mixed languages

## Why They Need Tokenization

### Core Requirements
1. **Unified tokenization**: One system for all languages
2. **No language detection**: Should work on mixed-language text
3. **Maintainability**: One tokenizer to maintain, not 4+ separate tools
4. **Token efficiency**: Avoid 2-3x inflation for Chinese (cost impact)

### Business Impact
- Separate tokenizers per language → 4x maintenance cost
- Poor Chinese tokenization → Chinese customers see worse quality
- Token inflation → Higher API costs for Chinese users
- Example: Document has English headings + Chinese body content

## Key Constraints

| Constraint | Requirement | Why |
|------------|-------------|-----|
| Unified API | Single tokenizer | Codebase simplicity |
| Multilingual | EN + ZH + JA + KO | Customer requirements |
| Token efficiency | <1.5 tokens/Chinese char | Cost control |
| No language detection | Handles mixed text | Real-world documents |
| Scalability | Millions of docs | Enterprise scale |

## Recommended Solution

### Primary: SentencePiece (Unigram LM)

```python
import sentencepiece as spm

# Train unified multilingual tokenizer
spm.SentencePieceTrainer.train(
    input='multilingual_corpus.txt',  # EN + ZH + JA + KO
    model_prefix='unified_tokenizer',
    vocab_size=50000,  # Larger for multilingual
    character_coverage=0.9995,  # Critical for CJK
    split_by_whitespace=False,  # No language assumptions
    model_type='unigram'
)

# Use for all languages
sp = spm.SentencePieceProcessor(model_file='unified_tokenizer.model')

# English document
en_tokens = sp.encode('Natural language processing', out_type=str)

# Chinese document
zh_tokens = sp.encode('自然语言处理', out_type=str)

# Mixed document (real-world scenario)
mixed_tokens = sp.encode('Introduction to 自然语言处理 (NLP)', out_type=str)
```

**Why SentencePiece**:
- ✅ **Language-agnostic**: No spaces/language assumptions
- ✅ **Efficient for CJK**: 0.9-1.3 tokens per Chinese char (vs 2-3 for byte-BPE)
- ✅ **Unified codebase**: Single model for all languages
- ✅ **Proven**: Used in T5, mT5, XLNet (Google/Alibaba scale)

### Corpus Requirements

**Balanced multilingual corpus**:
```
English:  40% (1M documents)
Chinese:  30% (750K documents)
Japanese: 15% (375K documents)
Korean:   15% (375K documents)
```

Balance reflects user distribution. Adjust based on your customer base.

## Alternatives

### If Already Using HuggingFace
**Use: Qwen or mT5 tokenizer**
```python
from transformers import AutoTokenizer

# Qwen: Chinese-optimized multilingual
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-7B")

# mT5: Balanced multilingual (101 languages)
tokenizer = AutoTokenizer.from_pretrained("google/mt5-base")
```
- No training needed (pre-trained)
- Well-tested on multilingual text
- Larger vocab than custom SentencePiece

### If English-Primary with Some Chinese
**Use: Custom BPE (character-based for Chinese)**
```python
from tokenizers import Tokenizer, models, pre_tokenizers

# Custom BPE with Chinese character support
tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()  # English split
# Add Chinese characters to vocab explicitly
```

## Implementation Pattern

```python
import sentencepiece as spm

class UnifiedTokenizer:
    def __init__(self, model_path):
        self.sp = spm.SentencePieceProcessor(model_file=model_path)

    def tokenize(self, text):
        """Works for any language"""
        return self.sp.encode(text, out_type=str)

    def detokenize(self, tokens):
        """Reconstruct original text"""
        return self.sp.decode(tokens)

# Use everywhere
tokenizer = UnifiedTokenizer('unified_tokenizer.model')

# Process English
en_doc = "The quick brown fox..."
en_tokens = tokenizer.tokenize(en_doc)

# Process Chinese
zh_doc = "自然语言处理技术..."
zh_tokens = tokenizer.tokenize(zh_doc)

# Process mixed (no language detection needed)
mixed_doc = "Introduction: 自然语言处理 (Natural Language Processing)"
mixed_tokens = tokenizer.tokenize(mixed_doc)
```

## Training Configuration

```python
import sentencepiece as spm

spm.SentencePieceTrainer.train(
    input='multilingual_corpus.txt',
    model_prefix='unified_tokenizer',

    # Vocabulary
    vocab_size=50000,  # Larger for multilingual coverage
    character_coverage=0.9995,  # CRITICAL for Chinese/Japanese/Korean

    # Multilingual settings
    split_by_whitespace=False,  # Handle CJK
    byte_fallback=True,  # Handle rare chars gracefully

    # Model type
    model_type='unigram',  # Best for multilingual

    # Special tokens
    user_defined_symbols=['[CLS]', '[SEP]', '[MASK]'],
    pad_id=0,
    unk_id=1,
    bos_id=2,
    eos_id=3
)
```

## Validation Checklist

- [ ] Test token efficiency: <1.5 tokens per Chinese char
- [ ] Test mixed-language documents (English headers + Chinese body)
- [ ] Validate coverage: All characters tokenizable (no UNK)
- [ ] Load test: Can handle millions of documents
- [ ] Compare to separate tokenizers (should match quality)
- [ ] Monitor token counts across languages (detect imbalance)

## Common Pitfalls

❌ **Using English tokenizer on Chinese**: Catastrophic failure
```python
# WRONG - English BPE on Chinese
from tokenizers import Tokenizer
tokenizer = Tokenizer.from_file("english_bpe.json")
tokenizer.encode("中文测试")  # Garbage output
```

❌ **Not setting character_coverage=0.9995**: Poor CJK support
```python
# WRONG - Default coverage
spm.train(vocab_size=50000)  # Bad for Chinese

# RIGHT
spm.train(vocab_size=50000, character_coverage=0.9995)
```

✅ **Training on balanced multilingual corpus**
```python
# RIGHT - Balanced corpus
spm.train(
    input='balanced_multilingual.txt',  # EN 40%, ZH 30%, JA 15%, KO 15%
    character_coverage=0.9995
)
```

## Summary

**For multilingual products, use SentencePiece** because:
- Single tokenizer for all languages (maintainability)
- Efficient for CJK (no token inflation)
- Language-agnostic (no detection needed)
- Battle-tested (Google T5, Alibaba Qwen)

**Alternative**: Use Qwen or mT5 tokenizer if already in HuggingFace ecosystem (no training required).
