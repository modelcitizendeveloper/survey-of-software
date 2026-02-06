# S1 Rapid Discovery: Approach

**Goal**: Identify the main Python libraries for automatic term extraction and gain initial understanding of their capabilities.

## Research Method

1. Web search for libraries mentioned in research brief (pyate, topia.termextract, spaCy, KeyBERT)
2. Expand search to discover additional widely-used libraries (YAKE, RAKE, textacy)
3. Verify pip installability (LIBRARY requirement, NOT GUI tools)
4. Quick categorization by approach (statistical, linguistic, transformer-based)

## Libraries Identified

### Core Libraries (from spec):
- **pyate**: spaCy-based implementation of multiple statistical algorithms (C-Value, Basic, Combo Basic, Weirdness)
- **topia.termextract**: Lightweight POS-based term extraction (legacy, 2009)
- **spaCy components**: Built-in NLP pipeline components + ecosystem extensions
- **KeyBERT**: BERT embedding-based keyword/keyphrase extraction

### Additional Discoveries:
- **YAKE**: Unsupervised statistical method, no training required
- **RAKE-NLTK**: Statistical co-occurrence analysis, domain-independent
- **textacy**: Higher-level spaCy wrapper with term extraction features

## Initial Categorization

### Statistical Approaches (No ML Training):
- YAKE (text statistics)
- RAKE-NLTK (word co-occurrence)
- topia.termextract (POS + statistics)

### Linguistic + Statistical:
- pyate (POS tagging + multiple algorithms)
- textacy (spaCy-based, TextRank)

### Transformer-Based:
- KeyBERT (BERT embeddings + cosine similarity)

## Focus for S1

Focus on the four specified libraries (pyate, topia.termextract, spaCy, KeyBERT) while noting alternatives (YAKE, RAKE) for completeness.
