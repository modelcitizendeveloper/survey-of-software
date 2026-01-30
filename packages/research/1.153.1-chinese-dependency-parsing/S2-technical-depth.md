# S2: Technical Depth - Chinese Dependency Parsing

## Core Challenges in Chinese Dependency Parsing

### 1. Word Segmentation Ambiguity

The word segmentation of Chinese expressions is difficult due to the fact that there is no word boundary in Chinese expressions and that there are some kinds of ambiguities that could result in different segmentations.

Recent work on joint word segmentation, POS tagging, and dependency parsing faces two key problems:
- Word segmentation based on character and dependency parsing based on word are not well-combined in the transition-based framework
- Current joint models suffer from insufficiency of annotated corpus

Sources:
- [Character-Level Chinese Dependency Parsing](https://arxiv.org/abs/2406.03772)
- [Incremental Joint Approach](https://www.researchgate.net/publication/262355038_Incremental_joint_approach_to_word_segmentation_POS_tagging_and_dependency_parsing_in_Chinese)

### 2. Long Sentence Complexity

Dependency parsing for Chinese long sentences presents additional challenges. Chinese long sentences often have complex nested structures that require specialized parsing strategies.

Source:
- [Dependency Parsing for Chinese Long Sentence](https://www.researchgate.net/publication/283256381_Dependency_Parsing_for_Chinese_Long_Sentence_A_Second-stage_Main_Structure_Parsing_Method)

## Recent Advances (2025)

### Fine-tuned Large Language Models

A 2025 RANLP paper investigated Chinese dependency parsing using fine-tuned LLMs, specifically exploring how different dependency representations impact parsing performance when fine-tuning Chinese Llama-3.

Key findings:
- Stanford typed dependency tuple representation yields highest number of valid dependency trees
- Converting dependency structure into lexical centered tree produces parses of significantly higher quality

Sources:
- [Branching Out: Exploration of Chinese Dependency Parsing with Fine-tuned LLMs](https://acl-bg.org/proceedings/2025/RANLP%202025/pdf/2025.ranlp-1.166.pdf)
- [ACL Anthology](https://aclanthology.org/2025.ranlp-1.166/)

### LLM-Assisted Data Augmentation

Research on Chinese dialogue-level dependency parsing shows LLMs can assist with data augmentation to improve parser training.

Source:
- [LLM-Assisted Data Augmentation for Chinese Dialogue-Level Dependency Parsing](https://direct.mit.edu/coli/article/50/3/867/120014/LLM-Assisted-Data-Augmentation-for-Chinese)

## Dependency vs Constituency Parsing

### When to Use Dependency Parsing

Dependency parsing is more suitable when you need:

1. **Direct word relationships**: Makes it easy to extract subject-verb-object triples
2. **Free word order languages**: Better suited than constituency parsing
3. **Downstream tasks**: Information extraction, question answering, relation extraction
4. **Performance**: Generally faster and more memory-efficient
5. **Semantic focus**: Direct relationships for semantic parsing or machine translation

### When to Use Constituency Parsing

Use constituency parsing when you need:

1. **Phrase structure**: Extract sub-phrases from sentences
2. **Hierarchical analysis**: Examine phrase-level writing patterns
3. **Traditional syntax**: Understanding sentence structure in classical terms

### Using Both Together

Both techniques have their own advantages and can be used together to better understand a sentence. Some advanced NLP systems employ both to enhance language understanding precision.

Sources:
- [Constituency Parsing and Dependency Parsing - GeeksforGeeks](https://www.geeksforgeeks.org/compiler-design/constituency-parsing-and-dependency-parsing/)
- [Constituency vs Dependency Parsing | Baeldung](https://www.baeldung.com/cs/constituency-vs-dependency-parsing)
- [Medium: Constituency Parsing VS Dependency Parsing](https://medium.com/@varuniy22comp/constituency-parsing-vs-dependency-parsing-3d0855d6e8f5)

## Performance Considerations

### Historical Benchmarks

Comparison of performance across popular open source parsers shows that recent higher-order graph-based techniques can be more accurate, though somewhat slower, than constituent parsers.

For Stanford parsers on English (provides context): Charniak-Johnson reranking parser achieved 89% labeled attachment F1 score for generating Stanford Dependencies.

Sources:
- [A Comparison of Chinese Parsers for Stanford Dependencies](https://nlp.stanford.edu/pubs/stanford_dependencies_chinese.pdf)
- [Parsing to Stanford Dependencies: Trade-offs between speed and accuracy](https://nlp.stanford.edu/pubs/lrecstanforddeps_final_final.pdf)

### Modern Approaches

Character-level parsing models and joint learning frameworks address error propagation challenges. The trend is toward:
- End-to-end neural models
- Pre-trained language model integration
- Joint task learning (segmentation + POS + parsing)
