# Feature Comparison Matrix

## Comprehensive Tool Comparison

| Feature | Stanford CoreNLP | ctext.org API | Jiayan | Ideal Solution |
|---------|------------------|---------------|--------|----------------|
| **Tokenization/Segmentation** |
| Classical Chinese accuracy | ✗ Poor | ✓ Basic | ✓✓✓ Good | ✓✓✓ |
| Modern Chinese accuracy | ✓✓✓ Excellent | N/A | ✓ Fair | N/A |
| Speed (tokens/sec) | ~1000 | API-limited | ~500 | ~1000 |
| **Part-of-Speech Tagging** |
| Classical Chinese POS | ✗ Inaccurate | ✗ None | ✓ Experimental | ✓✓✓ |
| POS tagset | Penn CTB (33 tags) | N/A | Custom (limited) | Classical grammar |
| Accuracy (modern Chinese) | ~95% | N/A | ~70% | N/A |
| **Syntactic Parsing** |
| Dependency parsing | ✓✓ Modern only | ✗ None | ✗ None | ✓✓✓ |
| Constituency parsing | ✓ Modern only | ✗ None | ✗ None | ✓✓ |
| Classical grammar support | ✗ None | ✗ None | ✗ None | ✓✓✓ |
| **Named Entity Recognition** |
| Modern Chinese NER | ✓✓✓ Good | ✗ None | ✗ None | N/A |
| Historical names | ✗ None | ✗ None | ✗ None | ✓✓✓ |
| Historical places | ✗ None | ✗ None | ✗ None | ✓✓✓ |
| Titles/Offices | ✗ None | ✗ None | ✗ None | ✓✓ |
| **Corpus Access** |
| Training data access | ✓ CTB (purchase) | ✓✓✓ 30K texts | ✗ None | ✓✓ |
| Classical texts | ✗ None | ✓✓✓ Extensive | ✗ None | ✓✓✓ |
| Parallel translations | ✗ None | ✓✓ Available | ✗ None | ✓ Nice-to-have |
| **Technical Details** |
| Language | Java | REST API | Python | Python/Java |
| Installation | Maven/Gradle | N/A | pip install | pip install |
| Dependencies | Heavy (2GB+) | None | Minimal | Moderate |
| Offline capable | ✓ Yes | ✗ No | ✓ Yes | ✓ Yes |
| **Documentation & Support** |
| Documentation quality | ✓✓✓ Excellent | ✓✓ Good | ✓ Limited | ✓✓✓ |
| Community size | Large | Medium | Small | N/A |
| Active maintenance | ✓✓✓ Very active | ✓✓ Active | ✓ Sporadic | ✓✓✓ |
| **Licensing & Cost** |
| License | GPL v3+ | Terms of Service | Open source | Open source |
| Cost | Free | Free/Paid tiers | Free | Free |
| Commercial use | ✓ Allowed | ✓ Paid tiers | ✓ Check license | ✓ |

## Performance Summary

### Accuracy (Classical Chinese Tasks)

| Task | Stanford CoreNLP | Jiayan | Baseline |
|------|------------------|--------|----------|
| Word segmentation | ~60% | ~85% | 100% (ground truth) |
| POS tagging | ~50% | ~65% | 100% (ground truth) |
| Dependency parsing | ~40% | N/A | 100% (ground truth) |

*Note: These are estimated based on domain mismatch. No published benchmarks exist for Classical Chinese specifically.*

### Speed (on 10K character corpus)

| Tool | Processing Time | Throughput |
|------|----------------|------------|
| Stanford CoreNLP | ~30 seconds | ~333 chars/sec |
| ctext.org API | Variable (network) | API-dependent |
| Jiayan | ~15 seconds | ~667 chars/sec |

## Integration Complexity

### Stanford CoreNLP
```python
# Requires Java installation, model downloads
# Python wrapper (Stanza) available but still heavy
Complexity: ★★★☆☆ (Moderate-High)
Setup time: 30-60 minutes
```

### ctext.org API
```python
# Simple HTTP requests, immediate access
# But requires API key management
Complexity: ★☆☆☆☆ (Very Low)
Setup time: 5 minutes
```

### Jiayan
```python
# Pure Python, pip install
# Minimal dependencies
Complexity: ★☆☆☆☆ (Very Low)
Setup time: 5 minutes
```

## Gap Analysis

### What's Missing

1. **Full Classical Chinese parser**: No tool provides accurate dependency or constituency parsing for 文言文
2. **Historical NER**: No pre-trained models for historical Chinese names, places, titles
3. **Classical POS tagging**: No standard tagset or accurate tagger for Classical Chinese grammar
4. **Annotated corpus**: Lack of large-scale annotated Classical Chinese treebank
5. **Benchmarks**: No standardized evaluation datasets for Classical Chinese NLP

### Why the Gap Exists

1. **Small market**: Classical Chinese is a specialized domain
2. **Annotation cost**: Creating annotated Classical Chinese corpus requires expert linguists
3. **Grammar complexity**: Classical Chinese grammar differs significantly from modern
4. **Variation across periods**: Pre-Qin, Han, Tang, Song texts have different characteristics
5. **Academic focus**: Most research focuses on modern Chinese NLP for commercial applications

## Recommended Tool Combination

For a complete Classical Chinese parsing pipeline:

```
1. Text acquisition    → ctext.org API
2. Segmentation        → Jiayan
3. POS tagging         → Custom model (train on annotated data)
4. Parsing             → Custom parser (rule-based or retrained neural model)
5. NER                 → Custom gazetteer + pattern matching
```

## Decision Matrix

### Choose Stanford CoreNLP if:
- Working primarily with modern Chinese
- Need production-ready, well-supported tool
- Have resources to retrain models
- Need full NLP pipeline

### Choose ctext.org API if:
- Need access to Classical Chinese corpus
- Building research/educational tools
- Want simple integration
- Don't need syntactic parsing

### Choose Jiayan if:
- Primary task is Classical Chinese segmentation
- Working in Python
- Need lightweight, fast solution
- Building custom Classical Chinese NLP pipeline

### Build Custom Solution if:
- Need accurate Classical Chinese parsing
- Have annotated training data or resources to create it
- Have NLP expertise in-house
- Time and budget allow (6-12 months development)
