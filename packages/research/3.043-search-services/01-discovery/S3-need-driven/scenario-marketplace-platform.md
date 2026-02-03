# S3 Scenario 5: Two-Sided Marketplace Platform (Airbnb, Uber, Fiverr Model)

**Company Profile**: Marketplace platform connecting buyers and sellers/service providers
**Search Volume**: 10M listings (products/services/spaces), 20M searches/month, two-entity search (sellers + listings)
**Budget**: $2K-15K/month for search infrastructure
**Priority**: Geo-search, multi-index, complex filters, personalization, quality ranking

---

## Business Context

### Company Details
- **Stage**: Series B to Public
- **Team Size**: 100-500 employees, 20-80 engineers, 5-15 on search/discovery
- **Users**: 1M-10M monthly active users (500K-2M buyers, 100K-500K sellers)
- **Revenue**: $50M-500M GMV (Gross Merchandise Value)
- **Growth**: 100-200% YoY
- **Business Model**: Commission-based (10-20% take rate)

### Technical Environment
- **Platform Type**: Two-sided marketplace (Airbnb = spaces, Uber = rides, Fiverr = services, Etsy = products)
- **Entities**: Sellers/hosts (500K profiles) + Listings (10M products/services/spaces)
- **Search Patterns**:
  - **Geo-search** (60%): "Apartments in San Francisco", "Plumbers near me"
  - **Category search** (30%): "Graphic design services", "Vintage clothing"
  - **Seller search** (10%): "Top-rated photographers", "Local contractors"
- **Search Traffic**: 20M searches/month (80% mobile, 20% desktop)
- **Conversion**: Search converts 10-15% (vs 3-5% browse)
- **Geographic Distribution**: Global (US 40%, Europe 30%, APAC 20%, other 10%)

### Marketplace Search Requirements
- **Geo-Search**: <10 miles radius, "near me", bounding box, polygon filters
- **Multi-Index**: Sellers + Listings (search both, rank independently)
- **Complex Filters**: Price range, rating (>4.5), availability (next 7 days), delivery time, seller location
- **Personalization**: User history (past searches, bookings), location preference, price sensitivity
- **Quality Ranking**: Seller rating + listing quality + conversion rate + response time
- **Latency**: <100ms p95 (acceptable for marketplace, not instant)
- **Scale**: 10M+ listings, 20M+ searches/month, 1M+ concurrent users (peak)
- **Faceting**: 20-50 facets (category, price, location, rating, delivery, seller type)

---

## Search Platform Evaluation

### Evaluation Criteria

| Criterion | Weight | Algolia | Typesense | Elasticsearch | AWS OpenSearch | Azure AI Search | Notes |
|-----------|--------|---------|-----------|--------------|---------------|----------------|-------|
| **Geo-Search** | 25% | 10/10 | 9/10 | 9/10 | 9/10 | 8/10 | All strong, Algolia best UX |
| **Multi-Index** | 20% | 10/10 | 8/10 | 9/10 | 9/10 | 7/10 | Algolia native, others DIY |
| **Personalization** | 20% | 9/10 | 5/10 | 7/10 | 7/10 | 6/10 | Algolia best (AI Ranking) |
| **Performance** | 15% | 10/10 | 9/10 | 7/10 | 7/10 | 7/10 | Algolia/Typesense <50ms |
| **Cost Efficiency** | 10% | 4/10 | 10/10 | 6/10 | 6/10 | 7/10 | Typesense 10× cheaper |
| **Scale (10M+ docs)** | 10% | 10/10 | 8/10 | 10/10 | 10/10 | 9/10 | Algolia/Elastic proven at 1B+ |
| **Total Score** | 100% | **8.9/10** | **8.0/10** | **8.0/10** | **7.9/10** | **7.3/10** | Algolia wins for marketplace |

### Winner: Algolia Premium (best for high-GMV marketplaces, need personalization)
### Alternative: Typesense (cost-conscious, DIY personalization acceptable)
### Large-Scale: Elasticsearch/OpenSearch (if >50M listings or need custom ML)

---

## Platform Deep Dive

### Option 1: Algolia Premium (Recommended for High-GMV Marketplaces)

**Pricing**: **$5K-25K/month** ($60K-300K/year, scales with records, searches, features)

**Pricing Model**:
- Grow Plus: $1,485/month (1M records, 10M searches, NeuralSearch)
- Premium: $5K-10K/month (10M records, 50M searches, AI Ranking, personalization)
- Elevate: $10K-25K/month (100M records, 200M searches, ML personalization, A/B testing)

**20M searches/month, 10M listings pricing**: Premium tier = **$8K-12K/month**

**Pros**:
- ✅ **Best geo-search** (10-20ms, bounding box, polygon, radius, _geoloc field)
- ✅ **Multi-index federation** (search sellers + listings simultaneously, merge results)
- ✅ **AI Ranking personalization** (user history, location, price sensitivity, ML-driven)
- ✅ **10-20ms latency** (70+ PoPs, global CDN, <50ms worldwide)
- ✅ **InstantSearch UI** (React/Vue components, 80% of UI pre-built)
- ✅ **A/B testing** (ranking experiments, statistical significance)
- ✅ **Analytics** (search volume, conversion, revenue attribution)
- ✅ **Proven at marketplace scale** (Twitch, Lacoste, Stripe, Medium use Algolia)

**Cons**:
- ⚠️ **Expensive** ($8K-12K/month vs Typesense $600/month, 15-20× more)
- ⚠️ **Usage-based pricing** (unpredictable spikes during peak seasons)
- ⚠️ **Vendor lock-in** (proprietary API, personalization data, hard to migrate)

**TCO (3-year, 10M listings, 20M searches/month)**:
- License: $10K/month × 36 months = **$360,000**
- Engineering (setup 80h + maintenance 10h/month): 80 + (10 × 36) = 440 hours × $100 = **$44,000**
- **Total TCO**: **$404,000** (3-year)

**When to Choose Algolia**:
- High-GMV marketplace ($50M-500M+/year)
- Personalization critical (ML ranking drives 10-20% conversion lift)
- Global audience (need <50ms worldwide, 70+ PoPs)
- Budget $5K-25K/month (can afford premium)
- Search is competitive advantage (Airbnb-level quality)

**ROI Calculation**:
- **Baseline conversion** (browse): 5%
- **With Algolia personalization**: 12% (2.4× improvement)
- **GMV impact**: 80% of bookings from search × (12% - 5% lift) × $200M GMV = **$11.2M incremental GMV**
- **Commission** (15% take rate): $11.2M × 15% = **$1.68M incremental revenue/year**
- **3-year value**: $1.68M × 3 = **$5.04M**
- **Cost**: $404K
- **ROI**: ($5.04M - $404K) / $404K = **11.5× ROI**

---

### Option 2: Typesense Business (Cost-Optimized Alternative)

**Pricing**: **$600/month** (Enterprise: 16 CPU, 32GB RAM, 10M records, unlimited searches)

**Pros**:
- ✅ **Strong geo-search** (radius, bounding box, polygon, comparable to Algolia)
- ✅ **10-20ms latency** (excellent performance, InstantSearch compatible)
- ✅ **Predictable pricing** ($600/month fixed, no usage-based surprises)
- ✅ **10M doc capacity** (fits entire marketplace: sellers + listings)
- ✅ **Multi-index** (DIY federation, search 2 collections, merge results)
- ✅ **Cost-effective** ($600/month vs Algolia $10K/month, 17× cheaper)

**Cons**:
- ⚠️ **No built-in personalization** (need to implement ML ranking, 200-400 hours)
- ⚠️ **DIY multi-index** (need to merge results from sellers + listings, 40-80 hours)
- ⚠️ **No analytics** (DIY tracking, 40-80 hours)
- ⚠️ **Higher maintenance** (15-20 hours/month vs Algolia 10 hours/month)

**TCO (3-year, 10M listings, 20M searches/month)**:
- License: $600/month × 36 months = **$21,600**
- Engineering (setup 200h + personalization 300h + maintenance 15h/month): 200 + 300 + (15 × 36) = 1,040 hours × $100 = **$104,000**
- **Total TCO**: **$125,600** (3-year)

**When to Choose Typesense**:
- Budget-conscious ($600/month vs Algolia $10K/month)
- Engineering team comfortable building personalization (ML expertise)
- Don't need global <50ms (regional marketplace, US-only or Europe-only)
- GMV <$50M/year (can't justify Algolia premium)

**ROI Calculation**:
- **Conversion improvement**: 90% of Algolia (10.8% vs 12%, due to DIY personalization)
- **GMV impact**: 80% of bookings × (10.8% - 5% lift) × $200M GMV = **$9.28M incremental GMV**
- **Commission** (15% take rate): $9.28M × 15% = **$1.39M incremental revenue/year**
- **3-year value**: $1.39M × 3 = **$4.17M**
- **Cost**: $125.6K
- **ROI**: ($4.17M - $125.6K) / $125.6K = **32× ROI** (better than Algolia due to lower cost)

---

### Option 3: Elasticsearch/OpenSearch (Best for Custom ML)

**Pricing**: **$2,000-5,000/month** ($24K-60K/year, Elastic Cloud or AWS OpenSearch)

**Elastic Cloud Setup** (10M docs, 20M searches/month):
- 3× c5d.4xlarge instances (16 vCPU, 32GB RAM, 1TB SSD each)
- 3 replicas (high availability)
- Cost: ~$3,000/month = **$36K/year**

**Pros**:
- ✅ **Custom ML ranking** (Learning to Rank plugin, full control over features/weights)
- ✅ **Powerful geo-search** (geo_shape, geo_bounding_box, geo_distance, aggregations)
- ✅ **Proven at scale** (100B+ documents, Uber/Airbnb scale)
- ✅ **Advanced aggregations** (trending locations, price distributions, analytics)
- ✅ **Multi-index federation** (search sellers + listings, merge, rank independently)

**Cons**:
- ⚠️ **50-200ms latency** (slower than Algolia/Typesense, but acceptable for marketplace)
- ⚠️ **Complex setup** (clusters, shards, replicas, Learning to Rank plugin, 4-8 weeks)
- ⚠️ **Higher maintenance** (30-40 hours/month, monitor performance, tune queries)
- ⚠️ **Expensive** ($3K/month vs Typesense $600/month, 5× more)

**TCO (3-year, 10M listings, 20M searches/month)**:
- License: $3,000/month × 36 months = **$108,000**
- Engineering (setup 400h + ML ranking 500h + maintenance 30h/month): 400 + 500 + (30 × 36) = 1,980 hours × $100 = **$198,000**
- **Total TCO**: **$306,000** (3-year)

**When to Choose Elasticsearch/OpenSearch**:
- Need custom ML ranking (Learning to Rank, feature engineering, A/B testing)
- Very large scale (>50M listings, >100M searches/month)
- Engineering team has Elasticsearch expertise (in-house ML, data science)
- Budget $2K-5K/month

**ROI Calculation**: Similar to Algolia (11-12× ROI with custom ML personalization)

---

## Architecture Pattern: Marketplace Multi-Index Search

### Phase 1: Geo-Search + Multi-Index (Algolia)

**Architecture**:
```
┌─────────────────────────────────────────────────────────────────┐
│                   Marketplace Search UI (Mobile 80%, Web 20%)    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Search Box with Geo-Input                                 │   │
│  │  - "Graphic designers in San Francisco"                   │   │
│  │  - "Apartments near me" (detect user location)            │   │
│  │  - "Vintage clothing" (category search)                   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Results (Federated: Sellers + Listings)                   │   │
│  │  - Sellers: Top 3 (profile pic, rating, reviews, location)│   │
│  │  - Listings: Top 20 (thumbnail, price, rating, distance)  │   │
│  │  - Map view: Pins for each listing (geo coordinates)      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Facets (Filters)                                          │   │
│  │  - Category (Graphic Design, Web Development, etc.)       │   │
│  │  - Price range ($50-$100, $100-$500, $500+)              │   │
│  │  - Rating (>4.5, >4.0, >3.5)                              │   │
│  │  - Distance (<5 miles, <10 miles, <25 miles)             │   │
│  │  - Availability (Next 7 days, Next 30 days)               │   │
│  │  - Seller type (Individual, Agency, Top-rated)            │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Search API (query + geo + user context)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Algolia (Multi-Index)                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Index 1: sellers (500K profiles)                          │   │
│  │  - Fields: name, bio, category, location (lat/lng),       │   │
│  │    rating, reviews_count, response_time, profile_pic      │   │
│  │  - Geo-search: _geoloc field (lat: 37.7749, lng: -122.4)  │   │
│  │  - Ranking: rating + reviews_count + response_time        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Index 2: listings (10M products/services/spaces)          │   │
│  │  - Fields: title, description, price, category, seller_id,│   │
│  │    location (lat/lng), rating, thumbnail, availability    │   │
│  │  - Geo-search: _geoloc field                              │   │
│  │  - Ranking: relevance + rating + conversion_rate + price  │   │
│  │  - Personalization: user history (past searches, bookings)│   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ AI Ranking (Personalization)                              │   │
│  │  - User features: location, price sensitivity, category   │   │
│  │  - Item features: CTR, conversion rate, quality score     │   │
│  │  - ML model: XGBoost, trained on 1M+ conversions          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Index updates (on seller/listing create/update)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Marketplace Database (PostgreSQL)                │
│  - sellers (500K profiles)                                        │
│  - listings (10M products/services/spaces)                        │
│  - bookings (1M/month, conversion events)                         │
│  - user_events (searches, clicks, bookings)                       │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow**:
1. **User searches** ("Graphic designers in San Francisco") → Algolia receives query + user location (37.7749, -122.4194)
2. **Multi-index federation** → Algolia searches `sellers` index AND `listings` index simultaneously
3. **Geo-filter** → Both indexes filtered by _geoloc within 10 miles of user location
4. **Personalization** → AI Ranking adjusts results based on user history (past searches: "logo design", past bookings: $200-$500 price range)
5. **Results merged** → Top 3 sellers + Top 20 listings returned (15-25ms total)
6. **User clicks listing** → Track event, update personalization model

---

### Phase 2: Custom Ranking Formula

**Listing Ranking** (Algolia custom ranking):
```javascript
await listingsIndex.setSettings({
  searchableAttributes: [
    'title',
    'description',
    'category',
    'seller_name'
  ],

  attributesForFaceting: [
    'category',
    'price_range',
    'rating',
    'seller_type',
    'availability'
  ],

  // Geo-search
  customGeoSearch: {
    enabled: true,
    geolocField: '_geoloc' // { lat: 37.7749, lng: -122.4194 }
  },

  // Custom ranking (after textual relevance)
  customRanking: [
    'desc(quality_score)',     // Quality score (1-100, composite)
    'desc(conversion_rate)',   // Historical conversion rate (0-1)
    'desc(rating)',            // Rating (1-5)
    'asc(price)',              // Lower price = higher rank (for budget-conscious)
    'desc(reviews_count)',     // More reviews = more trust
    'asc(distance)'            // Closer = higher rank
  ],

  // Ranking formula
  ranking: [
    'typo',       // Fewer typos = higher rank
    'geo',        // Geo distance (if geo-search query)
    'words',      // More matched words = higher rank
    'filters',    // Applied filters
    'proximity',  // Words closer together = higher rank
    'attribute',  // Match in searchableAttributes order
    'exact',      // Exact match = higher rank
    'custom'      // customRanking attributes
  ]
});

// Calculate quality_score before indexing
function calculateQualityScore(listing) {
  const ratingScore = (listing.rating / 5) * 40; // Max 40 points
  const conversionScore = listing.conversion_rate * 30; // Max 30 points
  const reviewsScore = Math.min(20, listing.reviews_count / 10); // Max 20 points (caps at 200 reviews)
  const responseScore = Math.max(0, 10 - (listing.seller_response_time_hours / 2)); // Max 10 points (<2h = 10 points)

  return ratingScore + conversionScore + reviewsScore + responseScore; // Max 100
}
```

---

## Implementation Guide

### Step 1: Multi-Index Setup (Algolia)

**Create two indexes**:
```javascript
const algoliasearch = require('algoliasearch');
const client = algoliasearch('APP_ID', 'ADMIN_API_KEY');

// Index 1: Sellers
const sellersIndex = client.initIndex('sellers');
await sellersIndex.setSettings({
  searchableAttributes: ['name', 'bio', 'category', 'skills'],
  attributesForFaceting: ['category', 'seller_type', 'rating', 'location_city'],
  customRanking: ['desc(rating)', 'desc(reviews_count)', 'asc(response_time_hours)'],
  ranking: ['typo', 'geo', 'words', 'proximity', 'attribute', 'exact', 'custom']
});

// Index 2: Listings
const listingsIndex = client.initIndex('listings');
await listingsIndex.setSettings({
  searchableAttributes: ['title', 'description', 'category', 'seller_name'],
  attributesForFaceting: ['category', 'price_range', 'rating', 'availability'],
  customRanking: ['desc(quality_score)', 'desc(conversion_rate)', 'desc(rating)', 'asc(price)'],
  ranking: ['typo', 'geo', 'words', 'proximity', 'attribute', 'exact', 'custom']
});

// Index sellers
const sellers = await db.query('SELECT * FROM sellers WHERE status = "active"');
const sellersDocs = sellers.map(seller => ({
  objectID: seller.id,
  name: seller.name,
  bio: seller.bio,
  category: seller.category,
  _geoloc: { lat: seller.latitude, lng: seller.longitude },
  rating: seller.rating_avg,
  reviews_count: seller.reviews_count,
  response_time_hours: seller.response_time_hours,
  profile_pic: seller.profile_pic_url
}));
await sellersIndex.saveObjects(sellersDocs);

// Index listings
const listings = await db.query('SELECT * FROM listings WHERE status = "active"');
const listingsDocs = listings.map(listing => ({
  objectID: listing.id,
  title: listing.title,
  description: listing.description,
  category: listing.category,
  price: listing.price,
  _geoloc: { lat: listing.latitude, lng: listing.longitude },
  rating: listing.rating_avg,
  reviews_count: listing.reviews_count,
  quality_score: calculateQualityScore(listing),
  conversion_rate: listing.conversion_rate,
  thumbnail: listing.thumbnail_url,
  seller_id: listing.seller_id,
  seller_name: listing.seller_name
}));
await listingsIndex.saveObjects(listingsDocs);
```

---

### Step 2: Frontend Multi-Index Search (React)

**Federated search UI**:
```jsx
import React from 'react';
import algoliasearch from 'algoliasearch/lite';
import { InstantSearch, Configure, SearchBox, Hits, Index } from 'react-instantsearch-dom';

const searchClient = algoliasearch('APP_ID', 'SEARCH_API_KEY');

function MarketplaceSearch() {
  const userLocation = { lat: 37.7749, lng: -122.4194 }; // San Francisco (from browser geolocation)

  return (
    <InstantSearch indexName="listings" searchClient={searchClient}>
      <SearchBox placeholder="Search designers, services, or locations..." />

      {/* Sellers Index (Top 3) */}
      <Index indexName="sellers">
        <Configure
          hitsPerPage={3}
          aroundLatLng={`${userLocation.lat},${userLocation.lng}`}
          aroundRadius={16093} // 10 miles in meters
        />
        <h2>Top Sellers</h2>
        <Hits hitComponent={SellerHit} />
      </Index>

      {/* Listings Index (Top 20) */}
      <Index indexName="listings">
        <Configure
          hitsPerPage={20}
          aroundLatLng={`${userLocation.lat},${userLocation.lng}`}
          aroundRadius={16093} // 10 miles
          enablePersonalization={true}
          userToken={getCurrentUser().id} // For AI Ranking personalization
        />
        <h2>Listings</h2>
        <Hits hitComponent={ListingHit} />
      </Index>
    </InstantSearch>
  );
}

function SellerHit({ hit }) {
  return (
    <div className="seller-card">
      <img src={hit.profile_pic} alt={hit.name} />
      <h3>{hit.name}</h3>
      <p>{hit.bio.slice(0, 100)}...</p>
      <div className="rating">
        {'⭐'.repeat(Math.round(hit.rating))} ({hit.reviews_count} reviews)
      </div>
      <p className="distance">{hit._rankingInfo?.geoDistance ? `${(hit._rankingInfo.geoDistance / 1609).toFixed(1)} miles away` : ''}</p>
    </div>
  );
}

function ListingHit({ hit }) {
  return (
    <div className="listing-card">
      <img src={hit.thumbnail} alt={hit.title} />
      <h3>{hit.title}</h3>
      <p className="price">${hit.price}</p>
      <div className="rating">
        {'⭐'.repeat(Math.round(hit.rating))} ({hit.reviews_count})
      </div>
      <p className="seller">By {hit.seller_name}</p>
      <p className="distance">{hit._rankingInfo?.geoDistance ? `${(hit._rankingInfo.geoDistance / 1609).toFixed(1)} miles away` : ''}</p>
    </div>
  );
}

export default MarketplaceSearch;
```

---

## Testing & Validation

### Geo-Search Testing

**Test geo-radius queries**:
```javascript
const testCases = [
  { query: 'graphic designer', userLocation: { lat: 37.7749, lng: -122.4194 }, radius: 10, expectedResults: ['John Designer (SF)', 'Jane Creative (SF)'] },
  { query: 'plumber', userLocation: { lat: 40.7128, lng: -74.0060 }, radius: 5, expectedResults: ['Bob Plumber (NYC)', 'Alice Repairs (NYC)'] }
];

for (const test of testCases) {
  const results = await listingsIndex.search(test.query, {
    aroundLatLng: `${test.userLocation.lat},${test.userLocation.lng}`,
    aroundRadius: test.radius * 1609 // Miles to meters
  });

  const distances = results.hits.map(hit => (hit._rankingInfo.geoDistance / 1609).toFixed(1));

  console.log(`Query: "${test.query}", Location: (${test.userLocation.lat}, ${test.userLocation.lng}), Radius: ${test.radius} miles`);
  console.log(`Results: ${results.hits.map(hit => hit.title).join(', ')}`);
  console.log(`Distances: ${distances.join(', ')} miles`);
  console.log(`Within radius: ${distances.every(d => d <= test.radius) ? '✅' : '❌'}`);
}
```

---

## Cost-Benefit Analysis (3-Year)

**Scenario**: Marketplace ($200M GMV/year, 10M listings, 20M searches/month)

**Baseline (No Search or Basic Keyword Search)**:
- 60% of bookings from search (basic keyword)
- Search conversion rate: 5%
- GMV from search: $200M × 60% × 5% = **$6M/year**

**With Algolia Personalization**:
- Search conversion rate: 12% (2.4× improvement from geo-search + personalization)
- GMV from search: $200M × 60% × 12% = **$14.4M/year**
- **Incremental GMV**: $14.4M - $6M = **$8.4M/year**
- **Commission revenue** (15% take rate): $8.4M × 15% = **$1.26M/year**
- **3-year value**: $1.26M × 3 = **$3.78M**

**TCO**:
- Algolia: $404K (3-year)
- Typesense: $125.6K (3-year)

**ROI**:
- **Algolia**: ($3.78M - $404K) / $404K = **8.4× ROI**
- **Typesense**: ($3.15M - $125.6K) / $125.6K = **24× ROI** (assuming 90% of Algolia conversion improvement)

**Winner**: Typesense (better ROI due to lower cost, if can build personalization)

---

## Final Recommendation

### For High-GMV Marketplace (>$100M GMV/year, budget $5K-25K/month):

**Choose Algolia Premium**:
- ✅ Best personalization (AI Ranking, user history, ML-driven)
- ✅ Best geo-search (10-20ms, 70+ PoPs, global <50ms)
- ✅ Multi-index federation (native, no DIY)
- ✅ 8-12× ROI (3-year, conversion lift)

### For Cost-Conscious Marketplace (<$50M GMV/year, budget $600/month):

**Choose Typesense**:
- ✅ 17× cheaper than Algolia ($600/month vs $10K/month)
- ✅ Strong geo-search (comparable to Algolia)
- ✅ 24× ROI (3-year, better than Algolia due to lower cost)
- ✅ DIY personalization (200-400 hours, but feasible)

### For Custom ML Marketplace (need Learning to Rank, data science team):

**Choose Elasticsearch/OpenSearch**:
- ✅ Custom ML ranking (LTR plugin, full control)
- ✅ Proven at massive scale (Uber, Airbnb use Elasticsearch)
- ✅ 11-12× ROI (3-year, with custom ML)

---

**Last Updated**: November 14, 2025
**Scenario**: Two-Sided Marketplace Platform
**Recommended Platform**: Algolia (high-GMV) or Typesense (cost-conscious)
**Expected ROI**: 8-24× (3-year, conversion lift from geo-search + personalization)
