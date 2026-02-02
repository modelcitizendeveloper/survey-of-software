# S2 Recommendation: Technical Selection

## Algorithm-Driven Decision

### By Algorithmic Needs

**Need rule-based speed?**
→ Jieba (Dictionary + HMM)
- No neural network overhead
- O(n) complexity after DAG construction
- 400 KB/s throughput

**Need neural accuracy?**
→ PKUSEG (BiLSTM-CRF) or LAC (BiGRU-CRF)
- Sentence-level context
- Learned from training data
- F1 96% (PKUSEG) or 91% (LAC)

**Need subword flexibility?**
→ SentencePiece (Unigram LM)
- Probabilistic segmentation
- No linguistic assumptions
- Data-driven boundaries

### By Technical Constraints

**Memory < 200 MB?**
→ Jieba (~100 MB) or SentencePiece (~50 MB)

**Memory OK, need accuracy?**
→ PKUSEG (~300 MB) or transformers (~1-2 GB GPU)

**Need streaming?**
→ Jieba (sentence-by-sentence) or SentencePiece

**Batch processing?**
→ PKUSEG, LAC, or transformers (GPU batch)

### By Training Requirements

**No training capacity?**
→ Jieba (pre-trained) or LAC (pre-trained) or BERT (pre-trained)

**Can train on domain corpus?**
→ PKUSEG (custom training) or SentencePiece (corpus-specific)

**Need fine-tuning?**
→ transformers (HuggingFace ecosystem)

## Technical Trade-off Analysis

### Speed vs Accuracy
```
Jieba:     Fast (400 KB/s) → Low accuracy (F1 85%)
LAC:       Fast (800 QPS)  → High accuracy (F1 91%)
PKUSEG:    Medium (130 KB/s) → Highest accuracy (F1 96%)
transformers: Slow (20 KB/s) → State-of-art (F1 97%)
```

**Sweet spot**: LAC (best speed + accuracy)

### Context Window Impact
```
Local context (Jieba bigrams):
  "结婚的和尚未结婚的" → May fail on ambiguity

Sentence context (PKUSEG BiLSTM):
  Sees full sentence → Resolves ambiguity better

Full document (transformers):
  Beyond single sentence → Best for long-range dependencies
```

**Trade-off**: More context = better accuracy but slower

### OOV Handling Robustness
```
Dictionary-based (Jieba HMM):
  OOV "新词" → HMM tags → Moderate quality

Neural embeddings (PKUSEG/LAC):
  OOV "新词" → Learned context → Good quality

Subword (SentencePiece):
  OOV "新词" → Decompose to "新" + "词" → Always works
```

**Most robust**: SentencePiece (no true OOV)

## Implementation Patterns

### Pattern 1: Hybrid Pipeline
```python
# Fast first pass with Jieba
from jieba import cut
from pkuseg import pkuseg

def hybrid_segment(text):
    # Quick Jieba for known words
    jieba_words = cut(text)

    # PKUSEG for ambiguous passages
    if has_ambiguity(jieba_words):
        seg = pkuseg()
        return seg.cut(text)
    return jieba_words
```

### Pattern 2: Multi-Model Ensemble
```python
# Use multiple segmenters, vote on boundaries
def ensemble_segment(text):
    jieba_result = jieba.cut(text)
    pkuseg_result = pkuseg.cut(text)
    lac_result = lac.run(text)

    # Majority voting on word boundaries
    return vote(jieba_result, pkuseg_result, lac_result)
```

### Pattern 3: Fallback Chain
```python
# Try complex first, fallback to simple on error
def robust_segment(text):
    try:
        return transformers_tokenize(text)  # Best accuracy
    except MemoryError:
        return pkuseg_segment(text)  # Good accuracy
    except Exception:
        return jieba_segment(text)  # Always works
```

## Critical Technical Insights

### 1. Character Coverage for SentencePiece
```python
# WRONG: Default coverage
spm.train(vocab_size=32000)  # Bad for Chinese

# RIGHT: Explicit 0.9995
spm.train(vocab_size=32000, character_coverage=0.9995)  # Good
```

**Why**: Chinese has 20K+ common chars, needs high coverage

### 2. Batch Size Impact on Neural Models
```python
# Small batch: Underutilizes GPU
model.segment(texts, batch_size=1)  # Slow

# Optimal batch: 16-32 for most GPUs
model.segment(texts, batch_size=32)  # Fast
```

**Effect**: 10x speedup on GPU with proper batching

### 3. Dictionary Quality Dominates Jieba Performance
```python
# Poor dictionary: 85% accuracy
jieba.load_userdict("small_dict.txt")

# Rich domain dictionary: 92% accuracy
jieba.load_userdict("large_domain_dict.txt")
```

**Lesson**: Invest in dictionary if using Jieba in production

## Next Steps from S2

After understanding algorithms and trade-offs:
1. **Map to use case** → Read S3 for scenario-based selection
2. **Consider long-term** → Read S4 for strategic viability
3. **Validate empirically** → Test on your actual data

## Technical Bottom Line

**No universal winner** - each algorithm optimizes for different constraints:
- Jieba: Speed-optimized rule-based
- PKUSEG: Accuracy-optimized neural
- LAC: Balanced neural (speed + accuracy)
- SentencePiece: Flexibility-optimized subword
- transformers: State-of-art but resource-intensive

**Pick based on your bottleneck**: speed, accuracy, memory, or flexibility.
