# Stanza

## What It Is
Stanford's modern neural NLP toolkit in Python. The spiritual successor to CoreNLP, trained on Universal Dependencies treebanks for 80+ languages. Native Python, no Java required.

## Chinese Support
Full pipeline for Chinese:
- Tokenization
- Multi-word token expansion
- POS tagging
- Lemmatization
- **Dependency parsing**
- Named entity recognition

**Parsing approach**: Transition-based dependency parsing (faster than CoreNLP's graph-based method)

## Technical Overview

**Language**: Python (PyTorch backend)
**Output format**: Universal Dependencies v2.12
**Models**: Pretrained neural models for Chinese from UD treebanks

**Architecture**:
- Neural pipeline with transformer-based models
- Each task is an independent module but shares tokenization
- DepparseProcessor requires: Tokenize, MWT, POS, Lemma processors
- Designed for accuracy and efficiency balance

**Key differences from CoreNLP**:
- Transition-based vs graph-based parsing
- Faster processing for large-scale applications
- Different training data and model architectures
- Native Python (no Java dependency)

## Ecosystem Position

**Strengths**:
- Official Stanford successor to CoreNLP for Python
- Clean, consistent API across 80+ languages
- Strong academic foundation with regular updates
- UD-native (trained and outputs UD format)
- Efficient for production use

**Limitations**:
- Focused on core NLP tasks (no semantic parsing like HanLP)
- Requires all upstream processors (token, POS, lemma) for parsing
- Less Chinese-specific optimization than HanLP or LTP
- PyTorch dependency adds overhead for minimal deployments

## Quick Assessment

**Use Stanza when**:
- Building UD-compliant multilingual pipelines
- Migrating from CoreNLP to modern Python stack
- Need reliable, well-documented tool from trusted source
- Prioritize accuracy on standard benchmarks
- Academic research requiring reproducibility

**Choose alternatives when**:
- Need Chinese-specific optimizations (→ LTP, HanLP)
- Require semantic dependency parsing (→ HanLP)
- Building minimal deployment (→ lighter tools)
- Already invested in TensorFlow ecosystem (→ HanLP)

## Key Resources
- Official docs: https://stanfordnlp.github.io/stanza/
- GitHub: https://github.com/stanfordnlp/stanza
- Dependency parsing: https://stanfordnlp.github.io/stanza/depparse.html
- Available models: https://stanfordnlp.github.io/stanza/available_models.html
