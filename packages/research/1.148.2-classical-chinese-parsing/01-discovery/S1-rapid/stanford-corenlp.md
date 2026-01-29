# Stanford CoreNLP

## Overview

Stanford CoreNLP is a comprehensive Java-based NLP toolkit developed by the Stanford NLP Group. It provides a wide range of natural language analysis tools including tokenization, part-of-speech tagging, named entity recognition, parsing, and coreference resolution.

## Classical Chinese Support

**Status**: Partial support through Chinese language models

- **Tokenization**: Chinese word segmentation available
- **POS Tagging**: Chinese part-of-speech tagging supported
- **Dependency Parsing**: Chinese dependency parsing available
- **Classical Chinese**: Not specifically optimized for pre-modern Chinese (文言文)

## Key Features

- Multi-language support (including Simplified and Traditional Chinese)
- Modular pipeline architecture
- Well-documented Java API
- Python wrapper available (stanfordnlp/stanza)
- Trained on modern Chinese corpora (CTB - Chinese Treebank)

## Strengths

- **Mature and stable**: Widely used in academic and industry settings
- **Comprehensive**: Full NLP pipeline from tokenization to dependency parsing
- **Actively maintained**: Regular updates from Stanford NLP Group
- **Strong parsing**: State-of-art dependency parsing for modern Chinese

## Limitations for Classical Chinese

- **Modern Chinese focus**: Models trained primarily on contemporary texts
- **Grammar differences**: Classical Chinese grammar differs significantly from modern
- **Word boundaries**: Classical Chinese word segmentation rules differ
- **No specialized models**: No pre-trained models specifically for 文言文

## Availability

- **Repository**: https://github.com/stanfordnlp/CoreNLP
- **License**: GPL v3+
- **Installation**: Maven Central, or direct download
- **Dependencies**: Java 8+

## Initial Assessment

Good general-purpose NLP toolkit, but would require retraining or fine-tuning for Classical Chinese. Better suited for modern Chinese text analysis.
