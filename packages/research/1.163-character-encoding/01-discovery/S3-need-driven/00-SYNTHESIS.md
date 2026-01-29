# S3 Need-Driven Discovery - Synthesis

## Overview

S3 analyzed character encoding libraries through the lens of real-world business scenarios. Instead of "what can these libraries do?", we asked "which library solves my specific problem?"

## Scenario Summary

| Scenario | Primary Challenge | Library Stack | Key Trade-off |
|----------|------------------|---------------|---------------|
| **Legacy Banking** | Big5 → UTF-8 migration | big5hkscs + validation | Accuracy vs performance |
| **Web Scraping** | Unknown/mixed encodings | charset-normalizer + ftfy + zhconv | Accuracy vs speed |
| **User Uploads** | Untrusted encoding claims | charset-normalizer + validation | Trust vs verify |
| **Bilingual Content** | Regional variants | OpenCC (context-aware) | Quality vs cost |
| **Database Migration** | One-time conversion | cchardet + parallel + validate | Speed vs safety |
| **Email Processing** | MIME multipart mojibake | email + ftfy (selective) | Preserve vs repair |
| **Log Aggregation** | High volume, mixed sources | cchardet + skip repair | Throughput vs accuracy |

## Key Insights

### 1. Context Determines Library Choice

**Not "which library is best"** but "which library fits this scenario"

**Example**: Detection libraries
- **Financial migration**: charset-normalizer (95% accuracy worth the 23x slowdown)
- **Log aggregation**: cchardet (throughput matters, 85% accuracy acceptable)
- **User uploads**: charset-normalizer + show alternatives (UX matters)

**Pattern**: Higher stakes → More accuracy → Slower libraries acceptable

### 2. Repair is Often Unnecessary

**Common mistake**: Always using ftfy

**Reality**: Only ~5-20% of scenarios need mojibake repair

**When to skip repair**:
- Known clean encodings (legacy CSV exports)
- Fresh scrapes (not mojibake, just unknown encoding)
- High-confidence detection (>95%)

**When to use repair**:
- Low detection confidence (<90%)
- User-submitted content (unknown provenance)
- Email forwarding chains (known mojibake source)
- Database with historical corruption

**Impact**: Skipping unnecessary repair saves 64% of pipeline time

### 3. Performance Scales with Volume

**Small volumes (<100 files/day)**: Use best accuracy
- charset-normalizer: Takes 2-3s per file, doesn't matter
- OpenCC: Context-aware conversion, worth the cost

**Medium volumes (1,000-10,000/day)**: Parallelize
- charset-normalizer + 8 workers: Process 10,000 files in <2 hours
- Accuracy still good, speed acceptable

**High volumes (>50,000/day)**: Switch to fast libraries
- cchardet: 10-100x faster, accept 85-90% accuracy
- zhconv: 3x faster than OpenCC, character-level ok for search

### 4. Validation is Non-Negotiable for High Stakes

**Financial/legal data**: Validate 100%
```python
# Conversion pipeline for banking
convert_with_strict_mode()  # Fail on any error
validate_row_counts()       # Ensure no data loss
check_replacement_chars()   # No � characters
create_audit_log()          # Compliance
```

**E-commerce scraping**: Validate samples
```python
# Can tolerate 1-2% errors
if confidence < 0.8:
    log_for_manual_review()
if replacement_chars > 5%:
    reject_page()
```

**Search indexing**: Accept errors
```python
# Errors just mean some search misses
# Don't fail entire pipeline over one bad document
```

### 5. Site/Source-Specific Overrides Beat Generic Detection

**Web scraping pattern**:
```python
# Maintain database of known problematic sites
if domain in KNOWN_PROBLEMATIC:
    use_hardcoded_encoding()  # Faster, more reliable
else:
    detect_encoding()  # For new/unknown sites
```

**Benefit**: 90% of traffic from 10% of sites → optimize the common case

**Database migration pattern**:
```python
# Group tables by encoding
big5_tables = ['customers', 'accounts']
gbk_tables = ['products', 'inventory']

# Skip detection, use known encoding
```

## Library Selection Decision Tree

### For Detection

```
Is encoding known?
├─ YES → Use Python codecs directly (no detection needed)
└─ NO → What matters more?
    ├─ Accuracy (financial, legal, display quality)
    │  └─ charset-normalizer
    └─ Speed (logs, high volume, search indexing)
       └─ cchardet
```

### For Repair

```
Is text garbled (mojibake)?
├─ NO → Skip ftfy
└─ YES → How certain?
    ├─ Definitely garbled → ftfy
    └─ Might be garbled → ftfy if detection confidence <90%
```

### For CJK Conversion

```
Need Traditional ↔ Simplified?
├─ NO → Skip
└─ YES → What's the use case?
    ├─ Professional content (articles, UI, docs)
    │  └─ OpenCC (context-aware, regional vocab)
    └─ Search/indexing (normalize for matching)
       └─ zhconv (fast, character-level ok)
```

## Common Anti-Patterns

### 1. Over-Engineering: Using All Libraries

```python
# WRONG: Kitchen sink approach
from charset_normalizer import from_bytes
import ftfy
import opencc

# Use all three on every file!
result = from_bytes(data)
text = ftfy.fix_text(str(result.best()))
text = opencc.convert(text)
```

**Problem**: Slow, unnecessary, may introduce errors

**Right approach**: Use only what you need
```python
# If encoding is known and clean:
text = data.decode('big5')  # Done!

# If encoding unknown but data clean:
result = from_bytes(data)
text = str(result.best())  # Done!

# Only add repair/conversion if actually needed
```

### 2. Trusting Meta Tags/Headers Blindly

```python
# WRONG:
encoding = response.headers.get('Content-Type')
html = response.content.decode(encoding)  # May fail or give wrong result
```

**Right approach**: Detect first, use meta as hint
```python
result = from_bytes(response.content)
if result.best().encoding_confidence < 0.8:
    # Try meta tag as fallback
    try:
        html = response.content.decode(meta_charset)
    except:
        html = str(result.best())  # Fall back to detection
else:
    html = str(result.best())  # Trust detection
```

### 3. No Validation After Conversion

```python
# WRONG:
convert_big5_to_utf8(input, output)
# Assume it worked!
```

**Right approach**: Validate
```python
result = convert_big5_to_utf8(input, output)
assert result['row_count_before'] == result['row_count_after']
assert '�' not in read_output()  # No replacement chars
log_audit_trail(result)
```

### 4. Sequential Processing When Parallel is Easy

```python
# WRONG: Process 10,000 files sequentially
for file in files:
    convert(file)  # Takes 10 hours
```

**Right approach**: Parallelize
```python
# Process in parallel
with ProcessPoolExecutor(max_workers=8) as executor:
    executor.map(convert, files)  # Takes 1.5 hours
```

## Cost-Benefit Analysis

### Scenario: Web Scraping 50,000 Pages/Day

**Option A: charset-normalizer (accuracy)**
- Accuracy: 95%+
- Speed: 150ms/page
- Total time: 2 hours
- Errors: ~2,500 pages (5%)
- Cost: Acceptable (can run overnight)

**Option B: cchardet (speed)**
- Accuracy: 85%
- Speed: 10ms/page
- Total time: 8 minutes
- Errors: ~7,500 pages (15%)
- Cost: Very low

**Decision factors**:
- If errors affect user experience → Option A (quality matters)
- If search indexing (errors just mean some misses) → Option B (speed matters)
- If real-time (5-min freshness) → Option B (must be fast)

**Hybrid approach** (best of both):
- Use cchardet by default (fast)
- If confidence <80%, re-detect with charset-normalizer (accuracy)
- ~90% fast path, ~10% slow path
- Overall: 20 minutes, 92% accuracy

## Tooling Recommendations by Business Context

### Startup (Move Fast)

**Stack**: charset-normalizer + ftfy + OpenCC
- Easy to use, good defaults
- Pure Python (no compilation)
- Can handle most scenarios
- Optimize later if needed

### Enterprise (Reliability Critical)

**Stack**: charset-normalizer + validation + audit logs
- Accuracy over speed
- Comprehensive error handling
- Compliance/audit trail
- Validated on production samples

### High-Scale (Performance Critical)

**Stack**: cchardet + zhconv + parallelization
- Speed over accuracy
- Accept 85-90% accuracy
- Heavy optimization (caching, parallelism)
- Monitor error rates

### Embedded/Edge (Resource Constrained)

**Stack**: chardet (pure Python) + zhconv (lightweight)
- No C extensions needed
- Lower memory footprint
- Slower but works everywhere

## Integration Testing Checklist

For each scenario implementation:

- [ ] Unit tests with synthetic data
- [ ] Integration tests with real production samples
- [ ] Error handling tests (corrupted files, invalid encodings)
- [ ] Performance tests (meet SLA?)
- [ ] Validation tests (no data loss?)
- [ ] Edge case tests (Big5-HKSCS, GB18030, mojibake)
- [ ] Rollback plan (what if conversion fails?)
- [ ] Monitoring (track error rates, performance)

## Next Steps for S4 (Strategic Selection)

Focus on long-term viability and ecosystem trends:
1. **Library longevity**: Which libraries will be maintained in 5 years?
2. **Ecosystem momentum**: What are major projects (requests, urllib3) using?
3. **GB18030 compliance**: Chinese government mandate implications
4. **Python version support**: Python 3.13+ compatibility
5. **Migration paths**: If library is deprecated, what's the replacement?
