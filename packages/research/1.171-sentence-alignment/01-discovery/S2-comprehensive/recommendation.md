# S2 Recommendation: Technical Decision Guide

## Architectural Tradeoffs

### Algorithm Comparison

| Dimension | Hunalign | Bleualign | vecalign |
|-----------|----------|-----------|----------|
| **Theoretical basis** | Statistical (length) | MT quality | Semantic embeddings |
| **Core assumption** | Length correlation | MT preserves meaning | Shared embedding space |
| **Language support** | Any | Any (with MT) | 93 languages (LASER) |
| **Resource requirements** | Dictionary (optional) | MT system (required) | GPU (recommended) |
| **Computational complexity** | O(n) | O(n×m) | O(n×m) + embedding |
| **Memory footprint** | Very low | Low | High (similarity matrix) |
| **Parallelizability** | Embarrassingly parallel | Parallel MT possible | GPU accelerated |
| **Failure mode** | Length divergence | Poor MT | Short sentences |

## When Each Algorithm Breaks Down

### Hunalign Failure Points
- **Paraphrases**: No semantic understanding
- **Literary translation**: Creative departures from literal meaning
- **Missing dictionary**: Accuracy drops significantly without lexical overlap

### Bleualign Failure Points
- **Low-resource MT**: Garbage-in, garbage-out
- **Cost at scale**: MT API costs can be prohibitive
- **Latency**: Translation adds significant overhead

### vecalign Failure Points
- **Memory constraints**: Similarity matrix for 100K+ sentences
- **Cold start**: Large model download, slow first run
- **Very short texts**: Embeddings less discriminative

## Parameter Tuning Decision Matrix

### Hunalign Parameters
```bash
# High precision (for training data)
hunalign -thresh=0.5 dict.txt src.txt tgt.txt

# Balanced (default use case)
hunalign -thresh=0.1 dict.txt src.txt tgt.txt

# High recall (for post-filtering)
hunalign -thresh=0 dict.txt src.txt tgt.txt
```

### Bleualign Parameters
- **max_skip**: Set based on expected divergence
  - Clean parallel: max_skip=2
  - Noisy web data: max_skip=5
- **smoothing**: method1 for most cases, method4 for very short sentences

### vecalign Parameters
- **alignment_max_size**:
  - 1-to-1 expected: max_size=2
  - Some merges/splits: max_size=4
  - Messy comparables: max_size=8+
- **min_sim**:
  - High precision: min_sim=0.5
  - Balanced: min_sim=0.3
  - High recall: min_sim=0.1

## Integration Patterns for Production

### Pattern 1: Pipeline Ensemble (Best Quality)
```
Input corpus
    ↓
[Hunalign: fast pass]
    ↓
Partition by confidence score
    ↓
├─ High confidence (>0.5) → Output
├─ Medium (0.2-0.5) → vecalign → Output
└─ Low (<0.2) → Manual review or discard
```

**Use case**: Building high-quality research corpora

### Pattern 2: Staged Refinement (Balanced)
```
Input corpus
    ↓
[Hunalign with dictionary]
    ↓
Extract high-confidence alignments as anchors
    ↓
[vecalign on remaining segments]
    ↓
Merge results
```

**Use case**: Large-scale MT data preparation with quality constraints

### Pattern 3: Parallel Alternatives (Speed vs. Quality Toggle)
```
         Input corpus
              ↓
        Branch by priority
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
[Hunalign]        [vecalign]
Fast mode         Quality mode
```

**Use case**: Interactive systems where user selects speed/quality tradeoff

### Pattern 4: Domain-Specific Hybrid
```
Medical corpus
    ↓
[Train domain-specific dictionary from terminology]
    ↓
[Hunalign with medical dictionary]
    ↓
Achieve 95%+ accuracy without ML overhead
```

**Use case**: Domain-specific corpora with strong terminology

## Quality Assurance Strategies

### Confidence Metrics
- **Hunalign**: Use alignment score column
- **Bleualign**: Add BLEU score output (requires modification)
- **vecalign**: Track cosine similarity per alignment

### Validation Workflow
```
1. Random sample 500 alignment pairs
2. Manual annotation (accept/reject)
3. Compute precision/recall
4. Tune threshold parameters
5. Re-align and re-evaluate
```

### Automatic Quality Checks
- **Length ratio**: Flag pairs with |len(src)/len(tgt)| > 3
- **Dictionary coverage**: Flag pairs with no dictionary overlap (hunalign)
- **Similarity score**: Flag pairs below minimum threshold
- **Sequence anomalies**: Flag large gaps in alignment sequence

## Cost-Benefit Analysis

### Scenario 1: Startup with Limited Resources
**Corpus**: 1M sentence pairs, European languages
**Budget**: Minimal
**Recommendation**: **Hunalign**
- Free, fast, good enough for many use cases
- Build dictionary from existing word lists
- **Expected quality**: 90% F1

### Scenario 2: Research Lab
**Corpus**: 500K pairs, diverse languages
**Budget**: Moderate (GPU available)
**Recommendation**: **vecalign**
- State-of-the-art results for publication
- GPU already available (no marginal cost)
- **Expected quality**: 96% F1

### Scenario 3: Enterprise MT Pipeline
**Corpus**: 10M+ pairs, high-quality needed
**Budget**: High
**Recommendation**: **Hybrid (hunalign + vecalign)**
- Hunalign for bulk (95% of data)
- vecalign for low-confidence subset (5% of data)
- **Expected quality**: 97% F1
- **Time**: 2 hours (vs. 20 hours for vecalign alone)

### Scenario 4: Low-Resource Language Pair
**Corpus**: 100K pairs, rare language
**Budget**: Moderate
**Recommendation**: **vecalign**
- No dictionary or MT available
- LASER supports 93 languages
- **Expected quality**: 93% F1 (even without resources)

## Edge Case Handling

### Problem: Very Long Documents
**Solution**: Chunk documents with overlap
```
1. Split into 10K sentence chunks
2. Add 100-sentence overlap between chunks
3. Align each chunk independently
4. Merge results, resolve overlaps
```

### Problem: Many-to-Many Alignments
**Solution**: Increase vecalign max_size
```bash
# Allow up to 16-sentence alignments
vecalign --alignment_max_size 16 ...
```

### Problem: Code-Switching or Mixed Languages
**Solution**: Pre-filter or post-filter
```
1. Detect language per sentence (langdetect)
2. Route to appropriate aligner
3. Or use vecalign (handles mixed gracefully)
```

### Problem: Extreme Length Divergence
**Example**: English "Yes." → Japanese long polite sentence
**Solution**: Bleualign or vecalign (hunalign will fail)

## Recommended Workflows by Corpus Type

### News Articles (Clean, Professional)
→ **Hunalign** (fast, accurate enough)

### Web Forums (Noisy, Informal)
→ **vecalign** (handles typos, informal language)

### Legal/Technical Documents (Literal Translation)
→ **Hunalign with domain dictionary** (near-perfect results)

### Literary Translation (Creative, Paraphrased)
→ **vecalign** or **bleualign** (semantic understanding needed)

### Low-Resource Languages
→ **vecalign** (no alternatives)

### Multi-Domain Mixed Corpus
→ **Hybrid ensemble** (per-domain routing)

## Next Steps

- **S3 (Need-Driven)**: Concrete implementation workflows for common use cases
- **S4 (Strategic)**: Long-term maintenance, scaling strategies, team decisions
