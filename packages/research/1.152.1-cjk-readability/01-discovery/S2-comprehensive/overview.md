# S2: Structure - How CJK Readability Analysis Works

## Core Algorithm Pipeline

```
Raw Chinese Text
    ↓
1. Text Segmentation (word boundary detection)
    ↓
2. Character/Word Frequency Analysis
    ↓
3. Linguistic Feature Extraction
    ↓
4. Readability Classification (HSK/TOCFL level)
```

## 1. Text Segmentation (Jieba Algorithm)

### The Problem
Chinese text has no spaces - "我爱你" could be "我/爱/你" (I/love/you) or "我爱/你" (my love/you). Must determine word boundaries before analysis.

### How Jieba Works
1. **Prefix dictionary structure**: Fast word graph scanning
2. **DAG construction**: Builds directed acyclic graph of all possible word combinations
3. **Dynamic programming**: Identifies most probable combination based on word frequency
4. **HMM for unknowns**: Uses Hidden Markov Model (Viterbi algorithm) for new words not in dictionary
5. **Character-based tagging**: Recognizes new words through statistical character patterns

### Alternatives
- **BERT-based segmentation**: Deep learning approach for specialized domains (geoscience, legal, etc.)
- **CkipTagger** (Sinica-Taiwan): POS tagging + tokenization
- **HanLP**: More sophisticated NLP pipeline

## 2. Character/Word Frequency Analysis

### Frequency Datasets

**SUBTLEX-CH**
- 46.8 million characters from film/TV subtitles
- 33.5 million words
- Psychologically/cognitively relevant (reflects real usage)

**Jun Da Corpus**
- 9,933 characters
- Most common character (的) appears 7,922,684 times
- 1,000 most common = 89% coverage

**FineFreq**
- Web-scale multilingual dataset
- Covers Mandarin + other high-resource languages

### Key Metrics
- **Coverage**: % of text a learner can read at their level
- **Shannon entropy**: Chinese "alphabet" = 9.56 bits/character (much higher than alphabetic languages)
- **Zipf distribution**: Frequency follows power law (few characters = most usage)

## 3. Linguistic Feature Extraction

### Traditional Features (Easy to Count)
- Character count
- Word count
- Average sentence length
- Vocabulary difficulty (based on HSK/TOCFL lists)
- Vocabulary frequency (from frequency corpora)

### Advanced Features (CRIE: 82 total)

**Character Level**
- Total characters
- Unique characters
- Character frequency distribution

**Word Level**
- Word length
- Word frequency
- Vocabulary diversity (type-token ratio)

**Sentence Level**
- Sentence length
- Clause complexity
- Dependency tree depth

**Discourse Level**
- Cohesion metrics
- Semantic relations
- Topic consistency

### CTAP (196 Features)
4 levels: character, word, sentence, discourse
- More comprehensive than CRIE
- Includes syntactic complexity, lexical sophistication

## 4. Readability Classification

### Simple Formula Approach
```
Readability Score = f(characters, words, avg_sentence_length)
```
- Linear regression on 3 variables
- Fast but less accurate
- Good for quick estimates

### Machine Learning Approach (CRIE)

**Training Data**
- Taiwanese primary/secondary school textbooks
- Pre-labeled by grade level (1-9)

**Model: Support Vector Machine (SVM)**
- Learns nonlinear relationships between 70-82 features
- Maps data to high-dimensionality space
- More accurate than linear formulas
- Can provide diagnostic information (which features make text hard?)

**Output**
- Grade level classification (1-9)
- Diagnostic report (which linguistic features contribute to difficulty)

### HSK/TOCFL Level Mapping

**Character Coverage Method**
```python
def get_hsk_level(text, char_freq_dict):
    chars_in_text = set(segment_characters(text))

    for level in [1, 2, 3, 4, 5, 6]:
        known_chars = get_hsk_chars(level)
        coverage = len(chars_in_text & known_chars) / len(chars_in_text)

        if coverage >= 0.95:  # 95% coverage threshold
            return level

    return "above HSK 6"
```

**Vocabulary Coverage Method**
- Same approach but uses words (ci) instead of characters
- More accurate for TOCFL (word-focused)
- Requires segmentation first

## Technical Challenges

1. **Segmentation ambiguity**: "研究生" = "research student" or "research born"?
2. **New words**: Internet slang, neologisms not in dictionaries
3. **Domain-specific vocabulary**: Medical/legal text needs specialized dictionaries
4. **Simplified vs Traditional**: Two character sets with different frequency patterns
5. **Context dependence**: Character difficulty varies by context (的 vs 辩证法)

## Performance Considerations

- **Jieba segmentation**: ~200K chars/second (fast enough for most use cases)
- **Feature extraction**: Depends on depth (CRIE 82 features slower than simple 3-feature formula)
- **SVM prediction**: Fast once trained (~milliseconds per text)
- **Bottleneck**: Usually segmentation + NLP parsing for syntactic features

## Sources
- [Chinese Word Segmentation - The challenges of splitting Chinese](https://medium.com/@ching.achterwinter/chinese-word-segmentation-2e28feee87fe)
- [Chinese Word Segmentation — ENC2045 Computational Linguistics](https://alvinntnu.github.io/NTNU_ENC2045_LECTURES/nlp/chinese-word-seg.html)
- [jieba · PyPI](https://pypi.org/project/jieba/)
- [Chinese Text Readability Assessment Based on Visualized POS Information](https://www.mdpi.com/1999-4893/18/12/777)
- [SUBTLEX-CH: Chinese Word and Character Frequencies](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0010729)
- [CRIE: An automated analyzer for Chinese texts](https://link.springer.com/article/10.3758/s13428-015-0649-1)
- [CTAP for Chinese: A Linguistic Complexity Feature Analysis](https://aclanthology.org/2022.lrec-1.592.pdf)
- [Chinese character frequency and entropy](https://www.johndcook.com/blog/2019/10/18/chinese-character-entropy/)
