# Stanza - Rapid Assessment

## Overview

Stanford NLP toolkit providing pretrained models for 80 languages based on Universal Dependencies (UD) treebanks. Supports tokenization, lemmatization, POS tagging, morphological features, and dependency parsing.

**Models:** [Available Models & Languages](https://stanfordnlp.github.io/stanza/available_models.html)

**Paper:** [Stanza: A Python NLP Toolkit](https://aclanthology.org/2020.acl-demos.14.pdf)

## Morphological Analysis Capabilities

**Strengths:**
- Universal Dependencies framework provides consistent morphological annotation
- Pretrained models trained on UD v2.12
- Strong academic backing (Stanford NLP)
- Standardized approach across languages

**Limitations:**
- Chinese has "weak morphology" - lacks formal devices like tense/number markers
- UD tagging focuses on grammatical features, not character structure
- Research notes "very little research devoted to Chinese word segmentation based on morphemes" ([Computational Linguistics](https://direct.mit.edu/coli/article/42/3/391/1538/Towards-Accurate-and-Efficient-Chinese-Part-of))

## Character Decomposition

**None** - Stanza focuses on morphological features (grammatical properties) not character decomposition. The UD framework doesn't model character-level structure.

## Maturity

**High** - Stable, well-documented, production-ready. Part of Stanford's NLP infrastructure.

## Quick Verdict

**Good for:** UD-style morphological tagging, cross-lingual NLP, grammatical analysis
**Not suitable for:** Character decomposition, radical analysis

Stanza provides morphological features in the UD sense (grammatical properties), not character structure analysis. Chinese morphology in UD focuses on word-level features, not sub-character components.

---

Sources:
- [Stanza Available Models](https://stanfordnlp.github.io/stanza/available_models.html)
- [Stanza Paper (ACL 2020)](https://aclanthology.org/2020.acl-demos.14.pdf)
- [Towards Accurate and Efficient Chinese POS Tagging](https://direct.mit.edu/coli/article/42/3/391/1538/Towards-Accurate-and-Efficient-Chinese-Part-of)
