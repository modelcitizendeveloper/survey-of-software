# C/C++ Pattern Matching Libraries

## Standard Library Functions

### strstr() / memmem()
- **Maturity**: Part of C standard library, universally available
- **Performance**: Varies by implementation (glibc ~100-500 MB/s)
- **Algorithms**: Naive in some implementations, optimized (Two-Way) in glibc
- **Ease**: Trivial API (one function call)
- **Best for**: Simple substring search when stdlib is sufficient

### std::string::find() (C++)
- **Maturity**: C++ standard library
- **Performance**: ~500 MB/s to 2 GB/s (implementation-dependent)
- **Algorithms**: Usually Boyer-Moore-Horspool variant
- **Ease**: Very simple (method on string object)
- **Best for**: C++ projects with single-pattern search

## Hyperscan (Intel)

- **Maturity**: 4.7K GitHub stars, Intel-backed, production-grade
- **Performance**: 10-100 GB/s depending on pattern set and hardware
- **Algorithms**: Hybrid (Aho-Corasick + DFA optimization + SIMD)
- **Ease**: Moderate API, requires pattern compilation
- **Best for**: High-performance multi-pattern matching (IDS, DPI, antivirus)
- **Production use**: Used by Snort, Suricata, commercial DPI systems

## Boost.StringAlgo

- **Maturity**: Part of Boost (widely used C++ libraries)
- **Performance**: Moderate (not optimized for extreme performance)
- **Algorithms**: Multiple (KMP, Boyer-Moore, naive)
- **Ease**: Simple API with algorithm selection
- **Best for**: C++ projects already using Boost

## libdivsufsort / SDSL

- **Maturity**: Academic implementations, 2K+ stars
- **Performance**: Excellent for indexed search (suffix arrays)
- **Algorithms**: Suffix array construction (SA-IS, SAIS)
- **Ease**: Complex (requires understanding suffix structures)
- **Best for**: Multiple searches on same text (build index once)

## RE2 (Google)

- **Maturity**: 8.8K GitHub stars, Google production use
- **Performance**: ~100-500 MB/s (regex, not pure string matching)
- **Algorithms**: DFA-based regex (Thompson NFA + DFA caching)
- **Ease**: Simple regex API, drop-in for PCRE
- **Best for**: Regex with guaranteed linear time (no catastrophic backtracking)
- **Production use**: Google internal infrastructure
