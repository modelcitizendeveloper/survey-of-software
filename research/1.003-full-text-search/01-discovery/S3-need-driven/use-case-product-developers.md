# Use Case: Product Developers (User-Facing Search)

## Who Needs This

**Persona**: Full-stack or backend developers building web applications where search is a core user-facing feature.

**Context**:
- Building e-commerce platforms, SaaS products, content management systems, or internal tools
- Search is expected by users (not optional)
- Performance directly impacts user experience and conversion rates
- Working with Python (Django, FastAPI, Flask)
- Dataset size: 10K-1M documents typically

**Team size**: 1-10 developers, small to mid-size startups or internal teams

**Budget constraints**: Limited infrastructure budget, prefer self-hosted to avoid $200-500/month managed service costs

---

## Why They Need Full-Text Search

**Primary problem**: Users need to find products, articles, records, or resources quickly within the application.

**Business impact**:
- Poor search = frustrated users = churn
- Fast search (<50ms) = better UX = higher engagement
- Relevant results = more conversions (e-commerce) or productivity (internal tools)

**Example scenarios**:
- **E-commerce**: "Find all waterproof hiking boots under $150"
- **Knowledge base**: "Search 50K support articles for solutions"
- **Internal tool**: "Find customer records by partial name or company"

**Why NOT just database LIKE queries**:
- SQL `LIKE '%term%'` is slow (O(n) full table scan)
- No relevance ranking (BM25)
- No fuzzy matching or typo tolerance
- No phrase search or boolean operators

---

## Their Requirements

### Performance Requirements
- **Query latency**: <50ms (ideally <10ms)
- **User-facing**: Every extra 100ms latency costs engagement
- **Throughput**: 10-100 queries/second during peak hours

### Scale Requirements
- **Initial**: 10K-50K documents
- **Growth**: Plan for 100K-1M over 2 years
- **Update frequency**: Daily bulk updates OR real-time incremental

### Feature Requirements (Priority Order)
1. **BM25 ranking** - Relevance is non-negotiable
2. **Phrase search** - "machine learning" (exact phrase)
3. **Prefix matching** - Autocomplete-style search
4. **Multi-field search** - Search across title, description, tags
5. **Filters** - Category, price range, date filters
6. **Fuzzy search** - Handle typos (nice-to-have)

### Installation Constraints
- **Deployment**: Docker containers, VM, or PaaS (Heroku, Railway)
- **Maintenance**: Minimal; can't dedicate a team to search infrastructure
- **Dependencies**: pip install preferred; system packages acceptable if documented

### Budget Reality
- **Infrastructure**: <$50/month for search (VPS, storage)
- **Development time**: 1-2 weeks for integration (not months)

---

## Library Selection Criteria (From S1)

### Top Priority: Performance
From S1, performance gap is **240×** (Tantivy 0.27ms vs Whoosh 64ms).

**Decision rule**:
- If search is user-facing → **Compiled libraries required** (Tantivy, Xapian, Pyserini)
- If internal tool + latency <100ms OK → **Pure Python acceptable** (Whoosh)

### Evaluation Against S1 Libraries

| Library | Fits? | Why / Why Not |
|---------|-------|---------------|
| **Tantivy** | ✅ Perfect | <10ms latency, scales to 10M docs, easy install (wheel), MIT license |
| **Xapian** | ✅ Good | <10ms latency, 100M+ docs, GPL license (check commercial terms) |
| **Pyserini** | ⚠️ Maybe | Fast, but JVM overhead (Java 21+ required), overkill for <1M docs |
| **Whoosh** | ⚠️ Acceptable | Pure Python (easy), but 64ms latency = marginal UX, aging codebase |
| **lunr.py** | ❌ Too Small | In-memory only, <10K docs ceiling, not production-ready |

### Recommended Choice
**Primary**: **Tantivy**
- 240× faster than pure Python
- Pre-built wheels (3.9MB) = easy deployment
- Scales to 10M documents (headroom for growth)
- MIT license (commercial-friendly)

**Fallback**: **Whoosh** (if pure Python is mandatory constraint)
- Zero dependencies
- Acceptable for internal tools (not user-facing)

---

## When to Consider Managed Services

**Trigger points for Path 3 (Algolia, Elasticsearch Cloud, Typesense Cloud)**:

### Scale Triggers
- **>1M documents** - Self-hosted Tantivy approaches RAM limits (8-16GB indexes)
- **>1000 QPS** - Need distributed search, load balancing
- **Multi-region** - Users in US, EU, Asia need geo-distributed search

### Feature Triggers
- **Personalization** - User-specific ranking, A/B testing
- **Advanced analytics** - Click-through tracking, query insights
- **Spell correction** - Beyond basic fuzzy matching
- **Synonym management** - Business-specific synonym rules

### Team Triggers
- **Dedicated search team** - If search becomes mission-critical enough to warrant a team, managed services reduce operational overhead
- **24/7 uptime SLA** - Self-hosted requires on-call rotation

### Cost Crossover
**DIY costs** (Tantivy on VPS):
- 1M docs: ~$50/month (8GB RAM VPS)
- Engineering time: 2 weeks initial + 2 hours/month maintenance

**Managed costs** (Algolia/Typesense):
- 1M records: ~$200-500/month
- Engineering time: 1 week initial + 0 hours/month maintenance

**Break-even**: When engineering time × hourly rate > service delta, managed wins.

---

## Real-World Examples

**Who uses DIY full-text search?**:
- **Documentation sites**: Python Docs, Django Docs (static search)
- **Startups (0-50K users)**: Cost-conscious, technical teams
- **Internal tools**: Where $500/month managed service isn't justified

**Who migrates to managed?**:
- **Scale-ups (50K+ users)**: Algolia, Elasticsearch Cloud
- **E-commerce at scale**: When search becomes revenue-critical
- **Global products**: Need multi-region search

---

## Success Metrics

How product developers know their library choice is working:

✅ **Good fit indicators**:
- Search latency consistently <50ms (p95)
- Index updates complete in <1 hour
- Memory usage <8GB for dataset size
- Users report relevant results

⚠️ **Warning signs to reconsider**:
- Latency degrading over time (>100ms p95)
- Index size growing faster than expected (>10GB per 1M docs)
- Engineering team spending >1 day/week on search maintenance
- Missing features users request (personalization, analytics)

---

## Validation Against S1 Findings

S1 concluded:
- **Tantivy** = top pick for production user-facing search
- **Path 1 (DIY) viable up to 10M documents**

**S3 validation**: Product developers are the PERFECT fit for Tantivy:
- Need performance (✅ Tantivy delivers <10ms)
- Cost-conscious (✅ DIY saves $200-500/month)
- Technical team (✅ Can handle pip install + basic deployment)
- Scale range fits (✅ 10K-1M docs typical, Tantivy scales to 10M)

**Alignment**: S1 findings directly address product developer needs.
