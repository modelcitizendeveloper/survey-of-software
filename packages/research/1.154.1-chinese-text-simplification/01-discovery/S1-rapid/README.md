# S1-rapid: Chinese Text Simplification Libraries

## Quick Summary

**Key Finding**: As of 2026, there are NO mature, pip-installable libraries specifically designed for Chinese text simplification. The landscape consists of:

1. **Research datasets** (MCTS) - training data, not production libraries
2. **Analysis libraries** (HSK-Character-Profiler, HanLP) - measure difficulty, don't transform text
3. **Utility libraries** (jieba, OpenCC) - building blocks for simplification, but you must write the logic yourself

**Reality check**: Unlike English (which has Rewordify, TextCompactor), Chinese text simplification is still mostly a DIY endeavor combining multiple libraries.

**Recommended approach**: Hybrid stack using jieba (segmentation) + HSK-Character-Profiler (analysis) + OpenCC (conversion) + custom simplification rules.

## Libraries Inventory

### 1. Text Simplification (Direct)

**MCTS (Multi-Reference Chinese Text Simplification)**
- **Type**: Research dataset + evaluation scripts
- **Not a library**: Provides training data (691K+ parallel sentences), not a pip-installable tool
- **GitHub**: https://github.com/blcuicall/mcts
- **Use case**: Train your own neural simplification model
- **Limitation**: Requires ML expertise, months of development

**chinese-comprehension**
- **Type**: Analysis tool (not simplification)
- **GitHub**: https://github.com/Destaq/chinese-comprehension
- **What it does**: Analyzes text against your known words
- **What it doesn't do**: Doesn't transform text, just gauges difficulty
- **Install**: Clone + `pip install -r requirements.txt` (not on PyPI)

**Verdict**: No direct text simplification libraries exist on PyPI.

### 2. Analysis Libraries (Measure Difficulty)

**HSK-Character-Profiler**
- **Purpose**: Analyze text readability based on HSK levels
- **GitHub**: https://github.com/Ancastal/HSK-Character-Profiler
- **Pip**: Not on PyPI, clone and run
- **Features**: Character proficiency analysis, text readability scoring
- **For simplification**: Use to verify output difficulty after simplification
- **Status**: Active (2024-2025)

**Language-Analyzer**
- **Purpose**: Multi-language text analysis including HSK profiling
- **GitHub**: https://github.com/Ancastal/Language-Analyzer
- **Features**: HSK profiling, readability analysis
- **Limitation**: Analysis only, not transformation

### 3. NLP Foundations (Building Blocks)

**jieba (结巴分词)**
- **Purpose**: Chinese text segmentation (word splitting)
- **PyPI**: `pip install jieba`
- **GitHub**: https://github.com/fxsjy/jieba
- **Essential for**: Splitting unsegmented Chinese into words before simplification
- **Accuracy**: ~95% for general text
- **Status**: Mature, widely used
- **Modes**:
  - Accurate Mode: Best for text analysis
  - Full Mode: Gets all possible words (overlapping)
  - Search Engine Mode: Cuts long words into short words

**HanLP 2.x**
- **Purpose**: Comprehensive NLP platform (deep learning)
- **PyPI**: `pip install hanlp`
- **GitHub**: https://github.com/HIT-SCIR/ltp
- **Features**: Segmentation, POS tagging, NER, parsing, SRL
- **For simplification**: Segmentation + POS tagging to identify replaceable words
- **Requires**: Python 3.6+, PyTorch/TensorFlow
- **Status**: Active (latest release Oct 2025)

**PyHanLP**
- **Purpose**: Python wrapper for HanLP 1.x (traditional algorithms)
- **PyPI**: `pip install pyhanlp`
- **GitHub**: https://github.com/hankcs/pyhanlp
- **Lighter than**: HanLP 2.x (no deep learning overhead)
- **Status**: Active (latest Jan 2025)

**LTP (Language Technology Platform)**
- **Purpose**: Multi-task Chinese NLP platform
- **PyPI**: `pip install ltp`
- **GitHub**: https://github.com/HIT-SCIR/ltp
- **Features**: Segmentation, POS, NER, dependency parsing, SDP
- **Architecture**: Shared pre-trained model across tasks (efficient)
- **For simplification**: Dependency parsing to identify complex sentence structures
- **Status**: Research-grade (N-LTP from 2020)

**chinese (Chinese Text Analyzer)**
- **PyPI**: `pip install chinese`
- **GitHub**: https://github.com/morinokami/chinese
- **Features**: Tokenization, pinyin conversion, definitions
- **Uses**: jieba or pynlpir for tokenization
- **Supports**: Simplified and Traditional Chinese
- **Limitation**: Analysis/conversion, not simplification

### 4. Character Conversion

**OpenCC (Open Chinese Convert)**
- **Purpose**: Traditional ↔ Simplified conversion
- **PyPI**: `pip install OpenCC` or `pip install opencc-python-reimplemented`
- **GitHub**: https://github.com/BYVoid/OpenCC
- **Conversion modes**:
  - s2t: Simplified → Traditional
  - t2s: Traditional → Simplified
  - s2tw: Simplified → Traditional (Taiwan standard)
  - s2hk: Simplified → Traditional (Hong Kong standard)
- **For simplification**: Pre-process text to normalized form (Simplified)
- **Status**: Mature, actively maintained

**hanziconv**
- **PyPI**: `pip install hanziconv`
- **GitHub**: https://github.com/berniey/hanziconv
- **Purpose**: Simpler Traditional/Simplified conversion
- **Lighter than**: OpenCC (pure Python)

**hanzidentifier**
- **PyPI**: `pip install hanzidentifier`
- **GitHub**: https://github.com/tsroten/hanzidentifier
- **Purpose**: Detect if text is Traditional or Simplified
- **Use before**: Conversion (know what you're working with)

### 5. Vocabulary Tools

**HSK 3.0 Lists**
- **GitHub**: https://github.com/krmanik/HSK-3.0
- **Purpose**: Official HSK vocabulary lists (levels 1-9, 2026 standard)
- **Use for**: Building synonym dictionaries at each level
- **Format**: Character lists, word lists

**TOCFL Vocabulary**
- **GitHub**: https://github.com/skishore/inkstone/pull/47
- **Purpose**: Taiwan TOCFL standards (Traditional Chinese)
- **Use for**: Simplification targeting TOCFL levels

### 6. Research Tools (Not Production Libraries)

**CTAP (Common Text Analysis Platform)**
- **Type**: Research tool (196 linguistic features)
- **Not pip-installable**: Research implementation
- **Paper**: https://aclanthology.org/2022.lrec-1.592.pdf
- **Use for**: Feature extraction for ML models

**CRIE (Chinese Readability Index Explorer)**
- **Type**: Research system (82 features + SVM)
- **Not publicly available**: Academic tool
- **Paper**: https://link.springer.com/article/10.3758/s13428-015-0649-1

## What's Missing

**What you can't pip install** (as of 2026):
- ❌ Complete Chinese text simplification library
- ❌ HSK-aware synonym replacement engine
- ❌ Sentence simplification (complex → simple restructuring)
- ❌ Idiom simplification (成语 handling)
- ❌ Pre-trained neural simplification models (easy to load and use)

**What you must build yourself**:
- Synonym dictionaries mapping HSK 6 words → HSK 3 equivalents
- Sentence splitting logic (identify and split complex sentences)
- Simplification rules engine
- Quality validation pipeline

## Recommended Stack

For building a Chinese text simplification system:

```python
# Install these libraries
pip install jieba          # Segmentation
pip install opencc-python-reimplemented  # Conversion
pip install hanlp          # Optional: advanced NLP features

# Clone these repos
git clone https://github.com/Ancastal/HSK-Character-Profiler
git clone https://github.com/krmanik/HSK-3.0
git clone https://github.com/blcuicall/mcts  # If training neural models
```

**Then build**:
1. Segmentation pipeline (jieba)
2. HSK level analyzer (HSK-Character-Profiler)
3. Custom simplification logic:
   - Word replacement (HSK vocabulary)
   - Sentence splitting
   - Idiom handling
4. Quality validation

## Time Estimates

| Approach | Time | Complexity |
|----------|------|------------|
| Rule-based MVP | 2-4 weeks | Mid-level Python + Chinese speaker |
| Production system | 2-3 months | Senior NLP engineer + linguist |
| Neural model | 4-6 months | ML engineer + data scientist |

## S1-rapid Conclusion

**The reality**: Chinese text simplification is a **BUILD, not BUY** problem in 2026.

Unlike mature NLP tasks (segmentation, POS tagging) with turnkey libraries, simplification requires:
- Custom logic combining multiple libraries
- Domain expertise (Chinese linguistics + NLP)
- Iterative testing with native speakers

**Next steps**:
- S2-comprehensive: Dive into MCTS dataset, neural approaches, feature engineering
- S3-need-driven: Map use cases to implementation strategies
- S4-strategic: Build vs buy analysis, ROI models

## Sources

- [MCTS: A Multi-Reference Chinese Text Simplification Dataset](https://arxiv.org/abs/2306.02796)
- [MCTS GitHub Repository](https://github.com/blcuicall/mcts)
- [chinese-comprehension GitHub](https://github.com/Destaq/chinese-comprehension)
- [HSK-Character-Profiler](https://github.com/Ancastal/HSK-Character-Profiler)
- [jieba PyPI](https://pypi.org/project/jieba/)
- [HanLP Documentation](https://hanlp.hankcs.com/docs/install.html)
- [OpenCC PyPI](https://pypi.org/project/OpenCC/)
- [LTP GitHub](https://github.com/HIT-SCIR/ltp)
- [HSK 3.0 Lists](https://github.com/krmanik/HSK-3.0)
