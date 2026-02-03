# S1 Recommendation: Quick Selection Guide

## Decision Tree

### Single Pattern, Standard Performance
**Use built-in string search**:
- C/C++: `strstr()`, `std::string::find()`
- Python: `str.find()`
- Rust: `str::find()`, `memchr::memmem()`
- Go: `strings.Index()`
- Java: `String.indexOf()`

**Characteristics**: 500 MB/s to 2 GB/s, zero overhead, adequate for most use cases

---

### Multiple Patterns (10-1000s)
**Use Aho-Corasick library**:
- C/C++: Hyperscan (if need extreme performance), Boost.StringAlgo
- Python: `pyahocorasick`
- Rust: `aho-corasick` crate
- Go: `cloudflare/ahocorasick`
- Java: `aho-corasick` (robert-bor)

**Characteristics**: 500 MB/s to 5 GB/s, scales with pattern count, one-time preprocessing cost

---

### Ultra-High Performance (>10 GB/s)
**Use specialized libraries**:
- **Hyperscan** (Intel x86_64): 10-100 GB/s, industry standard for IDS/DPI
- **Vectorscan** (ARM/portable): 80% of Hyperscan on non-x86
- **Hardware solutions**: FPGA/ASIC for >100 Gbps

**Use cases**: Network IDS (Snort, Suricata), deep packet inspection, real-time virus scanning

---

### Regex Needed (Not Just Exact Matching)
**Use linear-time regex engines**:
- C++: RE2 (Google)
- Rust: `regex` crate
- Go: `regexp` package (stdlib)
- Python: `pyre2` or stdlib `re` (for simple patterns)

**Avoid**: PCRE, stdlib regex in Python/Java/JavaScript for untrusted patterns (catastrophic backtracking risk)

---

### Fuzzy/Approximate Matching
**Use specialized algorithms**:
- General: `agrep`, TRE library (Bitap algorithm)
- Bioinformatics: BLAST, Bowtie (specialized for DNA/protein)
- Python: `fuzzywuzzy`, `thefuzz` (Levenshtein distance)

**Note**: Approximate matching is 10-100x slower than exact matching

---

## Selection by Primary Constraint

| Primary Constraint | Library Recommendation | Performance | Complexity |
|--------------------|------------------------|-------------|------------|
| **Simplicity** | stdlib (strstr, str.find, etc.) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Single-pattern speed** | Rust memchr, C++ memmem | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Multi-pattern** | Aho-Corasick libraries | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Extreme throughput** | Hyperscan | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Regex support** | RE2, Rust regex | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Fuzzy matching** | agrep, Bitap | ⭐⭐ | ⭐⭐ |
| **Memory constrained** | KMP implementations | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## Platform-Specific Defaults

**Python**:
- Single: `str.find()` (built-in)
- Multi: `pyahocorasick`
- Regex: `re` module (simple) or `pyre2` (untrusted)

**Rust**:
- Single: `memchr::memmem()` (SIMD)
- Multi: `aho-corasick` crate
- Regex: `regex` crate (linear time)

**C/C++**:
- Single: `memmem()` or `std::string::find()`
- Multi: Hyperscan (high-perf) or Boost (moderate)
- Regex: RE2

**Go**:
- Single: `strings.Index()` (built-in)
- Multi: `cloudflare/ahocorasick`
- Regex: `regexp` package (linear time)

**Java**:
- Single: `String.indexOf()` (built-in)
- Multi: `aho-corasick` (robert-bor)
- Regex: `java.util.regex.Pattern` (simple) or custom (untrusted)

## Production Use Cases

**Network IDS/IPS** (Snort, Suricata):
→ **Hyperscan** (10+ Gbps throughput)

**Antivirus/Malware Scanning** (ClamAV):
→ **Aho-Corasick** (millions of signatures)

**Text Editors** (VS Code, Sublime):
→ **stdlib or regex engines** (interactive, patterns change frequently)

**Log Analysis** (Splunk, ELK):
→ **Aho-Corasick** for keyword matching, **regex** for structure

**Bioinformatics** (NCBI, genome centers):
→ **BLAST, Bowtie** (specialized for biological sequences)

**Web Scraping/NLP** (keyword extraction):
→ **Aho-Corasick** or **flashtext** (Python)

## Key Takeaways

1. **Start with stdlib**: For 80% of use cases, built-in string search is sufficient
2. **AC for multi-pattern**: When searching for 10+ patterns, Aho-Corasick pays off
3. **Hyperscan for scale**: When throughput >5 GB/s matters (network, security)
4. **Linear-time regex**: Use RE2/Rust regex for untrusted patterns (avoid backtracking)
5. **Benchmark with real data**: Theoretical complexity doesn't always predict real performance

**Next**: See S2 for HOW these algorithms work internally
