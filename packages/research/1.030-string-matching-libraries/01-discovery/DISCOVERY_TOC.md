# Discovery Table of Contents: String Matching Libraries

## Overview

This discovery covers string matching libraries across three categories:
- **Fuzzy/Approximate Matching**: Handle typos, variations (RapidFuzz, Jellyfish)
- **Exact Multi-Pattern Matching**: Find many patterns efficiently (pyahocorasick)
- **Regex Engines**: Pattern-based matching (re, regex, google-re2)

---

## S1: Rapid Discovery (Popularity & Ecosystem)

**Time Budget**: 10 minutes
**Philosophy**: "Popular libraries exist for a reason"

### Files
- [approach.md](S1-rapid/approach.md) - Discovery methodology
- [rapidfuzz.md](S1-rapid/rapidfuzz.md) - Fastest fuzzy matcher (3.7K stars, 83M/mo downloads)
- [jellyfish.md](S1-rapid/jellyfish.md) - Phonetic matching specialist (2.2K stars)
- [pyahocorasick.md](S1-rapid/pyahocorasick.md) - Multi-pattern exact matching (1.1K stars)
- [regex-library.md](S1-rapid/regex-library.md) - Enhanced regex (160M/mo downloads)
- [google-re2.md](S1-rapid/google-re2.md) - Linear-time regex (Google-backed)
- [recommendation.md](S1-rapid/recommendation.md) - S1 quick picks

### Key Findings
- **RapidFuzz** dominates fuzzy matching (83M downloads)
- **regex library** widely adopted for enhanced regex (160M downloads)
- **pyahocorasick** specialized for multi-pattern (1.1K stars but proven at scale)
- Stdlib options (re, difflib) available but slower

---

## S2: Comprehensive Analysis (Technical Deep-Dive)

**Time Budget**: 30-40 minutes
**Philosophy**: "Understand how it works before choosing"

### Files
- [approach.md](S2-comprehensive/approach.md) - Technical methodology
- [rapidfuzz.md](S2-comprehensive/rapidfuzz.md) - Algorithms, performance benchmarks, API
- [jellyfish.md](S2-comprehensive/jellyfish.md) - Phonetic + distance algorithms
- [pyahocorasick.md](S2-comprehensive/pyahocorasick.md) - Aho-Corasick automaton details
- [regex-library.md](S2-comprehensive/regex-library.md) - Enhanced backtracking engine
- [google-re2.md](S2-comprehensive/google-re2.md) - DFA-based linear time
- [feature-comparison.md](S2-comprehensive/feature-comparison.md) - Side-by-side comparison
- [recommendation.md](S2-comprehensive/recommendation.md) - Technical best fit

### Key Findings
- **RapidFuzz**: O(nm) optimized, 40% faster (1,800 pairs/sec)
- **pyahocorasick**: O(n + z) regardless of pattern count (unique strength)
- **google-re2**: O(n) guaranteed vs O(2^n) worst for re/regex
- **Trade-offs**: Speed vs features, exact vs fuzzy, security vs capabilities

---

## S3: Need-Driven Validation (Use Cases)

**Time Budget**: 30 minutes
**Philosophy**: "Who needs this, and why does it matter?"

### Files
- [approach.md](S3-need-driven/approach.md) - Use case methodology
- [use-case-ecommerce-deduplication.md](S3-need-driven/use-case-ecommerce-deduplication.md) - Product title matching (RapidFuzz 85% fit)
- [use-case-fuzzy-search.md](S3-need-driven/use-case-fuzzy-search.md) - User-facing search (Elasticsearch 95% fit)
- [use-case-content-moderation.md](S3-need-driven/use-case-content-moderation.md) - Banned phrase detection (pyahocorasick 95% fit)
- [use-case-name-matching.md](S3-need-driven/use-case-name-matching.md) - Patient name deduplication (Jellyfish + RapidFuzz 95% fit)
- [recommendation.md](S3-need-driven/recommendation.md) - Use-case driven selection

### Key Findings
- **Context matters**: RapidFuzz wrong for user search (needs index) and content moderation (needs multi-pattern)
- **Indexing gap**: Fuzzy matching libraries need blocking/indexing for retrieval use cases
- **Hybrid wins**: Jellyfish (phonetic) + RapidFuzz (fuzzy) = 95% recall for names
- **pyahocorasick perfect fit**: Content moderation with 10K phrases (O(n) saves the day)

---

## S4: Strategic Assessment (Long-Term Viability)

**Time Budget**: 20-30 minutes
**Philosophy**: "Choose for 3-5 years, not just today"

### Files
- [approach.md](S4-strategic/approach.md) - Strategic methodology
- [rapidfuzz-viability.md](S4-strategic/rapidfuzz-viability.md) - Maintenance, ecosystem, risk analysis
- [other-libraries-viability.md](S4-strategic/other-libraries-viability.md) - pyahocorasick, Jellyfish, regex, google-re2
- [recommendation.md](S4-strategic/recommendation.md) - 3-5 year guidance

### Key Findings
- **Low Risk**: RapidFuzz (87/100), regex (95/100), pyahocorasick (90/100)
- **Medium Risk**: Jellyfish (75/100 - bus factor), google-re2 (70/100 - wrapper fragmentation)
- **Massive adoption = sustainability**: 83M (RapidFuzz), 160M (regex) downloads too big to fail
- **Fallback exists**: Stdlib (re, difflib) always available

---

## Cross-Pass Insights

### S1 → S2 → S3 → S4 Evolution

**RapidFuzz Journey:**
- S1: Most popular (83M downloads) ✓
- S2: Fastest (1,800 pairs/sec) ✓
- S3: But needs indexing for search, blocking for deduplication
- S4: Low risk (87/100), adopt confidently

**pyahocorasick Journey:**
- S1: Moderate popularity (1.1K stars)
- S2: O(n + z) unique strength for multi-pattern
- S3: Perfect fit for content moderation (10K phrases)
- S4: Mature, stable, low risk (90/100)

**Jellyfish Journey:**
- S1: Phonetic specialist (2.2K stars)
- S2: Slower than RapidFuzz for edit distance
- S3: Critical for name matching (only option with Soundex/Metaphone)
- S4: Medium risk (bus factor), use with monitoring

### Key Learnings

1. **Popularity ≠ Best Fit** (S1 vs S3)
   - RapidFuzz most popular but wrong for content moderation
   - pyahocorasick less popular but perfect for multi-pattern

2. **Speed ≠ Usability** (S2 vs S3)
   - RapidFuzz fastest but needs indexing infrastructure
   - Elasticsearch slower per comparison but better for search

3. **Technical Excellence ≠ Adoption Safety** (S2 vs S4)
   - Jellyfish good algorithms but medium risk (maintainer bus factor)
   - regex library technically similar to re but safer (160M downloads)

4. **Niche Libraries Have Strategic Value** (All passes)
   - pyahocorasick: Specialized but irreplaceable for multi-pattern
   - Jellyfish: Niche but only phonetic option

---

## Decision Framework Summary

### Quick Selection Guide

```
Need to match strings?
├─ Fuzzy/approximate?
│  ├─ Batch processing → RapidFuzz + blocking
│  ├─ User-facing search → Elasticsearch
│  └─ Name matching → Jellyfish + RapidFuzz
├─ Exact matching?
│  ├─ 1-10 patterns → str.find() or simple regex
│  └─ 100+ patterns → pyahocorasick
└─ Pattern-based (regex)?
   ├─ Standard use → re (stdlib)
   ├─ Need features → regex library
   └─ Security-critical → google-re2
```

---

## Research Confidence

| Pass | Confidence | Basis |
|------|-----------|-------|
| S1 | 75% | Popularity signals, recent data |
| S2 | 85% | Published benchmarks, algorithm analysis |
| S3 | 90% | Real use cases, requirement mapping |
| S4 | 85% | Maintenance history, adoption trends |
| **Overall** | **85%** | **Converging evidence across 4 passes** |

---

## Recommended Reading Order

### For Quick Decision (15 minutes)
1. S1 recommendation → S3 use case matching your scenario → Decision

### For Technical Understanding (45 minutes)
1. S1 recommendation
2. S2 approach + library of interest
3. S2 feature comparison
4. Decision

### For Strategic Adoption (90 minutes)
1. All S1 files (understand landscape)
2. S2 feature comparison + libraries of interest
3. S3 use case matching your scenario
4. S4 viability for chosen library
5. Decision with confidence

### For Complete Research Context (2-3 hours)
1. Read all passes in order (S1 → S2 → S3 → S4)
2. Trace library journey across passes
3. Understand evolution of insights

---

## Document Maintenance

**Created**: January 2026
**Valid Through**: January 2027 (reassess annually)
**Update Triggers**:
- Major library releases
- New competitors emerge
- Significant download trend changes
- Maintainer transitions

**Next Review**: January 2027
