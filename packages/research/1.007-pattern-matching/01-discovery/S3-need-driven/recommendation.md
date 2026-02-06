# S3 Recommendation: Use-Case Driven Selection

## Match Solution to Your Scenario

After understanding WHO uses pattern matching and WHY, select based on your specific context:

## Quick Use-Case Lookup

| Your Situation | Primary Algorithm | Library/Tool | Why |
|----------------|-------------------|--------------|-----|
| **Text editor search** | Boyer-Moore | stdlib (str.find) | Interactive, patterns change frequently |
| **Network IDS (10K+ sigs)** | Aho-Corasick | Hyperscan | Multi-pattern, ultra-high throughput |
| **DNA sequence (exact)** | KMP or AC | biopython, SeqAn | Small alphabet, exact matches |
| **DNA alignment (NGS)** | BWT/FM-index | Bowtie2, BWA | Index genome, millions of reads |
| **Log analysis (keywords)** | Aho-Corasick | pyahocorasick, rg | Multiple keywords, streaming |
| **Log analysis (structured)** | Indexing | Elasticsearch, Splunk | Index once, query many times |

## By Persona

### Application Developer (Building UI/Tools)

**Your constraints**: Development speed, user experience, maintenance
**Your priority**: Simple, reliable, fast enough

**Recommendations**:
1. **Use stdlib first**: strstr(), std::string::find(), str.find()
   - Zero integration cost
   - Well-tested
   - Fast enough for typical use cases

2. **If stdlib too slow**: Profile before optimizing
   - Is it really the bottleneck?
   - Consider algorithm switch only if proven necessary

3. **For regex**: Use safe engines (RE2, Rust regex)
   - Avoid catastrophic backtracking
   - Linear-time guarantee critical for untrusted input

**Example**: Building text editor → Use stdlib unless profiling shows it's slow

### Security Engineer (Deploying IDS/DPI)

**Your constraints**: Throughput, accuracy, zero false negatives
**Your priority**: Keep up with network speed, detect all attacks

**Recommendations**:
1. **Use Hyperscan** (or Vectorscan for ARM)
   - Industry standard for IDS
   - Proven at scale (Snort, Suricata)
   - 10-100 GB/s throughput

2. **Don't roll your own**
   - Pattern matching is critical path
   - Use battle-tested implementations
   - Security bugs in custom code unacceptable

3. **Hardware acceleration** if needed
   - SmartNICs for >100 Gbps
   - FPGAs for ultra-low latency

**Example**: Deploying Snort → Use Hyperscan (built-in), don't replace it

### Bioinformatics Researcher

**Your constraints**: Accuracy, reproducibility, citations
**Your priority**: Correct results, established tools

**Recommendations**:
1. **Use domain-specific tools**
   - BWA/Bowtie2 for NGS alignment
   - BLAST for homology search
   - Don't use general string matching

2. **Understand biological context**
   - Small alphabet (σ=4) affects algorithm choice
   - Approximate matching essential (sequencing errors)
   - Index genome (static), not reads (dynamic)

3. **Prioritize accuracy over speed**
   - False negative = missed gene (unacceptable)
   - Slow search = wait longer (acceptable)

**Example**: RNA-seq analysis → Use STAR or Bowtie2 (established, cited)

### DevOps/SRE (Log Analysis)

**Your constraints**: Throughput, flexibility, cost
**Your priority**: Real-time alerts, ad-hoc queries

**Recommendations**:
1. **For interactive search**: Use ripgrep
   - 10x faster than grep
   - Supports regex
   - User-friendly

2. **For real-time monitoring**: Use ELK or similar
   - Index logs (Elasticsearch)
   - Query index (much faster than pattern matching)
   - Alerting built-in

3. **For keyword extraction**: Use Aho-Corasick
   - Stream logs (don't buffer)
   - Multiple keywords in one pass

**Example**: Monitor production logs → ELK stack with Grok patterns

## By Scale

### Small Scale (<1 MB, <10 patterns)

**Reality**: Almost anything works
**Recommendation**: Use simplest solution
- Naive might be fine
- Stdlib (strstr, str.find)
- Don't over-engineer

**Why**: Constant factors dominate, complexity not worth it

### Medium Scale (1-100 MB, 10-100 patterns)

**Reality**: Algorithm choice starts mattering
**Recommendation**:
- Single pattern: Boyer-Moore (stdlib)
- Multiple patterns: Aho-Corasick library

**Example**: Search 10 MB log file for 50 keywords → pyahocorasick

### Large Scale (>100 MB, 100+ patterns)

**Reality**: Performance critical
**Recommendation**:
- Multiple patterns: Definitely Aho-Corasick
- Consider distributed processing
- Index if possible (logs, documents)

**Example**: Process 1 GB/s stream with 10K patterns → Hyperscan

### Massive Scale (TB+, 1M+ patterns)

**Reality**: Specialized infrastructure needed
**Recommendation**:
- Hyperscan for pattern matching
- Distributed systems (Kafka, Flink)
- Hardware acceleration (FPGAs, SmartNICs)

**Example**: CloudFlare WAF (Tbps aggregate) → Distributed Aho-Corasick

## By Primary Requirement

### Requirement: Interactive Latency (<100ms)

**Use cases**: Text editors, code search, browser Find
**Solution**: Boyer-Moore or well-optimized stdlib
**Why**: Average case fast enough, preprocessing negligible

**Critical**: Don't block UI thread

### Requirement: High Throughput (>1 GB/s)

**Use cases**: Network IDS, log processing, virus scanning
**Solution**: Hyperscan or SIMD-optimized algorithms
**Why**: Need SIMD, hardware acceleration

**Critical**: Must scale linearly with cores

### Requirement: Worst-Case Guarantee

**Use cases**: Real-time systems, safety-critical
**Solution**: KMP (single pattern) or AC (multiple)
**Why**: O(n) guaranteed, no surprises

**Critical**: Predictable latency more important than average-case speed

### Requirement: Memory Constrained

**Use cases**: Embedded systems, mobile, edge devices
**Solution**: Naive, Rabin-Karp, or KMP
**Why**: O(1) or O(m) space, no large tables

**Critical**: Throughput less important than footprint

### Requirement: Simplicity (Fast Development)

**Use cases**: Prototypes, tools, scripts
**Solution**: Use stdlib or high-level library
**Why**: Time to market > algorithmic perfection

**Critical**: Maintainability, readability

## Decision Tree

```
What's your PRIMARY constraint?

├─ Development Speed
│  └─ Use stdlib (strstr, str.find)
│     Good enough for 80% of cases
│
├─ Throughput (Need Speed)
│  ├─ Single pattern? → Boyer-Moore
│  └─ Multiple patterns?
│     ├─ <100 patterns → Run BM or use AC
│     └─ >100 patterns → Aho-Corasick or Hyperscan
│
├─ Worst-Case Guarantee
│  ├─ Single pattern → KMP
│  └─ Multiple patterns → Aho-Corasick
│
├─ Memory (RAM Limited)
│  └─ Naive or Rabin-Karp (O(1) space)
│
└─ Domain-Specific
   ├─ Bioinformatics → BWA, BLAST, Bowtie
   ├─ Security (IDS) → Hyperscan
   └─ Logs → ELK, ripgrep, AC
```

## Common Mistake Patterns

### Mistake 1: Premature Optimization

**Symptom**: Implementing complex algorithm before measuring
**Example**: "I'll use KMP because it's O(n)"
**Solution**: Use stdlib, profile, optimize only if proven slow

**Reality**: Well-optimized naive > hand-rolled KMP

### Mistake 2: Wrong Algorithm for Use Case

**Symptom**: Using single-pattern algorithm for 1000 patterns
**Example**: Running Boyer-Moore 1000 times
**Solution**: Use Aho-Corasick (designed for multi-pattern)

**Reality**: AC is 100-1000x faster for many patterns

### Mistake 3: Ignoring Domain Knowledge

**Symptom**: Using general string matching for specialized domain
**Example**: KMP for DNA alignment
**Solution**: Use domain-specific tools (Bowtie, BLAST)

**Reality**: Specialized tools 100-1000x faster, handle complexity

### Mistake 4: Not Considering Real Constraints

**Symptom**: Choosing algorithm based on theory, not practice
**Example**: "Boyer-Moore is O(n/m), must be fastest"
**Solution**: Benchmark with real data, consider implementation quality

**Reality**: Stdlib naive might be faster (SIMD, better implementation)

## Integration Checklist

Before deploying pattern matching solution:

**Functional**:
- [ ] Handles all required patterns
- [ ] Correct results (no false positives/negatives)
- [ ] Supports needed features (case-insensitive, regex, etc.)

**Performance**:
- [ ] Meets throughput requirements
- [ ] Acceptable latency (interactive or batch)
- [ ] Scales with data size and pattern count

**Reliability**:
- [ ] No crashes on edge cases (empty pattern, long text, etc.)
- [ ] Handles Unicode correctly (if needed)
- [ ] No catastrophic backtracking (if using regex)

**Operational**:
- [ ] Memory usage acceptable
- [ ] Easy to update patterns (if dynamic)
- [ ] Logging/monitoring for diagnostics

**Maintenance**:
- [ ] Code is readable (or use library)
- [ ] Tests cover edge cases
- [ ] Documentation for future developers

## Key Principles

### 1. Start Simple

Use stdlib or well-known library → Profile → Optimize only if needed

**Most projects never need custom algorithm implementation**

### 2. Match Context

- Interactive UI → Latency matters
- Batch processing → Throughput matters
- Security → Accuracy matters
- Embedded → Memory matters

**No universal best choice**

### 3. Use Established Tools

- Text search → ripgrep, grep
- Network IDS → Hyperscan, Snort
- Bioinformatics → BLAST, Bowtie
- Log analysis → ELK, Splunk

**Don't reinvent wheel in critical path**

### 4. Benchmark with Real Data

- Synthetic benchmarks lie
- Cache behavior unpredictable
- Implementation quality matters more than algorithm

**Measure, don't guess**

## Next Steps

After choosing algorithm based on use case:

1. **Prototype**: Integrate library, test with real data
2. **Benchmark**: Measure throughput, latency, memory
3. **Validate**: Ensure correct results (unit tests)
4. **Deploy**: Monitor in production
5. **Iterate**: Optimize if proven necessary

**See S4 for STRATEGIC considerations** (long-term viability, maintenance, ecosystem trends)
