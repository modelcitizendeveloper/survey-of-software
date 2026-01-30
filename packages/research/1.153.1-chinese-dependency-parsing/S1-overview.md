# S1: Overview - Chinese Dependency Parsing

## What is Dependency Parsing?

Dependency parsing analyzes the grammatical structure of a sentence by identifying relationships between words. It focuses on determining syntactic dependencies between "head" words and the words that modify them ("dependents"), creating a tree-like structure that shows how words depend on one another to construct meaning.

Unlike constituency parsing that groups words into phrases (NP, VP, etc.), dependency parsing focuses on binary word-to-word relations, forming a directed graph.

Sources:
- [Dependency grammar - Wikipedia](https://en.wikipedia.org/wiki/Dependency_grammar)
- [The Role of Dependency Parsing in NLP Projects](https://www.projectpro.io/article/dependency-parsing-in-nlp/1158)
- [Dependency Parsing In NLP Explained](https://spotintelligence.com/2023/10/22/dependency-parsing/)

## Why Chinese Dependency Parsing is Unique

Chinese lacks explicit word boundaries, making segmentation both necessary and inherently ambiguous. This creates a unique challenge: word segmentation is the precondition of dependency parsing, which makes dependency parsing suffer from error propagation and unable to directly make use of character-level pre-trained language models (such as BERT).

Word segmentation has significant impact on dependency parsing performance in Chinese, as variations in segmentation schemes lead to differences in the number and structure of tokens, which affect both the syntactic representations learned by the parser and the evaluation metrics used to assess parsing quality.

Sources:
- [Character-Level Dependency Model for Joint Word Segmentation](https://www.academia.edu/136870493/Character_Level_Dependency_Model_for_Joint_Word_Segmentation_POS_Tagging_and_Dependency_Parsing_in_Chinese)
- [Parsing Through Boundaries in Chinese Word Segmentation](https://arxiv.org/html/2503.23091)
- [A Graph-based Model for Joint Chinese Word Segmentation and Dependency Parsing](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00301/43541/A-Graph-based-Model-for-Joint-Chinese-Word)

## Major Frameworks

### Universal Dependencies (UD)

Universal Dependencies provides standardized treebanks across languages. For Chinese, several treebanks exist:

- **Chinese-CFL**: Essays by learners of Mandarin as a foreign language (Simplified Chinese)
- **Chinese-HK**: Film subtitles and legislative proceedings from Hong Kong (Traditional Chinese)
- **Chinese-PUD**: 1000 sentences from CoNLL 2017 shared task
- **Classical Chinese**: Ancient Chinese texts annotated by Kyoto University

Cross-lingual parsers have been implemented for Chinese and 29 UD treebanks with promising results.

Sources:
- [Universal Dependencies](https://universaldependencies.org/)
- [UD_Chinese-PUD GitHub](https://github.com/UniversalDependencies/UD_Chinese-PUD/tree/master)
- [UD_Chinese-HK GitHub](https://github.com/UniversalDependencies/UD_Chinese-HK)

### Stanford CoreNLP

Stanford CoreNLP includes a neural dependency parser that supports Chinese with CoNLL Dependencies. The parser uses a neural network classifier with three main transition types (LEFT-ARC, RIGHT-ARC, SHIFT) to build dependency trees through a linear-time scan.

A Chinese parser based on the Chinese Treebank is included in the distribution.

Sources:
- [Stanford Neural Dependency Parser](https://nlp.stanford.edu/software/nndep.html)
- [CoreNLP Dependency Parsing](https://stanfordnlp.github.io/CoreNLP/depparse.html)
- [CoreNLP GitHub](https://github.com/stanfordnlp/CoreNLP)

### HanLP

HanLP is a multilingual NLP library designed for researchers and enterprises, built on PyTorch and TensorFlow 2.x. HanLP 2.1 offers 10 joint tasks on 130 languages including tokenization, dependency parsing, semantic dependency parsing, and more.

Notable features:
- Open-source Ancient Chinese model with dependency parsing
- Licensed under Apache 2.0 (free for commercial use)
- Models like CTB7_BIAFFINE_DEP_ZH for Chinese dependency parsing

Sources:
- [HanLP PyPI](https://pypi.org/project/hanlp/)
- [HanLP Dependency Parsing Demo](https://hanlp.hankcs.com/en/demos/dep.html)
- [HanLP GitHub](https://github.com/hankcs/HanLP/tree/master)

## Key Findings

1. **Joint Processing**: Modern approaches combine word segmentation, POS tagging, and dependency parsing to reduce error propagation
2. **Character-Level Models**: Recent work uses character-level parsing to avoid word segmentation bottlenecks
3. **Multiple Standards**: Chinese dependency parsing uses different annotation schemes (UD, Stanford Dependencies, CTB)
4. **Active Research**: 2025 work shows LLMs fine-tuned on Chinese dependency parsing tasks improving quality
