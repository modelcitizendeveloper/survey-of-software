# Stanford CoreNLP (Comprehensive)

## Architecture

**Type**: Statistical NLP with neural network models
**Training Data**: Chinese Treebank (CTB) 5.1, 6.0, 7.0 - modern Chinese newspaper text
**Models**: LSTM-based for POS tagging, neural dependency parser

## Detailed Capabilities

### Tokenization
- Chinese word segmentation using CRF or neural models
- Trained on CTB (modern Chinese)
- Handles Simplified and Traditional characters
- **Classical Chinese fit**: Poor - modern segmentation rules don't apply

### POS Tagging
- Penn Chinese Treebank tagset
- 33 POS tags for modern Chinese
- Accuracy: ~95% on modern Chinese test sets
- **Classical Chinese fit**: Poor - grammar categories differ significantly

### Dependency Parsing
- Neural dependency parser (Universal Dependencies format)
- Trained on UD Chinese GSD corpus
- Accuracy: ~80% LAS on modern Chinese
- **Classical Chinese fit**: Limited - syntax rules differ

### Named Entity Recognition
- PERSON, LOCATION, ORGANIZATION
- Trained on modern Chinese news
- **Classical Chinese fit**: Poor - historical names and titles not recognized

## Performance Characteristics

- **Speed**: ~1000 tokens/second (CPU), faster on GPU
- **Memory**: ~2GB RAM for Chinese models
- **Scalability**: Can process large corpora batch-wise

## Integration

### Java
```java
Properties props = new Properties();
props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse");
props.setProperty("tokenize.language", "zh");
StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
```

### Python (via Stanza)
```python
import stanza
nlp = stanza.Pipeline('zh', processors='tokenize,pos,lemma,depparse')
doc = nlp("君子不器")  # Modern Chinese optimized
```

## Limitations for Classical Chinese

1. **Training data mismatch**: CTB contains 1990s-2000s news, not pre-Qin texts
2. **Word boundaries**: Classical Chinese compounds follow different rules
3. **Grammar structures**: Classical patterns (e.g., topic-comment) not well-represented
4. **Function words**: Different particles (也、矣、焉) not properly categorized
5. **No historical NER**: Can't recognize historical figures or ancient place names

## Adaptation Strategy

To use for Classical Chinese would require:
1. **Retraining**: Need Classical Chinese annotated corpus
2. **Tagset mapping**: Map modern POS tags to Classical categories
3. **Custom segmentation**: Implement Classical word boundary rules
4. **Significant effort**: Months of work, requires NLP expertise

## Verdict

Not suitable out-of-the-box for Classical Chinese. Good reference architecture if building custom solution.
