# S3 Need-Driven: Executive Summary & Scenario Comparison

**Research Type**: MPSE (Managed Platform/Service Evaluation) - S3 Need-Driven
**Date**: November 14, 2025
**Scenarios Analyzed**: 6 (E-commerce, SaaS Docs, Content/Media, Enterprise Knowledge, Marketplace, Mobile App)
**Platforms Evaluated**: 7 (Algolia, Meilisearch, Typesense, Elasticsearch, AWS OpenSearch, Azure AI Search, Coveo)
**Total Research Depth**: ~2,400 lines across 6 scenario documents

---

## Executive Summary

S3 need-driven research reveals **no one-size-fits-all search platform**. Platform choice is highly scenario-dependent, driven by:

1. **Use case requirements** (instant search vs full-text vs enterprise unified search)
2. **Budget constraints** ($0-$500K/year, 1000× variance)
3. **Technical environment** (mobile-first, cloud-native, legacy systems)
4. **Scale** (10K-100M documents, 50K-100M searches/month)
5. **Team capabilities** (DIY tolerance, engineering bandwidth)

**Key Insight**: All scenarios show massive ROI (8-406×), indicating search is **high-value investment** regardless of platform choice. The question is not "Should we invest in search?" but "Which platform maximizes ROI for our specific scenario?"

---

## Scenario Comparison Matrix

### Quick Reference: Platform Recommendations by Scenario

| Scenario | Recommended Platform | Alternative | Budget | ROI (3-year) | Key Factor |
|----------|---------------------|-------------|--------|--------------|------------|
| **E-Commerce Catalog** | Algolia Grow/Premium | Typesense Business | $500-5K/month | 29-36× | Merchandising UI, analytics |
| **SaaS Documentation** | Algolia DocSearch (free) | Meilisearch Build | $0-100/month | ∞ (free) / 23× | Free for public docs |
| **Content/Media Site** | Meilisearch Pro | Typesense Business | $300-600/month | 29-30× | Full-text search, scale |
| **Enterprise Knowledge** | Coveo | Azure AI Search | $50K-500K/year | 120-406× | 100+ connectors, RBAC |
| **Marketplace Platform** | Algolia Premium | Typesense Enterprise | $5K-25K/month | 8-32× | Geo-search, personalization |
| **Mobile App Search** | Algolia Grow | Typesense Growth | $245-1K/month | 128-163× | Mobile SDKs, offline cache |

---

## Pattern Identification: Common Architectures

### Pattern 1: Instant Search Architecture (E-Commerce, Marketplace, Mobile)

**Requirements**: <50ms latency, real-time indexing, faceting, autocomplete

**Architecture**:
```
User Browser/App → InstantSearch UI → Search Platform (Algolia/Typesense/Meili)
                                            ↓
                                    Indexing Pipeline
                                            ↓
                              Primary Database (PostgreSQL/MongoDB)
```

**Best Platforms**:
1. **Algolia** (10-20ms, global CDN, best DX)
2. **Typesense** (10-20ms, predictable pricing, good DX)
3. **Meilisearch** (15-25ms, best open-source DX, hybrid search)

**Key Insight**: Only 3 platforms deliver <50ms consistently. If instant search required, no other options.

---

### Pattern 2: Full-Text Search Architecture (Content/Media, Documentation)

**Requirements**: <100ms acceptable, 1M+ documents, full-text relevance, faceting

**Architecture**:
```
User → Search UI → Search Platform (Meilisearch/Typesense/OpenSearch)
                        ↓
                  Indexing Scripts (cron/webhooks)
                        ↓
                   CMS (WordPress/Ghost/Docusaurus)
```

**Best Platforms**:
1. **Meilisearch** ($30-300/month, excellent DX, hybrid search)
2. **Typesense** ($20-600/month, predictable pricing, fast purge)
3. **AWS OpenSearch** ($500-2K/month, if need advanced analytics)

**Key Insight**: 50-100ms latency acceptable for content search. Budget platforms (Meilisearch/Typesense) deliver 90% of premium features at 10% cost.

---

### Pattern 3: Enterprise Unified Search Architecture (Knowledge Base)

**Requirements**: 100+ data sources, document-level security, SSO, ML relevance

**Architecture**:
```
Enterprise Portal → Unified Search (Coveo/Azure AI Search/OpenSearch)
                            ↓
                 Security Layer (RBAC, ACLs)
                            ↓
            Connectors (100+ sources: Confluence, SharePoint, Slack, etc.)
                            ↓
           Data Sources (Confluence, SharePoint, Google Drive, Salesforce, etc.)
```

**Best Platforms**:
1. **Coveo** ($50K-500K/year, 100+ native connectors, best ML)
2. **Azure AI Search** ($10K-60K/year, Azure-native, cognitive skills)
3. **AWS OpenSearch** ($15K-40K/year, AWS-native, DIY connectors)

**Key Insight**: Connector count is critical. Coveo saves 500-2,000 hours vs DIY (worth $50K-200K).

---

### Pattern 4: Geo-Search Architecture (Marketplace)

**Requirements**: Geo-radius queries, multi-index, personalization, quality ranking

**Architecture**:
```
Mobile/Web App → Search UI (Map + List) → Search Platform (Algolia/Elastic)
                                                ↓
                                    Multi-Index (Sellers + Listings)
                                                ↓
                                     Geo-Search (_geoloc field)
                                                ↓
                                 Personalization (ML ranking, user history)
```

**Best Platforms**:
1. **Algolia Premium** ($5K-25K/month, best geo-search + personalization)
2. **Typesense** ($600/month, strong geo-search, DIY personalization)
3. **Elasticsearch** ($2K-5K/month, custom ML, Learning to Rank)

**Key Insight**: Geo-search commodity (all platforms support). Differentiation in personalization (Algolia AI Ranking vs DIY).

---

### Pattern 5: Mobile-Optimized Architecture (iOS/Android Apps)

**Requirements**: <50ms latency, offline caching, battery efficiency, small SDK

**Architecture**:
```
Mobile App (iOS/Android) → Native SDK (Algolia/Typesense) → Search Platform
         ↓
   Offline Cache (SQLite/CoreData/Room, last 100-500 results)
         ↓
   Battery Optimization (debouncing, request batching, gzip)
```

**Best Platforms**:
1. **Algolia** (best mobile SDKs, InstantSearch Mobile, offline caching)
2. **Typesense** (good performance, community SDKs, DIY offline)
3. **Firebase + Algolia Hybrid** (best offline, basic + full-text search)

**Key Insight**: Mobile SDK quality matters. Algolia official SDKs save 80-160 hours vs community/DIY.

---

## Platform Recommendation Decision Tree

### Decision 1: Budget Filter

**Budget <$100/month**:
- **Free (public docs)**: Algolia DocSearch ($0)
- **Free (basic search)**: Algolia Free Tier ($0, 10K records, 10K searches)
- **Cheapest paid**: Typesense Hobby ($20/month) or Meilisearch Build ($30/month)

**Budget $100-500/month**:
- **Best DX**: Meilisearch Pro ($300/month)
- **Best price**: Typesense Growth ($120/month)
- **Best features**: Algolia Grow ($245/month)

**Budget $500-5K/month**:
- **E-commerce**: Algolia Grow/Premium ($500-5K/month)
- **Content/media**: Meilisearch Pro ($300/month) or AWS OpenSearch ($500-2K/month)
- **Marketplace**: Algolia Premium ($5K+/month)

**Budget $5K-50K/month**:
- **Enterprise search**: Azure AI Search ($1K-5K/month) or Algolia Premium ($5K-25K/month)
- **Large-scale**: AWS OpenSearch ($2K-10K/month) or Elasticsearch ($3K-10K/month)

**Budget $50K+/year**:
- **Fortune 500**: Coveo ($50K-500K/year, 100+ connectors, best ML)

---

### Decision 2: Latency Requirement

**<50ms required** (instant search UX):
- **Only options**: Algolia, Meilisearch, Typesense
- **Global <50ms**: Only Algolia (70+ PoPs)
- **Regional <50ms**: Meilisearch or Typesense (single/multi-region)

**50-100ms acceptable** (full-text search):
- **All platforms viable**: Meilisearch, Typesense, Algolia, OpenSearch, Azure AI Search

**100-500ms acceptable** (enterprise search):
- **All platforms viable**: Focus on connectors, security, ML relevance

---

### Decision 3: Scale Requirement

**<100K documents**:
- **All platforms viable**: Choose by DX, cost, features

**100K-1M documents**:
- **Recommended**: Meilisearch, Typesense, Algolia, Azure AI Search
- **Avoid**: Elasticsearch/OpenSearch (overkill, too complex for <1M docs)

**1M-10M documents**:
- **Recommended**: Algolia, Typesense, Elasticsearch, OpenSearch
- **Note**: Meilisearch 1M doc limit (Pro plan)

**10M+ documents**:
- **Recommended**: Algolia, Elasticsearch, OpenSearch
- **Proven at 1B+ docs**: Algolia, Elasticsearch (battle-tested)

**100M+ documents**:
- **Only options**: Elasticsearch, AWS OpenSearch (proven at 100B+ docs)

---

### Decision 4: Use Case Filter

**E-Commerce** → Algolia (merchandising UI) or Typesense (cost-conscious)

**SaaS Documentation** → Algolia DocSearch (free, public) or Meilisearch (private, $30/month)

**Content/Media Site** → Meilisearch ($300/month) or Typesense ($300/month)

**Enterprise Knowledge Base** → Coveo ($50K+/year, Fortune 500) or Azure AI Search ($10K-50K/year, mid-market)

**Marketplace Platform** → Algolia Premium ($5K-25K/month, personalization) or Typesense ($600/month, DIY)

**Mobile App** → Algolia ($245-1K/month, best mobile SDKs) or Typesense ($120/month, cost-conscious)

**Observability (Logs/Metrics)** → Elasticsearch or AWS OpenSearch (only options for log analytics)

---

## Critical Success Factors

### Factor 1: Total Cost of Ownership (License + Engineering)

**Insight**: Engineering time can exceed license costs. Cheap platforms can have higher TCO if high maintenance or missing features.

**Example**:
- **Algolia Grow**: $8,820 (license) + $22,000 (engineering) = **$30,820** (3-year)
- **Typesense**: $4,320 (license) + $62,000 (engineering, merchandising UI) = **$66,320** (3-year)
- **Winner**: Algolia (lower TCO despite higher license, due to merchandising UI)

**Action**: Always calculate TCO (license + engineering). Don't optimize license cost in isolation.

---

### Factor 2: Feature Gaps Drive Hidden Costs

**Common Feature Gaps**:
- **No merchandising UI**: Build admin panel (80-160 hours, $8K-16K)
- **No analytics**: Implement tracking (40-80 hours, $4K-8K) or use Mixpanel ($25-100/month)
- **No ML personalization**: DIY (200-400 hours, $20K-40K) or skip
- **DIY connectors**: 20 hours/connector (worth $2K-3K each)

**Example** (Meilisearch vs Algolia for e-commerce):
- **Meilisearch**: $300/month license, but need to build merchandising UI ($8K-16K) + analytics ($4K-8K)
- **Algolia**: $745/month license, but merchandising UI + analytics included
- **Break-even**: If merchandising UI used >20 hours/year, Algolia cheaper (lower TCO)

**Action**: Identify feature gaps before choosing platform. Factor DIY costs into TCO.

---

### Factor 3: Open-Source Maturity Eliminates Premium Necessity

**Finding**: Meilisearch/Typesense have reached production maturity, delivering 80-85% of Algolia features at 10% cost.

**Feature Parity Analysis**:
- **Core search** (typo tolerance, faceting, performance): 95% parity
- **Advanced features** (merchandising UI, analytics, ML personalization): 10-20% parity

**Implication**: Pay premium only for specific gaps (merchandising UI, analytics, ML, global CDN). Don't pay 10× more for 5% better core search.

**Example**:
- **Meilisearch Pro**: $300/month (1M docs, hybrid search, 15-25ms latency)
- **Algolia Grow Plus**: $1,485/month (1M docs, NeuralSearch, 10-20ms latency)
- **Premium**: 5× more expensive for 10ms faster latency + NeuralSearch (rarely justifies cost)

**Action**: Start with Meilisearch/Typesense. Upgrade to Algolia only when specific gaps justify 5-10× cost premium.

---

### Factor 4: AI/ML Features Are Now Table Stakes (2024-2025 Shift)

**Democratization**: Hybrid/semantic search went from luxury ($10K+/month, Algolia Enterprise) to commodity ($30/month, Meilisearch Build) in 2 years.

**Current Pricing** (hybrid search, keyword + semantic):
- **Meilisearch Build**: $30/month (included)
- **Typesense**: $20-600/month (semantic search included)
- **Azure AI Search**: $250-5K/month (semantic L2 reranking, pay-per-query)
- **Algolia Elevate**: $10K+/month (NeuralSearch, AI Ranking, full suite)

**Cost Comparison** (500K searches/month):
- **Meilisearch**: $300/month (hybrid) = **$3,600/year**
- **Algolia Elevate**: $10K-25K/month = **$120K-300K/year**
- **Premium**: 33-83× more expensive for same AI features

**Implication**: Don't pay Algolia premium solely for AI features. Use Meilisearch (hybrid) or Azure AI Search (semantic) for 95% of AI use cases.

**Exception**: Algolia Enterprise justified if need ML personalization (user-specific ranking, behavioral signals) + can measure revenue impact >$50K/year.

---

### Factor 5: Ecosystem Lock-In Is Acceptable If Already Committed

**AWS OpenSearch** (vs cloud-agnostic Elasticsearch):
- **Savings**: IAM (20h), CloudWatch (20h), S3 snapshots (10h), Bedrock RAG (40h) = 90h saved ($9K)
- **Lock-in cost**: Migration 2-4 weeks (80-160h, $8K-16K)
- **Net value**: Marginal ($-7K to $1K)
- **Decision**: Use if already AWS-heavy, avoid if multi-cloud or uncertain

**Azure AI Search** (vs cloud-agnostic):
- **Savings**: Azure AD (20h), Blob indexers (40h), OpenAI integration (40h), cognitive skills (80h) = 180h saved ($18K)
- **Lock-in cost**: Migration 3-6 weeks (120-240h, $12K-24K)
- **Net value**: Marginal to positive ($-6K to $6K)
- **Decision**: Use if already Azure-heavy

**Coveo** (vs DIY):
- **Savings**: 100+ connectors (500-2,000h), ML relevance (200-500h), analytics (100-200h) = 800-2,700h saved ($80K-270K)
- **Lock-in cost**: Migration 6-24 months (500-2,000h, $50K-200K)
- **Net value**: Positive ($30K-70K), but requires 3-5 years to break even
- **Decision**: Only if budget >$50K/year and need 100+ connectors

**Action**: Embrace lock-in if integration value > migration risk. Avoid if multi-cloud or high churn risk.

---

### Factor 6: Search Is High-Value Investment (8-406× ROI)

**ROI by Scenario** (3-year):
- **E-Commerce**: 29-36× ROI (conversion lift from instant search + merchandising)
- **SaaS Docs**: ∞ (free, Algolia DocSearch) or 23× (Meilisearch, productivity savings)
- **Content/Media**: 29-30× ROI (engagement lift, ad revenue increase)
- **Enterprise Knowledge**: 120-406× ROI (massive productivity gains, 10K employees)
- **Marketplace**: 8-32× ROI (conversion lift from geo-search + personalization)
- **Mobile App**: 128-163× ROI (engagement + conversion lift from instant search)

**Key Insight**: All scenarios show massive ROI. Even "expensive" platforms (Algolia $30K-400K, Coveo $650K) deliver 8-163× ROI.

**Implication**: Search is not cost center, it's revenue/productivity driver. Focus on maximizing value (conversion, engagement, productivity), not minimizing license cost.

**Action**: Calculate ROI for your scenario. If ROI >10×, invest in search. Choose platform by max value, not min cost.

---

## Implementation Best Practices

### Practice 1: Start Small, Scale Gradually

**Phased Approach** (4-6 weeks):
1. **Week 1**: POC with S2 finalist platform (index 10K docs, test latency/relevance)
2. **Week 2**: Build MVP search UI (basic search box + results list, no facets)
3. **Week 3**: Soft launch (10% traffic, A/B test new vs old search)
4. **Week 4**: Ramp up (50% traffic, monitor performance, fix bugs)
5. **Weeks 5-6**: Full launch (100% traffic, decommission old search)

**Avoid**: Big-bang launch (risk too high, can't roll back easily)

---

### Practice 2: Measure Before & After (A/B Testing)

**Key Metrics**:
- **Engagement**: Search sessions / total sessions (target 20-40%)
- **CTR**: Clicked results / searches (target 60-80%)
- **Conversion**: Purchases from search / total purchases (target 40-60%)
- **Revenue**: GMV from search / total GMV (target 50-70%)
- **No-results rate**: No-results queries / total queries (target <5%)

**A/B Test** (10-50% traffic for 2-4 weeks):
- **Control**: Old search (baseline metrics)
- **Treatment**: New search (measure improvement)
- **Statistical significance**: 95% confidence, >1,000 conversions/variant

**Action**: Always measure before/after. If no improvement, investigate (relevance tuning, UI/UX, ranking formula).

---

### Practice 3: Relevance Tuning Is Ongoing (Not One-Time)

**Continuous Improvement**:
- **Monitor**: No-results queries (fix with synonyms, spelling corrections)
- **Monitor**: Low-CTR queries (tune ranking, boost relevant results)
- **Monitor**: High-exit queries (users leave after search, poor results quality)
- **Tune**: Ranking formula (weekly/monthly, A/B test changes)
- **Tune**: Synonyms (add 10-50/week based on user queries)
- **Tune**: Business rules (seasonal boosting, inventory management)

**Time Investment**: 5-20 hours/month (ongoing)

**Action**: Allocate 1-2 engineers for search quality (ongoing tuning, not set-and-forget).

---

### Practice 4: Index Freshness Matters

**Update Frequency by Use Case**:
- **E-commerce**: Real-time (inventory changes, price updates, <10s delay)
- **Documentation**: Hourly (docs update 1-10×/day, <1h delay acceptable)
- **Content/media**: 15-60 minutes (news articles, <15m for breaking news)
- **Enterprise knowledge**: Hourly (Confluence/SharePoint updates, <1h acceptable)
- **Marketplace**: Real-time (listings, seller profiles, <10s delay)
- **Mobile app**: Real-time (user profiles, posts, <10s delay)

**Implementation**:
- **Real-time**: Webhooks or app-level hooks (on create/update, push to search index)
- **Scheduled**: Cron jobs (full reindex daily, incremental hourly)

**Action**: Choose update frequency by use case. Real-time adds complexity (webhooks, error handling), but critical for e-commerce/marketplace.

---

## Top 3 Implementation Insights

### Insight 1: Default to Open-Source, Upgrade Only When Justified

**Decision Framework**:

**Start with**: Meilisearch ($30-300/month) or Typesense ($20-600/month)
- 80-85% feature parity with Algolia
- 10% of Algolia cost
- Excellent performance (<50ms)
- Hybrid search included (Meilisearch)

**Upgrade to Algolia when**:
- Need global CDN (<50ms worldwide, 70+ PoPs)
- Need merchandising UI (saves 80-160 hours, $8K-16K)
- Need built-in analytics (saves 40-80 hours + Mixpanel cost)
- Search is revenue driver (5-10% conversion improvement justifies 10× cost)

**Upgrade to Coveo when**:
- Need 100+ connectors (saves 500-2,000 hours, $50K-200K)
- Need best ML relevance (20-40% CTR improvement, Coveo claims)
- Budget >$50K/year (below minimum, Coveo not available)

**ROI Break-Even**:
- **Algolia vs Meilisearch**: Costs $4K-10K/year more (license). Saves $4K-16K (merchandising UI). Break-even if merchandising used >20 hours/year.
- **Coveo vs OpenSearch**: Costs $750K more (3-year). Saves 500-2,000 hours (connectors). Break-even if connectors save >7,500 hours (unlikely, only for 50+ connectors).

---

### Insight 2: Latency <50ms Is a Hard Filter (Only 3 Options)

**Finding**: Only Algolia, Meilisearch, Typesense deliver <50ms P95 consistently. All other platforms 50-200ms.

**Implication**:
- **If <50ms required** (e-commerce instant search, mobile apps, real-time UX) → Only 3 options
- **Global <50ms** → Only Algolia (70+ PoPs, automatic)
- **Regional <50ms** → Meilisearch or Typesense (deploy in primary region)

**If 50-200ms acceptable** (content search, documentation, enterprise knowledge) → All platforms viable

**Action**: Clarify latency requirement early. If <50ms required, eliminates 4 of 7 platforms immediately.

---

### Insight 3: Total Cost of Ownership Includes Engineering Time

**TCO Formula**: License + Infrastructure + Engineering (setup + maintenance + features)

**Example** (e-commerce, 500K searches/month, 3-year):

**Algolia Grow**:
- License: $745/month × 36 = $26,820
- Setup: 40h × $100 = $4,000
- Maintenance: 5h/month × 36 × $100 = $18,000
- Merchandising: 0h (built-in)
- **Total TCO**: $48,820

**Typesense Business**:
- License: $300/month × 36 = $10,800
- Setup: 80h × $100 = $8,000
- Maintenance: 10h/month × 36 × $100 = $36,000
- Merchandising: 120h × $100 = $12,000 (DIY)
- **Total TCO**: $66,800

**Winner**: Algolia (lower TCO despite higher license, due to merchandising UI)

**Key Insight**: Cheap platforms can have higher TCO if high maintenance or missing features. Always calculate full TCO, not just license cost.

**Action**: Use this formula for every platform evaluation. Factor engineering time (setup, maintenance, feature development) into decision.

---

## Scenario-Specific Quick Wins

### E-Commerce: Merchandising ROI Calculator

**Baseline** (no merchandising):
- Browse conversion: 3-5%
- Search conversion: 8-10% (basic keyword search)

**With merchandising** (Algolia or DIY):
- Search conversion: 15-20% (2× improvement from boosting, pinning, seasonal rules)
- **Incremental conversion**: 15% - 8% = 7 percentage points
- **Revenue impact**: 40% of GMV from search × 7% lift = **2.8% of total GMV**
- **For $50M GMV**: 2.8% × $50M = **$1.4M incremental revenue/year**

**Cost**:
- Algolia (built-in): Included in $745-5K/month license
- DIY (Typesense/Meilisearch): 120h @ $100/hour = $12K (one-time) + 10h/month maintenance

**ROI**: If GMV >$5M, merchandising pays for itself (even DIY).

---

### SaaS Docs: Free Tier Optimization

**Strategy**: Use Algolia DocSearch (free) for public docs, Meilisearch ($30/month) for private docs.

**Cost Savings**:
- Algolia DocSearch (public): **$0/year** vs Algolia paid $2,940/year (12× $245/month)
- Meilisearch (private): **$360/year** vs Algolia paid $2,940/year (8× savings)

**Eligibility**: Apply at docsearch.algolia.com/apply (1-2 weeks approval, public docs only).

**If rejected**: Use Meilisearch ($30/month) instead of paying Algolia $245/month (8× cheaper).

---

### Enterprise: Connector ROI Calculator

**DIY connectors**: 20 hours/connector @ $150/hour = **$3,000/connector**
- 10 connectors: $30K
- 50 connectors: $150K
- 100 connectors: $300K

**Coveo** (100+ connectors included): $50K-500K/year

**Break-even**:
- If need <15 connectors: DIY cheaper (OpenSearch $18K/year + $45K connectors = $63K < Coveo $150K)
- If need 20-50 connectors: Coveo comparable ($150K DIY vs Coveo $150-200K)
- If need 50+ connectors: Coveo cheaper (saves 100-200 hours/year ongoing maintenance)

**Action**: Count required connectors before choosing platform. If <20, DIY viable. If >50, Coveo justified.

---

## Final Decision Framework

### Step 1: Filter by Budget
- <$100/month → Typesense, Meilisearch, or Algolia Free
- $100-500/month → Meilisearch, Typesense, or Algolia Grow
- $500-5K/month → Algolia, Azure AI Search, or AWS OpenSearch
- $5K-50K/month → Algolia Premium, Azure AI Search, or Coveo
- $50K+/year → Coveo

### Step 2: Filter by Latency
- <50ms required → Algolia, Meilisearch, or Typesense (only options)
- 50-200ms acceptable → All platforms viable

### Step 3: Filter by Scale
- <1M docs → All platforms viable
- 1M-10M docs → Algolia, Typesense, Elasticsearch, OpenSearch
- 10M+ docs → Algolia, Elasticsearch, OpenSearch

### Step 4: Match Use Case
- E-commerce → Algolia (merchandising) or Typesense (cost)
- SaaS docs → Algolia DocSearch (free) or Meilisearch ($30)
- Content/media → Meilisearch or Typesense
- Enterprise → Coveo (Fortune 500) or Azure AI Search (mid-market)
- Marketplace → Algolia (personalization) or Typesense (cost)
- Mobile app → Algolia (SDKs) or Typesense (cost)

### Step 5: Calculate TCO & ROI
- TCO = License + Engineering (setup + maintenance + features)
- ROI = (Revenue/Productivity Gain - TCO) / TCO
- Choose platform with highest ROI (not lowest license cost)

---

**Last Updated**: November 14, 2025
**Research Stage**: S3 Need-Driven (Scenario-Based Evaluation)
**Total Scenarios**: 6 (E-commerce, SaaS Docs, Content, Enterprise, Marketplace, Mobile)
**Key Finding**: No one-size-fits-all. Platform choice is scenario-dependent, driven by use case, budget, scale, and team capabilities.
**All Scenarios ROI**: 8-406× (3-year), indicating search is high-value investment regardless of platform choice.
