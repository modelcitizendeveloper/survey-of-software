# S1 Recommendation: CJK Tokenizers

## Primary Recommendation: SentencePiece

**Confidence:** High (80%)

**Rationale:**
Explicitly designed for CJK languages. The `character_coverage=0.9995` and `split_by_whitespace=False` parameters show intentional CJK support. Adopted by major multilingual models precisely because it handles no-space languages well.

## Context Matters

**Use SentencePiece when:**
- Training a new model with significant CJK data
- Token efficiency matters (API costs, context windows)
- Building a multilingual system

**Use tiktoken when:**
- Speed is critical (real-time inference)
- Already using OpenAI models/ecosystem
- English-dominant with some CJK

**Use HuggingFace Tokenizers when:**
- Using HuggingFace models (Qwen, BERT-Chinese)
- Need pre-trained CJK-optimized tokenizer
- Want Rust-speed + CJK efficiency

## Key Insight from S1

**The tokenizer isn't the issue - the training vocabulary is.**

tiktoken is fast but trained on English-heavy data. SentencePiece with proper CJK training data produces efficient CJK tokenization. HuggingFace Tokenizers with CJK-trained models (like Qwen) get both speed AND efficiency.

**Strategic takeaway:** Don't pick a tokenizer - pick a training strategy or pre-trained model optimized for your target language distribution.
