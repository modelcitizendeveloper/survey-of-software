# Discovery Phase: Chinese Morphological Analysis

## Overview

Comprehensive 4-pass evaluation of libraries and approaches for Chinese character decomposition and morphological analysis.

**Date:** January 2026
**Research ID:** 1.148.1

## Executive Summary

### Key Finding
Two separate problem domains identified:
1. **Character decomposition** (sub-character structure analysis)
2. **Word segmentation** (identifying word boundaries)

No single library handles both. Recommended approach: Modular architecture combining makemeahanzi (character data) with HanLP/Stanza (word processing).

### Strategic Recommendation
- **Character analysis:** makemeahanzi + CJKVI-IDS (data-first approach)
- **Word processing:** HanLP or Stanza (proven NLP platforms)
- **Timeline:** 3-4 weeks to production
- **Risk level:** LOW (no technical debt, standard formats)

---

## S1: Rapid Pass

Quick evaluation of available libraries.

### Files
- [`approach.md`](S1-rapid/approach.md) - Methodology
- [`hanlp.md`](S1-rapid/hanlp.md) - Multilingual NLP toolkit
- [`stanza.md`](S1-rapid/stanza.md) - Stanford NLP with UD framework
- [`ltp.md`](S1-rapid/ltp.md) - Chinese language technology platform
- [`cjklib.md`](S1-rapid/cjklib.md) - Han character library
- [`recommendation.md`](S1-rapid/recommendation.md) - Initial verdict

### Key Insights
- **HanLP, Stanza, LTP:** Word-level NLP, no character decomposition
- **cjklib:** Only library with explicit character decomposition
- **Gap identified:** None handle compound word morpheme analysis

---

## S2: Comprehensive Pass

Deep dive with feature comparison and Python 3 compatibility research.

### Files
- [`approach.md`](S2-comprehensive/approach.md) - Extended methodology
- [`hanlp.md`](S2-comprehensive/hanlp.md) - Detailed assessment
- [`stanza.md`](S2-comprehensive/stanza.md) - UD morphology analysis
- [`ltp.md`](S2-comprehensive/ltp.md) - Lexical vs. morphological analysis
- [`cjklib.md`](S2-comprehensive/cjklib.md) - Python 3 fork evaluation
- [`feature-comparison.md`](S2-comprehensive/feature-comparison.md) - Detailed matrix
- [`recommendation.md`](S2-comprehensive/recommendation.md) - Two-tier approach

### Key Insights
- **makemeahanzi discovered:** Rich JSON data with etymology
- **cjklib3 fork:** Python 3 via 2to3 conversion (technical debt)
- **CJKVI-IDS:** Comprehensive IDS database for extended coverage
- **Morpheme gap confirmed:** No library decomposes compounds

---

## S3: Need-Driven Pass

Evaluation based on concrete use cases.

### Files
- [`approach.md`](S3-need-driven/approach.md) - Use case methodology
- [`use-case-educational.md`](S3-need-driven/use-case-educational.md) - Learning tools
- [`use-case-search.md`](S3-need-driven/use-case-search.md) - Information retrieval
- [`use-case-nlp-pipeline.md`](S3-need-driven/use-case-nlp-pipeline.md) - Text processing
- [`use-case-etymology.md`](S3-need-driven/use-case-etymology.md) - Character origins
- [`recommendation.md`](S3-need-driven/recommendation.md) - Use case mapping

### Key Insights
- **Educational:** makemeahanzi excels (rich etymology, stroke data)
- **Search/IR:** cjklib has best APIs (but Python 2 debt)
- **NLP:** HanLP/Stanza/LTP all excellent (choose by need)
- **Etymology:** makemeahanzi only library with explicit etymology field

### Use Case → Tool Mapping
| Use Case | Winner | Rationale |
|----------|--------|-----------|
| Learning tools | makemeahanzi | Etymology + strokes |
| Search systems | cjklib concepts + modern Python | Best algorithms, need modernization |
| NLP pipelines | HanLP/Stanza/LTP | Production-ready |
| Etymology research | makemeahanzi + Sears DB | Best data sources |

---

## S4: Strategic Pass

Long-term viability and risk assessment.

### Files
- [`approach.md`](S4-strategic/approach.md) - Strategic dimensions
- [`cjklib-viability.md`](S4-strategic/cjklib-viability.md) - HIGH RISK verdict
- [`makemeahanzi-viability.md`](S4-strategic/makemeahanzi-viability.md) - LOW RISK verdict
- [`nlp-platforms-viability.md`](S4-strategic/nlp-platforms-viability.md) - LOW RISK verdict
- [`recommendation.md`](S4-strategic/recommendation.md) - Modular architecture

### Risk Assessment
| Approach | Maintenance | Technical Debt | Long-term Viability |
|----------|-------------|----------------|-------------------|
| cjklib | HIGH RISK | HIGH | ⚠️ MODERATE |
| makemeahanzi | LOW RISK | NONE | ✅ HIGH |
| NLP Platforms | LOW RISK | LOW | ✅ HIGH |

### Strategic Insights
- **cjklib:** Technical debt from Python 2 → avoid for new projects
- **makemeahanzi:** Data-first = future-proof, zero lock-in
- **Modular architecture:** Separate character and word processing
- **Timeline:** 3-4 weeks to production-ready system

---

## Final Recommendations

### For Production Systems
**Character Analysis:** makemeahanzi (+ CJKVI-IDS for rare chars)
**Word Processing:** HanLP or Stanza
**Architecture:** Modular, loosely coupled
**Timeline:** 3-4 weeks

### For Research Projects
**Character Analysis:** Custom tool on CJKVI-IDS + makemeahanzi
**Word Processing:** Stanza (UD framework)
**Timeline:** 4-6 weeks

### For Quick Prototypes
**Character Analysis:** makemeahanzi JSON parsing
**Word Processing:** Jieba (lightweight)
**Timeline:** 1 week

---

## Related Documents

- [`../DOMAIN_EXPLAINER.md`](../DOMAIN_EXPLAINER.md) - Universal analogies for decision makers
- Source repositories:
  - [makemeahanzi](https://github.com/skishore/makemeahanzi)
  - [CJKVI-IDS](https://github.com/cjkvi/cjkvi-ids)
  - [HanLP](https://github.com/hankcs/HanLP)
  - [Stanza](https://stanfordnlp.github.io/stanza/)
  - [cjklib](https://github.com/cburgmer/cjklib)

---

## Research Metadata

**Researcher:** research/polecats/toast
**Date Completed:** 2026-01-29
**Libraries Evaluated:** 7 (HanLP, Stanza, LTP, cjklib, makemeahanzi, CJKVI-IDS, Jieba)
**Use Cases Analyzed:** 4 (Educational, Search, NLP Pipeline, Etymology)
**Total Documents:** 21 markdown files
**Word Count:** ~15,000 words

**Status:** ✅ Complete - All 4 passes executed, DOMAIN_EXPLAINER.md created
