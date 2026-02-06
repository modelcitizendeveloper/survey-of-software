# Foundational Libraries for Chinese Text Simplification

These libraries don't perform text simplification directly, but they're **essential building blocks** for any simplification system.

## jieba (结巴分词) - Chinese Text Segmentation

**Purpose**: Split continuous Chinese text into words
**Why needed**: Chinese has no spaces between words—you must segment before processing

### Installation
```bash
pip install jieba
```

### Basic Usage
```python
import jieba

text = "我爱自然语言处理"
words = jieba.cut(text)  # Returns generator
print(" / ".join(words))  # Output: 我 / 爱 / 自然语言 / 处理
```

### Segmentation Modes

#### 1. Accurate Mode (Default)
```python
seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# Output: 我 / 来到 / 北京 / 清华大学
```
- Best for text analysis and NLP tasks
- Attempts most accurate segmentation
- **Use for text simplification**

#### 2. Full Mode
```python
seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# Output: 我 / 来到 / 北京 / 清华 / 清华大学 / 华大 / 大学
```
- Finds all possible words (overlapping)
- Fast but not accurate
- Not recommended for simplification

#### 3. Search Engine Mode
```python
seg_list = jieba.cut_for_search("我来到北京清华大学")
# Output: 我 / 来到 / 北京 / 清华 / 华大 / 大学 / 清华大学
```
- Cuts long words into shorter segments
- Good for search indexing
- Not ideal for simplification

### Custom Dictionaries

Add domain-specific words jieba might miss:

```python
jieba.load_userdict("custom_words.txt")
# Format: word frequency part_of_speech
# 台中 100 n
# 云计算 50 n
```

**Critical for simplification**: Add HSK vocabulary to ensure consistent segmentation

### Accuracy

- General text: ~95% accuracy
- Domain-specific: May need custom dictionary (medical, legal, technical)
- Errors cascade: Wrong segmentation → wrong word replacements

### Performance

- Speed: Very fast (millions of characters per second)
- Memory: ~100MB with full dictionary loaded
- Language support: Simplified and Traditional Chinese

### Role in Simplification Pipeline

```python
# 1. Segment text
import jieba
text = "这个句子包含一些复杂的词汇"
words = list(jieba.cut(text))

# 2. Identify words to simplify
# (You build this logic)
for word in words:
    if word_difficulty(word) > target_hsk_level:
        simplified_word = find_synonym(word, target_hsk_level)
        # Replace word
```

**Links**:
- PyPI: https://pypi.org/project/jieba/
- GitHub: https://github.com/fxsjy/jieba

---

## OpenCC - Traditional/Simplified Conversion

**Purpose**: Convert between Traditional and Simplified Chinese variants
**Why needed**: Normalize text before simplification (most resources use Simplified)

### Installation

**Option 1**: Official binding (requires C++ library)
```bash
pip install OpenCC
```

**Option 2**: Pure Python (easier, no dependencies)
```bash
pip install opencc-python-reimplemented
```

### Basic Usage

```python
from opencc import OpenCC

# Initialize converter
cc = OpenCC('s2t')  # Simplified to Traditional

# Convert
text = "开放中文转换"
traditional = cc.convert(text)
print(traditional)  # Output: 開放中文轉換
```

### Conversion Modes

| Mode | Description | Example |
|------|-------------|---------|
| `s2t` | Simplified → Traditional | 中国 → 中國 |
| `t2s` | Traditional → Simplified | 中國 → 中国 |
| `s2tw` | Simplified → Taiwan Standard | 鼠标 → 滑鼠 |
| `s2hk` | Simplified → Hong Kong Standard | 信息 → 資訊 |
| `t2tw` | Traditional → Taiwan Standard | 鼠標 → 滑鼠 |
| `t2hk` | Traditional → Hong Kong Standard | 資訊 → 資訊 |

**Regional variants matter**: Taiwan and Hong Kong use different vocabulary beyond character conversion.

### Advanced Features

#### Character-Level Conversion
- One-to-one character mapping (mostly)
- Handles variant forms (異體字)

#### Phrase-Level Conversion
- Multi-character expressions converted as units
- Example: "计算机" (computer, Mainland) → "電腦" (Taiwan)

#### Regional Idioms
- Idioms converted to regional equivalents
- "鼠标" (mouse, Mainland) → "滑鼠" (Taiwan)

### Role in Simplification Pipeline

**Pre-processing**:
```python
from opencc import OpenCC

# Normalize to Simplified (most HSK resources use Simplified)
converter = OpenCC('t2s')
text = "這是傳統中文"
simplified = converter.convert(text)
# Now use simplified version for HSK analysis and simplification
```

**Post-processing** (if targeting Traditional Chinese learners):
```python
# After simplification, convert back to Traditional
converter = OpenCC('s2t')
output = converter.convert(simplified_text)
```

### Accuracy

- Character conversion: Near 100% for common characters
- Regional vocabulary: Good coverage, but not exhaustive
- Context: Character-level conversion can miss nuances

**Example issue**:
- "后" can mean "后面" (back) or "皇后" (empress)
- Traditional: "後" (back) vs "后" (empress)
- OpenCC uses phrase dictionaries to handle most cases

### Performance

- Very fast (millions of characters per second)
- Minimal memory footprint
- Thread-safe

**Links**:
- GitHub: https://github.com/BYVoid/OpenCC
- PyPI (official): https://pypi.org/project/OpenCC/
- PyPI (pure Python): https://pypi.org/project/opencc-python-reimplemented/

---

## HanLP - Comprehensive NLP Platform

**Purpose**: Multi-task Chinese NLP (segmentation, POS, NER, parsing, etc.)
**Why useful**: Advanced linguistic analysis for sophisticated simplification

### Installation

```bash
pip install hanlp
```

**Requirements**: Python 3.6+, PyTorch or TensorFlow 2.x

### Basic Usage

```python
import hanlp

# Load pre-trained model (downloads on first use)
HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)

# Analyze text
text = "我爱自然语言处理"
result = HanLP(text)

print(result)
# Output includes: tokens, POS tags, NER, dependency parse, etc.
```

### Key Features for Simplification

#### 1. Word Segmentation
```python
tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')
tokens = tokenizer("我爱自然语言处理")
# Alternative to jieba with different algorithm
```

#### 2. Part-of-Speech Tagging
```python
# Included in multi-task model
result = HanLP(text)
pos_tags = result['pos']
# Identify nouns, verbs, adjectives to simplify
```

**Use case**: Only simplify content words (nouns, verbs), not function words

#### 3. Named Entity Recognition
```python
result = HanLP(text)
entities = result['ner']
# Identify people, places, organizations
# DON'T simplify proper nouns
```

#### 4. Dependency Parsing
```python
result = HanLP(text)
deps = result['dep']
# Understand sentence structure
# Identify complex subordinate clauses to split
```

**Use case**: Find sentences with deep syntactic trees → candidates for splitting

#### 5. Semantic Role Labeling (SRL)
```python
result = HanLP(text)
srl = result['srl']
# Identify who did what to whom
# Restructure passive → active voice
```

### HanLP 2.x vs PyHanLP

**HanLP 2.x** (Modern):
- Deep learning models (BERT, ELECTRA)
- State-of-the-art accuracy
- Heavier (requires PyTorch/TF)
- Slower (seconds per sentence)

**PyHanLP** (Traditional):
- Classic algorithms (HMM, CRF)
- Lighter weight (no DL frameworks)
- Faster (milliseconds per sentence)
- Slightly lower accuracy

**For simplification MVP**: Start with PyHanLP (lighter), upgrade to HanLP 2.x if you need advanced features

### Role in Simplification Pipeline

**Advanced simplification logic**:

```python
import hanlp

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)

text = "我昨天买了一本非常有趣的书"
result = HanLP(text)

# 1. Extract POS tags
tokens = result['tok/fine']  # ['我', '昨天', '买', '了', '一', '本', '非常', '有趣', '的', '书']
pos = result['pos/pku']      # ['PN', 'TIME', 'VV', 'AS', 'CD', 'M', 'AD', 'VA', 'DEG', 'NN']

# 2. Identify adjectives and adverbs
for token, tag in zip(tokens, pos):
    if tag in ['VA', 'AD']:  # Adjectives, adverbs
        # Simplify: 非常 → 很, 有趣 → 好玩
        simplified = simplify_word(token)

# 3. Check dependency structure
deps = result['dep']
# If deep nesting → split sentence
```

### Performance Considerations

- **Model loading**: ~10-30 seconds (first time, cached after)
- **Inference**: 0.5-2 seconds per sentence (CPU), faster on GPU
- **Memory**: 500MB-2GB depending on model
- **Batch processing**: Significantly faster for multiple sentences

**For production**: Use smaller models (ELECTRA_SMALL) or cache results

### Alternatives

- **LTP** (Language Technology Platform): Similar features, different architecture
- **jieba + custom POS tagger**: Lighter but less accurate
- **StanfordNLP**: Multi-language but heavier

**Links**:
- Documentation: https://hanlp.hankcs.com/docs/install.html
- PyPI: https://pypi.org/project/hanlp/
- GitHub: https://github.com/hankcs/HanLP

---

## Integration Strategy

**Recommended stack for text simplification**:

1. **OpenCC** - Normalize to Simplified Chinese
2. **jieba** - Segment into words
3. **HanLP** (optional) - POS tagging, NER, parsing for advanced logic
4. **Custom logic** - Synonym replacement, sentence splitting
5. **HSK-Character-Profiler** - Validate output difficulty

**Minimal stack** (faster, lighter):
- jieba + OpenCC + custom rules

**Advanced stack** (higher quality, slower):
- HanLP (all-in-one) + custom rules + MCTS-trained model

## Sources

- [jieba PyPI](https://pypi.org/project/jieba/)
- [jieba GitHub](https://github.com/fxsjy/jieba)
- [OpenCC GitHub](https://github.com/BYVoid/OpenCC)
- [OpenCC PyPI](https://pypi.org/project/OpenCC/)
- [HanLP Documentation](https://hanlp.hankcs.com/docs/install.html)
- [HanLP PyPI](https://pypi.org/project/hanlp/)
