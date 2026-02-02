# Jieba: Technical Deep-Dive

## Algorithm Foundation

### Core Approach
1. **Prefix dictionary** → Directed Acyclic Graph (DAG)
2. **Dynamic programming** → Find maximum probability path
3. **HMM + Viterbi** → Handle unknown words (OOV)

### Step-by-Step Process

**Step 1: Build Word Graph**
```
Input: "我爱北京"
Dictionary lookup: {我, 爱, 北京, 北, 京}

DAG:
我 → 爱 → 北京
         → 北 → 京
```

**Step 2: Find Best Path**
```python
# Dynamic programming selects max probability path
P(我 → 爱 → 北京) = P(我) * P(爱) * P(北京)
P(我 → 爱 → 北 → 京) = P(我) * P(爱) * P(北) * P(京)

# Longer words typically have higher joint probability
# Result: 我 → 爱 → 北京
```

**Step 3: Handle Unknown Words**
```
If "新词" not in dictionary:
- Apply HMM with Viterbi algorithm
- Predict BMES tags (Begin, Middle, End, Single)
- Extract word boundaries from tags
```

## Segmentation Modes

### 1. Precise Mode (Default)
**Algorithm**: Full DAG + max probability path
```python
seg = jieba.cut("text", cut_all=False)
```
- Complexity: O(n²) for DAG construction, O(n) for DP
- Memory: O(n) for DAG storage
- Use: General NLP tasks

### 2. Full Mode
**Algorithm**: Enumerate all possible words
```python
seg = jieba.cut("text", cut_all=True)
```
- Returns ALL words found in dictionary (overlapping)
- Faster than precise mode (no DP needed)
- Use: Search indexing only (not for downstream NLP)

### 3. Search Engine Mode
**Algorithm**: Fine-grained segmentation on top of precise mode
```python
seg = jieba.cut_for_search("text")
```
- Runs precise mode first
- Further splits long words into shorter segments
- Use: Building search indexes (high recall)

### 4. Paddle Mode
**Algorithm**: Neural network (PaddlePaddle)
```python
jieba.enable_paddle()
seg = jieba.cut("text", use_paddle=True)
```
- Requires PaddlePaddle installation
- More accurate but slower
- Use: When accuracy > speed and you have GPU

## Dictionary Structure

### Default Dictionary
- **Format**: Word + Frequency + POS tag
- **Size**: ~50 MB (354,683 entries)
- **Encoding**: UTF-8
- **Structure**: Prefix trie for fast lookup

### Custom Dictionary
```python
jieba.load_userdict("user_dict.txt")
```

**Format**:
```
机器学习 5 n
深度学习 5 n
```
- Frequency = 5 ensures word is kept intact
- POS tag optional

**Effect**: Forces segmenter to treat term as single word

## HMM for Unknown Words

### Model
- **States**: B (Begin), M (Middle), E (End), S (Single)
- **Transition probabilities**: Learned from training corpus
- **Emission probabilities**: Character → State likelihoods

### Example
```
Unknown: "新词汇"
HMM tags: B M E
Result: "新词汇" (one word)
```

## Performance Characteristics

### Speed Breakdown
| Component | Time % |
|-----------|--------|
| Dictionary lookup | 60% |
| DAG construction | 25% |
| HMM (OOV) | 10% |
| Path selection | 5% |

### Optimization Techniques
1. **Prefix trie**: O(m) dictionary lookup (m = word length)
2. **DAG caching**: Reuse for common substrings
3. **Parallel processing**: Linux only, 3.3x speedup on 4-core
4. **Lazy loading**: Dictionary loaded on first use

## Memory Profile

| Component | Memory |
|-----------|--------|
| Dictionary trie | ~50 MB |
| DAG structure | O(n) per sentence |
| HMM matrices | ~5 MB |
| Total runtime | ~100-150 MB |

## Advanced Features

### Keyword Extraction

**TF-IDF**:
```python
import jieba.analyse
keywords = jieba.analyse.extract_tags(text, topK=10, withWeight=True)
```
- IDF values pre-computed from training corpus
- Stopwords filtered

**TextRank**:
```python
keywords = jieba.analyse.textrank(text, topK=10)
```
- Graph-based ranking
- Uses co-occurrence within sliding window

### POS Tagging
```python
import jieba.posseg as pseg
words = pseg.cut("text")
```
- Uses HMM for tagging
- 26 POS categories (similar to PKU corpus)

## Configuration Tuning

### Adjusting Word Frequency
```python
# Force word to be kept together
jieba.suggest_freq("中国科学院", True)

# Force word to be split
jieba.suggest_freq(("中", "将"), True)
```

### Loading Alternative Dictionaries
```python
# Traditional Chinese
jieba.set_dictionary("dict.txt.big")

# Custom full dictionary
jieba.set_dictionary("my_dict.txt")
```

## Accuracy Analysis

### Benchmark Performance
- **PKU corpus**: F1 ~89%
- **MSR corpus**: F1 ~87%
- **CTB corpus**: F1 ~81%

### Where It Fails
1. **Domain-specific terms**: Not in general dictionary
2. **New slang/neologisms**: No training data
3. **Ambiguous contexts**: Single best path may be wrong
4. **Proper names**: Especially transliterated foreign names

### Improvement Strategies
```python
# 1. Add domain dictionary
jieba.load_userdict("finance_terms.txt")

# 2. Dynamically add new terms
jieba.add_word("GPT-4")

# 3. Use Paddle mode for better accuracy
jieba.enable_paddle()
```

## Integration Patterns

### With NLTK
```python
from nltk import FreqDist
words = jieba.cut(text)
fdist = FreqDist(words)
```

### With spaCy
```python
def jieba_tokenizer(text):
    return list(jieba.cut(text))

nlp.tokenizer = jieba_tokenizer
```

### With scikit-learn
```python
from sklearn.feature_extraction.text import CountVectorizer

def jieba_tokenize(text):
    return " ".join(jieba.cut(text))

vectorizer = CountVectorizer(tokenizer=jieba_tokenize)
```

## Technical Limitations

1. **Greedy longest-match bias**: Prefers longer words, may over-segment
2. **No probabilistic output**: Single segmentation (no alternatives)
3. **Context window**: Local optimization, not sentence-global
4. **HMM simplicity**: Cannot capture long-distance dependencies

## Comparison with PKUSEG Algorithm

| Aspect | Jieba | PKUSEG |
|--------|-------|--------|
| Model | Dictionary + HMM | BiLSTM-CRF |
| Training | Pre-trained HMM | Neural training required |
| Context | Local (bigrams) | Global (sentence-level) |
| OOV handling | HMM tags | Neural embeddings |
| Speed | Fast (rule-based) | Slower (neural forward pass) |
| Accuracy | Lower (~85%) | Higher (~96%) |

## When Algorithm Details Matter

Choose Jieba's algorithm when:
- Speed is critical (rule-based > neural)
- Dictionary is high-quality for your domain
- Memory constraints (no GPU needed)

Avoid when:
- Accuracy is paramount (neural models better)
- OOV rate is high (HMM less robust than neural)
- Context matters (BiLSTM sees full sentence)
