# S3: Practical Implementation - Chinese Dependency Parsing

## Getting Started with HanLP (Python)

### Installation

HanLP requires Python 3.6 or higher:

```bash
pip install hanlp
```

### Basic Example: RESTful API

```python
from hanlp_restful import HanLPClient

HanLP = HanLPClient('https://hanlp.hankcs.com/api', auth=None, language='mul')
```

### Advanced: Native Python API

```python
import hanlp

tokenizer = hanlp.load('CTB6_CONVSEG')
tagger = hanlp.load('CTB5_POS_RNN_FASTTEXT_ZH')
syntactic_parser = hanlp.load('CTB7_BIAFFINE_DEP_ZH')
```

Create a pipeline with tokenizer, tagger, and syntactic_parser components with specified input/output keys for syntactic dependencies.

Sources:
- [HanLP PyPI](https://pypi.org/project/hanlp/)
- [HanLP Tutorial](https://hanlp.hankcs.com/docs/tutorial.html)
- [HanLP Dependency Parsing Demo](https://hanlp.hankcs.com/en/demos/dep.html)

## Using Stanford CoreNLP

Stanford CoreNLP provides a Java suite of NLP tools. The Chinese parser based on Chinese Treebank is included in the distribution.

The neural dependency parser performs a linear-time scan over sentence words, maintaining:
- A partial parse
- A stack of words currently being processed
- A buffer of words yet to be processed

It applies transitions (LEFT-ARC, RIGHT-ARC, SHIFT) until the buffer is empty and dependency graph is complete.

Sources:
- [CoreNLP GitHub](https://github.com/stanfordnlp/CoreNLP)
- [Stanford Parser](https://nlp.stanford.edu/software/lex-parser.shtml)
- [Parsing Chinese with Stanford NLP](https://michelleful.github.io/code-blog/2015/09/10/parsing-chinese-with-stanford/)

## Real-World Applications

### Question Answering

Dependency structure helps models align question focus with candidate answers. Dependency parsers extract typed relations and generate dependency trees relating questions to passages.

Example use: "Who invented the telephone?" → Extract subject-object relations to find "Alexander Graham Bell invented telephone"

Sources:
- [Question Answering Using Dependency Trees](https://www.rangakrish.com/index.php/2018/04/22/question-answering-using-dependency-trees/)
- [Question answering passage retrieval using dependency relations](https://www.researchgate.net/publication/221300315_Question_answering_passage_retrieval_using_dependency_relations)

### Information Extraction

Dependency parsing identifies relationships between entities in a sentence. Parsing clarifies subject–verb–object relations, improving accuracy for named-entity relation extraction.

Example: "Apple acquired Beats for $3 billion" → Extract (Apple, acquired, Beats) and (price, $3 billion)

Sources:
- [The Role of Dependency Parsing in NLP Projects](https://www.projectpro.io/article/dependency-parsing-in-nlp/1158)
- [Dependency Parsing: A Data Scientist's Guide](https://www.numberanalytics.com/blog/dependency-parsing-data-scientist-guide)

### Other Applications

- **Sentiment Analysis**: Identifies sentiments by associating objects and adjectives
- **Virtual Assistants/Chatbots**: Enhances interpretation of user requests
- **Machine Translation**: Improves translation quality through structural understanding
- **Knowledge Graph Construction**: Bridges token-level analysis to higher-level semantic tasks

Sources:
- [Dependency Parsing in Natural Language Processing with Examples](https://www.analyticsvidhya.com/blog/2021/12/dependency-parsing-in-natural-language-processing-with-examples/)
- [Dependency Parsing: A Comprehensive Guide for 2025](https://www.shadecoder.com/topics/dependency-parsing-a-comprehensive-guide-for-2025)

## Implementation Patterns

### For Chinese Specifically

Chinese implementation must handle:

1. **Word Segmentation First**: Either pipeline (segment → parse) or joint (simultaneous)
2. **Encoding Choice**: Simplified vs Traditional Chinese models
3. **Domain Adaptation**: Different models for modern vs classical Chinese

### Joint vs Pipeline Approach

**Pipeline Approach:**
- Segment text → POS tag → Dependency parse
- Simpler but error propagation issue
- Each stage compounds errors

**Joint Approach:**
- All tasks learned together
- Reduces error propagation
- More complex to implement
- Better overall accuracy

Modern best practice: Use joint models or character-level parsing to avoid segmentation bottleneck.

## Performance Tips

1. **Choose the right model size**: Larger models = better accuracy but slower
2. **Batch processing**: Process multiple sentences together for efficiency
3. **Cache results**: Dependency parsing is deterministic, cache common phrases
4. **Pre-filter**: For large datasets, pre-filter irrelevant text before parsing
5. **GPU acceleration**: Use GPU-enabled models for large-scale processing
