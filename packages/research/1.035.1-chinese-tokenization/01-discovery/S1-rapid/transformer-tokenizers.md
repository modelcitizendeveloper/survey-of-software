# Transformer Model Tokenizers

Pre-trained tokenizers bundled with transformer models.

## BERT-base-chinese

- **Maturity**: Google's official Chinese BERT, widely adopted
- **Vocab**: 21,128 (character-level)
- **Approach**: Character-level (each Chinese character = 1 token)
- **Accuracy**: F1 ~96-97% on downstream tasks after fine-tuning
- **Ease**: Pre-trained, ready to use, no training needed
- **Maintenance**: Google's official release (2018), stable but no longer updated
- **Token efficiency**: 1.0 tokens per Chinese char (optimal)
- **Best for**: Chinese-only transformer projects, research reproducibility

**Key advantage**: Sidesteps segmentation entirely - transformers learn composition from characters.

---

## Qwen (Alibaba)

- **Maturity**: Leading Chinese LLM, actively developed
- **Vocab**: ~150K (Chinese-optimized subword)
- **Approach**: SentencePiece-based, trained on Chinese-heavy corpus
- **Accuracy**: State-of-the-art on Chinese NLP benchmarks (2024-2025)
- **Ease**: Pre-trained, HuggingFace integration
- **Maintenance**: Actively maintained by Alibaba, frequent updates
- **Token efficiency**: ~1.3 tokens per Chinese char (better than GPT-4)
- **Best for**: Chinese-primary multilingual applications, production LLM deployment

**Production usage**: Alibaba Cloud, many Chinese enterprises.

---

## ChatGLM (Tsinghua)

- **Maturity**: 8.7K stars, bilingual (Chinese + English)
- **Vocab**: Custom, optimized for Chinese-English balance
- **Approach**: Custom tokenizer, bilingual training
- **Accuracy**: Strong on Chinese benchmarks, competitive with Qwen
- **Ease**: Pre-trained, HuggingFace integration
- **Maintenance**: Tsinghua KEG Lab, active development
- **Token efficiency**: ~1.4 tokens per Chinese char
- **Best for**: Bilingual Chinese-English applications, academic research

---

## mT5 (Google)

- **Maturity**: Multilingual T5, 101 languages including Chinese
- **Vocab**: 250K (large to cover many languages)
- **Approach**: SentencePiece Unigram, balanced multilingual corpus
- **Accuracy**: Good across languages, not Chinese-specialized
- **Ease**: Pre-trained, multiple sizes (small/base/large/xl/xxl)
- **Maintenance**: Google Research, periodic updates
- **Token efficiency**: ~1.5-2.0 tokens per Chinese char (less efficient than Qwen)
- **Best for**: True multilingual (20+ languages), when Chinese is one of many

---

## Quick Comparison

| Model | Vocab Size | Token Efficiency (CN) | Languages | Specialization |
|-------|------------|----------------------|-----------|----------------|
| **BERT-base-chinese** | 21K | ⭐⭐⭐⭐⭐ 1.0 | Chinese-only | Character-level |
| **Qwen** | 150K | ⭐⭐⭐⭐⭐ 1.3 | CN-primary, EN | Chinese-optimized |
| **ChatGLM** | Custom | ⭐⭐⭐⭐ 1.4 | CN + EN | Bilingual balanced |
| **mT5** | 250K | ⭐⭐⭐ 1.5-2.0 | 101 languages | Truly multilingual |

## Token Efficiency Impact

**Example**: "我喜欢学习中文" (7 Chinese characters)

- BERT-base-chinese: 7 tokens (1.0x)
- Qwen: ~9 tokens (1.3x)
- ChatGLM: ~10 tokens (1.4x)
- mT5: ~12 tokens (1.7x)
- GPT-4 (cl100k_base): ~18 tokens (2.6x) ⚠️

**Cost/latency impact**: More tokens = higher API cost + slower inference.

## Selection Heuristics

**Chinese-only research?** → BERT-base-chinese (standard, character-level)

**Chinese-primary production?** → Qwen (best token efficiency + performance)

**Bilingual Chinese-English?** → ChatGLM or Qwen (both work well)

**True multilingual (10+ languages)?** → mT5 (covers 101 languages)

**Using OpenAI APIs?** → Accept 2-3x token cost or switch to Qwen

**Research reproducibility?** → BERT-base-chinese (most citations, stable)
