# S2-comprehensive: Technical Deep Dive

## Status: 🚧 IN PROGRESS

This phase will cover the technical depth of Chinese text simplification, including:

## Planned Topics

### 1. Neural Model Architectures
- Transformer-based approaches (T5, BART, mBART)
- Seq2seq vs pre-trained models
- Fine-tuning strategies for Chinese
- Model size trade-offs (performance vs inference speed)

### 2. MCTS Training Pipeline
- Dataset structure and format
- Training data preprocessing
- Model training workflow
- Hyperparameter tuning
- Evaluation on multi-reference test set

### 3. Rule-Based Approaches (Detailed)
- Synonym extraction methods
- HSK-level word mapping strategies
- Sentence splitting algorithms
- Idiom detection and replacement
- Compound word handling

### 4. Evaluation Metrics
- BLEU score for simplification
- SARI (System output vs references And against the Input sentence)
- HSK-aware metrics (vocabulary coverage)
- Semantic similarity (meaning preservation)
- Fluency metrics
- Human evaluation protocols

### 5. Feature Engineering
- Linguistic features for simplification
- Character frequency analysis
- Sentence complexity metrics
- Discourse structure
- Readability formulas for Chinese

### 6. Comparative Analysis
- Rule-based vs neural (detailed comparison)
- Accuracy vs speed trade-offs
- Error analysis (what fails in each approach)
- Hybrid architectures

## Research Questions

1. **What makes a good simplification model?**
   - Accuracy benchmarks from MCTS paper
   - State-of-the-art results (2024-2026)

2. **How do you train on MCTS dataset?**
   - Step-by-step training guide
   - GPU requirements
   - Training time estimates
   - Fine-tuning vs training from scratch

3. **What linguistic features matter most?**
   - Feature importance analysis
   - Correlation with simplification quality

4. **How do you evaluate without ground truth?**
   - Multi-reference evaluation
   - Automatic metrics vs human judgment
   - Inter-annotator agreement

## Estimated Time

3-4 hours for comprehensive technical research

## Deliverables (Planned)

- `neural-architectures.md` - T5, BART, mBART for Chinese TS
- `mcts-training-guide.md` - How to train on MCTS dataset
- `evaluation-metrics.md` - BLEU, SARI, HSK metrics deep dive
- `rule-based-detailed.md` - Advanced rule-based techniques
- `feature-engineering.md` - Linguistic features for ML
- `recommendation.md` - S2 technical recommendations

---

**Status**: Outline created, detailed research pending
**Next session**: Start with neural-architectures.md or mcts-training-guide.md
