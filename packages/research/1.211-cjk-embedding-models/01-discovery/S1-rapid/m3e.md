# M3E - Moka Massive Mixed Embedding

## Overview
Chinese-focused embedding model developed by Moka AI, designed specifically for semantic search and retrieval tasks in Chinese language applications. Multiple model sizes available with different embedding dimensions.

## CJK Language Support
- **Chinese (Simplified & Traditional)**: Primary focus, excellent support
- **Japanese**: Limited support (not primary training focus)
- **Korean**: Limited support (not primary training focus)
- Training corpus: Large Chinese text corpus including web data, books, and technical content

## Architecture
- Based on BERT architecture with custom Chinese tokenization
- Multiple model variants:
  - m3e-small: 768-dimensional embeddings
  - m3e-base: 768-dimensional embeddings
  - m3e-large: 1024-dimensional embeddings
- Fine-tuned specifically for sentence-level semantic similarity

## Tokenization Approach
- Uses Chinese-specific tokenizer
- Vocabulary optimized for Chinese characters
- Handles traditional and simplified Chinese effectively
- Better character-level coverage than general multilingual models

## Key Strengths for CJK
- Purpose-built for Chinese language tasks
- High performance on Chinese semantic similarity benchmarks
- Lightweight models suitable for production deployment
- Active Chinese developer community
- Well-integrated with Chinese NLP ecosystem

## Limitations
- Chinese-centric (limited performance on Japanese/Korean)
- Smaller model sizes compared to multilingual alternatives
- Less documentation in English
- Training data details not fully disclosed

## Use Cases
- Chinese semantic search
- Document similarity in Chinese
- Question-answering systems for Chinese content
- Recommendation systems for Chinese text
- Cross-lingual retrieval (Chinese-English)

## Availability
- **License**: Apache 2.0 (open source)
- **Model Weights**: Available on Hugging Face and ModelScope
- **Cost**: Free (self-hosted)
- **Integration**: Compatible with sentence-transformers library
