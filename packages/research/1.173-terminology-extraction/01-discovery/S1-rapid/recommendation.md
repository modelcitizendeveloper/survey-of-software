# S1 Rapid Discovery: Initial Recommendations

## Executive Summary

Seven pip-installable libraries identified for terminology extraction in Python. Clear split between **statistical/linguistic** approaches (RAKE, YAKE, pyate) and **semantic/transformer** approaches (KeyBERT).

## Landscape Overview

### By Approach:

| Library | Type | Best For | Status |
|---------|------|----------|--------|
| **pyate** | Linguistic + Statistical | Technical terminology | ✓ Active (2023+) |
| **KeyBERT** | Transformer (BERT) | Semantic keywords | ✓ Active (2023+) |
| **YAKE** | Statistical | Quick extraction | ✓ Active |
| **RAKE-NLTK** | Statistical | General keywords | ✓ Maintained |
| **textacy** | spaCy extension | Broader NLP + terms | ✓ Active |
| **topia.termextract** | Legacy POS-based | Legacy projects | ⚠️ Abandoned (2009) |
| **spaCy** | NLP infrastructure | Framework/integration | ✓ Active |

### By Use Case:

**Technical terminology extraction (translation, tech writing)**:
→ **pyate** (multiple algorithms, spaCy-based, terminology-focused)

**Semantic keyword extraction (content tagging, semantic search)**:
→ **KeyBERT** (BERT embeddings, multilingual, meaning-based)

**Quick/lightweight extraction (minimal dependencies)**:
→ **YAKE** (no training, fast, lightweight)

**Legacy projects (existing topia.termextract usage)**:
→ Migrate to **pyate** (modern equivalent)

## Top 2 Recommendations for Further Research

### 1. pyate (Primary for Terminology)
**Why**: Specifically designed for **terminology extraction** (not just keywords). Implements multiple proven algorithms (C-Value, Combo Basic, Weirdness). Modern (spaCy v3), actively maintained, good documentation.

**Trade-offs**:
- ✓ Purpose-built for technical terms
- ✓ Multiple algorithms available
- ✗ Requires spaCy (heavier dependency)
- ✗ Limited to spaCy-supported languages

### 2. KeyBERT (Primary for Semantic Keywords)
**Why**: Modern transformer-based approach. Excels at **semantic keyword extraction** (finding meaningful terms). Excellent multilingual support. Simple API.

**Trade-offs**:
- ✓ Semantic understanding (not just statistics)
- ✓ Multilingual (70+ languages via BERT)
- ✗ Heavier (transformer models)
- ✗ Keywords ≠ terminology (different goals)

## Key Insight: Terminology vs Keywords

**Critical distinction**:
- **Terminology extraction**: Domain-specific technical terms (e.g., "natural language processing", "entity recognition")
- **Keyword extraction**: Semantically important words (e.g., "important", "key findings", "main result")

**pyate** targets terminology. **KeyBERT** targets keywords. Use case determines which is appropriate.

## Excluded from Deep Dive

- **topia.termextract**: Abandoned (2009), superseded by pyate
- **RAKE-NLTK**: General keyword extraction (not terminology-focused)
- **YAKE**: Good for general keywords, but less sophisticated for technical terms
- **textacy**: Broader toolkit (term extraction is one feature among many)
- **spaCy**: Infrastructure, not a term extraction library per se

## Next Steps (S2: Comprehensive)

**For pyate**:
- Compare algorithms (C-Value vs Combo Basic vs Weirdness)
- Benchmark on technical documents
- Evaluate multilingual support (via spaCy models)
- Installation complexity and dependencies

**For KeyBERT**:
- Test on technical vs general content
- Evaluate embedding model choices (sentence-transformers vs others)
- Multilingual performance (CJK support per research label)
- Memory footprint and inference speed

**For both**:
- Compare output quality on same corpus
- Evaluate integration with translation/NLP pipelines
- TCO analysis (dependencies, model sizes)
- Community and long-term viability
