# Getting Started with HanLP (Python)

## Installation

HanLP requires Python 3.6 or higher:

```bash
pip install hanlp
```

## Basic Example: RESTful API

```python
from hanlp_restful import HanLPClient

HanLP = HanLPClient('https://hanlp.hankcs.com/api', auth=None, language='mul')
```

## Advanced: Native Python API

```python
import hanlp

tokenizer = hanlp.load('CTB6_CONVSEG')
tagger = hanlp.load('CTB5_POS_RNN_FASTTEXT_ZH')
syntactic_parser = hanlp.load('CTB7_BIAFFINE_DEP_ZH')
```

Create a pipeline with tokenizer, tagger, and syntactic_parser components with specified input/output keys for syntactic dependencies.

## Sources
- [HanLP PyPI](https://pypi.org/project/hanlp/)
- [HanLP Tutorial](https://hanlp.hankcs.com/docs/tutorial.html)
- [HanLP Dependency Parsing Demo](https://hanlp.hankcs.com/en/demos/dep.html)
