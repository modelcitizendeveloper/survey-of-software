# text2vec-chinese - Chinese Text to Vector Library

## Overview
Practical Chinese text embedding library focused on ease of use and production deployment. Provides pre-trained models and utilities specifically optimized for Chinese NLP tasks.

## CJK Language Support
- **Chinese (Simplified)**: Primary and strongest support
- **Chinese (Traditional)**: Good support
- **Japanese**: Not supported
- **Korean**: Not supported
- Training: Multiple Chinese corpora including news, social media, and technical documents

## Architecture
- Multiple backend models supported:
  - CoSENT (Cosine Sentence) models
  - SBERT-based models
  - SimBERT variants
- Embedding dimensions: Typically 256 or 768 depending on model
- Optimized for speed and memory efficiency

## Tokenization Approach
- Jieba segmentation for word-level tokenization
- Character-level tokenization options
- Custom vocabulary for Chinese characters
- Handles Chinese punctuation and special characters

## Key Strengths for CJK
- Easy-to-use Python API focused on Chinese
- Multiple pre-trained models for different use cases
- Fast inference speed (optimized for production)
- Good balance between model size and performance
- Comprehensive Chinese documentation
- Active maintenance and community support

## Limitations
- Chinese-only (no Japanese/Korean support)
- Smaller model selection compared to international libraries
- Less flexibility than general-purpose frameworks
- Community primarily Chinese-speaking

## Use Cases
- Chinese text classification
- Semantic similarity for Chinese documents
- Question-answering in Chinese
- Text clustering for Chinese content
- Duplicate detection in Chinese text
- Sentence embedding for retrieval systems

## Availability
- **License**: Apache 2.0 (open source)
- **Model Weights**: Available via pip install, Hugging Face
- **Cost**: Free (self-hosted)
- **Integration**: Standalone Python library with simple API
- **Repository**: GitHub (shibing624/text2vec)
