# Pattern Matching Algorithms: Discovery Documentation

## Overview

Comprehensive research on pattern matching algorithms (KMP, Boyer-Moore, Aho-Corasick, Rabin-Karp), organized using the 4PS (Four-Pass Survey) methodology. Each pass reveals different aspects of the solution space, from rapid ecosystem scan to long-term strategic viability.

## Four-Pass Structure

### S1: Rapid Discovery (WHAT tools exist?)
**Reading time**: ~10 minutes
**Focus**: Library ecosystem scan across platforms

### S2: Comprehensive Discovery (HOW do they work?)
**Reading time**: ~30-45 minutes
**Focus**: Algorithm internals, complexity analysis, trade-offs

### S3: Need-Driven Discovery (WHO needs + WHY?)
**Reading time**: ~20 minutes
**Focus**: Use cases, personas, scenario-based matching

### S4: Strategic Discovery (WHICH for long-term?)
**Reading time**: ~25 minutes
**Focus**: Viability, maintenance, ecosystem trends, future-proofing

---

## S1: Rapid Discovery

### [Approach](S1-rapid/approach.md)
S1 methodology: What we scan and why

### Libraries by Platform

#### [C/C++ Libraries](S1-rapid/c-cpp-libraries.md)
- **strstr/memmem**: Standard library (universal, ~100-500 MB/s)
- **std::string::find()**: C++ stdlib (often BMH, ~500 MB/s - 2 GB/s)
- **Hyperscan**: Intel multi-pattern (4.7K stars, 10-100 GB/s)
- **Boost.StringAlgo**: Multiple algorithms
- **RE2**: Google regex (8.8K stars, linear-time guarantee)

#### [Python Libraries](S1-rapid/python-libraries.md)
- **str.find()**: Built-in (BMH variant, ~500 MB/s - 2 GB/s)
- **pyahocorasick**: Multi-pattern AC (936 stars, C extension)
- **re module**: Stdlib regex (backtracking NFA)
- **pyre2**: RE2 bindings (linear-time regex)
- **flashtext**: Keyword extraction (5.6K stars, Trie-based)

#### [Rust & Go Libraries](S1-rapid/rust-go-libraries.md)
**Rust**:
- **memchr**: SIMD byte search (1.1K stars, 5-10 GB/s)
- **aho-corasick**: Multi-pattern (1K+ stars, 1-5 GB/s)
- **regex**: DFA hybrid (3.5K stars, linear-time)

**Go**:
- **strings.Index()**: Stdlib (Rabin-Karp variant, ~500 MB/s - 2 GB/s)
- **regexp**: Stdlib (RE2-based, linear-time)
- **cloudflare/ahocorasick**: Multi-pattern (340 stars, 1-3 GB/s)

#### [Java/JVM Libraries](S1-rapid/java-jvm-libraries.md)
- **String.indexOf()**: Java stdlib (BMH in HotSpot, ~500 MB/s - 2 GB/s)
- **Pattern/Matcher**: Stdlib regex (backtracking NFA)
- **aho-corasick (robert-bor)**: Multi-pattern (1.1K stars)

#### [Specialized Libraries](S1-rapid/specialized-libraries.md)
- **Hyperscan**: Industry-standard IDS (4.7K stars, 10-100 GB/s)
- **Vectorscan**: Hyperscan fork for ARM
- **agrep**: Fuzzy matching (Wu-Manber bitap)
- **BLAST**: Bioinformatics (seed-and-extend)
- **Bowtie2**: NGS read alignment (BWT + FM-index)

### [Recommendation](S1-rapid/recommendation.md)
**Quick selection guide**: Stdlib for single pattern, AC for multi-pattern, Hyperscan for ultra-high performance

**Key takeaway**: 90% of use cases → Use stdlib. 10% with special needs → Use specialized libraries.

---

## S2: Comprehensive Discovery

### [Approach](S2-comprehensive/approach.md)
S2 methodology: Deep technical analysis

### Algorithm Deep-Dives

#### [Knuth-Morris-Pratt (KMP)](S2-comprehensive/knuth-morris-pratt.md)
- **Mechanism**: Failure function for skipping positions
- **Complexity**: O(n + m) guaranteed (optimal linear time)
- **Space**: O(m) for failure function
- **Strength**: Worst-case guarantee, no text backtracking
- **Weakness**: Slower average case than BM
- **Best for**: Small alphabets (DNA), worst-case guarantees, streaming

#### [Boyer-Moore (BM)](S2-comprehensive/boyer-moore.md)
- **Mechanism**: Right-to-left scan + two heuristics (bad char + good suffix)
- **Complexity**: O(n/m) best (sublinear!), O(nm) worst
- **Space**: O(m + σ) for lookup tables
- **Strength**: Sublinear average case (1-2 GB/s typical)
- **Weakness**: Worst-case O(nm), complex good suffix rule
- **Best for**: Large alphabets (English, Unicode), interactive search

#### [Aho-Corasick (AC)](S2-comprehensive/aho-corasick.md)
- **Mechanism**: Trie + KMP-style failure links for multi-pattern
- **Complexity**: O(n + m + z) where z = matches (optimal multi-pattern)
- **Space**: O(m × σ) worst case (trie size)
- **Strength**: Single pass finds all patterns, scales to millions
- **Weakness**: Large trie for sparse patterns, always linear (no sublinear)
- **Best for**: Multiple patterns (10+), IDS, virus scanning

#### [Rabin-Karp (RK)](S2-comprehensive/rabin-karp.md)
- **Mechanism**: Rolling hash for O(1) window comparison
- **Complexity**: O(n + m) average, O(nm) worst (hash collisions)
- **Space**: O(1) (minimal memory)
- **Strength**: Simple implementation, low memory, multiple patterns (same length)
- **Weakness**: Probabilistic (hash collisions), not deterministic
- **Best for**: Multiple same-length patterns, 2D matching, plagiarism detection

### [Feature Comparison](S2-comprehensive/feature-comparison.md)
**Comprehensive matrix**: Complexity, performance, alphabet size impact, use case suitability

**Key insights**:
- No universal winner: Each optimizes different bottleneck
- Alphabet size critical: Small (DNA) → KMP, Large (English) → BM
- Pattern count: Single → BM, Many → AC
- Worst-case: KMP/AC guaranteed, BM/RK not

### [Recommendation](S2-comprehensive/recommendation.md)
**Algorithm-driven selection**: Match to technical constraints (speed, memory, predictability)

**Key takeaway**: Choose based on limiting constraint. Profile with real data before deciding.

---

## S3: Need-Driven Discovery

### [Approach](S3-need-driven/approach.md)
S3 methodology: Start with needs, not tools

### Use Cases

#### [Text Editor Search](S3-need-driven/text-editor-search.md)
**Who**: Developer building text editor (VS Code, Sublime)
**Why**: Interactive find/replace, <50ms latency
**Constraints**: Patterns change frequently, must not block UI
**Solution**: Boyer-Moore (stdlib) or Rust regex
**Alternatives**: Index for large files (>10 MB)
**Pitfalls**: Catastrophic backtracking (regex), blocking UI thread

#### [Network IDS](S3-need-driven/network-ids.md)
**Who**: Security engineer deploying IDS (Snort, Suricata)
**Why**: Real-time intrusion detection, 1-100 Gbps
**Constraints**: Thousands of signatures, zero false negatives
**Solution**: Hyperscan (10-100 GB/s, industry standard)
**Alternatives**: Vectorscan (ARM), vanilla AC (lower throughput)
**Pitfalls**: Pattern explosion, regex backtracking, packet loss

#### [Bioinformatics](S3-need-driven/bioinformatics.md)
**Who**: Computational biologist (genome analysis)
**Why**: DNA sequence search, alignment, homology
**Constraints**: Small alphabet (σ=4), billions of base pairs, approximate matching
**Solution**: Domain-specific (BWA, Bowtie2, BLAST), not general string matching
**Alternatives**: KMP/AC for exact search (limited use)
**Pitfalls**: Using general algorithms, ignoring biological context

#### [Log Analysis](S3-need-driven/log-analysis.md)
**Who**: DevOps engineer, SRE (system/app logs)
**Why**: Error detection, security monitoring, performance analysis
**Constraints**: GB-TB/day, streaming, multiple keywords
**Solution**: Aho-Corasick (keywords), RE2 (structured extraction), ELK (indexed search)
**Alternatives**: ripgrep (interactive), Splunk (commercial)
**Pitfalls**: Regex backtracking, memory exhaustion, missing multi-line logs

### [Recommendation](S3-need-driven/recommendation.md)
**Use-case driven selection**: Match library to YOUR context

**Key takeaway**: Context matters more than benchmarks. Use domain-specific tools when available.

---

## S4: Strategic Discovery

### [Approach](S4-strategic/approach.md)
S4 methodology: Beyond technical specs to long-term viability

### Strategic Analyses

#### [Stdlib Viability](S4-strategic/stdlib-viability.md)
**Status**: ★★★★★ Stable, universal, continuously improving
**Trajectory**: STEADY (always available, incrementally better)
**Longevity**: Will exist as long as language exists (2035+)
**Risks**: None (lowest-risk option)
**Best for**: 90% of projects (default choice)
**Hidden benefit**: Zero maintenance burden, universal knowledge

#### [Hyperscan Viability](S4-strategic/hyperscan-viability.md)
**Status**: ★★★★☆ Mature, Intel-backed → transitioning to community-led
**Trajectory**: STABLE → COMMUNITY (Intel reduced investment 2023)
**Longevity**: 70% confidence in 2030 (via Vectorscan fork)
**Risks**: Intel abandonment, complex integration, x86-only
**Best for**: Network security, ultra-high throughput (>5 GB/s)
**Mitigation**: Monitor Vectorscan, plan for hardware acceleration

### [Recommendation](S4-strategic/recommendation.md)
**Three strategic paths**: Conservative (stdlib + proven libs), Performance-First (Hyperscan), Adaptive (evolve based on data)

**Long-term trends**:
- Hardware acceleration maturing (SmartNICs, 2027-2030)
- SIMD dominance (algorithm < hardware)
- Stdlib evolution (continuous improvement)

**Key insights**:
- **Conservative path**: Best for most (lowest risk, cost, maintenance)
- **Performance-First**: Network security, deep expertise required
- **Adaptive**: Growth startups, profile-driven decisions

**Bottom line**: Pattern matching is mature field (40-50 year old algorithms). Future improvements from SIMD/hardware, not new algorithms. Choose based on organizational fit, not fashion.

---

## Key Findings Summary

### Core Problem
Substring search is fundamental operation in computing. Naive O(nm) infeasible for large inputs. Optimized algorithms use preprocessing (pattern or text) to skip positions intelligently.

### Four Core Algorithms (1970s)

| Algorithm | Key Insight | Best Case | Worst Case | Best For |
|-----------|-------------|-----------|------------|----------|
| **KMP** | Failure function (no text backtrack) | O(n) | O(n) | Small alphabet, guarantees |
| **Boyer-Moore** | Right-to-left + bad char/good suffix | O(n/m) | O(nm) | Large alphabet, speed |
| **Aho-Corasick** | Trie + failure links (multi-pattern) | O(n + z) | O(n + z) | Many patterns |
| **Rabin-Karp** | Rolling hash | O(n + m) | O(nm) | Simplicity, low memory |

### Library Landscape

| Use Case | Library/Tool | Performance | Maturity |
|----------|--------------|-------------|----------|
| **General (stdlib)** | strstr, str.find | 500 MB/s - 2 GB/s | ★★★★★ |
| **Multi-pattern** | Aho-Corasick libs | 500 MB/s - 5 GB/s | ★★★★☆ |
| **Ultra-high perf** | Hyperscan | 10-100 GB/s | ★★★★☆ |
| **Regex (safe)** | RE2, Rust regex | 100-500 MB/s | ★★★★☆ |
| **Bioinformatics** | BWA, BLAST, Bowtie2 | Domain-specific | ★★★★★ |
| **Interactive search** | ripgrep | 10 GB/s | ★★★★☆ |

### Critical Technical Decisions

**Alphabet size matters**:
- Small (DNA: σ=4) → KMP competitive, BM less effective
- Large (Unicode: σ=65K) → BM excels, tables need sparse structures

**Pattern count is decisive**:
- Single → BM (sublinear average case)
- 10-100 → AC or BM × k (benchmark)
- 100+ → Definitely AC (or Hyperscan for ultra-perf)

**SIMD > Algorithm**:
- Modern: SIMD naive competitive with scalar BM (short patterns)
- Future: Stdlib incorporating SIMD (free performance)

### Strategic Recommendations

**Default (95% of projects)**:
- Start with stdlib (strstr, std::string::find, str.find)
- Profile before optimizing
- Migrate only if proven bottleneck

**Network Security**:
- Hyperscan (industry standard)
- Proven at scale (Snort, Suricata, CloudFlare)

**Bioinformatics**:
- Use domain tools (BWA, BLAST, Bowtie2)
- Don't use general string matching

**Future-proof**:
- Stdlib will improve (SIMD, better algorithms)
- Hardware acceleration maturing (2027-2030)
- Pattern matching mature (40-year-old algorithms won't be replaced)

---

## Related Research

- **1.001 - Sorting Libraries**: Performance comparison methodologies
- **1.002 - Fuzzy Search**: Approximate string matching (edit distance)
- **1.033 - NLP Libraries**: Text processing pipelines

---

## Document Status

- ✅ S1 Rapid Discovery: Complete
- ✅ S2 Comprehensive Discovery: Complete
- ✅ S3 Need-Driven Discovery: Complete
- ✅ S4 Strategic Discovery: Complete

**Last Updated**: February 2026
**Coverage**: Algorithms (KMP, BM, AC, RK), libraries (20+ surveyed), use cases (4 detailed), strategic analysis (2 deep-dives)
**Audience**: Software engineers, security engineers, researchers, product managers, CTOs

**Methodology**: Four-Pass Survey (4PS) - rapid → comprehensive → need-driven → strategic
