# mBERT - Multilingual BERT

## Overview
Google's multilingual variant of BERT (2018). First major multilingual transformer model, trained on Wikipedia text from 104 languages simultaneously. Established baseline for multilingual NLP.

## CJK Language Support
- **Chinese**: Yes (Wikipedia data)
- **Japanese**: Yes (Wikipedia data)
- **Korean**: Yes (Wikipedia data)
- CJK languages included in 104-language training set

## Architecture
- Transformer encoder (original BERT architecture)
- 12 layers, 768 hidden units, 12 attention heads
- 110M parameters (Base model only, no Large variant released)
- Trained with MLM + NSP objectives

## Tokenization Approach
- WordPiece tokenization
- Vocabulary size: 119,547 tokens
- Shared vocabulary across all 104 languages
- CJK characters treated as individual tokens (inefficient for these scripts)

## Key Strengths for CJK
- Historical baseline for multilingual research
- Surprisingly effective cross-lingual transfer despite simple training
- Well-documented and widely adopted
- Lightweight (110M parameters)

## Limitations
- **Vocabulary inefficiency**: WordPiece not optimized for CJK scripts
- Small model size limits capacity for 104 languages
- No language-specific tuning during pre-training
- Outperformed by newer models (XLM-R, XLM-RoBERTa)
- Training data limited to Wikipedia (narrower domain coverage)

## Use Cases
- Baseline for multilingual experiments
- Lightweight multilingual classification
- Low-resource language tasks (where it surprisingly performs well)
- Educational/research purposes

## Availability
- **License**: Apache 2.0 (fully open-source)
- **Model Weights**: Available on Hugging Face and TensorFlow Hub
- **Cost**: Free, minimal GPU requirements (runs on CPU for inference)

## Historical Significance
mBERT demonstrated that multilingual models could achieve cross-lingual transfer without explicit alignment, launching the multilingual model era. However, for production CJK applications, XLM-R or specialized models are now preferred.
