# S1 Recommendation: Quick Library Selection

## Three Tokenization Paradigms

### Traditional Word Segmenters
**Philosophy**: "Split Chinese text into linguistic words"
**Libraries**: Jieba, PKUSEG, LAC, LTP
**Best when**: Need word-level tokens, traditional NLP pipeline

### Subword Tokenizers
**Philosophy**: "Learn data-driven boundaries, no linguistic assumptions"
**Libraries**: SentencePiece, tiktoken, HuggingFace tokenizers
**Best when**: Building transformers, multilingual systems

### Transformer Character-Level
**Philosophy**: "Let transformers learn composition from characters"
**Libraries**: BERT-base-chinese, Qwen, ChatGLM, mT5
**Best when**: Using pre-trained LLMs, Chinese-only transformers

---

## Comparison Matrix

| Library | Type | Speed | Accuracy | Ease | Token Efficiency |
|---------|------|-------|----------|------|------------------|
| **Jieba** | Traditional | ⭐⭐⭐⭐⭐ 400 KB/s | ⭐⭐⭐ F1 ~85% | ⭐⭐⭐⭐⭐ Simple | N/A (word-level) |
| **PKUSEG** | Traditional | ⭐⭐⭐ 130 KB/s | ⭐⭐⭐⭐⭐ F1 ~96% | ⭐⭐⭐⭐ Medium | N/A (word-level) |
| **LAC** | Traditional | ⭐⭐⭐⭐⭐ 800 QPS | ⭐⭐⭐⭐ F1 ~91% | ⭐⭐⭐⭐ Medium | N/A (word-level) |
| **SentencePiece** | Subword | ⭐⭐⭐⭐ Fast | Task-dependent | ⭐⭐⭐ Complex | ⭐⭐⭐⭐⭐ 1.0-1.3 |
| **BERT-chinese** | Char-level | ⭐⭐ Slow | ⭐⭐⭐⭐⭐ F1 ~97% | ⭐⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ 1.0 |
| **Qwen** | Subword | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ SOTA | ⭐⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ 1.3 |
| **tiktoken (GPT-4)** | Byte-BPE | ⭐⭐⭐⭐⭐ Fastest | N/A | ⭐⭐⭐⭐⭐ Simple | ⭐⭐ 2.0-3.0 ⚠️ |

---

## Decision Tree

```
Need Chinese tokenization?

├─ Using pre-trained LLMs?
│  ├─ Chinese-only → BERT-base-chinese
│  ├─ Chinese-primary → Qwen
│  ├─ Bilingual CN+EN → ChatGLM or Qwen
│  └─ Multilingual (10+) → mT5
│
├─ Building transformers from scratch?
│  ├─ Multilingual → SentencePiece (train on corpus)
│  ├─ Chinese-only → Character-level or SentencePiece
│  └─ Have domain corpus → SentencePiece (custom vocab)
│
└─ Traditional NLP (non-transformer)?
   ├─ Need speed → Jieba (400 KB/s) or LAC (800 QPS)
   ├─ Need accuracy → PKUSEG (F1 ~96%)
   ├─ Production scale → LAC (Baidu-backed)
   └─ Prototyping → Jieba (simplest)
```

---

## By Primary Constraint

### Speed Critical (>400 KB/s needed)
1. **LAC** - 800 QPS, production-optimized
2. **Jieba** - 400 KB/s, fastest traditional
3. **tiktoken** - Fastest (but 2-3x token inflation for Chinese)

### Accuracy Critical (>95% F1 needed)
1. **PKUSEG** - F1 ~96%, domain models available
2. **BERT-base-chinese** - F1 ~97% on downstream tasks
3. **Qwen** - State-of-the-art (2024-2025)

### Ease Critical (minimal setup)
1. **Jieba** - 2-line quickstart, no training
2. **BERT-base-chinese** - Pre-trained, ready to use
3. **tiktoken** - Pre-trained (but inefficient for Chinese)

### Token Efficiency Critical (<1.5 tokens/char)
1. **BERT-base-chinese** - 1.0 tokens/char
2. **SentencePiece (Chinese-trained)** - 1.0-1.3 tokens/char
3. **Qwen** - 1.3 tokens/char
4. **Avoid**: tiktoken/GPT-4 (2.0-3.0 tokens/char)

### Multilingual Required
1. **SentencePiece** - Language-agnostic, train on mixed corpus
2. **mT5** - 101 languages pre-trained
3. **Qwen** - Chinese-primary, good English support

---

## Top 3 by Use Case

### Prototyping / Quick Start
1. **Jieba** - Fastest to start, good enough for most tasks
2. **BERT-base-chinese** - If using transformers
3. **tiktoken** - If using OpenAI APIs (accept cost)

### Production (Chinese-only)
1. **LAC** - Best speed + accuracy balance, Baidu-backed
2. **Qwen** - If using LLMs
3. **PKUSEG** - If accuracy > speed

### Research / Academic
1. **PKUSEG** - Highest traditional accuracy, reproducible
2. **BERT-base-chinese** - Standard for transformers
3. **SentencePiece** - Standard for multilingual

### Multilingual SaaS
1. **SentencePiece** - Train unified tokenizer
2. **mT5** - Pre-trained for 101 languages
3. **Qwen** - If Chinese-primary with some English

---

## Critical Warnings

### ⚠️ Byte-Level BPE Inefficiency
**Problem**: tiktoken (GPT-4 cl100k_base) uses 2-3 tokens per Chinese char
**Impact**: 2-3x higher API costs, slower inference
**Solution**: Use Qwen, ChatGLM, or SentencePiece for Chinese-heavy workloads

### ⚠️ Single Maintainer Risk
**Problem**: Jieba has single maintainer (fxsjy), maintenance mode since 2020
**Impact**: Bug fixes slow, no new features
**Mitigation**: Corporate alternatives (LAC), or plan migration path

### ⚠️ Domain Model Selection
**Problem**: PKUSEG requires choosing domain model (news/web/medicine/tourism)
**Impact**: Wrong model = lower accuracy
**Solution**: Test on your data, use 'mixed' model if unsure

---

## Quick Recommendation by Role

### Startup Engineer
→ **Jieba** (fast iteration, good enough)

### ML Engineer
→ **SentencePiece** or **Qwen** (building models)

### Data Scientist
→ **PKUSEG** or **BERT-base-chinese** (accuracy matters)

### Product Manager
→ **LAC** (production stability)

### Researcher
→ **PKUSEG** or **BERT-base-chinese** (reproducibility)

---

## Next Steps

1. **Pick from S1** based on constraints above
2. **Read S2** for technical deep-dive on your top choice
3. **Check S3** to validate against your specific use case
4. **Review S4** for long-term strategic considerations

## One-Line Guidance

**Default (2025)**: Jieba for traditional NLP, SentencePiece/Qwen for transformers, avoid tiktoken for Chinese-heavy workloads.
