# S3 Need-Driven Recommendation

## Use Case to Requirements Mapping

| Use Case | Primary Metric | Performance Need | Accuracy Need | Library Fit |
|----------|---------------|------------------|---------------|-------------|
| **E-commerce search** | Jaro-Winkler, Token-based | High (>1K ops/sec) | Medium (80-90% precision) | rapidfuzz (Python), string-similarity (JS) |
| **Data deduplication** | Multi-field weighted | Medium (batch OK) | High (>95% precision) | rapidfuzz (Python), strsim (Rust) |
| **Developer tools/CLI** | Levenshtein, Jaro-Winkler | Low (<1K ops/sec) | High (>90% top-1) | strsim (Rust), leven (Go), rapidfuzz (Python) |
| **Content moderation** | Token-based, Cosine | Medium | High (>95% recall for duplicates) | rapidfuzz + ML embeddings |
| **Healthcare record matching** | Jaro-Winkler for names | Low (batch) | Very high (>98% precision) | Apache Commons (Java), rapidfuzz (Python) |

## Problem to Algorithm Mapping

### Typo Tolerance

**Best algorithms:**
- **Levenshtein:** 1-2 character typos ("wireles" → "wireless")
- **Jaro-Winkler:** Transposition errors ("wirelsess" → "wireless")

**Why:**
Edit distance directly models typo operations (insert, delete, substitute).

**Thresholds:**
- Distance ≤ 2: Strong match (single typo)
- Distance ≤ 3: Moderate match (multiple typos or short words)
- Distance > 3: Likely different word (unless very long string)

### Name Matching

**Best algorithms:**
- **Jaro-Winkler:** Person names ("John Smith" ≈ "Jon Smith")
- **Token-based:** Company names ("IBM Corp" ≈ "International Business Machines")

**Why:**
Jaro-Winkler designed for names, prefix bonus helps with common first names.
Token-based handles reordering and variations in company/org names.

**Thresholds:**
- Jaro-Winkler > 0.9: High confidence match
- Jaro-Winkler 0.8-0.9: Likely match, manual review
- Jaro-Winkler < 0.8: Probably different people

### Product/Document Similarity

**Best algorithms:**
- **Token-based (Jaccard, Dice):** Short descriptions, product names
- **Cosine similarity on TF-IDF:** Long documents, semantic similarity

**Why:**
Token-based robust to word reordering, common in e-commerce.
Cosine captures semantic meaning, better for long text.

**Thresholds:**
- Jaccard > 0.7: High similarity
- Jaccard 0.5-0.7: Moderate similarity
- Jaccard < 0.5: Distinct items

### Duplicate Detection

**Best algorithms:**
- **Multi-field weighted:** Combine name + email + address scores
- **Token-based for structured text:** Addresses, company names

**Why:**
Single-field matching has too many false positives.
Weighted combination balances precision and recall.

**Example weights:**
- Name: 40% (core identifier)
- Email: 30% (unique but changeable)
- Address: 20% (stable but data entry errors common)
- Phone: 10% (format variations)

**Threshold:** Combined score > 0.85 for duplicate flag

## Domain-Specific Guidance

### E-commerce / Search

**Key requirements:**
- Latency-sensitive (autocomplete <100ms)
- High throughput (peak traffic)
- Multi-language (unicode-aware)

**Recommended stack:**
- Frontend: `string-similarity` (JavaScript, lightweight)
- Backend: `rapidfuzz` (Python), pre-filter with search index
- Algorithm: Token-based for multi-word queries, Jaro-Winkler for brand names

**Optimization:**
- Pre-compute candidates with Elasticsearch fuzzy query
- Fuzzy-match top 100 candidates only (not full catalog)
- Cache frequent queries

### Data Engineering / ETL

**Key requirements:**
- Batch processing (throughput > latency)
- High precision (minimize manual review)
- Multi-field matching

**Recommended stack:**
- Python: `rapidfuzz` for parallel batch processing
- Rust: `strsim` for high-volume pipelines
- Blocking: Pre-group by first 3 chars + zip code to reduce comparisons

**Algorithm:**
- Jaro-Winkler for person names
- Token-based for company names
- Weighted combination for final score

**Workflow:**
```
1. Blocking (reduce n² to n*k)
2. Pairwise fuzzy matching within blocks
3. Confidence scoring:
   - >0.95: Auto-merge
   - 0.70-0.95: Human review queue
   - <0.70: Skip
```

### Developer Tools / CLI

**Key requirements:**
- Minimal binary size
- Fast startup (<50ms)
- No external dependencies

**Recommended stack:**
- Rust: `strsim` (zero deps, fast)
- Go: `go-levenshtein` (minimal)
- Python: `rapidfuzz` (if Python already in stack)

**Algorithm:**
- Levenshtein for command names (max distance 2-3)
- Jaro-Winkler for longer strings (file paths, config keys)

**UX pattern:**
```
$ mytool comit
Error: unknown command 'comit'

Did you mean 'commit'?
```

### Healthcare / High-Stakes Matching

**Key requirements:**
- Very high precision (>98%, false positive = wrong patient)
- Audit trail (compliance)
- Multi-field matching (name + DOB + SSN/ID)

**Recommended stack:**
- Java: Apache Commons Text (enterprise, auditable)
- Python: `rapidfuzz` with manual review workflow

**Algorithm:**
- Jaro-Winkler for names (handles nicknames, maiden names)
- Exact match for SSN/ID (no fuzzy matching on identifiers)
- Multi-field weighted score

**Compliance:**
- Log all match decisions
- Require human review for scores 0.85-0.95
- Auto-match only for >0.95 (extremely high confidence)
- Reversible merges (audit trail)

## Performance Sizing Guide

### Operations per Second Needs

| Scenario | Ops/sec | Library Choice | Notes |
|----------|---------|----------------|-------|
| **Autocomplete (1 user)** | 10-50 | Any library | Latency < 100ms matters more |
| **Search (100 concurrent users)** | 1K-5K | rapidfuzz, strsim | Multi-core scaling |
| **Batch deduplication (1M records)** | 10K-50K | rapidfuzz (parallel), strsim | Blocking essential |
| **CLI typo correction** | <100 | strsim, leven | Minimal overhead |

### Dataset Size Considerations

| Records | Naive Comparisons | With Blocking | Strategy |
|---------|------------------|---------------|----------|
| 1K | 500K | 500K | No blocking needed |
| 10K | 50M | 500K | Block by prefix (first 2-3 chars) |
| 100K | 5B | 5M | Block by prefix + location/domain |
| 1M | 500B | 50M | Locality-sensitive hashing (LSH) |
| 10M+ | - | - | Specialized dedup tools (Dedupe.io) |

**Blocking reduction:** Typically 100-1000x fewer comparisons

## Common Anti-Patterns to Avoid

### Anti-Pattern 1: O(n²) Naive Comparison

**Problem:**
```python
for record1 in all_records:
    for record2 in all_records:
        if fuzzy_match(record1, record2) > 0.8:
            mark_as_duplicate(record1, record2)
```

**Why bad:** 1M records = 500 billion comparisons

**Fix:** Use blocking or LSH to reduce search space

### Anti-Pattern 2: Wrong Metric for Use Case

**Problem:**
Using Levenshtein for company names ("IBM Corp" vs "Corp IBM" = high distance)

**Why bad:** Sensitive to word order when you want order-invariant matching

**Fix:** Use token-based metrics (Jaccard, Dice) for multi-word strings

### Anti-Pattern 3: Ignoring Unicode Normalization

**Problem:**
"café" (U+00E9) ≠ "café" (U+0065 U+0301) despite visual equivalence

**Why bad:** Same text treated as different, duplicates missed

**Fix:** Normalize with unicodedata.normalize('NFKD', text) before comparison

### Anti-Pattern 4: Over-Automation Without Human Review

**Problem:**
Auto-merging all records with score >0.7 → irreversible data loss on false positives

**Why bad:** 70% confidence means 30% error rate, too high for automated decisions

**Fix:** Tiered approach: >0.95 auto, 0.70-0.95 review, <0.70 skip

### Anti-Pattern 5: Performance-Insensitive Library Choice

**Problem:**
Using pure Python textdistance in production API serving 1K requests/sec

**Why bad:** 10-100x slower than optimized alternatives, server overload

**Fix:** Use rapidfuzz (Python), strsim (Rust), or language-appropriate optimized library

## Validation Checklist

Before implementing fuzzy matching solution:

### Technical Feasibility
- [ ] Identified correct algorithm for use case (Levenshtein vs Jaro-Winkler vs token-based)
- [ ] Performance requirements clear (ops/sec, latency, throughput)
- [ ] Library available for tech stack (Python/Rust/Go/Java/JS)
- [ ] Unicode handling requirements defined (CJK, diacritics, etc.)

### Business Requirements
- [ ] Success metrics defined (precision, recall, user satisfaction)
- [ ] Compliance needs identified (GDPR, HIPAA, audit trails)
- [ ] Manual review process designed (for non-auto-merge cases)
- [ ] Rollback plan if fuzzy matching causes issues

### Resource Availability
- [ ] Engineering time budgeted (2-12 weeks for implementation)
- [ ] Human review capacity allocated (for duplicate review queues)
- [ ] Performance testing planned (load test with production data)
- [ ] Monitoring/alerting designed (track false positive rate, latency)

**Decision threshold:** 10+ checkboxes = green light to proceed
