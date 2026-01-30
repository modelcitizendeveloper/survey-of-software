# HanLP

## What It Is
Modern multilingual NLP library built on PyTorch/TensorFlow 2.x. Despite the name "Han Language Processing", HanLP 2.x supports 130+ languages while maintaining strong Chinese capabilities.

## Chinese Support
Comprehensive Chinese NLP tasks:
- Word segmentation
- POS tagging
- Named entity recognition
- **Dependency parsing** (syntactic)
- **Semantic dependency parsing** (semantic relations)
- Constituency parsing
- Semantic role labeling
- Plus: text classification, sentiment analysis, conversion tools

## Technical Overview

**Language**: Python (PyTorch/TensorFlow 2.x backend)
**Requirements**: Python 3.6+, optional GPU/TPU
**Output format**: CoNLL-X for dependency parsing

**Parsing models**:
- Biaffine parser architecture
- Pretrained models like `CTB7_BIAFFINE_DEP_ZH`
- Inputs: tokens + POS tags
- Outputs: Dependency trees

**API options**:
- Native Python API (for development)
- RESTful API (for production services)
- Lightweight packages (KB-sized for mobile)

## Ecosystem Position

**Strengths**:
- Both syntactic and semantic dependency parsing
- Multilingual support enables cross-language projects
- Modern architecture (transformers, pretrained models)
- Flexible deployment (native/REST/mobile)
- Active development with regular releases

**Limitations**:
- Heavier dependencies than specialized tools
- Documentation primarily in Chinese for advanced features
- Performance varies by task (segmentation gap vs THULAC per benchmarks)
- GPU recommended for production speed

## Quick Assessment

**Use HanLP when**:
- Building modern ML pipelines with Chinese text
- Need both syntactic and semantic dependencies
- Require multiple NLP tasks beyond parsing
- Have GPU resources for production
- Building multilingual applications

**Choose alternatives when**:
- Need only dependency parsing (Stanza is lighter)
- Constrained environments (mobile, edge) without GPU
- Prioritize raw speed over feature breadth
- Legacy system integration requirements

## Key Resources
- Official docs: https://hanlp.hankcs.com/docs/
- GitHub: https://github.com/hankcs/HanLP
- PyPI: https://pypi.org/project/hanlp/
- Online demo: https://hanlp.hankcs.com/en/demos/dep.html
