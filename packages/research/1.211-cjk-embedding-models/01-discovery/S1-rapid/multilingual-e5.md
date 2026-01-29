# multilingual-e5 - Microsoft's Multilingual Text Embeddings

## Overview
Part of Microsoft's E5 (EmbEddings from bidirEctional Encoder rEpresentations) family. Multilingual variant trained on 100+ languages with state-of-the-art performance on cross-lingual retrieval benchmarks. Uses contrastive learning on text pairs.

## CJK Language Support
- **Chinese (Simplified)**: Excellent support (included in 100+ languages)
- **Chinese (Traditional)**: Good support
- **Japanese**: Excellent support (included in 100+ languages)
- **Korean**: Excellent support (included in 100+ languages)
- Training: Massive multilingual corpus with supervised contrastive learning

## Architecture
- Multiple model sizes available:
  - multilingual-e5-small: 384-dimensional embeddings (~118M parameters)
  - multilingual-e5-base: 768-dimensional embeddings (~278M parameters)
  - multilingual-e5-large: 1024-dimensional embeddings (~560M parameters)
- XLM-RoBERTa backbone
- Contrastive learning objective
- Trained on 1 billion multilingual text pairs

## Tokenization Approach
- XLM-RoBERTa tokenizer (SentencePiece)
- Vocabulary size: 250,002 tokens
- Language-agnostic subword tokenization
- Handles CJK scripts effectively without explicit segmentation
- Shared vocabulary across all supported languages

## Key Strengths for CJK
- State-of-the-art MTEB (Massive Text Embedding Benchmark) scores
- Strong zero-shot cross-lingual transfer
- Multiple model sizes for different latency/quality trade-offs
- Excellent documentation and examples
- Active development by Microsoft Research
- Handles code-switching (mixed CJK-English text)
- Instruction-following variant available (e5-mistral)

## Limitations
- Larger models require significant GPU memory
- Multilingual models may slightly underperform on Chinese-only tasks vs M3E
- Training details partially documented (not fully reproducible)
- Less community adoption than sentence-transformers (newer release)
- No specialized CJK-only variant

## Use Cases
- Cross-lingual semantic search (CJK and English)
- Multilingual document retrieval
- Zero-shot classification for CJK languages
- Semantic similarity across language boundaries
- Multilingual RAG (Retrieval-Augmented Generation) pipelines
- Intent detection in multilingual customer support

## Availability
- **License**: MIT License (open source)
- **Model Weights**: Available on Hugging Face
- **Cost**: Free (self-hosted)
- **Integration**: Compatible with sentence-transformers, Hugging Face Transformers
- **Documentation**: Microsoft research papers, Hugging Face model cards
- **Benchmarks**: Extensive evaluation on MTEB benchmark
