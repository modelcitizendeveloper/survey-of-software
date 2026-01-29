# BLOOM - BigScience Large Open-science Open-access Multilingual Language Model

## Overview
176B parameter multilingual model trained by BigScience initiative (2022). Explicitly designed for multilingual accessibility with 46 natural languages and 13 programming languages.

## CJK Language Support
- **Chinese (Simplified)**: Yes, included in training
- **Japanese**: Yes, included in training
- **Korean**: Yes, included in training
- Training corpus: 1.6TB of deduplicated text across languages

## Architecture
- Transformer decoder (GPT-style)
- 176B parameters (largest variant)
- Trained on ROOTS corpus with language-balanced sampling
- 250 billion tokens during training

## Tokenization Approach
- Custom BLOOM tokenizer
- Vocabulary size: 250,680 tokens
- Designed to handle CJK characters more efficiently than BPE alone
- Language-specific preprocessing for CJK scripts

## Key Strengths for CJK
- Explicit multilingual training (not English-centric transfer)
- Large parameter count enables strong cross-lingual transfer
- Open-source with full model weights available
- Active research community

## Limitations
- Large model size (176B) requires significant compute
- CJK performance varies by language (Chinese stronger than Korean/Japanese in some benchmarks)
- Training data distribution may favor higher-resource languages

## Use Cases
- Multilingual text generation
- Cross-lingual transfer learning
- Research on multilingual model behavior
- Fine-tuning for specific CJK tasks

## Availability
- **License**: BigScience RAIL License (open but with use restrictions)
- **Model Weights**: Available on Hugging Face
- **Cost**: Free (self-hosted) but requires significant GPU resources
