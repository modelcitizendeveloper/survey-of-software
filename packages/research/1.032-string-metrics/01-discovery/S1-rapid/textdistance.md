# textdistance (Python)

**GitHub:** ~3.4K stars | **Ecosystem:** Python | **License:** MIT

## Positioning

Comprehensive pure-Python library with 40+ string distance and similarity algorithms. Swiss Army knife for research, prototyping, and when you need obscure metrics.

## Key Metrics

- **Coverage:** 40+ algorithms (most comprehensive Python library)
- **Download stats:** ~3M downloads/month on PyPI (Jan 2025)
- **Maintenance:** Maintained but slower release cadence (6-12 month gaps)
- **Python versions:** 3.5+ supported

## Algorithms Included

**Edit-based:**
- Levenshtein, Damerau-Levenshtein, Hamming, Jaro-Winkler

**Token-based:**
- Jaccard, Sørensen-Dice, Tversky, Overlap, Cosine, Bag distance

**Sequence-based:**
- LCSStr, LCSSeq, Ratcliff-Obershelp

**Phonetic:**
- MRA, Editex

**Compression-based:**
- NCD (Normalized Compression Distance), LZMA, BZ2, ZLib

**Qgram-based:**
- Qgram, Sorensen, Jaccard for character n-grams

## Community Signals

**Stack Overflow sentiment:**
- "Use textdistance for exploring different metrics, then optimize with rapidfuzz"
- "Great for research - try 10 algorithms quickly to see which works"
- "Pure Python makes debugging easier, but use C++ libraries for production"

**Common use cases:**
- Academic research on similarity measures
- Prototyping fuzzy matching systems
- Comparing algorithm effectiveness for specific domains
- When you need rare metrics (compression-based, phonetic)

## Trade-offs

**Strengths:**
- Broadest algorithm coverage (40+ metrics)
- Pure Python (easy to debug and modify)
- Consistent API across all algorithms
- Optional C/C++ accelerators for common metrics

**Limitations:**
- Slower than specialized C++ implementations (10-100x vs rapidfuzz)
- Some algorithms are naive implementations (not optimized)
- Large dependency if you only need 1-2 metrics

## Decision Context

**Choose textdistance when:**
- Exploring which metric works best for your data
- Need rare algorithms (compression-based, Tversky, MRA)
- Prototyping and performance isn't critical yet
- Want pure Python for ease of debugging

**Skip if:**
- Production workload with >1M comparisons (use rapidfuzz)
- Only need Levenshtein/Jaro-Winkler (simpler libraries exist)
- JavaScript/Rust/Go ecosystem (Python-only library)
