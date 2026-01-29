# XLM-RoBERTa - Cross-lingual Language Model RoBERTa

## Overview
Facebook AI's cross-lingual pre-trained model (2019). Extends RoBERTa architecture to 100 languages using unsupervised cross-lingual learning. Available in Base (270M) and Large (550M) variants.

## CJK Language Support
- **Chinese**: Full support (Simplified and Traditional)
- **Japanese**: Full support
- **Korean**: Full support
- Trained on CommonCrawl data covering all three CJK languages

## Architecture
- Transformer encoder (BERT-style, RoBERTa optimizations)
- Masked Language Modeling (MLM) objective only
- No Next Sentence Prediction (NSP)
- Self-supervised training on 2.5TB of CommonCrawl data

## Tokenization Approach
- SentencePiece tokenizer with unigram language model
- Vocabulary size: 250K
- Language-agnostic byte-pair encoding
- Handles CJK characters as multi-byte sequences

## Key Strengths for CJK
- Strong cross-lingual transfer (knowledge transfers between languages)
- No need for parallel data during pre-training
- Proven performance on XTREME benchmark (includes CJK tasks)
- Smaller than BLOOM (easier to deploy)

## Limitations
- Encoder-only (not suitable for text generation)
- Performance varies by language pair for transfer tasks
- Some CJK languages underrepresented in training data
- Base model relatively small for complex reasoning

## Use Cases
- Cross-lingual text classification
- Named Entity Recognition (NER) across CJK languages
- Cross-lingual information retrieval
- Multilingual semantic search
- Fine-tuning for downstream CJK tasks

## Availability
- **License**: MIT License (fully open-source)
- **Model Weights**: Available on Hugging Face
- **Cost**: Free, moderate GPU requirements (deployable on single GPU)
