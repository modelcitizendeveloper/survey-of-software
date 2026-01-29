# vecalign: Comprehensive Analysis

## Algorithm Deep Dive

### Embedding-Based Alignment
vecalign uses dense vector representations (LASER embeddings) to capture semantic similarity:
1. **Encode sentences** in both languages to fixed-size vectors (1024-dim)
2. **Compute similarity matrix** using cosine similarity
3. **Dynamic programming search** for best alignment path
4. **Support variable-length alignments** (1-to-N, N-to-M)

### Mathematical Model
```
Score(alignment) = Σ cosine_similarity(embed(src[i]), embed(tgt[j]))

Where:
- embed(): LASER multilingual encoder
- Vectors share same semantic space across 93 languages
```

### LASER Embeddings
- **Multilingual**: Single encoder for 93 languages
- **Sentence-level**: Fixed 1024-dimensional vectors
- **Transfer learning**: Trained on large-scale parallel data
- **Language-agnostic**: No language-specific preprocessing needed

### Search Strategy
- **Full DP**: O(n × m) with configurable constraints
- **Max alignment size**: Limits N-to-M complexity (default: 8)
- **Overlap penalty**: Discourages overlapping alignments
- **Cost matrix**: Precomputed similarity scores

## Parameter Tuning

### Key Parameters
```bash
# Maximum alignment size (N-to-M)
--alignment_max_size 8  # Allow up to 8 sentences on either side

# Neighborhood search window
--neighborhood 5  # Only consider alignments within ±5 positions

# Overlap penalty
--overlap_penalty 0.1  # Penalize overlapping alignments

# Minimum similarity threshold
--min_sim 0.3  # Ignore pairs below this cosine similarity
```

### Alignment Size Impact
| Max Size | Precision | Recall | Speed | Use Case |
|----------|-----------|--------|-------|----------|
| 2 | 96% | 88% | Fast | Clean 1-to-1 texts |
| 4 | 95% | 92% | Medium | Typical parallel data |
| 8 | 93% | 96% | Slow | Complex alignments |
| 16 | 91% | 98% | Very Slow | Messy comparables |

### Embedding Parameters
```bash
# LASER encoder language
--src_lang en
--tgt_lang de

# Embedding dimension (fixed at 1024 for LASER)
# GPU memory usage
--batch_size 32  # Larger = faster but more memory
```

## Performance Characteristics

### Benchmarks (Different Hardware)
| Hardware | Embed Speed | Align Speed | Total (100K pairs) |
|----------|-------------|-------------|---------------------|
| CPU (16-core) | 1K sent/s | 5K pairs/s | ~30 minutes |
| GPU (V100) | 10K sent/s | 5K pairs/s | ~3 minutes |
| GPU (A100) | 20K sent/s | 5K pairs/s | ~2 minutes |

*Embedding is the bottleneck on CPU; alignment on GPU*

### Memory Requirements
| Corpus Size | Embeddings | Similarity Matrix | Peak RAM |
|-------------|------------|-------------------|----------|
| 10K sentences | 40MB | 400MB | 500MB |
| 100K sentences | 400MB | 40GB | 50GB |
| 1M sentences | 4GB | 4TB | N/A* |

*Large corpora require chunking or sparse matrices*

### Scaling Strategy
```bash
# Process in chunks for large corpora
split -l 50000 source.txt src_chunk_
split -l 50000 target.txt tgt_chunk_

# Embed chunks (can be parallelized)
for chunk in src_chunk_*; do
    embed_chunk $chunk
done

# Align chunks independently
for i in {1..N}; do
    vecalign src_chunk_$i tgt_chunk_$i
done
```

## Edge Cases & Failure Modes

### When vecalign Excels

#### 1. Low-Resource Language Pairs
```
Source: Swahili
Target: Tamil
→ No dictionary or MT available; vecalign still works via shared embedding space
```

#### 2. Noisy Web Text
```
Source: "ur website iz awesome!!!"
Target: "Votre site web est génial !"
→ Embeddings capture meaning despite informal spelling
```

#### 3. Domain Shifts
```
Source: Medical jargon
Target: Medical jargon (different language)
→ LASER trained on diverse domains; handles terminology
```

### When vecalign Struggles

#### 1. Very Short Sentences
```
Source: "OK."
Target: "D'accord."
→ Embeddings less reliable for 1-2 word sentences
```
**Mitigation**: Combine with length-based prior

#### 2. Code-Switching
```
Source: "Let's go to the store."
Target: "Vamos al store." (Spanish + English)
→ Mixed-language embeddings can be noisy
```

#### 3. Extremely Long Documents
```
100K+ sentence pairs without chunking
→ Memory explosion from similarity matrix
```
**Mitigation**: Always chunk large corpora

## Quality Metrics

### Published Benchmarks (WMT Testsets)
| Language Pair | Precision | Recall | F1 | vs Hunalign | vs Bleualign |
|---------------|-----------|--------|-------|-------------|--------------|
| EN-DE | 98.5% | 97.8% | 98.1% | +3% | +1% |
| EN-FR | 98.2% | 97.5% | 97.8% | +2% | +0.5% |
| EN-ZH | 96.1% | 94.7% | 95.4% | +8% | +3% |
| EN-AR | 94.3% | 92.8% | 93.5% | +10% | +5% |

**Key insight**: Biggest gains on distant language pairs

### Corpus Type Impact
| Corpus Type | F1 Score | Notes |
|-------------|----------|-------|
| News (clean) | 98% | Excellent |
| Parliamentary | 97% | Very good |
| Web forums | 94% | Handles noise well |
| Literary | 91% | Struggles with creative translation |
| Technical docs | 98% | Excellent on terminology |

## Implementation Details

### Language & Dependencies
- **Python 3.6+**
- **PyTorch**: For LASER encoder
- **NumPy**: Matrix operations
- **Faiss** (optional): Fast similarity search for large corpora

### Installation Footprint
```
Total size: ~1.5 GB
- LASER models: 1.2 GB
- PyTorch: 200 MB
- Other dependencies: 100 MB
```

### GPU Utilization
```python
# Check GPU usage
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))

# vecalign automatically uses GPU if available
# Force CPU mode:
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

### Extensibility
- **Custom embeddings**: Can substitute LASER with other encoders
- **Custom scoring**: Modify similarity function
- **Custom search**: Override DP algorithm

## Integration Patterns

### End-to-End Pipeline
```bash
#!/bin/bash
# Complete vecalign workflow

# 1. Download LASER models (once)
bash download_models.sh

# 2. Extract embeddings
python3 embed.py \
  --text source.txt \
  --lang en \
  --output source.emb

python3 embed.py \
  --text target.txt \
  --lang de \
  --output target.emb

# 3. Align
python3 vecalign.py \
  --src source.txt \
  --tgt target.txt \
  --src_embed source.emb \
  --tgt_embed target.emb \
  --alignment_max_size 4 \
  > aligned.txt
```

### With Pre-Computed Embeddings (Reuse)
```bash
# Embed once
embed_corpus source.txt > source.emb

# Align multiple times with different parameters
vecalign --src_embed source.emb --tgt_embed target.emb --max_size 2
vecalign --src_embed source.emb --tgt_embed target.emb --max_size 8
# Embeddings are reused (fast iteration)
```

### Batch Processing for Production
```python
import subprocess
import multiprocessing as mp

def align_chunk(src_chunk, tgt_chunk):
    # Embed
    subprocess.run(['python3', 'embed.py', '--text', src_chunk, ...])
    # Align
    subprocess.run(['python3', 'vecalign.py', ...])
    return results

# Parallel processing
with mp.Pool(4) as pool:
    results = pool.starmap(align_chunk, chunk_pairs)
```

## Advanced Techniques

### Confidence Scoring
vecalign doesn't output confidence scores by default, but you can add:
```python
# Modify vecalign.py to output similarity scores
for src_idx, tgt_idx in alignments:
    score = cosine_similarity(src_emb[src_idx], tgt_emb[tgt_idx])
    print(src_idx, tgt_idx, score)
```

### Hybrid Ensemble
```
1. Run hunalign (fast, first pass)
2. Run vecalign (accurate, second pass)
3. Keep hunalign results where both agree (high confidence)
4. Use vecalign results where they disagree (trust accuracy)
```

### Multilingual Corpus Mining
```python
# Use vecalign to find parallel sentences in comparable corpora
# (not pre-aligned)

# 1. Embed all sentences in both languages
# 2. Find nearest neighbors in embedding space
# 3. Filter by similarity threshold
# 4. Run vecalign on candidate pairs
```

### Fine-Tuning LASER
Advanced users can fine-tune LASER embeddings on domain-specific data:
```
1. Collect domain-specific parallel corpus
2. Fine-tune LASER encoder (requires LASER training code)
3. Export fine-tuned model
4. Use with vecalign for improved domain accuracy
```

## Production Deployment

### Docker Container
```dockerfile
FROM pytorch/pytorch:latest

RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/thompsonb/vecalign
RUN cd vecalign && pip install -r requirements.txt
RUN bash download_models.sh

ENTRYPOINT ["python3", "vecalign.py"]
```

### REST API Wrapper
```python
from flask import Flask, request
import vecalign

app = Flask(__name__)

@app.route('/align', methods=['POST'])
def align():
    src = request.json['source']
    tgt = request.json['target']
    # Run vecalign
    result = vecalign.align(src, tgt)
    return {'alignments': result}
```

## References

- [vecalign GitHub](https://github.com/thompsonb/vecalign)
- [vecalign Paper](https://aclanthology.org/D19-1136/)
- [LASER: Language-Agnostic SEntence Representations](https://github.com/facebookresearch/LASER)
- [LASER Paper](https://aclanthology.org/P19-1309/)
- [Massively Multilingual Sentence Embeddings](https://arxiv.org/abs/1812.10464)
