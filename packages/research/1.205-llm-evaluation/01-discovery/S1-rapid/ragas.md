# Ragas (Retrieval-Augmented Generation Assessment Suite)

## Overview
- **Type**: Open-source Python library
- **License**: Apache 2.0
- **Focus**: RAG-specific evaluation metrics

## Key Features
- **RAG Triad**: Structured evaluation framework
- **Lightweight**: Easy integration, pandas-like workflow
- **Reference-free**: No ground truth required
- **Benchmarked**: Against LLM-AggreFact, TREC-DL, HotPotQA

## Core Metrics (RAG Triad)
1. **Faithfulness**: How accurately answer reflects retrieved evidence
2. **Context Relevancy**: How relevant retrieved docs are to query
3. **Answer Relevancy**: How relevant answer is to user question
4. **Context Recall**: Coverage of relevant information
5. **Context Precision**: Signal-to-noise in retrieved context

## Extended Capabilities
- Agentic workflow metrics
- Tool use evaluation
- SQL evaluation
- Multimodal faithfulness
- Noise sensitivity testing

## Limitations
- Metrics somewhat opaque (not self-explanatory)
- RAG-focused, not general LLM evaluation
- Need to combine with other tools for full coverage
- Lower metric count than DeepEval

## Best For
- RAG pipeline evaluation specifically
- Teams wanting targeted retrieval metrics
- Lower-cost alternative to LLM-as-judge for RAG
- Quick integration with existing RAG systems

## Installation
```bash
pip install ragas
```

## Pricing
- **Open-source**: Free
