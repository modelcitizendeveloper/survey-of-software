# S2 Recommendation: Algorithm-Driven Selection

## Match Algorithm to Technical Constraints

After understanding HOW each algorithm works, select based on your system's limiting constraint:

## By Primary Bottleneck

### CPU Cycles (Need Speed)

**Large alphabet + single pattern**:
→ **Boyer-Moore** (sublinear O(n/m), 1-2 GB/s typical)

**Small alphabet + single pattern**:
→ **KMP** (linear O(n) but no bad-char advantage for BM)

**Multiple patterns**:
→ **Aho-Corasick** (O(n) regardless of pattern count)

**Extreme performance (>10 GB/s)**:
→ **Hyperscan** (SIMD + DFA optimization)

### Memory (RAM Constrained)

**Absolute minimum O(1)**:
→ **Naive** or **Rabin-Karp** (no auxiliary structures)

**Small O(m)**:
→ **KMP** (only failure function array)

**Moderate O(m + σ)**:
→ **Boyer-Moore** (pattern + alphabet tables)

**Large O(m × σ) OK**:
→ **Aho-Corasick** (trie structure)

### Predictability (Real-Time Systems)

**Hard real-time (must guarantee latency)**:
→ **KMP** (O(n) worst case, no surprises)

**Soft real-time (tolerates occasional spike)**:
→ **Boyer-Moore** (O(nm) worst case rare in practice)

**No guarantees needed**:
→ **Rabin-Karp** (probabilistic, hash collisions unpredictable)

### Implementation Time (Development Speed)

**Minutes**:
→ **Naive** (3-5 lines of code)

**Hours**:
→ **Rabin-Karp** (rolling hash logic ~50 lines)

**Days**:
→ **KMP** (failure function construction subtle)

**Weeks**:
→ **Boyer-Moore** (good suffix rule complex)
→ **Aho-Corasick** (trie + failure links + output links)

## By Alphabet Size

### Binary (0/1, Yes/No)

**Characteristics**: σ=2, highly repetitive
**Best**: KMP or specialized bitwise algorithms
**Avoid**: Boyer-Moore (bad-char rule ineffective with σ=2)

### DNA/RNA (A,C,G,T/U)

**Characteristics**: σ=4, biological patterns
**Best**: KMP or Two-Way (linear guaranteed, small alphabet)
**Alternative**: Specialized bioinformatics tools (BLAST, Bowtie)
**Avoid**: Boyer-Moore (marginal advantage with σ=4)

### English Text (a-z, A-Z)

**Characteristics**: σ≈52 + punctuation ≈ 100
**Best**: Boyer-Moore (large skips on mismatch)
**Alternative**: KMP if worst-case matters
**Multi-pattern**: Aho-Corasick

### Byte Strings (0-255)

**Characteristics**: σ=256, typical for binary data
**Best**: Boyer-Moore (excellent bad-char skipping)
**Library**: Use optimized stdlib (memmem, std::string::find)

### Unicode (65,536 code points)

**Characteristics**: σ=65K, sparse usage
**Challenge**: BM/AC tables huge if dense
**Solutions**:
- Byte-level matching (UTF-8 bytes, σ=256)
- Sparse tables (hash maps instead of arrays)
- Character-level with careful implementation
**Best**: Depends on pattern density and encoding

## By Pattern Characteristics

### Highly Repetitive ("AAAAAAB", "abcabcabc")

**Problem**: Naive and BM can be slow (many partial matches)
**Best**: KMP (designed for repetition via failure function)
**Also good**: Aho-Corasick (handles repetition well)

### Unique Characters ("WXYZ", "unique")

**Advantage**: Mismatches likely on first comparison
**Best**: Boyer-Moore (large skips when mismatch early)
**Also good**: Naive (few partial matches anyway)

### Very Short (< 5 characters)

**Reality**: Preprocessing overhead matters
**Best**: Naive or optimized stdlib (memchr for single char)
**Reason**: Constant factors dominate, simple code wins

### Very Long (> 1000 characters)

**Consideration**: String comparison cost on match
**Best**: Usually Boyer-Moore or KMP
**Watch out**: Rabin-Karp verification expensive on hash collision

## By Text Characteristics

### Streaming (Can't Buffer)

**Requirement**: Process as it arrives, no backtracking
**Best**: KMP or Aho-Corasick (never backtrack in text)
**Avoid**: Boyer-Moore (may examine positions out of order)
**Use case**: Network packets, log tails, stdin

### Static (Index Once, Search Many Times)

**Different paradigm**: Preprocess text, not patterns
**Best**: Suffix tree/array (not covered here, different problem)
**Examples**: Genome databases, document search engines

### Random vs Structured

**Random text**: All algorithms perform near average case
**Highly structured** (logs, code): May hit worst cases more often
- Logs often repetitive → KMP safer than BM
- Code has varied tokens → BM often fine

## By Performance Requirement

### Interactive (<100ms latency)

**Use case**: Text editor Find, browser Ctrl+F
**Best**: Boyer-Moore or well-optimized stdlib
**Why**: Average case fast enough, preprocessing negligible
**Alternative**: Naive (patterns short, text small)

### Batch Processing (Throughput Matters)

**Use case**: Process GB of logs, scan files
**Best**: Depends on pattern count
- Single: Boyer-Moore
- Multiple: Aho-Corasick

### Real-Time Streaming (Sustained Rate)

**Use case**: IDS, live log analysis
**Best**: Aho-Corasick or Hyperscan
**Why**: Must handle continuous stream at wire speed

### Ultra-High Throughput (>10 GB/s)

**Use case**: 10+ Gbps network, in-memory databases
**Best**: Hyperscan (SIMD + highly optimized)
**Alternative**: Custom FPGA/ASIC implementation

## Implementation Quality Matters

### Library vs Hand-Rolled

**Reality**: Well-optimized library naive > Hand-rolled KMP

**Examples**:
- glibc memmem(): Two-Way algorithm (O(n), O(1) space)
- Python str.find(): Optimized BMH (~1-2 GB/s)
- Rust memchr: SIMD BMH (~5-10 GB/s)

**Recommendation**: Use stdlib/library unless:
- Specific algorithm needed (e.g., worst-case guarantee)
- Multiple patterns (stdlib usually single-pattern only)
- Extreme performance (custom SIMD/hardware)

### SIMD Matters

**Modern CPUs**: Can check 16-32 bytes in parallel
- SIMD naive can beat scalar KMP for short patterns
- SIMD BMH approaches Hyperscan performance

**Tools**:
- Intel AVX2/AVX-512
- ARM NEON
- Libraries: Hyperscan, Rust memchr, SIMD-everywhere

## Optimization Priority

### For Single Pattern:

1. **Use optimized library first** (strstr, str.find, memchr)
2. **If not fast enough**: Profile, identify bottleneck
3. **Consider algorithm switch**:
   - Stdlib naive → BM
   - BM struggling with repetition → KMP
4. **Low-level optimization**:
   - SIMD (check multiple positions)
   - Unroll loops
   - Tune cache usage

### For Multiple Patterns:

1. **< 10 patterns**: Try BM for each (simple, often fast enough)
2. **10-100 patterns**: Switch to Aho-Corasick
3. **100+ patterns**: Definitely Aho-Corasick or Hyperscan
4. **1000+ patterns**: Hyperscan if need high throughput

## Decision Table

| Scenario | Algorithm | Rationale |
|----------|-----------|-----------|
| Text editor Find | Boyer-Moore or stdlib | Interactive, varied patterns |
| grep one pattern | Boyer-Moore | Single pattern, need speed |
| grep multiple patterns | Aho-Corasick (or sequential BM) | Depends on count |
| Virus scanner (1M sigs) | Aho-Corasick or Hyperscan | Massive pattern set |
| Network IDS (10 Gbps) | Hyperscan | Extreme throughput |
| DNA sequence search | KMP or specialized | Small alphabet |
| Log analysis (keywords) | Aho-Corasick | Multiple patterns, streaming |
| Database LIKE query | Boyer-Moore (single pattern) | Typical use case |
| Real-time system | KMP | Worst-case guarantee |
| Memory-constrained device | Naive or Rabin-Karp | O(1) space |

## Benchmark Before Deploying

**Theory ≠ Practice**:
- Constant factors matter (100x difference possible)
- Cache behavior unpredictable from complexity
- SIMD can change everything
- Text characteristics affect performance

**How to benchmark**:
1. Use representative data (real text, real patterns)
2. Measure wall-clock time, not just comparisons
3. Test average case AND worst case
4. Profile memory usage AND throughput
5. Compare against stdlib baseline

## Key Takeaways

**No silver bullet**: Each algorithm optimizes different bottleneck

**Start simple**:
- Single pattern → Use stdlib (str.find, strstr)
- Multiple patterns (10+) → Aho-Corasick library

**Optimize when proven necessary**:
- Profile first (don't guess)
- Understand your bottleneck (CPU? Memory? Latency?)
- Match algorithm to constraint

**Modern reality**:
- SIMD matters more than algorithm choice (for short patterns)
- Library quality > algorithm choice (for medium patterns)
- Algorithm choice critical (only for many patterns or special constraints)

**Next**: See S3 for WHO needs these algorithms and WHY (use-case driven)
