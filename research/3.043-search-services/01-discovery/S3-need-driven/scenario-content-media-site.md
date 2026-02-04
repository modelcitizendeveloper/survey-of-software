# S3 Scenario 3: Content/Media Site Search (News, Blog, Publishing)

**Company Profile**: Digital media company, content publisher, news site
**Search Volume**: 1M articles/posts, 5M searches/month, high-traffic content site
**Budget**: $500-3K/month for search infrastructure
**Priority**: Full-text search quality, scale (millions of docs), cost efficiency, faceting by author/category/date

---

## Business Context

### Company Details
- **Stage**: Bootstrapped to Series A
- **Team Size**: 20-100 employees, 10-30 engineers, 2-4 on content platform
- **Users**: 5M-50M monthly pageviews
- **Revenue**: $1M-20M ARR (advertising, subscriptions, affiliate)
- **Growth**: 50-100% YoY
- **Business Model**: Ad-supported + subscription hybrid

### Technical Environment
- **CMS**: WordPress, Ghost, custom Node.js/Python CMS
- **Content Volume**: 1M articles (500K active, 500K archived)
- **Content Types**: Articles (80%), videos (10%), podcasts (5%), galleries (5%)
- **Update Frequency**: 50-500 new articles/day, 10-50 updates/day
- **Search Traffic**: 5M searches/month (10-20% of sessions use search)
- **Geographic Distribution**: 70% US, 20% Europe, 10% other
- **SEO Critical**: Search must be fast, relevant, indexable by Google

### Content Search Requirements
- **Latency**: <100ms p95 (full-text search, acceptable delay)
- **Full-Text Search**: Query across title, body, summary, tags
- **Faceting**: Author, category, publish date, content type, tags
- **Date Filtering**: Recent (last 7 days), last month, last year, all time
- **Ranking**: Relevance + recency + engagement (views, shares, comments)
- **Autocomplete**: Query suggestions (trending topics, popular searches)
- **Scale**: 1M+ documents, 5M+ searches/month
- **Cost Efficiency**: Target $500-2K/month (content is cost center)

---

## Search Platform Evaluation

### Evaluation Criteria

| Criterion | Weight | Meilisearch | Typesense | Algolia | OpenSearch | Azure AI Search | Notes |
|-----------|--------|-------------|-----------|---------|-----------|----------------|-------|
| **Cost Efficiency** | 25% | 9/10 | 10/10 | 5/10 | 7/10 | 7/10 | Type/Meili 5-10× cheaper than Algolia |
| **Full-Text Search** | 20% | 9/10 | 9/10 | 9/10 | 10/10 | 9/10 | All excellent, OpenSearch best for complex queries |
| **Scale (1M+ docs)** | 20% | 8/10 | 8/10 | 10/10 | 10/10 | 9/10 | Algolia/OpenSearch proven at 1B+ docs |
| **Faceting/Filtering** | 15% | 9/10 | 9/10 | 10/10 | 9/10 | 8/10 | All handle facets well |
| **Date Range Queries** | 10% | 8/10 | 8/10 | 9/10 | 10/10 | 8/10 | OpenSearch best (Elasticsearch heritage) |
| **Implementation Time** | 10% | 9/10 | 8/10 | 9/10 | 5/10 | 6/10 | Meilisearch/Algolia fastest (1-3 days) |
| **Total Score** | 100% | **8.8/10** | **8.8/10** | **8.4/10** | **8.6/10** | **7.9/10** | Meilisearch/Typesense tie |

### Winner: Meilisearch or Typesense (both excellent, choose by DX preference or price)
### Alternative: AWS OpenSearch (if AWS-heavy or need advanced aggregations)

---

## Platform Deep Dive

### Option 1: Meilisearch Pro (Recommended for Best DX)

**Pricing**: **$300/month** (Pro: 1M docs, 100M API calls, multi-region, hybrid search)

**Pros**:
- ✅ **Best DX** (9.0/10, fastest to production, 1-3 days setup)
- ✅ **Hybrid search included** ($300/month for AI features vs Algolia $10K+/month)
- ✅ **15-25ms latency** (excellent performance, sub-50ms consistently)
- ✅ **1M docs capacity** (fits entire content archive)
- ✅ **Predictable pricing** ($300/month fixed, no usage-based surprises)
- ✅ **Full-text search** (excellent relevance, typo tolerance)
- ✅ **Strong faceting** (30+ facets, date ranges, complex filters)
- ✅ **MIT license** (most permissive, can self-host if needed)

**Cons**:
- ⚠️ **No built-in analytics** (need to implement tracking, 40-80 hours)
- ⚠️ **Limited docs on advanced features** (vs Algolia comprehensive guides)
- ⚠️ **Smaller community** (vs Elasticsearch massive ecosystem)

**TCO (3-year, 1M docs, 5M searches/month)**:
- License: $300/month × 36 months = **$10,800**
- Engineering (setup 60h + maintenance 10h/month + analytics 60h): 60 + (10 × 36) + 60 = 480 hours × $100 = **$48,000**
- **Total TCO**: **$58,800** (3-year)

**When to Choose Meilisearch**:
- Prioritize developer experience (fastest implementation)
- Want hybrid search without premium pricing ($300/month vs Algolia $10K+/month)
- Content site with 500K-5M articles (fits in 1M doc limit)
- Budget $300-500/month

---

### Option 2: Typesense Business (Recommended for Best Price)

**Pricing**: **$300/month** (Business: 8 CPU, 16GB RAM, 2M records, unlimited searches)

**Pros**:
- ✅ **Predictable pricing** ($300/month fixed, no usage-based)
- ✅ **10-20ms latency** (excellent performance, InstantSearch compatible)
- ✅ **5-10 second purge** (fastest, critical for breaking news updates)
- ✅ **2M doc capacity** (double Meilisearch, fits larger archives)
- ✅ **Strong full-text search** (typo tolerance, faceting, date ranges)
- ✅ **Good DX** (7.4/10, straightforward API)

**Cons**:
- ⚠️ **No built-in analytics** (DIY, 40-80 hours)
- ⚠️ **Slightly lower DX** (vs Meilisearch 9.0/10)
- ⚠️ **Smaller community** (vs Elasticsearch)

**TCO (3-year, 1M docs, 5M searches/month)**:
- License: $300/month × 36 months = **$10,800**
- Engineering (setup 80h + maintenance 10h/month + analytics 60h): 80 + (10 × 36) + 60 = 500 hours × $100 = **$50,000**
- **Total TCO**: **$60,800** (3-year)

**When to Choose Typesense**:
- Want predictable pricing ($300/month, no surprises)
- Need fast purge (breaking news, <10s update requirement)
- Content archive >1M articles (Typesense 2M vs Meilisearch 1M)
- Budget $300-500/month

---

### Option 3: AWS OpenSearch (Best for AWS-Native)

**Pricing**: **$800-1,200/month** (3 m5.large.search instances, 3 replicas, 1TB storage)

**Pros**:
- ✅ **Proven at scale** (50B+ documents, battle-tested)
- ✅ **Advanced aggregations** (date histograms, trending topics, analytics)
- ✅ **AWS integration** (CloudWatch, S3 snapshots, IAM auth, Kinesis)
- ✅ **Powerful query DSL** (complex boolean, nested queries, geo-search)
- ✅ **OpenSearch Dashboards** (built-in analytics, Kibana fork)

**Cons**:
- ⚠️ **Expensive** ($800-1,200/month vs Meilisearch $300/month, 3-4× more)
- ⚠️ **50-200ms latency** (slower than Meilisearch/Typesense, but acceptable)
- ⚠️ **Complex setup** (clusters, shards, replicas, 2-4 weeks implementation)
- ⚠️ **AWS lock-in** (IAM, CloudWatch, S3, harder to migrate)

**TCO (3-year, 1M docs, 5M searches/month)**:
- License: $1,000/month × 36 months = **$36,000**
- Engineering (setup 200h + maintenance 20h/month): 200 + (20 × 36) = 920 hours × $100 = **$92,000**
- **Total TCO**: **$128,000** (3-year)

**When to Choose AWS OpenSearch**:
- Already AWS-heavy (S3, CloudWatch, Kinesis, Lambda)
- Need advanced analytics (trending topics, date histograms, dashboards)
- Need proven scale (5M+ articles, 50M+ searches/month)
- Budget $800-2K/month

---

### Option 4: Algolia (Not Recommended for Content Sites)

**Pricing**: **$1,485/month** (Grow Plus: 1M records, 10M searches)

**Why Not Recommended**:
- ❌ **5× more expensive** ($1,485/month vs Meilisearch $300/month)
- ❌ **Usage-based pricing** (5M searches = overage charges, unpredictable)
- ❌ **Overkill** (content search doesn't need global CDN, merchandising UI)
- ❌ **Same quality** (Meilisearch has comparable relevance for content)

**Only Consider If**: Global audience + need <50ms worldwide (rare for content sites, 50-100ms acceptable)

---

## Architecture Pattern: Content/Media Site Search

### Phase 1: Full-Text Search with CMS Integration

**Architecture** (WordPress + Meilisearch):
```
┌─────────────────────────────────────────────────────────────────┐
│                        Content Site (WordPress)                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Search UI (Custom or InstantSearch)                       │   │
│  │  - Search box (autocomplete, trending topics)             │   │
│  │  - Results (title, summary, author, date, thumbnail)      │   │
│  │  - Facets (category, author, date, content type)          │   │
│  │  - Pagination (load more, infinite scroll)                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Search API calls
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Meilisearch ($300/month)                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Index: articles                                           │   │
│  │  - 1M documents (posts)                                   │   │
│  │  - Fields: title, summary, body, author, category,        │   │
│  │    tags, publish_date, thumbnail, url                     │   │
│  │  - Searchable: title (priority), summary, body, tags      │   │
│  │  - Facets: category, author, publish_date, content_type   │   │
│  │  - Ranking: relevance + recency + engagement (views)      │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Index updates (on publish/update)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                 WordPress Plugin (Custom PHP)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Hooks:                                                    │   │
│  │  - publish_post → index to Meilisearch                    │   │
│  │  - save_post → update Meilisearch                         │   │
│  │  - trash_post → delete from Meilisearch                   │   │
│  │  - Schedule: full reindex daily (catch missed updates)    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Read/write posts
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   WordPress Database (MySQL)                     │
│  - wp_posts (1M articles, title, body, author, category)         │
│  - wp_postmeta (custom fields, views count, featured)            │
│  - wp_terms (categories, tags, taxonomy)                         │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow**:
1. **User types query** → Search UI sends API request to Meilisearch (15-25ms)
2. **Meilisearch** → Returns results (title, summary, author, date, thumbnail)
3. **User filters** → Facet selection (category, date range), re-query (15-25ms)
4. **User clicks article** → Navigate to article page (WordPress renders)

---

### Phase 2: Advanced Ranking (Recency + Engagement)

**Custom Ranking Formula**:
```javascript
// Meilisearch ranking (configure index settings)
await index.updateSettings({
  searchableAttributes: [
    'title',      // Highest priority (exact match in title = top result)
    'summary',    // Second priority
    'body',       // Third priority (full-text)
    'tags'        // Fourth priority
  ],

  filterableAttributes: [
    'category',
    'author',
    'publish_date',
    'content_type',
    'is_featured'
  ],

  sortableAttributes: [
    'publish_date',
    'views_count',
    'engagement_score'
  ],

  rankingRules: [
    'words',       // More matched words = higher rank
    'typo',        // Fewer typos = higher rank
    'proximity',   // Words closer together = higher rank
    'attribute',   // Match in searchableAttributes order
    'sort',        // Apply sortable attributes (recency, engagement)
    'exactness'    // Exact match = higher rank
  ]
});

// Custom engagement score (calculate before indexing)
function calculateEngagementScore(article) {
  const ageInDays = (Date.now() - article.publish_date) / (1000 * 60 * 60 * 24);
  const recencyScore = Math.max(0, 100 - ageInDays); // Decay over 100 days
  const viewsScore = Math.min(100, article.views_count / 100); // Normalize views (max 100)
  const sharesScore = Math.min(100, article.shares_count / 10); // Normalize shares (max 100)

  return (recencyScore * 0.5) + (viewsScore * 0.3) + (sharesScore * 0.2);
}
```

---

## Implementation Guide

### Step 1: WordPress Plugin (PHP)

**Create custom plugin** (`wp-content/plugins/meilisearch-integration/meilisearch.php`):
```php
<?php
/**
 * Plugin Name: Meilisearch Integration
 * Description: Index WordPress posts to Meilisearch
 * Version: 1.0
 */

require_once 'vendor/autoload.php';
use MeiliSearch\Client;

class WP_Meilisearch {
  private $client;
  private $index;

  public function __construct() {
    $this->client = new Client(
      getenv('MEILISEARCH_HOST'),
      getenv('MEILISEARCH_API_KEY')
    );
    $this->index = $this->client->index('articles');

    // Hooks
    add_action('publish_post', [$this, 'index_post'], 10, 1);
    add_action('save_post', [$this, 'update_post'], 10, 1);
    add_action('trash_post', [$this, 'delete_post'], 10, 1);

    // Schedule full reindex daily
    add_action('wp', [$this, 'schedule_full_reindex']);
    add_action('meilisearch_full_reindex', [$this, 'full_reindex']);
  }

  public function index_post($post_id) {
    $post = get_post($post_id);
    if ($post->post_status !== 'publish') return;

    $document = $this->transform_post($post);
    $this->index->addDocuments([$document]);
  }

  public function update_post($post_id) {
    $this->index_post($post_id);
  }

  public function delete_post($post_id) {
    $this->index->deleteDocument($post_id);
  }

  private function transform_post($post) {
    $categories = wp_get_post_categories($post->ID, ['fields' => 'names']);
    $tags = wp_get_post_tags($post->ID, ['fields' => 'names']);
    $author = get_the_author_meta('display_name', $post->post_author);
    $thumbnail = get_the_post_thumbnail_url($post->ID, 'medium');
    $views_count = get_post_meta($post->ID, 'views_count', true) ?: 0;

    return [
      'id' => $post->ID,
      'title' => $post->post_title,
      'summary' => $post->post_excerpt ?: wp_trim_words($post->post_content, 30),
      'body' => wp_strip_all_tags($post->post_content),
      'author' => $author,
      'category' => $categories,
      'tags' => $tags,
      'publish_date' => strtotime($post->post_date),
      'thumbnail' => $thumbnail,
      'url' => get_permalink($post->ID),
      'content_type' => $post->post_type,
      'views_count' => intval($views_count),
      'engagement_score' => $this->calculate_engagement_score($post, $views_count)
    ];
  }

  private function calculate_engagement_score($post, $views_count) {
    $age_in_days = (time() - strtotime($post->post_date)) / (60 * 60 * 24);
    $recency_score = max(0, 100 - $age_in_days);
    $views_score = min(100, $views_count / 100);

    return ($recency_score * 0.5) + ($views_score * 0.5);
  }

  public function schedule_full_reindex() {
    if (!wp_next_scheduled('meilisearch_full_reindex')) {
      wp_schedule_event(time(), 'daily', 'meilisearch_full_reindex');
    }
  }

  public function full_reindex() {
    $args = [
      'post_type' => 'post',
      'post_status' => 'publish',
      'posts_per_page' => -1
    ];

    $posts = get_posts($args);
    $documents = array_map([$this, 'transform_post'], $posts);

    // Clear index and re-add all documents
    $this->index->deleteAllDocuments();
    $this->index->addDocuments($documents);

    error_log("Meilisearch: Indexed " . count($documents) . " posts");
  }
}

new WP_Meilisearch();
```

---

### Step 2: Frontend Search UI (JavaScript)

**Custom search page** (`search.php` WordPress template):
```php
<?php get_header(); ?>

<div id="search-container"></div>

<script>
const searchApp = {
  client: null,
  index: null,
  query: '',
  results: [],
  facets: {
    category: [],
    author: [],
    dateRange: 'all'
  },

  init() {
    this.client = new MeiliSearch({
      host: '<?php echo getenv("MEILISEARCH_HOST"); ?>',
      apiKey: '<?php echo getenv("MEILISEARCH_SEARCH_KEY"); ?>'
    });
    this.index = this.client.index('articles');

    this.renderUI();
    this.attachEventListeners();
  },

  async search() {
    const filters = [];

    // Category filter
    if (this.facets.category.length > 0) {
      filters.push(`category IN [${this.facets.category.map(c => `"${c}"`).join(',')}]`);
    }

    // Date range filter
    const now = Math.floor(Date.now() / 1000);
    if (this.facets.dateRange === '7days') {
      filters.push(`publish_date > ${now - (7 * 24 * 60 * 60)}`);
    } else if (this.facets.dateRange === '30days') {
      filters.push(`publish_date > ${now - (30 * 24 * 60 * 60)}`);
    }

    const searchResults = await this.index.search(this.query, {
      limit: 20,
      filter: filters.join(' AND '),
      attributesToHighlight: ['title', 'summary'],
      sort: ['engagement_score:desc', 'publish_date:desc']
    });

    this.results = searchResults.hits;
    this.renderResults();
  },

  renderUI() {
    document.getElementById('search-container').innerHTML = `
      <input id="search-input" type="text" placeholder="Search articles..." />

      <div id="facets">
        <select id="date-range">
          <option value="all">All Time</option>
          <option value="7days">Last 7 Days</option>
          <option value="30days">Last 30 Days</option>
        </select>
      </div>

      <div id="search-results"></div>
    `;
  },

  attachEventListeners() {
    document.getElementById('search-input').addEventListener('input', (e) => {
      this.query = e.target.value;
      this.search();
    });

    document.getElementById('date-range').addEventListener('change', (e) => {
      this.facets.dateRange = e.target.value;
      this.search();
    });
  },

  renderResults() {
    const resultsHTML = this.results.map(hit => `
      <article class="search-result">
        <img src="${hit.thumbnail}" alt="${hit.title}" />
        <h3><a href="${hit.url}">${hit._formatted?.title || hit.title}</a></h3>
        <p>${hit._formatted?.summary || hit.summary}</p>
        <div class="meta">
          <span class="author">By ${hit.author}</span>
          <span class="date">${new Date(hit.publish_date * 1000).toLocaleDateString()}</span>
          <span class="category">${hit.category.join(', ')}</span>
        </div>
      </article>
    `).join('');

    document.getElementById('search-results').innerHTML = resultsHTML || '<p>No results found.</p>';
  }
};

searchApp.init();
</script>

<?php get_footer(); ?>
```

---

## Testing & Validation

### Performance Benchmarks

**Latency test** (target: <100ms p95):
```bash
# Apache Bench (1000 requests, 10 concurrent)
ab -n 1000 -c 10 "https://ms-xxx.meilisearch.io/indexes/articles/search?q=technology" \
  -H "Authorization: Bearer SEARCH_KEY"

# Expected results:
# - Meilisearch: 15-30ms median, 50-80ms p95 ✅
# - Typesense: 15-25ms median, 40-60ms p95 ✅
# - OpenSearch: 50-150ms median, 200-300ms p95 (acceptable for content)
```

### Relevance Testing

**Test queries** (news/blog content):
```javascript
const testQueries = [
  { query: 'artificial intelligence', expectedCategories: ['Technology', 'AI', 'Innovation'] },
  { query: 'climate change', expectedCategories: ['Environment', 'Science', 'Politics'] },
  { query: 'startup funding', expectedCategories: ['Business', 'Startups', 'Finance'] }
];

for (const test of testQueries) {
  const results = await index.search(test.query, { limit: 10 });
  const categories = results.hits.flatMap(hit => hit.category);

  console.log(`Query: "${test.query}"`);
  console.log(`Expected categories: ${test.expectedCategories.join(', ')}`);
  console.log(`Actual categories: ${[...new Set(categories)].join(', ')}`);
  console.log(`Relevance: ${test.expectedCategories.some(cat => categories.includes(cat)) ? '✅' : '❌'}`);
}
```

---

## Cost-Benefit Analysis (3-Year)

### Scenario: Digital Media Site (20M pageviews/month)

**Baseline (No Search or Basic WordPress Search)**:
- Search engagement: 5% of sessions (basic WP search is bad)
- Pageviews per search session: 2 pages

**With Meilisearch/Typesense Search**:
- Search engagement: 15% of sessions (3× improvement from better UX)
- Pageviews per search session: 4 pages (2× improvement from better results)
- **Incremental pageviews**: 20M × (15% × 4 - 5% × 2) = 10M pageviews/month

**Revenue Impact** (ad-supported model):
- CPM: $5 (typical for content sites)
- Incremental revenue: 10M pageviews × $5 CPM / 1000 = **$50K/month**
- **3-year incremental revenue**: $50K × 36 = **$1.8M**

**TCO**:
- Meilisearch: $58,800 (3-year)
- Typesense: $60,800 (3-year)

**ROI**:
- **Meilisearch**: ($1.8M - $58.8K) / $58.8K = **30× ROI**
- **Typesense**: ($1.8M - $60.8K) / $60.8K = **29× ROI**

**Winner**: Meilisearch (slightly better DX, hybrid search included)

---

## Migration Strategy

### Phased Rollout (3-4 Weeks)

**Week 1: Setup & Indexing**
- Set up Meilisearch/Typesense instance
- Create WordPress plugin (indexing hooks)
- Full reindex (1M articles, 2-4 hours)
- Configure ranking (relevance + recency + engagement)

**Week 2: Frontend Development**
- Build search UI (React or vanilla JS)
- Implement facets (category, author, date)
- Test on staging (performance, relevance)

**Week 3: Soft Launch (10% Traffic)**
- Deploy to production (feature flag 10% users)
- Monitor: latency, engagement, errors
- A/B test: new search vs old WP search

**Week 4: Full Launch (100% Traffic)**
- Increase to 100% traffic
- Monitor for 2 weeks
- Decommission old search

---

## Final Recommendation

### For Content/Media Sites (1M+ articles):

**Choose Meilisearch Pro** ($300/month):
- ✅ Best DX (9.0/10, fastest implementation)
- ✅ Hybrid search included ($300/month vs Algolia $10K+/month)
- ✅ 1M doc capacity (fits most content sites)
- ✅ Excellent performance (15-25ms latency)

**Choose Typesense Business** ($300/month):
- ✅ Predictable pricing (fixed $300/month)
- ✅ Fast purge (5-10s, critical for breaking news)
- ✅ 2M doc capacity (larger archives)
- ✅ Excellent performance (15-25ms latency)

**Choose AWS OpenSearch** ($800-1,200/month):
- ✅ AWS-native (already using S3, CloudWatch, Kinesis)
- ✅ Advanced analytics (trending topics, dashboards)
- ✅ Proven at massive scale (5M+ articles, 50M+ searches/month)

**Avoid**:
- ❌ Algolia ($1,485/month): Too expensive (5× Meilisearch cost, no benefit for content search)
- ❌ Azure AI Search ($250-500/month): Slower (50-150ms), Azure lock-in, OData complexity

---

**Last Updated**: November 14, 2025
**Scenario**: Content/Media Site Search (News, Blog, Publishing)
**Recommended Platform**: Meilisearch or Typesense ($300/month)
**Expected ROI**: 29-30× (3-year)
