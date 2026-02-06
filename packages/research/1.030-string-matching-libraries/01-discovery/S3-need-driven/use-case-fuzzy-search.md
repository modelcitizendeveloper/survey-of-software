# Use Case: User-Facing Fuzzy Search

## Who Needs This

**Persona**: Backend Developer at SaaS Product Company
- **Company**: B2B SaaS (project management, CRM, documentation platform)
- **Team Size**: 5-person engineering team
- **Scale**: 10K business customers, 100K end users
- **Challenge**: Users make typos, expect search to "just work"

## Why This Matters

**Business Problem:**
- Exact search frustrates users: "projct" finds nothing, should find "project"
- Support tickets: "Search doesn't work" (it does, user made typo)
- User churn: 23% of users who get zero search results don't return

**Pain Point:**
Current exact-match search (SQL LIKE '%query%') fails on:
- Typos: "recieve" vs "receive"
- Spelling variations: "organize" vs "organise"
- Abbreviations: "mgmt" should find "management"

**Goal:**
Implement fuzzy search that tolerates 1-2 character errors while maintaining < 100ms response time.

## Requirements

### Must-Have Features

✅ **Low latency** - < 100ms p95 response time (user-facing, interactive)
✅ **Typo tolerance** - Handle 1-2 character errors (insertion, deletion, substitution)
✅ **Relevance ranking** - Best matches first (not just all matches)
✅ **Real-time** - Search-as-you-type experience

### Nice-to-Have Features

⚪ **Phonetic matching** - "Smith" finds "Smyth"
⚪ **Synonym handling** - "car" finds "automobile"
⚪ **Highlight matches** - Show where query matched in results

### Constraints

📊 **Scale:** 100K users, ~50 searches/second peak
⏱️ **Latency:** < 100ms p95 (hard requirement for UX)
💰 **Budget:** Moderate - can spend on infrastructure if justified
🛠️ **Team:** Backend developers, not search specialists
🔒 **Accuracy:** Some false positives OK (better than zero results)

### Success Criteria

- Reduce "zero results" rate from 15% to < 3%
- Maintain < 100ms p95 latency
- > 90% user satisfaction with search results

---

## Library Evaluation

### RapidFuzz - Fit Analysis

**Must-Haves:**
- ✅ **Low latency**: < 1ms per comparison (fast enough if indexed properly)
- ✅ **Typo tolerance**: Levenshtein distance handles insertions, deletions, substitutions
- ✅ **Relevance ranking**: Similarity scores (0-100) enable ranking
- ✅ **Real-time**: Fast enough for interactive use

**Constraints:**
- 📊 **Scale**: 50 searches/sec × 100ms = 5 concurrent queries (manageable)
- ⏱️ **Latency**: **Critical challenge**: Can't compare query to all documents in < 100ms
  - **Solution**: Pre-build index (BK-tree, VP-tree, or approximate nearest neighbor)
  - **OR**: Use with search engine (Elasticsearch with RapidFuzz for scoring)
- 💰 **Budget**: Indexing structure needed (engineering time + infrastructure)
- 🛠️ **Team**: Index building requires expertise (learning curve)

**Fit Score:** 65/100 (drops due to indexing complexity)

**Note:** RapidFuzz is fast for pairwise comparisons, but not designed for retrieval. Best used in combination with indexing structure or search engine.

---

### Elasticsearch with Fuzzy Query - Fit Analysis

**Must-Haves:**
- ✅✅ **Low latency**: Inverted index + fuzzy query = < 50ms typical
- ✅ **Typo tolerance**: Built-in fuzzy query (Levenshtein distance)
- ✅✅ **Relevance ranking**: TF-IDF, BM25 scoring built-in
- ✅✅ **Real-time**: Designed for user-facing search

**Nice-to-Haves:**
- ⚪ **Phonetic**: Can add phonetic analyzers
- ⚪ **Synonyms**: Built-in synonym support
- ✅ **Highlighting**: Built-in match highlighting

**Constraints:**
- 📊 **Scale**: Designed for this exact use case
- ⏱️ **Latency**: Optimized for < 100ms (meets requirement ✅✅)
- 💰 **Budget**: Managed Elasticsearch: $50-200/month (acceptable)
- 🛠️ **Team**: Learning curve, but well-documented

**Fit Score:** 95/100

**Note:** Not a Python library, but a search engine. Includes fuzzy matching as core feature.

---

### Jellyfish (Phonetic) - Fit Analysis

**Must-Haves:**
- ⚠️ **Latency**: Need indexing structure (same issue as RapidFuzz)
- ✅ **Phonetic matching**: Soundex/Metaphone if needed
- ❌ **Relevance ranking**: No built-in ranking

**Fit Score:** 40/100

**Why Not Primary:**
- Same indexing challenge as RapidFuzz
- Slower than RapidFuzz for edit distance
- Phonetic matching not critical for this use case

---

## Comparison Matrix

| Requirement | RapidFuzz + Index | Elasticsearch | Jellyfish |
|-------------|-------------------|---------------|-----------|
| **Latency (<100ms)** | ⚠️ Needs work | ✅✅ Built-in | ⚠️ Needs work |
| **Typo tolerance** | ✅ | ✅ | ✅ |
| **Ranking** | ⚪ Manual | ✅✅ Built-in | ❌ |
| **Real-time** | ⚠️ With index | ✅✅ | ⚠️ |
| **Eng. effort** | High | Medium | High |
| **Cost/month** | $100-300 | $50-200 | $100-300 |

---

## Recommendation

### Primary: **Elasticsearch** (with fuzzy query feature)

**Fit: 95/100**

**Rationale:**

1. **Built for this exact use case**: User-facing fuzzy search is Elasticsearch's core competency
   - Inverted index for fast retrieval
   - Fuzzy query parameter for typo tolerance
   - BM25 scoring for relevance ranking

2. **Meets latency requirement**: < 50ms typical (well under 100ms SLA)

3. **Lower engineering effort**: Managed service handles indexing, scaling, optimization

4. **Complete feature set**: Highlighting, synonyms, phonetic analysis all available

**Trade-off Accepted:**
- Not a Python library (separate service)
- Ongoing cost ($50-200/month)
- Some vendor lock-in (but open-source version available)

---

### Alternative: **RapidFuzz + BK-tree Index** (if Elasticsearch not an option)

**Fit: 65/100**

**When to consider:**
- Cannot add external services (Elasticsearch)
- Need in-process Python solution
- Have engineering time to build index

**Approach:**
```python
from rapidfuzz import fuzz
import bktree  # BK-tree library for indexing

# Build index (one-time)
tree = bktree.BKTree(fuzz.ratio)
for doc in documents:
    tree.add(doc.title)

# Search (< 100ms for 10K documents)
def fuzzy_search(query, max_distance=2):
    results = tree.query(query, max_distance)
    # Returns [(distance, title), ...]
    return sorted(results, key=lambda x: x[0])
```

**Trade-off:**
- Higher engineering effort (build + maintain index)
- Custom relevance ranking logic needed
- Performance tuning required

---

## Key Insights

**S3 reveals indexing gap**: RapidFuzz is fast for comparisons but lacks retrieval index. For user-facing search, a search engine (Elasticsearch) or custom index (BK-tree) is needed.

**Latency drives architecture**: < 100ms requirement eliminates naive "compare query to all documents" approach. Must have index.

**Don't build what you can buy**: Elasticsearch exists precisely for this use case. Building custom fuzzy search with RapidFuzz + index is possible but not recommended unless constraints prevent using Elasticsearch.

---

## Validation Data

**Elasticsearch fuzzy search:**
- Latency: 20-80ms for 100K documents (meets < 100ms)
- Reduces "zero results" by 60-80% (typo tolerance works)
- Cost: $50-200/month managed service

**RapidFuzz + BK-tree:**
- Latency: 50-150ms for 10K documents (borderline)
- Engineering effort: 2-3 weeks to build + test
- Maintenance: Ongoing tuning needed
