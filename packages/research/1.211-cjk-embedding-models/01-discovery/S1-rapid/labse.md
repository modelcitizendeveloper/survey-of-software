# LaBSE - Language-agnostic BERT Sentence Embedding

## Overview
Google's multilingual sentence embedding model designed for cross-lingual semantic similarity. Trained on translation pairs across 109 languages with dual-encoder architecture. Strong performance on semantic textual similarity tasks across language boundaries.

## CJK Language Support
- **Chinese (Simplified)**: Excellent support (one of 109 training languages)
- **Chinese (Traditional)**: Good support (related script handling)
- **Japanese**: Excellent support (one of 109 training languages)
- **Korean**: Excellent support (one of 109 training languages)
- Training: Multilingual translation pairs including extensive CJK data

## Architecture
- Dual-encoder BERT architecture
- 768-dimensional embeddings
- 12 layers, 12 attention heads
- ~500M parameters
- Trained using additive margin softmax loss
- Translation ranking objective during pre-training

## Tokenization Approach
- SentencePiece tokenizer with shared vocabulary across all languages
- Vocabulary size: 501,153 tokens
- Subword tokenization handles CJK characters effectively
- Language-agnostic tokenization (no explicit language codes needed)
- Unified vocabulary enables true cross-lingual retrieval

## Key Strengths for CJK
- State-of-the-art cross-lingual performance for semantic similarity
- Balanced training across 109 languages (not English-centric)
- Strong zero-shot transfer to unseen language pairs
- Single model handles all CJK languages simultaneously
- Google's production-grade quality and benchmarking
- Works well for CJK ↔ English semantic search

## Limitations
- Large model size (requires significant memory)
- Fixed 768-dimensional embeddings (not configurable)
- Inference speed slower than smaller specialized models
- General-purpose model (may underperform domain-specific models)
- No official fine-tuning guidance from Google
- Training data and methodology not fully disclosed

## Use Cases
- Cross-lingual search (e.g., English query, Chinese documents)
- Multilingual duplicate detection
- Zero-shot cross-lingual classification
- Multilingual semantic similarity for customer support
- Language-agnostic recommendation systems
- Translation quality estimation

## Availability
- **License**: Apache 2.0 (open source)
- **Model Weights**: Available on TensorFlow Hub and Hugging Face
- **Cost**: Free (self-hosted)
- **Integration**: TensorFlow, PyTorch, sentence-transformers
- **Documentation**: Limited official docs, community-driven guides
