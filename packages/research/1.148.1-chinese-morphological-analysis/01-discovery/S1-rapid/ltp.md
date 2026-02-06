# LTP - Rapid Assessment

## Overview

Language Technology Platform developed by HIT (Harbin Institute of Technology). Integrated Chinese NLP platform with lexical analysis, syntactic parsing, and semantic parsing.

**Repository:** [GitHub - HIT-SCIR/ltp](https://github.com/HIT-SCIR/ltp)

**Recent Version:** N-LTP (Neural LTP) - multi-task framework with shared pretrained models

## Morphological Analysis Capabilities

**Strengths:**
- Six core Chinese NLP tasks: word segmentation, POS tagging, NER, dependency parsing, semantic dependency, semantic role labeling
- N-LTP uses multi-task learning with shared pretrained models
- Cloud service available: [LTP-Cloud](https://www.ltp-cloud.com/intro_en)
- Specifically designed for Chinese (not multilingual adaptation)

**Terminology Note:**
LTP uses "lexical analysis" rather than "morphological analysis". This includes:
- Chinese word segmentation
- Part-of-speech tagging
- Named entity recognition

**Limitations:**
- Focuses on word-level lexical analysis, not character-level decomposition
- No explicit character decomposition features documented
- Designed for document processing pipeline, not character structure study

## Character Decomposition

**None identified** - LTP operates at word/token level, not character component level.

## Maturity

**High** - Established platform with academic backing, production cloud service, and neural architecture updates (N-LTP).

## Quick Verdict

**Good for:** Chinese word segmentation, lexical analysis, NLP pipelines
**Not suitable for:** Character decomposition, radical analysis

LTP is a comprehensive Chinese NLP platform but operates at word level. Like HanLP, it's designed for document processing rather than character structure analysis.

---

Sources:
- [LTP Paper (ACL Anthology)](https://aclanthology.org/C10-3004/)
- [N-LTP: Neural Chinese Language Technology Platform](https://arxiv.org/abs/2009.11616)
- [GitHub Repository](https://github.com/HIT-SCIR/ltp)
- [LTP-Cloud Service](https://www.ltp-cloud.com/intro_en)
