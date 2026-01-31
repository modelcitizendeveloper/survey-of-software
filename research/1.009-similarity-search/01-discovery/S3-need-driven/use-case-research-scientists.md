# Use Case: Research Data Scientists

## Who Needs This

**User Persona:** Academic and industrial researchers experimenting with similarity search algorithms

**Context:**
- Benchmark new algorithms (compare against SOTA baselines)
- Prototype novel similarity metrics (custom distance functions)
- Research applications (genomics, chemistry, astronomy)
- Scale: 100K to 1B vectors (benchmark datasets)
- Latency: Not critical (offline experimentation)

**Examples:**
- ML researchers benchmarking new quantization methods
- Bioinformaticians searching protein/gene databases
- Chemists finding similar molecular structures
- Computer vision researchers on large-scale image retrieval
- NLP scientists evaluating embedding quality

## Why They Need Similarity Search

**Problem:** Need flexible, well-documented libraries to:
1. **Benchmark:** Compare novel methods against established baselines (FAISS, Annoy, ScaNN)
2. **Prototype:** Test new ideas quickly without reimplementing infrastructure
3. **Reproduce:** Replicate published results from papers

**Critical requirements:**
- **Flexibility:** Support custom metrics, index types
- **Accuracy:** SOTA baselines for fair comparison
- **Documentation:** Clear API, reproducible examples
- **Performance profiling:** Understand algorithm bottlenecks

## Requirements Breakdown

### Must-Have
- ✅ SOTA baselines (HNSW, PQ, LSH for benchmarking)
- ✅ Well-documented APIs (Python preferred)
- ✅ Reproducibility (deterministic builds, versioned releases)
- ✅ Flexible metrics (Euclidean, cosine, custom)

### Nice-to-Have
- 🟡 GPU support (accelerate experiments)
- 🟡 Profiling tools (measure index build/query time)
- 🟡 Standard benchmarks (ann-benchmarks compatibility)
- 🟡 Open-source (inspect/modify internals)

### Can Compromise
- ⚠️ Production-readiness (research code, not deployed services)
- ⚠️ Real-time latency (batch experiments overnight)
- ⚠️ Scalability (small datasets OK for proofs-of-concept)

## Library Recommendations by Research Goal

### Benchmarking Novel Algorithms: FAISS + ScaNN

**Why FAISS:**
- **SOTA baseline:** IVF+PQ, HNSW are gold standards
- **ann-benchmarks compatible:** Fair comparisons with other libraries
- **Flexible:** Composable indexes (test IVF+PQ+HNSW combinations)
- **Widely cited:** Papers benchmark against FAISS

**Why ScaNN:**
- **SOTA accuracy:** Anisotropic quantization (best for MIPS)
- **Recent innovations:** SOAR algorithm (Dec 2025), cutting-edge
- **Google Research:** Access to latest research

**Workflow:**
```
1. Implement novel algorithm (custom index)
2. Benchmark against FAISS (IVF, PQ, HNSW)
3. Benchmark against ScaNN (anisotropic quantization)
4. Report recall@K vs QPS on standard datasets (SIFT1M, glove-100-angular)
5. Publish results (cite FAISS/ScaNN papers)
```

**Standard datasets (ann-benchmarks):**
- SIFT1M: 1M vectors, 128-dim (image features)
- glove-100-angular: 1.2M vectors, 100-dim (word embeddings)
- deep1B: 1B vectors, 96-dim (billion-scale)

### Prototyping Custom Metrics: FAISS (with custom IndexFlat)

**Why FAISS:**
- **Extensible:** C++ core, easy to add custom distance metrics
- **GPU acceleration:** Test ideas at scale
- **Python bindings:** Rapid prototyping

**Example: Custom metric (Mahalanobis distance)**
```cpp
// Extend IndexFlat with custom distance
class IndexFlatMahalanobis : public IndexFlat {
    Matrix covariance_inv;
    float distance(const float* x, const float* y) override {
        // Implement (x-y)^T Σ^-1 (x-y)
    }
};
```

**Use case:** Test new distance functions before implementing optimized index

### Probabilistic Algorithms Research: datasketch

**Why datasketch:**
- **LSH theory:** Standard implementation of MinHash, SimHash, LSH Forest
- **Pure Python:** Easy to read/modify source code
- **Pedagogical:** Good for teaching LSH concepts

**Use case examples:**
- Compare MinHash variants (b-bit MinHash, weighted MinHash)
- Test novel LSH families (learned hash functions)
- Reproduce LSH papers (classic algorithms well-documented)

### Specialized Domains: Custom Libraries + FAISS Backend

**Genomics:** Protein/gene similarity
- **Library:** BLAST (biology-specific), then FAISS for embedding-based
- **Metric:** Edit distance → embed sequences → FAISS cosine

**Chemistry:** Molecular similarity
- **Library:** RDKit (molecular fingerprints), then FAISS for search
- **Metric:** Tanimoto similarity → embed Morgan fingerprints → FAISS

**Astronomy:** Star catalog search
- **Library:** Astropy (celestial coordinates), then FAISS for k-NN
- **Metric:** Angular separation → embed RA/Dec → FAISS

## Real-World Example: Benchmarking Novel Quantization

**Scenario:** PhD student proposes new quantization method, compare vs FAISS PQ

**Hypothesis:** Adaptive quantization (cluster-aware codebooks) beats standard PQ

**Experiment:**
1. **Dataset:** SIFT1M (1M vectors, 128-dim)
2. **Baselines:**
   - FAISS PQ (m=8, nbits=8)
   - FAISS HNSW (M=32)
3. **Novel method:** Adaptive PQ (implement in Python, index in FAISS)
4. **Metrics:**
   - Recall@10 (accuracy)
   - QPS (speed)
   - Memory (bytes per vector)

**Results table (for paper):**

| Method | Recall@10 | QPS | Memory |
|--------|-----------|-----|--------|
| FAISS Flat | 100% | 150 | 512 bytes |
| FAISS PQ | 93% | 12000 | 8 bytes |
| FAISS HNSW | 99% | 6000 | 600 bytes |
| **Adaptive PQ (ours)** | **95%** | **10000** | **10 bytes** |

**Conclusion:** Adaptive PQ achieves +2% recall vs standard PQ at 83% QPS

### Publication Checklist
- [ ] Compare against FAISS/ScaNN (standard baselines)
- [ ] Report on ann-benchmarks datasets (reproducibility)
- [ ] Publish code + trained indexes (open science)
- [ ] Cite FAISS/ScaNN papers

## Common Research Pitfalls

### Pitfall 1: Comparing Against Weak Baselines
**Problem:** Benchmarking against Annoy (93% recall) when FAISS HNSW achieves 99%
**Solution:** Always include SOTA baselines (FAISS HNSW, ScaNN for MIPS)

### Pitfall 2: Not Using Standard Benchmarks
**Problem:** Custom dataset, results not comparable to published work
**Solution:** Use ann-benchmarks datasets (SIFT1M, glove, deep1B)

### Pitfall 3: Cherry-Picking Metrics
**Problem:** Reporting only QPS (not recall), or only recall (not memory)
**Solution:** Report recall@K, QPS, memory, build time (complete picture)

### Pitfall 4: Ignoring Reproducibility
**Problem:** Code not released, results can't be replicated
**Solution:** Publish code, random seeds, hyperparameters, trained indexes

## Tools for Research

### ann-benchmarks (Standard Benchmark Suite)
- **URL:** github.com/erikbern/ann-benchmarks
- **Datasets:** 20+ standard datasets (SIFT, glove, NYTimes, etc.)
- **Libraries:** Pre-configured FAISS, Annoy, ScaNN, HNSW, etc.
- **Visualization:** Recall vs QPS plots

**Usage:**
```bash
python run.py --dataset glove-100-angular --algorithm faiss-ivf
python plot.py --dataset glove-100-angular
```

**Output:** Pareto frontier (recall vs QPS), compare algorithms

### Profiling Tools
```python
import time
import faiss

# Build profiling
start = time.time()
index.train(vectors)
index.add(vectors)
build_time = time.time() - start

# Query profiling
start = time.time()
for query in queries:
    index.search(query, k=10)
qps = len(queries) / (time.time() - start)
```

### Memory Profiling
```python
import resource

# Measure RSS (resident set size)
mem_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
index = faiss.read_index("large_index.faiss")
mem_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

memory_mb = (mem_after - mem_before) / 1024
```

## Paper-Writing Guidance

### Experimental Section Structure
```
1. Datasets: SIFT1M (1M, 128-dim), glove-100 (1.2M, 100-dim)
2. Baselines: FAISS (IVF+PQ, HNSW), ScaNN (anisotropic)
3. Metrics: Recall@10, QPS, memory, build time
4. Implementation: Python 3.10, FAISS 1.13.2, NVIDIA A100
5. Results: Table + Pareto frontier plot
6. Analysis: Why our method outperforms baselines
```

### Citation Best Practices
```
FAISS:
@article{johnson2019billion,
  title={Billion-scale similarity search with {GPU}s},
  author={Johnson, Jeff and Douze, Matthijs and J{\'e}gou, Herv{\'e}},
  journal={IEEE Transactions on Big Data},
  year={2019}
}

ScaNN:
@inproceedings{guo2020accelerating,
  title={Accelerating large-scale inference with anisotropic vector quantization},
  author={Guo, Ruiqi and Sun, Philip and Lindgren, Erik and Geng, Quan and Simcha, David and Chern, Felix and Kumar, Sanjiv},
  booktitle={ICML},
  year={2020}
}
```

## Validation Checklist

Before submitting research paper:
- [ ] Benchmark on ≥2 standard datasets (ann-benchmarks)
- [ ] Compare against FAISS (IVF+PQ, HNSW) and ScaNN
- [ ] Report recall@10, QPS, memory, build time
- [ ] Publish code + hyperparameters (GitHub)
- [ ] Include Pareto frontier plot (recall vs QPS)
- [ ] Cite FAISS/ScaNN/Annoy papers

## Library Comparison for Research

| Library | Best For | Pros (Research) | Cons (Research) |
|---------|----------|-----------------|-----------------|
| **FAISS** | Benchmarking, baselines | SOTA, GPU, flexible | Complex API |
| **ScaNN** | MIPS research, accuracy | Cutting-edge, highest accuracy | Monorepo install |
| **Annoy** | Simplicity baseline | Easy to understand | Lower recall ceiling |
| **datasketch** | LSH research, set similarity | Pure Python, pedagogical | Limited to probabilistic |

**Recommendation:** Start with FAISS (most papers use it as baseline), add ScaNN for MIPS comparisons

## Related Research Areas

- **Learned indexes:** ML models as indexes (The Case for Learned Index Structures)
- **Graph-based search:** HNSW, NSW, DiskANN
- **Quantization:** PQ, OPQ, additive quantization
- **Hashing:** LSH, learning to hash, SimHash
