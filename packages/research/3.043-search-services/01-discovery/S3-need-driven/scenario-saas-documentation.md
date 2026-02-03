# S3 Scenario 2: SaaS Documentation & Help Center Search

**Company Profile**: B2B SaaS company, developer tools or business software
**Search Volume**: 10K documents (docs, API reference, help articles), 50K searches/month
**Budget**: $0-500/month for documentation search
**Priority**: Fast implementation, developer-friendly, low maintenance, free/cheap

---

## Business Context

### Company Details
- **Stage**: Seed to Series B
- **Team Size**: 10-50 employees, 5-20 engineers, 1-2 on docs
- **Users**: 5K-50K developers/business users
- **Revenue**: $500K-10M ARR
- **Growth**: 100-200% YoY
- **Business Model**: SaaS subscription ($50-500/user/month)

### Technical Environment
- **Documentation Stack**: Docusaurus, VitePress, GitBook, or custom static site
- **Content**: 5K-10K pages (guides, tutorials, API reference, changelogs)
- **Traffic**: 50K-500K pageviews/month, 50K-100K searches/month
- **Content Update Frequency**: Daily (docs updates, new features, API changes)
- **Geographic Distribution**: 50% US, 30% Europe, 10% APAC, 10% other
- **User Type**: 70% developers (technical, API docs), 30% business users (help articles)

### Documentation Search Requirements
- **Latency**: <100ms acceptable (not instant search UX, but fast enough)
- **Relevance**: High (developers search for specific API methods, error codes)
- **Content Types**: Markdown docs, API reference (OpenAPI), code snippets, changelogs
- **Versioning**: Multiple versions (v1.0, v2.0, latest) with version-specific search
- **Multilingual**: Optional (English + 2-3 languages for global SaaS)
- **Autocomplete**: Query suggestions (API method names, error codes)
- **Free/Cheap**: Target $0-100/month (documentation is cost center, not revenue driver)

---

## Search Platform Evaluation

### Evaluation Criteria

| Criterion | Weight | Algolia DocSearch | Meilisearch | Typesense | Azure AI Search | Notes |
|-----------|--------|-------------------|-------------|-----------|----------------|-------|
| **Cost (Free/Cheap)** | 30% | 10/10 | 10/10 | 9/10 | 5/10 | DocSearch free, Meili $30, Type $20 |
| **Ease of Setup** | 25% | 10/10 | 9/10 | 8/10 | 5/10 | DocSearch申请→approval, Meili 1-2 days |
| **Developer Experience** | 20% | 9/10 | 9/10 | 8/10 | 6/10 | All have good DX, Azure complex |
| **Versioning Support** | 10% | 8/10 | 7/10 | 7/10 | 8/10 | DocSearch built-in, others DIY |
| **Performance** | 10% | 9/10 | 9/10 | 9/10 | 7/10 | All sub-100ms (acceptable) |
| **Maintenance** | 5% | 10/10 | 7/10 | 7/10 | 6/10 | DocSearch zero maintenance |
| **Total Score** | 100% | **9.5/10** | **8.9/10** | **8.2/10** | **6.0/10** | DocSearch wins (free + zero maintenance) |

### Winner: Algolia DocSearch (free for open-source or public docs)
### Alternative: Meilisearch Build ($30/month, for private docs or need more control)

---

## Platform Deep Dive

### Option 1: Algolia DocSearch (Recommended for Public Docs)

**Pricing**: **$0/month** (free for open-source, technical documentation, non-commercial)

**Eligibility Requirements**:
- ✅ Documentation is publicly available (not behind paywall)
- ✅ Content is technical documentation (not marketing, not e-commerce)
- ✅ Apply via docsearch.algolia.com/apply
- ⚠️ Approval process (1-2 weeks, manual review)
- ❌ Not eligible: Private docs, commercial content, non-technical sites

**Pros**:
- ✅ **Free forever** (no bandwidth limits, no search limits)
- ✅ **Zero maintenance** (Algolia manages crawling, indexing, updates)
- ✅ **Pre-built UI** (DocSearch React/JS component, drop-in integration)
- ✅ **Automatic crawling** (weekly scheduled, or on-demand via API)
- ✅ **Versioning support** (built-in, URL-based versioning)
- ✅ **Excellent DX** (9/10, 1-2 hours to integrate)
- ✅ **Used by**: React, Vue, Tailwind CSS, Docusaurus, VitePress (proven at scale)

**Cons**:
- ⚠️ **Approval required** (1-2 weeks, not guaranteed, public docs only)
- ⚠️ **Limited customization** (can't control ranking formula, indexing logic)
- ⚠️ **No private docs** (must be publicly accessible)
- ⚠️ **Crawler-based** (weekly updates, not real-time, can trigger on-demand but 24h delay)

**TCO (3-year)**: **$0** (free)

**Engineering Effort**:
- Setup: 2-4 hours (apply, configure, integrate UI)
- Maintenance: 0 hours/month (Algolia manages crawling)
- Total: **2-4 hours** ($200-400 one-time cost)

**When to Choose DocSearch**:
- Documentation is public (not behind paywall)
- Open-source project or technical documentation site
- Want zero maintenance (no DevOps, no indexing scripts)
- Budget $0 (free is hard to beat)

**How to Apply**:
1. Go to docsearch.algolia.com/apply
2. Fill form: URL, email, description
3. Wait 1-2 weeks for approval
4. Receive API keys + config
5. Integrate DocSearch UI component

**Integration Example** (Docusaurus):
```jsx
// docusaurus.config.js
module.exports = {
  themeConfig: {
    algolia: {
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'YOUR_INDEX_NAME',
      appId: 'YOUR_APP_ID',
      contextualSearch: true, // Enable versioning
      searchParameters: {
        facetFilters: ['version:VERSION'] // Filter by version
      }
    }
  }
};
```

---

### Option 2: Meilisearch Build (Best for Private Docs)

**Pricing**: **$30/month** (Build plan: 100K docs, 10M API calls, hybrid search included)

**Pros**:
- ✅ **Cheapest paid option** ($30/month, vs Algolia paid $245/month)
- ✅ **Private docs** (no public requirement, works behind auth)
- ✅ **Full control** (custom ranking, indexing logic, update frequency)
- ✅ **Hybrid search** (keyword + semantic, included at $30/month)
- ✅ **Real-time indexing** (push updates via API, <10s delay)
- ✅ **Excellent DX** (9.0/10, fastest to production)
- ✅ **DocSearch UI compatible** (can reuse Algolia's DocSearch UI)

**Cons**:
- ⚠️ **Not free** ($30/month vs DocSearch $0)
- ⚠️ **DIY indexing** (need to write crawling/indexing scripts, 20-40 hours)
- ⚠️ **Maintenance** (5-10 hours/month, monitor uptime, update indexing)

**TCO (3-year)**:
- License: $30/month × 36 months = **$1,080**
- Engineering (setup 40h + maintenance 5h/month): 40 + (5 × 36) = 220 hours × $100 = **$22,000**
- Total: **$23,080** (3-year)

**When to Choose Meilisearch**:
- Documentation is private (behind auth, not eligible for DocSearch)
- Need real-time indexing (docs update hourly, not weekly)
- Want hybrid search (semantic understanding, better relevance)
- Budget $30-100/month (acceptable for private docs)

**Implementation** (Docusaurus + Meilisearch):
```javascript
// scripts/index-docs.js
const { MeiliSearch } = require('meilisearch');
const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

const client = new MeiliSearch({ host: 'https://ms-xxx.meilisearch.io', apiKey: 'ADMIN_KEY' });

async function indexDocs() {
  const docsDir = './docs';
  const documents = [];

  // Recursively read all markdown files
  function readDocs(dir) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        readDocs(filePath);
      } else if (file.endsWith('.md') || file.endsWith('.mdx')) {
        const content = fs.readFileSync(filePath, 'utf-8');
        const { data: frontmatter, content: markdown } = matter(content);

        documents.push({
          id: filePath,
          title: frontmatter.title || file,
          description: frontmatter.description || '',
          content: markdown.slice(0, 5000), // First 5000 chars
          url: filePath.replace('./docs', '/docs').replace(/\.mdx?$/, ''),
          version: frontmatter.version || 'latest',
          category: frontmatter.category || 'General',
          tags: frontmatter.tags || []
        });
      }
    });
  }

  readDocs(docsDir);

  // Index to Meilisearch
  const index = client.index('documentation');
  await index.addDocuments(documents);

  console.log(`Indexed ${documents.length} documents`);
}

indexDocs();
```

---

### Option 3: Typesense (Alternative to Meilisearch)

**Pricing**: **$20/month** (Hobby: 2 CPU, 2GB RAM, 100K records, unlimited searches)

**Pros**:
- ✅ **Cheapest** ($20/month, even cheaper than Meilisearch $30)
- ✅ **Predictable pricing** (fixed resources, no usage-based)
- ✅ **Good performance** (15-25ms, sub-50ms consistently)
- ✅ **DocSearch UI compatible** (can reuse Algolia's UI)

**Cons**:
- ⚠️ **DIY indexing** (same as Meilisearch, 20-40 hours)
- ⚠️ **Lower resource limits** (2GB RAM vs Meilisearch 4GB on Build)
- ⚠️ **Slightly lower DX** (7.4/10 vs Meilisearch 9.0/10)

**TCO (3-year)**: $20/month × 36 = $720 + $22,000 engineering = **$22,720**

**When to Choose Typesense**:
- Want cheapest option ($20 vs Meilisearch $30)
- Docs <10K pages (fit in 2GB RAM)
- Predictable pricing preferred

---

### Option 4: Algolia Paid (Not Recommended for Docs)

**Pricing**: $245/month (Grow: 100K records, 1M searches)

**Why Not Recommended**:
- ❌ **Too expensive** ($245/month vs Meilisearch $30/month, 8× more)
- ❌ **Overkill** (documentation search doesn't need premium features)
- ❌ **Same features** (Meilisearch has same search quality for docs)

**Only Consider If**: DocSearch rejected AND need Algolia's merchandising/analytics (rare for docs)

---

## Architecture Pattern: Documentation Search

### Phase 1: Static Site + Search Integration

**Architecture** (Docusaurus + Algolia DocSearch):
```
┌─────────────────────────────────────────────────────────────────┐
│                        Documentation Site                        │
│                      (Docusaurus / VitePress)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ DocSearch UI Component                                    │   │
│  │  - Search modal (Cmd+K / Ctrl+K)                          │   │
│  │  - Autocomplete (API methods, guides)                     │   │
│  │  - Results with snippets (highlighted matches)            │   │
│  │  - Keyboard navigation (up/down, enter)                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Search API calls
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Algolia DocSearch (Free)                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Index: documentation                                      │   │
│  │  - 10K documents (pages, sections, headings)              │   │
│  │  - Fields: title, content, url, version, category         │   │
│  │  - Searchable: title (priority), headings, content        │   │
│  │  - Facets: version, category                              │   │
│  │  - Ranking: title match > heading match > content match   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Automatic weekly crawl
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Algolia Crawler (Managed)                      │
│  - Crawls docs site weekly (or on-demand trigger)                │
│  - Parses HTML, extracts text, metadata                          │
│  - Indexes to DocSearch index (automatic)                        │
│  - Zero maintenance (Algolia manages)                            │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Crawls public URL
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              Static Site (Vercel / Netlify / GitHub Pages)       │
│  - HTML pages (built from Markdown)                              │
│  - Versioned URLs (/v1.0/guide, /v2.0/guide, /latest/guide)     │
│  - Publicly accessible (required for DocSearch)                  │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow**:
1. **User presses Cmd+K** → DocSearch modal opens
2. **User types query** ("API authentication") → Algolia searches index (10-20ms)
3. **Results returned** → Show matched pages with snippets (highlighted)
4. **User clicks result** → Navigate to docs page

**Zero Maintenance**: Algolia crawls weekly, updates index automatically

---

### Phase 2: Private Docs + Real-Time Indexing (Meilisearch)

**Architecture** (GitBook/Custom + Meilisearch):
```
┌─────────────────────────────────────────────────────────────────┐
│                   Documentation Site (Private)                   │
│  - Behind authentication (Auth0, Clerk, custom)                  │
│  - Search UI (DocSearch compatible, custom styling)              │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Search API calls
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Meilisearch ($30/month)                        │
│  - Index: documentation (10K docs)                               │
│  - Hybrid search (keyword + semantic, included)                  │
│  - Version faceting (filter by v1.0, v2.0, latest)               │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Index updates via API (real-time)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Indexing Pipeline (Node.js)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. Watch docs directory for changes (fs.watch)           │   │
│  │ 2. On file change: parse Markdown, extract metadata      │   │
│  │ 3. Push to Meilisearch index (addDocuments API)          │   │
│  │ 4. Trigger: on git commit, or real-time file watcher     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Read docs source
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              Documentation Source (Git Repo)                     │
│  - Markdown files (./docs/*.md)                                  │
│  - Frontmatter metadata (title, description, version, category)  │
│  - CI/CD pipeline (on push → build → index → deploy)            │
└─────────────────────────────────────────────────────────────────┘
```

**Real-Time Indexing** (trigger on git commit):
```yaml
# .github/workflows/index-docs.yml
name: Index Documentation
on:
  push:
    branches: [main]
    paths: ['docs/**']

jobs:
  index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: node scripts/index-docs.js
        env:
          MEILISEARCH_HOST: ${{ secrets.MEILISEARCH_HOST }}
          MEILISEARCH_API_KEY: ${{ secrets.MEILISEARCH_API_KEY }}
```

---

## Implementation Guide

### Option A: Docusaurus + Algolia DocSearch (Free)

**Step 1: Apply for DocSearch** (Week 1)
1. Go to docsearch.algolia.com/apply
2. Fill form: docs URL, email, description
3. Wait 1-2 weeks for approval
4. Receive email with API keys

**Step 2: Configure Docusaurus** (Day 1, after approval)
```javascript
// docusaurus.config.js
module.exports = {
  title: 'My SaaS Documentation',
  url: 'https://docs.myapp.com',
  themeConfig: {
    algolia: {
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_SEARCH_API_KEY', // Public search-only key
      indexName: 'myapp_docs',

      // Contextual search (version filtering)
      contextualSearch: true,

      // Optional: custom search parameters
      searchParameters: {
        facetFilters: ['version:latest']
      },

      // Optional: custom placeholder
      placeholder: 'Search docs...',

      // Optional: custom styling
      searchPagePath: 'search'
    },

    navbar: {
      items: [
        {
          type: 'docsVersionDropdown', // Version switcher
          position: 'left'
        },
        {
          type: 'search',
          position: 'right'
        }
      ]
    }
  }
};
```

**Step 3: Test Search**
1. Build docs: `npm run build`
2. Deploy to production
3. Wait for Algolia crawler (weekly, or trigger via docsearch.algolia.com dashboard)
4. Test search: Cmd+K, type query, verify results

**Total Time**: 2-4 hours (after DocSearch approval)

---

### Option B: VitePress + Meilisearch (Private Docs)

**Step 1: Set Up Meilisearch** (Day 1)
```bash
# Sign up for Meilisearch Cloud (meilisearch.com)
# Create project, get API keys (host URL + master key)
```

**Step 2: Create Indexing Script** (Day 1)
```javascript
// scripts/index-vitepress-docs.js
const { MeiliSearch } = require('meilisearch');
const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');
const MarkdownIt = require('markdown-it');

const md = new MarkdownIt();
const client = new MeiliSearch({
  host: process.env.MEILISEARCH_HOST,
  apiKey: process.env.MEILISEARCH_API_KEY
});

async function indexDocs() {
  const docsDir = './docs';
  const documents = [];
  let idCounter = 0;

  function readDocs(dir, urlPrefix = '') {
    const files = fs.readdirSync(dir);

    files.forEach(file => {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        readDocs(filePath, `${urlPrefix}/${file}`);
      } else if (file.endsWith('.md')) {
        const content = fs.readFileSync(filePath, 'utf-8');
        const { data: frontmatter, content: markdown } = matter(content);

        // Parse markdown to extract headings
        const tokens = md.parse(markdown, {});
        let currentHeading = '';
        let currentContent = '';

        tokens.forEach(token => {
          if (token.type === 'heading_open' && token.tag === 'h2') {
            // Save previous section
            if (currentHeading && currentContent) {
              documents.push({
                id: `${idCounter++}`,
                title: frontmatter.title || file.replace('.md', ''),
                heading: currentHeading,
                content: currentContent.trim().slice(0, 2000),
                url: `${urlPrefix}/${file.replace('.md', '')}.html#${currentHeading.toLowerCase().replace(/\s+/g, '-')}`,
                version: frontmatter.version || 'latest',
                category: frontmatter.category || 'General'
              });
            }

            currentContent = '';
          } else if (token.type === 'inline' && token.content) {
            if (tokens[tokens.indexOf(token) - 1]?.type === 'heading_open') {
              currentHeading = token.content;
            } else {
              currentContent += token.content + ' ';
            }
          }
        });

        // Add last section
        if (currentHeading && currentContent) {
          documents.push({
            id: `${idCounter++}`,
            title: frontmatter.title || file.replace('.md', ''),
            heading: currentHeading,
            content: currentContent.trim().slice(0, 2000),
            url: `${urlPrefix}/${file.replace('.md', '')}.html#${currentHeading.toLowerCase().replace(/\s+/g, '-')}`,
            version: frontmatter.version || 'latest',
            category: frontmatter.category || 'General'
          });
        }
      }
    });
  }

  readDocs(docsDir);

  // Create or update index
  try {
    await client.createIndex('documentation', { primaryKey: 'id' });
  } catch (err) {
    // Index already exists
  }

  const index = client.index('documentation');

  // Configure searchable/filterable attributes
  await index.updateSettings({
    searchableAttributes: ['title', 'heading', 'content'],
    filterableAttributes: ['version', 'category'],
    sortableAttributes: [],
    displayedAttributes: ['title', 'heading', 'content', 'url', 'version'],
    rankingRules: [
      'words',
      'typo',
      'proximity',
      'attribute',
      'sort',
      'exactness'
    ]
  });

  // Index documents
  await index.addDocuments(documents);

  console.log(`Indexed ${documents.length} sections from docs`);
}

indexDocs().catch(console.error);
```

**Step 3: Create Search UI Component** (Day 2)
```vue
<!-- .vitepress/theme/SearchModal.vue -->
<template>
  <div v-if="isOpen" class="search-modal">
    <input
      ref="searchInput"
      v-model="query"
      @input="search"
      placeholder="Search documentation..."
      class="search-input"
    />
    <div v-if="results.length" class="search-results">
      <a
        v-for="result in results"
        :key="result.id"
        :href="result.url"
        class="search-result"
      >
        <h4>{{ result.title }} › {{ result.heading }}</h4>
        <p>{{ result.content.slice(0, 150) }}...</p>
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { MeiliSearch } from 'meilisearch';

const client = new MeiliSearch({
  host: 'https://ms-xxx.meilisearch.io',
  apiKey: 'SEARCH_API_KEY' // Public search-only key
});

const isOpen = ref(false);
const query = ref('');
const results = ref([]);

async function search() {
  if (query.value.length < 2) {
    results.value = [];
    return;
  }

  const index = client.index('documentation');
  const searchResults = await index.search(query.value, {
    limit: 10,
    attributesToHighlight: ['title', 'heading', 'content']
  });

  results.value = searchResults.hits;
}

// Keyboard shortcut: Cmd+K or Ctrl+K
onMounted(() => {
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      isOpen.value = !isOpen.value;
    }
  });
});
</script>
```

**Step 4: Automate Indexing** (Day 2)
```yaml
# .github/workflows/index-docs.yml
name: Index Documentation
on:
  push:
    branches: [main]
    paths: ['docs/**']

jobs:
  index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: node scripts/index-vitepress-docs.js
        env:
          MEILISEARCH_HOST: ${{ secrets.MEILISEARCH_HOST }}
          MEILISEARCH_API_KEY: ${{ secrets.MEILISEARCH_API_KEY }}
```

**Total Time**: 2-3 days (indexing script 1 day, UI 1 day, automation 1 day)

---

## Versioning Strategy

### Multi-Version Documentation

**URL Structure**:
```
/docs/latest/getting-started    (default, latest version)
/docs/v2.0/getting-started      (v2.0, stable)
/docs/v1.0/getting-started      (v1.0, legacy)
```

**Meilisearch Index** (single index, version facet):
```javascript
// Index documents with version field
const documents = [
  { id: '1', title: 'Getting Started', version: 'latest', content: '...' },
  { id: '2', title: 'Getting Started', version: 'v2.0', content: '...' },
  { id: '3', title: 'Getting Started', version: 'v1.0', content: '...' }
];

// Search with version filter
const results = await index.search('getting started', {
  filter: 'version = "latest"' // Only search latest version
});
```

**Search UI** (version dropdown):
```vue
<select v-model="selectedVersion" @change="search">
  <option value="latest">Latest</option>
  <option value="v2.0">v2.0</option>
  <option value="v1.0">v1.0 (legacy)</option>
</select>
```

---

## Testing & Validation

### Relevance Testing

**Test queries** (API-focused documentation):
```javascript
const testQueries = [
  { query: 'authentication', expectedResults: ['API Authentication', 'OAuth Guide', 'API Keys'] },
  { query: 'rate limit', expectedResults: ['Rate Limiting', 'API Quotas', 'Usage Limits'] },
  { query: 'webhook', expectedResults: ['Webhooks Overview', 'Webhook Events', 'Webhook Security'] },
  { query: 'error 401', expectedResults: ['Authentication Errors', 'Troubleshooting 401', 'API Errors'] }
];

for (const test of testQueries) {
  const results = await index.search(test.query, { limit: 5 });
  const titles = results.hits.map(hit => hit.title);

  console.log(`Query: "${test.query}"`);
  console.log(`Expected: ${test.expectedResults.join(', ')}`);
  console.log(`Actual: ${titles.join(', ')}`);
  console.log(`Relevance: ${test.expectedResults.some(title => titles.includes(title)) ? '✅' : '❌'}`);
}
```

---

## Cost-Benefit Analysis (3-Year)

### Scenario: B2B SaaS ($2M ARR)

**Option 1: Algolia DocSearch (Free)**
- License: **$0**
- Engineering: 4 hours setup × $100 = **$400**
- **Total TCO**: **$400** (3-year)

**Option 2: Meilisearch ($30/month)**
- License: $30 × 36 = **$1,080**
- Engineering: 40h setup + 5h/month × 36 = 220h × $100 = **$22,000**
- **Total TCO**: **$23,080** (3-year)

**ROI Calculation**:
- **Documentation search doesn't directly drive revenue**
- **Indirect benefits**: Faster onboarding (reduce support tickets 10-20%), better developer experience (increase adoption 5-10%)
- **Support cost savings**: 10-20% fewer support tickets = 2-4 hours/week × 52 weeks × $50/hour = **$5,200-10,400/year** saved
- **3-year savings**: $15,600-31,200

**Winner**: Algolia DocSearch (free, zero maintenance, best ROI)

**When to use Meilisearch**: Private docs (not eligible for DocSearch) OR need real-time indexing (docs update hourly, not weekly)

---

## Final Recommendation

### For Public Documentation (Open-Source or Technical Docs):

**Choose Algolia DocSearch** (free):
- ✅ Free forever (no bandwidth/search limits)
- ✅ Zero maintenance (Algolia manages crawling)
- ✅ Pre-built UI (DocSearch component)
- ✅ Used by: React, Vue, Tailwind, Docusaurus, VitePress

**Apply at**: docsearch.algolia.com/apply (1-2 weeks approval)

### For Private Documentation (Behind Paywall):

**Choose Meilisearch Build** ($30/month):
- ✅ Cheapest private docs search ($30/month vs Algolia $245/month)
- ✅ Hybrid search included (semantic understanding)
- ✅ Real-time indexing (push via API, <10s delay)
- ✅ Excellent DX (9.0/10, fastest to production)

**Alternative**: Typesense ($20/month, if budget <$30/month)

### Avoid:
- ❌ Algolia Paid ($245/month): Too expensive for docs (8× Meilisearch cost, no benefit)
- ❌ Azure AI Search ($250/month): Too slow (50-150ms), too complex (OData), Azure lock-in

---

**Last Updated**: November 14, 2025
**Scenario**: SaaS Documentation & Help Center Search
**Recommended Platform**: Algolia DocSearch (free, public docs) or Meilisearch ($30/month, private docs)
**Expected TCO**: $400 (DocSearch) or $23K (Meilisearch, 3-year)
