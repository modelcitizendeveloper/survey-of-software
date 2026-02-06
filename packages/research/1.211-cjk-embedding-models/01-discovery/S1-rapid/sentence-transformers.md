# sentence-transformers - Multilingual Sentence Embeddings

## Overview
Popular Python framework for computing dense vector representations using Transformer models. Supports hundreds of pre-trained models including many with strong multilingual and CJK support. Developed and maintained by UKPLab.

## CJK Language Support
- **Chinese (Simplified & Traditional)**: Excellent support via multilingual models
- **Japanese**: Excellent support via multilingual models
- **Korean**: Excellent support via multilingual models
- Multilingual models trained on 50+ languages including CJK
- Dedicated CJK models available in model hub

## Architecture
- Framework supporting multiple architectures:
  - SBERT (Sentence-BERT)
  - SimCSE
  - MPNet
  - BERT, RoBERTa, XLM-RoBERTa variants
- Typical embedding dimensions: 384, 768, or 1024
- Siamese/triplet network training for semantic similarity

## Tokenization Approach
- Model-dependent tokenization
- Multilingual models use language-agnostic tokenizers
- CJK-specific models may use specialized tokenization
- Supports both WordPiece and SentencePiece tokenizers
- Handles mixed-language input effectively

## Key Strengths for CJK
- Large ecosystem with hundreds of pre-trained models
- Strong multilingual models (paraphrase-multilingual-mpnet, LaBSE integration)
- Consistent API across all models
- Excellent documentation and community
- Production-ready with optimization options
- Fine-tuning capabilities for domain-specific tasks
- Active development and maintenance

## Limitations
- Multilingual models may underperform language-specific models on Chinese-only tasks
- Model selection can be overwhelming (many options)
- Some models are large (performance vs. resource trade-off)
- Not all models handle code-switching well

## Use Cases
- Cross-lingual semantic search (CJK ↔ English)
- Multilingual document clustering
- Paraphrase detection across languages
- Zero-shot classification for CJK text
- Information retrieval in mixed-language corpora
- Semantic similarity for customer support (multilingual)

## Availability
- **License**: Apache 2.0 (framework), model-dependent licenses
- **Model Weights**: Extensive collection on Hugging Face
- **Cost**: Free (self-hosted)
- **Integration**: PyPI package, ONNX export, API servers
- **Ecosystem**: Compatible with Hugging Face, Pinecone, Weaviate, etc.
