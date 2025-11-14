# S3 Scenario 1: E-Commerce Product Catalog Search

**Company Profile**: Mid-market e-commerce platform, product-focused business model
**Search Volume**: 500K products, 2M searches/month, seasonal spikes (3-5× Black Friday)
**Budget**: $500-5K/month for search infrastructure
**Priority**: Conversion rate optimization, sub-50ms latency, merchandising control

---

## Business Context

### Company Details
- **Stage**: Series A/B, established revenue
- **Team Size**: 15-30 engineers, 2-3 on search/discovery
- **Users**: 500K-2M MAU (Monthly Active Users)
- **Revenue**: $5M-50M ARR
- **Growth**: 50-100% YoY, seasonal peaks (Q4 = 3-5× normal traffic)
- **Business Model**: Direct-to-consumer e-commerce, 20-40% margins

### Technical Environment
- **Stack**: React/Next.js frontend, Node.js/Python backend, PostgreSQL primary DB
- **Infrastructure**: AWS (S3, EC2, RDS) or Vercel/Shopify Plus
- **Product Catalog**: 500K SKUs (100K active, 400K long-tail)
- **Search Traffic**: 2M searches/month (40% of sessions start with search)
- **Conversion**: Search converts 3-5× better than browse (15% vs 3-5%)
- **Geographic Distribution**: 60% US, 25% Europe, 10% APAC, 5% other

### Search Requirements
- **Latency**: <50ms p95 (instant search, no perceived delay)
- **Faceting**: 15-30 facets (category, price, brand, color, size, rating, availability)
- **Autocomplete**: <10ms, query suggestions + product suggestions
- **Typo Tolerance**: 2-edit distance, fuzzy matching
- **Ranking**: Relevance + business rules (inventory, margin, conversion)
- **Merchandising**: Boosting, pinning, burying products (business user control)
- **A/B Testing**: Experiment with ranking, UI, query rules
- **Analytics**: Real-time (traffic, conversion, revenue per query)

---

## Search Platform Evaluation

### Evaluation Criteria

| Criterion | Weight | Algolia | Meilisearch | Typesense | Azure AI Search | Notes |
|-----------|--------|---------|-------------|-----------|----------------|-------|
| **Performance (<50ms)** | 25% | 10/10 | 9/10 | 9/10 | 6/10 | Algolia/Meili/Type only sub-50ms |
| **Merchandising UI** | 20% | 10/10 | 2/10 | 2/10 | 4/10 | Algolia dashboard, others DIY |
| **Cost Efficiency** | 15% | 4/10 | 9/10 | 10/10 | 7/10 | Algolia 5-10× more expensive |
| **Faceting/Filtering** | 15% | 10/10 | 9/10 | 9/10 | 8/10 | All handle complex facets well |
| **Analytics Built-in** | 10% | 10/10 | 1/10 | 1/10 | 3/10 | Algolia comprehensive, others DIY |
| **Ranking Control** | 10% | 10/10 | 7/10 | 7/10 | 8/10 | Algolia most flexible |
| **Implementation Time** | 5% | 9/10 | 9/10 | 8/10 | 6/10 | Algolia/Meili fastest (1-3 days) |
| **Total Score** | 100% | **8.8/10** | **6.7/10** | **7.0/10** | **6.3/10** | Algolia wins on features |

### Winner: Algolia (for mid-market e-commerce with merchandising needs)
### Alternative: Typesense (for cost-conscious teams without merchandising UI requirements)

---

## Platform Deep Dive

### Option 1: Algolia Grow/Premium (Recommended)

**Pricing**:
- Grow: $245/month base (100K records, 1M searches) + $0.50/1K searches after
- Grow Plus: $1,485/month (1M records, 10M searches, NeuralSearch)
- Premium: Custom ($5K-25K/month, merchandising UI, ML ranking, priority support)

**2M searches/month pricing**:
- Grow: $245 + (1M extra searches × $0.50/1K) = **$745/month**
- Grow Plus (if 10M/month): **$1,485/month**
- Premium (500K products): **$5K-10K/month**

**Pros**:
- ✅ **10-20ms latency** (70+ PoPs, global CDN, best-in-class performance)
- ✅ **Merchandising UI** (dashboard for business users, no-code boosting/pinning)
- ✅ **Built-in analytics** (search analytics, revenue attribution, conversion tracking)
- ✅ **InstantSearch UI** (React/Vue/Angular components, 80% of UI pre-built)
- ✅ **A/B testing** (query rules, ranking experiments, statistical significance)
- ✅ **Typo tolerance** (2-edit distance, prefix matching, word splitting)
- ✅ **99.99% SLA** (Grow Plus/Premium, downtime = revenue loss)

**Cons**:
- ⚠️ **Expensive at scale** (2M searches = $745/month, 10M searches = $1,485/month)
- ⚠️ **Usage-based pricing** (unpredictable spikes during Black Friday = 3-5× bill)
- ⚠️ **Vendor lock-in** (proprietary API, merchandising UI, analytics = hard to migrate)

**TCO (3-year, 2M searches/month avg, 5M peak)**:
- **Grow plan**: $745/month × 36 months = $26,820
- **Peak month overage** (Black Friday, 5M searches): $745 + (4M extra × $0.50/1K) = $2,745/month × 3 months/year = $8,235
- **Total license**: $26,820 + $8,235 = **$35,055**
- **Engineering** (setup 40h + maintenance 5h/month): 40 + (5 × 36) = 220 hours × $100 = **$22,000**
- **Total TCO**: **$57,055** (3-year)

**When to Choose Algolia**:
- Need merchandising UI (business users manage search, not engineers)
- Search is revenue driver (15%+ conversion rate, high AOV)
- Budget $745-2K/month (mid-market, not early-stage)
- Global audience (need <50ms worldwide, 70+ PoPs)

**ROI Calculation**:
- **Baseline conversion** (browse): 3-5%
- **Search conversion** (Algolia): 15-20% (3-5× better)
- **Revenue impact**: 40% of sessions search × (15% - 5% conversion lift) × $50M GMV = **$2M additional revenue**
- **Cost**: $57K (3-year) / $2M revenue = **2.9% cost of revenue lift**
- **ROI**: 35× return on search investment

---

### Option 2: Typesense (Cost-Optimized Alternative)

**Pricing**:
- Growth: $120/month (4 CPU, 8GB RAM, 500K records, unlimited searches)
- Business: $300/month (8 CPU, 16GB RAM, 2M records, unlimited searches)
- Enterprise: $600/month (16 CPU, 32GB RAM, 10M records, unlimited searches)

**2M searches/month pricing**:
- Business plan: **$300/month** (fixed, no usage-based charges)

**Pros**:
- ✅ **10-20ms latency** (excellent performance, InstantSearch compatible)
- ✅ **Predictable pricing** ($300/month fixed, no overage charges during Black Friday)
- ✅ **5-10 second purge** (faster than Algolia 30s, critical for inventory updates)
- ✅ **InstantSearch compatible** (React/Vue components, reuse Algolia UI code)
- ✅ **Strong faceting** (30+ facets, complex filters, dynamic sorting)
- ✅ **Typo tolerance** (2-edit distance, prefix matching, comparable to Algolia)

**Cons**:
- ⚠️ **No merchandising UI** (need to build admin panel, 80-160 hours)
- ⚠️ **No built-in analytics** (need to implement tracking, 40-80 hours)
- ⚠️ **DIY A/B testing** (manual implementation, 20-40 hours)
- ⚠️ **Higher maintenance** (10-15 hours/month vs Algolia 5 hours/month)

**TCO (3-year, 2M searches/month)**:
- **Business plan**: $300/month × 36 months = **$10,800**
- **Engineering** (setup 80h + maintenance 10h/month + merchandising 120h + analytics 60h): 80 + (10 × 36) + 120 + 60 = 620 hours × $100 = **$62,000**
- **Total TCO**: **$72,800** (3-year)

**When to Choose Typesense**:
- Budget-conscious (save $300-500/month vs Algolia)
- Engineering team comfortable building merchandising UI
- Traffic predictable (fixed pricing better than usage-based)
- Don't need built-in analytics (can use Mixpanel/Amplitude)

**ROI Calculation**:
- **Conversion impact**: 90-95% of Algolia (14-18% vs 15-20%)
- **Revenue impact**: 40% of sessions × (14% - 5% lift) × $50M GMV = **$1.8M additional revenue**
- **Cost**: $72,800 / $1,800,000 = **4% cost of revenue lift**
- **ROI**: 25× return (90% of Algolia benefit, 60% higher engineering cost)

---

### Option 3: Meilisearch (Budget Option)

**Pricing**:
- Build: $30/month (100K docs, 10M API calls, hybrid search included)
- Pro: $300/month (1M docs, 100M API calls, multi-region)
- Enterprise: Custom ($2K-5K/month, SLA, support)

**2M searches/month pricing**:
- Pro plan (500K products): **$300/month**

**Pros**:
- ✅ **15-25ms latency** (excellent, sub-50ms consistently)
- ✅ **Best DX** (9.0/10, fastest to production, 1-3 days setup)
- ✅ **Hybrid search included** ($30/month for AI features vs Algolia $10K+/month)
- ✅ **Predictable pricing** ($300/month, no usage charges)
- ✅ **MIT license** (most permissive, can self-host if needed)

**Cons**:
- ⚠️ **No merchandising UI** (DIY, 80-160 hours)
- ⚠️ **No analytics** (DIY tracking, 40-80 hours)
- ⚠️ **Slower purge** (10-30 seconds vs Typesense 5-10s)
- ⚠️ **Limited docs on ranking tuning** (vs Algolia comprehensive guides)

**TCO (3-year, 2M searches/month)**:
- **Pro plan**: $300/month × 36 months = **$10,800**
- **Engineering** (setup 60h + maintenance 10h/month + merchandising 120h + analytics 60h): 60 + (10 × 36) + 120 + 60 = 600 hours × $100 = **$60,000**
- **Total TCO**: **$70,800** (3-year)

**When to Choose Meilisearch**:
- Early-stage e-commerce (revenue <$5M ARR)
- Engineering team prioritizes DX (fastest implementation)
- Want hybrid search without Algolia premium ($30/month vs $10K+/month)
- Budget $300-500/month maximum

**ROI Calculation**: Similar to Typesense (25× ROI)

---

### Option 4: Azure AI Search (Not Recommended for E-Commerce)

**Pricing**: $250/month (Standard S1, 25GB, 3 replicas)

**Why Not Recommended**:
- ❌ **50-150ms latency** (too slow for instant search, users perceive delay)
- ❌ **Complex OData queries** (steep learning curve, 2-4 weeks setup)
- ❌ **Azure lock-in** (requires Azure Blob Storage, cognitive services)
- ❌ **No merchandising UI** (DIY)

**Only Consider If**: Already Azure-heavy (Blob Storage, App Service, SQL Database)

---

## Architecture Pattern: E-Commerce Instant Search

### Phase 1: Core Search Implementation

**Architecture**:
```
┌─────────────────────────────────────────────────────────────────┐
│                        User Browser                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ InstantSearch UI (React/Vue)                              │   │
│  │  - Search Box (autocomplete, query suggestions)           │   │
│  │  - Hits List (product results, images, prices)            │   │
│  │  - Facets (category, price, brand, rating, availability)  │   │
│  │  - Pagination (infinite scroll or pages)                  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ API Calls (search, facet, filter)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Search Platform (Algolia/Typesense)          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Index: products                                           │   │
│  │  - 500K documents (SKUs)                                  │   │
│  │  - Fields: title, description, category, brand, price,   │   │
│  │    images, inventory, rating, reviews_count              │   │
│  │  - Searchable: title, description, brand                 │   │
│  │  - Facets: category, brand, price_range, color, size     │   │
│  │  - Ranking: textual_relevance, exact, typo, proximity,   │   │
│  │    custom (inventory > 0, high_margin, high_conversion)  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Index Updates (via API)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Indexing Pipeline (Node.js/Python)               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. Extract from PostgreSQL (products table)              │   │
│  │ 2. Transform (denormalize, flatten, enrich)              │   │
│  │ 3. Load to Search Platform (batch updates, 10K/batch)    │   │
│  │ 4. Schedule: Full reindex daily, incremental hourly      │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Source Data
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PostgreSQL (Primary Database)                  │
│  - products (SKU, title, description, price, inventory)          │
│  - categories (hierarchy)                                        │
│  - brands                                                        │
│  - product_variants (color, size)                                │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow**:
1. **User types query** → InstantSearch UI sends API request (every keystroke, debounced 100ms)
2. **Search platform** → Returns results in 10-20ms (cached, pre-indexed)
3. **User filters** → Facet selection, re-query with filters (10-20ms)
4. **User clicks product** → Navigate to PDP (product detail page)

---

### Phase 2: Merchandising & Business Rules

**Architecture Addition**:
```
┌─────────────────────────────────────────────────────────────────┐
│               Merchandising Dashboard (Algolia UI or DIY)       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Business User Actions:                                    │   │
│  │  - Boost products (increase ranking for "winter coat")    │   │
│  │  - Pin products (always show "featured item" first)       │   │
│  │  - Bury products (hide low-inventory or low-margin)       │   │
│  │  - Synonyms (map "sneakers" → "shoes", "tee" → "t-shirt")│   │
│  │  - Query rules (if query = "sale", filter by on_sale=true)│   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ API Calls (update rules, synonyms)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Search Platform                             │
│  - Query Rules: 50-200 rules (seasonal, promotional)             │
│  - Synonyms: 500-2,000 mappings (product-specific language)     │
│  - Custom Ranking: inventory_weight + margin_weight + conv_rate │
└─────────────────────────────────────────────────────────────────┘
```

**Business Rules Examples**:
- **Seasonal boosting**: Boost "winter coats" Oct-Feb, "swimsuits" May-Aug
- **Inventory management**: Bury products with <10 inventory (avoid overselling)
- **Margin optimization**: Boost high-margin products (increase to 50%+ of top results)
- **Conversion optimization**: Boost products with >4.5 rating, >100 reviews

---

### Phase 3: Analytics & Optimization

**Architecture Addition**:
```
┌─────────────────────────────────────────────────────────────────┐
│                  Analytics Dashboard (Algolia or DIY)            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Metrics:                                                  │   │
│  │  - Search volume (2M/month, trending up 10% MoM)          │   │
│  │  - Click-through rate (CTR): 60-70%                       │   │
│  │  - Conversion rate: 15-20% (vs 3-5% browse)               │   │
│  │  - Revenue per search: $5-10 (vs $1-2 browse)             │   │
│  │  - No-results queries: <5% (target <3%)                   │   │
│  │  - Top queries: "winter coat", "running shoes", "laptop"  │   │
│  │  - Failed queries: "sneekers" (typo, handle with synonym) │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Event Tracking (click, conversion, revenue)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Search Platform Analytics                      │
│  - Click events: track which results clicked, position           │
│  - Conversion events: track purchases from search                │
│  - Revenue attribution: $X GMV from search vs browse             │
└─────────────────────────────────────────────────────────────────┘
```

**DIY Analytics Implementation** (if using Typesense/Meilisearch):
```javascript
// Track search event
function trackSearch(query, resultsCount) {
  analytics.track('search', {
    query: query,
    results_count: resultsCount,
    timestamp: new Date().toISOString()
  });
}

// Track click event
function trackClick(query, productId, position) {
  analytics.track('search_click', {
    query: query,
    product_id: productId,
    position: position,
    timestamp: new Date().toISOString()
  });
}

// Track conversion event
function trackConversion(query, productId, revenue) {
  analytics.track('search_conversion', {
    query: query,
    product_id: productId,
    revenue: revenue,
    timestamp: new Date().toISOString()
  });
}
```

**Analytics Tools** (if DIY):
- **Mixpanel** ($25-100/month, event tracking, funnels, cohorts)
- **Amplitude** ($49-100/month, similar to Mixpanel)
- **Custom dashboard** (Grafana + PostgreSQL, 80-160 hours to build)

---

## Implementation Guide

### Step 1: Data Preparation (Day 1)

**Extract product data from PostgreSQL**:
```sql
-- Extract products with all searchable fields
SELECT
  p.id AS objectID,
  p.sku,
  p.title,
  p.description,
  p.price,
  p.inventory_count,
  p.rating_avg,
  p.reviews_count,
  c.name AS category,
  c.path AS category_hierarchy,
  b.name AS brand,
  array_agg(DISTINCT i.url) AS images,
  array_agg(DISTINCT v.color) AS colors,
  array_agg(DISTINCT v.size) AS sizes,
  p.created_at,
  p.updated_at
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN brands b ON p.brand_id = b.id
LEFT JOIN product_images i ON p.id = i.product_id
LEFT JOIN product_variants v ON p.id = v.product_id
WHERE p.status = 'active'
GROUP BY p.id, c.id, b.id;
```

**Transform to search index format**:
```javascript
// Node.js transformation
const products = await db.query(extractQuery);

const searchDocuments = products.map(product => ({
  objectID: product.id,
  sku: product.sku,
  title: product.title,
  description: product.description,
  price: product.price,
  inventory_count: product.inventory_count,
  rating: product.rating_avg,
  reviews_count: product.reviews_count,
  category: product.category,
  category_hierarchy: product.category_hierarchy.split(' > '), // ["Electronics", "Laptops", "Gaming"]
  brand: product.brand,
  images: product.images,
  colors: product.colors,
  sizes: product.sizes,

  // Custom ranking attributes
  in_stock: product.inventory_count > 0,
  high_rating: product.rating_avg >= 4.5,
  popular: product.reviews_count >= 100,

  // Price range facet
  price_range: getPriceRange(product.price), // "$0-$50", "$50-$100", "$100-$200", "$200+"

  // Timestamps
  created_at: product.created_at.getTime(),
  updated_at: product.updated_at.getTime()
}));

function getPriceRange(price) {
  if (price < 50) return "$0-$50";
  if (price < 100) return "$50-$100";
  if (price < 200) return "$100-$200";
  return "$200+";
}
```

---

### Step 2: Index Creation (Day 1)

**Algolia index setup**:
```javascript
const algoliasearch = require('algoliasearch');
const client = algoliasearch('APP_ID', 'ADMIN_API_KEY');
const index = client.initIndex('products');

// Configure index settings
await index.setSettings({
  // Searchable attributes (order matters for ranking)
  searchableAttributes: [
    'title',
    'brand',
    'category',
    'description'
  ],

  // Attributes for faceting
  attributesForFaceting: [
    'category',
    'brand',
    'price_range',
    'colors',
    'sizes',
    'rating', // Numeric facet
    'in_stock'
  ],

  // Custom ranking (tie-breaker after textual relevance)
  customRanking: [
    'desc(in_stock)',        // Prioritize in-stock products
    'desc(high_rating)',     // Then high-rated products
    'desc(popular)',         // Then popular products
    'desc(reviews_count)',   // Then most-reviewed
    'asc(price)'             // Then lowest price
  ],

  // Ranking formula (order matters)
  ranking: [
    'typo',       // Fewer typos = higher rank
    'geo',        // Closer to user (if geo-search enabled)
    'words',      // More matched words = higher rank
    'filters',    // Applied filters
    'proximity',  // Words closer together = higher rank
    'attribute',  // Match in searchableAttributes order
    'exact',      // Exact match = higher rank
    'custom'      // customRanking attributes
  ],

  // Typo tolerance
  typoTolerance: 'strict', // Allow 1-2 typos depending on word length

  // Minimum 2 characters before searching
  minWordSizefor1Typo: 4,
  minWordSizefor2Typos: 8,

  // Pagination
  hitsPerPage: 24,
  maxValuesPerFacet: 100,

  // Highlighting
  attributesToHighlight: ['title', 'description'],
  attributesToSnippet: ['description:50']
});

// Upload products (batch 10K at a time)
const batchSize = 10000;
for (let i = 0; i < searchDocuments.length; i += batchSize) {
  const batch = searchDocuments.slice(i, i + batchSize);
  await index.saveObjects(batch);
  console.log(`Indexed ${i + batch.length} / ${searchDocuments.length} products`);
}

console.log('Index creation complete');
```

**Typesense index setup**:
```javascript
const Typesense = require('typesense');
const client = new Typesense.Client({
  nodes: [{ host: 'xxx.a1.typesense.net', port: '443', protocol: 'https' }],
  apiKey: 'ADMIN_API_KEY'
});

// Create collection schema
await client.collections().create({
  name: 'products',
  fields: [
    { name: 'title', type: 'string' },
    { name: 'description', type: 'string' },
    { name: 'brand', type: 'string', facet: true },
    { name: 'category', type: 'string', facet: true },
    { name: 'category_hierarchy', type: 'string[]', facet: true },
    { name: 'price', type: 'float', facet: true },
    { name: 'price_range', type: 'string', facet: true },
    { name: 'inventory_count', type: 'int32' },
    { name: 'rating', type: 'float', facet: true },
    { name: 'reviews_count', type: 'int32' },
    { name: 'colors', type: 'string[]', facet: true },
    { name: 'sizes', type: 'string[]', facet: true },
    { name: 'in_stock', type: 'bool', facet: true },
    { name: 'images', type: 'string[]' },
    { name: 'created_at', type: 'int64' }
  ],
  default_sorting_field: 'created_at'
});

// Import products
await client.collections('products').documents().import(searchDocuments, { action: 'upsert' });
```

---

### Step 3: Frontend Integration (Days 2-3)

**InstantSearch React implementation**:
```jsx
import React from 'react';
import algoliasearch from 'algoliasearch/lite';
import {
  InstantSearch,
  SearchBox,
  Hits,
  RefinementList,
  Pagination,
  Configure,
  Stats,
  ClearRefinements
} from 'react-instantsearch-dom';

const searchClient = algoliasearch('APP_ID', 'SEARCH_API_KEY');

function SearchPage() {
  return (
    <InstantSearch indexName="products" searchClient={searchClient}>
      <Configure hitsPerPage={24} />

      <div className="search-container">
        {/* Search Box */}
        <SearchBox
          placeholder="Search products..."
          autoFocus
          translations={{ placeholder: 'Search 500K products' }}
        />

        <div className="search-layout">
          {/* Sidebar: Facets */}
          <aside className="facets-sidebar">
            <ClearRefinements />

            <div className="facet-section">
              <h3>Category</h3>
              <RefinementList attribute="category" limit={10} showMore />
            </div>

            <div className="facet-section">
              <h3>Brand</h3>
              <RefinementList attribute="brand" limit={10} showMore searchable />
            </div>

            <div className="facet-section">
              <h3>Price Range</h3>
              <RefinementList attribute="price_range" />
            </div>

            <div className="facet-section">
              <h3>Colors</h3>
              <RefinementList attribute="colors" limit={20} />
            </div>

            <div className="facet-section">
              <h3>Sizes</h3>
              <RefinementList attribute="sizes" />
            </div>

            <div className="facet-section">
              <h3>Availability</h3>
              <RefinementList attribute="in_stock" />
            </div>
          </aside>

          {/* Main: Results */}
          <main className="results-container">
            <Stats />

            <Hits hitComponent={ProductHit} />

            <Pagination showFirst showLast />
          </main>
        </div>
      </div>
    </InstantSearch>
  );
}

function ProductHit({ hit }) {
  return (
    <div className="product-card">
      <img src={hit.images[0]} alt={hit.title} />
      <h3>{hit.title}</h3>
      <p className="brand">{hit.brand}</p>
      <p className="price">${hit.price}</p>
      <div className="rating">
        {'⭐'.repeat(Math.round(hit.rating))} ({hit.reviews_count})
      </div>
      {!hit.in_stock && <span className="out-of-stock">Out of Stock</span>}
    </div>
  );
}

export default SearchPage;
```

---

### Step 4: Incremental Updates (Day 4)

**Real-time sync on product changes**:
```javascript
// Listen to PostgreSQL changes (use triggers or CDC)
// Option 1: Database triggers + message queue (RabbitMQ, SQS)
// Option 2: Change Data Capture (Debezium, AWS DMS)
// Option 3: Application-level hooks (on product.update, call updateSearchIndex)

async function updateSearchIndex(productId) {
  // Fetch updated product data
  const product = await db.query('SELECT * FROM products WHERE id = ?', [productId]);

  // Transform to search document
  const searchDoc = transformProduct(product);

  // Update in Algolia
  await index.saveObject(searchDoc);

  console.log(`Updated product ${productId} in search index`);
}

// Hook into product update endpoint
app.post('/api/products/:id', async (req, res) => {
  const productId = req.params.id;

  // Update in PostgreSQL
  await db.query('UPDATE products SET ... WHERE id = ?', [productId]);

  // Update in search index (async, non-blocking)
  updateSearchIndex(productId).catch(err => console.error('Search update failed:', err));

  res.json({ success: true });
});
```

**Scheduled full reindex** (daily, catch any missed updates):
```javascript
const cron = require('node-cron');

// Run daily at 2 AM
cron.schedule('0 2 * * *', async () => {
  console.log('Starting full reindex...');

  const products = await db.query('SELECT * FROM products WHERE status = "active"');
  const searchDocs = products.map(transformProduct);

  // Clear and rebuild index
  await index.clearObjects();
  await index.saveObjects(searchDocs);

  console.log(`Full reindex complete: ${searchDocs.length} products`);
});
```

---

## Testing & Validation

### Performance Testing

**Latency benchmarks** (target: <50ms p95):
```bash
# Apache Bench (1000 requests, 10 concurrent)
ab -n 1000 -c 10 "https://APP_ID-dsn.algolia.net/1/indexes/products/query" \
  -H "X-Algolia-API-Key: SEARCH_KEY" \
  -H "X-Algolia-Application-Id: APP_ID" \
  -p query.json

# Expected results:
# - Algolia: 10-20ms median, 30-50ms p95
# - Typesense: 15-25ms median, 40-60ms p95
# - Meilisearch: 15-30ms median, 50-80ms p95
```

### Relevance Testing

**Test queries** (validate ranking):
```javascript
const testQueries = [
  { query: 'winter coat', expectedTop3: ['Patagonia Winter Coat', 'North Face Parka', 'Columbia Jacket'] },
  { query: 'running shoes', expectedTop3: ['Nike Air Zoom', 'Adidas Ultraboost', 'Brooks Ghost'] },
  { query: 'laptop', expectedTop3: ['MacBook Pro', 'Dell XPS', 'ThinkPad X1'] },
  { query: 'sneekers', expectedTop3: ['Nike Sneakers', 'Adidas Sneakers', 'Converse'] }, // Typo test
];

for (const test of testQueries) {
  const results = await index.search(test.query);
  const top3Titles = results.hits.slice(0, 3).map(hit => hit.title);

  console.log(`Query: "${test.query}"`);
  console.log(`Expected: ${test.expectedTop3.join(', ')}`);
  console.log(`Actual: ${top3Titles.join(', ')}`);
  console.log(`Match: ${test.expectedTop3.every(title => top3Titles.includes(title)) ? '✅' : '❌'}`);
}
```

### Load Testing (Black Friday Simulation)

**Simulate 5× traffic spike**:
```bash
# k6 load testing (10M searches/month = 333K searches/day = 3.85 QPS normal, 19 QPS peak)
k6 run --vus 20 --duration 5m search-load-test.js

# search-load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export default function() {
  const query = ['winter coat', 'running shoes', 'laptop', 'phone'][Math.floor(Math.random() * 4)];

  const res = http.post('https://APP_ID-dsn.algolia.net/1/indexes/products/query',
    JSON.stringify({ query: query, hitsPerPage: 24 }),
    { headers: { 'X-Algolia-API-Key': 'SEARCH_KEY', 'X-Algolia-Application-Id': 'APP_ID' } }
  );

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 50ms': (r) => r.timings.duration < 50
  });

  sleep(0.05); // 20 QPS per VU
}
```

---

## Migration Strategy

### Phased Rollout (4-6 Weeks)

**Week 1-2: Setup & Testing**
- Set up search platform (Algolia/Typesense/Meilisearch)
- Index full product catalog (500K products)
- Configure ranking, facets, synonyms
- Performance testing (latency, load)
- Relevance testing (top 100 queries)

**Week 3: Soft Launch (10% Traffic)**
- Deploy InstantSearch UI to staging
- A/B test: 10% users see new search, 90% old search
- Monitor: latency, CTR, conversion, errors
- Iterate: fix bugs, tune ranking

**Week 4: Ramp Up (50% Traffic)**
- Increase to 50% traffic
- Monitor: peak load handling, cost
- Add merchandising rules (boost high-margin products)
- Train business team on merchandising UI

**Week 5-6: Full Launch (100% Traffic)**
- Increase to 100% traffic
- Monitor for 2 weeks (catch any edge cases)
- Decommission old search
- Celebrate 🎉

### Rollback Plan

**If critical issues arise**:
1. **Instant rollback** (revert feature flag, 100% traffic to old search)
2. **Investigate** (logs, metrics, user reports)
3. **Fix** (hotfix, redeploy)
4. **Re-test** (staging validation)
5. **Re-launch** (gradual rollout again)

---

## Cost-Benefit Analysis (3-Year)

### Scenario: Mid-Market E-Commerce ($25M GMV)

**Baseline (No Search Optimization)**:
- 40% sessions use search
- Search conversion rate: 8% (basic keyword search)
- Browse conversion rate: 3%
- Average order value: $75
- Annual GMV from search: $25M × 40% × 8% = **$800K**

**With Algolia/Typesense Instant Search**:
- Search conversion rate: 15% (2× improvement from instant search, merchandising)
- Annual GMV from search: $25M × 40% × 15% = **$1.5M**
- **Incremental GMV**: $1.5M - $800K = **$700K/year**
- **3-year incremental GMV**: $700K × 3 = **$2.1M**

**Algolia TCO**: $57K (3-year)
**Typesense TCO**: $72K (3-year)

**ROI**:
- **Algolia**: ($2.1M - $57K) / $57K = **36× ROI**
- **Typesense**: ($2.1M - $72K) / $72K = **29× ROI**

**Winner**: Algolia (higher ROI despite higher license cost, due to lower engineering effort)

**Caveat**: ROI assumes merchandising UI usage. If don't use merchandising (engineering team manages search), Typesense has better ROI.

---

## Final Recommendation

### For Mid-Market E-Commerce ($5M-50M GMV):

**Choose Algolia Grow/Premium** if:
- Search is revenue driver (>10% of GMV from search)
- Need merchandising UI (business team manages boosting/pinning)
- Need built-in analytics (revenue attribution, A/B testing)
- Budget $500-5K/month
- Global audience (need <50ms worldwide)

**Choose Typesense Business** if:
- Budget-conscious (save $300-500/month vs Algolia)
- Engineering team comfortable building merchandising UI
- Don't need built-in analytics (can use Mixpanel/Amplitude)
- Traffic predictable (fixed pricing preferred)

**Choose Meilisearch Pro** if:
- Early-stage (<$5M GMV)
- Prioritize speed to market (fastest DX, 1-3 days setup)
- Want hybrid search without premium pricing ($300/month vs Algolia $10K+/month)

**Avoid Azure AI Search/Elasticsearch**: Too slow for instant search (<50ms requirement), not suitable for e-commerce.

---

**Last Updated**: November 14, 2025
**Scenario**: E-Commerce Product Catalog Search
**Recommended Platform**: Algolia (mid-market) or Typesense (cost-conscious)
**Expected ROI**: 29-36× (3-year)
