# Subword Tokenizers

Data-driven tokenization that learns boundaries from corpora, not dictionaries.

## SentencePiece (Google)

- **Maturity**: 10.4K stars, production tool from Google
- **Speed**: Very fast (C++ implementation, parallelizable)
- **Accuracy**: Task-dependent (trained on your corpus)
- **Approach**: Unigram LM or BPE, learns subword units
- **Ease**: Requires corpus training, parameter tuning needed
- **Maintenance**: Actively maintained by Google, 2025 updates
- **CJK Support**: Explicit `character_coverage=0.9995` parameter for Chinese
- **Best for**: Multilingual models, custom domain vocabularies, when building transformers

**Key advantage**: Language-agnostic, no spaces assumed (ideal for Chinese).

**Production usage**: T5, mT5, XLNet, Qwen, Gemini, many Google/Alibaba models

---

## tiktoken (OpenAI)

- **Maturity**: 12.2K stars, production tool from OpenAI
- **Speed**: Extremely fast (Rust core)
- **Accuracy**: Not applicable (implements existing tokenizers)
- **Approach**: Implements BPE tokenizers (cl100k_base for GPT-3.5/4)
- **Ease**: Simple (pre-trained models), no training needed
- **Maintenance**: Actively maintained by OpenAI
- **CJK Issue**: cl100k_base uses byte-level BPE → 2-3x token inflation for Chinese
- **Best for**: Using OpenAI models, when you need cl100k_base compatibility

**Critical limitation**: Byte-level BPE inefficient for Chinese (each char = 2-3 tokens vs 1 for English).

---

## tokenizers (HuggingFace)

- **Maturity**: Part of transformers library (135K stars)
- **Speed**: Very fast (Rust implementation)
- **Accuracy**: Model-dependent (uses pre-trained tokenizers)
- **Approach**: BPE, WordPiece, Unigram, or character-level (depends on model)
- **Ease**: Simple if using pre-trained models, complex if training custom
- **Maintenance**: Actively maintained by HuggingFace
- **Best for**: Using HuggingFace models (BERT, Qwen, ChatGLM), transformer ecosystem

**Ecosystem advantage**: Seamless integration with 200K+ pre-trained models.

---

## Quick Comparison

| Tokenizer | Speed | Training Required | CJK Efficiency | Use Case |
|-----------|-------|-------------------|----------------|----------|
| **SentencePiece** | ⭐⭐⭐⭐ Fast | ✅ Yes (corpus) | ⭐⭐⭐⭐⭐ Excellent | Custom vocabularies |
| **tiktoken** | ⭐⭐⭐⭐⭐ Fastest | ❌ No | ⭐⭐ Poor (byte-BPE) | OpenAI compatibility |
| **tokenizers** | ⭐⭐⭐⭐ Fast | Optional | ⭐⭐⭐⭐ Model-dependent | HuggingFace ecosystem |

## Token Efficiency for Chinese

Critical consideration: How many tokens per Chinese character?

- **Character-level** (BERT-base-chinese): 1.0 tokens/char
- **SentencePiece** (Qwen, trained on Chinese): 1.0-1.3 tokens/char
- **Byte-level BPE** (GPT-4 cl100k_base): 2.0-3.0 tokens/char ⚠️

**Cost impact**: Using byte-level BPE for Chinese-heavy workloads = 2-3x higher API costs.

## Selection Heuristics

**Building multilingual model?** → SentencePiece (language-agnostic)

**Using OpenAI APIs?** → tiktoken (but accept 2-3x cost for Chinese)

**Using HuggingFace models?** → tokenizers (pre-trained available)

**Chinese-optimized needed?** → SentencePiece or Qwen tokenizer (1.0-1.3 tokens/char)

**Avoid byte-level BPE** for Chinese-primary applications (inefficient).
