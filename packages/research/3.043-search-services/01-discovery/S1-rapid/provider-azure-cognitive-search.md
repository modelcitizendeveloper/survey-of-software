# Provider Profile: Azure AI Search (formerly Cognitive Search)

**Category**: Enterprise AI-Powered Search
**Market Position**: Microsoft ecosystem leader, AI-first
**Est. Market Share**: ~5-10% (enterprise search market)

---

## Overview

**What it is**: Fully managed AI-powered search service with cognitive skills, integrated with Azure ecosystem

**Founded**: 2014 (as Azure Search), rebranded 2019 (Cognitive Search), 2024 (AI Search)
**Parent**: Microsoft Azure
**Public**: Part of Microsoft (NASDAQ: MSFT)
**Open Source**: No (proprietary)

**Key Value Proposition**: "AI-powered cloud search service for mobile and web app development" - deep AI integration for content understanding

---

## Core Capabilities

### 1. Search Performance
**Latency**: 50-300ms (typical), depends on query complexity and tier
**Architecture**: Distributed, partitioned index architecture
**Language**: Proprietary (Azure-native)
**Uptime**: 99.9% SLA (3+ replicas)

**Speed Characteristics**:
- Comparable to Elasticsearch for full-text search
- Slower than Algolia/Typesense for simple queries
- Optimized for AI-enriched content
- Performance varies by tier (Basic, Standard, Storage Optimized)

**Performance Notes**:
- Higher-capacity partitions (April 2024): Larger partitions at same billing rate
- Vector quotas increased: Better support for semantic/hybrid search
- Still optimizing for sub-50ms (not primary goal vs Algolia)

---

### 2. Typo Tolerance (Fuzzy Search)
**Algorithm**: Edit distance with phonetic matching
**Configuration**: Automatic or configurable per-query

**Fuzzy Query Options**:
- fuzzySearch parameter (true/false)
- Edit distance: 1 or 2 (maxEditDistance)
- Prefix length: Skip first N characters from fuzzy matching
- Phonetic search: Soundex algorithm for name matching

**vs Competitors**:
- Better than Elasticsearch (more automatic)
- Not as sophisticated as Algolia (less tuning)
- Good enough for most use cases

---

### 3. Relevance & Ranking
**Default Algorithm**: BM25 (TF-IDF variant)

**Scoring Profiles**:
- Custom scoring (boost by field values, functions)
- Magnitude boosting (numeric fields)
- Freshness boosting (date fields)
- Distance boosting (geospatial)
- Tag boosting (category matching)

**AI-Powered Ranking** (2024-2025):
- Semantic search (L2 reranking with AI)
- Vector search (k-NN, HNSW algorithm)
- Hybrid search (BM25 + semantic + vector)
- Reranking (semantic reranker for top results)

**Semantic Ranking**:
- Two-stage ranking: BM25 first pass, AI reranking top 50
- Microsoft-trained models (multilingual)
- Query understanding (intent, context)

**Custom Ranking**:
- Scoring profiles (boost by recency, popularity, location)
- Field weights (title 3x more important than body)
- Functions (linear, logarithmic, Gaussian curves)

---

### 4. Faceting & Filtering
**Facet Types**:
- Value facets (discrete values with counts)
- Range facets (numeric, date ranges)
- Dynamic faceting (top N values)

**Filtering**:
- OData filter syntax (eq, ne, gt, lt, and, or, not)
- Range filters (price ge 10 and price le 100)
- Collection filters (tags/any(t: t eq 'new'))
- Geo-spatial filters (geo.distance, geo.intersects)

**Performance**:
- Facets computed efficiently (indexed)
- Filters applied before scoring (performance optimization)
- Can combine facets + filters + semantic ranking

**vs Competitors**:
- Similar to Elasticsearch (OData syntax vs JSON DSL)
- More structured than Algolia (less flexible)
- Good for .NET developers (familiar OData syntax)

---

### 5. AI Cognitive Skills

**Built-In Skills** (unique differentiator):
- OCR (extract text from images)
- Language detection (identify document language)
- Key phrase extraction (summarize content)
- Entity recognition (people, places, organizations)
- Sentiment analysis (positive, negative, neutral)
- Image analysis (objects, faces, landmarks)
- Translation (50+ languages)
- PII detection & redaction

**Custom Skills**:
- Azure Functions (custom enrichment logic)
- Machine Learning models (bring-your-own models)
- OpenAI integration (GPT, embeddings)

**Knowledge Store**:
- Persist enriched data (Azure Storage, Cosmos DB)
- Reuse enrichments across applications
- Build knowledge graphs

**Use Case**: Index PDFs, extract text, translate, identify entities, enable semantic search

---

## Pricing Structure

### Free Tier
**Cost**: $0/month

**Limits**:
- 3 indexes, 50 MB total storage
- 10,000 documents
- 3 indexers, 3 data sources
- No SLA, no replicas

**Best for**: Development, testing, small projects

---

### Basic Tier
**Cost**: $75/month (us-east)

**Includes**:
- 15 indexes, 2 GB storage
- 1 partition, up to 3 replicas
- Up to 10M documents (depending on doc size)
- 99.9% SLA (with 3 replicas)

**Best for**: Small production apps, <1M docs

---

### Standard Tiers (S1, S2, S3)
**S1**: $250/month (us-east)
- 50 indexes, 25 GB storage per partition
- Up to 12 partitions, 12 replicas
- ~25M documents per partition

**S2**: $1,000/month
- 200 indexes, 100 GB storage per partition
- Up to 12 partitions, 12 replicas
- ~100M documents per partition

**S3**: $4,000/month
- 200 indexes, 200 GB storage per partition
- Up to 12 partitions, 12 replicas
- ~200M documents per partition

**High Density (S3 HD)**: $3,000/month
- 1,000 indexes, 200 GB storage (shared)
- 3 partitions, 3 replicas
- Multi-tenancy scenarios (many small indexes)

**Best for**: Production apps, mid-market to enterprise

---

### Storage Optimized (L1, L2)
**L1**: $2,000/month
- 10 indexes, 1 TB storage per partition
- Up to 12 partitions, 12 replicas
- ~1B documents per partition

**L2**: $4,000/month
- 10 indexes, 2 TB storage per partition
- Up to 12 partitions, 12 replicas
- ~2B documents per partition

**Best for**: Large datasets, log analytics, archival search

---

### Add-Ons (2024)
**Semantic Search**: Included (pay for compute usage)
- Standard tier: First 1,000 queries free/month
- Additional: ~$0.01-0.05 per query (depends on complexity)

**AI Enrichment**: Pay-per-use (Azure Cognitive Services)
- OCR: $1-5 per 1,000 pages
- Entity extraction: $1-3 per 1,000 documents
- Image analysis: $1-2 per 1,000 images
- Translation: $10 per million characters

**Typical Total Cost** (S1 + AI enrichment):
- 1M docs, 100K searches, minimal AI: ~$250-300/month
- 1M docs, 100K searches, heavy AI: ~$500-800/month

---

## Integration Approach

### API & SDKs
**API Type**: REST API with OData query syntax

**Official Azure SDKs** (10+ languages):
- .NET (C#, F#)
- Python (azure-search-documents)
- JavaScript/TypeScript (Node.js, browser)
- Java, Go

**Authentication**:
- API keys (admin, query keys)
- Azure AD (role-based access control)
- Managed identities (for Azure services)

**Setup Time**: 1-3 hours (.NET developers), 2-6 hours (others)

---

### Indexing Methods

**Push API**:
- Upload documents via REST API (JSON)
- Batch operations (up to 1,000 docs or 16 MB per batch)
- Indexing speed: 1,000-10,000 docs/sec (depends on tier)

**Pull API (Indexers)**:
- Automatic data extraction from sources
- Scheduled indexing (every N minutes/hours/days)
- Change detection (only index new/modified docs)

**Data Sources**:
- Azure SQL Database, Cosmos DB, Blob Storage, Table Storage
- Azure Data Lake Storage
- SharePoint Online (via Graph connector)
- Custom (via REST API)

**AI Enrichment Pipeline** (unique):
1. Indexer pulls data (e.g., PDFs from Blob Storage)
2. Cognitive Skills extract text, entities, sentiment
3. Enriched data indexed in search service
4. Knowledge Store persists enrichments (optional)

**Real-Time**: Near real-time (indexing delay ~1-10s)

---

### Search UI

**Azure Portal Search Explorer**: Built-in testing UI (not for production)

**No Pre-Built Components**: Must build custom UI (vs Algolia InstantSearch)

**Third-Party**:
- Custom React/Angular/Vue components (most common)
- Azure Cognitive Search JavaScript SDK (basic helpers)

---

## Performance Characteristics

**Search Latency** (typical):
- Simple full-text: 50-150ms
- Semantic search: 100-300ms (AI reranking adds overhead)
- Hybrid search: 150-400ms (BM25 + vector + semantic)
- Complex aggregations: 200ms-2s

**Geographic Performance**:
- Single region: 50-150ms
- Cross-region: 150-500ms
- No global CDN (vs Algolia DSN), but can deploy in multiple Azure regions

**Scalability**:
- Horizontal scaling (add partitions)
- Vertical scaling (upgrade tier)
- Max: 12 partitions x 12 replicas = 144 units (S3)
- Storage Optimized: Up to 24 TB per service (L2, 12 partitions)

**vs Competitors**:
- Slower than Algolia/Typesense for simple search
- Comparable to Elasticsearch for full-text
- AI enrichment adds latency (trade-off for semantic understanding)

---

## Key Differentiators

### 1. AI Cognitive Skills Pipeline
**What**: Built-in AI enrichment during indexing

**Capabilities**:
- Extract text from PDFs, images (OCR)
- Translate documents (50+ languages)
- Identify entities, key phrases, sentiment
- Analyze images (objects, faces, scenes)
- Custom skills (Azure Functions, OpenAI)

**Use Case**: Index 10,000 PDFs, extract text, identify people/organizations, enable semantic search

**vs Competitors**: Unique - no other search service has built-in AI enrichment pipeline

---

### 2. Azure Ecosystem Integration
**What**: Native integration with Microsoft/Azure services

**Integrations**:
- Azure Active Directory (SSO, RBAC)
- Azure Storage (Blob, Data Lake)
- Azure SQL, Cosmos DB (auto-indexing)
- Power BI (search analytics dashboards)
- SharePoint, Teams (enterprise search)
- Azure OpenAI (GPT, embeddings for RAG)

**Benefit**: If in Microsoft ecosystem, Azure AI Search is natural choice

---

### 3. Semantic Search with L2 Reranking
**What**: AI-powered relevance (Microsoft-trained models)

**How It Works**:
1. BM25 first-pass ranking (retrieve top 50 results)
2. AI semantic reranking (deep understanding, context)
3. Return top results (reordered by semantic relevance)

**Benefits**:
- Better than pure BM25 (understands intent, synonyms, context)
- Faster than pure vector search (hybrid approach)
- Multilingual (works across 50+ languages)

**Example**: Query "best laptop for programming" matches "developer workstation" semantically

---

### 4. Knowledge Store
**What**: Persist AI-enriched data for reuse

**Destinations**:
- Azure Storage (tables, blobs)
- Cosmos DB (JSON documents)

**Use Cases**:
- Build knowledge graphs
- Power BI analytics on enriched data
- Share enrichments across apps

**vs Competitors**: Unique - separate enrichment from search index

---

## Developer Experience

**Documentation Quality**: 4/5
- Comprehensive Microsoft docs
- Quickstarts, tutorials, samples
- API reference (REST, SDKs)
- Video content (Microsoft Learn)

**Complexity**: Moderate-high
- OData syntax learning curve (for non-.NET devs)
- AI enrichment pipeline requires understanding
- Less complex than Elasticsearch, more than Algolia

**Community**:
- Microsoft Q&A forums (active)
- Stack Overflow (azure-cognitive-search tag)
- GitHub samples (official repos)

**Support**:
- Azure Support plans (Basic, Developer, Standard, Professional Direct)
- Developer: $29/month (8-hour response)
- Standard: $100/month (1-hour critical response)
- Professional Direct: $1,000/month (1-hour + TAM)

**Monitoring**:
- Azure Monitor (metrics, logs, alerts)
- Search traffic analytics (query logs, latency)
- Application Insights integration

---

## Pros

✅ **AI enrichment pipeline** - unique built-in OCR, entity extraction, translation
✅ **Azure ecosystem integration** - seamless with Azure services, AD, SharePoint
✅ **Semantic search** - AI-powered relevance (L2 reranking) out-of-the-box
✅ **Knowledge Store** - persist enrichments for reuse
✅ **Hybrid search** - BM25 + vector + semantic (best of all worlds)
✅ **Enterprise-ready** - RBAC, compliance (SOC, HIPAA, ISO)
✅ **Auto-indexing** - pull from Azure SQL, Cosmos DB, Blob Storage
✅ **Higher partitions (2024)** - better value (same price, more capacity)
✅ **Multilingual** - 56 languages for semantic search

---

## Cons

❌ **Azure-only** - locked to Microsoft ecosystem (vs multi-cloud)
❌ **Slower than specialized search** - 50-300ms vs Algolia/Typesense <50ms
❌ **Complex pricing** - tier + partitions + replicas + AI enrichment
❌ **No pre-built UI** - must build custom (vs Algolia InstantSearch)
❌ **OData syntax** - learning curve (vs simple REST params)
❌ **AI enrichment costs** - can add significant expense ($100-500+/month)
❌ **Less mature than Elasticsearch** - smaller ecosystem, fewer plugins
❌ **Not open-source** - proprietary (vs OpenSearch, Meilisearch)
❌ **Limited free tier** - 50 MB (vs Meilisearch 1M records free)

---

## Best Use Cases

### Excellent For:
- **Azure-native applications** - already on Azure, use AD, Storage, SQL
- **Content-heavy sites** - need OCR, entity extraction, translation
- **Enterprise search** - SharePoint, Teams, intranet search
- **Semantic/hybrid search** - AI-powered relevance without custom ML
- **Multilingual content** - 56 languages supported
- **Document processing** - index PDFs, extract entities, enable search
- **RAG pipelines** - integrate with Azure OpenAI for LLM apps
- **Knowledge management** - build knowledge graphs with Knowledge Store

### Consider Alternatives For:
- **Multi-cloud/cloud-agnostic** - use Algolia, Meilisearch, Typesense
- **Simple product search** - Algolia, Meilisearch faster and easier
- **Low-latency requirement** - <50ms (Algolia, Typesense)
- **Budget-conscious** - Meilisearch, Typesense cheaper
- **Open-source preference** - use OpenSearch, Meilisearch, Typesense
- **Non-Azure infrastructure** - vendor-agnostic solutions better

---

## Migration Considerations

### Migrating TO Azure AI Search:
**Effort**: 2-4 weeks (moderate-high)
- Azure account setup: 1 day
- Data migration: 3-5 days (depends on source)
- Index schema design: 2-3 days
- AI enrichment pipeline: 3-7 days (if using cognitive skills)
- Query integration: 3-5 days (OData learning curve)
- Testing: 3-5 days
- Risk: Moderate (test AI enrichment thoroughly)

---

### Migrating FROM Azure AI Search:
**Effort**: 3-6 weeks (high effort)

**To Elasticsearch/OpenSearch**:
- Effort: 3-4 weeks
- Data export: 2-3 days
- Query rewrite: 1-2 weeks (OData → JSON DSL)
- Lose: AI enrichment pipeline (must rebuild externally)
- Risk: High (AI enrichments hard to replicate)

**To Algolia/Meilisearch**:
- Effort: 3-5 weeks
- Query rewrite: 1-2 weeks (OData → simple API)
- Ranking tuning: 1-2 weeks
- Lose: AI enrichment, semantic search
- Risk: High (test relevance carefully)

**Lock-in**: MODERATE-HIGH - Azure-specific (AD, Storage), AI enrichment hard to replicate

---

## Vendor Viability

**Financial Health**: 5/5
- Backed by Microsoft (3 trillion-dollar company)
- Azure growth: 29% YoY (2024)
- AI Search integral to Microsoft AI strategy

**Longevity**: 10+ years (Azure Search since 2014)
**Acquisition Risk**: None (part of Microsoft)
**5-year survival**: 99.9%
**10-year survival**: 99.5%

**Competition**: Google Vertex AI Search, AWS Kendra, Algolia, Elastic Cloud

---

## Verdict: Best for Azure-Native AI-Powered Search

**Rating**: 4.5/5 (if on Azure + need AI), 3/5 (if multi-cloud)

**Summary**: Azure AI Search excels in AI-powered content understanding with unique built-in cognitive skills for OCR, entity extraction, and translation. The semantic search with L2 reranking provides excellent relevance out-of-the-box. Best for Azure-native applications, especially document-heavy use cases requiring AI enrichment.

**When to use**:
- ✅ Already on Azure (use AD, Storage, SQL, Cosmos DB)
- ✅ Need AI enrichment (OCR, entity extraction, translation)
- ✅ Document-heavy content (PDFs, images, multilingual)
- ✅ Enterprise search (SharePoint, Teams integration)
- ✅ Semantic/hybrid search (AI-powered relevance)
- ✅ RAG pipelines (integrate with Azure OpenAI)
- ✅ Knowledge management (Knowledge Store)

**When to consider alternatives**:
- ❌ Multi-cloud or cloud-agnostic (use Algolia, Meilisearch, Elastic Cloud)
- ❌ Simple product search (Algolia, Meilisearch, Typesense faster/easier)
- ❌ Need <50ms latency (Algolia, Typesense)
- ❌ Budget-conscious startup (Meilisearch, Typesense cheaper)
- ❌ No Azure presence (vendor-agnostic better)
- ❌ Open-source requirement (use OpenSearch, Meilisearch)

**Best Alternative If**:
- AWS ecosystem: AWS OpenSearch, AWS Kendra
- Google Cloud: Vertex AI Search
- Multi-cloud: Algolia (premium), Meilisearch (budget), Elastic Cloud
- Simple search: Algolia, Typesense, Meilisearch
