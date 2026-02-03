# Algorithm Feature Comparison Matrix

## Complexity Comparison

| Algorithm | Preprocessing | Matching (Best) | Matching (Avg) | Matching (Worst) | Space |
|-----------|---------------|-----------------|----------------|------------------|-------|
| **Naive** | O(1) | O(n) | O(nm) | O(nm) | O(1) |
| **KMP** | O(m) | O(n) | O(n) | O(n) | O(m) |
| **Boyer-Moore** | O(m + σ) | O(n/m)* | O(n) | O(nm) | O(m + σ) |
| **Aho-Corasick** | O(Σm) | O(n + z) | O(n + z) | O(n + z) | O(Σm × σ) |
| **Rabin-Karp** | O(m) | O(n + m) | O(n + m) | O(nm) | O(1) |

*Sublinear: Boyer-Moore can skip characters
σ = alphabet size, Σm = sum of all pattern lengths, z = output size (number of matches)

## Characteristic Comparison

| Feature | Naive | KMP | Boyer-Moore | Aho-Corasick | Rabin-Karp |
|---------|-------|-----|-------------|--------------|------------|
| **Multiple patterns** | k × O(nm) | k × O(n) | k × O(n) | O(n + z) | O(n + km) |
| **Sublinear possible** | ❌ | ❌ | ✅ (O(n/m)) | ❌ | ❌ |
| **Text backtracking** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Cache-friendly** | ✅ | ✅ | ⚠️ (jumps) | ⚠️ (trie) | ✅ |
| **SIMD-friendly** | ✅ | ⚠️ | ✅ | ⚠️ | ✅ |
| **Implementation complexity** | Very Low | Medium | High | Very High | Low |
| **Worst-case guarantee** | ❌ | ✅ | ❌ | ✅ | ❌ |
| **Space efficient** | ✅ | ✅ | ✅ | ❌ | ✅ |

## Alphabet Size Impact

| Alphabet | Size | Naive | KMP | Boyer-Moore | Aho-Corasick | Rabin-Karp |
|----------|------|-------|-----|-------------|--------------|------------|
| **Binary** | 2 | Slow | Good | Poor | Good | Good |
| **DNA** | 4 | Slow | Good | Medium | Good | Good |
| **English** | 26 | Slow | Good | Excellent | Good | Good |
| **ASCII** | 128 | Slow | Good | Excellent | Good | Good |
| **Unicode** | 65K | Slow | Good | ⚠️ (space)* | ⚠️ (space)* | Good |

*Large alphabet: BM/AC need sparse structures (hash tables), reducing performance advantage

## Pattern Characteristics

### Repetitive Patterns (e.g., "AAAAAAB")

| Algorithm | Performance | Notes |
|-----------|-------------|-------|
| **Naive** | Poor | O(nm) worst case likely |
| **KMP** | Excellent | Designed for this case |
| **Boyer-Moore** | Poor | Worst case O(nm) |
| **Aho-Corasick** | Excellent | Handles repetition well |
| **Rabin-Karp** | Medium | Hash collisions likely |

### Unique-Character Patterns (e.g., "WXYZ")

| Algorithm | Performance | Notes |
|-----------|-------------|-------|
| **Naive** | Medium | No benefit from uniqueness |
| **KMP** | Good | But no special advantage |
| **Boyer-Moore** | Excellent | Large skips on mismatch |
| **Aho-Corasick** | Good | No special advantage |
| **Rabin-Karp** | Good | Fewer hash collisions |

## Use Case Suitability

| Use Case | Best Choice | Second Choice | Avoid |
|----------|-------------|---------------|-------|
| **Single pattern, large alphabet** | Boyer-Moore | KMP | Naive |
| **Single pattern, small alphabet** | KMP | Two-Way | Boyer-Moore |
| **Multiple patterns (10-100)** | Aho-Corasick | BM × k | Naive |
| **Multiple patterns (1000+)** | Aho-Corasick | Hyperscan | BM × k |
| **Streaming text** | KMP | Aho-Corasick | Boyer-Moore |
| **Interactive search** | Boyer-Moore | Naive (short) | Aho-Corasick |
| **Text editor** | Boyer-Moore | Naive | Aho-Corasick |
| **Virus scanner** | Aho-Corasick | Hyperscan | BM × k |
| **Worst-case guarantee** | KMP | Aho-Corasick | Boyer-Moore |
| **Minimal memory** | Naive | Rabin-Karp | Aho-Corasick |
| **Simple implementation** | Naive | Rabin-Karp | Aho-Corasick |

## Performance Characteristics

### Throughput (MB/s) - Typical

| Algorithm | Single Pattern | 100 Patterns | 10K Patterns |
|-----------|----------------|--------------|--------------|
| **Naive** | 100 MB/s | 1 MB/s | 0.01 MB/s |
| **KMP** | 500 MB/s | 5 MB/s | 0.05 MB/s |
| **Boyer-Moore** | 1-2 GB/s | 10-20 MB/s | 0.1-0.2 MB/s |
| **Aho-Corasick** | 500 MB/s | 500 MB/s | 500 MB/s |
| **Rabin-Karp** | 300 MB/s | 200 MB/s | 50 MB/s |
| **Hyperscan** | 5-10 GB/s | 5-10 GB/s | 5-10 GB/s |

*Values approximate, depend on text characteristics, implementation, and hardware

### Memory Usage - Pattern Size m=100

| Algorithm | Single Pattern | 100 Patterns | 10K Patterns |
|-----------|----------------|--------------|--------------|
| **Naive** | 0 | 0 | 0 |
| **KMP** | 100 B | 10 KB | 1 MB |
| **Boyer-Moore** | ~400 B | 40 KB | 4 MB |
| **Aho-Corasick** | ~1 KB | 100 KB | 10 MB |
| **Rabin-Karp** | 8 B | 8 B | 8 B |

*Aho-Corasick memory highly dependent on prefix sharing

## Practical Decision Matrix

### Primary Constraint: Speed

**Need sublinear performance?**
- **Yes, single pattern** → Boyer-Moore
- **Yes, multiple patterns** → Commentz-Walter (complex) or Hyperscan
- **No, just fast linear** → KMP or Aho-Corasick

### Primary Constraint: Simplicity

**Complexity tolerance?**
- **Very low** → Naive (or stdlib like strstr)
- **Low** → Rabin-Karp
- **Medium** → KMP
- **High** → Boyer-Moore
- **Very high** → Aho-Corasick

### Primary Constraint: Memory

**Memory limit?**
- **Extreme (O(1))** → Naive or Rabin-Karp
- **Low (O(m))** → KMP
- **Medium (O(m + σ))** → Boyer-Moore
- **Flexible** → Aho-Corasick

### Primary Constraint: Predictability

**Need worst-case guarantees?**
- **Yes, hard real-time** → KMP (O(n) guaranteed)
- **Yes, with multiple patterns** → Aho-Corasick (O(n + z) guaranteed)
- **No, average case OK** → Boyer-Moore (fastest in practice)

## Algorithm Selection Flowchart

```
How many patterns?
├─ ONE
│  ├─ Need worst-case guarantee? → KMP
│  ├─ Small alphabet (DNA)? → KMP or Two-Way
│  └─ Otherwise → Boyer-Moore
│
├─ FEW (2-10)
│  ├─ Patterns short? → Run BM for each
│  └─ Patterns long? → Aho-Corasick
│
├─ MANY (10-1000)
│  └─ Aho-Corasick
│
└─ MASSIVE (1000+)
   ├─ Need ultra-high performance? → Hyperscan
   └─ Otherwise → Aho-Corasick
```

## Advanced Considerations

### Hardware Acceleration

| Algorithm | SIMD | GPU | FPGA | Best For |
|-----------|------|-----|------|----------|
| **Naive** | ✅ Easy | ✅ Easy | ✅ Easy | Highly parallel |
| **KMP** | ⚠️ Medium | ⚠️ Medium | ✅ Good | Regular structure |
| **Boyer-Moore** | ✅ Good | ⚠️ Medium | ✅ Good | Character skipping |
| **Aho-Corasick** | ✅ Good | ✅ Good | ✅ Excellent | State machine |
| **Rabin-Karp** | ✅ Good | ✅ Excellent | ⚠️ Medium | Hash parallelism |

### Parallelization

| Algorithm | Thread Parallelism | Data Parallelism | Notes |
|-----------|-------------------|------------------|-------|
| **Naive** | Easy (split text) | Easy (SIMD) | Embarrassingly parallel |
| **KMP** | Medium (overlap) | Hard | Sequential dependencies |
| **Boyer-Moore** | Medium (overlap) | Medium (SIMD) | Large skips complicate |
| **Aho-Corasick** | Easy (split text) | Medium | State machine parallelizable |
| **Rabin-Karp** | Easy (split text) | Easy (SIMD) | Hash computation parallel |

### Cache Behavior

| Algorithm | Access Pattern | Cache Friendliness | Notes |
|-----------|----------------|-------------------|-------|
| **Naive** | Sequential | Excellent | Predictable prefetch |
| **KMP** | Sequential text, random pattern | Good | Failure function small |
| **Boyer-Moore** | Large jumps | Medium | Skip = bad prefetch |
| **Aho-Corasick** | Sequential text, random trie | Medium | Trie can be large |
| **Rabin-Karp** | Sequential | Excellent | Arithmetic only |

## Key Insights

### No Universal Winner

**Every algorithm optimizes different bottleneck**:
- Naive: Simplicity
- KMP: Worst-case time
- Boyer-Moore: Average-case time (sublinear)
- Aho-Corasick: Multiple patterns
- Rabin-Karp: Space efficiency + simplicity

### Alphabet Size is Critical

**Small alphabet (2-4)**:
- BM bad-character rule ineffective
- KMP competitive or better
- AC remains strong for multi-pattern

**Large alphabet (256+)**:
- BM dominates single-pattern
- AC trie becomes sparse (use hash tables)

### Pattern Count Matters Most

**1 pattern**: BM wins (sublinear)
**2-10 patterns**: Toss-up (BM × k vs AC)
**10+ patterns**: AC wins decisively
**1000+ patterns**: AC or Hyperscan (no alternative)

### Real-World != Theory

**Practical factors**:
- Constant factors matter (SIMD, cache, branch prediction)
- Modern CPUs: Naive with SIMD can beat KMP for short patterns
- Implementation quality: Well-tuned BM >> Naive AC

**Benchmarking essential**: Theoretical complexity doesn't always predict real performance
