# Provider Profile: Meilisearch Cloud

**Category**: Open-Source Search Alternative
**Market Position**: Fast-growing challenger, developer-friendly
**Est. Market Share**: ~5-10% (hosted search market)

---

## Overview

**What it is**: Open-source search engine (MIT license) with managed cloud offering, optimized for speed and developer experience

**Founded**: 2018
**Headquarters**: Paris, France
**Public**: No (Private, seed-funded)
**Employees**: ~30-50
**Open Source**: Yes (MIT license, GitHub: 46K+ stars)

**Key Value Proposition**: "Lightning-fast search API with plug-and-play simplicity" - 90% of use cases work out-of-the-box

---

## Core Capabilities

### 1. Search Performance
**Latency**: <50ms (typical), <20ms (median for small-medium datasets)
**Architecture**: Single-node or clustered deployment (high availability)
**Language**: Built in Rust (memory-safe, performant)
**Uptime**: 99.9% (cloud SLA)

**Speed Characteristics**:
- Sub-50ms search-as-you-type
- Optimized for datasets up to 10M records
- Memory-mapped storage (handles large datasets efficiently)
- Max index size: 80 TiB (Linux)

**Performance Notes**:
- Excellent for small-medium datasets (<5M records)
- Hybrid search (vector + keyword) stays within 50ms target
- Slightly slower than Typesense for very large datasets (>10M records)

---

### 2. Typo Tolerance
**Algorithm**: Edit distance (Levenshtein) with configurable thresholds
**Default Behavior**:
- 5-character word: 1 typo tolerated
- 9+ character word: 2 typos tolerated

**Configuration Options** (v1.15, 2024):
- Per-attribute typo tolerance (enable/disable per field)
- Numeric typo protection (2024 matches only 2024, not 2025)
- Minimum word length for typo tolerance (default: 5)
- Custom typo distance rules

**Example**: "javascript" matches "javascrip", "javasript", "javascritp"

**vs Competitors**:
- More configurable than Typesense
- Less sophisticated than Algolia (no phonetic matching)

---

### 3. Relevance & Ranking
**Default Algorithm**: Multi-criteria ranking with tie-breaking

**Ranking Rules** (ordered by priority):
1. Words (number of matching query terms)
2. Typo (fewer typos = higher rank)
3. Proximity (words close together)
4. Attribute (matches in important fields first)
5. Sort (custom sorting criteria)
6. Exactness (exact matches prioritized)

**Custom Ranking**:
- Sort by numeric fields (price, date, popularity)
- Multiple sort orders (requires separate indices)
- Weighted attributes (boost title vs body)

**AI/ML Features** (2024-2025):
- Hybrid search (keyword + vector embeddings)
- Semantic search (BERT/sentence-transformers)
- Vector search (built-in embedders or bring-your-own)
- Automatic embedding generation (OpenAI, HuggingFace)

**Limitations**:
- No built-in personalization (vs Algolia)
- No automatic synonym detection (manual only)
- No query categorization

---

### 4. Faceting & Filtering
**Facet Types**:
- Standard facets (count by field value)
- Hierarchical facets (category trees, limited support)
- Numeric range facets (price ranges)

**Filtering Syntax**:
- Equality: `category = "electronics"`
- Ranges: `price 100 TO 500`
- Arrays: `tags IN ["new", "sale"]`
- Boolean: `AND`, `OR`, `NOT`
- Geo-filtering: `_geoRadius(lat, lng, radius)`

**Performance**:
- Facet computation: <10ms (cached)
- Filters work seamlessly with hybrid search
- Can filter vector search results

**vs Competitors**:
- Similar to Typesense (basic faceting)
- Less advanced than Algolia (no disjunctive facets)

---

### 5. Additional Features

**Geo-Search**:
- Distance-based ranking (_geoPoint field)
- Radius filtering (_geoRadius filter)
- Bounding box search
- Sort by distance

**Multi-Tenancy**:
- Tenant tokens (secure, tenant-specific API keys)
- Document-level permissions
- Filter by tenant ID

**Highlighting**:
- HTML tags for matched terms (<em> by default)
- Customizable highlight tags
- Context snippets (surrounding text)

**Synonyms & Stop Words**:
- Manual synonym lists (no auto-detection)
- Stop words (common words to ignore)
- Multi-word synonyms supported

---

## Pricing Structure

### Free Tier (Self-Hosted)
**Cost**: $0 (open-source MIT license)

**Infrastructure Costs**:
- Small VPS: $5-20/month (1-2 GB RAM)
- Medium server: $40-100/month (4-8 GB RAM)
- Large server: $200-500/month (16-32 GB RAM)

**Includes**: All features (no paywalls)

**Best for**: Side projects, cost-sensitive startups, full control needed

---

### Build Plan (Cloud)
**Cost**: $30/month

**Includes**:
- 50,000 search requests/month (5x Algolia's free tier)
- Up to 100,000 documents
- 2 GB RAM, 1 vCPU
- 10 GB storage
- All core features (typo tolerance, faceting, geo-search)
- Hybrid/semantic search (included!)
- Email support

**Overage Pricing**:
- Searches: $0.60 per 1,000 (above 50K)
- Documents: $0.40 per 1,000 (above 100K)

**Typical Extra Costs**:
- 100K searches + 200K docs: $30 + $30 + $40 = $100/month
- 200K searches + 500K docs: $30 + $90 + $160 = $280/month

**Best for**: Small businesses, growing startups

---

### Pro Plan (Cloud)
**Cost**: $300/month

**Includes**:
- 250,000 search requests/month
- Up to 500,000 documents
- 8 GB RAM, 2 vCPU
- 50 GB storage
- Priority support (faster response times)
- Extended analytics
- Advanced monitoring

**Overage Pricing**:
- Searches: $0.40 per 1,000 (above 250K)
- Documents: $0.30 per 1,000 (above 500K)

**Typical Extra Costs**:
- 500K searches + 1M docs: $300 + $100 + $150 = $550/month
- 1M searches + 2M docs: $300 + $300 + $450 = $1,050/month

**Best for**: Mid-market, e-commerce, content platforms

---

### Resource-Based Pricing (Cloud, 2024)
**New Model**: Pay for provisioned resources (CPU, RAM, storage)

**Pricing**:
- CPU: ~$50-100/vCPU/month
- RAM: ~$10-20/GB/month
- Storage: ~$0.10-0.20/GB/month

**Example Configurations**:
- Small (2 vCPU, 4 GB RAM, 20 GB): ~$200/month
- Medium (4 vCPU, 16 GB RAM, 100 GB): ~$600/month
- Large (8 vCPU, 32 GB RAM, 500 GB): ~$1,200/month

**Benefits**:
- Predictable costs (no overage surprises)
- Control over performance (dial resources up/down)
- Transparency (bill matches real cost drivers)

**Mixed Billing**: Can run both usage-based and resource-based projects on same invoice

**Best for**: High-traffic sites, predictable workloads

---

### Enterprise (Cloud)
**Cost**: Custom pricing

**Adds to Pro**:
- Dedicated infrastructure
- Custom SLA (99.95%+)
- SAML/SSO integration
- Dedicated support (CSM, TAM)
- Professional services
- Custom contracts

**Best for**: Large enterprises, regulated industries

---

## Integration Approach

### API & SDKs
**API Type**: REST API with JSON responses

**Official SDKs** (15+ languages):
- JavaScript/TypeScript (Node.js, browser)
- React, Vue, Svelte hooks
- Python, Ruby, PHP
- Rust, Go, Java, C#, Swift, Dart

**Framework Integrations**:
- Instant Meilisearch (React, Vue, vanilla JS)
- Strapi plugin (CMS integration)
- Rails Meilisearch gem
- Laravel Scout driver
- Django Meilisearch

**Setup Time**: 15-45 minutes (plug-and-play)

---

### Indexing Methods

**API-based**:
1. POST /indexes/{index}/documents (JSON array)
2. SDK methods (addDocuments, updateDocuments)
3. Batch operations (no hard limit, but 100MB max payload)

**Indexing Speed**:
- Small batch (1,000 docs): ~500ms-2s
- Medium batch (10,000 docs): ~5-15s
- Large reindex (1M docs): ~10-30 minutes

**Real-Time Updates**: Near real-time (documents visible in <1s)

**Data Sources**:
- Database exports (JSON, CSV, NDJSON)
- CMS integrations (Strapi, WordPress via plugins)
- E-commerce (Shopify, WooCommerce via webhooks)
- Custom ETL pipelines

**No Built-In Crawlers**: Requires custom integration (vs Algolia's crawler)

---

### Search UI Components

**Instant Meilisearch**:
- InstantSearch.js adapter (Algolia-compatible UI)
- Pre-built components (searchBox, hits, pagination, refinementList)
- Compatible with Algolia's InstantSearch libraries

**Example Components**:
- SearchBox (autocomplete, instant search)
- Hits (result list with highlighting)
- RefinementList (facet filters)
- Pagination, Stats
- CurrentRefinements (active filters)

**Benefit**: Easy migration from Algolia (UI components compatible)

---

## Performance Characteristics

**Search Latency** (2024 benchmarks):
- Median: 15-25ms (small-medium datasets, <5M docs)
- P95: 30-50ms
- P99: 50-100ms (larger datasets or complex queries)

**Hybrid Search Latency**:
- Vector + keyword: <50ms (typical)
- Slight overhead vs pure keyword (~10-20ms added)

**Geographic Performance** (single-region deployment):
- Same region: 10-20ms
- Cross-continent: 50-150ms (add CDN for global performance)

**Scalability**:
- Recommended max: 10M records per index
- Tested up to: 80 TiB index size (Linux)
- Multi-node clustering: Available (high availability)

**vs Competitors**:
- Faster than Elasticsearch for small-medium datasets
- Comparable to Typesense (<5M records)
- Slower than Algolia at very high scale (>10M records)

---

## Key Differentiators

### 1. Open-Source MIT License
**What**: Truly open-source (vs Typesense's GPL, Algolia's proprietary)

**Benefits**:
- No vendor lock-in (self-host anywhere)
- Fork and customize if needed
- Commercial-friendly license
- Community contributions

**Impact**: 46K+ GitHub stars, active community

---

### 2. Plug-and-Play Simplicity
**What**: 90% of use cases work out-of-the-box with zero config

**Zero Config Features**:
- Automatic typo tolerance (no tuning needed)
- Sensible ranking defaults
- Auto-detect field types
- Instant indexing (no schema required)

**Example**: Index 100K products in 5 lines of code
```python
client = meilisearch.Client('http://localhost:7700', 'masterKey')
index = client.index('products')
index.add_documents(products)  # Done!
```

**vs Competitors**:
- Simpler than Elasticsearch (no mapping, no shards)
- More opinionated than Typesense (fewer knobs)
- Easier than Algolia (less config, more defaults)

---

### 3. Hybrid Search (Built-In, 2024)
**What**: Combine keyword + vector search in single query

**Features**:
- Automatic embedding generation (OpenAI, HuggingFace)
- Bring-your-own embeddings
- Weighted hybrid (adjust keyword vs vector balance)
- Filter hybrid results (price, category, etc.)

**Example Use Cases**:
- Semantic product search ("shoes for running")
- Cross-lingual search (query in English, match French docs)
- Image search (CLIP embeddings)

**Pricing**: Included in all plans (no upcharge vs Algolia's enterprise-only NeuralSearch)

---

### 4. Memory-Mapped Architecture
**What**: Rust-based engine with memory-mapped files (LMDB)

**Benefits**:
- Handles datasets larger than RAM (up to 80 TiB)
- Fast cold starts (no index loading delay)
- Efficient memory usage
- OS-level caching

**vs Competitors**:
- Better than Typesense (in-memory only, RAM = max dataset)
- Different than Algolia (distributed architecture)

---

## Developer Experience

**Documentation Quality**: 4.5/5
- Excellent getting started guides
- Interactive tutorials
- Comprehensive API reference
- Good examples (code snippets)

**Areas for Improvement**:
- Less video content than Algolia
- Fewer enterprise case studies

**Community**:
- Discord (2,000+ members, very active)
- GitHub discussions
- Stack Overflow (meilisearch tag)

**Support**:
- Self-hosted: Community support (Discord, GitHub)
- Build: Email support (48-hour response)
- Pro: Priority email (8-hour response)
- Enterprise: Dedicated support (1-4 hour response)

**Monitoring**:
- Built-in stats API (query count, latency)
- Prometheus metrics (self-hosted)
- Cloud dashboard (managed service)

---

## Pros

✅ **Open-source (MIT)** - no vendor lock-in, self-host option
✅ **Affordable pricing** - 5-10x cheaper than Algolia (50K searches for $30/month)
✅ **Fast performance** - sub-50ms for small-medium datasets
✅ **Plug-and-play simplicity** - 90% of use cases work with zero config
✅ **Hybrid search included** - semantic + keyword search (no upcharge)
✅ **Excellent DX** - simple API, great docs, active community
✅ **Generous free tier** - 50K searches vs Algolia's 10K
✅ **Resource-based pricing option** - predictable costs, no overage surprises
✅ **Instant migration from Algolia** - InstantSearch.js adapter

---

## Cons

❌ **No built-in personalization** - requires custom implementation (vs Algolia)
❌ **Limited merchandising tools** - no visual studio (vs Algolia Premium)
❌ **Basic analytics** - no click/conversion tracking (vs Algolia)
❌ **No built-in crawler** - requires custom data ingestion (vs Algolia)
❌ **Smaller team** - 30-50 employees vs Algolia's 800+
❌ **Limited geo-distribution** - single-region deployment (cloud), no automatic DSN
❌ **No A/B testing** - requires external tools
❌ **Weaker at very high scale** - <10M records sweet spot (vs Algolia's unlimited)
❌ **No auto-synonym detection** - manual synonyms only (vs Algolia AI Synonyms)

---

## Best Use Cases

### Excellent For:
- **Budget-conscious startups** - need fast search without breaking the bank
- **Small-medium datasets** - <5M records, <500K searches/month
- **Developer-centric products** - SaaS apps, documentation sites
- **Self-hosted preference** - full control, no cloud vendor
- **Hybrid/semantic search** - AI-powered search without enterprise pricing
- **Simple e-commerce** - product catalogs, basic filtering
- **Content platforms** - blogs, media sites, knowledge bases
- **Open-source projects** - MIT license, community-friendly

### Consider Alternatives For:
- **Very large datasets** - >10M records (Algolia, Elasticsearch better)
- **Complex merchandising** - visual rules, campaigns (need Algolia Premium)
- **Advanced personalization** - user profiling, dynamic re-ranking (Algolia)
- **Global distribution needed** - <50ms worldwide (Algolia DSN)
- **Enterprise analytics** - click tracking, attribution (Algolia, Coveo)
- **Built-in crawler** - automatic site indexing (Algolia, Elastic)

---

## Migration Considerations

### Migrating TO Meilisearch:
**From Algolia**:
- Effort: 3-7 days (low-moderate)
- Data export: 1 day (via API)
- Index config: 1-2 days (map ranking rules)
- Frontend: 1-2 days (Instant Meilisearch adapter = drop-in)
- Testing: 1-2 days

**Risk**: Low (InstantSearch UI compatible, parallel run easy)

**From Elasticsearch**:
- Effort: 5-10 days (moderate)
- Query translation: 2-3 days (DSL to Meilisearch params)
- Ranking tuning: 2-3 days (match relevance)
- Frontend: 2-4 days (rebuild UI)

---

### Migrating FROM Meilisearch:
**Effort**: 1-3 weeks (depends on destination)

**To Algolia**:
- Effort: 1-2 weeks
- Data migration: 2-3 days
- Ranking config: 3-5 days (map custom rules)
- UI: 0 days (already using InstantSearch.js)
- Cost: Increases 5-10x

**To Self-Hosted Meilisearch**:
- Effort: 1-3 days (very low)
- Export data from cloud → import to self-hosted
- Update API endpoint
- Risk: Very low (same API)

**Lock-in**: LOW - open-source, standard API, easy export

---

## Vendor Viability

**Financial Health**: 3.5/5
- Private company (seed funded, ~$5M)
- Revenue: <$10M (estimated, 2024)
- Growth: 100%+ YoY (small base)
- Profitable: No (growth stage)
- Burn rate: Low (small team)

**Open Source Safety Net**: High - even if company shuts down, MIT codebase continues

**Longevity**: 6 years (founded 2018)
**Acquisition Risk**: Moderate-high (attractive target for larger search vendors)
**5-year survival**: 80% (company), 95% (open-source project)
**10-year survival**: 60% (company), 90% (open-source project)

**Competitors**: Algolia, Typesense, Elasticsearch, AWS OpenSearch

---

## Verdict: Best Value for Small-Medium Projects

**Rating**: 4.5/5

**Summary**: Meilisearch offers exceptional value for small-medium projects, combining Algolia-like speed and developer experience with open-source flexibility and 5-10x lower costs. The MIT license and plug-and-play simplicity make it ideal for budget-conscious startups and developers who want fast search without vendor lock-in.

**When to use**:
- ✅ Budget <$500/month for search infrastructure
- ✅ Dataset <5M records, <500K searches/month
- ✅ Need hybrid/semantic search (included, no upcharge)
- ✅ Want open-source flexibility (MIT license, self-host option)
- ✅ Prefer plug-and-play simplicity over configuration complexity
- ✅ Migrating from Algolia to reduce costs (InstantSearch compatible)

**When to consider alternatives**:
- ❌ Need global <50ms latency (use Algolia DSN)
- ❌ Require advanced merchandising (Algolia Premium, Coveo)
- ❌ Dataset >10M records (Algolia, Elasticsearch scale better)
- ❌ Need built-in personalization (Algolia, Coveo)
- ❌ Want comprehensive analytics (click tracking, attribution - use Algolia)

**Best Alternative If**:
- Even lower cost + self-host: Typesense (GPL, fixed cluster pricing)
- Need enterprise features: Algolia (but 5-10x more expensive)
- Massive scale (>10M docs): Elasticsearch, AWS OpenSearch
