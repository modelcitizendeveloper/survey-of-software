# Bleualign: Comprehensive Analysis

## Algorithm Deep Dive

### BLEU-Based Alignment Strategy
Unlike length-based methods, bleualign uses translation quality to guide alignment:
1. **Translate source → target** (or target → source)
2. **Compare MT output to reference** using sentence-level BLEU
3. **Dynamic programming search** for alignment path maximizing total BLEU
4. **Handle complex alignments** (1-to-N, N-to-1, N-to-M)

### Mathematical Model
```
Score(alignment) = Σ BLEU(MT_output[i], reference[j])

Where alignment maps source sentence i to target sentence(s) j
```

### Why BLEU Works for Alignment
- **Semantic similarity**: High BLEU = similar meaning
- **Robust to paraphrasing**: Captures n-gram overlap beyond exact matches
- **Translation-aware**: Understands language-specific transformations

### Search Strategy
- **Full dynamic programming**: O(n × m) complexity
- **Pruning**: Can limit alignment window for speed
- **Greedy option**: Faster but less accurate

## Parameter Tuning

### Key Parameters
```python
# BLEU variant (sentence-level BLEU with smoothing)
align_documents(
    source_file='src.txt',
    target_file='tgt.txt',
    srctotarget='translated.txt',
    bleu_smoothing='method1'  # SmoothingFunction options
)

# Alignment window (limit search space)
align_documents(
    ...,
    max_skip=5  # Maximum sentences to skip
)

# Sentence matching mode
align_documents(
    ...,
    flexible=True  # Allow 1-to-N alignments
)
```

### Smoothing Methods
Sentence-level BLEU needs smoothing for short sentences:
- **method1**: Add 1 smoothing (default)
- **method2**: Exponential smoothing
- **method3**: Geometric mean
- **method4**: NIST smoothing

### MT System Impact
Different MT systems produce different alignments:
- **Neural MT**: Generally better alignments (semantic understanding)
- **Statistical MT**: Still effective but more brittle
- **Google Translate API**: Convenient but costs money
- **Local Moses**: Free but requires setup

## Performance Characteristics

### Benchmarks (With Different MT Systems)
| MT System | Speed (pairs/min) | Accuracy (F1) | Cost |
|-----------|-------------------|---------------|------|
| Local Moses (CPU) | 1-2K | 91-94% | Free |
| Local NMT (GPU) | 5-10K | 93-97% | Free (hardware) |
| Google Translate API | 10-20K | 94-98% | $$$ |
| DeepL API | 8-15K | 95-98% | $$ |

*Accuracy varies by language pair and corpus quality*

### Bottleneck Analysis
1. **Translation time**: 70-90% of total runtime
2. **BLEU computation**: 5-15%
3. **DP search**: 5-10%

**Optimization**: Cache translations, use batch MT APIs

## Edge Cases & Failure Modes

### When Bleualign Excels

#### 1. Paraphrased Translations
```
Source: "The quick brown fox jumps over the lazy dog."
Target: "A swift auburn canine leaps above an indolent hound."
→ Length-based methods fail; bleualign succeeds via semantic match
```

#### 2. Reordered Segments
```
Source: "First sentence. Second sentence."
Target: "Second sentence first. Then the first one."
→ BLEU captures meaning despite reordering
```

### When Bleualign Struggles

#### 1. Poor MT Quality
```
Low-resource language pair with bad MT
→ BLEU scores are noisy, alignment unreliable
```
**Mitigation**: Use better MT or switch to vecalign

#### 2. Idiomatic Expressions
```
Source: "It's raining cats and dogs."
Target: "Il pleut des cordes." (literal: "raining ropes")
→ MT may not capture idiom, BLEU misleads
```
**Mitigation**: Pre-align high-confidence segments manually

#### 3. Technical vs. Literary Text
```
Technical manual: Bleualign works great (literal translation)
Poetry: Bleualign may struggle (creative translation)
```

## Quality Metrics

### Published Benchmarks
| Dataset | Precision | Recall | F1 | vs Hunalign |
|---------|-----------|--------|-------|-------------|
| WMT News | 96% | 94% | 95% | +8% |
| TED Talks | 94% | 92% | 93% | +10% |
| Legal Docs | 98% | 97% | 97.5% | +2% |
| Literary | 87% | 83% | 85% | +14% |

**Key insight**: Biggest improvement over hunalign on paraphrased/reordered text

### MT System Quality Impact
- **High-quality MT** (BLEU > 30): F1 ~95-98%
- **Medium-quality MT** (BLEU 20-30): F1 ~88-93%
- **Low-quality MT** (BLEU < 20): F1 ~75-85%

## Implementation Details

### Language
- **Python**: Pure Python implementation
- **Dependencies**: NLTK (for BLEU), minimal extras
- **Package**: Available on PyPI

### Extensibility
- **Custom MT**: Easy to plug in any translation system
- **BLEU variants**: Can modify scoring function
- **Output formats**: Customizable via scripting

### Production Considerations

#### Caching Strategy
```python
# Translate once, align many times
translate_corpus(src, output='translations.txt')

# Reuse translations for different alignment runs
align_documents(src, tgt, srctotarget='translations.txt')
```

#### Batch Processing
```python
# Process in chunks to manage memory
for chunk in corpus_chunks:
    align_chunk(chunk)
    yield results
```

#### Error Handling
- **Missing translations**: Falls back to length-based
- **Malformed input**: Skips problematic sentences
- **MT API failures**: Retry logic needed (not built-in)

## Integration Patterns

### With Google Translate API
```python
from googletrans import Translator
from bleualign import align_documents

# Translate source to target
translator = Translator()
with open('source.txt') as f:
    translations = [translator.translate(line, dest='de').text
                    for line in f]

with open('translated.txt', 'w') as f:
    f.writelines(translations)

# Align
align_documents('source.txt', 'target.txt',
                srctotarget='translated.txt')
```

### With Local NMT
```bash
# Using fairseq or similar
fairseq-interactive data-bin \
  --path model.pt < source.txt > translations.txt

# Then bleualign
python -m bleualign source.txt target.txt \
  -s translations.txt -o aligned.txt
```

## Advanced Techniques

### Two-Way Alignment
```python
# Align both directions and intersect
align_src_to_tgt = align_documents(src, tgt, srctotarget=trans_st)
align_tgt_to_src = align_documents(tgt, src, srctotarget=trans_ts)

# Keep only mutual alignments (high precision)
mutual = intersect(align_src_to_tgt, align_tgt_to_src)
```

### Confidence Filtering
```python
# Bleualign doesn't output scores directly, but can be added
for src, tgt, bleu_score in alignments_with_scores:
    if bleu_score > threshold:
        print(src, tgt)
```

### Hybrid Pipeline
```
1. Hunalign (fast, first pass)
2. Extract low-confidence pairs (score < 0.3)
3. Bleualign on low-confidence subset (accurate)
4. Merge results
```

## Cost Analysis (MT APIs)

### Google Translate Pricing
- **$20/million characters**
- Example: 100K sentences × 50 chars avg = 5M chars = **$100**

### DeepL Pricing
- **$25/million characters** (better quality)
- Same corpus: **$125**

### Local NMT
- **Hardware**: GPU ($500-$2000)
- **Electricity**: Negligible for one-time use
- **Break-even**: ~5-10M sentences vs. API costs

## References

- [Bleualign GitHub](https://github.com/rsennrich/Bleualign)
- [Rico Sennrich's Paper](https://aclanthology.org/E12-1021/)
- [BLEU Metric](https://aclanthology.org/P02-1040/)
- [Sentence-Level BLEU](https://www.nltk.org/api/nltk.translate.bleu_score.html)
